# When you need Kaggle — and when you do not

Short answer: **most participants never need it.** Most of the laboratories
run perfectly well on a laptop or on free Colab. This page exists so that the two
that benefit from Kaggle are not a surprise on the day, and so that nobody
creates an account they will not use.

---

## The three cases where Kaggle earns its place

### 1 · The Day 1 fine-tuning demonstration

The Day 1 afternoon material includes a LoRA fine-tuning demonstration — changing
a model's weights so it always answers in a house style, rather than being asked
to in the prompt. It is the one moment in the week where a GPU changes the
experience rather than merely the speed.

| Environment | What the demo feels like |
|---|---|
| Laptop CPU | works, roughly 15–25 minutes for the training loop |
| Colab free tier | works, but GPU allocation is not guaranteed and sessions are cut |
| **Kaggle** | **two T4 GPUs or one P100, ~30 hours per week, guaranteed for the session** |

Kaggle's weekly GPU quota is the most generous free allocation available without
an institutional account, and — unlike Colab's free tier — it is a quota rather
than a lottery. If you want to run the fine-tuning yourself rather than watch the
facilitator, this is where to do it.

### 2 · Running an open-weight model locally, for the sovereignty discussion

Day 1 afternoon asks a real question: what does it actually cost an NSO to run
its own model instead of sending microdata to a commercial API? The honest way to
answer is to run one. A 7-billion-parameter open-weight model needs roughly 16 GB
of GPU memory in half precision, which no participant laptop will have and which
Kaggle provides for free.

The result is not a benchmark to publish. It is the number you need in order to
have an informed conversation with your IT department about what an on-premise
option would involve.

### 3 · As a data mirror, when the USB key is not with you

Kaggle Datasets host the pre-clipped country extracts for the geospatial
laboratories. That matters for two groups:

- **Remote participants**, who do not receive the USB key distributed on Day 0
- **Anyone continuing the work after the workshop**, when the key is in a drawer

A Kaggle dataset attached to a notebook is available instantly, with no download
to the participant's machine, and survives a runtime restart — which the `/content`
folder in Colab does not.

!!! note "The mirrors are published under the workshop organisation"

    Dataset slugs follow the pattern `stg17/ookla-<iso3>` and `stg17/ntl-<iso3>`.
    They are announced at the environment check session once the technical
    assistants have finished mirroring, at T-3 weeks.

---

## Where Kaggle is the wrong tool

| Situation | Use instead |
|---|---|
| Geospatial laboratories (Days 3 and 4) | Your laptop, or the Earth Engine variants. Kaggle's geospatial stack is fine but adds nothing here. |
| Anything needing an API key you were given | Colab. Kaggle Secrets works, but Colab's secret manager is what the notebooks were tested against. |
| Publishing your results | GitHub Pages. A Kaggle notebook is not a citable public product; Day 5 covers what is. |
| Long unattended runs | Kaggle sessions stop after 12 hours (9 with GPU). Nothing in this workshop runs that long. |

---

## Creating the account

1. Go to [kaggle.com](https://www.kaggle.com) and sign up — email or Google account.
2. **Verify your phone number.** This is the step people miss: GPU access and
   internet access from notebooks are both locked until the account is verified,
   and the verification is not obvious in the interface. Settings → Phone
   Verification.
3. Optional: Settings → Account → Create New API Token, if you want to push
   datasets or notebooks from your machine.

Total: about five minutes, plus however long the SMS takes.

---

## Running a workshop notebook on Kaggle

Every notebook in this repository detects Kaggle automatically. `stg17.env.setup()`
finds the platform, resolves `/kaggle/working/STG17_LOCAL` as the data root, and
reads secrets from the Kaggle secret manager instead of Colab's. Nothing in the
notebook needs editing.

```python
from stg17 import setup
S = setup(REQUIREMENTS, lang="EN")
print(S.platform)     # -> 'kaggle'
print(S.root)         # -> /kaggle/working/STG17_LOCAL
```

To upload one:

1. Kaggle → Create → New Notebook → File → Import Notebook
2. Upload the `.ipynb`, or paste the GitHub URL
3. Notebook settings on the right: **Accelerator → GPU T4 x2**, **Internet → On**
4. For API keys: Add-ons → Secrets → attach your key with the same name the
   notebook expects (`GROQ_API_KEY`, `ANTHROPIC_API_KEY`, …)

!!! warning "Internet is off by default on Kaggle"

    A fresh Kaggle notebook has no network access, and `pip install` fails with a
    confusing timeout rather than a clear message. Turn Internet on in the
    notebook settings panel before running the requirements cell. This catches
    almost everyone once.

---

## Summary

| Laboratory | Kaggle needed? |
|---|---|
| D1 · RAG assistant | No |
| D1 · From RAG to agent | No |
| D1 · Fine-tuning demonstration | **Recommended** — free guaranteed GPU |
| D1 · Open-weight model, sovereignty costing | **Recommended** — needs ~16 GB GPU memory |
| D2 · Document to dashboard | No |
| D2 · Provider benchmark | No |
| D2 · Toolkit stations | No |
| D3 · Ookla and WorldPop | No — but Kaggle Datasets mirror the extracts |
| D3 · Elasticsearch | No |
| D4 · NTL collect and explore | No — but Kaggle Datasets mirror the extracts |
| D4 · NTL analysis and validation | No |
| D5 · Publish your work | No |
