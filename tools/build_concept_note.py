#!/usr/bin/env python3
"""
STG17 · Regenerate the workshop concept note and agenda as a Word document.

    python tools/build_concept_note.py
    python tools/build_concept_note.py --out "C:/AfDB/Momar/STG17/Workshop Sep 2026"

--------------------------------------------------------------------------
WHY THIS IS GENERATED RATHER THAN EDITED
--------------------------------------------------------------------------
The original V05082026_2 document was written before the material existed, and it
had already drifted from it: it announces nine laboratories where the agenda now
carries thirteen, and describes laboratory environments that were superseded once
the notebooks were actually built (FAISS and Chroma for a corpus of a few thousand
passages; native function calling for an exercise that has to run without an API
key).

Everything factual here therefore comes from `config/agenda.yml` — the same file
that generates the website, the day pages and the laboratory register. Edit the
agenda; regenerate the note. The narrative sections, which describe institutional
history and organiser commitments rather than material, are carried over from the
original and are the only prose held in this file.

The layout mirrors the original: A4, 0.75-inch margins, Cambria headings in AfDB
gold and green, a title block, day banners, and the same eight sections.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml
from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# The original's palette, read off the document rather than invented.
GOLD = RGBColor(0xC0, 0x8A, 0x1E)
GREEN = RGBColor(0x0A, 0x35, 0x27)
NAVY = RGBColor(0x0B, 0x25, 0x45)
INK = RGBColor(0x33, 0x40, 0x3A)
MUTED = RGBColor(0x6B, 0x7B, 0x75)
WASH = "F4F8F5"
BANNER = "0A3527"
HEADROW = "0B2545"

MODE_LABEL = {
    "talk": "Talk",
    "lab": "Laboratory",
    "plenary": "Plenary · countries",
    "facilitated": "Facilitated",
    "ceremony": "Ceremony",
    "benchmark": "Benchmark · teams",
}


# ---------------------------------------------------------------------------
#  Narrative — carried from the original, corrected only where it had drifted
# ---------------------------------------------------------------------------
TITLE_BLOCK = [
    ("African Development Bank  ·  African Union  ·  SHaSA II", 9, MUTED, False),
    ("Specialized Technical Group on Emerging Issues", 9, MUTED, False),
    ("STG17", 22, GOLD, True),
    ("Technical Workshop", 11, MUTED, False),
    ("Emerging Issues, Emerging Practice", 17, GREEN, True),
    ("Innovating the Data Value Chain", 12, GREEN, False),
    ("Artificial Intelligence, Large Language Models and Big Data for Official Statistics", 10, INK, False),
    ("Hands-on applications to Ookla, WorldPop and Night-Time Lights", 10, MUTED, False),
]

BACKGROUND = [
    ("h3", "From SHaSA II to a Specialized Technical Group on Emerging Issues"),
    ("p", "The Executive Council of the thirtieth African Union Summit, held in Addis Ababa on "
          "28 and 29 January 2018, adopted SHaSA II together with its action plan, financing plan "
          "and resource mobilisation strategy, as the continental strategy for the development of "
          "statistics in Africa, and invited Member States to implement it. SHaSA II is "
          "operationalised through Specialized Technical Groups, one for each of its eighteen "
          "priority focus areas. STG17 is the group responsible for emerging issues — big data, "
          "open data and, increasingly, artificial intelligence."),
    ("h3", "The first Annual Meeting — Kigali, 10–12 September 2025"),
    ("p", "The African Development Bank, as Secretariat of STG17, and AU STATAFRIC convened the "
          "group’s first Annual Meeting in Kigali. The meeting validated the terms of reference of "
          "STG17, established its Bureau — chaired by Somalia, with Tunisia, Mozambique and "
          "Cameroon as vice-chairs and Côte d’Ivoire as rapporteur — and agreed the continental "
          "medium-term Action Plan 2025–2030 that this workshop serves."),
    ("h3", "What the countries said they needed"),
    ("p", "Country presentations and two working groups converged, without much dissent, on the "
          "same diagnosis. Considerable experience already exists across the continent — data "
          "innovation labs, mobile phone and satellite imagery projects, national AI and data "
          "strategies — but it is unevenly documented and rarely shared in a form others can "
          "reuse. Five obstacles were identified as holding back the effective and systematic use "
          "of alternative data sources. This workshop is built around them."),
    ("p", "The meeting also asked that artificial intelligence be taken seriously but handled "
          "carefully, with quality and ethics kept in view. That caution is deliberately built "
          "into the agenda rather than confined to a closing disclaimer: verification of LLM "
          "output before publication, confidentiality rules for microdata, evaluation sets, and "
          "honest statements of what a proxy indicator cannot support."),
]

OBSTACLES = [
    ("Obstacle identified in Kigali", "How this workshop responds"),
    ("Obstacles to accessing new data sources — legal frameworks, cost of access, usability",
     "Access and partnership models with private data holders (Day 3 morning); working directly "
     "with an openly licensed source and its restrictions (Ookla, CC BY-NC-SA); licensing, DOI "
     "and citation in the publication session (Day 5)"),
    ("Absence of harmonised methodologies, preventing efficient exchange between countries",
     "Every country team runs the same documented pipeline on the same three sources; all "
     "notebooks and READMEs land in one public GitHub organisation, forming the raw material for "
     "the methodological guidelines under activity 2.1.1"),
    ("Open questions on the quality of alternative sources and the applicability of official "
     "quality frameworks",
     "Coverage and selection bias in non-probabilistic sources (Day 3); validation of the NTL "
     "proxy against official subnational statistics, and an explicit limitations statement as "
     "part of every deliverable (Day 4)"),
    ("Weaknesses in NSO IT and big data infrastructure",
     "AI infrastructure fundamentals, cost modelling and sovereignty trade-offs (Day 1 "
     "afternoon); big data technologies and a hands-on comparison of when the added complexity "
     "is warranted (Day 3 afternoon) — feeding activity 4.2.3"),
    ("Gaps in human resources, skills and data roles",
     "The workshop itself, framed by a baseline and end-line self-assessment feeding the "
     "competencies framework (4.1.1), and by draft chapters for the reference manual on key "
     "data skills (4.2.1)"),
    ("Need for a champion system and for structured exchange between offices",
     "Country experience exchange on Day 1 and country presentations on Day 5, both designed to "
     "surface reusable work and name owners for follow-up projects (3.1.1, 3.1.2)"),
]

OUTPUTS = [
    ("Workshop output", "Feeds STG17 Action Plan activity"),
    ("Public GitHub repository: notebooks, dashboards and technical notes on Ookla, WorldPop and NTL",
     "2.1.1 — Methodological guidelines for the use of new data sources (1 topic/year)"),
    ("Draft chapters for the reference manual on key data skills",
     "4.2.1 — Reference manuals developed and webinar on key data skills"),
    ("Country experience exchange on AI and non-traditional data (Day 1 morning)",
     "3.3.2 — AI strategy: sharing of experience; 3.1.2 — Regional pooling of efforts"),
    ("AI infrastructure requirements assessed by participants (Day 1 afternoon)",
     "4.2.3 — Framework on infrastructure architecture approaches"),
    ("Ethics, licensing and data-acquisition checklist", "4.3 — Reference guide on Data Governance"),
    ("Baseline and end-line skills self-assessment", "4.1.1 — Competencies reference framework"),
    ("Country presentations of work produced during the week (Day 5)",
     "3.1.1 — Champion-led projects; 3.1.2 — Regional pooling of efforts"),
    ("Key takeaways and follow-up webinar topics agreed on Day 5",
     "1.3.1 — Brown bag webinar series (max 2/year)"),
    ("Modalities of access to private-sector data (Ookla, telecom operators)",
     "3.1 — Private sector partnerships"),
]

OBJECTIVES = [
    "Position the core AI concepts in relation to one another — AI, LLM, prompt engineering, RAG, "
    "fine-tuning, agentic systems, agents and MCP — and explain where each fits in the statistical "
    "value chain.",
    "Assess the infrastructure an NSO actually needs to run AI workloads: compute, storage, "
    "serving, cost and sovereignty trade-offs.",
    "Design, engineer and optimise prompts, and select the right model and inference provider for "
    "a given statistical task.",
    "Deploy LLMs across a portfolio of professional use cases: coding, report writing, "
    "presentations, graphics and visual identity, document analysis.",
    "Acquire, process and publish non-traditional data — Ookla Speedtest, WorldPop and Night-Time "
    "Lights — as subnational statistical indicators.",
    "Build a reproducible analytical product and publish it publicly on GitHub, with documented "
    "methods, limitations and licensing.",
    "Learn from what peer countries have already achieved, and identify at least one collaboration "
    "or reuse opportunity for their own office.",
]

PREPARATION = [
    ("When", "Who", "What"),
    ("T − 6 weeks", "Secretariat (AfDB)",
     "Confirm dates, venue, hybrid platform and interpretation; issue invitations carrying the "
     "country input request and the data-pack list"),
    ("T − 4 weeks", "Country focal points",
     "Confirm participants and nominate the country team that will carry the work through to Friday"),
    ("T − 4 weeks", "Lead facilitator",
     "Freeze the notebook set in both guided and open versions; create the GitHub organisation and "
     "one repository per country"),
    ("T − 3 weeks", "Technical assistants",
     "Mirror the Ookla tiles, WorldPop rasters and NTL subsets for every participating country and "
     "prepare the pre-clipped extracts and the reference country"),
    ("T − 2 weeks", "Participants",
     "Send the six country slides; create a GitHub account; submit the national data pack"),
    ("T − 2 weeks", "Secretariat",
     "Provision LLM and Groq API keys with per-participant quotas; provision and load the "
     "Elasticsearch cluster"),
    ("T − 1 week", "Technical assistants",
     "Run the remote environment check — one hour, offered twice in two time zones — and resolve "
     "machine-level problems before Day 1"),
    ("T − 1 week", "Lead facilitator",
     "Dry-run every laboratory end to end on a workshop-specification machine, timing each step"),
    ("Day 0", "All",
     "Room and network test; distribution of the USB keys carrying all data, notebooks and slides"),
    ("T + 1 week", "Secretariat",
     "Publish recordings and notebooks; consolidate the commitments board into a dated follow-up "
     "calendar circulated to the Bureau"),
]

RISKS = (
    "Bandwidth is the most frequent cause of laboratory failure, which is why every dataset is "
    "mirrored locally and distributed on USB keys rather than downloaded during sessions. Failed "
    "or rate-limited API keys are handled by per-participant quotas provisioned in advance and by "
    "a facilitator-run demonstration path for each API-dependent step; in addition, every "
    "laboratory that uses a model has a documented path that runs without one. Heterogeneous "
    "laptops are absorbed by the Colab fallback, tested during the environment check rather than "
    "discovered on Day 1. Uneven skill levels are handled by the two-track notebooks and by "
    "pairing participants across levels from Day 3 onwards. Incomplete national data — a missing "
    "boundary file, an indicator available only at national level — is handled by the fully "
    "prepared reference country, so that no team loses a day. Finally, the Day 1 country exchange "
    "is the session most likely to overrun; a timekeeper is appointed and the synthesis slot "
    "absorbs any overflow."
)

PRACTICAL = [
    ("Before the workshop",
     "Three items are requested from each participant at least two weeks in advance, and the "
     "workshop does not run smoothly without them. First, a country input for the Day 1 morning "
     "exchange: a maximum of six slides on what has been attempted at home in AI and "
     "non-traditional data, including what did not work. Second, a personal GitHub account, since "
     "laboratory outputs are published publicly from Day 2 onwards. Third, the national data "
     "pack: an administrative boundary file, one national statistical publication for the Day 2 "
     "dashboard exercise, and at least one official subnational indicator — GDP, population or "
     "electrification rate — for the Day 4 validation. A short remote environment check is "
     "offered in the week before the workshop, and an environment-check notebook is distributed "
     "so that participants can run it themselves beforehand."),
    ("Participants",
     "Laptop with administrator rights, 16 GB RAM recommended, and a stable internet connection. "
     "Participants work in country or sub-regional teams of two to four from Day 3 onwards; the "
     "same team carries its work through to the Friday presentation."),
    ("Facilitation",
     "One lead facilitator supported by two technical assistants for laboratory support, at a "
     "ratio of roughly one assistant per ten participants. Remote participants are grouped into "
     "virtual breakout teams, each with a dedicated assistant. A resource person supports the "
     "visual identity and image-generation station on Day 2."),
    ("Technical set-up",
     "A workshop GitHub organisation is created in advance and hosts all notebooks, dashboards "
     "and outputs. Every notebook opens directly in Google Colab from a badge and is also "
     "distributed on a USB key, so a restricted machine is never a blocker. API access to LLM "
     "providers, including Groq, is provisioned centrally with per-participant keys. Datasets — "
     "Ookla tiles, WorldPop rasters and the NTL subsets — are downloaded and mirrored locally in "
     "advance, since bandwidth is the single most common cause of laboratory delay. An "
     "Elasticsearch cluster is pre-provisioned and pre-loaded for Day 3, so that no session time "
     "is spent on installation."),
    ("Hybrid arrangements",
     "Presentations are streamed with simultaneous interpretation. Laboratories run in mixed "
     "on-site and remote teams. All recordings, notebooks and published dashboards remain "
     "available afterwards as inputs to the brown bag webinar series (activity 1.3.1)."),
]


# ---------------------------------------------------------------------------
#  Document helpers
# ---------------------------------------------------------------------------
def shade(cell, hex_colour: str) -> None:
    el = OxmlElement("w:shd")
    el.set(qn("w:val"), "clear")
    el.set(qn("w:fill"), hex_colour)
    cell._tc.get_or_add_tcPr().append(el)


def cell_text(cell, text: str, *, size=8.5, bold=False, colour=INK, space_after=0):
    cell.text = ""
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(space_after or 2)
    run = p.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = colour
    return p


def heading(doc, text: str, level: int):
    p = doc.add_paragraph(style=f"Heading {level}")
    run = p.add_run(text)
    run.font.name = "Cambria"
    run.font.size = Pt(13 if level == 1 else 11)
    run.font.bold = True
    run.font.color.rgb = GOLD if level == 1 else GREEN
    p.paragraph_format.space_before = Pt(14 if level == 1 else 10)
    p.paragraph_format.space_after = Pt(6)
    return p


def body(doc, text: str, *, size=9.5, colour=INK, italic=False, bullet=False):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    if bullet:
        p.paragraph_format.left_indent = Inches(0.22)
    run = p.add_run(("▪  " if bullet else "") + text)
    run.font.name = "Calibri"
    run.font.size = Pt(size)
    run.font.italic = italic
    run.font.color.rgb = colour
    return p


def grid(doc, rows, widths, *, header=True, sizes=None):
    table = doc.add_table(rows=len(rows), cols=len(rows[0]))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    for i, row in enumerate(rows):
        for j, value in enumerate(row):
            cell = table.cell(i, j)
            cell.width = Inches(widths[j])
            if header and i == 0:
                shade(cell, HEADROW)
                cell_text(cell, value, size=8.5, bold=True, colour=RGBColor(0xFF, 0xFF, 0xFF))
            else:
                if i % 2 == 0:
                    shade(cell, WASH)
                cell_text(cell, value, size=(sizes or 8.5))
    return table


# ---------------------------------------------------------------------------
#  Generated sections
# ---------------------------------------------------------------------------
def key_facts(agenda: dict, labs: dict) -> list[tuple[str, str]]:
    """Facts about the week, counted from the agenda rather than asserted."""
    days = len(agenda["days"])
    sessions = sum(len(d["sessions"]) for d in agenda["days"])
    talks = sum(1 for d in agenda["days"] for s in d["sessions"]
                if s.get("mode") in {"talk", "benchmark"})
    lab_sessions = sum(1 for d in agenda["days"] for s in d["sessions"] if s.get("mode") == "lab")
    return [
        ("Duration", f"{days} days — 27 contact hours "
                     f"(Monday to Thursday: 6 h per day; Friday: morning only)"),
        ("Daily rhythm", "Morning 09:00 – 12:30  ·  Lunch 12:30 – 14:00  ·  Afternoon 14:00 – 17:00"),
        ("Format", "Hybrid workshop — each half-day pairs a short presentation with an extended "
                   "hands-on laboratory"),
        ("Structure", f"{sessions} sessions: {talks} presentations, {lab_sessions} laboratory "
                      f"slots covering {len(labs)} specified laboratories, plus ceremonies, "
                      f"plenaries and facilitated discussion"),
        ("Organisers", "African Development Bank (AfDB), Secretariat of STG17, with AU STATAFRIC"),
        ("Opening & closing", "Jointly by AfDB and AU STATAFRIC — Day 1 morning and Day 5 morning"),
        ("Participants", "Senior NSO officials in statistical innovation, IT and data science; "
                         "REC and AFRISTAT experts"),
        ("Working languages", "English and French throughout. Every presentation and every "
                              "notebook is produced in both languages from a single source, so "
                              "the two versions cannot drift apart"),
        ("Country coverage", "All 55 African Union member states. Each notebook is driven by one "
                             "country parameter; the registry supplies boundaries, satellite "
                             "tiles and projection for every member state"),
        ("Shared output", "All laboratory work published on the workshop GitHub organisation"),
        ("Anchored in", "STG17 Action Plan 2025–2030 — Work Package 4.2, feeding WP 1, 2, 3 and 4"),
    ]


def fmt_plan(plan, sep: str) -> str:
    """
    Action Plan references, as text.

    `plan: [4.2.1, 2.1.1]` is a list of strings, but a bare `plan: 4.2` is read by
    YAML as a float — so every element is coerced rather than assumed.
    """
    if isinstance(plan, (list, tuple)):
        return sep.join(str(x) for x in plan)
    return str(plan)


def add_agenda(doc, agenda: dict) -> None:
    for day in agenda["days"]:
        banner = doc.add_table(rows=1, cols=1)
        cell = banner.cell(0, 0)
        cell.width = Inches(6.8)
        shade(cell, BANNER)
        cell.text = ""
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(5)
        p.paragraph_format.space_after = Pt(5)
        r = p.add_run(f"Day {day['n']}   |   {day['weekday_en']}\n")
        r.font.name = "Cambria"; r.font.size = Pt(12); r.font.bold = True
        r.font.color.rgb = RGBColor(0xF2, 0xA9, 0x00)
        r = p.add_run(f"{day['title_en']}\n")
        r.font.name = "Cambria"; r.font.size = Pt(11); r.font.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        r = p.add_run(day.get("strap_en", ""))
        r.font.name = "Calibri"; r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(0xC9, 0xDA, 0xD2)
        doc.add_paragraph().paragraph_format.space_after = Pt(2)

        morning = [s for s in day["sessions"] if s["time"] < "13:00"]
        afternoon = [s for s in day["sessions"] if s["time"] >= "13:00"]
        for label, block in (("Morning  ·  09:00 – 12:30", morning),
                             ("Afternoon  ·  14:00 – 17:00", afternoon)):
            if not block:
                continue
            p = body(doc, label, size=9, colour=GREEN)
            p.runs[0].font.bold = True
            rows = [("Time", "Session", "Mode", "Action Plan")]
            for s in block:
                # YAML reads a bare 4.2 as a float, so every element is coerced.
                plan = fmt_plan(s.get("plan", ""), " / ")
                rows.append((
                    s["time"],
                    f"{s['title_en']}\n{s.get('desc_en', '')}",
                    MODE_LABEL.get(s.get("mode", ""), s.get("mode", "")),
                    plan,
                ))
            grid(doc, rows, [0.85, 4.0, 1.05, 0.9], sizes=8.0)
            doc.add_paragraph().paragraph_format.space_after = Pt(2)


def add_labs(doc, labs: dict) -> None:
    rows = [("Laboratory", "Environment and data", "Team deliverable", "Fallback")]
    for key, lab in labs.items():
        rows.append((
            f"D{lab['day']} · {lab['title_en']}",
            lab.get("env_en", ""),
            lab.get("deliverable_en", ""),
            lab.get("fallback_en", ""),
        ))
    grid(doc, rows, [1.25, 2.1, 1.8, 1.65], sizes=7.5)


def add_mapping(doc, agenda: dict) -> None:
    rows = [("Workshop topic", "Day", "Primary STG17 activities served")]
    for day in agenda["days"]:
        for s in day["sessions"]:
            if s.get("mode") in {"ceremony"} or not s.get("plan"):
                continue
            plan = fmt_plan(s["plan"], " · ")
            half = "AM" if s["time"] < "13:00" else "PM"
            rows.append((s["title_en"], f"D{day['n']} {half}", plan))
    grid(doc, rows, [3.6, 0.75, 2.45], sizes=8.0)


def add_materials(doc, agenda: dict, labs: dict) -> None:
    ready = [k for k, v in labs.items() if v.get("status") == "ready"]
    decks = sorted({s["deck"] for d in agenda["days"] for s in d["sessions"] if s.get("deck")})
    built = sorted(p.name for p in (ROOT / "slides" / "decks").glob("*.deck.html"))
    notebooks = sorted(p.name for p in (ROOT / "notebooks").rglob("*.ipynb"))

    heading(doc, "State of the material", 3)
    body(doc,
         f"This section reports what exists at the date of this note, not what is planned. "
         f"Of {len(decks)} presentations in the agenda, {len(built)} are written and published in "
         f"both languages. Of {len(labs)} specified laboratories, {len(ready)} are complete and "
         f"runnable end to end. They are distributed as {len(notebooks)} notebooks: each "
         f"laboratory exists in English and French and in a guided and an open version, and the "
         f"environment-check notebook is supplied in both languages.")
    body(doc,
         "Two tracks in every laboratory. Participants arrive with markedly different levels. "
         "Each notebook therefore exists in two versions: a guided version in which the "
         "analytical steps are written and the participant fills the gaps, and an open version "
         "containing only the objective and the data. Teams choose at the start of each "
         "laboratory and may switch. The deliverable is identical either way, which keeps the "
         "Friday presentations comparable.")
    body(doc,
         "Every laboratory has a documented fallback, listed in the table above. The rule adopted "
         "throughout is that no laboratory may depend on a step that has not been tested in "
         "advance on the workshop machines, and that every team must be able to reach its "
         "deliverable even if its own national data, its network or its API key turns out to be "
         "unusable.")


# ---------------------------------------------------------------------------
#  Assembly
# ---------------------------------------------------------------------------
def build(agenda: dict, labs: dict) -> Document:
    doc = Document()
    s = doc.sections[0]
    s.page_width, s.page_height = Inches(8.27), Inches(11.69)
    for side in ("left_margin", "right_margin", "top_margin", "bottom_margin"):
        setattr(s, side, Inches(0.75))

    normal = doc.styles["Normal"]
    normal.font.name = "Calibri"
    normal.font.size = Pt(9.5)
    normal.font.color.rgb = INK

    # --- title block ---
    block = doc.add_table(rows=1, cols=1)
    cell = block.cell(0, 0)
    cell.width = Inches(6.8)
    shade(cell, WASH)
    cell.text = ""
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(10)
    for i, (text, size, colour, bold) in enumerate(TITLE_BLOCK):
        run = p.add_run(("\n" if i else "") + text)
        run.font.name = "Cambria" if bold or size > 10 else "Calibri"
        run.font.size = Pt(size)
        run.font.bold = bold
        run.font.color.rgb = colour
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    grid(doc, [(k, v) for k, v in key_facts(agenda, labs)], [1.5, 5.3],
         header=False, sizes=8.5)

    heading(doc, "1  Background", 1)
    for kind, text in BACKGROUND:
        heading(doc, text, 3) if kind == "h3" else body(doc, text)
    grid(doc, OBSTACLES, [3.0, 3.8], sizes=8.0)

    heading(doc, "2  Rationale and link with the STG17 Action Plan", 1)
    body(doc, "This workshop is a direct operational instrument of Work Package 4 — Capacity "
              "building and transfer, specifically activity 4.2 “Capacity Building on Emerging "
              "Technologies: project-driven training”. It is deliberately designed so that its "
              "outputs are not consumed by the training alone, but feed four other work packages "
              "of the Action Plan.")
    grid(doc, OUTPUTS, [3.6, 3.2], sizes=8.0)

    heading(doc, "3  Learning objectives", 1)
    body(doc, "By the end of the workshop, participants will be able to:")
    for objective in OBJECTIVES:
        body(doc, objective, bullet=True)

    heading(doc, "4  Detailed agenda", 1)
    body(doc, "How to read the tables. The Mode column indicates the working format — talk, "
              "laboratory, plenary or ceremony — and the team composition for laboratories. The "
              "Action Plan column gives the STG17 Action Plan activities that the session feeds, "
              "so that every hour of the week can be justified against the 2025–2030 commitments. "
              "Session titles and descriptions below are generated from the workshop’s own agenda "
              "file, which is also what produces the website and the laboratory register.")
    add_agenda(doc, agenda)

    heading(doc, "5  Topic ↔ Action Plan mapping", 1)
    add_mapping(doc, agenda)

    heading(doc, "6  Laboratory specifications", 1)
    body(doc, f"{len(labs)} laboratories carry the week. Each is specified below with the "
              f"environment it needs, the artefact the team must produce, and the fallback the "
              f"facilitation team applies when something breaks — which it will.")
    add_labs(doc, labs)
    add_materials(doc, agenda, labs)

    heading(doc, "7  Preparation timeline and responsibilities", 1)
    body(doc, "The agenda holds only if the preparation below is completed. The critical path "
              "runs through the mirroring of national datasets and the provisioning of API "
              "access; both must be finished a fortnight before the workshop opens.")
    grid(doc, PREPARATION, [1.1, 1.5, 4.2], sizes=8.0)
    heading(doc, "Known risks and how they are handled", 3)
    body(doc, RISKS)

    heading(doc, "8  Practical requirements", 1)
    for title, text in PRACTICAL:
        heading(doc, title, 3)
        body(doc, text)

    body(doc, "Generated from config/agenda.yml — the same source that produces the workshop "
              "website, the day pages and the laboratory register. Regenerate with "
              "tools/build_concept_note.py rather than editing this file, or the two will drift.",
         size=8, colour=MUTED, italic=True)
    return doc


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    ap = argparse.ArgumentParser(description="Regenerate the STG17 concept note and agenda.")
    ap.add_argument("--out", default=str(ROOT / "concept-note"),
                    help="directory to write the .docx into")
    ap.add_argument("--name",
                    default="STG17_Workshop_Agenda_Emerging_Issues_Emerging_Practice.docx")
    args = ap.parse_args()

    agenda = yaml.safe_load((ROOT / "config" / "agenda.yml").read_text(encoding="utf-8"))
    labs = agenda["labs"]

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    path = out / args.name
    build(agenda, labs).save(path)

    ready = sum(1 for v in labs.values() if v.get("status") == "ready")
    print(f"Written: {path}")
    print(f"  {len(agenda['days'])} days · "
          f"{sum(len(d['sessions']) for d in agenda['days'])} sessions · "
          f"{len(labs)} laboratories ({ready} ready) · "
          f"{path.stat().st_size / 1024:.0f} KB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
