# Bibliothèque de prompts — produire une présentation STG17 avec un assistant IA

Ces prompts existent pour qu'un responsable de session qui n'est pas graphiste
puisse produire une présentation qui tienne à côté de celles écrites à la main.
Ce ne sont pas des formules du type « rédige-moi une présentation ». Chacun porte
le système graphique, le contrat de densité et les règles de preuve de cet
atelier — précisément ce qu'un générateur rate quand on ne le lui dit pas.

> **Un générateur est un outil de brouillon, pas un auteur.** Chaque affirmation
> factuelle qu'il renvoie est une affirmation que **vous** publiez sous bannière
> BAD et STATAFRIC. Le prompt P6 existe spécifiquement pour intercepter les
> citations inventées avant qu'elles n'atteignent une salle de statisticiens.

## Quel prompt pour quel travail

| N° | Prompt | À utiliser quand | Fonctionne bien dans |
|----|--------|------------------|----------------------|
| **P1** | [Architecte de présentation](P1-deck-architect.md) | Vous avez une session à l'agenda et rien d'autre. Produit un plan diapositive par diapositive, pas de la prose. | Claude, ChatGPT, Gemini |
| **P2** | [Rédacteur de diapositive](P2-slide-writer.md) | Vous avez le plan et il faut écrire la diapositive *n* au contrat de densité, en HTML. | Claude, ChatGPT |
| **P3** | [Auteur de schéma](P3-diagram-svg.md) | Une diapositive a besoin d'un schéma. Produit du SVG inline à la palette BAD, prêt pour le bilingue. | Claude, ChatGPT |
| **P4** | [Illustration](P4-illustration.md) | Une diapositive a besoin d'une image d'ambiance, pas d'un schéma. | Gemini, Imagen, Midjourney |
| **P5** | [Notes d'orateur](P5-speaker-notes.md) | Les diapositives sont faites et ne portent aucune prose. Ceci écrit ce que l'orateur dit. | Claude, ChatGPT |
| **P6** | [Critique adversarial](P6-critic.md) | Avant publication. Traque les références inventées, les affirmations non étayées, les diapositives surchargées. | Claude, ChatGPT |
| **P7** | [Construction native](P7-native-deck.md) | Vous voulez un vrai PowerPoint conçu. **Commencez ici si le PPTX automatique vous a déçu** — voir la note ci-dessous. | Gamma, Copilot, Claude |
| **P8** | [Version française](P8-translate-fr.md) | La présentation anglaise existe et le français doit l'égaler en densité, pas seulement en sens. | Claude, ChatGPT |
| **P9** | [Présentation autonome](P9-standalone-deck.md) | Vous voulez une présentation `.html` autonome et finie, produite entièrement dans Claude — standard visuel maximal, hors pipeline. | Claude |

Une présentation normale suit **P1 → P2 (×n) → P3/P4 → P5 → P8 → P6**. Lancez P6
en dernier, dans une conversation neuve, pour que le critique n'ait pas assisté à
la rédaction.

## Pourquoi le PowerPoint automatique n'est pas la réponse

`tools/build_pptx.py` produit les fichiers de `docs/slides/pptx/`, et ce sont des
squelettes, pas des présentations. Mesuré sur `01-ai-family-tree-en.pptx` : la
diapositive d'ouverture porte trois phrases citées de vrais cahiers des charges
dans le HTML, et **20 mots** dans le PPTX — le sur-titre, le titre et le pied de
page. La diapositive de glossaire porte huit termes dans le HTML et **11 mots**
dans le PPTX. Le corps de chaque diapositive est perdu.

Ce n'est pas un problème de réglage. Une diapositive reveal.js est mise en page
par CSS — des mesures en `ch`, des colonnes flex, un encadré dimensionné pour
qu'un second ne tienne pas. PowerPoint n'a d'équivalent d'aucun de ces mécanismes,
donc la conversion automatique fidèle n'existe pas. Les options honnêtes sont :
garder le PPTX comme squelette de titres et le dire, ou construire le PowerPoint
nativement avec **[P7](P7-native-deck.md)**, qui remet le système graphique
complet à un outil qui met réellement des diapositives en page.

Dans les deux cas, la présentation reveal.js reste la source de vérité. C'est
elle que la compilation valide pour la densité et la symétrie bilingue, et c'est
elle que le site publie.

## Produire un prompt rempli

Ne recopiez pas ces fichiers à la main. `tools/prompt.py` y injecte la palette
vivante, les seuils de densité réellement appliqués par la compilation et
l'entrée d'agenda de la session, pour qu'un prompt ne puisse jamais dériver du
dépôt :

```bash
python tools/prompt.py --list                    # ce qui est disponible
python tools/prompt.py P1 --deck 02              # architecturer la session 02
python tools/prompt.py P2 --deck 02 --slide 4    # écrire une diapositive
python tools/prompt.py P3 --deck 08 --figure "Frise DMSP vers VIIRS"
python tools/prompt.py P8 --deck 01 --slide 9    # le français de la diapositive 9
python tools/prompt.py P6 --deck 01 --copy       # critique, deck joint, vers le presse-papiers
```

La commande écrit le prompt fini sur la sortie standard ; `--copy` le place dans
le presse-papiers. Collez-le dans l'assistant.

Ce qu'elle ne peut pas résoudre est signalé sur la sortie d'erreur plutôt que
collé sous forme de `{{JETON}}` brut. Quatre valeurs n'ont pas de source dans le
dépôt — le *type*, l'*idée*, la *phrase dite* et la *preuve* d'une diapositive
viennent du plan P1, qui vit dans vos notes. Remplissez-les à la main ;
l'avertissement est là pour vous éviter de l'oublier.

`--lang fr` choisit dans quelle langue de la présentation l'outil lit les
diapositives. Les corps de prompts, eux, restent en anglais : ils sont le contrat
graphique, et un contrat unique dans une seule langue ne peut pas dériver contre
lui-même. Chaque prompt demande au modèle de produire du français là où c'est le
français qui est attendu — c'est l'objet de [P8](P8-translate-fr.md).

## Les quatre règles que chaque prompt porte

Elles sont répétées dans chaque fichier, car un générateur obéit à ce qui est
dans son contexte, pas à ce qui est dans un document voisin.

**1 · Une idée par diapositive.** Au-delà de 110 mots visibles ou six lignes de
tableau, `tools/build_slides.py` échoue. Le budget est de 75. La prose appartient
à `<aside class="notes">`.

**2 · Chaque nombre porte une source.** Une affirmation sans citation est coupée,
pas atténuée. Les prompts demandent au modèle de marquer `[UNVERIFIED]` ce qu'il
ne peut pas sourcer plutôt que de supprimer le marqueur — une affirmation non
vérifiée que l'on voit est plus sûre qu'une affirmation assurée que l'on ne voit
pas.

**3 · La palette est fixe.** Marine `#0B2545`, jade `#1B7A43`, ambre `#F2A900`,
encre `#33403A`, atténué `#6B7B75`, filet `#D5E6DF`, lavis `#F4F8F5`. Tout
matériel généré qui introduit une cinquième couleur d'accent est rejeté en revue.

**4 · Rien n'est écrit deux fois.** La sortie doit être une source
`.deck.html` bilingue unique, avec les marqueurs `<!--EN-->` / `<!--FR-->`. Deux
fichiers séparés divergent en une semaine.

## Ce que ces prompts ne feront pas

Ils n'inventeront pas d'étude de cas, de statistique nationale ni d'article. Là
où une diapositive en a besoin, le prompt demande au modèle d'énoncer la *forme*
de la preuve qu'il faudrait — « une estimation évaluée par les pairs de
l'élasticité des lumières nocturnes au PIB en Afrique de l'Ouest » — et vous
laisse la fournir. C'est délibéré. La littérature 2012-2022 sur les lumières
nocturnes de cet atelier a été assemblée en vérifiant que chaque DOI se résout ;
un générateur à qui l'on demande des citations en produit de plausibles qui
n'existent pas.

## Licences

Le texte que vous générez et éditez vous appartient et se publie sous la licence
de l'atelier. Les images, non automatiquement — voir la note de licence dans
[le catalogue d'emplacements](figure-slots.md) et consignez l'outil et la date
dans `slides/figures/CREDITS.md` avant de publier toute image générée.
