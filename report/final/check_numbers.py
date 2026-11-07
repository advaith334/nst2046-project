#!/usr/bin/env python3
"""Check the report's key numbers against the result tables. Run from the repo root. Exits non-zero on a mismatch."""
import csv
import pathlib
import re
import sys

R = pathlib.Path(".")
tex = "".join(p.read_text() for p in sorted((R / "report/final/sections").glob("*.tex")))
pct = lambda x: int(float(x) * 100 + 0.5 if float(x) >= 0 else float(x) * 100 - 0.5)  # noqa: E731
rows = lambda f: list(csv.DictReader(open(R / f)))  # noqa: E731
sign = lambda v: (f"+{v}" if v > 0 else f"$-${abs(v)}" if v < 0 else "0")  # noqa: E731
need = []
for r in rows("report/analysis/confirm/tables/tests.csv"):
    if r["id"] in ("H1", "H2", "H3", "H4", "H5", "H6a", "H6b", "H6c", "H7a", "H7b", "H7c", "H7d", "H8"):
        need.append((r["id"], f"{sign(pct(r['est']))} [{sign(pct(r['ci_low']))}, {sign(pct(r['ci_high']))}]"))
for r in rows("tutoring/analysis/tables/tests.csv"):
    if r["id"] in ("T1", "T2", "T3", "T4"):
        need.append((r["id"], f"{sign(pct(r['est']))} [{sign(pct(r['ci_low']))}, {sign(pct(r['ci_high']))}]"))
m = {r["model"]: r for r in rows("tutoring/analysis/tables/reruns_models.csv")}
for key, name in (("mistral-nemo", "Nemo"), ("llama-8b-deepinfra", "Llama"), ("mistral-small", "Mistral Small"), ("claude-haiku", "Claude Haiku"), ("claude-sonnet", "Claude Sonnet")):
    r = m[key]
    a = lambda k: pct(r[k])  # noqa: E731
    need.append((key, f"{name} & {a('right_none')}\\% & {a('told_note_false')}\\% / {a('told_note_true')}\\% & {a('told_purpose_false')}\\% / {a('told_purpose_true')}\\% & {a('false2_none')}\\% / {a('false2_note_false')}\\%"))
for r in rows("tutoring/analysis/tables/frames_tests.csv"):
    if r["id"] != "R3":  # Nemo's assistant-frame rise is quoted as +7 without its interval.
        need.append((r["id"], f"{sign(pct(r['est']))} [{sign(pct(r['low']))}, {sign(pct(r['high']))}]"))
for r in rows("report/analysis/extra/tables/truth_sensitivity.csv"):
    if r["model"] in ("mistral-nemo", "llama-8b-deepinfra", "qwen-small"):
        need.append((r["model"] + " knew", f"+{pct(r['knew'])}"))
for r in rows("report/analysis/extra/tables/log_odds.csv"):
    need.append((r["arm"] + " push", f"{float(r['stored_incorrect']):.2f}"))
bad = [n for n in need if n[1] not in tex]
print(f"{len(need) - len(bad)} of {len(need)} found")
for n in bad:
    print("MISSING", n)
sys.exit(1 if bad else 0)
