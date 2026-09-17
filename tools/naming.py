#!/usr/bin/env python3
"""
STG17 · The one place that decides what a presentation file is called.

Both `build_site.py` (which renders the buttons) and `downloads.py` (which
creates the placeholders and reports what is missing) import this. If the two
disagreed about a filename, a file dropped in the right place would simply never
appear, with nothing to explain why — so the rule lives here once.

--------------------------------------------------------------------------
THE CONVENTION
--------------------------------------------------------------------------
    docs/downloads/Day1/1400_ai-infrastructure_EN.pdf

    Day<n>/     one folder per day of the workshop
    1400        the session start time, so files sort into running order
    ai-infra…   a short readable slug, cut at the first colon or dash
    _EN         the language, after an UNDERSCORE
    .pdf        or .pptx — both are offered, either may be supplied

A session with nothing yet carries an empty placeholder, `-inactif` before the
extension. Removing that marker is what publishes the file:

    1400_ai-infrastructure_EN-inactif.pdf     no file yet, link is dead
    1400_ai-infrastructure_EN.pdf             supplied, link is live

--------------------------------------------------------------------------
SEVERAL FILES FOR ONE SESSION
--------------------------------------------------------------------------
Add a number. The site shows one button per file, in numeric order:

    1400_ai-infrastructure_EN-1.pdf           "PDF · EN (1)"
    1400_ai-infrastructure_EN-2.pdf           "PDF · EN (2)"

A number may be followed by a label, which the button then shows instead of the
bare figure. Optional, and worth it when two files are not interchangeable:

    1400_ai-infrastructure_EN-2-exercises.pdf   "PDF · EN · exercises"

Formats and languages are independent: a session may carry two English PDFs, one
French PowerPoint and nothing else. Only what exists is shown.

--------------------------------------------------------------------------
WHY UNDERSCORE BEFORE THE LANGUAGE
--------------------------------------------------------------------------
Never `.en.` or `.fr.`: mkdocs-static-i18n claims any such segment in ANY
filename as its own language convention and publishes only one of the two files,
silently. That already cost half the slide decks once.

--------------------------------------------------------------------------
WHY THE TIME PREFIX
--------------------------------------------------------------------------
It sorts the folder into the order of the day, and it makes collisions
impossible: Day 2 has two sessions both called "Hands-on — …", which would
produce the same slug. `1045_hands-on` and `1530_hands-on` cannot collide.
"""

from __future__ import annotations

import re
import unicodedata
from pathlib import Path

#: Marks a file as not yet supplied. Removing it is what activates the link.
PLACEHOLDER = "-inactif"

#: Offered formats, with the icon the site uses for each.
KINDS = (("pdf", ":material-file-pdf-box:"), ("pptx", ":material-microsoft-powerpoint:"))
TAGS = ("EN", "FR")

#: Cut the title at the first colon or dash — everything after it is a subtitle,
#: and a filename does not need one.
_CUT = re.compile(r"\s*[:—–]\s*")


def slug(title: str, limit: int = 28) -> str:
    head = _CUT.split(title, 1)[0]
    head = unicodedata.normalize("NFKD", head).encode("ascii", "ignore").decode()
    head = re.sub(r"[^A-Za-z0-9]+", "-", head).strip("-").lower()
    head = re.sub(r"^(the|a|an)-", "", head)
    if len(head) <= limit:
        return head or "session"
    return head[:limit].rsplit("-", 1)[0] or head[:limit]


def stem(session: dict) -> str:
    """`1400_ai-infrastructure` — the part of the name a person reads."""
    start = session["time"].split("–")[0].split("-")[0].strip().replace(":", "")
    return f"{start}_{slug(session.get('title_en', ''))}"


def day_dir(root: Path, day_n: int) -> Path:
    """Where a supplied presentation goes. Published with the site."""
    return root / "docs" / "downloads" / f"Day{day_n}"


def placeholder_dir(root: Path, day_n: int) -> Path:
    """
    Where the empty named placeholders live — outside docs/, so they are never
    published.

    They exist to tell whoever prepares a presentation what to call the file;
    that is preparation scaffolding, not something a participant should find on
    the site. Copy the placeholder's name, drop the real file in `day_dir`.
    """
    return root / "maintainer" / "placeholders" / f"Day{day_n}"


def filename(session: dict, tag: str, kind: str, placeholder: bool = False) -> str:
    """The plain, unnumbered name — what `--init` writes as a placeholder."""
    return f"{stem(session)}_{tag}{PLACEHOLDER if placeholder else ''}.{kind}"


def is_placeholder(name: str) -> bool:
    return PLACEHOLDER in name


def _pattern(session: dict) -> re.Pattern:
    kinds = "|".join(k for k, _ in KINDS)
    tags = "|".join(TAGS)
    return re.compile(
        rf"^{re.escape(stem(session))}_({tags})"      # the session and its language
        rf"(?:-(\d+))?"                               # an optional number
        rf"(?:-([^.]+))?"                             # an optional label
        rf"\.({kinds})$",
        re.IGNORECASE,
    )


def supplied(root: Path, session: dict, day_n: int) -> list[dict]:
    """
    Every file actually supplied for a session, in the order it should be shown.

    A placeholder is never returned — it exists to tell a person what to call
    their file, not to be published as one. Neither is an empty file: a deck
    that failed to copy would otherwise produce a button leading to nothing.

    Returns dicts with `kind`, `tag`, `number`, `label` and `name`, sorted by
    format, then language, then number, so two PDFs appear as (1) then (2).
    """
    folder = day_dir(root, day_n)
    if not folder.is_dir():
        return []

    pattern = _pattern(session)
    kind_order = {k: i for i, (k, _) in enumerate(KINDS)}
    tag_order = {t: i for i, t in enumerate(TAGS)}

    out = []
    for path in folder.iterdir():
        if not path.is_file() or is_placeholder(path.name) or path.stat().st_size == 0:
            continue
        match = pattern.match(path.name)
        if not match:
            continue
        tag, number, label, kind = match.groups()
        out.append({
            "kind": kind.lower(),
            "tag": tag.upper(),
            "number": int(number) if number else None,
            "label": label,
            "name": path.name,
        })

    out.sort(key=lambda f: (kind_order.get(f["kind"], 9),
                            tag_order.get(f["tag"], 9),
                            f["number"] or 0,
                            f["label"] or ""))
    return out


def button_text(entry: dict) -> str:
    """`PDF · EN`, `PDF · EN (2)`, or `PDF · EN · exercises`."""
    base = f"{entry['kind'].upper()} · {entry['tag']}"
    if entry.get("label"):
        return f"{base} · {entry['label'].replace('-', ' ')}"
    if entry.get("number"):
        return f"{base} ({entry['number']})"
    return base


def ambiguous(files: list[dict]) -> list[str]:
    """
    An unnumbered file sitting beside numbered ones, for the same format and
    language. The workflow says to number the first file when a second arrives;
    forgetting leaves three files where two were meant, and no error anywhere.
    """
    seen: dict[tuple[str, str], list[dict]] = {}
    for f in files:
        seen.setdefault((f["kind"], f["tag"]), []).append(f)
    out = []
    for (kind, tag), group in seen.items():
        numbers = [f for f in group if f["number"]]
        plain = [f for f in group if not f["number"] and not f["label"]]
        if numbers and plain:
            out.append(f"{kind.upper()} {tag}: {plain[0]['name']} has no number while "
                       f"{numbers[0]['name']} has one — number it, or remove it")
    return out
