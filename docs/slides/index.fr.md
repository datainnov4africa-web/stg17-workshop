# Présentations

Douze présentations portent la semaine. Chacune existe en **anglais et en
français**, construite depuis une source bilingue unique afin que les deux ne
puissent pas diverger.

Chaque présentation est disponible sous trois formes :

- **:material-presentation-play: Présenter** — le deck reveal.js, dans le
  navigateur. Flèches pour naviguer, `S` pour les notes de l'orateur, `F` pour le
  plein écran, `O` pour la vue d'ensemble.
- **:material-file-pdf-box: PDF** — ajoutez `?print-pdf` à l'URL du deck et
  imprimez depuis le navigateur. Utile pour la cabine d'interprétation et pour les
  participants qui souhaitent annoter.
- **:material-microsoft-powerpoint: PPTX** — un dérivé modifiable pour les
  animateurs. Voir la note en bas de page.

---

## Jour 1 · Concepts de l'IA et infrastructure

### Deck 01 { #deck-01 }
**L'arbre généalogique de l'IA : comment les concepts s'articulent** — 30 min

Construction d'une carte conceptuelle commune : IA, LLM, ingénierie de prompt,
RAG, affinage, systèmes agentiques, agents, MCP. Cette demi-heure fixe le
vocabulaire de toute la semaine.

:material-progress-clock: *Lot Jour 1*

### Deck 02 { #deck-02 }
**Infrastructure de l'IA : ce qu'exige réellement son exploitation dans un office statistique** — 45 min

GPU et accélérateurs, inférence contre entraînement, nuage/hybride/sur site,
souveraineté des microdonnées d'un INS, modélisation des coûts, modèles à poids
ouverts contre propriétaires. À quoi ressemble une configuration d'entrée de gamme
réaliste pour un INS africain.

:material-progress-clock: *Lot Jour 1*

---

## Jour 2 · Ingénierie de prompt et usage optimisé des LLM

### Deck 03 { #deck-03 }
**Parler aux machines : l'art de l'ingénierie de prompt** — 75 min

:material-progress-clock: *Lot Jour 2*

### Deck 04 { #deck-04 }
**De bon à excellent : optimisation des prompts** — 45 min

:material-progress-clock: *Lot Jour 2*

### Deck 05 { #deck-05 }
**Choisir son moteur : vitesse, coût et souveraineté — travailler avec Groq** — 45 min

:material-progress-clock: *Lot Jour 2*

---

## Jour 3 · Données non traditionnelles et technologies qui les traitent

### Deck 06 { #deck-06 }
**Sources de données non traditionnelles : le trésor caché** — 75 min

:material-progress-clock: *Lot Jour 3*

### Deck 07 { #deck-07 }
**Moteurs de passage à l'échelle : technologies big data pour les systèmes statistiques** — 45 min

:material-progress-clock: *Lot Jour 3*

---

## Jour 4 · Lumières nocturnes

### Deck 08 { #deck-08 }
**Lumières nocturnes : ce que l'obscurité nous dit** — 30 min

De DMSP-OLS à VIIRS/DNB ; les produits Black Marble et la série annuelle EOG ; ce
que les NTL approchent bien et ce qu'elles n'approchent pas ; les six artefacts,
nommés ici et rencontrés concrètement à 10h30.

:material-check-circle:{ .ok } **Disponible**

<p>
<a class="md-button md-button--primary" href="../../slides/08-night-time-lights-what-the-darkness-tells-us-fr.html">Présenter (FR)</a>
<a class="md-button" href="../../slides/08-night-time-lights-what-the-darkness-tells-us-en.html">Present (EN)</a>
</p>

<p>
<a href="../../slides/08-night-time-lights-what-the-darkness-tells-us-fr.html?print-pdf">PDF (FR)</a> ·
<a href="../../slides/08-night-time-lights-what-the-darkness-tells-us-en.html?print-pdf">PDF (EN)</a> ·
<a href="https://github.com/STG17-Africa/stg17-workshop/raw/main/slides/pptx/08-ntl-what-darkness-tells-us.fr.pptx">PPTX (FR)</a> ·
<a href="https://github.com/STG17-Africa/stg17-workshop/raw/main/slides/pptx/08-ntl-what-darkness-tells-us.en.pptx">PPTX (EN)</a>
</p>

---

## Jour 5 · Publication et résultats

### Deck 09 { #deck-09 }
**Aider les pays à publier leurs travaux** — 75 min

:material-progress-clock: *Lot Jour 5*

### Deck 10 { #deck-10 }
**Cérémonies d'ouverture et de clôture** — 45 min + 15 min

:material-progress-clock: *Lot Jour 5*

---

## Présentations d'appui

### Deck 11 · Gabarit d'expérience pays { #deck-11 }

Le gabarit de six diapositives utilisé par les participants pour l'échange du
Jour 1 matin, avec les consignes inscrites dans les notes de l'orateur.
[Lire les consignes →](../before/country-slides.md)

:material-progress-clock: *Lot Jour 1*

### Deck 12 · Brief animateurs { #deck-12 }

Comment animer la semaine : minutage, mécanique des deux pistes, quand déclencher
un repli, quoi consigner sur le mur.
[Ressources animateurs →](../resources/facilitators.md)

:material-progress-clock: *Lot Jour 5*

---

## Notes pour les animateurs

!!! info "Le deck HTML fait foi"

    Les présentations sont construites depuis `slides/decks/<id>.deck.html` par
    `python tools/build_slides.py`. Les fichiers PPTX sont **dérivés** — les
    modifications faites dans PowerPoint ne remontent pas, et chaque fichier généré
    le dit sur sa dernière diapositive. Si un changement doit être permanent,
    modifiez la source et reconstruisez.

!!! warning "Les schémas SVG ne survivent pas à la conversion PPTX"

    Les frises, chaînes et schémas sont des SVG écrits à la main, que
    `python-pptx` ne sait pas rastériser. Chaque diapositive PPTX concernée porte
    un emplacement nommant la figure. Capturez-la depuis le deck HTML — deux
    secondes, et un meilleur résultat que n'importe quelle conversion automatique.

!!! tip "Présenter hors ligne"

    reveal.js se charge depuis un CDN. Si le réseau du lieu le bloque, le deck se
    dégrade proprement en document défilable plutôt qu'en page blanche — mais pour
    une vraie présentation, exécutez au préalable
    `python tools/vendor_reveal.py` pour télécharger reveal.js dans
    `slides/vendor/`. Les clés USB distribuées au Jour 0 portent déjà la version
    embarquée.
