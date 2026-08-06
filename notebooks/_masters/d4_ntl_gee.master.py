# %% [meta]
'''
id: d4_ntl_gee
day: 4
title_en: Night-Time Lights on Google Earth Engine - nothing downloaded
title_fr: Lumières nocturnes sur Google Earth Engine - aucun téléchargement
outdir: notebooks/day4
stem: D4_NTL_GEE
country: CIV
tracks: guided, open
'''

# %% [markdown]
'''
<!--EN-->
<div style="background:linear-gradient(135deg,#0B2545 0%,#1B7A43 100%);
 border-radius:18px;padding:32px 38px;font-family:'Segoe UI',system-ui,sans-serif;">
 <div style="color:#F2A900;font-size:12.5px;letter-spacing:3px;font-weight:700;
  text-transform:uppercase;">Day 4 · Earth Engine variant · runs in Colab</div>
 <div style="color:#fff;font-size:2em;font-weight:800;margin:10px 0 8px;line-height:1.15;">
  Night-Time Lights without downloading anything</div>
 <div style="color:#dbe7e0;font-size:1.05em;line-height:1.55;max-width:900px;">
  The same analysis as <code>D4_NTL_Collect_Explore</code>, with the pixels left where they are.
  You send an expression; Google runs it on their copy of the archive; a table comes back.
  A country-year statistic that costs 800 MB of download locally costs a few kilobytes here.
 </div>
 <div style="color:#F2A900;font-size:13px;margin-top:14px;font-weight:600;">
  Deliverable: the same national panel, plus a documented comparison against the local path.</div>
</div>
<!--FR-->
<div style="background:linear-gradient(135deg,#0B2545 0%,#1B7A43 100%);
 border-radius:18px;padding:32px 38px;font-family:'Segoe UI',system-ui,sans-serif;">
 <div style="color:#F2A900;font-size:12.5px;letter-spacing:3px;font-weight:700;
  text-transform:uppercase;">Jour 4 · variante Earth Engine · s'exécute dans Colab</div>
 <div style="color:#fff;font-size:2em;font-weight:800;margin:10px 0 8px;line-height:1.15;">
  Les lumières nocturnes sans rien télécharger</div>
 <div style="color:#dbe7e0;font-size:1.05em;line-height:1.55;max-width:900px;">
  La même analyse que <code>D4_NTL_Collect_Explore</code>, mais en laissant les pixels où ils sont.
  Vous envoyez une expression ; Google l'exécute sur sa copie de l'archive ; un tableau revient.
  Une statistique pays-année qui coûte 800 Mo de téléchargement en local coûte ici quelques kilo-octets.
 </div>
 <div style="color:#F2A900;font-size:13px;margin-top:14px;font-weight:600;">
  Livrable : le même panel national, plus une comparaison documentée avec la voie locale.</div>
</div>
'''

# %% [markdown]
'''
<!--EN-->
### When to use this notebook instead of the local one

Use Earth Engine when bandwidth is the constraint — which, on most institutional
networks in the region, it is. Use the local path when reproducibility on an
offline machine is the constraint, or when you need a product Google does not
host.

| | Local (rasterio) | Earth Engine |
|---|---|---|
| Network | none required | required |
| Who holds the pixels | you | Google |
| Reproducible offline | yes | no |
| Products available | anything NASA publishes | what Google has ingested |
| Scales with | your disk and RAM | Google's cluster |
| Long-term dependency | none | on a commercial service |

That last row is not a footnote. A national statistical office building a
production indicator on a free tier of a commercial service is taking on a
dependency it does not control — the sovereignty question of Day 1 afternoon, in
concrete form. The honest answer is usually: **prototype on Earth Engine,
produce on your own infrastructure**, and this notebook plus its local twin let
you do exactly that.
<!--FR-->
### Quand utiliser ce carnet plutôt que le carnet local

Utilisez Earth Engine quand la bande passante est la contrainte — ce qui, sur la
plupart des réseaux institutionnels de la région, est le cas. Utilisez la voie
locale quand la contrainte est la reproductibilité sur une machine hors ligne, ou
quand vous avez besoin d'un produit que Google n'héberge pas.

| | Local (rasterio) | Earth Engine |
|---|---|---|
| Réseau | aucun requis | requis |
| Qui détient les pixels | vous | Google |
| Reproductible hors ligne | oui | non |
| Produits disponibles | tout ce que publie la NASA | ce que Google a intégré |
| Passe à l'échelle avec | votre disque et votre RAM | le cluster de Google |
| Dépendance de long terme | aucune | envers un service commercial |

Cette dernière ligne n'est pas une note de bas de page. Un office national de
statistique qui bâtit un indicateur de production sur l'offre gratuite d'un
service commercial contracte une dépendance qu'il ne maîtrise pas — la question
de souveraineté du Jour 1 après-midi, sous forme concrète. La réponse honnête est
généralement : **prototyper sur Earth Engine, produire sur son infrastructure**,
et ce carnet, avec son jumeau local, permet exactement cela.
'''

# %% [markdown]
'''
<!--EN-->
---
## Requirements and authorisation

Earth Engine needs a **free** account attached to a Google Cloud project.
Registration takes a few minutes at
[code.earthengine.google.com/register](https://code.earthengine.google.com/register)
and is on the pre-workshop checklist for exactly that reason.

The first `initialise()` opens a browser window once. After that, credentials are
cached.
<!--FR-->
---
## Prérequis et autorisation

Earth Engine exige un compte **gratuit** rattaché à un projet Google Cloud.
L'inscription prend quelques minutes sur
[code.earthengine.google.com/register](https://code.earthengine.google.com/register)
et figure dans la liste préalable à l'atelier précisément pour cette raison.

Le premier `initialise()` ouvre une fenêtre de navigateur, une seule fois.
Ensuite, les identifiants sont mis en cache.
'''

# %%
# EN: --- Requirements for the Earth Engine variant ------------------------- | FR: --- Prérequis de la variante Earth Engine -----------------------------
REQUIREMENTS = {
    "ee":         "earthengine-api>=0.1.380",
    "geemap":     "geemap>=0.30",
    "pandas":     "pandas>=2.0",
    "matplotlib": "matplotlib>=3.7",
}

import subprocess
import sys

try:
    import stg17
except ImportError:
    subprocess.run([sys.executable, "-m", "pip", "install", "-q",
                    "stg17 @ git+https://github.com/{{ORG}}/{{REPO}}"], check=False)
    import stg17

from stg17 import setup, countries, theme, ui
from stg17.i18n import T

S = setup(REQUIREMENTS, lang="{{LANG_UPPER}}")

# %%
# EN: Your Cloud project id - from the Earth Engine registration page. | FR: L'identifiant de votre projet Cloud - depuis la page d'inscription Earth Engine.
GEE_PROJECT = None   # EN: e.g. "ee-yourname". None lets Earth Engine pick a default. | FR: ex. "ee-votrenom". None laisse Earth Engine choisir par défaut.

from stg17 import ntl_gee

ee = ntl_gee.initialise(project=GEE_PROJECT)

# %% [markdown]
'''
<!--EN-->
---
## Step 1 — Your country

Same single variable as the local notebook. Nothing else changes.
<!--FR-->
---
## Étape 1 — Votre pays

La même variable unique que dans le carnet local. Rien d'autre ne change.
'''

# %%
# ===========================================================================
# EN: THE ONLY LINE YOU NEED TO CHANGE | FR: LA SEULE LIGNE À MODIFIER
# ===========================================================================
COUNTRY_ISO3 = "{{ISO3}}"

YEARS         = list(range(2014, 2024))   # EN: EOG annual VNL covers 2012-2023 | FR: le VNL annuel EOG couvre 2012-2023
ADM_LEVEL     = 1
LIT_THRESHOLD = 0.5
SCALE_M       = 500       # EN: reduction resolution; raise to 1000 for a faster large country | FR: résolution de réduction ; passez à 1000 pour un grand pays plus rapide

C = countries.get(COUNTRY_ISO3)
OUT = S.outputs(C.iso3, "d4_ntl_gee")

nation = ntl_gee.country_geometry(ee, C, level=0)
zones = ntl_gee.country_geometry(ee, C, level=ADM_LEVEL)

n_zones = zones.size().getInfo()
print(f"{C.name('{{LANG}}')} ({C.iso3})")
print(T(f"  ADM{ADM_LEVEL} units found in FAO GAUL: {n_zones}",
        f"  Unités ADM{ADM_LEVEL} trouvées dans FAO GAUL : {n_zones}"))
print(T(f"  Reduction scale: {SCALE_M} m    Years: {YEARS[0]}-{YEARS[-1]}",
        f"  Échelle de réduction : {SCALE_M} m    Années : {YEARS[0]}-{YEARS[-1]}"))

if n_zones == 0:
    print(T("No units returned. GAUL spells some country names differently from ISO - "
            "check stg17.ntl_gee._GAUL_ALIASES, or upload your own boundaries as an asset.",
            "Aucune unité retournée. GAUL orthographie certains noms de pays différemment de l'ISO - "
            "vérifiez stg17.ntl_gee._GAUL_ALIASES, ou téléversez vos propres frontières comme asset."))

# %% [markdown]
'''
<!--EN-->
<div style="border:1px solid #F2A900;border-left:6px solid #F2A900;background:#FEF9EC;
 padding:13px 17px;border-radius:0 9px 9px 0;margin:14px 0;font-family:'Segoe UI',system-ui,sans-serif;">
<b style="color:#F2A900;font-size:11.5px;letter-spacing:1.6px;">▲ WATCH OUT — FAO GAUL IS FROM 2015</b><br>
<span style="color:#33403A;font-size:14.3px;line-height:1.58;">
The boundaries built into Earth Engine are the FAO GAUL 2015 release. They predate several
administrative reorganisations across the continent, and they still call Eswatini "Swaziland".
They are fine for a prototype. For anything you publish, upload your national boundary file as an
Earth Engine asset and pass it via <code>asset=</code> — the function supports it, and Day 5
explains the workflow.
</span></div>
<!--FR-->
<div style="border:1px solid #F2A900;border-left:6px solid #F2A900;background:#FEF9EC;
 padding:13px 17px;border-radius:0 9px 9px 0;margin:14px 0;font-family:'Segoe UI',system-ui,sans-serif;">
<b style="color:#F2A900;font-size:11.5px;letter-spacing:1.6px;">▲ ATTENTION — FAO GAUL DATE DE 2015</b><br>
<span style="color:#33403A;font-size:14.3px;line-height:1.58;">
Les frontières intégrées à Earth Engine sont celles de l'édition FAO GAUL 2015. Elles sont
antérieures à plusieurs réorganisations administratives sur le continent, et elles appellent
encore l'Eswatini « Swaziland ». Cela convient pour un prototype. Pour toute publication,
téléversez votre fichier de frontières national comme asset Earth Engine et passez-le via
<code>asset=</code> — la fonction le prend en charge, et le Jour 5 explique la procédure.
</span></div>
'''

# %% [markdown]
'''
<!--EN-->
---
## Step 2 — Look at one year, interactively

`geemap` renders an Earth Engine image as a live tile layer. Pan and zoom: the
tiles are computed on demand, so exploring a whole country costs nothing more
than exploring one district.

Note the colour ramp — it is the same `stg17_night` ramp the local notebook uses,
so a map produced here and a map produced there are directly comparable.
<!--FR-->
---
## Étape 2 — Observer une année, interactivement

`geemap` affiche une image Earth Engine comme une couche de tuiles vivante.
Déplacez et zoomez : les tuiles sont calculées à la demande, donc explorer un
pays entier ne coûte pas plus que d'explorer un district.

Notez la palette — c'est la même rampe `stg17_night` que celle du carnet local,
de sorte qu'une carte produite ici et une carte produite là-bas sont directement
comparables.
'''

# %%
# <solution hint="Build an interactive map for the most recent year with ntl_gee.map_year()" hint_fr="Construisez une carte interactive pour l'année la plus récente avec ntl_gee.map_year()">
m = ntl_gee.map_year(ee, YEARS[-1], C, level=ADM_LEVEL, vmax=60)
m
# </solution>

# %% [markdown]
'''
<!--EN-->
---
## Step 3 — The panel: year × administrative unit

This is the same table the local notebook builds, computed server-side. What
comes back over the network is a few hundred rows of numbers.

Watch the timing. On a normal connection this is faster than downloading a single
granule, and it covers ten years.
<!--FR-->
---
## Étape 3 — Le panel : année × unité administrative

C'est le même tableau que celui construit par le carnet local, calculé côté
serveur. Ce qui revient par le réseau est de quelques centaines de lignes de
nombres.

Observez le chronomètre. Sur une connexion normale, c'est plus rapide que le
téléchargement d'un seul granule, et cela couvre dix années.
'''

# %%
# <solution hint="Call ntl_gee.zonal_panel() over YEARS and time it" hint_fr="Appelez ntl_gee.zonal_panel() sur YEARS et chronométrez">
import time

t0 = time.time()
panel = ntl_gee.zonal_panel(ee, YEARS, zones, level=ADM_LEVEL,
                            scale=SCALE_M, lit_threshold=LIT_THRESHOLD)
elapsed = time.time() - t0

print(T(f"\n{len(panel)} rows in {elapsed:.0f} s — nothing was downloaded.",
        f"\n{len(panel)} lignes en {elapsed:.0f} s — rien n'a été téléchargé."))

latest = panel[panel.year == YEARS[-1]].nlargest(12, "sol")
ui.result_table(latest[[f"ADM{ADM_LEVEL}", "sol", "mean_rad", "lit_km2", "lit_pct"]],
                highlight="sol",
                caption=T(f"{C.name('en')} — brightest ADM{ADM_LEVEL} units, {YEARS[-1]}",
                          f"{C.name('fr')} — unités ADM{ADM_LEVEL} les plus lumineuses, {YEARS[-1]}"))
# </solution>

# %% [markdown]
'''
<!--EN-->
---
## Step 4 — The national series

Two panels: the national Sum of Lights indexed to its first year, and the share
of territory above the lit threshold. Together they separate "more light in the
same places" from "light reaching new places" — a distinction that matters
enormously for an electrification reading and that a single series hides.
<!--FR-->
---
## Étape 4 — La série nationale

Deux panneaux : la Somme des lumières nationale indexée sur sa première année, et
la part du territoire au-dessus du seuil d'éclairement. Ensemble, ils séparent
« plus de lumière aux mêmes endroits » de « la lumière atteint de nouveaux
endroits » — une distinction capitale pour une lecture en termes
d'électrification, et qu'une série unique masque.
'''

# %%
# <solution hint="Aggregate the panel to national level and plot the two series" hint_fr="Agrégez le panel au niveau national et tracez les deux séries">
import matplotlib.pyplot as plt

national = (panel.groupby("year", as_index=False)
                 .agg(sol=("sol", "sum"), lit_km2=("lit_km2", "sum"),
                      area_km2=("area_km2", "sum")))
national["lit_pct"] = 100 * national["lit_km2"] / national["area_km2"]

from stg17 import ntl

growth = ntl.cagr(national.sol.iloc[0], national.sol.iloc[-1], len(national) - 1)

fig, ax = plt.subplots(1, 2, figsize=(13, 4.2))
ax[0].plot(national.year, 100 * national.sol / national.sol.iloc[0], "o-",
           color=theme.GREEN, lw=2.2)
ax[0].set_title(T(f"National light index (base 100 = {YEARS[0]})",
                  f"Indice lumineux national (base 100 = {YEARS[0]})"))
ax[0].set_ylabel(T("Sum of Lights (index)", "Somme des lumières (indice)"))

ax[1].plot(national.year, national.lit_pct, "s-", color=theme.AMBER, lw=2.2)
ax[1].set_title(T(f"Territory above {LIT_THRESHOLD} nW/cm2/sr",
                  f"Territoire au-dessus de {LIT_THRESHOLD} nW/cm2/sr"))
ax[1].set_ylabel(T("% of area", "% de la superficie"))

fig.suptitle(T(f"{C.name('en')} · EOG annual VNL · SoL growth {growth:.1f} %/yr",
               f"{C.name('fr')} · VNL annuel EOG · croissance SoL {growth:.1f} %/an"),
             fontweight="bold", color=theme.NAVY)
theme.credit(ax[1], T("Source: NOAA/EOG VIIRS annual VNL v2.2 via Google Earth Engine",
                      "Source : VNL annuel VIIRS NOAA/EOG v2.2 via Google Earth Engine"),
             lang="{{LANG}}")
plt.show()
# </solution>

# %% [markdown]
'''
<!--EN-->
---
## Step 5 — Compare the two pipelines

This is the step that makes the notebook worth running even if you already did
the local one.

Load the panel your local notebook produced and put the two national series side
by side. **They will not be identical.** EOG's annual VNL and NASA's VNP46A4 use
different compositing, different outlier removal and different masking. A gap of
a few percent is expected and healthy; a gap of a factor of two means one of the
two runs has a problem worth finding.

What a statistical office takes from this: the number depends on the pipeline,
so the pipeline is part of the metadata. Publishing "Sum of Lights = 4.2 million"
without naming the product and the version is not a reproducible statistic.
<!--FR-->
---
## Étape 5 — Comparer les deux chaînes

C'est l'étape qui justifie l'exécution de ce carnet même si vous avez déjà fait
le carnet local.

Chargez le panel produit par votre carnet local et placez les deux séries
nationales côte à côte. **Elles ne seront pas identiques.** Le VNL annuel de
l'EOG et le VNP46A4 de la NASA utilisent un compositage, une élimination des
valeurs aberrantes et un masquage différents. Un écart de quelques pour cent est
attendu et sain ; un écart d'un facteur deux signifie que l'une des deux
exécutions a un problème qu'il vaut la peine de trouver.

Ce qu'un office de statistique en retient : le nombre dépend de la chaîne, donc
la chaîne fait partie des métadonnées. Publier « Somme des lumières = 4,2
millions » sans nommer le produit et sa version n'est pas une statistique
reproductible.
'''

# %%
# <solution hint="Load the local panel if present and overlay the two indexed national series" hint_fr="Chargez le panel local s'il existe et superposez les deux séries nationales indexées">
from pathlib import Path

local_panel_path = S.outputs(C.iso3, "d4_ntl") / f"{C.iso3}_panel_adm{ADM_LEVEL}.csv"

if local_panel_path.exists():
    import pandas as pd

    local = pd.read_csv(local_panel_path)
    local_nat = local.groupby("year", as_index=False).agg(sol=("sol", "sum"))
    common = sorted(set(local_nat.year) & set(national.year))

    fig, ax = plt.subplots(figsize=(9, 4))
    for frame, label, colour in [
        (national, T("Earth Engine (EOG VNL)", "Earth Engine (VNL EOG)"), theme.GREEN),
        (local_nat, T("Local (NASA VNP46A4)", "Local (NASA VNP46A4)"), theme.NAVY),
    ]:
        sub = frame[frame.year.isin(common)]
        ax.plot(sub.year, 100 * sub.sol / sub.sol.iloc[0], "o-", lw=2, color=colour, label=label)
    ax.set_title(T("Two defensible pipelines, two slightly different answers",
                   "Deux chaînes défendables, deux réponses légèrement différentes"))
    ax.set_ylabel(T("Sum of Lights (index, first common year = 100)",
                    "Somme des lumières (indice, 1re année commune = 100)"))
    ax.legend()
    plt.show()
else:
    print(T(f"No local panel at {local_panel_path}.",
            f"Pas de panel local à {local_panel_path}."))
    print(T("Run D4_NTL_Collect_Explore and the afternoon analysis notebook first, "
            "then come back to this cell — the comparison is the point of the exercise.",
            "Exécutez d'abord D4_NTL_Collect_Explore et le carnet d'analyse de l'après-midi, "
            "puis revenez à cette cellule — la comparaison est l'objet de l'exercice."))
# </solution>

# %% [markdown]
'''
<!--EN-->
---
## Step 6 — Export and save

Two outputs. The panel as CSV, which is what the afternoon laboratory consumes.
And, optionally, a clipped GeoTIFF exported to your Drive — the practical bridge
between the two worlds: composite on Google's cluster, then continue in rasterio
on one manageable national file instead of six 10° tiles.
<!--FR-->
---
## Étape 6 — Exporter et enregistrer

Deux sorties. Le panel en CSV, que le laboratoire de l'après-midi consomme. Et,
optionnellement, un GeoTIFF découpé exporté vers votre Drive — le pont pratique
entre les deux mondes : compositer sur le cluster de Google, puis poursuivre sous
rasterio sur un seul fichier national maniable plutôt que sur six tuiles de 10°.
'''

# %%
# <solution hint="Save the panel to CSV with a metadata sidecar, then optionally queue a Drive export" hint_fr="Enregistrez le panel en CSV avec un fichier de métadonnées, puis lancez éventuellement un export Drive">
import json
from datetime import datetime, timezone

panel_path = OUT / f"{C.iso3}_gee_panel_adm{ADM_LEVEL}.csv"
panel.to_csv(panel_path, index=False, encoding="utf-8")

(OUT / f"{C.iso3}_gee_metadata.json").write_text(json.dumps({
    "country": {"iso3": C.iso3, "name_en": C.name("en"), "name_fr": C.name("fr")},
    "engine": "Google Earth Engine",
    "collection": ntl_gee.COLLECTIONS["annual_vnl"]["id"],
    "band": ntl_gee.COLLECTIONS["annual_vnl"]["band"],
    "years": YEARS,
    "reduction_scale_m": SCALE_M,
    "lit_threshold_nW_cm2_sr": LIT_THRESHOLD,
    "boundaries_source": f"FAO GAUL 2015 level {ADM_LEVEL} (NOT authoritative - substitute your national file before publishing)",
    "admin_level": ADM_LEVEL,
    "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    "workshop": "STG17 · AfDB / STATAFRIC · Action Plan 2025-2030",
}, indent=2, ensure_ascii=False), encoding="utf-8")

print(T(f"  wrote {panel_path}", f"  écrit {panel_path}"))

# EN: Optional: queue a clipped national GeoTIFF to your Google Drive. | FR: Optionnel : mettre en file un GeoTIFF national découpé vers votre Google Drive.
EXPORT_TO_DRIVE = False
if EXPORT_TO_DRIVE:
    image = ntl_gee.annual_image(ee, YEARS[-1], region=nation)
    ntl_gee.export_to_drive(ee, image, f"{C.iso3}_VNL_{YEARS[-1]}", nation, scale=SCALE_M)
# </solution>

# %% [markdown]
'''
<!--EN-->
---
## Limitations of this path specifically

<div style="border:1px solid #F2A900;border-radius:10px;background:#FFFDF6;
 padding:16px 20px;margin:16px 0;font-family:'Segoe UI',system-ui,sans-serif;">
<ul style="color:#33403A;font-size:14px;line-height:1.7;margin:0;padding-left:22px;">
<li><b>All the limitations of the local notebook still apply</b> — proxy status, threshold
sensitivity, gas flares, saturation, boundary choice. Earth Engine changes how you compute, not
what the light means.</li>
<li><b>Different product, different numbers.</b> EOG annual VNL is not NASA VNP46A4. Name the one
you used in every published figure.</li>
<li><b>FAO GAUL 2015 boundaries</b> are the default here and are not your official boundaries.</li>
<li><b>The reduction scale is a parameter.</b> Reducing at 1000 m instead of 500 m is four times
faster and quietly loses small settlements. Whichever you choose, record it.</li>
<li><b>getInfo() is capped at 5000 features.</b> A country with more ADM2 units than that needs
the panel built in groups, or exported to Drive as a table.</li>
<li><b>Continuity risk.</b> This result is reproducible only while Google serves the collection
under terms you can accept. For a production statistical indicator, that is a governance question
to answer before the pipeline is adopted, not after.</li>
</ul></div>

<div style="background:linear-gradient(135deg,#0B2545,#1B7A43);border-radius:16px;
 padding:22px 30px;margin-top:22px;text-align:center;font-family:'Segoe UI',system-ui,sans-serif;">
 <div style="color:#F2A900;font-size:11.5px;letter-spacing:2.5px;font-weight:700;">
  DATA SCIENCE TOOLKIT · AfDB / STATAFRIC</div>
 <div style="color:#fff;font-size:1.05em;margin-top:7px;font-weight:600;">
  STG17 workshop · Action Plan 2025-2030 · activities 4.2.1, 4.2.3 and 2.1.1</div></div>
<!--FR-->
---
## Limites propres à cette voie

<div style="border:1px solid #F2A900;border-radius:10px;background:#FFFDF6;
 padding:16px 20px;margin:16px 0;font-family:'Segoe UI',system-ui,sans-serif;">
<ul style="color:#33403A;font-size:14px;line-height:1.7;margin:0;padding-left:22px;">
<li><b>Toutes les limites du carnet local s'appliquent encore</b> — statut d'indicateur indirect,
sensibilité au seuil, torchères, saturation, choix des frontières. Earth Engine change la façon
de calculer, pas la signification de la lumière.</li>
<li><b>Produit différent, chiffres différents.</b> Le VNL annuel EOG n'est pas le VNP46A4 de la
NASA. Nommez celui que vous avez utilisé dans chaque figure publiée.</li>
<li><b>Les frontières FAO GAUL 2015</b> sont la valeur par défaut ici et ne sont pas vos
frontières officielles.</li>
<li><b>L'échelle de réduction est un paramètre.</b> Réduire à 1000 m au lieu de 500 m est quatre
fois plus rapide et perd discrètement les petites agglomérations. Quel que soit votre choix,
consignez-le.</li>
<li><b>getInfo() est plafonné à 5000 entités.</b> Un pays comptant davantage d'unités ADM2 exige
un panel construit par groupes, ou exporté vers Drive sous forme de table.</li>
<li><b>Risque de continuité.</b> Ce résultat n'est reproductible que tant que Google sert la
collection à des conditions que vous pouvez accepter. Pour un indicateur statistique de
production, c'est une question de gouvernance à trancher avant l'adoption de la chaîne, pas
après.</li>
</ul></div>

<div style="background:linear-gradient(135deg,#0B2545,#1B7A43);border-radius:16px;
 padding:22px 30px;margin-top:22px;text-align:center;font-family:'Segoe UI',system-ui,sans-serif;">
 <div style="color:#F2A900;font-size:11.5px;letter-spacing:2.5px;font-weight:700;">
  DATA SCIENCE TOOLKIT · BAD / STATAFRIC</div>
 <div style="color:#fff;font-size:1.05em;margin-top:7px;font-weight:600;">
  Atelier STG17 · Plan d'action 2025-2030 · activités 4.2.1, 4.2.3 et 2.1.1</div></div>
'''
