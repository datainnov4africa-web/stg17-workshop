# prompts-pptx — working files, not published

Prompts to paste into Claude web (claude.ai) to build the PowerPoint decks.

**Nothing in this folder is published.** It sits outside `docs/`, so MkDocs never
sees it. That is deliberate.

## Using one

1. Open the file for the deck you want, select all, copy.
2. Paste into a new Claude web conversation.
3. Claude writes a `python-pptx` script, runs it, and returns two `.pptx` files —
   English and French.
4. Download both and put them where they belong.

One conversation per deck. Starting fresh matters: a conversation that has already
built one deck carries its choices into the next.

## The files

  `deck-NN.txt`             The content is fixed and included in full. Claude does
                            layout only — the references and speaker notes are the
                            reviewed ones from the repository.
  `NEW-DECK-generator.txt`  For the sessions with no deck written yet. Claude
                            writes the content as well. Everything it produces
                            needs its references checked before use.

## Regenerating

These files are generated. When a deck source changes, run:

    python tools/pptx_prompt.py

Do not edit a `deck-NN.txt` by hand — the next run overwrites it. Edit the deck
source under `slides/decks/` instead.

## Two things to know about the result

**Figures do not transfer.** Each hand-drawn SVG becomes a labelled placeholder,
and Claude lists them at the end. Screenshot them from the HTML deck at
`docs/slides/` and drop them in. This is deliberate: a diagram redrawn from its
description loses the meaning it was drawn to carry.

**The reveal.js deck stays the source of truth.** It is what the build validates
for density, visual weight and bilingual symmetry, and what the site publishes.
Treat a `.pptx` as output — never edit content in it, because the change will not
come back.
