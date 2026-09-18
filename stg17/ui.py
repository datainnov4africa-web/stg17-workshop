"""
STG17 · Pedagogical components for notebooks.

Every laboratory is built from the same small vocabulary of visual blocks, so a
participant who has done one notebook already knows how to read the next one:

    hero()          the title banner that opens a notebook
    roadmap()       what the notebook will do, in one table
    step()          "STEP 3/9 — Reading a real VNP46A4 file"
    key_concept()   the one idea to retain from the section just executed
    warning()       a trap that costs an hour if you fall in it
    your_turn()     the participant does something (both tracks use this)
    checkpoint()    a foldable question with its answer hidden underneath
    deliverable()   what the team must produce and commit
    limitations()   what this result cannot support — part of every deliverable
    result_table()  a styled DataFrame
    status_table()  the green/red pass-fail grid of the environment check
    footer()        the closing signature block

These render as HTML in Jupyter, Colab, Kaggle and nbviewer alike. They are
deliberately inline-styled: GitHub's notebook renderer strips <style> blocks,
and the point of this workshop is that the notebooks look right *on GitHub*,
where the countries will publish them.

All text arguments accept either a plain string (used as-is) or a
(english, french) tuple, in which case the active language decides.
"""

from __future__ import annotations

from typing import Sequence

from . import theme
from .i18n import get_lang, phrase

try:  # pragma: no cover - display is a notebook concern
    from IPython.display import HTML, display
except ImportError:  # allows importing the module in a plain script
    HTML = None

    def display(*_args, **_kwargs):
        pass


FONT = "'Segoe UI','Inter',system-ui,-apple-system,sans-serif"
MONO = "'JetBrains Mono','Cascadia Code',Consolas,ui-monospace,monospace"

Text = "str | tuple[str, str]"


def _t(value) -> str:
    """Resolve a bilingual (en, fr) tuple, or pass a plain string through."""
    if isinstance(value, (tuple, list)) and len(value) == 2:
        return value[1] if get_lang() == "fr" else value[0]
    return "" if value is None else str(value)


def _show(html: str):
    if HTML is None:  # not in a notebook — return the markup for testing
        return html
    display(HTML(html))
    return None


# ---------------------------------------------------------------------------
#  Opening and closing
# ---------------------------------------------------------------------------
def hero(title, subtitle="", eyebrow="", day="", lab=""):
    """
    The banner that opens every notebook.

    `eyebrow` is the small uppercase line above the title — use it for the
    session name. `day` and `lab` render as chips on the right, so a participant
    who opens the wrong file notices within a second.
    """
    title, subtitle = _t(title), _t(subtitle)
    eyebrow = _t(eyebrow) or ("Banque africaine de développement · STG17"
                              if get_lang() == "fr"
                              else "African Development Bank · STG17")
    chips = ""
    for label, bg in ((day, "rgba(255,255,255,.16)"), (lab, "rgba(242,169,0,.22)")):
        if label:
            chips += (
                f'<span style="background:{bg};color:#fff;border-radius:20px;'
                f'padding:4px 14px;font-size:12px;font-weight:700;letter-spacing:.5px;'
                f'margin-left:8px;white-space:nowrap;">{_t(label)}</span>'
            )
    return _show(f"""
<div style="background:linear-gradient(135deg,{theme.NAVY} 0%,{theme.GREEN} 100%);
 border-radius:18px;padding:30px 36px;font-family:{FONT};margin:6px 0 18px;">
  <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:10px;">
    <div style="color:{theme.AMBER};font-size:12.5px;letter-spacing:3px;font-weight:700;
     text-transform:uppercase;">{eyebrow}</div>
    <div>{chips}</div>
  </div>
  <div style="color:#fff;font-size:1.95em;font-weight:800;margin:10px 0 8px;line-height:1.15;">
    {title}</div>
  <div style="color:#dbe7e0;font-size:1.02em;line-height:1.55;max-width:900px;">{subtitle}</div>
</div>""")


def footer(line="", sub=""):
    """The closing signature block of a notebook."""
    line = _t(line) or ("DATA SCIENCE TOOLKIT · BAD / STATAFRIC"
                        if get_lang() == "fr" else "DATA SCIENCE TOOLKIT · AfDB / STATAFRIC")
    sub = _t(sub) or ("Atelier STG17 · Plan d'action 2025-2030"
                      if get_lang() == "fr" else "STG17 workshop · Action Plan 2025-2030")
    return _show(f"""
<div style="background:linear-gradient(135deg,{theme.NAVY},{theme.GREEN});border-radius:16px;
 padding:22px 30px;margin-top:22px;text-align:center;font-family:{FONT};">
 <div style="color:{theme.AMBER};font-size:11.5px;letter-spacing:2.5px;font-weight:700;">{line}</div>
 <div style="color:#fff;font-size:1.05em;margin-top:7px;font-weight:600;">{sub}</div></div>""")


# ---------------------------------------------------------------------------
#  Structure
# ---------------------------------------------------------------------------
def roadmap(rows: Sequence[tuple], title=None):
    """
    The "what we are about to do" table, placed right after the hero.

    rows: sequence of (label, description) pairs. Both may be bilingual tuples.
    """
    title = _t(title) or ("Ce que fait ce carnet, étape par étape"
                          if get_lang() == "fr" else "What this notebook does, step by step")
    body = ""
    for i, (label, desc) in enumerate(rows):
        shade = theme.WASH if i % 2 == 0 else "#fff"
        body += (
            f'<tr style="background:{shade};">'
            f'<td style="padding:9px 12px;border:1px solid {theme.LINE};white-space:nowrap;'
            f'vertical-align:top;"><b style="color:{theme.GREEN};">{_t(label)}</b></td>'
            f'<td style="padding:9px 12px;border:1px solid {theme.LINE};color:{theme.INK};">'
            f'{_t(desc)}</td></tr>'
        )
    return _show(f"""
<div style="border:1px solid {theme.GREEN};border-radius:12px;padding:18px 22px;background:#fff;
 font-family:{FONT};margin:4px 0 16px;">
 <div style="color:{theme.NAVY};font-weight:800;font-size:1.05em;margin-bottom:10px;">{title}</div>
 <table style="width:100%;border-collapse:collapse;font-size:13.5px;">{body}</table></div>""")


def step(n, total, title, description="", icon=""):
    """
    A section header: STEP 3/9 followed by the title and a one-line purpose.

    The running count matters pedagogically — a participant who is lost knows
    immediately how far they are and how much is left.
    """
    return _show(f"""
<div style="border-left:5px solid {theme.GREEN};background:{theme.WASH};
 border-radius:0 12px 12px 0;padding:13px 18px;margin:18px 0 8px;font-family:{FONT};">
 <span style="background:{theme.GREEN};color:#fff;border-radius:20px;padding:3px 13px;
  font-weight:700;font-size:11.5px;letter-spacing:.5px;">
  {'ÉTAPE' if get_lang() == 'fr' else 'STEP'} {n}/{total}</span>
 <span style="color:{theme.NAVY};font-weight:800;font-size:1.14em;margin-left:11px;">
  {icon + ' ' if icon else ''}{_t(title)}</span>
 <div style="color:#3a4a42;margin-top:5px;font-size:.96em;line-height:1.5;">{_t(description)}</div>
</div>""")


def section(number, title, subtitle=""):
    """A part header, for notebooks organised in parts rather than numbered steps."""
    return _show(f"""
<div style="display:flex;align-items:stretch;border:1px solid {theme.GREEN};border-radius:10px;
 overflow:hidden;margin:26px 0 10px;font-family:{FONT};">
 <div style="background:{theme.GREEN};color:#fff;min-width:88px;display:flex;align-items:center;
  justify-content:center;font-size:34px;font-weight:800;">{number}</div>
 <div style="padding:16px 22px;background:{theme.WASH};flex:1;">
  <h2 style="margin:0;color:{theme.NAVY};font-size:21px;">{_t(title)}</h2>
  <p style="margin:6px 0 0;color:#3D4A45;font-size:14px;line-height:1.5;">{_t(subtitle)}</p>
 </div></div>""")


# ---------------------------------------------------------------------------
#  Callouts
# ---------------------------------------------------------------------------
def _callout(label, body, colour, bg, icon=""):
    return _show(f"""
<div style="border:1px solid {colour};border-left:6px solid {colour};background:{bg};
 padding:13px 17px;border-radius:0 9px 9px 0;margin:14px 0;font-family:{FONT};">
 <b style="color:{colour};font-size:11.5px;letter-spacing:1.6px;text-transform:uppercase;">
  {icon + ' ' if icon else ''}{label}</b><br>
 <span style="color:{theme.INK};font-size:14.3px;line-height:1.58;">{body}</span></div>""")


def key_concept(body, title=None):
    """The single idea to retain. One per section, never two."""
    return _callout(_t(title) or phrase("key_concept"), _t(body), theme.GREEN, theme.WASH, "◆")


def warning(body, title=None):
    """A trap. Reserve this for things that actually cost time or produce wrong numbers."""
    return _callout(_t(title) or phrase("warning"), _t(body), theme.AMBER, "#FEF9EC", "▲")


def info(body, title=None):
    return _callout(_t(title) or "Note", _t(body), theme.INFO, "#EEF4FB", "●")


def your_turn(body, title=None):
    """Hands on keyboard — the point in a notebook where the participant acts."""
    return _callout(_t(title) or phrase("your_turn"), _t(body), theme.NAVY, "#EEF1F6", "✎")


def deliverable(body, title=None):
    """
    What the team must produce and commit. Taken verbatim from the laboratory
    specifications in section 6 of the concept note.
    """
    return _callout(_t(title) or phrase("deliverable"), _t(body), theme.GREEN, "#EAF4EE", "★")


def limitations(items: Sequence, title=None):
    """
    The honest statement of what the result cannot support.

    Not optional and not decorative: the concept note makes this statement part
    of the Day 4 deliverable, and no country should publish a proxy indicator
    without it.
    """
    title = _t(title) or phrase("limitations_title")
    lis = "".join(f'<li style="margin:5px 0;">{_t(i)}</li>' for i in items)
    return _show(f"""
<div style="border:1px solid {theme.AMBER};border-radius:10px;background:#FFFDF6;
 padding:16px 20px;margin:16px 0;font-family:{FONT};">
 <div style="color:{theme.NAVY};font-weight:800;font-size:1.02em;margin-bottom:6px;">
  ▲ {title}</div>
 <ul style="color:{theme.INK};font-size:14px;line-height:1.6;margin:6px 0 0;padding-left:22px;">
  {lis}</ul></div>""")


def checkpoint(qa: Sequence[tuple], title=None):
    """
    Foldable self-test questions.

    qa: sequence of (question, answer) pairs, each optionally bilingual.
    The answer is hidden behind a <details>, which survives GitHub's renderer —
    so the self-test still works for someone reading the published repository.
    """
    title = _t(title) or phrase("checkpoint")
    blocks = ""
    for q, a in qa:
        blocks += (
            f'<details style="margin:9px 0;border:1px solid {theme.GREEN};border-radius:9px;'
            f'padding:11px 15px;background:#fff;">'
            f'<summary style="cursor:pointer;color:{theme.NAVY};font-weight:600;">{_t(q)}</summary>'
            f'<p style="color:#3D4A45;margin:9px 0 0;line-height:1.6;">{_t(a)}</p></details>'
        )
    return _show(f"""
<div style="background:{theme.WASH};border-radius:11px;padding:16px 19px;margin:18px 0;
 font-family:{FONT};">
 <b style="color:{theme.GREEN};letter-spacing:1.6px;font-size:11.5px;text-transform:uppercase;">
  ? {title}</b>{blocks}</div>""")


def fallback(body, title=None):
    """
    The documented degraded path for this laboratory.

    Every laboratory has one, and it is shown *before* it is needed rather than
    improvised when something breaks — which, per the concept note, it will.
    """
    title = _t(title) or ("Si cela échoue — chemin de repli"
                          if get_lang() == "fr" else "If this fails — fallback path")
    return _callout(title, _t(body), theme.INFO, "#EEF4FB", "⟲")


# ---------------------------------------------------------------------------
#  Tables
# ---------------------------------------------------------------------------
def result_table(df, caption="", max_rows: int = 25, highlight: str | None = None):
    """
    Render a DataFrame in the workshop identity.

    `highlight` names a numeric column to shade from light to dark green,
    which turns a table of regions into something a reader can scan.
    """
    import pandas as pd  # local import: not every notebook needs pandas at import time

    view = df.head(max_rows)
    styler = view.style.set_table_styles(
        [
            {"selector": "th", "props": [
                ("background", theme.NAVY), ("color", "white"), ("font-weight", "700"),
                ("padding", "8px 11px"), ("font-size", "12.5px"), ("text-align", "left"),
                ("border", f"1px solid {theme.NAVY}")]},
            {"selector": "td", "props": [
                ("padding", "7px 11px"), ("font-size", "12.5px"),
                ("border", f"1px solid {theme.LINE}"), ("color", theme.INK)]},
            {"selector": "", "props": [
                ("border-collapse", "collapse"), ("font-family", FONT),
                ("box-shadow", "0 1px 3px rgba(11,37,69,.08)")]},
        ]
    ).hide(axis="index")

    if highlight and highlight in view.columns:
        styler = styler.background_gradient(subset=[highlight], cmap="Greens")
    if caption:
        styler = styler.set_caption(
            f'<div style="font-family:{FONT};color:{theme.MUTED};font-size:12px;'
            f'padding:6px 0;">{_t(caption)}</div>'
        )
    for col in view.select_dtypes("number").columns:
        styler = styler.format({col: "{:,.2f}"}, na_rep="—")
    return styler


def status_table(rows: Sequence[tuple], title=None, note=None):
    """
    The pass/fail grid used by the environment check and by every validation step.

    rows: (label, status, detail) where status is one of
          "ok" | "warn" | "fail" | "skip".

    Returns the HTML string as well as displaying it, so the environment-check
    notebook can also produce the copy-paste diagnostic string for the technical
    assistants.
    """
    icons = {"ok": ("✔", theme.OK), "warn": ("!", theme.WARN),
             "fail": ("✘", theme.FAIL), "skip": ("–", theme.MUTED)}
    body = ""
    for label, status, detail in rows:
        icon, colour = icons.get(str(status).lower(), icons["skip"])
        body += (
            f'<tr><td style="padding:7px 11px;border-bottom:1px solid {theme.LINE};'
            f'width:34px;text-align:center;color:{colour};font-weight:800;font-size:15px;">{icon}</td>'
            f'<td style="padding:7px 11px;border-bottom:1px solid {theme.LINE};'
            f'font-weight:600;color:{theme.NAVY};white-space:nowrap;">{_t(label)}</td>'
            f'<td style="padding:7px 11px;border-bottom:1px solid {theme.LINE};'
            f'color:{theme.INK};font-family:{MONO};font-size:12px;">{_t(detail)}</td></tr>'
        )
    head = (f'<div style="color:{theme.NAVY};font-weight:800;font-size:1.05em;'
            f'margin-bottom:9px;">{_t(title)}</div>') if title else ""
    tail = (f'<div style="color:{theme.MUTED};font-size:12px;margin-top:10px;'
            f'line-height:1.5;">{_t(note)}</div>') if note else ""
    html = (f'<div style="border:1px solid {theme.LINE};border-radius:11px;padding:16px 19px;'
            f'background:#fff;font-family:{FONT};margin:12px 0;box-shadow:{"0 1px 3px rgba(11,37,69,.08)"};">'
            f'{head}<table style="width:100%;border-collapse:collapse;font-size:13px;">'
            f'{body}</table>{tail}</div>')
    _show(html)
    return html


def metric_row(metrics: Sequence[tuple]):
    """
    A row of headline numbers: (value, label, optional sublabel).

    Used to open the "results" section of an analysis notebook, so the reader
    gets the answer before the method.
    """
    cards = ""
    for m in metrics:
        value, label = m[0], m[1]
        sub = m[2] if len(m) > 2 else ""
        cards += f"""
 <div style="flex:1;min-width:150px;background:#fff;border:1px solid {theme.LINE};
  border-top:4px solid {theme.GREEN};border-radius:11px;padding:15px 17px;">
  <div style="color:{theme.NAVY};font-size:1.85em;font-weight:800;line-height:1.1;">{value}</div>
  <div style="color:{theme.INK};font-size:13px;font-weight:600;margin-top:5px;">{_t(label)}</div>
  <div style="color:{theme.MUTED};font-size:11.5px;margin-top:2px;">{_t(sub)}</div></div>"""
    return _show(f'<div style="display:flex;gap:12px;flex-wrap:wrap;margin:14px 0;'
                 f'font-family:{FONT};">{cards}</div>')


def colab_badge(notebook_path: str, org: str = "datainnov4africa-web",
                repo: str = "stg17-workshop", branch: str = "main"):
    """
    The 'Open in Colab' badge, pointing at this notebook in the workshop repository.

    Rendered from cell 0 of every notebook so that a participant who received
    the file by email, on a USB key, or through GitHub can always reach the
    hosted version in one click.
    """
    url = f"https://colab.research.google.com/github/{org}/{repo}/blob/{branch}/{notebook_path}"
    raw = f"https://github.com/{org}/{repo}/blob/{branch}/{notebook_path}"
    return _show(f"""
<div style="font-family:{FONT};margin:6px 0 14px;display:flex;gap:10px;align-items:center;
 flex-wrap:wrap;">
 <a href="{url}" target="_blank" style="text-decoration:none;">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open in Colab"></a>
 <a href="{raw}" target="_blank" style="text-decoration:none;color:{theme.GREEN};
  font-size:12.5px;font-weight:600;">{'Voir sur GitHub' if get_lang() == 'fr' else 'View on GitHub'}</a>
</div>""")
