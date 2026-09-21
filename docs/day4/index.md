<!-- GENERATED from config/agenda.yml by tools/build_site.py. Do not edit. -->

# Day 4 — Africa after dark: Reading development from Night-Time Lights

*Thursday · A full day on NTL — from raw radiance to a validated subnational indicator*

## Morning · 09:00 – 12:30

### 09:00–09:30 &nbsp;·&nbsp; Night-Time Lights: What the darkness tells us

:material-presentation: **Talk** &nbsp;·&nbsp; Action Plan 2.1.1

Concepts and utility, kept deliberately short so the day is spent in the data — from DMSP-OLS (1992–2013) to VIIRS/DNB; the NASA Black Marble products (VNP46A2 daily, A3 monthly, A4 annual); what NTL proxies well — economic activity, electrification, urbanisation, crisis monitoring. The known artefacts are introduced here by name only and met hands-on in Part 2.

[:material-file-pdf-box: PDF · EN](../downloads/Day4/0900_night-time-lights_EN.pdf){ .md-button } [:material-file-pdf-box: PDF · FR](../downloads/Day4/0900_night-time-lights_FR.pdf){ .md-button } [:material-microsoft-powerpoint: PPTX · EN](../downloads/Day4/0900_night-time-lights_EN.pptx){ .md-button } [:material-microsoft-powerpoint: PPTX · FR](../downloads/Day4/0900_night-time-lights_FR.pptx){ .md-button }


### 09:30–10:30 &nbsp;·&nbsp; Hands-on part 1 — Collect

:material-flask: **Laboratory** &nbsp;·&nbsp; Action Plan 4.2.1

Access NTL rasters (NASA Earthdata, EOG or Google Earth Engine); understand the file structure, bands and quality flags; clip to the national extent and save a working subset.

[:material-notebook-outline: IPYNB · EN](../downloads/Day4/0930_hands-on-part-1_EN.ipynb){ .md-button } [:material-notebook-outline: IPYNB · FR](../downloads/Day4/0930_hands-on-part-1_FR.ipynb){ .md-button }

[![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/datainnov4africa-web/stg17-workshop/blob/main/docs/downloads/Day4/0930_hands-on-part-1_EN.ipynb) **EN** &nbsp; [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/datainnov4africa-web/stg17-workshop/blob/main/docs/downloads/Day4/0930_hands-on-part-1_FR.ipynb) **FR**

!!! example "Laboratory — NTL collect and explore"

    **Deliverable:** A documented national raster subset and an inventory of the artefacts present in that country

    **Fallback:** Pre-clipped national subsets are prepared for every participating country; the Earth Engine variant downloads nothing at all


!!! quote "10:30–10:45 — Coffee break"

### 10:45–12:30 &nbsp;·&nbsp; Hands-on part 2 — Explore and Understand

:material-flask: **Laboratory** &nbsp;·&nbsp; Action Plan 4.2.1 · 2.1.1

Visualise and interrogate the raster before computing on it — distribution of radiance values, effect of the cloud and quality masks, month-to-month variation. Teams deliberately hunt for the artefacts named in the morning talk (blooming around cities, saturation, gas flares, seasonality, sensor discontinuity, rural low-light noise) and document which ones are present in their own country. Closes with a short round of comparisons across teams.

[:material-notebook-outline: IPYNB · EN](../downloads/Day4/1045_hands-on-part-2_EN.ipynb){ .md-button } [:material-notebook-outline: IPYNB · FR](../downloads/Day4/1045_hands-on-part-2_FR.ipynb){ .md-button }

[![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/datainnov4africa-web/stg17-workshop/blob/main/docs/downloads/Day4/1045_hands-on-part-2_EN.ipynb) **EN** &nbsp; [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/datainnov4africa-web/stg17-workshop/blob/main/docs/downloads/Day4/1045_hands-on-part-2_FR.ipynb) **FR**

!!! example "Laboratory — NTL explore and understand"

    **Deliverable:** The artefact inventory for your country, with evidence

    **Fallback:** The reference country (Côte d'Ivoire) is prepared end to end


!!! quote "12:30–14:00 — Lunch"

## Afternoon · 14:00 – 17:00

### 14:00–16:45 &nbsp;·&nbsp; Hands-on part 3 — NTL Analysis & Validation

:material-flask: **Laboratory** &nbsp;·&nbsp; Action Plan 4.2.1 · 2.1.1 · 4.3 · 3.1.1

Compute zonal statistics by administrative level (sum of radiance, mean radiance, lit area); build annual and monthly time series; detect change between two periods; map and visualise the results. Then validate the NTL proxy by correlating it with official subnational statistics (population, electrification rate) and decide, with evidence, whether it is usable for dissemination in your country or remains a diagnostic tool only. Document the limitations explicitly; this statement is part of the deliverable. The resulting maps, charts and limitations statement can be published as a public website via GitHub Pages.

!!! example "Laboratory — NTL analysis and validation"

    **Deliverable:** Zonal statistics table, time series, change detection between two periods and the maps; correlation against the official indicator, and a written limitations statement

    **Fallback:** One reference country is prepared end to end and handed to any team whose national data proves incomplete, with a reference official indicator supplied for it


!!! quote "16:45–17:00 — Coffee break"

