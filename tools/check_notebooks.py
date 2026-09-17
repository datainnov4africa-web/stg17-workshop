#!/usr/bin/env python3
"""
STG17 · Validate every published notebook before it reaches a participant.

    python tools/check_notebooks.py

Four checks, each of which has a specific failure it is guarding against:

  1. **Valid JSON and nbformat** — a notebook that will not open at 09:30
  2. **No secrets** — an API key committed to a public repository is a published key
  3. **Code cells parse** — a syntax error found by CI, not by forty people
  4. **No execution outputs** — outputs bloat diffs and can leak data

Every notebook is supplied by the workshop team, not generated here, so these
four are deliberately the only rules: they are the ones whose violation would
harm a participant or the repository. Anything about how a notebook is written
is the author's business.

Exit code 1 on any failure, so it can gate a pull request.
"""

from __future__ import annotations

import ast
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NOTEBOOKS = ROOT / "docs" / "downloads"

# Patterns for credentials that must never appear in a committed notebook.
# Deliberately conservative: a false positive costs a minute, a false negative
# costs a key rotation and an incident report.
SECRET_PATTERNS = [
    (re.compile(r"\bsk-[A-Za-z0-9]{20,}"), "OpenAI-style key"),
    (re.compile(r"\bgsk_[A-Za-z0-9]{20,}"), "Groq key"),
    (re.compile(r"\bsk-ant-[A-Za-z0-9\-_]{20,}"), "Anthropic key"),
    (re.compile(r"\bghp_[A-Za-z0-9]{30,}"), "GitHub personal access token"),
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "AWS access key id"),
    (re.compile(r"\bey[A-Za-z0-9_\-]{20,}\.[A-Za-z0-9_\-]{20,}\."), "JWT / bearer token"),
    (re.compile(r'(?i)(api[_-]?key|token|password|secret)\s*=\s*["\'][^"\']{16,}["\']'),
     "hard-coded credential"),
]

# Placeholders that legitimately look like the patterns above.
ALLOWED = re.compile(r"(?i)(CHANGE-ME|<your|xxx+|\.\.\.|example|placeholder|gsk_\.\.\.)")


def check(path: Path) -> list[str]:
    problems: list[str] = []
    relative = path.relative_to(ROOT).as_posix()

    # 1. Valid notebook -------------------------------------------------------
    try:
        notebook = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{relative}: not valid JSON — {exc}"]
    if notebook.get("nbformat") != 4:
        problems.append(f"{relative}: nbformat is {notebook.get('nbformat')}, expected 4")

    cells = notebook.get("cells", [])
    if not cells:
        problems.append(f"{relative}: no cells")

    # The serialised notebook, for pattern matching that should see everything
    # including markdown and metadata.
    whole = json.dumps(notebook, ensure_ascii=False)
    # The cell sources concatenated, unescaped. Anything matching real Python
    # must be matched against this: in the JSON dump every quote is backslashed,
    # so `COUNTRY_ISO3 = "CIV"` appears as `COUNTRY_ISO3 = \"CIV\"` and a naive
    # regex silently never matches.
    source_text = "\n".join(
        "".join(cell.get("source", [])) for cell in cells
    )

    # 2. Secrets --------------------------------------------------------------
    for pattern, label in SECRET_PATTERNS:
        for match in pattern.finditer(source_text):
            snippet = match.group(0)
            context = source_text[max(0, match.start() - 60): match.end() + 20]
            if ALLOWED.search(context):
                continue
            problems.append(
                f"{relative}: possible {label} — {snippet[:12]}… "
                f"(if this is a placeholder, make it obviously one)"
            )

    # 3. Code cells parse -----------------------------------------------------
    for index, cell in enumerate(cells):
        if cell.get("cell_type") != "code":
            continue
        source = "".join(cell.get("source", []))
        if not source.strip():
            continue
        if source.lstrip().startswith(("!", "%")):
            continue  # shell or magic line, not Python
        stripped = "\n".join(
            "" if line.lstrip().startswith(("!", "%")) else line
            for line in source.splitlines()
        )
        try:
            ast.parse(stripped)
        except SyntaxError as exc:
            problems.append(f"{relative}: cell {index} does not parse — line {exc.lineno}: {exc.msg}")

    # 4. No stored outputs ----------------------------------------------------
    with_outputs = [i for i, c in enumerate(cells)
                    if c.get("cell_type") == "code" and c.get("outputs")]
    if with_outputs:
        problems.append(f"{relative}: {len(with_outputs)} cell(s) carry execution outputs "
                        f"— clear them before supplying the notebook")

    return problems


def main() -> int:
    paths = sorted(NOTEBOOKS.rglob("*.ipynb"))
    paths = [p for p in paths if ".ipynb_checkpoints" not in p.parts]
    if not paths:
        print("No notebooks supplied yet under docs/downloads/.")
        return 0

    all_problems: list[str] = []
    for path in paths:
        problems = check(path)
        status = "OK" if not problems else f"{len(problems)} problem(s)"
        print(f"  {path.relative_to(ROOT).as_posix():<52} {status}")
        all_problems.extend(problems)

    if all_problems:
        print(f"\n{len(all_problems)} problem(s):\n")
        for problem in all_problems:
            print("   -", problem)
        return 1

    print(f"\n{len(paths)} notebook(s) checked. All clear.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
