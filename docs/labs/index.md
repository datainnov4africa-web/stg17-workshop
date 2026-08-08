<!-- GENERATED from config/agenda.yml by tools/build_site.py. Do not edit. -->

# The laboratories

Nine laboratories carry the week. Each is specified below with the environment it needs, the artefact the team must produce, and the fallback the facilitation team applies when something breaks — which it will.

!!! tip "Two tracks in every laboratory"

    Participants arrive with markedly different levels. Each notebook therefore exists in two versions: a **guided** version in which the analytical steps are written and the participant fills the gaps, and an **open** version containing only the objective and the data. Teams choose at the start of each laboratory and may switch. The deliverable is identical either way, which keeps the Friday presentations comparable.

## Day 1

### RAG assistant

| | |
|---|---|
| **Team** | pairs |
| **Default country** | `CIV` — change `COUNTRY_ISO3` to your own |
| **Environment and data** | Python in Colab, Kaggle or local; scikit-learn for the word-matching retriever, which needs no download; sentence-transformers optional for the meaning-matching one; no vector database — the corpus is small enough that one is not warranted |
| **Team deliverable** | A transcript of answers with the exact passages behind each one, and a retrieval evaluation separating retrieval failures from generation failures |
| **Fallback** | A fictional five-document corpus ships with the toolkit, so no team is blocked by uncleared publications; without any model provider, the retrieval half of the laboratory still runs — and that is where most RAG problems are |
| **Earth Engine variant** | — |
| **Status** | :material-check-circle:{ .ok } Available |

[![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/STG17-Africa/stg17-workshop/blob/main/notebooks/day1/D1_RAG_Assistant_EN.ipynb) **guided** &nbsp; [:material-github:](https://github.com/STG17-Africa/stg17-workshop/blob/main/notebooks/day1/D1_RAG_Assistant_EN.ipynb)

[![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/STG17-Africa/stg17-workshop/blob/main/notebooks/day1/D1_RAG_Assistant_EN_open.ipynb) **open** &nbsp; [:material-github:](https://github.com/STG17-Africa/stg17-workshop/blob/main/notebooks/day1/D1_RAG_Assistant_EN_open.ipynb)

### From RAG to agent

| | |
|---|---|
| **Team** | pairs |
| **Default country** | `CIV` — change `COUNTRY_ISO3` to your own |
| **Environment and data** | Same environment plus a provisioned LLM API key; function calling with two tools — the retriever and a table lookup |
| **Team deliverable** | An agent that answers a question, retrieves the supporting figure and drafts a five-line note |
| **Fallback** | A working reference agent is provided; teams modify it rather than build from scratch |
| **Earth Engine variant** | — |
| **Status** | :material-progress-clock: Day 1 batch |

## Day 2

### Document to dashboard

| | |
|---|---|
| **Team** | solo |
| **Default country** | `CIV` — change `COUNTRY_ISO3` to your own |
| **Environment and data** | LLM API; Python or plain HTML/JS; the participant's own national publication; GitHub Pages |
| **Team deliverable** | A public dashboard URL and the extraction-verification table comparing output against the source |
| **Fallback** | A sample publication and a static dashboard template are supplied; publishing can be done from the template alone |
| **Earth Engine variant** | — |
| **Status** | :material-progress-clock: Day 2 batch |

### Provider benchmark

| | |
|---|---|
| **Team** | solo |
| **Default country** | `CIV` — change `COUNTRY_ISO3` to your own |
| **Environment and data** | Two API endpoints including Groq; one shared spreadsheet |
| **Team deliverable** | Three rows in the shared comparison sheet: latency, cost per thousand documents, quality score |
| **Fallback** | The facilitator runs the benchmark live from the podium if participant keys fail |
| **Earth Engine variant** | — |
| **Status** | :material-progress-clock: Day 2 batch |

### Toolkit stations

| | |
|---|---|
| **Team** | stations |
| **Default country** | `CIV` — change `COUNTRY_ISO3` to your own |
| **Environment and data** | Varies by station; all accessible from a browser |
| **Team deliverable** | Two finished artefacts per participant, one from each chosen station |
| **Fallback** | Stations are independent — a station that fails costs only itself |
| **Earth Engine variant** | — |
| **Status** | :material-progress-clock: Day 2 batch |

## Day 3

### Ookla and WorldPop

| | |
|---|---|
| **Team** | teams |
| **Default country** | `TUN` — change `COUNTRY_ISO3` to your own |
| **Environment and data** | Python with geopandas and pyarrow; Ookla parquet tiles and WorldPop rasters mirrored locally; national administrative boundaries |
| **Team deliverable** | A population-weighted download-speed and latency indicator per first-level administrative region, one map and one quarterly series |
| **Fallback** | Pre-clipped country extracts are prepared in advance for every participating country |
| **Earth Engine variant** | yes — nothing downloaded |
| **Status** | :material-progress-clock: Day 3 batch |

### Elasticsearch

| | |
|---|---|
| **Team** | teams |
| **Default country** | `TUN` — change `COUNTRY_ISO3` to your own |
| **Environment and data** | Pre-provisioned and pre-loaded cluster, one index per country, Kibana available |
| **Team deliverable** | Five saved queries and a timing comparison against the morning's pandas approach |
| **Fallback** | If the cluster is unreachable, the same exercise runs locally in DuckDB with an identical query set |
| **Earth Engine variant** | — |
| **Status** | :material-progress-clock: Day 3 batch |

### Search-driven exploration

| | |
|---|---|
| **Team** | teams |
| **Default country** | `TUN` — change `COUNTRY_ISO3` to your own |
| **Environment and data** | The same cluster, or the DuckDB fallback |
| **Team deliverable** | A search-driven exploration of connectivity by region and quarter, with the timing conclusion |
| **Fallback** | Identical query set runs in DuckDB on the same parquet files |
| **Earth Engine variant** | — |
| **Status** | :material-progress-clock: Day 3 batch |

## Day 4

### NTL collect and explore

| | |
|---|---|
| **Team** | teams |
| **Default country** | `CIV` — change `COUNTRY_ISO3` to your own |
| **Environment and data** | Python with rasterio and h5py; VIIRS monthly and annual subsets mirrored locally; Earth Engine account optional |
| **Team deliverable** | A documented national raster subset and an inventory of the artefacts present in that country |
| **Fallback** | Pre-clipped national subsets are prepared for every participating country; the Earth Engine variant downloads nothing at all |
| **Earth Engine variant** | yes — nothing downloaded |
| **Status** | :material-check-circle:{ .ok } Available |

[![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/STG17-Africa/stg17-workshop/blob/main/notebooks/day4/D4_NTL_Collect_Explore_EN.ipynb) **guided** &nbsp; [:material-github:](https://github.com/STG17-Africa/stg17-workshop/blob/main/notebooks/day4/D4_NTL_Collect_Explore_EN.ipynb)

[![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/STG17-Africa/stg17-workshop/blob/main/notebooks/day4/D4_NTL_Collect_Explore_EN_open.ipynb) **open** &nbsp; [:material-github:](https://github.com/STG17-Africa/stg17-workshop/blob/main/notebooks/day4/D4_NTL_Collect_Explore_EN_open.ipynb)

[![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/STG17-Africa/stg17-workshop/blob/main/notebooks/day4/D4_NTL_GEE_EN.ipynb) **Earth Engine variant** &nbsp; [:material-github:](https://github.com/STG17-Africa/stg17-workshop/blob/main/notebooks/day4/D4_NTL_GEE_EN.ipynb)

### NTL explore and understand

| | |
|---|---|
| **Team** | teams |
| **Default country** | `CIV` — change `COUNTRY_ISO3` to your own |
| **Environment and data** | Same notebook as part 1 — steps 7 and 8 |
| **Team deliverable** | The artefact inventory for your country, with evidence |
| **Fallback** | The reference country (Côte d'Ivoire) is prepared end to end |
| **Earth Engine variant** | yes — nothing downloaded |
| **Status** | :material-check-circle:{ .ok } Available |

[![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/STG17-Africa/stg17-workshop/blob/main/notebooks/day4/D4_NTL_Collect_Explore_EN.ipynb) **guided** &nbsp; [:material-github:](https://github.com/STG17-Africa/stg17-workshop/blob/main/notebooks/day4/D4_NTL_Collect_Explore_EN.ipynb)

[![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/STG17-Africa/stg17-workshop/blob/main/notebooks/day4/D4_NTL_Collect_Explore_EN_open.ipynb) **open** &nbsp; [:material-github:](https://github.com/STG17-Africa/stg17-workshop/blob/main/notebooks/day4/D4_NTL_Collect_Explore_EN_open.ipynb)

[![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/STG17-Africa/stg17-workshop/blob/main/notebooks/day4/D4_NTL_GEE_EN.ipynb) **Earth Engine variant** &nbsp; [:material-github:](https://github.com/STG17-Africa/stg17-workshop/blob/main/notebooks/day4/D4_NTL_GEE_EN.ipynb)

### NTL analysis

| | |
|---|---|
| **Team** | teams |
| **Default country** | `CIV` — change `COUNTRY_ISO3` to your own |
| **Environment and data** | rasterstats or exactextract; the panel produced in the morning |
| **Team deliverable** | Zonal statistics table, time series, change detection between two periods, and the maps |
| **Fallback** | One reference country is prepared end to end and handed to any team whose national data proves incomplete |
| **Earth Engine variant** | yes — nothing downloaded |
| **Status** | :material-progress-clock: Day 4 batch |

### NTL validation

| | |
|---|---|
| **Team** | teams |
| **Default country** | `CIV` — change `COUNTRY_ISO3` to your own |
| **Environment and data** | The official subnational indicator brought by the team |
| **Team deliverable** | Correlation against the official indicator, and a written limitations statement |
| **Fallback** | A reference official indicator is supplied for the reference country |
| **Earth Engine variant** | — |
| **Status** | :material-progress-clock: Day 4 batch |

## Day 5

### Publish your work

| | |
|---|---|
| **Team** | teams |
| **Default country** | `CIV` — change `COUNTRY_ISO3` to your own |
| **Environment and data** | A GitHub account and the country-template repository |
| **Team deliverable** | A public country repository with README, licence, metadata, GitHub Pages site and citation file |
| **Fallback** | The template can be published as-is and populated afterwards |
| **Earth Engine variant** | — |
| **Status** | :material-progress-clock: Day 5 batch |

