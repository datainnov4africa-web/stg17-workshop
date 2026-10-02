#!/usr/bin/env python3
"""
STG17 · The page that shows what the countries built.

    python tools/build_dashboards.py            render the page
    python tools/build_dashboards.py --captures take the missing screenshots too

Reads `liens.txt`, reads each dashboard, and writes:

    docs/dashboards/index.md     docs/dashboards/index.fr.md
    docs/assets/img/dashboards/  one thumbnail per dashboard

Re-run it whenever a participant adds a line to liens.txt: the page follows.
Writing fourteen country sections by hand would be stale by the next line, and
the descriptions would have to be invented — here every figure on the page was
lifted from the dashboard it describes.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import urllib.error
import urllib.request
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dashboards_data as D  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
PAGES = ROOT / "docs" / "dashboards"
IMG = ROOT / "docs" / "assets" / "img" / "dashboards"
CHROME = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")

T = {
    "titre":      ("Tableaux de bord des pays", "Country dashboards"),
    "eyebrow":    ("BAD · UA STATAFRIC · STG17 · TRAVAUX DES PARTICIPANTS",
                   "AfDB · AU STATAFRIC · STG17 · PARTICIPANTS' WORK"),
    "lede":       ("Ce que les équipes pays ont construit pendant la semaine, publié par elles-mêmes "
                   "et accessible à tous. Chaque tableau de bord est interactif et bilingue.",
                   "What the country teams built during the week, published by themselves and open to "
                   "everyone. Every dashboard is interactive and bilingual."),
    "f_pays":     ("pays", "countries"),
    "f_tb":       ("tableaux de bord", "dashboards"),
    "f_labos":    ("laboratoires", "laboratories"),
    "acces":      ("Accès direct", "Jump to a country"),
    "ouvrir":     ("Ouvrir le tableau de bord", "Open the dashboard"),
    "apercu":     ("Aperçu de", "Preview of"),
    "indisponible": ("Ce tableau de bord n'était pas accessible au moment de la mise à jour de cette page.",
                     "This dashboard could not be reached when this page was last built."),
    "maj":        ("Page construite à partir de liens.txt", "Page built from liens.txt"),
}


FLAGS = ROOT / "docs" / "assets" / "img" / "flags"
TWEMOJI = "https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.1.0/assets/svg/{}.svg"


def drapeau(iso3: str) -> str:
    """
    The flag as a local SVG, fetched once and committed with the site.

    Not the emoji character: a flag emoji is two regional-indicator letters,
    and Windows has no glyph for the pair — it draws the two letters instead,
    so a reader on Windows would see "BW" where the page promises a flag. The
    SVG removes the question. Twemoji, CC-BY 4.0, credited on the page.
    """
    iso2 = D.AFRIQUE[iso3][0]
    cible = FLAGS / f"{iso3}.svg"
    if not cible.exists():
        points = "-".join(f"{0x1F1E6 + ord(c) - ord('A'):x}" for c in iso2)
        try:
            req = urllib.request.Request(TWEMOJI.format(points),
                                         headers={"User-Agent": "stg17-site"})
            with urllib.request.urlopen(req, timeout=30) as rep:
                svg = rep.read()
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError):
            return ""
        cible.parent.mkdir(parents=True, exist_ok=True)
        cible.write_bytes(svg)
    return f"{iso3}.svg"


def _img_drapeau(iso3: str, nom: str, base: str) -> str:
    fichier = drapeau(iso3)
    if not fichier:
        return ""
    return (f'<img class="flag" src="{base}assets/img/flags/{fichier}" alt="" '
            f'width="22" height="22" loading="lazy"> ')


def _sans_accent(s: str) -> str:
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()


def ancre(iso: str) -> str:
    return f"pays-{iso}"


# ---------------------------------------------------------------------------
#  Thumbnails
# ---------------------------------------------------------------------------
def capture(e: dict, brut: Path) -> bool:
    if brut.exists() or not CHROME.exists():
        return brut.exists()
    brut.parent.mkdir(parents=True, exist_ok=True)
    # A connectivity dashboard reaches fourteen megabytes and can take minutes to
    # settle. One that never settles must cost its own thumbnail and nothing
    # else: the page is still worth building for the other thirty-seven.
    try:
        subprocess.run([str(CHROME), "--headless=new", "--disable-gpu", "--no-sandbox",
                        "--hide-scrollbars", "--window-size=1280,860",
                        f"--screenshot={brut}", "--virtual-time-budget=20000", e["url"]],
                       capture_output=True, timeout=240)
    except (subprocess.TimeoutExpired, OSError):
        pass
    return brut.exists()


def vignette(brut: Path, cible: Path, largeur: int = 720) -> bool:
    """A readable thumbnail, small enough that fourteen of them load at once."""
    try:
        from PIL import Image
    except ImportError:
        return False
    if not brut.exists():
        return False
    cible.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(brut) as im:
        im = im.convert("RGB")
        h = round(im.height * largeur / im.width)
        im = im.resize((largeur, h), Image.LANCZOS)
        im = im.crop((0, 0, largeur, min(h, round(largeur * 0.62))))
        im.save(cible, "WEBP", quality=78, method=5)
    return True


# ---------------------------------------------------------------------------
#  What a dashboard says about itself
# ---------------------------------------------------------------------------
def _n(x, lang: str) -> str:
    """A figure as the page should read it: thin space for thousands in French."""
    s = str(x).strip()
    return s.replace(",", " ") if lang == "fr" and re.fullmatch(r"[\d,]+", s) else s


def _pluriel(n, mot_fr: str, mot_en: str, lang: str) -> str:
    """`1 indicateur` and `12 indicateurs`. French and English agree here, but
    only because both make the plural on anything other than one."""
    if not n:
        return ""
    mot = mot_fr if lang == "fr" else mot_en
    return f"{n} {mot}{'s' if n > 1 else ''}"


#: An indicator name copied from a statistical release can run to a full line of
#: its own — "Indice alimentation & boissons non alcoolisées (période 6202)".
#: The card shows the head of it; the dashboard itself shows the rest.
def _court(s: str, limite: int = 46) -> str:
    s = re.sub(r"\s*\((?:p[ée]riode|period)[^)]*\)\s*$", "", s, flags=re.I).strip(" .–—-")
    if len(s) <= limite:
        return s
    coupe = s[:limite].rsplit(" ", 1)[0]
    return (coupe or s[:limite]).rstrip(" ,;:&") + "…"


def indicateurs(e: dict, lang: str) -> list[tuple[str, str, str]]:
    """(label, value, unit) as the dashboard shows them. The unit is kept apart
    from the figure so it can be set smaller, and so that a long unit never
    widens the value column until the label is crushed to one letter a line."""
    out = []
    if e["famille"] == "j2":
        for k in e.get("kpis") or []:
            lab = D._loc(k.get("label"), lang)
            val = D._loc(k.get("valeur"), lang)
            uni = D._loc(k.get("unite"), lang)
            if lab and val:
                out.append((_court(lab), _n(val, lang), uni))
    else:
        for k in e.get("kpi") or []:
            lab = D._loc(k.get("label"), lang)
            if lab and k.get("valeur"):
                note = D._loc(k.get("note"), lang)
                val = _n(k["valeur"], lang)
                # The threshold has to clear the longer language, or the same
                # figure would read "68 % of measured" in English and a bare
                # "68" in French.
                out.append((_court(lab), val, note if note and len(note) <= 30 else ""))
    return out[:4]


def description(e: dict, lang: str) -> str:
    """One sentence, built from the dashboard's own structure. Never invented."""
    fr = lang == "fr"
    if e["famille"] == "j2":
        src = D._loc(e.get("titre_source"), lang)
        ed = D._loc(e.get("editeur"), lang)
        bouts = []
        if src:
            bouts.append(f"À partir de « {src} »" if fr else f"Built from “{src}”")
        if ed:
            bouts.append((f"publié par {ed}" if bouts else f"Publié par {ed}") if fr
                         else (f"published by {ed}" if bouts else f"Published by {ed}"))
        chiffres = [n for n in (
            _pluriel(e.get("nb_indicateurs"), "indicateur", "indicator", lang),
            _pluriel(e.get("nb_vues"), "vue", "view", lang),
            _pluriel(e.get("nb_zones"), "zone", "area", lang)) if n]
        phrase = ", ".join(bouts)
        if chiffres:
            phrase += (". " if phrase else "") + " · ".join(chiffres)
        return phrase or ("Une publication statistique nationale transformée en tableau de bord."
                          if fr else "A national statistical release turned into a dashboard.")
    if e["famille"] == "j3":
        p = ("Données ouvertes Ookla Speedtest rapportées à la population, par unité administrative."
             if fr else
             "Ookla Speedtest open data set against population, by administrative unit.")
        d = []
        if e.get("graphiques"):
            d.append(f"{e['graphiques']} graphiques" if fr else f"{e['graphiques']} charts")
        if e.get("cartes"):
            d.append("cartes interactives" if fr else "interactive maps")
        return p + (" " + " · ".join(d) + "." if d else "")
    p = ("Indicateurs infranationaux dérivés des lumières nocturnes VIIRS."
         if fr else "Subnational indicators derived from VIIRS night-time lights.")
    d = []
    if e.get("graphiques"):
        d.append(f"{e['graphiques']} graphiques" if fr else f"{e['graphiques']} charts")
    if e.get("onglets_html"):
        n = len(e["onglets_html"])
        d.append(f"{n} volets d'analyse" if fr else f"{n} analytical sections")
    return p + (" " + " · ".join(d) + "." if d else "")


# ---------------------------------------------------------------------------
#  The page
# ---------------------------------------------------------------------------
def rendre(releve: list[dict], lang: str) -> str:
    fr = lang == "fr"
    i = 0 if fr else 1
    pays: dict[str, list[dict]] = {}
    for e in releve:
        if e.get("iso"):
            pays.setdefault(e["iso"], []).append(e)
    ordre = sorted(pays, key=lambda c: _sans_accent(D.PAYS[c][i]))
    total = sum(len(v) for v in pays.values())
    # The French build sits one level deeper, at /fr/dashboards/, so the climb
    # back to assets/ is one step longer. build_site.py does the same.
    base = "../../" if fr else "../"

    L: list[str] = []
    L.append(f"# {T['titre'][i]}\n")
    L.append('<div class="stg-hero" markdown>')
    L.append(f'<p class="eyebrow">{T["eyebrow"][i]}</p>')
    L.append(f'<p class="lede">{T["lede"][i]}</p>')
    L.append(f'<p class="facts"><span>{len(ordre)} {T["f_pays"][i]}</span>'
             f'<span>{total} {T["f_tb"][i]}</span>'
             f'<span>3 {T["f_labos"][i]}</span></p>')
    L.append("</div>\n")

    # Quick access: every flag, one click to the country. Before anything else
    # on the page, because fourteen countries is already too many to scroll.
    L.append(f"## {T['acces'][i]} {{: #acces }}\n")
    L.append('<nav class="stg-flags">')
    for c in ordre:
        nom = D.PAYS[c][i]
        L.append(f'<a href="#{ancre(c)}">{_img_drapeau(c, nom, base)}{nom}</a>')
    L.append("</nav>\n")

    for c in ordre:
        nom = D.PAYS[c][i]
        L.append(f"## {_img_drapeau(c, nom, base)}{nom} {{: #{ancre(c)} }}" + chr(10))
        L.append('<div class="stg-dash">')
        for e in sorted(pays[c], key=lambda x: x["famille"]):
            lab = D.FAMILLES[e["famille"]][i]
            a_une_vignette = (IMG / f"{e['cle']}.webp").exists()
            L.append("<article>")
            if a_une_vignette:
                L.append(f'<a class="shot" href="{e["url"]}" target="_blank" rel="noopener">'
                         f'<img src="{base}assets/img/dashboards/{e["cle"]}.webp" '
                         f'alt="{T["apercu"][i]} {nom} — {lab}" loading="lazy" width="720">'
                         f"</a>")
            L.append(f"<h3>{lab}</h3>")
            if not e.get("vivant"):
                L.append(f'<p class="muet">{T["indisponible"][i]}</p>')
            else:
                L.append(f"<p>{description(e, lang)}</p>")
                paires = indicateurs(e, lang)
                if paires:
                    L.append('<dl class="kpis">')
                    for k, v, u in paires:
                        note = f'<span class="u">{u}</span>' if u else ""
                        L.append(f"<dt>{k}</dt><dd>{v}{note}</dd>")
                    L.append("</dl>")
            L.append(f'<p class="go"><a class="md-button" href="{e["url"]}" target="_blank" '
                     f'rel="noopener">{T["ouvrir"][i]}</a></p>')
            L.append("</article>")
        L.append("</div>\n")

    L.append(f'<p class="stg-note">{T["maj"][i]}.</p>')
    return "\n".join(L) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--captures", action="store_true", help="take the missing screenshots")
    args = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    entrees = D.entrees()
    releve, manquantes = [], 0
    for n, e in enumerate(entrees, 1):
        r = D.relever(e)
        brut = D.CACHE / "vignettes" / f"{e['cle']}.png"
        if args.captures and r.get("vivant"):
            capture(r, brut)
        if brut.exists():
            vignette(brut, IMG / f"{e['cle']}.webp")
        elif not (IMG / f"{e['cle']}.webp").exists():
            manquantes += 1
        releve.append(r)
        etat = "ok" if r.get("vivant") else "unreachable"
        marque = "thumb" if (IMG / (e["cle"] + ".webp")).exists() else "  -  "
        print(f"  {n:3}/{len(entrees)}  {etat:11} {marque}  {e['cle']}", flush=True)

    PAGES.mkdir(parents=True, exist_ok=True)
    for lang, nom in (("en", "index.md"), ("fr", "index.fr.md")):
        (PAGES / nom).write_text(rendre(releve, lang), encoding="utf-8")

    vivants = sum(1 for r in releve if r.get("vivant"))
    pays = len({r["iso"] for r in releve if r.get("iso")})
    print(f"{len(releve)} dashboard(s) from {pays} countries · {vivants} reachable "
          f"· {len(releve) - vivants} not · {manquantes} without a thumbnail")
    print(f"Wrote {PAGES / 'index.md'} and {PAGES / 'index.fr.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
