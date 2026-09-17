<!-- GENERATED from config/agenda.yml by tools/build_site.py. Do not edit. -->

# Day 4 — Africa after dark: Reading development from Night-Time Lights

*Thursday · A full day on NTL — from raw radiance to a validated subnational indicator*

## Morning · 09:00 – 12:30

### 09:00–09:30 &nbsp;·&nbsp; Night-Time Lights: What the darkness tells us

:material-presentation: **Talk** &nbsp;·&nbsp; Action Plan 2.1.1

Concepts and utility, kept deliberately short so the day is spent in the data — from DMSP-OLS (1992–2013) to VIIRS/DNB; the NASA Black Marble products (VNP46A2 daily, A3 monthly, A4 annual); what NTL proxies well — economic activity, electrification, urbanisation, crisis monitoring. The known artefacts are introduced here by name only and met hands-on in Part 2.


### 09:30–10:30 &nbsp;·&nbsp; Hands-on part 1 — Collect

:material-flask: **Laboratory** &nbsp;·&nbsp; Action Plan 4.2.1

Access NTL rasters (NASA Earthdata, EOG or Google Earth Engine); understand the file structure, bands and quality flags; clip to the national extent and save a working subset.

!!! example "Laboratory — NTL collect and explore"

    **Deliverable:** A documented national raster subset and an inventory of the artefacts present in that country

    **Fallback:** Pre-clipped national subsets are prepared for every participating country; the Earth Engine variant downloads nothing at all


!!! quote "10:30–10:45 — Coffee break"

### 10:45–12:30 &nbsp;·&nbsp; Hands-on part 2 — Explore and Understand

:material-flask: **Laboratory** &nbsp;·&nbsp; Action Plan 4.2.1 · 2.1.1

Visualise and interrogate the raster before computing on it — distribution of radiance values, effect of the cloud and quality masks, month-to-month variation. Teams deliberately hunt for the artefacts named in the morning talk (blooming around cities, saturation, gas flares, seasonality, sensor discontinuity, rural low-light noise) and document which ones are present in their own country. Closes with a short round of comparisons across teams.

!!! example "Laboratory — NTL explore and understand"

    **Deliverable:** The artefact inventory for your country, with evidence

    **Fallback:** The reference country (Côte d'Ivoire) is prepared end to end


!!! quote "12:30–14:00 — Lunch"

## Afternoon · 14:00 – 17:00

### 14:00–15:30 &nbsp;·&nbsp; Hands-on part 3 — Analysis

:material-flask: **Laboratory** &nbsp;·&nbsp; Action Plan 4.2.1 · 2.1.1

Zonal statistics by administrative level (sum of radiance, mean radiance, lit area); annual and monthly time series; change detection between two periods; mapping and visualisation of the results.

!!! example "Laboratory — NTL analysis"

    **Deliverable:** Zonal statistics table, time series, change detection between two periods, and the maps

    **Fallback:** One reference country is prepared end to end and handed to any team whose national data proves incomplete


### 15:30–16:30 &nbsp;·&nbsp; Hands-on part 4 — Validation

:material-flask: **Laboratory** &nbsp;·&nbsp; Action Plan 2.1.1 · 4.3

Correlate the NTL proxy with official subnational statistics (population, electrification rate). Decide, with evidence, whether the proxy is usable for dissemination in your country or remains a diagnostic tool only. Document the limitations explicitly — this statement is part of the deliverable.

!!! example "Laboratory — NTL validation"

    **Deliverable:** Correlation against the official indicator, and a written limitations statement

    **Fallback:** A reference official indicator is supplied for the reference country


### 16:30–16:45 &nbsp;·&nbsp; Publication and preparation for Day 5

:material-flask: **Laboratory** &nbsp;·&nbsp; Action Plan 4.2.1 · 3.1.1

Commit notebooks, maps and the limitations statement to GitHub; assemble the week's three outputs — dashboard, connectivity scores, NTL analysis — into the country presentation for Friday.


!!! quote "16:45–17:00 — Coffee break"

