#!/usr/bin/env python3
"""
STG17 · Build the reveal.js decks from their bilingual sources.

    python tools/build_slides.py             # build every deck, EN and FR
    python tools/build_slides.py --only 08

Same principle as `build_notebooks.py`, and for the same reason: twelve decks in
two languages is twenty-four files, and twenty-four hand-maintained files drift.

--------------------------------------------------------------------------
THE DECK SOURCE FORMAT
--------------------------------------------------------------------------
A source is `slides/decks/<id>.deck.html` — a fragment, not a full document.
The wrapper (doctype, reveal.js, theme, footer, initialisation) is added here.

A front-matter comment carries the metadata:

    <!--meta
    id: 08
    title_en: Night-Time Lights - What the Darkness Tells Us
    title_fr: Lumières nocturnes - Ce que l'obscurité nous dit
    session_en: Day 4 · 09:00-09:30
    session_fr: Jour 4 · 09h00-09h30
    duration: 30
    -->

Bilingual text uses the same markers as the notebook masters:

    <!--EN-->English<!--FR-->Français<!--/FR-->

Inside a `<section>`, blocks may be marked with `data-lang="en"` / `"fr"` to keep
whole slides in one language only — useful for a slide whose figure has baked-in
labels.

Output: `docs/slides/<id>-<slug>.en.html` and `.fr.html`, served by the site and
therefore reachable from the agenda pages.
"""

from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DECKS = ROOT / "slides" / "decks"
OUT = ROOT / "docs" / "slides"
THEME = ROOT / "slides" / "theme"

RE_META = re.compile(r"<!--meta(.*?)-->", re.S)
RE_EN = re.compile(r"<!--\s*EN\s*-->", re.I)
RE_FR = re.compile(r"<!--\s*FR\s*-->", re.I)
RE_END = re.compile(r"<!--\s*/(?:EN|FR)\s*-->", re.I)
RE_SECTION = re.compile(r"(<section\b.*?</section>)", re.S | re.I)
RE_LANG_ATTR = re.compile(r'<section\b[^>]*\bdata-lang="(\w+)"', re.I)

REVEAL_VERSION = "5.1.0"
CDN = f"https://cdn.jsdelivr.net/npm/reveal.js@{REVEAL_VERSION}"

TEMPLATE = """<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
<title>{title} · STG17</title>
<meta name="description" content="{session} — STG17 workshop, AfDB / AU STATAFRIC">
<link rel="stylesheet" href="{reveal}/dist/reset.css">
<link rel="stylesheet" href="{reveal}/dist/reveal.css">
<link rel="stylesheet" href="theme/_afdb-vars.css">
<link rel="stylesheet" href="theme/afdb.css">
<link rel="stylesheet" href="{reveal}/plugin/highlight/monokai.css">
</head>
<body class="no-reveal">
<div class="reveal">
  <div class="slides">
{slides}
  </div>
</div>
<div class="footer">
  <span class="brand">African Development Bank · AU STATAFRIC · STG17</span>
  <span>{session}</span>
</div>

<script src="{reveal}/dist/reveal.js"></script>
<script src="{reveal}/plugin/notes/notes.js"></script>
<script src="{reveal}/plugin/highlight/highlight.js"></script>
<script>
// If the CDN is unreachable — a real possibility on the networks this workshop
// runs on — Reveal is undefined and the body keeps its `no-reveal` class, so the
// deck renders as a long scrollable document instead of a blank page.
if (typeof Reveal !== 'undefined') {{
  document.body.classList.remove('no-reveal');
  Reveal.initialize({{
    hash: true,
    slideNumber: 'c/t',
    controls: true,
    progress: true,
    center: false,
    transition: 'fade',
    transitionSpeed: 'fast',
    width: 1280,
    height: 720,
    margin: 0.045,
    minScale: 0.2,
    maxScale: 1.6,
    plugins: [ RevealNotes, RevealHighlight ]
  }});
}} else {{
  console.warn('reveal.js could not be loaded — falling back to document mode.');
}}
</script>
</body>
</html>
"""


def parse_meta(text: str) -> dict:
    match = RE_META.search(text)
    if not match:
        raise SystemExit("Deck source has no <!--meta ... --> block.")
    meta = {}
    for line in match.group(1).splitlines():
        line = line.strip()
        if not line or ":" not in line:
            continue
        key, _, value = line.partition(":")
        meta[key.strip()] = value.strip()
    return meta


def split_lang(fragment: str, lang: str, where: str = "") -> str:
    """Keep one language's text. Same convention as the notebook masters."""
    if not RE_EN.search(fragment) and not RE_FR.search(fragment):
        return fragment
    for pattern, label in ((RE_EN, "<!--EN-->"), (RE_FR, "<!--FR-->")):
        if len(pattern.findall(fragment)) > 1:
            raise SystemExit(
                f"{where}: {label} appears more than once in one slide. "
                f"Split the slide, or move the stray block."
            )
    en_match, fr_match = RE_EN.search(fragment), RE_FR.search(fragment)
    if en_match and fr_match:
        head = fragment[: min(en_match.start(), fr_match.start())]
        chosen = (fragment[fr_match.end():] if lang == "fr"
                  else fragment[en_match.end(): fr_match.start()])
    elif en_match:
        head = fragment[: en_match.start()]
        chosen = fragment[en_match.end():] if lang == "en" else ""
    else:
        head = fragment[: fr_match.start()]
        chosen = fragment[fr_match.end():] if lang == "fr" else ""
    return head + RE_END.sub("", chosen)


def build(source: Path, lang: str) -> tuple[Path, str]:
    raw = source.read_text(encoding="utf-8")
    meta = parse_meta(raw)
    body = RE_META.sub("", raw)

    kept = []
    for index, part in enumerate(RE_SECTION.split(body)):
        if not part.strip():
            continue
        if not part.lstrip().lower().startswith("<section"):
            continue  # whitespace or stray text between sections
        lang_attr = RE_LANG_ATTR.search(part)
        if lang_attr and lang_attr.group(1).lower() != lang:
            continue

        # Split only the INNER body, then put the wrapper back.
        #
        # Splitting the whole <section>…</section> string would truncate the
        # English build at the <!--FR--> marker and take the closing </section>
        # with it, because that tag sits after the French block. Browsers recover
        # from unclosed sections by nesting them, so reveal.js still shows
        # something — which is exactly why this survived a visual check. The
        # French build was unaffected, its text running to the end of the string.
        open_tag = re.match(r"<section\b[^>]*>", part, re.I)
        assert open_tag, "RE_SECTION matched something that is not a <section>"
        inner = part[open_tag.end():]
        close = ""
        if inner.rstrip().lower().endswith("</section>"):
            cut = inner.rstrip()[: -len("</section>")]
            close = inner[len(cut):]
            inner = cut
        kept.append(open_tag.group(0)
                    + split_lang(inner, lang, where=f"{source.name} slide {index}")
                    + close)

    title = meta.get(f"title_{lang}", meta.get("title_en", ""))
    session = meta.get(f"session_{lang}", meta.get("session_en", ""))
    html = TEMPLATE.format(
        lang=lang, title=title, session=session, reveal=CDN,
        slides="\n".join(kept),
    )
    # Hyphen, not dot, before the language code: mkdocs-static-i18n treats a
    # `.fr.` segment as its own suffix convention and would publish only one
    # of the two decks per language build, breaking every cross-language link.
    out_path = OUT / f"{meta['id']}-{slugify(meta.get('title_en', meta['id']))}-{lang}.html"
    return out_path, html


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    return re.sub(r"-+", "-", text)[:48]


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the STG17 reveal.js decks")
    parser.add_argument("--only", help="build only decks whose filename contains this")
    parser.add_argument("--offline", action="store_true",
                        help="point at slides/vendor/ instead of the CDN "
                             "(run tools/vendor_reveal.py first)")
    args = parser.parse_args()

    global CDN
    if args.offline:
        if not (ROOT / "slides" / "vendor" / "dist" / "reveal.js").exists():
            print("slides/vendor/ is empty. Run:  python tools/vendor_reveal.py")
            return 1
        CDN = "../../slides/vendor"
        print("Offline mode: decks will load reveal.js from slides/vendor/.")

    OUT.mkdir(parents=True, exist_ok=True)
    # The reveal theme needs the generated variables file next to it in docs/,
    # because the published pages resolve ../../slides/theme/ relative to the site.
    sources = sorted(DECKS.glob("*.deck.html"))
    if args.only:
        sources = [s for s in sources if args.only in s.name]
    if not sources:
        print("No deck sources found under slides/decks/.")
        return 0

    written = 0
    warnings: list[str] = []
    broken: list[str] = []
    for source in sources:
        built = {}
        for lang in ("en", "fr"):
            path, html = build(source, lang)
            path.write_text(html, encoding="utf-8")
            built[lang] = html
            written += 1
            print(f"  {source.name:<44} -> {path.name}")
            broken.extend(check_stylesheets(html, path))
            over, dense = check_density(source, html, lang)
            broken.extend(over)
            warnings.extend(dense)
        warnings.extend(check_symmetry(source, built))

    if warnings:
        print("\nAsymmetries between the English and French builds:")
        for warning in warnings:
            print("   !", warning)
        print("  These are authoring omissions, not build failures — the decks are usable.")

    # A broken stylesheet path is fatal, unlike an asymmetry. An unstyled deck
    # still renders — reveal.js loads from the CDN — so nothing errors and the
    # slides advance normally. It just looks like a browser default. That is not
    # a usable deck in front of a room, and it must not reach one.
    if broken:
        print("\nBroken stylesheet references:")
        for problem in broken:
            print("   x", problem)
        return 1

    print(f"\n{len(sources)} deck source(s) · wrote {written} file(s).")
    return 0


def check_stylesheets(html: str, out_path: Path) -> list[str]:
    """
    Verify every local stylesheet the deck references actually resolves on disk.

    A missing theme file does not fail loudly: reveal.js loads from the CDN and
    renders the slides, so the deck *works* — it is just unstyled, in the browser
    default serif, with none of the AfDB identity. That looks like a design
    problem rather than a broken path, which is exactly how it survives review.

    The original bug: the theme lived outside `docs/`, so MkDocs never copied it
    into the site, and the href climbed two directories above the site root.
    """
    issues = []
    for href in re.findall(r'<link[^>]+href="([^"]+\.css)"', html):
        if href.startswith(("http://", "https://", "//")):
            continue  # CDN — reachability is a network question, not a path one
        target = (out_path.parent / href).resolve()
        if not target.exists():
            issues.append(
                f"{out_path.name}: stylesheet {href!r} resolves to {target}, which does "
                f"not exist — the deck will render unstyled without any error"
            )
        elif ROOT / "docs" not in target.parents:
            issues.append(
                f"{out_path.name}: stylesheet {href!r} resolves outside docs/ "
                f"({target}) — MkDocs will not publish it"
            )
    return issues


#: A slide is read at four metres by someone who is also listening. Past roughly
#: this many words it stops being a slide and becomes a projected document — the
#: type must shrink to fit, and the audience reads instead of listening.
#: Measured on visible text only: speaker notes and SVG labels are excluded,
#: because notes are what the presenter *says* and are meant to be long.
WORD_BUDGET = 75
WORD_LIMIT = 110
TABLE_ROW_LIMIT = 6          # header + five data rows


def visible_text(section_html: str) -> str:
    """The words an audience actually reads, with notes and diagram labels removed."""
    body = re.sub(r"<aside class=\"notes\">.*?</aside>", "", section_html, flags=re.S)
    body = re.sub(r"<svg.*?</svg>", "", body, flags=re.S)
    body = re.sub(r"<div class=\"src\">.*?</div>", "", body, flags=re.S)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", body)).strip()


def check_density(source: Path, html: str, lang: str) -> tuple[list[str], list[str]]:
    """
    Flag slides carrying more than an audience can read while listening.

    Returns (fatal, advisory). Over WORD_LIMIT is fatal: that slide will be
    unreadable on a projector no matter how the CSS is tuned, and shipping it is
    worse than shipping nothing. Between WORD_BUDGET and WORD_LIMIT is advisory —
    a dense-but-defensible reference slide exists, and a build that refuses to run
    over a judgement call is a build people route around.
    """
    fatal, advisory, grounds = [], [], []
    for index, match in enumerate(
        re.finditer(r"<section\b([^>]*)>(.*?)</section>", html, re.S), start=1
    ):
        attrs, section = match.group(1), match.group(2)
        words = len(visible_text(section).split())
        heading = re.search(r"<h[12][^>]*>(.*?)</h[12]>", section, re.S)
        title = re.sub(r"<[^>]+>", "", heading.group(1)).strip()[:44] if heading else "(divider)"
        where = f"{source.name} [{lang}] slide {index} — {title!r}"

        # A slide marked `appendix` is a bibliography: it exists so the *published*
        # deck works as a reading list, and nobody is expected to read it from the
        # back of a room. It is still reported, so the exemption cannot quietly
        # become the place overflow prose goes to hide.
        if "appendix" in attrs:
            advisory.append(f"{where}: {words} words — appendix, exempt from the "
                            f"projection limit. Keep it a reference list, not an argument.")
        elif words > WORD_LIMIT:
            fatal.append(f"{where}: {words} words (limit {WORD_LIMIT}). "
                         f"Split it, or move the prose into <aside class=\"notes\">.")
        elif words > WORD_BUDGET:
            advisory.append(f"{where}: {words} words (budget {WORD_BUDGET})")

        rows = len(re.findall(r"<tr", section))
        if rows > TABLE_ROW_LIMIT:
            fatal.append(f"{where}: table has {rows} rows (limit {TABLE_ROW_LIMIT}). "
                         f"Keep the rows that change a decision; drop the rest.")

        callouts = len(re.findall(r'class="(?:key|warn)"', section))
        if callouts > 1:
            advisory.append(f"{where}: {callouts} callouts — two callouts is two ideas, "
                            f"which is two slides")

        fatal.extend(check_visual(attrs, section, where))
        grounds.append(any(c in attrs for c in COLOURED_SECTIONS))

    advisory.extend(check_rhythm(grounds, source, lang))
    return fatal, advisory


#: Sections that put something other than white behind the content.
COLOURED_SECTIONS = ("title", "divider", "night", "split", "bleed", "jade", "tint")
WHITE_RUN_LIMIT = 3


def check_rhythm(grounds: list[bool], source: Path, lang: str) -> list[str]:
    """
    Flag a stretch of consecutive white slides.

    No single white slide is a fault. Four in a row is: the audience stops
    perceiving slide changes, and the deck reads as one long scrolling page.
    A divider, a `split` panel or a `tint` ground breaks the run and costs
    nothing — not a word, not a minute.
    """
    out, run, start = [], 0, 0
    for i, coloured in enumerate(grounds + [True]):
        if coloured:
            if run > WHITE_RUN_LIMIT:
                out.append(f"{source.name} [{lang}] slides {start + 1}–{i}: {run} white "
                           f"slides in a row. Break the run — a divider, a `split` panel "
                           f"or a `tint` ground.")
            run = 0
        else:
            if run == 0:
                start = i
            run += 1
    return out


#: Anything that gives a slide weight the audience reads before the words:
#: a drawn figure, a colour field, a numeral at size, a set of cards.
VISUAL_ELEMENTS = (
    "<svg", "<img", "figure-slot",
    'class="metrics"', 'class="findings"', 'class="statement"', 'class="steps"',
    'class="compare"', 'class="chips"', 'class="hero-n"', 'class="quote"',
    'class="terms"', "<table",
)
#: Section classes that ARE the visual treatment.
VISUAL_SECTIONS = ("title", "divider", "night", "split", "bleed", "jade", "tint", "appendix")


def check_visual(attrs: str, section: str, where: str) -> list[str]:
    """
    Refuse a slide that is bare text on a white ground.

    The density guard above made slides short. Short is not the same as
    designed: a heading, two sentences and a callout on white is a well-set
    paragraph, and a deck of them reads as a document that happens to paginate.

    Every content slide must carry one of: a drawn figure, a colour field, a
    numeral at size, or a card set. None of those costs a single word — which
    is the point, because the word budget stays where it is.
    """
    if any(cls in attrs for cls in VISUAL_SECTIONS):
        return []
    if any(marker in section for marker in VISUAL_ELEMENTS):
        return []
    return [
        f"{where}: bare text on white. Give it visual weight — a figure, a "
        f"`split` colour panel, a `hero-n` numeral, `steps`, `compare`, `chips`, "
        f"or set the section to `tint`, `jade` or `night`. None of these adds words."
    ]


def check_symmetry(source: Path, built: dict[str, str]) -> list[str]:
    """
    Compare the two language builds and report anything present in one only.

    A bilingual deck is meant to be the same deck twice. When a slide, a speaker
    note or a source line exists in English and not in French, the French
    audience silently gets less — and nothing fails, so nobody notices. This
    check is what turns that into a visible line in the build output.

    Reported, not fatal: an author may legitimately give one language an extra
    slide (a national example, a note about interpretation), and a build that
    refuses to run over a judgement call is a build people stop using.
    """
    issues = []
    counts = {}
    for lang, html in built.items():
        sections = re.findall(r"<section\b[^>]*>(.*?)</section>", html, re.S)
        opens, closes = len(re.findall(r"<section\b", html)), len(re.findall(r"</section>", html))
        if opens != closes:
            issues.append(f"{source.name} [{lang}]: {opens} <section> but {closes} </section> "
                          f"— the deck will render with nested slides")
        counts[lang] = {
            "slides": len(sections),
            "notes": sum(1 for s in sections if 'aside class="notes"' in s),
            "sources": sum(1 for s in sections if 'class="src"' in s),
            "figures": sum(1 for s in sections if "<svg" in s),
        }

    labels = {"slides": "slides", "notes": "speaker notes",
              "sources": "source lines", "figures": "figures"}
    for key, label in labels.items():
        en, fr = counts["en"][key], counts["fr"][key]
        if en != fr:
            issues.append(f"{source.name}: {en} {label} in English, {fr} in French")
    return issues


if __name__ == "__main__":
    sys.exit(main())
