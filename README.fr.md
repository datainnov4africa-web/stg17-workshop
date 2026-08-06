<div align="center">

# Atelier STG17 — Enjeux émergents, pratiques émergentes

**Innover dans la chaîne de valeur des données** · Intelligence artificielle,
grands modèles de langage et mégadonnées pour la statistique officielle

Banque africaine de développement (Secrétariat du STG17) · Union africaine STATAFRIC
SHaSA II · Groupe technique spécialisé 17 · Plan d'action 2025-2030, PT 4.2

🇫🇷 Français · [🇬🇧 English](README.md)

[**Site**](https://stg17-africa.github.io/stg17-workshop/fr/) ·
[Prérequis](https://stg17-africa.github.io/stg17-workshop/fr/before/prerequisites/) ·
[Laboratoires](https://stg17-africa.github.io/stg17-workshop/fr/labs/) ·
[Publier vos travaux](https://stg17-africa.github.io/stg17-workshop/fr/publish/)

</div>

---

Cinq jours, 27 heures de contact, neuf laboratoires pratiques. Chaque carnet
existe en **anglais et en français**, en piste **guidée** et **ouverte**, et
s'exécute sur **n'importe lequel des 55 États membres de l'Union africaine** en
changeant une seule variable.

```python
COUNTRY_ISO3 = "CIV"   # ← changez ceci, et rien d'autre
```

## Démarrage rapide

**Participants** — lisez les
[prérequis](https://stg17-africa.github.io/stg17-workshop/fr/before/prerequisites/),
puis exécutez la vérification d'environnement :

[![Ouvrir dans Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/STG17-Africa/stg17-workshop/blob/main/notebooks/00_Environment_Check_FR.ipynb)

**Animateurs et contributeurs :**

```bash
git clone https://github.com/STG17-Africa/stg17-workshop.git
cd stg17-workshop
pip install -r requirements-dev.txt
python tools/serve.py          # régénère tout, puis prévisualise
#
# Le site est servi sous le chemin GitHub Pages, PAS à la racine :
#   English   http://127.0.0.1:8000/stg17-workshop/
#   Français  http://127.0.0.1:8000/stg17-workshop/fr/
```

## Ce que contient le dépôt

| Chemin | Ce que c'est |
|---|---|
| `config/workshop.yml` | Toutes les valeurs à figer : organisation GitHub, points d'accès, pays par défaut |
| `config/agenda.yml` | **L'agenda, sous forme de données.** Les pages jour du site en sont le rendu |
| `stg17/` | Le paquet Python partagé — registre pays, thème BAD, runtime bilingue, moteurs NTL et frontières |
| `notebooks/_masters/` | **Là où vous modifiez.** Un master bilingue par laboratoire |
| `notebooks/dayN/` | Généré : `_EN` / `_FR` × guidé / ouvert |
| `slides/decks/` | **Là où vous modifiez.** Une source de deck bilingue par session |
| `docs/` | Le site MkDocs. `page.md` est l'anglais, `page.fr.md` le français |
| `country-template/` | Le dépôt que chaque pays copie pour publier ses résultats |
| `tools/` | Les scripts de build. Tout ce qui est dérivé est régénéré par `build_all.py` |
| `prep/` | Kit animateur : calendrier de préparation, répétition à blanc, manifeste de clé USB |

## Les décisions de conception à connaître

**Une seule variable pays.** `stg17.countries` porte les 55 États membres de l'UA
avec leur emprise ; la sélection des tuiles VIIRS, la zone UTM, l'emprise
cartographique et les codes WorldPop sont *calculés*, non tabulés. Un fichier de
frontières est résolu depuis le miroir local, puis geoBoundaries, puis un fichier
apporté par le participant — normalisé vers les mêmes noms de colonnes quelle que
soit la source, de sorte que le code d'analyse ne contient aucune condition.

**Rien n'est écrit deux fois.** Un laboratoire est un master bilingue ; le build
produit quatre carnets. Une session est une source de deck ; le build produit deux
présentations. L'agenda est un fichier YAML ; le build produit dix pages. La CI
échoue si un fichier généré s'écarte de sa source — c'est ce qui empêche le
matériel français de prendre discrètement un mois de retard sur l'anglais.

**Chaque laboratoire dispose d'un repli qui fonctionne réellement.** Extraits pays
pré-découpés sur clé USB, variante Earth Engine qui ne télécharge rien, DuckDB
quand le cluster Elasticsearch est injoignable, et un pays de référence préparé de
bout en bout. La bande passante est la cause d'échec la plus fréquente, et le
matériel est bâti sur ce constat plutôt que sur l'espoir du contraire.

**La déclaration de limites est un livrable.** Un indicateur indirect publié sans
exposé honnête de ce qu'il ne peut pas soutenir n'est pas un produit statistique.
Le Jour 4 transforme cette déclaration en document formel, validé contre les
propres chiffres infranationaux officiels du participant.

## Modifier

| Pour changer | Modifiez | Puis exécutez |
|---|---|---|
| Un laboratoire | `notebooks/_masters/<id>.master.py` | `python tools/build_notebooks.py` |
| Une session, son horaire, son rattachement au Plan d'action | `config/agenda.yml` | `python tools/build_site.py` |
| Une présentation | `slides/decks/<id>.deck.html` | `python tools/build_slides.py` |
| La palette BAD | `stg17/theme.py` | `python -m stg17.theme --emit-css` |
| Le vocabulaire partagé | `stg17/i18n.py` | `python tools/build_site.py` |
| L'organisation GitHub, les points d'accès, les dates | `config/workshop.yml` | `python tools/build_all.py` |

Ne modifiez jamais un fichier sous `notebooks/dayN/` ou `docs/dayN/` — ils sont
générés, et la CI vous le signalera.

### Le format des masters de carnets

```python
# %% [meta]
'''
id: d4_ntl_collect_explore
day: 4
outdir: notebooks/day4
stem: D4_NTL_Collect_Explore
tracks: guided, open
'''

# %% [markdown]
'''
<!--EN-->
## Step 3 — Read a real granule
<!--FR-->
## Étape 3 — Lire un granule réel
'''

# %%
# EN: Read the layer and scale it | FR: Lire la couche et la mettre à l'échelle
# <solution hint="Read one granule" hint_fr="Lisez un granule">
radiance, meta = ntl.read_layer(path)
# </solution>
```

Les cellules markdown portent les deux langues. Les cellules de code sont
identiques octet pour octet entre les langues — seuls les commentaires diffèrent,
et tout ce qui est affiché passe par `stg17.i18n.T()`, résolu à l'exécution. Les
blocs de solution sont ce que la piste ouverte retire.

## État d'avancement

| Phase | Contenu | État |
|---|---|---|
| **0 · Socle** | Dépôt, design system, registre pays, moteur de build, site bilingue, vérification d'environnement, laboratoire pilote (Jour 4 NTL, + variante Earth Engine), présentation pilote, prérequis, gabarit pays, CI | ✅ Terminé |
| 1 · Jour 1 | Laboratoires RAG et agent, présentations 01-02 | ⏳ |
| 2 · Jour 2 | Tableau de bord, benchmark fournisseurs, ateliers boîte à outils, présentations 03-05 | ⏳ |
| 3 · Jour 3 | Ookla + WorldPop, Elasticsearch, exploration par recherche, présentations 06-07 | ⏳ |
| 4 · Jour 4 | Analyse et validation NTL | ⏳ |
| 5 · Jour 5 | Laboratoire de publication, présentations 09-12, kit animateur | ⏳ |

## Licence

Code MIT · contenus CC BY 4.0. Les données tierces conservent leur propre licence
— voir [licences et éthique](https://stg17-africa.github.io/stg17-workshop/fr/resources/licensing/).

> ⚠️ Les produits dérivés des données ouvertes Ookla héritent de la
> **CC BY-NC-SA 4.0**. Le « pas d'usage commercial » et le « partage dans les
> mêmes conditions » se propagent, ce qui signifie qu'un tel produit ne peut pas
> être diffusé sous la plupart des politiques nationales de données ouvertes. Ce
> point est traité comme un sujet à part entière dans le laboratoire du Jour 3 et
> dans le guide de publication.

Ni la Banque africaine de développement ni l'UA STATAFRIC ne prennent position sur
une quelconque délimitation frontalière figurant dans ce dépôt ou dans les dépôts
pays qui en dérivent.
