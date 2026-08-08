# %% [meta]
'''
id: d1_agent
day: 1
title_en: From RAG to Agent - Where the Human Belongs
title_fr: Du RAG à l'agent - Où se place l'humain
outdir: notebooks/day1
stem: D1_Agent
country: CIV
tracks: guided, open
'''

# %% [markdown]
'''
<!--EN-->
<div style="background:linear-gradient(135deg,#0B2545 0%,#1B7A43 100%);
 border-radius:18px;padding:32px 38px;font-family:'Segoe UI',system-ui,sans-serif;margin-bottom:6px;">
 <div style="color:#F2A900;font-size:12.5px;letter-spacing:3px;font-weight:700;
  text-transform:uppercase;">African Development Bank · AU STATAFRIC · STG17 · Day 1 · 15:45</div>
 <div style="color:#fff;font-size:2em;font-weight:800;margin:10px 0 8px;line-height:1.15;">
  From RAG to agent</div>
 <div style="color:#dbe7e0;font-size:1.05em;line-height:1.55;max-width:900px;">
  This morning the model was handed passages you chose. Now it chooses which tool to call.
  One thing does not change: <b>the model asks, your code runs</b> — and everything your office
  needs to control lives in that gap.
 </div>
 <div style="color:#F2A900;font-size:13px;margin-top:14px;font-weight:600;">
  75 minutes · the core steps run with no API key at all</div>
</div>

> **Why an agent is a different risk.** An assistant that is wrong produces a wrong
> sentence, and a human reads it before it goes anywhere. An agent that is wrong
> takes a wrong **action**. The failure has already happened by the time anyone
> reads the output.
<!--FR-->
<div style="background:linear-gradient(135deg,#0B2545 0%,#1B7A43 100%);
 border-radius:18px;padding:32px 38px;font-family:'Segoe UI',system-ui,sans-serif;margin-bottom:6px;">
 <div style="color:#F2A900;font-size:12.5px;letter-spacing:3px;font-weight:700;
  text-transform:uppercase;">Banque africaine de développement · UA STATAFRIC · STG17 · Jour 1 · 15h45</div>
 <div style="color:#fff;font-size:2em;font-weight:800;margin:10px 0 8px;line-height:1.15;">
  Du RAG à l'agent</div>
 <div style="color:#dbe7e0;font-size:1.05em;line-height:1.55;max-width:900px;">
  Ce matin, le modèle recevait des passages que vous aviez choisis. Il choisit maintenant quel
  outil appeler. Une chose ne change pas : <b>le modèle demande, votre code exécute</b> — et tout
  ce que votre office doit contrôler vit dans cet interstice.
 </div>
 <div style="color:#F2A900;font-size:13px;margin-top:14px;font-weight:600;">
  75 minutes · les étapes centrales fonctionnent sans aucune clé API</div>
</div>

> **Pourquoi un agent est un risque différent.** Un assistant qui se trompe produit
> une phrase fausse, et un humain la lit avant qu'elle n'aille où que ce soit. Un
> agent qui se trompe accomplit une **action** fausse. L'échec a déjà eu lieu quand
> quelqu'un lit la sortie.
'''

# %% [markdown]
'''
<!--EN-->
### The road through this laboratory

| # | Step | What you learn |
|---|------|----------------|
| 1 | The toolbox | What a tool is, and why `writes` is a field and not a comment |
| 2 | The protocol | How a model asks for something it cannot execute |
| 3 | **The gap** | The twenty lines where your office's policy lives |
| 4 | The loop, with no model | Every failure mode, reproducibly, with no API key |
| 5 | The loop, for real | The same code, driven by an actual model |
| 6 | The write tool | Refuse it, then approve it, and watch the disk |
| 7 | The budget | Why `max_steps` is a cost control, not a safety net |
| 8 | The audit log | What you show when someone asks what happened |

**Requirements.** The `stg17` toolkit and `scikit-learn`. **Steps 1–4 and 6–8 need
no model provider** — they exercise the part your office writes and owns. Step 5
needs one.

> This is deliberate. The loop, the gate, the error handling and the log are
> yours. The model is rented. Building yours first, and testing it without the
> rented part, is the whole methodological point of this session.
<!--FR-->
### Le parcours de ce laboratoire

| # | Étape | Ce que vous apprenez |
|---|-------|----------------------|
| 1 | La boîte à outils | Ce qu'est un outil, et pourquoi `writes` est un champ et non un commentaire |
| 2 | Le protocole | Comment un modèle demande une chose qu'il ne peut pas exécuter |
| 3 | **L'interstice** | Les vingt lignes où vit la politique de votre office |
| 4 | La boucle, sans modèle | Tous les modes d'échec, reproductibles, sans clé API |
| 5 | La boucle, pour de vrai | Le même code, piloté par un vrai modèle |
| 6 | L'outil d'écriture | Le refuser, puis l'approuver, et observer le disque |
| 7 | Le budget | Pourquoi `max_steps` est un contrôle de coût, pas un filet de sécurité |
| 8 | Le journal d'audit | Ce que vous montrez quand on demande ce qui s'est passé |

**Prérequis.** La boîte à outils `stg17` et `scikit-learn`. **Les étapes 1 à 4 et 6
à 8 n'exigent aucun fournisseur de modèle** — elles exercent la part que votre
office écrit et possède. L'étape 5 en exige un.

> C'est délibéré. La boucle, le contrôle, la gestion d'erreur et le journal sont à
> vous. Le modèle est loué. Construire la vôtre d'abord, et la tester sans la part
> louée, est tout l'enjeu méthodologique de cette session.
'''

# %%
# EN: The toolkit, and the retrieval index this morning's laboratory built. | FR: La boîte à outils, et l'index de récupération construit ce matin.
import subprocess
import sys

REPO = "https://github.com/{{ORG}}/{{REPO}}"

try:
    import stg17  # noqa: F401
except ImportError:
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", f"git+{REPO}.git"], check=False)

import pandas as pd  # noqa: E402
from stg17 import agent, countries, env, llm, rag, ui  # noqa: E402
from stg17.i18n import T  # noqa: E402

S = env.setup({"scikit-learn": "scikit-learn>=1.3", "pandas": "pandas>=2.0"}, lang="{{LANG_UPPER}}")

COUNTRY_ISO3 = "{{ISO3}}"
C = countries.get(COUNTRY_ISO3)
OUT = S.outputs(C.iso3, "d1_agent")

CORPUS_DIR = rag.write_sample_corpus(S.path("corpus", "sample"))
docs = rag.load_corpus(CORPUS_DIR)
index = rag.build_index(rag.chunk_documents(docs), kind="tfidf")
print(f"{C.name_en} ({C.iso3}) · {len(docs)} documents · -> {OUT}")

# %% [markdown]
'''
<!--EN-->
---
## 1 · The toolbox

A tool is a function you allow the model to ask for. Four of them here: three that
read, one that writes.

`writes` is a field on the tool, not a note in the documentation. A tool that only
reads can run without asking anyone. A tool that changes something — a file, a
record, an email, a payment — is a different kind of risk. Making that a typed
property means an office cannot forget which is which when it adds the fifth tool
six months from now.
<!--FR-->
---
## 1 · La boîte à outils

Un outil est une fonction que vous autorisez le modèle à demander. Quatre ici :
trois qui lisent, un qui écrit.

`writes` est un champ de l'outil, pas une note dans la documentation. Un outil qui
ne fait que lire peut s'exécuter sans demander à personne. Un outil qui modifie
quelque chose — un fichier, un enregistrement, un courriel, un paiement — est un
risque d'une autre nature. En faire une propriété typée fait qu'un office ne peut
pas oublier lequel est lequel en ajoutant le cinquième outil dans six mois.
'''

# %%
# EN: Three read tools and one write tool. Read the signatures the model will see. | FR: Trois outils de lecture et un d'écriture. Lisez les signatures que verra le modèle.
TOOLS = [
    agent.search_tool(index),
    agent.list_tool(docs),
    agent.calculator_tool(),
    agent.note_tool(OUT / "notes"),
]

print(agent.render_tools(TOOLS))

ui.result_table(
    pd.DataFrame([{"tool": t.name, "writes": t.writes,
                   "default policy": "refused" if t.writes else "runs"} for t in TOOLS]),
    caption=T("The default policy runs reads and refuses writes. You will change it in step 6.",
              "La politique par défaut exécute les lectures et refuse les écritures. "
              "Vous la changerez à l'étape 6."),
)

# %% [markdown]
'''
<!--EN-->
### Why a calculator, when the model can do arithmetic?

It cannot. A language model predicts the next token, so it predicts *digits* that
look right rather than computing them — and it is confidently wrong on numbers a
statistical office cares about.

Note the guard inside that tool: it accepts digits and operators and refuses
everything else. That is a whitelist, not a blacklist. Running `eval` on model
output with anything weaker is a remote code execution path, and "the model would
not do that" is not a security control.
<!--FR-->
### Pourquoi une calculatrice, si le modèle sait calculer ?

Il ne sait pas. Un modèle de langage prédit le token suivant : il prédit donc des
*chiffres* qui ont l'air justes plutôt que de calculer — et il se trompe avec
assurance sur des nombres qui comptent pour un office statistique.

Notez le garde-fou dans cet outil : il accepte les chiffres et les opérateurs et
refuse tout le reste. C'est une liste blanche, pas une liste noire. Exécuter
`eval` sur la sortie d'un modèle avec moins que cela est un chemin d'exécution de
code à distance, et « le modèle ne ferait pas ça » n'est pas un contrôle de
sécurité.
'''

# %%
# EN: The guard, demonstrated. Both of these are refused, not executed. | FR: Le garde-fou, démontré. Les deux sont refusés, pas exécutés.
calc = agent.calculator_tool()
for expression in ["19.2 - 8.6", "__import__('os').system('echo hello')"]:
    print(f"{expression[:44]:<46} -> {calc.run(expression=expression)[:60]}")

# %% [markdown]
'''
<!--EN-->
---
## 2 · The protocol — how a model asks

The model has no ability to run anything. It emits text. We agree on a shape for
that text, and our code reads it.

Read the system prompt below, then look at the last rule in particular: *never
state a figure that a tool has not returned to you*. That is this morning's
refusal rule, moved into a setting where the consequence is larger.
<!--FR-->
---
## 2 · Le protocole — comment un modèle demande

Le modèle n'a aucune capacité d'exécution. Il émet du texte. Nous convenons d'une
forme pour ce texte, et notre code la lit.

Lisez le prompt système ci-dessous, puis la dernière règle en particulier :
*n'énoncez jamais un chiffre qu'un outil ne vous a pas renvoyé*. C'est la règle de
refus de ce matin, déplacée dans un cadre où la conséquence est plus grande.
'''

# %%
# EN: What the model is told. The tool list is generated from TOOLS. | FR: Ce qui est dit au modèle. La liste d'outils est générée depuis TOOLS.
print(agent.SYSTEM.replace("<<TOOLS>>", agent.render_tools(TOOLS))[:1500])

# %%
# EN: Parsing is tolerant of what models actually do, and strict about the rest. | FR: L'analyse tolère ce que font réellement les modèles, et reste stricte sur le reste.
EXAMPLES = [
    '{"thought":"look it up","tool":"search_documents","args":{"query":"unemployment"}}',
    '```json\n{"tool":"calculate","args":{"expression":"2+2"}}\n```',
    'Certainly! {"answer":"8.6 per cent [search_documents]"} Let me know if...',
    'I will now search the documents for you.',
]
for text in EXAMPLES:
    try:
        action = agent.parse_action(text)
        what = f"answer: {action.answer[:34]}" if action.is_final else f"tool: {action.tool}"
        print(f"  OK      {text[:44]!r:<48} -> {what}")
    except agent.ProtocolError as exc:
        print(f"  REJECT  {text[:44]!r:<48} -> {exc}")

# %% [markdown]
'''
<!--EN-->
> **The last example is not a failure of the model.** It is a reply our code
> cannot act on, and the agent hands the error straight back so the model can
> correct itself. A system that crashes on a malformed reply will crash in
> production, because models produce them.
<!--FR-->
> **Le dernier exemple n'est pas un échec du modèle.** C'est une réponse sur
> laquelle notre code ne peut pas agir, et l'agent renvoie l'erreur au modèle pour
> qu'il se corrige. Un système qui plante sur une réponse malformée plantera en
> production, car les modèles en produisent.
'''

# %% [markdown]
'''
<!--EN-->
---
## 3 · The gap

Here is the whole of it, from `stg17/agent.py`:

```python
# The model has asked. Nothing has happened yet.
allowed = self.approve(tool, step.action.args)
step.approved = allowed
if not allowed:
    step.error = "refused by policy"
    transcript.append("TOOL RESULT: REFUSED — a human did not approve this call.")
    continue

result = tool.run(**step.action.args)
```

Four lines between the request and the execution. Every approval gate, audit
requirement and safety check your office needs goes there. There is nowhere else
it can go, and it cannot be added afterwards without changing this loop.

Three policies ship with the toolkit:

| Policy | Behaviour |
|---|---|
| `approve_reads_only` | Reads run. Writes are refused outright. **The default.** |
| `approve_interactive` | Reads run. A write asks a person, at the keyboard. |
| `approve_all` | Everything runs. Correct for a sample corpus; wrong for a record. |
<!--FR-->
---
## 3 · L'interstice

Le voici en entier, extrait de `stg17/agent.py` :

```python
# Le modèle a demandé. Rien ne s'est encore produit.
allowed = self.approve(tool, step.action.args)
step.approved = allowed
if not allowed:
    step.error = "refused by policy"
    transcript.append("TOOL RESULT: REFUSED — un humain n'a pas approuvé cet appel.")
    continue

result = tool.run(**step.action.args)
```

Quatre lignes entre la demande et l'exécution. Tout point d'approbation,
obligation d'audit et contrôle de sûreté de votre office s'y place. Il n'y a nulle
part ailleurs où le mettre, et cela ne s'ajoute pas après coup sans modifier cette
boucle.

Trois politiques sont fournies :

| Politique | Comportement |
|---|---|
| `approve_reads_only` | Les lectures s'exécutent. Les écritures sont refusées. **Par défaut.** |
| `approve_interactive` | Les lectures s'exécutent. Une écriture demande à une personne. |
| `approve_all` | Tout s'exécute. Correct sur un corpus d'exemple ; faux sur un enregistrement. |
'''

# %% [markdown]
'''
<!--EN-->
---
## 4 · The loop, driven by a script

`ScriptedModel` replays fixed replies and makes no decisions. That is exactly what
makes it useful: it lets you reproduce every failure mode on demand, and it needs
no API key.

The script below contains, deliberately, one of each thing that goes wrong: a
good call, a fenced reply, a tool that does not exist, an unparsable reply, a
refused write, and finally an answer.
<!--FR-->
---
## 4 · La boucle, pilotée par un script

`ScriptedModel` rejoue des réponses fixes et ne décide rien. C'est précisément ce
qui le rend utile : il permet de reproduire chaque mode d'échec à volonté, et
n'exige aucune clé API.

Le script ci-dessous contient délibérément un exemplaire de chaque chose qui
tourne mal : un bon appel, une réponse encadrée, un outil inexistant, une réponse
illisible, une écriture refusée, et enfin une réponse.
'''

# %%
# <solution hint="Run the agent with the scripted model and display its audit log" hint_fr="Exécutez l'agent avec le modèle scripté et affichez son journal d'audit">
SCRIPT = [
    '{"thought":"find the figure","tool":"search_documents","args":{"query":"unemployment rate"}}',
    '```json\n{"thought":"the gap between them","tool":"calculate","args":{"expression":"19.2 - 8.6"}}\n```',
    '{"thought":"try something that does not exist","tool":"lookup_table","args":{}}',
    'I will now write that down for you.',
    '{"thought":"save it","tool":"save_note","args":{"filename":"gap.md","text":"10.6 points"}}',
    '{"thought":"enough","answer":"Youth unemployment is 10.6 points above the overall '
    'rate [search_documents, calculate]. I could not save the note."}',
]

dry = agent.Agent(TOOLS, model=agent.ScriptedModel(SCRIPT), max_steps=8)
run = dry.run(T("How much higher is youth unemployment than the overall rate?",
                "De combien le chômage des jeunes dépasse-t-il le taux global ?"))

print("\n" + run.answer)
ui.result_table(run.audit(), caption=T(
    "Step 3 asked for a tool that does not exist. Step 4 could not be parsed. Step 5 was "
    "refused. None of the three stopped the agent — and all three are in the log.",
    "L'étape 3 a demandé un outil inexistant. L'étape 4 était illisible. L'étape 5 a été "
    "refusée. Aucune des trois n'a arrêté l'agent — et les trois sont dans le journal."))
# </solution>

# %%
# EN: Did the refused write actually not happen? Check the disk, not the log. | FR: L'écriture refusée n'a-t-elle vraiment pas eu lieu ? Vérifiez le disque, pas le journal.
notes = OUT / "notes"
print(T(f"note directory exists: {notes.exists()}",
        f"le répertoire de notes existe : {notes.exists()}"))

ui.key_concept(T(
    "A gate that logs a refusal and executes anyway is worse than no gate, because it "
    "produces a reassuring audit trail. Always verify the effect, not the record of it.",
    "Un contrôle qui journalise un refus et exécute quand même est pire que pas de "
    "contrôle, car il produit une trace d'audit rassurante. Vérifiez toujours l'effet, "
    "pas sa trace."))

# %% [markdown]
'''
<!--EN-->
---
## 5 · The loop, driven by an actual model

The same `Agent`, the same tools, the same gate. Only the source of the replies
changes.

If no provider is available, skip this and continue — you have already seen the
mechanism, and steps 6 to 8 do not need one.
<!--FR-->
---
## 5 · La boucle, pilotée par un vrai modèle

Le même `Agent`, les mêmes outils, le même contrôle. Seule la source des réponses
change.

Si aucun fournisseur n'est disponible, passez et poursuivez — vous avez déjà vu le
mécanisme, et les étapes 6 à 8 n'en ont pas besoin.
'''

# %%
# <solution hint="Run the same agent against a real provider and compare the audit log" hint_fr="Exécutez le même agent avec un vrai fournisseur et comparez le journal d'audit">
TASK = T("How many documents can you see, and what is the youth unemployment rate?",
         "Combien de documents voyez-vous, et quel est le taux de chômage des jeunes ?")

live = None
try:
    # Guarded twice on purpose: a provider can be reachable when the notebook
    # starts and gone by the time this cell runs. A laboratory must not end on
    # somebody else's outage.
    if llm.first_available() is None:
        raise llm.ProviderUnavailable(T("no provider configured", "aucun fournisseur configuré"))
    live = agent.Agent(TOOLS, max_steps=6).run(TASK)
    print("\n" + live.answer)
    ui.result_table(live.audit(), caption=T(
        "The model chose this sequence. You did not.",
        "Le modèle a choisi cette séquence. Vous, non."))
except Exception as exc:  # noqa: BLE001
    print(T(f"Step 5 skipped ({type(exc).__name__}: {exc}). Steps 6 to 8 continue — they "
            f"are the part your office writes, and they need no provider.",
            f"Étape 5 ignorée ({type(exc).__name__} : {exc}). Les étapes 6 à 8 se "
            f"poursuivent — c'est la part que votre office écrit, et elle n'exige aucun "
            f"fournisseur."))
# </solution>

# %% [markdown]
'''
<!--EN-->
---
## 6 · The write tool, allowed

Now change one argument. Nothing else about the agent changes — which is the
point: the policy is a parameter, not a rewrite.

`approve_interactive` would ask you at the keyboard. In a notebook that blocks on
input, so the cell below uses `approve_all` and then checks the disk. In your
office, the interactive one is the honest default until you have a written policy
saying otherwise.
<!--FR-->
---
## 6 · L'outil d'écriture, autorisé

Changez maintenant un seul argument. Rien d'autre ne change dans l'agent — c'est
l'essentiel : la politique est un paramètre, pas une réécriture.

`approve_interactive` vous interrogerait au clavier. Dans un carnet, cela bloque
sur une saisie ; la cellule ci-dessous utilise donc `approve_all` puis vérifie le
disque. Dans votre office, la version interactive est la valeur par défaut honnête
tant que vous n'avez pas de politique écrite disant le contraire.
'''

# %%
# EN: One argument changes. Watch both the log and the file system. | FR: Un seul argument change. Observez le journal et le système de fichiers.
allowed = agent.Agent(
    TOOLS,
    model=agent.ScriptedModel([
        '{"thought":"save the finding","tool":"save_note","args":'
        '{"filename":"finding.md","text":"Youth unemployment exceeds the overall rate '
        'by 10.6 points (Labour Force Survey 2023 Q4, fictional sample corpus)."}}',
        '{"thought":"done","answer":"Saved. [save_note]"}',
    ]),
    approve=agent.approve_all,
).run(T("Save the finding as a note.", "Enregistrez le constat dans une note."))

written = sorted((OUT / "notes").glob("*")) if (OUT / "notes").exists() else []
print(T(f"files now on disk: {[p.name for p in written]}",
        f"fichiers désormais sur disque : {[p.name for p in written]}"))
if written:
    print("-" * 60)
    print(written[0].read_text(encoding="utf-8"))

# %% [markdown]
'''
<!--EN-->
---
## 7 · The budget

An agent decides how many model calls to make. Without a cap, the cost of one
question is unbounded — and a loop that cannot terminate will not terminate on its
own.

`max_steps` is not a safety net. It is a budget, and it is the only reason you can
put a price on a question before you ask it.
<!--FR-->
---
## 7 · Le budget

Un agent décide combien d'appels au modèle il effectue. Sans plafond, le coût
d'une question est illimité — et une boucle incapable de se terminer ne se
terminera pas d'elle-même.

`max_steps` n'est pas un filet de sécurité. C'est un budget, et c'est la seule
raison pour laquelle vous pouvez chiffrer une question avant de la poser.
'''

# %%
# EN: A model that never stops asking. The cap is what ends this. | FR: Un modèle qui ne cesse jamais de demander. C'est le plafond qui y met fin.
runaway = agent.Agent(
    TOOLS, max_steps=3,
    model=agent.ScriptedModel(['{"tool":"list_documents","args":{}}'] * 20),
).run(T("Keep going forever.", "Continuez indéfiniment."), verbose=False)

print(T(f"stopped after {len(runaway.steps)} steps · reason: {runaway.stopped}",
        f"arrêté après {len(runaway.steps)} étapes · motif : {runaway.stopped}"))
print(runaway.answer)

# %% [markdown]
'''
<!--EN-->
---
## 8 · The audit log — the deliverable

An agent whose tool calls were not recorded cannot be explained afterwards, and a
statistical office cannot stand behind a process it cannot explain.

The log keeps what the model actually said, not a summary of it. When something
goes wrong three months from now, the raw reply is what tells you whether the
model asked for the wrong thing or your code did the wrong thing with a
reasonable request.
<!--FR-->
---
## 8 · Le journal d'audit — le livrable

Un agent dont les appels d'outils n'ont pas été enregistrés ne peut pas être
expliqué après coup, et un office statistique ne peut pas assumer un processus
qu'il ne peut pas expliquer.

Le journal conserve ce que le modèle a réellement dit, pas un résumé. Quand
quelque chose ira mal dans trois mois, c'est la réponse brute qui dira si le
modèle a demandé la mauvaise chose ou si votre code a mal traité une demande
raisonnable.
'''

# %%
# EN: Everything from this laboratory, on disk, ready for Friday. | FR: Tout ce laboratoire, sur disque, prêt pour vendredi.
for name, this_run in [("agent_audit_scripted.json", run),
                       ("agent_audit_approved.json", allowed),
                       ("agent_audit_live.json", live)]:
    if this_run is None:
        continue
    agent.save_audit(this_run, OUT / name, meta={
        "country": C.iso3,
        "tools": [t.name for t in TOOLS],
        "write_tools": [t.name for t in TOOLS if t.writes],
        "policy": "approve_all" if this_run is allowed else "approve_reads_only",
        "max_steps": 8,
        "corpus": str(CORPUS_DIR),
    })
    print(f"  {name}")

run.audit().to_csv(OUT / "agent_audit.csv", index=False)
print(T(f"\nWritten to {OUT}", f"\nÉcrit dans {OUT}"))

# %% [markdown]
'''
<!--EN-->
---
### What you have

<table>
<tr><td><b>agent_audit_*.json</b></td><td>Every request the model made, whether it was
allowed, what came back, and the raw reply behind each one.</td></tr>
<tr><td><b>agent_audit.csv</b></td><td>The same log as a table, for a report.</td></tr>
<tr><td><b>notes/finding.md</b></td><td>What the agent wrote, once a policy allowed it to.</td></tr>
</table>

### The limits of what you built

- The protocol is text, not native function calling. Production systems use the
  provider's own tool API — this one is visible on purpose, and it occasionally
  needs a retry when the model wraps its JSON in prose.
- `approve_all` was used in step 6 for demonstration. It is the wrong default for
  anything touching a real record.
- The agent has four tools and one of them writes. Adding a fifth is where offices
  get into trouble: **every new tool is a new thing the model can ask for.**
- **Nothing here validates that the answer follows from the tool results.** The log
  proves what happened, not that it was right.

### Checkpoint

| Question | Answer |
|---|---|
| Where does an approval gate go? | Between the model's request and `tool.run` — nowhere else |
| Why is `writes` a field on `Tool`? | So the policy cannot forget which tools change something |
| What does `max_steps` control? | Cost. An agent decides how many calls to make |
| A refused write shows in the log — what must you also check? | The disk. A gate that logs but executes is worse than none |
| An agent is wrong. Why is that worse than an assistant being wrong? | The action already happened |
<!--FR-->
---
### Ce que vous avez

<table>
<tr><td><b>agent_audit_*.json</b></td><td>Chaque demande du modèle, son autorisation ou non,
le retour obtenu, et la réponse brute derrière chacune.</td></tr>
<tr><td><b>agent_audit.csv</b></td><td>Le même journal sous forme de tableau, pour un rapport.</td></tr>
<tr><td><b>notes/finding.md</b></td><td>Ce que l'agent a écrit, une fois qu'une politique l'a autorisé.</td></tr>
</table>

### Les limites de ce que vous avez construit

- Le protocole est textuel, pas de l'appel de fonctions natif. Les systèmes de
  production utilisent l'API d'outils du fournisseur — celui-ci est visible à
  dessein, et il demande parfois une reprise quand le modèle enrobe son JSON de prose.
- `approve_all` a servi à l'étape 6 pour la démonstration. C'est la mauvaise valeur
  par défaut pour tout ce qui touche un enregistrement réel.
- L'agent a quatre outils dont un écrit. Ajouter le cinquième est le moment où les
  offices se mettent en difficulté : **chaque nouvel outil est une nouvelle chose
  que le modèle peut demander.**
- **Rien ici ne valide que la réponse découle des résultats d'outils.** Le journal
  prouve ce qui s'est passé, pas que c'était juste.

### Point de contrôle

| Question | Réponse |
|---|---|
| Où se place un point d'approbation ? | Entre la demande du modèle et `tool.run` — nulle part ailleurs |
| Pourquoi `writes` est-il un champ de `Tool` ? | Pour que la politique ne puisse pas oublier quels outils modifient quelque chose |
| Que contrôle `max_steps` ? | Le coût. Un agent décide combien d'appels effectuer |
| Une écriture refusée figure au journal — que faut-il vérifier aussi ? | Le disque. Un contrôle qui journalise mais exécute est pire que rien |
| Un agent se trompe. Pourquoi est-ce pire qu'un assistant qui se trompe ? | L'action a déjà eu lieu |
'''

# %% [markdown] tags=only-open
'''
<!--EN-->
---
## Your turn

1. **Write the policy your office would actually use.** Not `approve_reads_only` —
   a function that inspects the arguments. Refuse `save_note` outside a named
   directory; refuse a search whose query mentions a respondent identifier. Policies
   are code, and that is what makes them testable.
2. **Add a fifth tool, then justify it.** Something your office genuinely needs —
   a lookup against a published table, perhaps. Then write two sentences on what a
   malicious or confused request to it could do. If you cannot write those two
   sentences, do not add the tool.
3. **Break it deliberately.** Write a `ScriptedModel` that asks for the same tool
   twenty times, or passes arguments of the wrong type, or requests a filename of
   `../../etc/passwd`. Fix what breaks. The `save_note` tool already sanitises its
   filename — read that line and decide whether you trust it.
4. **Measure the cost.** Run the live agent on five questions and record the number
   of model calls each took. That distribution, not an average, is what you budget
   against.

Tomorrow morning is prompt engineering: making a single call reliable enough that
an agent built on it is worth trusting.
<!--FR-->
---
## À vous

1. **Écrivez la politique que votre office utiliserait réellement.** Pas
   `approve_reads_only` — une fonction qui inspecte les arguments. Refusez
   `save_note` hors d'un répertoire nommé ; refusez une recherche dont la requête
   mentionne un identifiant de répondant. Les politiques sont du code, et c'est ce
   qui les rend testables.
2. **Ajoutez un cinquième outil, puis justifiez-le.** Quelque chose dont votre
   office a réellement besoin — une consultation dans une table publiée, par
   exemple. Puis écrivez deux phrases sur ce qu'une demande malveillante ou confuse
   pourrait en faire. Si vous ne pouvez pas écrire ces deux phrases, n'ajoutez pas
   l'outil.
3. **Cassez-le délibérément.** Écrivez un `ScriptedModel` qui demande vingt fois le
   même outil, ou passe des arguments du mauvais type, ou demande un nom de fichier
   `../../etc/passwd`. Corrigez ce qui casse. L'outil `save_note` assainit déjà son
   nom de fichier — lisez cette ligne et décidez si vous lui faites confiance.
4. **Mesurez le coût.** Exécutez l'agent réel sur cinq questions et notez le nombre
   d'appels au modèle pour chacune. C'est cette distribution, et non une moyenne,
   qui sert de base au budget.

Demain matin : l'ingénierie de prompt — rendre un appel unique assez fiable pour
qu'un agent bâti dessus mérite confiance.
'''

# %% [markdown]
'''
<!--EN-->
---
> ### If something did not work
>
> **No model provider.** Steps 1–4 and 6–8 are the whole teaching content and need
> none. Step 5 is a demonstration that the same code accepts a real model.
>
> **The live agent looped without answering.** Raise `max_steps`, or narrow the
> task. A model asked to do three things at once often never decides it is done.
>
> **The live agent invented a figure.** Read its raw replies in the audit log. If it
> stated a number no tool returned, the system prompt was not enough for that model
> — that is a real finding, and it belongs in your Friday note.
>
> **A tool call failed with a TypeError.** The model passed an argument name that
> does not exist. The agent hands the error back so it can retry; if it never
> recovers, your tool descriptions are ambiguous.
<!--FR-->
---
> ### Si quelque chose n'a pas fonctionné
>
> **Aucun fournisseur de modèle.** Les étapes 1 à 4 et 6 à 8 constituent tout le
> contenu pédagogique et n'en exigent aucun. L'étape 5 démontre que le même code
> accepte un vrai modèle.
>
> **L'agent réel a bouclé sans répondre.** Augmentez `max_steps`, ou resserrez la
> tâche. Un modèle à qui l'on demande trois choses à la fois ne décide souvent
> jamais qu'il a fini.
>
> **L'agent réel a inventé un chiffre.** Lisez ses réponses brutes dans le journal
> d'audit. S'il a énoncé un nombre qu'aucun outil n'a renvoyé, le prompt système
> n'a pas suffi pour ce modèle — c'est un vrai constat, et il a sa place dans votre
> note de vendredi.
>
> **Un appel d'outil a échoué sur un TypeError.** Le modèle a passé un nom
> d'argument inexistant. L'agent lui renvoie l'erreur pour qu'il réessaie ; s'il ne
> s'en remet jamais, vos descriptions d'outils sont ambiguës.
'''
