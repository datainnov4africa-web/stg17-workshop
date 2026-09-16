#!/usr/bin/env python3
"""
STG17 · Render the agenda into the website, in both languages.

    python tools/build_site.py

Reads `config/agenda.yml` and `config/workshop.yml` and writes:

    docs/dayN/index.md      docs/dayN/index.fr.md      one page per day
    docs/labs/index.md      docs/labs/index.fr.md      the laboratory register
    docs/resources/action-plan.md  (+ .fr.md)          topic <-> Action Plan mapping

Why generate rather than hand-write
-----------------------------------
The concept note requires the project structure to follow the agenda. Ten pages
in two languages transcribed by hand would drift from the agenda within a week,
and a website that contradicts the printed agenda is worse than no website. So
the agenda is data, and the pages are a rendering of it. Change a session time
in `agenda.yml`, re-run, and both languages update together.

The convention `index.md` / `index.fr.md` is the suffix layout of
mkdocs-static-i18n: English is the default build, French is served under /fr/.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"

MODE_LABEL = {
    "ceremony":  ("Ceremony", "Cérémonie"),
    "talk":      ("Talk", "Exposé"),
    "lab":       ("Laboratory", "Laboratoire"),
    "plenary":   ("Plenary", "Plénière"),
    "facilitated": ("Facilitated", "Animée"),
    "benchmark": ("Talk + benchmark", "Exposé + benchmark"),
    # V16 pairs a short talk with the laboratory that follows it, in one slot.
    "talk_lab": ("Talk + laboratory", "Exposé + laboratoire"),
}
MODE_ICON = {
    "ceremony": ":material-account-group:", "talk": ":material-presentation:",
    "lab": ":material-flask:", "plenary": ":material-forum:",
    "facilitated": ":material-lightbulb-on:", "benchmark": ":material-speedometer:",
    "talk_lab": ":material-presentation-play:",
}
STATUS_LABEL = {
    "ready":  (":material-check-circle:{ .ok } Available",
               ":material-check-circle:{ .ok } Disponible"),
    "phase1": (":material-progress-clock: Day 1 batch", ":material-progress-clock: Lot Jour 1"),
    "phase2": (":material-progress-clock: Day 2 batch", ":material-progress-clock: Lot Jour 2"),
    "phase3": (":material-progress-clock: Day 3 batch", ":material-progress-clock: Lot Jour 3"),
    "phase4": (":material-progress-clock: Day 4 batch", ":material-progress-clock: Lot Jour 4"),
    "phase5": (":material-progress-clock: Day 5 batch", ":material-progress-clock: Lot Jour 5"),
}

# The breaks as the V16 document schedules them. Kept here rather than in the
# agenda file because they are the same every day and carry no content; the
# importer skips the "Coffee Break" rows for the same reason.
BREAKS = {
    "10:30–10:45": ("Coffee break", "Pause café"),
    "12:30–14:00": ("Lunch", "Déjeuner"),
    "16:45–17:00": ("Coffee break", "Pause café"),
}

GENERATED = {
    "en": "<!-- GENERATED from config/agenda.yml by tools/build_site.py. Do not edit. -->",
    "fr": "<!-- GÉNÉRÉ depuis config/agenda.yml par tools/build_site.py. Ne pas modifier. -->",
}


def load_yaml(path: Path):
    import yaml

    return yaml.safe_load(path.read_text(encoding="utf-8"))


def pick(entry: dict, key: str, lang: str, default: str = "") -> str:
    return entry.get(f"{key}_{lang}", entry.get(f"{key}_en", default))


def fmt_time(value: str, lang: str) -> str:
    """
    `09:00–12:30` in English, `09h00-12h30` in French.

    A small thing, but the French pages are read by francophone statisticians and
    an English clock format on every line of the agenda reads as a translation
    that was not finished.
    """
    if lang != "fr":
        return value
    return re.sub(r"(\d{2}):(\d{2})", r"\1h\2", value)


# ---------------------------------------------------------------------------
#  Notebook links
# ---------------------------------------------------------------------------
#: Where organisers drop the presentation files. One flat folder, because a
#: person copying a file should not have to work out which subfolder it belongs
#: in. The expected name for every session is printed by `tools/downloads.py`.
DOWNLOADS = ROOT / "docs" / "downloads"

#: Hyphen before the language code, never a dot: mkdocs-static-i18n claims any
#: `.en.` or `.fr.` segment in ANY filename as its own suffix convention, and
#: would publish only one of the two files. This already broke the decks once.
DOWNLOAD_KINDS = (
    ("pdf", ":material-file-pdf-box:"),
    ("pptx", ":material-microsoft-powerpoint:"),
)


def download_links(session: dict, lang: str) -> str:
    """
    Buttons for the files that exist, and nothing for the files that do not.

    A greyed-out button for material nobody has produced yet tells a visitor the
    workshop is unfinished; an absent button tells them nothing at all, which is
    what was asked for. The moment a file is dropped into docs/downloads/ under
    the expected name, its button appears on the next build.
    """
    session_id = session.get("id")
    if not session_id:
        return ""

    found = []
    for code, icon in DOWNLOAD_KINDS:
        for tag in ("EN", "FR"):
            name = f"{session_id}-{tag}.{code}"
            if (DOWNLOADS / name).exists():
                found.append(f"[{icon} {code.upper()} · {tag}](../downloads/{name})"
                             "{ .md-button }")
    return " ".join(found)


def notebook_links(lab: dict, lang: str, github: dict) -> str:
    """
    Colab badges and repository links for one laboratory, in the active language.

    Only emitted for laboratories whose notebooks actually exist. A badge that
    404s on Day 4 morning is worse than no badge, so the register shows the
    honest status instead.
    """
    stem = lab.get("notebook")
    if not stem or lab.get("status") != "ready":
        return ""

    org, repo, branch = github.get("org"), github.get("repo"), github.get("branch", "main")
    day = lab.get("day")
    out = []
    labels = {
        "en": ("guided", "open", "Earth Engine variant"),
        "fr": ("guidée", "ouverte", "variante Earth Engine"),
    }[lang]

    for suffix, label in ((f"_{lang.upper()}", labels[0]), (f"_{lang.upper()}_open", labels[1])):
        path = f"notebooks/day{day}/{stem}{suffix}.ipynb"
        colab = f"https://colab.research.google.com/github/{org}/{repo}/blob/{branch}/{path}"
        out.append(f"[![Colab]({{{{ colab_badge }}}})]({colab}) **{label}** &nbsp; "
                   f"[:material-github:](https://github.com/{org}/{repo}/blob/{branch}/{path})")

    gee_stem = lab.get("gee_notebook")
    if gee_stem:
        path = f"notebooks/day{day}/{gee_stem}_{lang.upper()}.ipynb"
        colab = f"https://colab.research.google.com/github/{org}/{repo}/blob/{branch}/{path}"
        out.append(f"[![Colab]({{{{ colab_badge }}}})]({colab}) **{labels[2]}** &nbsp; "
                   f"[:material-github:](https://github.com/{org}/{repo}/blob/{branch}/{path})")

    return "\n\n".join(out).replace("{{ colab_badge }}",
                                    "https://colab.research.google.com/assets/colab-badge.svg")


# ---------------------------------------------------------------------------
#  Day pages
# ---------------------------------------------------------------------------
def render_day(day: dict, labs: dict, lang: str, config: dict) -> str:
    fr = lang == "fr"
    github = config.get("github", {})
    lines = [GENERATED[lang], ""]

    weekday = pick(day, "weekday", lang)
    title = pick(day, "title", lang)
    strap = pick(day, "strap", lang)

    lines += [
        f"# {'Jour' if fr else 'Day'} {day['n']} — {title}",
        "",
        f"*{weekday} · {strap}*",
        "",
    ]

    # Morning / afternoon split at 14:00
    morning = [s for s in day["sessions"] if s["time"] < "13:00"]
    afternoon = [s for s in day["sessions"] if s["time"] >= "13:00"]

    for label, block in ((("Matinée · 09h00 – 12h30" if fr else "Morning · 09:00 – 12:30"), morning),
                         (("Après-midi · 14h00 – 17h00" if fr else "Afternoon · 14:00 – 17:00"),
                          afternoon)):
        if not block:
            continue
        lines += [f"## {label}", ""]

        # Sessions and breaks on one timeline. A break belongs to the half-day
        # it starts in — lunch at 12:30 closes the morning — and is printed in
        # sequence, so the reader can follow the day without reconstructing it.
        timeline = [(s["time"], "session", s) for s in block]
        # A break earns its line only when it separates something. Day 5 closes
        # at 12:45, so lunch must not print after the closing ceremony; the
        # 16:45 coffee, which V16 schedules after the last session, must.
        starts = [s["time"].split("–")[0] for s in block]
        last_end = max((s["time"].split("–")[-1] for s in block), default="")
        timeline += [
            (span, "break", names) for span, names in BREAKS.items()
            if (span < "13:00") == (block is morning)
            and (any(start >= span.split("–")[-1] for start in starts)
                 or span.split("–")[0] == last_end)
        ]

        for start, kind, payload in sorted(timeline, key=lambda item: item[0]):
            if kind == "break":
                break_en, break_fr = payload
                lines += [f'!!! quote "{fmt_time(start, lang)} — '
                          f'{break_fr if fr else break_en}"', ""]
                continue
            session = payload
            icon = MODE_ICON.get(session.get("mode", "talk"), "")
            mode = MODE_LABEL.get(session.get("mode", "talk"), ("", ""))[1 if fr else 0]
            lines += [
                f"### {fmt_time(session['time'], lang)} &nbsp;·&nbsp; {pick(session, 'title', lang)}",
                "",
                f"{icon} **{mode}**"
                + (f" &nbsp;·&nbsp; *{session['presenter']}*"
                   if session.get("presenter") else "")
                + (f" &nbsp;·&nbsp; {'Plan d’action' if fr else 'Action Plan'} "
                   f"{' · '.join(str(p) for p in session.get('plan', []))}"
                   if session.get("plan") else ""),
                "",
                pick(session, "desc", lang),
                "",
            ]

            deck = session.get("deck")
            if deck:
                verb = "Diapositives" if fr else "Slides"
                lines += [f"[:material-presentation: {verb}](../slides/index.md#deck-{deck})"
                          "{ .md-button .md-button--primary }", ""]

            files = download_links(session, lang)
            if files:
                lines += [files, ""]

            lab_id = session.get("lab")
            if lab_id and lab_id in labs:
                lab = labs[lab_id]
                links = notebook_links(lab, lang, github)
                status = STATUS_LABEL.get(lab.get("status", "phase1"), ("", ""))[1 if fr else 0]
                lines += [
                    '!!! example "'
                    + ("Laboratoire — " if fr else "Laboratory — ")
                    + pick(lab, "title", lang) + '"',
                    "",
                    # French typography puts a space before the colon; English does not.
                    f"    **{'Livrable :' if fr else 'Deliverable:'}** "
                    + pick(lab, "deliverable", lang),
                    "",
                    f"    **{'Repli :' if fr else 'Fallback:'}** " + pick(lab, "fallback", lang),
                    "",
                    f"    **{'Statut :' if fr else 'Status:'}** {status}",
                    "",
                ]
                if links:
                    lines += ["    " + line for line in links.splitlines()] + [""]
            lines.append("")


    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
#  Laboratory register
# ---------------------------------------------------------------------------
def render_week(agenda: dict, labs: dict, lang: str, config: dict) -> str:
    """
    The whole week on one page.

    The five day pages carry the detail; this one carries the shape. It exists
    because "show me the agenda" is a request for one page, and answering it with
    five links is answering a different question. It is also the page a
    facilitator prints and pins to the wall.

    Generated from the same agenda.yml as everything else, so it cannot drift
    from the day pages it summarises.
    """
    fr = lang == "fr"
    lines = [GENERATED[lang], ""]

    lines += [
        "# " + ("L'agenda de la semaine" if fr else "The week at a glance"),
        "",
        ("*Cinq jours, du concept au dépôt publié. Chaque séance renvoie à sa page "
         "de jour, à sa présentation et à son laboratoire.*" if fr else
         "*Five days, from the concepts to a published repository. Every session links "
         "to its day page, its deck and its laboratory.*"),
        "",
    ]

    icon = {"talk": ":material-presentation:", "lab": ":material-flask:",
            "benchmark": ":material-speedometer:", "panel": ":material-account-group:",
            "ceremony": ":material-star:", "wrap": ":material-flag-checkered:"}

    for day in agenda["days"]:
        n = day["n"]
        lines += [
            f"## {'Jour' if fr else 'Day'} {n} · {pick(day, 'title', lang)}",
            "",
            f"*{pick(day, 'weekday', lang)} · {pick(day, 'strap', lang)}* "
            f"— [{'page détaillée' if fr else 'day page'} →](../day{n}/index.md)",
            "",
            ("| Heure | Séance | Type | Ressource |" if fr else
             "| Time | Session | Kind | Resource |"),
            "|---|---|---|---|",
        ]
        for s in day["sessions"]:
            mode = s.get("mode", "talk")
            kind = icon.get(mode, ":material-circle-small:")
            link = "—"
            if s.get("deck"):
                link = (f"[{'Diapositives' if fr else 'Slides'}]"
                        f"(../slides/index.md#deck-{s['deck']})")
            elif mode == "lab":
                link = f"[{'Laboratoires' if fr else 'Laboratories'}](../labs/index.md)"
            title = pick(s, "title", lang).replace("|", "·")
            lines.append(f"| {fmt_time(s['time'], lang)} | {title} | {kind} | {link} |")
        lines.append("")

    ready = sum(1 for v in labs.values() if v.get("status") == "ready")
    lines += [
        "---",
        "",
        "## " + ("Où en est la préparation" if fr else "Preparation status"),
        "",
        (f"**{ready} laboratoires sur {len(labs)}** sont prêts et exécutables. "
         f"Les autres portent la mention *lot Jour N* sur leur page — la matière "
         f"existe dans l'agenda, les carnets arrivent par phases." if fr else
         f"**{ready} of {len(labs)} laboratories** are ready and runnable. The rest "
         f"are marked *Day N batch* on their page — the material exists in the "
         f"agenda; the notebooks arrive in phases."),
        "",
        ("Chaque laboratoire a un chemin de repli documenté, pour qu'une clé "
         "manquante ou un réseau contraint ne mette jamais fin à une séance." if fr else
         "Every laboratory has a documented fallback, so that a missing key or a "
         "constrained network never ends a session."),
        "",
    ]
    return "\n".join(lines)


def render_labs(agenda: dict, lang: str, config: dict) -> str:
    fr = lang == "fr"
    labs = agenda["labs"]
    github = config.get("github", {})
    lines = [GENERATED[lang], ""]

    lines += [
        "# " + ("Les laboratoires" if fr else "The laboratories"),
        "",
        (f"{len(labs)} laboratoires portent la semaine. Chacun est spécifié ci-dessous avec "
         "l'environnement qu'il exige, la production que l'équipe doit livrer, et le chemin de "
         "repli appliqué par l'équipe d'animation quand quelque chose casse — ce qui arrivera."
         if fr else
         f"{len(labs)} laboratories carry the week. Each is specified below with the environment it "
         "needs, the artefact the team must produce, and the fallback the facilitation team "
         "applies when something breaks — which it will."),
        "",
        ("!!! tip \"Deux pistes dans chaque laboratoire\"\n\n"
         "    Les participants arrivent avec des niveaux très différents. Chaque carnet existe "
         "donc en deux versions : une version **guidée**, où les étapes analytiques sont écrites "
         "et où le participant comble les trous, et une version **ouverte**, ne contenant que "
         "l'objectif et les données. Les équipes choisissent au début de chaque laboratoire et "
         "peuvent basculer. Le livrable est identique dans les deux cas, ce qui garde les "
         "présentations du vendredi comparables."
         if fr else
         "!!! tip \"Two tracks in every laboratory\"\n\n"
         "    Participants arrive with markedly different levels. Each notebook therefore exists "
         "in two versions: a **guided** version in which the analytical steps are written and the "
         "participant fills the gaps, and an **open** version containing only the objective and "
         "the data. Teams choose at the start of each laboratory and may switch. The deliverable "
         "is identical either way, which keeps the Friday presentations comparable."),
        "",
    ]

    by_day: dict[int, list] = {}
    for lab_id, lab in labs.items():
        by_day.setdefault(lab["day"], []).append((lab_id, lab))

    for day_n in sorted(by_day):
        lines += [f"## {'Jour' if fr else 'Day'} {day_n}", ""]
        for lab_id, lab in by_day[day_n]:
            status = STATUS_LABEL.get(lab.get("status", "phase1"), ("", ""))[1 if fr else 0]
            lines += [
                f"### {pick(lab, 'title', lang)}",
                "",
                f"| | |",
                f"|---|---|",
                f"| **{'Équipe' if fr else 'Team'}** | {pick(lab, 'team', lang)} |",
                f"| **{'Pays par défaut' if fr else 'Default country'}** | `{lab.get('country', 'CIV')}` "
                + ("— changez `COUNTRY_ISO3` pour le vôtre |" if fr
                   else "— change `COUNTRY_ISO3` to your own |"),
                f"| **{'Environnement et données' if fr else 'Environment and data'}** | "
                + pick(lab, "env", lang) + " |",
                f"| **{'Livrable de l’équipe' if fr else 'Team deliverable'}** | "
                + pick(lab, "deliverable", lang) + " |",
                f"| **{'Repli' if fr else 'Fallback'}** | " + pick(lab, "fallback", lang) + " |",
                f"| **{'Variante Earth Engine' if fr else 'Earth Engine variant'}** | "
                + (("oui — aucun téléchargement" if fr else "yes — nothing downloaded")
                   if lab.get("gee") else "—") + " |",
                f"| **{'Statut' if fr else 'Status'}** | {status} |",
                "",
            ]
            links = notebook_links(lab, lang, github)
            if links:
                lines += [links, ""]

    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
#  Action Plan mapping
# ---------------------------------------------------------------------------
ACTIVITIES = {
    "1.3.1": ("Brown bag webinar series (max 2/year)", "Série de webinaires « brown bag » (max 2/an)"),
    "2.1.1": ("Methodological guidelines for the use of new data sources",
              "Lignes directrices méthodologiques pour l'usage des nouvelles sources"),
    "3.1":   ("Private sector partnerships", "Partenariats avec le secteur privé"),
    "3.1.1": ("Champion-led projects", "Projets portés par des champions"),
    "3.1.2": ("Regional pooling of efforts", "Mutualisation régionale des efforts"),
    "3.2.1": ("Cooperation with universities", "Coopération avec les universités"),
    "3.3.2": ("AI strategy: sharing of experience", "Stratégie IA : partage d'expérience"),
    "4.1.1": ("Competencies reference framework", "Cadre de référence des compétences"),
    "4.2":   ("Capacity building on emerging technologies",
              "Renforcement des capacités sur les technologies émergentes"),
    "4.2.1": ("Reference manuals and webinar on key data skills",
              "Manuels de référence et webinaire sur les compétences clés en données"),
    "4.2.2": ("Skills transfer · UN Big Data Hub", "Transfert de compétences · Centre ONU mégadonnées"),
    "4.2.3": ("Framework on infrastructure architecture approaches",
              "Cadre sur les approches d'architecture d'infrastructure"),
    "4.3":   ("Reference guide on Data Governance",
              "Guide de référence sur la gouvernance des données"),
}


def render_action_plan(agenda: dict, lang: str) -> str:
    fr = lang == "fr"
    lines = [GENERATED[lang], ""]
    lines += [
        "# " + ("Correspondance thème ↔ Plan d'action" if fr else "Topic ↔ Action Plan mapping"),
        "",
        ("Chaque heure de la semaine est rattachée aux engagements du Plan d'action STG17 "
         "2025-2030. Ce tableau est produit à partir de l'agenda lui-même : il ne peut pas "
         "diverger du programme."
         if fr else
         "Every hour of the week is tied to the commitments of the STG17 Action Plan 2025-2030. "
         "This table is produced from the agenda itself, so it cannot drift from the programme."),
        "",
    ]

    # Invert: activity -> sessions
    index: dict[str, list[str]] = {}
    for day in agenda["days"]:
        for session in day["sessions"]:
            for activity in session.get("plan", []):
                key = str(activity)
                label = (f"{'J' if fr else 'D'}{day['n']} {fmt_time(session['time'], lang)} — "
                         f"{pick(session, 'title', lang)}")
                index.setdefault(key, []).append(label)

    lines += [
        "| " + ("Activité" if fr else "Activity") + " | "
        + ("Intitulé" if fr else "Title") + " | "
        + ("Sessions qui l'alimentent" if fr else "Sessions feeding it") + " |",
        "|---|---|---|",
    ]
    for activity in sorted(index, key=lambda a: [int(p) for p in a.split(".")]):
        title = ACTIVITIES.get(activity, ("—", "—"))[1 if fr else 0]
        sessions = "<br>".join(index[activity])
        lines.append(f"| **{activity}** | {title} | {sessions} |")

    lines += [
        "",
        "## " + ("Ce que l'atelier livre au Plan d'action"
                 if fr else "What the workshop delivers to the Action Plan"),
        "",
        "| " + ("Production de l'atelier" if fr else "Workshop output") + " | "
        + ("Activité alimentée" if fr else "Activity fed") + " |",
        "|---|---|",
    ]
    outputs = [
        (("Public GitHub repository: notebooks, dashboards and technical notes on Ookla, "
          "WorldPop and NTL",
          "Dépôt GitHub public : carnets, tableaux de bord et notes techniques sur Ookla, "
          "WorldPop et NTL"), "2.1.1"),
        (("Draft chapters for the reference manual on key data skills",
          "Projets de chapitres du manuel de référence sur les compétences clés en données"), "4.2.1"),
        (("Country experience exchange on AI and non-traditional data",
          "Échange d'expériences pays sur l'IA et les données non traditionnelles"), "3.3.2 · 3.1.2"),
        (("AI infrastructure requirements assessed by participants",
          "Besoins d'infrastructure IA évalués par les participants"), "4.2.3"),
        (("Ethics, licensing and data-acquisition checklist",
          "Liste de contrôle éthique, licences et acquisition de données"), "4.3"),
        (("Baseline and end-line skills self-assessment",
          "Auto-évaluation initiale et finale des compétences"), "4.1.1"),
        (("Country presentations of work produced during the week",
          "Présentations pays des travaux produits durant la semaine"), "3.1.1 · 3.1.2"),
        (("Key takeaways and follow-up webinar topics",
          "Enseignements clés et thèmes de webinaires de suivi"), "1.3.1"),
        (("Modalities of access to private-sector data (Ookla, telecom operators)",
          "Modalités d'accès aux données du secteur privé (Ookla, opérateurs télécoms)"), "3.1"),
    ]
    for (en, frn), activity in outputs:
        lines.append(f"| {frn if fr else en} | **{activity}** |")

    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
#  Glossary — generated from the package, not transcribed
# ---------------------------------------------------------------------------
GLOSSARY_SECTIONS = [
    ("Artificial intelligence", "Intelligence artificielle",
     ["prompt_engineering", "rag", "fine_tuning", "agent", "hallucination",
      "grounding", "inference", "token", "embedding", "vector_store"]),
    ("Night-time lights", "Lumières nocturnes",
     ["sol", "radiance", "lit_area", "mean_radiance", "blooming", "saturation",
      "gas_flare", "cloud_mask", "quality_flag"]),
    ("Geography", "Géographie",
     ["adm0", "adm1", "adm2", "zonal_stats", "boundaries"]),
    ("Connectivity", "Connectivité",
     ["download_speed", "upload_speed", "latency", "quadkey", "tests"]),
    ("Statistical practice", "Pratique statistique",
     ["proxy", "coverage_bias", "validation", "limitations", "reproducibility",
      "metadata"]),
]

#: One-line definitions. The *terms* come from stg17.i18n.GLOSSARY so that a
#: notebook, a slide and this page always use the same wording; the definitions
#: live here because they belong to the site rather than to the runtime.
DEFINITIONS = {
    "sol": ("The sum of radiance over an area. A proxy for lit activity — not GDP.",
            "La somme de la radiance sur une zone. Un indicateur indirect de l'activité "
            "éclairée — pas le PIB."),
    "radiance": ("Light leaving the ground, in nW·cm⁻²·sr⁻¹, as measured by the sensor.",
                 "La lumière quittant le sol, en nW·cm⁻²·sr⁻¹, telle que mesurée par le capteur."),
    "lit_area": ("The share of territory whose radiance exceeds a chosen threshold. "
                 "Moves when the threshold moves — always publish both.",
                 "La part du territoire dont la radiance dépasse un seuil choisi. Varie avec "
                 "le seuil — publiez toujours les deux."),
    "mean_radiance": ("Average radiance over valid pixels. Nearly meaningless alone, "
                      "because the distribution is extremely skewed.",
                      "Radiance moyenne sur les pixels valides. Presque dénuée de sens seule, "
                      "car la distribution est très asymétrique."),
    "blooming": ("Light spilling beyond its physical source, so a city lights up more "
                 "pixels than it occupies. Inflates urban totals.",
                 "La lumière débordant de sa source physique : une ville éclaire plus de "
                 "pixels qu'elle n'en occupe. Gonfle les totaux urbains."),
    "saturation": ("The brightest cores exceed the sensor's usable range, so growth "
                   "there stops appearing in the data.",
                   "Les cœurs les plus lumineux dépassent la plage exploitable du capteur : "
                   "leur croissance n'apparaît plus dans les données."),
    "gas_flare": ("An industrial flame, extremely bright and constant, that can dominate "
                  "a region's total while electrifying nobody.",
                  "Une flamme industrielle, très lumineuse et constante, qui peut dominer le "
                  "total d'une région sans électrifier personne."),
    "cloud_mask": ("The layer marking pixels obscured by cloud, which must be excluded "
                   "before any statistic is computed.",
                   "La couche marquant les pixels masqués par les nuages, à exclure avant "
                   "tout calcul statistique."),
    "quality_flag": ("Per-pixel metadata describing how trustworthy that observation is.",
                     "Métadonnée par pixel décrivant la fiabilité de l'observation."),
    "adm0": ("The national level.", "Le niveau national."),
    "adm1": ("The first subnational level — regions, provinces, states.",
             "Le premier niveau infranational — régions, provinces, États."),
    "adm2": ("The second subnational level — districts, departments.",
             "Le deuxième niveau infranational — districts, départements."),
    "zonal_stats": ("Summarising a raster within polygon boundaries. The operation that "
                    "turns satellite imagery into a statistical table.",
                    "Résumer un raster à l'intérieur de polygones. L'opération qui transforme "
                    "l'imagerie satellitaire en tableau statistique."),
    "boundaries": ("The polygons defining administrative units. Which file you use "
                   "changes every subnational figure you publish.",
                   "Les polygones définissant les unités administratives. Le fichier retenu "
                   "change chaque chiffre infranational publié."),
    "download_speed": ("Measured throughput toward the user, in kbit/s in the Ookla tiles.",
                       "Débit mesuré vers l'utilisateur, en kbit/s dans les tuiles Ookla."),
    "upload_speed": ("Measured throughput from the user.",
                     "Débit mesuré depuis l'utilisateur."),
    "latency": ("Round-trip delay in milliseconds. Often more decisive than raw speed "
                "for whether a service is usable.",
                "Délai aller-retour en millisecondes. Souvent plus déterminant que le débit "
                "brut pour savoir si un service est utilisable."),
    "quadkey": ("The identifier of a web-Mercator tile. Ookla publishes at zoom 16, "
                "about 611 m at the equator.",
                "L'identifiant d'une tuile Mercator web. Ookla publie au zoom 16, environ "
                "611 m à l'équateur."),
    "tests": ("The number of speed tests behind a tile's average. A tile with three "
              "tests is not comparable with one built from three thousand.",
              "Le nombre de tests de débit derrière la moyenne d'une tuile. Une tuile de "
              "trois tests n'est pas comparable à une tuile de trois mille."),
    "proxy": ("A measurable quantity used to stand in for one you cannot measure "
              "directly. Its usefulness is an empirical question, not an assumption.",
              "Une grandeur mesurable utilisée à la place d'une grandeur qu'on ne peut pas "
              "mesurer directement. Son utilité est une question empirique, pas une hypothèse."),
    "coverage_bias": ("Systematic under-representation of part of the population, "
                      "characteristic of non-probabilistic sources. Ookla measures people "
                      "who run speed tests, not people.",
                      "Sous-représentation systématique d'une partie de la population, propre "
                      "aux sources non probabilistes. Ookla mesure ceux qui lancent des tests "
                      "de débit, pas la population."),
    "validation": ("Establishing, with evidence, the relationship between a proxy and "
                   "an official measure — before publishing either.",
                   "Établir, preuves à l'appui, la relation entre un indicateur indirect et "
                   "une mesure officielle — avant de publier l'un ou l'autre."),
    "limitations": ("The statement of what a result cannot support. In this workshop it "
                    "is part of the deliverable, not an appendix.",
                    "L'exposé de ce qu'un résultat ne peut pas soutenir. Dans cet atelier, "
                    "c'est une partie du livrable, pas une annexe."),
    "reproducibility": ("Whether someone else, with the same inputs, obtains the same "
                        "numbers. Requires the parameters, not just the code.",
                        "Le fait qu'une autre personne, avec les mêmes intrants, obtienne les "
                        "mêmes nombres. Exige les paramètres, pas seulement le code."),
    "metadata": ("The description that makes a dataset findable and interpretable by "
                 "someone who was not in the room.",
                 "La description qui rend un jeu de données trouvable et interprétable par "
                 "quelqu'un qui n'était pas dans la salle."),
    "prompt_engineering": ("Shaping a model's input — role, context, constraints, "
                           "examples — to steer its output. The cheapest lever, and the "
                           "one to exhaust first.",
                           "Façonner l'entrée d'un modèle — rôle, contexte, contraintes, "
                           "exemples — pour orienter sa sortie. Le levier le moins coûteux, "
                           "et le premier à épuiser."),
    "rag": ("Retrieving relevant documents and putting them in the model's context, so "
            "it answers from your material rather than from memory.",
            "Récupérer les documents pertinents et les placer dans le contexte du modèle, "
            "pour qu'il réponde depuis votre matériel plutôt que depuis sa mémoire."),
    "fine_tuning": ("Changing a model's weights on your own examples. The heavy lever — "
                    "try prompting and RAG first.",
                    "Modifier les poids d'un modèle sur vos propres exemples. Le levier "
                    "lourd — essayez d'abord le prompt et le RAG."),
    "agent": ("A model given tools and allowed to decide which to call, in what order. "
              "Powerful, and the reason human checkpoints matter.",
              "Un modèle doté d'outils, autorisé à décider lesquels appeler et dans quel "
              "ordre. Puissant, et la raison pour laquelle les points de contrôle humains "
              "comptent."),
    "hallucination": ("A fluent, confident, false output. Not a bug to be patched — a "
                      "property of the mechanism, to be managed by verification.",
                      "Une sortie fluide, assurée et fausse. Pas un défaut à corriger — une "
                      "propriété du mécanisme, à gérer par la vérification."),
    "grounding": ("Tying an answer to a retrievable source, so a reader can check it.",
                  "Rattacher une réponse à une source récupérable, pour qu'un lecteur "
                  "puisse la vérifier."),
    "inference": ("Running a trained model to produce output. Where the recurring cost "
                  "of an AI system actually sits.",
                  "Exécuter un modèle entraîné pour produire une sortie. C'est là que se "
                  "trouve réellement le coût récurrent d'un système d'IA."),
    "token": ("The sub-word unit a model reads and writes. Cost and context limits are "
              "counted in tokens, not words.",
              "L'unité sous-lexicale que le modèle lit et écrit. Les coûts et les limites "
              "de contexte se comptent en tokens, pas en mots."),
    "embedding": ("A numeric vector representing meaning, so that similarity can be "
                  "computed. The mechanism behind retrieval.",
                  "Un vecteur numérique représentant le sens, afin de pouvoir calculer une "
                  "similarité. Le mécanisme derrière la récupération."),
    "vector_store": ("The index that makes similarity search over embeddings fast.",
                     "L'index qui rend rapide la recherche par similarité sur les plongements."),
}


def render_glossary(lang: str) -> str:
    """
    Build the glossary page from `stg17.i18n.GLOSSARY`.

    Generating rather than transcribing means "Sum of Lights" is translated
    identically in a notebook, on a slide and here — which is the whole point of
    having a shared vocabulary in the first place.
    """
    sys.path.insert(0, str(ROOT))
    from stg17 import i18n  # noqa: PLC0415

    fr = lang == "fr"
    lines = [GENERATED[lang], ""]
    lines += [
        "# " + ("Glossaire" if fr else "Glossary"),
        "",
        ("Le vocabulaire commun de la semaine. Ces termes sont tirés du paquet `stg17` "
         "lui-même : un carnet, une diapositive et cette page emploient nécessairement "
         "la même formulation."
         if fr else
         "The shared vocabulary of the week. These terms come from the `stg17` package "
         "itself, so a notebook, a slide and this page necessarily use the same wording."),
        "",
        ("!!! tip \"Discipline de vocabulaire\"\n\n"
         "    L'exposé du Jour 1 matin existe pour fixer ces mots. Un « agent » et un "
         "« assistant RAG » ne sont pas la même chose, et confondre les deux dans un "
         "cahier des charges coûte cher. Quand un terme est employé de travers pendant "
         "la semaine, revenez ici."
         if fr else
         "!!! tip \"Vocabulary discipline\"\n\n"
         "    The Day 1 morning talk exists to fix these words. An \"agent\" and a "
         "\"RAG assistant\" are not the same thing, and confusing the two in a terms of "
         "reference is expensive. When a term is used loosely during the week, come back "
         "here."),
        "",
    ]

    for title_en, title_fr, keys in GLOSSARY_SECTIONS:
        lines += [f"## {title_fr if fr else title_en}", ""]
        for key in keys:
            term = i18n.GLOSSARY.get(key, (key, key))[1 if fr else 0]
            other = i18n.GLOSSARY.get(key, (key, key))[0 if fr else 1]
            definition = DEFINITIONS.get(key, ("", ""))[1 if fr else 0]
            lines += [f"**{term}**  \n*{other}*", "", f": {definition}", ""]

    lines += [
        "---",
        "",
        ("Un terme manque ? Ajoutez-le à `stg17/i18n.py` et à `tools/build_site.py`, "
         "puis ré-exécutez `python tools/build_site.py`. Il apparaîtra dans les deux "
         "langues."
         if fr else
         "A term missing? Add it to `stg17/i18n.py` and to `tools/build_site.py`, then "
         "run `python tools/build_site.py`. It will appear in both languages."),
        "",
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
def main() -> int:
    try:
        import yaml  # noqa: F401
    except ImportError:
        print("PyYAML is required:  pip install pyyaml")
        return 1

    agenda = load_yaml(ROOT / "config" / "agenda.yml")
    config = load_yaml(ROOT / "config" / "workshop.yml")
    labs = agenda["labs"]

    written = 0
    for day in agenda["days"]:
        target = DOCS / f"day{day['n']}"
        target.mkdir(parents=True, exist_ok=True)
        for lang, name in (("en", "index.md"), ("fr", "index.fr.md")):
            (target / name).write_text(render_day(day, labs, lang, config), encoding="utf-8")
            written += 1

    (DOCS / "week").mkdir(parents=True, exist_ok=True)
    for lang, name in (("en", "index.md"), ("fr", "index.fr.md")):
        (DOCS / "week" / name).write_text(
            render_week(agenda, labs, lang, config), encoding="utf-8")
        written += 1

    (DOCS / "labs").mkdir(parents=True, exist_ok=True)
    for lang, name in (("en", "index.md"), ("fr", "index.fr.md")):
        (DOCS / "labs" / name).write_text(render_labs(agenda, lang, config), encoding="utf-8")
        written += 1

    (DOCS / "resources").mkdir(parents=True, exist_ok=True)
    for lang, name in (("en", "action-plan.md"), ("fr", "action-plan.fr.md")):
        (DOCS / "resources" / name).write_text(render_action_plan(agenda, lang), encoding="utf-8")
        written += 1

    for lang, name in (("en", "glossary.md"), ("fr", "glossary.fr.md")):
        (DOCS / "resources" / name).write_text(render_glossary(lang), encoding="utf-8")
        written += 1

    print(f"Rendered {written} page(s) from config/agenda.yml "
          f"({len(agenda['days'])} days, {len(labs)} laboratories).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
