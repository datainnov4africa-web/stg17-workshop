#!/usr/bin/env python3
"""
STG17 · Smoke test for the agent loop of the Day 1 laboratory.

    python tools/check_agent.py

Runs with no model provider: `ScriptedModel` replays fixed replies, so the loop,
the approval gate, the error recovery and the audit log are all exercised without
an API key. That is the point — those four things are the part an office writes
and owns, and they should be testable without renting anything.

The check that matters most is the last one: a refused write tool must leave the
disk untouched. An approval gate that logs a refusal and executes anyway is worse
than no gate, because it produces a reassuring audit trail.
"""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from stg17 import agent, rag  # noqa: E402

FAILURES: list[str] = []


def check(condition: bool, description: str, detail: str = "") -> None:
    if condition:
        print(f"  ok    {description}")
    else:
        print(f"  FAIL  {description}" + (f"  ({detail})" if detail else ""))
        FAILURES.append(description)


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    print("Agent loop (stg17.agent)")
    tmp = Path(tempfile.mkdtemp())
    docs = rag.load_corpus(rag.write_sample_corpus(tmp / "corpus"))
    index = rag.build_index(rag.chunk_documents(docs), kind="tfidf")
    notes = tmp / "notes"
    tools = [agent.search_tool(index), agent.list_tool(docs),
             agent.calculator_tool(), agent.note_tool(notes)]

    # --- the protocol -----------------------------------------------------
    plain = agent.parse_action('{"tool":"calculate","args":{"expression":"2+2"}}')
    check(plain.tool == "calculate" and plain.args == {"expression": "2+2"},
          "a bare JSON object parses")
    fenced = agent.parse_action('```json\n{"tool":"list_documents","args":{}}\n```')
    check(fenced.tool == "list_documents", "a fenced object parses")
    chatty = agent.parse_action('Sure! {"answer":"done"} hope that helps')
    check(chatty.is_final and chatty.answer == "done", "an object wrapped in prose parses")
    for bad in ("not json", "[1,2,3]", '{"thought":"nothing else"}'):
        try:
            agent.parse_action(bad)
            check(False, f"malformed reply {bad[:18]!r} is rejected")
        except agent.ProtocolError:
            check(True, f"malformed reply {bad[:18]!r} is rejected")

    # --- the loop, including every recoverable failure ---------------------
    script = [
        '{"tool":"search_documents","args":{"query":"unemployment rate"}}',
        '```json\n{"tool":"calculate","args":{"expression":"19.2 - 8.6"}}\n```',
        '{"tool":"no_such_tool","args":{}}',
        'this is not json',
        '{"tool":"save_note","args":{"filename":"n.md","text":"x"}}',
        '{"answer":"Youth unemployment is 10.6 points higher [search_documents, calculate]"}',
    ]
    run = agent.Agent(tools, model=agent.ScriptedModel(script), max_steps=8).run(
        "Compare youth and overall unemployment.", verbose=False)

    check(run.stopped == "answered", "the loop ends on a final answer", run.stopped)
    check(len(run.steps) == 6, "every reply produced a step", str(len(run.steps)))
    check(run.steps[0].result.startswith("[labour force survey"),
          "the search tool returns a cited passage")
    check(run.steps[1].result == "10.6", "the calculator computes", run.steps[1].result)
    check("no such tool" in run.steps[2].error, "an unknown tool is reported, not raised")
    check("protocol error" in run.steps[3].error, "an unparsable reply is recovered from")

    # --- the gap ----------------------------------------------------------
    check(run.steps[4].approved is False, "a write tool is refused by the default policy")
    check(not notes.exists(),
          "a REFUSED write leaves the disk untouched",
          "the note directory was created despite refusal")
    check(run.refused == 1 and run.tool_calls == 4, "the audit counts calls and refusals")

    # The gate must be capable of allowing, or "nothing was written" proves nothing.
    allowed = agent.Agent(tools, model=agent.ScriptedModel([
        '{"tool":"save_note","args":{"filename":"n.md","text":"hello"}}',
        '{"answer":"saved"}']), approve=agent.approve_all).run("Save a note.", verbose=False)
    check(allowed.steps[0].approved is True, "the gate can allow a write")
    check((notes / "n.md").exists() and (notes / "n.md").read_text(encoding="utf-8") == "hello",
          "an APPROVED write reaches the disk")

    # --- the budget -------------------------------------------------------
    looping = agent.Agent(tools, max_steps=3, model=agent.ScriptedModel(
        ['{"tool":"list_documents","args":{}}'] * 10)).run("Loop forever.", verbose=False)
    check(looping.stopped == "step limit", "max_steps stops a non-terminating agent")
    check(len(looping.steps) == 3, "the cap is exact", str(len(looping.steps)))

    # --- the calculator guard --------------------------------------------
    calc = agent.calculator_tool()
    check(calc.run(expression="2 + 2 * 3") == "8", "arithmetic works")
    check(calc.run(expression="__import__('os').system('echo hi')").startswith("REFUSED"),
          "the calculator refuses anything that is not arithmetic")
    check(calc.run(expression="open('/etc/passwd').read()").startswith("REFUSED"),
          "the calculator refuses a file read")

    # --- the audit --------------------------------------------------------
    path = agent.save_audit(run, tmp / "audit.json", {"country": "CIV"})
    saved = json.loads(path.read_text(encoding="utf-8"))
    check(len(saved["steps"]) == 6, "the audit records every step")
    check(any(s["approved"] is False for s in saved["steps"]),
          "the audit records the refusal")
    check(all("raw" in s for s in saved["steps"]),
          "the audit keeps what the model actually said")

    print()
    if FAILURES:
        print(f"{len(FAILURES)} check(s) failed:")
        for name in FAILURES:
            print("   -", name)
        return 1
    print("All clear.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
