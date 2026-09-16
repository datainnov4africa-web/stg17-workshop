<!-- GÉNÉRÉ depuis config/agenda.yml par tools/build_site.py. Ne pas modifier. -->

# Les laboratoires

13 laboratoires portent la semaine. Chacun est spécifié ci-dessous avec l'environnement qu'il exige, la production que l'équipe doit livrer, et le chemin de repli appliqué par l'équipe d'animation quand quelque chose casse — ce qui arrivera.

!!! tip "Deux pistes dans chaque laboratoire"

    Les participants arrivent avec des niveaux très différents. Chaque carnet existe donc en deux versions : une version **guidée**, où les étapes analytiques sont écrites et où le participant comble les trous, et une version **ouverte**, ne contenant que l'objectif et les données. Les équipes choisissent au début de chaque laboratoire et peuvent basculer. Le livrable est identique dans les deux cas, ce qui garde les présentations du vendredi comparables.

## Jour 1

### Assistant RAG

| | |
|---|---|
| **Équipe** | binômes |
| **Pays par défaut** | `CIV` — changez `COUNTRY_ISO3` pour le vôtre |
| **Environnement et données** | Python dans Colab, Kaggle ou en local ; scikit-learn pour le récupérateur par mots, sans téléchargement ; sentence-transformers en option pour le récupérateur sémantique ; pas de base vectorielle — le corpus est trop petit pour la justifier |
| **Livrable de l’équipe** | Un relevé de réponses avec les passages exacts qui les fondent, et une évaluation de la récupération séparant les échecs de récupération des échecs de génération |
| **Repli** | Un corpus fictif de cinq documents est fourni avec la boîte à outils, donc aucune équipe n'est bloquée par des publications non validées ; sans aucun fournisseur de modèle, la moitié « récupération » du laboratoire fonctionne quand même — et c'est là que sont la plupart des problèmes du RAG |
| **Variante Earth Engine** | — |
| **Statut** | :material-check-circle:{ .ok } Disponible |

[![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/STG17-Africa/stg17-workshop/blob/main/notebooks/day1/D1_RAG_Assistant_FR.ipynb) **guidée** &nbsp; [:material-github:](https://github.com/STG17-Africa/stg17-workshop/blob/main/notebooks/day1/D1_RAG_Assistant_FR.ipynb)

[![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/STG17-Africa/stg17-workshop/blob/main/notebooks/day1/D1_RAG_Assistant_FR_open.ipynb) **ouverte** &nbsp; [:material-github:](https://github.com/STG17-Africa/stg17-workshop/blob/main/notebooks/day1/D1_RAG_Assistant_FR_open.ipynb)

### Du RAG à l'agent

| | |
|---|---|
| **Équipe** | binômes |
| **Pays par défaut** | `CIV` — changez `COUNTRY_ISO3` pour le vôtre |
| **Environnement et données** | Même environnement que le laboratoire RAG ; quatre outils — récupération, liste de documents, calculatrice protégée et un outil qui écrit sur disque. Un protocole textuel JSON plutôt que l'appel de fonctions natif, pour que l'interstice demande-exécution reste visible et que l'exercice tourne sur tout fournisseur, y compris un modèle local |
| **Livrable de l’équipe** | Un journal d'audit consignant chaque outil demandé par le modèle, son autorisation par la politique, et la réponse brute derrière chaque demande — plus la note écrite par l'agent une fois une politique l'y autorisant |
| **Repli** | Un modèle scripté rejoue des réponses fixes : la boucle, le point d'approbation, la reprise sur erreur et le journal d'audit s'exercent donc sans clé API. C'est délibéré et non un chemin de repli — ces quatre éléments sont ce qu'un office écrit et possède ; le modèle est ce qu'il loue |
| **Variante Earth Engine** | — |
| **Statut** | :material-check-circle:{ .ok } Disponible |

[![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/STG17-Africa/stg17-workshop/blob/main/notebooks/day1/D1_Agent_FR.ipynb) **guidée** &nbsp; [:material-github:](https://github.com/STG17-Africa/stg17-workshop/blob/main/notebooks/day1/D1_Agent_FR.ipynb)

[![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/STG17-Africa/stg17-workshop/blob/main/notebooks/day1/D1_Agent_FR_open.ipynb) **ouverte** &nbsp; [:material-github:](https://github.com/STG17-Africa/stg17-workshop/blob/main/notebooks/day1/D1_Agent_FR_open.ipynb)

## Jour 2

### Du document au tableau de bord

| | |
|---|---|
| **Équipe** | individuel |
| **Pays par défaut** | `CIV` — changez `COUNTRY_ISO3` pour le vôtre |
| **Environnement et données** | API LLM ; Python ou simple HTML/JS ; la publication nationale du participant ; GitHub Pages |
| **Livrable de l’équipe** | Une URL publique de tableau de bord et le tableau de vérification comparant l'extraction à la source |
| **Repli** | Une publication d'exemple et un gabarit statique de tableau de bord sont fournis ; la publication peut se faire à partir du seul gabarit |
| **Variante Earth Engine** | — |
| **Statut** | :material-progress-clock: Lot Jour 2 |

### Benchmark des fournisseurs

| | |
|---|---|
| **Équipe** | individuel |
| **Pays par défaut** | `CIV` — changez `COUNTRY_ISO3` pour le vôtre |
| **Environnement et données** | Deux points d'accès API dont Groq ; une feuille de calcul partagée |
| **Livrable de l’équipe** | Trois lignes dans la feuille de comparaison partagée : latence, coût pour mille documents, score de qualité |
| **Repli** | L'animateur exécute le benchmark en direct depuis le pupitre si les clés des participants échouent |
| **Variante Earth Engine** | — |
| **Statut** | :material-progress-clock: Lot Jour 2 |

### Ateliers boîte à outils

| | |
|---|---|
| **Équipe** | ateliers tournants |
| **Pays par défaut** | `CIV` — changez `COUNTRY_ISO3` pour le vôtre |
| **Environnement et données** | Variable selon l'atelier ; tous accessibles depuis un navigateur |
| **Livrable de l’équipe** | Deux productions achevées par participant, une de chaque atelier choisi |
| **Repli** | Les ateliers sont indépendants — un atelier en panne ne coûte que lui-même |
| **Variante Earth Engine** | — |
| **Statut** | :material-progress-clock: Lot Jour 2 |

## Jour 3

### Ookla et WorldPop

| | |
|---|---|
| **Équipe** | équipes |
| **Pays par défaut** | `TUN` — changez `COUNTRY_ISO3` pour le vôtre |
| **Environnement et données** | Python avec geopandas et pyarrow ; tuiles parquet Ookla et rasters WorldPop en miroir local ; frontières administratives nationales |
| **Livrable de l’équipe** | Un indicateur de débit descendant et de latence pondéré par la population, par région administrative de premier niveau, une carte et une série trimestrielle |
| **Repli** | Des extraits pays pré-découpés sont préparés à l'avance pour chaque pays participant |
| **Variante Earth Engine** | oui — aucun téléchargement |
| **Statut** | :material-progress-clock: Lot Jour 3 |

### Elasticsearch

| | |
|---|---|
| **Équipe** | équipes |
| **Pays par défaut** | `TUN` — changez `COUNTRY_ISO3` pour le vôtre |
| **Environnement et données** | Cluster pré-provisionné et pré-chargé, un index par pays, Kibana disponible |
| **Livrable de l’équipe** | Cinq requêtes enregistrées et une comparaison de temps avec l'approche pandas du matin |
| **Repli** | Si le cluster est injoignable, le même exercice tourne en local sous DuckDB avec un jeu de requêtes identique |
| **Variante Earth Engine** | — |
| **Statut** | :material-progress-clock: Lot Jour 3 |

### Exploration pilotée par la recherche

| | |
|---|---|
| **Équipe** | équipes |
| **Pays par défaut** | `TUN` — changez `COUNTRY_ISO3` pour le vôtre |
| **Environnement et données** | Le même cluster, ou le repli DuckDB |
| **Livrable de l’équipe** | Une exploration de la connectivité par région et trimestre pilotée par la recherche, avec la conclusion sur les temps |
| **Repli** | Le jeu de requêtes identique tourne sous DuckDB sur les mêmes fichiers parquet |
| **Variante Earth Engine** | — |
| **Statut** | :material-progress-clock: Lot Jour 3 |

## Jour 4

### NTL collecter et explorer

| | |
|---|---|
| **Équipe** | équipes |
| **Pays par défaut** | `CIV` — changez `COUNTRY_ISO3` pour le vôtre |
| **Environnement et données** | Python avec rasterio et h5py ; sous-ensembles VIIRS mensuels et annuels en miroir local ; compte Earth Engine optionnel |
| **Livrable de l’équipe** | Un sous-ensemble raster national documenté et un inventaire des artefacts présents dans ce pays |
| **Repli** | Des sous-ensembles nationaux pré-découpés sont préparés pour chaque pays participant ; la variante Earth Engine ne télécharge rien |
| **Variante Earth Engine** | oui — aucun téléchargement |
| **Statut** | :material-check-circle:{ .ok } Disponible |

[![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/STG17-Africa/stg17-workshop/blob/main/notebooks/day4/D4_NTL_Collect_Explore_FR.ipynb) **guidée** &nbsp; [:material-github:](https://github.com/STG17-Africa/stg17-workshop/blob/main/notebooks/day4/D4_NTL_Collect_Explore_FR.ipynb)

[![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/STG17-Africa/stg17-workshop/blob/main/notebooks/day4/D4_NTL_Collect_Explore_FR_open.ipynb) **ouverte** &nbsp; [:material-github:](https://github.com/STG17-Africa/stg17-workshop/blob/main/notebooks/day4/D4_NTL_Collect_Explore_FR_open.ipynb)

[![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/STG17-Africa/stg17-workshop/blob/main/notebooks/day4/D4_NTL_GEE_FR.ipynb) **variante Earth Engine** &nbsp; [:material-github:](https://github.com/STG17-Africa/stg17-workshop/blob/main/notebooks/day4/D4_NTL_GEE_FR.ipynb)

### NTL explorer et comprendre

| | |
|---|---|
| **Équipe** | équipes |
| **Pays par défaut** | `CIV` — changez `COUNTRY_ISO3` pour le vôtre |
| **Environnement et données** | Même carnet que la partie 1 — étapes 7 et 8 |
| **Livrable de l’équipe** | L'inventaire des artefacts de votre pays, avec les preuves |
| **Repli** | Le pays de référence (Côte d'Ivoire) est préparé de bout en bout |
| **Variante Earth Engine** | oui — aucun téléchargement |
| **Statut** | :material-check-circle:{ .ok } Disponible |

[![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/STG17-Africa/stg17-workshop/blob/main/notebooks/day4/D4_NTL_Collect_Explore_FR.ipynb) **guidée** &nbsp; [:material-github:](https://github.com/STG17-Africa/stg17-workshop/blob/main/notebooks/day4/D4_NTL_Collect_Explore_FR.ipynb)

[![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/STG17-Africa/stg17-workshop/blob/main/notebooks/day4/D4_NTL_Collect_Explore_FR_open.ipynb) **ouverte** &nbsp; [:material-github:](https://github.com/STG17-Africa/stg17-workshop/blob/main/notebooks/day4/D4_NTL_Collect_Explore_FR_open.ipynb)

[![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/STG17-Africa/stg17-workshop/blob/main/notebooks/day4/D4_NTL_GEE_FR.ipynb) **variante Earth Engine** &nbsp; [:material-github:](https://github.com/STG17-Africa/stg17-workshop/blob/main/notebooks/day4/D4_NTL_GEE_FR.ipynb)

### NTL analyse

| | |
|---|---|
| **Équipe** | équipes |
| **Pays par défaut** | `CIV` — changez `COUNTRY_ISO3` pour le vôtre |
| **Environnement et données** | rasterstats ou exactextract ; le panel produit le matin |
| **Livrable de l’équipe** | Tableau de statistiques zonales, séries temporelles, détection de changement entre deux périodes, et les cartes |
| **Repli** | Un pays de référence est préparé de bout en bout et remis à toute équipe dont les données nationales s'avèrent incomplètes |
| **Variante Earth Engine** | oui — aucun téléchargement |
| **Statut** | :material-progress-clock: Lot Jour 4 |

### NTL validation

| | |
|---|---|
| **Équipe** | équipes |
| **Pays par défaut** | `CIV` — changez `COUNTRY_ISO3` pour le vôtre |
| **Environnement et données** | L'indicateur infranational officiel apporté par l'équipe |
| **Livrable de l’équipe** | Corrélation avec l'indicateur officiel, et une déclaration écrite des limites |
| **Repli** | Un indicateur officiel de référence est fourni pour le pays de référence |
| **Variante Earth Engine** | — |
| **Statut** | :material-progress-clock: Lot Jour 4 |

## Jour 5

### Publier vos travaux

| | |
|---|---|
| **Équipe** | équipes |
| **Pays par défaut** | `CIV` — changez `COUNTRY_ISO3` pour le vôtre |
| **Environnement et données** | Un compte GitHub et le dépôt country-template |
| **Livrable de l’équipe** | Un dépôt pays public avec README, licence, métadonnées, site GitHub Pages et fichier de citation |
| **Repli** | Le gabarit peut être publié tel quel et rempli ensuite |
| **Variante Earth Engine** | — |
| **Statut** | :material-progress-clock: Lot Jour 5 |

