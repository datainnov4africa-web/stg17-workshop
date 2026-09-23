# When you need Kaggle — and when you do not

Short answer: **no laboratory requires it.** Every laboratory in the week runs on
a laptop or on free Colab. This page exists so that you know what Kaggle is for
here, and so that nobody creates an account they will not use.

---

## What Kaggle is, in this workshop

Kaggle is one of the places a workshop notebook can run, alongside Colab, your
own machine and a plain CI runner. The toolkit detects it automatically, and
several of the supplied notebooks read their API keys from the Kaggle secret
manager exactly as they would from Colab's — with nothing to edit.

## When it is worth creating the account

**If your machine is locked down and Colab is blocked.** Institutional networks
sometimes allow one and not the other. A second tested route to a running
notebook is the real value of Kaggle for this week — and the time to discover
which routes your network allows is the environment check, not Day 1.

**If an optional exercise ever needs a guaranteed GPU.** Kaggle's weekly quota —
two T4 GPUs or one P100, around 30 hours per week — is the most generous free
allocation available without an institutional account, and unlike Colab's free
tier it is a quota rather than a lottery.

!!! note "No laboratory in the agenda needs a GPU"

    The twelve laboratories are retrieval, prompting, dashboards, geospatial
    analysis and publication. None of them trains a model. If a facilitator adds
    an optional exercise that does, this is where to run it.

---

## Where Kaggle is the wrong tool

| Situation | Use instead |
|---|---|
| Geospatial laboratories (Days 3 and 4) | Your laptop, or the Earth Engine variants. Kaggle's geospatial stack is fine but adds nothing here. |
| Anything needing an API key you created | Colab. Kaggle Secrets works, but Colab's secret manager is what the notebooks were tested against. |
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
3. Notebook settings on the right: **Internet → On**
4. For API keys: Add-ons → Secrets → attach your key with the same name the
   notebook expects (`GROQ_API_KEY`, `GITHUB_TOKEN`, …)

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
| D2 · Document to dashboard | No |
| D2 · Provider benchmark | No |
| D2 · Toolkit stations | No |
| D3 · Ookla and WorldPop | No |
| D3 · Elasticsearch | No |
| D3 · Search-driven exploration | No |
| D4 · NTL collect and explore | No |
| D4 · NTL explore and understand | No |
| D4 · NTL analysis and validation | No |
| D5 · Publish your work | No |

Twelve laboratories, twelve times no. Create the account only if Colab is
blocked on your network.
