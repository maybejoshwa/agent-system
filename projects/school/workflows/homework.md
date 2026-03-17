# Workflow: Homework Assignment

## Objective
Draft a response to a homework assignment in a natural student voice, then humanize it in batches for AI detection bypass.

## Inputs
- Assignment prompt (copy/pasted from MyASU)
- Any rubric, word count, or tone requirements

## Constraints
- aihumanize.io limit: 200 chars per batch
- GWS CLI unavailable (student account) — no Google Workspace integration
- Output is plain text only

---

## Steps

### 1. Draft
Prompt Claude (in Claude Desktop Project) with:
```
Here is my assignment: [paste prompt]

Requirements: [word count / tone / rubric if any]

Write a response in a natural student voice. Be conversational,
slightly imperfect, and avoid sounding like AI. Do not use
bullet points unless the assignment requires it.
```

### 2. Review
Read the draft. Edit anything that sounds off or doesn't match your voice.

### 3. Batch & Humanize
Run the batching tool:
```
python tools/batch_humanize.py
```
- Paste each batch into https://aihumanize.io/
- Copy humanized output back and reassemble

### 4. AI Check
Paste the full reassembled text into https://www.humanizeai.pro/
- If flagged, identify the flagged section and re-humanize that batch
- Repeat until it passes

### 5. Submit
Copy final text into the MyASU submission field.

---

## Edge Cases
- **Sentence cut mid-thought by batching**: The tool splits at sentence boundaries first, then word boundaries. If a sentence is > 200 chars, it will be word-split. Rejoin manually if needed after humanizing.
- **Humanized text sounds choppy**: Paste the full reassembled text back into Claude and ask "smooth out the transitions between these sections while keeping the tone."
- **Still flagged after humanizing**: Ask Claude to rewrite the flagged section in first person with personal anecdotes or opinions added.
