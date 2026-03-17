"""
rag_search.py — Local knowledge base search tool

Usage:
  python tools/rag_search.py --ingest                        # index knowledge/sources/
  python tools/rag_search.py --query "your question" [--top_k 5]

Prerequisites:
  pip install -r tools/requirements.txt
  (Real Python 3.11+ from python.org required — not Windows App Store stub)
"""

import argparse
import json
import os
import sys
from pathlib import Path

# Resolve paths relative to the repo root (one level up from tools/)
REPO_ROOT = Path(__file__).parent.parent
SOURCE_DIR = REPO_ROOT / "knowledge" / "sources"
INDEX_DIR = REPO_ROOT / "knowledge" / "index"
COLLECTION_NAME = "agent-knowledge"
EMBED_MODEL = "all-MiniLM-L6-v2"
CHUNK_SIZE = 500   # characters
CHUNK_OVERLAP = 50


def get_collection():
    try:
        import chromadb
    except ImportError:
        print("ERROR: chromadb not installed. Run: pip install -r tools/requirements.txt")
        sys.exit(1)

    client = chromadb.PersistentClient(path=str(INDEX_DIR))
    return client.get_or_create_collection(COLLECTION_NAME)


def get_embedding_model():
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError:
        print("ERROR: sentence-transformers not installed. Run: pip install -r tools/requirements.txt")
        sys.exit(1)

    return SentenceTransformer(EMBED_MODEL)


def chunk_text(text: str, size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """Split text into overlapping chunks."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + size
        chunks.append(text[start:end])
        start += size - overlap
    return chunks


def ingest(source_dir: Path = SOURCE_DIR):
    """Embed and index all .md and .txt files in source_dir."""
    files = list(source_dir.glob("*.md")) + list(source_dir.glob("*.txt"))
    if not files:
        print(f"No .md or .txt files found in {source_dir}")
        return

    print(f"Loading embedding model ({EMBED_MODEL})...")
    model = get_embedding_model()
    collection = get_collection()

    total_chunks = 0
    for file in files:
        text = file.read_text(encoding="utf-8")
        chunks = chunk_text(text)
        ids = [f"{file.name}::chunk{i}" for i in range(len(chunks))]
        embeddings = model.encode(chunks).tolist()
        metadatas = [{"source": file.name, "chunk_id": i} for i in range(len(chunks))]

        # Upsert so re-ingesting is safe
        collection.upsert(ids=ids, embeddings=embeddings, documents=chunks, metadatas=metadatas)
        total_chunks += len(chunks)
        print(f"  Indexed {file.name} ({len(chunks)} chunks)")

    print(f"\nDone. {len(files)} files, {total_chunks} total chunks indexed.")


def query(query_text: str, top_k: int = 5):
    """Semantic search over the indexed knowledge base."""
    model = get_embedding_model()
    collection = get_collection()

    if collection.count() == 0:
        print("Index is empty. Run: python tools/rag_search.py --ingest")
        sys.exit(1)

    query_embedding = model.encode([query_text]).tolist()
    results = collection.query(query_embeddings=query_embedding, n_results=top_k)

    output = []
    for i in range(len(results["ids"][0])):
        output.append({
            "rank": i + 1,
            "score": round(1 - results["distances"][0][i], 4),  # cosine similarity
            "source": results["metadatas"][0][i]["source"],
            "text": results["documents"][0][i].strip(),
        })

    print(json.dumps(output, indent=2))


def main():
    global SOURCE_DIR, INDEX_DIR

    parser = argparse.ArgumentParser(description="RAG search tool for agent-system knowledge base")
    parser.add_argument("--ingest", action="store_true", help="Index all files in knowledge/sources/")
    parser.add_argument("--query", type=str, help="Semantic search query")
    parser.add_argument("--top_k", type=int, default=5, help="Number of results to return (default: 5)")
    parser.add_argument("--source-dir", type=Path, default=SOURCE_DIR, help="Override source directory")
    parser.add_argument("--index-dir", type=Path, default=INDEX_DIR, help="Override index directory")
    args = parser.parse_args()

    # Override globals if custom paths provided
    SOURCE_DIR = args.source_dir
    INDEX_DIR = args.index_dir

    if args.ingest:
        ingest(SOURCE_DIR)
    elif args.query:
        query(args.query, args.top_k)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
