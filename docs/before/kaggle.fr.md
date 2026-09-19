# Quand Kaggle est nécessaire — et quand il ne l'est pas

Réponse courte : **la plupart des participants n'en auront jamais besoin.** La
plupart des laboratoires tournent très bien sur un portable ou sur Colab gratuit.
Cette page existe pour que les deux qui bénéficient de Kaggle ne soient pas une
surprise le jour venu, et pour que personne ne crée un compte qu'il n'utilisera
pas.

---

## Les deux cas où Kaggle mérite sa place

### 1 · La démonstration d'affinage du Jour 1

Le matériel du Jour 1 après-midi comprend une démonstration d'affinage LoRA —
modifier les poids d'un modèle pour qu'il réponde toujours dans un style maison,
plutôt que de le lui demander dans le prompt. C'est le seul moment de la semaine
où un GPU change l'expérience, et pas seulement la vitesse.

| Environnement | Ce que donne la démo |
|---|---|
| Processeur de portable | fonctionne, environ 15 à 25 minutes pour la boucle d'entraînement |
| Colab, offre gratuite | fonctionne, mais l'attribution du GPU n'est pas garantie et les sessions sont coupées |
| **Kaggle** | **deux GPU T4 ou un P100, ~30 heures par semaine, garanti pour la session** |

Le quota GPU hebdomadaire de Kaggle est l'allocation gratuite la plus généreuse
accessible sans compte institutionnel — et, contrairement à l'offre gratuite de
Colab, c'est un quota et non une loterie. Si vous voulez exécuter l'affinage
vous-même plutôt que de regarder l'animateur, c'est là qu'il faut le faire.

### 2 · Exécuter un modèle à poids ouverts en local, pour la discussion de souveraineté

Le Jour 1 après-midi pose une vraie question : que coûte réellement à un INS
l'exploitation de son propre modèle plutôt que l'envoi de microdonnées vers une
API commerciale ? La manière honnête d'y répondre est d'en exécuter un. Un modèle
à poids ouverts de 7 milliards de paramètres réclame environ 16 Go de mémoire GPU
en demi-précision, ce qu'aucun portable de participant n'aura et que Kaggle
fournit gratuitement.

Le résultat n'est pas un benchmark à publier. C'est le chiffre dont vous avez
besoin pour avoir une conversation informée avec votre direction informatique sur
ce qu'impliquerait une option sur site.

---

## Là où Kaggle est le mauvais outil

| Situation | Utilisez plutôt |
|---|---|
| Laboratoires géospatiaux (Jours 3 et 4) | Votre portable, ou les variantes Earth Engine. La pile géospatiale de Kaggle est correcte mais n'apporte rien ici. |
| Tout ce qui nécessite une clé API qu'on vous a remise | Colab. Kaggle Secrets fonctionne, mais c'est le gestionnaire de Colab qui a été testé avec les carnets. |
| Publier vos résultats | GitHub Pages. Un carnet Kaggle n'est pas un produit public citable ; le Jour 5 explique ce qui l'est. |
| Longues exécutions sans surveillance | Les sessions Kaggle s'arrêtent après 12 heures (9 avec GPU). Rien dans cet atelier ne dure aussi longtemps. |

---

## Créer le compte

1. Rendez-vous sur [kaggle.com](https://www.kaggle.com) et inscrivez-vous —
   courriel ou compte Google.
2. **Vérifiez votre numéro de téléphone.** C'est l'étape que l'on manque :
   l'accès au GPU et l'accès internet depuis les carnets restent tous deux
   verrouillés tant que le compte n'est pas vérifié, et la vérification n'est pas
   évidente dans l'interface. Settings → Phone Verification.
3. Optionnel : Settings → Account → Create New API Token, si vous souhaitez
   pousser des jeux de données ou des carnets depuis votre machine.

Total : environ cinq minutes, plus le délai du SMS.

---

## Exécuter un carnet de l'atelier sur Kaggle

Tous les carnets de ce dépôt détectent Kaggle automatiquement.
`stg17.env.setup()` identifie la plateforme, résout
`/kaggle/working/STG17_LOCAL` comme racine de données, et lit les secrets dans le
gestionnaire de Kaggle plutôt que dans celui de Colab. Rien n'est à modifier dans
le carnet.

```python
from stg17 import setup
S = setup(REQUIREMENTS, lang="FR")
print(S.platform)     # -> 'kaggle'
print(S.root)         # -> /kaggle/working/STG17_LOCAL
```

Pour en téléverser un :

1. Kaggle → Create → New Notebook → File → Import Notebook
2. Téléversez le `.ipynb`, ou collez l'URL GitHub
3. Réglages du carnet à droite : **Accelerator → GPU T4 x2**, **Internet → On**
4. Pour les clés API : Add-ons → Secrets → attachez votre clé sous le nom exact
   attendu par le carnet (`GROQ_API_KEY`, `ANTHROPIC_API_KEY`, …)

!!! warning "L'accès internet est désactivé par défaut sur Kaggle"

    Un carnet Kaggle neuf n'a aucun accès réseau, et `pip install` échoue sur un
    délai d'attente déroutant plutôt que sur un message clair. Activez Internet
    dans le panneau de réglages avant d'exécuter la cellule des prérequis. Presque
    tout le monde se fait prendre une fois.

---

## Récapitulatif

| Laboratoire | Kaggle nécessaire ? |
|---|---|
| J1 · Assistant RAG | Non |
| J1 · Du RAG à l'agent | Non |
| J1 · Démonstration d'affinage | **Recommandé** — GPU gratuit garanti |
| J1 · Modèle à poids ouverts, chiffrage de souveraineté | **Recommandé** — exige ~16 Go de mémoire GPU |
| J2 · Du document au tableau de bord | Non |
| J2 · Benchmark des fournisseurs | Non |
| J2 · Ateliers boîte à outils | Non |
| J3 · Ookla et WorldPop | Non |
| J3 · Elasticsearch | Non |
| J4 · NTL collecter et explorer | Non |
| J4 · NTL analyse et validation | Non |
| J5 · Publier vos travaux | Non |
