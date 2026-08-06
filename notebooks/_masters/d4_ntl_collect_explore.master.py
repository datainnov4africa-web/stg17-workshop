# %% [meta]
'''
id: d4_ntl_collect_explore
day: 4
title_en: Night-Time Lights - Collect and Explore
title_fr: Lumières nocturnes - Collecter et explorer
outdir: notebooks/day4
stem: D4_NTL_Collect_Explore
country: CIV
tracks: guided, open
'''

# %% [markdown]
'''
<!--EN-->
<div style="background:linear-gradient(135deg,#0B2545 0%,#1B7A43 100%);
 border-radius:18px;padding:32px 38px;font-family:'Segoe UI',system-ui,sans-serif;">
 <div style="color:#F2A900;font-size:12.5px;letter-spacing:3px;font-weight:700;
  text-transform:uppercase;">Day 4 · Laboratory 1 and 2 · 09:30 - 12:30</div>
 <div style="color:#fff;font-size:2em;font-weight:800;margin:10px 0 8px;line-height:1.15;">
  Africa after dark — Collect and Explore</div>
 <div style="color:#dbe7e0;font-size:1.05em;line-height:1.55;max-width:900px;">
  You will acquire NASA Black Marble night-time lights for <b>your own country</b>, clip them
  strictly to the national boundary, and then interrogate the raster <b>before</b> computing
  anything on it — hunting, by name, for the six artefacts that have misled published studies.
 </div>
 <div style="color:#F2A900;font-size:13px;margin-top:14px;font-weight:600;">
  Deliverable: a documented national raster subset, and an inventory of which artefacts
  are present in your country.</div>
</div>
<!--FR-->
<div style="background:linear-gradient(135deg,#0B2545 0%,#1B7A43 100%);
 border-radius:18px;padding:32px 38px;font-family:'Segoe UI',system-ui,sans-serif;">
 <div style="color:#F2A900;font-size:12.5px;letter-spacing:3px;font-weight:700;
  text-transform:uppercase;">Jour 4 · Laboratoires 1 et 2 · 09h30 - 12h30</div>
 <div style="color:#fff;font-size:2em;font-weight:800;margin:10px 0 8px;line-height:1.15;">
  L'Afrique après la nuit tombée — Collecter et explorer</div>
 <div style="color:#dbe7e0;font-size:1.05em;line-height:1.55;max-width:900px;">
  Vous allez acquérir les lumières nocturnes NASA Black Marble pour <b>votre propre pays</b>,
  les découper strictement à la frontière nationale, puis interroger le raster <b>avant</b> de
  calculer quoi que ce soit dessus — en traquant nommément les six artefacts qui ont induit en
  erreur des études publiées.
 </div>
 <div style="color:#F2A900;font-size:13px;margin-top:14px;font-weight:600;">
  Livrable : un sous-ensemble raster national documenté, et un inventaire des artefacts
  présents dans votre pays.</div>
</div>
'''

# %% [markdown]
'''
<!--EN-->
### Why we explore before we compute

It is tempting to jump to zonal statistics: load the raster, sum by district,
publish a table. The table will look plausible. It may also be wrong in ways
nobody can see from the table itself — because a gas flare in one district
contributes more radiance than a city of 200 000 people, because the brightest
pixels of your capital saturated years ago and stopped growing, or because one
year of your series is missing a tile and quietly covers two thirds of the
territory.

None of that is visible downstream. All of it is visible in the raster, in the
first twenty minutes, if you look. That is what this laboratory is for.

> **This notebook comes in two tracks.** The *guided* track has the analytical
> steps written and asks you to fill the gaps. The *open* track gives you the
> objective and the data. Both produce the same deliverable, so the Friday
> presentations stay comparable. Switch at any time using the link at the top.
<!--FR-->
### Pourquoi explorer avant de calculer

Il est tentant de sauter directement aux statistiques zonales : charger le
raster, sommer par district, publier un tableau. Le tableau paraîtra plausible.
Il pourra aussi être faux d'une manière que personne ne peut voir depuis le
tableau lui-même — parce qu'une torchère de gaz dans un district apporte plus de
radiance qu'une ville de 200 000 habitants, parce que les pixels les plus
lumineux de votre capitale ont saturé il y a des années et ont cessé de croître,
ou parce qu'une année de votre série a perdu une tuile et ne couvre discrètement
que deux tiers du territoire.

Rien de tout cela n'est visible en aval. Tout est visible dans le raster, dans
les vingt premières minutes, si l'on regarde. C'est l'objet de ce laboratoire.

> **Ce carnet existe en deux pistes.** La piste *guidée* comporte les étapes
> analytiques écrites et vous demande de combler les trous. La piste *ouverte*
> vous donne l'objectif et les données. Les deux produisent le même livrable,
> afin que les présentations du vendredi restent comparables. Basculez à tout
> moment via le lien en haut de page.
'''

# %% [markdown]
'''
<!--EN-->
---
## Requirements

Everything this notebook needs, in one cell. On Colab it takes about 90 seconds;
locally it installs only what is missing. Re-running is safe.
<!--FR-->
---
## Prérequis

Tout ce dont ce carnet a besoin, en une cellule. Sur Colab cela prend environ
90 secondes ; en local, seul ce qui manque est installé. La ré-exécution est sûre.
'''

# %%
# EN: --- Requirements for this laboratory --------------------------------- | FR: --- Prérequis de ce laboratoire ---------------------------------------
REQUIREMENTS = {
    "numpy":      "numpy>=1.24",
    "pandas":     "pandas>=2.0",
    "matplotlib": "matplotlib>=3.7",
    "geopandas":  "geopandas>=0.14",
    "shapely":    "shapely>=2.0",
    "rasterio":   "rasterio>=1.3",
    "h5py":       "h5py>=3.9",
    "requests":   "requests>=2.31",
}

import subprocess
import sys

try:
    import stg17
except ImportError:
    subprocess.run([sys.executable, "-m", "pip", "install", "-q",
                    "stg17 @ git+https://github.com/{{ORG}}/{{REPO}}"], check=False)
    import stg17

from stg17 import setup, countries, boundaries, ntl, theme, ui
from stg17.i18n import T

S = setup(REQUIREMENTS, lang="{{LANG_UPPER}}")

# %% [markdown]
'''
<!--EN-->
---
<div style="border-left:5px solid #1B7A43;background:#F4F8F5;border-radius:0 12px 12px 0;
 padding:13px 18px;margin:18px 0 8px;font-family:'Segoe UI',system-ui,sans-serif;">
 <span style="background:#1B7A43;color:#fff;border-radius:20px;padding:3px 13px;
  font-weight:700;font-size:11.5px;">STEP 1/8</span>
 <span style="color:#0B2545;font-weight:800;font-size:1.14em;margin-left:11px;">
  Choose your country</span>
 <div style="color:#3a4a42;margin-top:5px;font-size:.96em;">
  One variable. Everything else in this notebook follows from it.</div>
</div>

This is the mechanism that makes the laboratory portable across the continent.
Change `COUNTRY_ISO3` to your own code and re-run the notebook from the top: the
tiles to download, the boundary file to fetch, the map extent, the projection
used for areas, and every figure title all follow automatically.

If you do not know your ISO3 code, run `countries.table()` in a new cell — it
lists all 55 African Union member states.
<!--FR-->
---
<div style="border-left:5px solid #1B7A43;background:#F4F8F5;border-radius:0 12px 12px 0;
 padding:13px 18px;margin:18px 0 8px;font-family:'Segoe UI',system-ui,sans-serif;">
 <span style="background:#1B7A43;color:#fff;border-radius:20px;padding:3px 13px;
  font-weight:700;font-size:11.5px;">ÉTAPE 1/8</span>
 <span style="color:#0B2545;font-weight:800;font-size:1.14em;margin-left:11px;">
  Choisissez votre pays</span>
 <div style="color:#3a4a42;margin-top:5px;font-size:.96em;">
  Une seule variable. Tout le reste du carnet en découle.</div>
</div>

C'est le mécanisme qui rend le laboratoire transposable à tout le continent.
Remplacez `COUNTRY_ISO3` par votre propre code et ré-exécutez le carnet depuis le
début : les tuiles à télécharger, le fichier de frontières à récupérer, l'emprise
cartographique, la projection utilisée pour les aires et tous les titres de
figures suivent automatiquement.

Si vous ne connaissez pas votre code ISO3, exécutez `countries.table()` dans une
nouvelle cellule — elle liste les 55 États membres de l'Union africaine.
'''

# %%
# ===========================================================================
# EN: THE ONLY LINE YOU NEED TO CHANGE | FR: LA SEULE LIGNE À MODIFIER
# ===========================================================================
COUNTRY_ISO3 = "{{ISO3}}"

# EN: Analysis parameters - defensible defaults, documented below. | FR: Paramètres d'analyse - valeurs par défaut défendables, documentées ci-dessous.
PRODUCT       = "VNP46A4"   # EN: annual composite | FR: composite annuel
YEARS         = [2016, 2020, 2024]   # EN: start small; extend once it works | FR: commencez petit ; étendez une fois que cela marche
LIT_THRESHOLD = 0.5         # EN: nW/cm2/sr above which a pixel counts as "lit" | FR: nW/cm2/sr au-delà duquel un pixel est compté comme "éclairé"
ADM_LEVEL     = 1           # EN: administrative level for the first look | FR: niveau administratif pour le premier regard

C = countries.get(COUNTRY_ISO3)
OUT = S.outputs(C.iso3, "d4_ntl")

print(f"{C.name('{{LANG}}')} ({C.iso3}) — {C.region_name('{{LANG}}')}")
print(T(f"  Tiles needed  : {' '.join(C.viirs_tiles)}",
        f"  Tuiles requises : {' '.join(C.viirs_tiles)}"))
print(T(f"  Years          : {YEARS}", f"  Années          : {YEARS}"))
print(T(f"  Outputs go to  : {OUT}", f"  Sorties dans    : {OUT}"))
print(T(f"  Estimated download: {countries.estimate_download_mb(C, len(YEARS), PRODUCT):.0f} MB",
        f"  Téléchargement estimé : {countries.estimate_download_mb(C, len(YEARS), PRODUCT):.0f} Mo"))

# %% [markdown]
'''
<!--EN-->
<div style="border:1px solid #1B7A43;border-left:6px solid #1B7A43;background:#F4F8F5;
 padding:13px 17px;border-radius:0 9px 9px 0;margin:14px 0;font-family:'Segoe UI',system-ui,sans-serif;">
<b style="color:#1B7A43;font-size:11.5px;letter-spacing:1.6px;">◆ KEY CONCEPT — WHICH PRODUCT, AND WHY</b><br>
<span style="color:#33403A;font-size:14.3px;line-height:1.58;">
NASA publishes Black Marble at three cadences. <b>VNP46A2</b> is daily and lets you see a
single night — useful for crisis monitoring, noisy for anything else. <b>VNP46A3</b> is monthly
and is where seasonality lives. <b>VNP46A4</b> is annual, already composited over cloud-free
nights, and is the right default for a statistical time series: it removes most of the
meteorological noise that would otherwise dominate a year-on-year comparison.<br><br>
Separately, the <b>EOG annual VNL</b> series (available through Earth Engine) covers the same
years with a different processing chain. It is equally defensible and gives slightly different
numbers. That is not a problem — it is a fact to state in your metadata. Two honest pipelines
disagreeing by a few percent is normal; a pipeline that does not say which one it used is not.
</span></div>
<!--FR-->
<div style="border:1px solid #1B7A43;border-left:6px solid #1B7A43;background:#F4F8F5;
 padding:13px 17px;border-radius:0 9px 9px 0;margin:14px 0;font-family:'Segoe UI',system-ui,sans-serif;">
<b style="color:#1B7A43;font-size:11.5px;letter-spacing:1.6px;">◆ CONCEPT CLÉ — QUEL PRODUIT, ET POURQUOI</b><br>
<span style="color:#33403A;font-size:14.3px;line-height:1.58;">
La NASA publie Black Marble à trois cadences. <b>VNP46A2</b> est journalier et permet de voir
une nuit précise — utile pour le suivi de crise, bruité pour le reste. <b>VNP46A3</b> est
mensuel : c'est là que vit la saisonnalité. <b>VNP46A4</b> est annuel, déjà composité sur les
nuits sans nuages, et constitue la valeur par défaut pertinente pour une série statistique :
il élimine l'essentiel du bruit météorologique qui dominerait sinon une comparaison
interannuelle.<br><br>
Par ailleurs, la série <b>VNL annuelle de l'EOG</b> (accessible via Earth Engine) couvre les
mêmes années avec une chaîne de traitement différente. Elle est tout aussi défendable et donne
des chiffres légèrement différents. Ce n'est pas un problème — c'est un fait à déclarer dans vos
métadonnées. Que deux pipelines honnêtes divergent de quelques pour cent est normal ; qu'un
pipeline ne dise pas lequel il a utilisé ne l'est pas.
</span></div>
'''

# %% [markdown]
'''
<!--EN-->
---
<div style="border-left:5px solid #1B7A43;background:#F4F8F5;border-radius:0 12px 12px 0;
 padding:13px 18px;margin:18px 0 8px;font-family:'Segoe UI',system-ui,sans-serif;">
 <span style="background:#1B7A43;color:#fff;border-radius:20px;padding:3px 13px;
  font-weight:700;font-size:11.5px;">STEP 2/8</span>
 <span style="color:#0B2545;font-weight:800;font-size:1.14em;margin-left:11px;">
  Collect — find the data before downloading it</span>
 <div style="color:#3a4a42;margin-top:5px;font-size:.96em;">
  Local mirror first, NASA second, Earth Engine third. In that order, always.</div>
</div>

Three sources, tried in order, and the order matters:

1. **The local mirror** — what the technical assistants pre-clipped onto the USB
   key. Works with no network at all. Always tried first.
2. **NASA Earthdata** — the authoritative source. Searching is public and needs
   no account; *downloading* needs a free token.
3. **Google Earth Engine** — nothing is downloaded at all; see the companion
   notebook `D4_NTL_GEE_{{LANG_UPPER}}`.

We search CMR first regardless, because knowing what exists is free and takes
two seconds, and because a year that CMR does not list is a year you will spend
twenty minutes hunting for otherwise.
<!--FR-->
---
<div style="border-left:5px solid #1B7A43;background:#F4F8F5;border-radius:0 12px 12px 0;
 padding:13px 18px;margin:18px 0 8px;font-family:'Segoe UI',system-ui,sans-serif;">
 <span style="background:#1B7A43;color:#fff;border-radius:20px;padding:3px 13px;
  font-weight:700;font-size:11.5px;">ÉTAPE 2/8</span>
 <span style="color:#0B2545;font-weight:800;font-size:1.14em;margin-left:11px;">
  Collecter — trouver la donnée avant de la télécharger</span>
 <div style="color:#3a4a42;margin-top:5px;font-size:.96em;">
  Miroir local d'abord, NASA ensuite, Earth Engine en troisième. Dans cet ordre, toujours.</div>
</div>

Trois sources, essayées dans cet ordre, et l'ordre importe :

1. **Le miroir local** — ce que les assistants techniques ont pré-découpé sur la
   clé USB. Fonctionne sans aucun réseau. Toujours essayé en premier.
2. **NASA Earthdata** — la source faisant autorité. La recherche est publique et
   ne demande aucun compte ; le *téléchargement* exige un jeton gratuit.
3. **Google Earth Engine** — rien n'est téléchargé ; voir le carnet compagnon
   `D4_NTL_GEE_{{LANG_UPPER}}`.

Nous interrogeons systématiquement le CMR en premier, parce que savoir ce qui
existe est gratuit et prend deux secondes, et parce qu'une année que le CMR ne
liste pas est une année que vous passeriez sinon vingt minutes à chercher.
'''

# %%
# EN: 1) The local mirror - the only source that works with no network at all. | FR: 1) Le miroir local - la seule source qui fonctionne sans aucun réseau.
from pathlib import Path

LOCAL_DIR = S.path("h5_cache", C.iso3)
files = ntl.discover(LOCAL_DIR, years=tuple(YEARS))

print(T(f"Local mirror: {LOCAL_DIR}", f"Miroir local : {LOCAL_DIR}"))
if files:
    for year in sorted(files):
        print(T(f"  {year}: {len(files[year])} granule(s) — {[g.tile for g in files[year]]}",
                f"  {year} : {len(files[year])} granule(s) — {[g.tile for g in files[year]]}"))
else:
    print(T("  empty — we will look at NASA next.",
            "  vide — nous interrogeons la NASA ensuite."))

# %%
# EN: 2) Ask NASA what exists. Public endpoint: no account needed for this step. | FR: 2) Demander à la NASA ce qui existe. Point public : aucun compte requis pour cette étape.
available = ntl.search_cmr(PRODUCT, C.viirs_tiles, YEARS)
print(T(f"\nCMR lists {len(available)} granule(s) for {C.name('en')}.",
        f"\nLe CMR liste {len(available)} granule(s) pour {C.name('fr')}."))

expected = len(C.viirs_tiles) * len(YEARS)
if len(available) < expected:
    print(T(f"Expected {expected} ({len(C.viirs_tiles)} tiles x {len(YEARS)} years). "
            f"Note which are missing — an incomplete year must not be compared with a complete one.",
            f"Attendu : {expected} ({len(C.viirs_tiles)} tuiles x {len(YEARS)} années). "
            f"Notez lesquels manquent — une année incomplète ne doit pas être comparée à une année complète."))

# %%
# EN: 3) Download only what the mirror does not already have. | FR: 3) Ne télécharger que ce que le miroir n'a pas déjà.
from stg17 import env

TOKEN = env.get_secret("EARTHDATA_TOKEN")

have = {g.path.name for granules in files.values() for g in granules}
todo = [g for g in available if g["title"] not in have]

print(T(f"{len(todo)} granule(s) to download.", f"{len(todo)} granule(s) à télécharger."))
if todo and TOKEN:
    ntl.download_granules(todo, LOCAL_DIR, token=TOKEN)
    files = ntl.discover(LOCAL_DIR, years=tuple(YEARS))
elif todo:
    print(T("No EARTHDATA_TOKEN — skipping the download. See the fallback below.",
            "Pas de EARTHDATA_TOKEN — téléchargement ignoré. Voir le repli ci-dessous."))

# %% [markdown]
'''
<!--EN-->
<div style="border:1px solid #1D5FA8;border-left:6px solid #1D5FA8;background:#EEF4FB;
 padding:13px 17px;border-radius:0 9px 9px 0;margin:14px 0;font-family:'Segoe UI',system-ui,sans-serif;">
<b style="color:#1D5FA8;font-size:11.5px;letter-spacing:1.6px;">⟲ IF THIS FAILS — FALLBACK PATH</b><br>
<span style="color:#33403A;font-size:14.3px;line-height:1.58;">
<b>No token, no network, or a download that will not finish?</b> Do not lose the morning on it.
Take one of these, in order of preference:<br>
<b>(a)</b> The USB key carries pre-clipped subsets for every participating country — point
<code>STG17_ROOT</code> at it and re-run from Step 2.<br>
<b>(b)</b> Run the companion notebook <code>D4_NTL_GEE_{{LANG_UPPER}}</code>, which downloads nothing.<br>
<b>(c)</b> Set <code>COUNTRY_ISO3 = "CIV"</code>. Côte d'Ivoire is the reference country, prepared
end to end, so no team loses a day to a missing file. Say so in your limitations statement and
carry on — the method is what you are learning, and it transfers unchanged.
</span></div>
<!--FR-->
<div style="border:1px solid #1D5FA8;border-left:6px solid #1D5FA8;background:#EEF4FB;
 padding:13px 17px;border-radius:0 9px 9px 0;margin:14px 0;font-family:'Segoe UI',system-ui,sans-serif;">
<b style="color:#1D5FA8;font-size:11.5px;letter-spacing:1.6px;">⟲ EN CAS D'ÉCHEC — CHEMIN DE REPLI</b><br>
<span style="color:#33403A;font-size:14.3px;line-height:1.58;">
<b>Pas de jeton, pas de réseau, ou un téléchargement qui n'aboutit pas ?</b> N'y perdez pas la
matinée. Prenez l'une de ces options, par ordre de préférence :<br>
<b>(a)</b> La clé USB contient des extraits pré-découpés pour chaque pays participant — pointez
<code>STG17_ROOT</code> dessus et reprenez à l'Étape 2.<br>
<b>(b)</b> Exécutez le carnet compagnon <code>D4_NTL_GEE_{{LANG_UPPER}}</code>, qui ne télécharge rien.<br>
<b>(c)</b> Mettez <code>COUNTRY_ISO3 = "CIV"</code>. La Côte d'Ivoire est le pays de référence,
préparé de bout en bout, pour qu'aucune équipe ne perde une journée sur un fichier manquant.
Mentionnez-le dans votre déclaration de limites et poursuivez — c'est la méthode que vous
apprenez, et elle se transpose sans changement.
</span></div>
'''

# %% [markdown]
'''
<!--EN-->
---
<div style="border-left:5px solid #1B7A43;background:#F4F8F5;border-radius:0 12px 12px 0;
 padding:13px 18px;margin:18px 0 8px;font-family:'Segoe UI',system-ui,sans-serif;">
 <span style="background:#1B7A43;color:#fff;border-radius:20px;padding:3px 13px;
  font-weight:700;font-size:11.5px;">STEP 3/8</span>
 <span style="color:#0B2545;font-weight:800;font-size:1.14em;margin-left:11px;">
  Inventory — audit completeness before trusting anything</span>
 <div style="color:#3a4a42;margin-top:5px;font-size:.96em;">
  A missing tile does not raise an error. It quietly deletes part of your country.</div>
</div>

This is the quality-control step that most published work skips, and it is the
cheapest insurance in the whole pipeline. A year holding one tile instead of two
will produce a perfectly formatted national total covering half the territory.
Nothing downstream complains. The series just has a dip that someone will later
interpret as an economic event.
<!--FR-->
---
<div style="border-left:5px solid #1B7A43;background:#F4F8F5;border-radius:0 12px 12px 0;
 padding:13px 18px;margin:18px 0 8px;font-family:'Segoe UI',system-ui,sans-serif;">
 <span style="background:#1B7A43;color:#fff;border-radius:20px;padding:3px 13px;
  font-weight:700;font-size:11.5px;">ÉTAPE 3/8</span>
 <span style="color:#0B2545;font-weight:800;font-size:1.14em;margin-left:11px;">
  Inventaire — auditer la complétude avant de faire confiance</span>
 <div style="color:#3a4a42;margin-top:5px;font-size:.96em;">
  Une tuile manquante ne déclenche aucune erreur. Elle supprime silencieusement une partie de votre pays.</div>
</div>

C'est l'étape de contrôle qualité que la plupart des travaux publiés sautent, et
c'est l'assurance la moins chère de toute la chaîne. Une année contenant une
tuile au lieu de deux produira un total national parfaitement formaté couvrant la
moitié du territoire. Rien en aval ne proteste. La série présente simplement un
creux que quelqu'un interprétera plus tard comme un événement économique.
'''

# %%
# <solution hint="Build the completeness table with ntl.inventory(files, C) and display it with ui.result_table" hint_fr="Construisez le tableau de complétude avec ntl.inventory(files, C) et affichez-le avec ui.result_table">
inv = ntl.inventory(files, C)
ui.result_table(
    inv,
    caption=T("Completeness audit. Any year marked False must be excluded from "
              "inter-annual comparison, or completed before use.",
              "Audit de complétude. Toute année marquée False doit être exclue de la "
              "comparaison interannuelle, ou complétée avant usage."),
)
# </solution>

incomplete = inv.loc[~inv["complete"], "year"].tolist() if len(inv) else []
if incomplete:
    print(T(f"WARNING — incomplete years: {incomplete}. Excluded from comparisons below.",
            f"ATTENTION — années incomplètes : {incomplete}. Exclues des comparaisons ci-dessous."))
    YEARS = [y for y in YEARS if y not in incomplete]

# %% [markdown]
'''
<!--EN-->
---
<div style="border-left:5px solid #1B7A43;background:#F4F8F5;border-radius:0 12px 12px 0;
 padding:13px 18px;margin:18px 0 8px;font-family:'Segoe UI',system-ui,sans-serif;">
 <span style="background:#1B7A43;color:#fff;border-radius:20px;padding:3px 13px;
  font-weight:700;font-size:11.5px;">STEP 4/8</span>
 <span style="color:#0B2545;font-weight:800;font-size:1.14em;margin-left:11px;">
  Administrative boundaries — what makes it <i>your</i> country</span>
 <div style="color:#3a4a42;margin-top:5px;font-size:.96em;">
  This clipping is the difference between "light near you" and "light in your country".</div>
</div>

A Black Marble tile is 10° × 10° — roughly 1 100 km on a side. It contains your
country and several of your neighbours. Everything that follows depends on
restricting the computation to pixels **inside your national polygons**.

The loader below normalises whatever it finds — geoBoundaries, GADM or a national
shapefile — into the same column names, repairs invalid geometries, and
reprojects to EPSG:4326. That is why the analysis code below contains no
conditionals about the source.
<!--FR-->
---
<div style="border-left:5px solid #1B7A43;background:#F4F8F5;border-radius:0 12px 12px 0;
 padding:13px 18px;margin:18px 0 8px;font-family:'Segoe UI',system-ui,sans-serif;">
 <span style="background:#1B7A43;color:#fff;border-radius:20px;padding:3px 13px;
  font-weight:700;font-size:11.5px;">ÉTAPE 4/8</span>
 <span style="color:#0B2545;font-weight:800;font-size:1.14em;margin-left:11px;">
  Frontières administratives — ce qui fait que c'est <i>votre</i> pays</span>
 <div style="color:#3a4a42;margin-top:5px;font-size:.96em;">
  Ce découpage fait la différence entre « la lumière près de chez vous » et « la lumière dans votre pays ».</div>
</div>

Une tuile Black Marble fait 10° × 10° — environ 1 100 km de côté. Elle contient
votre pays et plusieurs de vos voisins. Tout ce qui suit dépend de la restriction
du calcul aux pixels **situés à l'intérieur de vos polygones nationaux**.

Le chargeur ci-dessous normalise ce qu'il trouve — geoBoundaries, GADM ou un
shapefile national — vers les mêmes noms de colonnes, répare les géométries
invalides et reprojette en EPSG:4326. C'est pourquoi le code d'analyse plus bas
ne contient aucune condition sur la source.
'''

# %%
# <solution hint="Load ADM0 and ADM1 with boundaries.load_levels(), then plot both" hint_fr="Chargez ADM0 et ADM1 avec boundaries.load_levels(), puis tracez les deux">
import matplotlib.pyplot as plt

adm = boundaries.load_levels(C, levels=(0, ADM_LEVEL), root=S.root)
adm0, admN = adm[0], adm[ADM_LEVEL]

print(T(f"Source: {admN.attrs['source_name']}", f"Source : {admN.attrs['source_name']}"))
print(T(f"Levels loaded: {boundaries.summary(adm)}",
        f"Niveaux chargés : {boundaries.summary(adm)}"))

fig, ax = plt.subplots(1, 2, figsize=(11, 4.4))
adm0.plot(ax=ax[0], facecolor=theme.WASH, edgecolor=theme.NAVY, linewidth=1.2)
ax[0].set_title(T(f"{C.name('en')} — national outline", f"{C.name('fr')} — contour national"))
admN.plot(ax=ax[1], facecolor="none", edgecolor=theme.GREEN, linewidth=0.7)
ax[1].set_title(T(f"ADM{ADM_LEVEL} — {len(admN)} units", f"ADM{ADM_LEVEL} — {len(admN)} unités"))
for a in ax:
    a.set_axis_off()
plt.show()
# </solution>

# %% [markdown]
'''
<!--EN-->
<div style="border:1px solid #F2A900;border-left:6px solid #F2A900;background:#FEF9EC;
 padding:13px 17px;border-radius:0 9px 9px 0;margin:14px 0;font-family:'Segoe UI',system-ui,sans-serif;">
<b style="color:#F2A900;font-size:11.5px;letter-spacing:1.6px;">▲ WATCH OUT — WHICH BOUNDARIES YOU PUBLISH WITH</b><br>
<span style="color:#33403A;font-size:14.3px;line-height:1.58;">
geoBoundaries is the right choice for a workshop: open, uniform across the continent, citable,
and downloadable without an account. It is usually the <b>wrong</b> choice for a national
publication, where your office's own official boundaries carry the legal weight and are the ones
your users will reconcile against. Boundary depiction is also politically sensitive in several
member states. Replace this source with your national file before publishing, and record which
one you used in your metadata — Day 5 covers exactly how.
</span></div>
<!--FR-->
<div style="border:1px solid #F2A900;border-left:6px solid #F2A900;background:#FEF9EC;
 padding:13px 17px;border-radius:0 9px 9px 0;margin:14px 0;font-family:'Segoe UI',system-ui,sans-serif;">
<b style="color:#F2A900;font-size:11.5px;letter-spacing:1.6px;">▲ ATTENTION — AVEC QUELLES FRONTIÈRES PUBLIER</b><br>
<span style="color:#33403A;font-size:14.3px;line-height:1.58;">
geoBoundaries est le bon choix pour un atelier : ouvert, uniforme sur tout le continent, citable
et téléchargeable sans compte. C'est en général le <b>mauvais</b> choix pour une publication
nationale, où les frontières officielles de votre office portent la valeur juridique et sont
celles auxquelles vos utilisateurs se référeront. La représentation des frontières est en outre
politiquement sensible dans plusieurs États membres. Remplacez cette source par votre fichier
national avant publication, et consignez celle que vous avez utilisée dans vos métadonnées — le
Jour 5 explique précisément comment.
</span></div>
'''

# %% [markdown]
'''
<!--EN-->
---
<div style="border-left:5px solid #1B7A43;background:#F4F8F5;border-radius:0 12px 12px 0;
 padding:13px 18px;margin:18px 0 8px;font-family:'Segoe UI',system-ui,sans-serif;">
 <span style="background:#1B7A43;color:#fff;border-radius:20px;padding:3px 13px;
  font-weight:700;font-size:11.5px;">STEP 5/8</span>
 <span style="color:#0B2545;font-weight:800;font-size:1.14em;margin-left:11px;">
  Open a real granule — read the metadata from the file</span>
 <div style="color:#3a4a42;margin-top:5px;font-size:.96em;">
  Never hard-code a scale factor. NASA changes them between collection versions.</div>
</div>

A Black Marble granule is an HDF5 file. The radiance layer is stored as integers,
and the file itself carries the `scale_factor` and the `_FillValue` needed to turn
those integers into physical units.

Reading those attributes from the file rather than pasting a constant is a
two-line difference that decides whether your pipeline still produces correct
numbers after NASA publishes collection 003.
<!--FR-->
---
<div style="border-left:5px solid #1B7A43;background:#F4F8F5;border-radius:0 12px 12px 0;
 padding:13px 18px;margin:18px 0 8px;font-family:'Segoe UI',system-ui,sans-serif;">
 <span style="background:#1B7A43;color:#fff;border-radius:20px;padding:3px 13px;
  font-weight:700;font-size:11.5px;">ÉTAPE 5/8</span>
 <span style="color:#0B2545;font-weight:800;font-size:1.14em;margin-left:11px;">
  Ouvrir un granule réel — lire les métadonnées dans le fichier</span>
 <div style="color:#3a4a42;margin-top:5px;font-size:.96em;">
  Ne codez jamais un facteur d'échelle en dur. La NASA les modifie entre versions de collection.</div>
</div>

Un granule Black Marble est un fichier HDF5. La couche de radiance y est stockée
en entiers, et le fichier lui-même porte le `scale_factor` et le `_FillValue`
nécessaires pour convertir ces entiers en unités physiques.

Lire ces attributs dans le fichier plutôt que de coller une constante est une
différence de deux lignes qui décide si votre chaîne produira encore des nombres
corrects après la publication par la NASA de la collection 003.
'''

# %%
# <solution hint="Read one granule with ntl.read_layer() and print everything the file told you" hint_fr="Lisez un granule avec ntl.read_layer() et affichez tout ce que le fichier vous a appris">
import numpy as np

assert files, T("No granule available — take one of the fallback paths above.",
                "Aucun granule disponible — prenez l'un des chemins de repli ci-dessus.")

demo_year = max(files)
demo = files[demo_year][0]
radiance, meta = ntl.read_layer(demo.path)

print(T(f"File          : {meta['file']}", f"Fichier         : {meta['file']}"))
print(T(f"HDF5 group    : {meta['group']}", f"Groupe HDF5     : {meta['group']}"))
print(T(f"Layer chosen  : {meta['layer']}", f"Couche retenue  : {meta['layer']}"))
print(T(f"scale_factor  : {meta['scale']}  (read from the file, not assumed)",
        f"scale_factor    : {meta['scale']}  (lu dans le fichier, non supposé)"))
print(T(f"_FillValue    : {meta['fill']}", f"_FillValue      : {meta['fill']}"))
print(T(f"Array shape   : {meta['shape']}  -> {radiance.size/1e6:.1f} million pixels",
        f"Forme du tableau : {meta['shape']}  -> {radiance.size/1e6:.1f} millions de pixels"))
print(T(f"Valid pixels  : {100*np.isfinite(radiance).mean():.1f} %",
        f"Pixels valides  : {100*np.isfinite(radiance).mean():.1f} %"))
print(T(f"Radiance      : min {np.nanmin(radiance):.2f}   median {np.nanmedian(radiance):.2f}   "
        f"max {np.nanmax(radiance):.0f}  nW/cm2/sr",
        f"Radiance        : min {np.nanmin(radiance):.2f}   médiane {np.nanmedian(radiance):.2f}   "
        f"max {np.nanmax(radiance):.0f}  nW/cm2/sr"))
# </solution>

# %% [markdown]
'''
<!--EN-->
---
<div style="border-left:5px solid #1B7A43;background:#F4F8F5;border-radius:0 12px 12px 0;
 padding:13px 18px;margin:18px 0 8px;font-family:'Segoe UI',system-ui,sans-serif;">
 <span style="background:#1B7A43;color:#fff;border-radius:20px;padding:3px 13px;
  font-weight:700;font-size:11.5px;">STEP 6/8</span>
 <span style="color:#0B2545;font-weight:800;font-size:1.14em;margin-left:11px;">
  Clip to the nation and look at it</span>
 <div style="color:#3a4a42;margin-top:5px;font-size:.96em;">
  Georeference from the tile name, burn the polygons, mask everything outside.</div>
</div>

Black Marble tiles sit on a regular 10° × 10° grid, so the affine transform
follows exactly from the tile index and the array shape — no georeferencing
metadata required, and no dependence on how a particular collection names its
attributes.

We then burn the national polygon into a mask and set everything outside it to
`NaN`. **This is the clipping.** From here on, every number describes your
country and only your country.
<!--FR-->
---
<div style="border-left:5px solid #1B7A43;background:#F4F8F5;border-radius:0 12px 12px 0;
 padding:13px 18px;margin:18px 0 8px;font-family:'Segoe UI',system-ui,sans-serif;">
 <span style="background:#1B7A43;color:#fff;border-radius:20px;padding:3px 13px;
  font-weight:700;font-size:11.5px;">ÉTAPE 6/8</span>
 <span style="color:#0B2545;font-weight:800;font-size:1.14em;margin-left:11px;">
  Découper au territoire national et regarder</span>
 <div style="color:#3a4a42;margin-top:5px;font-size:.96em;">
  Géoréférencer depuis le nom de tuile, brûler les polygones, masquer l'extérieur.</div>
</div>

Les tuiles Black Marble reposent sur une grille régulière de 10° × 10° : la
transformation affine découle donc exactement de l'indice de tuile et de la forme
du tableau — aucune métadonnée de géoréférencement n'est nécessaire, et aucune
dépendance à la façon dont une collection nomme ses attributs.

Nous brûlons ensuite le polygone national dans un masque et mettons tout
l'extérieur à `NaN`. **C'est le découpage.** À partir d'ici, chaque nombre décrit
votre pays et rien que votre pays.
'''

# %%
# <solution hint="Build the transform with ntl.tile_transform(), rasterize adm0, mask outside, then plot log1p radiance" hint_fr="Construisez la transformation avec ntl.tile_transform(), rasterisez adm0, masquez l'extérieur, puis tracez log1p de la radiance">
transform = ntl.tile_transform(demo.tile, radiance.shape)
zones = ntl.rasterize_zones(adm0.assign(__zid__=1), transform, radiance.shape)

inside = radiance.copy()
inside[zones == 0] = np.nan
coverage = 100 * np.isfinite(inside).sum() / max((zones > 0).sum(), 1)

west, south, east, north = ntl.tile_bounds_from(transform, radiance.shape)

fig, ax = plt.subplots(1, 2, figsize=(13, 5.4))
for axis, array, title in [
    (ax[0], radiance, T(f"Whole tile {demo.tile} — neighbours included",
                        f"Tuile entière {demo.tile} — voisins compris")),
    (ax[1], inside, T(f"Clipped to {C.name('en')}", f"Découpé sur {C.name('fr')}")),
]:
    im = axis.imshow(np.log1p(np.nan_to_num(array)), cmap="stg17_night",
                     extent=[west, east, south, north], origin="upper")
    adm0.boundary.plot(ax=axis, edgecolor="white", linewidth=0.8)
    axis.set_title(title)
    axis.set_xlim(C.bbox[0] - 0.5, C.bbox[2] + 0.5)
    axis.set_ylim(C.bbox[1] - 0.5, C.bbox[3] + 0.5)
fig.colorbar(im, ax=ax, shrink=0.75, label=T("log(1 + radiance)", "log(1 + radiance)"))
fig.suptitle(T(f"{C.name('en')} · {PRODUCT} · {demo_year}",
               f"{C.name('fr')} · {PRODUCT} · {demo_year}"),
             fontweight="bold", color=theme.NAVY)
plt.show()

print(T(f"Pixels inside the national boundary: {(zones > 0).sum():,}  "
        f"({coverage:.1f} % of them carry a valid value)",
        f"Pixels à l'intérieur de la frontière : {(zones > 0).sum():,}  "
        f"({coverage:.1f} % portent une valeur valide)"))
# </solution>

# %% [markdown]
'''
<!--EN-->
---
<div style="border-left:5px solid #1B7A43;background:#F4F8F5;border-radius:0 12px 12px 0;
 padding:13px 18px;margin:18px 0 8px;font-family:'Segoe UI',system-ui,sans-serif;">
 <span style="background:#1B7A43;color:#fff;border-radius:20px;padding:3px 13px;
  font-weight:700;font-size:11.5px;">STEP 7/8</span>
 <span style="color:#0B2545;font-weight:800;font-size:1.14em;margin-left:11px;">
  Explore — the distribution, and why the threshold matters</span>
 <div style="color:#3a4a42;margin-top:5px;font-size:.96em;">
  Night-time radiance is extraordinarily skewed. Choosing a "lit" threshold is a judgement call, so make it visible.</div>
</div>

Plot the distribution of radiance across your country and you will see the single
most important property of this data: it is dominated by near-zero values, with a
very long tail. Most of your territory is dark. A handful of pixels are hundreds
of times brighter than the median.

That shape has two consequences a statistician should care about:

* **A mean is nearly meaningless** on its own. Sum of Lights and the *share of
  territory above a threshold* are the useful summaries.
* **The threshold is a decision, not a fact.** Move it and "% of the country lit"
  moves with it. So state it, and show the sensitivity — which is what the second
  panel below does.
<!--FR-->
---
<div style="border-left:5px solid #1B7A43;background:#F4F8F5;border-radius:0 12px 12px 0;
 padding:13px 18px;margin:18px 0 8px;font-family:'Segoe UI',system-ui,sans-serif;">
 <span style="background:#1B7A43;color:#fff;border-radius:20px;padding:3px 13px;
  font-weight:700;font-size:11.5px;">ÉTAPE 7/8</span>
 <span style="color:#0B2545;font-weight:800;font-size:1.14em;margin-left:11px;">
  Explorer — la distribution, et pourquoi le seuil compte</span>
 <div style="color:#3a4a42;margin-top:5px;font-size:.96em;">
  La radiance nocturne est extraordinairement asymétrique. Choisir un seuil « éclairé » est un jugement : rendez-le visible.</div>
</div>

Tracez la distribution de la radiance sur votre pays et vous verrez la propriété
la plus importante de cette donnée : elle est dominée par des valeurs proches de
zéro, avec une queue très longue. L'essentiel de votre territoire est sombre. Une
poignée de pixels sont des centaines de fois plus lumineux que la médiane.

Cette forme a deux conséquences qui devraient intéresser un statisticien :

* **Une moyenne n'a presque aucun sens** à elle seule. La Somme des lumières et
  la *part du territoire au-dessus d'un seuil* sont les résumés utiles.
* **Le seuil est une décision, pas un fait.** Déplacez-le et le « % du pays
  éclairé » se déplace avec lui. Déclarez-le donc, et montrez la sensibilité —
  c'est ce que fait le second panneau ci-dessous.
'''

# %%
# <solution hint="Plot the log-scaled histogram, then the sensitivity of lit-area share to the threshold" hint_fr="Tracez l'histogramme en échelle log, puis la sensibilité de la part éclairée au seuil">
valid = inside[np.isfinite(inside)]

fig, ax = plt.subplots(1, 2, figsize=(13, 4.2))

ax[0].hist(np.log10(np.clip(valid, 1e-2, None)), bins=90, color=theme.GREEN, alpha=0.85)
ax[0].axvline(np.log10(LIT_THRESHOLD), color=theme.AMBER, lw=2, ls="--",
              label=T(f"lit threshold = {LIT_THRESHOLD}", f"seuil éclairé = {LIT_THRESHOLD}"))
ax[0].set_xlabel(T("log10 radiance (nW/cm2/sr)", "log10 radiance (nW/cm2/sr)"))
ax[0].set_ylabel(T("Pixel count", "Nombre de pixels"))
ax[0].set_title(T("Distribution of radiance", "Distribution de la radiance"))
ax[0].legend()

thresholds = np.array([0.1, 0.25, 0.5, 1.0, 2.0, 5.0, 10.0])
shares = [100 * (valid >= t).mean() for t in thresholds]
ax[1].plot(thresholds, shares, "o-", color=theme.NAVY, lw=2)
ax[1].axvline(LIT_THRESHOLD, color=theme.AMBER, lw=2, ls="--")
ax[1].set_xscale("log")
ax[1].set_xlabel(T("Threshold (nW/cm2/sr)", "Seuil (nW/cm2/sr)"))
ax[1].set_ylabel(T("% of territory counted as lit", "% du territoire compté comme éclairé"))
ax[1].set_title(T("Your headline number depends on this choice",
                  "Votre chiffre phare dépend de ce choix"))

theme.credit(ax[1], T(f"{C.name('en')} · {PRODUCT} · {demo_year} · NASA Black Marble",
                      f"{C.name('fr')} · {PRODUCT} · {demo_year} · NASA Black Marble"),
             lang="{{LANG}}")
plt.show()

print(T(f"At the {LIT_THRESHOLD} threshold, {100*(valid >= LIT_THRESHOLD).mean():.1f} % of "
        f"{C.name('en')} counts as lit.",
        f"Au seuil {LIT_THRESHOLD}, {100*(valid >= LIT_THRESHOLD).mean():.1f} % de "
        f"{C.name('fr')} est compté comme éclairé."))
print(T(f"At 0.1 it would be {100*(valid >= 0.1).mean():.1f} %; at 5.0, "
        f"{100*(valid >= 5.0).mean():.1f} %. State your threshold in every published figure.",
        f"À 0,1 ce serait {100*(valid >= 0.1).mean():.1f} % ; à 5,0, "
        f"{100*(valid >= 5.0).mean():.1f} %. Déclarez votre seuil dans chaque figure publiée."))
# </solution>

# %% [markdown]
'''
<!--EN-->
---
<div style="border-left:5px solid #1B7A43;background:#F4F8F5;border-radius:0 12px 12px 0;
 padding:13px 18px;margin:18px 0 8px;font-family:'Segoe UI',system-ui,sans-serif;">
 <span style="background:#1B7A43;color:#fff;border-radius:20px;padding:3px 13px;
  font-weight:700;font-size:11.5px;">STEP 8/8</span>
 <span style="color:#0B2545;font-weight:800;font-size:1.14em;margin-left:11px;">
  The artefact hunt — which of these six live in your country?</span>
 <div style="color:#3a4a42;margin-top:5px;font-size:.96em;">
  This is the deliverable. Every country's answer is different, and that is the point.</div>
</div>

The morning talk named six artefacts. Here you find them — in your own raster,
with your own eyes. Work through the panels below and record, for each artefact,
whether it is present in your country and where.

Do not expect to find all six. Nigeria and Algeria will find gas flares
immediately; Rwanda will not. A country with one dominant city will see blooming
and saturation before anything else; a country with several medium cities may
see neither. **The inventory is the deliverable, and a well-argued "not present"
is as valuable as a "present".**
<!--FR-->
---
<div style="border-left:5px solid #1B7A43;background:#F4F8F5;border-radius:0 12px 12px 0;
 padding:13px 18px;margin:18px 0 8px;font-family:'Segoe UI',system-ui,sans-serif;">
 <span style="background:#1B7A43;color:#fff;border-radius:20px;padding:3px 13px;
  font-weight:700;font-size:11.5px;">ÉTAPE 8/8</span>
 <span style="color:#0B2545;font-weight:800;font-size:1.14em;margin-left:11px;">
  La chasse aux artefacts — lesquels des six vivent dans votre pays ?</span>
 <div style="color:#3a4a42;margin-top:5px;font-size:.96em;">
  C'est le livrable. La réponse de chaque pays est différente, et c'est justement l'intérêt.</div>
</div>

L'exposé du matin a nommé six artefacts. Ici, vous les trouvez — dans votre
propre raster, de vos propres yeux. Parcourez les panneaux ci-dessous et
consignez, pour chaque artefact, s'il est présent dans votre pays et où.

Ne vous attendez pas à les trouver tous les six. Le Nigéria et l'Algérie
repéreront immédiatement les torchères ; le Rwanda non. Un pays doté d'une ville
dominante verra le halo lumineux et la saturation avant tout le reste ; un pays
à plusieurs villes moyennes pourrait ne voir ni l'un ni l'autre. **L'inventaire
est le livrable, et un « absent » bien argumenté vaut autant qu'un « présent ».**
'''

# %%
# EN: The catalogue, for reference while you look. | FR: Le catalogue, à garder sous les yeux pendant l'observation.
ui.result_table(ntl.describe_artefacts(lang="{{LANG}}"),
                caption=T("The six artefacts named in the morning talk.",
                          "Les six artefacts nommés dans l'exposé du matin."))

# %%
# <solution hint="Zoom on the brightest cluster to see blooming and saturation; plot the top-20 pixels to spot flares" hint_fr="Zoomez sur l'amas le plus lumineux pour voir le halo et la saturation ; tracez les 20 pixels les plus intenses pour repérer les torchères">
# EN: --- (a) Blooming and saturation: zoom on the brightest place in the country --- | FR: --- (a) Halo et saturation : zoom sur le lieu le plus lumineux du pays ---
flat_index = np.nanargmax(np.nan_to_num(inside, nan=-1))
row, col = np.unravel_index(flat_index, inside.shape)
half = 90
sub = inside[max(0, row - half):row + half, max(0, col - half):col + half]

lon = transform.c + (col + 0.5) * transform.a
lat = transform.f + (row + 0.5) * transform.e

fig, ax = plt.subplots(1, 2, figsize=(13, 4.6))
im = ax[0].imshow(np.log1p(np.nan_to_num(sub)), cmap="stg17_night")
ax[0].set_title(T(f"Brightest cluster — around {lat:.2f}N {lon:.2f}E",
                  f"Amas le plus lumineux — vers {lat:.2f}N {lon:.2f}E"))
ax[0].set_axis_off()
fig.colorbar(im, ax=ax[0], shrink=0.8)

profile = np.nanmax(sub, axis=0)
ax[1].plot(profile, color=theme.AMBER, lw=1.8)
ax[1].set_title(T("Cross-section: a flat top means saturation,\na wide skirt means blooming",
                  "Coupe : un sommet plat signale la saturation,\nun pied large signale le halo"))
ax[1].set_xlabel(T("pixel (west to east)", "pixel (ouest vers est)"))
ax[1].set_ylabel(T("radiance", "radiance"))
plt.show()
# </solution>

# %%
# <solution hint="Rank the brightest pixels and check whether any sit far from a city - those are flare candidates" hint_fr="Classez les pixels les plus intenses et vérifiez si certains sont loin de toute ville - ce sont des candidats torchères">
# EN: --- (b) Gas flares: extreme, isolated, and constant year to year ------- | FR: --- (b) Torchères : extrêmes, isolées, et constantes d'une année à l'autre ---
import pandas as pd

k = 20
flat = np.nan_to_num(inside, nan=-1).ravel()
top = np.argpartition(flat, -k)[-k:]
top = top[np.argsort(flat[top])[::-1]]
rows_, cols_ = np.unravel_index(top, inside.shape)

hotspots = pd.DataFrame({
    T("rank", "rang"): range(1, k + 1),
    T("radiance", "radiance"): flat[top].round(1),
    T("latitude", "latitude"): (transform.f + (rows_ + 0.5) * transform.e).round(3),
    T("longitude", "longitude"): (transform.c + (cols_ + 0.5) * transform.a).round(3),
})
ui.result_table(hotspots, highlight=T("radiance", "radiance"),
                caption=T("The 20 brightest pixels. Cross-check them against a map of your "
                          "cities: any that sit far from a settlement is a flare, a port, an "
                          "airport or an industrial site — not household electrification.",
                          "Les 20 pixels les plus intenses. Recoupez-les avec une carte de vos "
                          "villes : tout point éloigné de toute agglomération est une torchère, "
                          "un port, un aéroport ou un site industriel — pas de l'électrification "
                          "des ménages."))
# </solution>

# %%
# <solution hint="Compare the same clipped raster across the available years to reveal discontinuity and rural noise" hint_fr="Comparez le même raster découpé sur les années disponibles pour révéler discontinuité et bruit rural">
# EN: --- (c) Year-to-year behaviour: discontinuity and rural low-light noise -- | FR: --- (c) Comportement interannuel : discontinuité et bruit rural ---
usable_years = sorted(files)
fig, axes = plt.subplots(1, len(usable_years), figsize=(4.6 * len(usable_years), 4.6))
axes = np.atleast_1d(axes)

series = {}
for axis, year in zip(axes, usable_years):
    granule = files[year][0]
    array, _ = ntl.read_layer(granule.path)
    tr = ntl.tile_transform(granule.tile, array.shape)
    zmask = ntl.rasterize_zones(adm0.assign(__zid__=1), tr, array.shape)
    array[zmask == 0] = np.nan
    series[year] = array

    axis.imshow(np.log1p(np.nan_to_num(array)), cmap="stg17_night")
    axis.set_title(f"{year}")
    axis.set_axis_off()

fig.suptitle(T(f"{C.name('en')} — same clip, {usable_years[0]} to {usable_years[-1]}",
               f"{C.name('fr')} — même découpe, de {usable_years[0]} à {usable_years[-1]}"),
             fontweight="bold", color=theme.NAVY)
plt.show()

for year, array in series.items():
    finite = array[np.isfinite(array)]
    print(T(f"  {year}:  SoL {np.nansum(np.clip(finite, 0, None)):>14,.0f}   "
            f"lit {100*(finite >= LIT_THRESHOLD).mean():5.1f} %   "
            f"negative pixels {100*(finite < 0).mean():4.1f} %",
            f"  {year} :  SoL {np.nansum(np.clip(finite, 0, None)):>14,.0f}   "
            f"éclairé {100*(finite >= LIT_THRESHOLD).mean():5.1f} %   "
            f"pixels négatifs {100*(finite < 0).mean():4.1f} %"))
# </solution>

# %% [markdown]
'''
<!--EN-->
### Your turn — record the inventory

Fill the dictionary below with what you actually saw. Be honest: "not present"
and "cannot tell from this data" are both valid and both useful answers. This
table is a component of your Friday presentation and of the limitations statement
that accompanies every published figure.
<!--FR-->
### À vous — consignez l'inventaire

Remplissez le dictionnaire ci-dessous avec ce que vous avez réellement observé.
Soyez honnête : « absent » et « indéterminable avec ces données » sont deux
réponses valides et utiles. Ce tableau est un élément de votre présentation du
vendredi et de la déclaration de limites qui accompagne chaque figure publiée.
'''

# %%
# EN: Edit this. It is your finding, not a computation. | FR: À modifier. C'est votre constat, pas un calcul.
FINDINGS = {
    # EN: artefact -> (present?, where / evidence) | FR: artefact -> (présent ?, où / preuve)
    "blooming":             ("?", ""),
    "saturation":           ("?", ""),
    "gas_flares":           ("?", ""),
    "seasonality":          ("n/a", T("annual product — check with VNP46A3 monthly",
                                      "produit annuel — à vérifier avec VNP46A3 mensuel")),
    "sensor_discontinuity": ("n/a", T("VIIRS only in this notebook — no DMSP splice",
                                      "VIIRS uniquement ici — aucun raccord DMSP")),
    "rural_noise":          ("?", ""),
    "snow_ice":             ("?", ""),
}

inventory_df = pd.DataFrame([
    {T("Artefact", "Artefact"): key.replace("_", " ").title(),
     T("Present in " + C.name("en"), "Présent en " + C.name("fr")): value[0],
     T("Evidence / location", "Preuve / localisation"): value[1] or "—"}
    for key, value in FINDINGS.items()
])
ui.result_table(inventory_df,
                caption=T(f"Artefact inventory — {C.name('en')}, {PRODUCT}, {usable_years}",
                          f"Inventaire des artefacts — {C.name('fr')}, {PRODUCT}, {usable_years}"))

# %% [markdown]
'''
<!--EN-->
---
## Save the deliverable

Two files, both of which go into your country repository on Friday: the clipped
national raster subset, and the artefact inventory. Both carry the parameters
that produced them, because a raster without its provenance is not reusable and
an inventory without its threshold is not interpretable.
<!--FR-->
---
## Enregistrer le livrable

Deux fichiers, qui rejoindront tous deux le dépôt de votre pays vendredi : le
sous-ensemble raster national découpé, et l'inventaire des artefacts. Les deux
portent les paramètres qui les ont produits, car un raster sans sa provenance
n'est pas réutilisable et un inventaire sans son seuil n'est pas interprétable.
'''

# %%
# <solution hint="Write the clipped GeoTIFF with rasterio, the inventory as CSV, and a JSON metadata sidecar" hint_fr="Écrivez le GeoTIFF découpé avec rasterio, l'inventaire en CSV, et un fichier JSON de métadonnées">
import json
from datetime import datetime, timezone

import rasterio

tif_path = OUT / f"{C.iso3}_{PRODUCT}_{demo_year}_clipped.tif"
with rasterio.open(
    tif_path, "w", driver="GTiff",
    height=inside.shape[0], width=inside.shape[1], count=1,
    dtype="float32", crs="EPSG:4326", transform=transform,
    nodata=np.nan, compress="deflate",
) as dst:
    dst.write(inside.astype("float32"), 1)
    dst.update_tags(
        country=C.name("en"), iso3=C.iso3, product=PRODUCT, year=str(demo_year),
        layer=meta["layer"], scale_factor=str(meta["scale"]),
        lit_threshold=str(LIT_THRESHOLD), source="NASA Black Marble",
        boundaries=admN.attrs["source_name"],
    )

csv_path = OUT / f"{C.iso3}_artefact_inventory.csv"
inventory_df.to_csv(csv_path, index=False, encoding="utf-8")

meta_path = OUT / f"{C.iso3}_d4_metadata.json"
meta_path.write_text(json.dumps({
    "country": {"iso3": C.iso3, "name_en": C.name("en"), "name_fr": C.name("fr")},
    "product": PRODUCT,
    "years_processed": usable_years,
    "years_incomplete_excluded": incomplete,
    "tiles": C.viirs_tiles,
    "layer": meta["layer"],
    "scale_factor_from_file": meta["scale"],
    "lit_threshold_nW_cm2_sr": LIT_THRESHOLD,
    "boundaries_source": admN.attrs["source_name"],
    "admin_level": ADM_LEVEL,
    "artefacts_found": {k: v[0] for k, v in FINDINGS.items()},
    "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    "workshop": "STG17 · AfDB / STATAFRIC · Action Plan 2025-2030",
}, indent=2, ensure_ascii=False), encoding="utf-8")

for path in (tif_path, csv_path, meta_path):
    print(T(f"  wrote {path}", f"  écrit {path}"))
# </solution>

# %% [markdown]
'''
<!--EN-->
<div style="border:1px solid #1B7A43;border-left:6px solid #1B7A43;background:#EAF4EE;
 padding:13px 17px;border-radius:0 9px 9px 0;margin:14px 0;font-family:'Segoe UI',system-ui,sans-serif;">
<b style="color:#1B7A43;font-size:11.5px;letter-spacing:1.6px;">★ TEAM DELIVERABLE</b><br>
<span style="color:#33403A;font-size:14.3px;line-height:1.58;">
<b>1.</b> A documented national raster subset (<code>*_clipped.tif</code>) carrying its product,
year, layer, scale factor and boundary source as embedded tags.<br>
<b>2.</b> An inventory of which artefacts are present in your country, with the evidence.<br>
<b>3.</b> The metadata sidecar (<code>*_metadata.json</code>), which is what makes the result
reproducible by someone who was not in the room.<br><br>
Commit all three to your country repository. The afternoon laboratory (analysis and validation)
starts from exactly these files.
</span></div>
<!--FR-->
<div style="border:1px solid #1B7A43;border-left:6px solid #1B7A43;background:#EAF4EE;
 padding:13px 17px;border-radius:0 9px 9px 0;margin:14px 0;font-family:'Segoe UI',system-ui,sans-serif;">
<b style="color:#1B7A43;font-size:11.5px;letter-spacing:1.6px;">★ LIVRABLE DE L'ÉQUIPE</b><br>
<span style="color:#33403A;font-size:14.3px;line-height:1.58;">
<b>1.</b> Un sous-ensemble raster national documenté (<code>*_clipped.tif</code>) portant en
étiquettes intégrées son produit, son année, sa couche, son facteur d'échelle et sa source de
frontières.<br>
<b>2.</b> Un inventaire des artefacts présents dans votre pays, avec les preuves.<br>
<b>3.</b> Le fichier de métadonnées (<code>*_metadata.json</code>), qui rend le résultat
reproductible par quelqu'un qui n'était pas dans la salle.<br><br>
Versionnez les trois dans le dépôt de votre pays. Le laboratoire de l'après-midi (analyse et
validation) démarre exactement de ces fichiers.
</span></div>
'''

# %% [markdown]
'''
<!--EN-->
---
## Limitations — read before quoting any number from this notebook

<div style="border:1px solid #F2A900;border-radius:10px;background:#FFFDF6;
 padding:16px 20px;margin:16px 0;font-family:'Segoe UI',system-ui,sans-serif;">
<ul style="color:#33403A;font-size:14px;line-height:1.7;margin:0;padding-left:22px;">
<li><b>Radiance is a proxy, not an outcome.</b> It measures light leaving the ground at night. It
does not measure GDP, and it does not measure the household connection rate. Anyone who reads
"electrification" directly off a Sum of Lights series is over-claiming.</li>
<li><b>The lit threshold is a choice.</b> Every "% of territory lit" figure in this notebook moves
if you move <code>LIT_THRESHOLD</code>. Publish the threshold alongside the number, always.</li>
<li><b>Gas flares are indistinguishable from cities</b> at this resolution without an external
mask. In flare-affected countries, regional totals can be dominated by activity that
electrifies nobody.</li>
<li><b>Saturation caps growth in the brightest cores.</b> A capital that stopped growing in the
data may simply have stopped growing in the sensor.</li>
<li><b>Boundaries used here are geoBoundaries, not your national file.</b> Subnational figures
will shift when you substitute the official boundaries — sometimes materially, at ADM2.</li>
<li><b>Annual composites hide seasonality.</b> Nothing in this notebook can speak to
month-to-month variation; that needs VNP46A3 and a separate treatment of cloud cover.</li>
</ul></div>

This is not a disclaimer to append at the end. It is a component of the
deliverable, and Day 4 afternoon turns it into a formal statement backed by a
correlation against your own official subnational indicator.
<!--FR-->
---
## Limites — à lire avant de citer le moindre chiffre de ce carnet

<div style="border:1px solid #F2A900;border-radius:10px;background:#FFFDF6;
 padding:16px 20px;margin:16px 0;font-family:'Segoe UI',system-ui,sans-serif;">
<ul style="color:#33403A;font-size:14px;line-height:1.7;margin:0;padding-left:22px;">
<li><b>La radiance est un indicateur indirect, pas un résultat.</b> Elle mesure la lumière quittant
le sol la nuit. Elle ne mesure ni le PIB, ni le taux de raccordement des ménages. Quiconque lit
« électrification » directement sur une série de Somme des lumières sur-interprète.</li>
<li><b>Le seuil d'éclairement est un choix.</b> Chaque « % du territoire éclairé » de ce carnet
change si vous changez <code>LIT_THRESHOLD</code>. Publiez toujours le seuil à côté du chiffre.</li>
<li><b>Les torchères sont indiscernables des villes</b> à cette résolution sans masque externe.
Dans les pays concernés, les totaux régionaux peuvent être dominés par une activité qui
n'électrifie personne.</li>
<li><b>La saturation plafonne la croissance des cœurs les plus lumineux.</b> Une capitale qui a
cessé de croître dans les données a peut-être simplement cessé de croître dans le capteur.</li>
<li><b>Les frontières utilisées ici sont celles de geoBoundaries, pas votre fichier national.</b>
Les chiffres infranationaux se déplaceront lors de la substitution — parfois sensiblement, à
l'ADM2.</li>
<li><b>Les composites annuels masquent la saisonnalité.</b> Rien dans ce carnet ne peut parler de
la variation mensuelle ; cela exige le VNP46A3 et un traitement distinct de la couverture
nuageuse.</li>
</ul></div>

Ceci n'est pas un avertissement à ajouter à la fin. C'est un élément du livrable,
et l'après-midi du Jour 4 le transforme en déclaration formelle étayée par une
corrélation avec votre propre indicateur infranational officiel.
'''

# %% [markdown]
'''
<!--EN-->
---
<div style="background:#F4F8F5;border-radius:11px;padding:16px 19px;margin:18px 0;
 font-family:'Segoe UI',system-ui,sans-serif;">
<b style="color:#1B7A43;letter-spacing:1.6px;font-size:11.5px;">? CHECKPOINT — TEST YOURSELF</b>

<details style="margin:9px 0;border:1px solid #1B7A43;border-radius:9px;padding:11px 15px;background:#fff;">
<summary style="cursor:pointer;color:#0B2545;font-weight:600;">Why do we read <code>scale_factor</code> from the file instead of using the documented value?</summary>
<p style="color:#3D4A45;margin:9px 0 0;line-height:1.6;">Because the documented value belongs to a
collection version. NASA has changed it before and will again. Code that reads the attribute keeps
producing correct physical units across a version change; code with a constant produces wrong
numbers silently, and no test catches it because the pipeline still runs.</p></details>

<details style="margin:9px 0;border:1px solid #1B7A43;border-radius:9px;padding:11px 15px;background:#fff;">
<summary style="cursor:pointer;color:#0B2545;font-weight:600;">Your national Sum of Lights rises 40 % in one year. Name three explanations before "the economy grew".</summary>
<p style="color:#3D4A45;margin:9px 0 0;line-height:1.6;">(1) The previous year was missing a tile,
so you are comparing a partial country with a whole one. (2) A new gas flare came online.
(3) The collection version changed between the two files. Only after excluding all three does an
economic reading become defensible — and even then it is a proxy.</p></details>

<details style="margin:9px 0;border:1px solid #1B7A43;border-radius:9px;padding:11px 15px;background:#fff;">
<summary style="cursor:pointer;color:#0B2545;font-weight:600;">Why compute areas in EPSG:32630 rather than in degrees?</summary>
<p style="color:#3D4A45;margin:9px 0 0;line-height:1.6;">A degree of longitude is about 111 km at
the equator and about 91 km at 35°N. Summing "square degrees" therefore inflates the apparent area
of northern regions relative to equatorial ones — which biases every north-south comparison on the
continent. The country's UTM zone is available as <code>C.utm_epsg()</code>.</p></details>

<details style="margin:9px 0;border:1px solid #1B7A43;border-radius:9px;padding:11px 15px;background:#fff;">
<summary style="cursor:pointer;color:#0B2545;font-weight:600;">A colleague clips with the bounding box instead of the polygon. What breaks?</summary>
<p style="color:#3D4A45;margin:9px 0 0;line-height:1.6;">The bounding box of most countries
contains large parts of their neighbours. Lagos would contribute to Benin's total, and Johannesburg
to Lesotho's. The bbox in this toolkit is used only to choose which tiles to download and to set a
map extent — never to clip.</p></details>
</div>
<!--FR-->
---
<div style="background:#F4F8F5;border-radius:11px;padding:16px 19px;margin:18px 0;
 font-family:'Segoe UI',system-ui,sans-serif;">
<b style="color:#1B7A43;letter-spacing:1.6px;font-size:11.5px;">? POINT DE CONTRÔLE — TESTEZ-VOUS</b>

<details style="margin:9px 0;border:1px solid #1B7A43;border-radius:9px;padding:11px 15px;background:#fff;">
<summary style="cursor:pointer;color:#0B2545;font-weight:600;">Pourquoi lire <code>scale_factor</code> dans le fichier plutôt qu'utiliser la valeur documentée ?</summary>
<p style="color:#3D4A45;margin:9px 0 0;line-height:1.6;">Parce que la valeur documentée appartient
à une version de collection. La NASA l'a déjà changée et le refera. Un code qui lit l'attribut
continue de produire des unités physiques correctes après un changement de version ; un code
contenant une constante produit silencieusement des nombres faux, et aucun test ne le détecte
puisque la chaîne s'exécute toujours.</p></details>

<details style="margin:9px 0;border:1px solid #1B7A43;border-radius:9px;padding:11px 15px;background:#fff;">
<summary style="cursor:pointer;color:#0B2545;font-weight:600;">Votre Somme des lumières nationale augmente de 40 % en un an. Citez trois explications avant « l'économie a crû ».</summary>
<p style="color:#3D4A45;margin:9px 0 0;line-height:1.6;">(1) L'année précédente manquait une tuile :
vous comparez un pays partiel à un pays entier. (2) Une nouvelle torchère est entrée en service.
(3) La version de collection a changé entre les deux fichiers. Ce n'est qu'après avoir écarté ces
trois cas qu'une lecture économique devient défendable — et encore, c'est un indicateur
indirect.</p></details>

<details style="margin:9px 0;border:1px solid #1B7A43;border-radius:9px;padding:11px 15px;background:#fff;">
<summary style="cursor:pointer;color:#0B2545;font-weight:600;">Pourquoi calculer les aires en EPSG:32630 plutôt qu'en degrés ?</summary>
<p style="color:#3D4A45;margin:9px 0 0;line-height:1.6;">Un degré de longitude vaut environ 111 km
à l'équateur et environ 91 km à 35°N. Sommer des « degrés carrés » gonfle donc l'aire apparente des
régions septentrionales par rapport aux régions équatoriales — ce qui biaise toute comparaison
nord-sud sur le continent. La zone UTM du pays est disponible via <code>C.utm_epsg()</code>.</p></details>

<details style="margin:9px 0;border:1px solid #1B7A43;border-radius:9px;padding:11px 15px;background:#fff;">
<summary style="cursor:pointer;color:#0B2545;font-weight:600;">Un collègue découpe avec l'emprise rectangulaire plutôt qu'avec le polygone. Qu'est-ce qui casse ?</summary>
<p style="color:#3D4A45;margin:9px 0 0;line-height:1.6;">L'emprise rectangulaire de la plupart des
pays contient de larges portions de leurs voisins. Lagos contribuerait au total du Bénin, et
Johannesburg à celui du Lesotho. L'emprise de cette boîte à outils sert uniquement à choisir les
tuiles à télécharger et à cadrer une carte — jamais à découper.</p></details>
</div>
'''

# %% [markdown]
'''
<!--EN-->
---
### Where this goes next

| When | What |
|---|---|
| **Day 4, 14:00** | Analysis — zonal statistics by administrative level, time series, change detection |
| **Day 4, 15:45** | Validation — correlate the proxy against your own official subnational indicator, and decide with evidence whether it is publishable |
| **Day 4, 16:30** | Commit these files, and assemble the week's three outputs into the Friday presentation |
| **Day 5, 09:00** | Publish the country repository, with licensing, DOI and metadata |

<div style="background:linear-gradient(135deg,#0B2545,#1B7A43);border-radius:16px;
 padding:22px 30px;margin-top:22px;text-align:center;font-family:'Segoe UI',system-ui,sans-serif;">
 <div style="color:#F2A900;font-size:11.5px;letter-spacing:2.5px;font-weight:700;">
  DATA SCIENCE TOOLKIT · AfDB / STATAFRIC</div>
 <div style="color:#fff;font-size:1.05em;margin-top:7px;font-weight:600;">
  STG17 workshop · Action Plan 2025-2030 · activities 4.2.1 and 2.1.1</div></div>
<!--FR-->
---
### La suite

| Quand | Quoi |
|---|---|
| **Jour 4, 14h00** | Analyse — statistiques zonales par niveau administratif, séries temporelles, détection de changement |
| **Jour 4, 15h45** | Validation — corréler l'indicateur indirect avec votre propre indicateur infranational officiel, et décider avec preuves s'il est publiable |
| **Jour 4, 16h30** | Versionner ces fichiers, et assembler les trois productions de la semaine dans la présentation du vendredi |
| **Jour 5, 09h00** | Publier le dépôt du pays, avec licence, DOI et métadonnées |

<div style="background:linear-gradient(135deg,#0B2545,#1B7A43);border-radius:16px;
 padding:22px 30px;margin-top:22px;text-align:center;font-family:'Segoe UI',system-ui,sans-serif;">
 <div style="color:#F2A900;font-size:11.5px;letter-spacing:2.5px;font-weight:700;">
  DATA SCIENCE TOOLKIT · BAD / STATAFRIC</div>
 <div style="color:#fff;font-size:1.05em;margin-top:7px;font-weight:600;">
  Atelier STG17 · Plan d'action 2025-2030 · activités 4.2.1 et 2.1.1</div></div>
'''
