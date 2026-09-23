# Before the workshop

The agenda holds only if the preparation below is done. This section is short on
purpose — six pages, and the first is the only one that is mandatory reading.

<div class="stg-cards" markdown>

<div markdown>
### :material-clipboard-check: Prerequisites
The complete list, derived from the twelve laboratories. **Start here.**

[Read →](prerequisites.md)
</div>

<div markdown>
### :material-account-key: Accounts to create
Seven accounts, none paid. What each is for and how long it takes.

[Read →](accounts.md)
</div>

<div markdown>
### :material-folder-table: Your national data pack
Three files that make the week produce *your* country's indicators.

[Read →](data-pack.md)
</div>

<div markdown>
### :material-gpu: When you need Kaggle
No laboratory requires it. A spare route if Colab is blocked.

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

## What is expected of you, and when

| When | What |
|---|---|
| **T − 4 weeks** | Your office confirms who attends, and names the team that will carry the work through to Friday. |
| **T − 2 weeks** | Send your six country slides, create a GitHub account, and submit your national data pack. |
| **T − 1 week** | Join the remote environment check — one hour, offered twice in two time zones. |
| **Day 0** | Room and network test on site; collect the workshop material from the facilitation team. |

Everything else — the datasets and the machines — is prepared for you. If
something is missing on the day, there is a documented fallback for every
laboratory; say so and it is applied.

## Known risks, and how they are handled

**Bandwidth** is the most frequent cause of laboratory failure, which is why the
datasets are prepared in advance by the facilitation team rather than downloaded
during sessions, and why every published notebook also runs on Colab, where
nothing is downloaded to your own machine.

**Failed or rate-limited API keys** are handled by a facilitator-run
demonstration path for each API-dependent step, and by the notebooks themselves:
most laboratories that call a model also run without a key, through a local
Ollama model or a built-in offline mode. The Day 2 morning notebook is the
exception and does need one, Gemini or Groq. Your keys are your own, created
before you travel — see [accounts to create](accounts.md).

**Heterogeneous laptops** are absorbed by the Colab fallback, tested during the
environment check rather than discovered on Day 1.

**Uneven skill levels** are handled by the facilitation team, which circulates
throughout every laboratory, and by pairing participants across levels from Day 3
onwards.

**Incomplete national data** — a missing boundary file, an indicator available
only at national level — is handled by the fully prepared reference country, so
that no team loses a day.
