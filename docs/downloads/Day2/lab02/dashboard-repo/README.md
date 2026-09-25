# Marché du travail, population et accès Internet

Tableau de bord bilingue (EN/FR) construit à partir de **Bulletin statistique trimestriel**, pages 1, 2.

Réalisé pendant l'atelier technique STG17 *Emerging Issues, Emerging Practice*
(Banque africaine de développement / AU STATAFRIC), labo 02 — du document statistique
au tableau de bord public.

## Contenu du dépôt

| Fichier | Ce que c'est |
|---|---|
| `index.html` | le tableau de bord. Un fichier, sans compilation, sans serveur, sans traceur |
| `data/dashboard_data.json` | le jeu de données vérifié qui alimente la page |
| `data/verification_report.csv` | tous les contrôles automatiques, pour chaque cellule |
| `data/glossary.json` | la terminologie FR/EN utilisée pour les libellés |
| `LIMITATIONS.md` | ce que ces chiffres ne permettent pas de conclure |

## Méthode

1. Texte extrait page par page avec `pdfplumber`.
2. Chaque tableau lu **deux fois et indépendamment** : une fois par un lecteur à base de
   règles, une fois par `openai/gpt-oss-120b`
   via Groq.
3. Chaque cellule a franchi cinq contrôles — provenance de page, preuve citée, unité et
   plage, réconciliation avec les totaux publiés, et accord entre les deux lectures.
4. Les cellules sans preuve dans la page ont été **écartées**, pas publiées. Celles qui
   échouent à un autre contrôle sont publiées avec une mention « à revoir » visible.
5. Libellés traduits glossaire d'abord, modèle ensuite, avec contrôle par rétrotraduction.

Résultats de l'exécution qui a produit cette page :

| Issue | Cellules |
|---|---|
| vérifiées | 76 |
| publiées mais signalées | 0 |
| écartées | 1 |

## Reproduire

Ouvrez `02-Labo-Du-document-statistique-au-tableau-de-bord-public.ipynb` dans Colab,
Kaggle ou Jupyter, pointez `SOURCE` sur la même publication et exécutez.

## Citation

Citez **la publication source**, pas ce tableau de bord. Cette page est une présentation
de chiffres publiés par l'institut ; elle n'est pas elle-même une publication statistique.

## Responsable

<!-- nom, unité, courriel, et la date de la prochaine actualisation -->
