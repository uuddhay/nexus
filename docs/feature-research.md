# Feature Research — Mining Open-Source Projects for Nexus

> **Date:** 2026-07-20
> **Scope:** Compared Nexus against Open WebUI, Jan, Dify, LobeChat, and n8n to identify valuable feature gaps.

---

## Executive Summary

Nexus is already a remarkably **feature-complete** self-hosted AI workspace. It outpaces competitors in email, calendar, documents, deep research, and MCP integration. However, these projects have pioneered features that would meaningfully extend Nexus. Below is a prioritized, actionable list.

---

## 🔴 P0 — High Impact, Feasible to Add

These features would close the biggest gaps with moderate implementation effort.

### 1. Visual Workflow Builder (from Dify / n8n)

**Source:** Dify (drag-and-drop AI workflow canvas), n8n (400+ node automation)
**Nexus gap:** No visual workflow editor. Users write skills in SKILL.md files.
**Why:** Lets non-technical users chain tools: "If email is urgent → search web → draft reply → send notification." Currently requires SKILL.md YAML.
**How:** Add a `/api/workflow` route + a lightweight visual canvas in `static/js/`. Nodes are existing tools (web search, email, calendar, LLM call). Save as JSON workflow that `src/agent_loop.py` executes step by step.

### 2. Scheduled Automations (from Open WebUI / n8n)

**Source:** Open WebUI "Automations" (cron-based prompt scheduling), n8n (triggers)
**Nexus gap:** Nexus has task scheduling but no cron-based prompt automations.
**Why:** "Every morning at 8am, summarize my email and add it to a note." Users want recurring AI tasks.
**How:** Build on existing `routes/task_routes.py` — add a cron expression field + template prompt. The agent runs the prompt on schedule and posts results to a note or email.

### 3. Model Capabilities System (from Open WebUI / Jan)

**Source:** Open WebUI's per-model `capabilities` (vision, file_upload, web_search, code_interpreter, terminal, citations, builtin_tools)
**Nexus gap:** No UI to toggle what each model can do. All models get the same toolset.
**Why:** Users want to control which models can search the web vs. which are "safe" chat-only models.
**How:** Add a `capabilities` JSON field to model config. The frontend shows toggles per model. `src/agent_loop.py` checks capabilities before enabling tools.

### 4. Live Workflow / Task Progress UI (from Open WebUI)

**Source:** Open WebUI's live message flow — shows the AI building checklists in real time
**Nexus gap:** Agent tasks run in the background; no real-time visibility into progress.
**Why:** Users want to watch the agent work through its steps (searching → reading → drafting). Builds trust and allows intervention.
**How:** Use Server-Sent Events (SSE) from the tool executor to push step completions to the frontend. Render a live checklist in the chat UI.

### 5. Code Interpreter Sandbox (from Open WebUI)

**Source:** Open WebUI's code_interpreter capability (sandboxed Python execution)
**Nexus gap:** Shell access exists but there's no sandboxed, disposable Python environment for data analysis.
**Why:** "Analyze this CSV and create a chart" — users want safe code execution without full shell access.
**How:** Add a lightweight Docker container or subprocess sandbox for Python execution. Mount temp files, return stdout/stderr + generated images.

---

## 🟡 P1 — Medium-Term Value

### 6. Plugin / Extension System (from Open WebUI / Dify)

**Source:** Open WebUI's Filters, Actions, Pipes, Tools, Skills; Dify's plugin marketplace
**Nexus gap:** Skills exist (SKILL.md) but there's no plugin marketplace or third-party extension API.
**Why:** Community contributions are easier to distribute as plugins vs. editing SKILL.md files.
**How:** Define a plugin manifest format (`plugin.json`). Add `/api/plugins/install` that clones a git repo + registers its tools/routes.

### 7. Community Sharing Marketplace (from Open WebUI)

**Source:** Open WebUI Community (openwebui.com) — share models, prompts, tools, skills
**Nexus gap:** No community hub for sharing skills/presets.
**Why:** Users want "one-click install" for community-created skills and presets.
**How:** Build a simple `skills.sh`-style directory. Add "Import from community" button in the Skills UI.

### 8. RBAC with User Groups (from Open WebUI)

**Source:** Open WebUI's granular permissions (workspace, sharing, chat, features, settings)
**Nexus gap:** Basic admin/user auth but no group-level permissions.
**Why:** Multi-user deployments need per-group model access, feature toggles.
**How:** Add a `groups` table + group-to-permission mapping. Filter available models/tools by group membership.

### 9. Usage Analytics Dashboard (from Open WebUI)

**Source:** Admin dashboards tracking message volume, token consumption, cost
**Nexus gap:** No analytics at all.
**Why:** Admins want to see who's using which models and how many tokens they're consuming.
**How:** Log token usage to a `token_usage` table. Add `/api/admin/analytics` route + a simple dashboard page in `static/`.

### 10. Search Providers Expansion (from Open WebUI)

**Source:** Open WebUI supports 20+ search providers including SearXNG, Brave, Kagi, Tavily, Perplexity, Firecrawl, serpstack, serper, Serply, DuckDuckGo, SearchApi, SerpApi, Bing, Jina, Exa, Sougou, Azure AI Search
**Nexus gap:** Nexus supports a subset (SearXNG, DuckDuckGo, etc.) but is missing several.
**Why:** More provider options = more deployment flexibility.
**How:** Add provider integrations following the pattern in `services/search/providers.py`.

---

## 🔵 P2 — Nice-to-Have, Lower Effort

### 11. PWA / Offline Support (from Open WebUI)

**Source:** Open WebUI has PWA with offline access on localhost
**Nexus gap:** No service worker, no offline caching.
**Why:** Better mobile experience, works when network drops.
**How:** Register a service worker that caches the SPA shell + recent conversations.

### 12. i18n / Multilingual UI (from Dify / Open WebUI)

**Source:** Dify supports 20+ languages; Open WebUI has full i18n
**Nexus gap:** English-only UI.
**Why:** Non-English users are a growing market for self-hosted AI.
**How:** Extract all UI strings into JSON locale files. Add a language selector in settings.

### 13. Desktop App via Tauri (from Jan)

**Source:** Jan is a Tauri-based desktop app (macOS, Windows, Linux)
**Nexus gap:** Web-only; no native desktop experience.
**Why:** System tray, native notifications, global hotkey, offline-first feel.
**How:** Wrap the SPA in Tauri. Bundles as a native app with tray icon (launcher.py already has tray groundwork).

### 14. OAuth / SSO Providers (from Open WebUI)

**Source:** Open WebUI supports LDAP, OAuth (Google, GitHub, etc.), SCIM 2.0
**Nexus gap:** Local auth only.
**Why:** Teams want to use their identity provider.
**How:** Add `routes/oauth_routes.py` with common OAuth flows. Store provider config in settings.

### 15. Model Hub / Browser (from Jan)

**Source:** Jan's Model Hub — browse and download models from HuggingFace
**Nexus gap:** Nexus has the Cookbook for model recommendations but no visual model browser.
**Why:** Users want to discover and download models without leaving Nexus.
**How:** Add a "Model Hub" tab that queries HuggingFace API and shows model cards. One-click download via Cookbook.

### 16. Changelog / Release Notes Auto-Generation

**Source:** Jan has a dedicated changelog page; Open WebUI has version update checks
**Nexus gap:** No built-in "What's new" experience.
**Why:** Users want to know what changed after updating.
**How:** Add a `/api/changelog` endpoint that reads a `CHANGELOG.md`. Show a modal on version change.

---

## 📊 Feature Comparison Matrix

| Feature | Nexus | Open WebUI | Dify | Jan | n8n |
|---|---|---|---|---|---|
| Chat + Agents | ✅ | ✅ | ✅ | ✅ | ✅ |
| RAG | ✅ | ✅ | ✅ | ❌ | ❌ |
| Email (IMAP/SMTP) | **✅** | ❌ | ❌ | ❌ | ❌ |
| Calendar + CalDAV | **✅** | ❌ | ❌ | ❌ | ✅ |
| Documents Editor | **✅** | ❌ | ❌ | ❌ | ❌ |
| Deep Research | **✅** | ❌ | ❌ | ❌ | ❌ |
| Model Serving | **✅** | ❌ | ❌ | ✅ | ❌ |
| MCP Support | **✅** | ✅ | ❌ | ✅ | ✅ |
| Visual Workflow Builder | ❌ | ❌ | **✅** | ❌ | **✅** |
| Scheduled Automations | ❌ | **✅** | ✅ | ❌ | **✅** |
| Code Interpreter Sandbox | ❌ | **✅** | ❌ | ❌ | ❌ |
| Plugin Marketplace | ❌ | **✅** | ✅ | ✅ | ✅ |
| RBAC with Groups | ❌ | **✅** | ✅ | ❌ | ✅ |
| Usage Analytics | ❌ | **✅** | ✅ | ❌ | ❌ |
| Desktop App | ❌ | ❌ | ❌ | **✅** | ✅ |
| i18n | ❌ | ✅ | **✅** | ✅ | ✅ |
| PWA / Offline | ❌ | ✅ | ❌ | ❌ | ❌ |
| OAuth/SSO | ❌ | **✅** | ✅ | ❌ | ✅ |

---

## 🎯 Recommended Sprint Plan

### Sprint 1: Quick Wins
1. **Model Capabilities UI** — Add per-model capability toggles (vision, search, tools)
2. **Search Providers** — Add 5 missing search providers (Firecrawl, Jina, Exa, Kagi, Perplexity)
3. **Live Task Progress** — SSE-based real-time agent step visibility

### Sprint 2: Workflows + Automations
4. **Visual Workflow Builder** — MVP: chain existing tools on a canvas, save/execute as JSON
5. **Scheduled Automations** — Cron-based prompt scheduling with output to notes/email

### Sprint 3: Multi-User + Analytics
6. **RBAC with Groups** — Group-level model/tool access control
7. **Usage Analytics** — Token tracking + admin dashboard

### Sprint 4: Ecosystem
8. **Plugin Marketplace** — `plugin.json` manifest + one-click install from git repos
9. **Community Hub** — Skills/presets sharing with import-from-URL

---

*Research conducted by analyzing the public codebases of:*
- *[Open WebUI](https://github.com/open-webui/open-webui) (MIT, 82k+ stars)*
- *[Jan](https://github.com/janhq/jan) (Apache 2.0, 28k+ stars)*
- *[Dify](https://github.com/langgenius/dify) (Apache 2.0, 65k+ stars)*
- *[n8n](https://github.com/n8n-io/n8n) (Sustainable Use License, 55k+ stars)*
