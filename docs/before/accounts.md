# Accounts to create

**None of them costs anything.** Create them in this order — the first two
unblock everything else, and Earth Engine has an approval delay you want to
start early.

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
    The Day 2, Day 3 and Day 4 notebooks publish your deliverable to GitHub from
    inside the notebook. Without `GITHUB_TOKEN` the notebook keeps your files and
    skips the publishing step: you still have the work, but not the public URL — and
    the public URL *is* the deliverable.

!!! tip "Already have a personal account?"
    Use it. There is no need for a separate one, and a single identity makes the
    Day 5 citation and DOI step simpler.

## 2 · Google — required

Used for Google Colab, the tested fallback path for every notebook in the
workshop. Most participants already have one.

Test it once before the workshop: open any day page — [Day 1](../day1/index.md),
for instance — click the Colab badge beside a notebook, and run the first cell.
If it runs, your fallback path works.

## 3 · Google Earth Engine — strongly recommended

The Day 4 afternoon notebook reads VIIRS night-time lights through Earth Engine,
and asks for your project id when it starts. Without an approved account that
notebook cannot run at all, which is why this one is worth starting early.

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
locked down and Colab is blocked on your network. No laboratory requires it, and
the notebooks read Kaggle's secret manager exactly as they read Colab's.

## 6 · An LLM provider — required, and you create it yourself

You create these accounts and obtain your own keys, before you travel. Both
providers below issue a free key from a web console in a few minutes; the
notebooks read it from a secret or an environment variable, never from a cell
you edit.

Have them **before Day 1**: the first laboratory that calls a model runs on
Day 1 at 14:30, not on Day 2.

| Provider | Used in | Key name | Create it at |
|---|---|---|---|
| **Groq** | Every LLM laboratory, Days 1 and 2 | `GROQ_API_KEY` | [console.groq.com/keys](https://console.groq.com/keys) |
| **Google Gemini** | Day 2 morning, where it is the default provider | `GEMINI_API_KEY` | [aistudio.google.com/apikey](https://aistudio.google.com/apikey) |
| **Ollama** (local) | Days 1 and 2 | *none* | Installed on your laptop — the sovereign path, no key and no data leaving the building |

Groq is the one to create first: it is the provider every LLM notebook accepts,
and the default of all but one.

!!! tip "If you already hold a key elsewhere"

    The Day 2 dashboard notebook also accepts **Mistral**, **Z.ai**,
    **Cerebras** and **OpenRouter**, and two notebooks accept any
    **OpenAI-compatible endpoint**. Change one line at the top of the notebook.
    None of these is an account you need to create for the workshop.

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

Most notebooks read keys through `stg17.env.get_secret()`, which searches Colab
secrets, then Kaggle secrets, then the environment, then `.env` — and reports a
missing key as a documented fallback rather than a crash. The rest carry their own
reader, which looks in the same places in the same order.
