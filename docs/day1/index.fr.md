<!-- GÉNÉRÉ depuis config/agenda.yml par tools/build_site.py. Ne pas modifier. -->

# Jour 1 — Concepts de l'IA et l'infrastructure qui les porte

*Lundi · Un vocabulaire commun, l'expérience des pays, et ce qu'exige réellement la construction et l'exploitation de l'IA*

## Matinée · 09h00 – 12h30

### 09h00–09h30 &nbsp;·&nbsp; Cérémonie d'ouverture

:material-account-group: **Cérémonie** &nbsp;·&nbsp; Plan d’action 4.2 · 4.1.1

Mots de bienvenue et d'ouverture de la Banque africaine de développement et de l'UA STATAFRIC. Objectifs de la semaine, présentation du Plan d'action STG17 2025-2030 et de la place de cet atelier en son sein. Tour de table.


### 09h30–10h00 &nbsp;·&nbsp; Le Hub régional des Nations Unies pour les mégadonnées au Rwanda : jalons et cas d'usage

:material-presentation: **Exposé** &nbsp;·&nbsp; *NISR*

Dix ans du Comité d'experts des Nations Unies sur les mégadonnées et la science des données pour la statistique officielle, et ce que le Hub régional hébergé par le NISR a produit depuis son lancement : les cas d'usage menés le plus loin


### 10h00–10h30 &nbsp;·&nbsp; L'arbre généalogique de l'IA : comment les concepts s'articulent

:material-presentation: **Exposé** &nbsp;·&nbsp; Plan d’action 3.3.2 · 4.1.1

Construction d'une carte conceptuelle commune — IA, LLM, ingénierie de prompt, RAG, affinage, systèmes agentiques, agents, MCP. Ce que chaque concept peut et ne peut pas faire pour la statistique officielle, et la discipline de vocabulaire qui évite les malentendus coûteux. Cette demi-heure fixe le langage de toute la semaine.

[:material-microsoft-powerpoint: PPTX · EN](../downloads/Day1/1000_ai-family-tree_EN.pptx){ .md-button } [:material-microsoft-powerpoint: PPTX · FR](../downloads/Day1/1000_ai-family-tree_FR.pptx){ .md-button }


!!! quote "10h30–10h45 — Pause café"

### 10h45–11h45 &nbsp;·&nbsp; Expériences des pays en IA et en usage des mégadonnées non traditionnelles

:material-forum: **Plénière** &nbsp;·&nbsp; Plan d’action 3.3.2 · 3.1.2 · 2.1.1

Brèves présentations pays (8 minutes chacune, 6 diapositives maximum) sur ce qui a réellement été tenté sur place — pilotes lancés, partenariats de données signés, obstacles rencontrés, résultats publiés. Les pays sont invités à être francs sur ce qui n'a pas fonctionné ; c'est la moitié la plus utile de l'échange.


### 11h45–12h30 &nbsp;·&nbsp; Synthèse : où en est le continent

:material-lightbulb-on: **Animée** &nbsp;·&nbsp; Plan d’action 3.1.2 · 4.1.1

Discussion animée structurée autour de quatre questions tirées des présentations — quels cas d'usage reviennent, quels partenariats de données sont réplicables, quels obstacles sont partagés, et où la mutualisation serait payante. Les productions sont consignées sur un mur ouvert toute la semaine. Se termine par l'auto-évaluation initiale des compétences.


!!! quote "12h30–14h00 — Déjeuner"

## Après-midi · 14h00 – 17h00

### 14h00–14h30 &nbsp;·&nbsp; Infrastructure de l'IA : ce qu'exige réellement l'exploitation de l'IA dans un office statistique

:material-presentation: **Exposé** &nbsp;·&nbsp; Plan d’action 4.2.3 · 3.3.2

Fondamentaux et besoins — GPU et accélérateurs, mémoire et contexte, inférence contre entraînement, latence et débit. Nuage, hybride ou sur site ; souveraineté des données et contraintes de confidentialité des microdonnées d'un INS ; modélisation des coûts par cas d'usage ; modèles à poids ouverts contre propriétaires. À quoi ressemble une configuration d'entrée de gamme réaliste pour un INS africain, avec des ordres de grandeur indicatifs.


### 14h30–15h30 &nbsp;·&nbsp; Atelier partie 1 — Génération augmentée par récupération (RAG)

:material-flask: **Laboratoire** &nbsp;·&nbsp; Plan d’action 4.2.1 · 2.1.1

Construire un assistant RAG fonctionnel sur un corpus statistique (note de concept STG17, plan d'action, SHaSA II, documents méthodologiques nationaux) — découpage, plongements, base vectorielle, récupération, réponse ancrée. Le tester sur des questions à réponse connue et observer où la récupération échoue, et pourquoi.

!!! example "Laboratoire — Assistant RAG"

    **Livrable :** Un relevé de réponses avec les passages exacts qui les fondent, et une évaluation de la récupération séparant les échecs de récupération des échecs de génération

    **Repli :** Un corpus fictif de cinq documents est fourni avec la boîte à outils, donc aucune équipe n'est bloquée par des publications non validées ; sans aucun fournisseur de modèle, la moitié « récupération » du laboratoire fonctionne quand même — et c'est là que sont la plupart des problèmes du RAG


### 15h30–16h45 &nbsp;·&nbsp; Atelier partie 2 — Du RAG à l'agent

:material-flask: **Laboratoire** &nbsp;·&nbsp; Plan d’action 4.2.1 · 4.2.3

Transformer le récupérateur construit avant la pause en outil, et l'envelopper dans un agent — outils et appel de fonctions, planification et itération, mémoire, gestion d'erreurs et points de contrôle humains. L'agent répond à une question, retrouve les chiffres à l'appui et rédige une courte note ; les participants examinent ensuite précisément où il doit rester supervisé.

!!! example "Laboratoire — Du RAG à l'agent"

    **Livrable :** Un journal d'audit consignant chaque outil demandé par le modèle, son autorisation par la politique, et la réponse brute derrière chaque demande — plus la note écrite par l'agent une fois une politique l'y autorisant

    **Repli :** Un modèle scripté rejoue des réponses fixes : la boucle, le point d'approbation, la reprise sur erreur et le journal d'audit s'exercent donc sans clé API. C'est délibéré et non un chemin de repli — ces quatre éléments sont ce qu'un office écrit et possède ; le modèle est ce qu'il loue


!!! quote "16h45–17h00 — Pause café"

