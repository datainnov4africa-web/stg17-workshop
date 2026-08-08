# P9 · Standalone presentation, built in Claude

One prompt in, one finished `.html` file out — self-contained, opens in any
browser, no build step, no CDN, no repository. Use it when you want a single
presentation at the highest visual standard the format allows and you do not
need the bilingual pipeline.

The other prompts in this library produce fragments that live inside the
workshop build and inherit `afdb.css`. **P9 produces the whole document,
stylesheet included**, so the design quality is bounded by the prompt rather
than by an existing theme.

Paste it into Claude, answer nothing else, and ask for the file.

---

## The prompt

````text
Build a complete, self-contained HTML presentation. Output ONE file. It must
open correctly by double-clicking it, offline, with no build step and no network
request of any kind.

# Subject

{{SUBJECT}}

# Audience

{{AUDIENCE}}

# Duration and length

{{DURATION}} minutes. Budget 90 seconds per content slide and 20 seconds per
section divider, and size the deck to fit with slack. State your arithmetic in
an HTML comment at the top of the file.

# THE STANDARD — read this before writing a line

I am not asking for slides that are acceptable. I am asking for a deck that
would pass as the work of a design studio commissioned by a development bank.
Concretely, that means three things most generated decks fail:

  1. EVERY SLIDE HAS A VISUAL IDEA, not only a verbal one. A heading with two
     paragraphs beneath it is a page, not a slide. If a slide's only content is
     prose, you have not finished designing it.

  2. THE DECK HAS RHYTHM. White, white, white, white reads as one long scrolling
     document — the audience stops registering that anything changed. Colour
     fields, full-bleed diagrams and section dividers must interrupt at regular
     intervals. Never more than three consecutive white slides.

  3. TYPE DOES THE WORK. One family, a wide range of sizes, decisive weight
     contrast. A 46px numeral next to 15px supporting text carries more than any
     decoration. Nothing is centred except the title slide.

# Visual register — editorial-graphic

Flat colour fields, oversized numerals, strong typography, drawn SVG diagrams.

  NOT: photography, stock imagery, icon fonts, emoji, clip art.
  NOT: gradients (except one diagonal on the title slide), drop shadows on text,
       glows, 3D, bevels, glass effects, animated backgrounds.
  NOT: rounded-everything. Radius is 10–14px on panels, 0 on colour fields.

It must look right on a badly calibrated projector in a lit room, print
legibly in black and white, and not look dated in ten years.

# Palette — these seven values, and no eighth

  navy    #0B2545   structure, colour fields, headings, authority
  jade    #1B7A43   primary accent, the normal path, rules
  amber   #F2A900   the one element the eye should find; warnings
  ink     #33403A   body text
  muted   #6B7B75   captions, secondary text, sources
  line    #D5E6DF   hairlines and table borders
  wash    #F4F8F5   tinted ground and panel fill

Amber is scarce by design. If more than one element on a slide is amber, none of
them is emphasised. Never carry meaning by colour alone — a colour-blind viewer
and a monochrome printout must both still work.

# Type scale — use these, do not invent intermediate sizes

  Deck title      54px / 800     Slide title (h2)   32px / 800, -2% tracking,
  Statement       42px / 700                        with a 3px amber rule under it
  Hero numeral    92px / 800     Body               20px / 400, line-height 1.35
  Card title      17px / 800     Card body          14px / 400
  Table cell      15px           Source line        11px, muted
  Minimum anywhere 11px

If content does not fit at these sizes, the content is too long. Split the
slide. Never shrink type to make text fit — that is the single clearest
signature of an amateur deck.

# Slide archetypes — compose from these, and vary them deliberately

  TITLE        full-bleed navy→jade diagonal, eyebrow in amber caps, big title
  DIVIDER      solid navy, almost empty, one line saying what the part is for
  STATEMENT    one sentence at 42px, two or three words in jade, nothing else
  SPLIT        a navy/jade/amber colour panel (≈40%) carrying the claim, content
               beside it. The workhorse — it rescues any "heading + prose" slide
  HERO NUMBER  one numeral at 92px with its unit and a short caption
  BLEED FIGURE the diagram fills the slide under a navy title band
  STEPS        a row of 3–5 numbered cards, for a process
  COMPARE      two panels, colour-coded, for before/after or good/over-claimed
  TABLE        navy header row, alternating white and wash bodies, NO vertical
               rules, max 6 rows including the header, cells are fragments
  CARDS        2–4 evidence or metric cards in a row
  QUOTE        a pull quote with an 8px amber left rule
  CLOSING      what happens next. Never "Thank you", never "Questions?"

# Diagrams

Draw them as inline SVG, `viewBox="0 0 1180 H"` with H between 200 and 320. No
external files, no `<style>` blocks, no classes — every attribute inline. Give
each `<marker>` a unique id.

Left to right for process, top to bottom for hierarchy. At most seven primary
elements. Put the takeaway INSIDE the figure as a bold amber line at the bottom:
a diagram that needs the presenter to explain what it means is not finished.

Aim for two to four diagrams in a {{DURATION}}-minute deck. A deck with none is
a document.

# Density — a hard limit, not a guideline

At most 110 words visible on any slide, and aim for 75. Visible excludes speaker
notes, SVG labels and the source line. Count them.

Everything you want to say that does not fit goes into speaker notes. Write
those as full sentences in the second person, 80–150 words per slide, including
at least one delivery instruction ("pause here", "ask for hands", "do not read
the table aloud"). They are the script, not a dumping ground.

# Evidence

Every number and claim carries a source. If you are not certain a reference
exists exactly as you would write it, output `[UNVERIFIED — need: <the shape of
the evidence>]` instead. Never invent a DOI, an author list, or a statistic.
A fabricated citation in front of a professional audience is worse than a gap.

# Technical requirements

  - ONE file. All CSS in a single `<style>` block, all script in one `<script>`.
  - NO external requests: no CDN, no web fonts, no images by URL. Use a system
    font stack: -apple-system, "Segoe UI", Inter, Roboto, sans-serif.
  - Write your own minimal slide engine, about 40 lines: arrow keys and space to
    advance, one slide visible at a time, a slide counter, and `S` to toggle a
    speaker-notes panel. Do not depend on reveal.js.
  - A fixed 16:9 stage scaled to the viewport with a CSS transform, so the layout
    is identical at every window size. Base the stage on 1280×720.
  - `@media print` rules so Ctrl+P produces one slide per page.
  - Semantic HTML: real `<h2>`, `<table>`, `<figure>`; `role="img"` and
    `aria-label` on every SVG; sufficient contrast everywhere.

# Before you output, verify — and report the results in a comment

  1. Word count of the densest slide. Under 110?
  2. Longest run of consecutive white slides. Three or fewer?
  3. Number of slides whose only content is prose. Must be zero.
  4. Number of diagrams. Two or more?
  5. Any colour outside the seven listed? Must be none.
  6. Timing arithmetic against {{DURATION}} minutes.

If any check fails, fix it before you output — do not output and then note it.

Produce the complete file now.
````

---

## Using it

Fill the three braces first — subject, audience, duration — or run
`python tools/prompt.py P9` and edit the three lines it leaves marked.

Ask for the file, save it as `something.html`, and open it. Then, in a **fresh**
conversation, run [P6](P6-critic.md) against it: the model that wrote the deck
is the worst judge of whether its citations are real.

## What P9 cannot give you

The bilingual pipeline. A P9 deck is one language, one file, outside the build —
so nothing checks that its French matches its English, nothing enforces the
density budget after the fact, and it is not published on the workshop site.

For a session deck that belongs in the workshop, use **P1 → P2 → P3 → P5 → P8**
instead. P9 is for the standalone case: a keynote, a country presentation, a
one-off for a ministry.
