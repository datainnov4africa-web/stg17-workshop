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

A session that has no file yet carries an empty placeholder with `-inactif`
before the extension:

    1400_ai-infrastructure_EN-inactif.pdf     no file yet, link is dead
    1400_ai-infrastructure_EN.pdf             supplied, link is live

To supply a presentation: name it exactly like the placeholder, minus
`-inactif`, and drop it in the same folder. Nothing else to edit.

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
    return root / "docs" / "downloads" / f"Day{day_n}"


def filename(session: dict, tag: str, kind: str, placeholder: bool = False) -> str:
    return f"{stem(session)}_{tag}{PLACEHOLDER if placeholder else ''}.{kind}"


def is_placeholder(name: str) -> bool:
    return PLACEHOLDER in name


def supplied(root: Path, session: dict, day_n: int) -> list[tuple[str, str, str]]:
    """
    The files actually supplied for a session: (kind, tag, filename).

    A placeholder is never returned — it exists to tell a person what to call
    their file, not to be published as one.
    """
    folder = day_dir(root, day_n)
    if not folder.is_dir():
        return []
    out = []
    for kind, _icon in KINDS:
        for tag in TAGS:
            name = filename(session, tag, kind)
            path = folder / name
            if path.is_file() and not is_placeholder(name) and path.stat().st_size > 0:
                out.append((kind, tag, name))
    return out
