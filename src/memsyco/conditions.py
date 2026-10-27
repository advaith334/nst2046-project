"""Turns (case, condition, option order) into the exact request sent to a model.

Every condition is built from the same templates; only the belief block changes:

| condition                  | memory block            | user turn prefix        |
|----------------------------|-------------------------|-------------------------|
| no_belief                  | none                    | none                    |
| stored_incorrect           | incorrect, label off    | none                    |
| stated_incorrect           | none                    | "I believe that ..."    |
| stored_incorrect_labelled  | incorrect, label on     | none                    |
| stored_unrelated           | unrelated, label off    | none                    |
| stored_correct             | correct, label off      | none                    |
| useful_label_off / _on     | useful record           | case.user_context       |
"""

from __future__ import annotations

import random
from dataclasses import dataclass

from .memory import MemoryStore, render_block, template
from .schema import LETTERS, USEFUL_CONDITIONS, Case, Condition

# condition -> (memory record kind or None, label_on, stated)
_PLAN: dict[Condition, tuple[str | None, bool, bool]] = {
    Condition.NO_BELIEF: (None, False, False),
    Condition.STORED_INCORRECT: ("incorrect", False, False),
    Condition.STATED_INCORRECT: (None, False, True),
    Condition.STORED_INCORRECT_LABELLED: ("incorrect", True, False),
    Condition.STORED_UNRELATED: ("unrelated", False, False),
    Condition.STORED_CORRECT: ("correct", False, False),
    Condition.USEFUL_LABEL_OFF: ("useful", False, False),
    Condition.USEFUL_LABEL_ON: ("useful", True, False),
}


def label_on(condition: Condition) -> bool:
    return _PLAN[condition][1]


@dataclass
class Rendered:
    system: str
    user: str
    messages: list[dict[str, str]]
    prompt: str  # plain-text transcript for completion-mode (base) models


def option_map(case: Case, seed: str | int | None) -> dict[str, str]:
    """Display letter -> canonical letter. `seed=None` keeps canonical order."""
    canonical = list(case.options)
    order = canonical[:]
    if seed is not None:
        random.Random(seed).shuffle(order)
    return {LETTERS[i]: c for i, c in enumerate(order)}


def render(case: Case, condition: Condition, store: MemoryStore, omap: dict[str, str]) -> Rendered:
    if (case.kind == "factual") == (condition in USEFUL_CONDITIONS):
        raise ValueError(f"condition {condition.value} does not apply to {case.kind} case {case.id}")
    kind, is_labelled, stated = _PLAN[condition]

    system = template("system")
    memory = ""
    if kind is not None:
        records = store.retrieve(case.id, kind)
        if not records:
            raise ValueError(f"no {kind} record stored for {case.id}")
        memory = render_block(records, is_labelled)
        system = f"{system}\n\n{memory}"

    parts: list[str] = []
    if stated:
        assert case.beliefs is not None
        parts.append(template("stated_belief").format(belief=case.beliefs.incorrect))
    if case.user_context:
        parts.append(case.user_context)
    if case.evidence:
        parts.append(template("evidence").format(evidence=case.evidence))
    options = "\n".join(f"{d}. {case.options[c]}" for d, c in omap.items())
    parts.append(template("question").format(question=case.question, options=options))
    user = "\n\n".join(parts)

    prompt = template("completion").format(
        system=template("system"),
        memory=f"{memory}\n\n" if memory else "",
        user=user,
    )
    return Rendered(
        system=system,
        user=user,
        messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
        prompt=prompt,
    )
