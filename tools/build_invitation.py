#!/usr/bin/env python3
"""
STG17 · The invitation letter to the African Development Bank, in French and English.

    python tools/build_invitation.py
    python tools/build_invitation.py --out "C:/AfDB/Momar/STG17/Workshop Sep 2026"

--------------------------------------------------------------------------
WHAT THIS CHANGES FROM THE ORIGINAL
--------------------------------------------------------------------------
Two things, and nothing else. The reference number, the date, the addressee, the
subject, the dates and venue, and the signature block are reproduced exactly as
they stand in `STG17_Lettre_invitation_BAD.docx`; they are the sender's, not
mine to revise.

  1. A paragraph recommending the profile of the experts to be designated —
     the Data Innovation Lab or Unit, the Data Science Unit, or the Innovation
     Unit or Lab. The English unit names are kept verbatim inside the French
     letter, in parentheses, because they are organisational designations and
     translating them would make them harder to match against a real org chart.

  2. An English version of the whole letter.

Both languages are held side by side in `LETTER` below, so a change to one is
made next to the other rather than in a different file a week later. The AU
letterhead — the emblem, the Arabic title, the five language names — is rebuilt
from images extracted out of the original document, so the two versions carry the
same masthead as the letter they descend from.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt, RGBColor

ROOT = Path(__file__).resolve().parent.parent
LETTERHEAD = ROOT / "assets" / "letterhead"

BLACK = RGBColor(0x00, 0x00, 0x00)

#: The five-language masthead, laid out as in the original: English, Arabic and
#: Swahili down the left, the emblem in the centre, French, Portuguese and
#: Spanish down the right.
MASTHEAD_LEFT = ["AFRICAN UNION", None, "UMOJA WA AFRIKA"]   # None = the Arabic image
MASTHEAD_RIGHT = ["UNION AFRICAINE", "UNIÃO AFRICANA", "UNIÓN AFRICANA"]

LETTER = {
    "fr": {
        "filename": "STG17_Lettre_invitation_BAD_FR.docx",
        "ref": "Réf. : CCP/OSPD/STAT/07.26.099",
        "date": "Date : 2 septembre 2026",
        "addressee": "À Monsieur le Directeur du Département des statistiques de la Banque "
                     "africaine de développement (BAD)",
        "subject": "Objet : Invitation à l’atelier de renforcement des capacités du Groupe "
                   "technique spécialisé sur les questions émergentes (GTS 17), du 28 septembre "
                   "au 2 octobre 2026 à Kigali (Rwanda)",
        "salutation": "Monsieur le Directeur du Département,",
        "body": [
            "L’Institut de statistique de l’Union africaine (STATAFRIC) organise en collaboration "
            "avec la Banque africaine de développement (BAD) un atelier de renforcement des "
            "capacités du Groupe technique spécialisé sur les questions émergentes (GTS 17), "
            "intitulé « Opérationnaliser les données non traditionnelles, les technologies du Big "
            "Data et l’intelligence artificielle au service de la statistique publique africaine », "
            "du 28 septembre au 2 octobre 2026 à Kigali, au Rwanda.",

            "Cet atelier a pour objectif général de renforcer les capacités techniques et "
            "méthodologiques des instituts nationaux de la statistique africains dans "
            "l’utilisation des sources de données non traditionnelles, des technologies du Big "
            "Data et de l’intelligence artificielle, en dotant chaque pays membre du GTS 17 d’un "
            "cas d’usage national documenté et reproductible, construit sur un socle "
            "technologique commun.",

            "La Banque africaine de développement (BAD) assure le secrétariat du Bureau du GTS 17 "
            "et, à ce titre, ses experts assureront l’animation technique de l’atelier durant les "
            "cinq jours de travaux. Aussi avons-nous le plaisir de vous inviter, ainsi que les "
            "experts que vous voudrez bien désigner à cet effet, à prendre une part active à "
            "cette rencontre.",

            # --- the paragraph this version adds -------------------------------
            "Compte tenu du caractère résolument technique et pratique des travaux — chaque "
            "demi-journée associe un exposé bref à un laboratoire prolongé sur machine — nous "
            "recommandons que les experts désignés soient issus en priorité du laboratoire ou de "
            "l’unité d’innovation par les données (Data Innovation Lab or Unit), de l’unité de "
            "science des données (Data science unit), ou de l’unité ou du laboratoire "
            "d’innovation (Innovation unit or lab). Une pratique effective de la programmation, "
            "de l’analyse de données ou du déploiement de solutions d’intelligence artificielle "
            "sera particulièrement précieuse, les participants étant appelés à produire eux-mêmes "
            "des résultats reproductibles tout au long de la semaine.",

            "Nous vous saurions gré de bien vouloir nous faire parvenir, dans les meilleurs "
            "délais, les noms, fonctions et coordonnées des experts de la Banque chargés de cette "
            "animation technique, ainsi que toute information utile à la bonne préparation de "
            "l’atelier.",

            "Dans cette attente, et vous remerciant de l’appui constant que la Banque apporte aux "
            "travaux du GTS 17, nous vous prions d’agréer, Monsieur le Directeur du Département, "
            "l’expression de notre haute considération.",
        ],
        "signature": ["M. Adoum GAGOLOUM",
                      "Chef de la Division des statistiques économiques, STATAFRIC",
                      "Commission de l’Union africaine"],
    },
    "en": {
        "filename": "STG17_Invitation_Letter_AfDB_EN.docx",
        "ref": "Ref.: CCP/OSPD/STAT/07.26.099",
        "date": "Date: 2 September 2026",
        "addressee": "To the Director of the Statistics Department, African Development Bank (AfDB)",
        "subject": "Subject: Invitation to the capacity-building workshop of the Specialized "
                   "Technical Group on Emerging Issues (STG 17), 28 September to 2 October 2026, "
                   "Kigali (Rwanda)",
        "salutation": "Dear Director,",
        "body": [
            "The African Union Institute for Statistics (STATAFRIC), in collaboration with the "
            "African Development Bank (AfDB), is organising a capacity-building workshop of the "
            "Specialized Technical Group on Emerging Issues (STG 17), entitled “Operationalising "
            "non-traditional data, Big Data technologies and artificial intelligence in the "
            "service of African official statistics”, from 28 September to 2 October 2026 in "
            "Kigali, Rwanda.",

            "The general objective of the workshop is to strengthen the technical and "
            "methodological capacity of African national statistical institutes in the use of "
            "non-traditional data sources, Big Data technologies and artificial intelligence, by "
            "equipping every STG 17 member country with a documented and reproducible national "
            "use case, built on a common technological foundation.",

            "The African Development Bank (AfDB) provides the secretariat of the STG 17 Bureau "
            "and, in that capacity, its experts will lead the technical facilitation of the "
            "workshop throughout the five days of proceedings. We therefore have the pleasure of "
            "inviting you, together with the experts you may wish to designate for this purpose, "
            "to take an active part in this meeting.",

            "Given the decidedly technical and hands-on nature of the proceedings — each half-day "
            "pairs a short presentation with an extended laboratory at the keyboard — we "
            "recommend that the designated experts be drawn, as a priority, from the Data "
            "Innovation Lab or Unit, the Data Science Unit, or the Innovation Unit or Lab. "
            "Practical experience in programming, data analysis or the deployment of artificial "
            "intelligence solutions will be particularly valuable, as participants are expected "
            "to produce reproducible results themselves throughout the week.",

            "We should be grateful if you would send us, at your earliest convenience, the names, "
            "positions and contact details of the Bank’s experts responsible for this technical "
            "facilitation, together with any information useful to the proper preparation of the "
            "workshop.",

            "Pending your reply, and thanking you for the Bank’s constant support to the work of "
            "STG 17, please accept, Dear Director, the assurance of our highest consideration.",
        ],
        "signature": ["Mr Adoum GAGOLOUM",
                      "Head of the Economic Statistics Division, STATAFRIC",
                      "African Union Commission"],
    },
}


def run(paragraph, text: str, *, size=12, bold=False, align=None, space_after=10,
        space_before=0, name="Calibri"):
    paragraph.paragraph_format.space_after = Pt(space_after)
    paragraph.paragraph_format.space_before = Pt(space_before)
    if align is not None:
        paragraph.alignment = align
    r = paragraph.add_run(text)
    r.font.name = name
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.color.rgb = BLACK
    return r


def masthead(doc) -> None:
    """
    The African Union five-language masthead, rebuilt from the original's images.

    Laid out as a borderless 3x3 grid so the emblem sits between the two language
    columns and stays put when the text below reflows.
    """
    table = doc.add_table(rows=3, cols=3)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    for i in range(3):
        for j, width in enumerate((2.3, 1.4, 2.3)):
            table.cell(i, j).width = Inches(width)

    emblem = LETTERHEAD / "image1.png"
    arabic = LETTERHEAD / "image2.png"

    for i, text in enumerate(MASTHEAD_LEFT):
        cell = table.cell(i, 0)
        cell.text = ""
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(0)
        if text is None:
            if arabic.exists():
                p.add_run().add_picture(str(arabic), width=Inches(0.81))
        else:
            run(p, text, size=10, bold=True, space_after=0)

    cell = table.cell(0, 1)
    cell.merge(table.cell(2, 1))
    cell.text = ""
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if emblem.exists():
        p.add_run().add_picture(str(emblem), width=Inches(0.75))

    for i, text in enumerate(MASTHEAD_RIGHT):
        cell = table.cell(i, 2)
        cell.text = ""
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(0)
        run(p, text, size=10, bold=True, space_after=0)


def build(letter: dict) -> Document:
    doc = Document()
    s = doc.sections[0]
    s.page_width, s.page_height = Inches(8.27), Inches(11.69)
    s.left_margin = s.right_margin = Inches(0.75)
    s.top_margin = s.bottom_margin = Inches(0.5)

    normal = doc.styles["Normal"]
    normal.font.name = "Calibri"
    normal.font.size = Pt(12)

    masthead(doc)
    run(doc.add_paragraph(), "", size=6, space_after=6)

    run(doc.add_paragraph(), letter["ref"], size=11, bold=True, space_after=0)
    run(doc.add_paragraph(), letter["date"], size=11, bold=True, space_after=16)

    run(doc.add_paragraph(), letter["addressee"], bold=True, space_after=14)
    run(doc.add_paragraph(), letter["subject"], bold=True, space_after=16)
    run(doc.add_paragraph(), letter["salutation"], space_after=12)

    for text in letter["body"]:
        run(doc.add_paragraph(), text, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after=10)

    run(doc.add_paragraph(), "", size=8, space_after=12)
    for i, line in enumerate(letter["signature"]):
        run(doc.add_paragraph(), line, bold=True,
            align=WD_ALIGN_PARAGRAPH.RIGHT, space_after=0 if i < 2 else 8)
    return doc


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    ap = argparse.ArgumentParser(
        description="Build the STG17 invitation letter in French and English.")
    ap.add_argument("--out", default=str(ROOT / "concept-note"),
                    help="directory to write the two .docx files into")
    ap.add_argument("--lang", choices=["fr", "en", "both"], default="both")
    args = ap.parse_args()

    if not (LETTERHEAD / "image1.png").exists():
        print(f"[!] Letterhead images missing from {LETTERHEAD}. The letters will be built "
              f"without the African Union emblem — restore them before sending.")

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    langs = ["fr", "en"] if args.lang == "both" else [args.lang]

    failed = []
    for lang in langs:
        letter = LETTER[lang]
        path = out / letter["filename"]
        try:
            build(letter).save(path)
        except PermissionError:
            failed.append(path)
            print(f"[!] {path.name} is open in another program — not written.")
            continue
        words = sum(len(p.split()) for p in letter["body"])
        print(f"Written: {path}   ({words} words in the body)")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
