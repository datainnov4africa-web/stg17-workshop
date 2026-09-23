# Quand Kaggle est nécessaire — et quand il ne l'est pas

Réponse courte : **aucun laboratoire ne l'exige.** Tous les laboratoires de la
semaine tournent sur un portable ou sur Colab gratuit. Cette page existe pour que
vous sachiez à quoi sert Kaggle ici, et pour que personne ne crée un compte qu'il
n'utilisera pas.

---

## Ce qu'est Kaggle, dans cet atelier

Kaggle est l'un des endroits où un carnet de l'atelier peut s'exécuter, aux côtés
de Colab, de votre propre machine et d'un simple exécuteur d'intégration
continue. La boîte à outils le détecte automatiquement, et plusieurs des carnets
fournis lisent leurs clés API dans le gestionnaire de secrets de Kaggle
exactement comme ils le feraient dans celui de Colab — sans rien à modifier.

## Quand le compte vaut la peine d'être créé

**Si votre machine est verrouillée et que Colab est bloqué.** Les réseaux
institutionnels autorisent parfois l'un et pas l'autre. Disposer d'une seconde
voie testée vers un carnet qui s'exécute, c'est la valeur réelle de Kaggle pour
cette semaine — et le moment de découvrir quelles voies votre réseau autorise est
la vérification d'environnement, pas le Jour 1.

**Si un exercice optionnel exige un jour un GPU garanti.** Le quota hebdomadaire
de Kaggle — deux GPU T4 ou un P100, environ 30 heures par semaine — est
l'allocation gratuite la plus généreuse accessible sans compte institutionnel et,
contrairement à l'offre gratuite de Colab, c'est un quota et non une loterie.

!!! note "Aucun laboratoire de l'agenda n'a besoin d'un GPU"

    Les douze laboratoires portent sur la recherche d'information, le prompt,
    les tableaux de bord, l'analyse géospatiale et la publication. Aucun
    n'entraîne de modèle. Si un animateur ajoute un exercice optionnel qui le
    fait, c'est ici qu'il faudra l'exécuter.

---

## Là où Kaggle est le mauvais outil

| Situation | Utilisez plutôt |
|---|---|
| Laboratoires géospatiaux (Jours 3 et 4) | Votre portable, ou les variantes Earth Engine. La pile géospatiale de Kaggle est correcte mais n'apporte rien ici. |
| Tout ce qui nécessite une clé API que vous avez créée | Colab. Kaggle Secrets fonctionne, mais c'est le gestionnaire de Colab qui a été testé avec les carnets. |
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
3. Réglages du carnet à droite : **Internet → On**
4. Pour les clés API : Add-ons → Secrets → attachez votre clé sous le nom exact
   attendu par le carnet (`GROQ_API_KEY`, `GITHUB_TOKEN`, …)

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
| J2 · Du document au tableau de bord | Non |
| J2 · Benchmark des fournisseurs | Non |
| J2 · Ateliers boîte à outils | Non |
| J3 · Ookla et WorldPop | Non |
| J3 · Elasticsearch | Non |
| J3 · Exploration pilotée par la recherche | Non |
| J4 · NTL collecter et explorer | Non |
| J4 · NTL explorer et comprendre | Non |
| J4 · NTL analyse et validation | Non |
| J5 · Publier vos travaux | Non |

Douze laboratoires, douze fois non. Ne créez le compte que si Colab est bloqué
sur votre réseau.
