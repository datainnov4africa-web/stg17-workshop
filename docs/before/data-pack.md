# Your national data pack

Three files, due two weeks before the workshop. They are what make the week
produce **your country's** indicators rather than a demonstration on someone
else's.

---

## A · An administrative boundary file

**What:** ADM1 at minimum; ADM2 as well if your office publishes it.
**Format:** Shapefile (`.shp` with its `.dbf`, `.shx`, `.prj`) or GeoJSON.
**Used in:** Days 3 and 4 — every zonal statistic in the week.

Bring **your office's official boundaries**, not a download from the internet.
The whole point of the week is that your results reconcile with what your office
already publishes; boundaries that differ from your published ones guarantee they
will not.

The notebooks fall back to [geoBoundaries](https://www.geoboundaries.org) if
nothing is supplied, and that is fine for learning the method. It is not fine for
publishing: geoBoundaries is open and citable but carries no legal weight in your
country, and boundary depiction is politically sensitive in several member
states.

!!! info "What the loader needs"
    Nothing standardised. `stg17.boundaries` probes for the name column across the
    conventions used by geoBoundaries, GADM, HDX and national files, repairs
    invalid geometries, and reprojects to EPSG:4326. If it cannot find a name
    column it says so rather than guessing. Send the file as-is.

**Checklist**

- [ ] One polygon per administrative unit, no gaps and no overlaps
- [ ] A column holding the unit name, in any spelling convention
- [ ] A coordinate reference system declared (`.prj` present, or GeoJSON in WGS84)
- [ ] The complete national territory, including islands and enclaves

---

## B · One national statistical publication

**What:** A PDF or report containing tables — a statistical yearbook, a census
report, a sector bulletin.
**Used in:** Day 2 morning, where an LLM extracts and structures its data, you
verify the extraction against the source, and you publish the result as a live
dashboard.

Choose something **you know well enough to spot an error in**. The verification
step is the part of that laboratory that matters: an LLM will extract a table
confidently and get one cell wrong, and the entire pedagogical point is that you
catch it. That only works on a document you can check by eye.

Good choices: a yearbook chapter with 5–20 tables; a regional bulletin; a survey
report with subnational breakdowns. Avoid: scanned documents that are images
rather than text (extraction becomes an OCR exercise, which is a different
laboratory), and anything confidential.

!!! warning "Nothing confidential"
    Whatever you bring may end up in a public repository and may be sent to a
    commercial LLM API. Use only material your office has already published.

---

## C · At least one official subnational indicator

**What:** GDP, population, or the electrification rate — by ADM1 or ADM2, ideally
for several years.
**Format:** CSV or Excel. One row per administrative unit, one column per year.
**Used in:** Day 4 afternoon — validating the night-time lights proxy.

**This is the item most often forgotten, and the one that most changes what you
leave with.** Without it you can compute the NTL proxy, but you cannot validate
it — and validation is what decides whether the result is publishable in your
country or remains a diagnostic tool. That decision, made with evidence, is the
Day 4 deliverable.

An example of the shape needed:

| region | pcode | 2016 | 2020 | 2024 |
|---|---|---|---|---|
| Abidjan | CI01 | 62.4 | 68.1 | 74.9 |
| Yamoussoukro | CI02 | 41.7 | 46.0 | 52.3 |

The region names do not have to match the boundary file exactly — the laboratory
includes a matching step, because they never match exactly in practice.

---

## How to send it

Package the three items in one archive named `<ISO3>_data_pack.zip` with a short
`README.txt` stating, for each file: what it is, who produced it, which year it
refers to, and whether it is already public.

Send it to the Secretariat at the address in your invitation, by **T − 2 weeks**.

!!! tip "If one of the three is impossible"
    Say so early rather than arriving without it. Côte d'Ivoire is prepared end to
    end as the reference country and Tunisia is prepared for the connectivity
    laboratories. Any team whose own data proves unusable switches, notes it in
    their limitations statement, and loses no time — but the switch works far
    better when it is planned than when it is improvised on Thursday morning.
