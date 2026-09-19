# Dry run — T − 1 week

The rule adopted throughout this workshop is that **no laboratory may depend on a
step that has not been tested in advance on the workshop machines**. This page is
how that rule is enforced.

Run by the lead facilitator, on a machine matching the participant specification
(16 GB RAM, no administrator privileges assumed, same network as the venue if
possible). Not on a development machine — a development machine has every library
already installed, which is exactly the condition being tested.

**Time each step.** The purpose is not only to confirm that a laboratory works,
but to know how long it takes, so that a session running over can be recognised
in the first ten minutes rather than the last.

## Per laboratory

| Check | Why |
|---|---|
| Requirements cell completes from a clean environment | The most common Day 1 failure |
| Colab badge opens the right notebook | A badge pointing at a moved file is invisible until someone needs it |
| The notebook runs top to bottom with no manual intervention | If it needs a nudge, so will forty people |
| **Each documented fallback is exercised, not just read** | An untested fallback is a plan, not a fallback |
| The deliverable is actually written to disk | Teams have finished a laboratory and had nothing to commit |
| Timing recorded, per step | Feeds the facilitator brief |

## Fallbacks to exercise explicitly

Disconnect, revoke, or unplug — do not simulate.

- [ ] **D1 RAG** — start from the pre-built vector index, skipping embedding
- [ ] **D1 agent** — run the reference agent with no API key present
- [ ] **D2 dashboard** — publish from the static template alone
- [ ] **D2 benchmark** — facilitator-run path with participant keys unset
- [ ] **D3 Ookla** — pre-clipped extract, network disabled
- [ ] **D3 Elasticsearch** — DuckDB path with the cluster unreachable, same query set
- [ ] **D4 NTL** — (a) pre-prepared local extract, network disabled; (b) Earth Engine variant;
      (c) reference country substitution
- [ ] **D5 publish** — country template published with no prior repository

## Timing sheet

| Laboratory | Budgeted | Measured | Longest step | Note |
|---|---|---|---|---|
| D1 · RAG assistant | 45 min | | | |
| D1 · From RAG to agent | 75 min | | | |
| D2 · Document to dashboard | 120 min | | | |
| D2 · Provider benchmark | 45 min | | | |
| D2 · Toolkit stations | 75 min | | | |
| D3 · Ookla + WorldPop | 120 min | | | |
| D3 · Elasticsearch | 45 min | | | |
| D3 · Search exploration | 60 min | | | |
| D4 · Collect and explore | 165 min | | | |
| D4 · Analysis | 90 min | | | |
| D4 · Validation | 45 min | | | |
| D5 · Publish | 75 min | | | |

A laboratory that measures at more than 80 % of its budget on a facilitator's
machine will overrun in the room. Cut a step before the week, not during it.

## Infrastructure

- [ ] Elasticsearch cluster reachable from the venue network, one index per country
- [ ] Kibana reachable
- [ ] API keys provisioned, one per participant, quotas set and verified by a test call
- [ ] Earth Engine project approved and tested from a second Google account
- [ ] Hybrid platform tested with a remote participant, screen share and audio
- [ ] Interpretation booth has the decks as PDF

## After the dry run

Update `config/workshop.yml` with anything that changed, run
`python tools/build_all.py`, and record the measured timings in the facilitator
brief (deck 12). A dry run whose findings are not written down has to be repeated.
