# %% [meta]
'''
id: d1_rag_assistant
day: 1
title_en: Build a RAG Assistant Over Your Own Publications
title_fr: Construire un assistant RAG sur vos propres publications
outdir: notebooks/day1
stem: D1_RAG_Assistant
country: CIV
tracks: guided, open
'''

# %% [markdown]
'''
<!--EN-->
<div style="background:linear-gradient(135deg,#0B2545 0%,#1B7A43 100%);
 border-radius:18px;padding:32px 38px;font-family:'Segoe UI',system-ui,sans-serif;margin-bottom:6px;">
 <div style="color:#F2A900;font-size:12.5px;letter-spacing:3px;font-weight:700;
  text-transform:uppercase;">African Development Bank · AU STATAFRIC · STG17 · Day 1 · 14:45</div>
 <div style="color:#fff;font-size:2em;font-weight:800;margin:10px 0 8px;line-height:1.15;">
  A RAG assistant over your own publications</div>
 <div style="color:#dbe7e0;font-size:1.05em;line-height:1.55;max-width:900px;">
  By the end of this laboratory you will have an assistant that answers questions about your
  office's documents, <b>cites the passage it used</b>, and says so when the answer is not there.
  That last behaviour is the one that makes it publishable.
 </div>
 <div style="color:#F2A900;font-size:13px;margin-top:14px;font-weight:600;">
  90 minutes · no GPU · works on a laptop, on Colab and on Kaggle</div>
</div>

> **What you are building, in one sentence.** Not a model that knows your
> statistics — this morning established that no model does. A pipeline that
> *retrieves* the right paragraph from your own documents and asks a model to
> answer **from that paragraph only**.
<!--FR-->
<div style="background:linear-gradient(135deg,#0B2545 0%,#1B7A43 100%);
 border-radius:18px;padding:32px 38px;font-family:'Segoe UI',system-ui,sans-serif;margin-bottom:6px;">
 <div style="color:#F2A900;font-size:12.5px;letter-spacing:3px;font-weight:700;
  text-transform:uppercase;">Banque africaine de développement · UA STATAFRIC · STG17 · Jour 1 · 14h45</div>
 <div style="color:#fff;font-size:2em;font-weight:800;margin:10px 0 8px;line-height:1.15;">
  Un assistant RAG sur vos propres publications</div>
 <div style="color:#dbe7e0;font-size:1.05em;line-height:1.55;max-width:900px;">
  À la fin de ce laboratoire, vous disposerez d'un assistant qui répond aux questions sur les
  documents de votre office, <b>cite le passage utilisé</b>, et déclare quand la réponse n'y est
  pas. C'est ce dernier comportement qui le rend publiable.
 </div>
 <div style="color:#F2A900;font-size:13px;margin-top:14px;font-weight:600;">
  90 minutes · sans GPU · fonctionne sur portable, sur Colab et sur Kaggle</div>
</div>

> **Ce que vous construisez, en une phrase.** Non pas un modèle qui connaît vos
> statistiques — ce matin a établi qu'aucun modèle ne les connaît. Une chaîne qui
> *récupère* le bon paragraphe dans vos propres documents et demande à un modèle
> de répondre **à partir de ce paragraphe uniquement**.
'''

# %% [markdown]
'''
<!--EN-->
### The road through this laboratory

| # | Step | What you learn |
|---|------|----------------|
| 1 | Setup and a model provider | Which paths work when a key is missing |
| 2 | Load a corpus | Why a scanned PDF is invisible to your assistant |
| 3 | Cut it into passages | What chunk size and overlap actually change |
| 4 | Two retrievers, compared | Word matching versus meaning matching, and how each fails |
| 5 | The prompt that forbids invention | Where the refusal rule lives |
| 6 | Ask, and read the citation | An answer without its source is not usable |
| 7 | The refusal test | A system that always answers is broken |
| 8 | Calibrate the score floor | Turning "always answers" into "answers when it can" |
| 9 | Evaluate and save | Separating a retrieval problem from a generation problem |

**Requirements.** `scikit-learn`, `pandas`, and the `stg17` toolkit. Optional:
`sentence-transformers` for the meaning-based retriever (about 90 MB, once), and
`pypdf` if your corpus is PDF. The next cell installs what is missing.

**A model provider is optional for steps 1–4 and 8–9.** Steps 5–7 need one. If
you have no API key, the notebook tells you which paths remain open.
<!--FR-->
### Le parcours de ce laboratoire

| # | Étape | Ce que vous apprenez |
|---|-------|----------------------|
| 1 | Installation et fournisseur de modèle | Quels chemins fonctionnent sans clé |
| 2 | Charger un corpus | Pourquoi un PDF scanné est invisible pour votre assistant |
| 3 | Le découper en passages | Ce que changent réellement la taille et le recouvrement |
| 4 | Deux récupérateurs comparés | Mots contre sens, et comment chacun échoue |
| 5 | Le prompt qui interdit l'invention | Où vit la règle de refus |
| 6 | Interroger et lire la citation | Une réponse sans sa source est inutilisable |
| 7 | Le test de refus | Un système qui répond toujours est défaillant |
| 8 | Calibrer le seuil de score | Passer de « répond toujours » à « répond quand il peut » |
| 9 | Évaluer et enregistrer | Distinguer un problème de récupération d'un problème de génération |

**Prérequis.** `scikit-learn`, `pandas` et la boîte à outils `stg17`. En option :
`sentence-transformers` pour le récupérateur sémantique (environ 90 Mo, une fois),
et `pypdf` si votre corpus est en PDF. La cellule suivante installe ce qui manque.

**Un fournisseur de modèle est optionnel pour les étapes 1 à 4 et 8 à 9.** Les
étapes 5 à 7 en exigent un. Sans clé API, le carnet vous indique quels chemins
restent ouverts.
'''

# %%
# EN: The workshop toolkit, plus what this laboratory needs. Safe to re-run. | FR: La boîte à outils de l'atelier, plus ce qu'exige ce laboratoire. Ré-exécutable.
import subprocess
import sys

REPO = "https://github.com/{{ORG}}/{{REPO}}"

try:
    import stg17  # noqa: F401
except ImportError:
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", f"git+{REPO}.git"], check=False)

from stg17 import env, i18n, rag, ui  # noqa: E402
from stg17.i18n import T  # noqa: E402

S = env.setup({"scikit-learn": "scikit-learn>=1.3", "pandas": "pandas>=2.0"}, lang="{{LANG_UPPER}}")
print(S.summary())

# %% [markdown]
'''
<!--EN-->
---
## 1 · One variable, and a model provider

`COUNTRY_ISO3` decides where your outputs are written and how they are labelled.
Change it to your own country and the rest of the notebook follows — the registry
covers all 55 African Union member states.

The provider table below is the honest picture of what you can run today.
<!--FR-->
---
## 1 · Une variable, et un fournisseur de modèle

`COUNTRY_ISO3` détermine où vos sorties sont écrites et comment elles sont
étiquetées. Mettez votre propre pays et le reste du carnet suit — le registre
couvre les 55 États membres de l'Union africaine.

Le tableau des fournisseurs ci-dessous donne l'image honnête de ce que vous
pouvez exécuter aujourd'hui.
'''

# %%
# EN: Change this one line to run the whole notebook on your own country. | FR: Changez cette seule ligne pour exécuter tout le carnet sur votre pays.
COUNTRY_ISO3 = "{{ISO3}}"

from stg17 import countries, llm  # noqa: E402

C = countries.get(COUNTRY_ISO3)
OUT = S.outputs(C.iso3, "d1_rag")
print(f"{C.name_en} / {C.name_fr}  ({C.iso3})  ->  {OUT}")

ui.status_table(
    llm.status(),
    title=T("Model providers on this machine", "Fournisseurs de modèles sur cette machine"),
    note=T("You need exactly one. If all are unavailable, steps 1-4 and 8-9 still run: "
           "they are the retrieval half, and retrieval is where most RAG problems live.",
           "Un seul suffit. Si aucun n'est disponible, les étapes 1 à 4 et 8 à 9 "
           "fonctionnent quand même : c'est la moitié « récupération », et c'est là que "
           "vivent la plupart des problèmes du RAG."),
)

# %% [markdown]
'''
<!--EN-->
---
## 2 · The corpus

Two ways to proceed, and the second is not a consolation prize:

**Your own documents.** Put PDFs, Word exports or text files in a folder and set
`CORPUS_DIR` to it. This is the real exercise — your assistant is only as good as
what you feed it.

**The sample corpus.** Five short fictional publications in the shapes an office
actually produces: a census report, a methodological note, a survey bulletin, a
summary of confidentiality provisions, a dissemination calendar. Every figure in
them is invented and every file says so on its first line.

> **Why the sample is deliberately fictional.** A convincing sample corpus is the
> fastest route from a teaching exercise to an invented number in a real
> publication. If yours reads like your own statistics, someone will eventually
> quote it.
<!--FR-->
---
## 2 · Le corpus

Deux façons de procéder, et la seconde n'est pas un lot de consolation :

**Vos propres documents.** Placez des PDF, des exports Word ou des fichiers texte
dans un dossier et indiquez-le dans `CORPUS_DIR`. C'est l'exercice réel — votre
assistant ne vaut que ce que vous lui donnez.

**Le corpus d'exemple.** Cinq courtes publications fictives dans les formes qu'un
office produit réellement : un rapport de recensement, une note méthodologique,
un bulletin d'enquête, un résumé des dispositions de confidentialité, un
calendrier de diffusion. Chaque chiffre y est inventé et chaque fichier le
déclare dès sa première ligne.

> **Pourquoi l'exemple est délibérément fictif.** Un corpus d'exemple convaincant
> est le chemin le plus court entre un exercice pédagogique et un chiffre inventé
> dans une vraie publication. S'il ressemble à vos propres statistiques,
> quelqu'un finira par le citer.
'''

# %%
# EN: Set this to a folder of your own documents, or leave it None for the sample. | FR: Indiquez un dossier de vos propres documents, ou laissez None pour l'exemple.
CORPUS_DIR = None

if CORPUS_DIR is None:
    CORPUS_DIR = rag.write_sample_corpus(S.path("corpus", "sample"))
    print(T(f"Using the fictional sample corpus at {CORPUS_DIR}",
            f"Corpus d'exemple fictif utilisé : {CORPUS_DIR}"))

docs = rag.load_corpus(CORPUS_DIR)

import pandas as pd  # noqa: E402

ui.result_table(
    pd.DataFrame([{"title": d.title, "words": d.words, "source": d.source} for d in docs]),
    caption=T("Every document your assistant can see. A file missing here is a file "
              "your assistant will never mention — and it will not tell you that.",
              "Tous les documents que votre assistant peut voir. Un fichier absent ici "
              "est un fichier que votre assistant ne mentionnera jamais — et il ne vous "
              "le dira pas."),
)

# %% [markdown]
'''
<!--EN-->
### The failure that is hardest to diagnose

A scanned PDF is an image. It has no text layer, `load_corpus` extracts nothing
from it, and it is reported and skipped. Without that report, the symptom is an
assistant that calmly does not know about a report sitting in its folder.

If your own documents are scans, they need OCR before this laboratory can use
them — and that is a Day 3 conversation, not a Day 1 one.
<!--FR-->
### L'échec le plus difficile à diagnostiquer

Un PDF scanné est une image. Il n'a pas de couche texte, `load_corpus` n'en
extrait rien, et il est signalé puis ignoré. Sans ce signalement, le symptôme est
un assistant qui ignore paisiblement un rapport présent dans son dossier.

Si vos propres documents sont des scans, ils exigent de l'OCR avant que ce
laboratoire puisse les utiliser — et c'est une discussion du Jour 3, pas du Jour 1.
'''

# %% [markdown]
'''
<!--EN-->
---
## 3 · Cutting documents into passages

The model is never given a whole document. It is given a few passages, so the
passage boundary decides what it can see at once.

Two numbers control this:

- **`size`** — how long a passage is, in characters. Too small and the answer is
  split across two passages, only one of which is retrieved. Too large and the
  passage carries three topics, so the retriever cannot tell which one you asked
  about.
- **`overlap`** — how much of the previous passage is repeated at the start of the
  next. It exists because the sentence that answers a question is often the one
  that straddles a boundary.

Run the cell, then **change the numbers and run it again**. Watch the passage
count and read one passage each time. There is no correct value — there is a
value that suits your documents, and you find it by looking.
<!--FR-->
---
## 3 · Découper les documents en passages

Le modèle ne reçoit jamais un document entier. Il reçoit quelques passages : la
frontière de passage décide donc de ce qu'il peut voir d'un coup.

Deux nombres commandent cela :

- **`size`** — la longueur d'un passage, en caractères. Trop petit, la réponse est
  scindée entre deux passages dont un seul est récupéré. Trop grand, le passage
  porte trois sujets et le récupérateur ne sait plus lequel vous intéressait.
- **`overlap`** — la part du passage précédent répétée au début du suivant. Il
  existe parce que la phrase qui répond à une question est souvent celle qui
  chevauche une frontière.

Exécutez la cellule, puis **changez les nombres et ré-exécutez**. Observez le
nombre de passages et lisez-en un à chaque fois. Il n'y a pas de bonne valeur — il
y a une valeur adaptée à vos documents, et on la trouve en regardant.
'''

# %%
# <solution hint="Chunk the documents with rag.chunk_documents, then print the count and one passage" hint_fr="Découpez les documents avec rag.chunk_documents, puis affichez le nombre et un passage">
CHUNK_SIZE = 900
CHUNK_OVERLAP = 150

chunks = rag.chunk_documents(docs, size=CHUNK_SIZE, overlap=CHUNK_OVERLAP)

print(T(f"{len(docs)} document(s) -> {len(chunks)} passage(s)",
        f"{len(docs)} document(s) -> {len(chunks)} passage(s)"))
print("-" * 70)
print(chunks[0].citation)
print("-" * 70)
print(chunks[0].text[:600])
# </solution>

# %% [markdown]
'''
<!--EN-->
---
## 4 · Two retrievers, and how each one fails

This is the step that repays the most attention.

**TF-IDF** matches words. It needs no download and works on any network. Ask it
about "population" and it finds paragraphs containing "population". Ask it "how
many people live there" and it may find nothing at all, because those words do
not appear.

**Embeddings** match meaning. A model turns each passage into a vector, and
"how many people live there" lands near a paragraph about population even with no
shared word. It costs a one-off download of about 90 MB.

They fail in opposite ways, and the difference matters:

- TF-IDF returns **nothing** when the words do not match. Honest, and easy to detect.
- Embeddings return **the nearest passage**, always — even when nothing in your
  corpus is close. Confident, and invisible without a score threshold.

The cell below builds both and asks them the same questions.
<!--FR-->
---
## 4 · Deux récupérateurs, et la manière dont chacun échoue

C'est l'étape qui récompense le plus l'attention.

**TF-IDF** apparie des mots. Il n'exige aucun téléchargement et fonctionne sur
tout réseau. Interrogez-le sur « population » et il trouve les paragraphes
contenant « population ». Demandez-lui « combien de personnes y vivent » et il
peut ne rien trouver, car ces mots n'y figurent pas.

**Les embeddings** apparient du sens. Un modèle transforme chaque passage en
vecteur, et « combien de personnes y vivent » se place près d'un paragraphe sur la
population, même sans mot commun. Coût : un téléchargement unique d'environ 90 Mo.

Ils échouent en sens inverse, et la différence compte :

- TF-IDF ne renvoie **rien** quand les mots ne correspondent pas. Honnête, et facile à détecter.
- Les embeddings renvoient **le passage le plus proche**, toujours — même quand
  rien dans votre corpus n'en approche. Assuré, et invisible sans seuil de score.

La cellule ci-dessous construit les deux et leur pose les mêmes questions.
'''

# %%
# EN: TF-IDF always works. Embeddings are attempted and reported honestly if unavailable. | FR: TF-IDF fonctionne toujours. Les embeddings sont tentés, et leur absence est signalée honnêtement.
tfidf = rag.build_index(chunks, kind="tfidf")

try:
    S.installed += env.ensure({"sentence-transformers": "sentence-transformers>=2.2"})
    dense = rag.build_index(chunks, kind="embedding")
except Exception as exc:  # noqa: BLE001
    dense = None
    print(T(f"Embedding retriever unavailable ({type(exc).__name__}). The laboratory "
            f"continues on TF-IDF; the comparison below will show one column only.",
            f"Récupérateur sémantique indisponible ({type(exc).__name__}). Le laboratoire "
            f"continue en TF-IDF ; la comparaison ci-dessous n'aura qu'une colonne."))

# %%
# <solution hint="For each probe question, print the top passage from each retriever side by side" hint_fr="Pour chaque question test, affichez le meilleur passage de chaque récupérateur côte à côte">
PROBES = [
    T("What was the unemployment rate?", "Quel était le taux de chômage ?"),
    T("How many people live in the country?", "Combien de personnes vivent dans le pays ?"),
    T("Can individual data be sent to another country?",
      "Les données individuelles peuvent-elles être envoyées dans un autre pays ?"),
]

rows = []
for question in PROBES:
    row = {"question": question}
    hit = tfidf.search(question, k=1)
    row["tfidf"] = f"{hit[0].chunk.title} ({hit[0].score:.2f})" if hit else "— nothing —"
    if dense is not None:
        hit = dense.search(question, k=1)
        row["embeddings"] = f"{hit[0].chunk.title} ({hit[0].score:.2f})" if hit else "—"
    rows.append(row)

ui.result_table(
    pd.DataFrame(rows),
    caption=T("The second question is the interesting one: it asks about population "
              "without using the word.",
              "La deuxième question est la plus instructive : elle porte sur la "
              "population sans employer le mot."),
)
# </solution>

# %% [markdown]
'''
<!--EN-->
> **Which should you use?** Embeddings, where you can. But an office on a
> constrained network running TF-IDF with a well-written question set gets a
> working assistant, and a working assistant beats a planned one. Note in your
> documentation which retriever produced your results — they are not
> interchangeable, and a reader cannot tell from the output.
<!--FR-->
> **Lequel utiliser ?** Les embeddings, quand c'est possible. Mais un office sur
> un réseau contraint qui exécute TF-IDF avec un bon jeu de questions obtient un
> assistant qui fonctionne, et un assistant qui fonctionne vaut mieux qu'un
> assistant prévu. Consignez dans votre documentation quel récupérateur a produit
> vos résultats — ils ne sont pas interchangeables, et un lecteur ne peut pas le
> deviner à la sortie.
'''

# %% [markdown]
'''
<!--EN-->
---
## 5 · The prompt that forbids invention

Retrieval is half the system. The other half is an instruction strict enough that
the model does not fall back on its own memory when the passages are unhelpful.

The rule that does the work is the first one: when the passages do not contain
the answer, reply with a fixed refusal string and nothing else. A fixed string,
not a polite sentence, because the notebook needs to *detect* the refusal in
order to count it.
<!--FR-->
---
## 5 · Le prompt qui interdit l'invention

La récupération est la moitié du système. L'autre moitié est une instruction
assez stricte pour que le modèle ne se rabatte pas sur sa mémoire quand les
passages sont inutiles.

La règle décisive est la première : si les passages ne contiennent pas la
réponse, répondre par une chaîne de refus fixe et rien d'autre. Une chaîne fixe,
et non une phrase polie, car le carnet doit *détecter* le refus pour le compter.
'''

# %%
# EN: Read this. It is short, and every line of it is load-bearing. | FR: Lisez ceci. C'est court, et chaque ligne y est porteuse.
print(rag.SYSTEM)
print("\n" + "=" * 70)
print(T("The refusal string the notebook looks for:", "La chaîne de refus recherchée :"),
      rag.REFUSAL)

# %%
# EN: What the model actually receives — the passages first, the question last. | FR: Ce que le modèle reçoit réellement — les passages d'abord, la question ensuite.
index = dense if dense is not None else tfidf
preview = rag.build_prompt(PROBES[0], index.search(PROBES[0], k=2))
print(preview[:900] + ("\n...[truncated]" if len(preview) > 900 else ""))

# %% [markdown]
'''
<!--EN-->
---
## 6 · Ask, and read the citation

Now the three steps run together. Read the answer, then read the passages beneath
it and check that the answer is actually in them.

Do that check by hand at least three times before you trust the pipeline. It is
the only way to develop a feel for when it is working.
<!--FR-->
---
## 6 · Interroger, et lire la citation

Les trois étapes s'enchaînent maintenant. Lisez la réponse, puis lisez les
passages en dessous et vérifiez que la réponse s'y trouve réellement.

Faites cette vérification à la main au moins trois fois avant de faire confiance à
la chaîne. C'est le seul moyen d'acquérir le sens de ce qui fonctionne.
'''

# %%
# <solution hint="Call rag.answer() and display the answer with its passages" hint_fr="Appelez rag.answer() et affichez la réponse avec ses passages">
QUESTION = T("What was the unemployment rate, and for which quarter?",
             "Quel était le taux de chômage, et pour quel trimestre ?")

try:
    result = rag.answer(QUESTION, index, k=3)
    print(result.text)
    print("\n" + "-" * 70)
    for i, hit in enumerate(result.hits, start=1):
        print(f"[{i}] {hit.chunk.citation}   score={hit.score:.3f}")
        print(f"    {hit.chunk.text[:200].strip()}...")
    print("-" * 70)
    print(f"{result.provider} / {result.model} · {result.latency_s:.1f}s")
except Exception as exc:  # noqa: BLE001
    result = None
    print(T(f"No model provider available ({exc}). Steps 6 and 7 need one; step 8 "
            f"onwards does not. Continue and come back to these two.",
            f"Aucun fournisseur de modèle ({exc}). Les étapes 6 et 7 en exigent un ; "
            f"la 8 et les suivantes non. Poursuivez et revenez à ces deux étapes."))
# </solution>

# %% [markdown]
'''
<!--EN-->
---
## 7 · The refusal test

This is the step most first builds skip, and it is the one that decides whether
the assistant is publishable.

Ask questions your corpus **cannot** answer. A correct system refuses. An
incorrect one produces a fluent, plausible, unsourced answer — and it will do
that in front of a journalist just as readily as it does here.
<!--FR-->
---
## 7 · Le test de refus

C'est l'étape que la plupart des premières versions sautent, et c'est elle qui
décide si l'assistant est publiable.

Posez des questions auxquelles votre corpus **ne peut pas** répondre. Un système
correct refuse. Un système incorrect produit une réponse fluide, plausible et
sans source — et il le fera devant un journaliste aussi volontiers qu'ici.
'''

# %%
# EN: Questions with no answer in the corpus. Every one should be refused. | FR: Questions sans réponse dans le corpus. Chacune devrait être refusée.
UNANSWERABLE = [
    T("What is the current price of maize per kilogram?",
      "Quel est le prix actuel du maïs au kilogramme ?"),
    T("How many hospitals are there in the northern region?",
      "Combien d'hôpitaux compte la région du nord ?"),
    T("What will the population be in 2050?",
      "Quelle sera la population en 2050 ?"),
]

checks = []
if result is not None:
    for question in UNANSWERABLE:
        a = rag.answer(question, index, k=3)
        checks.append({"question": question,
                       "refused": a.refused,
                       "reply": a.text[:90].replace("\n", " ")})
    ui.result_table(
        pd.DataFrame(checks),
        caption=T("Every row should say refused = True. A False is not a small defect: "
                  "it is the system inventing an answer with a source line attached.",
                  "Chaque ligne devrait indiquer refused = True. Un False n'est pas un "
                  "défaut mineur : c'est le système qui invente une réponse en y "
                  "attachant une ligne de source."),
    )
else:
    print(T("Skipped — needs a model provider.", "Ignoré — exige un fournisseur de modèle."))

# %% [markdown]
'''
<!--EN-->
> **If a row says False.** Do not conclude the model is bad. Look at the passages
> it was given: with an embedding retriever it received the *nearest* passage
> regardless of how far away it was, and something vaguely related is much harder
> to refuse than something obviously irrelevant. That is what step 8 fixes.
<!--FR-->
> **Si une ligne indique False.** N'en concluez pas que le modèle est mauvais.
> Regardez les passages qu'il a reçus : avec un récupérateur sémantique, il a reçu
> le passage *le plus proche* quelle que soit la distance, et un contenu vaguement
> apparenté est bien plus difficile à refuser qu'un contenu manifestement hors
> sujet. C'est ce que corrige l'étape 8.
'''

# %% [markdown]
'''
<!--EN-->
---
## 8 · Calibrate the score floor

Every retrieved passage carries a similarity score. Questions your corpus answers
score higher than questions it does not — but the two ranges overlap, and where
they separate depends on your documents.

Find the floor by measuring, not by guessing: score a set of answerable questions
and a set of unanswerable ones, and put the threshold between the distributions.

Too low and irrelevant passages reach the model, which then struggles to refuse.
Too high and real questions get refused. There is no universal value.
<!--FR-->
---
## 8 · Calibrer le seuil de score

Chaque passage récupéré porte un score de similarité. Les questions auxquelles
votre corpus répond obtiennent un score plus élevé que les autres — mais les deux
plages se chevauchent, et l'endroit où elles se séparent dépend de vos documents.

Trouvez le seuil en mesurant, pas en devinant : notez un ensemble de questions
avec réponse et un ensemble sans réponse, et placez le seuil entre les
distributions.

Trop bas, des passages hors sujet atteignent le modèle, qui peine alors à
refuser. Trop haut, de vraies questions sont refusées. Aucune valeur universelle.
'''

# %%
# <solution hint="Score the answerable and unanswerable questions, and compare their top scores" hint_fr="Notez les questions avec et sans réponse, et comparez leurs meilleurs scores">
ANSWERABLE = [
    T("What was the unemployment rate?", "Quel était le taux de chômage ?"),
    T("How was non-response handled?", "Comment la non-réponse a-t-elle été traitée ?"),
    T("When is the consumer price index released?",
      "Quand l'indice des prix à la consommation est-il publié ?"),
]

scored = []
for question, answerable in [(q, True) for q in ANSWERABLE] + [(q, False) for q in UNANSWERABLE]:
    hits = index.search(question, k=1)
    scored.append({"question": question[:52],
                   "answerable": answerable,
                   "top_score": round(hits[0].score, 3) if hits else 0.0})

table = pd.DataFrame(scored).sort_values("top_score", ascending=False)
ui.result_table(table, caption=T(
    "Put MIN_SCORE between the lowest answerable score and the highest unanswerable one. "
    "If those overlap, your corpus does not separate cleanly — say so in your documentation.",
    "Placez MIN_SCORE entre le plus bas score avec réponse et le plus haut sans réponse. "
    "S'ils se chevauchent, votre corpus ne se sépare pas nettement — dites-le dans votre "
    "documentation."))

lo = table.loc[table.answerable, "top_score"].min()
hi = table.loc[~table.answerable, "top_score"].max()
MIN_SCORE = round((lo + hi) / 2, 3) if lo > hi else 0.0
print(T(f"answerable floor {lo} · unanswerable ceiling {hi} · MIN_SCORE = {MIN_SCORE}",
        f"plancher avec réponse {lo} · plafond sans réponse {hi} · MIN_SCORE = {MIN_SCORE}"))
if MIN_SCORE == 0.0:
    print(T(f"The distributions overlap: an unanswerable question scored {hi}, above an "
            f"answerable one at {lo}. No threshold separates them here.\n"
            f"That is a finding, not a failure — and with retriever '{index.kind}' it is "
            f"the expected one. TF-IDF scores by shared words, so an off-topic question "
            f"that happens to share vocabulary outranks an on-topic one phrased "
            f"differently. Embeddings usually separate more cleanly. Report which "
            f"retriever you used alongside the threshold.",
            f"Les distributions se chevauchent : une question sans réponse a obtenu {hi}, "
            f"au-dessus d'une question avec réponse à {lo}. Aucun seuil ne les sépare ici.\n"
            f"C'est un constat, pas un échec — et avec le récupérateur « {index.kind} » "
            f"c'est le constat attendu. TF-IDF note selon les mots partagés : une question "
            f"hors sujet qui partage du vocabulaire devance une question pertinente "
            f"formulée autrement. Les embeddings séparent en général plus nettement. "
            f"Indiquez le récupérateur utilisé à côté du seuil."))
# </solution>

# %% [markdown]
'''
<!--EN-->
---
## 9 · Evaluate, then save the evidence

Two different things can go wrong, and from the answer alone they look identical:

- **Retrieval failed** — the right paragraph never reached the model. No prompt
  fixes this. Change the chunking, the retriever, or the question.
- **Generation failed** — the right paragraph reached the model and the answer is
  still wrong. Now the prompt is the place to work.

`evaluate_retrieval` measures the first, so you know which half to fix.
<!--FR-->
---
## 9 · Évaluer, puis conserver les preuves

Deux choses différentes peuvent échouer, et depuis la réponse seule elles se
ressemblent :

- **La récupération a échoué** — le bon paragraphe n'a jamais atteint le modèle.
  Aucun prompt ne corrige cela. Changez le découpage, le récupérateur, ou la
  question.
- **La génération a échoué** — le bon paragraphe est arrivé et la réponse est
  quand même fausse. C'est alors sur le prompt qu'il faut travailler.

`evaluate_retrieval` mesure la première, pour que vous sachiez quelle moitié
corriger.
'''

# %%
# EN: Which document SHOULD answer each question? That is the whole evaluation set. | FR: Quel document DEVRAIT répondre à chaque question ? C'est tout le jeu d'évaluation.
CASES = [
    {"question": ANSWERABLE[0], "expect": "labour"},
    {"question": ANSWERABLE[1], "expect": "methodology"},
    {"question": ANSWERABLE[2], "expect": "dissemination"},
    {"question": UNANSWERABLE[0], "expect": None},
]

report = rag.evaluate_retrieval(index, CASES, k=3)
ui.result_table(report, caption=T(
    "hit = the expected document reached the model. A False here means no prompt "
    "change will help.",
    "hit = le document attendu a atteint le modèle. Un False ici signifie qu'aucune "
    "modification du prompt n'y changera rien."))

rate = report["hit"].mean()
print(T(f"Retrieval hit rate: {rate:.0%} on {len(report)} case(s).",
        f"Taux de récupération correcte : {rate:.0%} sur {len(report)} cas."))

# %%
# EN: The deliverable: answers, their passages and their provenance, on disk. | FR: Le livrable : réponses, passages et provenance, sur disque.
transcript = []
if result is not None:
    for question in ANSWERABLE:
        transcript.append(rag.answer(question, index, k=3, min_score=MIN_SCORE))

path = rag.save_transcript(
    transcript,
    OUT / "rag_transcript.json",
    meta={
        "country": C.iso3,
        "corpus": str(CORPUS_DIR),
        "documents": len(docs),
        "passages": len(chunks),
        "chunk_size": CHUNK_SIZE,
        "chunk_overlap": CHUNK_OVERLAP,
        "retriever": index.kind,
        "min_score": MIN_SCORE,
        "retrieval_hit_rate": round(float(rate), 3),
    },
)
report.to_csv(OUT / "rag_retrieval_eval.csv", index=False)
print(T(f"Written: {path.name} and rag_retrieval_eval.csv in {OUT}",
        f"Écrits : {path.name} et rag_retrieval_eval.csv dans {OUT}"))

# %% [markdown]
'''
<!--EN-->
---
### What you have

<table>
<tr><td><b>rag_transcript.json</b></td><td>Every answer with the exact passages behind it,
the retriever used, the chunk parameters and the score floor.</td></tr>
<tr><td><b>rag_retrieval_eval.csv</b></td><td>Which questions retrieved the right document,
and which did not.</td></tr>
</table>

Both go into your country repository on Friday. An answer without the passage it
came from cannot be checked by anyone else, and an assistant whose outputs nobody
can audit is not one a statistical office can stand behind.

### The limits of what you built

- It answers from **your documents only**. A question about anything else is
  correctly refused, and that is a feature.
- Retrieval quality is bounded by chunking. A figure split across two passages
  may never be retrieved whole.
- The score floor was calibrated on a handful of questions. Twenty would be
  better; a hundred would be defensible.
- **Nothing here validates the answer against the source.** It cites a passage;
  it does not prove the answer is in it. A human still reads before publication.

### Checkpoint

| Question | Answer |
|---|---|
| Where does the refusal rule live? | In the system prompt — rule 1 |
| A wrong answer with the right passage attached: what do you fix? | The prompt |
| A wrong answer with an irrelevant passage: what do you fix? | The retrieval — chunking, retriever, or score floor |
| Why is "not in my documents" a good answer? | Because the alternative is a fluent invention with a citation attached |
<!--FR-->
---
### Ce que vous avez

<table>
<tr><td><b>rag_transcript.json</b></td><td>Chaque réponse avec les passages exacts qui la
fondent, le récupérateur utilisé, les paramètres de découpage et le seuil de score.</td></tr>
<tr><td><b>rag_retrieval_eval.csv</b></td><td>Quelles questions ont récupéré le bon document,
et lesquelles non.</td></tr>
</table>

Les deux rejoignent le dépôt de votre pays vendredi. Une réponse sans le passage
dont elle vient ne peut être vérifiée par personne d'autre, et un assistant dont
personne ne peut auditer les sorties n'est pas un assistant qu'un office
statistique peut assumer.

### Les limites de ce que vous avez construit

- Il répond **à partir de vos documents seulement**. Une question sur autre chose
  est correctement refusée, et c'est une qualité.
- La qualité de récupération est bornée par le découpage. Un chiffre scindé entre
  deux passages peut ne jamais être récupéré entier.
- Le seuil de score a été calibré sur une poignée de questions. Vingt seraient
  mieux ; cent seraient défendables.
- **Rien ici ne valide la réponse contre la source.** Il cite un passage ; il ne
  prouve pas que la réponse s'y trouve. Un humain lit encore avant publication.

### Point de contrôle

| Question | Réponse |
|---|---|
| Où vit la règle de refus ? | Dans le prompt système — règle 1 |
| Réponse fausse avec le bon passage : que corrigez-vous ? | Le prompt |
| Réponse fausse avec un passage hors sujet : que corrigez-vous ? | La récupération — découpage, récupérateur ou seuil |
| Pourquoi « absent de mes documents » est-il une bonne réponse ? | Parce que l'alternative est une invention fluide accompagnée d'une citation |
'''

# %% [markdown] tags=only-open
'''
<!--EN-->
---
## Your turn

Four extensions, in increasing order of difficulty. The first two are worth doing
before Friday.

1. **Use your own documents.** Point `CORPUS_DIR` at real publications from your
   office and rerun. Then write the twenty-question evaluation set that matters to
   your users, not to this notebook.
2. **Move the chunk size.** Halve it, double it, and record the retrieval hit rate
   each time. Put the three numbers in your Friday repository — that table is a
   methodological finding.
3. **Make the citation clickable.** Add a page number to `Chunk` when the source is
   a PDF, so an answer points at a page rather than a passage index.
4. **Retrieve twice.** Retrieve with TF-IDF and with embeddings, merge the results,
   and deduplicate. Measure whether the hit rate improves enough to justify running
   both.

Tomorrow at 15:45 this assistant becomes an agent: the model stops receiving
passages you chose and starts choosing which tool to call. Everything you learned
about refusal applies there too, with higher stakes — a wrong sentence becomes a
wrong action.
<!--FR-->
---
## À vous

Quatre extensions, par difficulté croissante. Les deux premières méritent d'être
faites avant vendredi.

1. **Utilisez vos propres documents.** Pointez `CORPUS_DIR` vers de vraies
   publications de votre office et ré-exécutez. Puis rédigez le jeu d'évaluation de
   vingt questions qui compte pour vos utilisateurs, pas pour ce carnet.
2. **Faites bouger la taille des passages.** Divisez-la par deux, multipliez-la par
   deux, et notez le taux de récupération à chaque fois. Mettez les trois nombres
   dans votre dépôt de vendredi — ce tableau est un constat méthodologique.
3. **Rendez la citation cliquable.** Ajoutez un numéro de page à `Chunk` quand la
   source est un PDF, pour qu'une réponse pointe vers une page plutôt que vers un
   indice de passage.
4. **Récupérez deux fois.** Récupérez avec TF-IDF et avec les embeddings, fusionnez
   et dédoublonnez. Mesurez si le taux s'améliore assez pour justifier d'exécuter
   les deux.

Demain à 15h45, cet assistant devient un agent : le modèle cesse de recevoir des
passages que vous avez choisis et se met à choisir quel outil appeler. Tout ce que
vous avez appris sur le refus s'y applique aussi, avec des enjeux plus élevés — une
phrase fausse devient une action fausse.
'''

# %% [markdown]
'''
<!--EN-->
---
> ### If something did not work
>
> **No model provider.** Steps 1–4 and 8–9 run without one, and they are the
> retrieval half — where most RAG problems actually live. Set one API key before
> Day 2 and rerun steps 5–7.
>
> **The embedding download failed.** TF-IDF is a legitimate retriever, not a
> degraded mode. Record which one you used and carry on.
>
> **Your PDFs produced nothing.** They are scans. They need OCR, which is outside
> this laboratory. Use the sample corpus today and bring the question to Day 3.
>
> **Everything is refused.** `MIN_SCORE` is too high. Set it to `0.0` and rerun
> step 8 with more questions.
<!--FR-->
---
> ### Si quelque chose n'a pas fonctionné
>
> **Aucun fournisseur de modèle.** Les étapes 1 à 4 et 8 à 9 fonctionnent sans, et
> ce sont celles de la récupération — là où vivent la plupart des problèmes du RAG.
> Définissez une clé API avant le Jour 2 et ré-exécutez les étapes 5 à 7.
>
> **Le téléchargement des embeddings a échoué.** TF-IDF est un récupérateur
> légitime, pas un mode dégradé. Notez lequel vous avez utilisé et poursuivez.
>
> **Vos PDF n'ont rien donné.** Ce sont des scans. Ils exigent de l'OCR, hors du
> périmètre de ce laboratoire. Utilisez le corpus d'exemple aujourd'hui et
> apportez la question au Jour 3.
>
> **Tout est refusé.** `MIN_SCORE` est trop élevé. Mettez-le à `0.0` et
> ré-exécutez l'étape 8 avec davantage de questions.
'''
