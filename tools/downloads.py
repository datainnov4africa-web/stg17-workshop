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

Name your file exactly the same, minus `-inactif`, and drop it in that folder.
The button appears on the day page at the next build. No file to edit, no name to
invent. `.pptx` works the same way — rename the extension.

Several files for one session: add a number, and the site shows one button each.

    1400_ai-infrastructure_EN-1.pdf     ->  "PDF · EN (1)"
    1400_ai-infrastructure_EN-2.pdf     ->  "PDF · EN (2)"

A label after the number replaces the figure on the button, which is worth it
when the two are not interchangeable:

    1400_ai-infrastructure_EN-2-exercises.pdf   ->  "PDF · EN · exercises"

This command reports the case the workflow makes easy to get wrong: an
unnumbered file left beside a numbered one, which is neither an error nor what
anybody meant.
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
        folder = naming.placeholder_dir(ROOT, day["n"])
        folder.mkdir(parents=True, exist_ok=True)

        # The drop target is published, so it must survive a clone even while
        # empty — git does not track empty directories.
        drop = naming.day_dir(ROOT, day["n"])
        drop.mkdir(parents=True, exist_ok=True)
        (drop / ".gitkeep").touch(exist_ok=True)

        for session in day["sessions"]:
            supplied = {f["kind"] + f["tag"] for f in naming.supplied(ROOT, session, day["n"])}
            for kind, _icon in naming.KINDS:
                for tag in naming.TAGS:
                    if kind + tag in supplied:
                        kept += 1          # already supplied — leave it alone
                        continue
                    mark = folder / naming.filename(session, tag, kind, placeholder=True)
                    if not mark.exists():
                        mark.touch()
                        made += 1
    return made, kept


def print_notebooks(session: dict, labs: dict, day: dict) -> None:
    """
    The notebooks a laboratory session expects, and whether they exist.

    Notebooks work the other way round from a presentation: they are generated
    from a master by `tools/build_notebooks.py`, so that English, French, guided
    and open cannot drift apart. An .ipynb copied into notebooks/dayN/ by hand is
    overwritten on the next build. A laboratory may declare several with
    `notebooks:`; `notebook:` stays valid for the usual single one.
    """
    lab = labs.get(session.get("lab", ""))
    if not lab:
        return
    stems = lab.get("notebooks") or ([lab["notebook"]] if lab.get("notebook") else [])
    if not stems:
        return

    day_n = lab.get("day", day["n"])
    folder = ROOT / "notebooks" / f"day{day_n}"
    wanted = [f"{s}_{tag}" for s in stems for tag in ("EN", "FR", "EN_open", "FR_open")]
    wanted += [f"{g}_{tag}"
               for g in (lab.get("gee_notebooks")
                         or ([lab["gee_notebook"]] if lab.get("gee_notebook") else []))
               for tag in ("EN", "FR")]
    here = [s for s in wanted if (folder / f"{s}.ipynb").exists()]

    status = lab.get("status", "?")
    flag = "" if status == "ready" else "   <- no Colab badge until status: ready"
    print(f"        notebooks: {len(here)}/{len(wanted)} present in notebooks/day{day_n}/, "
          f"status {status}{flag}")
    if len(stems) > 1:
        print(f"                   {len(stems)} notebooks: {', '.join(stems)}")


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
        print(f"Placeholders (never published): {ROOT / 'maintainer' / 'placeholders'}")
        print(f"Drop your files in:             {ROOT / 'docs' / 'downloads'}")
        print()
        print("Copy a placeholder's name, remove '-inactif', and put the real")
        print("file in the matching docs/downloads/DayN/ folder. Then:")
        print("    python tools/build_site.py\n")
        return 0

    total, gaps, warnings = 0, 0, []
    for day in agenda["days"]:
        if args.day and day["n"] != args.day:
            continue
        rows = []
        for session in day["sessions"]:
            have = naming.supplied(ROOT, session, day["n"])
            total += len(have)
            wanted = session.get("mode") in EXPECTED_MODES
            if not have and wanted:
                gaps += 1
            for problem in naming.ambiguous(have):
                warnings.append(f"Day {day['n']} · {session['time']} — {problem}")
            if args.missing and have:
                continue
            rows.append((session, have, wanted))

        if not rows:
            continue
        print(f"\n--- Day {day['n']} · {day['title_en'][:56]}")
        print(f"    {naming.day_dir(ROOT, day['n'])}")
        for session, have, wanted in rows:
            mark = "OK" if have else ("!!" if wanted else "· ")
            print(f" {mark} {session['time']:<13} {session.get('mode','?'):<10} "
                  f"{session['title_en'][:44]}")
            for f in have:
                print(f"        {f['name']}   ->  {naming.button_text(f)}")
            if not have:
                print(f"        name your file: {naming.stem(session)}_EN.pdf"
                      f"   (or _FR, or .pptx, or -1 / -2 for several)")
            print_notebooks(session, labs, day)

    if warnings:
        print("\n[!] Numbering to sort out:")
        for line in warnings:
            print(f"      {line}")

    print(f"\n{total} presentation file(s) supplied · "
          f"{gaps} talk-type session(s) with nothing yet")
    print("After dropping a file:  python tools/build_site.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
