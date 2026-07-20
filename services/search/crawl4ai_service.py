"""crawl4ai-powered web fetch service.

Wraps crawl4ai's AsyncWebCrawler as a drop-in upgrade for
services/search/content.py's fetch_webpage_content().

Benefits over plain httpx+BeautifulSoup:
- JavaScript rendering (handles SPAs, dynamic content)
- Anti-detection (stealth mode, user-agent rotation)
- Clean markdown output (LLM-friendly)
- Content filtering (BM25, fit markdown)
- Configurable extraction strategies

Architecture:
- Lazy-init single shared AsyncWebCrawler instance
- Falls back to the original httpx-based fetch on failure
- Respects existing Nexus cache and size limits
"""

from __future__ import annotations

import asyncio
import logging
import os
from typing import Optional

from src.constants import WEB_FETCH_SOFT_MAX_BYTES, WEB_FETCH_HARD_MAX_BYTES

logger = logging.getLogger(__name__)

# Global lazy singleton — one browser context per process
_crawler_instance: Optional["AsyncWebCrawler"] = None
_crawler_lock = asyncio.Lock()


async def get_crawler() -> "AsyncWebCrawler":
    """Get or create the shared AsyncWebCrawler instance."""
    global _crawler_instance
    if _crawler_instance is not None:
        return _crawler_instance

    async with _crawler_lock:
        if _crawler_instance is not None:
            return _crawler_instance

        try:
            from crawl4ai import AsyncWebCrawler, BrowserConfig

            # Lightweight headless config — no GPU, no extra features
            browser_cfg = BrowserConfig(
                browser_type="chromium",
                headless=True,
                verbose=False,
                light_mode=True,
                text_mode=False,
                ignore_https_errors=True,
                java_script_enabled=True,
                viewport_width=1080,
                viewport_height=600,
            )
            _crawler_instance = AsyncWebCrawler(config=browser_cfg)
            await _crawler_instance.start()
            logger.info("crawl4ai AsyncWebCrawler started (shared instance)")
        except Exception as e:
            logger.warning("crawl4ai init failed (%s); falling back to httpx", e)
            _crawler_instance = None  # sentinel — don't retry every call

        return _crawler_instance


async def _crawl4ai_fetch(
    url: str,
    max_bytes: Optional[int] = None,
    timeout: int = 30,
) -> dict:
    """Fetch a URL using crawl4ai's AsyncWebCrawler.

    Returns a dict with keys matching the existing fetch_webpage_content()
    contract so callers can swap implementations transparently:

        {"content": str, "title": str, "error": None|str,
         "truncated": bool, "fetched_bytes": int, "total_bytes": int|None}

    When crawl4ai cannot handle the URL (init failure, timeout, etc.) the
    caller should fall back to the httpx-based fetcher.
    """
    from crawl4ai import CrawlerRunConfig

    crawler = await get_crawler()
    if crawler is None:
        return {"error": "crawl4ai not available", "content": "", "title": "",
                "truncated": False, "fetched_bytes": 0, "total_bytes": None}

    # Build a sensible run config — prefer clean markdown output
    run_cfg = CrawlerRunConfig(
        verbose=False,
        page_timeout=timeout * 1000,         # ms
        wait_until="domcontentloaded",
        delay_before_return_html=0.1,
        remove_overlay_elements=True,
        remove_consent_popups=True,
        exclude_social_media_domains=True,
        exclude_external_images=True,
        scan_full_page=False,
        simulate_user=False,
        magic=False,
        override_navigator=False,
        only_text=False,
    )

    try:
        result = await asyncio.wait_for(
            crawler.arun(url, config=run_cfg),
            timeout=timeout + 5,
        )
    except asyncio.TimeoutError:
        return {"error": f"crawl4ai timed out ({timeout}s)", "content": "", "title": "",
                "truncated": False, "fetched_bytes": 0, "total_bytes": None}
    except Exception as e:
        return {"error": f"crawl4ai: {e}", "content": "", "title": "",
                "truncated": False, "fetched_bytes": 0, "total_bytes": None}

    if result is None:
        return {"error": "crawl4ai returned no result", "content": "", "title": "",
                "truncated": False, "fetched_bytes": 0, "total_bytes": None}

    # Extract markdown — the API returns a MarkdownGenerationResult object
    # with nested fields: raw_markdown, fit_markdown, markdown_with_citations
    md_obj = result.markdown
    if md_obj is not None and not isinstance(md_obj, str):
        body = (getattr(md_obj, "fit_markdown", None)
                or getattr(md_obj, "raw_markdown", None)
                or getattr(md_obj, "markdown_with_citations", None)
                or "").strip()
    elif isinstance(md_obj, str):
        body = md_obj.strip()
    else:
        body = ""
    title = getattr(result, "title", "") or ""

    if not body:
        return {"error": "crawl4ai: no readable content extracted", "content": "", "title": title,
                "truncated": False, "fetched_bytes": 0, "total_bytes": None}

    # Enforce size limits (matching WEB_FETCH_HARD_MAX_BYTES contract)
    raw_len = len(body)
    effective_max = min(max_bytes or WEB_FETCH_SOFT_MAX_BYTES, WEB_FETCH_HARD_MAX_BYTES)
    truncated = raw_len > effective_max
    if truncated:
        body = body[:effective_max]

    return {
        "content": body,
        "title": title,
        "error": None,
        "truncated": truncated,
        "fetched_bytes": min(raw_len, effective_max),
        "total_bytes": raw_len if truncated else None,
    }


async def fetch_with_crawl4ai_fallback(
    url: str,
    max_bytes: Optional[int] = None,
    timeout: int = 30,
) -> dict:
    """Try crawl4ai first, fall back to the existing httpx-based fetcher."""
    # Try crawl4ai first
    result = await _crawl4ai_fetch(url, max_bytes=max_bytes, timeout=timeout)
    if result.get("error") is None and result.get("content"):
        logger.debug("crawl4ai fetched %s (%d bytes)", url, len(result["content"]))
        return result

    # Fall back to original fetcher
    from services.search.content import fetch_webpage_content as _orig_fetch

    logger.info("crawl4ai fetch failed for %s (%s); falling back to httpx", url, result.get("error"))
    kwargs = {"timeout": timeout}
    if max_bytes is not None:
        kwargs["max_bytes"] = max_bytes
    try:
        import inspect
        sig = inspect.signature(_orig_fetch)
        if "max_bytes" not in sig.parameters:
            kwargs.pop("max_bytes", None)
    except (TypeError, ValueError):
        pass
    return _orig_fetch(url, **kwargs)
