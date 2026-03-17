# GWS CLI Reference

Quick reference for Google Workspace CLI operations. Full rules: `agent/gws_rules.md`.

## Auth

```bash
gws auth status          # check current auth state + scopes
gws auth login           # re-authenticate
```

## Google Drive

```bash
# List files
gws drive files list --params '{"pageSize": 20}'
gws drive files list --params '{"pageSize": 15, "orderBy": "modifiedTime desc"}'

# Get file metadata
gws drive files get --params '{"fileId": "FILE_ID"}'

# Upload
gws drive +upload ./file.pdf
gws drive +upload ./file.pdf --parent FOLDER_ID

# Delete
gws drive files delete --params '{"fileId": "FILE_ID"}'
```

## Gmail

```bash
# List messages
gws gmail users messages list --params '{"userId": "me", "q": "is:unread", "maxResults": 20}'
gws gmail users messages list --params '{"userId": "me", "q": "from:example.com"}'

# Get message
gws gmail users messages get --params '{"userId": "me", "id": "MSG_ID", "format": "full"}'
gws gmail users messages get --params '{"userId": "me", "id": "MSG_ID", "format": "metadata", "metadataHeaders": ["Subject","From","Date"]}'

# Send
gws gmail users messages send --params '{"userId": "me"}' --body '{"raw": "BASE64URL_ENCODED_EMAIL"}'

# Modify labels (e.g. mark read)
gws gmail users messages modify --params '{"userId": "me", "id": "MSG_ID"}' --body '{"removeLabelIds": ["UNREAD"]}'
```

## Google Sheets

```bash
# Get spreadsheet
gws sheets spreadsheets get --params '{"spreadsheetId": "SHEET_ID"}'

# Create
gws sheets spreadsheets create --body '{"properties": {"title": "Title"}}'

# Read values
gws sheets spreadsheets values get --params '{"spreadsheetId": "SHEET_ID", "range": "Sheet1!A1:Z"}'

# Write values
gws sheets spreadsheets values update \
  --params '{"spreadsheetId": "SHEET_ID", "range": "Sheet1!A1", "valueInputOption": "RAW"}' \
  --body '{"values": [["col1", "col2"], ["val1", "val2"]]}'
```

## Google Docs

```bash
gws docs documents get --params '{"documentId": "DOC_ID"}'
gws docs documents create --body '{"title": "Title"}'
gws docs documents batchUpdate --params '{"documentId": "DOC_ID"}' --body '{"requests": [...]}'
```

## Google Slides

```bash
gws slides presentations get --params '{"presentationId": "PRES_ID"}'
gws slides presentations create --body '{"title": "Title"}'
gws slides presentations batchUpdate --params '{"presentationId": "PRES_ID"}' --body '{"requests": [...]}'
```

## Google Calendar

```bash
# List events
gws calendar events list --params '{"calendarId": "primary", "maxResults": 20}'
gws calendar events list --params '{"calendarId": "primary", "timeMin": "2026-03-17T00:00:00Z", "timeMax": "2026-03-17T23:59:59Z", "singleEvents": true, "orderBy": "startTime"}'

# Get event
gws calendar events get --params '{"calendarId": "primary", "eventId": "EVENT_ID"}'

# Create event
gws calendar events insert --params '{"calendarId": "primary"}' --body '{"summary": "Title", "start": {"dateTime": "2026-03-17T10:00:00-05:00"}, "end": {"dateTime": "2026-03-17T11:00:00-05:00"}}'

# Delete event
gws calendar events delete --params '{"calendarId": "primary", "eventId": "EVENT_ID"}'
```

## Pagination

If response contains `nextPageToken`, there is more data:
```bash
--params '{"pageToken": "NEXT_PAGE_TOKEN", ...}'
```
Or use `--page-all` to auto-paginate (returns NDJSON, one page per line).

## Debugging

```bash
gws <service> --help              # list subcommands
gws <service> <cmd> --help        # show params + examples
gws schema drive.files.list       # full schema for a method
```
