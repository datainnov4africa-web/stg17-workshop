# Comptes à créer

Six comptes. **Aucun n'est payant.** Créez-les dans cet ordre — les deux premiers
débloquent tout le reste, et Earth Engine comporte un délai d'approbation qu'il
vaut mieux engager tôt.

## 1 · GitHub — obligatoire

Tout ce que vous construisez à partir du Jour 2 est publié publiquement. Sans
compte, vous pouvez suivre les laboratoires mais vous ne pouvez pas produire le
livrable.

1. [github.com/signup](https://github.com/signup)
2. Choisissez un identifiant que vous acceptez de voir associé aux travaux publiés
   de votre office — il apparaîtra dans l'historique des commits du dépôt de votre
   pays.
3. Transmettez l'identifiant au Secrétariat afin d'être ajouté à l'organisation
   GitHub de l'atelier avant le Jour 2.

!!! tip "Vous avez déjà un compte personnel ?"
    Utilisez-le. Un second compte n'apporte rien, et une identité unique simplifie
    l'étape de citation et de DOI du Jour 5.

## 2 · Google — obligatoire

Utilisé pour Google Colab, le chemin de repli testé de tous les carnets de
l'atelier. La plupart des participants en ont déjà un.

Testez-le une fois avant l'atelier : ouvrez n'importe quel carnet depuis le
[registre des laboratoires](../labs/index.md), cliquez sur le badge Colab et
exécutez la première cellule. Si elle s'exécute, votre chemin de repli fonctionne.

## 3 · Google Earth Engine — vivement recommandé

La voie sans téléchargement des Jours 3 et 4. Sur un réseau contraint, ce n'est
pas un confort — c'est la différence entre terminer le laboratoire et ne pas le
terminer.

1. [code.earthengine.google.com/register](https://code.earthengine.google.com/register)
2. Choisissez l'usage **non commercial / recherche**.
3. Rattachez un projet Google Cloud — la procédure en crée un si vous n'en avez pas.
4. Attendez l'approbation.

!!! warning "Engagez cette démarche tôt"
    L'approbation peut prendre un ou deux jours. Chaque année, quelques
    participants découvrent le Jour 4 au matin que leur inscription est encore en
    attente.

Notez l'identifiant du projet — il alimente la variable `GEE_PROJECT` des carnets
Earth Engine.

## 4 · NASA Earthdata — obligatoire pour la voie locale du Jour 4

Interroger le catalogue de la NASA est public et ne demande rien. **Télécharger**
les granules exige un compte gratuit et un jeton porteur.

1. [urs.earthdata.nasa.gov](https://urs.earthdata.nasa.gov) → Register
2. Connectez-vous, puis profil → **Generate Token**
3. Copiez le jeton. Il est long. Stockez-le sous `EARTHDATA_TOKEN` — voir ci-dessous.

!!! danger "Un téléchargement sans jeton n'échoue pas bruyamment"
    Sans jeton valide, la NASA renvoie une page de connexion HTML. Un script naïf
    l'enregistre sous un nom en `.h5` et l'étape suivante lit n'importe quoi. Le
    téléchargeur de l'atelier vérifie la taille du fichier et supprime tout ce qui
    est anormalement petit — mais si vous écrivez le vôtre, souvenez-vous-en.

## 5 · Kaggle — optionnel

Uniquement si vous comptez exécuter vous-même la démonstration d'affinage du
Jour 1, ou si vous participez à distance et ne recevrez pas la clé USB.
[Guide complet →](kaggle.md)

## 6 · Un fournisseur LLM — fourni par le Secrétariat

Le Secrétariat provisionne des clés par participant avec quotas, distribuées à
l'inscription du Jour 1. Vous n'avez ni compte à créer ni frais à engager.

| Fournisseur | Utilisé au | Pourquoi celui-ci |
|---|---|---|
| **Groq** | Benchmark du Jour 2 | Cité dans l'agenda ; sa vitesse d'inférence est l'objet même de la session |
| **Anthropic** | Jours 1-2 | Contexte long, utilisé pour le laboratoire d'extraction documentaire |
| **Un point d'accès compatible OpenAI** | Jours 1-2 | La référence de comparaison |
| **Ollama** (local) | Jour 1 | La voie souveraine — aucune clé, aucune donnée ne sort du bâtiment |

---

## Où placer vos clés

**Ne collez jamais une clé dans une cellule de carnet.** Une clé collée dans un
carnet que vous poussez ensuite sur GitHub est une clé que vous avez publiée, et
la révoquer est le moindre des désagréments.

=== "Google Colab"

    Cliquez sur l'icône :material-key: dans la barre latérale gauche →
    **Add new secret**. Nommez-la exactement comme le carnet l'attend
    (`GROQ_API_KEY`, `EARTHDATA_TOKEN`, …) et activez **Notebook access**.

=== "Kaggle"

    Add-ons → Secrets → Attach a secret, sous le même nom.

=== "Votre propre machine"

    Créez un fichier nommé `.env` à côté des carnets :

    ```
    GROQ_API_KEY=gsk_...
    EARTHDATA_TOKEN=eyJ0eXAi...
    ```

    Le `.gitignore` du dépôt exclut déjà `.env` : il ne peut pas être versionné par
    accident.

Tous les carnets lisent les clés via `stg17.env.get_secret()`, qui parcourt les
secrets Colab, puis ceux de Kaggle, puis l'environnement, puis `.env` — et signale
une clé absente comme un repli documenté plutôt que comme un plantage.
