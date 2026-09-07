# STG17 Technical Workshop — Activity Report
## Preparation of training materials and workshop documentation

**Period:** 6 August – 1 September 2026
**Event:** STG17 Technical Workshop, *Emerging Issues, Emerging Practice* — Kigali, 28 September – 2 October 2026
**Framework:** SHaSA II · STG17 Action Plan 2025–2030, Work Package 4.2 (feeding WP 1, 2, 3 and 4)
**Organisers:** African Development Bank (Secretariat of STG17) with AU STATAFRIC

---

## 1. Summary

A complete production system for the workshop's training materials was designed, built and
populated. The system generates every deliverable — presentations, notebooks, website and
official documents — from a single agenda file, in English and French, so that the two
language versions and the different output formats cannot drift apart.

Four of the ten presentations, four of the thirteen laboratories, and the full institutional
document set are complete. The remaining materials are produced by the same pipeline.

| Deliverable | Status |
|---|---|
| Bilingual production pipeline (EN / FR) | Complete and in service |
| Presentations written | 4 of 10 |
| Laboratories complete and runnable | 4 of 13 |
| Hands-on notebooks published | 18 |
| Workshop website (bilingual) | 57 pages, building without error |
| Institutional documents | 7 files delivered |
| Automated quality checks | 10, running on every change |

---

## 2. Training materials produced

### 2.1 Presentations

Four presentations were written, each in English and French from a single bilingual source,
complete with speaker notes and verified references:

| # | Title | Duration | Slides |
|---|---|---|---|
| 01 | The AI Family Tree — How the Concepts Fit Together | 30 min | 17 |
| 02 | AI Infrastructure — What It Really Takes | 45 min | 20 |
| 03 | Talking to Machines — The Craft of Prompt Engineering | 75 min | 17 |
| 08 | Night-Time Lights — What the Darkness Tells Us | 30 min | 21 |

Each is published in three forms: a browser presentation with speaker notes, a print-ready
PDF, and a PowerPoint export.

**Evidence base.** Every statistic and citation was verified against its source before use,
rather than reproduced from memory. The reference set includes the peer-reviewed night-time
lights literature (Roman 2018; Elvidge 2021; Gibson 2021; Bluhm and Krause 2022, among
others), the prompt-engineering evidence (Sclar et al., ICLR 2024; Zheng et al., EMNLP 2024),
the African Union Data Policy Framework (2022), and the UNECE HLG-MOS frameworks on machine
learning and cloud computing for official statistics.

### 2.2 Hands-on laboratories

Four laboratories are complete and have been executed end to end. Each exists in four
notebook versions — English and French, guided and open — giving **18 published notebooks**
including the environment check.

| Laboratory | Day | Subject |
|---|---|---|
| RAG assistant | 1 | Retrieval-augmented generation over an office's own publications |
| From RAG to agent | 1 | Tool use, the human approval gate, and the audit log |
| Night-time lights — collect | 4 | Acquisition, mosaicking and quality artefacts |
| Night-time lights — explore | 4 | Zonal statistics and subnational indicators |

**Design principles applied throughout:**

- **Every country is supported.** Notebooks are driven by a single country parameter; the
  registry supplies boundaries, satellite tiles and map projection for all 55 African Union
  member states.
- **Every laboratory has a tested fallback.** The core teaching steps of the Day 1
  laboratories run with no API key at all, so a provisioning failure cannot stop a session.
- **Two tracks.** A guided version with the analytical steps written out, and an open version
  with only the objective and the data. The deliverable is identical either way.
- **Colab-ready.** Every notebook opens directly in Google Colab from a badge, and is also
  distributed offline.

---

## 3. Technical infrastructure

### 3.1 The bilingual production pipeline

The central design decision: **nothing bilingual is written twice.**

| Source | Generates |
|---|---|
| One notebook master | 4 notebooks (EN / FR, guided / open) |
| One presentation source | 2 web decks and 2 PowerPoint files |
| The agenda file | 16 website pages, the concept note, the laboratory register |

An automated check fails the build if any generated file drifts from its source.

### 3.2 Reusable software library

A Python library of **12 modules (approximately 4,500 lines)** was written to carry the
technical work of the week, so that participants and country teams use the same tested code
rather than re-implementing it:

- **Country registry** — all 55 AU member states, with satellite tiles, projections and
  boundaries computed rather than tabulated
- **Night-time lights** — acquisition, mosaicking, zonal statistics, and a catalogue of the
  seven measurement artefacts
- **Earth Engine equivalent** — a zero-download path for participants with limited bandwidth
- **Multi-provider LLM client** — one interface over four providers, so that no laboratory
  depends on a single vendor
- **RAG and agent modules** — the machinery behind the two Day 1 laboratories
- **Visual identity, bilingual glossary, environment detection**

### 3.3 Workshop website

A bilingual website of **57 pages**, English at the root and French under `/fr/`, covering the
agenda, the laboratories, the presentations, the preparation requirements, the publication
guide and the reference resources. It builds without warnings under strict validation.

A **country publication template** was also produced, so that each participating office can
publish its own results as a public website with the correct licence, metadata and citation
file.

### 3.4 Quality assurance

**Ten automated checks** run on every change. They verify that notebooks match their sources,
that no credentials are present in any published file, that Colab links resolve, that the
website pages match the agenda, that the presentations build, and that the RAG and agent
modules still work — the last of these including a specific test that a refused action leaves
the system unchanged.

Additional editorial guards were added after review: a **density limit** that fails the build
when a slide carries too much text, and a **visual weight check** that rejects a slide
consisting only of text on a plain background.

---

## 4. Institutional documents

Seven documents were produced and delivered:

| Document | Language | Notes |
|---|---|---|
| Workshop concept note and agenda | EN | Regenerated from the agenda file; corrects three points at which the previous version had diverged from the material |
| Invitation letter to the AfDB | FR / EN | Adds a recommended participant profile |
| Invitation letter to national statistical institutes | FR / EN | New; covers the designation of participants and the preparation expected of them |
| Baseline and end-line assessment | EN / FR | Participant workbook, one sheet per language |
| Assessment answer key | EN | Facilitators only, issued as a separate file |

**On the concept note.** The earlier version announced nine laboratories where the agenda now
carries thirteen, specified laboratory environments that were superseded once the notebooks
were built, and described the materials as bilingual only "where available". The regenerated
version reports the actual state of the material, with every figure counted at generation time
so that it cannot become a stale claim.

**On the assessment instrument.** It measures both self-assessed capability (10 statements)
and knowledge (12 questions), because self-rated confidence often *falls* between a baseline
and an end-line as participants learn what they did not know. Reporting only the first would
misrepresent the workshop as a failure. The same instrument is used before and after, so that
the two measurements are comparable, and every answer is constrained by a dropdown so that
returned files tabulate without cleaning. This feeds STG17 Action Plan activity 4.1.1.

---

## 5. Support tools for the facilitation team

- **A prompt library (10 prompts)** enabling a session owner who is not a designer to produce
  presentation material that meets the same standard as the hand-authored decks, including an
  adversarial reviewer that hunts invented citations before they reach an audience.
- **Ready-to-use prompts** for producing the PowerPoint versions of each presentation.
- **Document generators** for the concept note, the invitation letters and the assessment,
  each reading from the agenda file so that a change to the agenda propagates to every
  document.

---

## 6. Status and remaining work

**Delivered:** the production pipeline, the software library, the website, the quality-control
system, the full institutional document set, four presentations and four laboratories.

**Remaining:** six presentations (Days 2, 3 and 5) and nine laboratories. These are produced by
the same pipeline and follow the same standards; the design and validation work is complete.

**Version control.** Twenty-three documented changes are recorded, each stating what was
changed and why, providing a full audit trail of the preparation.
