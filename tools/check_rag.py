#!/usr/bin/env python3
"""
STG17 · Smoke test for the retrieval machinery of the Day 1 laboratory.

    python tools/check_rag.py

Runs with no model provider and no network: it exercises loading, chunking,
word-matching retrieval and evaluation, which is the half of RAG where the
failures that are hard to see actually live.

A chunker that silently drops the last paragraph of every document, or an
evaluator that scores a miss as a hit, looks completely normal inside a notebook.
This catches both.
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from stg17 import rag  # noqa: E402

FAILURES: list[str] = []


def check(condition: bool, description: str, detail: str = "") -> None:
    if condition:
        print(f"  ok    {description}")
    else:
        print(f"  FAIL  {description}" + (f"  ({detail})" if detail else ""))
        FAILURES.append(description)


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    print("Retrieval machinery (stg17.rag)")
    tmp = Path(tempfile.mkdtemp())

    # --- corpus -----------------------------------------------------------
    corpus = rag.write_sample_corpus(tmp / "corpus")
    docs = rag.load_corpus(corpus)
    check(len(docs) == 5, "sample corpus loads five documents", f"got {len(docs)}")
    check(all(d.words > 40 for d in docs), "every sample document carries text")
    check(all("FICTIONAL" in d.text or "FICTIONNEL" in d.text.upper() or
              "invented" in d.text.lower() for d in docs),
          "every sample document declares itself fictional")

    # --- chunking ---------------------------------------------------------
    chunks = rag.chunk_documents(docs, size=400, overlap=80)
    check(len(chunks) > len(docs), "chunking splits documents", f"{len(chunks)} chunks")
    check(all(c.text.strip() for c in chunks), "no chunk is empty")

    # The tail of every document must survive. A chunker that drops the final
    # buffer loses the last paragraph of every file, and nothing downstream says so.
    for doc in docs:
        tail = doc.text.split("\n\n")[-1].strip()[:40]
        mine = [c.text for c in chunks if c.doc_id == doc.doc_id]
        check(any(tail in text for text in mine),
              f"last paragraph of '{doc.title[:28]}' survives chunking")

    # Chunks must stay attributable, or a citation points at the wrong document.
    check({c.doc_id for c in chunks} == {d.doc_id for d in docs},
          "every chunk keeps its document identity")

    # --- retrieval --------------------------------------------------------
    index = rag.build_index(chunks, kind="tfidf")
    cases = [
        {"question": "What was the unemployment rate?", "expect": "labour"},
        {"question": "How was non-response handled?", "expect": "methodology"},
        {"question": "When is the consumer price index released?", "expect": "dissemination"},
        {"question": "Can individual data be sent abroad?", "expect": "statistical-act"},
    ]
    report = rag.evaluate_retrieval(index, cases, k=3)
    check(bool(report["hit"].all()),
          "every seeded question retrieves its own document",
          f"missed: {report.loc[~report.hit, 'question'].tolist()}")

    # The evaluator must be capable of reporting a miss. If it cannot, a hit rate
    # of 100% means nothing.
    wrong = rag.evaluate_retrieval(
        index, [{"question": "unemployment rate", "expect": "dissemination-calendar"}], k=1)
    check(not bool(wrong["hit"].iloc[0]), "the evaluator can report a miss")

    # --- prompt and refusal ----------------------------------------------
    hits = index.search("unemployment", k=2)
    prompt = rag.build_prompt("What was it?", hits)
    check("PASSAGES:" in prompt and "QUESTION:" in prompt, "prompt carries passages then question")
    check(all(h.chunk.text[:30] in prompt for h in hits), "every retrieved passage reaches the prompt")
    check(rag.REFUSAL in rag.SYSTEM, "the system prompt mandates the refusal string")
    check(rag.Answer("q", f"...{rag.REFUSAL}").refused, "a refusal is detected")
    check(not rag.Answer("q", "8.6 per cent [1]").refused, "a real answer is not read as a refusal")

    # --- transcript -------------------------------------------------------
    out = rag.save_transcript([rag.Answer("q", "a", hits)], tmp / "t.json", {"country": "CIV"})
    check(out.exists() and out.stat().st_size > 200, "transcript is written with its passages")

    print()
    if FAILURES:
        print(f"{len(FAILURES)} check(s) failed:")
        for name in FAILURES:
            print("   -", name)
        return 1
    print("All clear.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
