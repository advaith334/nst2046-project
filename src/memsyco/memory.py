"""The memory harness: saves belief records with a label and source, retrieves them by case ID.

The "unverified" label is stored on the record and applied only in `render_record`, so the
labelled and unlabelled conditions differ in that prefix and nothing else.
"""

from __future__ import annotations

from collections import defaultdict
from functools import cache
from importlib import resources

from .schema import BeliefRecord, Case


@cache
def template(name: str) -> str:
    return resources.files("memsyco.prompts").joinpath(f"{name}.txt").read_text(encoding="utf-8")


class MemoryStore:
    def __init__(self) -> None:
        self._records: dict[str, list[BeliefRecord]] = defaultdict(list)

    def save(self, record: BeliefRecord) -> None:
        self._records[record.case_id].append(record)

    def retrieve(self, case_id: str, kind: str) -> list[BeliefRecord]:
        return [r for r in self._records[case_id] if r.kind == kind]

    @classmethod
    def from_cases(cls, cases: list[Case]) -> "MemoryStore":
        """Save every record a case can need: correct / incorrect / unrelated, or its useful record."""
        store = cls()
        for case in cases:
            if case.beliefs is not None:
                for kind in ("correct", "incorrect", "unrelated"):
                    belief = getattr(case.beliefs, kind)
                    text = template("belief_record").format(belief=belief)
                    store.save(BeliefRecord(case_id=case.id, kind=kind, text=text))
            if case.memory_record:
                store.save(BeliefRecord(case_id=case.id, kind="useful", text=case.memory_record))
        return store


def render_record(record: BeliefRecord, label_on: bool) -> str:
    label = template("label_prefix") if label_on else ""
    return template("memory_record").format(label=label, text=record.text)


def render_block(records: list[BeliefRecord], label_on: bool) -> str:
    lines = "\n".join(render_record(r, label_on) for r in records)
    return template("memory_block").format(records=lines)
