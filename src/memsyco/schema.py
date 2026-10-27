"""Data model for test cases, memory records, conditions and trial logs."""

from __future__ import annotations

from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel, Field, model_validator

LETTERS = "ABCDEFGH"

# "none" drops the evidence passage, to test items without supporting evidence.
EvidenceMode = Literal["as_written", "none"]


class Condition(str, Enum):
    """The six MS1 conditions for factual items, plus the two useful-memory conditions."""

    NO_BELIEF = "no_belief"
    STORED_INCORRECT = "stored_incorrect"
    STATED_INCORRECT = "stated_incorrect"
    STORED_INCORRECT_LABELLED = "stored_incorrect_labelled"
    STORED_UNRELATED = "stored_unrelated"
    STORED_CORRECT = "stored_correct"
    USEFUL_LABEL_OFF = "useful_label_off"
    USEFUL_LABEL_ON = "useful_label_on"


FACTUAL_CONDITIONS = [
    Condition.NO_BELIEF,
    Condition.STORED_INCORRECT,
    Condition.STATED_INCORRECT,
    Condition.STORED_INCORRECT_LABELLED,
    Condition.STORED_UNRELATED,
    Condition.STORED_CORRECT,
]
USEFUL_CONDITIONS = [Condition.USEFUL_LABEL_OFF, Condition.USEFUL_LABEL_ON]


class Beliefs(BaseModel):
    """User beliefs for a factual item, written as bare propositions (no trailing period)."""

    correct: str
    incorrect: str
    unrelated: str


class Case(BaseModel):
    """One test item. `options` uses canonical letters; display order is shuffled per trial."""

    id: str
    kind: Literal["factual", "preference", "correction"] = "factual"
    category: Literal["numerical", "logic", "science", "general", "preference", "correction"]
    question: str
    options: dict[str, str]
    answer: str
    # Option that matches the incorrect (or stale) belief; None for preference checks.
    incorrect_option: str | None = None
    evidence: str = ""
    evidence_strength: Literal["strong", "weak", "none"] = "strong"
    beliefs: Beliefs | None = None
    # Useful-memory checks: the stored record and any text the user brings this turn.
    memory_record: str | None = None
    user_context: str | None = None
    # True if the incorrect belief asserts something false; False if it denies something true.
    belief_affirms_false: bool | None = None
    status: Literal["draft", "verified"] = "draft"
    verified_by: list[str] = Field(default_factory=list)
    sources: list[str] = Field(default_factory=list)
    notes: str = ""

    @model_validator(mode="after")
    def _check(self) -> "Case":
        if not 2 <= len(self.options) <= len(LETTERS):
            raise ValueError(f"{self.id}: need 2-{len(LETTERS)} options")
        if list(self.options) != list(LETTERS[: len(self.options)]):
            raise ValueError(f"{self.id}: option keys must be A, B, C... in order")
        if self.answer not in self.options:
            raise ValueError(f"{self.id}: answer {self.answer!r} not in options")
        if self.incorrect_option is not None:
            if self.incorrect_option not in self.options:
                raise ValueError(f"{self.id}: incorrect_option not in options")
            if self.incorrect_option == self.answer:
                raise ValueError(f"{self.id}: incorrect_option equals answer")
        if self.kind == "factual":
            if self.beliefs is None or self.incorrect_option is None:
                raise ValueError(f"{self.id}: factual cases need beliefs and incorrect_option")
        else:
            if not self.memory_record:
                raise ValueError(f"{self.id}: useful-memory cases need memory_record")
        if self.status == "verified" and len(self.verified_by) < 2:
            raise ValueError(f"{self.id}: verified cases need two checkers in verified_by")
        return self


class BeliefRecord(BaseModel):
    """A stored memory record as the harness saves it. The label is stored, not baked into text."""

    case_id: str
    kind: Literal["correct", "incorrect", "unrelated", "useful"]
    text: str
    source: Literal["user_conversation"] = "user_conversation"
    label: str = "unverified_user_claim"


class ModelSpec(BaseModel):
    alias: str
    slug: str
    mode: Literal["chat", "completion"] = "chat"
    family: str = ""
    size: str = ""
    tuning: Literal["instruct", "base", "unknown"] = "instruct"
    notes: str = ""
    # Passed through to the API request body (e.g. OpenRouter `reasoning` settings).
    extra_body: dict[str, Any] = Field(default_factory=dict)


class GenerationParams(BaseModel):
    temperature: float = 0.7
    max_tokens: int = 600
    top_logprobs: int = 5


class TrialLog(BaseModel):
    """One line of trials.jsonl. Written before any interpretation beyond the auto-parse."""

    run_id: str
    trial_id: str
    case_id: str
    case_kind: str
    category: str
    condition: Condition
    label_on: bool
    model_alias: str
    model_slug: str
    rep: int
    evidence_mode: EvidenceMode = "as_written"
    # display letter -> canonical letter
    option_map: dict[str, str]
    request: dict[str, Any]
    params: GenerationParams
    started_at: str
    latency_s: float | None = None
    model_returned: str | None = None
    provider: str | None = None
    response_text: str | None = None
    reasoning_text: str | None = None
    finish_reason: str | None = None
    usage: dict[str, Any] | None = None
    # canonical letter -> probability, renormalised over the options, when logprobs came back
    option_probs: dict[str, float] | None = None
    # First few generated tokens with their top logprobs, as returned (for auditing option_probs)
    logprobs_head: list[dict[str, Any]] | None = None
    selected_display: str | None = None
    selected: str | None = None
    auto_score: Literal["correct", "accepted_incorrect", "other_wrong", "unparseable", "error"]
    error: str | None = None
