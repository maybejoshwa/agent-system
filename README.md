# agent-system

An AI agent system built on the **WAT Framework** — separating probabilistic reasoning (AI) from deterministic execution (code).

Inspired by [Nate Herk](https://www.youtube.com/@nateherk) / AI Automation Society.

---

## WAT+ Framework

Five layers that keep AI reasoning and code execution cleanly separated:

| Layer | Location | Format | Purpose |
|-------|----------|--------|---------|
| **Workflows** | `/workflows` | `.md` | SOPs — objectives, inputs, tool sequences, edge cases in plain English |
| **Agent** | `CLAUDE.md` | `.md` | Core instruction set — navigation, tool selection, behavior rules |
| **Tools** | `/tools` | `.py` | Execution code — deterministic scripts, APIs, data transforms |
| **Knowledge** | `/knowledge/sources` | `.md/.txt` | RAG source files — searchable reference material |
| **Skills** | `~/.claude/commands/` | `.md` | Reusable slash-command procedures for recurring tasks |

**MCP Servers** (in `~/.claude/settings.json`): `filesystem` · `fetch` · `sequential-thinking`

> API keys and secrets are **never** stored in tool files. They live in `.env`.

---

## Project Structure

```
agent-system/
├── CLAUDE.md              # Agent instructions (WAT+ framework)
├── workflows/             # Markdown SOPs (one file per automation)
├── tools/                 # Python scripts that execute actions
│   ├── rag_search.py      # RAG search tool
│   └── requirements.txt   # pip dependencies
├── skills/                # Skill documentation (invokable at ~/.claude/commands/)
├── knowledge/
│   ├── sources/           # Knowledge base source files (.md, .txt)
│   └── index/             # ChromaDB vector index (gitignored)
├── agent/
│   └── gws_rules.md       # GWS CLI enforcement rules (full reference)
├── .env                   # Secrets (never committed)
└── .gitignore
```

---

## Execution Layer: GWS CLI

[GWS CLI](https://github.com/googleworkspace/cli) handles all Google Workspace operations (Drive, Gmail, Docs, Sheets, Slides, Calendar). No direct API calls. No fabricated responses.

```bash
gws drive files list
gws gmail users messages list --params '{"userId": "me", "q": "is:unread"}'
gws calendar events list --params '{"calendarId": "primary"}'
```

---

## Setup

```bash
git clone https://github.com/maybejoshwa/agent-system.git
cd agent-system
```

### GWS Authentication (one-time)
```bash
export GOOGLE_WORKSPACE_CLI_CLIENT_ID="your-client-id"
export GOOGLE_WORKSPACE_CLI_CLIENT_SECRET="your-client-secret"
gws auth login
```

---

## Git Commit Convention

```
feat(scope):      new capability
fix(scope):       bug or behavior correction
update(scope):    modification to existing rule or file
docs(scope):      documentation only
refactor(scope):  restructure without behavior change
```
