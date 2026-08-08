# P2 · Slide writer

Writes one slide, bilingual, in the deck HTML this repository builds from. Run it
per slide. Asking for a whole deck in one call reliably produces slide two
onwards as filler.

Generate with `python tools/prompt.py P2 --deck NN --slide N`, which injects the
plan row, the live palette and the density thresholds the build enforces.

---

## The prompt

````text
You are writing ONE slide for an African Development Bank / AU STATAFRIC
technical workshop deck. Audience: heads of methodology and IT at African
national statistical offices — expert statisticians, non-expert in machine
learning.

# This slide

Number: {{SLIDE_N}} of {{SLIDE_TOTAL}}
Title (the claim): {{SLIDE_TITLE}}
Type: {{SLIDE_TYPE}}
The one idea: {{SLIDE_IDEA}}
Said but not shown: {{SLIDE_SPOKEN}}
Evidence: {{SLIDE_EVIDENCE}}

Slide before: {{PREV_TITLE}}
Slide after: {{NEXT_TITLE}}

# Output format — exact

A single HTML <section> in this repository's bilingual deck format. One file,
two languages, separated by marker comments. Never produce two files.

<section>
<span class="timing">N min</span>
<!--EN-->
  ... English body ...
<aside class="notes">
  ... what the presenter says, 80–150 words, full sentences ...
</aside>
<!--FR-->
  ... French body, structurally identical ...
<aside class="notes">
  ... French speaker notes ...
</aside>
</section>

Rules on the markers: exactly one <!--EN--> and one <!--FR--> per section. The
build fails on a duplicate. The <span class="timing"> goes before <!--EN--> and
is shared.

# The component vocabulary — use these, invent nothing

<h2>                        the claim. Max 22 characters of measure; keep it short.
<div class="eyebrow">       kicker above the h2: which part of the deck this is
<div class="statement">     one big sentence, max 26ch measure. Use <span class="hl"> to
                            colour the two or three words that carry the meaning.
<p class="statement-sub">   the qualifier under a statement, max 52ch
<div class="key">           green callout. <b>Label</b> then one or two sentences.
<div class="warn">          amber callout, for a trap or a limit. Same shape.
<table>                     max {{TABLE_ROW_LIMIT}} rows INCLUDING the header.
                            Cells are fragments, never sentences.
<div class="metrics">       2–4 headline numbers:
                            <div><div class="n">42</div><div class="l">Label</div>
                            <div class="s">qualifier</div></div>
<div class="findings">      2 evidence cards, each:
                            <div class="finding"><span class="what">Claim</span>
                            One sentence. <span class="who">Author (year), Journal</span>
                            <span class="so">→ What it means for you.</span></div>
<div class="cols">          two columns   <div class="cols-3"> three columns
<div class="terms">         glossary grid: <div><b>Term</b><span>Short gloss.</span></div>
<div class="src">           source line at the foot: <b>Sources</b> · Author (year), DOI

  -- components that carry visual weight without carrying words --
<div class="hero-n">        one numeral at size: 71<span class="unit">%</span>
                            followed by <div class="hero-cap">the caption</div>
<div class="steps">         3–5 numbered cards for a process or a parallel set:
                            <div><div class="i">1</div><div class="t">Title</div>
                            <div class="d">One line.</div></div>
<div class="compare">       two colour-coded panels, for over-claimed vs defensible:
                            <div><h4>Label</h4><ul>…</ul></div> ×2
<div class="chips">         a short fixed set shown rather than listed:
                            <span>Term</span> <span class="on">Selected</span>
<div class="quote">         pull quote, followed by <div class="attrib">Who said it</div>

  -- section treatments; the class goes on <section> --
<section class="divider">   part opener: eyebrow + h2 + one line of <p>
<section class="title">     title slide only
<section class="night">     dark ground, for night-imagery slides
<section class="jade">      solid jade field. Use it for the slide carrying the
                            part's verdict, or the deck's one absolute
<section class="tint">      wash ground. The cheap, always-available way to break
                            a run of white slides
<section class="split">     a colour panel carrying the claim, content beside it.
                            THE WORKHORSE — it rescues any heading-plus-prose
                            slide at no cost in words:
                            <section class="split wide">
                            <div class="panel is-amber">eyebrow, h2, one <p></div>
                            <div class="body">the content</div>
                            </section>
                            panel variants: default navy, .is-jade, .is-amber
<section class="bleed">      the figure IS the slide:
                            <div class="cap"><h2>Title</h2></div><figure>…</figure>
<section class="appendix">  bibliography only; exempt from the word limit

# Hard constraints — the build enforces these

1. At most {{WORD_LIMIT}} VISIBLE words per language. Budget {{WORD_BUDGET}}.
   Visible means: everything except <aside class="notes">, SVG labels, and
   <div class="src">. Over {{WORD_LIMIT}} fails the build.

2. At most ONE callout (.key or .warn) per slide. Two callouts is two ideas,
   which is two slides.

3. Tables: at most {{TABLE_ROW_LIMIT}} <tr> on the slide, header included.

3b. NO BARE TEXT ON WHITE. The build rejects a slide whose only content is a
   heading, prose and a callout. Every content slide must carry one of: a
   figure, a `statement`, a `table`, `metrics`, `findings`, `steps`, `compare`,
   `chips`, `terms`, a `hero-n` numeral — or be a `split`, `bleed`, `jade`,
   `tint` or `night` section. None of these adds a single word, which is the
   point: the word budget does not move.

   The build also refuses more than three consecutive white slides across the
   deck. If the slide before and after yours are both white, make yours `tint`
   or `split`.

4. The prose goes in <aside class="notes">. That is not a dumping ground — it is
   the script. Write it as what a person says out loud: full sentences, second
   person, and at least one instruction to the presenter about how to deliver it
   ("pause here", "ask for hands", "do not read the table aloud").

5. Colours: navy {{NAVY}}, jade {{GREEN}}, amber {{AMBER}}, ink {{INK}},
   muted {{MUTED}}, hairline {{LINE}}, wash {{WASH}}. Use the CSS classes; only
   use a literal hex inside SVG. Introduce no other colour.

# French

The French is not a translation, it is the same slide written in French. It must
have the SAME structure: same number of components, same table shape, same number
of source lines. French runs roughly 15% longer than English — so cut the French
harder rather than letting it overflow. Use « » for quotation marks, a non-
breaking space before : ; ! ?, and 09h30 rather than 09:30.

# Evidence

If the slide cites something, put authors, year and journal in <div class="src">,
with the DOI in <span style="font-family:var(--afdb-mono)">. If you are not
certain the reference exists exactly as you would write it, output instead:

    <div class="src">[UNVERIFIED — need: <shape of evidence>]</div>

Never invent a DOI. Never adjust a real finding to fit the slide.

# Write the slide now.

Output only the <section> block. No commentary, no explanation of your choices.
````

---

## Reviewing what comes back

Three checks, in this order:

1. **Read only the visible text aloud.** If it takes more than 20 seconds, it is
   still a document. Send it back with "cut the visible text by half; move what
   you cut into the notes."
2. **Check the notes are speech.** If the notes are bullet points, they are not
   notes. Ask again for full sentences in the second person.
3. **Check the French independently.** Do not assume it mirrors the English —
   count the components in both.

Then paste into the deck source and run `python tools/build_slides.py`. The build
will tell you if you are over budget; it is a more reliable reader than you are
at this point in the day.
