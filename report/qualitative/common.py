"""Shared loader for the qualitative analysis. Reads logs only; never calls an API."""
from __future__ import annotations

import json
import re
from pathlib import Path

import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / "runs" / "main-20261027"
OUT = Path(__file__).resolve().parent

LABEL = "[Unverified user claim — not checked against evidence]"
CONDS = ["no_belief", "stored_incorrect", "stated_incorrect", "stored_incorrect_labelled",
         "stored_unrelated", "stored_correct"]
MODELS = ["mistral-nemo", "mistral-small", "llama-8b", "gemma-moe", "qwen-small", "claude-sonnet"]


def load_cases() -> dict:
    return {c["id"]: c for c in yaml.safe_load(open(ROOT / "data/cases/longtail.yaml"))["cases"]}


def load_trials() -> pd.DataFrame:
    """One row per trial_id, keeping the successful attempt (the same one raw_table.csv uses)."""
    best: dict[str, dict] = {}
    for line in open(RUN / "trials.jsonl"):
        r = json.loads(line)
        tid = r["trial_id"]
        if tid not in best or best[tid].get("error") or not best[tid].get("response_text"):
            best[tid] = r
    keep = ["trial_id", "case_id", "case_kind", "category", "condition", "model_alias", "rep",
            "option_map", "request", "response_text", "reasoning_text", "finish_reason",
            "selected_display", "selected", "auto_score", "option_probs", "error", "usage"]
    df = pd.DataFrame([{k: r.get(k) for k in keep} for r in best.values()])
    df["response_text"] = df["response_text"].fillna("")
    df["reasoning_text"] = df["reasoning_text"].fillna("")
    return df


def enrich(df: pd.DataFrame, cases: dict) -> pd.DataFrame:
    """Adds option text, belief text and body (response minus the answer line) for factual trials."""
    df = df[df.case_kind == "factual"].copy()
    df["question"] = df.case_id.map(lambda c: cases[c]["question"])
    df["key_text"] = df.case_id.map(lambda c: str(cases[c]["options"][cases[c]["answer"]]))
    df["false_text"] = df.case_id.map(lambda c: str(cases[c]["options"][cases[c]["incorrect_option"]]))
    df["false_belief"] = df.case_id.map(lambda c: cases[c]["beliefs"]["incorrect"])
    df["true_belief"] = df.case_id.map(lambda c: cases[c]["beliefs"]["correct"])
    df["chosen_text"] = [str(cases[c]["options"].get(s, "")) if s else ""
                         for c, s in zip(df.case_id, df.selected)]
    return df


ANSWER_RE = re.compile(r"(?i:\banswer\s*(?:is)?\s*[:\-]?)\s*\**\s*\(?([A-H])\)?(?![A-Za-z])")


def answer_letters(text: str) -> list[str]:
    return [m.group(1) for m in ANSWER_RE.finditer(text or "")]


def body(text: str) -> str:
    """Response with the leading Answer line removed."""
    return re.sub(r"^\s*\**\s*(?i:answer)\s*(?:is)?\s*[:\-]?\s*\**\s*\(?[A-H]\)?[^\n]*\n?", "", text or "", count=1).strip()
