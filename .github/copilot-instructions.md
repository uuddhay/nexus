# Nexus — Copilot Instructions

## Project Overview

Nexus is a self-hosted AI workspace for chat, agents, research, documents, email, notes, calendar, and local model workflows. It runs as a FastAPI Python backend with a vanilla JS/HTML/CSS frontend (no framework).

## Key Architecture

- **Backend**: FastAPI (Python 3.11+) — `app.py` is the entrypoint, routes live in `routes/`, core logic in `src/`, services in `services/`
- **Frontend**: Vanilla JS (ES modules) in `static/js/`, CSS in `static/style.css`, HTML in `static/index.html`
- **Database**: SQLAlchemy + SQLite by default (`core/database.py`)
- **Auth**: bcrypt-based with session management (`core/auth.py`)
- **Config**: Environment variables + `src/constants.py` (single source of truth)

## Directory Layout

| Path | Purpose |
|---|---|
| `app.py` | FastAPI app entrypoint, middleware, route mounting |
| `routes/` | HTTP route handlers (one file per feature area) |
| `src/` | Core business logic (LLM, agents, tools, embeddings) |
| `core/` | Shim re-exporting `src.constants`; `database.py`, `auth.py` |
| `services/` | Backend service layers (research, memory, search, hwfit) |
| `static/` | Frontend assets (JS, CSS, fonts, images) |
| `mcp_servers/` | MCP servers (email, image-gen, memory, RAG) |
| `scripts/` | CLI tools (nexus-* symlinks) |
| `data/` | Runtime data directory (not checked in) |
| `integrations/` | Claude Code and Codex agent skill bundles |
| `tests/` | pytest test suite (see tests/README.md) |
| `docs/` | Documentation and landing page |

## Coding Conventions

- **Python**: Type hints required on all function signatures. Use `from __future__ import annotations` in new files.
- **Logging**: Use `logging.getLogger(__name__)` — never `print()`.
- **Error handling**: Custom exceptions in `core/exceptions.py`. Handle in route layer.
- **DB access**: Use SQLAlchemy sessions from `core.database.SessionLocal`.
- **Config**: All constants/env vars in `src/constants.py`. Use `os.getenv()` with sensible defaults.
- **Routes**: Each route file registers a sub‑FastAPI router mounted in `app.py`. Keep route handlers thin — delegate to `src/` or `services/`.
- **Frontend**: Vanilla JS without frameworks. CSS custom properties for theming (`static/style.css`). The `static/index.html` SPA loads JS modules dynamically.

## Key Design Decisions

1. **Self-contained**: Single Python process serving both API + SPA frontend
2. **Local-first**: SQLite default, on-device embeddings (fastembed), local-only auth
3. **Agent system**: Tool-calling loop in `src/agent_loop.py` with skill registry (SKILL.md format)
4. **MCP**: Built-in MCP servers in `mcp_servers/` for email, image gen, memory, RAG
5. **Cookbook**: Model download/serve/recommend engine in `services/hwfit/`
6. **Scoped agent API**: `/api/codex/*` endpoints are the canonical scope-gated API for all agent integrations (Claude, Codex, etc.)

## Test Conventions

- pytest with asyncio (`pytest-asyncio`)
- Tests in `tests/` — see `tests/README.md` and `tests/_taxonomy.py` for markers
- Fast lane: `python -m pytest -m "not slow"`
- Full suite: `python -m pytest`

## Common Commands

```bash
# Run locally
python -m uvicorn app:app --host 127.0.0.1 --port 7000

# First-time setup
python setup.py

# Run tests
python -m pytest
python -m pytest -m "not slow"  # fast lane

# Docker
docker compose up -d --build
```
