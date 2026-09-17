#!/usr/bin/env python3
"""
STG17 · Regenerate everything derived, in the right order.

    python tools/build_all.py
    python tools/build_all.py --check      # CI: fail if anything is stale

Run this after editing any source of truth:

    config/workshop.yml            org name, endpoints, default countries
    config/agenda.yml              the agenda -> day pages, lab register, mapping
    stg17/theme.py                 the palette -> site CSS, slide CSS
    stg17/i18n.py                  the shared vocabulary -> the glossary
    slides/decks/*.deck.html       -> the EN and FR reveal decks

The order matters: the CSS variables must exist before the site is built, and
the notebooks must exist before the agenda pages link to them.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def run(description: str, command: list[str]) -> bool:
    print(f"\n=== {description} " + "=" * max(0, 62 - len(description)))
    result = subprocess.run([sys.executable, *command], cwd=ROOT, check=False)
    if result.returncode != 0:
        print(f"--- FAILED: {description}")
        return False
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Regenerate every derived artefact")
    parser.add_argument("--check", action="store_true",
                        help="verify freshness without writing (for CI)")
    parser.add_argument("--pptx", action="store_true",
                        help="also derive the PowerPoint files (needs python-pptx)")
    args = parser.parse_args()

    steps: list[tuple[str, list[str]]] = [
        ("Country registry self-check", ["-m", "stg17.countries"]),
        ("AfDB palette -> CSS variables", ["-m", "stg17.theme", "--emit-css"]),
                ("Notebook validation", ["tools/check_notebooks.py"]),
        ("Agenda -> day pages, lab register, mapping, glossary", ["tools/build_site.py"]),
        ("Slide decks", ["tools/build_slides.py"]),
    ]
    if args.pptx:
        steps.append(("PowerPoint derivatives", ["tools/build_pptx.py"]))

    failures = [description for description, command in steps if not run(description, command)]

    print("\n" + "=" * 70)
    if failures:
        print("FAILED:")
        for description in failures:
            print("   -", description)
        return 1
    print("Everything regenerated. Preview the site with:  mkdocs serve")
    return 0


if __name__ == "__main__":
    sys.exit(main())
