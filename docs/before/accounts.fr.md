# Comptes à créer

Sept comptes. **Aucun n'est payant.** Créez-les dans cet ordre — les deux premiers
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
4. Créez un **jeton d'accès personnel** : Settings → Developer settings →
   Personal access tokens → *Fine-grained tokens* → Generate new token.
   Accordez-lui **Contents : Read and write** sur vos propres dépôts, et
   stockez-le sous `GITHUB_TOKEN` — voir [où placer vos clés](#ou-placer-vos-cles).

!!! info "Pourquoi un jeton, et pas seulement le compte"
    Les notebooks des Jours 2, 3 et 4 publient votre livrable sur GitHub depuis le
    notebook lui-même. Sans `GITHUB_TOKEN`, le notebook conserve vos fichiers et saute
    l'étape de publication : vous avez toujours le travail, mais pas l'URL
    publique — et c'est l'URL publique qui *est* le livrable.

!!! tip "Vous avez déjà un compte personnel ?"
    Utilisez-le. Un second compte n'apporte rien, et une identité unique simplifie
    l'étape de citation et de DOI du Jour 5.

## 2 · Google — obligatoire

Utilisé pour Google Colab, le chemin de repli testé de tous les notebooks de
l'atelier. La plupart des participants en ont déjà un.

Testez-le une fois avant l'atelier : ouvrez une page-jour — le [Jour 1](../day1/index.md),
par exemple —, cliquez sur le badge Colab placé à côté d'un notebook et exécutez la
première cellule. Si elle s'exécute, votre chemin de repli fonctionne.

## 3 · Google Earth Engine — vivement recommandé

Le notebook du Jour 4 après-midi lit les lumières nocturnes VIIRS via Earth Engine
et vous demande l'identifiant de votre projet au démarrage. Sans compte approuvé,
ce notebook ne peut pas s'exécuter du tout — d'où l'intérêt de s'y prendre tôt.

1. [code.earthengine.google.com/register](https://code.earthengine.google.com/register)
2. Choisissez l'usage **non commercial / recherche**.
3. Rattachez un projet Google Cloud — la procédure en crée un si vous n'en avez pas.
4. Attendez l'approbation.

!!! warning "Engagez cette démarche tôt"
    L'approbation peut prendre un ou deux jours. Chaque année, quelques
    participants découvrent le Jour 4 au matin que leur inscription est encore en
    attente.

Notez l'identifiant du projet — il alimente la variable `GEE_PROJECT` des notebooks
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

Une seconde voie testée vers un notebook qui s'exécute, utile si votre machine est
verrouillée et que Colab est bloqué sur votre réseau. Aucun laboratoire ne
l'exige, et les notebooks lisent le gestionnaire de secrets de Kaggle exactement
comme celui de Colab.

## 6 · Un fournisseur LLM — nécessaire, et c'est vous qui le créez

Vous créez ces comptes et obtenez vos propres clés, avant votre départ. Les deux
fournisseurs ci-dessous délivrent une clé gratuite depuis une console web en
quelques minutes ; les notebooks la lisent depuis un secret ou une variable
d'environnement, jamais depuis une cellule que vous modifiez.

Ayez-les **avant le Jour 1** : le premier laboratoire qui appelle un modèle
s'exécute le Jour 1 à 14h30, pas au Jour 2.

| Fournisseur | Utilisé au | Nom de la clé | À créer sur |
|---|---|---|---|
| **Groq** | Tous les laboratoires LLM, Jours 1 et 2 | `GROQ_API_KEY` | [console.groq.com/keys](https://console.groq.com/keys) |
| **Google Gemini** | Matinée du Jour 2, où il est le fournisseur par défaut | `GEMINI_API_KEY` | [aistudio.google.com/apikey](https://aistudio.google.com/apikey) |
| **Ollama** (local) | Jours 1 et 2 | *aucune* | Installé sur votre portable — la voie souveraine, aucune clé et aucune donnée ne sort du bâtiment |

Groq est celui à créer en premier : c'est le fournisseur que tous les notebooks LLM
acceptent, et le défaut de tous sauf un.

!!! tip "Si vous disposez déjà d'une clé ailleurs"

    Le notebook tableau de bord du Jour 2 accepte aussi **Mistral**, **Z.ai**,
    **Cerebras** et **OpenRouter**, et deux notebooks acceptent n'importe quel
    point d'accès **compatible OpenAI**. Une ligne à changer en tête du notebook.
    Aucun de ces comptes n'est à créer pour l'atelier.

---

## Où placer vos clés

**Ne collez jamais une clé dans une cellule de notebook.** Une clé collée dans un
notebook que vous poussez ensuite sur GitHub est une clé que vous avez publiée, et
la révoquer est le moindre des désagréments.

=== "Google Colab"

    Cliquez sur l'icône :material-key: dans la barre latérale gauche →
    **Add new secret**. Nommez-la exactement comme le notebook l'attend
    (`GROQ_API_KEY`, `EARTHDATA_TOKEN`, …) et activez **Notebook access**.

=== "Kaggle"

    Add-ons → Secrets → Attach a secret, sous le même nom.

=== "Votre propre machine"

    Créez un fichier nommé `.env` à côté des notebooks :

    ```
    GROQ_API_KEY=gsk_...
    EARTHDATA_TOKEN=eyJ0eXAi...
    GITHUB_TOKEN=github_pat_...
    ```

    Le `.gitignore` du dépôt exclut déjà `.env` : il ne peut pas être versionné par
    accident.

La plupart des notebooks lisent les clés via `stg17.env.get_secret()`, qui parcourt
les secrets Colab, puis ceux de Kaggle, puis l'environnement, puis `.env` — et
signale une clé absente comme un repli documenté plutôt que comme un plantage. Les
autres embarquent leur propre lecteur, qui cherche aux mêmes endroits, dans le
même ordre.
