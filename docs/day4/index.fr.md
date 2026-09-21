<!-- GÉNÉRÉ depuis config/agenda.yml par tools/build_site.py. Ne pas modifier. -->

# Jour 4 — L'Afrique après la nuit tombée : lire le développement dans les lumières nocturnes

*Jeudi · Une journée entière sur les NTL — de la radiance brute à un indicateur infranational validé*

## Matinée · 09h00 – 12h30

### 09h00–09h30 &nbsp;·&nbsp; Lumières nocturnes : ce que l'obscurité nous dit

:material-presentation: **Exposé** &nbsp;·&nbsp; Plan d’action 2.1.1

Concepts et utilité, délibérément brefs pour que la journée se passe dans les données — de DMSP-OLS (1992-2013) à VIIRS/DNB ; les produits NASA Black Marble (VNP46A2 journalier, A3 mensuel, A4 annuel) et la série VNL annuelle de l'EOG ; unités de radiance, résolution et disponibilité temporelle ; ce que les NTL approchent bien — activité économique, électrification, urbanisation, suivi de crise. Les artefacts connus ne sont ici que nommés ; on les rencontre concrètement en partie 2.

[:material-file-pdf-box: PDF · EN](../downloads/Day4/0900_night-time-lights_EN.pdf){ .md-button } [:material-file-pdf-box: PDF · FR](../downloads/Day4/0900_night-time-lights_FR.pdf){ .md-button } [:material-microsoft-powerpoint: PPTX · EN](../downloads/Day4/0900_night-time-lights_EN.pptx){ .md-button } [:material-microsoft-powerpoint: PPTX · FR](../downloads/Day4/0900_night-time-lights_FR.pptx){ .md-button }


### 09h30–10h30 &nbsp;·&nbsp; Atelier partie 1 — Collecter

:material-flask: **Laboratoire** &nbsp;·&nbsp; Plan d’action 4.2.1

Accéder aux rasters NTL (NASA Earthdata, EOG ou Google Earth Engine) ; comprendre la structure des fichiers, les bandes et les indicateurs de qualité ; découper à l'emprise nationale et enregistrer un sous-ensemble de travail.

[:material-notebook-outline: IPYNB · EN](../downloads/Day4/0930_hands-on-part-1_EN.ipynb){ .md-button } [:material-notebook-outline: IPYNB · FR](../downloads/Day4/0930_hands-on-part-1_FR.ipynb){ .md-button }

[![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/datainnov4africa-web/stg17-workshop/blob/main/docs/downloads/Day4/0930_hands-on-part-1_EN.ipynb) **EN** &nbsp; [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/datainnov4africa-web/stg17-workshop/blob/main/docs/downloads/Day4/0930_hands-on-part-1_FR.ipynb) **FR**

!!! example "Laboratoire — NTL collecter et explorer"

    **Livrable :** Un sous-ensemble raster national documenté et un inventaire des artefacts présents dans ce pays

    **Repli :** Des sous-ensembles nationaux pré-découpés sont préparés pour chaque pays participant ; la variante Earth Engine ne télécharge rien


!!! quote "10h30–10h45 — Pause café"

### 10h45–12h30 &nbsp;·&nbsp; Atelier partie 2 — Explorer et comprendre

:material-flask: **Laboratoire** &nbsp;·&nbsp; Plan d’action 4.2.1 · 2.1.1

Visualiser et interroger le raster avant de calculer dessus — distribution des valeurs de radiance, effet des masques de nuages et de qualité, variation d'un mois à l'autre. Les équipes traquent délibérément les artefacts nommés dans l'exposé du matin (halo lumineux autour des villes, saturation, torchères, saisonnalité, discontinuité de capteur, bruit de faible luminosité rural) et documentent lesquels sont présents dans leur propre pays. Se termine par un tour de comparaisons entre équipes.

[:material-notebook-outline: IPYNB · EN](../downloads/Day4/1045_hands-on-part-2_EN.ipynb){ .md-button } [:material-notebook-outline: IPYNB · FR](../downloads/Day4/1045_hands-on-part-2_FR.ipynb){ .md-button }

[![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/datainnov4africa-web/stg17-workshop/blob/main/docs/downloads/Day4/1045_hands-on-part-2_EN.ipynb) **EN** &nbsp; [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/datainnov4africa-web/stg17-workshop/blob/main/docs/downloads/Day4/1045_hands-on-part-2_FR.ipynb) **FR**

!!! example "Laboratoire — NTL explorer et comprendre"

    **Livrable :** L'inventaire des artefacts de votre pays, avec les preuves

    **Repli :** Le pays de référence (Côte d'Ivoire) est préparé de bout en bout


!!! quote "12h30–14h00 — Déjeuner"

## Après-midi · 14h00 – 17h00

### 14h00–16h45 &nbsp;·&nbsp; Atelier partie 3 — Analyse et validation NTL

:material-flask: **Laboratoire** &nbsp;·&nbsp; Plan d’action 4.2.1 · 2.1.1 · 4.3 · 3.1.1

Calculer les statistiques zonales par niveau administratif (somme de radiance, radiance moyenne, superficie éclairée) ; construire des séries temporelles annuelles et mensuelles ; détecter le changement entre deux périodes ; cartographier et visualiser les résultats. Valider ensuite l'indicateur indirect NTL en le corrélant avec des statistiques infranationales officielles (population, taux d'électrification) et décider, preuves à l'appui, s'il est utilisable pour la diffusion dans votre pays ou s'il reste un simple outil de diagnostic. Documenter explicitement les limites ; cette déclaration fait partie du livrable. Les cartes, graphiques et la déclaration de limites qui en résultent peuvent être publiés en site public via GitHub Pages.

[:material-microsoft-powerpoint: PPTX · EN · Earth Engine](../downloads/Day4/1400_hands-on-part-3_EN-Earth-Engine.pptx){ .md-button } [:material-microsoft-powerpoint: PPTX · FR · Earth Engine](../downloads/Day4/1400_hands-on-part-3_FR-Earth-Engine.pptx){ .md-button } [:material-notebook-outline: IPYNB · EN](../downloads/Day4/1400_hands-on-part-3_EN.ipynb){ .md-button } [:material-notebook-outline: IPYNB · FR](../downloads/Day4/1400_hands-on-part-3_FR.ipynb){ .md-button }

[![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/datainnov4africa-web/stg17-workshop/blob/main/docs/downloads/Day4/1400_hands-on-part-3_EN.ipynb) **EN** &nbsp; [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/datainnov4africa-web/stg17-workshop/blob/main/docs/downloads/Day4/1400_hands-on-part-3_FR.ipynb) **FR**

!!! example "Laboratoire — NTL analyse et validation"

    **Livrable :** Tableau de statistiques zonales, séries temporelles, détection de changement entre deux périodes et les cartes ; corrélation avec l'indicateur officiel, et une déclaration écrite des limites

    **Repli :** Un pays de référence est préparé de bout en bout et remis à toute équipe dont les données nationales s'avèrent incomplètes, avec un indicateur officiel de référence fourni pour ce pays


!!! quote "16h45–17h00 — Pause café"

