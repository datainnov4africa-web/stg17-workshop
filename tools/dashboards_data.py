#!/usr/bin/env python3
"""
STG17 · What the participants built, read from the dashboards themselves.

`liens.txt` holds one URL per line, as participants reported them. This module
turns that list into facts: which country, which laboratory, and what the
dashboard actually says — its indicators, its sections, its figures.

Nothing here is written by hand. A description on the page is either a number
lifted from the dashboard or a sentence built from its own structure, because a
showcase that invents findings would misrepresent the work it celebrates.

Three laboratories produced three different dashboards, so three readers:

    stg17-dashboard   Day 2 · a national statistical release, turned into a
                      dashboard. The page is a template; the content lives in
                      data/dashboard_data.json and is read from there.
    connectivity-*    Day 3 · Ookla Speedtest open data against population.
                      Markup: .kpi-l / .kpi-v / .kpi-u, sections in <h2>.
    ntl-*             Day 4 · night-time lights. Markup: .kpi-label /
                      .kpi-value / .kpi-sub, eight tabs.
"""

from __future__ import annotations

import html as H
import json
import re
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LIENS = ROOT / "liens.txt"

#: ISO3 -> (ISO2, French name, English name), for every African Union member.
#:
#: The whole continent rather than the countries that happened to show up: a
#: participant publishing from a country not in this table would otherwise get a
#: card with no flag and no name, and the page would look complete while hiding
#: it. Flags are computed from the ISO2 code, never typed, because a flag is two
#: regional-indicator letters and a typo there is invisible in review.
AFRIQUE = {
    "ago": ("AO", "Angola", "Angola"),
    "bdi": ("BI", "Burundi", "Burundi"),
    "ben": ("BJ", "Bénin", "Benin"),
    "bfa": ("BF", "Burkina Faso", "Burkina Faso"),
    "bwa": ("BW", "Botswana", "Botswana"),
    "caf": ("CF", "République centrafricaine", "Central African Republic"),
    "civ": ("CI", "Côte d'Ivoire", "Côte d'Ivoire"),
    "cmr": ("CM", "Cameroun", "Cameroon"),
    "cod": ("CD", "République démocratique du Congo", "DR Congo"),
    "cog": ("CG", "Congo", "Congo"),
    "com": ("KM", "Comores", "Comoros"),
    "cpv": ("CV", "Cabo Verde", "Cabo Verde"),
    "dji": ("DJ", "Djibouti", "Djibouti"),
    "dza": ("DZ", "Algérie", "Algeria"),
    "egy": ("EG", "Égypte", "Egypt"),
    "eri": ("ER", "Érythrée", "Eritrea"),
    "esh": ("EH", "République arabe sahraouie démocratique", "Sahrawi Republic"),
    "eth": ("ET", "Éthiopie", "Ethiopia"),
    "gab": ("GA", "Gabon", "Gabon"),
    "gha": ("GH", "Ghana", "Ghana"),
    "gin": ("GN", "Guinée", "Guinea"),
    "gmb": ("GM", "Gambie", "Gambia"),
    "gnb": ("GW", "Guinée-Bissau", "Guinea-Bissau"),
    "gnq": ("GQ", "Guinée équatoriale", "Equatorial Guinea"),
    "ken": ("KE", "Kenya", "Kenya"),
    "lbr": ("LR", "Liberia", "Liberia"),
    "lby": ("LY", "Libye", "Libya"),
    "lso": ("LS", "Lesotho", "Lesotho"),
    "mar": ("MA", "Maroc", "Morocco"),
    "mdg": ("MG", "Madagascar", "Madagascar"),
    "mli": ("ML", "Mali", "Mali"),
    "moz": ("MZ", "Mozambique", "Mozambique"),
    "mrt": ("MR", "Mauritanie", "Mauritania"),
    "mus": ("MU", "Maurice", "Mauritius"),
    "mwi": ("MW", "Malawi", "Malawi"),
    "nam": ("NA", "Namibie", "Namibia"),
    "ner": ("NE", "Niger", "Niger"),
    "nga": ("NG", "Nigéria", "Nigeria"),
    "rwa": ("RW", "Rwanda", "Rwanda"),
    "sdn": ("SD", "Soudan", "Sudan"),
    "sen": ("SN", "Sénégal", "Senegal"),
    "sle": ("SL", "Sierra Leone", "Sierra Leone"),
    "som": ("SO", "Somalie", "Somalia"),
    "ssd": ("SS", "Soudan du Sud", "South Sudan"),
    "stp": ("ST", "Sao Tomé-et-Principe", "São Tomé and Príncipe"),
    "swz": ("SZ", "Eswatini", "Eswatini"),
    "syc": ("SC", "Seychelles", "Seychelles"),
    "tcd": ("TD", "Tchad", "Chad"),
    "tgo": ("TG", "Togo", "Togo"),
    "tun": ("TN", "Tunisie", "Tunisia"),
    "tza": ("TZ", "Tanzanie", "Tanzania"),
    "uga": ("UG", "Ouganda", "Uganda"),
    "zaf": ("ZA", "Afrique du Sud", "South Africa"),
    "zmb": ("ZM", "Zambie", "Zambia"),
    "zwe": ("ZW", "Zimbabwe", "Zimbabwe"),
}


def _drapeau(iso2: str) -> str:
    """Two regional indicator letters. Computed, so it cannot be mistyped."""
    return "".join(chr(0x1F1E6 + ord(c) - ord("A")) for c in iso2.upper())


#: What the page uses: ISO3 -> (French, English, flag).
PAYS = {k: (fr, en, _drapeau(i2)) for k, (i2, fr, en) in AFRIQUE.items()}


#: An account that only ever published for one country. `stg17-dashboard`
#: carries no country code in its name, so the account is what identifies it —
#: and the dashboard's own metadata confirms it when the file can be read.
COMPTES = {
    "929213": "gmb", "abate2025": "eth", "benabolaji": "nga", "bigmoussa": "sen",
    "doraboadi": "gha", "dusjbos2": "rwa", "emanelmaasarawi": "egy",
    "hassan-2026": "som", "hatemsedghiani": "tun", "henokskielek1": "nam",
    "loxionmlk": "bwa", "munirmdee1980": "tza", "musttaleb2017": "mar",
    "ranne2": "mdg", "bc2429git": "zwe",
}

FAMILLES = {
    "j2": ("Du document statistique au tableau de bord", "From statistical release to dashboard"),
    "j3": ("Connectivité et population", "Connectivity and population"),
    "j4": ("Lumières nocturnes", "Night-time lights"),
}


def _texte(s: str) -> str:
    return H.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s))).strip()


def entrees() -> list[dict]:
    """
    One entry per distinct dashboard, from liens.txt.

    A line may give the repository rather than the published site —
    `github.com/user/repo` instead of `user.github.io/repo` — which is the same
    work reported differently, so it is converted rather than dropped.
    Duplicates are collapsed; the file is written by hand, under time pressure,
    on the last morning of a workshop.
    """
    vues, out = set(), []
    for ligne in LIENS.read_text(encoding="utf-8-sig").splitlines():
        u = ligne.strip()
        if not u:
            continue
        m = (re.match(r"https://([^.]+)\.github\.io/([^/]+)/?$", u)
             or re.match(r"https://github\.com/([^/]+)/([^/]+)/?$", u))
        if not m:
            continue
        compte, depot = m.group(1), m.group(2)
        cle = f"{compte}__{depot}"
        if cle in vues:
            continue
        vues.add(cle)
        # The repository name says which laboratory it came from. "ntl" marks the
        # night-time lights work and "connectivity" the Ookla work; everything
        # else is the Day 2 exercise — turning a published PDF release into a
        # dashboard — whatever the participant chose to call it. Reading it the
        # other way round, with Day 4 as the default, mislabelled a dashboard
        # named CIPI-Dashboard as night-time lights.
        bas = depot.lower()
        if re.search(r"(^|[-_])ntl([-_]|$)", bas):
            famille = "j4"
        elif "connectivity" in bas:
            famille = "j3"
        else:
            famille = "j2"
        iso = next((c for c in PAYS if re.search(rf"\b{c}\b|[-_]{c}[-_]|[-_]{c}$", depot)), None)
        out.append({
            "cle": cle, "compte": compte, "depot": depot, "famille": famille,
            "iso": iso, "url": f"https://{compte}.github.io/{depot}/",
            "source": u,
        })

    # `stg17-dashboard` is the one repository name that carries no country code,
    # because the Day 2 laboratory never asked for one. The same participant
    # almost always published a connectivity or a lights dashboard too, and
    # those do carry it — so the account answers the question, and no table has
    # to be edited when a new participant appears. relever() still prefers the
    # dashboard's own metadata when that file can be read.
    par_compte: dict[str, str] = {}
    for e in out:
        if e["iso"]:
            par_compte.setdefault(e["compte"], e["iso"])
    for e in out:
        if not e["iso"]:
            e["iso"] = par_compte.get(e["compte"]) or COMPTES.get(e["compte"])
    return out


# ---------------------------------------------------------------------------
#  Reading a dashboard
# ---------------------------------------------------------------------------
import tempfile

CACHE = Path(tempfile.gettempdir()) / "stg17-dashboards-cache"


def _telecharger(url: str, nom: str) -> str | None:
    """Fetched once, then read from disk. These pages reach fourteen megabytes."""
    CACHE.mkdir(parents=True, exist_ok=True)
    f = CACHE / nom
    if f.exists():
        return f.read_text(encoding="utf-8", errors="replace")
    try:
        r = urllib.request.Request(url, headers={"User-Agent": "stg17-site"})
        with urllib.request.urlopen(r, timeout=60) as rep:
            doc = rep.read().decode("utf-8", "replace")
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError):
        return None
    f.write_text(doc, encoding="utf-8")
    return doc


_ATTR_LANG = re.compile(r'data-(en|fr)="([^"]*)"')


def _bilingue(attributs: str, rendu: str) -> dict:
    """{'en': …, 'fr': …} from data-en / data-fr, falling back to what is shown."""
    d = {m.group(1): H.unescape(m.group(2)).strip() for m in _ATTR_LANG.finditer(attributs)}
    vu = _texte(rendu)
    return {"en": d.get("en") or vu, "fr": d.get("fr") or d.get("en") or vu}


def _loc(v, lang: str) -> str:
    """A field that may be a plain string or {"en": …, "fr": …}."""
    if isinstance(v, dict):
        return str(v.get(lang) or v.get("en") or v.get("fr") or "").strip()
    return str(v or "").strip()


def relever(e: dict) -> dict:
    """Everything the page needs about one dashboard, read from the dashboard."""
    e = dict(e)
    if e["famille"] == "j2":
        doc = _telecharger(e["url"] + "data/dashboard_data.json", f"{e['cle']}.json")
        if doc is None:
            # Not every Day 2 dashboard was built by the laboratory's own
            # generator, so the data file may not exist. The page is still real:
            # fall back to reading it as a page.
            return _relever_html(e)
        try:
            d = json.loads(doc)
        except json.JSONDecodeError:
            return _relever_html(e)
        e["vivant"] = True
        meta = d.get("meta", {}) or {}
        e["editeur"] = meta.get("publisher", {})
        e["titre_source"] = meta.get("title", {}) or meta.get("source", {})
        e["periode"] = _loc(meta.get("period", ""), "fr")
        e["kpis"] = [{"label": k.get("labels") or k.get("label") or {},
                      "valeur": k.get("value", k.get("v", "")),
                      "unite": k.get("unit") or k.get("u") or {}}
                     for k in (d.get("kpis") or [])][:6]
        e["onglets"] = [v.get("tab", {}) for v in (d.get("views") or [])]
        e["faits"] = d.get("facts") or []
        e["nb_indicateurs"] = len(d.get("indicators") or {})
        e["nb_zones"] = len(d.get("areas") or [])
        e["nb_vues"] = len(d.get("views") or [])
        if not e.get("iso"):
            pays = _loc(meta.get("country", ""), "en").lower()
            e["iso"] = next((c for c, (fr, en, _) in PAYS.items() if en.lower() == pays), None)
        return e

    return _relever_html(e)


def _relever_html(e: dict) -> dict:
    """A dashboard read from its page, for the two laboratories that render
    server-side and for any Day 2 dashboard without the data file."""
    doc = _telecharger(e["url"], f"{e['cle']}.html")
    e["vivant"] = doc is not None
    if not doc:
        return e
    t = re.search(r"<title>(.*?)</title>", doc, re.S)
    e["titre"] = _texte(t.group(1)) if t else ""
    e["graphiques"] = doc.count("plotly-graph-div")
    e["cartes"] = "leaflet" in doc or "mapx" in doc
    # The two laboratories carry both languages, but not in the same way, so the
    # page would otherwise print English labels to a French reader.
    if e["famille"] == "j4":
        # Night-time lights: every label holds both, as attributes.
        #   <div class="kpi-label" data-en="Sum of Lights" data-fr="Somme des lumières">
        paires = re.findall(r'class="kpi-label"([^>]*)>(.*?)</', doc, re.S)
        val = [_texte(x) for x in re.findall(r'class="kpi-value"[^>]*>(.*?)</div>', doc, re.S)]
        sub = [_texte(x) for x in re.findall(r'class="kpi-sub"[^>]*>(.*?)</div>', doc, re.S)]
        e["onglets_html"] = [_texte(x) for x in re.findall(r'class="tab"[^>]*>(.*?)</', doc, re.S)]
        labs = [_bilingue(at, tx) for at, tx in paires]
    else:
        # Connectivity: the whole block of indicators appears twice, English
        # first and French second, and the page hides one. Same count, same
        # order, so they pair by position — and a dashboard that shipped only
        # one language still works, it simply reads the same in both.
        bruts = [_texte(x) for x in re.findall(r'class="kpi-l"[^>]*>(.*?)</div>', doc, re.S)]
        # The figure only, never the unit: the unit sits in a nested span, so
        # stopping at the first tag keeps "19.6" rather than "19.6 Mbps", which
        # would otherwise be printed twice.
        val = [_texte(x) for x in re.findall(r'class="kpi-v"[^>]*>([^<]*)', doc)]
        sub = [_texte(x) for x in re.findall(r'class="kpi-u"[^>]*>(.*?)</', doc, re.S)]
        e["sections"] = [_texte(x) for x in re.findall(r"<h2[^>]*>(.*?)</h2>", doc, re.S)]
        moitie = len(bruts) // 2
        if moitie and bruts[:moitie] != bruts[moitie:]:
            labs = [{"en": en, "fr": fr} for en, fr in zip(bruts[:moitie], bruts[moitie:])]
            # Units differ between the blocks — "% of measured" against
            # "% des personnes mesurées" — so they are paired like the labels.
            val = val[:moitie]
            sub = [{"en": a, "fr": b} for a, b in zip(sub[:moitie], sub[moitie:])]                 if len(sub) >= 2 * moitie else sub[:moitie]
        else:
            labs = [{"en": x, "fr": x} for x in bruts]

    vus, kpi = set(), []
    for lab, b, c in zip(labs, val, list(sub) + [""] * 30):
        if not lab.get("en") or not b or lab["en"] in vus:
            continue
        vus.add(lab["en"])
        kpi.append({"label": lab, "valeur": b, "note": c})
    e["kpi"] = kpi[:6]
    return e
