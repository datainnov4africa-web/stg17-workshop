# P5 · Speaker notes

The density contract moves most of a deck's substance into
`<aside class="notes">`. That makes the notes the deck's real content, and it
means a deck with thin notes is not a finished deck — it is a set of headlines.

Use this when slides exist and the notes are empty or were written as bullets.

---

## The prompt

````text
You are writing speaker notes for a session at an African Development Bank and
AU STATAFRIC technical workshop. The audience are heads of statistical
methodology and IT at African national statistical offices — expert in official
statistics, non-expert in machine learning, attending in their second or third
working language as often as their first.

# The slide

Visible content (this is ALL the audience can see):
---
{{SLIDE_VISIBLE}}
---

Its place in the session: slide {{SLIDE_N}} of {{SLIDE_TOTAL}}, {{TIMING}}.
Slide before: {{PREV_TITLE}}
Slide after: {{NEXT_TITLE}}

# What speaker notes are here

Not a summary of the slide. The audience can read. The notes are everything the
presenter knows that is NOT on the slide:

  - the reason this matters to a statistical office specifically
  - the caveat, the exception, or the thing that is more complicated than shown
  - the concrete example, named, with its source
  - what the audience usually asks at this point, and the honest answer
  - the transition into the next slide

# Form

  - 80–150 words. Longer than that and no one reads them under pressure.
  - Full sentences, second person, addressed to the presenter.
  - Include at least one delivery instruction: "pause here", "ask for a show of
    hands", "do not read the table aloud", "let this sit on screen".
  - Where the slide shows a number, the notes say where the number came from.
  - Never begin with "In this slide we see". Begin with the substance.

# The register that works

Write as an experienced colleague briefing another before they walk in — direct,
specific, occasionally warning them about something. Compare:

  WEAK:   "This slide explains the three levers available for adapting a model."
  STRONG: "If you take one slide from this deck into a procurement meeting, take
          this one. The ordering is not a matter of taste — it is ordered by cost
          and by how easily the output can be audited, two criteria the office
          already applies to everything else it buys. Exhaust lever one before
          reaching for lever two. In practice most offices never need lever three."

The second one tells the presenter what to DO with the slide.

# Bilingual

Produce the English notes, then the French notes. The French is written in
French, not translated from the English: same content, same length, natural
register. Use « » for quotations and 09h30 rather than 09:30.

# Output

Two blocks, nothing else:

<aside class="notes">
English notes.
</aside>

<aside class="notes">
Notes françaises.
</aside>
````

---

## A note on facilitators

These notes are read by someone who may not have written the deck — the workshop
runs across five days with several presenters, and a session may be delivered by
a colleague at short notice. Write them for that person, not for yourself. The
test: could someone who has never seen this deck deliver the slide from the notes
alone?
