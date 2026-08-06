# Licensing and ethics

Three questions decide whether a product from this workshop can be published, and
they are separate questions. Getting the first two right and the third wrong is
the common failure.

## 1 · What licence does your output carry?

The licence of a derived product is determined by the **strictest** licence among
its inputs. It is not a preference.

| Source used | Its licence | What your derived product may carry |
|---|---|---|
| NASA Black Marble (VNP46A*) | US Government work, effectively public domain | Anything, including your office's own open-data licence |
| NOAA / EOG annual VNL | Public domain | Anything |
| WorldPop | CC BY 4.0 | CC BY 4.0 or stricter. Attribution required |
| geoBoundaries (gbOpen) | CC BY 4.0 | CC BY 4.0 or stricter |
| GADM | Academic use only, **no commercial redistribution** | Not suitable for a published national product |
| **Ookla Open Data** | **CC BY-NC-SA 4.0** | **CC BY-NC-SA 4.0 only** |

!!! danger "The Ookla trap"

    **NonCommercial** and **ShareAlike** both propagate. A population-weighted
    connectivity indicator derived from Ookla tiles:

    - may not be used for commercial purposes,
    - must itself be released under CC BY-NC-SA 4.0,
    - **cannot** be released under your office's standard open-data licence if
      that licence permits commercial reuse — which most do.

    This is not a reason to avoid the source. It is a reason to state it on the
    product and to raise the question internally *before* the indicator becomes
    part of a regular publication. Several offices will conclude that a negotiated
    agreement with Ookla or with national operators is the route to a freely
    reusable indicator — which is exactly the private-sector partnership
    discussion of Action Plan activity 3.1.

**Keep the piles separate.** If your NTL product should be freely reusable and
your Ookla product cannot be, publish them as two clearly separated products with
two `LICENSE-DATA` files. One bundle inherits the strictest terms for everything
in it.

## 2 · What may leave the building?

| Data | May it go to a commercial LLM API? | May it go into a public repository? |
|---|---|---|
| A published statistical yearbook | Yes | Yes |
| Aggregated indicators already released | Yes | Yes |
| Unreleased official figures | **No** | **No** |
| Microdata, however anonymised | **No** | **No** |
| Boundary files your office publishes | Yes | Yes |
| Personal data of any kind | **No** | **No** |

The Day 2 laboratory sends a document to an LLM API. Bring something your office
has **already published**. That is not a formality: the request leaves your
network, and you do not control what happens to it afterwards.

## 3 · What are you claiming?

The ethical question specific to this workshop is not about data protection — it
is about over-claiming.

A night-time lights series presented as "regional GDP" is a false statement, made
with real data, by a credible institution. That is more damaging than no
indicator at all, because it will be believed and it will inform decisions.

**The discipline:**

- State what the indicator measures, in one sentence, next to every figure.
- State the parameters a reader could not guess — the threshold, the boundary
  file, the product version, the years excluded.
- State the correlation with your official figures, with its coefficient, rather
  than asserting equivalence.
- State what the indicator should **not** be used for.

The Day 4 afternoon laboratory turns this into a formal document, and the country
template makes it a required section of the README. It is a deliverable, not a
disclaimer.

## 4 · Boundaries

Boundary depiction is politically sensitive in several member states. geoBoundaries
and FAO GAUL are convenient for a workshop and carry no legal weight anywhere.
Substitute your office's official boundaries before publishing, and expect the
subnational figures to shift — sometimes materially at ADM2.

Neither this workshop, the African Development Bank nor AU STATAFRIC takes a
position on any delimitation. A country repository represents its own office.

## 5 · A checklist before you publish

- [ ] Every input listed, with its licence and the date it was retrieved
- [ ] Output licence determined by the strictest input, not by preference
- [ ] Nothing confidential, nothing unreleased, no personal data — **including in the git history**
- [ ] No API keys, anywhere, including in notebook outputs
- [ ] Limitations statement present, specific, and about your country
- [ ] Boundary source named
- [ ] A named maintainer with an institutional email
