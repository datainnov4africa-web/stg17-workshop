"""
STG17 · The African Development Bank visual identity, in one place.

Notebooks, the workshop website and the reveal.js slide decks all read their
colours from here (the site and slides via the generated CSS custom properties
in `docs/assets/afdb.css` and `slides/theme/afdb.css`, which are produced by
`python -m stg17.theme --emit-css`).

Change a colour here, run the emit command, and the whole workshop follows.

--------------------------------------------------------------------------
PROVENANCE OF THE PALETTE
--------------------------------------------------------------------------
These values are reconstructed from the finalised STG17 webinar material of
June 2026 (the Côte d'Ivoire and Sudan Night-Time Lights notebooks), not from
an official AfDB brand charter. If the Communications department supplies the
charter, substitute the hex values below and regenerate — nothing else in the
repository hard-codes a colour.
"""

from __future__ import annotations

from pathlib import Path

# ---------------------------------------------------------------------------
#  Core palette
# ---------------------------------------------------------------------------
NAVY = "#0B2545"      # headings, axis labels, the "authority" colour
GREEN = "#1B7A43"     # primary accent — AfDB jade
AMBER = "#F2A900"     # secondary accent, highlights, callouts
INK = "#33403A"       # body text on light backgrounds
MUTED = "#6B7B75"     # captions, secondary text
LINE = "#D5E6DF"      # hairlines, table borders
WASH = "#F4F8F5"      # tinted panel background
PAPER = "#FBFCFB"     # page background
WHITE = "#FFFFFF"

# Semantic colours — used by the pass/fail tables in the environment check and
# by the validation step of every laboratory.
OK = "#1B7A43"
WARN = "#F2A900"
FAIL = "#C0392B"
INFO = "#1D5FA8"

#: Categorical sequence for charts with several series. Ordered so that the
#: first three carry the AfDB identity and the rest stay distinguishable in
#: greyscale and for the most common forms of colour vision deficiency.
CATEGORICAL = [GREEN, NAVY, AMBER, "#1D5FA8", "#8E4585", "#C0392B", "#5D7052", "#B07D2B"]

#: Sequential ramp for radiance, population density, download speed — anything
#: that runs from "none" to "a lot". Dark background on purpose: night-time
#: lights read far better on a dark ramp.
SEQUENTIAL_NIGHT = ["#08090F", "#1A1E33", "#3B2F63", "#8A3B6B", "#D4574E", "#F2A900", "#FFF3C4"]

#: Diverging ramp for change detection (loss <-> gain).
DIVERGING = ["#7B3294", "#C2A5CF", "#F7F7F7", "#A6DBA0", "#1B7A43"]


def register_matplotlib(dpi: int = 110, dark: bool = False) -> None:
    """
    Apply the AfDB look to every subsequent matplotlib figure.

    Call once, near the top of a notebook. Everything after it — including
    figures produced inside library code — inherits the identity, so no
    laboratory needs to restyle its charts by hand.
    """
    import matplotlib as mpl
    from matplotlib.colors import LinearSegmentedColormap
    from cycler import cycler

    fg = WHITE if dark else INK
    bg = "#0E1520" if dark else WHITE
    grid = "#2A3441" if dark else LINE

    mpl.rcParams.update(
        {
            "figure.dpi": dpi,
            "savefig.dpi": dpi,
            "figure.facecolor": bg,
            "savefig.facecolor": bg,
            "axes.facecolor": bg,
            "axes.edgecolor": grid,
            "axes.labelcolor": fg,
            "axes.titlecolor": WHITE if dark else NAVY,
            "axes.titleweight": "bold",
            "axes.titlesize": 12,
            "axes.labelsize": 10,
            "axes.grid": True,
            "axes.axisbelow": True,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.prop_cycle": cycler(color=CATEGORICAL),
            "grid.color": grid,
            "grid.alpha": 0.45 if dark else 0.30,
            "grid.linewidth": 0.7,
            "text.color": fg,
            "xtick.color": fg,
            "ytick.color": fg,
            "xtick.labelsize": 9,
            "ytick.labelsize": 9,
            "legend.frameon": False,
            "legend.fontsize": 9,
            "font.size": 10,
            "font.family": "sans-serif",
            "font.sans-serif": ["Segoe UI", "DejaVu Sans", "Arial", "Liberation Sans"],
            "figure.autolayout": False,
            "figure.constrained_layout.use": True,
        }
    )

    # Register the two named colormaps so they can be used as cmap="stg17_night".
    for name, colours in (("stg17_night", SEQUENTIAL_NIGHT), ("stg17_change", DIVERGING)):
        try:
            mpl.colormaps.register(
                LinearSegmentedColormap.from_list(name, colours), name=name, force=True
            )
        except (AttributeError, ValueError):  # older matplotlib, or already registered
            pass


def credit(ax, text: str = "", lang: str = "en") -> None:
    """
    Stamp the standard source line under a figure.

    Every chart that leaves this workshop carries its provenance. That is not
    decoration: an unattributed figure cannot be published by a statistical
    office, and the Friday deliverables are meant to be publishable.
    """
    default = ("Source : atelier STG17 · BAD / STATAFRIC" if lang.startswith("fr")
               else "Source: STG17 workshop · AfDB / STATAFRIC")
    ax.figure.text(
        0.005, -0.02, text or default,
        ha="left", va="top", fontsize=7.5, color=MUTED,
    )


# ---------------------------------------------------------------------------
#  CSS generation — keeps the site and the slides in lockstep with the notebooks
# ---------------------------------------------------------------------------
_CSS_TEMPLATE = """/* ===========================================================================
   STG17 workshop — African Development Bank identity
   GENERATED FILE. Do not edit by hand.
   Source: stg17/theme.py   Regenerate: python -m stg17.theme --emit-css
   =========================================================================== */
:root {{
  --afdb-navy:  {NAVY};
  --afdb-green: {GREEN};
  --afdb-amber: {AMBER};
  --afdb-ink:   {INK};
  --afdb-muted: {MUTED};
  --afdb-line:  {LINE};
  --afdb-wash:  {WASH};
  --afdb-paper: {PAPER};
  --afdb-ok:    {OK};
  --afdb-warn:  {WARN};
  --afdb-fail:  {FAIL};
  --afdb-info:  {INFO};
  --afdb-font:  "Segoe UI", "Inter", system-ui, -apple-system, "Helvetica Neue", sans-serif;
  --afdb-mono:  "JetBrains Mono", "Cascadia Code", "Consolas", ui-monospace, monospace;
  --afdb-radius: 10px;
  --afdb-shadow: 0 1px 3px rgba(11, 37, 69, .08), 0 8px 24px rgba(11, 37, 69, .06);
}}
"""


def emit_css(path: str | Path) -> Path:
    """Write the custom-property block that the site and the slide theme import."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(
        _CSS_TEMPLATE.format(
            NAVY=NAVY, GREEN=GREEN, AMBER=AMBER, INK=INK, MUTED=MUTED,
            LINE=LINE, WASH=WASH, PAPER=PAPER, OK=OK, WARN=WARN, FAIL=FAIL, INFO=INFO,
        ),
        encoding="utf-8",
    )
    return p


if __name__ == "__main__":  # pragma: no cover
    import argparse

    ap = argparse.ArgumentParser(description="STG17 theme utilities")
    ap.add_argument("--emit-css", action="store_true",
                    help="regenerate the CSS variable blocks for the site and the slides")
    args = ap.parse_args()

    if args.emit_css:
        root = Path(__file__).resolve().parent.parent
        for target in (root / "docs/assets/_afdb-vars.css",
                       root / "docs/slides/theme/_afdb-vars.css"):
            print("wrote", emit_css(target))
    else:
        for name, value in [("navy", NAVY), ("green", GREEN), ("amber", AMBER)]:
            print(f"{name:>6}: {value}")
