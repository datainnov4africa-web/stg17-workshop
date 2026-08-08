#!/usr/bin/env python3
"""
STG17 · Assemble a ready-to-paste prompt from the prompt library.

    python tools/prompt.py P1 --deck 02
    python tools/prompt.py P2 --deck 02 --slide 4
    python tools/prompt.py P3 --deck 08 --figure "How a gas flare differs from a city"
    python tools/prompt.py P6 --deck 01 --copy
    python tools/prompt.py --list

--------------------------------------------------------------------------
WHY THIS EXISTS
--------------------------------------------------------------------------
A prompt that carries the design system is only useful while the design system
it carries is the real one. Copy a prompt into a chat window, change a colour in
`stg17/theme.py` a fortnight later, and the pasted copy is now instructing a
generator to produce off-brand material — silently, and with no build step to
catch it.

So the prompt files hold `{{TOKENS}}` and nothing else, and every value is read
here from the same source the build reads:

    palette        stg17.theme
    density limits tools.build_slides  (imported, not restated)
    session facts  config/agenda.yml
    deck content   slides/decks/*.deck.html
    prompt bodies  docs/resources/prompts/P*.md

If a threshold changes, the next prompt printed carries the new one. There is no
copy to update.
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
PROMPTS = ROOT / "docs" / "resources" / "prompts"
DECKS = ROOT / "slides" / "decks"

#: Who these decks are for. Stated once, because every prompt that describes the
#: audience wrongly produces material pitched at the wrong level.
DEFAULT_AUDIENCE = (
    "Heads of statistical methodology and heads of IT at African national "
    "statistical offices. Expert in official statistics, non-expert in machine "
    "learning. Many are attending in their second or third working language. "
    "They are decision-makers: they specify, procure and defend what their "
    "office builds."
)

sys.path.insert(0, str(ROOT))
from stg17 import theme  # noqa: E402


def _load_build_slides():
    """Import build_slides for its thresholds, without running its main()."""
    spec = importlib.util.spec_from_file_location(
        "_bs", Path(__file__).resolve().parent / "build_slides.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


BS = _load_build_slides()


# ---------------------------------------------------------------------------
#  Reading the repository
# ---------------------------------------------------------------------------
def deck_source(deck_id: str) -> Path:
    """The .deck.html whose meta id matches, or a clear error listing what exists."""
    for path in sorted(DECKS.glob("*.deck.html")):
        meta = BS.parse_meta(path.read_text(encoding="utf-8"))
        if meta.get("id") == deck_id:
            return path
    known = ", ".join(
        BS.parse_meta(p.read_text(encoding="utf-8")).get("id", "?")
        for p in sorted(DECKS.glob("*.deck.html"))
    )
    raise SystemExit(f"No deck source with id {deck_id!r}. Sources present: {known or '(none)'}")


def agenda_session(deck_id: str) -> tuple[dict, dict, dict | None, dict | None]:
    """The agenda entry for a deck, with its day and its neighbours in the day."""
    agenda = yaml.safe_load((ROOT / "config" / "agenda.yml").read_text(encoding="utf-8"))
    for day in agenda["days"]:
        sessions = day["sessions"]
        for i, session in enumerate(sessions):
            if str(session.get("deck", "")) == deck_id:
                return (
                    session,
                    day,
                    sessions[i - 1] if i > 0 else None,
                    sessions[i + 1] if i + 1 < len(sessions) else None,
                )
    raise SystemExit(
        f"Deck {deck_id!r} is not attached to any session in config/agenda.yml.\n"
        f"Add a `deck: '{deck_id}'` key to the session it belongs to first — the "
        f"agenda is what gives a deck its duration, its audience and its neighbours."
    )


def sections(source: str, lang: str = "en") -> list[str]:
    """
    The <section> blocks of one language, in order.

    `split_lang` operates on a single slide, not on a document: running it over
    the whole source would treat the first <!--EN--> and the last <!--FR--> as
    one pair and return the entire middle of the deck. So split into sections
    first, then reduce each one — the same order `build_slides.build()` uses.
    """
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
        out.append(open_tag.group(0) + BS.split_lang(inner, lang) + close)
    return out


def visible(section_html: str) -> str:
    return BS.visible_text(section_html)


def section_title(section_html: str) -> str:
    """
    A slide's name for a human.

    Not every slide has a heading: a `.statement` slide deliberately carries one
    large sentence and no <h2>. Falling back to the statement keeps the prompt
    referring to slides the way the author thinks of them.
    """
    for pattern in (r"<h[12][^>]*>(.*?)</h[12]>", r'<div class="statement"[^>]*>(.*?)</div>'):
        match = re.search(pattern, section_html, re.S)
        if match:
            text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", match.group(1))).strip()
            return text if len(text) <= 70 else text[:67] + "…"
    return "(untitled slide)"


# ---------------------------------------------------------------------------
#  Token values
# ---------------------------------------------------------------------------
def build_tokens(args) -> dict[str, str]:
    tokens = {
        "NAVY": theme.NAVY,
        "GREEN": theme.GREEN,
        "AMBER": theme.AMBER,
        "INK": theme.INK,
        "MUTED": theme.MUTED,
        "LINE": theme.LINE,
        "WASH": theme.WASH,
        "WORD_LIMIT": str(BS.WORD_LIMIT),
        "WORD_BUDGET": str(BS.WORD_BUDGET),
        "TABLE_ROW_LIMIT": str(BS.TABLE_ROW_LIMIT),
        "FIGURE_BRIEF": args.figure or "(describe the diagram here)",
        "FIGURE_TAKEAWAY": args.takeaway or "(state the five-second takeaway here)",
        "IMAGE_BRIEF": args.figure or "(describe the image here)",
        # P9 is the one prompt that does not have to be about a workshop
        # session, so its three inputs are supplied rather than looked up.
        # When --deck is given they are filled from the agenda below.
        "SUBJECT": args.subject or "(state the subject here)",
        "AUDIENCE": args.audience or DEFAULT_AUDIENCE,
        "DURATION": args.duration or "30",
    }

    if not args.deck:
        return tokens

    session, day, prev, nxt = agenda_session(args.deck)
    source_path = deck_source(args.deck)
    source = source_path.read_text(encoding="utf-8")
    meta = BS.parse_meta(source)
    secs = sections(source, args.lang)

    def label(s, key="title_en"):
        return f"{s['time']} — {s[key]}" if s else "(none — this opens the day)"

    tokens.update(
        {
            "DECK_ID": args.deck,
            "TITLE_EN": session.get("title_en", meta.get("title_en", "")),
            "TITLE_FR": session.get("title_fr", meta.get("title_fr", "")),
            "DAY": str(day["n"]),
            "TIME": session.get("time", ""),
            "MODE": session.get("mode", "talk"),
            "DURATION": args.duration or meta.get("duration", "30"),
            "SUBJECT": args.subject or "\n\n".join(
                x for x in (session.get("title_en", ""), session.get("desc_en", "")) if x
            ),
            "DESC_EN": session.get("desc_en", ""),
            "DESC_FR": session.get("desc_fr", ""),
            "PLAN": str(session.get("plan", "")),
            "PREV_SESSION": label(prev),
            "NEXT_SESSION": label(nxt) if nxt else "(none — this closes the day)",
            "SLIDE_TOTAL": str(len(secs)),
            "DECK_TEXT": source,
        }
    )

    if args.slide:
        i = args.slide - 1
        if not 0 <= i < len(secs):
            raise SystemExit(
                f"Deck {args.deck} has {len(secs)} slides; asked for {args.slide}."
            )
        words = len(visible(secs[i]).split())
        tokens.update(
            {
                "SLIDE_N": str(args.slide),
                "SLIDE_TITLE": section_title(secs[i]),
                "SLIDE_VISIBLE": visible(secs[i]),
                "SLIDE_EN": secs[i],
                "WORD_COUNT": str(words),
                "TIMING": (re.search(r'class="timing">([^<]*)<', secs[i]) or [None, "?"])[1]
                if re.search(r'class="timing">([^<]*)<', secs[i])
                else "not set",
                "PREV_TITLE": section_title(secs[i - 1]) if i > 0 else "(this is the first slide)",
                "NEXT_TITLE": section_title(secs[i + 1])
                if i + 1 < len(secs)
                else "(this is the last slide)",
            }
        )
    return tokens


# ---------------------------------------------------------------------------
#  Assembly
# ---------------------------------------------------------------------------
RE_BLOCK = re.compile(r"^````text\n(.*?)^````", re.S | re.M)


def extract_prompt(markdown: str, path: Path) -> str:
    match = RE_BLOCK.search(markdown)
    if not match:
        raise SystemExit(
            f"{path.name} has no ````text ... ```` block — the prompt library "
            f"keeps the promptable text fenced so the surrounding guidance is "
            f"never pasted into a chat window by accident."
        )
    return match.group(1).rstrip()


def fill(prompt: str) -> tuple[str, list[str]]:
    """Substitute tokens; report the ones left unfilled rather than shipping them."""
    unresolved = []

    def sub(match):
        key = match.group(1)
        if key in TOKENS:
            return TOKENS[key]
        unresolved.append(key)
        return match.group(0)

    return re.sub(r"\{\{(\w+)\}\}", sub, prompt), sorted(set(unresolved))


def to_clipboard(text: str) -> bool:
    for command in (["clip"], ["pbcopy"], ["xclip", "-selection", "clipboard"]):
        try:
            subprocess.run(command, input=text.encode("utf-8"), check=True)
            return True
        except (FileNotFoundError, subprocess.CalledProcessError):
            continue
    return False


def main() -> int:
    # The prompts and the decks they carry are full of en dashes, middots, «»
    # and mathematical signs. A Windows console defaults to cp1252 and dies on
    # the first one, so the tool sets its own encoding rather than expecting
    # every user to know about PYTHONIOENCODING.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")

    ap = argparse.ArgumentParser(
        description="Assemble a filled-in prompt from docs/resources/prompts/.",
        epilog="The prompt library is documented in docs/resources/prompts/index.md.",
    )
    ap.add_argument("prompt", nargs="?", help="P1 … P8, or a filename in docs/resources/prompts/")
    ap.add_argument("--deck", help="deck id as it appears in the source <!--meta--> block")
    ap.add_argument("--slide", type=int, help="1-based slide number, for P2 / P5 / P8")
    ap.add_argument("--figure", help="what the diagram or image should show, for P3 / P4")
    ap.add_argument("--takeaway", help="the five-second takeaway of a figure, for P3")
    ap.add_argument("--subject", help="what the deck is about, for P9 without --deck")
    ap.add_argument("--audience", help="who it is for, for P9; defaults to the STG17 audience")
    ap.add_argument("--duration", help="minutes; overrides the deck's own duration")
    ap.add_argument("--lang", default="en", choices=["en", "fr"],
                    help="which language of the deck to read slides from")
    ap.add_argument("--copy", action="store_true", help="also copy to the clipboard")
    ap.add_argument("--list", action="store_true", help="list the available prompts")
    args = ap.parse_args()

    if args.list or not args.prompt:
        print("Prompt library — docs/resources/prompts/\n")
        # Sort on the number, not the string: plain order puts P10 before P2.
        def order(p):
            m = re.match(r"P(\d+)", p.stem)
            return int(m.group(1)) if m else 999
        for path in sorted(PROMPTS.glob("P*.md"), key=order):
            first = next(
                (l.lstrip("# ").strip() for l in path.read_text(encoding="utf-8").splitlines() if l.startswith("# ")),
                path.stem,
            )
            print(f"  {path.stem.split('-')[0]:<4} {first}")
        print("\n  python tools/prompt.py P1 --deck 02")
        return 0

    # The glob is anchored with the hyphen so "P1" cannot match "P10-...".
    matches = sorted(PROMPTS.glob(f"{args.prompt}-*.md")) or sorted(PROMPTS.glob(args.prompt))
    if not matches:
        raise SystemExit(f"No prompt {args.prompt!r} in {PROMPTS}. Try --list.")

    global TOKENS
    TOKENS = build_tokens(args)
    filled, unresolved = fill(extract_prompt(matches[0].read_text(encoding="utf-8"), matches[0]))

    print(filled)

    if unresolved:
        print(
            f"\n[!] {len(unresolved)} placeholder(s) still unfilled: {', '.join(unresolved)}\n"
            f"    Fill them by hand before pasting, or supply the missing option "
            f"(--deck / --slide / --figure).",
            file=sys.stderr,
        )
    if args.copy:
        print("\n[copied to clipboard]" if to_clipboard(filled) else
              "\n[!] no clipboard tool found (clip / pbcopy / xclip)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
