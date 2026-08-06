"""
STG17 · Country registry — the single knob that makes every laboratory portable.

Every notebook in this workshop starts with one line:

    COUNTRY_ISO3 = "CIV"      # <- change this, and nothing else

Everything downstream — boundaries, VIIRS tile selection, WorldPop code, map
extent, figure titles, output filenames — is resolved from this registry.

Coverage: the 55 member states of the African Union.

--------------------------------------------------------------------------
A NOTE ON THE BOUNDING BOXES  (read this before trusting them)
--------------------------------------------------------------------------
The `bbox` stored here is a deliberately *generous* approximation. It is used
for two things only:

  1. selecting which 10x10 degree Black Marble tiles to download, and
  2. setting a default map extent before the real boundary file is loaded.

It is NEVER used to clip data. Clipping is always done against the official
administrative boundary polygons loaded by `stg17.boundaries`. A bbox that is
slightly too large therefore costs one extra tile download at worst; it cannot
bias a statistic. If you find a bbox that is too *small* for your country,
that is a bug — please open an issue, it would silently drop territory.

Several states have overseas or outlying islands (Mauritius, Seychelles,
Equatorial Guinea, Cabo Verde...). Their bboxes span the full archipelago,
which is why some look surprisingly wide.
"""

from __future__ import annotations

import math
import unicodedata
from dataclasses import dataclass, field
from typing import Iterable

# ---------------------------------------------------------------------------
# AU regional groupings. Indicative only: the African Union places Angola in
# both its Central and Southern regions, and practice varies for Malawi and
# Burundi. Used here purely to group countries in menus and reports.
# ---------------------------------------------------------------------------
REGIONS_EN = {
    "north": "North Africa",
    "west": "West Africa",
    "central": "Central Africa",
    "east": "East Africa",
    "southern": "Southern Africa",
}
REGIONS_FR = {
    "north": "Afrique du Nord",
    "west": "Afrique de l'Ouest",
    "central": "Afrique centrale",
    "east": "Afrique de l'Est",
    "southern": "Afrique australe",
}


@dataclass(frozen=True)
class Country:
    """One African Union member state, with everything a laboratory needs."""

    iso3: str
    iso2: str
    name_en: str
    name_fr: str
    region: str
    bbox: tuple[float, float, float, float]  # (west, south, east, north) in EPSG:4326
    note: str = ""

    # -- derived ------------------------------------------------------------
    @property
    def worldpop_code(self) -> str:
        """WorldPop uses the lowercase ISO3 code in every filename and URL."""
        return self.iso3.lower()

    @property
    def centroid(self) -> tuple[float, float]:
        """(lon, lat) centre of the bbox — a default map centre, not a real centroid."""
        w, s, e, n = self.bbox
        return ((w + e) / 2.0, (s + n) / 2.0)

    @property
    def viirs_tiles(self) -> list[str]:
        """
        Black Marble (VNP46A*) tiles covering this country.

        The Black Marble grid divides the globe into 10x10 degree tiles:
            h = floor((lon + 180) / 10)      h in 0..35, west to east
            v = floor((90 - lat) / 10)       v in 0..17, north to south

        We return every tile the bbox touches. Small countries need 1 tile,
        Algeria and DR Congo need 6.
        """
        w, s, e, n = self.bbox
        h0, h1 = int((w + 180) // 10), int((min(e, 179.999) + 180) // 10)
        v0, v1 = int((90 - min(n, 89.999)) // 10), int((90 - s) // 10)
        return [f"h{h:02d}v{v:02d}" for v in range(v0, v1 + 1) for h in range(h0, h1 + 1)]

    @property
    def area_deg2(self) -> float:
        """Bbox area in square degrees — a rough proxy for how heavy processing will be."""
        w, s, e, n = self.bbox
        return (e - w) * (n - s)

    def name(self, lang: str = "en") -> str:
        return self.name_fr if str(lang).lower().startswith("fr") else self.name_en

    def region_name(self, lang: str = "en") -> str:
        table = REGIONS_FR if str(lang).lower().startswith("fr") else REGIONS_EN
        return table[self.region]

    def utm_epsg(self) -> int:
        """
        Best-fit UTM zone EPSG code for the country centre.

        Needed whenever an area or a distance is computed: doing zonal statistics
        in degrees silently inflates areas near the equator relative to the poles.
        Northern hemisphere -> 326xx, southern -> 327xx.
        """
        lon, lat = self.centroid
        zone = int((lon + 180) / 6) + 1
        return (32600 if lat >= 0 else 32700) + zone

    def __str__(self) -> str:  # pragma: no cover - cosmetic
        return f"{self.name_en} ({self.iso3})"


# ---------------------------------------------------------------------------
#  The registry — 55 African Union member states
#  bbox = (west, south, east, north)
# ---------------------------------------------------------------------------
_REGISTRY: list[Country] = [
    # ---------------------------- NORTH ------------------------------------
    Country("DZA", "DZ", "Algeria", "Algérie", "north", (-8.70, 18.90, 12.00, 37.15)),
    Country("EGY", "EG", "Egypt", "Égypte", "north", (24.65, 21.70, 36.95, 31.70)),
    Country("LBY", "LY", "Libya", "Libye", "north", (9.30, 19.45, 25.20, 33.20)),
    Country("MAR", "MA", "Morocco", "Maroc", "north", (-13.25, 27.60, -0.95, 35.95)),
    Country("MRT", "MR", "Mauritania", "Mauritanie", "north", (-17.10, 14.70, -4.80, 27.35)),
    Country("SAH", "EH", "Sahrawi Arab Democratic Republic",
            "République arabe sahraouie démocratique", "north", (-17.15, 20.75, -8.65, 27.70),
            note="Boundary datasets vary; geoBoundaries publishes this territory as ESH."),
    Country("TUN", "TN", "Tunisia", "Tunisie", "north", (7.50, 30.20, 11.65, 37.60),
            note="Ookla reference country for Day 3 — four quarters of 2024 mirrored."),

    # ---------------------------- WEST -------------------------------------
    Country("BEN", "BJ", "Benin", "Bénin", "west", (0.75, 6.20, 3.90, 12.45)),
    Country("BFA", "BF", "Burkina Faso", "Burkina Faso", "west", (-5.55, 9.35, 2.45, 15.10)),
    Country("CPV", "CV", "Cabo Verde", "Cabo Verde", "west", (-25.40, 14.75, -22.65, 17.25),
            note="Archipelago — small land area spread over a wide bbox."),
    Country("CIV", "CI", "Côte d'Ivoire", "Côte d'Ivoire", "west", (-8.65, 4.30, -2.45, 10.80),
            note="Night-Time Lights reference country — VNP46A4 2012-2025 and ADM0-3 prepared."),
    Country("GMB", "GM", "Gambia", "Gambie", "west", (-16.85, 13.05, -13.75, 13.85)),
    Country("GHA", "GH", "Ghana", "Ghana", "west", (-3.30, 4.70, 1.25, 11.20)),
    Country("GIN", "GN", "Guinea", "Guinée", "west", (-15.10, 7.15, -7.60, 12.70)),
    Country("GNB", "GW", "Guinea-Bissau", "Guinée-Bissau", "west", (-16.75, 10.85, -13.60, 12.70)),
    Country("LBR", "LR", "Liberia", "Libéria", "west", (-11.55, 4.30, -7.35, 8.60)),
    Country("MLI", "ML", "Mali", "Mali", "west", (-12.30, 10.10, 4.30, 25.05)),
    Country("NER", "NE", "Niger", "Niger", "west", (0.15, 11.65, 16.00, 23.55)),
    Country("NGA", "NG", "Nigeria", "Nigéria", "west", (2.65, 4.25, 14.70, 13.90)),
    Country("SEN", "SN", "Senegal", "Sénégal", "west", (-17.55, 12.30, -11.30, 16.70)),
    Country("SLE", "SL", "Sierra Leone", "Sierra Leone", "west", (-13.35, 6.85, -10.25, 10.05)),
    Country("TGO", "TG", "Togo", "Togo", "west", (-0.20, 6.05, 1.85, 11.20)),

    # ---------------------------- CENTRAL ----------------------------------
    Country("BDI", "BI", "Burundi", "Burundi", "central", (28.95, -4.50, 30.90, -2.25),
            note="WorldPop rasters 2015-2030 already mirrored in the workshop material."),
    Country("CMR", "CM", "Cameroon", "Cameroun", "central", (8.45, 1.60, 16.25, 13.10)),
    Country("CAF", "CF", "Central African Republic", "République centrafricaine",
            "central", (14.40, 2.20, 27.50, 11.05)),
    Country("TCD", "TD", "Chad", "Tchad", "central", (13.40, 7.40, 24.05, 23.50)),
    Country("COG", "CG", "Congo", "Congo", "central", (11.15, -5.10, 18.70, 3.75)),
    Country("COD", "CD", "Democratic Republic of the Congo",
            "République démocratique du Congo", "central", (12.15, -13.50, 31.35, 5.45)),
    Country("GNQ", "GQ", "Equatorial Guinea", "Guinée équatoriale", "central",
            (5.55, -1.50, 11.40, 3.85), note="Mainland plus Bioko and Annobón islands."),
    Country("GAB", "GA", "Gabon", "Gabon", "central", (8.65, -4.00, 14.55, 2.35)),
    Country("STP", "ST", "Sao Tome and Principe", "Sao Tomé-et-Principe", "central",
            (6.35, -0.05, 7.50, 1.80)),

    # ---------------------------- EAST -------------------------------------
    Country("COM", "KM", "Comoros", "Comores", "east", (43.15, -12.45, 44.60, -11.30)),
    Country("DJI", "DJ", "Djibouti", "Djibouti", "east", (41.70, 10.85, 43.50, 12.75)),
    Country("ERI", "ER", "Eritrea", "Érythrée", "east", (36.40, 12.30, 43.20, 18.05)),
    Country("ETH", "ET", "Ethiopia", "Éthiopie", "east", (32.95, 3.35, 48.05, 14.95)),
    Country("KEN", "KE", "Kenya", "Kenya", "east", (33.85, -4.75, 41.95, 5.10),
            note="WorldPop rasters and geoBoundaries ADM0-3 already mirrored."),
    Country("MDG", "MG", "Madagascar", "Madagascar", "east", (43.15, -25.65, 50.55, -11.90)),
    Country("MUS", "MU", "Mauritius", "Maurice", "east", (56.50, -20.60, 63.60, -10.30),
            note="Bbox spans Rodrigues and the Agalega islands."),
    Country("RWA", "RW", "Rwanda", "Rwanda", "east", (28.80, -2.90, 30.95, -1.00)),
    Country("SYC", "SC", "Seychelles", "Seychelles", "east", (46.15, -10.30, 56.35, -3.65),
            note="115 islands spread over 1.3 million km2 of ocean."),
    Country("SOM", "SO", "Somalia", "Somalie", "east", (40.95, -1.70, 51.50, 12.05)),
    Country("SSD", "SS", "South Sudan", "Soudan du Sud", "east", (24.10, 3.45, 36.00, 12.30)),
    Country("SDN", "SD", "Sudan", "Soudan", "east", (21.80, 8.60, 38.65, 22.30),
            note="Second Night-Time Lights reference country — conflict-impact use case."),
    Country("TZA", "TZ", "United Republic of Tanzania", "République-Unie de Tanzanie",
            "east", (29.30, -11.80, 40.50, -0.95),
            note="WorldPop rasters 2015-2030 already mirrored."),
    Country("UGA", "UG", "Uganda", "Ouganda", "east", (29.50, -1.55, 35.10, 4.30),
            note="WorldPop rasters 2015-2030 already mirrored."),

    # ---------------------------- SOUTHERN ---------------------------------
    Country("AGO", "AO", "Angola", "Angola", "southern", (11.60, -18.10, 24.15, -4.30),
            note="The AU places Angola in both its Central and Southern regions."),
    Country("BWA", "BW", "Botswana", "Botswana", "southern", (19.95, -26.95, 29.40, -17.75)),
    Country("SWZ", "SZ", "Eswatini", "Eswatini", "southern", (30.75, -27.35, 32.20, -25.70)),
    Country("LSO", "LS", "Lesotho", "Lesotho", "southern", (26.95, -30.70, 29.50, -28.55)),
    Country("MWI", "MW", "Malawi", "Malawi", "southern", (32.60, -17.20, 36.00, -9.30)),
    Country("MOZ", "MZ", "Mozambique", "Mozambique", "southern", (30.15, -26.90, 40.90, -10.40)),
    Country("NAM", "NA", "Namibia", "Namibie", "southern", (11.65, -29.00, 25.30, -16.90)),
    Country("ZAF", "ZA", "South Africa", "Afrique du Sud", "southern", (16.40, -34.90, 32.95, -22.10),
            note="Bbox excludes the Prince Edward Islands, which carry no night-time lights."),
    Country("ZMB", "ZM", "Zambia", "Zambie", "southern", (21.95, -18.10, 33.75, -8.15)),
    Country("ZWE", "ZW", "Zimbabwe", "Zimbabwe", "southern", (25.20, -22.45, 33.10, -15.55)),
]

BY_ISO3: dict[str, Country] = {c.iso3: c for c in _REGISTRY}
BY_ISO2: dict[str, Country] = {c.iso2: c for c in _REGISTRY}

#: The country prepared end to end, handed to any team whose national data
#: proves incomplete. Named in section 6 of the concept note.
REFERENCE_COUNTRY = "CIV"


# ---------------------------------------------------------------------------
#  Lookup
# ---------------------------------------------------------------------------
def _fold(s: str) -> str:
    """Lowercase and strip accents, so 'Cote d Ivoire' finds 'Côte d'Ivoire'."""
    s = unicodedata.normalize("NFKD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    return "".join(ch for ch in s.lower() if ch.isalnum())


_NAME_INDEX = {}
for _c in _REGISTRY:
    _NAME_INDEX[_fold(_c.name_en)] = _c
    _NAME_INDEX[_fold(_c.name_fr)] = _c


def get(code_or_name: str) -> Country:
    """
    Resolve a country from an ISO3 code, an ISO2 code, or a name in EN or FR.

    Accepts sloppy input on purpose — participants type what they know:

        get("CIV") == get("civ") == get("CI")
                   == get("Cote d'Ivoire") == get("Côte d'Ivoire")

    Raises a KeyError carrying a useful suggestion, never a bare one.
    """
    if isinstance(code_or_name, Country):
        return code_or_name
    raw = str(code_or_name).strip()
    key = raw.upper()
    if key in BY_ISO3:
        return BY_ISO3[key]
    if key in BY_ISO2:
        return BY_ISO2[key]
    folded = _fold(raw)
    if folded in _NAME_INDEX:
        return _NAME_INDEX[folded]
    # Not found: offer the closest matches rather than a dead end.
    near = sorted(
        (c for c in _REGISTRY),
        key=lambda c: -_similarity(folded, _fold(c.name_en)),
    )[:3]
    hint = ", ".join(f"{c.name_en} ({c.iso3})" for c in near)
    raise KeyError(
        f"Unknown country: {raw!r}. "
        f"Did you mean one of: {hint}? "
        f"Use stg17.countries.table() to list all 55 AU member states."
    )


def _similarity(a: str, b: str) -> float:
    """Cheap character-bigram overlap — good enough to suggest 'did you mean'."""
    if not a or not b:
        return 0.0
    ga = {a[i:i + 2] for i in range(len(a) - 1)} or {a}
    gb = {b[i:i + 2] for i in range(len(b) - 1)} or {b}
    return len(ga & gb) / max(len(ga | gb), 1)


def all_countries(region: str | None = None) -> list[Country]:
    """Every AU member state, optionally filtered to one region, sorted by English name."""
    out = [c for c in _REGISTRY if region is None or c.region == region]
    return sorted(out, key=lambda c: c.name_en)


def iso3_codes() -> list[str]:
    return sorted(BY_ISO3)


def table(lang: str = "en", region: str | None = None):
    """
    Return the registry as a pandas DataFrame — handy in a notebook to let a
    participant find their country and see how heavy its rasters will be.
    """
    import pandas as pd

    fr = str(lang).lower().startswith("fr")
    rows = []
    for c in all_countries(region):
        rows.append(
            {
                "ISO3": c.iso3,
                ("Pays" if fr else "Country"): c.name(lang),
                ("Région" if fr else "Region"): c.region_name(lang),
                ("Tuiles VIIRS" if fr else "VIIRS tiles"): " ".join(c.viirs_tiles),
                ("Nb tuiles" if fr else "N tiles"): len(c.viirs_tiles),
                "UTM EPSG": c.utm_epsg(),
            }
        )
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
#  Tile helpers (usable without a Country object)
# ---------------------------------------------------------------------------
def tiles_for_bbox(bbox: Iterable[float]) -> list[str]:
    """Black Marble tiles intersecting an arbitrary (west, south, east, north) bbox."""
    w, s, e, n = bbox
    h0, h1 = int((w + 180) // 10), int((min(e, 179.999) + 180) // 10)
    v0, v1 = int((90 - min(n, 89.999)) // 10), int((90 - s) // 10)
    return [f"h{h:02d}v{v:02d}" for v in range(v0, v1 + 1) for h in range(h0, h1 + 1)]


def tile_bounds(tile: str) -> tuple[float, float, float, float]:
    """Inverse of the above: the (west, south, east, north) extent of one tile."""
    h, v = int(tile[1:3]), int(tile[4:6])
    west = -180.0 + h * 10.0
    north = 90.0 - v * 10.0
    return (west, north - 10.0, west + 10.0, north)


def estimate_download_mb(country: Country, years: int = 1, product: str = "VNP46A4") -> float:
    """
    Rough download volume, so a participant on a weak connection knows what they
    are committing to before they start. Annual tiles run ~55 MB, monthly ~45 MB.

    These are order-of-magnitude figures observed on the workshop mirror, not a
    guarantee — compression varies a lot between a desert tile and a coastal one.
    """
    per_tile = {"VNP46A4": 55.0, "VNP46A3": 45.0, "VNP46A2": 12.0}.get(product, 50.0)
    multiplier = 12 if product == "VNP46A3" else 1
    return len(country.viirs_tiles) * per_tile * years * multiplier


# ---------------------------------------------------------------------------
#  Self-check — run `python -m stg17.countries` to validate the registry
# ---------------------------------------------------------------------------
def _self_check() -> list[str]:
    problems = []
    seen = set()
    for c in _REGISTRY:
        if c.iso3 in seen:
            problems.append(f"duplicate ISO3 {c.iso3}")
        seen.add(c.iso3)
        w, s, e, n = c.bbox
        if not (w < e and s < n):
            problems.append(f"{c.iso3}: malformed bbox {c.bbox}")
        if not (-180 <= w and e <= 180 and -90 <= s and n <= 90):
            problems.append(f"{c.iso3}: bbox out of range {c.bbox}")
        if c.region not in REGIONS_EN:
            problems.append(f"{c.iso3}: unknown region {c.region!r}")
        if not c.viirs_tiles:
            problems.append(f"{c.iso3}: no VIIRS tile resolved")
    if len(_REGISTRY) != 55:
        problems.append(f"expected 55 AU member states, registry holds {len(_REGISTRY)}")
    return problems


if __name__ == "__main__":  # pragma: no cover
    issues = _self_check()
    print(f"STG17 country registry: {len(_REGISTRY)} African Union member states")
    heaviest = max(_REGISTRY, key=lambda c: len(c.viirs_tiles))
    print(f"Most VIIRS tiles: {heaviest.name_en} -> {len(heaviest.viirs_tiles)} "
          f"({' '.join(heaviest.viirs_tiles)})")
    if issues:
        print("\nPROBLEMS:")
        for p in issues:
            print("  -", p)
        raise SystemExit(1)
    print("Self-check passed.")
