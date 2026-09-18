# Références et pour aller plus loin

Chaque affirmation factuelle du matériel de l'atelier renvoie à une source de
cette page. Les DOI sont donnés pour qu'une affirmation puisse être vérifiée
plutôt que crue, et chaque entrée porte une ligne expliquant **pourquoi elle est
là** — une bibliographie sans cela est une liste, pas un guide de lecture.

!!! note "Vérification"

    Titres, revues, volumes et DOI de cette page ont été contrôlés auprès des
    éditeurs lors de la préparation du matériel. Si vous trouvez une erreur,
    ouvrez une issue sur le dépôt de l'atelier — un DOI faux dans un atelier
    consacré à la reproductibilité est pire que pas de DOI du tout.

---

## Commencez ici

Si vous ne lisez qu'un article avant le Jour 4, lisez le premier. Si vous en
lisez deux, lisez le second.

**Levin, N., Kyba, C.C.M., Zhang, Q., Sánchez de Miguel, A., Román, M.O., Li, X., et al.** (2020).
Remote sensing of night lights: A review and an outlook for the future.
*Remote Sensing of Environment*, 237, 111443.
[doi:10.1016/j.rse.2019.111443](https://doi.org/10.1016/j.rse.2019.111443)

: La revue de référence — capteurs, produits, applications, pièges. Si une
question sur les lumières nocturnes a une réponse, elle est probablement ici.

**Gibson, J., Olivia, S., Boe-Gibson, G.** (2020).
Night Lights in Economics: Sources and Uses.
*Journal of Economic Surveys*, 34(5), 955–980.

: Le contrepoint sceptique. À lire *avec* la littérature enthousiaste, pas à sa
place. C'est la raison d'être du laboratoire de validation du Jour 4 après-midi.

---

## Les produits

**Román, M.O., Wang, Z., Sun, Q., Kalb, V., Miller, S.D., Molthan, A., et al.** (2018).
NASA's Black Marble nighttime lights product suite.
*Remote Sensing of Environment*, 210, 113–143.
[doi:10.1016/j.rse.2018.03.017](https://doi.org/10.1016/j.rse.2018.03.017)

: La suite VNP46 — de VNP46A1 à A4, à 500 m depuis janvier 2012. C'est le produit
qu'utilise le carnet local du Jour 4. À lire avant de citer une valeur de radiance.

**Elvidge, C.D., Zhizhin, M., Ghosh, T., Hsu, F.-C., Taneja, J.** (2021).
Annual Time Series of Global VIIRS Nighttime Lights Derived from Monthly Averages: 2012 to 2019.
*Remote Sensing*, 13(5), 922.
[doi:10.3390/rs13050922](https://doi.org/10.3390/rs13050922)

: La série annuelle VNL v2 de l'EOG, et le filtrage appliqué pour retirer les feux
de biomasse, les aurores et le fond. C'est le produit derrière la variante Earth
Engine — et la raison pour laquelle les deux carnets donnent des chiffres
légèrement différents.

**Li, X., Zhou, Y., Zhao, M., Zhao, X.** (2020).
A harmonized global nighttime light dataset 1992–2018.
*Scientific Data*, 7, 168.
[doi:10.1038/s41597-020-0510-y](https://doi.org/10.1038/s41597-020-0510-y)

: S'il vous faut absolument une série franchissant la rupture DMSP/VIIRS, voici la
manière défendable de procéder. Citez l'harmonisation explicitement — une série
raccordée présentée comme un enregistrement unique n'est pas une statistique
reproductible.

---

## Ce que les lumières peuvent et ne peuvent pas mesurer

**Henderson, J.V., Storeygard, A., Weil, D.N.** (2012).
Measuring Economic Growth from Outer Space.
*American Economic Review*, 102(2), 994–1028.
[doi:10.1257/aer.102.2.994](https://doi.org/10.1257/aer.102.2.994)

: L'article fondateur. Son résultat compte pour les offices nationaux de
statistique : là où les comptes nationaux sont fragiles, la meilleure estimation
de la croissance accorde un poids **à peu près égal** à la croissance mesurée et à
celle prédite par les lumières. Un complément, pas un remplacement.

**Gibson, J., Olivia, S., Boe-Gibson, G., Li, C.** (2021).
Which night lights data should we use in economics, and where?
*Journal of Development Economics*, 149, 102602.
[doi:10.1016/j.jdeveco.2020.102602](https://doi.org/10.1016/j.jdeveco.2020.102602)

: Les résultats diffèrent sensiblement selon le produit utilisé, et les écarts sont
les plus grands là où travaillent les études sur les pays en développement. C'est
pourquoi chaque figure produite par l'atelier nomme son produit et sa version.

**Bluhm, R., Krause, M.** (2022).
Top lights: Bright cities and their contribution to economic development.
*Journal of Development Economics*, 157, 102880.
[doi:10.1016/j.jdeveco.2022.102880](https://doi.org/10.1016/j.jdeveco.2022.102880)

: La démonstration la plus nette qu'un artefact peut inverser une conclusion. Une
fois le plafonnement DMSP corrigé, les villes primaires d'Afrique subsaharienne
croissent *plus vite* que les villes secondaires — une prime visible seulement dans
les données corrigées, et cohérente avec les recensements.

---

## Afrique

**Min, B., Gaba, K.M., Sarr, O.F., Agalassou, A.** (2013).
Detection of rural electrification in Africa using DMSP-OLS night lights imagery.
*International Journal of Remote Sensing*, 34(22), 8118–8141.
[doi:10.1080/01431161.2013.833358](https://doi.org/10.1080/01431161.2013.833358)

: Sénégal et Mali, validés contre des relevés de terrain à l'échelle des localités.
La référence pour l'usage le plus défendable des lumières nocturnes par un INS
africain : suivre où l'électrification est arrivée.

**Elvidge, C.D., Zhizhin, M., Baugh, K., Hsu, F.-C., Ghosh, T.** (2016).
Methods for Global Survey of Natural Gas Flaring from Visible Infrared Imaging Radiometer Suite Data.
*Energies*, 9(1), 14.
[doi:10.3390/en9010014](https://doi.org/10.3390/en9010014)

: Comment les torchères sont détectées — donc comment les exclure. Indispensable
pour tout pays producteur : une seule torchère peut dominer la Somme des lumières
d'une région sans électrifier personne.

---

## Accès aux données

| Ressource | Ce qu'elle donne | Compte requis |
|---|---|---|
| [NASA LAADS DAAC](https://ladsweb.modaps.eosdis.nasa.gov/) | Black Marble VNP46A1-A4, la source faisant autorité | Compte Earthdata gratuit + jeton porteur |
| [Earth Observation Group, Colorado School of Mines](https://eogdata.mines.edu/products/vnl/) | VNL annuel EOG v2, et le relevé mondial des torchères | Inscription gratuite |
| [Catalogue Google Earth Engine](https://developers.google.com/earth-engine/datasets) | `NOAA/VIIRS/DNB/ANNUAL_V22`, `NOAA/VIIRS/DNB/MONTHLY_V1/VCMSLCFG`, `NASA/VIIRS/002/VNP46A2` | Compte non commercial gratuit + projet Cloud |
| [*Light Every Night* de la Banque mondiale](https://registry.opendata.aws/wb-light-every-night/) | L'archive complète depuis 1992, prête à l'analyse, sur AWS | **Aucun** |
| [geoBoundaries](https://www.geoboundaries.org/) | Frontières administratives ouvertes, ADM0-ADM5, CC BY 4.0 | Aucun |
| [WorldPop](https://hub.worldpop.org/) | Population maillée, 100 m, CC BY 4.0 | Aucun |
| [Ookla Open Data](https://github.com/teamookla/ookla-open-data) | Tuiles de performance trimestrielles, fixe et mobile | Aucun — mais **CC BY-NC-SA 4.0**, voir [licences](licensing.md) |

**Runfola, D., Anderson, A., Baier, H., Crittenden, M., Dowker, E., Fuhrig, S., et al.** (2020).
geoBoundaries: A global database of political administrative boundaries.
*PLOS ONE*, 15(4), e0231866.
[doi:10.1371/journal.pone.0231866](https://doi.org/10.1371/journal.pone.0231866)

: La source de frontières utilisée dans tous les laboratoires. À citer si vous
publiez avec elle — et lisez la [mise en garde sur la publication avec des
frontières non officielles](../publish/index.md#etape-4-licences-la-partie-facile-a-rater).

---

## Tutoriels et formation

**Banque mondiale — [Open Nighttime Lights](https://worldbank.github.io/OpenNightLights/welcome.html)**

: Tutoriels libres, ouverts, sous Jupyter et fondés sur Earth Engine, couvrant les
fondamentaux de la télédétection jusqu'à une analyse complète. La suite naturelle
du Jour 4 pour qui veut aller au-delà d'une seule journée. Sources sur
[github.com/worldbank/OpenNightLights](https://github.com/worldbank/OpenNightLights).

**Comité d'experts des Nations unies sur les mégadonnées et la science des données pour la statistique officielle**

: Le foyer institutionnel de ce type de travaux dans le système statistique des
Nations unies, et l'origine de la Plateforme mondiale citée dans l'exposé du Jour 3.

---

## Comment citer le matériel de l'atelier

Si vous réutilisez un carnet ou une figure de ce dépôt :

```
STG17 Workshop — Emerging Issues, Emerging Practice.
African Development Bank (Secretariat of STG17) and African Union STATAFRIC,
under SHaSA II, STG17 Action Plan 2025–2030. https://github.com/datainnov4africa-web/stg17-workshop
```

Et si vous publiez un produit national construit avec, [dotez-le de son propre
DOI](../publish/index.md#etape-6-un-doi-pour-que-le-travail-puisse-etre-cite) —
c'est ce qui le rend citable à son tour.
