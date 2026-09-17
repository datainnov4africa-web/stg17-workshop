# Environment check

One notebook. About five minutes. It tells you, item by item, whether your
machine can run the thirteen laboratories — and then produces a short diagnostic
string to send to the technical assistants.

The environment-check notebook is distributed with the workshop materials. Your
facilitator will send the link, or open it from the USB key.

!!! tip "Run it twice"
    Once at home, as soon as you receive your invitation, and once during the
    remote check session at T − 1 week. The first run tells you what to fix; the
    second confirms you fixed it.

## What it checks

| Section | What it establishes |
|---|---|
| **1 · Toolkit** | Whether the `stg17` package installs on your machine |
| **2 · Laboratory map** | Which laboratories need what — so you only fix what you will use |
| **3 · Your machine** | Python version, RAM, free disk, GPU presence, detected platform |
| **4 · Libraries** | Imports each library *for real* — an installed-but-broken `rasterio` reports as present in `pip list` and fails on import |
| **5 · Accounts and network** | Which API keys are visible (presence only, never the key) and which endpoints your network reaches |
| **6 · Your country** | Resolves your ISO3 code to its satellite tiles, projection and estimated download volume, then actually loads your boundaries |
| **7 · A first figure** | Confirms the plotting stack renders in the workshop identity |
| **8 · Diagnostic string** | A compact, shareable summary — no keys, no personal paths |

## Reading the result

The check is deliberately generous about what counts as a problem.

**Red in the *core libraries* group** needs fixing before Day 3. The notebook
prints the exact `pip install` line for whatever is missing.

**Amber on an API key** is not a failure. Every laboratory that uses a key also
has a documented path that works without one.

**Amber on a network endpoint** is not a failure either. Blocked endpoints are
common on institutional networks, and every dataset is mirrored on the USB key
distributed on Day 0.

**Red on the boundary load** is worth reporting. It usually means geoBoundaries
does not publish the level you asked for, which is useful to know before Thursday.

## The diagnostic string

Section 8 prints something like this:

```
STG17 ENVIRONMENT CHECK
platform   : local / Windows 11 / py3.11.9
device     : CPU only
country    : CIV (2 VIIRS tiles)
boundaries : ok - 33 ADM1 units
core missing  : rasterio, h5py
optional ok   : 9/17
network fail  : NASA Earthdata (CMR)
keys present  : GROQ_API_KEY
```

Copy it and send it to the technical assistants, or paste it into the chat during
the check session. **It contains no keys, no paths from your personal folders and
no personal data** — only what is needed to help you.

## If the notebook itself will not run

That is itself a diagnosis, and a common one. Take the Colab badge at the top of
this page: it runs the same notebook on Google's machines with nothing installed
on yours. If Colab works and your laptop does not, your fallback path for the
whole week is Colab, which is a perfectly good answer — say so at the check
session and the facilitators will pair you accordingly.
