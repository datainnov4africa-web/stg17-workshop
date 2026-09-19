"""
STG17 · Night-Time Lights through Google Earth Engine — the zero-download path.

Why this module exists
----------------------
Section 7 of the concept note names bandwidth as the single most common cause of
laboratory failure. The local path (`stg17.ntl`) answers that by preparing and
mirroring the data locally in advance. Earth Engine answers it differently and
just as usefully: the
rasters never move. You send an expression, Google runs it on their copy, and a
table of numbers comes back. A country-year zonal statistic that costs 800 MB of
download locally costs a few kilobytes here.

The trade-off is honest and worth teaching:

    Local (rasterio)                    Earth Engine
    ----------------------------------  ------------------------------------
    Works with no network at all        Needs network and an account
    You hold the pixels; full control   You hold a receipt; Google holds pixels
    Reproducible on an offline machine  Reproducible only while GEE serves it
    Any product NASA publishes          Only the collections Google ingests
    Scales with your disk and RAM       Scales with Google's cluster

For a national statistical office the second column raises a real question about
dependency and continuity, which is exactly the sovereignty discussion of Day 1
afternoon. Neither path is "the right one"; the Day 4 laboratory runs both and
compares the numbers.

Collections used
----------------
    NOAA/VIIRS/DNB/ANNUAL_V22          annual VNL, 2012-2023, cloud-free average
    NOAA/VIIRS/DNB/MONTHLY_V1/VCMSLCFG monthly VIIRS, stray-light corrected
    NASA/VIIRS/002/VNP46A2             daily Black Marble, gap-filled

The annual VNL series is the Earth Engine analogue of VNP46A4 — not identical
(different processing chain, different masking) which is itself a teaching point:
two defensible pipelines give two slightly different numbers, and a statistical
office must state which one it used.
"""

from __future__ import annotations

from .countries import Country, get
from .i18n import T

# ---------------------------------------------------------------------------
#  Collections
# ---------------------------------------------------------------------------
COLLECTIONS = {
    "annual_vnl": {
        "id": "NOAA/VIIRS/DNB/ANNUAL_V22",
        "band": "average",
        "cadence": "annual",
        "range": (2012, 2023),
        "note_en": "EOG annual VIIRS Nighttime Lights, cloud-free composite",
        "note_fr": "VIIRS annuel EOG, composite sans nuages",
    },
    "monthly": {
        "id": "NOAA/VIIRS/DNB/MONTHLY_V1/VCMSLCFG",
        "band": "avg_rad",
        "cadence": "monthly",
        "range": (2014, None),
        "note_en": "Monthly VIIRS, stray-light corrected",
        "note_fr": "VIIRS mensuel, corrigé de la lumière parasite",
    },
    "black_marble_daily": {
        "id": "NASA/VIIRS/002/VNP46A2",
        "band": "Gap_Filled_DNB_BRDF_Corrected_Radiance",
        "cadence": "daily",
        "range": (2012, None),
        "note_en": "Black Marble daily, gap-filled and BRDF-corrected",
        "note_fr": "Black Marble journalier, comblé et corrigé BRDF",
    },
}

#: FAO GAUL administrative boundaries available inside Earth Engine. Convenient
#: for a first run, but *not* what a country should publish with — see
#: `stg17.boundaries` and the Day 5 documentation on authoritative boundaries.
GAUL = {
    0: "FAO/GAUL/2015/level0",
    1: "FAO/GAUL/2015/level1",
    2: "FAO/GAUL/2015/level2",
}
GAUL_NAME_FIELD = {0: "ADM0_NAME", 1: "ADM1_NAME", 2: "ADM2_NAME"}


# ---------------------------------------------------------------------------
#  Authentication
# ---------------------------------------------------------------------------
def initialise(project: str | None = None, quiet: bool = False):
    """
    Authenticate and initialise Earth Engine, in Colab or locally.

    Earth Engine now requires a Cloud project even for free non-commercial use.
    Registration is at https://code.earthengine.google.com/register and takes a
    few minutes — which is why it is on the pre-workshop checklist rather than
    something to discover on Day 4 at 09:30.

    Returns the `ee` module, already initialised.
    """
    try:
        import ee  # noqa: PLC0415
    except ImportError as exc:  # pragma: no cover
        raise ImportError(
            T("earthengine-api is not installed. Run: pip install earthengine-api geemap",
              "earthengine-api n'est pas installé. Exécutez : pip install earthengine-api geemap")
        ) from exc

    try:
        ee.Initialize(project=project) if project else ee.Initialize()
        if not quiet:
            print(T("Earth Engine ready.", "Earth Engine prêt."))
        return ee
    except Exception:  # noqa: BLE001 - first run, no stored credentials
        if not quiet:
            print(T("Earth Engine needs authorisation — a browser window will open.",
                    "Earth Engine demande une autorisation — une fenêtre va s'ouvrir."))
        ee.Authenticate()
        ee.Initialize(project=project) if project else ee.Initialize()
        if not quiet:
            print(T("Earth Engine ready.", "Earth Engine prêt."))
        return ee


def check_available() -> tuple[bool, str]:
    """Is Earth Engine importable and already authorised? Used by the environment check."""
    try:
        import ee  # noqa: PLC0415
    except ImportError:
        return False, "earthengine-api not installed"
    try:
        ee.Initialize()
        return True, "authorised"
    except Exception as exc:  # noqa: BLE001
        return False, f"installed, not authorised ({type(exc).__name__})"


# ---------------------------------------------------------------------------
#  Geometry
# ---------------------------------------------------------------------------
def country_geometry(ee, country: str | Country, level: int = 0,
                     asset: str | None = None):
    """
    A FeatureCollection of administrative units for one country.

    Uses FAO GAUL by default. Pass `asset` to point at boundaries you uploaded
    yourself — which is what a national office should do, because GAUL's
    delimitations are not necessarily those the office publishes.
    """
    c = get(country)
    if asset:
        return ee.FeatureCollection(asset)
    collection = ee.FeatureCollection(GAUL[level])
    return collection.filter(ee.Filter.eq("ADM0_NAME", _gaul_name(c)))


#: GAUL spells several country names differently from ISO. Only the divergences
#: are listed; everything else matches `Country.name_en`.
_GAUL_ALIASES = {
    "CIV": "Côte d'Ivoire",
    "COD": "Democratic Republic of the Congo",
    "TZA": "United Republic of Tanzania",
    "SWZ": "Swaziland",          # GAUL 2015 predates the rename to Eswatini
    "CPV": "Cape Verde",
    "SAH": "Western Sahara",
    "STP": "Sao Tome and Principe",
    "LBY": "Libya",
}


def _gaul_name(country: Country) -> str:
    return _GAUL_ALIASES.get(country.iso3, country.name_en)


def bbox_geometry(ee, country: str | Country):
    """A rectangle from the country bbox — cheap, and enough for a quick preview."""
    c = get(country)
    w, s, e, n = c.bbox
    return ee.Geometry.Rectangle([w, s, e, n])


# ---------------------------------------------------------------------------
#  Imagery
# ---------------------------------------------------------------------------
def annual_image(ee, year: int, collection: str = "annual_vnl", region=None):
    """
    One annual composite as an ee.Image, masked to non-negative radiance.

    Background noise in genuinely dark areas is slightly negative in the VNL
    product. Clamping at zero before summing avoids "negative light", which is
    both physically meaningless and confusing in a published table.
    """
    spec = COLLECTIONS[collection]
    image = (ee.ImageCollection(spec["id"])
             .filterDate(f"{year}-01-01", f"{year}-12-31")
             .select(spec["band"])
             .mean())
    image = image.max(0).rename("radiance")
    return image.clip(region) if region is not None else image


def monthly_image(ee, year: int, month: int, region=None):
    """One monthly composite. Useful for the seasonality artefact hunt."""
    spec = COLLECTIONS["monthly"]
    start = ee.Date.fromYMD(year, month, 1)
    image = (ee.ImageCollection(spec["id"])
             .filterDate(start, start.advance(1, "month"))
             .select(spec["band"])
             .mean()
             .max(0)
             .rename("radiance"))
    return image.clip(region) if region is not None else image


# ---------------------------------------------------------------------------
#  Zonal statistics
# ---------------------------------------------------------------------------
def zonal_year(ee, year: int, zones, scale: int = 500,
               lit_threshold: float = 0.5, collection: str = "annual_vnl"):
    """
    Sum of Lights, mean radiance and lit area per zone, for one year.

    `scale` is the resolution in metres at which Earth Engine reduces. Leaving
    it at the native 500 m keeps the result comparable with the local rasterio
    path; raising it to 1000 m makes a large country run about four times faster
    at the cost of losing small settlements. State whichever you used.
    """
    image = annual_image(ee, year, collection)
    pixel_area = ee.Image.pixelArea().divide(1e6)          # km² per pixel
    lit_area = image.gte(lit_threshold).multiply(pixel_area).rename("lit_km2")
    stack = (image.rename("sol")
             .addBands(image.rename("mean_rad"))
             .addBands(lit_area)
             .addBands(pixel_area.rename("area_km2")))

    reducer = (ee.Reducer.sum().forEachBand(image.rename("sol"))
               .combine(ee.Reducer.mean().forEachBand(image.rename("mean_rad")), sharedInputs=False)
               .combine(ee.Reducer.sum().forEachBand(lit_area), sharedInputs=False)
               .combine(ee.Reducer.sum().forEachBand(pixel_area.rename("area_km2")),
                        sharedInputs=False))

    result = stack.reduceRegions(collection=zones, reducer=reducer, scale=scale,
                                 tileScale=4)
    return result.map(lambda f: f.set("year", year))


def zonal_panel(ee, years, zones, level: int = 1, scale: int = 500,
                lit_threshold: float = 0.5, collection: str = "annual_vnl",
                verbose: bool = True):
    """
    The year x zone panel, pulled back as a pandas DataFrame.

    Returns the same column names as `stg17.ntl.zonal_panel` — year, ADM*, sol,
    lit_km2, area_km2, mean_rad, lit_pct — so a notebook can swap between the
    local path and the Earth Engine path by changing one import, and the two can
    be compared row by row.

    Uses `getInfo()`, which is capped at 5000 features per call. For a country
    with more ADM2 units than that, iterate over ADM1 groups.
    """
    import pandas as pd  # noqa: PLC0415

    name_field = GAUL_NAME_FIELD.get(level, "ADM1_NAME")
    frames = []
    for year in years:
        if verbose:
            print(T(f"  Earth Engine: {year}...", f"  Earth Engine : {year}..."))
        features = zonal_year(ee, year, zones, scale, lit_threshold, collection).getInfo()
        rows = []
        for feature in features.get("features", []):
            props = feature.get("properties", {})
            rows.append({
                "year": year,
                f"ADM{level}": props.get(name_field, ""),
                "sol": props.get("sol"),
                "mean_rad": props.get("mean_rad"),
                "lit_km2": props.get("lit_km2"),
                "area_km2": props.get("area_km2"),
            })
        frames.append(pd.DataFrame(rows))

    panel = pd.concat(frames, ignore_index=True)
    panel["lit_pct"] = 100 * panel["lit_km2"] / panel["area_km2"].clip(lower=1e-9)
    return panel


# ---------------------------------------------------------------------------
#  Interactive map
# ---------------------------------------------------------------------------
def map_year(ee, year: int, country: str | Country, level: int = 1,
             collection: str = "annual_vnl", vmax: float = 60.0):
    """
    A geemap map of one year, styled to match the workshop identity.

    Returns a `geemap.Map` — display it as the last expression of a cell. In
    Colab it is fully interactive; on GitHub the notebook shows a static
    placeholder, which is why every laboratory also saves a matplotlib figure.
    """
    import geemap  # noqa: PLC0415

    from . import theme  # noqa: PLC0415

    c = get(country)
    region = country_geometry(ee, c, level=0)
    image = annual_image(ee, year, collection, region)
    lon, lat = c.centroid

    m = geemap.Map(center=[lat, lon], zoom=6, basemap="CartoDB.DarkMatter")
    m.addLayer(image, {"min": 0, "max": vmax, "palette": theme.SEQUENTIAL_NIGHT},
               f"{c.name_en} — {year}")
    m.addLayer(country_geometry(ee, c, level=level).style(
        color="ffffff", fillColor="00000000", width=1), {}, f"ADM{level}")
    return m


def export_to_drive(ee, image, description: str, region, scale: int = 500,
                    folder: str = "STG17"):
    """
    Queue a GeoTIFF export to Google Drive.

    The bridge between the two paths: run the heavy masking and compositing on
    Google's side, then pull one clipped national raster down and continue in
    rasterio. Often the most practical option on a weak connection.
    """
    task = ee.batch.Export.image.toDrive(
        image=image, description=description, folder=folder,
        region=region.geometry() if hasattr(region, "geometry") else region,
        scale=scale, crs="EPSG:4326", maxPixels=1e10, fileFormat="GeoTIFF",
    )
    task.start()
    print(T(f"Export started: {description}. Track it at https://code.earthengine.google.com/tasks",
            f"Export lancé : {description}. Suivi sur https://code.earthengine.google.com/tasks"))
    return task
