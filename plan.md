# Nexus — Master Plan

> **Mission:** The only self-hosted AI workspace that lives inside your digital life.
> **Motto:** *Nexus knows your email, calendar, documents, and research — because they all live in one place.*

---

## 🏆 The Unfair Advantage

| What Nexus has | Competitors |
|---|---|
| Email (IMAP/SMTP) | **No one else has this** |
| Calendar + CalDAV | **No one else has this** |
| Documents Editor | **No one else has this** |
| Deep Research | **No one else has this** |
| Model Serving (Cookbook) | **Only Jan** |
| Chat + Agents + MCP | Everyone |
| All in one process | **No one else has this** |

**The strategy is not to catch up. The strategy is to build what no one else can** — cross-domain AI that reads your email, knows your calendar, drafts documents, and researches topics, all in one private platform.

---

## 🔴 PHASE 1 — Sprint 1-2: Autonomous Core

These features leverage Nexus's unique data surface. No competitor can replicate them without building email, calendar, documents, and research from scratch.

### 1. 🧠 Morning Briefing Agent
*"Every morning, Nexus briefs me on what I need to know."*

- **Schedule:** Configurable time (default 7am)
- **Data sources:** Unread priority emails, today's calendar events, overdue tasks, relevant news via Deep Research
- **Output:** Personalized Markdown briefing saved as a Note or sent via email
- **Implementation:** `services/briefing/` module, cron scheduler in `routes/task_routes.py`

### 2. 📧 Smart Email Assistant
*"Nexus reads my email, understands it, and acts on it."*

- Auto-categorize (work, personal, spam, newsletter)
- Flag urgent emails (sender, subject, content analysis)
- Suggest reply drafts (one-click apply)
- **Email → Task:** "Can you review by Friday?" → creates task with due date
- **Email → Calendar:** "Meet Tuesday 3pm" → creates calendar event
- Daily digest: "23 emails, here are the 4 that matter"
- **Implementation:** `services/email_assistant/` module

### 3. 🔗 Cross-Domain Action Engine
*"Take what happens in one domain and act in another."*

| Trigger | Action |
|---|---|
| Email received | Create task, schedule event, save document |
| Meeting approaching | Auto-research attendees/topic |
| Task overdue | Send follow-up email |
| Meeting ended | Create summary note |
| Document updated | Notify via email |

- **Implementation:** Cross-domain registry in `src/agent_loop.py`, routing between existing domain handlers

---

## 🟡 PHASE 2 — Sprint 3-5: Match + Exceed

### 4. ⚡ AI-Native Visual Workflow Builder
*Beat Dify and n8n by letting users describe workflows in plain language.*

- User types: *"Every morning, check email for urgent messages, search web for competitor news, and save a briefing as a document."*
- AI generates the workflow JSON automatically
- Visual canvas for tweaking (`static/js/workflow.js`)
- Cron-based execution engine (`services/workflow/`)

### 5. 🔌 Plugin Marketplace
*Beat Open WebUI's community sharing.*

- Format: `plugin.json` manifest (directory with SKILL.md + optional Python/frontend)
- One-click install: paste GitHub URL → Nexus clones + registers
- "Browse Nexus Community" button in Skills UI

### 6. 📊 Usage Analytics + RBAC
*Match Open WebUI and Dify for teams.*

- Token usage tracking (per-user, per-model, per-session)
- Admin dashboard (charts, costs, active users)
- Role-based access (admin, power user, viewer)
- Group-based model/tool permissions

---

## 🔵 PHASE 3 — Sprint 6+: The Unassailable Moat

### 7. 🏢 Multi-Agent Teams
*Beyond LobeHub — agents with real data to act on.*

- Specialized agents: Email Agent, Research Agent, Calendar Agent, Writing Agent
- Agent collaboration: Research Agent finds info → Writing Agent drafts → Email Agent sends
- Scheduled agents (cron, event-driven, on-demand)
- Preference learning over time

### 8. 🖥️ Desktop Native App (Tauri)
*Build on existing launcher.py groundwork.*

- System tray with unread counts
- Native notifications
- Global hotkey (quick search/action)
- Offline-first with local SQLite
- Auto-start on boot

### 9. 🌍 i18n / Multilingual
*Match Dify and Open WebUI for international users.*

- Extract all UI strings to JSON locale files
- Community-contributed translations
- Language selector in settings

---

## 📋 Current Implementation Status

| Feature | Status | Details |
|---|---|---|
| Chat + Agents | ✅ Done | `src/agent_loop.py`, tool registry, MCP |
| Email | ✅ Done | IMAP/SMTP, triage, summaries, drafts |
| Calendar | ✅ Done | CalDAV, recurring events, reminders |
| Documents | ✅ Done | Markdown/HTML/CSV editor with AI edits |
| Deep Research | ✅ Done | Multi-step web research with citations |
| Cookbook | ✅ Done | Model recommendations + serving |
| RAG | ✅ Done | ChromaDB, fastembed, semantic memory |
| Web Fetch (crawl4ai) | ✅ Done | JS rendering, markdown output (optional) |
| Skills (SKILL.md) | ✅ Done | Agent skill registry |
| MCP Servers | ✅ Done | Email, image-gen, memory, RAG |
| Copilot Instructions | ✅ Done | `.github/copilot-instructions.md` |
| Token Prefix (`nx_`) | ✅ Done | `ody_` → `nx_` rebrand |
| **Morning Briefing** | 📝 **Next** | Phase 1 priority |
| **Email Assistant** | 📝 **Next** | Phase 1 priority |
| **Cross-Domain Engine** | 📝 **Next** | Phase 1 priority |
| Visual Workflow | ❌ Planned | Phase 2 |
| Plugin Marketplace | ❌ Planned | Phase 2 |
| Usage Analytics | ❌ Planned | Phase 2 |
| RBAC + Groups | ❌ Planned | Phase 2 |
| Multi-Agent Teams | ❌ Planned | Phase 3 |
| Desktop App | ❌ Planned | Phase 3 |
| i18n | ❌ Planned | Phase 3 |

---

## 🏗️ Architecture Principles

1. **Everything in one process** — FastAPI serves API + SPA. No microservices. Simpler deployment.
2. **Local-first, private by default** — SQLite, on-device embeddings, local auth. Cloud is optional opt-in.
3. **Graceful degradation** — Optional deps (crawl4ai, PyMuPDF, markitdown) fall back with clear messages.
4. **Cross-domain from day one** — All data (email, calendar, docs, tasks) lives in the same database. The AI sees everything.
5. **Skill-based agent system** — SKILL.md is the unit of agent capability. Plugin marketplace extends this.
6. **Self-contained** — Single Docker image or `pip install`. No external dependencies beyond a database.

---

## 🚀 Quick Start for Developers

```bash
# Run locally
python -m uvicorn app:app --host 127.0.0.1 --port 7000

# Run tests (fast lane)
python -m pytest -m "not slow"

# Run all tests
python -m pytest

# Docker
docker compose up -d --build

# Install optional features
pip install crawl4ai    # JS-rendered web fetching
playwright install chromium
```

---

*See [docs/feature-research.md](docs/feature-research.md) for the full competitive analysis.*
