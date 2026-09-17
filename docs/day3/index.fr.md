<!-- GÉNÉRÉ depuis config/agenda.yml par tools/build_site.py. Ne pas modifier. -->

# Jour 3 — Au-delà de l'enquête : données non traditionnelles et technologies qui les traitent

*Mercredi · Une nouvelle matière première pour la statistique officielle — et les moteurs qui la rendent exploitable à l'échelle*

## Matinée · 09h00 – 12h30

### 09h00–10h30 &nbsp;·&nbsp; Sources de données non traditionnelles : le trésor caché

:material-presentation-play: **Exposé + laboratoire** &nbsp;·&nbsp; Plan d’action 2.1.1 · 3.1 · 4.3

Taxonomie des sources non traditionnelles — imagerie satellitaire, mesure participative, données de caisse et de transaction, moissonnage web, capteurs et IdO, données produites par les citoyens. Cadres de qualité et biais de couverture des sources non probabilistes ; modèles d'accès et de partenariat avec les détenteurs privés ; éthique et confidentialité.


!!! quote "10h30–10h45 — Pause café"

### 10h45–12h30 &nbsp;·&nbsp; Atelier — Données ouvertes Ookla Speedtest et WorldPop

:material-flask: **Laboratoire** &nbsp;·&nbsp; Plan d’action 2.1.1 · 3.1

Ookla : tuiles de performance au zoom 16 en Mercator web (environ 611 m à l'équateur), trimestrielles depuis le T1 2019 ; champs clés (quadkey, avg_d_kbps, avg_lat_ms, tests, devices) ; licence CC BY-NC-SA 4.0 et ses conséquences pour la publication par un INS ; vérifier la couverture nationale avant de concevoir tout indicateur. WorldPop : rasters de population maillés servant à pondérer et normaliser. Les équipes joignent les tuiles aux frontières administratives et produisent un premier indicateur de connectivité pondéré par la population, par région.

!!! example "Laboratoire — Ookla et WorldPop"

    **Livrable :** Un indicateur de débit descendant et de latence pondéré par la population, par région administrative de premier niveau, une carte et une série trimestrielle

    **Repli :** Des extraits pays pré-découpés sont préparés à l'avance pour chaque pays participant


!!! quote "12h30–14h00 — Déjeuner"

## Après-midi · 14h00 – 17h00

### 14h00–14h30 &nbsp;·&nbsp; Moteurs de passage à l'échelle : technologies big data pour les systèmes statistiques

:material-presentation: **Exposé** &nbsp;·&nbsp; Plan d’action 4.2.3 · 4.2.2

Fondamentaux — ingestion, stockage (lac de données et lakehouse), traitement distribué (par lots contre flux, Spark), indexation et recherche, orchestration, métadonnées et versionnement. Où chaque technologie mérite sa place dans un INS, et où un outil plus simple ferait l'affaire. La Plateforme mondiale des Nations unies et le Centre ONU pour les mégadonnées de Kigali comme infrastructures partagées.


### 14h45–15h30 &nbsp;·&nbsp; Atelier partie 1 — Ookla à l'échelle avec Elasticsearch

:material-flask: **Laboratoire** &nbsp;·&nbsp; Plan d’action 4.2.1 · 4.2.3

Indexer les tuiles Ookla dans un cluster Elasticsearch pré-provisionné ; comprendre le mapping et le type geo_shape ; exécuter les premières agrégations et requêtes géospatiales.

!!! example "Laboratoire — Elasticsearch"

    **Livrable :** Cinq requêtes enregistrées et une comparaison de temps avec l'approche pandas du matin

    **Repli :** Si le cluster est injoignable, le même exercice tourne en local sous DuckDB avec un jeu de requêtes identique


### 15h30–16h45 &nbsp;·&nbsp; Atelier partie 2 — Exploration pilotée par la recherche

:material-flask: **Laboratoire** &nbsp;·&nbsp; Plan d’action 4.2.1 · 4.2.3

Construire une exploration de la connectivité par région et par trimestre pilotée par la recherche ; comparer temps de requête et empreinte mémoire avec l'approche pandas du matin, et en tirer la conclusion pratique sur le moment où la complexité supplémentaire se justifie.

!!! example "Laboratoire — Exploration pilotée par la recherche"

    **Livrable :** Une exploration de la connectivité par région et trimestre pilotée par la recherche, avec la conclusion sur les temps

    **Repli :** Le jeu de requêtes identique tourne sous DuckDB sur les mêmes fichiers parquet


!!! quote "16h45–17h00 — Pause café"

