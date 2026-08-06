#!/usr/bin/env python3
"""
STG17 · Derive editable PowerPoint decks from the reveal.js sources.

    pip install python-pptx
    python tools/build_pptx.py                # every deck, EN and FR
    python tools/build_pptx.py --only 08

Why this exists
---------------
The reveal.js decks are the source of truth: they are versioned, they publish to
the website, and they carry the SVG diagrams at full fidelity. But a facilitator
who wants to reorder two slides an hour before a session, or a country that wants
to adapt a deck for a national audience, will reach for PowerPoint. Refusing them
that is how a parallel, undocumented set of slides comes into existence.

So: PPTX is a *derived artefact*. Edit the deck source, rebuild. If someone edits
the PPTX directly, their changes are theirs — they do not flow back, and the file
says so on its final slide.

What survives the conversion
----------------------------
Headings, body text, bullet lists, tables, callouts and the AfDB colours all
convert. **SVG diagrams do not** — python-pptx cannot rasterise them. Each slide
that had one gets a placeholder naming the figure and telling the facilitator to
screenshot it from the HTML deck, which is a two-second operation and produces a
better result than any automatic conversion would.
"""

from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DECKS = ROOT / "slides" / "decks"
# Emitted into docs/ so that MkDocs copies them into the published site and
# they are downloadable from the slides page. They are NOT committed: they are
# derived binaries that would churn on every rebuild, so the Pages workflow
# regenerates them at deploy time.
OUT = ROOT / "docs" / "slides" / "pptx"

# Palette — kept in sync with stg17/theme.py by the CI check in build_all.py.
NAVY = (0x0B, 0x25, 0x45)
GREEN = (0x1B, 0x7A, 0x43)
AMBER = (0xF2, 0xA9, 0x00)
INK = (0x33, 0x40, 0x3A)
MUTED = (0x6B, 0x7B, 0x75)
WASH = (0xF4, 0xF8, 0xF5)

RE_META = re.compile(r"<!--meta(.*?)-->", re.S)
RE_SECTION = re.compile(r"<section\b([^>]*)>(.*?)</section>", re.S | re.I)
RE_EN = re.compile(r"<!--\s*EN\s*-->", re.I)
RE_FR = re.compile(r"<!--\s*FR\s*-->", re.I)
RE_END = re.compile(r"<!--\s*/(?:EN|FR)\s*-->", re.I)
RE_TAG = re.compile(r"<[^>]+>")


def text_of(fragment: str) -> str:
    """Strip tags and collapse whitespace, preserving nothing but the words."""
    return html.unescape(RE_TAG.sub(" ", fragment)).replace("\xa0", " ").strip()


def split_lang(fragment: str, lang: str) -> str:
    if not RE_EN.search(fragment) and not RE_FR.search(fragment):
        return fragment
    en, fr = RE_EN.search(fragment), RE_FR.search(fragment)
    if en and fr:
        head = fragment[: min(en.start(), fr.start())]
        body = fragment[fr.end():] if lang == "fr" else fragment[en.end(): fr.start()]
    elif en:
        head, body = fragment[: en.start()], (fragment[en.end():] if lang == "en" else "")
    else:
        head, body = fragment[: fr.start()], (fragment[fr.end():] if lang == "fr" else "")
    return head + RE_END.sub("", body)


def parse_slide(attrs: str, body: str) -> dict:
    """Reduce one <section> to the handful of things PowerPoint can carry."""
    classes = re.search(r'class="([^"]*)"', attrs)
    kind = (classes.group(1) if classes else "").strip()

    eyebrow = re.search(r'<div class="eyebrow"[^>]*>(.*?)</div>', body, re.S)
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", body, re.S)
    h2 = re.search(r"<h2[^>]*>(.*?)</h2>", body, re.S)

    bullets: list[str] = []
    for li in re.findall(r"<li[^>]*>(.*?)</li>", body, re.S):
        item = text_of(li)
        if item:
            bullets.append(item)

    callouts: list[tuple[str, str]] = []
    for cls, inner in re.findall(r'<div class="(key|warn)"[^>]*>(.*?)</div>', body, re.S):
        label = re.search(r"<b[^>]*>(.*?)</b>", inner, re.S)
        rest = re.sub(r"<b[^>]*>.*?</b>", "", inner, flags=re.S)
        callouts.append((text_of(label.group(1)) if label else "", text_of(rest)))

    tables: list[list[list[str]]] = []
    for table in re.findall(r"<table[^>]*>(.*?)</table>", body, re.S):
        rows = []
        for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", table, re.S):
            cells = [text_of(c) for c in re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>", tr, re.S)]
            if cells:
                rows.append(cells)
        if rows:
            tables.append(rows)

    metrics = []
    for block in re.findall(r'<div class="metrics"[^>]*>(.*?)</div>\s*</div>', body, re.S):
        for n, label in re.findall(r'<div class="n">(.*?)</div>\s*<div class="l">(.*?)</div>',
                                   block, re.S):
            metrics.append((text_of(n), text_of(label)))

    has_svg = "<svg" in body
    figcaption = re.search(r"<figcaption[^>]*>(.*?)</figcaption>", body, re.S)

    # Paragraph text that is not inside a callout, a table or a figure.
    stripped = re.sub(r"<(figure|table|div class=\"(key|warn|metrics)\").*?</\1>", "",
                      body, flags=re.S)
    paragraphs = [text_of(p) for p in re.findall(r"<p[^>]*>(.*?)</p>", stripped, re.S)]
    paragraphs = [p for p in paragraphs if p and len(p) > 3]

    return {
        "kind": kind,
        "eyebrow": text_of(eyebrow.group(1)) if eyebrow else "",
        "title": text_of(h1.group(1)) if h1 else (text_of(h2.group(1)) if h2 else ""),
        "subtitle": text_of(h2.group(1)) if (h1 and h2) else "",
        "bullets": bullets,
        "callouts": callouts,
        "tables": tables,
        "metrics": metrics,
        "paragraphs": paragraphs,
        "has_svg": has_svg,
        "figcaption": text_of(figcaption.group(1)) if figcaption else "",
    }


# ---------------------------------------------------------------------------
def build(source: Path, lang: str) -> Path:
    from pptx import Presentation
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from pptx.util import Emu, Inches, Pt

    raw = source.read_text(encoding="utf-8")
    meta = {}
    match = RE_META.search(raw)
    for line in (match.group(1).splitlines() if match else []):
        if ":" in line:
            key, _, value = line.partition(":")
            meta[key.strip()] = value.strip()

    body_html = RE_META.sub("", raw)
    slides = []
    for attrs, body in RE_SECTION.findall(body_html):
        lang_attr = re.search(r'data-lang="(\w+)"', attrs)
        if lang_attr and lang_attr.group(1).lower() != lang:
            continue
        slides.append(parse_slide(attrs, split_lang(body, lang)))

    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
    blank = prs.slide_layouts[6]
    W, H = prs.slide_width, prs.slide_height

    def rgb(t):
        return RGBColor(*t)

    def add_box(slide, left, top, width, height, text, size, colour, bold=False,
                align=PP_ALIGN.LEFT, wrap=True):
        box = slide.shapes.add_textbox(left, top, width, height)
        frame = box.text_frame
        frame.word_wrap = wrap
        para = frame.paragraphs[0]
        para.alignment = align
        run = para.add_run()
        run.text = text
        run.font.size = Pt(size)
        run.font.bold = bold
        run.font.color.rgb = rgb(colour)
        run.font.name = "Segoe UI"
        return frame

    for index, s in enumerate(slides):
        slide = prs.slides.add_slide(blank)
        is_title = "title" in s["kind"]
        is_divider = "divider" in s["kind"]
        is_night = "night" in s["kind"]

        # Background
        if is_title or is_divider or is_night:
            bg = slide.shapes.add_shape(1, 0, 0, W, H)   # 1 = rectangle
            bg.fill.solid()
            bg.fill.fore_color.rgb = rgb(NAVY if not is_night else (0x08, 0x09, 0x0F))
            bg.line.fill.background()
            bg.shadow.inherit = False
        else:
            rule = slide.shapes.add_shape(1, 0, 0, W, Emu(60000))
            rule.fill.solid()
            rule.fill.fore_color.rgb = rgb(AMBER)
            rule.line.fill.background()

        fg = (0xFF, 0xFF, 0xFF) if (is_title or is_divider or is_night) else NAVY
        body_fg = (0xDB, 0xE7, 0xE0) if (is_title or is_divider or is_night) else INK

        top = Inches(0.55)
        if s["eyebrow"]:
            add_box(slide, Inches(0.8), top, W - Inches(1.6), Inches(0.35),
                    s["eyebrow"].upper(), 11, AMBER if fg[0] == 0xFF else GREEN, bold=True)
            top += Inches(0.45)

        if s["title"]:
            add_box(slide, Inches(0.8), top, W - Inches(1.6), Inches(1.0),
                    s["title"], 34 if is_title else 28, fg, bold=True)
            top += Inches(1.05 if is_title else 0.95)

        if s["subtitle"]:
            add_box(slide, Inches(0.8), top, W - Inches(1.6), Inches(0.6),
                    s["subtitle"], 17, body_fg)
            top += Inches(0.7)

        for text in s["paragraphs"][:3]:
            add_box(slide, Inches(0.8), top, W - Inches(1.6), Inches(0.6), text, 14, body_fg)
            top += Inches(0.55)

        if s["metrics"]:
            line = "   ·   ".join(f"{n}  {label}" for n, label in s["metrics"])
            add_box(slide, Inches(0.8), top, W - Inches(1.6), Inches(0.5), line, 15, GREEN, bold=True)
            top += Inches(0.6)

        if s["bullets"]:
            box = slide.shapes.add_textbox(Inches(0.8), top, W - Inches(1.6),
                                           H - top - Inches(1.2))
            frame = box.text_frame
            frame.word_wrap = True
            for i, bullet in enumerate(s["bullets"][:9]):
                para = frame.paragraphs[0] if i == 0 else frame.add_paragraph()
                run = para.add_run()
                run.text = "•  " + bullet
                run.font.size = Pt(14)
                run.font.color.rgb = rgb(body_fg)
                run.font.name = "Segoe UI"
                para.space_after = Pt(7)
            top += Inches(0.4) * min(len(s["bullets"]), 9)

        for label, text in s["callouts"][:2]:
            height = Inches(1.05)
            if top + height > H - Inches(0.9):
                break
            panel = slide.shapes.add_shape(1, Inches(0.8), top, W - Inches(1.6), height)
            panel.fill.solid()
            panel.fill.fore_color.rgb = rgb(WASH)
            panel.line.color.rgb = rgb(GREEN)
            panel.shadow.inherit = False
            frame = panel.text_frame
            frame.word_wrap = True
            para = frame.paragraphs[0]
            run = para.add_run()
            run.text = (label.upper() + " — " if label else "") + text
            run.font.size = Pt(12)
            run.font.color.rgb = rgb(INK)
            run.font.name = "Segoe UI"
            top += height + Inches(0.15)

        for rows in s["tables"][:1]:
            n_rows = min(len(rows), 7)
            n_cols = max(len(r) for r in rows[:n_rows])
            height = Inches(0.32) * n_rows
            if top + height > H - Inches(0.9):
                break
            shape = slide.shapes.add_table(n_rows, n_cols, Inches(0.8), top,
                                           W - Inches(1.6), height)
            table = shape.table
            for r in range(n_rows):
                for c in range(n_cols):
                    cell = table.cell(r, c)
                    cell.text = rows[r][c] if c < len(rows[r]) else ""
                    para = cell.text_frame.paragraphs[0]
                    if para.runs:
                        para.runs[0].font.size = Pt(10)
                        para.runs[0].font.name = "Segoe UI"
                        para.runs[0].font.color.rgb = rgb((0xFF, 0xFF, 0xFF) if r == 0 else INK)
                        para.runs[0].font.bold = (r == 0)
            top += height + Inches(0.15)

        if s["has_svg"]:
            note = ("FIGURE — screenshot slide " + str(index + 1) +
                    " of the HTML deck and paste it here."
                    if lang == "en" else
                    "FIGURE — capturez la diapositive " + str(index + 1) +
                    " du deck HTML et collez-la ici.")
            if s["figcaption"]:
                note += "  (" + s["figcaption"] + ")"
            add_box(slide, Inches(0.8), min(top, H - Inches(1.3)), W - Inches(1.6),
                    Inches(0.7), note, 11, MUTED)

        # Footer
        footer = ("African Development Bank · AU STATAFRIC · STG17"
                  if lang == "en" else
                  "Banque africaine de développement · UA STATAFRIC · STG17")
        add_box(slide, Inches(0.8), H - Inches(0.5), W - Inches(1.6), Inches(0.3),
                footer, 9, MUTED if not (is_title or is_divider or is_night) else (0x6B, 0x7B, 0x75))

    # Final slide: say plainly that this file is derived.
    slide = prs.slides.add_slide(blank)
    bg = slide.shapes.add_shape(1, 0, 0, W, H)
    bg.fill.solid()
    bg.fill.fore_color.rgb = rgb(NAVY)
    bg.line.fill.background()
    bg.shadow.inherit = False
    warning = (
        "This PowerPoint file is generated from the reveal.js deck at\n"
        f"slides/decks/{source.name}\n\n"
        "Edits made here do not flow back. If your change should be permanent,\n"
        "edit the deck source and run:  python tools/build_slides.py && python tools/build_pptx.py"
        if lang == "en" else
        "Ce fichier PowerPoint est généré à partir du deck reveal.js\n"
        f"slides/decks/{source.name}\n\n"
        "Les modifications faites ici ne remontent pas. Si votre changement doit être permanent,\n"
        "modifiez la source et exécutez :  python tools/build_slides.py && python tools/build_pptx.py"
    )
    from pptx.enum.text import PP_ALIGN as _A
    add_box(slide, Inches(1.2), Inches(2.6), W - Inches(2.4), Inches(2.5),
            warning, 14, (0xDB, 0xE7, 0xE0), align=_A.CENTER)

    OUT.mkdir(parents=True, exist_ok=True)
    stem = source.name.replace(".deck.html", "")
    # Hyphen, not dot: mkdocs-static-i18n treats a `.fr.` segment as its own
    # language suffix for ANY file type, and would publish one collapsed file
    # instead of the two.
    path = OUT / f"{stem}-{lang}.pptx"
    prs.save(path)
    return path


def main() -> int:
    try:
        import pptx  # noqa: F401
    except ImportError:
        print("python-pptx is required:  pip install python-pptx")
        return 1

    parser = argparse.ArgumentParser(description="Derive PPTX decks from the reveal.js sources")
    parser.add_argument("--only", help="build only decks whose filename contains this")
    args = parser.parse_args()

    sources = sorted(DECKS.glob("*.deck.html"))
    if args.only:
        sources = [s for s in sources if args.only in s.name]
    if not sources:
        print("No deck sources found under slides/decks/.")
        return 0

    for source in sources:
        for lang in ("en", "fr"):
            path = build(source, lang)
            print(f"  {source.name:<44} -> {path.relative_to(ROOT)}")
    print(f"\n{len(sources)} deck source(s) · {len(sources) * 2} PPTX file(s).")
    print("Reminder: SVG diagrams are placeholders in PPTX — screenshot them from the HTML deck.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
