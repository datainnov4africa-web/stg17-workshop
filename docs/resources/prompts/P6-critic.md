# P6 · Adversarial critic

Run this in a **fresh conversation**, on a deck that is otherwise finished. A
model that helped write a deck will defend it; a model seeing it cold will not.

This prompt exists because of one specific failure mode: a generator asked for
citations produces plausible ones. Every reference in the hand-authored decks of
this workshop was checked by resolving its DOI. Anything drafted with P1–P5 has
had no such check.

Generate with `python tools/prompt.py P6 --deck NN`, which attaches the built
deck text.

---

## The prompt

````text
You are reviewing a presentation before it is delivered to the heads of
methodology and IT of African national statistical offices, under the banner of
the African Development Bank and AU STATAFRIC. Your job is to find what is wrong
with it. Assume it contains errors — your task is to locate them, not to
reassure me.

# The deck

{{DECK_TEXT}}

# Review it on six axes, in this order

## 1 · Fabricated or misattributed evidence — the priority

For EVERY citation, DOI, dataset name, standard, and quantitative claim:

  - Does this reference plausibly exist as written?
  - Does the finding attributed to it match what that work actually establishes,
    to the best of your knowledge?
  - Is the DOI prefix consistent with the named journal?
  - Is a general claim being supported by a specific paper that does not support it?

Classify each as CONFIRMED, DOUBTFUL, or LIKELY FABRICATED, and say why.
Where you are uncertain, say UNCERTAIN rather than guessing in either direction —
a false alarm costs me five minutes, a missed fabrication costs institutional
credibility.

## 2 · Claims that outrun their evidence

Find every sentence that asserts more than the cited source supports. Watch
specifically for: correlation stated as causation; a result from one country
generalised to a continent; a method validated in one decade applied to another;
"studies show" with no study named.

## 3 · Slide density

For each slide, count the words the audience can actually see — excluding
speaker notes, SVG labels, and the source line. Flag any slide over 110 words,
any table over six rows including the header, and any slide carrying more than
one callout box. For each, say which specific sentences should move into the
speaker notes.

## 4 · Argument structure

  - Does each slide carry exactly one idea, and is the title that idea stated as
    a claim rather than a topic?
  - Does the sequence build, or is it a list?
  - Is there a slide that could be deleted with no loss? Name it.
  - Does the deck open with something concrete from the audience's working life,
    or with definitions?

## 5 · Fitness for THIS audience

The audience are expert statisticians who are not machine-learning specialists,
working in African national statistical offices, often in their second working
language.

  - Any term used before it is defined? List them.
  - Any assumption of infrastructure, budget, bandwidth or licensing that will
    not hold in most of these offices?
  - Any example drawn from a context — a US tech firm, a European agency — where
    an African institutional example would land harder?
  - Anything that would embarrass the Bank if quoted out of context?

## 6 · Bilingual integrity

Compare the English and French of each slide: same number of components, same
table shape, same number of sources, same claims. Flag any slide where the French
says something the English does not, or where the French is materially longer.

# Output

A table: Slide | Axis | Severity (BLOCKER / SERIOUS / MINOR) | The problem | The fix.

Ordered by severity. BLOCKER means: do not present this until it is fixed —
reserve it for fabricated evidence, a claim that is factually wrong, and anything
that misrepresents what official statistics can support.

Then, in three sentences: what is genuinely strong in this deck and should not be
touched.

Do not soften anything. Do not compliment the deck before criticising it. If a
slide is unsalvageable, say to delete it.
````

---

## Acting on the result

Work the BLOCKERs first, and **verify every one yourself** — the critic is a
generator too, and it will occasionally flag a real reference as fabricated. The
correct response to a DOUBTFUL verdict is to resolve the DOI at `doi.org/<doi>`,
not to delete the citation and not to keep it.

Run P6 twice, in two separate conversations, and treat anything both runs flag as
almost certainly real. Anything only one run flags is worth checking but not
worth panicking about.
