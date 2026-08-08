#!/usr/bin/env python3
"""
STG17 · Write ready-to-paste prompts for building the PowerPoint decks in Claude web.

    python tools/pptx_prompt.py            # every existing deck + the generator
    python tools/pptx_prompt.py 02         # just deck 02
    python tools/pptx_prompt.py --copy 02  # and put it on the clipboard

Output goes to `prompts-pptx/` — deliberately OUTSIDE `docs/`, so MkDocs never
sees it and none of this is published. These are working files.

--------------------------------------------------------------------------
WHY THE PROMPT CARRIES THE HTML RATHER THAN A PARSED SUMMARY
--------------------------------------------------------------------------
`build_pptx.py` tried to translate slides into PowerShapes automatically and
dropped the body of every slide: the opening slide of deck 01 carries three
quoted sentences in the HTML and twenty words in the PPTX. The lesson is that the
lossy step is the parser, not the format.

So this tool does almost no interpretation. It hands Claude the deck's own
`<section>` markup, plus a legend mapping each CSS class to a PowerPoint
archetype, and lets a model that reads HTML well do the layout. The only thing it
rewrites is `<svg>`, which becomes a labelled placeholder — because a diagram
redrawn from its description loses the meaning it was drawn to carry.
"""

from __future__ import annotations

import argparse
import importlib.util
import re
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DECKS = ROOT / "slides" / "decks"
OUT = ROOT / "prompts-pptx"

sys.path.insert(0, str(ROOT))
from stg17 import theme  # noqa: E402


def _bs():
    spec = importlib.util.spec_from_file_location(
        "_bs", Path(__file__).resolve().parent / "build_slides.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


BS = _bs()


# ===========================================================================
#  The design specification — shared by both prompts
# ===========================================================================
SPEC = f"""
# THE STANDARD

I am not asking for acceptable slides. I am asking for a deck that would pass as
the work of a design studio commissioned by a development bank, and that a
minister would not be embarrassed to sit through.

Three things most generated decks fail, so check yourself against them:

  1. EVERY SLIDE HAS A VISUAL IDEA, not only a verbal one. A title with two
     paragraphs under it is a page, not a slide. If a slide's only content is
     prose, you have not finished designing it — give it a colour panel, a
     numeral, a card row or a table.

  2. THE DECK HAS RHYTHM. White, white, white, white reads as one long document
     and the audience stops noticing that anything changed. Never more than three
     consecutive white slides; aim for roughly a third of the deck carrying a
     full colour field.

  3. TYPE DOES THE WORK. One family, a wide size range, decisive weight
     contrast. A 46pt numeral beside 14pt supporting text carries more than any
     decoration. Nothing is centred except the title slide.

# VISUAL REGISTER — editorial-graphic

Flat colour fields, oversized numerals, strong typography, clean tables.

  NOT: stock photography, clip art, icon fonts, emoji, WordArt.
  NOT: gradients other than the title slide, text shadows, glows, 3-D, bevels.
  NOT: rounded-everything. Panels 10-14pt radius; full colour fields square.

It must read on a badly calibrated projector in a lit room, print legibly in
black and white, and not look dated in ten years.

# PALETTE — these seven values and no eighth

  NAVY  0B2545   structure, colour fields, headings, authority
  JADE  1B7A43   primary accent, the normal path, rules
  AMBER F2A900   the ONE element the eye should find; warnings
  INK   33403A   body text
  MUTED 6B7B75   captions, secondary text, source lines
  LINE  D5E6DF   hairlines and table borders
  WASH  F4F8F5   tinted ground and panel fill

Amber is scarce by design: if two things on a slide are amber, neither is
emphasised. Never carry meaning by colour alone — a colour-blind viewer and a
monochrome printout must both still work.

# TYPE SCALE — use these, invent no intermediate sizes

  Font: Segoe UI throughout. No serif anywhere.

  Deck title      54pt bold        Slide title      32pt bold, NAVY, with a 3pt
  Statement       42pt bold                         AMBER rule directly beneath
  Hero numeral    92pt bold JADE   Body             20pt, INK
  Card title      17pt bold        Card body        14pt
  Table cell      15pt             Table header     15pt bold, white on NAVY
  Source line     11pt MUTED       Footer           10pt MUTED

  Minimum anywhere: 11pt. DISABLE autofit shrink everywhere. If text does not fit
  at these sizes the content is too long — but the content is fixed here, so
  instead reduce the slide's padding or split the shape. Silently shrinking text
  is the clearest signature of an amateur deck.

# CANVAS AND FOOTER

  16:9 widescreen, 13.333 x 7.5 inches.
  Margins: left/right 0.8", top 0.6", bottom 0.9".
  Reserve the bottom 0.55" for the footer; no content enters it.

  Footer on every slide except the title: a 2pt AMBER rule across the content
  width, and beneath it — left, "African Development Bank · AU STATAFRIC · STG17"
  in NAVY bold 10pt; right, the slide number in MUTED 10pt.

# ARCHETYPES — build each slide as one of these

  TITLE       full-bleed NAVY, AMBER eyebrow in caps 12pt, title 54pt white,
              subtitle 24pt at 80% white, metadata block bottom left 13pt
  DIVIDER     solid NAVY, deliberately almost empty: eyebrow, title 44pt white
              with an AMBER rule, one line of body in a pale blue-grey
  STATEMENT   white ground, one sentence 42pt in the upper half with two or three
              words in JADE, a qualifier beneath at 17pt MUTED, nothing else
  SPLIT       a NAVY, JADE or AMBER rectangle over the left ~40% carrying the
              eyebrow and title in white, the content in the remaining 60%
  TABLE       header row NAVY with white text, body rows alternating white and
              WASH, a 1pt LINE rule under each row, NO VERTICAL BORDERS AT ALL,
              cells top-aligned and left-aligned
  METRICS     2-4 white cards in a row, 1pt LINE border, a 4pt JADE bar across
              the top, then numeral 46pt / label 13pt bold / qualifier 11pt
  STEPS       3-5 cards, numeral 46pt JADE, title 17pt, two lines at 14pt, a 5pt
              top bar — AMBER on the last card
  COMPARE     two panels on WASH with a 5pt top bar: MUTED or red left, JADE right
  CALLOUT     a WASH panel (or FEF9EC for a warning) with a 6pt left bar in the
              accent colour, label in 13pt caps, body 18pt
  HERO NUMBER one numeral 92pt with its unit beside it at 35pt MUTED, and a
              caption of at most two lines
  FIGURE      see FIGURES below
  CLOSING     NAVY ground, what happens next. No "Thank you", no "Questions?"
""".strip()


LEGEND = """
# HOW TO READ THE SOURCE BELOW

Each slide is given as the HTML this workshop authors its decks in. The class
names tell you which archetype to build:

  <section class="title">      -> TITLE            <div class="statement">  -> STATEMENT
  <section class="divider">    -> DIVIDER          <div class="key">        -> CALLOUT, jade
  <section class="split">      -> SPLIT            <div class="warn">       -> CALLOUT, amber
  <section class="jade">       -> full JADE field   <div class="metrics">    -> METRICS
  <section class="night">      -> near-black field  <div class="steps">      -> STEPS
  <section class="tint">       -> WASH ground       <div class="compare">    -> COMPARE
  <section class="bleed">      -> FIGURE, full width<div class="findings">   -> 2 evidence cards
  <section class="appendix">   -> reference list    <div class="terms">      -> 2-column glossary
                                                    <div class="chips">      -> pill labels
  <div class="eyebrow">  the kicker above the title    <div class="hero-n">   -> HERO NUMBER
  <p class="statement-sub"> the qualifier under a statement
  <div class="src">      the source line, 11pt MUTED at the foot of the slide
  <div class="panel">    inside a split: the colour side. is-jade / is-amber change its colour
  <div class="body">     inside a split: the content side
  <span class="timing">  presenter-only. DO NOT put this on the slide.
  <aside class="notes">  the speaker notes. These go in the NOTES PANE, never on the slide face.

Inside <div class="metrics"> and <div class="steps">, the inner classes are:
  .n / .i = the number, .l / .t = the label or title, .s / .d = the qualifier.
""".strip()


FIGURES = """
# FIGURES — do not invent them

Where the source contains [FIGURE: ...], the original slide carries a hand-drawn
diagram that cannot be transferred. Insert a placeholder: a rectangle at the full
content width, 2.6 inches high, WASH fill, dashed LINE border, with the figure's
description centred in MUTED 13pt.

Do NOT attempt to redraw the diagram with PowerPoint shapes or SmartArt. A
diagram guessed from its description loses the meaning it was drawn to carry, and
looks worse than an honest gap.

At the end, list every placeholder so I know which figures to screenshot from the
HTML deck and drop in.
""".strip()


BILINGUAL = """
# TWO FILES, ONE PASS

Build BOTH language versions: `{stem}-en.pptx` and `{stem}-fr.pptx`.

Write ONE script. Put the content in a single list of slide dictionaries, each
holding both languages, then loop over ('en', 'fr') and write two files. Do not
write the deck out twice — two copies of the same structure drift the moment one
is edited.

The French is not a translation to be produced now; it is given in the source
below and must be used verbatim. French typographic rules already applied there —
« guillemets », a space before : ; ! ?, 09h30 not 09:30, decimal commas — must be
preserved exactly. Do not "correct" them.

Where a French text block is longer than its English counterpart, reduce the
padding rather than the font size.
""".strip()


HOW = """
# HOW TO PRODUCE IT

Write Python using python-pptx, run it, and give me the two .pptx files to
download. Build on the blank layout (`prs.slide_layouts[6]`) and place every
shape explicitly — the built-in title and content placeholders carry theme
formatting that cannot be fully overridden.

Set `shape.shadow.inherit = False` on every shape you create. python-pptx
inherits a theme shadow otherwise, which is invisible on screen and looks smeared
on a projector.

Put the palette, the type scale and the margins in module-level constants, and
write one function per archetype, so the deck at the bottom of the script reads
as a list of calls.

# BEFORE YOU FINISH, VERIFY AND REPORT

  1. Slide count matches the source, in both languages.
  2. No slide face carries more than 110 words.
  3. No table over 6 rows including the header.
  4. No font below 11pt, and no autofit shrink anywhere.
  5. Speaker notes present on every slide that has them in the source.
  6. No colour outside the seven listed.
  7. Every [FIGURE: ...] placeholder listed for me.

Fix anything that fails before you output — do not output and then note it.
""".strip()


# ===========================================================================
#  Turning a deck source into promptable content
# ===========================================================================
RE_SVG = re.compile(r"<figure>\s*<svg\b[^>]*?aria-label=\"(.*?)\".*?</svg>(.*?)</figure>", re.S)
RE_SVG_BARE = re.compile(r"<svg\b[^>]*?aria-label=\"(.*?)\".*?</svg>", re.S)
RE_FIGCAP = re.compile(r"<figcaption>(.*?)</figcaption>", re.S)


def strip_svg(html: str) -> str:
    """Replace each diagram with a description a human can act on."""
    def one(match: re.Match) -> str:
        label = re.sub(r"\s+", " ", match.group(1)).strip()
        caption = ""
        cap = RE_FIGCAP.search(match.group(2) if match.lastindex and match.lastindex > 1 else "")
        if cap:
            caption = " | CAPTION: " + re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", cap.group(1))).strip()
        return f"[FIGURE: {label}{caption}]"

    def bare(match: re.Match) -> str:
        # An <svg> not wrapped in <figure>. Rare, but the pattern is allowed, and
        # a label spanning two source lines must still collapse to one line.
        return f"[FIGURE: {re.sub(r'\s+', ' ', match.group(1)).strip()}]"

    return RE_SVG_BARE.sub(bare, RE_SVG.sub(one, html))


def deck_sections(source: str, lang: str) -> list[str]:
    """One language's <section> blocks, SVGs replaced, in order."""
    body = BS.RE_META.sub("", source)
    out = []
    for part in BS.RE_SECTION.split(body):
        if not part.lstrip().lower().startswith("<section"):
            continue
        attr = BS.RE_LANG_ATTR.search(part)
        if attr and attr.group(1).lower() != lang:
            continue
        open_tag = re.match(r"<section\b[^>]*>", part, re.I)
        inner = part[open_tag.end():]
        close = ""
        if inner.rstrip().lower().endswith("</section>"):
            cut = inner.rstrip()[: -len("</section>")]
            close, inner = inner[len(cut):], cut
        out.append(strip_svg(open_tag.group(0) + BS.split_lang(inner, lang) + close))
    return out


def existing_decks() -> dict[str, Path]:
    found = {}
    for path in sorted(DECKS.glob("*.deck.html")):
        meta = BS.parse_meta(path.read_text(encoding="utf-8"))
        found[meta["id"]] = path
    return found


def agenda() -> dict:
    return yaml.safe_load((ROOT / "config" / "agenda.yml").read_text(encoding="utf-8"))


# ===========================================================================
#  Prompt 1 — an existing deck, content given verbatim
# ===========================================================================
def prompt_for_deck(deck_id: str, path: Path) -> tuple[str, str]:
    source = path.read_text(encoding="utf-8")
    meta = BS.parse_meta(source)
    stem = path.name.replace(".deck.html", "")
    en, fr = deck_sections(source, "en"), deck_sections(source, "fr")

    slides = []
    for i, (e, f) in enumerate(zip(en, fr), start=1):
        slides.append(
            f"\n{'=' * 74}\nSLIDE {i} of {len(en)}\n{'=' * 74}\n"
            f"\n--- ENGLISH ---\n{e.strip()}\n\n--- FRANÇAIS ---\n{f.strip()}\n"
        )

    text = f"""You are building a PowerPoint deck for the African Development Bank and AU
STATAFRIC, for the STG17 workshop on artificial intelligence for official
statistics.

The content is FIXED and given in full below. It has been written, reviewed and
its references checked. Your job is the design and the layout — not the content.

  Do not add slides. Do not remove slides. Do not reword a claim.
  Do not add a citation, a statistic or an example that is not below.
  Do not "improve" anything. If something reads oddly, leave it.

Deck: {meta.get('title_en', '')}
Session: {meta.get('session_en', '')} · {meta.get('duration', '?')} minutes
Audience: heads of statistical methodology and IT at African national statistical
offices — expert statisticians, non-expert in machine learning, many working in
their second or third language.

{SPEC}

{BILINGUAL.format(stem=stem)}

{LEGEND}

{FIGURES}

{HOW}

{'#' * 74}
# THE DECK — {len(en)} slides, English and French
{'#' * 74}
{''.join(slides)}
{'=' * 74}
END OF DECK. Build both files now.
"""
    return f"deck-{deck_id}.txt", text


# ===========================================================================
#  Prompt 2 — a deck that does not exist yet
# ===========================================================================
def prompt_generator(sessions: list[tuple[dict, dict]]) -> tuple[str, str]:
    lines = []
    for session, day in sessions:
        lines.append(
            f"  {session['deck']} · Day {day['n']} · {session['time']} · "
            f"{session.get('mode', 'talk')}\n"
            f"     EN: {session.get('title_en', '')}\n"
            f"     FR: {session.get('title_fr', '')}\n"
            f"     Scope: {session.get('desc_en', '')}\n"
            f"     STG17 Action Plan: {session.get('plan', '')}\n"
        )

    text = f"""You are writing AND designing a PowerPoint deck for the African Development Bank
and AU STATAFRIC, for the STG17 workshop on artificial intelligence for official
statistics.

Unlike the other prompts in this folder, the content does not exist yet. You are
writing it as well as laying it out.

# CHOOSE ONE SESSION

Tell me which of these you are building, then build it. If I named one in my
message, build that one.

{chr(10).join(lines)}
Audience: heads of statistical methodology and IT at African national statistical
offices — expert statisticians, non-expert in machine learning, many working in
their second or third language. They are decision-makers: they specify, procure
and defend what their office builds.

# CONTENT RULES — these matter more than the design

1. ONE IDEA PER SLIDE, at most 110 visible words, aiming for 75. Everything else
   you want to say goes in the speaker notes: 80-150 words per slide, full
   sentences, second person, including at least one delivery instruction
   ("pause here", "ask for a show of hands", "do not read the table aloud").

2. TIMING. Budget 90 seconds per content slide, 20 seconds per divider, 3 minutes
   for a slide with a figure the audience must read. Fit the session length with
   slack, and state your arithmetic.

3. OPEN CONCRETELY. Start with an artefact from the audience's working life — a
   sentence from real terms of reference, a line from a published table. Never
   open with definitions or an agenda slide. Close with what happens next in the
   workshop, never with "Thank you".

4. STRUCTURE IN PARTS. Two to four parts, each opened by a divider slide stating
   what the part is for.

5. ONE ABSOLUTE. Somewhere include a single slide stating the line this material
   does not cross — what the audience must not do with what they have learned.

6. EVIDENCE, AND NO INVENTION. Every number and claim carries a source: authors,
   year, journal or institution. If you are not certain a reference exists exactly
   as you would write it, put

       [UNVERIFIED — need: <the shape of the evidence required>]

   on the slide instead. Do NOT produce a plausible-looking citation. This deck is
   shown to statisticians under an AfDB banner; a fabricated DOI costs more than
   an empty slot. I will supply what is missing.

7. TITLES ARE CLAIMS, not topics. "Fine-tuning teaches style, not facts", never
   "About fine-tuning".

# BOTH LANGUAGES

Produce `deck-<id>-en.pptx` and `deck-<id>-fr.pptx` from one script, as one list
of slides each holding both languages.

The French is written in French, not translated from the English: same claim,
same structure, same components, natural register. French runs about 15 % longer,
so compress the French rather than letting it overflow. Apply French typography:
« guillemets », a space before : ; ! ?, 09h30 not 09:30, decimal commas.

Fixed vocabulary, matching the workshop glossary: grand modèle de langage (LLM),
ingénierie de prompt, affinage (fine-tuning), RAG, agent, hallucination,
apprentissage automatique, jeu de données, lumières nocturnes, Somme des lumières.

{SPEC}

{FIGURES}

{HOW}

# ONE MORE CHECK, BEFORE THE OTHERS

  8. List every [UNVERIFIED] slot separately at the end, so I can work through
     them. If there are none, say so explicitly — that is a claim I will test.

Build it now.
"""
    return "NEW-DECK-generator.txt", text


README = """# prompts-pptx — working files, not published

Prompts to paste into Claude web (claude.ai) to build the PowerPoint decks.

**Nothing in this folder is published.** It sits outside `docs/`, so MkDocs never
sees it. That is deliberate.

## Using one

1. Open the file for the deck you want, select all, copy.
2. Paste into a new Claude web conversation.
3. Claude writes a `python-pptx` script, runs it, and returns two `.pptx` files —
   English and French.
4. Download both and put them where they belong.

One conversation per deck. Starting fresh matters: a conversation that has already
built one deck carries its choices into the next.

## The files

  `deck-NN.txt`             The content is fixed and included in full. Claude does
                            layout only — the references and speaker notes are the
                            reviewed ones from the repository.
  `NEW-DECK-generator.txt`  For the sessions with no deck written yet. Claude
                            writes the content as well. Everything it produces
                            needs its references checked before use.

## Regenerating

These files are generated. When a deck source changes, run:

    python tools/pptx_prompt.py

Do not edit a `deck-NN.txt` by hand — the next run overwrites it. Edit the deck
source under `slides/decks/` instead.

## Two things to know about the result

**Figures do not transfer.** Each hand-drawn SVG becomes a labelled placeholder,
and Claude lists them at the end. Screenshot them from the HTML deck at
`docs/slides/` and drop them in. This is deliberate: a diagram redrawn from its
description loses the meaning it was drawn to carry.

**The reveal.js deck stays the source of truth.** It is what the build validates
for density, visual weight and bilingual symmetry, and what the site publishes.
Treat a `.pptx` as output — never edit content in it, because the change will not
come back.
"""


def to_clipboard(text: str) -> bool:
    for cmd in (["clip"], ["pbcopy"], ["xclip", "-selection", "clipboard"]):
        try:
            subprocess.run(cmd, input=text.encode("utf-8"), check=True)
            return True
        except (FileNotFoundError, subprocess.CalledProcessError):
            continue
    return False


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")

    ap = argparse.ArgumentParser(
        description="Write ready-to-paste Claude-web prompts for the PowerPoint decks.")
    ap.add_argument("deck", nargs="?", help="a deck id such as 02; omit for all")
    ap.add_argument("--copy", action="store_true", help="also copy the prompt to the clipboard")
    args = ap.parse_args()

    OUT.mkdir(exist_ok=True)
    (OUT / "README.md").write_text(README, encoding="utf-8")

    decks = existing_decks()
    if args.deck and args.deck not in decks:
        raise SystemExit(
            f"No deck source with id {args.deck!r}. Written so far: "
            f"{', '.join(sorted(decks)) or '(none)'}.\n"
            f"For a session with no deck yet, use prompts-pptx/NEW-DECK-generator.txt."
        )

    targets = {args.deck: decks[args.deck]} if args.deck else decks
    written = []
    for deck_id, path in sorted(targets.items()):
        name, text = prompt_for_deck(deck_id, path)
        (OUT / name).write_text(text, encoding="utf-8")
        written.append((name, text))
        print(f"  {name:<28} {len(text):>7,} chars   from {path.name}")

    if not args.deck:
        pending = [(s, d) for d in agenda()["days"] for s in d["sessions"]
                   if s.get("deck") and s["deck"] not in decks]
        name, text = prompt_generator(pending)
        (OUT / name).write_text(text, encoding="utf-8")
        print(f"  {name:<28} {len(text):>7,} chars   for {len(pending)} session(s) "
              f"with no deck yet: {', '.join(s['deck'] for s, _ in pending)}")

    if args.copy and written:
        print("\n[copied to clipboard]" if to_clipboard(written[0][1])
              else "\n[!] no clipboard tool found (clip / pbcopy / xclip)")

    print(f"\nIn {OUT.relative_to(ROOT)}/ — outside docs/, so nothing here is published.")
    print("Open a file, select all, paste into a fresh Claude web conversation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
