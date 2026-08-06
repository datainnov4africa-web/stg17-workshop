"""
STG17 · Administrative boundaries for any African Union member state.

Boundaries are the backbone of every geospatial laboratory in this workshop:
they are what turns a raster of radiance into "how much light in Bouaké". Get
them wrong and every number downstream is wrong, silently.

Three sources are supported, tried in this order:

  1. **The local mirror** — what the technical assistants pre-clipped and put on
     the USB key. Always tried first: it is the only source that works without
     network, and bandwidth is the single most common cause of laboratory delay.
  2. **geoBoundaries** (www.geoboundaries.org) — open, CC BY 4.0, consistent
     ADM0-ADM3 coverage for the whole continent, downloadable without an account.
  3. **A file the participant brings** — the national boundary file from their
     own office, which is the authoritative one and the one their results should
     ultimately use.

A word on which to publish with
-------------------------------
geoBoundaries is right for a workshop: it is open, uniform and citable. It is
usually *not* right for a national publication, where the office's own official
boundaries carry the legal weight. The Day 5 publication documentation makes
this an explicit step. Boundary depiction is also politically sensitive in
several member states; neither this workshop nor the AfDB takes a position on
any delimitation, and the source is always cited in the output metadata.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from pathlib import Path

from .countries import Country, get
from .i18n import T

GEOBOUNDARIES_API = "https://www.geoboundaries.org/api/current/gbOpen/{iso3}/ADM{level}/"

#: Column names seen in the wild for the administrative unit name, in priority
#: order. geoBoundaries uses shapeName; GADM uses NAME_1/NAME_2; national files
#: use anything at all. Probing beats hard-coding.
_NAME_CANDIDATES = [
    "shapeName", "shapename", "NAME_{lvl}", "NAME{lvl}", "ADM{lvl}_EN", "ADM{lvl}_FR",
    "adm{lvl}_name", "ADM{lvl}_NAME", "name", "NAME", "nom", "NOM", "Region", "REGION",
]
_PCODE_CANDIDATES = [
    "shapeID", "shapeid", "ADM{lvl}_PCODE", "adm{lvl}_pcode", "PCODE", "pcode",
    "GID_{lvl}", "HASC_{lvl}",
]


# ---------------------------------------------------------------------------
#  Column probing
# ---------------------------------------------------------------------------
def detect_name_column(gdf, level: int) -> str | None:
    """Find the column holding the administrative unit name at this level."""
    for pattern in _NAME_CANDIDATES:
        candidate = pattern.format(lvl=level)
        if candidate in gdf.columns:
            return candidate
    # Last resort: the first string column that is not a code and not the geometry.
    for col in gdf.columns:
        if col == gdf.geometry.name:
            continue
        if gdf[col].dtype == object and not str(col).lower().endswith(("id", "code", "pcode")):
            return col
    return None


def detect_pcode_column(gdf, level: int) -> str | None:
    """Find the column holding the stable code for this level, if there is one."""
    for pattern in _PCODE_CANDIDATES:
        candidate = pattern.format(lvl=level)
        if candidate in gdf.columns:
            return candidate
    return None


# ---------------------------------------------------------------------------
#  Loading
# ---------------------------------------------------------------------------
def local_candidates(root: Path, iso3: str, level: int) -> list[Path]:
    """
    Every path the mirrored boundary file might plausibly occupy.

    Deliberately generous: the June 2026 webinar material, the DDP folder and a
    freshly built mirror all use different layouts, and a participant should not
    have to know which one they received.
    """
    iso3 = iso3.upper()
    low = iso3.lower()
    patterns = [
        f"boundaries/{iso3}/ADM{level}.geojson",
        f"boundaries/{iso3}/geoBoundaries-{iso3}-ADM{level}.geojson",
        f"boundaries/geoBoundaries-{iso3}-ADM{level}.geojson",
        f"Boundaries/{low}_admin_boundaries.shp/{low}_admin{level}.shp",
        f"Boundaries/{iso3}/ADM{level}.shp",
        f"{low}_admin_boundaries.shp/{low}_admin{level}.shp",
        f"geoBoundaries-{iso3}-ADM{level}.geojson",
        f"gadm41_{iso3}_shp/gadm41_{iso3}_{level}.shp",
    ]
    return [root / p for p in patterns]


def find_local(root: Path, iso3: str, level: int) -> Path | None:
    """First existing mirrored boundary file for this country and level."""
    for candidate in local_candidates(Path(root), iso3, level):
        if candidate.exists():
            return candidate
    # Fall back to a recursive search, which is slower but rescues odd layouts.
    root = Path(root)
    if root.exists():
        for pattern in (f"*{iso3.upper()}*ADM{level}*.geojson",
                        f"*{iso3.lower()}*admin{level}*.shp",
                        f"*{iso3.upper()}*_{level}.shp"):
            matches = sorted(root.rglob(pattern))
            if matches:
                return matches[0]
    return None


def geoboundaries_url(iso3: str, level: int) -> str | None:
    """
    Ask the geoBoundaries API for the direct download URL of one ADM level.

    Returns None rather than raising when the country/level combination does not
    exist — several small states publish no ADM2 at all, and a laboratory must
    degrade to the level that does exist instead of failing.
    """
    url = GEOBOUNDARIES_API.format(iso3=iso3.upper(), level=level)
    try:
        with urllib.request.urlopen(url, timeout=30) as response:  # noqa: S310
            payload = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, OSError):
        return None
    if isinstance(payload, list):
        payload = payload[0] if payload else {}
    return payload.get("gjDownloadURL") or payload.get("simplifiedGeometryGeoJSON")


def download(iso3: str, level: int, dest_dir: Path) -> Path | None:
    """Fetch one ADM level from geoBoundaries into the local mirror. Idempotent."""
    dest_dir = Path(dest_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / f"geoBoundaries-{iso3.upper()}-ADM{level}.geojson"
    if dest.exists() and dest.stat().st_size > 1024:
        return dest

    url = geoboundaries_url(iso3, level)
    if not url:
        return None
    print(T(f"Downloading {iso3} ADM{level} from geoBoundaries...",
            f"Téléchargement de {iso3} ADM{level} depuis geoBoundaries..."))
    try:
        urllib.request.urlretrieve(url, dest)  # noqa: S310
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        print(T(f"  download failed: {exc}", f"  échec du téléchargement : {exc}"))
        return None
    return dest


def load(country: str | Country,
         level: int = 1,
         root: str | Path | None = None,
         path: str | Path | None = None,
         allow_download: bool = True):
    """
    Load one administrative level as a GeoDataFrame, normalised and repaired.

    The returned frame always carries:
      * ``ADM0`` … ``ADM{level}``  — unit names, whatever the source called them
      * ``PCODE``                  — a stable code when the source has one
      * ``ISO3``                   — the country code
      * geometry in **EPSG:4326**, with invalid rings repaired

    Normalising here rather than in each notebook is what lets the same analysis
    code run over geoBoundaries, GADM and a national shapefile without a single
    conditional.
    """
    import geopandas as gpd  # noqa: PLC0415

    c = get(country)
    src: Path | None = Path(path) if path else None

    if src is None and root is not None:
        src = find_local(Path(root), c.iso3, level)

    if src is None and allow_download:
        target_dir = Path(root or ".") / "boundaries" / c.iso3
        src = download(c.iso3, level, target_dir)

    if src is None:
        raise FileNotFoundError(
            T(f"No ADM{level} boundary found for {c.name_en} ({c.iso3}). "
              f"Either put the file on the USB-key mirror, pass path=..., "
              f"or check that geoBoundaries publishes ADM{level} for this country.",
              f"Aucune frontière ADM{level} trouvée pour {c.name_fr} ({c.iso3}). "
              f"Placez le fichier dans le miroir de la clé USB, passez path=..., "
              f"ou vérifiez que geoBoundaries publie l'ADM{level} pour ce pays.")
        )

    gdf = gpd.read_file(src)

    # -- CRS: assume WGS84 when the source forgot to say, then reproject -------
    if gdf.crs is None:
        gdf = gdf.set_crs("EPSG:4326")
    elif gdf.crs.to_epsg() != 4326:
        gdf = gdf.to_crs("EPSG:4326")

    # -- Geometry repair: self-intersecting rings break zonal statistics -------
    invalid = ~gdf.geometry.is_valid
    if invalid.any():
        gdf.loc[invalid, "geometry"] = gdf.loc[invalid, "geometry"].buffer(0)

    # -- Normalise the naming columns -----------------------------------------
    for lvl in range(level + 1):
        col = detect_name_column(gdf, lvl) if lvl == level else None
        if lvl == 0:
            gdf["ADM0"] = c.name_en
        elif col:
            gdf[f"ADM{lvl}"] = gdf[col].astype(str).str.strip()
        elif f"ADM{lvl}" not in gdf.columns:
            # A parent level absent from a child file: fill from a matching column
            # if one exists, otherwise leave it blank rather than inventing it.
            guess = detect_name_column(gdf, lvl)
            gdf[f"ADM{lvl}"] = gdf[guess].astype(str).str.strip() if guess else ""

    pcode = detect_pcode_column(gdf, level)
    gdf["PCODE"] = gdf[pcode].astype(str) if pcode else [
        f"{c.iso3}-{level}-{i:04d}" for i in range(len(gdf))
    ]
    gdf["ISO3"] = c.iso3
    gdf["__zid__"] = range(1, len(gdf) + 1)   # integer id used to rasterize zones
    gdf.attrs["source_file"] = str(src)
    gdf.attrs["source_name"] = _source_label(src)
    gdf.attrs["level"] = level
    return gdf


def _source_label(path: Path) -> str:
    name = str(path).lower()
    if "geoboundaries" in name:
        return "geoBoundaries (gbOpen, CC BY 4.0)"
    if "gadm" in name:
        return "GADM 4.1 (academic use — check licence before publishing)"
    return f"national file: {Path(path).name}"


def load_levels(country: str | Country,
                levels: tuple[int, ...] = (0, 1, 2),
                root: str | Path | None = None,
                allow_download: bool = True) -> dict[int, object]:
    """
    Load several levels at once, skipping any the country does not publish.

    Returns {level: GeoDataFrame}. A country with no ADM2 simply comes back with
    two entries, and the notebook adapts its finest analysis level accordingly
    rather than crashing halfway through.
    """
    out = {}
    for lvl in levels:
        try:
            out[lvl] = load(country, lvl, root=root, allow_download=allow_download)
        except (FileNotFoundError, ValueError) as exc:
            print(T(f"ADM{lvl} unavailable — skipped ({type(exc).__name__})",
                    f"ADM{lvl} indisponible — ignoré ({type(exc).__name__})"))
    return out


def summary(levels: dict[int, object]) -> str:
    """One line describing what was loaded — printed by every geospatial lab."""
    parts = [f"ADM{lvl}: {len(gdf)}" for lvl, gdf in sorted(levels.items())]
    return "  ".join(parts)


def finest_level(levels: dict[int, object]) -> int:
    """The deepest level actually available — the analysis level for zonal stats."""
    return max(levels) if levels else 0
