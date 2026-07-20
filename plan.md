# Nexus — Master Plan

> **Mission:** The only self-hosted AI workspace that lives inside your digital life.
> **Motto:** *Nexus knows your email, calendar, documents, and research — because they all live in one place.*

---

## 📊 Honest Competitive Assessment

### Where Nexus Wins (No Competitor Has This)

| Domain | Nexus | Hermes Agent | Open WebUI | Dify | Jan |
|---|---|---|---|---|---|
| Email (IMAP/SMTP) | **✅** | ❌ | ❌ | ❌ | ❌ |
| Calendar + CalDAV | **✅** | ❌ | ❌ | ❌ | ❌ |
| Documents Editor | **✅** | ❌ | ❌ | ❌ | ❌ |
| Deep Research | **✅** | ❌ | ❌ | ❌ | ❌ |
| Model Serving | **✅** | ❌ | ❌ | ❌ | ✅ |
| Web UI (SPA) | **✅** | ❌ (CLI only) | ✅ | ✅ | ❌ (Desktop) |

### Where Hermes Agent Leads (Nexus Must Catch Up)

| Capability | Hermes Agent | Nexus | Impact |
|---|---|---|---|
| **Self-improving skills** | ✅ Creates + improves skills autonomously | ❌ Static SKILL.md only | **High** — agent gets smarter over time |
| **Messaging gateway** | ✅ 20+ platforms (Telegram, Discord, WhatsApp, Signal, etc.) | ❌ Web-only | **High** — reach users where they live |
| **Sub-agent delegation** | ✅ Spawn parallel sub-agents | ❌ Single agent loop | **High** — parallel work |
| **Cron scheduling** | ✅ Natural-language cron with platform delivery | ⚠️ Basic task scheduling | **Medium** — automations |
| **Session search (FTS5)** | ✅ Full-text across all past conversations | ❌ No cross-session search | **Medium** — recall |
| **Code execution sandbox** | ✅ Sandboxed Python | ❌ Shell only | **Medium** — safe code run |
| **Browser automation** | ✅ Chromium automation | ❌ Not available | **Medium** — web tasks |
| **TUI/CLI interface** | ✅ Full terminal UI | ❌ Web-only | **Medium** — power users |
| **Context files** | ✅ Project context injection | ❌ Not available | **Medium** — focused work |
| **Voice mode** | ✅ Real-time voice in CLI/Telegram/Discord | ⚠️ Basic TTS/STT | **Low-Medium** |
| **Terminal backends** | ✅ 6 (local, Docker, SSH, Modal, Daytona, Singularity) | ⚠️ Local only | **Low** — niche |

### Where Competitors Win: The Agent/Coding Tools Landscape

| Project | Type | Key Capabilities Nexus Lacks | Nexus Opportunity |
|---|---|---|---|
| **Claude Code** | CLI coding agent | Plugin system (commands/agents/hooks/skills), 7-phase feature workflow, PR review toolkit, iterative dev loops (Ralph Wiggum), managed settings, MDM deploy | Adopt plugin architecture + structured dev workflows in Nexus UI |
| **OpenCode/Crush** | TUI coding agent | Go/Bubble Tea TUI, LSP integration, session management, auto-compact, MCP tools, custom commands with named args | TUI mode for Nexus power users |
| **Hermes Agent** | Generalist agent | Self-improving skills, 20-platform messaging gateway, sub-agent delegation, FTS5 search, cron scheduling, sandboxed code exec | Close the agent gap (see Sprint 1-4) |
| **Aider** | CLI pair programmer | Map&edit repo-aware editing, automatic git commits, multi-model architect/editor mode, voice coding | Agent-in-IDE pattern for Nexus |
| **Cline** | VS Code agent | Autonomous coding in IDE, terminal/file/editor access, MCP tools, checkpoint/restore, diff-based edits | VS Code extension for Nexus |
| **Continue** | IDE platform | Custom AI rules, model selection per workspace, tab autocomplete, inline edits, chat sidebar, @-context mentions | IDE bridge to Nexus |
| **Codex CLI** | CLI agent by OpenAI | Sandboxed execution, file edit tools, agent loop, bash/shell | Sandbox execution for Nexus |

**The Real Insight**

**Claude Code and Hermes Agent lead in agent capability.** Nexus leads in *data depth* — email, calendar, documents, research.

### Where Vibe Coding / App Builders Win

| Platform | What it does | Nexus Opportunity |
|---|---|---|
| **Manus.ai** (Meta) | Full-stack apps from plain English prompts. Built-in DB, auth, Stripe, SEO, analytics, browser operator, code export | **Conversational app builder inside Nexus** — "Build me a task dashboard" → Nexus generates the UI using existing components |
| **Lovable** | React + Supabase apps from prompts | Visual workspace dashboard builder |
| **Replit Agent** | Full IDE + AI agent, deploy apps | In-browser coding for extending Nexus |
| **Bolt.new** | StackBlitz-based prompt-to-app | Instant prototyping tool |

**The ultimate Nexus differentiator:** *An AI that can build you a custom dashboard showing your emails, calendar, tasks, and research — because it has access to all of them. Then publish it as a plugin. No Manus, Lovable, or Replit can do that — they don't have your data.*

**The winning move:** Adopt the best ideas from each platform's agent system, embedded in Nexus's web UI — with access to data no CLI agent can reach.

---

## 🎯 Immediate Priority: Close the Agent Gap

### Sprint 1: Agent Learning Loop
*"Nexus should get better the more you use it — just like Hermes Agent."*

| Feature | What | Why |
|---|---|---|
| **Self-improving skills** | After completing a complex task, the agent creates a SKILL.md from its approach. Skills get refined during reuse. | Hermes Agent's #1 differentiator |
| **FTS5 session search** | Full-text search across all past conversations. Find that discussion about X from 3 weeks ago. | Hermes Agent has this; users expect it |
| **Skill consolidation** | Background curator merges related skills, archives stale ones, surfaces conflicts. | Keeps skill library manageable |

### Sprint 2: Messaging Gateway
*"Talk to Nexus from Telegram, Discord, WhatsApp — not just the web UI."*

| Feature | What | Why |
|---|---|---|
| **Telegram bridge** | Chat with Nexus via Telegram bot. Commands, files, voice. | Most requested integration |
| **Slack/Discord bridge** | Nexus as a bot in your team channels. | Team use case |
| **WhatsApp bridge** | Nexus on your phone. | Mobile accessibility |

### Sprint 3: Delegation + Parallel Execution
*"Nexus should spawn sub-agents for hard problems."*

| Feature | What | Why |
|---|---|---|
| **Sub-agent delegation** | Main agent spawns sub-agents for parallel work (research, email drafting, data analysis). | Hermes Agent has this |
| **Parallel tool execution** | Independent tools run concurrently. | Performance |
| **Checkpoint/restore** | Save agent state mid-task. Resume after interruption. | Reliability |

### Sprint 4: Code Execution Sandbox
*"Safe Python execution for data analysis and automation."*

| Feature | What | Why |
|---|---|---|
| **Sandboxed Python** | Docker or subprocess sandbox for running user code. Returns output + generated files. | Open WebUI has this |
| **Plot/visualization support** | Matplotlib output captured and displayed inline. | Data analysis use case |
| **Timeout + resource limits** | Kill runaway scripts. | Safety |

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

### 4. 🧬 Agent Learning Loop (Beat Hermes Agent)
*"Nexus creates skills from experience and improves them over time."*

- After complex multi-step tasks, the agent generates a `SKILL.md` capturing the approach
- Skills are refined during reuse (adds missing steps, fixes outdated info)
- A background curator (`services/curator/`) periodically reviews skills, merges duplicates, archives stale ones
- FTS5-powered session search lets the agent (and user) find past solutions

### 5. 💬 Messaging Gateway (Beat Hermes Agent on Reach)
*"Talk to Nexus from Telegram, Discord, WhatsApp, Slack, Signal — anywhere."*

- Single gateway process (`mcp_servers/messaging_gateway.py`) connects to messaging platforms
- Telegram: full bot API (text, files, voice, commands, inline queries)
- Discord/Slack: bot in team channels, DMs, slash commands
- WhatsApp: via Baileys or WWebJS bridge
- **Why Nexus wins:** Unlike Hermes Agent's gateway, Nexus's gateway has access to email, calendar, and documents. *"Email me that document through Telegram"* — no other agent can do this.

### 6. ⚡ AI-Native Visual Workflow Builder
*Beat Dify and n8n by letting users describe workflows in plain language.*

- User types: *"Every morning, check email for urgent messages, search web for competitor news, and save a briefing as a document."*
- AI generates the workflow JSON automatically
- Visual canvas for tweaking (`static/js/workflow.js`)
- Cron-based execution engine (`services/workflow/`)

---

## 🔵 PHASE 3 — Sprint 6+: The Unassailable Moat

### 7. 🏢 Multi-Agent Teams
*"Email Agent + Research Agent + Calendar Agent + Writing Agent working together."*

- Specialized agents with domain expertise
- Agent collaboration graph: Research Agent finds info → Writing Agent drafts → Email Agent sends
- Scheduled agents (cron, event-driven, on-demand)
- Preference learning over time

### 8. 🖥️ Desktop Native App (Tauri)
*Build on existing launcher.py groundwork.*

- System tray with unread counts
- Native notifications
- Global hotkey (quick search/action)
- Offline-first with local SQLite
- Auto-start on boot

### 9. 🔌 Plugin Marketplace
*One-click install from the community.*

- Format: `plugin.json` manifest (directory with SKILL.md + optional Python/frontend)
- One-click install: paste GitHub URL → Nexus clones + registers
- "Browse Nexus Community" button in Skills UI

### 10. 📊 Usage Analytics + RBAC
*For teams and power users.*

- Token usage tracking (per-user, per-model, per-session)
- Admin dashboard (charts, costs, active users)
- Role-based access (admin, power user, viewer)
- Group-based model/tool permissions

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
| **Self-improving skills** | 📝 **Sprint 1** | Close Hermes Agent gap |
| **FTS5 session search** | 📝 **Sprint 1** | Cross-session recall |
| **Messaging gateway** | 📝 **Sprint 2** | Telegram, Discord, WhatsApp, Slack |
| **Sub-agent delegation** | 📝 **Sprint 3** | Parallel agent execution |
| **Code execution sandbox** | 📝 **Sprint 4** | Safe Python evaluation |
| **Morning Briefing** | 📝 **Sprint 1-2** | Nexus's unique value |
| **Email Assistant** | 📝 **Sprint 1-2** | Nexus's unique value |
| **Cross-Domain Engine** | 📝 **Sprint 1-2** | Nexus's unique value |
| Visual Workflow | ❌ Planned | Phase 2 |
| Plugin Marketplace | ❌ Planned | Phase 3 |
| Usage Analytics | ❌ Planned | Phase 3 |
| RBAC + Groups | ❌ Planned | Phase 3 |
| Multi-Agent Teams | ❌ Planned | Phase 3 |
| Desktop App | ❌ Planned | Phase 3 |
| i18n | ❌ Planned | Phase 3 |

---

## 🏗️ Architecture Principles

1. **Everything in one process** — FastAPI serves API + SPA. No microservices. Simpler deployment.
2. **Local-first, private by default** — SQLite, on-device embeddings, local auth. Cloud is optional opt-in.
3. **Graceful degradation** — Optional deps (crawl4ai, PyMuPDF, markitdown) fall back with clear messages.
4. **Cross-domain from day one** — All data (email, calendar, docs, tasks) lives in the same database. The AI sees everything.
5. **Skill-based agent system** — SKILL.md is the unit of agent capability. Self-improving skills over time.
6. **Messaging-first** — Not just web UI. Talk to Nexus from anywhere.
7. **Self-contained** — Single Docker image or `pip install`. No external dependencies beyond a database.

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
