"""
STG17 · A tool-using agent, with the human in the loop where it belongs.

The Day 1 afternoon builds an assistant that answers from passages you chose. This
module is the next step: the model chooses which tool to call, and your code
decides whether to honour the request.

--------------------------------------------------------------------------
THE ONE SENTENCE THIS MODULE EXISTS TO MAKE CONCRETE
--------------------------------------------------------------------------
    The model ASKS for the tool. Your code RUNS it.

Every approval gate, audit log and safety check lives in the gap between those
two verbs. `Agent.step` is that gap, written out in about twenty lines, so a
participant can point at the exact place where their office's control sits.

--------------------------------------------------------------------------
WHY A TEXT PROTOCOL RATHER THAN NATIVE FUNCTION CALLING
--------------------------------------------------------------------------
Production systems use the provider's own tool-calling API. This module has the
model emit a JSON object instead, which the code parses.

That is a teaching decision, and it costs something — a model occasionally emits
malformed JSON, which native tool calling would have prevented. It buys three
things worth more in this room:

  1. It works identically on every provider, including a local Ollama model on a
     laptop with no API key. A laboratory where half the room cannot run the
     exercise teaches half a room.
  2. The parse step is visible. With native tool calling the request-to-execution
     gap is inside the SDK, and the thing this session is about becomes invisible.
  3. Participants can read the raw model output and see it asking. That is the
     moment the distinction stops being abstract.

`stg17.llm.chat` deliberately has no `tools` parameter for the same reason: the
translation between intent and provider syntax is the teaching content, not
something to hide.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Sequence

from .i18n import T

MAX_STEPS = 6
MAX_RESULT_CHARS = 1800


# ---------------------------------------------------------------------------
#  Tools
# ---------------------------------------------------------------------------
@dataclass
class Tool:
    """
    One function the model may ask for.

    `writes` is the field that matters. A tool that only reads can be executed
    without asking anyone; a tool that changes something — a file, a record, an
    email — is a different kind of risk and gets a different default policy.
    Splitting them at the type level rather than by convention means an office
    cannot forget which is which.
    """

    name: str
    description: str
    args: dict[str, str]                  # argument name -> what it is
    run: Callable[..., Any]
    writes: bool = False

    def signature(self) -> str:
        params = ", ".join(f"{k}: {v}" for k, v in self.args.items()) or "no arguments"
        mark = " [WRITES — needs approval]" if self.writes else ""
        return f"{self.name}({params}){mark}\n    {self.description}"


def render_tools(tools: Sequence[Tool]) -> str:
    return "\n\n".join(t.signature() for t in tools)


# ---------------------------------------------------------------------------
#  The protocol
# ---------------------------------------------------------------------------
SYSTEM = """You are an assistant to a national statistical office, working through a task one
step at a time with a small set of tools.

Reply with EXACTLY ONE JSON object and nothing else — no explanation before it, no
code fence around it. Two shapes are allowed:

  {"thought": "why this tool", "tool": "tool_name", "args": {"argument": "value"}}
  {"thought": "why I can stop", "answer": "your final answer to the user"}

Rules:
- Call one tool at a time. You will be given its result and asked again.
- Never invent a tool name or an argument name. Use only what is listed.
- Never state a figure that a tool has not returned to you. If the tools cannot
  find it, say so in your answer.
- When you have enough to answer, answer. Do not keep calling tools.
- Your final answer must name the tools whose results it rests on.

TOOLS AVAILABLE:

<<TOOLS>>"""


@dataclass
class Action:
    thought: str = ""
    tool: str | None = None
    args: dict = field(default_factory=dict)
    answer: str | None = None

    @property
    def is_final(self) -> bool:
        return self.answer is not None


class ProtocolError(ValueError):
    """The model did not emit a usable action. Recoverable — we tell it so."""


_FENCE = re.compile(r"```(?:json)?\s*(.*?)```", re.S)


def parse_action(text: str) -> Action:
    """
    Read the model's reply as an action.

    Tolerant of a code fence and of surrounding prose, because models add both
    despite instructions. Not tolerant of a missing tool name or a non-object —
    those raise, and the agent hands the error back to the model, which is how a
    real system recovers from a malformed call.
    """
    raw = text.strip()
    fence = _FENCE.search(raw)
    if fence:
        raw = fence.group(1).strip()
    else:
        start, end = raw.find("{"), raw.rfind("}")
        if start != -1 and end > start:
            raw = raw[start:end + 1]

    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ProtocolError(f"not valid JSON: {exc.msg}") from exc
    if not isinstance(payload, dict):
        raise ProtocolError("expected a JSON object")

    if "answer" in payload:
        return Action(thought=str(payload.get("thought", "")), answer=str(payload["answer"]))
    if "tool" in payload:
        args = payload.get("args", {})
        if not isinstance(args, dict):
            raise ProtocolError("'args' must be an object")
        return Action(thought=str(payload.get("thought", "")),
                      tool=str(payload["tool"]), args=args)
    raise ProtocolError("object has neither 'tool' nor 'answer'")


# ---------------------------------------------------------------------------
#  Approval policies — the gap, made a parameter
# ---------------------------------------------------------------------------
def approve_reads_only(tool: Tool, args: dict) -> bool:
    """The sane default: run read tools, refuse write tools outright."""
    return not tool.writes


def approve_all(tool: Tool, args: dict) -> bool:
    """
    Everything runs. Correct for an exercise on a sample corpus; wrong for
    anything touching a real record, which is why it is named this plainly.
    """
    return True


def approve_interactive(tool: Tool, args: dict) -> bool:
    """Ask a person, at the keyboard, before a write tool runs."""
    if not tool.writes:
        return True
    shown = json.dumps(args, ensure_ascii=False)[:300]
    reply = input(T(f"\n  APPROVE? {tool.name}({shown})  [y/N] ",
                    f"\n  APPROUVER ? {tool.name}({shown})  [o/N] "))
    return reply.strip().lower() in {"y", "o", "yes", "oui"}


# ---------------------------------------------------------------------------
#  Running
# ---------------------------------------------------------------------------
@dataclass
class Step:
    n: int
    raw: str                       # exactly what the model said
    action: Action | None = None
    approved: bool | None = None   # None for a read tool under a policy that auto-runs
    result: str = ""
    error: str = ""

    def row(self) -> dict:
        return {
            "step": self.n,
            "tool": (self.action.tool if self.action else None) or ("(answer)" if self.action and self.action.is_final else "(unparsed)"),
            "args": json.dumps(self.action.args, ensure_ascii=False)[:60] if self.action else "",
            "approved": self.approved,
            "result": (self.error or self.result)[:80].replace("\n", " "),
        }


@dataclass
class Run:
    question: str
    steps: list[Step] = field(default_factory=list)
    answer: str = ""
    stopped: str = ""              # why the loop ended

    @property
    def tool_calls(self) -> int:
        return sum(1 for s in self.steps if s.action and s.action.tool)

    @property
    def refused(self) -> int:
        return sum(1 for s in self.steps if s.approved is False)

    def audit(self):
        """The log. Every request, whether it was allowed, and what came back."""
        import pandas as pd  # noqa: PLC0415
        return pd.DataFrame([s.row() for s in self.steps])

    def to_dict(self) -> dict:
        return {
            "question": self.question,
            "answer": self.answer,
            "stopped": self.stopped,
            "tool_calls": self.tool_calls,
            "refused_calls": self.refused,
            "steps": [
                {"step": s.n, "raw": s.raw, "thought": s.action.thought if s.action else "",
                 "tool": s.action.tool if s.action else None,
                 "args": s.action.args if s.action else {},
                 "approved": s.approved, "result": s.result, "error": s.error}
                for s in self.steps
            ],
        }


class Agent:
    """
    The loop: ask the model, parse, check, execute, feed back, repeat.

    `max_steps` is not a safety net, it is a budget. An agent decides how many
    model calls to make, so without a cap the cost of one question is unbounded —
    and a loop that cannot terminate will not terminate on its own.
    """

    def __init__(self, tools: Sequence[Tool], provider: str = "auto",
                 max_steps: int = MAX_STEPS,
                 approve: Callable[[Tool, dict], bool] = approve_reads_only,
                 model: Callable[[str, str], str] | None = None):
        self.tools = {t.name: t for t in tools}
        self.provider = provider
        self.max_steps = max_steps
        self.approve = approve
        #: Injectable so the executor can be exercised with no provider. See
        #: `ScriptedModel` — the loop, the gate and the audit log are your code,
        #: and your code should be testable without anyone's API key.
        self.model = model or self._call_provider

    def _call_provider(self, system: str, conversation: str) -> str:
        from . import llm  # noqa: PLC0415
        return llm.chat(conversation, system=system, provider=self.provider,
                        max_tokens=900, deterministic=True).text

    def run(self, question: str, verbose: bool = True) -> Run:
        # Substitution by replace, not str.format: the prompt above contains JSON
        # examples, and every brace in them would be read as a format field.
        system = SYSTEM.replace("<<TOOLS>>", render_tools(list(self.tools.values())))
        transcript = [f"TASK: {question}"]
        run = Run(question=question)

        for n in range(1, self.max_steps + 1):
            raw = self.model(system, "\n\n".join(transcript))
            step = Step(n=n, raw=raw.strip())
            run.steps.append(step)

            try:
                step.action = parse_action(raw)
            except ProtocolError as exc:
                step.error = f"protocol error: {exc}"
                transcript.append(f"ASSISTANT: {raw.strip()}")
                transcript.append(
                    f"SYSTEM: Your reply could not be read ({exc}). Reply with exactly one "
                    f"JSON object, no code fence, no other text.")
                if verbose:
                    print(f"  [{n}] {step.error}")
                continue

            if step.action.is_final:
                run.answer = step.action.answer or ""
                run.stopped = "answered"
                if verbose:
                    print(f"  [{n}] answered")
                return run

            tool = self.tools.get(step.action.tool or "")
            if tool is None:
                step.error = f"no such tool: {step.action.tool!r}"
                transcript.append(f"ASSISTANT: {raw.strip()}")
                transcript.append(f"TOOL RESULT: ERROR - {step.error}. "
                                  f"Available: {', '.join(self.tools)}")
                if verbose:
                    print(f"  [{n}] {step.error}")
                continue

            # ---- THE GAP ----------------------------------------------------
            # The model has asked. Nothing has happened yet. This is where an
            # office's policy lives, and it is four lines long.
            allowed = self.approve(tool, step.action.args)
            step.approved = allowed
            if not allowed:
                step.error = "refused by policy"
                transcript.append(f"ASSISTANT: {raw.strip()}")
                transcript.append(
                    "TOOL RESULT: REFUSED - a human did not approve this call. "
                    "Do not retry it. Continue without it, or explain in your answer "
                    "what you could not do.")
                if verbose:
                    print(f"  [{n}] {tool.name} REFUSED")
                continue
            # -----------------------------------------------------------------

            try:
                result = tool.run(**step.action.args)
            except Exception as exc:  # noqa: BLE001 - the model must see its own bad call
                step.error = f"{type(exc).__name__}: {exc}"
                transcript.append(f"ASSISTANT: {raw.strip()}")
                transcript.append(f"TOOL RESULT: ERROR - {step.error}")
                if verbose:
                    print(f"  [{n}] {tool.name} failed: {step.error}")
                continue

            step.result = str(result)[:MAX_RESULT_CHARS]
            transcript.append(f"ASSISTANT: {raw.strip()}")
            transcript.append(f"TOOL RESULT: {step.result}")
            if verbose:
                print(f"  [{n}] {tool.name} -> {step.result[:60]}...")

        run.stopped = "step limit"
        run.answer = T(
            "The step limit was reached before an answer. That is a budget being "
            "enforced, not a crash — raise max_steps, or give the agent a narrower task.",
            "La limite d'étapes a été atteinte avant une réponse. C'est un budget qui "
            "s'applique, pas une panne — augmentez max_steps, ou donnez une tâche plus "
            "étroite à l'agent.")
        return run


# ---------------------------------------------------------------------------
#  A model stand-in, so the executor is testable with no API key
# ---------------------------------------------------------------------------
class ScriptedModel:
    """
    Replays a fixed list of replies, ignoring what it is asked.

    This is not a simulation of a model — it makes no decisions. It exists so
    that the loop, the approval gate, the error handling and the audit log can be
    exercised and understood without a provider. Those four things are the part
    an office writes and owns; the model is the part it rents.
    """

    def __init__(self, replies: Sequence[str]):
        self.replies = list(replies)
        self.seen: list[str] = []

    def __call__(self, system: str, conversation: str) -> str:
        self.seen.append(conversation)
        if not self.replies:
            return json.dumps({"thought": "nothing scripted left", "answer": "(end of script)"})
        return self.replies.pop(0)


# ---------------------------------------------------------------------------
#  Ready-made tools
# ---------------------------------------------------------------------------
def search_tool(index, k: int = 3) -> Tool:
    """Retrieval from the Day 1 RAG index, as something the model can ask for."""
    def run(query: str) -> str:
        hits = index.search(query, k=k)
        if not hits:
            return "No passage matched."
        return "\n\n".join(
            f"[{h.chunk.citation} · score {h.score:.2f}]\n{h.chunk.text[:500]}" for h in hits)

    return Tool(
        name="search_documents",
        description=T("Search the office's publications and return the most relevant passages.",
                      "Rechercher dans les publications de l'office et renvoyer les passages "
                      "les plus pertinents."),
        args={"query": T("what to look for, in words", "ce qu'il faut chercher, en mots")},
        run=run,
    )


def list_tool(docs) -> Tool:
    def run() -> str:
        return "\n".join(f"- {d.title} ({d.words} words)" for d in docs)

    return Tool(
        name="list_documents",
        description=T("List every document the assistant can see.",
                      "Lister tous les documents visibles par l'assistant."),
        args={}, run=run,
    )


_ARITHMETIC = re.compile(r"^[0-9\s+\-*/().,%]+$")


def calculator_tool() -> Tool:
    """
    Arithmetic, because a language model predicts digits rather than computing them.

    The guard is a whitelist, not a blacklist. `eval` on model output with anything
    less is a remote code execution path, and "the model would not do that" is not
    a security control.
    """
    def run(expression: str) -> str:
        expr = expression.replace(",", "").strip()
        if not _ARITHMETIC.match(expr):
            return ("REFUSED: only digits and + - * / ( ) . % are allowed. "
                    "This tool does arithmetic, not code.")
        try:
            return str(eval(expr, {"__builtins__": {}}, {}))  # noqa: S307 - whitelisted above
        except Exception as exc:  # noqa: BLE001
            return f"ERROR: {type(exc).__name__}: {exc}"

    return Tool(
        name="calculate",
        description=T("Evaluate an arithmetic expression. Use this for every calculation.",
                      "Évaluer une expression arithmétique. À utiliser pour tout calcul."),
        args={"expression": T("digits and + - * / ( ) only", "chiffres et + - * / ( ) seulement")},
        run=run,
    )


def note_tool(directory: str | Path) -> Tool:
    """A write tool. Deliberately the only one, so the gate has something to stop."""
    out = Path(directory)

    def run(filename: str, text: str) -> str:
        out.mkdir(parents=True, exist_ok=True)
        safe = re.sub(r"[^A-Za-z0-9._-]", "_", filename)[:60] or "note.md"
        path = out / safe
        path.write_text(text, encoding="utf-8")
        return f"Written: {path}"

    return Tool(
        name="save_note",
        description=T("Write a short note to disk. This changes something, so it needs approval.",
                      "Écrire une courte note sur disque. Cela modifie quelque chose : "
                      "approbation requise."),
        args={"filename": T("the file name", "le nom du fichier"),
              "text": T("the note content", "le contenu de la note")},
        run=run, writes=True,
    )


def save_audit(run: Run, path: str | Path, meta: dict | None = None) -> Path:
    """
    The audit log, on disk.

    An agent whose tool calls were not recorded cannot be explained afterwards,
    and a statistical office cannot stand behind a process it cannot explain.
    """
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"meta": meta or {}, **run.to_dict()},
                              ensure_ascii=False, indent=2), encoding="utf-8")
    return out
