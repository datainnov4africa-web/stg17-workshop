# Publier les travaux de votre pays

Vendredi matin, votre équipe dispose de trois choses : un tableau de bord, un jeu
d'indicateurs de connectivité, et une analyse des lumières nocturnes accompagnée
d'une déclaration de limites. Cette page est le parcours qui mène de ces fichiers
à un **produit public, documenté et citable** que votre office peut assumer — et
qu'un autre pays africain peut réutiliser.

Comptez **45 minutes** pour le premier dépôt. Les suivants en demandent dix.

!!! abstract "Ce que vous aurez à l'arrivée"

    - Un dépôt GitHub public nommé `stg17-<iso3>`, avec un README en anglais et en français
    - Un site en ligne à `https://<votre-org>.github.io/stg17-<iso3>/`
    - Une licence *correcte* — y compris les parties héritées d'Ookla
    - Des métadonnées lisibles par machine, pour être trouvable et pas seulement en ligne
    - Un DOI et une citation, pour pouvoir être référencé dans une publication
    - Un mainteneur nommé, pour que tout cela soit encore vrai dans deux ans

---

## Étape 0 · Décidez ce que vous publiez, et ce que vous ne publiez pas

Avant de toucher à GitHub, répartissez la production de la semaine en trois tas.

| Tas | Exemples | Que faire |
|---|---|---|
| **Publier** | Notebooks, indicateurs agrégés, cartes, méthodologie, déclaration de limites | Tout ce qui suit s'applique |
| **Publier avec précaution** | Produits dérivés de sources à licence restrictive ; frontières dont la représentation est politiquement sensible | Lisez d'abord [l'étape 4 sur les licences](#etape-4-licences-la-partie-facile-a-rater) |
| **Ne pas publier** | Microdonnées, tout ce qui relève du secret statistique, chiffres officiels non diffusés, clés API | À garder entièrement hors du dépôt — voir l'avertissement ci-dessous |

!!! danger "Git se souvient de tout"

    Supprimer un fichier dans un commit ultérieur ne le retire **pas** du dépôt.
    Il reste dans l'historique, et n'importe qui peut le récupérer. Si vous
    versionnez par accident des microdonnées ou une clé API :

    1. **Révoquez la clé immédiatement.** La rotation est le seul vrai remède.
    2. Prévenez le Secrétariat. Réécrire l'historique d'un dépôt publié est
       possible mais perturbant, et mieux vaut le faire une fois, correctement.

    Le `.gitignore` du gabarit pays exclut déjà `.env`, les `*.csv` dans
    `data/raw/`, et les pièges habituels. Ne l'affaiblissez pas sans réfléchir à la
    raison d'être de chaque ligne.

---

## Étape 1 · Partez du gabarit pays

Ne construisez pas la structure à la main. Le gabarit porte les conventions dont
le Secrétariat a besoin pour agréger les travaux entre pays — et il porte le
workflow GitHub Actions qui publie votre site.

1. Prenez le gabarit pays fourni avec le matériel de l'atelier — l'équipe
   d'animation vous en enverra le lien
2. Créez un nouveau dépôt sur GitHub et copiez-y les fichiers du gabarit
3. Propriétaire : l'organisation GitHub de votre office si elle existe, sinon votre compte
4. Nom : **`stg17-<iso3>`** en minuscules — `stg17-civ`, `stg17-tun`, `stg17-ken`
5. Visibilité : **Public**

!!! question "Pourquoi cette convention de nommage ?"
    C'est elle qui rend le catalogue STG17 interrogeable. Une seule recherche
    GitHub sur `stg17-` renvoie les travaux de tous les pays, et les scripts
    d'agrégation du Secrétariat en dépendent. Un dépôt nommé `mon-projet-ntl` est
    invisible pour les deux.

### Ce que contient le gabarit

```
stg17-<iso3>/
├── README.md              ← la porte d'entrée, en anglais
├── README.fr.md           ← et en français
├── LICENSE                ← licence du code (MIT)
├── LICENSE-DATA           ← licence des données — lisez l'étape 4 avant de choisir
├── CITATION.cff           ← comment vous citer
├── metadata.json          ← description lisible par machine
├── notebooks/             ← vos travaux, exactement tels que vous les avez exécutés
├── data/
│   ├── raw/               ← exclu de git : les sources, non redistribuées
│   ├── processed/         ← petits produits dérivés, ceux-là publiés
│   └── README.md          ← d'où vient chaque intrant, et sous quelle licence
├── outputs/
│   ├── figures/
│   ├── tables/
│   └── maps/
├── docs/                  ← le site GitHub Pages
│   └── index.md
└── .github/workflows/
    └── pages.yml          ← construit et publie docs/ à chaque poussée
```

---

## Étape 2 · Déposez vos travaux, et rédigez le README

### Les notebooks

Copiez-les **exactement tels que vous les avez exécutés**, sorties comprises.
C'est le seul endroit où versionner les sorties d'un notebook est justifié : un
lecteur qui ne peut pas exécuter votre chaîne doit tout de même pouvoir voir ce
qu'elle a produit.

Avant de versionner, vérifiez trois choses :

- [ ] Aucune clé API dans une cellule — cherchez `sk-`, `gsk_`, `Bearer`
- [ ] Le `COUNTRY_ISO3` en tête est bien le vôtre
- [ ] Le notebook s'exécute de haut en bas sur un noyau neuf

### Le README

C'est le seul document que la plupart des visiteurs liront. Le gabarit vous donne
le squelette ; remplissez chaque section honnêtement.

```markdown
# Lumières nocturnes et indicateurs de connectivité — <Pays>

Un paragraphe : ce que contient ce dépôt, qui l'a produit, et à quelle
question il répond.

## Résultats
Deux ou trois figures, avec une phrase chacune. Montrez la réponse avant la méthode.

## Sources de données
| Source | Produit | Période | Licence | Récupéré le |
|---|---|---|---|---|
| NASA Black Marble | VNP46A4 | 2016-2024 | Domaine public | 2026-06-12 |
| Ookla Open Data | Fixe, trimestriel | T1-T4 2024 | CC BY-NC-SA 4.0 | 2026-06-12 |
| <Votre office> | Frontières ADM1 | 2024 | <votre licence> | — |

## Méthode
Brève. Renvoyez au notebook pour le détail.

## Limites
**Non optionnel.** Voir ci-dessous.

## Comment reproduire
Les trois commandes nécessaires.

## Licence, citation et contact
Qui maintient ce dépôt, et comment le joindre.
```

!!! success "Rédigez les deux README"
    `README.md` en anglais et `README.fr.md` en français. Vos voisins lisent l'un
    ou l'autre, et l'objet même de la publication est qu'ils puissent réutiliser
    le travail. Le gabarit les relie l'un à l'autre en tête de page.

### La déclaration de limites

Reprenez celle rédigée au Jour 4. Ce n'est pas un avertissement ajouté à la fin —
c'est la section qui rend le reste du dépôt crédible.

Une bonne déclaration de limites répond à quatre questions :

1. **Que mesure réellement cet indicateur ?** (« La radiance nocturne est un
   indicateur indirect des infrastructures éclairées, pas du PIB ni du taux de
   raccordement des ménages. »)
2. **Quels choix avez-vous faits qu'un lecteur ne devinerait pas ?** (Le seuil
   d'éclairement. Le fichier de frontières. La version du produit. Les années
   exclues pour incomplétude.)
3. **Qu'est-ce qui est connu comme faux ou incertain ?** (Les torchères dans vos
   régions productrices. La saturation dans la capitale. Deux années auxquelles il
   manque une tuile.)
4. **À quoi cela ne doit-il pas servir ?** (« Ceci ne doit pas servir à répartir un
   budget entre districts sans vérification de terrain. »)

---

## Étape 3 · Activez GitHub Pages

Deux clics, et vos travaux ont une URL publique.

1. Dépôt → **Settings** → **Pages**
2. **Source : GitHub Actions**
3. Poussez n'importe quel commit. Le workflow `pages.yml` inclus construit `docs/`
   et le déploie.

Votre site apparaît à `https://<propriétaire>.github.io/stg17-<iso3>/` en quelques
minutes. Consultez l'onglet **Actions** si ce n'est pas le cas.

??? failure "Le site n'apparaît pas"

    | Symptôme | Cause | Correctif |
    |---|---|---|
    | 404 après plusieurs minutes | Source Pages encore réglée sur « Deploy from a branch » | Settings → Pages → Source : **GitHub Actions** |
    | Le workflow affiche une croix rouge | En général un `mkdocs.yml` mal formé | Ouvrez l'exécution en échec, lisez les 20 dernières lignes du journal |
    | Le site se construit mais est vide | `docs/index.md` manquant | Le gabarit en fournit un ; vérifiez que vous ne l'avez pas supprimé |
    | Les images ne s'affichent pas | Chemins absolus du type `/outputs/carte.png` | Utilisez des chemins relatifs : `../outputs/carte.png` |
    | Fonctionne en local, 404 en ligne | Sensibilité à la casse — les serveurs GitHub y sont sensibles, Windows non | Renommez `Figure1.PNG` pour correspondre exactement au lien |

---

## Étape 4 · Licences — la partie facile à rater

Trois choses distinctes ont besoin d'une licence, et ce n'est pas la même.

### Votre code → MIT

Les notebooks et scripts que vous avez écrits. MIT est permissive, courte, et c'est
ce que fournit le gabarit. Rien à décider.

### Vos contenus rédigés → CC BY 4.0

Le README, la méthodologie, la déclaration de limites, les figures que vous avez
produites. Attribution requise, réutilisation par ailleurs libre.

### Vos données dérivées → **cela dépend de vos sources**

C'est ici que des offices prudents se font encore prendre.

!!! warning "Ookla est en CC BY-NC-SA 4.0, et cela se propage"

    Le jeu de données ouvert Ookla Speedtest est publié sous **Creative Commons
    Attribution - Pas d'utilisation commerciale - Partage dans les mêmes conditions
    4.0**. Deux de ces termes se transmettent à tout ce que vous en dérivez :

    - **Pas d'utilisation commerciale** — votre indicateur dérivé ne peut pas être
      utilisé à des fins commerciales. C'est une contrainte réelle pour un office
      statistique dont la politique de données ouvertes autorise généralement la
      réutilisation commerciale.
    - **Partage dans les mêmes conditions** — votre indicateur dérivé doit
      lui-même être placé sous CC BY-NC-SA 4.0. Vous ne pouvez pas le relicencier
      en CC BY 4.0, ni le verser au domaine public.

    **Conséquence :** un indicateur de connectivité pondéré par la population,
    construit à partir des tuiles Ookla, **ne peut pas** être publié sous la
    licence de données ouvertes standard de votre office. Il doit porter la
    CC BY-NC-SA 4.0.

    Ce n'est pas une raison d'écarter la source. C'est une raison d'indiquer
    clairement la licence sur le produit, et de poser la question en interne avant
    que l'indicateur n'intègre une publication régulière. Plusieurs offices
    concluront qu'un accord négocié avec Ookla ou avec les opérateurs nationaux est
    la voie vers un indicateur librement réutilisable — ce qui est exactement la
    discussion sur les partenariats avec le secteur privé de l'activité 3.1.

### La décision, sous forme de tableau

| Votre produit dérive de | Vous pouvez le licencier en |
|---|---|
| NASA Black Marble seulement | CC BY 4.0, ou la licence ouverte de votre office. Black Marble est une œuvre du gouvernement américain, de fait dans le domaine public |
| WorldPop seulement | CC BY 4.0 — WorldPop est en CC BY 4.0, et le BY se propage sans restreindre |
| **Ookla, seul ou combiné à quoi que ce soit** | **CC BY-NC-SA 4.0. Aucun autre choix** |
| Vos propres statistiques officielles seulement | La licence propre à votre office |
| Vos statistiques officielles + Ookla | CC BY-NC-SA 4.0 |

!!! tip "Gardez les tas séparés"
    Si vous voulez que votre indicateur NTL soit librement réutilisable et que
    votre indicateur Ookla ne l'est pas, publiez-les comme **deux produits
    clairement séparés** avec deux fichiers `LICENSE-DATA`, plutôt qu'un ensemble
    unique qui hériterait des conditions les plus strictes. Le gabarit le permet :
    placez-les dans des dossiers distincts, chacun avec son `LICENSE-DATA` et une
    ligne dans le README des données.

### Les frontières

Quel que soit le fichier de frontières utilisé, il doit être cité, avec sa
licence. Si vous avez utilisé geoBoundaries durant l'atelier et les frontières
officielles de votre office pour la publication, dites-le — et notez que les
chiffres diffèrent entre les deux, car ce sera le cas.

Ni cet atelier, ni la Banque africaine de développement, ni l'UA STATAFRIC ne
prennent position sur une quelconque délimitation frontalière. Votre dépôt engage
votre office.

---

## Étape 5 · Métadonnées — être trouvable, pas seulement en ligne

Un dépôt que personne ne peut trouver n'est pas publié. Deux fichiers font le
travail.

### `metadata.json`

Le gabarit en fournit un exemple rempli. Modifiez les valeurs, conservez les clés.

```json
{
  "title": "Night-time lights and connectivity indicators — Côte d'Ivoire",
  "title_fr": "Lumières nocturnes et indicateurs de connectivité — Côte d'Ivoire",
  "country": { "iso3": "CIV", "name_en": "Côte d'Ivoire" },
  "producer": "Institut National de la Statistique",
  "workshop": "STG17 · AfDB / STATAFRIC · Action Plan 2025-2030",
  "temporal_coverage": { "start": "2016", "end": "2024" },
  "spatial_resolution": "ADM2",
  "sources": [
    { "name": "NASA Black Marble VNP46A4", "licence": "Public domain" },
    { "name": "Ookla Open Data", "licence": "CC BY-NC-SA 4.0" }
  ],
  "licence_code": "MIT",
  "licence_data": "CC BY-NC-SA 4.0",
  "keywords": ["night-time lights", "VIIRS", "connectivity", "SDG 7", "SDG 9"],
  "maintainer": { "name": "...", "email": "...", "role": "..." },
  "version": "1.0.0",
  "published": "2026-06-19"
}
```

### Sujets GitHub

Dépôt → About → l'icône d'engrenage → Topics. Ajoutez au minimum :
`stg17`, `official-statistics`, votre code ISO3, et les sources de données
utilisées. C'est ainsi que le catalogue vous trouve.

---

## Étape 6 · Un DOI, pour que le travail puisse être cité

Une URL GitHub peut changer ou disparaître. Un DOI, non. C'est ce qui transforme
votre dépôt d'un lien en quelque chose qu'un collègue peut citer dans un article
et qu'un relecteur pourra encore résoudre dans dix ans.

1. Créez un compte sur [zenodo.org](https://zenodo.org) — gratuit, opéré par le CERN
2. Zenodo → **GitHub** → trouvez votre dépôt → activez-le
3. De retour sur GitHub : **Releases** → **Create a new release** → étiquette `v1.0.0`
4. Zenodo archive la version automatiquement et attribue un DOI
5. Copiez le badge DOI dans votre README, et le DOI dans `CITATION.cff`

### `CITATION.cff`

GitHub lit ce fichier et ajoute un bouton **« Cite this repository »** sur la page
de votre dépôt.

```yaml
cff-version: 1.2.0
title: "Lumières nocturnes et indicateurs de connectivité — Côte d'Ivoire"
message: "Si vous utilisez ces travaux, merci de les citer comme suit."
type: dataset
authors:
  - family-names: "..."
    given-names: "..."
    affiliation: "Institut National de la Statistique"
doi: 10.5281/zenodo.XXXXXXX
version: 1.0.0
date-released: 2026-06-19
license: CC-BY-NC-SA-4.0
keywords: [night-time lights, VIIRS, statistique officielle, Côte d'Ivoire]
```

!!! tip "Rejoignez la communauté Zenodo STG17"
    Lors de la soumission, sélectionnez la communauté **STG17**. Les travaux de
    tous les pays apparaissent alors dans une collection unique, parcourable et
    citable — ce qui est l'objet de l'activité 2.1.1.

---

## Étape 7 · Versionnement et maintenance

La question qui décide si tout ceci est un artefact d'atelier ou un produit
statistique : **qui en est responsable dans dix-huit mois ?**

**Nommez un mainteneur** dans le README et dans `metadata.json`. Une personne,
avec une adresse institutionnelle — pas « le département des statistiques ». Si
cette personne part, le README est mis à jour. Cette seule ligne fait la
différence entre un dépôt encore fiable en 2028 et un dépôt qui pourrit
discrètement.

**Versionnez avec des releases.** Étiquetez `v1.0.0` pour la production de
l'atelier. Lorsque vous ré-exécutez avec une année de données supplémentaire,
étiquetez `v1.1.0`, et laissez Zenodo attribuer un nouveau DOI pointant vers cette
version exacte. Quiconque a cité la v1.0.0 obtient toujours ce qu'il a cité.

**Utilisez un versionnement sémantique, adapté aux données :**

| Changement | Incrément |
|---|---|
| Correction d'une coquille, ajout d'une figure | `v1.0.1` |
| Ajout d'une année, ajout d'une région | `v1.1.0` |
| Changement de méthode, révision des chiffres passés | `v2.0.0` — et dites-le en évidence |

**Consignez ce qui a changé.** Un `CHANGELOG.md` avec trois lignes par version
suffit, et c'est ce dont a besoin un utilisateur qui compare deux de vos versions.

---

## Étape 8 · Soumettez au catalogue STG17

Une fois votre dépôt public et doté d'un DOI :

1. Transmettez au Secrétariat l'URL du dépôt, le DOI, et un paragraphe sur ce qui
   est réutilisable
2. Il est examiné au regard de la liste ci-dessous et ajouté au catalogue
   continental

Vos travaux alimentent alors l'**activité 2.1.1** (lignes directrices
méthodologiques pour l'usage des nouvelles sources de données) et deviennent
candidats à la série de webinaires « brown bag » (activité 1.3.1).

### Liste de contrôle de soumission

- [ ] Le dépôt est public et nommé `stg17-<iso3>`
- [ ] `README.md` et `README.fr.md` tous deux présents et complets
- [ ] Le tableau des sources liste chaque intrant, sa période et sa licence
- [ ] Déclaration de limites présente et propre à votre pays
- [ ] `LICENSE` et `LICENSE-DATA` présents, et la licence des données est *correcte* au regard des sources utilisées
- [ ] Les notebooks s'exécutent de haut en bas sur un noyau neuf
- [ ] Aucune clé, aucune microdonnée, aucun chiffre non diffusé — y compris dans l'historique git
- [ ] Site GitHub Pages en ligne
- [ ] `metadata.json` rempli, sujets GitHub renseignés
- [ ] DOI attribué, `CITATION.cff` mis à jour
- [ ] Un mainteneur nommé avec une adresse institutionnelle

---

## Appui continu

L'offre du Secrétariat ne s'arrête pas le vendredi. Si vous bloquez sur l'une des
étapes ci-dessus — y compris « le service juridique de mon office n'est pas à
l'aise avec la licence » — ouvrez une issue sur le dépôt de l'atelier ou écrivez
directement au Secrétariat. Plusieurs offices se heurteront à la même question, et
y répondre une fois en public vaut mieux que d'y répondre cinq fois en privé.
