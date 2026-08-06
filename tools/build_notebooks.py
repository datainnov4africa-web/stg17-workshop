#!/usr/bin/env python3
"""
STG17 · Build the published notebooks from their bilingual masters.

    python tools/build_notebooks.py                  # build everything
    python tools/build_notebooks.py --only d4_ntl    # build one master
    python tools/build_notebooks.py --check          # CI: fail if outputs are stale

Why a build step at all
-----------------------
The workshop needs every laboratory in English and French, and each of those in
a guided track (code written, gaps to fill) and an open track (objective and data
only). That is four files per laboratory. Maintaining four files by hand
guarantees that a fix applied on Tuesday to the English guided notebook is still
missing from the French open one in November. So: one master, four outputs, and
a CI check that the outputs match the master.

--------------------------------------------------------------------------
THE MASTER FORMAT
--------------------------------------------------------------------------
A master is an ordinary .ipynb under notebooks/_masters/, with this metadata:

    "metadata": {
      "stg17": {
        "id":      "d4_ntl_collect_explore",
        "day":     4,
        "title_en": "Night-Time Lights — Collect and Explore",
        "title_fr": "Lumières nocturnes — Collecter et explorer",
        "outdir":  "notebooks/day4",
        "stem":    "D4_NTL_Collect_Explore",
        "country": "CIV",
        "tracks":  ["guided", "open"]
      }
    }

**Markdown cells** carry both languages:

    <!--EN-->
    ## Step 3 — Read a real granule
    We open the HDF5 and take the scale factor *from the file*.
    <!--FR-->
    ## Étape 3 — Lire un granule réel
    Nous ouvrons le HDF5 et lisons le facteur d'échelle *dans le fichier*.

The FR block runs to the end of the cell, or to an optional <!--/FR-->.
A markdown cell with no marker is emitted unchanged in both languages — right
for a cell that is only code, a badge, or a language-neutral image.

**Code cells** are identical in both languages except for comments:

    # EN: Read the layer and scale it | FR: Lire la couche et la mettre à l'échelle
    radiance, meta = ntl.read_layer(path)

Anything a code cell *prints* goes through stg17.i18n.T(), which resolves at run
time — so the executable code is byte-identical across the two languages, and a
bug fixed once is fixed everywhere.

**Solution blocks** mark what the open track removes:

    # <solution hint="Build the year x district panel" hint_fr="Construisez le panel année x district">
    panel = ntl.zonal_panel(files, adm2, lit_threshold=LIT)
    # </solution>

Guided track keeps the code and drops the two marker lines. Open track replaces
the block with a TODO carrying the hint, at the original indentation.

**Cell tags** restrict a cell to one output:

    only-en · only-fr · only-guided · only-open · no-colab

**Tokens** are substituted anywhere in any cell:

    {{LANG}} {{LANG_UPPER}} {{OTHER_LANG}} {{TRACK}} {{TITLE}} {{ISO3}}
    {{ORG}} {{REPO}} {{BRANCH}} {{NB_PATH}} {{COLAB_URL}} {{YEAR}}

--------------------------------------------------------------------------
MASTERS ARE WRITTEN AS .py, NOT AS .ipynb
--------------------------------------------------------------------------
A master may be either `<id>.master.ipynb` or — preferably — `<id>.master.py`,
a plain Python file in the familiar percent format:

    # %% [meta]
    '''
    id: d4_ntl_collect_explore
    day: 4
    title_en: Night-Time Lights - Collect and Explore
    outdir: notebooks/day4
    stem: D4_NTL_Collect_Explore
    tracks: guided, open
    '''

    # %% [markdown]
    '''
    <!--EN-->
    ## Step 3 - Read a real granule
    <!--FR-->
    ## Étape 3 - Lire un granule réel
    '''

    # %% tags=only-guided
    radiance, meta = ntl.read_layer(path)

The .py form is the recommended one and the one every master in this repository
uses. Markdown lives inside a triple-quoted string, which keeps the file valid
Python — so an editor highlights the code, a linter reads it, and git produces a
readable diff. None of that is true of a notebook full of escaped JSON, and the
material has to stay maintainable for the five years of the Action Plan.
"""

from __future__ import annotations

import argparse
import copy
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MASTERS = ROOT / "notebooks" / "_masters"
CONFIG = ROOT / "config" / "workshop.yml"

LANGS = ("en", "fr")
TRACKS = ("guided", "open")

# --- markers ---------------------------------------------------------------
RE_EN = re.compile(r"<!--\s*EN\s*-->", re.I)
RE_FR = re.compile(r"<!--\s*FR\s*-->", re.I)
RE_END = re.compile(r"<!--\s*/(?:EN|FR)\s*-->", re.I)
RE_COMMENT = re.compile(r"^(\s*)#\s*EN:\s*(.*?)\s*\|\s*FR:\s*(.*?)\s*$")
RE_SOL_OPEN = re.compile(r"^(\s*)#\s*<solution(?P<attrs>[^>]*)>\s*$")
RE_SOL_CLOSE = re.compile(r"^\s*#\s*</solution>\s*$")
RE_ATTR = re.compile(r'(\w+)\s*=\s*"([^"]*)"')


# ---------------------------------------------------------------------------
#  Minimal YAML reader
# ---------------------------------------------------------------------------
def load_config() -> dict:
    """
    Read the handful of values the build needs out of config/workshop.yml.

    Uses PyYAML when available and a deliberately small fallback parser when it
    is not, so that `--check` runs in a bare CI container without installing
    anything. The fallback only understands the nesting this file actually uses.
    """
    text = CONFIG.read_text(encoding="utf-8")
    try:
        import yaml  # noqa: PLC0415

        return yaml.safe_load(text)
    except ImportError:
        pass

    config: dict = {}
    stack = [(0, config)]
    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip())
        line = raw.strip()
        if line.startswith("- ") or ":" not in line:
            continue
        key, _, value = line.partition(":")
        key, value = key.strip(), value.strip().strip('"').strip("'")
        while stack and indent <= stack[-1][0] and len(stack) > 1:
            stack.pop()
        parent = stack[-1][1]
        if value:
            parent[key] = value
        else:
            child: dict = {}
            parent[key] = child
            stack.append((indent, child))
    return config


# ---------------------------------------------------------------------------
#  Reading a master
# ---------------------------------------------------------------------------
RE_CELL_MARK = re.compile(
    r"^#\s*%%\s*(?:\[(?P<kind>\w+)\])?\s*(?P<attrs>.*)$"
)


def _strip_fence(text: str) -> str:
    """Remove the outer triple-quoted fence around a markdown or meta cell."""
    body = text.strip()
    for fence in ('"""', "'''"):
        if body.startswith(fence):
            body = body[len(fence):]
            if body.rstrip().endswith(fence):
                body = body.rstrip()[: -len(fence)]
            break
    return body.strip("\n")


def _parse_meta(text: str) -> dict:
    """The `# %% [meta]` block: one `key: value` per line, lists comma-separated."""
    spec: dict = {}
    for line in _strip_fence(text).splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, _, value = line.partition(":")
        key, value = key.strip(), value.strip()
        if key in ("tracks", "requires"):
            spec[key] = [v.strip() for v in value.split(",") if v.strip()]
        elif key == "day" and value.isdigit():
            spec[key] = int(value)
        else:
            spec[key] = value
    return spec


def parse_percent_master(path: Path) -> dict:
    """
    Read a `<id>.master.py` file into the same in-memory shape as a master .ipynb.

    Cell boundaries are `# %%` lines. `[markdown]` and `[meta]` cells have their
    triple-quoted fence removed; everything else is code. `tags=a,b` on the
    marker line becomes cell metadata tags.
    """
    lines = path.read_text(encoding="utf-8").splitlines()
    cells: list[dict] = []
    spec: dict = {}

    current_kind, current_tags, buffer = None, [], []

    def flush():
        if current_kind is None:
            return
        text = "\n".join(buffer)
        if current_kind == "meta":
            spec.update(_parse_meta(text))
            return
        if current_kind == "markdown":
            text = _strip_fence(text)
        if not text.strip():
            return
        cells.append({
            "cell_type": "markdown" if current_kind == "markdown" else "code",
            "metadata": {"tags": list(current_tags)} if current_tags else {},
            "source": (text.rstrip("\n") + "\n").splitlines(keepends=True),
            **({} if current_kind == "markdown" else {"outputs": [], "execution_count": None}),
        })

    for line in lines:
        mark = RE_CELL_MARK.match(line)
        if mark:
            flush()
            current_kind = (mark.group("kind") or "code").lower()
            attrs = mark.group("attrs") or ""
            tag_match = re.search(r"tags\s*=\s*([\w\-,\s]+)", attrs)
            current_tags = ([t.strip() for t in tag_match.group(1).split(",") if t.strip()]
                            if tag_match else [])
            buffer = []
            continue
        if current_kind is not None:
            buffer.append(line)
    flush()

    if not spec:
        raise SystemExit(f"{path.name}: no '# %% [meta]' block found.")
    return {"cells": cells, "metadata": {"stg17": spec}}


def read_master(path: Path) -> dict:
    if path.suffixes[-2:] == [".master", ".py"] or path.name.endswith(".master.py"):
        return parse_percent_master(path)
    return json.loads(path.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
#  Cell transformation
# ---------------------------------------------------------------------------
class MasterError(SystemExit):
    """A master that cannot be built correctly — always fatal, never silent."""


def split_markdown(source: str, lang: str, where: str = "") -> str:
    """
    Keep only the requested language's block of a bilingual markdown cell.

    A cell with no <!--EN--> marker is language-neutral and passes through: that
    is how badge cells, images and pure-HTML separators stay in one place.
    """
    if not RE_EN.search(source) and not RE_FR.search(source):
        return source

    # A second marker of either language in one cell means the author nested the
    # blocks by mistake, and the split below would silently file part of the
    # English text under French. That produces a notebook which looks fine in a
    # diff and is wrong on screen, so it has to be fatal.
    for pattern, label in ((RE_EN, "<!--EN-->"), (RE_FR, "<!--FR-->")):
        if len(pattern.findall(source)) > 1:
            preview = source.strip().splitlines()[0][:70]
            raise MasterError(
                f"{where}: {label} appears more than once in a single markdown cell.\n"
                f"  Cell starts: {preview}\n"
                f"  Split the cell in two, or move the stray block. Each cell holds "
                f"exactly one <!--EN--> section followed by one <!--FR--> section."
            )

    en_match, fr_match = RE_EN.search(source), RE_FR.search(source)
    if en_match and fr_match:
        preamble = source[: min(en_match.start(), fr_match.start())]
        en_text = source[en_match.end(): fr_match.start()]
        fr_text = source[fr_match.end():]
    elif en_match:
        preamble, en_text, fr_text = source[: en_match.start()], source[en_match.end():], ""
    else:
        preamble, en_text, fr_text = source[: fr_match.start()], "", source[fr_match.end():]

    chosen = fr_text if lang == "fr" else en_text
    chosen = RE_END.sub("", chosen)
    return (preamble + chosen).strip("\n") + "\n"


def transform_code(source: str, lang: str, track: str) -> str:
    """Apply the comment convention and the solution blocks to one code cell."""
    out: list[str] = []
    in_solution = False
    hint_en = hint_fr = ""
    indent = ""

    for line in source.splitlines():
        open_match = RE_SOL_OPEN.match(line)
        if open_match:
            in_solution = True
            indent = open_match.group(1)
            attrs = dict(RE_ATTR.findall(open_match.group("attrs") or ""))
            hint_en = attrs.get("hint", "")
            hint_fr = attrs.get("hint_fr", hint_en)
            if track == "open":
                hint = hint_fr if lang == "fr" else hint_en
                label = "À FAIRE" if lang == "fr" else "TODO"
                out.append(f"{indent}# {label}: {hint}" if hint else f"{indent}# {label}")
                out.append(f"{indent}...")
            continue

        if RE_SOL_CLOSE.match(line):
            in_solution = False
            continue

        if in_solution and track == "open":
            continue  # the body is what the open track removes

        comment_match = RE_COMMENT.match(line)
        if comment_match:
            lead, en_text, fr_text = comment_match.groups()
            out.append(f"{lead}# {fr_text if lang == 'fr' else en_text}")
            continue

        out.append(line)

    return "\n".join(out)


def substitute(source: str, tokens: dict[str, str]) -> str:
    for key, value in tokens.items():
        source = source.replace("{{" + key + "}}", str(value))
    return source


def cell_allowed(cell: dict, lang: str, track: str) -> bool:
    tags = [str(t).lower() for t in cell.get("metadata", {}).get("tags", [])]
    if f"only-{lang}" in tags:
        return True
    other_lang = "fr" if lang == "en" else "en"
    if f"only-{other_lang}" in tags:
        return False
    if f"only-{track}" in tags:
        return True
    other_track = "open" if track == "guided" else "guided"
    if f"only-{other_track}" in tags:
        return False
    return True


# ---------------------------------------------------------------------------
#  Header cell
# ---------------------------------------------------------------------------
def header_cell(spec: dict, lang: str, track: str, nb_path: str, config: dict,
                tracks: list[str] | None = None) -> dict:
    """
    The navigation strip prepended to every published notebook.

    Carries the Colab badge, a link to the other language, and a link to the
    other track. A participant who opened the wrong file — the wrong language,
    or the guided track when they wanted the open one — is one click away from
    the right one, which matters when 40 people are choosing at 09:30.
    """
    github = config.get("github", {})
    org = github.get("org", "STG17-Africa")
    repo = github.get("repo", "stg17-workshop")
    branch = github.get("branch", "main")

    colab = f"https://colab.research.google.com/github/{org}/{repo}/blob/{branch}/{nb_path}"
    other_lang = "fr" if lang == "en" else "en"
    other_track = "open" if track == "guided" else "guided"
    other_lang_file = Path(nb_path).name.replace(
        f"_{lang.upper()}", f"_{other_lang.upper()}")
    stem = Path(nb_path).name
    if track == "guided":
        other_track_file = stem.replace(".ipynb", "_open.ipynb")
    else:
        other_track_file = stem.replace("_open.ipynb", ".ipynb")

    title = spec.get(f"title_{lang}", spec.get("title_en", spec.get("id", "")))
    day = spec.get("day", "")
    labels = {
        "en": ("Open in Colab", "Français", f"{other_track} track", "Day", "track"),
        "fr": ("Ouvrir dans Colab", "English", f"piste {'ouverte' if other_track == 'open' else 'guidée'}",
               "Jour", "piste"),
    }[lang]
    track_label = {"en": {"guided": "guided track", "open": "open track"},
                   "fr": {"guided": "piste guidée", "open": "piste ouverte"}}[lang][track]

    # Only offer the other track when the master actually produces one. An
    # environment check or a publication walkthrough has a single track, and a
    # dead link on the first line of a notebook reads as a broken repository.
    track_link = ""
    if tracks and len(tracks) > 1:
        track_link = (f'\n <a href="./{other_track_file}" style="color:#1B7A43;font-weight:600;'
                      f'\n  text-decoration:none;">⇄ {labels[2]}</a>')

    source = f"""<div style="display:flex;gap:14px;align-items:center;flex-wrap:wrap;
 font-family:'Segoe UI',system-ui,sans-serif;font-size:13px;padding:10px 2px;
 border-bottom:2px solid #1B7A43;margin-bottom:4px;">
 <a href="{colab}" target="_blank"><img
  src="https://colab.research.google.com/assets/colab-badge.svg" alt="{labels[0]}"></a>
 <span style="color:#6B7B75;">{labels[3]} {day}{' · ' + track_label if tracks and len(tracks) > 1 else ''}</span>
 <span style="flex:1;"></span>
 <a href="./{other_lang_file}" style="color:#1B7A43;font-weight:600;
  text-decoration:none;">🌐 {labels[1]}</a>{track_link}
</div>

<!-- {title} · STG17 workshop · AfDB / STATAFRIC -->
<!-- GENERATED FILE — edit notebooks/_masters/{spec.get('id')}.master.ipynb instead. -->
"""
    return {"cell_type": "markdown", "metadata": {"stg17_generated": True},
            "source": source.splitlines(keepends=True)}


# ---------------------------------------------------------------------------
#  Build
# ---------------------------------------------------------------------------
def output_path(spec: dict, lang: str, track: str) -> Path:
    stem = spec.get("stem") or spec["id"].upper()
    suffix = "" if track == "guided" else "_open"
    return ROOT / spec.get("outdir", "notebooks") / f"{stem}_{lang.upper()}{suffix}.ipynb"


def build_one(master: dict, spec: dict, lang: str, track: str, config: dict) -> tuple[Path, str]:
    """Render one (language, track) pair. Returns the path and the JSON text."""
    out_path = output_path(spec, lang, track)
    rel = out_path.relative_to(ROOT).as_posix()
    github = config.get("github", {})

    tokens = {
        "LANG": lang,
        "LANG_UPPER": lang.upper(),
        "OTHER_LANG": "fr" if lang == "en" else "en",
        "TRACK": track,
        "TITLE": spec.get(f"title_{lang}", spec.get("title_en", "")),
        "ISO3": spec.get("country", "CIV"),
        "ORG": github.get("org", "STG17-Africa"),
        "REPO": github.get("repo", "stg17-workshop"),
        "BRANCH": github.get("branch", "main"),
        "NB_PATH": rel,
        "COLAB_URL": (f"https://colab.research.google.com/github/{github.get('org')}/"
                      f"{github.get('repo')}/blob/{github.get('branch')}/{rel}"),
        "YEAR": str(config.get("workshop", {}).get("year", 2026)),
    }

    cells = [header_cell(spec, lang, track, rel, config, spec.get("tracks", list(TRACKS)))]
    for index, cell in enumerate(master["cells"]):
        if not cell_allowed(cell, lang, track):
            continue
        new = copy.deepcopy(cell)
        source = "".join(new.get("source", []))

        if new["cell_type"] == "markdown":
            source = split_markdown(source, lang, where=f"{spec['id']} cell {index}")
        else:
            source = transform_code(source, lang, track)
            new["outputs"] = []
            new["execution_count"] = None

        source = substitute(source, tokens)
        if not source.strip():
            continue  # a cell that emptied out — e.g. an open-track solution body
        new["source"] = source.splitlines(keepends=True)
        new.get("metadata", {}).pop("tags", None)
        cells.append(new)

    notebook = {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3 (ipykernel)",
                           "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.11"},
            "stg17": {**spec, "language": lang, "track": track, "generated": True},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    return out_path, json.dumps(notebook, ensure_ascii=False, indent=1) + "\n"


def build_master(path: Path, config: dict, check: bool) -> list[str]:
    """Build all outputs for one master. Returns the list of stale/written paths."""
    master = read_master(path)
    spec = master.get("metadata", {}).get("stg17")
    if not spec:
        raise SystemExit(f"{path.name}: missing metadata.stg17 block — see the module docstring.")

    tracks = spec.get("tracks", list(TRACKS))
    changed = []
    for lang in LANGS:
        for track in tracks:
            out_path, text = build_one(master, spec, lang, track, config)
            rel = out_path.relative_to(ROOT).as_posix()
            if check:
                if not out_path.exists() or out_path.read_text(encoding="utf-8") != text:
                    changed.append(rel)
            else:
                out_path.parent.mkdir(parents=True, exist_ok=True)
                existing = out_path.read_text(encoding="utf-8") if out_path.exists() else None
                if existing != text:
                    out_path.write_text(text, encoding="utf-8")
                    changed.append(rel)
    return changed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    parser.add_argument("--only", help="build only masters whose id contains this string")
    parser.add_argument("--check", action="store_true",
                        help="do not write; exit 1 if any output is out of date")
    args = parser.parse_args()

    config = load_config()
    masters = sorted([*MASTERS.glob("*.master.py"), *MASTERS.glob("*.master.ipynb")])
    if args.only:
        masters = [m for m in masters if args.only.lower() in m.name.lower()]
    if not masters:
        print("No master notebooks found under notebooks/_masters/.")
        return 0

    total_changed: list[str] = []
    for master in masters:
        changed = build_master(master, config, args.check)
        total_changed.extend(changed)
        status = "STALE" if (args.check and changed) else ("updated" if changed else "up to date")
        print(f"  {master.name:<46} {status}")

    if args.check and total_changed:
        print("\nThese generated notebooks do not match their master:")
        for path in total_changed:
            print("   -", path)
        print("\nRun:  python tools/build_notebooks.py")
        return 1

    verb = "would write" if args.check else "wrote"
    print(f"\n{len(masters)} master(s) · {verb} {len(total_changed)} file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
