"""
STG17 workshop toolkit — Emerging Issues, Emerging Practice.

African Development Bank (Secretariat of STG17) with AU STATAFRIC,
under SHaSA II · STG17 Action Plan 2025-2030, Work Package 4.2.

The whole point of this package is that a laboratory notebook contains
*statistics*, not plumbing. Boundary column probing, tile georeferencing,
bilingual strings, dependency installation and the AfDB identity all live here,
so the notebook a participant reads shows the method and nothing else.

Typical first two cells of any laboratory
-----------------------------------------
    !pip install -q "stg17 @ git+https://github.com/datainnov4africa-web/stg17-workshop"

    from stg17 import setup, countries, ui
    S = setup({"geopandas": "geopandas>=0.14"}, lang="EN")
    COUNTRY = countries.get("CIV")      # <- the only line a participant changes

Modules
-------
    countries   the 55 African Union member states, VIIRS tiles, UTM zones
    env         platform detection, dependency install, secrets, data root
    i18n        EN/FR runtime, shared glossary
    theme       the AfDB palette and the matplotlib style
    ui          hero, step, key_concept, checkpoint, deliverable, limitations
    boundaries  administrative boundaries from a mirror, geoBoundaries or a file
    ntl         Black Marble HDF5 -> validated zonal statistics
    ntl_gee     the same, through Google Earth Engine, with nothing downloaded
"""

from __future__ import annotations

__version__ = "0.1.0"
__all__ = [
    "boundaries",
    "countries",
    "env",
    "i18n",
    "ntl",
    "ntl_gee",
    "setup",
    "theme",
    "ui",
    "T",
    "set_lang",
]

from . import boundaries, countries, env, i18n, ntl, theme, ui
from .env import setup
from .i18n import T, set_lang

# ntl_gee is imported lazily: it must not fail on a machine without the Earth
# Engine client, and most laboratories never touch it.
def __getattr__(name):  # pragma: no cover
    if name == "ntl_gee":
        from . import ntl_gee as module
        return module
    raise AttributeError(f"module 'stg17' has no attribute {name!r}")
