<!-- GÉNÉRÉ depuis config/agenda.yml par tools/build_site.py. Ne pas modifier. -->

# Les laboratoires

12 laboratoires portent la semaine. Chacun est décrit ci-dessous avec l'environnement qu'il exige, la production que l'équipe doit livrer, et le chemin de repli appliqué quand quelque chose casse — ce qui arrivera.

Les supports et le carnet d'un laboratoire ne sont pas sur cette page : ils sont sur la page du jour, à côté de la séance qui le porte. Chaque laboratoire ci-dessous y renvoie.

## Jour 1

### Assistant RAG

:material-calendar-clock: **Jour 1 · 14h30–15h30** &nbsp;·&nbsp; [voir la séance](../day1/index.md#14h3015h30-atelier-partie-1-generation-augmentee-par-recuperation-rag)

**Environnement et données** — Python dans Colab, Kaggle ou en local ; scikit-learn pour le récupérateur par mots, sans téléchargement ; sentence-transformers en option pour le récupérateur sémantique ; pas de base vectorielle — le corpus est trop petit pour la justifier

**Ce que produit l’équipe** — Un relevé de réponses avec les passages exacts qui les fondent, et une évaluation de la récupération séparant les échecs de récupération des échecs de génération

**En cas de panne** — Un corpus fictif de cinq documents est fourni avec la boîte à outils, donc aucune équipe n'est bloquée par des publications non validées ; sans aucun fournisseur de modèle, la moitié « récupération » du laboratoire fonctionne quand même — et c'est là que sont la plupart des problèmes du RAG

### Du RAG à l'agent

:material-calendar-clock: **Jour 1 · 15h30–16h45** &nbsp;·&nbsp; [voir la séance](../day1/index.md#15h3016h45-atelier-partie-2-du-rag-a-lagent)

**Environnement et données** — Même environnement que le laboratoire RAG ; quatre outils — récupération, liste de documents, calculatrice protégée et un outil qui écrit sur disque. Un protocole textuel JSON plutôt que l'appel de fonctions natif, pour que l'interstice demande-exécution reste visible et que l'exercice tourne sur tout fournisseur, y compris un modèle local

**Ce que produit l’équipe** — Un journal d'audit consignant chaque outil demandé par le modèle, son autorisation par la politique, et la réponse brute derrière chaque demande — plus la note écrite par l'agent une fois une politique l'y autorisant

**En cas de panne** — Un modèle scripté rejoue des réponses fixes : la boucle, le point d'approbation, la reprise sur erreur et le journal d'audit s'exercent donc sans clé API. C'est délibéré et non un chemin de repli — ces quatre éléments sont ce qu'un office écrit et possède ; le modèle est ce qu'il loue

## Jour 2

### Du document au tableau de bord

:material-calendar-clock: **Jour 2 · 10h45–12h30** &nbsp;·&nbsp; [voir la séance](../day2/index.md#10h4512h30-atelier-du-document-statistique-au-tableau-de-bord-public)

**Environnement et données** — API LLM ; Python ou simple HTML/JS ; la publication nationale du participant ; GitHub Pages

**Ce que produit l’équipe** — Une URL publique de tableau de bord et le tableau de vérification comparant l'extraction à la source

**En cas de panne** — Une publication d'exemple et un gabarit statique de tableau de bord sont fournis ; la publication peut se faire à partir du seul gabarit

### Benchmark des fournisseurs

:material-calendar-clock: **Jour 2 · 14h45–15h30** &nbsp;·&nbsp; [voir la séance](../day2/index.md#14h4515h30-choisir-son-moteur-vitesse-cout-et-souverainete-travailler-avec-groq)

**Environnement et données** — Deux points d'accès API dont Groq ; une feuille de calcul partagée

**Ce que produit l’équipe** — Trois lignes dans la feuille de comparaison partagée : latence, coût pour mille documents, score de qualité

**En cas de panne** — L'animateur exécute le benchmark en direct depuis le pupitre si les clés des participants échouent

### Ateliers boîte à outils

:material-calendar-clock: **Jour 2 · 15h30–16h45** &nbsp;·&nbsp; en ateliers tournants &nbsp;·&nbsp; [voir la séance](../day2/index.md#15h3016h45-atelier-une-boite-a-outils-llm-pour-statisticiens)

**Environnement et données** — Variable selon l'atelier ; tous accessibles depuis un navigateur

**Ce que produit l’équipe** — Deux productions achevées par participant, une de chaque atelier choisi

**En cas de panne** — Les ateliers sont indépendants — un atelier en panne ne coûte que lui-même

## Jour 3

### Ookla et WorldPop

:material-calendar-clock: **Jour 3 · 10h45–12h30** &nbsp;·&nbsp; en équipes &nbsp;·&nbsp; [voir la séance](../day3/index.md#10h4512h30-atelier-donnees-ouvertes-ookla-speedtest-et-worldpop)

**Environnement et données** — Python avec geopandas et pyarrow ; tuiles parquet Ookla et rasters WorldPop en miroir local ; frontières administratives nationales

**Ce que produit l’équipe** — Un indicateur de débit descendant et de latence pondéré par la population, par région administrative de premier niveau, une carte et une série trimestrielle

**En cas de panne** — Des extraits pays pré-découpés sont préparés à l'avance pour chaque pays participant

### Elasticsearch

:material-calendar-clock: **Jour 3 · 14h45–15h30** &nbsp;·&nbsp; en équipes &nbsp;·&nbsp; [voir la séance](../day3/index.md#14h4515h30-atelier-partie-1-ookla-a-lechelle-avec-elasticsearch)

**Environnement et données** — Cluster pré-provisionné et pré-chargé, un index par pays, Kibana disponible

**Ce que produit l’équipe** — Cinq requêtes enregistrées et une comparaison de temps avec l'approche pandas du matin

**En cas de panne** — Si le cluster est injoignable, le même exercice tourne en local sous DuckDB avec un jeu de requêtes identique

### Exploration pilotée par la recherche

:material-calendar-clock: **Jour 3 · 15h30–16h45** &nbsp;·&nbsp; en équipes &nbsp;·&nbsp; [voir la séance](../day3/index.md#15h3016h45-atelier-partie-2-exploration-pilotee-par-la-recherche)

**Environnement et données** — Le même cluster, ou le repli DuckDB

**Ce que produit l’équipe** — Une exploration de la connectivité par région et trimestre pilotée par la recherche, avec la conclusion sur les temps

**En cas de panne** — Le jeu de requêtes identique tourne sous DuckDB sur les mêmes fichiers parquet

## Jour 4

### NTL collecter et explorer

:material-calendar-clock: **Jour 4 · 09h30–10h30** &nbsp;·&nbsp; en équipes &nbsp;·&nbsp; [voir la séance](../day4/index.md#09h3010h30-atelier-partie-1-collecter)

**Environnement et données** — Python avec rasterio et h5py ; sous-ensembles VIIRS mensuels et annuels en miroir local ; compte Earth Engine optionnel

**Ce que produit l’équipe** — Un sous-ensemble raster national documenté et un inventaire des artefacts présents dans ce pays

**En cas de panne** — Des sous-ensembles nationaux pré-découpés sont préparés pour chaque pays participant ; la variante Earth Engine ne télécharge rien

### NTL explorer et comprendre

:material-calendar-clock: **Jour 4 · 10h45–12h30** &nbsp;·&nbsp; en équipes &nbsp;·&nbsp; [voir la séance](../day4/index.md#10h4512h30-atelier-partie-2-explorer-et-comprendre)

**Environnement et données** — Même carnet que la partie 1 — étapes 7 et 8

**Ce que produit l’équipe** — L'inventaire des artefacts de votre pays, avec les preuves

**En cas de panne** — Le pays de référence (Côte d'Ivoire) est préparé de bout en bout

### NTL analyse et validation

:material-calendar-clock: **Jour 4 · 14h00–16h45** &nbsp;·&nbsp; en équipes &nbsp;·&nbsp; [voir la séance](../day4/index.md#14h0016h45-atelier-partie-3-analyse-et-validation-ntl)

**Environnement et données** — rasterstats ou exactextract ; le panel produit le matin ; l'indicateur infranational officiel apporté par l'équipe

**Ce que produit l’équipe** — Tableau de statistiques zonales, séries temporelles, détection de changement entre deux périodes et les cartes ; corrélation avec l'indicateur officiel, et une déclaration écrite des limites

**En cas de panne** — Un pays de référence est préparé de bout en bout et remis à toute équipe dont les données nationales s'avèrent incomplètes, avec un indicateur officiel de référence fourni pour ce pays

## Jour 5

### Publier vos travaux

:material-calendar-clock: **Jour 5 · 09h00–10h30** &nbsp;·&nbsp; en équipes &nbsp;·&nbsp; [voir la séance](../day5/index.md#09h0010h30-aider-les-pays-a-publier-leurs-travaux)

**Environnement et données** — Un compte GitHub et le dépôt country-template

**Ce que produit l’équipe** — Un dépôt pays public avec README, licence, métadonnées, site GitHub Pages et fichier de citation

**En cas de panne** — Le gabarit peut être publié tel quel et rempli ensuite

