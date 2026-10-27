"""Loading run configs, model registries and case files."""

from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import BaseModel, Field

from .schema import FACTUAL_CONDITIONS, Case, Condition, GenerationParams, ModelSpec


class RunConfig(BaseModel):
    name: str
    models_file: Path
    model_set: str
    case_files: list[Path]
    useful_memory_files: list[Path] = Field(default_factory=list)
    conditions: list[Condition] = Field(default_factory=lambda: list(FACTUAL_CONDITIONS))
    reps: int = 2
    seed: int = 2046
    shuffle_options: bool = True
    max_workers: int = 4
    base_url: str | None = None
    params: GenerationParams = Field(default_factory=GenerationParams)


def load_yaml(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_config(path: Path) -> RunConfig:
    cfg = RunConfig(**load_yaml(path))
    root = path.parent.parent if path.parent.name == "config" else path.parent
    resolve = lambda p: p if p.is_absolute() else root / p  # noqa: E731
    cfg.models_file = resolve(cfg.models_file)
    cfg.case_files = [resolve(p) for p in cfg.case_files]
    cfg.useful_memory_files = [resolve(p) for p in cfg.useful_memory_files]
    return cfg


def load_cases(paths: list[Path]) -> list[Case]:
    cases: list[Case] = []
    for path in paths:
        cases.extend(Case(**c) for c in load_yaml(path).get("cases", []))
    ids = [c.id for c in cases]
    dupes = {i for i in ids if ids.count(i) > 1}
    if dupes:
        raise ValueError(f"duplicate case ids: {sorted(dupes)}")
    return cases


def load_models(path: Path, model_set: str) -> list[ModelSpec]:
    data = load_yaml(path)
    registry = {m["alias"]: ModelSpec(**m) for m in data.get("models", [])}
    try:
        aliases = data["sets"][model_set]
    except KeyError:
        raise ValueError(f"model set {model_set!r} not in {path}") from None
    missing = [a for a in aliases if a not in registry]
    if missing:
        raise ValueError(f"unknown model aliases in set {model_set!r}: {missing}")
    return [registry[a] for a in aliases]
