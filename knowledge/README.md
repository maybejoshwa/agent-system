# Knowledge Base

This is the RAG (Retrieval Augmented Generation) knowledge base. Claude can search it semantically using the `/rag-search` skill or by running `tools/rag_search.py` directly.

## How It Works

```
knowledge/sources/   ← you write .md or .txt files here
knowledge/index/     ← ChromaDB vector index (auto-generated, gitignored)
tools/rag_search.py  ← the tool that embeds and queries
```

The tool uses `sentence-transformers` (offline, no API key) to embed documents and `chromadb` as the local vector store.

## Adding Knowledge

1. Drop a `.md` or `.txt` file into `knowledge/sources/`
2. Re-run the ingest:
   ```bash
   python tools/rag_search.py --ingest
   ```
3. The index updates automatically — no other changes needed

## Searching

```bash
# From CLI
python tools/rag_search.py --query "how does GWS handle pagination"

# From Claude Code
/rag-search
```

## Current Knowledge Sources

| File | Contents |
|------|---------|
| `agent-system-overview.md` | WAT framework, system architecture, how each layer fits together |
| `gws-reference.md` | Condensed GWS CLI command reference |

## Prerequisites

Real Python 3.11+ from [python.org](https://python.org) (not Windows App Store stub), then:

```bash
pip install -r tools/requirements.txt
```

First ingest also downloads the `all-MiniLM-L6-v2` embedding model (~90MB, one-time).
