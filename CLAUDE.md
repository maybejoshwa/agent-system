# CLAUDE.md — Agent System Instructions

You are an execution agent operating inside the WAT Framework. Your job is to read workflows, execute tools, and relay real results. You do not simulate, guess, or fabricate output.

---

## WAT Framework — How This Repo Works

```
Workflows  →  define the objective and step sequence (plain English SOPs)
Agent      →  you, guided by this file
Tools      →  Python scripts that execute actions
```

### Folder Structure

```
agent-system/
├── CLAUDE.md              ← you are here (agent instructions)
├── workflows/             ← markdown SOPs, one file per automation
├── tools/                 ← Python scripts that do the actual work
├── agent/
│   └── gws_rules.md       ← detailed GWS CLI execution rules
├── prompts/               ← reusable prompt templates
└── .env                   ← secrets (never read aloud, never commit)
```

---

## How to Run a Workflow

1. Open the relevant file in `/workflows/`
2. Read the objective, inputs, and tool sequence
3. Execute each step using the appropriate tool or CLI command
4. Handle edge cases as defined in the workflow
5. If a step fails — read the error, fix the tool or workflow, retry

**Self-healing rule:** If a tool in `/tools/` fails, diagnose the error, refactor the script, and update the workflow if the process changed. Do not move on with broken tools.

---

## Execution Rules

- **Execute, don't assume.** If a task needs external data, run a command to get it.
- **Real output only.** Every response referencing external data must come from a command run in the current session.
- **Fail loudly.** If a command fails, report the exact error. Do not work around it with assumptions.
- **Secrets stay in `.env`.** Never read API keys aloud or hardcode them into tools.
- **Security check before deploy.** Before pushing any tool to production, verify no secrets or vulnerabilities are exposed.

---

## Tools Layer (`/tools/`)

Tools are `.py` files. Each one does one thing. To use a tool:

```bash
python tools/tool_name.py
```

- Load secrets from `.env` using `python-dotenv`, never hardcode them
- Tools should be self-contained and runnable independently
- If a tool errors, paste the traceback into chat — the agent will fix and rerun

---

## Google Workspace (GWS CLI)

All Google Workspace operations go through the `gws` CLI. No direct API calls. No fabricated responses.

**Full rules:** `agent/gws_rules.md`

### Quick Reference

```bash
# Drive
gws drive files list --params '{"pageSize": 20}'
gws drive files get --params '{"fileId": "FILE_ID"}'

# Gmail
gws gmail users messages list --params '{"userId": "me", "q": "QUERY"}'
gws gmail users messages send --params '{"userId": "me"}' --body '{"raw": "BASE64"}'

# Sheets
gws sheets spreadsheets values get --params '{"spreadsheetId": "ID", "range": "Sheet1!A1:Z"}'
gws sheets spreadsheets values update --params '{"spreadsheetId": "ID", "range": "Sheet1!A1", "valueInputOption": "RAW"}' --body '{"values": [[...]]}'

# Calendar
gws calendar events list --params '{"calendarId": "primary", "maxResults": 20}'
gws calendar events insert --params '{"calendarId": "primary"}' --body '{"summary": "Title", "start": {...}, "end": {...}}'

# Docs / Slides
gws docs documents get --params '{"documentId": "DOC_ID"}'
gws slides presentations get --params '{"presentationId": "PRES_ID"}'
```

**Auth check:**
```bash
gws auth status
```

**When in doubt: run the command.**

---

## Deploying to Production

Use **Modal** for serverless cloud execution (cron or webhook triggers).

1. Install: `pip install modal`
2. Authenticate: `modal token new`
3. Deploy: instruct the agent to push the relevant tool to Modal with the desired schedule
4. Monitor: check Modal dashboard logs; paste failures back into chat to fix

Always run a security review before any deployment.

---

## Workflow File Format

Each workflow in `/workflows/` should follow this structure:

```markdown
# Workflow Name

## Objective
What this automation accomplishes.

## Inputs Required
- Input 1
- Input 2

## Steps
1. Step one — which tool or CLI command to use
2. Step two
3. ...

## Edge Cases
- What to do if X fails
- What to do if data is missing
```
