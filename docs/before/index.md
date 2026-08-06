# Before the workshop

The agenda holds only if the preparation below is done. This section is short on
purpose — six pages, and the first is the only one that is mandatory reading.

<div class="stg-cards" markdown>

<div markdown>
### :material-clipboard-check: Prerequisites
The complete list, derived from the nine laboratories. **Start here.**

[Read →](prerequisites.md)
</div>

<div markdown>
### :material-account-key: Accounts to create
Six accounts, none paid. What each is for and how long it takes.

[Read →](accounts.md)
</div>

<div markdown>
### :material-folder-table: Your national data pack
Three files that make the week produce *your* country's indicators.

[Read →](data-pack.md)
</div>

<div markdown>
### :material-gpu: When you need Kaggle
Usually never. Two laboratories are the exception.

[Read →](kaggle.md)
</div>

<div markdown>
### :material-notebook-check: Environment check
One notebook, five minutes, a diagnostic string to send us.

[Run it →](environment-check.md)
</div>

<div markdown>
### :material-presentation: Country slides template
Six slides for the Day 1 exchange. Be candid about what did not work.

[Read →](country-slides.md)
</div>

</div>

## The preparation timeline

| When | Who | What |
|---|---|---|
| T − 6 weeks | Secretariat (AfDB) | Confirm dates, venue, hybrid platform and interpretation; issue invitations carrying the country input request and the data-pack list |
| T − 4 weeks | Country focal points | Confirm participants and nominate the country team that will carry the work through to Friday |
| T − 4 weeks | Lead facilitator | Freeze the notebook set in both guided and open versions; create the GitHub organisation and one repository per country |
| T − 3 weeks | Technical assistants | Mirror the Ookla tiles, WorldPop rasters and NTL subsets for every participating country; prepare the pre-clipped extracts and the reference country |
| **T − 2 weeks** | **Participants** | **Send the six country slides; create a GitHub account; submit the national data pack** |
| T − 2 weeks | Secretariat | Provision LLM and Groq API keys with per-participant quotas; provision and load the Elasticsearch cluster |
| T − 1 week | Technical assistants | Run the remote environment check — one hour, offered twice in two time zones |
| T − 1 week | Lead facilitator | Dry-run every laboratory end to end on a workshop-specification machine, timing each step |
| Day 0 | All | Room and network test; distribution of the USB keys carrying all data, notebooks and slides |
| T + 1 week | Secretariat | Publish recordings and notebooks; consolidate the commitments board into a dated follow-up calendar |

## Known risks, and how they are handled

**Bandwidth** is the most frequent cause of laboratory failure, which is why every
dataset is mirrored locally and distributed on USB keys rather than downloaded
during sessions — and why every geospatial laboratory has an Earth Engine variant
that downloads nothing at all.

**Failed or rate-limited API keys** are handled by per-participant quotas
provisioned in advance, and by a facilitator-run demonstration path for each
API-dependent step.

**Heterogeneous laptops** are absorbed by the Colab fallback, tested during the
environment check rather than discovered on Day 1.

**Uneven skill levels** are handled by the two-track notebooks and by pairing
participants across levels from Day 3 onwards.

**Incomplete national data** — a missing boundary file, an indicator available
only at national level — is handled by the fully prepared reference country, so
that no team loses a day.
