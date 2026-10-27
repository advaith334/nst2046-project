"""Model access. One OpenAI-compatible client pointed at OpenRouter (or any compatible server,
e.g. a local Ollama for base models), plus a fake client for dry runs."""

from __future__ import annotations

import hashlib
import math
import os
import re
import time
from dataclasses import dataclass, field
from typing import Any, Protocol

from .conditions import Rendered
from .schema import LETTERS, GenerationParams, ModelSpec

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"


@dataclass
class Completion:
    text: str
    model_returned: str | None = None
    provider: str | None = None
    reasoning: str | None = None
    finish_reason: str | None = None
    usage: dict[str, Any] | None = None
    # Normalised: one entry per generated token, {"token": str, "top": {token: logprob}}
    logprobs: list[dict[str, Any]] | None = None
    latency_s: float = 0.0
    raw: dict[str, Any] = field(default_factory=dict)


class Client(Protocol):
    def complete(self, model: ModelSpec, rendered: Rendered, params: GenerationParams) -> Completion: ...


def request_body(model: ModelSpec, rendered: Rendered, params: GenerationParams) -> dict[str, Any]:
    """The exact body sent, also written to the trial log."""
    body: dict[str, Any] = {
        "model": model.slug,
        "temperature": params.temperature,
        "max_tokens": params.max_tokens,
        # No OpenRouter prompt transforms (e.g. middle-out compression); no tools, no web plugin.
        "transforms": [],
        **model.extra_body,
    }
    if model.mode == "chat":
        body["messages"] = rendered.messages
        if params.top_logprobs:
            body["logprobs"] = True
            body["top_logprobs"] = params.top_logprobs
    else:
        body["prompt"] = rendered.prompt
        if params.top_logprobs:
            body["logprobs"] = params.top_logprobs
    return body


class OpenAICompatClient:
    def __init__(self, base_url: str = OPENROUTER_BASE_URL, api_key: str | None = None, max_attempts: int = 5):
        import openai

        key = api_key or os.environ.get("OPENROUTER_API_KEY")
        if not key:
            raise RuntimeError("OPENROUTER_API_KEY is not set (copy .env.example to .env)")
        self._openai = openai
        self._client = openai.OpenAI(
            base_url=base_url,
            api_key=key,
            default_headers={"X-Title": "NST2046 memsyco"},
            max_retries=0,
            timeout=120,
        )
        self.max_attempts = max_attempts

    def complete(self, model: ModelSpec, rendered: Rendered, params: GenerationParams) -> Completion:
        body = request_body(model, rendered, params)
        retryable = (
            self._openai.RateLimitError,
            self._openai.APIConnectionError,
            self._openai.APITimeoutError,
            self._openai.InternalServerError,
        )
        for attempt in range(self.max_attempts):
            start = time.monotonic()
            try:
                if model.mode == "chat":
                    resp = self._client.chat.completions.create(**_split(body))
                else:
                    resp = self._client.completions.create(**_split(body))
                break
            except retryable:
                if attempt == self.max_attempts - 1:
                    raise
                time.sleep(min(60, 2**attempt))
        latency = time.monotonic() - start
        raw = resp.model_dump()
        choice = raw["choices"][0]
        if model.mode == "chat":
            msg = choice.get("message") or {}
            text = msg.get("content") or ""
            reasoning = msg.get("reasoning")
            lp = _norm_chat_logprobs(choice.get("logprobs"))
        else:
            text = choice.get("text") or ""
            reasoning = None
            lp = _norm_completion_logprobs(choice.get("logprobs"))
        return Completion(
            text=text,
            model_returned=raw.get("model"),
            provider=raw.get("provider"),
            reasoning=reasoning,
            finish_reason=choice.get("finish_reason"),
            usage=raw.get("usage"),
            logprobs=lp,
            latency_s=latency,
            raw=raw,
        )


def _split(body: dict[str, Any]) -> dict[str, Any]:
    """Move keys the openai SDK doesn't know into extra_body."""
    known = {"model", "messages", "prompt", "temperature", "max_tokens", "logprobs", "top_logprobs"}
    kwargs = {k: v for k, v in body.items() if k in known}
    extra = {k: v for k, v in body.items() if k not in known}
    if extra:
        kwargs["extra_body"] = extra
    return kwargs


def _norm_chat_logprobs(lp: dict[str, Any] | None) -> list[dict[str, Any]] | None:
    if not lp or not lp.get("content"):
        return None
    out = []
    for item in lp["content"]:
        top = {t["token"]: t["logprob"] for t in (item.get("top_logprobs") or [])}
        top.setdefault(item["token"], item["logprob"])
        out.append({"token": item["token"], "top": top})
    return out


def _norm_completion_logprobs(lp: dict[str, Any] | None) -> list[dict[str, Any]] | None:
    if not lp or not lp.get("tokens"):
        return None
    tops = lp.get("top_logprobs") or [{} for _ in lp["tokens"]]
    out = []
    for tok, tok_lp, top in zip(lp["tokens"], lp.get("token_logprobs") or [], tops):
        top = dict(top or {})
        if tok_lp is not None:
            top.setdefault(tok, tok_lp)
        out.append({"token": tok, "top": top})
    return out


class FakeClient:
    """Deterministic stand-in for --dry-run: picks a letter from a hash of the prompt."""

    def complete(self, model: ModelSpec, rendered: Rendered, params: GenerationParams) -> Completion:
        digest = hashlib.sha256((model.slug + rendered.prompt).encode()).digest()
        n = max(2, sum(1 for ln in rendered.user.splitlines() if re.match(r"^[A-H]\. ", ln)))
        letter = LETTERS[digest[0] % n]
        probs = [digest[i + 1] + 1 for i in range(n)]
        total = sum(probs)
        top = {LETTERS[i]: math.log(p / total) for i, p in enumerate(probs)}
        if model.mode == "chat":
            text = f"Answer: {letter}\nDry-run explanation."
            tokens = [{"token": "Answer", "top": {"Answer": 0.0}}, {"token": ":", "top": {":": 0.0}},
                      {"token": f" {letter}", "top": {f" {k}": v for k, v in top.items()}}]
        else:
            text = f" {letter}\nDry-run explanation."
            tokens = [{"token": f" {letter}", "top": {f" {k}": v for k, v in top.items()}}]
        return Completion(text=text, model_returned=model.slug, provider="dry-run", finish_reason="stop",
                          logprobs=tokens, latency_s=0.0)
