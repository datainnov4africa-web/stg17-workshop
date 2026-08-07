# P3 · Diagram author

Produces a publication-grade schematic as inline SVG. This is the prompt that
does the most work: the diagrams are what separates these decks from a text
deck, and SVG is the only figure format that stays crisp on a projector, is
versioned as text, and gets its labels translated by the same build that
translates the slide.

Use this for anything with structure — a timeline, a pipeline, a decision tree, a
comparison, a mechanism. Use [P4](P4-illustration.md) for atmosphere and imagery.

Generate with `python tools/prompt.py P3 --deck NN --figure "what it shows"`.

---

## The prompt

````text
You are producing a technical diagram for an African Development Bank
presentation, as inline SVG. It will be projected at 1280×720 and also printed to
PDF, so it must be legible at both.

# What the diagram must show

{{FIGURE_BRIEF}}

Slide it belongs to: {{SLIDE_TITLE}}
The single thing a viewer should understand within five seconds:
{{FIGURE_TAKEAWAY}}

# Format — exact

Output a single <figure> block containing one <svg> and, if the diagram needs a
caption that states a consequence, one <figcaption>.

<figure>
<svg viewBox="0 0 1180 H" xmlns="http://www.w3.org/2000/svg" role="img"
     aria-label="one sentence describing the diagram for a screen reader">
  <g font-family="Inter,sans-serif">
   ...
  </g>
</svg>
<figcaption>One sentence. What the diagram means, not what it contains.</figcaption>
</figure>

  - viewBox width is ALWAYS 1180. Choose H between 200 and 320. Nothing taller
    than 320 — it will collide with the heading.
  - No width/height attributes on the <svg>; the stylesheet scales it.
  - No <style> block, no CSS classes, no external references, no fonts beyond
    the font-family attribute. Everything inline.
  - Arrowheads via <defs><marker>. Give every marker a UNIQUE id — this diagram
    will be duplicated into a French copy in the same HTML document, and a
    repeated id silently breaks one of the two. Suffix the French copy's ids
    with "f".

# Palette — no other colour

  navy    #0B2545   structure, the authoritative box, headings
  jade    #1B7A43   the normal path, arrows, the "good" state
  amber   #F2A900   the exception, the warning, the thing to look at
  ink     #33403A   body labels on light ground
  muted   #6B7B75   secondary labels, axes, hairlines
  line    #D5E6DF   rules and grid
  wash    #F4F8F5   the fill of an ordinary box
  white   #FFFFFF   text on navy or jade
  fail    #C0392B   only for a genuine error state

On a dark slide (<section class="night">) use #11131f for panel fills and
#95A5A0 for labels.

# Typography inside the diagram

  17–19px  box titles, bold (font-weight 700–800)
  15–16px  labels and axis values
  13–14px  secondary notes inside a box
  12px     absolute minimum — below this it is unreadable projected

Never rely on colour alone to carry meaning: a viewer with a colour vision
deficiency, and a black-and-white printout, must both still work. Use position,
weight, a dashed versus solid stroke, or an explicit label.

# Composition rules

1. Left to right for process, top to bottom for hierarchy. Do not mix.
2. Rounded rectangles, rx=10 to rx=14. Consistent within one diagram.
3. Give every element air. If boxes are closer than 20px apart, use fewer boxes.
4. Label the arrows if the transition is not obvious from the boxes.
5. Put the takeaway IN the diagram as a line of text at the bottom, in amber
   #8a6100 bold, 17px. A diagram that needs the presenter to explain what it
   means has not finished being designed.
6. At most 7 primary elements. If the subject needs more, it needs two diagrams.

# What makes these diagrams work — study the pattern

The strongest diagram in this deck set shows a language model predicting a
token: input boxes on the left, the model as a navy block in the centre, a
probability distribution as three horizontal bars on the right, and a dashed
amber curve looping back from the output to the input with the label
"pick one · append it · run the whole thing again". Underneath, one line of navy
text states the consequence: "No lookup. No database. No step where the model
checks whether it is right."

That is the shape to aim for: mechanism on top, consequence stated underneath,
and the one element that carries the insight drawn in amber so the eye finds it.

# Text in the diagram must be translatable

Every <text> element will be duplicated and rewritten in French. Keep labels
short, avoid embedding numbers inside sentences, and never letter-space or
manually position individual characters — French labels run longer and will
break any hand-tuned spacing.

# Produce it now

Output the English <figure> block, then the French <figure> block with every
label translated and every marker id suffixed with "f". Nothing else — no
explanation.
````

---

## Checking the result

Open the built deck and look at it at 100%, then step back two metres from the
screen. Most generated SVG fails one of these:

- **Text overflowing its box.** The model cannot measure text. Widen the box or
  shorten the label; do not shrink the font below 12px.
- **Duplicate marker ids** between the EN and FR copies — the symptom is arrows
  that lose their heads in one language only.
- **A legend.** If the diagram needs a legend, it has too many encodings. Label
  the elements directly.

`python tools/build_slides.py` checks that the EN and FR figure counts match, so
a dropped French diagram fails the build rather than shipping silently.
