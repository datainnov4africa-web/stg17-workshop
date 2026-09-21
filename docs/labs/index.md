<!-- GENERATED from config/agenda.yml by tools/build_site.py. Do not edit. -->

# The laboratories

12 laboratories carry the week. Each is described below with the environment it needs, the artefact the team must produce, and the fallback applied when something breaks — which it will.

A laboratory's slides and notebook are not on this page: they sit on the day page, beside the session that runs it. Each laboratory below links there.

## Day 1

### RAG assistant

:material-calendar-clock: **Day 1 · 14:30–15:30** &nbsp;·&nbsp; [go to the session](../day1/index.md#14301530-hands-on-part-1-retrieval-augmented-generation)

**Environment and data** — Python in Colab, Kaggle or local; scikit-learn for the word-matching retriever, which needs no download; sentence-transformers optional for the meaning-matching one; no vector database — the corpus is small enough that one is not warranted

**What the team produces** — A transcript of answers with the exact passages behind each one, and a retrieval evaluation separating retrieval failures from generation failures

**If something breaks** — A fictional five-document corpus ships with the toolkit, so no team is blocked by uncleared publications; without any model provider, the retrieval half of the laboratory still runs — and that is where most RAG problems are

### From RAG to agent

:material-calendar-clock: **Day 1 · 15:30–16:45** &nbsp;·&nbsp; [go to the session](../day1/index.md#15301645-hands-on-part-2-from-rag-to-agent)

**Environment and data** — Same environment as the RAG laboratory; four tools — retrieval, a document list, a guarded calculator and one that writes to disk. A JSON text protocol rather than native function calling, so the request-to-execution gap stays visible and the exercise runs on any provider including a local model

**What the team produces** — An audit log recording every tool the model asked for, whether policy allowed it, and the raw reply behind each request — plus the note the agent wrote once a policy permitted it

**If something breaks** — A scripted model replays fixed replies, so the loop, the approval gate, the error recovery and the audit log are all exercised with no API key. That is deliberate rather than a consolation path — those four things are what an office writes and owns; the model is what it rents

## Day 2

### Document to dashboard

:material-calendar-clock: **Day 2 · 10:45–12:30** &nbsp;·&nbsp; [go to the session](../day2/index.md#10451230-hands-on-from-statistical-document-to-public-dashboard)

**Environment and data** — LLM API; Python or plain HTML/JS; the participant's own national publication; GitHub Pages

**What the team produces** — A public dashboard URL and the extraction-verification table comparing output against the source

**If something breaks** — A sample publication and a static dashboard template are supplied; publishing can be done from the template alone

### Provider benchmark

:material-calendar-clock: **Day 2 · 14:45–15:30** &nbsp;·&nbsp; [go to the session](../day2/index.md#14451530-choosing-your-engine-speed-cost-and-sovereignty-working-with-groq)

**Environment and data** — Two API endpoints including Groq; one shared spreadsheet

**What the team produces** — Three rows in the shared comparison sheet: latency, cost per thousand documents, quality score

**If something breaks** — The facilitator runs the benchmark live from the podium if participant keys fail

### Toolkit stations

:material-calendar-clock: **Day 2 · 15:30–16:45** &nbsp;·&nbsp; rotating stations &nbsp;·&nbsp; [go to the session](../day2/index.md#15301645-hands-on-one-model-many-jobs-an-llm-toolkit-for-statisticians)

**Environment and data** — Varies by station; all accessible from a browser

**What the team produces** — Two finished artefacts per participant, one from each chosen station

**If something breaks** — Stations are independent — a station that fails costs only itself

## Day 3

### Ookla and WorldPop

:material-calendar-clock: **Day 3 · 10:45–12:30** &nbsp;·&nbsp; in teams &nbsp;·&nbsp; [go to the session](../day3/index.md#10451230-hands-on-ookla-speedtest-open-data-and-worldpop)

**Environment and data** — Python with geopandas and pyarrow; Ookla parquet tiles and WorldPop rasters mirrored locally; national administrative boundaries

**What the team produces** — A population-weighted download-speed and latency indicator per first-level administrative region, one map and one quarterly series

**If something breaks** — Pre-clipped country extracts are prepared in advance for every participating country

### Elasticsearch

:material-calendar-clock: **Day 3 · 14:45–15:30** &nbsp;·&nbsp; in teams &nbsp;·&nbsp; [go to the session](../day3/index.md#14451530-hands-on-part-1-ookla-at-scale-with-elasticsearch)

**Environment and data** — Pre-provisioned and pre-loaded cluster, one index per country, Kibana available

**What the team produces** — Five saved queries and a timing comparison against the morning's pandas approach

**If something breaks** — If the cluster is unreachable, the same exercise runs locally in DuckDB with an identical query set

### Search-driven exploration

:material-calendar-clock: **Day 3 · 15:30–16:45** &nbsp;·&nbsp; in teams &nbsp;·&nbsp; [go to the session](../day3/index.md#15301645-hands-on-part-2-search-driven-exploration)

**Environment and data** — The same cluster, or the DuckDB fallback

**What the team produces** — A search-driven exploration of connectivity by region and quarter, with the timing conclusion

**If something breaks** — Identical query set runs in DuckDB on the same parquet files

## Day 4

### NTL collect and explore

:material-calendar-clock: **Day 4 · 09:30–10:30** &nbsp;·&nbsp; in teams &nbsp;·&nbsp; [go to the session](../day4/index.md#09301030-hands-on-part-1-collect)

**Environment and data** — Python with rasterio and h5py; VIIRS monthly and annual subsets mirrored locally; Earth Engine account optional

**What the team produces** — A documented national raster subset and an inventory of the artefacts present in that country

**If something breaks** — Pre-clipped national subsets are prepared for every participating country; the Earth Engine variant downloads nothing at all

### NTL explore and understand

:material-calendar-clock: **Day 4 · 10:45–12:30** &nbsp;·&nbsp; in teams &nbsp;·&nbsp; [go to the session](../day4/index.md#10451230-hands-on-part-2-explore-and-understand)

**Environment and data** — Same notebook as part 1 — steps 7 and 8

**What the team produces** — The artefact inventory for your country, with evidence

**If something breaks** — The reference country (Côte d'Ivoire) is prepared end to end

### NTL analysis and validation

:material-calendar-clock: **Day 4 · 14:00–16:45** &nbsp;·&nbsp; in teams &nbsp;·&nbsp; [go to the session](../day4/index.md#14001645-hands-on-part-3-ntl-analysis-validation)

**Environment and data** — rasterstats or exactextract; the panel produced in the morning; the official subnational indicator brought by the team

**What the team produces** — Zonal statistics table, time series, change detection between two periods and the maps; correlation against the official indicator, and a written limitations statement

**If something breaks** — One reference country is prepared end to end and handed to any team whose national data proves incomplete, with a reference official indicator supplied for it

## Day 5

### Publish your work

:material-calendar-clock: **Day 5 · 09:00–10:30** &nbsp;·&nbsp; in teams &nbsp;·&nbsp; [go to the session](../day5/index.md#09001030-assisting-countries-in-publishing-their-work)

**Environment and data** — A GitHub account and the country-template repository

**What the team produces** — A public country repository with README, licence, metadata, GitHub Pages site and citation file

**If something breaks** — The template can be published as-is and populated afterwards

