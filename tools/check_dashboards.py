#!/usr/bin/env python3
"""
STG17 · Every URL in liens.txt reaches the page, or this fails.

    python tools/check_dashboards.py

The showcase is generated, so the question that matters is not whether the
generator ran but whether anything fell through it. A line a participant wrote
and that never appears on the page is the one failure nobody would notice: the
page looks complete, and one country's work is missing from it.

So this walks the file line by line and, for each URL, asks four questions:

    recognised   does it parse as a dashboard address at all?
    placed       is it attached to a country the page can name?
    read         was its content fetched, so its description is real?
    rendered     does its address actually appear in BOTH built pages?

The last one is the proof. The rest are the reasons a URL might fail it.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dashboards_data as D  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
PAGES = {"en": ROOT / "docs" / "dashboards" / "index.md",
         "fr": ROOT / "docs" / "dashboards" / "index.fr.md"}
IMG = ROOT / "docs" / "assets" / "img" / "dashboards"


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    brut = D.LIENS.read_text(encoding="utf-8-sig")
    lignes = brut.splitlines()
    rendus = {lang: (p.read_text(encoding="utf-8") if p.exists() else "")
              for lang, p in PAGES.items()}
    absentes = [lang for lang, t in rendus.items() if not t]

    entrees = {e["cle"]: e for e in D.entrees()}
    vus: set[str] = set()
    problemes: list[str] = []
    vides = doublons = 0
    lignes_utiles = 0

    print(f"liens.txt · {len(lignes)} ligne(s)\n")
    print("   n°  URL                                                            etat")
    print("  " + "-" * 92)
    for i, l in enumerate(lignes, 1):
        u = l.strip()
        if not u:
            vides += 1
            continue
        lignes_utiles += 1
        m = (re.match(r"https://([^.]+)\.github\.io/([^/]+)/?$", u)
             or re.match(r"https://github\.com/([^/]+)/([^/]+)/?$", u))
        if not m:
            problemes.append(f"ligne {i} : adresse non reconnue — {u}")
            print(f"  {i:4}  {u[:60]:62} NON RECONNUE")
            continue
        cle = f"{m.group(1)}__{m.group(2)}"
        if cle in vus:
            doublons += 1
            print(f"  {i:4}  {u[:60]:62} doublon (deja compte)")
            continue
        vus.add(cle)
        e = entrees.get(cle)
        if not e:
            problemes.append(f"ligne {i} : reconnue mais absente du parseur — {u}")
            print(f"  {i:4}  {u[:60]:62} PERDUE PAR LE PARSEUR")
            continue

        etats = []
        if not e.get("iso"):
            problemes.append(f"ligne {i} : aucun pays rattache — {u}")
            etats.append("SANS PAYS")
        manque_rendu = [lang for lang, t in rendus.items() if e["url"] not in t]
        if absentes:
            etats.append("page non construite")
        elif manque_rendu:
            problemes.append(f"ligne {i} : absente de la page {'/'.join(manque_rendu)} — {u}")
            etats.append(f"ABSENTE DE {'/'.join(manque_rendu).upper()}")
        else:
            etats.append("sur les 2 pages")
        if not (IMG / f"{cle}.webp").exists():
            etats.append("sans vignette")
        pays = D.PAYS[e["iso"]][0] if e.get("iso") else "?"
        print(f"  {i:4}  {u[:60]:62} {pays:11} {' · '.join(etats)}")

    print("\n" + "=" * 94)
    print(f"  lignes vides .............. {vides}")
    print(f"  doublons .................. {doublons}")
    print(f"  URL distinctes ............ {len(vus)}")
    print(f"  connues du parseur ........ {len(entrees)}")
    orphelines = set(entrees) - vus
    if orphelines:
        problemes.append(f"le parseur connait {len(orphelines)} cle(s) absente(s) du fichier")
    if absentes:
        problemes.append(f"page(s) non construite(s) : {', '.join(absentes)} — "
                         f"lancez d'abord python tools/build_dashboards.py")
    if problemes:
        print(f"\n{len(problemes)} probleme(s) :\n")
        for p in problemes:
            print(f"   - {p}")
        return 1
    print(f"\nLes {len(vus)} URL du fichier figurent toutes sur les deux pages.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
