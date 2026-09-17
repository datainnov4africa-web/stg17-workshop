# P4 · Illustration

For imagery, not schematics. A satellite view of the continent at night, a
server room at a believable institutional scale, an abstract field of connected
nodes. If the thing you want has boxes and arrows, use [P3](P3-diagram-svg.md)
instead — a generator draws arrows badly and letters them worse.

The existing slot catalogue lives in [the figure-slot catalogue](figure-slots.md).
This file is the prompt for creating a *new* slot.

---

## The prompt

````text
Generate a 16:9 landscape illustration for a technical presentation published by
the African Development Bank.

# Subject

{{IMAGE_BRIEF}}

# Register

Editorial and institutional, in the visual language of a development bank annual
report — not a technology company's marketing, and not science fiction. Calm,
factual, restrained. Nothing exaggerated for drama: if the subject is a dark
continent at night, the darkness should read as a measurement, not as a mood.

# Palette

Deep navy #0B2545, jade green #1B7A43, amber #F2A900, and neutral greys.
Amber is the only warm accent and should be used sparingly, on the element that
matters. No other saturated colour anywhere in the frame.

# Absolute constraints

  - NO text, lettering, numerals, or writing of any kind anywhere in the image.
  - NO flags, national symbols, borders drawn as political lines, or coats of arms.
  - NO identifiable people, and no faces.
  - NO logos, including invented ones.
  - Composition must leave the LEFT THIRD of the frame visually quiet — a title
    will be placed there.
  - 16:9, minimum 1920×1080.

# Why those constraints

Every slide exists in English and French; text baked into an image would have to
be regenerated per language and would drift out of sync with the build. The
material is used across 55 African Union member states, so a recognisable flag or
face turns a general illustration into a statement about one country.

Produce the image.
````

---

## After you have the image

1. Save it at exactly the filename the slot names, under `slides/figures/`.
2. Replace the `<div class="figure-slot">…</div>` placeholder with
   `<img src="../../slides/figures/NAME.png" alt="…">` — and write a real `alt`,
   because the published site is read with screen readers.
3. Record the tool, the model version and the date in `slides/figures/CREDITS.md`.
4. Re-run `python tools/build_slides.py`.

**Before publishing, check the current terms of the tool you used.** Terms for
generated imagery change, and this material goes onto public GitHub Pages under
an institutional banner. Where the terms are unclear, leave the placeholder — a
dashed box that says "illustration pending" is honest, and a deck is not worse
for having one.
