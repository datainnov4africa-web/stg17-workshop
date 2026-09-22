<!-- GÉNÉRÉ depuis config/agenda.yml par tools/build_site.py. Ne pas modifier. -->

# Jour 2 — Ingénierie de prompt et usage optimisé des LLM

*Mardi · Obtenir des modèles de langage un travail fiable, rapide et abordable*

## Matinée · 09h00 – 12h30

### 09h00–10h30 &nbsp;·&nbsp; Parler aux machines : l'art de l'ingénierie de prompt

:material-presentation-play: **Exposé + laboratoire** &nbsp;·&nbsp; Plan d’action 4.2.1

Cadrage de la tâche, rôle et contexte, contraintes explicites, exemples few-shot, décomposition, sorties JSON structurées, garde-fous et itération systématique. Pourquoi les modèles hallucinent et comment la conception du prompt réduit le phénomène. Anti-patrons courants et comment les détecter dans vos propres prompts.

[:material-file-pdf-box: PDF · EN](../downloads/Day2/0900_talking-to-machines_EN.pdf){ .md-button } [:material-file-pdf-box: PDF · FR](../downloads/Day2/0900_talking-to-machines_FR.pdf){ .md-button } [:material-microsoft-powerpoint: PPTX · EN](../downloads/Day2/0900_talking-to-machines_EN.pptx){ .md-button } [:material-microsoft-powerpoint: PPTX · FR](../downloads/Day2/0900_talking-to-machines_FR.pptx){ .md-button } [:material-notebook-outline: IPYNB · EN](../downloads/Day2/0900_talking-to-machines_EN.ipynb){ .md-button } [:material-notebook-outline: IPYNB · FR](../downloads/Day2/0900_talking-to-machines_FR.ipynb){ .md-button }

[![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/datainnov4africa-web/stg17-workshop/blob/main/docs/downloads/Day2/0900_talking-to-machines_EN.ipynb) **EN** &nbsp; [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/datainnov4africa-web/stg17-workshop/blob/main/docs/downloads/Day2/0900_talking-to-machines_FR.ipynb) **FR**


!!! quote "10h30–10h45 — Pause café"

### 10h45–12h30 &nbsp;·&nbsp; Atelier — Du document statistique au tableau de bord public

:material-flask: **Laboratoire** &nbsp;·&nbsp; Plan d’action 4.2.1 · 2.1.1

Prendre une publication statistique nationale (PDF ou rapport), utiliser un LLM pour en extraire et structurer les données, vérifier l'extraction contre la source, générer un tableau de bord interactif et le publier en ligne sur GitHub Pages. Chaque participant repart avec une URL publique. L'étape de vérification n'est pas optionnelle — c'est elle qui rend le résultat publiable.

[:material-notebook-outline: IPYNB · EN](../downloads/Day2/1045_hands-on_EN.ipynb){ .md-button } [:material-notebook-outline: IPYNB · FR](../downloads/Day2/1045_hands-on_FR.ipynb){ .md-button }

[![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/datainnov4africa-web/stg17-workshop/blob/main/docs/downloads/Day2/1045_hands-on_EN.ipynb) **EN** &nbsp; [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/datainnov4africa-web/stg17-workshop/blob/main/docs/downloads/Day2/1045_hands-on_FR.ipynb) **FR**

!!! example "Laboratoire — Du document au tableau de bord"

    **Livrable :** Une URL publique de tableau de bord et le tableau de vérification comparant l'extraction à la source

    **Repli :** Une publication d'exemple et un gabarit statique de tableau de bord sont fournis ; la publication peut se faire à partir du seul gabarit


!!! quote "12h30–14h00 — Déjeuner"

## Après-midi · 14h00 – 17h00

### 14h00–14h45 &nbsp;·&nbsp; De bon à excellent : optimisation des prompts

:material-presentation-play: **Exposé + laboratoire** &nbsp;·&nbsp; Plan d’action 4.2.1 · 4.2.3

L'amélioration systématique plutôt que le tâtonnement — construire un jeu d'évaluation, mesurer la qualité des sorties, maîtriser la variance, gérer la longueur de contexte et le coût en tokens, la mise en cache, et arbitrer entre prompt, RAG et affinage.

[:material-file-pdf-box: PDF · EN](../downloads/Day2/1400_from-good-to-great_EN.pdf){ .md-button } [:material-file-pdf-box: PDF · FR](../downloads/Day2/1400_from-good-to-great_FR.pdf){ .md-button } [:material-microsoft-powerpoint: PPTX · EN](../downloads/Day2/1400_from-good-to-great_EN.pptx){ .md-button } [:material-microsoft-powerpoint: PPTX · FR](../downloads/Day2/1400_from-good-to-great_FR.pptx){ .md-button } [:material-notebook-outline: IPYNB · EN](../downloads/Day2/1400_from-good-to-great_EN.ipynb){ .md-button } [:material-notebook-outline: IPYNB · FR](../downloads/Day2/1400_from-good-to-great_FR.ipynb){ .md-button }

[![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/datainnov4africa-web/stg17-workshop/blob/main/docs/downloads/Day2/1400_from-good-to-great_EN.ipynb) **EN** &nbsp; [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/datainnov4africa-web/stg17-workshop/blob/main/docs/downloads/Day2/1400_from-good-to-great_FR.ipynb) **FR**


### 14h45–15h30 &nbsp;·&nbsp; Choisir son moteur : vitesse, coût et souveraineté — travailler avec Groq

:material-speedometer: **Exposé + benchmark** &nbsp;·&nbsp; Plan d’action 4.2.3

Comment la vitesse d'inférence change ce qui est faisable dans une chaîne statistique de production. Les participants exécutent le même prompt chez deux fournisseurs, dont Groq, et consignent latence, coût pour mille documents et qualité de sortie dans une feuille de comparaison partagée. Cette feuille devient un intrant réutilisable pour les achats de leur office.

!!! example "Laboratoire — Benchmark des fournisseurs"

    **Livrable :** Trois lignes dans la feuille de comparaison partagée : latence, coût pour mille documents, score de qualité

    **Repli :** L'animateur exécute le benchmark en direct depuis le pupitre si les clés des participants échouent


### 15h30–16h45 &nbsp;·&nbsp; Atelier — Une boîte à outils LLM pour statisticiens

:material-flask: **Laboratoire** &nbsp;·&nbsp; Plan d’action 4.2.1

Ateliers tournants sur des cas d'usage professionnels — écrire et déboguer du code ; rédiger rapports et notes méthodologiques ; produire des présentations ; générer graphiques et visuels ; travail sur l'image et l'identité visuelle, y compris la création de logos ; analyse documentaire et synthèses audio avec NotebookLM ; multimodalité avec Gemini. Chaque participant choisit deux ateliers pertinents pour son office et repart avec un livrable achevé de chacun.

!!! example "Laboratoire — Ateliers boîte à outils"

    **Livrable :** Deux productions achevées par participant, une de chaque atelier choisi

    **Repli :** Les ateliers sont indépendants — un atelier en panne ne coûte que lui-même


!!! quote "16h45–17h00 — Pause café"

