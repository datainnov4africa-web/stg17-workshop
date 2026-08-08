<!-- GENERATED from config/agenda.yml by tools/build_site.py. Do not edit. -->

# Day 1 — AI concepts and the infrastructure behind them

*Monday · Shared vocabulary, country experience, and what it really takes to build and run AI*

## Morning · 09:00 – 12:30

### 09:00–09:45 &nbsp;·&nbsp; Opening ceremony

:material-account-group: **Ceremony** &nbsp;·&nbsp; Action Plan 4.2 · 4.1.1

Welcome and opening remarks by the African Development Bank and AU STATAFRIC. Objectives of the week, presentation of the STG17 Action Plan 2025–2030 and of where this workshop sits within it. Tour de table.


### 09:45–10:15 &nbsp;·&nbsp; The AI Family Tree: How the Concepts Fit Together

:material-presentation: **Talk** &nbsp;·&nbsp; Action Plan 3.3.2 · 4.1.1

Building a shared concept map — AI, LLM, prompt engineering, RAG, fine-tuning, agentic systems, agents, MCP. What each concept can and cannot do for official statistics, and the vocabulary discipline that avoids costly misunderstandings. This half-hour sets the language used for the rest of the week.

[:material-presentation: Slides](../slides/index.md#deck-01)


### 10:30–11:45 &nbsp;·&nbsp; Country experiences in AI and the use of non-traditional big data

:material-forum: **Plenary** &nbsp;·&nbsp; Action Plan 3.3.2 · 3.1.2 · 2.1.1

Short country presentations (8 minutes each, no more than 6 slides) on what has actually been attempted at home — pilots launched, data partnerships signed, obstacles met, results published. Countries are invited to be candid about what did not work; that is the more useful half of the exchange.


### 11:45–12:30 &nbsp;·&nbsp; Synthesis: where the continent stands

:material-lightbulb-on: **Facilitated** &nbsp;·&nbsp; Action Plan 3.1.2 · 4.1.1

Facilitated discussion structured around four questions drawn from the presentations — which use cases recur, which data partnerships are replicable, which obstacles are shared, and where pooling effort would pay. Outputs are recorded on a wall board kept open all week. Closes with the baseline skills self-assessment.


!!! quote "10:15–10:30 — Coffee break"

## Afternoon · 14:00 – 17:00

### 14:00–14:45 &nbsp;·&nbsp; AI Infrastructure: What It Really Takes to Run AI in a Statistical Office

:material-presentation: **Talk** &nbsp;·&nbsp; Action Plan 4.2.3 · 3.3.2

Fundamentals and needs — GPUs and accelerators, memory and context, inference versus training, latency and throughput. Cloud, hybrid or on-premise; data sovereignty and confidentiality constraints for NSO microdata; cost modelling per use case; open-weight versus proprietary models. What a realistic entry-level configuration looks like for an African NSO, with indicative orders of magnitude.

[:material-presentation: Slides](../slides/index.md#deck-02)


### 14:45–15:30 &nbsp;·&nbsp; Hands-on part 1 — Retrieval-Augmented Generation

:material-flask: **Laboratory** &nbsp;·&nbsp; Action Plan 4.2.1 · 2.1.1

Build a working RAG assistant over a statistical corpus (STG17 Concept Note, Action Plan, SHaSA II, national methodological documents) — chunking, embeddings, vector store, retrieval, grounded answering. Test it against questions with known answers and observe where retrieval fails, and why.

!!! example "Laboratory — RAG assistant"

    **Deliverable:** A transcript of answers with the exact passages behind each one, and a retrieval evaluation separating retrieval failures from generation failures

    **Fallback:** A fictional five-document corpus ships with the toolkit, so no team is blocked by uncleared publications; without any model provider, the retrieval half of the laboratory still runs — and that is where most RAG problems are

    **Status:** :material-check-circle:{ .ok } Available

    [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/STG17-Africa/stg17-workshop/blob/main/notebooks/day1/D1_RAG_Assistant_EN.ipynb) **guided** &nbsp; [:material-github:](https://github.com/STG17-Africa/stg17-workshop/blob/main/notebooks/day1/D1_RAG_Assistant_EN.ipynb)
    
    [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/STG17-Africa/stg17-workshop/blob/main/notebooks/day1/D1_RAG_Assistant_EN_open.ipynb) **open** &nbsp; [:material-github:](https://github.com/STG17-Africa/stg17-workshop/blob/main/notebooks/day1/D1_RAG_Assistant_EN_open.ipynb)


### 15:45–17:00 &nbsp;·&nbsp; Hands-on part 2 — From RAG to Agent

:material-flask: **Laboratory** &nbsp;·&nbsp; Action Plan 4.2.1 · 4.2.3

Turn the retriever built before the break into a tool, and wrap it in an agent — tools and function calling, planning and iteration, memory, error handling and human-in-the-loop checkpoints. The agent answers a question, retrieves the supporting figures and drafts a short note; participants then examine exactly where it must stay supervised.

!!! example "Laboratory — From RAG to agent"

    **Deliverable:** An agent that answers a question, retrieves the supporting figure and drafts a five-line note

    **Fallback:** A working reference agent is provided; teams modify it rather than build from scratch

    **Status:** :material-progress-clock: Day 1 batch


!!! quote "15:30–15:45 — Coffee break"

