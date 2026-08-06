# %% [meta]
'''
id: 00_environment_check
day: 0
title_en: Environment Check - Are you ready for the workshop?
title_fr: Vérification de l'environnement - Êtes-vous prêt pour l'atelier ?
outdir: notebooks
stem: 00_Environment_Check
country: CIV
tracks: guided
'''

# %% [markdown]
'''
<!--EN-->
<div style="background:linear-gradient(135deg,#0B2545 0%,#1B7A43 100%);
 border-radius:18px;padding:32px 38px;font-family:'Segoe UI',system-ui,sans-serif;margin-bottom:6px;">
 <div style="color:#F2A900;font-size:12.5px;letter-spacing:3px;font-weight:700;
  text-transform:uppercase;">African Development Bank · AU STATAFRIC · STG17</div>
 <div style="color:#fff;font-size:2em;font-weight:800;margin:10px 0 8px;line-height:1.15;">
  Environment Check</div>
 <div style="color:#dbe7e0;font-size:1.05em;line-height:1.55;max-width:900px;">
  Run this notebook <b>before</b> the workshop opens. It takes about five minutes and tells you,
  item by item, whether your machine can run the nine laboratories of the week — and exactly what
  to do about anything that is missing.
 </div>
 <div style="color:#F2A900;font-size:13px;margin-top:14px;font-weight:600;">
  Run it once at home, once again during the remote check session at T-1 week.</div>
</div>

> **You do not need to fix everything yourself.** The last cell produces a short
> diagnostic string. Copy it and send it to the technical assistants — that is
> what the check session exists for. Arriving on Day 1 with an unchecked machine
> is the one preventable way to lose a morning.
<!--FR-->
<div style="background:linear-gradient(135deg,#0B2545 0%,#1B7A43 100%);
 border-radius:18px;padding:32px 38px;font-family:'Segoe UI',system-ui,sans-serif;margin-bottom:6px;">
 <div style="color:#F2A900;font-size:12.5px;letter-spacing:3px;font-weight:700;
  text-transform:uppercase;">Banque africaine de développement · UA STATAFRIC · STG17</div>
 <div style="color:#fff;font-size:2em;font-weight:800;margin:10px 0 8px;line-height:1.15;">
  Vérification de l'environnement</div>
 <div style="color:#dbe7e0;font-size:1.05em;line-height:1.55;max-width:900px;">
  Exécutez ce carnet <b>avant</b> l'ouverture de l'atelier. Il demande environ cinq minutes et vous
  indique, point par point, si votre machine peut faire tourner les neuf laboratoires de la semaine
  — et exactement quoi faire pour ce qui manque.
 </div>
 <div style="color:#F2A900;font-size:13px;margin-top:14px;font-weight:600;">
  À exécuter une fois chez vous, puis à nouveau lors de la séance de vérification à distance (T-1 semaine).</div>
</div>

> **Vous n'avez pas à tout réparer vous-même.** La dernière cellule produit une
> courte chaîne de diagnostic. Copiez-la et envoyez-la aux assistants techniques
> — c'est précisément l'objet de la séance de vérification. Arriver au Jour 1
> avec une machine non vérifiée est la seule façon évitable de perdre une matinée.
'''

# %% [markdown]
'''
<!--EN-->
---
## 1 · Install the workshop toolkit

Everything the laboratories need is bundled in one package, `stg17`. Installing it
also pulls the scientific stack. On Colab this takes about two minutes; locally it
depends on what you already have.

If the cell below fails, do not fight it — note the error, continue to the next
cell, and bring the message to the check session.
<!--FR-->
---
## 1 · Installer la boîte à outils de l'atelier

Tout ce dont les laboratoires ont besoin est réuni dans un seul paquet, `stg17`.
Son installation entraîne également la pile scientifique. Sur Colab cela prend
environ deux minutes ; en local, cela dépend de ce que vous possédez déjà.

Si la cellule ci-dessous échoue, n'insistez pas : notez l'erreur, passez à la
cellule suivante, et apportez le message à la séance de vérification.
'''

# %%
# EN: The workshop toolkit. Safe to re-run: pip skips what is already present. | FR: La boîte à outils de l'atelier. Ré-exécutable sans risque : pip ignore ce qui est déjà présent.
import subprocess
import sys

REPO = "https://github.com/{{ORG}}/{{REPO}}"

try:
    import stg17  # noqa: F401
    print("stg17 already installed - version", stg17.__version__)
except ImportError:
    print("Installing stg17 from", REPO)
    subprocess.run([sys.executable, "-m", "pip", "install", "-q",
                    f"stg17 @ git+{REPO}"], check=False)
    try:
        import stg17  # noqa: F401
        print("stg17 installed - version", stg17.__version__)
    except ImportError:
        # EN: Offline fallback: the USB key carries the package next to the notebooks. | FR: Repli hors ligne : la clé USB contient le paquet à côté des carnets.
        sys.path.insert(0, "..")
        import stg17  # noqa: F401
        print("stg17 loaded from the local folder - version", stg17.__version__)

# %%
# EN: One call sets the language, applies the AfDB theme and finds your data root. | FR: Un seul appel fixe la langue, applique le thème BAD et localise votre racine de données.
from stg17 import setup, countries, ui
from stg17.i18n import T

S = setup(lang="{{LANG_UPPER}}")

# %% [markdown]
'''
<!--EN-->
---
## 2 · The nine laboratories and what each one needs

Not every laboratory needs everything. The table below is the map: if you only
attend Days 3 and 4, the LLM keys do not concern you, and if your machine cannot
install `rasterio`, the Colab badge on each notebook solves it.
<!--FR-->
---
## 2 · Les neuf laboratoires et ce dont chacun a besoin

Tous les laboratoires n'ont pas besoin de tout. Le tableau ci-dessous est la
carte : si vous ne participez qu'aux Jours 3 et 4, les clés LLM ne vous
concernent pas, et si votre machine ne peut pas installer `rasterio`, le badge
Colab de chaque carnet règle le problème.
'''

# %%
# EN: What each laboratory of the week requires. | FR: Ce que requiert chaque laboratoire de la semaine.
import pandas as pd

YES, NO, OPT = T("yes", "oui"), T("no", "non"), T("optional", "optionnel")
LABS = [
    ("D1", T("RAG assistant", "Assistant RAG"),
     "sentence-transformers, faiss/chroma", "-", OPT),
    ("D1", T("From RAG to agent", "Du RAG à l'agent"),
     T("an LLM API key", "une clé API LLM"), "-", YES),
    ("D2", T("Document to dashboard", "Du document au tableau de bord"),
     T("an LLM API key, a GitHub account", "une clé API LLM, un compte GitHub"), "-", YES),
    ("D2", T("Provider benchmark", "Benchmark des fournisseurs"),
     T("Groq + one other provider", "Groq + un autre fournisseur"), "-", YES),
    ("D2", T("LLM toolkit stations", "Ateliers boîte à outils LLM"),
     T("a browser only", "un navigateur seulement"), "-", YES),
    ("D3", T("Ookla + WorldPop", "Ookla + WorldPop"),
     "geopandas, pyarrow, rasterio", "~400 MB", NO),
    ("D3", T("Elasticsearch at scale", "Elasticsearch à l'échelle"),
     T("elasticsearch client (or duckdb)", "client elasticsearch (ou duckdb)"), "-", NO),
    ("D4", T("NTL collect & explore", "NTL collecter et explorer"),
     "h5py, rasterio, rioxarray", T("~150 MB/year", "~150 Mo/an"), NO),
    ("D4", T("NTL analysis & validation", "NTL analyse et validation"),
     "rasterstats/exactextract, scipy", "-", NO),
    ("D5", T("Publish your work", "Publier vos travaux"),
     T("a GitHub account", "un compte GitHub"), "-", YES),
]
cols = {
    "en": ["Day", "Laboratory", "Needs", "Download", "Network required"],
    "fr": ["Jour", "Laboratoire", "Besoins", "Téléchargement", "Réseau requis"],
}["{{LANG}}"]
ui.result_table(pd.DataFrame(LABS, columns=cols),
                caption=T("Nothing here is a prerequisite for attending - it is a prerequisite for "
                          "running that particular laboratory on your own machine.",
                          "Rien ici n'est un prérequis pour participer - c'est un prérequis pour "
                          "exécuter ce laboratoire précis sur votre propre machine."))

# %% [markdown]
'''
<!--EN-->
---
## 3 · Your machine

Three things matter and are checked below: the Python version, the memory
available, and whether a GPU is present.

**On memory.** 16 GB is recommended. With 8 GB the Day 3 and Day 4 laboratories
still work, because every heavy step processes one tile at a time rather than
loading a country at once — but keep other applications closed.

**On the GPU.** Almost nothing in this workshop needs one. The only exception is
the fine-tuning demonstration on Day 1, which runs perfectly well on a CPU, just
slowly. If you want it fast, use Kaggle — see `docs/before/kaggle`.
<!--FR-->
---
## 3 · Votre machine

Trois éléments comptent et sont vérifiés ci-dessous : la version de Python, la
mémoire disponible, et la présence éventuelle d'un GPU.

**À propos de la mémoire.** 16 Go sont recommandés. Avec 8 Go, les laboratoires
des Jours 3 et 4 fonctionnent tout de même, car chaque étape lourde traite une
tuile à la fois plutôt que de charger un pays entier — mais fermez les autres
applications.

**À propos du GPU.** Presque rien dans cet atelier n'en a besoin. Seule exception :
la démonstration d'affinage du Jour 1, qui tourne très bien sur processeur, mais
lentement. Pour la rendre rapide, utilisez Kaggle — voir `docs/before/kaggle`.
'''

# %%
# EN: Hardware and interpreter. | FR: Matériel et interpréteur.
import platform
import shutil

from stg17 import env

rows = []

py_ok = sys.version_info >= (3, 9)
rows.append((T("Python version", "Version de Python"),
             "ok" if py_ok else "fail",
             f"{platform.python_version()} " +
             ("" if py_ok else T("- 3.9 or newer is required", "- 3.9 ou plus récent est requis"))))

rows.append((T("Operating system", "Système d'exploitation"), "ok",
             f"{platform.system()} {platform.release()} ({platform.machine()})"))

try:
    import psutil
    ram_gb = psutil.virtual_memory().total / 1e9
    status = "ok" if ram_gb >= 15 else ("warn" if ram_gb >= 7 else "fail")
    detail = f"{ram_gb:.1f} GB"
    if status == "warn":
        detail += T(" - workable, close other applications",
                    " - exploitable, fermez les autres applications")
    if status == "fail":
        detail += T(" - use the Colab badge on every notebook",
                    " - utilisez le badge Colab de chaque carnet")
except ImportError:
    status, detail = "skip", T("psutil not installed", "psutil non installé")
rows.append((T("Memory", "Mémoire"), status, detail))

free_gb = shutil.disk_usage(".").free / 1e9
rows.append((T("Free disk space", "Espace disque libre"),
             "ok" if free_gb >= 20 else "warn",
             f"{free_gb:.0f} GB " + T("(20 GB recommended for the mirrored data)",
                                      "(20 Go recommandés pour les données miroir)")))

gpu, gpu_name = env.has_gpu()
rows.append((T("GPU", "GPU"), "ok" if gpu else "skip",
             gpu_name + ("" if gpu else T(" - fine, only Day 1 fine-tuning is slower",
                                          " - sans importance, seul l'affinage du Jour 1 est plus lent"))))

rows.append((T("Platform", "Plateforme"), "ok", S.platform))
rows.append((T("Data root", "Racine des données"), "ok", str(S.root)))

ui.status_table(rows, title=T("Your machine", "Votre machine"))

# %% [markdown]
'''
<!--EN-->
---
## 4 · Python libraries

The check below imports each library rather than trusting a version list — an
installed-but-broken `rasterio` (a very common outcome on Windows) reports as
present in `pip list` and fails on import. We want the truth.

Anything marked **fail** in the *core* group needs fixing before Day 3. Anything
in the *optional* group can wait, or can be skipped entirely by using Colab.
<!--FR-->
---
## 4 · Bibliothèques Python

La vérification ci-dessous importe réellement chaque bibliothèque plutôt que de
se fier à une liste de versions : un `rasterio` installé mais cassé (issue très
fréquente sous Windows) apparaît comme présent dans `pip list` et échoue à
l'import. Nous voulons la vérité.

Tout ce qui est marqué **échec** dans le groupe *cœur* doit être corrigé avant le
Jour 3. Le groupe *optionnel* peut attendre, ou être entièrement contourné en
utilisant Colab.
'''

# %%
# EN: Import each library for real. Report version, or the exact error. | FR: Importer réellement chaque bibliothèque. Rapporter la version, ou l'erreur exacte.
import importlib

CORE = {
    "numpy": "numpy", "pandas": "pandas", "matplotlib": "matplotlib",
    "geopandas": "geopandas", "shapely": "shapely", "rasterio": "rasterio",
    "h5py": "h5py", "pyarrow": "pyarrow", "requests": "requests", "scipy": "scipy",
}
OPTIONAL = {
    "rioxarray": "rioxarray", "rasterstats": "rasterstats", "folium": "folium",
    "plotly": "plotly", "seaborn": "seaborn", "duckdb": "duckdb",
    "sentence_transformers": "sentence-transformers", "faiss": "faiss-cpu",
    "elasticsearch": "elasticsearch", "ee": "earthengine-api", "geemap": "geemap",
    "torch": "torch", "transformers": "transformers", "openai": "openai",
    "anthropic": "anthropic", "groq": "groq", "psutil": "psutil",
}


def probe(packages):
    out = []
    for import_name, pip_name in packages.items():
        try:
            module = importlib.import_module(import_name)
            version = getattr(module, "__version__", "?")
            out.append((import_name, "ok", str(version)))
        except ImportError:
            out.append((import_name, "fail", f"pip install {pip_name}"))
        except Exception as exc:
            # EN: Installed but unusable - the case a version list would hide. | FR: Installé mais inutilisable - le cas qu'une liste de versions masquerait.
            out.append((import_name, "fail", f"{type(exc).__name__}: {str(exc)[:60]}"))
    return out


core_rows = probe(CORE)
ui.status_table(core_rows, title=T("Core libraries - needed from Day 3",
                                   "Bibliothèques cœur - nécessaires dès le Jour 3"))

# %%
optional_rows = probe(OPTIONAL)
ui.status_table(
    optional_rows,
    title=T("Optional libraries - install only what your laboratories need",
            "Bibliothèques optionnelles - n'installez que ce dont vos laboratoires ont besoin"),
    note=T("Missing entries here are not a problem. Each notebook installs what it needs "
           "in its own first cell.",
           "Les absences ici ne posent pas de problème. Chaque carnet installe ce dont il a "
           "besoin dans sa propre première cellule."),
)

# %% [markdown]
'''
<!--EN-->
### Fix the core libraries in one cell

Run this only if something in the *core* group came back red. On Windows,
`geopandas` and `rasterio` occasionally refuse to install through pip; if that
happens, do not spend the evening on it — use Colab, and mention it at the check
session.
<!--FR-->
### Corriger les bibliothèques cœur en une cellule

N'exécutez ceci que si un élément du groupe *cœur* est ressorti en rouge. Sous
Windows, `geopandas` et `rasterio` refusent parfois de s'installer via pip ; si
cela arrive, n'y passez pas la soirée — utilisez Colab, et signalez-le lors de la
séance de vérification.
'''

# %%
# EN: Uncomment and run only if needed. | FR: Décommentez et exécutez uniquement si nécessaire.
missing_core = [name for name, status, _ in core_rows if status == "fail"]
if missing_core:
    print(T(f"Missing: {', '.join(missing_core)}", f"Manquant : {', '.join(missing_core)}"))
    print(T("Run this line to install them:", "Exécutez cette ligne pour les installer :"))
    print(f"    !pip install {' '.join(CORE[name] for name in missing_core)}")
    # env.pip_install([CORE[name] for name in missing_core], quiet=False)
else:
    print(T("All core libraries are importable. Nothing to do.",
            "Toutes les bibliothèques cœur sont importables. Rien à faire."))

# %% [markdown]
'''
<!--EN-->
---
## 5 · Accounts and access

Six accounts are used across the week. **None of them requires payment.** They do
require a few minutes each, which is why they are on the pre-workshop list rather
than on the Day 1 agenda.

| Account | Needed for | Where |
|---|---|---|
| **GitHub** | Days 2-5 — all outputs are published publicly | github.com/signup |
| **Google** | Colab, the fallback path for every notebook | already have one, probably |
| **Google Earth Engine** | the zero-download path for Days 3-4 | code.earthengine.google.com/register |
| **NASA Earthdata** | downloading Black Marble granules on Day 4 | urs.earthdata.nasa.gov |
| **Kaggle** | GPU for the Day 1 fine-tuning demo, and dataset mirrors | kaggle.com |
| **An LLM provider** | Days 1-2 | keys are provisioned centrally by the Secretariat |

**Never paste a key into a notebook cell.** The check below reads keys from the
Colab secret manager, the Kaggle secret manager, your environment, or a local
`.env` file — and reports only the last four characters. A key pasted into a cell
of a notebook you later push to GitHub is a key you have published.
<!--FR-->
---
## 5 · Comptes et accès

Six comptes sont utilisés durant la semaine. **Aucun n'est payant.** Chacun
demande néanmoins quelques minutes, c'est pourquoi ils figurent dans la liste
préalable plutôt qu'à l'ordre du jour du Jour 1.

| Compte | Nécessaire pour | Où |
|---|---|---|
| **GitHub** | Jours 2-5 — tous les résultats sont publiés publiquement | github.com/signup |
| **Google** | Colab, le chemin de repli de tous les carnets | vous en avez probablement déjà un |
| **Google Earth Engine** | la voie sans téléchargement des Jours 3-4 | code.earthengine.google.com/register |
| **NASA Earthdata** | télécharger les granules Black Marble au Jour 4 | urs.earthdata.nasa.gov |
| **Kaggle** | GPU pour la démo d'affinage du Jour 1, et miroirs de données | kaggle.com |
| **Un fournisseur LLM** | Jours 1-2 | les clés sont fournies par le Secrétariat |

**Ne collez jamais une clé dans une cellule.** La vérification ci-dessous lit les
clés dans le gestionnaire de secrets Colab, celui de Kaggle, votre environnement,
ou un fichier `.env` local — et n'affiche que les quatre derniers caractères. Une
clé collée dans une cellule d'un carnet que vous poussez ensuite sur GitHub est
une clé que vous avez publiée.
'''

# %%
# EN: Which keys can this machine see? Presence only - never the key itself. | FR: Quelles clés cette machine voit-elle ? Présence seulement - jamais la clé elle-même.
KEYS = ["GROQ_API_KEY", "ANTHROPIC_API_KEY", "OPENAI_API_KEY",
        "EARTHDATA_TOKEN", "HF_TOKEN"]
ui.status_table(
    env.secret_status(KEYS),
    title=T("API keys visible from this machine", "Clés API visibles depuis cette machine"),
    note=T("An amber row is not a failure. Every laboratory that uses a key also has a "
           "documented path that works without one.",
           "Une ligne orange n'est pas un échec. Chaque laboratoire utilisant une clé dispose "
           "aussi d'un chemin documenté fonctionnant sans clé."),
)

# %%
# EN: Network reachability for the services the laboratories call. | FR: Accessibilité réseau des services appelés par les laboratoires.
import socket
import urllib.request

ENDPOINTS = [
    ("GitHub", "https://github.com"),
    ("Google Colab", "https://colab.research.google.com"),
    ("geoBoundaries", "https://www.geoboundaries.org/api/current/gbOpen/CIV/ADM1/"),
    ("NASA Earthdata (CMR)", "https://cmr.earthdata.nasa.gov/search/granules.json?page_size=1"),
    ("WorldPop", "https://hub.worldpop.org"),
    ("Ookla open data (AWS)", "https://ookla-open-data.s3.amazonaws.com"),
    ("Hugging Face", "https://huggingface.co"),
]

socket.setdefaulttimeout(12)
net_rows = []
for name, url in ENDPOINTS:
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "STG17-check/1.0"})
        with urllib.request.urlopen(request, timeout=12) as response:
            net_rows.append((name, "ok", f"HTTP {response.status}"))
    except Exception as exc:
        net_rows.append((name, "warn", f"{type(exc).__name__}"))

ui.status_table(
    net_rows,
    title=T("Network reachability", "Accessibilité réseau"),
    note=T("Blocked endpoints are common on institutional networks and are NOT a blocker: "
           "all datasets are mirrored on the USB key distributed on Day 0.",
           "Les points de terminaison bloqués sont fréquents sur les réseaux institutionnels et "
           "ne sont PAS bloquants : toutes les données sont copiées sur la clé USB du Jour 0."),
)

# %% [markdown]
'''
<!--EN-->
---
## 6 · Your country

Every laboratory is parameterised by a single variable. Change the line below to
your own country and re-run — that is the entire mechanism, and it is what lets
each of the 55 African Union member states run the same pipeline on its own
territory.

The cell reports how many Black Marble tiles your country spans, which is the
best available predictor of how long Day 4 will take on your machine.
<!--FR-->
---
## 6 · Votre pays

Chaque laboratoire est paramétré par une seule variable. Remplacez la ligne
ci-dessous par votre pays et ré-exécutez — c'est tout le mécanisme, et c'est ce
qui permet à chacun des 55 États membres de l'Union africaine d'exécuter le même
pipeline sur son propre territoire.

La cellule indique combien de tuiles Black Marble couvre votre pays, ce qui est
le meilleur prédicteur disponible du temps que prendra le Jour 4 sur votre machine.
'''

# %%
COUNTRY_ISO3 = "{{ISO3}}"       # <-- EN: change this to your country | FR: remplacez par votre pays

C = countries.get(COUNTRY_ISO3)
from stg17 import ntl

print(f"{C.name('{{LANG}}')} ({C.iso3}) - {C.region_name('{{LANG}}')}")
print(T(f"  Bounding box      : {C.bbox}", f"  Emprise           : {C.bbox}"))
print(T(f"  Black Marble tiles: {' '.join(C.viirs_tiles)}  ({len(C.viirs_tiles)} tiles)",
        f"  Tuiles Black Marble : {' '.join(C.viirs_tiles)}  ({len(C.viirs_tiles)} tuiles)"))
print(T(f"  Projected CRS     : EPSG:{C.utm_epsg()} (used for areas and distances)",
        f"  SCR projeté       : EPSG:{C.utm_epsg()} (utilisé pour les aires et distances)"))
print(T(f"  WorldPop code     : {C.worldpop_code}", f"  Code WorldPop     : {C.worldpop_code}"))

mb = countries.estimate_download_mb(C, years=14, product="VNP46A4")
print(T(f"\n  Day 4 download if you collect 14 annual composites: about {mb/1000:.1f} GB.",
        f"\n  Téléchargement du Jour 4 pour 14 composites annuels : environ {mb/1000:.1f} Go."))
print(T("  The Earth Engine variant of the same laboratory downloads nothing at all.",
        "  La variante Earth Engine du même laboratoire ne télécharge rien du tout."))

# %%
# EN: Can we actually load your national boundaries? This is the real test. | FR: Peut-on réellement charger vos frontières nationales ? C'est le vrai test.
from stg17 import boundaries

try:
    adm1 = boundaries.load(C, level=1, root=S.root, allow_download=True)
    print(T(f"ADM1 loaded: {len(adm1)} units from {adm1.attrs['source_name']}",
            f"ADM1 chargé : {len(adm1)} unités depuis {adm1.attrs['source_name']}"))
    print("   ", ", ".join(sorted(adm1["ADM1"].astype(str))[:6]), "...")
    boundary_status = ("ok", f"{len(adm1)} ADM1 units")
except Exception as exc:
    print(T(f"Could not load ADM1: {exc}", f"Impossible de charger l'ADM1 : {exc}"))
    print(T("This is worth reporting at the check session - bring the message above.",
            "Cela mérite d'être signalé à la séance de vérification - apportez le message ci-dessus."))
    boundary_status = ("warn", type(exc).__name__)

# %% [markdown]
'''
<!--EN-->
---
## 7 · A first figure

If the chart below renders in the workshop colours — navy, jade, amber — then
your plotting stack is correctly configured and everything you produce this week
will carry the AfDB identity without you doing anything.
<!--FR-->
---
## 7 · Une première figure

Si le graphique ci-dessous s'affiche aux couleurs de l'atelier — bleu marine,
jade, ambre — alors votre pile graphique est correctement configurée et tout ce
que vous produirez cette semaine portera l'identité BAD sans effort de votre part.
'''

# %%
# EN: A deliberately simple figure - we are testing the toolchain, not the analysis. | FR: Une figure volontairement simple - nous testons la chaîne d'outils, pas l'analyse.
import matplotlib.pyplot as plt
import numpy as np

from stg17 import theme

years = np.arange(2012, 2026)
demo = 100 * (1.045 ** (years - 2012)) + np.sin(years) * 2

fig, ax = plt.subplots(figsize=(8, 3.2))
ax.plot(years, demo, "o-", lw=2.2, color=theme.GREEN, label=T("Illustrative index", "Indice illustratif"))
ax.fill_between(years, demo * 0.96, demo * 1.04, color=theme.GREEN, alpha=0.12)
ax.set_title(T(f"Rendering test - {C.name('en')}", f"Test de rendu - {C.name('fr')}"))
ax.set_xlabel(T("Year", "Année"))
ax.set_ylabel(T("Index (2012 = 100)", "Indice (2012 = 100)"))
ax.legend()
theme.credit(ax, T("Synthetic data - this figure measures nothing.",
                   "Données synthétiques - cette figure ne mesure rien."), lang="{{LANG}}")
plt.show()

# %% [markdown]
'''
<!--EN-->
---
## 8 · Your diagnostic string

Copy the block below and send it to the technical assistants, or paste it into
the chat during the check session. It contains no keys, no file paths from your
personal folders, and no personal data — only what is needed to help you.
<!--FR-->
---
## 8 · Votre chaîne de diagnostic

Copiez le bloc ci-dessous et envoyez-le aux assistants techniques, ou collez-le
dans le fil de discussion pendant la séance de vérification. Il ne contient
aucune clé, aucun chemin issu de vos dossiers personnels, et aucune donnée
personnelle — uniquement ce qui est nécessaire pour vous aider.
'''

# %%
# EN: Assemble a compact, shareable diagnostic. No secrets, no personal paths. | FR: Assembler un diagnostic compact et partageable. Aucun secret, aucun chemin personnel.
core_fail = [n for n, s, _ in core_rows if s == "fail"]
opt_ok = [n for n, s, _ in optional_rows if s == "ok"]
net_fail = [n for n, s, _ in net_rows if s != "ok"]
keys_ok = [n for n, s, _ in env.secret_status(KEYS) if s == "ok"]

report = f"""STG17 ENVIRONMENT CHECK
platform   : {S.platform} / {platform.system()} {platform.release()} / py{platform.python_version()}
device     : {gpu_name}
country    : {C.iso3} ({len(C.viirs_tiles)} VIIRS tiles)
boundaries : {boundary_status[0]} - {boundary_status[1]}
core missing  : {', '.join(core_fail) if core_fail else 'none'}
optional ok   : {len(opt_ok)}/{len(OPTIONAL)}
network fail  : {', '.join(net_fail) if net_fail else 'none'}
keys present  : {', '.join(keys_ok) if keys_ok else 'none'}"""

print(report)

verdict = "ok" if not core_fail else "warn"
ui.status_table(
    [(T("Ready for Days 1-2 (AI laboratories)", "Prêt pour les Jours 1-2 (laboratoires IA)"),
      "ok", T("Colab covers everything", "Colab couvre tout")),
     (T("Ready for Days 3-4 (geospatial laboratories)", "Prêt pour les Jours 3-4 (laboratoires géospatiaux)"),
      verdict,
      T("all core libraries present", "toutes les bibliothèques cœur présentes") if not core_fail
      else T(f"install: {', '.join(core_fail)}", f"à installer : {', '.join(core_fail)}")),
     (T("Ready for Day 5 (publication)", "Prêt pour le Jour 5 (publication)"),
      "ok" if "github.com" not in str(net_fail) else "warn",
      T("a GitHub account is the only requirement",
        "un compte GitHub est le seul prérequis"))],
    title=T("Verdict", "Verdict"),
)

# %% [markdown]
'''
<!--EN-->
<div style="background:linear-gradient(135deg,#0B2545,#1B7A43);border-radius:16px;
 padding:24px 30px;margin-top:20px;text-align:center;font-family:'Segoe UI',system-ui,sans-serif;">
 <div style="color:#F2A900;font-size:11.5px;letter-spacing:2.5px;font-weight:700;">
  ENVIRONMENT CHECK COMPLETE</div>
 <div style="color:#fff;font-size:1.05em;margin-top:8px;font-weight:600;line-height:1.5;">
  Send your diagnostic string to the technical assistants.<br>
  Next: read the prerequisites page and prepare your national data pack.</div>
</div>

### What to prepare next

1. **Your national data pack** — an administrative boundary file, one national
   statistical publication for the Day 2 dashboard exercise, and at least one
   official subnational indicator (GDP, population or electrification rate) for
   the Day 4 validation.
2. **Six slides on your country's experience** — what has been attempted at home
   in AI and non-traditional data, *including what did not work*. That is the more
   useful half of the exchange.
3. **A GitHub account**, if the check above did not find one.

All three are due two weeks before the workshop opens.
<!--FR-->
<div style="background:linear-gradient(135deg,#0B2545,#1B7A43);border-radius:16px;
 padding:24px 30px;margin-top:20px;text-align:center;font-family:'Segoe UI',system-ui,sans-serif;">
 <div style="color:#F2A900;font-size:11.5px;letter-spacing:2.5px;font-weight:700;">
  VÉRIFICATION TERMINÉE</div>
 <div style="color:#fff;font-size:1.05em;margin-top:8px;font-weight:600;line-height:1.5;">
  Envoyez votre chaîne de diagnostic aux assistants techniques.<br>
  Ensuite : lisez la page des prérequis et préparez votre paquet de données national.</div>
</div>

### Ce qu'il reste à préparer

1. **Votre paquet de données national** — un fichier de frontières
   administratives, une publication statistique nationale pour l'exercice de
   tableau de bord du Jour 2, et au moins un indicateur infranational officiel
   (PIB, population ou taux d'électrification) pour la validation du Jour 4.
2. **Six diapositives sur l'expérience de votre pays** — ce qui a été tenté chez
   vous en matière d'IA et de données non traditionnelles, *y compris ce qui n'a
   pas fonctionné*. C'est la moitié la plus utile de l'échange.
3. **Un compte GitHub**, si la vérification ci-dessus n'en a pas trouvé.

Ces trois éléments sont attendus deux semaines avant l'ouverture de l'atelier.
'''
