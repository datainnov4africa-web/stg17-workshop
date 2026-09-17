# P7 · Native deck build

The automated PPTX derivative in `docs/slides/pptx/` carries headings and little
else — it drops statements, tables, callouts and diagrams, because there is no
faithful automatic translation from a CSS-laid-out HTML slide to a PowerPoint
shape tree. It is a handout skeleton, not a presentation.

This prompt is the alternative: hand the design system to a tool that actually
lays out slides, and have it build the deck natively.

Works in **Gamma** (paste as a single prompt, then "Generate"), **Microsoft 365
Copilot in PowerPoint**, **Canva Magic Design**, or any assistant that emits
`python-pptx` code. The design specification below is the part that matters and
is the same in all cases.

---

## The prompt

````text
Build a 16:9 presentation deck to the following specification. Follow the design
system exactly — it is an institutional identity, not a suggestion.

# The content

{{DECK_TEXT}}

Use this content as given. Do not add slides, do not invent examples, do not
"improve" a claim, and do not add a citation that is not already there. Where the
content includes speaker notes, put them in the notes pane, not on the slide.

# Design system — African Development Bank

## Canvas and grid
  16:9, 13.333 × 7.5 inches (33.87 × 19.05 cm).
  Margins: 0.8in left and right, 0.6in top, 0.9in bottom.
  A 12-column grid across the content width, 0.2in gutter.
  Nothing in the bottom 0.55in — that strip is the footer.

## Colour — these seven values and nothing else
  Navy    #0B2545   headings, the authoritative element, title backgrounds
  Jade    #1B7A43   primary accent, positive path, rules
  Amber   #F2A900   secondary accent, the element the eye should find, warnings
  Ink     #33403A   body text
  Muted   #6B7B75   captions, secondary text, sources
  Line    #D5E6DF   hairlines, table borders
  Wash    #F4F8F5   tinted panel fill
  White   #FFFFFF   text on navy or jade

  Do not introduce gradients other than the title slide's navy → jade diagonal.
  Do not use drop shadows on text. Do not use a fifth accent colour anywhere.

## Type
  One family throughout: Segoe UI (fallback Inter, then Arial). No serif faces.
  Slide title (h2)     32pt, weight 800, navy, letter-spacing -2%
                       with a 3pt amber rule beneath it, width of the text
  Statement            42pt, weight 700, navy, max 26 characters per line
  Body                 20pt, weight 400, ink, line spacing 1.35
  Callout body         18pt
  Table cell           15pt      Table header 15pt, white on navy
  Metric number        46pt, weight 800, navy
  Metric label         13pt, weight 700, ink
  Source line          11pt, muted
  Footer               10pt, muted

  Minimum size anywhere on a slide: 11pt. If content does not fit at 11pt, the
  content is too long — split the slide rather than shrinking the type.

## Slide archetypes — build each slide as one of these

  TITLE      Full-bleed navy→jade diagonal gradient. Eyebrow in amber caps 12pt,
             title 54pt white, subtitle 24pt at 80% white, metadata block bottom
             left at 13pt, 70% white.

  DIVIDER    Solid navy. Amber eyebrow, white title 44pt with an amber rule,
             one line of body at 22pt in #9FB4C6. Deliberately almost empty.

  STATEMENT  White ground. One sentence at 42pt occupying the upper half, with
             two or three words coloured jade. A qualifier beneath at 17pt muted.
             Nothing else on the slide.

  TABLE      Header row navy with white text, rounded top corners. Body rows
             alternating white and wash. 1pt Line rule beneath each row, no
             vertical rules at all. Cells are fragments, left-aligned, top-aligned.

  CALLOUT    A wash panel (jade) or #FEF9EC panel (amber) with a 6pt left border
             in the accent colour, rounded on the right side only. Label in
             13pt caps in the accent, body 18pt.

  METRICS    2–4 cards in a row, white fill, 1pt Line border, 4pt jade top
             border, 10pt corner radius. Number, label, qualifier stacked.

  FIGURE     The diagram occupies the full content width. Caption beneath at
             13pt muted, stating what the figure MEANS, not what it contains.

  SPLIT      A navy, jade or amber colour panel across ~40% of the width
             carrying the eyebrow and title, content in the remaining 60%.
             Use it for any slide that would otherwise be heading-plus-prose.

  HERO NUM   One numeral at 92pt weight 800 in jade, its unit at 35pt muted
             beside it, and a caption of at most two lines at 17pt.

  STEPS      3–5 cards in a row, each with a 46pt numeral, a 17pt title and two
             lines at 14pt. A 5pt top border, jade, amber on the last card.

  COMPARE    Two panels side by side on a wash fill, 5pt top border — muted or
             red on the left, jade on the right. Labels in 13pt caps.

  CLOSING    Navy or night ground, what happens next, no "thank you" slide.

## Rhythm — the rule most decks fail
  Never more than three consecutive white slides. Roughly a third of the deck
  should carry a colour field. Every content slide must have a visual idea as
  well as a verbal one: a slide whose only content is prose is unfinished.

## Footer, on every slide except the title
  A 2pt amber rule across the content width at 0.55in from the bottom.
  Beneath it, left: "African Development Bank · AU STATAFRIC · STG17" in navy
  bold 10pt. Right: the slide number in muted 10pt.

# Diagrams

Where the content contains an SVG diagram, do NOT attempt to redraw it from the
description. Insert a placeholder rectangle in Line colour with a dashed border
and the label "FIGURE: <the aria-label text>" in muted 13pt, sized to the full
content width and 2.6in high. I will paste the rendered figure in afterwards.

An honest placeholder is better than a redrawn diagram that has lost its meaning.

# What NOT to do

  - No stock photography, no clip art, no 3D shapes, no icon sets.
  - No bullet lists longer than five items, and no sub-bullets at all.
  - No slide with more than 110 words visible.
  - No animated transitions.
  - No "Agenda", "Outline", "Questions?" or "Thank you" slides.
  - Do not centre body text. Left-aligned, with a ragged right edge.

Build it now.
````

---

## If you want a scripted result instead

Ask the same assistant for `python-pptx` code implementing that specification,
and run it against the deck source. That path is reproducible and versionable,
which the manual one is not — and if you take it, the script belongs in
`tools/`, replacing `build_pptx.py` rather than sitting beside it.

Which path is right depends on whether the PPTX needs to regenerate every time
the content changes (script it) or is a one-off export for a specific meeting
(build it natively and stop).

## Honest limits

Whatever tool you use, the reveal.js deck under `docs/slides/` stays the source
of truth. It is what the build validates for density and bilingual symmetry, and
it is what is published on the site. A PowerPoint built with this prompt is a
derivative for people who need a file to email — keep it downstream, and
regenerate it rather than editing it in two places.
