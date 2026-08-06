"""
STG17 · One interface, four inference providers.

The Day 2 benchmark asks participants to run the same prompt against two
providers and record latency, cost and quality. That comparison is only honest
if the *calling code* is identical — otherwise you are benchmarking your own
plumbing. This module is that identical calling code.

    from stg17.llm import chat, PROVIDERS

    answer = chat("Summarise this table in two sentences.", provider="groq")

Providers
---------
    groq        Named in the agenda. Its inference speed is the point of the
                Day 2 session: it changes what is feasible in a production
                statistical pipeline, not merely how long you wait.
    anthropic   Long context, used for the Day 2 document-extraction laboratory.
    openai      Any OpenAI-compatible endpoint — the comparison baseline.
    ollama      Local, on your own machine. No key, no network, no data leaving
                the building. The sovereign path discussed on Day 1 afternoon.

--------------------------------------------------------------------------
WHY THIS MODULE IS NOT A THIN WRAPPER
--------------------------------------------------------------------------
The four providers do not accept the same parameters, and pretending otherwise
produces code that works in the demo and fails in the laboratory. Two examples
participants meet directly:

  * **`temperature` is rejected outright by current Anthropic models.** Sending
    it returns HTTP 400. On Groq and OpenAI-compatible endpoints it is the
    normal way to control variability. A "portable" wrapper that always sends
    `temperature=0` breaks on one provider out of four.

  * **Reasoning is configured differently.** Anthropic models expose an
    *effort* setting (`low` … `max`) and decide their own thinking depth;
    OpenAI-compatible endpoints do not have that concept at all.

So `chat()` takes an intent — "be deterministic", "think hard about this" — and
translates it per provider. That translation is the teaching content, and it is
written out explicitly below rather than hidden, because the Day 2 session is
partly about *why* procurement comparisons between providers are hard.

Keys are never passed as arguments. They come from `stg17.env.get_secret()`,
which reads the Colab secret manager, the Kaggle secret manager, the process
environment, or a local `.env` — and never from a notebook cell.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any

from .env import get_secret
from .i18n import T

# ---------------------------------------------------------------------------
#  Provider registry
# ---------------------------------------------------------------------------
#: Default model per provider. Deliberately conservative choices: the workshop
#: is not a model bake-off, and a participant whose quota runs out mid-laboratory
#: has lost the session. Override per call with `model=`.
PROVIDERS: dict[str, dict[str, Any]] = {
    "anthropic": {
        "label": "Anthropic",
        "env": "ANTHROPIC_API_KEY",
        "package": "anthropic",
        "default_model": "claude-opus-5",
        "supports_temperature": False,   # current models reject it with a 400
        "supports_effort": True,
        "note_en": "Long context; used for the Day 2 document-extraction laboratory.",
        "note_fr": "Contexte long ; utilisé pour le laboratoire d'extraction documentaire du Jour 2.",
    },
    "groq": {
        "label": "Groq",
        "env": "GROQ_API_KEY",
        "package": "groq",
        "default_model": "llama-3.3-70b-versatile",
        "supports_temperature": True,
        "supports_effort": False,
        "note_en": "Very high tokens/second. The Day 2 benchmark exists to measure it.",
        "note_fr": "Débit très élevé en tokens/seconde. Le benchmark du Jour 2 sert à le mesurer.",
    },
    "openai": {
        "label": "OpenAI-compatible",
        "env": "OPENAI_API_KEY",
        "package": "openai",
        "default_model": "gpt-4o-mini",
        "supports_temperature": True,
        "supports_effort": False,
        "note_en": "Any endpoint speaking the OpenAI protocol — the comparison baseline.",
        "note_fr": "Tout point d'accès parlant le protocole OpenAI — la référence de comparaison.",
    },
    "ollama": {
        "label": "Ollama (local)",
        "env": "OLLAMA_HOST",
        "package": "requests",
        "default_model": "qwen2.5:7b",
        "supports_temperature": True,
        "supports_effort": False,
        "note_en": "Runs on your machine. No key, no network, no data leaving the building.",
        "note_fr": "Tourne sur votre machine. Aucune clé, aucun réseau, aucune donnée ne sort.",
    },
}

#: The order `chat()` tries when `provider="auto"`. Ollama last: it is the only
#: one that cannot fail for lack of a key, so it is the honest final fallback.
FALLBACK_ORDER = ("anthropic", "groq", "openai", "ollama")


# ---------------------------------------------------------------------------
#  Result
# ---------------------------------------------------------------------------
@dataclass
class Reply:
    """
    One model response, with everything the Day 2 comparison sheet needs.

    Deliberately carries `latency_s` and token counts rather than just the text:
    a benchmark that measures only quality is not a procurement input, and an
    office choosing a provider needs the three numbers together.
    """

    text: str
    provider: str
    model: str
    latency_s: float
    input_tokens: int | None = None
    output_tokens: int | None = None
    stop_reason: str | None = None
    raw: Any = field(default=None, repr=False)

    @property
    def total_tokens(self) -> int | None:
        if self.input_tokens is None or self.output_tokens is None:
            return None
        return self.input_tokens + self.output_tokens

    @property
    def tokens_per_second(self) -> float | None:
        """Output tokens per second — the number the Day 2 session is about."""
        if not self.output_tokens or self.latency_s <= 0:
            return None
        return self.output_tokens / self.latency_s

    def row(self) -> dict[str, Any]:
        """One row for the shared comparison sheet."""
        return {
            "provider": self.provider,
            "model": self.model,
            "latency_s": round(self.latency_s, 2),
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "tokens_per_s": round(self.tokens_per_second, 1) if self.tokens_per_second else None,
            "stop_reason": self.stop_reason,
        }

    def __str__(self) -> str:  # pragma: no cover - cosmetic
        return self.text


class ProviderUnavailable(RuntimeError):
    """
    Raised when a provider cannot be reached — no key, package absent, or down.

    Every laboratory catches this and takes its documented fallback path. A
    missing key must never end a session; that is the whole design rule.
    """


# ---------------------------------------------------------------------------
#  Availability
# ---------------------------------------------------------------------------
def available(provider: str) -> bool:
    """Is this provider usable right now — package installed and key present?"""
    spec = PROVIDERS.get(provider)
    if spec is None:
        return False
    import importlib.util  # noqa: PLC0415

    if importlib.util.find_spec(spec["package"]) is None:
        return False
    if provider == "ollama":
        return True   # no key; reachability is checked at call time
    return bool(get_secret(spec["env"]))


def status() -> list[tuple[str, str, str]]:
    """Rows for `stg17.ui.status_table` showing which providers this machine can use."""
    rows = []
    for name, spec in PROVIDERS.items():
        if available(name):
            rows.append((spec["label"], "ok", spec["default_model"]))
        else:
            import importlib.util  # noqa: PLC0415

            if importlib.util.find_spec(spec["package"]) is None:
                detail = T(f"pip install {spec['package']}", f"pip install {spec['package']}")
            else:
                detail = T(f"{spec['env']} not set", f"{spec['env']} non défini")
            rows.append((spec["label"], "warn", detail))
    return rows


def first_available(order: tuple[str, ...] = FALLBACK_ORDER) -> str | None:
    return next((p for p in order if available(p)), None)


# ---------------------------------------------------------------------------
#  The one call
# ---------------------------------------------------------------------------
def chat(prompt: str,
         system: str | None = None,
         provider: str = "auto",
         model: str | None = None,
         max_tokens: int = 4096,
         deterministic: bool = True,
         effort: str = "medium",
         messages: list[dict] | None = None) -> Reply:
    """
    Send one prompt and get one answer, from whichever provider is available.

    Parameters describe *intent*, not provider syntax — this is the layer that
    makes the Day 2 comparison fair:

    deterministic
        "Give me the same answer for the same input, as far as you can."
        Becomes `temperature=0` where that parameter exists, and is simply not
        sent to providers that reject it. Note that no provider guarantees
        identical output; determinism is a request, not a contract.
    effort
        "How hard should the model think?" — `low` | `medium` | `high` | `max`.
        Honoured natively by providers that expose a reasoning-effort setting;
        ignored elsewhere. It is not silently emulated by prompt injection,
        because a benchmark that changes the prompt per provider is measuring
        the wrong thing.

    Raises `ProviderUnavailable` rather than returning a plausible-looking
    empty string, so that a laboratory takes its fallback path explicitly.
    """
    if provider == "auto":
        chosen = first_available()
        if chosen is None:
            raise ProviderUnavailable(
                T("No LLM provider is available. Set one API key, or install and start "
                  "Ollama for the local path. Every laboratory that needs a model also "
                  "has a documented path that works without one.",
                  "Aucun fournisseur LLM n'est disponible. Définissez une clé API, ou "
                  "installez et démarrez Ollama pour la voie locale. Chaque laboratoire "
                  "utilisant un modèle dispose aussi d'un chemin documenté sans modèle.")
            )
        provider = chosen

    if provider not in PROVIDERS:
        raise ValueError(f"Unknown provider {provider!r}. Choose from: {', '.join(PROVIDERS)}")

    model = model or PROVIDERS[provider]["default_model"]
    turns = messages or [{"role": "user", "content": prompt}]

    dispatch = {
        "anthropic": _chat_anthropic,
        "groq": _chat_openai_compatible,
        "openai": _chat_openai_compatible,
        "ollama": _chat_ollama,
    }[provider]

    started = time.perf_counter()
    reply = dispatch(turns, system, provider, model, max_tokens, deterministic, effort)
    reply.latency_s = time.perf_counter() - started
    return reply


# ---------------------------------------------------------------------------
#  Anthropic
# ---------------------------------------------------------------------------
def _chat_anthropic(turns, system, provider, model, max_tokens, deterministic, effort) -> Reply:
    try:
        import anthropic  # noqa: PLC0415
    except ImportError as exc:
        raise ProviderUnavailable("pip install anthropic") from exc

    key = get_secret("ANTHROPIC_API_KEY")
    if not key:
        raise ProviderUnavailable("ANTHROPIC_API_KEY not set")

    client = anthropic.Anthropic(api_key=key)

    request: dict[str, Any] = {
        "model": model,
        "max_tokens": max_tokens,
        "messages": turns,
        # Effort controls how much the model thinks and how much it spends.
        # `medium` is the workshop default: it is the balance point, and a
        # laboratory that silently ran at `max` would give participants a
        # misleading impression of both cost and latency.
        "output_config": {"effort": effort},
    }
    if system:
        request["system"] = system

    # NOTE — no `temperature`. Current Anthropic models reject it with a 400.
    # `deterministic` is honoured on the providers that support it; here it is
    # deliberately dropped rather than faked, and this comment is the reason
    # the Day 2 benchmark discussion exists at all.
    _ = deterministic

    # Large outputs must stream: a long non-streaming request hits the HTTP
    # timeout and fails after the tokens have already been paid for.
    if max_tokens > 16000:
        with client.messages.stream(**request) as stream:
            response = stream.get_final_message()
    else:
        response = client.messages.create(**request)

    # A safety classifier can decline a request. That arrives as a normal
    # HTTP 200 with stop_reason "refusal" and an empty or partial content list —
    # so code that reads content[0] unconditionally breaks here, not at the
    # network layer. Check the stop reason first.
    if response.stop_reason == "refusal":
        return Reply(
            text=T("The provider declined this request.",
                   "Le fournisseur a décliné cette requête."),
            provider=provider, model=model, latency_s=0.0,
            stop_reason="refusal", raw=response,
        )

    text = "".join(block.text for block in response.content if block.type == "text")
    return Reply(
        text=text,
        provider=provider,
        model=response.model,
        latency_s=0.0,
        input_tokens=response.usage.input_tokens,
        output_tokens=response.usage.output_tokens,
        stop_reason=response.stop_reason,
        raw=response,
    )


# ---------------------------------------------------------------------------
#  Groq and any OpenAI-compatible endpoint
# ---------------------------------------------------------------------------
def _chat_openai_compatible(turns, system, provider, model, max_tokens,
                            deterministic, effort) -> Reply:
    """
    Groq and OpenAI share a wire protocol, so they share an implementation.

    That shared protocol is exactly why the Day 2 benchmark is worth running:
    identical code, identical prompt, and yet latency and cost per thousand
    documents differ by an order of magnitude between endpoints.
    """
    spec = PROVIDERS[provider]
    key = get_secret(spec["env"])
    if not key:
        raise ProviderUnavailable(f"{spec['env']} not set")

    messages = ([{"role": "system", "content": system}] if system else []) + list(turns)
    request: dict[str, Any] = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
    }
    if deterministic:
        request["temperature"] = 0     # accepted here; rejected by Anthropic
    _ = effort                          # no equivalent on this protocol

    try:
        if provider == "groq":
            from groq import Groq  # noqa: PLC0415

            client = Groq(api_key=key)
        else:
            from openai import OpenAI  # noqa: PLC0415

            client = OpenAI(api_key=key)
    except ImportError as exc:
        raise ProviderUnavailable(f"pip install {spec['package']}") from exc

    response = client.chat.completions.create(**request)
    choice = response.choices[0]
    usage = getattr(response, "usage", None)

    return Reply(
        text=choice.message.content or "",
        provider=provider,
        model=getattr(response, "model", model),
        latency_s=0.0,
        input_tokens=getattr(usage, "prompt_tokens", None),
        output_tokens=getattr(usage, "completion_tokens", None),
        stop_reason=getattr(choice, "finish_reason", None),
        raw=response,
    )


# ---------------------------------------------------------------------------
#  Ollama — the local, sovereign path
# ---------------------------------------------------------------------------
def _chat_ollama(turns, system, provider, model, max_tokens, deterministic, effort) -> Reply:
    """
    Talk to a model running on this machine.

    Present in the workshop for one reason: it is the only path where the
    microdata never leaves the building. Day 1 afternoon asks what an NSO
    actually needs to run this in production — memory, throughput, cost — and
    the answer is far more concrete once a participant has watched a 7-billion
    parameter model generate on their own laptop.
    """
    import requests  # noqa: PLC0415

    host = get_secret("OLLAMA_HOST") or "http://localhost:11434"
    messages = ([{"role": "system", "content": system}] if system else []) + list(turns)

    payload = {
        "model": model,
        "messages": messages,
        "stream": False,
        "options": {"num_predict": max_tokens, **({"temperature": 0} if deterministic else {})},
    }
    _ = effort

    try:
        response = requests.post(f"{host.rstrip('/')}/api/chat", json=payload, timeout=300)
        response.raise_for_status()
    except Exception as exc:  # noqa: BLE001
        raise ProviderUnavailable(
            T(f"Ollama not reachable at {host}. Start it with `ollama serve`, "
              f"then `ollama pull {model}`.",
              f"Ollama injoignable sur {host}. Démarrez-le avec `ollama serve`, "
              f"puis `ollama pull {model}`.")
        ) from exc

    data = response.json()
    return Reply(
        text=data.get("message", {}).get("content", ""),
        provider=provider,
        model=data.get("model", model),
        latency_s=0.0,
        input_tokens=data.get("prompt_eval_count"),
        output_tokens=data.get("eval_count"),
        stop_reason=data.get("done_reason"),
        raw=data,
    )


# ---------------------------------------------------------------------------
#  Benchmark helper — the Day 2 deliverable
# ---------------------------------------------------------------------------
def benchmark(prompt: str, providers: list[str] | None = None,
              system: str | None = None, repeats: int = 3,
              max_tokens: int = 512, verbose: bool = True):
    """
    Run the same prompt across several providers and return a comparison table.

    `repeats` defaults to 3 because a single timing is noise: first-call latency
    includes connection setup, and a provider judged on one sample will be judged
    wrong. The table reports the median, which is what belongs in a procurement
    note.

    Unavailable providers are reported as a row, not skipped silently — "we could
    not test this one" is itself a finding for an office deciding what to buy.
    """
    import statistics  # noqa: PLC0415

    import pandas as pd  # noqa: PLC0415

    providers = providers or [p for p in PROVIDERS if available(p)]
    rows = []

    for name in providers:
        if not available(name):
            rows.append({"provider": PROVIDERS[name]["label"], "status": "unavailable",
                         "median_latency_s": None, "tokens_per_s": None,
                         "output_tokens": None, "model": None})
            if verbose:
                print(T(f"  {name}: unavailable — skipped, and recorded as such",
                        f"  {name} : indisponible — ignoré, et consigné comme tel"))
            continue

        latencies, replies = [], []
        for attempt in range(repeats):
            try:
                reply = chat(prompt, system=system, provider=name, max_tokens=max_tokens)
            except ProviderUnavailable as exc:
                if verbose:
                    print(T(f"  {name}: failed on attempt {attempt + 1} — {exc}",
                            f"  {name} : échec à la tentative {attempt + 1} — {exc}"))
                break
            latencies.append(reply.latency_s)
            replies.append(reply)

        if not replies:
            rows.append({"provider": PROVIDERS[name]["label"], "status": "failed",
                         "median_latency_s": None, "tokens_per_s": None,
                         "output_tokens": None, "model": None})
            continue

        last = replies[-1]
        median = statistics.median(latencies)
        rows.append({
            "provider": PROVIDERS[name]["label"],
            "status": "ok",
            "model": last.model,
            "median_latency_s": round(median, 2),
            "output_tokens": last.output_tokens,
            "tokens_per_s": (round(last.output_tokens / median, 1)
                             if last.output_tokens and median > 0 else None),
        })
        if verbose:
            print(T(f"  {name}: {median:.2f}s median over {len(latencies)} run(s)",
                    f"  {name} : {median:.2f}s médian sur {len(latencies)} exécution(s)"))

    return pd.DataFrame(rows)


def cost_per_thousand(input_tokens: int, output_tokens: int,
                      price_in_per_mtok: float, price_out_per_mtok: float) -> float:
    """
    Cost of processing a thousand documents of this size, in the pricing currency.

    Kept explicit rather than table-driven on purpose: published prices change,
    and a hard-coded price table in a workshop repository is a wrong number
    waiting to be quoted in a procurement document. Participants read the
    current price from the provider and pass it in.
    """
    per_doc = (input_tokens * price_in_per_mtok + output_tokens * price_out_per_mtok) / 1e6
    return per_doc * 1000
