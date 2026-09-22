# Prerequisites

Everything on this page is derived from the thirteen laboratories that make up the
week. Nothing is here for form's sake: each item is something a laboratory will
fail without.

!!! danger "The three items due two weeks before the workshop"

    1. **Six slides** on your country's experience with AI and non-traditional data — *including what did not work*
    2. **A personal GitHub account** — laboratory outputs are published publicly from Day 2 onwards
    3. **Your national data pack** — a boundary file, a national publication, and one official subnational indicator

    Everything else can be sorted during the remote environment check at T-1 week.
    These three cannot, because other people's sessions depend on them.

---

## 1 · Your machine

| | Minimum | Recommended | If you fall short |
|---|---|---|---|
| **RAM** | 8 GB | 16 GB | Every laboratory has a Colab badge. Use it. |
| **Free disk** | 10 GB | 25 GB | Use the Earth Engine variants, which download nothing |
| **Python** | 3.9 | 3.11 | Colab ships 3.11 |
| **Rights** | ability to install packages | administrator | Colab needs no rights at all |
| **Network** | intermittent is fine | stable | The datasets are prepared in advance by the facilitation team |
| **GPU** | not needed | not needed | No laboratory needs one. [Kaggle](kaggle.md) provides a free GPU should an optional exercise ever call for it |

**On the 8 GB case.** The geospatial laboratories still work. Every heavy step
processes one satellite tile at a time rather than loading a country at once,
which was a deliberate design choice. Close your browser tabs and you will be
fine.

**On restricted laptops.** Institutional machines that forbid installing software
are common and entirely anticipated. Google Colab is the tested fallback path for
every single notebook, and the badge sits in the first cell of each one. Test it
during the environment check rather than discovering it on Day 1.

---

## 2 · Accounts

Six accounts, none of them paid. Full instructions on the
[accounts page](accounts.md).

| Account | Needed for | Time to create |
|---|---|---|
| **GitHub** | Days 2–5. All outputs are published publicly — **and a personal access token**, because the Day 2 and Day 3 notebooks publish from inside the notebook | 10 min |
| **Google** | Colab — the fallback path for every notebook | you probably have one |
| **Google Earth Engine** | the zero-download path for Days 3 and 4 | 10 min, plus approval |
| **NASA Earthdata** | downloading Black Marble granules on Day 4 | 5 min |
| **Kaggle** | Optional — a spare route to a running notebook if Colab is blocked. See [when you need Kaggle](kaggle.md) | 5 min |
| **Groq** | Days 1 and 2 — the provider every LLM laboratory accepts, from Day 1 at 14:30 | 5 min, free key |
| **Google Gemini** | Day 2 morning, where it is the default provider | 5 min, free key |

!!! warning "Earth Engine approval is not instant"

    Registration requires attaching a Google Cloud project and can take a day or
    two to be approved for non-commercial use. Start it as soon as you receive
    your invitation, not the week before.

---

## 3 · Your national data pack

Three files, described in full on the [data pack page](data-pack.md). Together
they are what make the week produce *your country's* indicators rather than a
demonstration on someone else's.

**A. An administrative boundary file** — ADM1 at minimum, ADM2 if your office
publishes it. Shapefile or GeoJSON. Your office's official boundaries, not a
download from the internet: the whole point is that your results reconcile with
what your office already publishes.

**B. One national statistical publication** — a PDF or report containing tables.
Used in the Day 2 laboratory, where an LLM extracts and structures its data and
you verify the extraction against the source. Choose something you know well
enough to spot an error in.

**C. At least one official subnational indicator** — GDP, population or
electrification rate, by ADM1 or ADM2. Used on Day 4 afternoon to validate the
night-time lights proxy against ground truth. **Without this, you can compute the
proxy but you cannot validate it**, and validation is what decides whether the
result is publishable.

!!! tip "If your national data turns out to be incomplete"

    Côte d'Ivoire is prepared end to end as the reference country, and Tunisia is
    prepared for the connectivity laboratories. Any team whose own data proves
    unusable switches to the reference country, notes it in their limitations
    statement, and loses no time. The method is what transfers; the country is a
    parameter.

---

## 4 · Skills

There is no formal prerequisite. Participants arrive with markedly different
levels, and the facilitation team works with the room throughout each
laboratory.

That said, you will get more out of the week if you are comfortable with:

- **Reading Python.** Not writing it from scratch — reading it, and changing a
  parameter. If you can look at `panel.groupby("year").sum()` and guess what it
  does, you have enough.
- **The idea of a table with rows and columns.** Every laboratory ends in one.
- **Your own office's data.** More valuable here than any technical skill. The
  laboratories supply the method; you supply the judgement about whether the
  result means anything in your country.

You do **not** need prior experience with satellite imagery, machine learning,
geospatial software or large language models. Days 1 and 4 both start from first
principles.

---

## 5 · Run the environment check

One notebook, five minutes, and it tells you item by item whether your machine
can run the thirteen laboratories — then produces a short diagnostic string to send
to the technical assistants.

[:material-notebook: Environment check →](environment-check.md){ .md-button .md-button--primary }

A remote environment check session is offered in the week before the workshop,
one hour, run twice in two time zones. Bring your diagnostic string to it.

---

## 6 · Prepare your six slides

The Day 1 morning exchange is where the week gets its material. Eight minutes,
six slides maximum, and a template is provided.

The single most useful instruction: **be candid about what did not work.** Every
office in the room has a pilot that stalled, a partnership that was never signed,
a model that was never deployed. Those are the more useful half of the exchange,
and the synthesis session is designed to pool them.

[:material-presentation: Country slides template →](country-slides.md){ .md-button }

---

## Checklist

- [ ] Laptop with 8 GB RAM minimum, ideally 16 GB and administrator rights
- [ ] GitHub account created, username sent to the Secretariat
- [ ] GitHub personal access token created and stored as `GITHUB_TOKEN`
- [ ] Google account working, Colab tested once
- [ ] Google Earth Engine registered and approved
- [ ] NASA Earthdata account and a bearer token generated
- [ ] Kaggle account (optional — only if Colab is blocked on your network)
- [ ] Administrative boundary file located and shareable
- [ ] One national statistical publication chosen
- [ ] One official subnational indicator located
- [ ] Environment check notebook run, diagnostic string sent
- [ ] Six country slides drafted, using the template
- [ ] Attended one of the two remote environment check sessions
