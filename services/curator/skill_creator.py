"""Skill creation from session experience.

After a complex multi-step session, analyze what was done and create/update
a SKILL.md capturing the approach for future reuse.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from typing import Optional

logger = logging.getLogger(__name__)

# Minimum tool calls to consider a session "complex" enough for skill creation
MIN_TOOL_CALLS_FOR_SKILL = 8

# Minimum confidence for an auto-created skill — low because it's unverified
AUTO_CREATED_CONFIDENCE = 0.3


async def maybe_create_skill_from_session(
    owner: str,
    session_id: str,
    message_count: int,
    tool_call_count: int,
    conversation_summary: str,
    skills_manager,
) -> Optional[str]:
    """Analyze a completed session and create a SKILL.md if warranted.

    Returns the skill name if created, None otherwise.

    Triggers when:
    - Tool calls >= MIN_TOOL_CALLS_FOR_SKILL (complex session)
    - The conversation has a clear problem-solution arc
    """
    if tool_call_count < MIN_TOOL_CALLS_FOR_SKILL:
        logger.debug(
            "skill_creator: session %s only had %d tool calls (min %d)",
            session_id, tool_call_count, MIN_TOOL_CALLS_FOR_SKILL,
        )
        return None

    if not conversation_summary or len(conversation_summary) < 100:
        logger.debug("skill_creator: session %s summary too short", session_id)
        return None

    # Use the LLM to analyze and generate a SKILL.md
    skill_data = await _analyze_session(conversation_summary, owner)
    if not skill_data:
        return None

    name = skill_data.get("name", "").strip()
    description = skill_data.get("description", "").strip()
    procedure = skill_data.get("procedure", "").strip()
    when_to_use = skill_data.get("when_to_use", "").strip()
    pitfalls = skill_data.get("pitfalls", "").strip()
    verification = skill_data.get("verification", "").strip()
    tags = skill_data.get("tags", [])

    if not name or not procedure:
        logger.debug("skill_creator: LLM returned incomplete skill data")
        return None

    # Check if skill already exists — if so, skip (refinement is separate)
    existing = skills_manager.load(owner=owner, name=name)
    if existing:
        logger.info("skill_creator: skill '%s' already exists, skipping", name)
        return name

    # Build the SKILL.md content
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    lines = ["---"]
    lines.append(f"name: {name}")
    lines.append(f"description: {description}")
    lines.append(f"version: 1.0.0")
    lines.append(f"category: learned")
    lines.append(f"tags: [{', '.join(tags)}]")
    lines.append(f"status: draft")
    lines.append(f"confidence: {AUTO_CREATED_CONFIDENCE}")
    lines.append(f"source: learned")
    lines.append(f"created: {now}")
    lines.append(f"teacher_model: nexus-agent")
    lines.append("---")
    lines.append("")
    if when_to_use:
        lines.append("## When to Use")
        lines.append(when_to_use)
        lines.append("")
    if procedure:
        lines.append("## Procedure")
        lines.append(procedure)
        lines.append("")
    if pitfalls:
        lines.append("## Pitfalls")
        lines.append(pitfalls)
        lines.append("")
    if verification:
        lines.append("## Verification")
        lines.append(verification)

    body = "\n".join(lines)

    try:
        skills_manager.add(
            owner=owner,
            name=name,
            category="learned",
            body=body,
            tags=tags,
        )
        logger.info("skill_creator: created skill '%s' from session %s", name, session_id)
        return name
    except Exception as e:
        logger.error("skill_creator: failed to save skill '%s': %s", name, e)
        return None


async def _analyze_session(conversation_summary: str, owner: str) -> Optional[dict]:
    """Ask the LLM to analyze a session and propose a SKILL.md.

    Returns a dict with keys: name, description, when_to_use, procedure,
    pitfalls, verification, tags.
    """
    from src.task_endpoint import resolve_task_candidates

    candidates = resolve_task_candidates(owner=owner)
    if not candidates:
        logger.warning("skill_creator: no model configured for analysis")
        return None

    url, model, headers = candidates[0]

    prompt = (
        "You are a skill extraction expert. Analyze the following conversation "
        "summary from an AI assistant session. Identify if there is a reusable "
        "procedure or skill that should be captured as a SKILL.md for future use.\n\n"
        "Only create a skill if the session demonstrates a clear, repeatable "
        "multi-step process — not a simple Q&A.\n\n"
        "Return your analysis as a JSON object with these fields:\n"
        "- name: short kebab-case identifier (e.g. 'deploy-to-railway')\n"
        "- description: one-line summary (max 120 chars)\n"
        "- when_to_use: plain English trigger conditions\n"
        "- procedure: numbered steps (markdown)\n"
        "- pitfalls: common failure modes (markdown list)\n"
        "- verification: how to confirm success (markdown list)\n"
        "- tags: list of category tags like ['dev', 'deploy']\n"
        "- should_create: true/false — whether a skill is warranted\n\n"
        "If no skill is warranted, return {\"should_create\": false}.\n\n"
        f"Conversation summary:\n\n{conversation_summary}"
    )

    import httpx

    try:
        async with httpx.AsyncClient(timeout=60) as client:
            resp = await client.post(
                url,
                headers=headers,
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 2000,
                    "temperature": 0.3,
                },
            )
            if resp.status_code >= 400:
                logger.warning("skill_creator: LLM returned HTTP %d", resp.status_code)
                return None

            text = resp.json()["choices"][0]["message"]["content"]

        # Extract JSON from response (handle markdown-wrapped JSON)
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()

        data = json.loads(text)
        if not data.get("should_create"):
            return None
        return data
    except Exception as e:
        logger.warning("skill_creator: LLM analysis failed: %s", e)
        return None
