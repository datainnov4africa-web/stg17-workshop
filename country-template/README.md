<!--
  STG17 country repository template.
  Replace every <PLACEHOLDER> below, delete this comment, and delete any section
  that does not apply. Keep the structure — it is what makes country work
  comparable across the continent.
  Français : voir README.fr.md
-->

# <Indicator name> — <Country>

🇬🇧 English · [🇫🇷 Français](README.fr.md)

> One paragraph: what this repository contains, who produced it, and what
> question it answers. Written for a colleague in another national statistical
> office who has five minutes.

**Produced by** <Your office> during the STG17 technical workshop
*Emerging Issues, Emerging Practice*, African Development Bank and AU STATAFRIC,
<month year>.

[![Pages](https://img.shields.io/badge/site-live-1B7A43)](https://<owner>.github.io/stg17-<iso3>/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)
[![Code: MIT](https://img.shields.io/badge/code-MIT-0B2545)](LICENSE)
[![Data: see LICENSE-DATA](https://img.shields.io/badge/data-see%20LICENSE--DATA-F2A900)](LICENSE-DATA)

---

## Results

> Two or three figures, one sentence each. **Show the answer before the method.**
> Most readers stop here, and that is fine — this section should be enough for
> them to know whether the rest is worth their time.

![<Figure 1>](outputs/figures/<figure1>.png)

*<One sentence saying what the reader should take from this figure.>*

| Headline figure | Value | Period |
|---|---|---|
| <e.g. National Sum of Lights growth> | <x.x % / year> | <2016–2024> |
| <e.g. Territory above the lit threshold> | <xx %> | <2024> |
| <e.g. Correlation with official indicator> | <r = 0.xx> | <2020> |

---

## Data sources

| Source | Product / version | Period | Licence | Retrieved |
|---|---|---|---|---|
| NASA Black Marble | VNP46A4 collection 002 | <2016–2024> | Public domain (US Government) | <YYYY-MM-DD> |
| Ookla Open Data | Fixed broadband, quarterly | <2024 Q1–Q4> | **CC BY-NC-SA 4.0** | <YYYY-MM-DD> |
| WorldPop | Constrained 100 m | <2024> | CC BY 4.0 | <YYYY-MM-DD> |
| <Your office> | ADM1 / ADM2 boundaries | <2024> | <your licence> | — |
| <Your office> | <official subnational indicator> | <2020> | <your licence> | — |

> Delete the rows you did not use. **Do not delete the licence column** — the
> licence of your output is determined by the strictest licence in this table.
> See [LICENSE-DATA](LICENSE-DATA).

---

## Method

> Short. Five to ten sentences. Link to the notebook for anything a reader would
> need in order to reproduce rather than merely to understand.

1. <Acquisition>
2. <Clipping to national boundaries>
3. <Zonal statistics at ADM2, aggregated to ADM1 and ADM0>
4. <Validation against the official indicator>

Parameters that a reader could not guess and that change the numbers:

| Parameter | Value | Why |
|---|---|---|
| Lit threshold | <0.5> nW·cm⁻²·sr⁻¹ | <reason> |
| Administrative level | ADM<2> | <reason> |
| Years excluded | <none / 2018 (incomplete tile coverage)> | <reason> |
| Boundary file | <source> | <reason> |

Full detail: [`notebooks/`](notebooks/).

---

## Limitations

> **This section is not optional and is not a disclaimer.** It is what makes the
> rest of the repository credible. Answer these four questions specifically for
> your country — the generic version below is a starting point, not an answer.

**What this indicator actually measures.** <e.g. Night-time radiance is a proxy
for lit infrastructure. It is not GDP and it is not the household connection
rate.>

**Choices a reader would not guess.** <The lit threshold. The boundary file. The
product version. Any years excluded.>

**What is known to be wrong or uncertain in this country.** <e.g. Gas flares in
<region> dominate that region's total. The capital saturates the sensor above
<value>. <n> years are missing a tile and were excluded.>

**What this should not be used for.** <e.g. This should not be used to allocate
budget between districts without a ground-truth check.>

---

## Reproduce

```bash
git clone https://github.com/<owner>/stg17-<iso3>.git
cd stg17-<iso3>
pip install -r requirements.txt
jupyter lab notebooks/
```

Every notebook is parameterised by a single variable at the top:

```python
COUNTRY_ISO3 = "<ISO3>"
```

Change it and the pipeline runs on another country. That is deliberate: this work
is meant to be reused.

The raw inputs are **not** in this repository — they are large and, in some cases,
not ours to redistribute. [`data/README.md`](data/README.md) says where each one
came from and how to fetch it.

---

## Licence

| What | Licence |
|---|---|
| Code and notebooks | [MIT](LICENSE) |
| Written content and figures | CC BY 4.0 |
| Derived data in `data/processed/` and `outputs/` | [see LICENSE-DATA](LICENSE-DATA) |

> ⚠️ **If any input is Ookla open data**, the derived output inherits
> **CC BY-NC-SA 4.0** — NonCommercial and ShareAlike both propagate. It cannot be
> released under your office's standard open-data licence. See
> [the publication guide](https://stg17-africa.github.io/stg17-workshop/publish/).

## Citation

See [`CITATION.cff`](CITATION.cff), or use the **Cite this repository** button at
the top right of this page.

## Maintenance

**Maintainer:** <Name>, <role>, <institutional email>

A person, not a department. If they move on, this line is updated. Issues and
pull requests are welcome, including from other national statistical offices.

---

<sub>Produced under the STG17 Action Plan 2025–2030, Work Package 4.2, with the
African Development Bank as Secretariat of STG17 and AU STATAFRIC. Neither the
AfDB nor AU STATAFRIC takes a position on any boundary delimitation shown in this
repository.</sub>
