"""
STG17 · Environment detection, dependency installation and secrets.

The same notebook has to run in four places without editing:

  * **Google Colab**       — the fallback path for restricted laptops
  * **Kaggle**             — where a GPU or a long run is needed (see docs/before/kaggle)
  * **a local machine**    — the normal path, reading the USB-key mirror
  * **plain CI**           — where notebooks are only validated, never executed

`setup()` works out which one it is in, installs what is missing, resolves the
data root, and returns a small object the rest of the notebook reads from.

Secrets are NEVER pasted into a cell. `get_secret()` looks, in order, at the
Colab secret manager, the Kaggle secret manager, the process environment, and
finally a local .env file. If none has the key it says so plainly and tells the
participant where to put it — it does not prompt, because a prompt in a
notebook that someone later commits is how keys end up on GitHub.
"""

from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

from .i18n import T, phrase


# ---------------------------------------------------------------------------
#  Where are we?
# ---------------------------------------------------------------------------
def in_colab() -> bool:
    return "google.colab" in sys.modules or bool(os.environ.get("COLAB_RELEASE_TAG"))


def in_kaggle() -> bool:
    return bool(os.environ.get("KAGGLE_KERNEL_RUN_TYPE")) or Path("/kaggle/input").exists()


def in_ci() -> bool:
    return bool(os.environ.get("CI")) or bool(os.environ.get("GITHUB_ACTIONS"))


def platform_name() -> str:
    if in_colab():
        return "colab"
    if in_kaggle():
        return "kaggle"
    if in_ci():
        return "ci"
    return "local"


def has_gpu() -> tuple[bool, str]:
    """
    Is a CUDA device visible, and which one?

    Reported by the environment check because it decides whether the Day 1
    fine-tuning demonstration is a two-minute exercise or a twenty-minute one.
    """
    try:
        import torch  # noqa: PLC0415

        if torch.cuda.is_available():
            return True, torch.cuda.get_device_name(0)
        return False, "CPU only"
    except ImportError:
        pass
    try:
        out = subprocess.run(
            ["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"],
            capture_output=True, text=True, timeout=10, check=False,
        )
        if out.returncode == 0 and out.stdout.strip():
            return True, out.stdout.strip().splitlines()[0]
    except (FileNotFoundError, subprocess.SubprocessError):
        pass
    return False, "CPU only"


# ---------------------------------------------------------------------------
#  Dependency installation
# ---------------------------------------------------------------------------
def missing(packages: list[str]) -> list[str]:
    """
    Which of these import names are not available?

    Takes *import* names, not pip names — they differ often enough
    (`sklearn` / `scikit-learn`, `PIL` / `pillow`) that guessing is a bug source.
    """
    return [p for p in packages if importlib.util.find_spec(p) is None]


def pip_install(specs: list[str], quiet: bool = True) -> bool:
    """Install pip specifications into the running interpreter. Returns success."""
    if not specs:
        return True
    cmd = [sys.executable, "-m", "pip", "install", "--upgrade", *(["-q"] if quiet else []), *specs]
    print(T(f"Installing: {', '.join(specs)}", f"Installation : {', '.join(specs)}"))
    result = subprocess.run(cmd, check=False)
    if result.returncode != 0:
        print(T("Installation failed. Try running the cell again, or use the "
                "Colab badge at the top of this notebook.",
                "Échec de l'installation. Relancez la cellule, ou utilisez le badge "
                "Colab en haut de ce carnet."))
        return False
    return True


def ensure(requirements: dict[str, str], quiet: bool = True) -> list[str]:
    """
    Ensure every dependency is importable, installing only what is missing.

    `requirements` maps import name -> pip specification, for example::

        {"geopandas": "geopandas>=0.14", "rasterio": "rasterio>=1.3", "h5py": "h5py"}

    Returns the list of packages it had to install, which the environment check
    reports so participants can see what changed on their machine.
    """
    absent = missing(list(requirements))
    if not absent:
        return []
    specs = [requirements[name] for name in absent]
    pip_install(specs, quiet=quiet)
    return absent


# ---------------------------------------------------------------------------
#  Secrets
# ---------------------------------------------------------------------------
class SecretMissing(RuntimeError):
    """Raised only when a secret is genuinely required and the lab cannot degrade."""


def get_secret(name: str, required: bool = False, hint: str = "") -> str | None:
    """
    Fetch an API key without ever putting it in the notebook.

    Search order: Colab Secrets -> Kaggle Secrets -> environment -> .env file.

    With `required=False` (the default) a missing key returns None and the
    laboratory takes its documented fallback path — the facilitator-run
    demonstration, or the offline dataset. Nothing crashes because a key failed,
    which is exactly the failure mode the concept note asks us to design out.
    """
    # 1. Colab secret manager (the left-hand key icon)
    if in_colab():
        try:
            from google.colab import userdata  # noqa: PLC0415

            value = userdata.get(name)
            if value:
                return value
        except Exception:  # noqa: BLE001 - secret absent or access not granted
            pass

    # 2. Kaggle secret manager (Add-ons -> Secrets)
    if in_kaggle():
        try:
            from kaggle_secrets import UserSecretsClient  # noqa: PLC0415

            value = UserSecretsClient().get_secret(name)
            if value:
                return value
        except Exception:  # noqa: BLE001
            pass

    # 3. Process environment
    value = os.environ.get(name)
    if value:
        return value

    # 4. A local .env sitting next to the notebook or at the repository root
    for candidate in (Path(".env"), Path("../.env"), Path("../../.env")):
        if candidate.exists():
            for line in candidate.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, _, val = line.partition("=")
                if key.strip() == name:
                    return val.strip().strip('"').strip("'")

    if required:
        raise SecretMissing(
            T(f"Secret {name!r} not found. {hint}",
              f"Secret {name!r} introuvable. {hint}")
        )
    return None


def secret_status(names: list[str]) -> list[tuple[str, str, str]]:
    """
    Rows for `stg17.ui.status_table` showing which keys are available.

    Only ever reports presence and the last four characters — never the key.
    """
    rows = []
    for name in names:
        value = get_secret(name)
        if value:
            rows.append((name, "ok", f"…{value[-4:]} ({len(value)} chars)"))
        else:
            rows.append((name, "warn", T("not set — fallback path will be used",
                                         "absent — le chemin de repli sera utilisé")))
    return rows


# ---------------------------------------------------------------------------
#  Data root
# ---------------------------------------------------------------------------
_ROOT_CANDIDATES = {
    "colab": ["/content/STG17_LOCAL", "/content/drive/MyDrive/STG17_LOCAL"],
    "kaggle": ["/kaggle/working/STG17_LOCAL", "/kaggle/input"],
    "local": ["C:/STG17_LOCAL", "~/STG17_LOCAL", "./STG17_LOCAL", "../STG17_LOCAL",
              "C:/NTL_LOCAL"],
    "ci": ["./STG17_LOCAL"],
}


def resolve_root(explicit: str | None = None, create: bool = True) -> Path:
    """
    Find the local data mirror.

    Order: an explicit argument, then the STG17_ROOT environment variable, then
    the platform's usual locations, preferring one that already holds data.
    `C:/NTL_LOCAL` is included for continuity with the June 2026 webinar
    material, where the HDF5 archive already lives at that path.
    """
    if explicit:
        root = Path(explicit).expanduser()
        if create:
            root.mkdir(parents=True, exist_ok=True)
        return root

    if os.environ.get("STG17_ROOT"):
        root = Path(os.environ["STG17_ROOT"]).expanduser()
        if create:
            root.mkdir(parents=True, exist_ok=True)
        return root

    candidates = [Path(c).expanduser() for c in _ROOT_CANDIDATES[platform_name()]]
    # Prefer a candidate that already contains something useful.
    for candidate in candidates:
        if candidate.exists() and any(candidate.iterdir()):
            return candidate
    for candidate in candidates:
        if candidate.exists():
            return candidate
    root = candidates[0]
    if create:
        root.mkdir(parents=True, exist_ok=True)
    return root


def mount_drive() -> Path | None:
    """
    Mount Google Drive in Colab, so a participant's downloads survive a runtime
    reset. Silently does nothing anywhere else.
    """
    if not in_colab():
        return None
    try:
        from google.colab import drive  # noqa: PLC0415

        drive.mount("/content/drive", force_remount=False)
        return Path("/content/drive/MyDrive")
    except Exception:  # noqa: BLE001
        return None


# ---------------------------------------------------------------------------
#  The one call every notebook makes
# ---------------------------------------------------------------------------
@dataclass
class Session:
    """Everything a notebook needs to know about where it is running."""

    platform: str
    root: Path
    gpu: bool
    gpu_name: str
    installed: list[str] = field(default_factory=list)
    lang: str = "en"

    @property
    def is_colab(self) -> bool:
        return self.platform == "colab"

    @property
    def is_kaggle(self) -> bool:
        return self.platform == "kaggle"

    def path(self, *parts) -> Path:
        """Build a path under the data root: session.path('h5_cache', 'CIV')."""
        return self.root.joinpath(*[str(p) for p in parts])

    def outputs(self, iso3: str, lab: str) -> Path:
        """
        Per-country, per-laboratory output directory — created on demand.

        Keeping outputs separated by laboratory is what makes the Friday commit
        to GitHub a single tidy folder rather than a scatter of files.
        """
        out = self.root / "outputs" / iso3.upper() / lab
        out.mkdir(parents=True, exist_ok=True)
        return out

    def summary(self) -> str:
        gpu = self.gpu_name if self.gpu else "CPU"
        return f"platform={self.platform} root={self.root} device={gpu} lang={self.lang}"


def setup(requirements: dict[str, str] | None = None,
          lang: str = "en",
          root: str | None = None,
          dark: bool = False,
          quiet: bool = True) -> Session:
    """
    The first executable cell of every notebook in this workshop.

    Detects the platform, installs missing dependencies, applies the AfDB
    matplotlib theme, sets the language for every subsequent human-readable
    string, and resolves the data root.

        S = setup({"geopandas": "geopandas>=0.14"}, lang="EN")

    Returns a `Session`. Print `S.summary()` if a technical assistant asks what
    your machine is doing.
    """
    from . import i18n, theme  # local import keeps module import cheap

    resolved_lang = i18n.set_lang(lang)
    installed = ensure(requirements or {}, quiet=quiet) if requirements else []
    theme.register_matplotlib(dark=dark)
    gpu, gpu_name = has_gpu()
    session = Session(
        platform=platform_name(),
        root=resolve_root(root),
        gpu=gpu,
        gpu_name=gpu_name,
        installed=installed,
        lang=resolved_lang,
    )

    banner = {
        "colab": phrase("colab_detected"),
        "kaggle": phrase("kaggle_detected"),
    }.get(session.platform, phrase("local_detected"))
    print(banner)
    print(f"  {T('Data root', 'Racine des données')} : {session.root}")
    print(f"  {T('Device', 'Processeur')}    : {gpu_name}")
    if installed:
        print(f"  {T('Installed', 'Installé')} : {', '.join(installed)}")
    print(phrase("setup_ok"))
    return session
