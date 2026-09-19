# For facilitators

One lead facilitator, two technical assistants, roughly one assistant per ten
participants. Remote participants are grouped into virtual breakout teams, each
with a dedicated assistant. A resource person supports the visual identity and
image-generation station on Day 2.

## Mixed levels

Participants arrive with markedly different levels. Nothing in the material
separates them, so the handling is entirely yours: circulate, and give the person
who is behind the next step quietly, at their table. Someone who needs help
should not have to ask for it in front of the room.

## Running a laboratory

1. **Two minutes on the objective and the deliverable.** Not on the method — the
   notebook does that better than you will from the podium.
2. **Name the fallback before anyone needs it.** "If your download stalls, use the
   Earth Engine variant, or set the country to CIV." Said in advance it is a
   design feature; said after twenty minutes of silence it is a rescue.
3. **Circulate.** The assistants handle individual breakage; the lead facilitator
   watches for the *same* problem appearing at three tables, which is a signal to
   stop the room and address it once.
4. **Ten minutes before the end, ask for the deliverable.** Teams that have not
   saved anything need those ten minutes.

## When to trigger a fallback

| Signal | Action |
|---|---|
| Three or more teams stuck on the same step for 10 minutes | Stop the room. Demonstrate from the podium. |
| A team's national data proves unusable | Switch them to the reference country immediately. Do not let them debug a data problem during a method laboratory. |
| The Elasticsearch cluster is unreachable | Announce the DuckDB path for everyone at once, not team by team. |
| API keys rate-limited | Facilitator-run demonstration path. Do not spend the session on quota administration. |
| Network down entirely | The locally prepared copies of the datasets. Every laboratory works from them. |

## The wall board

Opened during the Day 1 synthesis and kept visible all week. Four columns:

- **Recurring use cases** — what more than one country is attempting
- **Replicable partnerships** — data agreements another office could copy
- **Shared obstacles** — the material for the Action Plan
- **Where pooling would pay** — candidate joint projects

Consolidated on Friday into the key-takeaways session and, at T+1 week, into the
dated follow-up calendar circulated to the Bureau.

## Timing risks

**Day 1 morning country presentations** are the session most likely to overrun.
Appoint a timekeeper. Eight minutes each, six slides maximum, and the synthesis
slot absorbs any overflow — that is what it is for.

**Day 3 afternoon** has three sessions in three hours with a coffee break. If the
Elasticsearch indexing runs long, cut the second query set rather than the
publication slot at 16:45: teams that do not commit on Wednesday arrive at Friday
with nothing to show.

**Day 4** is a full day on one topic. Watch for fatigue after lunch; the analysis
laboratory at 14:00 is the densest hour of the week.

## Before the week

- [ ] Dry-run every laboratory end to end on a workshop-specification machine, timing each step
- [ ] Confirm the Elasticsearch cluster is loaded, one index per participating country
- [ ] Confirm the reference country runs end to end from a clean machine
- [ ] Check every Colab badge resolves
