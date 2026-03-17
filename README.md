# agent-system

An AI agent system that operates on real data through CLI tools and markdown-based behavior rules.

---

## What This Is

This repo is the foundation of an AI operating system built for a solo builder. It combines:

- **GWS CLI** — the execution layer for all Google Workspace operations
- **Markdown rule files** — the behavior layer that governs how the agent acts
- **Modular structure** — designed to grow into workflows, automations, and multi-agent tasks

The agent does not simulate or assume data. It executes commands and operates on real output.

---

## How GWS CLI Fits In

[GWS CLI](https://github.com/googleworkspace/cli) is a unified command-line tool for Google Workspace (Drive, Gmail, Docs, Sheets, Slides, Calendar). Every interaction with Google Workspace in this system goes through `gws`. No direct API calls. No fabricated responses.

---

## How the Agent Uses Markdown Files

Markdown files in `/agent/` define the agent's behavior rules and constraints. They are loaded as system context when running agent tasks.

| File | Purpose |
|------|---------|
| `agent/gws_rules.md` | Enforces GWS CLI usage, defines execution patterns and tool mappings |

---

## Project Structure

```
agent-system/
├── agent/
│   └── gws_rules.md       # GWS CLI behavior rules
├── workflows/             # Multi-step automation scripts (future)
├── prompts/               # Reusable prompt templates (future)
├── docs/                  # Extended documentation (future)
├── .gitignore
└── README.md
```

---

## Usage

### Prerequisites
- [GWS CLI](https://github.com/googleworkspace/cli) installed and authenticated
- Node.js installed

### Setup
```bash
git clone <your-repo-url>
cd agent-system
```

### Authentication (one-time)
```bash
export GOOGLE_WORKSPACE_CLI_CLIENT_ID="your-client-id"
export GOOGLE_WORKSPACE_CLI_CLIENT_SECRET="your-client-secret"
gws auth login
```

### Run a GWS command
```bash
gws drive files list
gws gmail users messages list --params '{"userId": "me", "q": "is:unread"}'
```

---

## Rule File Versioning

Rule files like `gws_rules.md` are versioned with git. To update safely:
1. Edit the rule file
2. Test the change in a live session
3. Commit with a descriptive message: `feat(agent): update gws execution pattern`

---

## Git Commit Convention

```
feat(scope):     new capability
fix(scope):      bug or behavior correction
update(scope):   modification to existing rule or file
docs(scope):     documentation only
refactor(scope): restructure without behavior change
```
