# P8 · French rendering

An English slide exists and the French must match it — in structure and in
density, not only in meaning. French runs roughly 15% longer than English, so a
faithful translation of a slide that sits at 100 words lands at 115 and fails the
build. The French has to be *written shorter*, which a translation prompt will
not do unless told.

---

## The prompt

````text
You are producing the French of a slide for an African Development Bank and
AU STATAFRIC workshop. The audience are francophone heads of methodology at
African national statistical offices.

# The English slide

{{SLIDE_EN}}

# This is not translation

Write the same slide in French. Same claim, same structure, same components in
the same order, same table shape, same number of source lines. But written as a
francophone statistician would write it — not as an English slide converted.

# The constraint that makes this hard

The English is {{WORD_COUNT}} visible words. The hard limit is {{WORD_LIMIT}};
the budget is {{WORD_BUDGET}}. French naturally runs longer, so you must
compress: prefer the shorter construction, drop an adjective the English could
afford, turn a relative clause into an apposition. Count your visible words —
excluding <aside class="notes">, SVG labels and <div class="src"> — and state
the count at the end.

If you cannot fit the meaning within the limit, say so explicitly rather than
overflowing. That is a signal the English slide is itself too dense.

# Conventions — French typography and this workshop's vocabulary

  - « guillemets » with non-breaking spaces inside, never "quotes"
  - non-breaking space before : ; ! ? and inside « »
  - times as 09h30, never 09:30
  - decimals with a comma: 0,71 — thousands with a thin space: 12 500
  - capitalise only the first word of a title
  - "données" is plural; "un office statistique" not "un bureau"

  Fixed terms — use these, they match the glossary and the notebooks:
    LLM = grand modèle de langage (keep "LLM" as the abbreviation)
    prompt engineering = ingénierie de prompt
    fine-tuning = affinage
    RAG = RAG (do not translate the acronym; gloss it once as
          "génération augmentée par récupération")
    agent = agent
    hallucination = hallucination
    night-time lights = lumières nocturnes
    Sum of Lights = Somme des lumières
    lit area = superficie éclairée
    blooming = halo lumineux
    gas flare = torchère
    zonal statistics = statistiques zonales
    boundaries = frontières administratives
    dataset = jeu de données
    machine learning = apprentissage automatique

# What must NOT change

  - Author names, years, journal titles, DOIs — reproduce them exactly.
  - Numbers and units.
  - The claim itself. If the English overclaims, the French overclaims
    identically; flag it to me separately rather than quietly correcting it.
  - The <span class="timing"> value.

# Output

The French body only — everything that goes after the <!--FR--> marker, including
its <aside class="notes">. No <section> wrapper, no commentary.

Then, on a line by itself: VISIBLE WORDS: n
````

---

## Verification

`python tools/build_slides.py` compares the two languages slide by slide and
fails on a mismatch in slide count, note count, source count or figure count. It
cannot check that the French *says* the same thing — that remains a human read,
and it is worth doing before a deck is presented in a francophone country.

The one thing to check by eye every time: that the French did not silently gain
or lose a callout. That is the most common structural drift, and it is invisible
in a diff of two long files.
