#!/usr/bin/env python3
"""
STG17 · Import the agenda from the Word document into config/agenda.yml.

    python tools/import_agenda.py --from "C:/AfDB/.../STG17_..._V16092026.docx"
    python tools/import_agenda.py --from "..." --dry-run

--------------------------------------------------------------------------
WHY AN IMPORTER RATHER THAN A ONE-OFF EDIT
--------------------------------------------------------------------------
The Word document is the agenda of record, and it is still being edited: two
reads of the same file twenty minutes apart returned different text for the
opening ceremony. Transcribing a snapshot by hand would be wrong again within the
hour. So this runs on demand: edit the document, re-run, and the site follows.

--------------------------------------------------------------------------
WHAT IT PRESERVES
--------------------------------------------------------------------------
The document is English-only, while the site is bilingual. French titles and
descriptions therefore live in `config/agenda.yml` and are matched back by
English title on every run — they are never overwritten and never lost. Anything
the document adds or rewrites arrives without French, and is reported so it can
be translated rather than silently published in English on a French page.

The same matching carries `plan`, `deck`, `lab` and `id` across runs, so the
Action-Plan references and the download filenames survive a re-import.

The `labs:` block is spliced back verbatim: it holds specifications this document
does not contain, and reformatting it would lose its comments.
"""

from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from pathlib import Path

import yaml
from docx import Document

ROOT = Path(__file__).resolve().parent.parent
AGENDA = ROOT / "config" / "agenda.yml"

#: Mode strings as the document writes them -> the site's internal vocabulary.
#: "Talk (NISR)" keeps the presenter out of the mode and into `presenter`, so the
#: Mode column stays a format and the site can still credit the institution.
MODE_MAP = {
    "ceremony": ("ceremony", None),
    "talk": ("talk", None),
    "talk (nisr)": ("talk", "NISR"),
    "talk & laboratory": ("talk_lab", None),
    "laboratory": ("lab", None),
    "plenary · countries": ("plenary", None),
    "facilitated": ("facilitated", None),
    "benchmark · teams": ("benchmark", None),
}

SKIP_TITLES = re.compile(r"^(coffee break|lunch|break|pause)", re.I)
DAY_BANNER = re.compile(r"^Day\s+(\d+)\s*\|", re.I)


def slug(text: str, limit: int = 36) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    text = re.sub(r"^(the|a|an)-", "", text)
    if len(text) <= limit:
        return text
    cut = text[:limit].rsplit("-", 1)[0]
    return cut or text[:limit]


def norm(text: str) -> str:
    """A title reduced to what survives light editing, for matching across runs."""
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


# ---------------------------------------------------------------------------
#  Reading the document
# ---------------------------------------------------------------------------
def read_document(path: Path) -> list[dict]:
    """
    Days and sessions, found structurally rather than by table index.

    Table positions shift whenever a section is added or removed — this document
    has already lost four sections since August — so a banner is any single-cell
    table beginning "Day N |", and its session tables are the ones that follow it
    with a Time / Session / Mode header, up to the next banner.
    """
    doc = Document(path)
    days: list[dict] = []
    unknown_modes: set[str] = set()

    for table in doc.tables:
        first = table.rows[0].cells[0].text.strip()

        banner = DAY_BANNER.match(first)
        if banner and len(table.columns) == 1:
            lines = [ln.strip() for ln in first.split("\n") if ln.strip()]
            weekday = lines[0].split("|", 1)[1].strip() if "|" in lines[0] else ""
            days.append({
                "n": int(banner.group(1)),
                "weekday_en": weekday,
                "title_en": lines[1] if len(lines) > 1 else "",
                "strap_en": lines[2] if len(lines) > 2 else "",
                "sessions": [],
            })
            continue

        header = [c.text.strip().lower() for c in table.rows[0].cells]
        if not days or "time" not in header or "session" not in header:
            continue

        for row in table.rows[1:]:
            cells, seen, prev = [c.text.strip() for c in row.cells], [], None
            for cell in cells:                      # collapse merged cells
                if cell != prev:
                    seen.append(cell)
                prev = cell
            if len(seen) < 2:
                continue

            time = seen[0].replace("-", "–")
            body = seen[1]
            mode_raw = seen[2] if len(seen) > 2 else ""

            title, _, desc = body.partition("\n")
            title, desc = title.strip(), " ".join(desc.split())
            if not title or SKIP_TITLES.match(title):
                continue                            # breaks are rendered by the site

            mode, presenter = MODE_MAP.get(mode_raw.strip().lower(), (None, None))
            if mode is None:
                unknown_modes.add(mode_raw)
                mode = "talk"

            session = {"time": time, "mode": mode, "title_en": title, "desc_en": desc}
            if presenter:
                session["presenter"] = presenter
            days[-1]["sessions"].append(session)

    if unknown_modes:
        print("[!] Mode values the importer did not recognise, filed as 'talk':")
        for value in sorted(unknown_modes):
            print(f"      {value!r}  — add it to MODE_MAP if it should render differently")
    return days


# ---------------------------------------------------------------------------
#  Merging with what the repository already knows
# ---------------------------------------------------------------------------
CARRY = ("title_fr", "desc_fr", "plan", "deck", "lab", "id")


def merge(new_days: list[dict], old: dict) -> tuple[list[dict], list[str], list[str]]:
    """Carry French, Action-Plan references, deck, lab and id across by title."""
    known = {}
    for day in old.get("days", []):
        for session in day.get("sessions", []):
            known[norm(session.get("title_en", ""))] = session

    used, untranslated = set(), []
    for day in new_days:
        seen_ids: set[str] = set()
        for session in day["sessions"]:
            match = known.get(norm(session["title_en"]))
            if match:
                used.add(norm(session["title_en"]))
                for key in CARRY:
                    if match.get(key):
                        session[key] = match[key]

            if not session.get("id"):
                base = f"d{day['n']}-{slug(session['title_en'])}"
                candidate, i = base, 2
                while candidate in seen_ids:
                    candidate, i = f"{base}-{i}", i + 1
                session["id"] = candidate
            seen_ids.add(session["id"])

            if not session.get("desc_fr") or not session.get("title_fr"):
                untranslated.append(f"D{day['n']} {session['time']} — {session['title_en']}")

            # Key order the file is read in, not the order they were added.
            ordered = {}
            for key in ("time", "mode", "presenter", "id", "deck", "lab",
                        "title_en", "title_fr", "desc_en", "desc_fr", "plan"):
                if session.get(key) not in (None, "", []):
                    ordered[key] = session[key]
            session.clear()
            session.update(ordered)

    dropped = [known[k].get("title_en", k) for k in known if k not in used]
    return new_days, untranslated, dropped


def carry_day_french(new_days: list[dict], old: dict) -> None:
    by_n = {d["n"]: d for d in old.get("days", [])}
    for day in new_days:
        previous = by_n.get(day["n"], {})
        for key in ("weekday_fr", "title_fr", "strap_fr"):
            if previous.get(key):
                day[key] = previous[key]
        day_ordered = {}
        for key in ("n", "weekday_en", "weekday_fr", "title_en", "title_fr",
                    "strap_en", "strap_fr", "sessions"):
            if day.get(key) not in (None, "", []):
                day_ordered[key] = day[key]
        day.clear()
        day.update(day_ordered)


# ---------------------------------------------------------------------------
#  Writing
# ---------------------------------------------------------------------------
def write_agenda(days: list[dict], source: Path) -> None:
    """
    Replace the `days:` block, splice `labs:` back unchanged.

    Re-dumping the whole file would strip the comments in the laboratory block,
    including the one recording why a French string there is quoted.
    """
    text = AGENDA.read_text(encoding="utf-8")
    start = text.index("\ndays:") + 1
    end = text.index("\nlabs:") + 1

    header = text[:start]
    header = re.sub(r"#  Transcribed from:.*?\n(#.*?\n)*",
                    f"#  Imported from: {source.name}\n"
                    f"#  Re-run `python tools/import_agenda.py` after editing that document.\n",
                    header, count=1, flags=re.S)

    body = yaml.safe_dump({"days": days}, allow_unicode=True, sort_keys=False,
                          width=4096, default_flow_style=False)
    AGENDA.write_text(header + body + "\n" + text[end:], encoding="utf-8")


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    ap = argparse.ArgumentParser(description="Import the agenda from the Word document.")
    ap.add_argument("--from", dest="source", required=True, help="path to the .docx")
    ap.add_argument("--dry-run", action="store_true", help="report, write nothing")
    args = ap.parse_args()

    source = Path(args.source)
    if not source.exists():
        raise SystemExit(f"Not found: {source}")

    days = read_document(source)
    old = yaml.safe_load(AGENDA.read_text(encoding="utf-8"))
    days, untranslated, dropped = merge(days, old)
    carry_day_french(days, old)

    print(f"\nRead {source.name}")
    for day in days:
        print(f"  Day {day['n']}  {len(day['sessions'])} sessions   {day['title_en'][:52]}")
    total = sum(len(d["sessions"]) for d in days)
    print(f"  {len(days)} days · {total} sessions (breaks excluded — the site renders those)")

    if dropped:
        print(f"\n[!] {len(dropped)} session(s) in agenda.yml no longer in the document:")
        for title in dropped:
            print(f"      {title}")
        print("    Their French text is kept in case they return; nothing else references them.")

    if untranslated:
        print(f"\n[!] {len(untranslated)} session(s) have no French text yet:")
        for line in untranslated:
            print(f"      {line}")
        print("    The French page would fall back to English. Translate these in "
              "config/agenda.yml.")

    if args.dry_run:
        print("\nDry run — nothing written.")
        return 0

    write_agenda(days, source)
    print(f"\nWritten: {AGENDA}")
    print("Next:  python tools/build_site.py   (then build_all.py to regenerate everything)")
    return 1 if untranslated else 0


if __name__ == "__main__":
    raise SystemExit(main())
