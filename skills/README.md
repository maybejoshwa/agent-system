# Skills

Skills are reusable slash commands — markdown SOPs that Claude invokes when you type `/skill-name`.

## How Skills Work

- **Invocation**: Type `/skill-name` in any Claude Code chat
- **Location**: The actual invokable files live at `~/.claude/commands/` (global, available in every session)
- **This folder**: Source documentation — what each skill does and why it's designed that way

## Current Skills

| Command | File | Purpose |
|---------|------|---------|
| `/inbox-summary` | `~/.claude/commands/inbox-summary.md` | Summarize unread Gmail, surface action items |
| `/draft-email` | `~/.claude/commands/draft-email.md` | Draft and optionally send email from plain-language description |
| `/calendar-brief` | `~/.claude/commands/calendar-brief.md` | Today/tomorrow schedule as a clean timeline |
| `/drive-recent` | `~/.claude/commands/drive-recent.md` | 15 most recently modified Drive files with links |
| `/rag-search` | `~/.claude/commands/rag-search.md` | Semantic search over local knowledge base |

## Adding a New Skill

1. Create `~/.claude/commands/your-skill-name.md` using this template:

```markdown
# Skill: your-skill-name

One sentence description.

Steps:
1. Step one — be specific about which tool, CLI command, or script to use
2. Step two
3. ...

Edge cases:
- What to do if X fails
```

2. It's immediately available — no restart needed
3. Add a row to the table above for documentation

## Global vs Project-Local Skills

- **Global** (`~/.claude/commands/`): Available in every Claude Code session — use for utilities that apply across projects
- **Project-local** (`.claude/commands/` inside a repo): Only active when Claude Code is open in that specific project — use for project-specific procedures
