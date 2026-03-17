# GWS_RULES.md — Google Workspace CLI Enforcement Layer

---

## 1. Core Directive

**GWS CLI is the sole interface for all Google Workspace operations.**

Every interaction with Google Drive, Gmail, Google Docs, Sheets, Slides, or Calendar must be executed through the `gws` command-line tool. No exceptions.

This is an execution environment. Data is retrieved, not generated.

---

## 2. Strict Rules

| Rule | Description |
|------|-------------|
| NO_API | Do not use Google APIs directly. Do not construct HTTP requests to Google endpoints. |
| NO_SIMULATION | Do not simulate, mock, or fabricate command output under any circumstance. |
| NO_HALLUCINATION | Do not reference, describe, or summarize Google Workspace data that has not been retrieved in the current session via GWS CLI. |
| NO_SKIP | Do not skip CLI execution when a GWS CLI command exists for the task. Reasoning alone is not a substitute. |
| NO_ASSUMPTION | Do not assume file names, email contents, calendar events, or any workspace data. Fetch it. |

**Violation of any rule above is a critical agent failure.**

---

## 3. Execution Pattern

Every Google Workspace operation must follow this pattern without deviation:

```
STEP 1 — IDENTIFY
  Determine which GWS CLI command covers the required operation.
  Reference: gws <service> --help

STEP 2 — EXECUTE
  Run the exact CLI command in the terminal.
  Pass required params via --params '{"key": "value"}'.

STEP 3 — PARSE
  Read the JSON response returned by the CLI.
  Extract only the fields needed for the current task.

STEP 4 — CONTINUE
  Use the parsed output to inform the next step.
  Do not inject external knowledge into the workflow at this stage.
```

Do not proceed to the next step until the current step produces a real result.

---

## 4. Tool Mapping

### Google Drive
```bash
gws drive files list --params '{"pageSize": 20}'
gws drive files get --params '{"fileId": "FILE_ID"}'
gws drive +upload ./file.pdf
gws drive +upload ./file.pdf --parent FOLDER_ID
gws drive files delete --params '{"fileId": "FILE_ID"}'
```

### Gmail
```bash
gws gmail users messages list --params '{"userId": "me", "q": "QUERY", "maxResults": 20}'
gws gmail users messages get --params '{"userId": "me", "id": "MSG_ID", "format": "full"}'
gws gmail users messages get --params '{"userId": "me", "id": "MSG_ID", "format": "metadata", "metadataHeaders": ["Subject","From","Date"]}'
gws gmail users messages send --params '{"userId": "me"}' --body '{"raw": "BASE64_ENCODED_EMAIL"}'
gws gmail users messages modify --params '{"userId": "me", "id": "MSG_ID"}' --body '{"removeLabelIds": ["UNREAD"]}'
```

### Google Docs
```bash
gws docs documents get --params '{"documentId": "DOC_ID"}'
gws docs documents create --body '{"title": "Title"}'
gws docs documents batchUpdate --params '{"documentId": "DOC_ID"}' --body '{"requests": [...]}'
```

### Google Sheets
```bash
gws sheets spreadsheets get --params '{"spreadsheetId": "SHEET_ID"}'
gws sheets spreadsheets create --body '{"properties": {"title": "Title"}}'
gws sheets spreadsheets values get --params '{"spreadsheetId": "SHEET_ID", "range": "Sheet1!A1:Z"}'
gws sheets spreadsheets values update --params '{"spreadsheetId": "SHEET_ID", "range": "Sheet1!A1", "valueInputOption": "RAW"}' --body '{"values": [[...]]}'
```

### Google Slides
```bash
gws slides presentations get --params '{"presentationId": "PRES_ID"}'
gws slides presentations create --body '{"title": "Title"}'
gws slides presentations batchUpdate --params '{"presentationId": "PRES_ID"}' --body '{"requests": [...]}'
```

### Google Calendar
```bash
gws calendar calendars list
gws calendar events list --params '{"calendarId": "primary", "maxResults": 20}'
gws calendar events get --params '{"calendarId": "primary", "eventId": "EVENT_ID"}'
gws calendar events insert --params '{"calendarId": "primary"}' --body '{"summary": "Title", "start": {...}, "end": {...}}'
gws calendar events delete --params '{"calendarId": "primary", "eventId": "EVENT_ID"}'
```

---

## 5. Failure Handling

### On CLI Error
1. Read the full error message from stderr.
2. Identify the cause: missing param, auth failure, rate limit, invalid ID, permissions.
3. Do not guess at the correct output. Address the root cause.

### Auth Errors
```
error: token expired → run: gws auth login
error: credentials not found → check: GOOGLE_WORKSPACE_CLI_CLIENT_ID and GOOGLE_WORKSPACE_CLI_CLIENT_SECRET env vars
```

### Missing Parameters
```
error: Required path parameter X is missing
→ Add the missing param to --params JSON. Reference: gws <service> <command> --help
```

### Retry Logic
- Retry a failed command once after resolving the identified cause.
- Do not retry the same failing command more than twice without a change.
- If retries fail, report the exact error to the user. Do not proceed with assumed data.

### Debugging
```bash
gws <command> --dry-run    # validate request without sending
gws <service> --help       # show available subcommands
gws <service> <cmd> --help # show required params and examples
```

---

## 6. Output Handling

### Parsing JSON Responses
- GWS CLI returns JSON. Parse and extract only the fields relevant to the task.
- Do not present raw JSON to the user unless they explicitly request it.
- Summarize in a structured, readable format (table, list, or prose as appropriate).

### Field Extraction Pattern
```
raw response → identify relevant fields → format for display → present to user
```

### Pagination
- If a response contains `nextPageToken`, there is more data.
- Fetch additional pages when completeness is required for the task.
```bash
--params '{"pageToken": "NEXT_PAGE_TOKEN", ...}'
```

### Large Responses
- For large file lists or message lists: summarize counts, group by type, highlight key entries.
- Do not dump hundreds of raw records unless the user asks for export.

---

## 7. Behavioral Constraints

```
THIS IS AN EXECUTION ENVIRONMENT.
NOT A SIMULATION ENVIRONMENT.
NOT A REASONING ENVIRONMENT.
```

- The agent's role is to execute commands and relay real results.
- Training knowledge about Google Workspace is context, not data.
- If the CLI has not been run, the data does not exist in this session.
- Every claim about a user's Google Workspace must trace back to a CLI call made in the current session.
- Speed is not a justification for skipping execution.
- Uncertainty is not a justification for fabricating output.

**When in doubt: run the command.**
