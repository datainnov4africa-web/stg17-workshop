<div align="center">

# Atelier STG17 — Enjeux émergents, pratiques émergentes

**Innover dans la chaîne de valeur des données** · Intelligence artificielle,
grands modèles de langage et mégadonnées pour la statistique officielle

Banque africaine de développement (Secrétariat du STG17) · Union africaine STATAFRIC
SHaSA II · Groupe technique spécialisé 17 · Plan d'action 2025-2030, PT 4.2

🇫🇷 Français · [🇬🇧 English](README.md)

[**Site**](https://datainnov4africa-web.github.io/stg17-workshop/fr/) ·
[Prérequis](https://datainnov4africa-web.github.io/stg17-workshop/fr/before/prerequisites/) ·
[Laboratoires](https://datainnov4africa-web.github.io/stg17-workshop/fr/labs/) ·
[Publier vos travaux](https://datainnov4africa-web.github.io/stg17-workshop/fr/publish/)

</div>

---

Cinq jours, 27 heures de contact, treize laboratoires pratiques. Chaque
présentation et chaque carnet sont fournis en **anglais et en français**. Le
registre des pays couvre **les 55 États membres de l'Union africaine** : à partir
d'un code ISO3, `stg17.countries` résout l'emprise géographique, la zone UTM, les
tuiles satellitaires et les codes WorldPop — calculés plutôt que tabulés.

## Démarrage rapide

**Participants** — lisez les
[prérequis](https://datainnov4africa-web.github.io/stg17-workshop/fr/before/prerequisites/),
puis faites la
[vérification d'environnement](https://datainnov4africa-web.github.io/stg17-workshop/fr/before/environment-check/).
Le carnet est distribué avec le matériel de l'atelier : votre animateur vous en
envoie le lien.

**Animateurs et contributeurs :**

```bash
git clone https://github.com/datainnov4africa-web/stg17-workshop.git
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
| `docs/downloads/DayN/` | **Là où vous déposez** une présentation ou un carnet. Voir `maintainer/HOW-TO-ADD-FILES.txt` |
| `docs/` | Le site MkDocs. `page.md` est l'anglais, `page.fr.md` le français |
| `country-template/` | Le dépôt que chaque pays copie pour publier ses résultats |
| `tools/` | Les scripts de build. Tout ce qui est dérivé est régénéré par `build_all.py` |
| `maintainer/` | Non publié : gabarits de noms, kit animateur, répétition à blanc |

## Les décisions de conception à connaître

**Une seule variable pays.** `stg17.countries` porte les 55 États membres de l'UA
avec leur emprise ; la sélection des tuiles VIIRS, la zone UTM, l'emprise
cartographique et les codes WorldPop sont *calculés*, non tabulés. Un fichier de
frontières est résolu depuis le miroir local, puis geoBoundaries, puis un fichier
apporté par le participant — normalisé vers les mêmes noms de colonnes quelle que
soit la source, de sorte que le code d'analyse ne contient aucune condition.

**Rien n'est écrit deux fois.** L'agenda est un fichier YAML, et le build en tire
toutes les pages de jour, le registre des laboratoires et la vue de la semaine,
dans les deux langues. La CI échoue si une page générée s'écarte de sa source —
c'est ce qui empêche le matériel français de prendre discrètement un mois de
retard sur l'anglais. Les présentations et les carnets, eux, ne sont pas générés
du tout : ils sont fournis, et le build n'affiche de bouton que pour les fichiers
réellement présents.

**Chaque laboratoire dispose d'un repli qui fonctionne réellement.** Extraits pays
pré-découpés préparés à l'avance, variante Earth Engine qui ne télécharge rien, DuckDB
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
| Une session, son horaire, son rattachement au Plan d'action | `config/agenda.yml` | `python tools/build_site.py` |
| Une présentation ou un carnet | déposez le fichier dans `docs/downloads/DayN/` | `python tools/build_site.py` |
| La palette BAD | `stg17/theme.py` | `python -m stg17.theme --emit-css` |
| Le vocabulaire partagé | `stg17/i18n.py` | `python tools/build_site.py` |
| L'organisation GitHub, les points d'accès, les dates | `config/workshop.yml` | `python tools/build_all.py` |

Ne modifiez jamais un fichier sous `docs/dayN/` — il est généré depuis
`config/agenda.yml`, et la CI vous le signalera.

Les présentations et les carnets ne sont pas générés ici : ils sont tous
fournis. Déposez le fichier dans `docs/downloads/DayN/` sous le nom que lui donne
le gabarit correspondant dans `maintainer/placeholders/DayN/`, puis lancez
`python tools/build_site.py`. La règle complète est dans
`maintainer/HOW-TO-ADD-FILES.txt`.

## État d'avancement

| Phase | Contenu | État |
|---|---|---|
| **0 · Socle** | Dépôt, design system, registre pays, moteur de build, site bilingue, vérification d'environnement, prérequis, gabarit pays, CI | ✅ Terminé |
| 1 · Jour 1 | Laboratoires RAG et agent | ⏳ |
| 2 · Jour 2 | Tableau de bord, benchmark fournisseurs, ateliers boîte à outils | ⏳ |
| 3 · Jour 3 | Ookla + WorldPop, Elasticsearch, exploration par recherche | ⏳ |
| 4 · Jour 4 | Analyse et validation NTL | ⏳ |
| 5 · Jour 5 | Laboratoire de publication, kit animateur | ⏳ |

Les présentations et les carnets sont fournis par séance, non par phase — ce qui
est déjà en place s'obtient avec `python tools/downloads.py`.

## Licence

Code MIT · contenus CC BY 4.0. Les données tierces conservent leur propre licence
— voir [licences et éthique](https://datainnov4africa-web.github.io/stg17-workshop/fr/resources/licensing/).

> ⚠️ Les produits dérivés des données ouvertes Ookla héritent de la
> **CC BY-NC-SA 4.0**. Le « pas d'usage commercial » et le « partage dans les
> mêmes conditions » se propagent, ce qui signifie qu'un tel produit ne peut pas
> être diffusé sous la plupart des politiques nationales de données ouvertes. Ce
> point est traité comme un sujet à part entière dans le laboratoire du Jour 3 et
> dans le guide de publication.

Ni la Banque africaine de développement ni l'UA STATAFRIC ne prennent position sur
une quelconque délimitation frontalière figurant dans ce dépôt ou dans les dépôts
pays qui en dérivent.
