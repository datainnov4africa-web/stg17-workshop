# Prérequis

Tout ce qui figure sur cette page découle des treize laboratoires qui composent la
semaine. Rien n'y est pour la forme : chaque élément est quelque chose sans quoi
un laboratoire échouera.

!!! danger "Les trois éléments attendus deux semaines avant l'atelier"

    1. **Six diapositives** sur l'expérience de votre pays en IA et données non traditionnelles — *y compris ce qui n'a pas fonctionné*
    2. **Un compte GitHub personnel** — les productions des laboratoires sont publiées publiquement dès le Jour 2
    3. **Votre paquet de données national** — un fichier de frontières, une publication nationale, et un indicateur infranational officiel

    Tout le reste peut se régler pendant la vérification d'environnement à
    distance à T-1 semaine. Pas ces trois-là : les sessions des autres en dépendent.

---

## 1 · Votre machine

| | Minimum | Recommandé | Si vous êtes en dessous |
|---|---|---|---|
| **RAM** | 8 Go | 16 Go | Chaque laboratoire porte un badge Colab. Utilisez-le. |
| **Disque libre** | 10 Go | 25 Go | Utilisez les variantes Earth Engine, qui ne téléchargent rien |
| **Python** | 3.9 | 3.11 | Colab fournit 3.11 |
| **Droits** | pouvoir installer des paquets | administrateur | Colab ne demande aucun droit |
| **Réseau** | intermittent suffit | stable | Les jeux de données sont préparés à l'avance par l'équipe d'animation |
| **GPU** | non nécessaire | non nécessaire | Aucun laboratoire n'en a besoin. [Kaggle](kaggle.md) en fournit un gratuitement si un exercice optionnel venait à l'exiger |

**Sur le cas des 8 Go.** Les laboratoires géospatiaux fonctionnent quand même.
Chaque étape lourde traite une tuile satellitaire à la fois plutôt que de charger
un pays entier — c'était un choix de conception délibéré. Fermez vos onglets de
navigateur et tout ira bien.

**Sur les portables verrouillés.** Les machines institutionnelles interdisant
l'installation de logiciels sont fréquentes et entièrement anticipées. Google
Colab est le chemin de repli testé pour absolument tous les carnets, et le badge
se trouve dans la première cellule de chacun. Testez-le pendant la vérification
d'environnement plutôt que de le découvrir au Jour 1.

---

## 2 · Comptes

Six comptes, aucun payant. Instructions complètes sur la
[page des comptes](accounts.md).

| Compte | Nécessaire pour | Temps de création |
|---|---|---|
| **GitHub** | Jours 2 à 5. Toutes les productions sont publiées publiquement — **et un jeton d'accès personnel**, car les carnets des Jours 2 et 3 publient depuis le carnet lui-même | 10 min |
| **Google** | Colab — le chemin de repli de tous les carnets | vous en avez probablement un |
| **Google Earth Engine** | la voie sans téléchargement des Jours 3 et 4 | 10 min, plus l'approbation |
| **NASA Earthdata** | télécharger les granules Black Marble au Jour 4 | 5 min |
| **Kaggle** | Optionnel — une voie de secours vers un carnet qui s'exécute si Colab est bloqué. Voir [quand Kaggle est nécessaire](kaggle.md) | 5 min |
| **Un fournisseur LLM** | Jours 1 et 2 | fourni par le Secrétariat |

!!! warning "L'approbation Earth Engine n'est pas instantanée"

    L'inscription exige de rattacher un projet Google Cloud et l'approbation pour
    usage non commercial peut prendre un jour ou deux. Lancez-la dès réception de
    votre invitation, pas la semaine précédente.

---

## 3 · Votre paquet de données national

Trois fichiers, décrits en détail sur la [page du paquet de données](data-pack.md).
Ensemble, ils font que la semaine produit les indicateurs de *votre pays* plutôt
qu'une démonstration sur celui d'un autre.

**A. Un fichier de frontières administratives** — ADM1 au minimum, ADM2 si votre
office le publie. Shapefile ou GeoJSON. Les frontières officielles de votre
office, pas un téléchargement trouvé sur internet : tout l'intérêt est que vos
résultats se réconcilient avec ce que votre office publie déjà.

**B. Une publication statistique nationale** — un PDF ou un rapport contenant des
tableaux. Utilisée au laboratoire du Jour 2, où un LLM en extrait et structure
les données et où vous vérifiez l'extraction contre la source. Choisissez quelque
chose que vous connaissez assez bien pour y repérer une erreur.

**C. Au moins un indicateur infranational officiel** — PIB, population ou taux
d'électrification, par ADM1 ou ADM2. Utilisé le Jour 4 après-midi pour valider
l'indicateur indirect des lumières nocturnes contre la réalité de terrain. **Sans
lui, vous pouvez calculer l'indicateur mais vous ne pouvez pas le valider**, et
c'est la validation qui décide si le résultat est publiable.

!!! tip "Si vos données nationales s'avèrent incomplètes"

    La Côte d'Ivoire est préparée de bout en bout comme pays de référence, et la
    Tunisie l'est pour les laboratoires de connectivité. Toute équipe dont les
    données propres s'avèrent inexploitables bascule sur le pays de référence, le
    note dans sa déclaration de limites, et ne perd aucun temps. C'est la méthode
    qui se transpose ; le pays est un paramètre.

---

## 4 · Compétences

Il n'y a aucun prérequis formel. Les participants arrivent avec des niveaux très
différents, et l'équipe d'animation accompagne la salle tout au long de chaque
laboratoire.

Cela dit, vous tirerez davantage de la semaine si vous êtes à l'aise avec :

- **La lecture de Python.** Pas son écriture à partir de zéro — sa lecture, et la
  modification d'un paramètre. Si vous pouvez regarder
  `panel.groupby("year").sum()` et deviner ce que cela fait, cela suffit.
- **L'idée d'un tableau avec des lignes et des colonnes.** Chaque laboratoire
  aboutit à un tableau.
- **Les données de votre propre office.** Plus précieuses ici que n'importe quelle
  compétence technique. Les laboratoires fournissent la méthode ; vous apportez le
  jugement sur la signification du résultat dans votre pays.

Vous n'avez **pas** besoin d'expérience préalable en imagerie satellitaire,
apprentissage automatique, logiciels géospatiaux ou grands modèles de langage.
Les Jours 1 et 4 partent tous deux des principes de base.

---

## 5 · Exécutez la vérification d'environnement

Un carnet, cinq minutes, et il vous dit point par point si votre machine peut
exécuter les treize laboratoires — puis produit une courte chaîne de diagnostic à
envoyer aux assistants techniques.

[:material-notebook: Vérification d'environnement →](environment-check.md){ .md-button .md-button--primary }

Une séance de vérification à distance est proposée la semaine précédant l'atelier,
une heure, organisée deux fois dans deux fuseaux horaires. Apportez-y votre
chaîne de diagnostic.

---

## 6 · Préparez vos six diapositives

L'échange du Jour 1 matin est ce qui donne sa matière à la semaine. Huit minutes,
six diapositives maximum, et un gabarit est fourni.

L'instruction la plus utile : **soyez franc sur ce qui n'a pas fonctionné.**
Chaque office présent dans la salle a un pilote qui s'est enlisé, un partenariat
jamais signé, un modèle jamais déployé. C'est la moitié la plus utile de
l'échange, et la session de synthèse est conçue pour les mutualiser.

[:material-presentation: Gabarit des diapositives pays →](country-slides.md){ .md-button }

---

## Liste de contrôle

- [ ] Portable avec 8 Go de RAM minimum, idéalement 16 Go et droits administrateur
- [ ] Compte GitHub créé, identifiant transmis au Secrétariat
- [ ] Jeton d'accès personnel GitHub créé et stocké sous `GITHUB_TOKEN`
- [ ] Compte Google fonctionnel, Colab testé une fois
- [ ] Google Earth Engine inscrit et approuvé
- [ ] Compte NASA Earthdata et jeton porteur généré
- [ ] Compte Kaggle (optionnel — uniquement si Colab est bloqué sur votre réseau)
- [ ] Fichier de frontières administratives localisé et partageable
- [ ] Une publication statistique nationale choisie
- [ ] Un indicateur infranational officiel localisé
- [ ] Carnet de vérification d'environnement exécuté, chaîne de diagnostic envoyée
- [ ] Six diapositives pays rédigées, à partir du gabarit
- [ ] Participation à l'une des deux séances de vérification à distance
