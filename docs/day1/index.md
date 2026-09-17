<!-- GENERATED from config/agenda.yml by tools/build_site.py. Do not edit. -->

# Day 1 — AI concepts and the infrastructure behind them

*Monday · Shared vocabulary, country experience, and what it really takes to build and run AI*

## Morning · 09:00 – 12:30

### 09:00–09:30 &nbsp;·&nbsp; Opening ceremony

:material-account-group: **Ceremony** &nbsp;·&nbsp; Action Plan 4.2 · 4.1.1

Welcome and opening remarks by the African Development Bank, AU STATAFRIC, and NISR. Objectives of the week, presentation of the STG17 Action Plan 2025–2030 and of where this workshop sits within it. Tour de table.


### 09:30–10:00 &nbsp;·&nbsp; The UN Big Data Regional Hub in Rwanda: milestones and use cases

:material-presentation: **Talk** &nbsp;·&nbsp; *NISR*

Ten years of the UN Committee of Experts on Big Data and Data Science for Official Statistics, and what the Regional Hub hosted by NISR has delivered since its launch: the use cases taken furthest


### 10:00–10:30 &nbsp;·&nbsp; The AI Family Tree: How the concepts fit together

:material-presentation: **Talk** &nbsp;·&nbsp; Action Plan 3.3.2 · 4.1.1

Building a shared concept map — AI, LLM, prompt engineering, RAG, fine-tuning, agentic systems, agents, MCP. What each concept can and cannot do for official statistics, and the vocabulary discipline that avoids costly misunderstandings. This half-hour sets the language used for the rest of the week.

[:material-file-pdf-box: PDF · EN](../downloads/Day1/1000_ai-family-tree_EN.pdf){ .md-button } [:material-file-pdf-box: PDF · FR](../downloads/Day1/1000_ai-family-tree_FR.pdf){ .md-button } [:material-microsoft-powerpoint: PPTX · EN](../downloads/Day1/1000_ai-family-tree_EN.pptx){ .md-button } [:material-microsoft-powerpoint: PPTX · FR](../downloads/Day1/1000_ai-family-tree_FR.pptx){ .md-button }


!!! quote "10:30–10:45 — Coffee break"

### 10:45–11:45 &nbsp;·&nbsp; Country experiences in AI and the use of non-traditional big data

:material-forum: **Plenary** &nbsp;·&nbsp; Action Plan 3.3.2 · 3.1.2 · 2.1.1

Short country presentations on what has actually been attempted at home — pilots launched, data partnerships signed, obstacles met, results published. Countries are invited to be candid about what did not work; that is the more useful half of the exchange.


### 11:45–12:30 &nbsp;·&nbsp; Synthesis: where the continent stands

:material-lightbulb-on: **Facilitated** &nbsp;·&nbsp; Action Plan 3.1.2 · 4.1.1

Facilitated discussion structured around four questions drawn from the presentations — which use cases recur, which data partnerships are replicable, which obstacles are shared, and where pooling effort would pay.


!!! quote "12:30–14:00 — Lunch"

## Afternoon · 14:00 – 17:00

### 14:00–14:30 &nbsp;·&nbsp; AI Infrastructure: What it really takes to run AI in a Statistical Office

:material-presentation: **Talk** &nbsp;·&nbsp; Action Plan 4.2.3 · 3.3.2

Fundamentals and needs — GPUs and accelerators, memory and context, inference versus training, latency and throughput. Cloud, hybrid or on-premise; data sovereignty and confidentiality constraints for NSO microdata; cost modelling per use case; open-weight versus proprietary models.


### 14:30–15:30 &nbsp;·&nbsp; Hands-on part 1 — Retrieval-Augmented Generation

:material-flask: **Laboratory** &nbsp;·&nbsp; Action Plan 4.2.1 · 2.1.1

Build a working RAG assistant over a statistical corpus — chunking, embeddings, vector store, retrieval, grounded answering. Test it against questions with known answers and observe where retrieval fails, and why.

[:material-file-pdf-box: PDF · EN](../downloads/Day1/1430_hands-on-part-1_EN.pdf){ .md-button } [:material-file-pdf-box: PDF · FR](../downloads/Day1/1430_hands-on-part-1_FR.pdf){ .md-button } [:material-microsoft-powerpoint: PPTX · EN](../downloads/Day1/1430_hands-on-part-1_EN.pptx){ .md-button } [:material-microsoft-powerpoint: PPTX · FR](../downloads/Day1/1430_hands-on-part-1_FR.pptx){ .md-button } [:material-notebook-outline: IPYNB · EN](../downloads/Day1/1430_hands-on-part-1_EN.ipynb){ .md-button } [:material-notebook-outline: IPYNB · FR](../downloads/Day1/1430_hands-on-part-1_FR.ipynb){ .md-button }

!!! example "Laboratory — RAG assistant"

    **Deliverable:** A transcript of answers with the exact passages behind each one, and a retrieval evaluation separating retrieval failures from generation failures

    **Fallback:** A fictional five-document corpus ships with the toolkit, so no team is blocked by uncleared publications; without any model provider, the retrieval half of the laboratory still runs — and that is where most RAG problems are

    [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/STG17-Africa/stg17-workshop/blob/main/docs/downloads/Day1/1430_hands-on-part-1_EN.ipynb) **EN** &nbsp; [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/STG17-Africa/stg17-workshop/blob/main/docs/downloads/Day1/1430_hands-on-part-1_FR.ipynb) **FR**


### 15:30–16:45 &nbsp;·&nbsp; Hands-on part 2 — From RAG to Agent

:material-flask: **Laboratory** &nbsp;·&nbsp; Action Plan 4.2.1 · 4.2.3

Turn the retriever built before the break into a tool, and wrap it in an agent — tools and function calling, planning and iteration, memory, error handling and human-in-the-loop checkpoints. The agent answers a question, retrieves the supporting figures and drafts a short note; participants then examine exactly where it must stay supervised.

!!! example "Laboratory — From RAG to agent"

    **Deliverable:** An audit log recording every tool the model asked for, whether policy allowed it, and the raw reply behind each request — plus the note the agent wrote once a policy permitted it

    **Fallback:** A scripted model replays fixed replies, so the loop, the approval gate, the error recovery and the audit log are all exercised with no API key. That is deliberate rather than a consolation path — those four things are what an office writes and owns; the model is what it rents


!!! quote "16:45–17:00 — Coffee break"

