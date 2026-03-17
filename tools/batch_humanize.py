"""
batch_humanize.py
Splits text into chunks ≤ MAX_CHARS, breaking at sentence then word boundaries.
Usage: python tools/batch_humanize.py
       (paste text when prompted, then press Enter twice)
"""

import re
import sys

MAX_CHARS = 200  # aihumanize.io free tier limit


def split_into_sentences(text: str) -> list[str]:
    """Split text into sentences."""
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s.strip() for s in sentences if s.strip()]


def make_batches(text: str, max_chars: int = MAX_CHARS) -> list[str]:
    """Split text into batches of at most max_chars, respecting word boundaries."""
    sentences = split_into_sentences(text)
    batches = []
    current = ""

    for sentence in sentences:
        # If this single sentence is too long, split by words
        if len(sentence) > max_chars:
            words = sentence.split()
            for word in words:
                if not current:
                    current = word
                elif len(current) + 1 + len(word) <= max_chars:
                    current += " " + word
                else:
                    batches.append(current)
                    current = word
            if current:
                batches.append(current)
                current = ""
        else:
            candidate = (current + " " + sentence).strip() if current else sentence
            if len(candidate) <= max_chars:
                current = candidate
            else:
                if current:
                    batches.append(current)
                current = sentence

    if current:
        batches.append(current)

    return batches


def main():
    print("=" * 60)
    print("  Homework Humanizer Batcher")
    print(f"  Batch size: {MAX_CHARS} chars (aihumanize.io limit)")
    print("=" * 60)
    print("\nPaste your text below, then press Enter twice when done:\n")

    lines = []
    try:
        while True:
            line = input()
            if line == "" and lines and lines[-1] == "":
                break
            lines.append(line)
    except EOFError:
        pass

    text = "\n".join(lines).strip()

    if not text:
        print("No text provided.")
        sys.exit(1)

    batches = make_batches(text)
    total = len(batches)

    print(f"\n{'=' * 60}")
    print(f"  {total} batch{'es' if total != 1 else ''} to process")
    print(f"  Total chars: {len(text)}")
    print(f"{'=' * 60}\n")

    for i, batch in enumerate(batches, 1):
        print(f"--- Batch {i}/{total} ({len(batch)} chars) ---")
        print(batch)
        print()
        if i < total:
            input("  >> Paste above into aihumanize.io, then press Enter for next batch...")
            print()

    print("=" * 60)
    print("  All batches done! Now paste humanized output into:")
    print("  https://www.humanizeai.pro/ to check for AI detection.")
    print("=" * 60)


if __name__ == "__main__":
    main()
