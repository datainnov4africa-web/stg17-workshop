# Votre paquet de données national

Trois fichiers, attendus deux semaines avant l'atelier. Ce sont eux qui font que
la semaine produit les indicateurs de **votre pays** plutôt qu'une démonstration
sur celui d'un autre.

---

## A · Un fichier de frontières administratives

**Quoi :** ADM1 au minimum ; ADM2 également si votre office le publie.
**Format :** Shapefile (`.shp` avec ses `.dbf`, `.shx`, `.prj`) ou GeoJSON.
**Utilisé aux :** Jours 3 et 4 — dans chaque statistique zonale de la semaine.

Apportez **les frontières officielles de votre office**, pas un téléchargement
trouvé sur internet. Tout l'objet de la semaine est que vos résultats se
réconcilient avec ce que votre office publie déjà ; des frontières différentes des
vôtres garantissent qu'ils ne s'y réconcilieront pas.

Les carnets se replient sur [geoBoundaries](https://www.geoboundaries.org) si rien
n'est fourni, et cela convient pour apprendre la méthode. Cela ne convient pas
pour publier : geoBoundaries est ouvert et citable mais ne porte aucune valeur
juridique dans votre pays, et la représentation des frontières est politiquement
sensible dans plusieurs États membres.

!!! info "Ce dont le chargeur a besoin"
    Rien de normalisé. `stg17.boundaries` sonde la colonne de nom selon les
    conventions de geoBoundaries, GADM, HDX et des fichiers nationaux, répare les
    géométries invalides et reprojette en EPSG:4326. S'il ne trouve pas de colonne
    de nom, il le dit plutôt que de deviner. Envoyez le fichier tel quel.

**Liste de contrôle**

- [ ] Un polygone par unité administrative, sans trou ni recouvrement
- [ ] Une colonne portant le nom de l'unité, quelle qu'en soit la convention
- [ ] Un système de coordonnées déclaré (`.prj` présent, ou GeoJSON en WGS84)
- [ ] L'intégralité du territoire national, îles et enclaves comprises

---

## B · Une publication statistique nationale

**Quoi :** Un PDF ou un rapport contenant des tableaux — annuaire statistique,
rapport de recensement, bulletin sectoriel.
**Utilisé au :** Jour 2 matin, où un LLM extrait et structure les données, où vous
vérifiez l'extraction contre la source, et où vous publiez le résultat sous forme
de tableau de bord en ligne.

Choisissez quelque chose que **vous connaissez assez bien pour y repérer une
erreur**. L'étape de vérification est ce qui compte dans ce laboratoire : un LLM
extraira un tableau avec assurance et se trompera sur une cellule, et tout
l'intérêt pédagogique est que vous l'attrapiez. Cela ne fonctionne que sur un
document que vous pouvez contrôler à l'œil.

Bons choix : un chapitre d'annuaire comportant 5 à 20 tableaux ; un bulletin
régional ; un rapport d'enquête avec ventilations infranationales. À éviter : les
documents numérisés qui sont des images et non du texte (l'extraction devient un
exercice d'OCR, qui est un autre laboratoire), et tout ce qui est confidentiel.

!!! warning "Rien de confidentiel"
    Ce que vous apportez peut se retrouver dans un dépôt public et peut être
    envoyé à une API LLM commerciale. N'utilisez que du matériel que votre office
    a déjà publié.

---

## C · Au moins un indicateur infranational officiel

**Quoi :** PIB, population, ou taux d'électrification — par ADM1 ou ADM2,
idéalement sur plusieurs années.
**Format :** CSV ou Excel. Une ligne par unité administrative, une colonne par année.
**Utilisé au :** Jour 4 après-midi — validation de l'indicateur indirect des
lumières nocturnes.

**C'est l'élément le plus souvent oublié, et celui qui change le plus ce avec quoi
vous repartez.** Sans lui, vous pouvez calculer l'indicateur NTL, mais vous ne
pouvez pas le valider — et c'est la validation qui décide si le résultat est
publiable dans votre pays ou reste un outil de diagnostic. Cette décision, prise
preuves à l'appui, est le livrable du Jour 4.

Un exemple de la forme attendue :

| region | pcode | 2016 | 2020 | 2024 |
|---|---|---|---|---|
| Abidjan | CI01 | 62,4 | 68,1 | 74,9 |
| Yamoussoukro | CI02 | 41,7 | 46,0 | 52,3 |

Les noms de régions n'ont pas à correspondre exactement au fichier de frontières —
le laboratoire comporte une étape d'appariement, car en pratique ils ne
correspondent jamais exactement.

---

## Comment l'envoyer

Réunissez les trois éléments dans une archive nommée `<ISO3>_data_pack.zip` avec
un court `README.txt` indiquant, pour chaque fichier : ce que c'est, qui l'a
produit, à quelle année il se rapporte, et s'il est déjà public.

Envoyez-la au Secrétariat à l'adresse figurant dans votre invitation, avant
**T − 2 semaines**.

!!! tip "Si l'un des trois est impossible"
    Dites-le tôt plutôt que d'arriver sans lui. La Côte d'Ivoire est préparée de
    bout en bout comme pays de référence et la Tunisie l'est pour les laboratoires
    de connectivité. Toute équipe dont les données propres s'avèrent
    inexploitables bascule, le note dans sa déclaration de limites, et ne perd
    aucun temps — mais la bascule se passe bien mieux quand elle est prévue que
    lorsqu'elle est improvisée le jeudi matin.
