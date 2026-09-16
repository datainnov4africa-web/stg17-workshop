#!/usr/bin/env python3
"""
STG17 · What to name a presentation file, and what is still missing.

    python tools/downloads.py              # every session, present and missing
    python tools/downloads.py --missing    # only what is still needed
    python tools/downloads.py --day 2

Presentations are supplied by the organisers, not generated here. This prints the
exact filename the site expects for each session, so a file can be copied into
`docs/downloads/` and appear on the next build with no further edit.

--------------------------------------------------------------------------
THE NAMING RULE
--------------------------------------------------------------------------
    docs/downloads/<session id>-<EN|FR>.<pdf|pptx>

The language tag is separated by a HYPHEN, never a dot. mkdocs-static-i18n
treats any `.en.` or `.fr.` segment in any filename as its own suffix convention
and publishes only one of the two files — that silently lost half the slide decks
once already.

Session ids come from `config/agenda.yml` and are stable across re-imports of the
Word agenda: `tools/import_agenda.py` carries them over by title. If a session is
renamed beyond recognition its id is regenerated, and this command will show the
old file as a stray.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
AGENDA = ROOT / "config" / "agenda.yml"
DOWNLOADS = ROOT / "docs" / "downloads"

KINDS = ("pdf", "pptx")
TAGS = ("EN", "FR")

#: Modes for which a presentation is the normal expectation. The others may still
#: have one — a ceremony often does — so they are listed, just not counted as gaps.
EXPECTED_MODES = {"talk", "talk_lab", "benchmark"}


def print_notebooks(session: dict, labs: dict, day: dict) -> None:
    """
    The notebooks a laboratory session expects, and whether they exist.

    Notebooks are NOT dropped into a folder like a PDF: they are generated from
    a single master by `tools/build_notebooks.py`, so that the four variants —
    English and French, guided and open — cannot drift apart. Copying an .ipynb
    into notebooks/dayN/ by hand would be overwritten on the next build.

    Listed here anyway, because "where do I find the expected names" is the same
    question for both kinds of file, and it deserves one answer.
    """
    lab = labs.get(session.get("lab", ""))
    if not lab or not lab.get("notebook"):
        return

    day_n = lab.get("day", day["n"])
    stems = [f"{lab['notebook']}_{tag}" for tag in ("EN", "FR", "EN_open", "FR_open")]
    if lab.get("gee_notebook"):
        stems += [f"{lab['gee_notebook']}_{tag}" for tag in ("EN", "FR")]

    folder = ROOT / "notebooks" / f"day{day_n}"
    here = [s for s in stems if (folder / f"{s}.ipynb").exists()]
    status = lab.get("status", "?")
    flag = "" if status == "ready" else "   <- badges hidden until status: ready"

    print(f"      notebooks ({len(here)}/{len(stems)} present, status: {status}){flag}")
    print(f"        notebooks/day{day_n}/{lab['notebook']}_[EN|FR][_open].ipynb")
    if lab.get("gee_notebook"):
        print(f"        notebooks/day{day_n}/{lab['gee_notebook']}_[EN|FR].ipynb")
    print(f"        generated from notebooks/_masters/ — run: python tools/build_notebooks.py")


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    ap = argparse.ArgumentParser(description="Expected presentation filenames.")
    ap.add_argument("--missing", action="store_true", help="only sessions with nothing yet")
    ap.add_argument("--day", type=int, help="restrict to one day")
    args = ap.parse_args()

    agenda = yaml.safe_load(AGENDA.read_text(encoding="utf-8"))
    labs = agenda.get("labs", {})
    DOWNLOADS.mkdir(parents=True, exist_ok=True)
    on_disk = {p.name for p in DOWNLOADS.iterdir() if p.is_file()}

    print(f"\nDrop presentations into:  {DOWNLOADS}")
    print("Naming:  <session id>-EN.pdf   <session id>-FR.pptx   (hyphen, not a dot)\n")

    expected, present, gaps = set(), 0, 0

    for day in agenda["days"]:
        if args.day and day["n"] != args.day:
            continue
        rows = []
        for session in day["sessions"]:
            sid = session.get("id")
            if not sid:
                continue
            have = [f"{sid}-{tag}.{kind}" for kind in KINDS for tag in TAGS
                    if f"{sid}-{tag}.{kind}" in on_disk]
            expected.update(f"{sid}-{tag}.{kind}" for kind in KINDS for tag in TAGS)
            present += len(have)
            wanted = session.get("mode") in EXPECTED_MODES
            if not have and wanted:
                gaps += 1
            if args.missing and have:
                continue
            rows.append((session, sid, have, wanted))

        if not rows:
            continue
        print(f"--- Day {day['n']} · {day['title_en'][:58]}")
        for session, sid, have, wanted in rows:
            mark = "  " if have else ("!!" if wanted else "· ")
            print(f" {mark} {session['time']:<13} {session.get('mode','?'):<10} {sid}")
            if have:
                print(f"      on disk: {', '.join(sorted(have))}")
            else:
                print(f"      expects: {sid}-EN.pdf | {sid}-FR.pdf | "
                      f"{sid}-EN.pptx | {sid}-FR.pptx   (any subset)")
            print_notebooks(session, labs, day)
        print()

    stray = sorted(on_disk - expected - {".gitkeep"})
    stray = [s for s in stray if not s.endswith(".txt")]
    if stray:
        print("[!] Files in docs/downloads/ matching no session — check the spelling:")
        for name in stray:
            print(f"      {name}")
        print()

    print(f"{present} file(s) in place · {gaps} talk-type session(s) with nothing yet")
    print("Files appear on the site automatically: python tools/build_site.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
