# Publish your country's work

By Friday morning your team has three things: a dashboard, a set of connectivity
indicators, and a night-time lights analysis with a limitations statement. This
page is the route from those files to a **public, documented, citable product**
your office can stand behind — and that another African country can reuse.

Allow **45 minutes** for the first repository. Subsequent ones take ten.

!!! abstract "What you will have at the end"

    - A public GitHub repository named `stg17-<iso3>`, with a README in English and French
    - A live website at `https://<your-org>.github.io/stg17-<iso3>/`
    - A licence that is *correct* — including the parts inherited from Ookla
    - Machine-readable metadata, so the work is discoverable rather than merely online
    - A DOI and a citation, so it can be referenced in a publication
    - A named maintainer, so it is still true in two years

---

## Step 0 · Decide what you are publishing, and what you are not

Before touching GitHub, split your week's output into three piles.

| Pile | Examples | What to do |
|---|---|---|
| **Publish** | Notebooks, aggregated indicators, maps, methodology, limitations statement | Everything below applies |
| **Publish with care** | Derived products from restrictively licensed sources; boundaries whose depiction is politically sensitive | Read [Step 4 on licensing](#step-4-licensing-the-part-that-is-easy-to-get-wrong) first |
| **Do not publish** | Microdata, anything under statistical confidentiality, unreleased official figures, API keys | Keep it out of the repository entirely — see the warning below |

!!! danger "Git remembers everything"

    Deleting a file in a later commit does **not** remove it from the repository.
    It stays in the history, and anyone can retrieve it. If you accidentally
    commit microdata or an API key:

    1. **Revoke the key immediately.** Rotation is the only real fix.
    2. Tell the Secretariat. Rewriting history on a published repository is
       possible but disruptive, and it is better done once, properly.

    The `.gitignore` in the country template already excludes `.env`, `*.csv` in
    `data/raw/`, and the usual traps. Do not weaken it without thinking about why
    each line is there.

---

## Step 1 · Start from the country template

Do not build the structure by hand. The template carries the conventions the
Secretariat needs in order to aggregate work across countries — and it carries the
GitHub Actions workflow that publishes your site.

1. Take the country template supplied with the workshop materials — it is on the
   USB key, and the facilitation team will send you the link
2. Create a new repository on GitHub and copy the template's files into it
3. Owner: your office's GitHub organisation if it has one, otherwise your account
4. Name: **`stg17-<iso3>`** in lowercase — `stg17-civ`, `stg17-tun`, `stg17-ken`
5. Visibility: **Public**

!!! question "Why this naming convention?"
    It is what makes the STG17 catalogue searchable. A single GitHub search for
    `stg17-` returns every country's work, and the Secretariat's aggregation
    scripts rely on it. A repository called `my-ntl-project` is invisible to both.

### What the template contains

```
stg17-<iso3>/
├── README.md              ← the front door, in English
├── README.fr.md           ← and in French
├── LICENSE                ← code licence (MIT)
├── LICENSE-DATA           ← data licence — read Step 4 before choosing
├── CITATION.cff           ← how to cite you
├── metadata.json          ← machine-readable description
├── notebooks/             ← your work, exactly as you ran it
├── data/
│   ├── raw/               ← gitignored: sources, not redistributed
│   ├── processed/         ← small derived outputs that ARE published
│   └── README.md          ← where each input came from, and its licence
├── outputs/
│   ├── figures/
│   ├── tables/
│   └── maps/
├── docs/                  ← the GitHub Pages site
│   └── index.md
└── .github/workflows/
    └── pages.yml          ← builds and publishes docs/ on every push
```

---

## Step 2 · Put your work in, and write the README

### The notebooks

Copy them in **exactly as you ran them**, outputs included. This is the one place
where committing notebook outputs is right: a reader who cannot execute your
pipeline should still be able to see what it produced.

Before committing, check three things:

- [ ] No API keys anywhere in a cell — search for `sk-`, `gsk_`, `Bearer`
- [ ] The `COUNTRY_ISO3` at the top is yours
- [ ] The notebook runs top to bottom on a fresh kernel

### The README

This is the only document most visitors will read. The template gives you the
skeleton; fill each section honestly.

```markdown
# Night-time lights and connectivity indicators — <Country>

One paragraph: what this repository contains, who produced it, and what
question it answers.

## Results
Two or three figures, with a sentence each. Show the answer before the method.

## Data sources
| Source | Product | Period | Licence | Retrieved |
|---|---|---|---|---|
| NASA Black Marble | VNP46A4 | 2016–2024 | Public domain | 2026-06-12 |
| Ookla Open Data | Fixed, quarterly | 2024 Q1–Q4 | CC BY-NC-SA 4.0 | 2026-06-12 |
| <Your office> | ADM1 boundaries | 2024 | <your licence> | — |

## Method
Short. Link to the notebook for detail.

## Limitations
**Not optional.** See below.

## How to reproduce
The three commands someone needs.

## Licence, citation and contact
Who maintains this, and how to reach them.
```

!!! success "Write both READMEs"
    `README.md` in English and `README.fr.md` in French. Your neighbours read one
    or the other, and the point of publishing is that they can reuse the work.
    The template links them at the top of each.

### The limitations statement

Carry over the statement you wrote on Day 4. It is not a disclaimer appended at
the end — it is the section that makes the rest of the repository credible.

A good limitations statement answers four questions:

1. **What does this indicator actually measure?** ("Night-time radiance is a
   proxy for lit infrastructure, not for GDP or household connection rates.")
2. **What choices did you make that a reader would not guess?** (The lit
   threshold. The boundary file. The product version. The years excluded for
   incompleteness.)
3. **What is known to be wrong or uncertain?** (Gas flares in your producing
   regions. Saturation in the capital. Two years missing a tile.)
4. **What should this not be used for?** ("This should not be used to allocate
   budget between districts without a ground-truth check.")

---

## Step 3 · Turn on GitHub Pages

Two clicks, and your work has a public URL.

1. Repository → **Settings** → **Pages**
2. **Source: GitHub Actions**
3. Push any commit. The included `pages.yml` workflow builds `docs/` and deploys it.

Your site appears at `https://<owner>.github.io/stg17-<iso3>/` within a couple of
minutes. Check the **Actions** tab if it does not.

??? failure "The site does not appear"

    | Symptom | Cause | Fix |
    |---|---|---|
    | 404 after several minutes | Pages source still set to "Deploy from a branch" | Settings → Pages → Source: **GitHub Actions** |
    | Workflow shows a red X | Usually a malformed `mkdocs.yml` | Open the failed run, read the last 20 lines of the log |
    | Site builds but is blank | `docs/index.md` missing | The template ships one; check you did not delete it |
    | Images do not load | Absolute paths like `/outputs/map.png` | Use relative paths: `../outputs/map.png` |
    | Works locally, 404 online | Case sensitivity — GitHub's servers are case-sensitive, Windows is not | Rename `Figure1.PNG` to match the link exactly |

---

## Step 4 · Licensing — the part that is easy to get wrong

Three separate things need a licence, and they are not the same licence.

### Your code → MIT

The notebooks and scripts you wrote. MIT is permissive, short, and what the
template ships. Nothing to decide.

### Your written content → CC BY 4.0

The README, the methodology, the limitations statement, the figures you produced.
Attribution required, reuse otherwise unrestricted.

### Your derived data → **it depends on your sources**

This is where careful offices still get caught.

!!! warning "Ookla is CC BY-NC-SA 4.0, and that propagates"

    The Ookla Speedtest open dataset is published under **Creative Commons
    Attribution-NonCommercial-ShareAlike 4.0**. Two of those terms travel into
    anything you derive from it:

    - **NonCommercial** — your derived indicator may not be used for commercial
      purposes. That is a real constraint for a statistical office whose open-data
      policy typically permits commercial reuse.
    - **ShareAlike** — your derived indicator must itself be licensed under
      CC BY-NC-SA 4.0. You cannot relicense it as CC BY 4.0, and you cannot place
      it in the public domain.

    **Consequence:** a population-weighted connectivity indicator built from Ookla
    tiles **cannot** be published under your office's standard open-data licence.
    It must carry CC BY-NC-SA 4.0.

    This is not a reason to avoid the source. It is a reason to state the licence
    clearly on the product, and to raise the question internally before the
    indicator becomes part of a regular publication. Several offices will conclude
    that a negotiated agreement with Ookla or with national operators is the route
    to a freely reusable indicator — which is exactly the private-sector
    partnership discussion of activity 3.1.

### The decision, as a table

| Your product derives from | You may license it as |
|---|---|
| NASA Black Marble only | CC BY 4.0, or your office's open-data licence. Black Marble is US Government work, effectively public domain |
| WorldPop only | CC BY 4.0 — WorldPop is CC BY 4.0, and BY propagates but does not restrict |
| **Ookla, alone or combined with anything else** | **CC BY-NC-SA 4.0. No other choice** |
| Your own official statistics only | Your office's own licence |
| Your official statistics + Ookla | CC BY-NC-SA 4.0 |

!!! tip "Keep the piles separate"
    If you want your NTL indicator to be freely reusable and your Ookla indicator
    is not, publish them as **two clearly separated products** with two
    `LICENSE-DATA` files, rather than one bundle that inherits the strictest terms.
    The template supports this: put them in separate folders, each with its own
    `LICENSE-DATA` and a line in the data README.

### Boundaries

Whichever boundary file you used must be cited, with its licence. If you used
geoBoundaries during the workshop and your office's official boundaries for
publication, say so — and note that the figures differ between the two, because
they will.

Neither this workshop, the African Development Bank nor AU STATAFRIC takes a
position on any boundary delimitation. Your repository represents your office.

---

## Step 5 · Metadata — being discoverable, not merely online

A repository nobody can find is not published. Two files do the work.

### `metadata.json`

The template ships a filled example. Edit the values, keep the keys.

```json
{
  "title": "Night-time lights and connectivity indicators — Côte d'Ivoire",
  "title_fr": "Lumières nocturnes et indicateurs de connectivité — Côte d'Ivoire",
  "country": { "iso3": "CIV", "name_en": "Côte d'Ivoire" },
  "producer": "Institut National de la Statistique",
  "workshop": "STG17 · AfDB / STATAFRIC · Action Plan 2025-2030",
  "temporal_coverage": { "start": "2016", "end": "2024" },
  "spatial_resolution": "ADM2",
  "sources": [
    { "name": "NASA Black Marble VNP46A4", "licence": "Public domain" },
    { "name": "Ookla Open Data", "licence": "CC BY-NC-SA 4.0" }
  ],
  "licence_code": "MIT",
  "licence_data": "CC BY-NC-SA 4.0",
  "keywords": ["night-time lights", "VIIRS", "connectivity", "SDG 7", "SDG 9"],
  "maintainer": { "name": "...", "email": "...", "role": "..." },
  "version": "1.0.0",
  "published": "2026-06-19"
}
```

### GitHub topics

Repository → About → the gear icon → Topics. Add at minimum:
`stg17`, `official-statistics`, your ISO3 code, and the data sources you used.
This is how the catalogue finds you.

---

## Step 6 · A DOI, so the work can be cited

A GitHub URL can move or disappear. A DOI cannot. It is what turns your
repository from a link into something a colleague can cite in a paper and a
reviewer can still resolve in ten years.

1. Create an account at [zenodo.org](https://zenodo.org) — free, CERN-operated
2. Zenodo → **GitHub** → find your repository → toggle it **on**
3. Back on GitHub: **Releases** → **Create a new release** → tag `v1.0.0`
4. Zenodo archives the release automatically and mints a DOI
5. Copy the DOI badge into your README, and the DOI into `CITATION.cff`

### `CITATION.cff`

GitHub reads this file and adds a **"Cite this repository"** button to your
repository page.

```yaml
cff-version: 1.2.0
title: "Night-time lights and connectivity indicators — Côte d'Ivoire"
message: "If you use this work, please cite it as below."
type: dataset
authors:
  - family-names: "..."
    given-names: "..."
    affiliation: "Institut National de la Statistique"
doi: 10.5281/zenodo.XXXXXXX
version: 1.0.0
date-released: 2026-06-19
license: CC-BY-NC-SA-4.0
keywords: [night-time lights, VIIRS, official statistics, Côte d'Ivoire]
```

!!! tip "Join the STG17 Zenodo community"
    When submitting, select the **STG17** community. All country work then appears
    in one browsable, citable collection — which is the point of activity 2.1.1.

---

## Step 7 · Versioning and maintenance

The question that decides whether this is a workshop artefact or a statistical
product: **who owns it in eighteen months?**

**Name a maintainer** in the README and in `metadata.json`. A person, with an
institutional email — not "the statistics department". If that person leaves, the
README is updated. This single line is the difference between a repository that
is still trustworthy in 2028 and one that quietly rots.

**Version with releases.** Tag `v1.0.0` for the workshop output. When you rerun
with a new year of data, tag `v1.1.0`, and let Zenodo mint a new DOI that resolves
to that exact version. Anyone who cited v1.0.0 still gets what they cited.

**Use semantic versioning, adapted to data:**

| Change | Bump |
|---|---|
| Fixed a typo, added a figure | `v1.0.1` |
| Added a year, added a region | `v1.1.0` |
| Changed the method, revised past figures | `v2.0.0` — and say so prominently |

**Record what changed.** A `CHANGELOG.md` with three lines per release is enough,
and it is what a user comparing two of your releases needs.

---

## Step 8 · Submit to the STG17 catalogue

Once your repository is public and has a DOI:

1. Send the Secretariat the repository URL, the DOI, and one paragraph on what is
   reusable
2. It is reviewed against the checklist below and added to the continental
   catalogue

Your work then feeds **activity 2.1.1** (methodological guidelines for the use of
new data sources) and becomes a candidate for the brown-bag webinar series
(activity 1.3.1).

### Submission checklist

- [ ] Repository is public and named `stg17-<iso3>`
- [ ] `README.md` and `README.fr.md` both present and complete
- [ ] Data sources table lists every input, its period and its licence
- [ ] Limitations statement present and specific to your country
- [ ] `LICENSE` and `LICENSE-DATA` present, and the data licence is *correct* for the sources used
- [ ] Notebooks run top to bottom on a fresh kernel
- [ ] No keys, no microdata, no unreleased figures — including in the git history
- [ ] GitHub Pages site live
- [ ] `metadata.json` filled, GitHub topics set
- [ ] DOI minted, `CITATION.cff` updated
- [ ] A named maintainer with an institutional email

---

## Continued support

The Secretariat's offer does not end on Friday. If you are stuck on any step
above — including "my office's legal service is unhappy about the licence" —
open an issue on the workshop repository or write to the Secretariat directly.
Several offices will hit the same question, and answering it once in public is
worth more than answering it five times in private.
