# Accounts to create

Six accounts. **None of them costs anything.** Create them in this order — the
first two unblock everything else, and Earth Engine has an approval delay you
want to start early.

## 1 · GitHub — required

Everything you build from Day 2 onwards is published publicly. Without an account
you can follow the laboratories but you cannot produce the deliverable.

1. [github.com/signup](https://github.com/signup)
2. Choose a username you are willing to have attached to your office's published
   work — it will appear in the commit history of your country repository.
3. Send the username to the Secretariat so you can be added to the workshop
   organisation before Day 2.
4. Create a **personal access token**: Settings → Developer settings → Personal
   access tokens → *Fine-grained tokens* → Generate new token. Grant it
   **Contents: Read and write** on your own repositories, and store it as
   `GITHUB_TOKEN` — see [where to put your keys](#where-to-put-your-keys).

!!! info "Why a token, and not just the account"
    The Day 2 and Day 3 notebooks publish your deliverable to GitHub from inside
    the notebook. Without `GITHUB_TOKEN` the notebook keeps your files and skips
    the publishing step: you still have the work, but not the public URL — and
    the public URL *is* the deliverable.

!!! tip "Already have a personal account?"
    Use it. There is no need for a separate one, and a single identity makes the
    Day 5 citation and DOI step simpler.

## 2 · Google — required

Used for Google Colab, the tested fallback path for every notebook in the
workshop. Most participants already have one.

Test it once before the workshop: open any notebook from the
[laboratory register](../labs/index.md), click the Colab badge, and run the first
cell. If it runs, your fallback path works.

## 3 · Google Earth Engine — strongly recommended

The zero-download path for Days 3 and 4. On a constrained network this is not a
convenience — it is the difference between finishing the laboratory and not.

1. [code.earthengine.google.com/register](https://code.earthengine.google.com/register)
2. Choose **non-commercial / research** use.
3. Attach a Google Cloud project — the registration flow creates one if you have none.
4. Wait for approval.

!!! warning "Start this early"
    Approval can take a day or two. Every year a handful of participants discover
    on Day 4 morning that their registration is still pending.

Note the project id — it goes into the `GEE_PROJECT` variable of the Earth Engine
notebooks.

## 4 · NASA Earthdata — required for the Day 4 local path

Searching NASA's catalogue is public and needs nothing. **Downloading** granules
needs a free account and a bearer token.

1. [urs.earthdata.nasa.gov](https://urs.earthdata.nasa.gov) → Register
2. Log in, then profile → **Generate Token**
3. Copy the token. It is long. Store it as `EARTHDATA_TOKEN` — see below.

!!! danger "A download without a token does not fail loudly"
    Without a valid token, NASA returns an HTML login page. A naive script saves
    it under a `.h5` filename and the next step reads garbage. The workshop
    downloader checks the file size and deletes anything suspiciously small — but
    if you write your own, remember this.

## 5 · Kaggle — optional

A second tested route to a running notebook, worth having if your machine is
locked down and Colab is blocked on your network. No laboratory requires it.
[Full guidance →](kaggle.md)

## 6 · An LLM provider — provisioned for you

The Secretariat provisions per-participant keys with quotas, distributed at
registration on Day 1. You do not need to create these accounts or pay anything.

| Provider | Used in | Why this one |
|---|---|---|
| **Groq** | Day 2 benchmark | Named in the agenda; its inference speed is the point of the session |
| **Anthropic** | Days 1–2 | Long context, used for the document-extraction laboratory |
| **An OpenAI-compatible endpoint** | Days 1–2 | The comparison baseline |
| **Ollama** (local) | Day 1 | The sovereign path — no key, no data leaving the building |

---

## Where to put your keys

**Never paste a key into a notebook cell.** A key pasted into a notebook you later
push to GitHub is a key you have published, and revoking it is the least of the
consequences.

=== "Google Colab"

    Click the :material-key: key icon in the left sidebar → **Add new secret**.
    Name it exactly as the notebook expects (`GROQ_API_KEY`, `EARTHDATA_TOKEN`, …)
    and enable **Notebook access**.

=== "Kaggle"

    Add-ons → Secrets → Attach a secret, using the same name.

=== "Your own machine"

    Create a file called `.env` next to the notebooks:

    ```
    GROQ_API_KEY=gsk_...
    EARTHDATA_TOKEN=eyJ0eXAi...
    GITHUB_TOKEN=github_pat_...
    ```

    The repository `.gitignore` already excludes `.env`, so it cannot be committed
    by accident.

All notebooks read keys through `stg17.env.get_secret()`, which searches Colab
secrets, then Kaggle secrets, then the environment, then `.env` — and reports a
missing key as a documented fallback rather than a crash.
