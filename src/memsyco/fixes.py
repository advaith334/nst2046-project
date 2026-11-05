"""Harness-level fixes, as clients that wrap the real one, so each trial is logged like any other.

- `answer_first`: answer with no memory, then a second turn sees the memory and gives the final reply.
- `memory_gate`: a one-word classification call; memories about the outside world are withheld.

A third fix, a rule attached to the memory block, needs only a template and has no class here.
"""

from __future__ import annotations

from .client import Client, Completion
from .conditions import Rendered
from .memory import template
from .schema import GenerationParams, ModelSpec

GATE_PARAMS = GenerationParams(temperature=0.0, max_tokens=8, top_logprobs=0)


def split_memory(rendered: Rendered) -> tuple[str, str]:
    """The base system prompt and the memory block after it ("" if this condition has none)."""
    base = template("system")
    return base, rendered.system[len(base):].strip()


def _plain(system: str, user: str) -> Rendered:
    return Rendered(system=system, user=user, prompt="", messages=[
        {"role": "system", "content": system}, {"role": "user", "content": user}])


def _combined(final: Completion, earlier: Completion, note: str) -> Completion:
    """The final reply, with the earlier call's cost added and its output kept in the log."""
    usage = dict(final.usage or {})
    usage["cost"] = (usage.get("cost") or 0.0) + ((earlier.usage or {}).get("cost") or 0.0)
    final.usage = usage
    final.reasoning = note
    return final


class AnswerFirstClient:
    def __init__(self, inner: Client):
        self.inner = inner

    def complete(self, model: ModelSpec, rendered: Rendered, params: GenerationParams) -> Completion:
        base, memory = split_memory(rendered)
        if not memory:
            return self.inner.complete(model, rendered, params)
        draft = self.inner.complete(model, _plain(base, rendered.user), params)
        messages = [{"role": "system", "content": rendered.system}, {"role": "user", "content": rendered.user},
                    {"role": "assistant", "content": draft.text}, {"role": "user", "content": template("revise_turn")}]
        final = self.inner.complete(model, Rendered(system=rendered.system, user=rendered.user, messages=messages,
                                                    prompt=""), params)
        return _combined(final, draft, f"draft before memory: {draft.text}")


class MemoryGateClient:
    def __init__(self, inner: Client):
        self.inner = inner

    def complete(self, model: ModelSpec, rendered: Rendered, params: GenerationParams) -> Completion:
        base, memory = split_memory(rendered)
        if not memory:
            return self.inner.complete(model, rendered, params)
        gate = self.inner.complete(model, _plain("You classify saved memories.",
                                                 template("gate_question").format(memory=memory)), GATE_PARAMS)
        withheld = "FACT" in (gate.text or "").upper()
        final = self.inner.complete(model, _plain(base, rendered.user) if withheld else rendered, params)
        return _combined(final, gate, f"gate said {(gate.text or '').strip()!r}, memory {'withheld' if withheld else 'kept'}")


FIXES = {"answer_first": AnswerFirstClient, "memory_gate": MemoryGateClient}
