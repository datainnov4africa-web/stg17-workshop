# Data

Raw inputs are **not** committed to this repository. They are large, and some are
not ours to redistribute. This file records where each one came from, so that the
work is reproducible without the repository becoming a mirror.

## `raw/` - not in git

| File | Source | How to fetch it | Licence | Retrieved |
|---|---|---|---|---|
| `<VNP46A4_*.h5>` | NASA Earthdata | `stg17.ntl.search_cmr()` then `download_granules()`, free token required | Public domain | `<date>` |
| `<ookla_*.parquet>` | Ookla Open Data (AWS S3) | see the Day 3 notebook | **CC BY-NC-SA 4.0** | `<date>` |
| `<adm.shp>` | `<Your office>` | internal | `<your licence>` | `<date>` |

## `processed/` - committed

Small derived tables that the figures and the README depend on. Anything here is
covered by [`../LICENSE-DATA`](../LICENSE-DATA).

| File | What it is | Produced by |
|---|---|---|
| `<iso3>_panel_adm2.csv` | Year x district zonal statistics | `notebooks/<...>.ipynb` |
| `<iso3>_validation.csv` | Proxy against the official indicator | `notebooks/<...>.ipynb` |

## Size policy

Nothing over **5 MB** goes into git. Large derived products belong on Zenodo,
linked from the README. GitHub is a code host, and a repository full of rasters is
slow to clone and impossible to review.
