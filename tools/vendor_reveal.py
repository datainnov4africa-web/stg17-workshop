#!/usr/bin/env python3
"""
STG17 · Download reveal.js into slides/vendor/ so the decks work offline.

    python tools/vendor_reveal.py
    python tools/build_slides.py --offline     # rewrite the decks to use it

The venues this workshop runs in do not reliably reach a CDN, and a facilitator
discovering that thirty seconds before a session is a preventable failure. Run
this once before packing the USB keys.

Downloads only the seven files the decks actually reference — about 400 KB, not
the whole distribution.
"""

from __future__ import annotations

import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VENDOR = ROOT / "slides" / "vendor"
VERSION = "5.1.0"
BASE = f"https://cdn.jsdelivr.net/npm/reveal.js@{VERSION}"

FILES = [
    "dist/reset.css",
    "dist/reveal.css",
    "dist/reveal.js",
    "plugin/notes/notes.js",
    "plugin/highlight/highlight.js",
    "plugin/highlight/monokai.css",
]


def main() -> int:
    VENDOR.mkdir(parents=True, exist_ok=True)
    total = 0
    for relative in FILES:
        target = VENDOR / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists() and target.stat().st_size > 500:
            print(f"  have  {relative}")
            total += target.stat().st_size
            continue
        url = f"{BASE}/{relative}"
        try:
            with urllib.request.urlopen(url, timeout=60) as response:  # noqa: S310
                data = response.read()
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            print(f"  FAILED {relative}: {exc}")
            return 1
        target.write_bytes(data)
        total += len(data)
        print(f"  wrote {relative}  ({len(data)/1024:.0f} KB)")

    (VENDOR / "VERSION").write_text(VERSION, encoding="utf-8")
    print(f"\nreveal.js {VERSION} vendored into {VENDOR.relative_to(ROOT)} "
          f"({total/1024:.0f} KB total).")
    print("Rebuild the decks for offline use:  python tools/build_slides.py --offline")
    return 0


if __name__ == "__main__":
    sys.exit(main())
