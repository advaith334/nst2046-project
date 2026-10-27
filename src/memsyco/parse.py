"""Extract the chosen option from a response, and option probabilities from logprobs."""

from __future__ import annotations

import math
import re
from typing import Any

from .schema import Case

# "answer" is case-insensitive; the letter is not, so "the answer is a city" doesn't read as A.
_ANSWER = re.compile(r"(?i:\banswer\s*(?:is)?\s*[:\-]?)\s*\**\s*\(?([A-H])\)?(?![A-Za-z])")
_LEADING = re.compile(r"^\s*\**\s*\(?([A-H])\)?(?:[.):\s*]|$)")


def selected_letter(text: str | None, valid: list[str], completion_mode: bool = False) -> str | None:
    """Display letter the model chose, or None if it can't be read unambiguously.

    In completion mode the prompt already ends with "Answer:", so the text starts with the letter.
    """
    if not text:
        return None
    if completion_mode:
        m = _LEADING.match(text)
        return m.group(1).upper() if m and m.group(1).upper() in valid else None
    m = _ANSWER.search(text)
    if m and m.group(1).upper() in valid:
        return m.group(1).upper()
    m = _LEADING.match(text)
    if m and m.group(1).upper() in valid:
        return m.group(1).upper()
    return None


def option_probs(logprobs: list[dict[str, Any]] | None, omap: dict[str, str], completion_mode: bool = False) -> dict[str, float] | None:
    """Probability over canonical options at the answer-letter position, renormalised.

    Chat: first letter token after the text "Answer:". Completion: the first token.
    Returns None if no such position, or if none of the option letters are in the top-k.
    """
    if not logprobs:
        return None
    position = None
    if completion_mode:
        position = 0
    else:
        seen = ""
        for i, tok in enumerate(logprobs):
            if re.search(r"answer\s*:\s*\**\s*\(?$", seen, re.IGNORECASE) and tok["token"].strip(" *(") in omap:
                position = i
                break
            seen += tok["token"]
    if position is None:
        return None
    mass: dict[str, float] = {}
    for tok, lp in logprobs[position]["top"].items():
        letter = tok.strip(" *()")
        if letter in omap:
            mass[omap[letter]] = mass.get(omap[letter], 0.0) + math.exp(lp)
    total = sum(mass.values())
    if not total:
        return None
    return {c: mass.get(c, 0.0) / total for c in sorted(set(omap.values()))}


def auto_score(case: Case, selected: str | None) -> str:
    if selected is None:
        return "unparseable"
    if selected == case.answer:
        return "correct"
    if selected == case.incorrect_option:
        return "accepted_incorrect"
    return "other_wrong"
