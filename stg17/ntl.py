"""
STG17 · Night-Time Lights — reading NASA Black Marble and turning it into statistics.

This module is the engine behind the four Day 4 laboratories. It does five
things, and each is something a participant would otherwise get subtly wrong:

  1. **Discovers** the HDF5 files in the local mirror and reports what is missing
  2. **Reads** a VNP46A4 / VNP46A3 granule, taking `scale_factor` and
     `_FillValue` *from the file itself* rather than from a constant
  3. **Georeferences** a tile from its name, because the 10x10 degree Black
     Marble grid is regular and the affine transform can be derived exactly
  4. **Mosaics and clips** strictly to the national polygons
  5. **Computes zonal statistics** at the finest administrative level and
     aggregates upward, so ADM2 sums to ADM1 sums to ADM0 by construction

Products
--------
    VNP46A2   daily,   ~500 m   gap-filled DNB BRDF-corrected radiance
    VNP46A3   monthly, ~500 m   monthly composite
    VNP46A4   annual,  ~500 m   annual composite   <- the workshop default

Units are nW·cm⁻²·sr⁻¹ (nanowatts per square centimetre per steradian).

What "Sum of Lights" is, and is not
-----------------------------------
SoL is the sum of radiance over an area. It is a *proxy*: it tracks street,
residential and industrial lighting, and it tracks gas flares just as happily.
It is not GDP, and it is not the household electrification rate. The Day 4
validation laboratory exists precisely to establish, with evidence and per
country, whether the proxy is good enough to disseminate or should stay a
diagnostic tool. Read `stg17.ntl.ARTEFACTS` before interpreting any series.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from .countries import Country, get
from .i18n import T

# ---------------------------------------------------------------------------
#  Products
# ---------------------------------------------------------------------------
PRODUCTS = {
    "VNP46A4": {"cadence": "annual", "res_m": 500, "note_en": "Annual composite — the workshop default",
                "note_fr": "Composite annuel — valeur par défaut de l'atelier"},
    "VNP46A3": {"cadence": "monthly", "res_m": 500, "note_en": "Monthly composite",
                "note_fr": "Composite mensuel"},
    "VNP46A2": {"cadence": "daily", "res_m": 500, "note_en": "Daily, gap-filled BRDF-corrected",
                "note_fr": "Journalier, corrigé BRDF et comblé"},
}

#: Layer preference order. NearNadir is less affected by view-angle effects and
#: is what most published African NTL work uses; AllAngle is the fallback when a
#: collection does not ship the near-nadir composite.
PREFERRED_LAYERS = (
    "NearNadir_Composite_Snow_Free",
    "AllAngle_Composite_Snow_Free",
    "Gap_Filled_DNB_BRDF-Corrected_Radiance",
    "DNB_BRDF-Corrected_Radiance",
)

#: The artefacts teams are asked to hunt for in Day 4 part 2. Each is real,
#: each has bitten a published study, and each is detectable in an afternoon.
ARTEFACTS = {
    "blooming": (
        "Light spills beyond its physical source: a city of 20 km² lights up 60 km² of pixels. "
        "Inflates urban SoL and blurs the urban/rural boundary.",
        "La lumière déborde de sa source physique : une ville de 20 km² éclaire 60 km² de pixels. "
        "Gonfle la SoL urbaine et brouille la frontière urbain/rural.",
    ),
    "saturation": (
        "Very bright cores (central business districts, large industrial sites) hit the top of "
        "the sensor's usable range, so growth there stops showing up.",
        "Les cœurs très lumineux (quartiers d'affaires, grands sites industriels) atteignent le "
        "haut de la plage exploitable du capteur : la croissance n'y apparaît plus.",
    ),
    "gas_flares": (
        "Oil and gas flares are extremely bright and constant. They can dominate a region's SoL "
        "while representing zero household electrification.",
        "Les torchères pétrolières et gazières sont très lumineuses et constantes. Elles peuvent "
        "dominer la SoL d'une région sans traduire aucune électrification des ménages.",
    ),
    "seasonality": (
        "Monthly series move with cloud cover, aerosols, moonlight and, in the Sahel, harmattan "
        "dust. Compare like months, or use annual composites.",
        "Les séries mensuelles bougent avec la couverture nuageuse, les aérosols, le clair de lune "
        "et, au Sahel, l'harmattan. Comparez des mois identiques, ou utilisez l'annuel.",
    ),
    "sensor_discontinuity": (
        "DMSP-OLS (1992-2013) and VIIRS (2012-) are different instruments with different units. "
        "Never splice the two series without an explicit harmonisation step.",
        "DMSP-OLS (1992-2013) et VIIRS (2012-) sont des instruments différents, aux unités "
        "différentes. Ne jamais raccorder les deux séries sans harmonisation explicite.",
    ),
    "rural_noise": (
        "Genuinely dark rural pixels carry background noise that can be slightly negative. "
        "Summing them without a threshold adds noise, not signal.",
        "Les pixels ruraux réellement sombres portent un bruit de fond parfois légèrement négatif. "
        "Les sommer sans seuil ajoute du bruit, pas du signal.",
    ),
    "snow_ice": (
        "Snow-covered surfaces reflect moonlight and inflate radiance. Marginal for most of "
        "Africa, real for the Atlas and the Ethiopian highlands.",
        "Les surfaces enneigées réfléchissent le clair de lune et gonflent la radiance. Marginal "
        "pour l'essentiel de l'Afrique, réel pour l'Atlas et les hauts plateaux éthiopiens.",
    ),
}

_RE_TILE = re.compile(r"h(\d{2})v(\d{2})")
_RE_DATE = re.compile(r"\.A(\d{4})(\d{3})\.")


# ---------------------------------------------------------------------------
#  File discovery
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class Granule:
    """One HDF5 file, with what we could work out from its name."""

    path: Path
    year: int
    doy: int
    tile: str

    @property
    def h(self) -> int:
        return int(self.tile[1:3])

    @property
    def v(self) -> int:
        return int(self.tile[4:6])


def parse_filename(path: str | Path) -> Granule | None:
    """
    Read year, day-of-year and tile from a Black Marble filename.

        VNP46A4.A2020001.h17v08.002.2021165104956.h5
                 ^year^doy  ^tile

    Returns None for a file that does not follow the convention, so a stray
    file in the mirror is skipped rather than crashing the discovery step.
    """
    p = Path(path)
    tile_match = _RE_TILE.search(p.name)
    date_match = _RE_DATE.search(p.name)
    if not tile_match or not date_match:
        return None
    return Granule(p, int(date_match.group(1)), int(date_match.group(2)),
                   f"h{tile_match.group(1)}v{tile_match.group(2)}")


def discover(directory: str | Path, years: tuple[int, ...] | None = None) -> dict[int, list[Granule]]:
    """
    Index the HDF5 files under a directory, grouped by year.

    Recursive, so it copes with both a flat mirror and the
    `h5_cache/<ISO3>/Annual/` layout used by the June 2026 webinar material.
    """
    directory = Path(directory)
    out: dict[int, list[Granule]] = {}
    if not directory.exists():
        return out
    for path in sorted(directory.rglob("*.h5")):
        granule = parse_filename(path)
        if granule is None:
            continue
        if years and granule.year not in years:
            continue
        out.setdefault(granule.year, []).append(granule)
    return out


def inventory(files: dict[int, list[Granule]], country: Country) -> "object":
    """
    A completeness audit, returned as a DataFrame.

    This is the quality-control step that belongs *before* any analysis: a year
    missing one of its tiles will produce a national total that silently drops a
    third of the territory, and nothing downstream will complain.
    """
    import pandas as pd  # noqa: PLC0415

    expected = set(country.viirs_tiles)
    rows = []
    for year in sorted(files):
        present = {g.tile for g in files[year]}
        missing = sorted(expected - present)
        rows.append({
            "year": year,
            "tiles_present": len(present),
            "tiles_expected": len(expected),
            "complete": not missing,
            "missing": ", ".join(missing) if missing else "—",
        })
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
#  Acquisition from NASA Earthdata
# ---------------------------------------------------------------------------
CMR_GRANULES = "https://cmr.earthdata.nasa.gov/search/granules.json"


def search_cmr(product: str, tiles: list[str], years: list[int],
               page_size: int = 200, verbose: bool = True) -> list[dict]:
    """
    Ask NASA's Common Metadata Repository which granules exist.

    The search endpoint is **public** — no token needed — which makes it the
    right place to find out what is available before committing to a download.
    Only the download itself requires an Earthdata login.

    Returns one dict per granule with its title and its HTTPS URL, de-duplicated:
    CMR routinely returns the same granule through several distribution
    endpoints, and a naive script downloads it three times.
    """
    import requests  # noqa: PLC0415

    seen: dict[str, dict] = {}
    for year in years:
        params = {
            "short_name": product,
            "temporal": f"{year}-01-01T00:00:00Z,{year}-12-31T23:59:59Z",
            "page_size": page_size,
        }
        try:
            response = requests.get(CMR_GRANULES, params=params, timeout=60)
            response.raise_for_status()
            entries = response.json().get("feed", {}).get("entry", [])
        except Exception as exc:  # noqa: BLE001
            if verbose:
                print(T(f"  CMR query failed for {year}: {exc}",
                        f"  Requête CMR échouée pour {year} : {exc}"))
            continue

        for entry in entries:
            title = entry.get("title", "")
            if not any(tile in title for tile in tiles):
                continue
            url = next(
                (link.get("href") for link in entry.get("links", [])
                 if str(link.get("href", "")).endswith(".h5")
                 and str(link.get("href", "")).startswith("http")),
                None,
            )
            if not url:
                continue
            key = title.split("/")[-1]
            if key not in seen:
                seen[key] = {"title": key, "url": url, "year": year}

        if verbose:
            found = sum(1 for g in seen.values() if g["year"] == year)
            print(T(f"  {year}: {found} granule(s) matching {', '.join(tiles)}",
                    f"  {year} : {found} granule(s) correspondant à {', '.join(tiles)}"))
    return sorted(seen.values(), key=lambda g: g["title"])


def download_granules(granules: list[dict], dest_dir: str | Path, token: str | None = None,
                      retries: int = 3, min_bytes: int = 1_000_000,
                      verbose: bool = True) -> list[Path]:
    """
    Download granules with resume, retry and size verification.

    Written defensively on purpose. In the June 2026 webinar the download step
    was where sessions died: a connection drops at 80%, the partial file stays
    on disk, and the next run treats it as complete and reads garbage. So:

      * an existing file larger than `min_bytes` is trusted and skipped
      * a failed download is deleted rather than left truncated
      * each granule is retried, with the whole batch continuing on failure

    `token` is an Earthdata bearer token, obtained at
    https://urs.earthdata.nasa.gov/users/<you>/user_tokens — an account is free.
    Without one this returns an empty list and says why, rather than producing
    a folder of HTML login pages named `.h5`, which is what a naive script does.
    """
    import requests  # noqa: PLC0415

    dest = Path(dest_dir)
    dest.mkdir(parents=True, exist_ok=True)

    if not token:
        print(T("No Earthdata token. Set EARTHDATA_TOKEN, or use the mirrored data "
                "from the USB key, or run the Earth Engine variant of this laboratory.",
                "Pas de jeton Earthdata. Définissez EARTHDATA_TOKEN, ou utilisez les données "
                "de la clé USB, ou exécutez la variante Earth Engine de ce laboratoire."))
        return []

    headers = {"Authorization": f"Bearer {token}"}
    written: list[Path] = []

    for granule in granules:
        target = dest / granule["title"]
        if target.exists() and target.stat().st_size >= min_bytes:
            if verbose:
                print(T(f"  skip (already have) {target.name}",
                        f"  ignoré (déjà présent) {target.name}"))
            written.append(target)
            continue

        for attempt in range(1, retries + 1):
            try:
                with requests.get(granule["url"], headers=headers, stream=True,
                                  timeout=300, allow_redirects=True) as response:
                    response.raise_for_status()
                    tmp = target.with_suffix(".part")
                    with open(tmp, "wb") as handle:
                        for chunk in response.iter_content(chunk_size=1 << 20):
                            handle.write(chunk)
                if tmp.stat().st_size < min_bytes:
                    raise OSError(f"file too small ({tmp.stat().st_size} bytes) — "
                                  "probably a login page, not a granule")
                tmp.replace(target)
                written.append(target)
                if verbose:
                    print(T(f"  downloaded {target.name} "
                            f"({target.stat().st_size/1e6:.0f} MB)",
                            f"  téléchargé {target.name} "
                            f"({target.stat().st_size/1e6:.0f} Mo)"))
                break
            except Exception as exc:  # noqa: BLE001
                for leftover in (target.with_suffix(".part"),):
                    leftover.unlink(missing_ok=True)
                if attempt == retries:
                    print(T(f"  FAILED {granule['title']}: {exc}",
                            f"  ÉCHEC {granule['title']} : {exc}"))
                elif verbose:
                    print(T(f"  retry {attempt}/{retries} for {granule['title']}",
                            f"  tentative {attempt}/{retries} pour {granule['title']}"))
    return written


# ---------------------------------------------------------------------------
#  Reading
# ---------------------------------------------------------------------------
def _find_grid_group(handle) -> str:
    """
    Locate the DNB data-field group whatever the collection layout.

    Collection 001 and 002 nest the fields differently, and NASA has moved them
    before. Walking the file is three lines and immune to that.
    """
    found: list[str] = []
    handle.visit(found.append)
    for name in found:
        if name.endswith("Data Fields") and "DNB" in name:
            return name
    for name in found:
        if name.endswith("Data Fields"):
            return name
    raise KeyError("No 'Data Fields' group found — is this really a Black Marble granule?")


def read_layer(path: str | Path, prefer: tuple[str, ...] = PREFERRED_LAYERS):
    """
    Read one radiance layer, scaled, with fill values converted to NaN.

    Returns ``(array, meta)`` where meta carries the layer name, the scale factor
    and the fill value **as read from the file**. Nothing is hard-coded: when
    NASA changes a scale factor between collection versions, this code keeps
    producing correct numbers and a constant would have produced wrong ones.
    """
    import h5py  # noqa: PLC0415

    with h5py.File(path, "r") as handle:
        group_name = _find_grid_group(handle)
        group = handle[group_name]
        layer_name = next((name for name in prefer if name in group), None)
        if layer_name is None:
            # Fall back to any 2-D dataset that looks like radiance.
            layer_name = next(
                (k for k in group if getattr(group[k], "ndim", 0) == 2), None
            )
        if layer_name is None:
            raise KeyError(f"No usable radiance layer in {Path(path).name}")

        dataset = group[layer_name]
        raw = dataset[:].astype("float32")
        attrs = dataset.attrs
        scale = float(np.ravel(attrs.get("scale_factor", 1.0))[0])
        offset = float(np.ravel(attrs.get("add_offset", 0.0))[0])
        fill = attrs.get("_FillValue", None)
        fill = float(np.ravel(fill)[0]) if fill is not None else None

    if fill is not None:
        raw[raw == fill] = np.nan
    array = raw * scale + offset

    meta = {
        "layer": layer_name,
        "group": group_name,
        "scale": scale,
        "offset": offset,
        "fill": fill,
        "shape": array.shape,
        "file": Path(path).name,
    }
    return array, meta


def tile_transform(tile: str, shape: tuple[int, int]):
    """
    The exact EPSG:4326 affine transform of a Black Marble tile.

    Every tile covers exactly 10x10 degrees, so the transform follows from the
    tile index and the array shape — no georeferencing metadata needed, and no
    dependence on a particular collection's attribute names.
    """
    from rasterio.transform import Affine  # noqa: PLC0415

    h, v = int(tile[1:3]), int(tile[4:6])
    nrow, ncol = shape
    west, north = -180.0 + h * 10.0, 90.0 - v * 10.0
    return Affine(10.0 / ncol, 0, west, 0, -10.0 / nrow, north)


# ---------------------------------------------------------------------------
#  Zonal statistics
# ---------------------------------------------------------------------------
def tile_bounds_from(transform, shape: tuple[int, int]) -> tuple[float, float, float, float]:
    """
    (west, south, east, north) of an array, for matplotlib's ``extent=``.

    Note the order: matplotlib wants [left, right, bottom, top], which is not the
    order rasterio uses. Mixing them up flips maps upside down, which is the kind
    of error that survives review because the map still looks like a map.
    """
    nrow, ncol = shape
    west = transform.c
    north = transform.f
    east = west + ncol * transform.a
    south = north + nrow * transform.e   # transform.e is negative
    return (west, south, east, north)


def rasterize_zones(gdf, transform, shape: tuple[int, int]):
    """
    Burn administrative polygons into an integer zone raster aligned to a tile.

    Pixels outside every polygon get 0. **This is the clipping**: everything the
    statistics touch afterwards is inside the national boundary by construction,
    which is what makes the numbers defensible.
    """
    from rasterio import features  # noqa: PLC0415

    shapes = ((geom, int(zid)) for geom, zid in zip(gdf.geometry, gdf["__zid__"]))
    return features.rasterize(
        shapes, out_shape=shape, transform=transform, fill=0, dtype="int32", all_touched=False
    )


def pixel_area_km2(transform, shape: tuple[int, int], latitudes=None):
    """
    Per-row pixel area in km², accounting for meridian convergence.

    A 500 m pixel at the equator and a 500 m pixel at 35°N do not cover the same
    ground area. Ignoring this is the most common quiet error in "lit area"
    figures, and it biases north-south comparisons across the continent.
    """
    nrow, ncol = shape
    deg_lat = abs(transform.e)
    deg_lon = abs(transform.a)
    rows = np.arange(nrow)
    lat_centres = transform.f + (rows + 0.5) * transform.e
    km_per_deg_lat = 110.574
    km_per_deg_lon = 111.320 * np.cos(np.radians(lat_centres))
    return (deg_lat * km_per_deg_lat) * (deg_lon * km_per_deg_lon)  # shape (nrow,)


def zonal_stats_tile(radiance, transform, zones, n_zones: int,
                     lit_threshold: float = 0.5):
    """
    Accumulate per-zone statistics for one tile.

    Returns arrays indexed by zone id (1..n_zones):
        sol       sum of radiance                     (nW·cm⁻²·sr⁻¹)
        lit_km2   area of pixels above the threshold  (km²)
        area_km2  total zone area seen in this tile   (km²)
        n_valid   count of non-NaN pixels
        rad_sum   radiance sum used for the area-weighted mean

    Vectorised with np.bincount: a country the size of DR Congo runs in seconds
    rather than the minutes a per-polygon loop would take.
    """
    flat_zones = zones.ravel()
    valid_mask = flat_zones > 0

    flat_rad = radiance.ravel()
    finite = np.isfinite(flat_rad)
    row_area = pixel_area_km2(transform, radiance.shape)
    flat_area = np.repeat(row_area, radiance.shape[1])

    use = valid_mask & finite
    idx = flat_zones[use]
    rad = flat_rad[use]
    area = flat_area[use]

    size = n_zones + 1
    sol = np.bincount(idx, weights=np.clip(rad, 0, None), minlength=size)
    n_valid = np.bincount(idx, minlength=size)
    area_km2 = np.bincount(idx, weights=area, minlength=size)
    lit = rad >= lit_threshold
    lit_km2 = np.bincount(idx[lit], weights=area[lit], minlength=size)

    return {
        "sol": sol[1:], "lit_km2": lit_km2[1:], "area_km2": area_km2[1:],
        "n_valid": n_valid[1:],
    }


def zonal_panel(files: dict[int, list[Granule]], gdf, lit_threshold: float = 0.5,
                prefer: tuple[str, ...] = PREFERRED_LAYERS, verbose: bool = True):
    """
    Build the year x administrative-unit panel — the core table of Day 4.

    Iterates year by year and tile by tile, accumulating into the zone arrays.
    Memory stays flat regardless of how many years are processed, because only
    one tile is ever held in memory at a time.

    Returns a DataFrame with one row per (year, administrative unit) and the
    columns: year, ADM*, PCODE, sol, lit_km2, area_km2, mean_rad, lit_pct.
    """
    import pandas as pd  # noqa: PLC0415

    n_zones = int(gdf["__zid__"].max())
    adm_cols = [c for c in gdf.columns if c.startswith("ADM")]
    lookup = gdf.set_index("__zid__")[adm_cols + ["PCODE"]]

    rows = []
    for year in sorted(files):
        acc = {k: np.zeros(n_zones) for k in ("sol", "lit_km2", "area_km2", "n_valid")}
        for granule in files[year]:
            try:
                radiance, _meta = read_layer(granule.path, prefer)
            except (OSError, KeyError) as exc:
                if verbose:
                    print(T(f"  skipped {granule.path.name}: {exc}",
                            f"  ignoré {granule.path.name} : {exc}"))
                continue
            transform = tile_transform(granule.tile, radiance.shape)
            zones = rasterize_zones(gdf, transform, radiance.shape)
            if not zones.any():
                continue  # this tile does not touch the country at all
            stats = zonal_stats_tile(radiance, transform, zones, n_zones, lit_threshold)
            for key in acc:
                acc[key] += stats[key]

        frame = pd.DataFrame({
            "__zid__": np.arange(1, n_zones + 1),
            "year": year,
            "sol": acc["sol"],
            "lit_km2": acc["lit_km2"],
            "area_km2": acc["area_km2"],
            "n_valid": acc["n_valid"],
        })
        rows.append(frame)
        if verbose:
            print(T(f"  {year}: SoL = {acc['sol'].sum():,.0f}",
                    f"  {year} : SoL = {acc['sol'].sum():,.0f}"))

    panel = pd.concat(rows, ignore_index=True).join(lookup, on="__zid__")
    # Mean radiance over *valid* pixels only — dividing by zone area instead
    # would quietly count NaN pixels as zeros.
    panel["mean_rad"] = np.where(panel["n_valid"] > 0, panel["sol"] / panel["n_valid"], np.nan)
    panel["lit_pct"] = np.where(panel["area_km2"] > 0,
                                100 * panel["lit_km2"] / panel["area_km2"], np.nan)
    return panel.drop(columns="__zid__")


def aggregate(panel, by: list[str]):
    """
    Roll a finer panel up to a coarser level by summing its children.

    Aggregating by summation rather than by re-running the zonal statistics at
    the coarser level is what guarantees ADM2 sums exactly to ADM1 sums exactly
    to ADM0 — the hierarchical reconciliation check of the validation step.
    """
    import pandas as pd  # noqa: PLC0415

    grouped = (panel.groupby(["year"] + by, as_index=False)
                    .agg(sol=("sol", "sum"), lit_km2=("lit_km2", "sum"),
                         area_km2=("area_km2", "sum"), n_valid=("n_valid", "sum")))
    grouped["mean_rad"] = np.where(grouped["n_valid"] > 0,
                                   grouped["sol"] / grouped["n_valid"], np.nan)
    grouped["lit_pct"] = np.where(grouped["area_km2"] > 0,
                                  100 * grouped["lit_km2"] / grouped["area_km2"], np.nan)
    return grouped


# ---------------------------------------------------------------------------
#  Small analytical helpers used by more than one laboratory
# ---------------------------------------------------------------------------
def cagr(first: float, last: float, years: int) -> float:
    """Compound annual growth rate in percent. Returns NaN for a non-positive base."""
    if first <= 0 or years <= 0:
        return float("nan")
    return ((last / first) ** (1.0 / years) - 1.0) * 100.0


def gini(values) -> float:
    """
    Gini coefficient of a distribution — used as the spatial-inequality measure.

    Applied to per-district SoL it answers "is light concentrating or spreading?",
    which is a different and more actionable question than "is there more light?".
    """
    x = np.asarray([v for v in values if np.isfinite(v) and v >= 0], dtype=float)
    if x.size == 0 or x.sum() == 0:
        return float("nan")
    x = np.sort(x)
    n = x.size
    index = np.arange(1, n + 1)
    return float((2 * np.sum(index * x)) / (n * np.sum(x)) - (n + 1) / n)


def mosaic_extent(country: Country) -> tuple[float, float, float, float]:
    """Map extent (west, east, south, north) for imshow, from the country bbox."""
    w, s, e, n = country.bbox
    return (w, e, s, n)


def describe_artefacts(lang: str = "en") -> "object":
    """The artefact catalogue as a DataFrame, for display in the Day 4 notebook."""
    import pandas as pd  # noqa: PLC0415

    fr = str(lang).startswith("fr")
    return pd.DataFrame([
        {("Artefact" if fr else "Artefact"): key.replace("_", " ").title(),
         ("Ce qu'il fait aux chiffres" if fr else "What it does to the numbers"): texts[1 if fr else 0]}
        for key, texts in ARTEFACTS.items()
    ])
