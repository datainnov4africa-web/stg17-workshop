"""
STG17 · Bilingual runtime (EN / FR).

Two mechanisms keep the English and French notebooks from drifting apart:

  1. **Build time** — markdown cells are written once in the master notebook
     inside <!--EN--> / <!--FR--> blocks.
     one file per language. See that script for the full convention.

  2. **Run time** — anything a *code* cell prints goes through `T()`:

         from stg17.i18n import T, set_lang
         set_lang("fr")
         print(T("Loading boundaries...", "Chargement des frontières..."))

Because `T()` resolves at run time, the SAME code cell works in both notebooks.
Only comments differ between the two builds, and those are handled by the
`# EN: ... | FR: ...` convention that the build script rewrites.

The active language is also what `stg17.ui` uses for its banners and what
`stg17.countries` uses for country names, so a single `set_lang()` call at the
top of a notebook switches every human-readable string it will ever produce.
"""

from __future__ import annotations

import os
from typing import Any

_LANG = "en"

#: The two languages of the workshop. English is the working language of the
#: sessions; French is provided for the laboratory material, per the concept note.
LANGS = ("en", "fr")


def set_lang(lang: str) -> str:
    """
    Set the active language. Accepts 'en', 'EN', 'fr', 'FR', 'french', 'français'.

    Returns the normalised code, so a notebook can do:

        LANG = set_lang("FR")     # -> 'fr'
    """
    global _LANG
    norm = "fr" if str(lang).strip().lower().startswith("f") else "en"
    _LANG = norm
    os.environ["STG17_LANG"] = norm
    return norm


def get_lang() -> str:
    """The active language code, 'en' or 'fr'."""
    return _LANG


def is_fr() -> bool:
    return _LANG == "fr"


def T(en: str, fr: str) -> str:
    """
    The workhorse. Returns whichever of the two strings matches the active language.

    Deliberately positional and two-argument: it stays readable inside an
    f-string and inside a print, which is where 95% of its uses live.

        print(T(f"{n} regions loaded", f"{n} régions chargées"))
    """
    return fr if _LANG == "fr" else en


def pick(mapping: dict[str, Any], default: Any = None) -> Any:
    """
    Select from a {'en': ..., 'fr': ...} dictionary. Useful for lists, dataframe
    column names and anything that is not a plain string.

        cols = pick({"en": ["Region", "Speed"], "fr": ["Région", "Vitesse"]})
    """
    return mapping.get(_LANG, mapping.get("en", default))


def rename(df, mapping: dict[str, tuple[str, str]]):
    """
    Rename DataFrame columns bilingually.

        df = rename(df, {"SoL": ("Sum of Lights", "Somme des lumières"),
                         "pop": ("Population", "Population")})

    Columns absent from the frame are ignored, so the same call is safe across
    laboratories that produce slightly different tables.
    """
    out = {k: (v[1] if _LANG == "fr" else v[0]) for k, v in mapping.items() if k in df.columns}
    return df.rename(columns=out)


# ---------------------------------------------------------------------------
#  Shared vocabulary — terms that recur across several laboratories.
#  Keeping them here means "Sum of Lights" is translated identically in the
#  Day 4 analysis notebook, the slide deck and the website glossary.
# ---------------------------------------------------------------------------
GLOSSARY: dict[str, tuple[str, str]] = {
    # Night-time lights
    "sol": ("Sum of Lights", "Somme des lumières"),
    "radiance": ("Radiance", "Radiance"),
    "lit_area": ("Lit area", "Superficie éclairée"),
    "mean_radiance": ("Mean radiance", "Radiance moyenne"),
    "blooming": ("Blooming", "Halo lumineux (blooming)"),
    "saturation": ("Saturation", "Saturation"),
    "gas_flare": ("Gas flare", "Torchère de gaz"),
    "cloud_mask": ("Cloud mask", "Masque nuageux"),
    "quality_flag": ("Quality flag", "Indicateur de qualité"),
    # Geography
    "adm0": ("National (ADM0)", "National (ADM0)"),
    "adm1": ("Region (ADM1)", "Région (ADM1)"),
    "adm2": ("District (ADM2)", "District (ADM2)"),
    "zonal_stats": ("Zonal statistics", "Statistiques zonales"),
    "boundaries": ("Administrative boundaries", "Frontières administratives"),
    # Connectivity
    "download_speed": ("Download speed", "Débit descendant"),
    "upload_speed": ("Upload speed", "Débit montant"),
    "latency": ("Latency", "Latence"),
    "quadkey": ("Quadkey", "Quadkey"),
    "tests": ("Tests", "Tests"),
    # Statistical practice
    "proxy": ("Proxy indicator", "Indicateur indirect (proxy)"),
    "coverage_bias": ("Coverage bias", "Biais de couverture"),
    "validation": ("Validation", "Validation"),
    "limitations": ("Limitations", "Limites"),
    "reproducibility": ("Reproducibility", "Reproductibilité"),
    "metadata": ("Metadata", "Métadonnées"),
    # AI
    "prompt_engineering": ("Prompt engineering", "Ingénierie de prompt"),
    "rag": ("Retrieval-Augmented Generation (RAG)",
            "Génération augmentée par récupération (RAG)"),
    "fine_tuning": ("Fine-tuning", "Affinage (fine-tuning)"),
    "agent": ("Agent", "Agent"),
    "hallucination": ("Hallucination", "Hallucination"),
    "grounding": ("Grounding", "Ancrage factuel"),
    "inference": ("Inference", "Inférence"),
    "token": ("Token", "Token"),
    "embedding": ("Embedding", "Plongement (embedding)"),
    "vector_store": ("Vector store", "Base vectorielle"),
}


def term(key: str) -> str:
    """Look up a shared term in the active language. Unknown keys return the key."""
    entry = GLOSSARY.get(key)
    if entry is None:
        return key
    return entry[1] if _LANG == "fr" else entry[0]


# ---------------------------------------------------------------------------
#  Standing phrases used by more than one notebook
# ---------------------------------------------------------------------------
PHRASES: dict[str, tuple[str, str]] = {
    "setup_ok": ("Environment ready.", "Environnement prêt."),
    "colab_detected": ("Google Colab detected — installing dependencies.",
                       "Google Colab détecté — installation des dépendances."),
    "kaggle_detected": ("Kaggle detected — using the /kaggle working directory.",
                        "Kaggle détecté — utilisation du répertoire de travail /kaggle."),
    "local_detected": ("Local environment detected.",
                       "Environnement local détecté."),
    "fallback_offered": (
        "Your national data is incomplete. Switching to the reference country "
        "so that you can finish the laboratory — see the note above.",
        "Vos données nationales sont incomplètes. Bascule sur le pays de référence "
        "pour vous permettre de terminer le laboratoire — voir la note ci-dessus.",
    ),
    "no_network": (
        "No network. Every step below works from the mirrored data on the USB key.",
        "Pas de réseau. Toutes les étapes ci-dessous fonctionnent depuis les données "
        "de la clé USB.",
    ),
    "deliverable": ("Team deliverable", "Livrable de l'équipe"),
    "checkpoint": ("Checkpoint — test yourself", "Point de contrôle — testez-vous"),
    "key_concept": ("Key concept", "Concept clé"),
    "warning": ("Watch out", "Attention"),
    "your_turn": ("Your turn", "À vous"),
    "limitations_title": ("Limitations and honest reading",
                          "Limites et lecture honnête"),
}


def phrase(key: str) -> str:
    entry = PHRASES.get(key)
    if entry is None:
        return key
    return entry[1] if _LANG == "fr" else entry[0]


# Honour an environment variable, so a notebook converted to a script, or a CI
# run, picks up the right language without editing code.
if os.environ.get("STG17_LANG"):
    set_lang(os.environ["STG17_LANG"])
