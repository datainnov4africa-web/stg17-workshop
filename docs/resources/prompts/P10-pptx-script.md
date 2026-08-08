# P10 · PowerPoint, by script

Produces a runnable `python-pptx` program that builds the `.pptx` file. Use this
when you want a real PowerPoint and you want it to regenerate every time the
content changes.

The two PowerPoint routes, and when each is right:

| | [P7](P7-native-deck.md) — build it in a tool | **P10 — build it by script** |
|---|---|---|
| You paste into | Gamma, Copilot, Canva | Claude, then run the script |
| Result | a deck inside that tool, exported | a `.pptx` on your disk |
| Regenerating after a content change | redo it by hand | rerun the script |
| Fine visual control | the tool's judgement | exactly what the spec says |
| Best for | a one-off for a specific meeting | a deck that will be revised |

If the deck will ever be revised — and a workshop deck always is — take P10.

---

## The prompt

````text
Write a single Python program that builds a PowerPoint presentation with
python-pptx. I will run it and get a .pptx file. Do not describe the approach;
write the program.

# The content

{{DECK_TEXT}}

Use this content as given. Do not add slides, do not invent examples, do not
"improve" a claim, and do not add a citation that is not already there. Speaker
notes go into the notes slide, never onto the slide face.

If the content is bilingual — marked with <!--EN--> and <!--FR--> — build TWO
files, `<name>-en.pptx` and `<name>-fr.pptx`, from one pass over the source.

# Program requirements

  - Python 3.10+, `python-pptx` only. No other third-party dependency.
  - Every measurement through `pptx.util.Inches`, `Pt`, `Emu` — no magic numbers
    scattered inline. Put the design system in module-level constants at the top
    so a colour or a size is changed in one place.
  - One function per slide archetype: `slide_title`, `slide_divider`,
    `slide_statement`, `slide_split`, `slide_table`, `slide_metrics`,
    `slide_steps`, `slide_compare`, `slide_callout`, `slide_hero_number`,
    `slide_figure`, `slide_closing`. Each takes plain arguments and returns the
    slide. The deck at the bottom of the file is then a readable list of calls.
  - Build on the BLANK layout (`prs.slide_layouts[6]`) and place every shape
    explicitly. Do not use the built-in title/content placeholders — they carry
    theme formatting you cannot fully control.
  - `--out DIR` argument, defaulting to the current directory. Print each file
    written.
  - Docstrings that say WHY a choice was made where it is not obvious, not what
    the line does.

# Design system — African Development Bank

## Canvas
  16:9 widescreen: `prs.slide_width = Inches(13.333)`, `slide_height = Inches(7.5)`.
  Content margins: left and right 0.8", top 0.6", bottom 0.9".
  Reserve the bottom 0.55" for the footer; no content may enter it.

## Colour — these seven, and no eighth
  NAVY  = RGBColor(0x0B, 0x25, 0x45)   structure, colour fields, headings
  JADE  = RGBColor(0x1B, 0x7A, 0x43)   primary accent, the normal path
  AMBER = RGBColor(0xF2, 0xA9, 0x00)   the one element the eye should find
  INK   = RGBColor(0x33, 0x40, 0x3A)   body text
  MUTED = RGBColor(0x6B, 0x7B, 0x75)   captions, secondary text, sources
  LINE  = RGBColor(0xD5, 0xE6, 0xDF)   hairlines, table borders
  WASH  = RGBColor(0xF4, 0xF8, 0xF5)   tinted ground and panel fill

  No gradients except the title slide. No drop shadows on text — set
  `shape.shadow.inherit = False` on every shape you create, because python-pptx
  inherits a theme shadow otherwise and it looks amateurish on projection.

## Type
  Font: "Segoe UI" throughout, with no serif anywhere.
  Slide title      Pt(32), bold, NAVY, plus a 3pt AMBER rule directly beneath,
                   the width of the text block
  Statement        Pt(42), bold, NAVY, at most ~26 characters per line
  Hero numeral     Pt(92), bold, JADE
  Body             Pt(20), INK, line spacing 1.35
  Callout body     Pt(18)
  Table cell       Pt(15); header Pt(15) bold white on NAVY
  Card title       Pt(17) bold; card body Pt(14)
  Source line      Pt(11), MUTED
  Footer           Pt(10), MUTED

  Minimum anywhere Pt(11). Set `text_frame.word_wrap = True` and DO NOT enable
  autofit shrink — if text does not fit at these sizes the content is too long,
  and silently shrinking it is the clearest signature of an amateur deck. Raise
  a clear error naming the slide instead.

## Archetypes
  TITLE      full-bleed NAVY rectangle behind everything, an AMBER eyebrow in
             caps at Pt(12), title Pt(54) white, subtitle Pt(24) at 80% white,
             a metadata block bottom left at Pt(13)
  DIVIDER    solid NAVY, deliberately almost empty: eyebrow, title Pt(44) white
             with an AMBER rule, one line of body
  STATEMENT  white ground, one sentence at Pt(42) in the upper half, a qualifier
             beneath at Pt(17) MUTED, nothing else
  SPLIT      a NAVY, JADE or AMBER rectangle over the left ~40% of the slide
             carrying eyebrow and title, content in the remaining 60%
  TABLE      header row NAVY with white text, body rows alternating white and
             WASH, a 1pt LINE bottom border per row, NO vertical borders at all
             (set every cell's left/right border to none), cells top-aligned
  METRICS    2–4 white cards in a row, 1pt LINE border, a 4pt JADE bar across
             the top, numeral Pt(46) then label then qualifier
  STEPS      3–5 cards, each a numeral Pt(46) JADE, title Pt(17), two lines
             Pt(14); a 5pt top bar, AMBER on the last card
  COMPARE    two panels on WASH, 5pt top bar — MUTED left, JADE right
  CALLOUT    a WASH panel (or #FEF9EC for a warning) with a 6pt left bar in the
             accent colour, label in Pt(13) caps, body Pt(18)
  HERO NUM   one numeral Pt(92) with its unit beside it at Pt(35) MUTED and a
             caption of at most two lines
  FIGURE     see below
  CLOSING    NAVY ground, what happens next. No "Thank you", no "Questions?"

## Footer, on every slide except the title
  A 2pt AMBER line across the content width at 0.55" from the bottom.
  Below it: left, "African Development Bank · AU STATAFRIC · STG17" in NAVY bold
  Pt(10); right, the slide number in MUTED Pt(10).

# Figures — the honest part

python-pptx cannot rasterise SVG, and redrawing a diagram from its description
loses the meaning it was drawn to carry. So:

  - Accept an optional `--figures DIR`. For a figure whose `aria-label` or id
    matches a PNG in that directory, insert the PNG at the full content width.
  - Where no PNG exists, insert a rectangle with a dashed LINE border, WASH fill,
    and the label "FIGURE: <the aria-label text>" centred in MUTED Pt(13),
    sized to the content width and 2.6" high.
  - Print a summary at the end listing every placeholder still unfilled, so I
    know exactly which figures to screenshot and drop in.

Do not attempt to draw the diagram with PowerPoint shapes.

# Verify before you finish, and print the results

  1. Every slide's visible text under 110 words.
  2. No table over 6 rows including the header.
  3. No font size below Pt(11), and no autofit-shrink anywhere.
  4. Speaker notes present on every content slide.
  5. No colour outside the seven constants.
  6. Slide count and the file names written.

Write the complete program now.
````

---

## Running it

```bash
pip install python-pptx
python build_deck.py --out ./out --figures ./figures
```

To fill the figure placeholders: open the reveal.js deck, screenshot each SVG at
full width, save the PNGs under `figures/` with names matching what the script
prints, and rerun. The script is idempotent — rerunning replaces the files.

## Where this fits

The reveal.js deck under `docs/slides/` stays the source of truth: it is what the
build validates for density, visual weight and bilingual symmetry, and it is what
the site publishes. A P10 script is a **derivative generator** — treat the
`.pptx` as build output, never as a file to edit.

If a P10 script becomes the way your team produces PowerPoint, it belongs in
`tools/`, replacing `build_pptx.py` rather than sitting beside it. Two scripts
that both claim to produce the PPTX is how the stale one gets shipped.
