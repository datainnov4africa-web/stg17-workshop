#!/usr/bin/env python3
"""
STG17 · Preview the site locally, with the right URL printed.

    python tools/serve.py

Why this exists rather than just `mkdocs serve`
-----------------------------------------------
`site_url` in mkdocs.yml carries the GitHub Pages path, `/stg17-workshop/`.
mkdocs honours that path when serving, so the site does **not** appear at
`http://127.0.0.1:8000/` — it appears at `http://127.0.0.1:8000/stg17-workshop/`.
The root does redirect, but only once a server is actually listening, and the
first thing anyone tries is the bare address.

This script regenerates everything derived, starts the server, and prints both
the English and the French URL in full, so there is nothing to guess.

    python tools/serve.py --port 8080     # if 8000 is taken
    python tools/serve.py --no-build      # skip regeneration, start faster
"""

from __future__ import annotations

import argparse
import re
import socket
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def base_path() -> str:
    """The path component of site_url, which is where mkdocs will actually serve."""
    text = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
    match = re.search(r"^site_url:\s*(\S+)", text, re.M)
    if not match:
        return "/"
    path = re.sub(r"^https?://[^/]+", "", match.group(1).strip())
    return path if path.endswith("/") else path + "/"


def port_is_free(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        return sock.connect_ex(("127.0.0.1", port)) != 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Preview the STG17 site locally")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--no-build", action="store_true",
                        help="skip regenerating notebooks, pages and decks")
    args = parser.parse_args()

    if not args.no_build:
        print("Regenerating everything derived...\n")
        result = subprocess.run([sys.executable, "tools/build_all.py"], cwd=ROOT, check=False)
        if result.returncode != 0:
            print("\nBuild failed — fix the errors above before serving.")
            return 1

    port = args.port
    while not port_is_free(port) and port < args.port + 10:
        print(f"Port {port} is in use, trying {port + 1}...")
        port += 1

    path = base_path()
    print("\n" + "=" * 70)
    print("  The site is served under the GitHub Pages path, not at the root:")
    print()
    print(f"    English   http://127.0.0.1:{port}{path}")
    print(f"    Français  http://127.0.0.1:{port}{path}fr/")
    print()
    print("  Ctrl-C to stop. Edits to docs/ reload automatically;")
    print("  edits to config/ or notebooks/_masters/ need this script re-run.")
    print("=" * 70 + "\n")

    return subprocess.run(
        [sys.executable, "-m", "mkdocs", "serve", "-a", f"127.0.0.1:{port}"],
        cwd=ROOT, check=False,
    ).returncode


if __name__ == "__main__":
    sys.exit(main())
