"""Build the confirmatory items from MMLU (Hendrycks et al., 2021; MIT licence).

Takes a seeded random sample from the test split of each subject group, so no item is chosen by
hand or written by an AI. The false option is also drawn at random, and belief sentences come
from one template. Writes data/external/mmlu/items.yaml, which is git-ignored; the seed and this
script rebuild it. Usage: uv run python scripts/build_mmlu_items.py
"""

import hashlib
import json
import random
import re
import time
import urllib.error
import urllib.request
from pathlib import Path

import yaml

SEED = 2046
PER_GROUP = 60
GROUPS = {
    "school": ["high_school_mathematics", "high_school_biology", "high_school_chemistry", "high_school_physics"],
    "health": ["clinical_knowledge", "nutrition", "human_aging"],
}
TARGET = Path("data/external/mmlu/items.yaml")
ROWS = "https://datasets-server.huggingface.co/rows?dataset=cais/mmlu&config={config}&split=test&offset={offset}&length=100"
# Options that only make sense next to the others, or that cannot be stated as a belief.
RELATIONAL = re.compile(r"\b(all|none|both|neither) of (the|these)|\babove\b|\bboth [a-d] and\b|^[a-d] and [a-d]$", re.I)


def fetch(config: str) -> list[dict]:
    """All test rows for a subject, cached so a rebuild does not depend on the rate limit."""
    cache = TARGET.with_name(f"raw_{config}.json")
    if cache.exists():
        return json.loads(cache.read_text(encoding="utf-8"))
    rows, offset = [], 0
    while True:
        for attempt in range(6):
            try:
                with urllib.request.urlopen(ROWS.format(config=config, offset=offset), timeout=60) as resp:
                    data = json.load(resp)
                break
            except urllib.error.HTTPError as e:
                if e.code != 429 or attempt == 5:
                    raise
                time.sleep(15 * (attempt + 1))
        rows += [r["row"] for r in data["rows"]]
        offset += 100
        if offset >= data["num_rows_total"]:
            cache.parent.mkdir(parents=True, exist_ok=True)
            cache.write_text(json.dumps(rows), encoding="utf-8")
            return rows


def usable(row: dict) -> bool:
    question, choices = row["question"].strip(), row["choices"]
    # A bare number beside sentence-length options is a corrupted row in the dataset.
    if any(re.fullmatch(r"[\d.,\s-]+", c) for c in choices) and any(len(c) > 20 for c in choices):
        return False
    return (len(choices) == 4 and len(question) <= 300 and "\n" not in question
            and all(0 < len(c) <= 80 and not RELATIONAL.search(c) for c in choices)
            and len({c.lower() for c in choices}) == 4 and "following" not in question.lower())


def belief(question: str, option: str) -> str:
    return f'the answer to "{question}" is {option}'


def build() -> list[dict]:
    rng = random.Random(SEED)
    items = []
    for group, configs in GROUPS.items():
        rows = ({"config": c, **r} for c in configs for r in fetch(c) if usable(r))
        unique = {r["question"].strip(): r for r in rows}  # MMLU repeats some questions
        pool = [unique[q] for q in sorted(unique)]
        for row in rng.sample(pool, PER_GROUP):
            question, choices = row["question"].strip(), [c.strip() for c in row["choices"]]
            false_index = rng.choice([i for i in range(4) if i != row["answer"]])
            items.append({"group": group, "config": row["config"], "question": question, "choices": choices,
                          "answer": row["answer"], "false": false_index})
    cases = []
    for i, item in enumerate(items):
        letters = "ABCD"
        other = items[(i + 7) % len(items)]
        digest = hashlib.sha1(item["question"].encode()).hexdigest()[:8]
        cases.append({
            "id": f"mmlu_{item['group']}_{digest}",
            "category": "general" if item["group"] == "health" else "science",
            "question": item["question"],
            "options": dict(zip(letters, item["choices"])),
            "answer": letters[item["answer"]],
            "incorrect_option": letters[item["false"]],
            "evidence_strength": "none",
            "beliefs": {
                "correct": belief(item["question"], item["choices"][item["answer"]]),
                "incorrect": belief(item["question"], item["choices"][item["false"]]),
                "unrelated": belief(other["question"], other["choices"][other["answer"]]),
            },
            "sources": [f"https://huggingface.co/datasets/cais/mmlu ({item['config']})"],
            "notes": item["group"],
        })
    return cases


if __name__ == "__main__":
    cases = build()
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    for group in GROUPS:
        part = TARGET.with_name(f"{group}.yaml")
        part.write_text(yaml.safe_dump({"cases": [c for c in cases if c["notes"] == group]}, allow_unicode=True, sort_keys=False), encoding="utf-8")
    text = yaml.safe_dump({"cases": cases}, allow_unicode=True, sort_keys=False)
    TARGET.write_text(text, encoding="utf-8")
    print(f"{len(cases)} items, sha256 {hashlib.sha256(text.encode()).hexdigest()}")
