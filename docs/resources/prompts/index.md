# Prompt library — building STG17 presentations with an AI assistant

These prompts exist so that a session owner who is not a designer can produce a
deck that stands next to the hand-authored ones. They are not "write me a
presentation" one-liners. Each carries the design system, the density contract
and the evidence rules of this workshop, because those are the things a
generator gets wrong when you do not state them.

> **A generator is a drafting tool, not an author.** Every factual claim it
> returns is a claim *you* are publishing under an AfDB and STATAFRIC banner.
> Prompt P6 exists specifically to catch invented citations before they reach a
> room of statisticians.

## Which prompt for which job

| # | Prompt | Use it when | Works well in |
|---|--------|-------------|---------------|
| **P1** | [Deck architect](P1-deck-architect.md) | You have a session in the agenda and nothing else. Produces a slide-by-slide plan, not prose. | Claude, ChatGPT, Gemini |
| **P2** | [Slide writer](P2-slide-writer.md) | You have the plan and need slide *n* written to the density contract, in deck HTML. | Claude, ChatGPT |
| **P3** | [Diagram author](P3-diagram-svg.md) | A slide needs a schematic. Produces inline SVG in the AfDB palette, bilingual-ready. | Claude, ChatGPT |
| **P4** | [Illustration](P4-illustration.md) | A slide needs photographic or atmospheric imagery, not a schematic. | Gemini, Imagen, Midjourney |
| **P5** | [Speaker notes](P5-speaker-notes.md) | The slides are done and carry no prose. This writes what the presenter says. | Claude, ChatGPT |
| **P6** | [Adversarial critic](P6-critic.md) | Before a deck is published. Hunts invented references, unsupported claims, overloaded slides. | Claude, ChatGPT |
| **P7** | [Native deck build](P7-native-deck.md) | You want a genuinely designed PowerPoint or Gamma deck. **Start here if the automated PPTX disappointed you** — see the note below. | Gamma, Copilot, Claude |
| **P8** | [French translation](P8-translate-fr.md) | An English deck exists and the French must match it in density, not just in meaning. | Claude, ChatGPT |

A normal deck runs **P1 → P2 (×n) → P3/P4 → P5 → P8 → P6**. Run P6 last, in a
fresh conversation, so the critic has not seen the drafting.

## Why the automated PowerPoint is not the answer

`tools/build_pptx.py` produces the files in `docs/slides/pptx/`, and they are a
skeleton, not a presentation. Measured on `01-ai-family-tree-en.pptx`: the deck's
opening slide carries three quoted sentences from real terms of reference in the
HTML, and **20 words** in the PPTX — the eyebrow, the title and the footer. The
glossary slide carries eight terms in the HTML and **11 words** in the PPTX. The
body of every slide is dropped.

That is not a tuning problem. A reveal.js slide is laid out by CSS — measures in
`ch`, flex columns, a callout sized so a second one will not fit. PowerPoint has
no equivalent of any of that, so a faithful automatic conversion does not exist.
The honest options are: keep the PPTX as a title-and-heading handout skeleton and
say so, or build the PowerPoint natively with **[P7](P7-native-deck.md)**, which
hands the full design system to a tool that actually lays out slides.

The reveal.js deck stays the source of truth either way. It is what the build
validates for density and bilingual symmetry, and it is what the site publishes.

## Generate a filled-in prompt

Do not copy these files by hand. `tools/prompt.py` injects the live palette,
the density thresholds actually enforced by the build, and the session's own
agenda entry, so a prompt can never drift from the repository:

```bash
python tools/prompt.py --list                    # what is available
python tools/prompt.py P1 --deck 02              # architect a deck for session 02
python tools/prompt.py P2 --deck 02 --slide 4    # write one slide
python tools/prompt.py P3 --deck 08 --figure "DMSP to VIIRS timeline"
python tools/prompt.py P8 --deck 01 --slide 9    # the French of slide 9
python tools/prompt.py P6 --deck 01 --copy       # critique, deck attached, to clipboard
```

The command prints the finished prompt to stdout, and `--copy` puts it on the
clipboard. Paste it into the assistant.

Anything it cannot resolve is reported on stderr rather than pasted as a raw
`{{TOKEN}}`. Four values have no source in the repository — a slide's *type*,
*idea*, *spoken line* and *evidence* come from the P1 plan, which lives in your
notes. Fill those by hand; the warning is there to stop you forgetting.

`--lang fr` selects which language of the deck the tool reads slides from. The
prompt bodies themselves stay in English: they are the design contract, and one
contract in one language cannot drift against itself. Every prompt instructs the
model to produce French output where French is what you need — that is what
[P8](P8-translate-fr.md) is for.

## The four rules every prompt carries

These are repeated inside each file because a generator obeys what is in its
context, not what is in a neighbouring document.

**1 · One idea per slide.** Over 110 visible words or six table rows fails
`tools/build_slides.py`. The budget is 75. Prose belongs in
`<aside class="notes">`.

**2 · Every number carries a source.** A claim with no citation is cut, not
softened. Prompts instruct the model to mark anything it cannot source as
`[UNVERIFIED]` rather than dropping the marker — an unverified claim you can see
is safer than a confident one you cannot.

**3 · The palette is fixed.** Navy `#0B2545`, jade `#1B7A43`, amber `#F2A900`,
ink `#33403A`, muted `#6B7B75`, hairline `#D5E6DF`, wash `#F4F8F5`. Generated
material that introduces a fifth accent colour is rejected in review.

**4 · Nothing is written twice.** Output must be a single bilingual
`.deck.html` source using `<!--EN-->` / `<!--FR-->` markers. Two separate files
drift within a week.

## What these prompts will not do

They will not invent a case study, a country statistic, or a paper. Where a
slide needs one, the prompt asks the model to state the *shape* of the evidence
it would need — "a peer-reviewed estimate of the elasticity of night-time lights
to GDP in West Africa" — and leave you to supply it. That is deliberate. The
2012–2022 night-time-lights literature in this workshop was assembled by
checking each DOI resolves; a generator asked for citations will produce
plausible ones that do not exist.

## Licensing

Text you generate and edit is yours to publish under the workshop's licence.
Images are not automatically so — see the licensing note in
[the figure-slot catalogue](figure-slots.md) and record the tool and date in
`slides/figures/CREDITS.md` before publishing any generated image.
