#!/usr/bin/env python3
"""
STG17 · Presentation files: create the placeholders, see what is still missing.

    python tools/downloads.py --init      create Day1..Day5 and every placeholder
    python tools/downloads.py             what is supplied, what is not
    python tools/downloads.py --missing   only what is still needed
    python tools/downloads.py --day 2

--------------------------------------------------------------------------
HOW A PRESENTATION IS SUPPLIED
--------------------------------------------------------------------------
`--init` writes an empty placeholder for every session:

    docs/downloads/Day1/1400_ai-infrastructure_EN-inactif.pdf

Name your file exactly the same, minus `-inactif`, and drop it in that folder:

    docs/downloads/Day1/1400_ai-infrastructure_EN.pdf

The button appears on the day page at the next build. No file to edit, no name to
invent, no id to copy. `.pptx` works the same way — rename the extension.

A placeholder is never published as a download: `naming.supplied()` skips any
name carrying the marker, and skips empty files, so an accidentally emptied file
cannot produce a dead button either.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

import naming

ROOT = Path(__file__).resolve().parent.parent
AGENDA = ROOT / "config" / "agenda.yml"

#: Modes for which a presentation is the normal expectation. The rest may still
#: have one — a ceremony often does — they are just not counted as gaps.
EXPECTED_MODES = {"talk", "talk_lab", "benchmark"}


def create_placeholders(agenda: dict) -> tuple[int, int]:
    """One empty file per session, language and format. Never overwrites."""
    made = kept = 0
    for day in agenda["days"]:
        folder = naming.day_dir(ROOT, day["n"])
        folder.mkdir(parents=True, exist_ok=True)
        for session in day["sessions"]:
            for kind, _icon in naming.KINDS:
                for tag in naming.TAGS:
                    real = folder / naming.filename(session, tag, kind)
                    mark = folder / naming.filename(session, tag, kind, placeholder=True)
                    if real.is_file():
                        kept += 1          # already supplied — leave it alone
                        continue
                    if not mark.exists():
                        mark.touch()
                        made += 1
    return made, kept


def print_notebooks(session: dict, labs: dict, day: dict) -> None:
    """
    The notebooks a laboratory session expects, and whether they exist.

    Notebooks work the other way round from a presentation: they are generated
    from one master by `tools/build_notebooks.py`, so that English, French,
    guided and open cannot drift apart. An .ipynb copied into notebooks/dayN/ by
    hand is overwritten on the next build.
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
    flag = "" if status == "ready" else "   <- no Colab badge until status: ready"
    print(f"        notebooks: {len(here)}/{len(stems)} present, status {status}{flag}")


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    ap = argparse.ArgumentParser(description="Presentation files for the workshop site.")
    ap.add_argument("--init", action="store_true",
                    help="create the day folders and every placeholder")
    ap.add_argument("--missing", action="store_true", help="only sessions with nothing yet")
    ap.add_argument("--day", type=int, help="restrict to one day")
    args = ap.parse_args()

    agenda = yaml.safe_load(AGENDA.read_text(encoding="utf-8"))
    labs = agenda.get("labs", {})

    if args.init:
        made, kept = create_placeholders(agenda)
        print(f"\n{made} placeholder(s) created, {kept} file(s) already supplied.")
        print(f"Folders: {ROOT / 'docs' / 'downloads'}\\Day1 .. Day{len(agenda['days'])}")
        print("\nTo supply a presentation: rename your file exactly like the placeholder,")
        print("minus '-inactif', and drop it in the same folder. Then:")
        print("    python tools/build_site.py\n")
        return 0

    total_supplied, gaps = 0, 0
    for day in agenda["days"]:
        if args.day and day["n"] != args.day:
            continue
        folder = naming.day_dir(ROOT, day["n"])
        rows = []
        for session in day["sessions"]:
            have = naming.supplied(ROOT, session, day["n"])
            total_supplied += len(have)
            wanted = session.get("mode") in EXPECTED_MODES
            if not have and wanted:
                gaps += 1
            if args.missing and have:
                continue
            rows.append((session, have, wanted))

        if not rows:
            continue
        print(f"\n--- Day {day['n']} · {day['title_en'][:56]}")
        print(f"    {folder}")
        for session, have, wanted in rows:
            mark = "OK" if have else ("!!" if wanted else "· ")
            print(f" {mark} {session['time']:<13} {session.get('mode','?'):<10} "
                  f"{session['title_en'][:44]}")
            if have:
                print(f"        supplied: {', '.join(n for _k, _t, n in have)}")
            else:
                print(f"        name your file: {naming.stem(session)}_EN.pdf"
                      f"   (or _FR, or .pptx)")
            print_notebooks(session, labs, day)

    print(f"\n{total_supplied} presentation file(s) supplied · "
          f"{gaps} talk-type session(s) with nothing yet")
    print("After dropping a file:  python tools/build_site.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
