"""
STG17 · Retrieval-augmented generation over a statistical office's own documents.

The Day 1 laboratory builds an assistant that answers questions about *your*
publications and cites the paragraph it used. This module holds the machinery so
that the notebook can hold the teaching.

--------------------------------------------------------------------------
THE DESIGN DECISION THAT MATTERS
--------------------------------------------------------------------------
There are two retrievers here, not one, and the choice between them is a lesson
rather than a configuration detail:

    TF-IDF        pure scikit-learn, no download, works on any network.
                  Matches words. Fails when the question and the document use
                  different vocabulary for the same idea.

    Embeddings    downloads a ~90 MB model once. Matches meaning, so
                  "how many people live there" finds a paragraph about
                  population. Fails differently: it will confidently return
                  something related-but-wrong when the corpus has no answer.

A participant who has watched both fail on the same question understands
retrieval better than one who was handed the better of the two. `build_index`
defaults to `"auto"`, which prefers embeddings and falls back silently — but the
notebook asks for each explicitly, and compares.

--------------------------------------------------------------------------
THE REFUSAL
--------------------------------------------------------------------------
The failure mode of a first RAG build is not a wrong retrieval. It is an empty
retrieval followed by a fluent answer from the model's own memory. So the system
prompt here mandates a literal refusal string, and `Answer.refused` detects it.

An office evaluating an assistant on whether it always replies has the wrong
metric. "Not in my documents" is a correct answer.
"""

from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Sequence

from .i18n import T

#: What the model must say when the retrieved passages do not answer the
#: question. Checked verbatim, so it must not be translated inside the prompt.
REFUSAL = "NOT_IN_MY_DOCUMENTS"


# ---------------------------------------------------------------------------
#  Documents and chunks
# ---------------------------------------------------------------------------
@dataclass
class Document:
    """One source file, as plain text."""

    doc_id: str
    title: str
    source: str          # a path or a URL, shown to the user as the citation
    text: str

    @property
    def words(self) -> int:
        return len(self.text.split())


@dataclass
class Chunk:
    """A passage of one document — the unit that is retrieved and cited."""

    doc_id: str
    title: str
    source: str
    text: str
    index: int           # position within the document, for ordering a citation

    @property
    def citation(self) -> str:
        return f"{self.title} — passage {self.index + 1}"


@dataclass
class Hit:
    chunk: Chunk
    score: float


@dataclass
class Answer:
    question: str
    text: str
    hits: list[Hit] = field(default_factory=list)
    provider: str = ""
    model: str = ""
    latency_s: float = 0.0

    @property
    def refused(self) -> bool:
        """True when the model declined because the passages did not answer."""
        return REFUSAL in self.text

    @property
    def sources(self) -> list[str]:
        seen, out = set(), []
        for hit in self.hits:
            if hit.chunk.source not in seen:
                seen.add(hit.chunk.source)
                out.append(hit.chunk.source)
        return out

    def to_dict(self) -> dict:
        return {
            "question": self.question,
            "answer": self.text,
            "refused": self.refused,
            "provider": self.provider,
            "model": self.model,
            "latency_s": round(self.latency_s, 2),
            "passages": [
                {"citation": h.chunk.citation, "source": h.chunk.source,
                 "score": round(h.score, 4), "text": h.chunk.text}
                for h in self.hits
            ],
        }


# ---------------------------------------------------------------------------
#  Loading
# ---------------------------------------------------------------------------
_SUPPORTED = {".txt", ".md", ".markdown", ".pdf", ".html", ".htm"}


def _clean(text: str) -> str:
    """Normalise whitespace without destroying paragraph structure."""
    text = unicodedata.normalize("NFC", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _read_pdf(path: Path) -> str:
    try:
        from pypdf import PdfReader  # noqa: PLC0415
    except ImportError as exc:  # pragma: no cover - environment dependent
        raise RuntimeError(
            T("Reading PDFs needs `pypdf`. Install it, or convert the file to text.",
              "La lecture des PDF nécessite `pypdf`. Installez-le, ou convertissez "
              "le fichier en texte.")
        ) from exc
    reader = PdfReader(str(path))
    return "\n\n".join((page.extract_text() or "") for page in reader.pages)


def _read_html(path: Path) -> str:
    raw = path.read_text(encoding="utf-8", errors="replace")
    raw = re.sub(r"<(script|style|nav|footer)\b.*?</\1>", " ", raw, flags=re.S | re.I)
    return re.sub(r"<[^>]+>", " ", raw)


def load_corpus(source: str | Path, pattern: str = "**/*", limit: int | None = None
                ) -> list[Document]:
    """
    Read every supported file under a directory into `Document` objects.

    Supports .txt, .md, .pdf and .html. A PDF whose text layer is empty — a scan —
    yields an empty document and is reported rather than silently dropped, because
    "the assistant does not know about that report" is otherwise very hard to
    diagnose.
    """
    root = Path(source)
    if root.is_file():
        paths = [root]
    else:
        paths = sorted(p for p in root.glob(pattern)
                       if p.is_file() and p.suffix.lower() in _SUPPORTED)
    if limit:
        paths = paths[:limit]

    docs, empty = [], []
    for path in paths:
        suffix = path.suffix.lower()
        if suffix == ".pdf":
            text = _read_pdf(path)
        elif suffix in {".html", ".htm"}:
            text = _read_html(path)
        else:
            text = path.read_text(encoding="utf-8", errors="replace")
        text = _clean(text)
        if not text:
            empty.append(path.name)
            continue
        docs.append(Document(
            doc_id=hashlib.sha1(str(path).encode()).hexdigest()[:10],
            title=path.stem.replace("_", " ").replace("-", " ").strip(),
            source=str(path),
            text=text,
        ))

    if empty:
        print(T(f"[!] {len(empty)} file(s) yielded no text and were skipped: "
                f"{', '.join(empty[:5])}. A scanned PDF has no text layer — it needs OCR.",
                f"[!] {len(empty)} fichier(s) n'ont donné aucun texte et ont été ignorés : "
                f"{', '.join(empty[:5])}. Un PDF scanné n'a pas de couche texte — il faut de l'OCR."))
    return docs


# ---------------------------------------------------------------------------
#  Chunking
# ---------------------------------------------------------------------------
def chunk_documents(docs: Sequence[Document], size: int = 900, overlap: int = 150
                    ) -> list[Chunk]:
    """
    Split documents into overlapping passages, on paragraph boundaries.

    `size` is in characters, not tokens, because a participant can see characters
    in their own document and cannot see tokens.

    The overlap exists because the sentence that answers a question is often the
    one that straddles a boundary. Too little overlap loses it; too much inflates
    the index and returns near-duplicate passages. The notebook has participants
    move both numbers and watch what changes.
    """
    if overlap >= size:
        raise ValueError("overlap must be smaller than size")

    chunks: list[Chunk] = []
    for doc in docs:
        paragraphs = [p.strip() for p in doc.text.split("\n\n") if p.strip()]
        buffer, index = "", 0
        for para in paragraphs:
            if len(buffer) + len(para) + 2 <= size:
                buffer = f"{buffer}\n\n{para}" if buffer else para
                continue
            if buffer:
                chunks.append(Chunk(doc.doc_id, doc.title, doc.source, buffer, index))
                index += 1
                buffer = buffer[-overlap:] + "\n\n" + para if overlap else para
            else:
                # A single paragraph longer than `size`: cut it on whitespace.
                for start in range(0, len(para), size - overlap):
                    piece = para[start:start + size]
                    chunks.append(Chunk(doc.doc_id, doc.title, doc.source, piece, index))
                    index += 1
                buffer = ""
        if buffer:
            chunks.append(Chunk(doc.doc_id, doc.title, doc.source, buffer, index))
    return chunks


# ---------------------------------------------------------------------------
#  Retrieval
# ---------------------------------------------------------------------------
class TfidfIndex:
    """
    Word-matching retrieval. No download, works on any network.

    Honest about its limit: it cannot connect "how many people live there" to a
    paragraph that says "population". That failure is the reason embeddings
    exist, and the notebook shows it happening.
    """

    kind = "tfidf"

    def __init__(self, chunks: Sequence[Chunk]):
        from sklearn.feature_extraction.text import TfidfVectorizer  # noqa: PLC0415

        self.chunks = list(chunks)
        self.vectorizer = TfidfVectorizer(
            lowercase=True, ngram_range=(1, 2), min_df=1,
            strip_accents="unicode", sublinear_tf=True,
        )
        self.matrix = self.vectorizer.fit_transform([c.text for c in self.chunks])

    def search(self, query: str, k: int = 4) -> list[Hit]:
        from sklearn.metrics.pairwise import cosine_similarity  # noqa: PLC0415

        scores = cosine_similarity(self.vectorizer.transform([query]), self.matrix)[0]
        order = scores.argsort()[::-1][:k]
        return [Hit(self.chunks[i], float(scores[i])) for i in order if scores[i] > 0]


class EmbeddingIndex:
    """
    Meaning-matching retrieval. Downloads a small model once, then works offline.

    Fails differently from TF-IDF: where TF-IDF returns nothing when the words do
    not match, this returns the *nearest* passage even when nothing is close. A
    score threshold is therefore not optional — see `answer(min_score=...)`.
    """

    kind = "embedding"
    DEFAULT_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

    def __init__(self, chunks: Sequence[Chunk], model_name: str = DEFAULT_MODEL):
        from sentence_transformers import SentenceTransformer  # noqa: PLC0415

        self.chunks = list(chunks)
        self.model_name = model_name
        # Multilingual on purpose: half this workshop works in French, and an
        # English-only encoder would quietly retrieve worse for them.
        self.model = SentenceTransformer(model_name)
        self.vectors = self.model.encode(
            [c.text for c in self.chunks],
            normalize_embeddings=True, show_progress_bar=False, batch_size=32,
        )

    def search(self, query: str, k: int = 4) -> list[Hit]:
        import numpy as np  # noqa: PLC0415

        q = self.model.encode([query], normalize_embeddings=True)[0]
        scores = np.asarray(self.vectors) @ q
        order = scores.argsort()[::-1][:k]
        return [Hit(self.chunks[i], float(scores[i])) for i in order]


def build_index(chunks: Sequence[Chunk], kind: str = "auto"):
    """
    `"tfidf"`, `"embedding"`, or `"auto"` — embeddings if they can be loaded.

    `auto` prints which one it chose. A laboratory that silently degrades is a
    laboratory where half the room draws conclusions from a different system than
    the other half.
    """
    if kind == "tfidf":
        return TfidfIndex(chunks)
    if kind == "embedding":
        return EmbeddingIndex(chunks)
    if kind != "auto":
        raise ValueError("kind must be 'tfidf', 'embedding' or 'auto'")

    try:
        index = EmbeddingIndex(chunks)
        print(T("Using embeddings — retrieval matches meaning.",
                "Embeddings utilisés — la récupération correspond au sens."))
        return index
    except Exception as exc:  # noqa: BLE001 - any failure means fall back
        print(T(f"Embeddings unavailable ({type(exc).__name__}); using TF-IDF. "
                f"Retrieval will match words, not meaning.",
                f"Embeddings indisponibles ({type(exc).__name__}) ; TF-IDF utilisé. "
                f"La récupération correspondra aux mots, pas au sens."))
        return TfidfIndex(chunks)


# ---------------------------------------------------------------------------
#  Generation
# ---------------------------------------------------------------------------
SYSTEM = (
    "You are a careful assistant to a national statistical office. You answer "
    "ONLY from the passages supplied to you in the user message.\n\n"
    "Rules, in order of priority:\n"
    "1. If the passages do not contain the answer, reply with exactly "
    f"{REFUSAL} and nothing else. Do not use your own knowledge. Do not guess. "
    "Do not offer a partial answer that the passages do not support.\n"
    "2. When the passages do answer, quote the figure or statement as it appears. "
    "Do not round, convert or restate a number.\n"
    "3. End every answer with the passage numbers you used, like [1] or [2, 3].\n"
    "4. Be brief. Three sentences unless the question genuinely needs more.\n"
    "5. Answer in the language of the question."
)


def build_prompt(question: str, hits: Sequence[Hit]) -> str:
    """The user message: the retrieved passages, then the question."""
    if not hits:
        return (f"PASSAGES:\n(none were retrieved)\n\nQUESTION: {question}")
    blocks = [
        f"[{i}] {h.chunk.citation}\n{h.chunk.text}"
        for i, h in enumerate(hits, start=1)
    ]
    return "PASSAGES:\n" + "\n\n---\n\n".join(blocks) + f"\n\nQUESTION: {question}"


def answer(question: str, index, k: int = 4, min_score: float = 0.0,
           provider: str = "auto", max_tokens: int = 700) -> Answer:
    """
    Retrieve, augment, generate — the three steps, in one call.

    `min_score` drops weak passages before they reach the model. With an
    embedding index this matters: it always returns the nearest passage, so
    without a floor the model is handed something irrelevant and asked to answer
    from it. Setting it too high turns answerable questions into refusals. The
    notebook has participants find the value for their own corpus.
    """
    from . import llm  # noqa: PLC0415 - keeps `import stg17.rag` cheap

    hits = [h for h in index.search(question, k=k) if h.score >= min_score]
    reply = llm.chat(
        build_prompt(question, hits),
        system=SYSTEM,
        provider=provider,
        max_tokens=max_tokens,
        deterministic=True,
    )
    return Answer(
        question=question,
        text=reply.text.strip(),
        hits=hits,
        provider=reply.provider,
        model=reply.model,
        latency_s=reply.latency_s,
    )


# ---------------------------------------------------------------------------
#  Evaluation
# ---------------------------------------------------------------------------
def evaluate_retrieval(index, cases: Iterable[dict], k: int = 4):
    """
    Did the right document reach the model at all?

    `cases` is a list of {"question": ..., "expect": <substring of the source
    path or title>}, plus optionally {"expect": None} for a question the corpus
    cannot answer — those are the ones that catch a system which never refuses.

    Returns a DataFrame. The column that matters is `hit`: a generation problem
    and a retrieval problem look identical from the answer, and they have
    completely different fixes.
    """
    import pandas as pd  # noqa: PLC0415

    rows = []
    for case in cases:
        hits = index.search(case["question"], k=k)
        found = [f"{h.chunk.title} :: {h.chunk.source}" for h in hits]
        expect = case.get("expect")
        hit = (expect is None) or any(expect.lower() in f.lower() for f in found)
        rows.append({
            "question": case["question"],
            "expect": expect if expect is not None else "(unanswerable)",
            "hit": hit,
            "top_score": round(hits[0].score, 3) if hits else 0.0,
            "top_source": hits[0].chunk.title if hits else "-",
        })
    return pd.DataFrame(rows)


#: A teaching corpus, for participants who have not yet cleared their own
#: publications for use. Every figure below is INVENTED, and every file says so
#: in its first line — a sample corpus that reads like real national statistics
#: is the fastest way to get a fabricated number into a real report.
_SAMPLE = {
    "population-and-housing-census-2021.md": """\
# Population and Housing Census 2021 — Main results

> FICTIONAL DOCUMENT. Every figure here is invented for teaching purposes and
> describes the imaginary Republic of Terrafrica. Do not cite any of it.

The resident population enumerated on census night was 29 389 150 inhabitants.
The intercensal annual growth rate was 2.9 per cent.

The urban population represented 52.7 per cent of the total, up from 47.1 per
cent at the previous census. Three regions account for more than half of all
urban residents.

Average household size was 4.2 persons nationally, ranging from 3.4 in the
capital region to 5.6 in the northern regions.

The sex ratio was 104 men per 100 women. The median age was 19.4 years.
""",
    "census-methodology-note.md": """\
# Census 2021 — Methodological note

> FICTIONAL DOCUMENT. Invented figures, imaginary Republic of Terrafrica.

Enumeration used tablet-based collection in all 42 districts, with paper
questionnaires retained as a contingency in areas without reliable power.

Non-response was adjusted using post-stratification weights calibrated to
projected population totals by region, sex and five-year age group.

Coverage error was estimated through a post-enumeration survey conducted six
weeks after the main operation, on a sample of 480 enumeration areas. Net
undercount was estimated at 2.1 per cent nationally.

Occupation was coded to ISCO-08 at the four-digit level. Fourteen per cent of
responses required manual review by a coding supervisor.
""",
    "labour-force-survey-2023-q4.md": """\
# Labour Force Survey — Fourth quarter 2023

> FICTIONAL DOCUMENT. Invented figures, imaginary Republic of Terrafrica.

The unemployment rate was 8.6 per cent, unchanged from the previous quarter.
Youth unemployment, for persons aged 15 to 24, stood at 19.2 per cent.

Informal employment represented 71.4 per cent of total employment outside
agriculture. The survey does not measure informal activity that takes place
entirely within the household.

The labour force participation rate was 63.8 per cent overall: 74.1 per cent for
men and 53.9 per cent for women.
""",
    "statistical-act-summary.md": """\
# Statistical Act — Summary of confidentiality provisions

> FICTIONAL DOCUMENT, describing an imaginary legal framework for teaching.

Individual data collected under this Act may be used for statistical purposes
only. It may not be communicated to any administrative, judicial or fiscal
authority, and may not be used as the basis for any individual decision.

Data identifying a respondent may not be transferred outside the national
territory without the written authorisation of the Statistical Council.

Aggregated results may be published where no cell permits the identification of
a respondent. A cell derived from fewer than three units is suppressed.

Staff and contractors are bound by statistical secrecy without time limit.
""",
    "dissemination-calendar-2024.md": """\
# Dissemination calendar 2024

> FICTIONAL DOCUMENT. Invented dates, imaginary Republic of Terrafrica.

Consumer price index: released on the twelfth working day following the
reference month.

Labour Force Survey: quarterly, released eight weeks after the end of the
reference quarter.

National accounts, annual estimates: provisional in June, semi-final the
following June, final after three years.

Census thematic reports: monthly through 2024, beginning with fertility and
mortality in March.
""",
}


def write_sample_corpus(path: str | Path) -> Path:
    """
    Write a small teaching corpus of fictional statistical publications.

    For participants whose own documents are not yet cleared for use, or who are
    on a network that will not carry a large download. Five short documents in
    the shapes a statistical office actually produces: a census results report, a
    methodological note, a survey bulletin, a legal summary and a calendar.

    Every file opens by declaring itself fictional. That is not decoration — a
    plausible sample corpus is how an invented number reaches a real publication.
    """
    out = Path(path)
    out.mkdir(parents=True, exist_ok=True)
    for name, body in _SAMPLE.items():
        (out / name).write_text(body, encoding="utf-8")
    return out


def save_transcript(answers: Sequence[Answer], path: str | Path, meta: dict | None = None
                    ) -> Path:
    """
    Write the answers, their passages and their provenance to JSON.

    This is the Friday deliverable. An answer without the passage it came from
    cannot be checked by anyone else, and an unpublishable assistant is one whose
    outputs nobody can audit.
    """
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "meta": meta or {},
        "answers": [a.to_dict() for a in answers],
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    return out
