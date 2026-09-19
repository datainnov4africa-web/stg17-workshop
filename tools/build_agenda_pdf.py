#!/usr/bin/env python3
"""
STG17 · The agenda as a downloadable PDF, in English and in French.

    python tools/build_agenda_pdf.py
    python tools/build_agenda_pdf.py --lang fr
    python tools/build_agenda_pdf.py --out "C:/AfDB/Momar/STG17/Workshop Sep 2026"

--------------------------------------------------------------------------
WHY THIS IS GENERATED RATHER THAN WRITTEN
--------------------------------------------------------------------------
`config/agenda.yml` already renders the five day pages, the week view, the
laboratory register and the Action-Plan mapping. A hand-made PDF beside them
would be a second copy of the agenda, and a second copy is a copy that drifts:
the concept note this repository had to regenerate announced nine laboratories
where the agenda already carried thirteen. This reads the same file, so the
downloaded agenda and the website cannot disagree.

--------------------------------------------------------------------------
TWO CHOICES WORTH KNOWING
--------------------------------------------------------------------------
*Colours* come from `stg17.theme`, the one place in this repository where a
colour is allowed to live. Nothing here hard-codes a hex value.

*Typography* is Helvetica, a PDF core font. It needs no font file on the machine
that builds the document, and it carries every character the French agenda uses
— accented capitals, the en dash of a time range, the middot and the
typographic apostrophe. Registering Calibri would look marginally closer to the
Word original at the cost of a PDF that only builds on Windows.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from xml.sax.saxutils import escape

import yaml
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (CondPageBreak, Image, Paragraph,
                                SimpleDocTemplate, Spacer, Table, TableStyle)

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from stg17 import theme  # noqa: E402  - after sys.path, deliberately

NAVY = colors.HexColor(theme.NAVY)
GREEN = colors.HexColor(theme.GREEN)
AMBER = colors.HexColor(theme.AMBER)
INK = colors.HexColor(theme.INK)
MUTED = colors.HexColor(theme.MUTED)
LINE = colors.HexColor(theme.LINE)
WASH = colors.HexColor(theme.WASH)

MARGIN = 16 * mm
COL_TIME = 25 * mm
COL_BODY = A4[0] - 2 * MARGIN - COL_TIME

#: The dates the website states. `config/workshop.yml` still carries "TBC" in
#: `dates_en` / `venue_en`, and nothing in the build reads those fields — so the
#: configuration would put "To be confirmed" on the cover of a document that is
#: meant to be circulated. These are used only when the configuration has not
#: been filled in, and the fallback announces itself on stdout when it fires.
FALLBACK_DATES = {"en": "28 September – 2 October 2026",
                  "fr": "28 septembre – 2 octobre 2026"}
FALLBACK_VENUE = {"en": "Kigali, Rwanda", "fr": "Kigali, Rwanda"}

MODE_LABEL = {
    "ceremony":    ("Ceremony", "Cérémonie"),
    "talk":        ("Presentation", "Exposé"),
    "talk_lab":    ("Presentation and laboratory", "Exposé et laboratoire"),
    "lab":         ("Laboratory", "Laboratoire"),
    "benchmark":   ("Benchmark", "Benchmark"),
    "plenary":     ("Plenary", "Plénière"),
    "facilitated": ("Facilitated discussion", "Discussion animée"),
    "panel":       ("Panel", "Table ronde"),
    "wrap":        ("Wrap-up", "Clôture"),
}

STRINGS = {
    "en": {
        "doc_title": "Agenda",
        "lede": ("Five days, from the concepts to a published repository. Every "
                 "half-day pairs a short presentation with an extended laboratory "
                 "at the keyboard."),
        "time": "Time", "session": "Session",
        "day": "Day",
        "l_dates": "DATES", "l_venue": "VENUE", "l_shape": "FORMAT",
        "shape": "{days} days · {sessions} sessions · {labs} laboratories",
        "site": "Full detail, materials and notebooks:",
    },
    "fr": {
        "doc_title": "Agenda",
        "lede": ("Cinq jours, du concept au dépôt publié. Chaque demi-journée "
                 "associe un exposé bref à un laboratoire prolongé sur machine."),
        "time": "Heure", "session": "Séance",
        "day": "Jour",
        "l_dates": "DATES", "l_venue": "LIEU", "l_shape": "FORMAT",
        "shape": "{days} jours · {sessions} séances · {labs} laboratoires",
        "site": "Détail complet, supports et carnets :",
    },
}


# ---------------------------------------------------------------------------
#  Small helpers
# ---------------------------------------------------------------------------
def pick_raw(item: dict, field: str, lang: str) -> str:
    """The `field_en` / `field_fr` pair, falling back to English."""
    return item.get(f"{field}_{lang}") or item.get(f"{field}_en") or ""


def pick(item: dict, field: str, lang: str) -> str:
    """
    The same pair, escaped for reportlab.

    `Paragraph` parses a small XML dialect, so a single ampersand in a session
    title — "Monitoring & evaluation" is an ordinary thing for an agenda to say
    — raises at build time rather than printing. Escaping here rather than at
    each call site means a new Paragraph cannot forget it. Use `pick_raw` for
    text that goes to the canvas or to PDF metadata, which are not parsed.
    """
    return escape(pick_raw(item, field, lang))


def fmt_time(value: str, lang: str) -> str:
    """`09:00–09:15` reads `09h00–09h15` in French, as it does on the site."""
    return value.replace(":", "h") if lang == "fr" else value


def styles(lang: str) -> dict:
    return {
        "title": ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=20,
                                leading=24, textColor=NAVY, spaceAfter=2),
        "subtitle": ParagraphStyle("subtitle", fontName="Helvetica", fontSize=10.5,
                                   leading=14.5, textColor=GREEN, spaceAfter=8),
        "lede": ParagraphStyle("lede", fontName="Helvetica", fontSize=9.2,
                               leading=13.5, textColor=MUTED, alignment=TA_JUSTIFY),
        "meta": ParagraphStyle("meta", fontSize=9.5, leading=14, textColor=INK,
                               fontName="Helvetica-Bold"),
        "org": ParagraphStyle("org", fontSize=8.4, leading=12, textColor=MUTED,
                              fontName="Helvetica"),
        "orgr": ParagraphStyle("orgr", fontSize=7.8, leading=11, textColor=MUTED,
                               fontName="Helvetica", alignment=TA_RIGHT),
        # The band: a small amber label over a white value. The label is what
        # lets the three cells be read at a glance instead of decoded.
        "blabel": ParagraphStyle("blabel", fontName="Helvetica-Bold", fontSize=6.4,
                                 leading=9, textColor=AMBER, spaceAfter=1),
        "bvalue": ParagraphStyle("bvalue", fontName="Helvetica-Bold", fontSize=9.6,
                                 leading=13, textColor=colors.white),
        "banner": ParagraphStyle("banner", fontName="Helvetica-Bold", fontSize=11,
                                 leading=14, textColor=colors.white),
        "strap": ParagraphStyle("strap", fontSize=8.4, leading=12,
                                textColor=colors.HexColor("#BED3C6"),
                                fontName="Helvetica-Oblique"),
        "th": ParagraphStyle("th", fontName="Helvetica-Bold", fontSize=8.2,
                             leading=11, textColor=colors.white),
        "time": ParagraphStyle("time", fontName="Helvetica-Bold", fontSize=8.6,
                               leading=12, textColor=NAVY),
        "stitle": ParagraphStyle("stitle", fontName="Helvetica-Bold", fontSize=8.8,
                                 leading=12, textColor=INK, spaceAfter=1),
        "sdesc": ParagraphStyle("sdesc", fontSize=7.9, leading=11, textColor=MUTED,
                                alignment=TA_JUSTIFY, fontName="Helvetica"),
        "tag": ParagraphStyle("tag", fontName="Helvetica-Bold", fontSize=7,
                              leading=10, textColor=GREEN, spaceBefore=2),
        "foot": ParagraphStyle("foot", fontSize=7.4, leading=10, textColor=MUTED,
                               fontName="Helvetica"),
    }


#: Languages whose stale-configuration notice has already been printed. The
#: dates are needed both by the title block and by the running head, and the
#: warning is about the file, not about the number of times it is read.
_ANNOUNCED: set[str] = set()


def furniture(config: dict, lang: str) -> tuple[str, str]:
    """
    The dates and venue, preferring the configuration and saying so when it is
    unusable. A document that announces "TBC" on its cover is worse than one
    built from the dates the website already states.
    """
    ws = config.get("workshop", {})
    dates = (ws.get(f"dates_{lang}") or "").strip()
    venue = (ws.get(f"venue_{lang}") or "").strip()
    stale = []
    if not dates or "TBC" in dates.upper() or "CONFIRMER" in dates.upper():
        dates, _ = FALLBACK_DATES[lang], stale.append("dates")
    if not venue or "TBC" in venue.upper() or "CONFIRMER" in venue.upper():
        venue, _ = FALLBACK_VENUE[lang], stale.append("venue")
    if stale and lang not in _ANNOUNCED:
        _ANNOUNCED.add(lang)
        print(f"    [i] config/workshop.yml {' and '.join(stale)} still unset for "
              f"'{lang}' — used the dates the website states.")
    return dates, venue


# ---------------------------------------------------------------------------
#  The document
# ---------------------------------------------------------------------------
def page_furniture(canvas, doc, *, title: str, right: str, footer: str):
    """A hairline masthead and a page number, drawn on every page."""
    canvas.saveState()
    w, h = A4

    canvas.setStrokeColor(AMBER)
    canvas.setLineWidth(2)
    canvas.line(MARGIN, h - 11 * mm, w - MARGIN, h - 11 * mm)

    canvas.setFont("Helvetica", 7.2)
    canvas.setFillColor(MUTED)
    canvas.drawString(MARGIN, h - 9 * mm, title)
    canvas.drawRightString(w - MARGIN, h - 9 * mm, right)

    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN, 12 * mm, w - MARGIN, 12 * mm)
    canvas.setFont("Helvetica", 7)
    canvas.drawString(MARGIN, 8.5 * mm, footer)
    canvas.drawRightString(w - MARGIN, 8.5 * mm, str(canvas.getPageNumber()))
    canvas.restoreState()


def title_block(config: dict, agenda: dict, lang: str, st: dict) -> list:
    ws = config.get("workshop", {})
    org = config.get("organisers", {})
    S = STRINGS[lang]
    dates, venue = furniture(config, lang)

    days = agenda["days"]
    n_sessions = sum(len(d["sessions"]) for d in days)
    n_labs = len(agenda.get("labs", {}))

    lead = pick(org.get("lead", {}), "name", lang)
    partner = pick(org.get("partner", {}), "name", lang)
    framework = pick(org, "framework", lang)

    width = A4[0] - 2 * MARGIN
    out = []

    # A letterhead line: the African Union emblem beside the two organisers, as
    # on the invitation letters this agenda accompanies. Absent emblem, the text
    # simply takes the full width — a missing image must not cost the identity.
    emblem = ROOT / "assets" / "letterhead" / "image1.png"
    org_line = [Paragraph(f"{lead}<br/>{partner}", st["org"]),
                Paragraph(escape(framework), st["orgr"])]
    if emblem.exists():
        head = Table([[Image(str(emblem), width=13 * mm, height=13 * mm)] + org_line],
                     colWidths=[17 * mm, (width - 17 * mm) * 0.52,
                                (width - 17 * mm) * 0.48])
    else:
        head = Table([org_line], colWidths=[width * 0.52, width * 0.48])
    head.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (0, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ("LINEBELOW", (0, 0), (-1, -1), 0.6, LINE),
    ]))
    out += [head, Spacer(1, 6 * mm)]

    out += [
        Paragraph(pick(ws, "title", lang), st["title"]),
        Paragraph(pick(ws, "subtitle", lang), st["subtitle"]),
        Spacer(1, 4 * mm),
    ]

    # The three facts a reader checks first, given the weight they deserve:
    # a solid navy band, each value under a small amber label. The pale strip
    # this replaces put the venue adrift in the right half of the page.
    def cell(label: str, value: str):
        return [Paragraph(label, st["blabel"]), Paragraph(value, st["bvalue"])]

    band = Table([[cell(S["l_dates"], escape(dates)),
                   cell(S["l_venue"], escape(venue)),
                   cell(S["l_shape"], S["shape"].format(
                       days=len(days), sessions=n_sessions, labs=n_labs))]],
                 colWidths=[width * 0.36, width * 0.28, width * 0.36])
    band.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY),
        ("LINEBEFORE", (0, 0), (0, -1), 3, AMBER),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    out += [band, Spacer(1, 6 * mm)]

    out += [Paragraph(S["lede"], st["lede"]), Spacer(1, 6 * mm)]
    return out


def day_block(day: dict, agenda: dict, lang: str, st: dict) -> list:
    S = STRINGS[lang]
    width = A4[0] - 2 * MARGIN

    banner = Table(
        [[Paragraph(f"{S['day']} {day['n']} &nbsp;·&nbsp; {pick(day, 'title', lang)}",
                    st["banner"])],
         [Paragraph(f"{pick(day, 'weekday', lang)} — {pick(day, 'strap', lang)}",
                    st["strap"])]],
        colWidths=[width])
    banner.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY),
        ("LINEBEFORE", (0, 0), (0, -1), 3, AMBER),
        ("LEFTPADDING", (0, 0), (-1, -1), 9), ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (0, 0), 7), ("BOTTOMPADDING", (0, 0), (0, 0), 1),
        ("TOPPADDING", (0, 1), (0, 1), 0), ("BOTTOMPADDING", (0, 1), (0, 1), 7),
    ]))

    rows = [[Paragraph(S["time"], st["th"]), Paragraph(S["session"], st["th"])]]
    for s in day["sessions"]:
        cell = [Paragraph(pick(s, "title", lang), st["stitle"])]
        desc = pick(s, "desc", lang)
        if desc:
            cell.append(Paragraph(desc, st["sdesc"]))
        label = MODE_LABEL.get(s.get("mode", "talk"), ("", ""))[0 if lang == "en" else 1]
        if label:
            cell.append(Paragraph(label.upper(), st["tag"]))
        rows.append([Paragraph(fmt_time(s["time"], lang), st["time"]), cell])

    table = Table(rows, colWidths=[COL_TIME, COL_BODY], repeatRows=1)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), GREEN),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.4, LINE),
        ("LEFTPADDING", (0, 0), (-1, -1), 7), ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]
    for i in range(1, len(rows)):
        if i % 2 == 0:
            style.append(("BACKGROUND", (0, i), (-1, i), WASH))
    table.setStyle(TableStyle(style))

    return [CondPageBreak(45 * mm), banner, table, Spacer(1, 6 * mm)]


def build(agenda: dict, config: dict, lang: str, path: Path) -> None:
    st = styles(lang)
    S = STRINGS[lang]
    ws = config.get("workshop", {})
    gh = config.get("github", {})
    dates, venue = furniture(config, lang)

    masthead = f"{ws.get('code', 'STG17')} · {pick_raw(ws, 'title', lang)}"
    right = f"{venue} · {dates}"
    # The running foot carries the institutional frame, not the build recipe.
    # Where the document comes from is a maintainer's question, so it lives in
    # the PDF metadata below, where a maintainer looks and a participant does not.
    footer = (f"{ws.get('code', 'STG17')} · "
              f"{pick_raw(config.get('organisers', {}), 'framework', lang)}")

    def on_page(canvas, doc):
        page_furniture(canvas, doc, title=masthead, right=right, footer=footer)

    doc = SimpleDocTemplate(
        str(path), pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=18 * mm, bottomMargin=16 * mm,
        title=f"{ws.get('code', 'STG17')} — {S['doc_title']}",
        author=pick_raw(config.get("organisers", {}).get("lead", {}), "name", lang),
        subject=pick_raw(ws, "subtitle", lang),
        creator="config/agenda.yml via tools/build_agenda_pdf.py — regenerate, do not edit",
        # Without this, reportlab stamps the current time into /CreationDate and
        # /ID, so two runs a second apart differ in about forty bytes. The file
        # is committed and build_all.py regenerates it, which would show both
        # PDFs as modified on every run with nothing having changed.
        invariant=True,
    )

    story = title_block(config, agenda, lang, st)
    for day in agenda["days"]:
        story += day_block(day, agenda, lang, st)

    if gh.get("org") and gh.get("repo"):
        url = f"https://{gh['org']}.github.io/{gh['repo']}/"
        if lang == "fr":
            url += "fr/"
        story += [Spacer(1, 2 * mm),
                  Paragraph(f"{S['site']} <font color='#1B7A43'>{url}</font>", st["foot"])]

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)


# ---------------------------------------------------------------------------
def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    ap = argparse.ArgumentParser(
        description="Build the STG17 agenda as a PDF, in English and in French.")
    ap.add_argument("--out", default=str(ROOT / "docs" / "downloads"),
                    help="directory to write the PDFs into")
    ap.add_argument("--lang", choices=["en", "fr", "both"], default="both")
    args = ap.parse_args()

    agenda = yaml.safe_load((ROOT / "config" / "agenda.yml").read_text(encoding="utf-8"))
    config = yaml.safe_load((ROOT / "config" / "workshop.yml").read_text(encoding="utf-8"))

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    langs = ["en", "fr"] if args.lang == "both" else [args.lang]

    failed = []
    for lang in langs:
        path = out / f"STG17_Agenda_{lang.upper()}.pdf"
        try:
            build(agenda, config, lang, path)
        except PermissionError:
            failed.append(path)
            print(f"[!] {path.name} is open in another program — not written.")
            continue
        n = sum(len(d["sessions"]) for d in agenda["days"])
        print(f"Written: {path}   ({len(agenda['days'])} days, {n} sessions, "
              f"{path.stat().st_size // 1024} KB)")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
