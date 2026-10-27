"""Expands cases x conditions x models x reps into fresh, independent requests and logs each one."""

from __future__ import annotations

import json
import random
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from .client import Client, request_body
from .conditions import label_on, option_map, render
from .config import RunConfig
from .memory import MemoryStore
from .parse import auto_score, option_probs, selected_letter
from .schema import USEFUL_CONDITIONS, Case, Condition, ModelSpec, TrialLog


@dataclass
class TrialSpec:
    case: Case
    condition: Condition
    model: ModelSpec
    rep: int

    @property
    def trial_id(self) -> str:
        return f"{self.case.id}|{self.condition.value}|{self.model.alias}|r{self.rep}"


def plan_trials(cfg: RunConfig, cases: list[Case], models: list[ModelSpec]) -> list[TrialSpec]:
    specs = []
    for model in models:
        for case in cases:
            conditions = cfg.conditions if case.kind == "factual" else USEFUL_CONDITIONS
            for condition in conditions:
                for rep in range(1, cfg.reps + 1):
                    specs.append(TrialSpec(case, condition, model, rep))
    random.Random(cfg.seed).shuffle(specs)
    return specs


def option_seed(cfg: RunConfig, case: Case, rep: int) -> str | None:
    # Same option order across conditions and models for a given case and rep, so option
    # position can't explain a condition effect; it varies between reps.
    return f"{cfg.seed}:{case.id}:r{rep}" if cfg.shuffle_options else None


def run_trial(spec: TrialSpec, cfg: RunConfig, store: MemoryStore, client: Client, run_id: str) -> TrialLog:
    case, model = spec.case, spec.model
    omap = option_map(case, option_seed(cfg, case, spec.rep))
    rendered = render(case, spec.condition, store, omap)
    completion_mode = model.mode == "completion"
    log = dict(
        run_id=run_id,
        trial_id=spec.trial_id,
        case_id=case.id,
        case_kind=case.kind,
        category=case.category,
        condition=spec.condition,
        label_on=label_on(spec.condition),
        model_alias=model.alias,
        model_slug=model.slug,
        rep=spec.rep,
        option_map=omap,
        request=request_body(model, rendered, cfg.params),
        params=cfg.params,
        started_at=datetime.now(timezone.utc).isoformat(),
    )
    try:
        comp = client.complete(model, rendered, cfg.params)
    except Exception as e:  # recorded, not dropped
        return TrialLog(**log, auto_score="error", error=f"{type(e).__name__}: {e}")

    display = selected_letter(comp.text, list(omap), completion_mode)
    selected = omap.get(display) if display else None
    return TrialLog(
        **log,
        latency_s=comp.latency_s,
        model_returned=comp.model_returned,
        provider=comp.provider,
        response_text=comp.text,
        reasoning_text=comp.reasoning,
        finish_reason=comp.finish_reason,
        usage=comp.usage,
        option_probs=option_probs(comp.logprobs, omap, completion_mode),
        selected_display=display,
        selected=selected,
        auto_score=auto_score(case, selected),
    )


def _git_state() -> dict[str, str | bool | None]:
    def git(*args: str) -> str | None:
        try:
            return subprocess.run(["git", *args], capture_output=True, text=True, check=True).stdout.strip()
        except (subprocess.CalledProcessError, FileNotFoundError):
            return None

    return {"commit": git("rev-parse", "HEAD"), "dirty": bool(git("status", "--porcelain"))}


def completed_ids(path: Path) -> set[str]:
    if not path.exists():
        return set()
    done = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        if row["auto_score"] != "error":
            done.add(row["trial_id"])
    return done


def run(
    cfg: RunConfig,
    cases: list[Case],
    models: list[ModelSpec],
    client: Client,
    out_dir: Path,
    run_id: str,
    limit: int | None = None,
    dry_run: bool = False,
) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    trials_path = out_dir / "trials.jsonl"
    store = MemoryStore.from_cases(cases)
    specs = plan_trials(cfg, cases, models)
    done = completed_ids(trials_path)
    todo = [s for s in specs if s.trial_id not in done][:limit]

    manifest = {
        "run_id": run_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "dry_run": dry_run,
        "git": _git_state(),
        "config": json.loads(cfg.model_dump_json()),
        "models": [m.model_dump() for m in models],
        "cases": [c.id for c in cases],
        "planned_trials": len(specs),
    }
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"{len(specs)} trials planned, {len(done)} already done, running {len(todo)}")

    errors = 0
    with open(trials_path, "a", encoding="utf-8") as f, ThreadPoolExecutor(cfg.max_workers) as pool:
        futures = [pool.submit(run_trial, s, cfg, store, client, run_id) for s in todo]
        for i, fut in enumerate(as_completed(futures), 1):
            row = fut.result()
            errors += row.auto_score == "error"
            f.write(row.model_dump_json() + "\n")
            f.flush()
            if i % 25 == 0 or i == len(todo):
                print(f"  {i}/{len(todo)} done ({errors} errors)")
    return trials_path
