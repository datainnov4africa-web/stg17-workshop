# References and further reading

Every factual claim in the workshop material traces to a source on this page.
DOIs are given so that a claim can be checked rather than trusted, and each entry
carries a line on **why it is here** — a bibliography without that is a list, not
a reading guide.

!!! note "Verification"

    Titles, journals, volumes and DOIs on this page were checked against the
    publishers' records when the material was prepared. If you find an error,
    open an issue on the workshop repository — a wrong DOI in a workshop about
    reproducibility is worse than no DOI.

---

## Start here

If you read one paper before Day 4, read the first. If you read two, read the second.

**Levin, N., Kyba, C.C.M., Zhang, Q., Sánchez de Miguel, A., Román, M.O., Li, X., et al.** (2020).
Remote sensing of night lights: A review and an outlook for the future.
*Remote Sensing of Environment*, 237, 111443.
[doi:10.1016/j.rse.2019.111443](https://doi.org/10.1016/j.rse.2019.111443)

: The comprehensive review — sensors, products, applications, pitfalls. If a
question about night-time lights has an answer, it is probably in here.

**Gibson, J., Olivia, S., Boe-Gibson, G.** (2020).
Night Lights in Economics: Sources and Uses.
*Journal of Economic Surveys*, 34(5), 955–980.

: The sceptical companion. Read it *alongside* the enthusiastic literature, not
instead of it. It is the reason the Day 4 afternoon laboratory exists.

---

## The products

**Román, M.O., Wang, Z., Sun, Q., Kalb, V., Miller, S.D., Molthan, A., et al.** (2018).
NASA's Black Marble nighttime lights product suite.
*Remote Sensing of Environment*, 210, 113–143.
[doi:10.1016/j.rse.2018.03.017](https://doi.org/10.1016/j.rse.2018.03.017)

: The VNP46 suite — VNP46A1 to A4, at 500 m since January 2012. This is the
product the Day 4 local notebook uses. Read it before quoting a radiance figure.

**Elvidge, C.D., Zhizhin, M., Ghosh, T., Hsu, F.-C., Taneja, J.** (2021).
Annual Time Series of Global VIIRS Nighttime Lights Derived from Monthly Averages: 2012 to 2019.
*Remote Sensing*, 13(5), 922.
[doi:10.3390/rs13050922](https://doi.org/10.3390/rs13050922)

: The EOG annual VNL v2 series, and the filtering used to remove biomass burning,
aurora and background. This is the product behind the Earth Engine variant — and
the reason the two notebooks give slightly different numbers.

**Li, X., Zhou, Y., Zhao, M., Zhao, X.** (2020).
A harmonized global nighttime light dataset 1992–2018.
*Scientific Data*, 7, 168.
[doi:10.1038/s41597-020-0510-y](https://doi.org/10.1038/s41597-020-0510-y)

: If you must produce a series spanning the DMSP/VIIRS break, this is the
defensible way to do it. Cite the harmonisation explicitly — a spliced series
presented as a single record is not a reproducible statistic.

---

## What lights can and cannot measure

**Henderson, J.V., Storeygard, A., Weil, D.N.** (2012).
Measuring Economic Growth from Outer Space.
*American Economic Review*, 102(2), 994–1028.
[doi:10.1257/aer.102.2.994](https://doi.org/10.1257/aer.102.2.994)

: The foundational paper. Its finding matters for national statistical offices:
where national income accounts are weak, the best estimate of growth puts roughly
**equal weight** on measured growth and on growth predicted from lights. A
complement, not a replacement.

**Gibson, J., Olivia, S., Boe-Gibson, G., Li, C.** (2021).
Which night lights data should we use in economics, and where?
*Journal of Development Economics*, 149, 102602.
[doi:10.1016/j.jdeveco.2020.102602](https://doi.org/10.1016/j.jdeveco.2020.102602)

: Results differ materially depending on the product used, and the differences
are largest where studies of developing countries operate. This is why every
figure the workshop produces names its product and version.

**Bluhm, R., Krause, M.** (2022).
Top lights: Bright cities and their contribution to economic development.
*Journal of Development Economics*, 157, 102880.
[doi:10.1016/j.jdeveco.2022.102880](https://doi.org/10.1016/j.jdeveco.2022.102880)

: The clearest demonstration that an artefact can reverse a conclusion. Once
DMSP top-coding is corrected, primary cities in Sub-Saharan Africa grow *faster*
than secondary cities — a premium visible only in the corrected data, and
consistent with census figures.

---

## Africa

**Min, B., Gaba, K.M., Sarr, O.F., Agalassou, A.** (2013).
Detection of rural electrification in Africa using DMSP-OLS night lights imagery.
*International Journal of Remote Sensing*, 34(22), 8118–8141.
[doi:10.1080/01431161.2013.833358](https://doi.org/10.1080/01431161.2013.833358)

: Senegal and Mali, validated against ground records at settlement level. The
reference for the most defensible use of night-time lights by an African NSO:
tracking where electrification has arrived.

**Elvidge, C.D., Zhizhin, M., Baugh, K., Hsu, F.-C., Ghosh, T.** (2016).
Methods for Global Survey of Natural Gas Flaring from Visible Infrared Imaging Radiometer Suite Data.
*Energies*, 9(1), 14.
[doi:10.3390/en9010014](https://doi.org/10.3390/en9010014)

: How flares are detected — and therefore how to exclude them. Essential for any
producing country: a single flare can dominate a region's Sum of Lights while
electrifying nobody.

---

## Data access

| Resource | What it gives | Account needed |
|---|---|---|
| [NASA LAADS DAAC](https://ladsweb.modaps.eosdis.nasa.gov/) | Black Marble VNP46A1–A4, the authoritative source | Free Earthdata login + bearer token |
| [Earth Observation Group, Colorado School of Mines](https://eogdata.mines.edu/products/vnl/) | EOG annual VNL v2, and the global gas-flare survey | Free registration |
| [Google Earth Engine catalog](https://developers.google.com/earth-engine/datasets) | `NOAA/VIIRS/DNB/ANNUAL_V22`, `NOAA/VIIRS/DNB/MONTHLY_V1/VCMSLCFG`, `NASA/VIIRS/002/VNP46A2` | Free non-commercial account + Cloud project |
| [World Bank *Light Every Night*](https://registry.opendata.aws/wb-light-every-night/) | The full 1992–present archive, analysis-ready, on AWS | **None** |
| [geoBoundaries](https://www.geoboundaries.org/) | Open administrative boundaries, ADM0–ADM5, CC BY 4.0 | None |
| [WorldPop](https://hub.worldpop.org/) | Gridded population, 100 m, CC BY 4.0 | None |
| [Ookla Open Data](https://github.com/teamookla/ookla-open-data) | Quarterly fixed and mobile performance tiles | None — but **CC BY-NC-SA 4.0**, see [licensing](licensing.md) |

**Runfola, D., Anderson, A., Baier, H., Crittenden, M., Dowker, E., Fuhrig, S., et al.** (2020).
geoBoundaries: A global database of political administrative boundaries.
*PLOS ONE*, 15(4), e0231866.
[doi:10.1371/journal.pone.0231866](https://doi.org/10.1371/journal.pone.0231866)

: The boundary source used throughout the laboratories. Cite it if you publish
with it — and read the [caution about publishing with non-official boundaries](../publish/index.md#step-4-licensing-the-part-that-is-easy-to-get-wrong).

---

## Tutorials and training

**World Bank — [Open Nighttime Lights](https://worldbank.github.io/OpenNightLights/welcome.html)**

: Free, open, Jupyter-based tutorials built on Earth Engine, covering remote
sensing fundamentals through to a full analysis. The natural continuation of
Day 4 for anyone who wants more than a single day can give. Source at
[github.com/worldbank/OpenNightLights](https://github.com/worldbank/OpenNightLights).

**UN Committee of Experts on Big Data and Data Science for Official Statistics**

: The institutional home of this kind of work in the UN statistical system, and
the source of the UN Global Platform referenced in the Day 3 talk.

---

## How to cite the workshop material

If you reuse a notebook or a figure from this repository:

```
STG17 Workshop — Emerging Issues, Emerging Practice.
African Development Bank (Secretariat of STG17) and African Union STATAFRIC,
under SHaSA II, STG17 Action Plan 2025–2030. https://github.com/STG17-Africa/stg17-workshop
```

And if you publish a national product built with it, [give it its own DOI](../publish/index.md#step-6-a-doi-so-the-work-can-be-cited)
— that is what makes it citable in turn.
