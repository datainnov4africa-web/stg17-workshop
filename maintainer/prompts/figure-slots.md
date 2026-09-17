# Figure slots — the illustration catalogue

Diagrams in these decks are hand-authored SVG — a timeline, a pipeline, a
schematic of blooming and saturation. SVG is the right tool there: it stays
crisp at any projector resolution, it is versioned as text, and its labels are
translated by the same build that translates the slide.

**Illustrative imagery is a different problem.** A photoreal night view of a
West African coastline, a stylised satellite over the continent, an icon set — a
generator does these far better than hand-written SVG. This file holds the
prompts for those, one per slot.

## How a slot works

Where a deck expects generated imagery, it renders a dashed placeholder:

```html
<div class="figure-slot">
  Illustration: <code>figures/08-cover-night-africa.png</code><br>
  See resources/prompts/figure-slots.md · slot 08-A
</div>
```

To fill it:

1. Run the prompt below in Gemini (or any image generator you have access to)
2. Save the result at **exactly** the filename given in the slot
3. Replace the `<div class="figure-slot">…</div>` with
   `<img src="../../slides/figures/08-cover-night-africa.png" alt="…">`
4. Re-run `python tools/build_slides.py`

The deck works with or without the image. A placeholder is honest; a broken
image tag in front of forty people is not.

## House rules for every prompt

Append this to any prompt so the result matches the workshop identity:

> Colour palette restricted to deep navy `#0B2545`, jade green `#1B7A43`, amber
> `#F2A900`, and neutrals. Clean, editorial, institutional register — suitable
> for a development bank publication. No text or lettering in the image. No
> flags, no national symbols, no identifiable people. 16:9 landscape.

**Why no text in the image:** every deck exists in English and French. Text baked
into an illustration would have to be regenerated per language and would drift.
All labelling belongs in the HTML, where the build translates it.

**Why no flags or identifiable people:** the material is used across 55 member
states, and a recognisable flag or face turns a general illustration into a
statement about one country.

---

## Deck 08 · Night-Time Lights

### Slot 08-A — Title background
`figures/08-cover-night-africa.png`

> A satellite view of the African continent at night, seen from low orbit. Coastal
> cities appear as small clusters of warm amber light against a deep navy-black
> landmass; the interior is largely dark with sparse scattered points. A faint
> atmospheric limb glows along the curve of the horizon. Photorealistic, calm,
> high altitude, no clouds obscuring the coast. Nothing exaggerated — the darkness
> should read as fact, not as drama.

### Slot 08-B — Blooming, illustrative
`figures/08-blooming-city.png`

> A stylised overhead view of a mid-sized city at night. The built-up area is a
> compact dense grid; the light it emits spreads well beyond it as a soft glow,
> visibly larger than the city itself. Two subtle outlines are implied: the tight
> edge of the built area, and the much wider edge of the lit area. Clean
> illustration, not photographic. Amber light on a dark navy ground.

### Slot 08-C — Gas flare against a settlement
`figures/08-flare-vs-city.png`

> An overhead night view of a sparsely populated region. Near the centre, a small
> settlement emits a modest warm glow. Some distance away, isolated in otherwise
> empty terrain, a single intensely bright point burns much brighter than the
> settlement — an industrial flare. The visual contrast between "many people, some
> light" and "no people, extreme light" is the whole point of the image.

---

## Deck 01 · The AI Family Tree

### Slot 01-A — Title background
`figures/01-cover-concept-network.png`

> An abstract network of connected nodes, arranged so that clusters are visible
> but no hierarchy is implied. Node sizes vary. Connections are thin and precise
> rather than glowing. Jade green and amber nodes on a deep navy field. Restrained
> and technical, closer to a schematic than to a science-fiction visual.

---

## Deck 02 · AI Infrastructure

### Slot 02-A — Title background
`figures/02-cover-datacentre.png`

> The interior of a modest, well-organised server room — two or three racks, not a
> hyperscale facility. Cool neutral lighting with amber status indicators. The
> scale should read as *achievable by a national institution*, not as a technology
> company's flagship data centre. That distinction is the point of the session.

---

## Deck 06 · Non-Traditional Data Sources

### Slot 06-A — Title background
`figures/06-cover-data-sources.png`

> A layered composition suggesting several distinct data sources over a single
> landscape: a satellite pass, a mobile network, a sensor, a transaction record.
> The layers are stacked and slightly offset, so that they read as separate
> observations of the same territory rather than as one merged image. Abstract,
> no literal icons, no text.

---

## Deck 07 · Engines of Scale

### Slot 07-A — Title background
`figures/07-cover-pipeline.png`

> An abstract representation of data flowing through stages of processing:
> ingestion, storage, distributed computation, indexing. Rendered as a horizontal
> flow of particles that gather, split across parallel paths, and recombine.
> Jade and amber on navy. Technical, calm, no glow effects.

---

## Adding a new slot

1. Give it an id: deck number, then a letter — `03-A`, `03-B`
2. Add the placeholder `<div class="figure-slot">` in the deck source
3. Add the prompt here, under its deck heading, with the exact target filename
4. Keep the house rules paragraph in mind — no text, no flags, no people

## Licensing note

Images produced by a generative model may carry terms that restrict
redistribution, and those terms change. Before an illustration goes into a deck
that will be published on GitHub Pages, check the current terms of the tool you
used, and record the tool and the date in `slides/figures/CREDITS.md`. Where the
terms are unclear, prefer a hand-authored SVG — which is why the substantive
diagrams in these decks are SVG in the first place.
