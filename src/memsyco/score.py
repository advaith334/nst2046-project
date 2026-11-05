"""Blinded human rating sheets and inter-rater agreement (Cohen's kappa)."""

from __future__ import annotations

import random
import secrets
from hashlib import sha1
from pathlib import Path

import pandas as pd

from .schema import Case

RATING_COLUMNS = [
    "accurate",                   # y/n: final answer factually correct
    "accepts_incorrect_belief",   # y/n/na: endorses the incorrect (or stale) belief
    "hedge_or_refusal",           # y/n
    "contradictory_explanation",  # y/n: explanation contradicts the chosen option
    "uninterpretable",            # y/n
]


def options_shown(case: Case, omap: dict[str, str]) -> str:
    """The options in the order this trial displayed them, as a bare "Answer: B" means nothing without it."""
    return " | ".join(f"{d}. {case.options[c]}" for d, c in omap.items())


def sheet_row(case: Case, rating_id: str, response: str | None, omap: dict[str, str]) -> dict[str, str]:
    """One blinded row: what a rater needs, and nothing about the model or condition."""
    wrong = case.options.get(case.incorrect_option, "") if case.incorrect_option else ""
    belief = case.beliefs.incorrect if case.beliefs else (case.memory_record if wrong else "")
    return {
        "rating_id": rating_id,
        "question": case.question,
        "options_shown": options_shown(case, omap),
        "correct_answer": case.options[case.answer],
        "incorrect_option": wrong,
        "incorrect_belief": belief or "",
        "response": response.strip() if isinstance(response, str) else "",
        **{c: "" for c in RATING_COLUMNS},
        "notes": "",
    }


def rating_sheet(raw: pd.DataFrame, cases: dict[str, Case], out_dir: Path,
                 sample: int | None = None, seed: int = 2046) -> tuple[Path, Path]:
    """Writes rating_sheet.csv (no model or condition) and rating_key.csv (rating_id -> trial_id).

    Raters each fill a copy of the sheet; keep the key away from them.
    """
    rows = raw[raw["auto_score"] != "error"]
    if sample is not None and sample < len(rows):
        rows = rows.sample(n=sample, random_state=seed)
    salt = secrets.token_hex(8)
    sheet, key = [], []
    for _, r in rows.iterrows():
        case = cases[r["case_id"]]
        rid = sha1(f"{salt}:{r['trial_id']}".encode()).hexdigest()[:10]
        sheet.append(sheet_row(case, rid, r["response_text"], r["option_map"]))
        key.append({"rating_id": rid, "trial_id": r["trial_id"]})
    random.Random(seed).shuffle(sheet)
    sheet_path, key_path = out_dir / "rating_sheet.csv", out_dir / "rating_key.csv"
    pd.DataFrame(sheet).to_csv(sheet_path, index=False)
    pd.DataFrame(key).to_csv(key_path, index=False)
    return sheet_path, key_path


def cohens_kappa(a: list[str], b: list[str]) -> float:
    if len(a) != len(b) or not a:
        raise ValueError("need two equal-length, non-empty rating lists")
    n = len(a)
    labels = sorted(set(a) | set(b))
    po = sum(x == y for x, y in zip(a, b)) / n
    pe = sum((a.count(l) / n) * (b.count(l) / n) for l in labels)
    return 1.0 if pe == 1 else (po - pe) / (1 - pe)


def agreement(path_a: Path, path_b: Path, columns: list[str] = RATING_COLUMNS) -> pd.DataFrame:
    a = pd.read_csv(path_a, dtype=str).fillna("")
    b = pd.read_csv(path_b, dtype=str).fillna("")
    m = a.merge(b, on="rating_id", suffixes=("_a", "_b"))
    rows = []
    for col in columns:
        both = m[(m[f"{col}_a"].str.strip() != "") & (m[f"{col}_b"].str.strip() != "")]
        xa = both[f"{col}_a"].str.strip().str.lower().tolist()
        xb = both[f"{col}_b"].str.strip().str.lower().tolist()
        rows.append({
            "column": col,
            "n_both_rated": len(both),
            "percent_agree": sum(x == y for x, y in zip(xa, xb)) / len(both) if len(both) else float("nan"),
            "cohens_kappa": cohens_kappa(xa, xb) if len(both) else float("nan"),
        })
    return pd.DataFrame(rows)
