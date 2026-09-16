<!-- GENERATED from config/agenda.yml by tools/build_site.py. Do not edit. -->

# Day 3 — Beyond the Survey: Non-Traditional Data and the Technologies That Handle Them

*Wednesday · New raw material for official statistics — and the engines that make it usable at scale*

## Morning · 09:00 – 12:30

### 09:00–10:30 &nbsp;·&nbsp; Non-Traditional Data Sources: The Hidden Treasure

:material-presentation-play: **Talk + laboratory** &nbsp;·&nbsp; Action Plan 2.1.1 · 3.1 · 4.3

Taxonomy of non-traditional sources — satellite imagery, crowdsourced measurement, scanner and transaction data, web scraping, sensors and IoT, citizen-generated data. Quality frameworks and coverage bias in non-probabilistic sources; access and partnership models with private data holders; ethics and confidentiality.

[:material-presentation: Slides](../slides/index.md#deck-06){ .md-button .md-button--primary }


!!! quote "10:30–10:45 — Coffee break"

### 10:45–12:30 &nbsp;·&nbsp; Hands-on — Ookla Speedtest Open Data and WorldPop

:material-flask: **Laboratory** &nbsp;·&nbsp; Action Plan 2.1.1 · 3.1

Ookla: performance tiles at web-Mercator zoom 16 (about 611 m at the equator), quarterly since Q1 2019; key fields (quadkey, avg_d_kbps, avg_lat_ms, tests, devices); CC BY-NC-SA 4.0 licence and its consequences for NSO publication; verify national coverage before designing any indicator. WorldPop: gridded population rasters used to weight and normalise. Teams join the tiles to administrative boundaries and produce a first population-weighted connectivity indicator per region.

!!! example "Laboratory — Ookla and WorldPop"

    **Deliverable:** A population-weighted download-speed and latency indicator per first-level administrative region, one map and one quarterly series

    **Fallback:** Pre-clipped country extracts are prepared in advance for every participating country

    **Status:** :material-progress-clock: Day 3 batch


!!! quote "12:30–14:00 — Lunch"

## Afternoon · 14:00 – 17:00

### 14:00–14:30 &nbsp;·&nbsp; Engines of Scale: Big Data Technologies for Statistical Systems

:material-presentation: **Talk** &nbsp;·&nbsp; Action Plan 4.2.3 · 4.2.2

Fundamentals — ingestion, storage (data lake and lakehouse), distributed processing (batch versus streaming, Spark), indexing and search, orchestration, metadata and versioning.

[:material-presentation: Slides](../slides/index.md#deck-07){ .md-button .md-button--primary }


### 14:45–15:30 &nbsp;·&nbsp; Hands-on part 1 — Ookla at Scale with Elasticsearch

:material-flask: **Laboratory** &nbsp;·&nbsp; Action Plan 4.2.1 · 4.2.3

Index the Ookla tiles in a pre-provisioned Elasticsearch cluster; understand the mapping and the geo_shape type; run the first aggregation and geospatial queries.

!!! example "Laboratory — Elasticsearch"

    **Deliverable:** Five saved queries and a timing comparison against the morning's pandas approach

    **Fallback:** If the cluster is unreachable, the same exercise runs locally in DuckDB with an identical query set

    **Status:** :material-progress-clock: Day 3 batch


### 15:30–16:45 &nbsp;·&nbsp; Hands-on part 2 — Search-driven exploration

:material-flask: **Laboratory** &nbsp;·&nbsp; Action Plan 4.2.1 · 4.2.3

Build a search-driven exploration of connectivity by region and quarter; compare query time and memory footprint against the pandas approach of the morning, and draw the practical conclusion about when the added complexity is worth it. Publication on GitHub Each team commits its notebooks, queries and outputs to the workshop GitHub organisation, with a README documenting method, sources and licence.

!!! example "Laboratory — Search-driven exploration"

    **Deliverable:** A search-driven exploration of connectivity by region and quarter, with the timing conclusion

    **Fallback:** Identical query set runs in DuckDB on the same parquet files

    **Status:** :material-progress-clock: Day 3 batch


!!! quote "16:45–17:00 — Coffee break"

