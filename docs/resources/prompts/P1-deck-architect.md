# P1 · Deck architect

Turns an agenda entry into a slide-by-slide plan. Run this **before** writing any
slide. Its output is a plan you edit, argue with, and cut — not a draft.

Generate the filled version with `python tools/prompt.py P1 --deck NN`. Tokens in
`{{ }}` are substituted from `config/agenda.yml`, `stg17/theme.py` and
`tools/build_slides.py`.

---

## The prompt

````text
You are designing a conference presentation for the African Development Bank and
AU STATAFRIC, delivered to the heads of statistical methodology and IT of African
national statistical offices. Treat them as senior professionals who are expert
in official statistics and non-expert in machine learning. They are attending a
five-day technical workshop; this is one session inside it.

# The session

Title (EN): {{TITLE_EN}}
Title (FR): {{TITLE_FR}}
Day {{DAY}}, {{TIME}} — {{DURATION}} minutes, {{MODE}}
Stated purpose: {{DESC_EN}}
STG17 Action Plan activities addressed: {{PLAN}}

What happens immediately before: {{PREV_SESSION}}
What happens immediately after: {{NEXT_SESSION}}

# Your task

Produce a slide-by-slide PLAN. Not slide content — a plan. For each slide give:

  - a number and a one-line title that states a CLAIM, not a topic
    (write "Fine-tuning teaches style, not facts", not "About fine-tuning")
  - the slide TYPE, from this fixed set:
        title | divider | statement | figure | table | callout | cards | closing
  - the single idea it carries, in one sentence
  - what the presenter says that is NOT on the slide, in one sentence
  - the evidence it rests on: a specific paper, dataset, standard or framework —
    or the word NONE if it rests on argument alone

# Hard constraints

1. TIME. Budget 90 seconds per content slide, 20 seconds per divider, 3 minutes
   for any slide with a figure the audience must read. Your plan must fit
   {{DURATION}} minutes with 15% slack. State your arithmetic at the end.

2. DENSITY. Each slide will later be written to a hard limit of
   {{WORD_LIMIT}} visible words and {{TABLE_ROW_LIMIT}} table rows, with a budget
   of {{WORD_BUDGET}}. Plan slides that can live inside that. If an idea needs
   more, that is two slides, and you should plan them as two.

3. STRUCTURE. Open with a concrete artefact from the audience's own working life
   — a sentence from a real terms of reference, a line from a published table, a
   figure they would recognise. Do not open with definitions or with an outline
   slide. Close with what happens next in the workshop, not with "thank you".

4. ARC. Group content slides into 2–4 parts, each introduced by a divider slide
   that states what the part is for. A 30-minute session with no dividers reads
   as one undifferentiated block.

5. ONE ABSOLUTE. Somewhere in the deck there must be a single slide stating the
   line this material does not cross — the thing the audience must not do with
   what they have just learned. Mark which slide that is.

# Evidence rules

For every slide where you name evidence, give the actual reference: authors,
year, journal or institution. If you are not certain a specific paper exists
with that finding, write:

    [UNVERIFIED — need: <the shape of the evidence required>]

Do NOT substitute a plausible-looking citation. A fabricated DOI in a room of
statisticians costs more than an empty slot. I will supply the missing sources.

# Output format

A markdown table with columns: # | Title (claim) | Type | The one idea | Said,
not shown | Evidence.

Then, below the table:
  - the timing arithmetic
  - the 2–4 part names
  - which slide carries the absolute
  - a list of every [UNVERIFIED] slot, so I can work through it

Do not write any slide content. Do not write speaker notes. Plan only.
````

---

## How to use the result

Read the "Said, not shown" column first. If it is empty or thin for most slides,
the plan is a document outline, not a talk — send it back and say so.

Then cut. A first plan is reliably 30% too long, and the timing arithmetic the
model produces is reliably optimistic. Delete the slides you would skip if you
were running ten minutes late; what remains is usually the real deck.

Only then move to [P2](P2-slide-writer.md), one slide at a time.
