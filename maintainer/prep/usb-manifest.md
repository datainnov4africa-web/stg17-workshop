# USB key manifest

One key per participant, prepared at T − 1 week and distributed on Day 0.

Bandwidth is the single most common cause of laboratory failure. The key exists
so that **every laboratory can be completed with the network unplugged**. That is
a hard requirement, not an aspiration — if a laboratory cannot run from the key,
it is not ready.

**Capacity:** 64 GB minimum. A full set for ten participating countries runs to
roughly 28 GB; 128 GB gives room for the whole continent.

```
STG17_KEY/
├── README.txt                    ← what this is, in EN and FR, one page
├── START-HERE.html               ← offline copy of the site, opens in a browser
│
├── STG17_LOCAL/                  ← point STG17_ROOT at this directory
│   ├── boundaries/
│   │   ├── CIV/  ADM0.geojson  ADM1.geojson  ADM2.geojson
│   │   ├── TUN/  …
│   │   └── …                     one folder per participating country
│   ├── h5_cache/
│   │   ├── CIV/Annual/           VNP46A4, 2016 · 2020 · 2024, pre-clipped
│   │   └── …
│   ├── ookla/
│   │   ├── TUN/  2024Q1..Q4 .parquet
│   │   └── …
│   ├── worldpop/
│   │   └── <iso3>_pop_2024_100m.tif
│   └── outputs/                  ← empty; participants write here
│
├── downloads/                    ← every supplied deck and notebook, EN and FR,
│                                   copied from docs/downloads/DayN/
├── country-template/             ← so a team can start their repository offline
├── wheels/                       ← pip wheels for the whole stack, offline install
│   └── install-offline.txt       ← the one pip command to run
└── docs-offline/                 ← mkdocs build output, browsable without network
```

## Preparation checklist

- [ ] Assemble `STG17_LOCAL/` for every participating country — boundaries, NTL
      extracts, Ookla tiles, WorldPop rasters, laid out as the tree above. No
      tool in this repository does it; budget real time for it
- [ ] `python tools/build_all.py`
- [ ] Copy `docs/downloads/` to `downloads/` — the decks and notebooks work from
      the key with no network, which the Colab badges do not
- [ ] `mkdocs build` → copy `site/` to `docs-offline/`
- [ ] `pip download -r requirements-dev.txt -d wheels/` on a machine matching the
      workshop specification — wheels are platform-specific, and a Linux wheel on
      a Windows laptop is worse than no wheel
- [ ] Verify the reference country (CIV) runs end to end **from the key, with the
      network disabled**, on a clean machine
- [ ] Verify one Ookla laboratory runs from the key with the network disabled
- [ ] `README.txt` written in both languages
- [ ] Label each key physically — they get mixed up on the second day

## What must NOT go on the key

- API keys of any kind, including in a `.env` file
- Participant data packs from other countries (each office's material is theirs)
- Anything under statistical confidentiality
- Raw Ookla parquet for countries that are not participating — the licence
  permits redistribution, but the key should stay under 32 GB and unused data is
  just weight

## Verification, on the day

Before distribution, plug one key into a machine that has **never** run the
workshop material, disconnect the network, and complete the Day 4 collect-and-
explore laboratory end to end. If it works there, it works everywhere.
