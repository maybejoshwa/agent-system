# Agent System Overview

## What This System Is

A personal AI agent system built on the WAT framework, designed for a solo builder. It combines:
- Claude Code as the AI layer (reasoning, coordination, decision-making)
- GWS CLI as the Google Workspace execution layer
- Python tools for deterministic automation
- MCPs for extended capabilities (filesystem, web fetch, structured thinking)
- Skills as reusable slash-command procedures

## The WAT Framework

WAT stands for Workflows, Agents, Tools. It separates probabilistic AI reasoning from deterministic code execution.

**Why this matters:** If each step in a chain is 90% accurate, five steps gives you only 59% overall accuracy. By offloading execution to deterministic scripts, the agent stays focused on coordination where it excels.

### Layer 1: Workflows (`/workflows`)
Markdown SOP files. Each defines an objective, required inputs, tool sequence, and edge cases in plain English. Written like a brief to a capable team member.

### Layer 2: Agent (`CLAUDE.md`)
The agent layer — this system. Reads workflows, runs tools in sequence, handles errors, improves workflows when they fail.

### Layer 3: Tools (`/tools`)
Python scripts that execute actual work: API calls, data transforms, file operations. Credentials live in `.env`, never in the scripts.

## Extended Layers

### Skills (`~/.claude/commands/`)
Reusable slash commands. Invoke with `/skill-name`. Current skills:
- `/inbox-summary` — Gmail inbox summary with action items
- `/draft-email` — draft and send email from plain language
- `/calendar-brief` — daily schedule briefing
- `/drive-recent` — recently modified Drive files
- `/rag-search` — search this knowledge base

### Knowledge Base (`/knowledge/sources`)
RAG-indexed markdown files. Search with `/rag-search` or `python tools/rag_search.py --query "..."`.
Add new knowledge by dropping files in `knowledge/sources/` and running `--ingest`.

### MCPs (configured in `~/.claude/settings.json`)
- `filesystem` — structured file I/O in the repo and .tmp/
- `fetch` — live web content and external APIs
- `sequential-thinking` — structured multi-step reasoning

## Google Workspace Execution

All GWS operations go through the `gws` CLI. Authenticated as maybejoshwa@gmail.com. Covers: Drive, Gmail, Docs, Sheets, Slides, Calendar, Tasks. Never use direct API calls or fabricated data — if the CLI hasn't run, the data doesn't exist in the session.

## Key Principles

1. Execute, don't assume — run commands to get real data
2. Self-healing — when a tool fails, fix it, update the workflow, move on
3. Outputs go to cloud — Google Drive/Sheets/Slides, not local files
4. Secrets in `.env` only — never hardcoded, never read aloud
5. Modular — every layer grows independently, zero cross-layer wiring needed
