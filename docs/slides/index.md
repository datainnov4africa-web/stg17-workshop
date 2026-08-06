# Slides

Twelve decks carry the week. Each exists in **English and French**, built from a
single bilingual source so the two cannot drift apart.

Each deck is available three ways:

- **:material-presentation-play: Present** — the reveal.js deck, in the browser.
  Arrow keys to navigate, `S` for speaker notes, `F` for full screen, `O` for the
  slide overview.
- **:material-file-pdf-box: PDF** — append `?print-pdf` to the deck URL and print
  from the browser. Useful for the interpretation booth and for participants who
  want to annotate.
- **:material-microsoft-powerpoint: PPTX** — an editable derivative for
  facilitators. See the note at the bottom of this page.

---

## Day 1 · AI concepts and infrastructure

### Deck 01 { #deck-01 }
**The AI Family Tree: How the Concepts Fit Together** — 30 min

Building a shared concept map: AI, LLM, prompt engineering, RAG, fine-tuning,
agentic systems, agents, MCP. This half-hour sets the vocabulary used for the
rest of the week.

:material-progress-clock: *Day 1 batch*

### Deck 02 { #deck-02 }
**AI Infrastructure: What It Really Takes to Run AI in a Statistical Office** — 45 min

GPUs and accelerators, inference versus training, cloud/hybrid/on-premise, data
sovereignty for NSO microdata, cost modelling, open-weight versus proprietary.
What a realistic entry-level configuration looks like for an African NSO.

:material-progress-clock: *Day 1 batch*

---

## Day 2 · Prompt engineering and optimised use of LLMs

### Deck 03 { #deck-03 }
**Talking to Machines: The Craft of Prompt Engineering** — 75 min

:material-progress-clock: *Day 2 batch*

### Deck 04 { #deck-04 }
**From Good to Great: Prompt Optimisation** — 45 min

:material-progress-clock: *Day 2 batch*

### Deck 05 { #deck-05 }
**Choosing your Engine: speed, cost and sovereignty — working with Groq** — 45 min

:material-progress-clock: *Day 2 batch*

---

## Day 3 · Non-traditional data and the technologies that handle them

### Deck 06 { #deck-06 }
**Non-Traditional Data Sources: The Hidden Treasure** — 75 min

:material-progress-clock: *Day 3 batch*

### Deck 07 { #deck-07 }
**Engines of Scale: Big Data Technologies for Statistical Systems** — 45 min

:material-progress-clock: *Day 3 batch*

---

## Day 4 · Night-Time Lights

### Deck 08 { #deck-08 }
**Night-Time Lights: What the Darkness Tells Us** — 30 min

From DMSP-OLS to VIIRS/DNB; the Black Marble products and the EOG annual series;
what NTL proxies well and what it does not; the six artefacts, named here and met
hands-on at 10:30.

:material-check-circle:{ .ok } **Available**

<p>
<a class="md-button md-button--primary" href="08-night-time-lights-what-the-darkness-tells-us-en.html">Present (EN)</a>
<a class="md-button" href="08-night-time-lights-what-the-darkness-tells-us-fr.html">Présenter (FR)</a>
</p>

<p>
<a href="08-night-time-lights-what-the-darkness-tells-us-en.html?print-pdf">PDF (EN)</a> ·
<a href="08-night-time-lights-what-the-darkness-tells-us-fr.html?print-pdf">PDF (FR)</a> ·
<a href="pptx/08-ntl-what-darkness-tells-us-en.pptx">PPTX (EN)</a> ·
<a href="pptx/08-ntl-what-darkness-tells-us-fr.pptx">PPTX (FR)</a>
</p>

---

## Day 5 · Publishing and results

### Deck 09 { #deck-09 }
**Assisting Countries in Publishing their Work** — 75 min

:material-progress-clock: *Day 5 batch*

### Deck 10 { #deck-10 }
**Opening and closing ceremony** — 45 min + 15 min

:material-progress-clock: *Day 5 batch*

---

## Supporting decks

### Deck 11 · Country experience template { #deck-11 }

The six-slide template participants use for the Day 1 morning exchange, with the
prompts written into the speaker notes.
[Read the guidance →](../before/country-slides.md)

:material-progress-clock: *Day 1 batch*

### Deck 12 · Facilitator brief { #deck-12 }

How to run the week: timing, the two-track mechanic, when to trigger a fallback,
what to record on the wall board.
[Facilitator resources →](../resources/facilitators.md)

:material-progress-clock: *Day 5 batch*

---

## Notes for facilitators

!!! info "The HTML deck is the source of truth"

    Decks are built from `slides/decks/<id>.deck.html` by
    `python tools/build_slides.py`. The PPTX files are **derived** — edits made in
    PowerPoint do not flow back, and each generated file says so on its last
    slide. If a change should be permanent, edit the deck source and rebuild.

!!! warning "SVG diagrams do not survive the PPTX conversion"

    The timelines, pipelines and schematics are hand-authored SVG, which
    `python-pptx` cannot rasterise. Each affected PPTX slide carries a placeholder
    naming the figure. Screenshot it from the HTML deck — two seconds, and a
    better result than any automatic conversion.

!!! tip "Presenting offline"

    reveal.js loads from a CDN. If the venue network blocks it, the deck degrades
    gracefully into a scrollable document rather than a blank page — but for a
    proper presentation, run `python tools/vendor_reveal.py` beforehand to
    download reveal.js into `slides/vendor/`. The USB keys distributed on Day 0
    already carry the vendored version.
