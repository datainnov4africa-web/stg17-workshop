---
hide:
  - navigation
---

<div class="stg-hero" markdown>
<div class="eyebrow">African Development Bank · African Union STATAFRIC · SHaSA II</div>

# Emerging Issues, Emerging Practice

<p class="lede">Innovating the Data Value Chain — artificial intelligence, large language models
and big data for official statistics. One rule holds the week together: everything you build is
published, documented, and reusable by another African country.</p>

<div class="stg-meta" markdown>
:material-calendar-range: <b>28 September – 2 October 2026</b> &nbsp;·&nbsp;
:material-map-marker: Kigali, Rwanda &nbsp;·&nbsp;
:material-account-multiple: Hybrid &nbsp;·&nbsp;
:material-translate: English and French
</div>

<div class="stg-stats">
<div><span class="n">5</span><span class="l">days<br>27 contact hours</span></div>
<div><span class="n">13</span><span class="l">hands-on<br>laboratories</span></div>
<div><span class="n">2</span><span class="l">languages, from<br>a single source</span></div>
</div>
</div>

<div class="stg-cta" markdown>
[:material-rocket-launch: Start here — what to prepare](before/prerequisites.md){ .md-button .md-button--primary }
[:material-calendar-week: See the week](week/index.md){ .md-button }
</div>

## Start here

<div class="stg-cards" markdown>

<div markdown>
### :material-clipboard-check: Before you arrive
Accounts to create, the national data pack to assemble, and the environment check
to run. Three things are due **two weeks** before the workshop opens.

[Prerequisites →](before/prerequisites.md)
</div>

<div markdown>
### :material-calendar-week: The week
Five days, session by session, with the presentation and the notebooks attached to
each one. Generated from the agenda itself, so it cannot drift.

[Day 1 →](day1/index.md)
</div>

<div markdown>
### :material-flask: The laboratories
Thirteen hands-on laboratories, each in **English and French**, each in a
**guided** and an **open** track, each parameterised by a single country variable.

[Laboratory register →](labs/index.md)
</div>

<div markdown>
### :material-github: Publish your country's work
The step-by-step route from a notebook that runs on your laptop to a public,
citable, DOI-bearing repository your office can stand behind.

[Publication guide →](publish/index.md)
</div>

</div>

## What makes this workshop different

**Every notebook runs on your country.** One variable — `COUNTRY_ISO3` — resolves
the administrative boundaries, the satellite tiles, the projection used for areas
and every figure title. The registry covers all 55 African Union member states.
Change one line, re-run, and the pipeline you learned on Côte d'Ivoire produces
your own national indicator.

```python
COUNTRY_ISO3 = "CIV"   # ← change this, and nothing else
```

**Nothing depends on a step that has not been tested.** Every laboratory has a
documented fallback that actually works: pre-clipped country extracts on a USB
key, an Earth Engine variant that downloads nothing, a DuckDB path when the
Elasticsearch cluster is unreachable, and one reference country prepared end to
end so that no team loses a day to a missing file.

**The limitations statement is part of the deliverable.** A proxy indicator
published without an honest account of what it cannot support is not a
statistical product. Day 4 turns that statement into a formal, evidence-backed
document validated against your own official subnational figures.

## Where this comes from

The Executive Council of the thirtieth African Union Summit adopted SHaSA II in
January 2018 as the continental strategy for the development of statistics in
Africa. It is operationalised through Specialized Technical Groups, one for each
of its eighteen priority focus areas. **STG17** is the group responsible for
emerging issues — big data, open data and, increasingly, artificial intelligence.

The first Annual Meeting, convened in Kigali in September 2025 by the African
Development Bank as Secretariat of STG17 with AU STATAFRIC, identified five
obstacles holding back the systematic use of alternative data sources. This
workshop is built around them, and is a direct operational instrument of
**Work Package 4.2** of the Action Plan 2025–2030.

| Obstacle identified in Kigali | How this workshop responds |
|---|---|
| Obstacles to accessing new data sources — legal frameworks, cost, usability | Access and partnership models with private data holders (Day 3); working directly with an openly licensed source and its restrictions (Ookla, CC BY-NC-SA); licensing, DOI and citation (Day 5) |
| Absence of harmonised methodologies | Every country team runs the same documented pipeline on the same three sources; all notebooks land in one public GitHub organisation |
| Open questions on the quality of alternative sources | Coverage and selection bias in non-probabilistic sources (Day 3); validation of the NTL proxy against official subnational statistics (Day 4) |
| Weaknesses in NSO IT and big data infrastructure | AI infrastructure fundamentals, cost modelling and sovereignty trade-offs (Day 1); big data technologies and when the added complexity is warranted (Day 3) |
| Gaps in human resources, skills and data roles | The workshop itself, framed by a baseline and end-line self-assessment feeding the competencies framework |
| Need for structured exchange between offices | Country experience exchange on Day 1 and country presentations on Day 5 |

[Full topic ↔ Action Plan mapping →](resources/action-plan.md)

## Learning objectives

By the end of the workshop, participants will be able to:

- Position the core AI concepts in relation to one another — AI, LLM, prompt
  engineering, RAG, fine-tuning, agentic systems, agents and MCP — and explain
  where each fits in the statistical value chain.
- Assess the infrastructure an NSO actually needs to run AI workloads: compute,
  storage, serving, cost and sovereignty trade-offs.
- Design, engineer and optimise prompts, and select the right model and inference
  provider for a given statistical task.
- Deploy LLMs across a portfolio of professional use cases: coding, report
  writing, presentations, graphics and visual identity, document analysis.
- Acquire, process and publish non-traditional data — Ookla Speedtest, WorldPop
  and Night-Time Lights — as subnational statistical indicators.
- Build a reproducible analytical product and publish it publicly on GitHub, with
  documented methods, limitations and licensing.
- Learn from what peer countries have already achieved, and identify at least one
  collaboration or reuse opportunity for their own office.

!!! tip "Working language"

    Sessions run in English with simultaneous interpretation. **All laboratory
    material — every notebook, every presentation and this entire site — exists in
    English and French.** Use the language selector in the header, or the
    :material-web: link at the top of any notebook.
