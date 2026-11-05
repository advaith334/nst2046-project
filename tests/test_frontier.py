"""Tests for the frontier tests F1-F4 (frontier/README.md), kept apart from the main study's tests."""

from pathlib import Path

import pytest

from memsyco.conditions import option_map, render
from memsyco.config import load_cases, load_config, load_models, load_yaml
from memsyco.frontier import prompt
from memsyco.memory import MemoryStore, template
from memsyco.schema import Condition

ROOT = Path(__file__).resolve().parent.parent
FRONTIER = ROOT / "frontier"


@pytest.fixture(scope="module")
def cases():
    cfg = load_config(ROOT / "config" / "pilot.yaml")
    return load_cases(cfg.case_files + cfg.useful_memory_files)


@pytest.fixture(scope="module")
def store(cases):
    return MemoryStore.from_cases(cases)


def by_id(cases, cid):
    return next(c for c in cases if c.id == cid)


class ScriptedClient:
    def __init__(self, *replies):
        from memsyco.client import Completion

        self.seen, self.replies = [], [Completion(text=r, usage={"cost": 0.5}) for r in replies]

    def complete(self, model, rendered, params):
        self.seen.append(rendered)
        return self.replies.pop(0)


def test_frontier_models_are_separate_and_track_b_matches_the_main_study():
    main = {m["alias"]: m for m in load_yaml(ROOT / "config" / "models.yaml")["models"]}
    data = load_yaml(FRONTIER / "config" / "models.yaml")
    frontier = {m["alias"]: m for m in data["models"]}
    # Models in both (track B, which includes Claude Sonnet, and the judge) copy the main registry exactly.
    shared = set(frontier) & set(main)
    assert shared == set(data["sets"]["main_models"]) | {"deepseek-flash"}
    for alias in shared:
        for key in ("slug", "mode"):
            assert frontier[alias].get(key) == main[alias].get(key), (alias, key)
        # The only allowed difference: Claude Sonnet's token limit (see frontier/config/models.yaml).
        body = dict(frontier[alias].get("extra_body") or {})
        if alias == "claude-sonnet":
            assert body.pop("max_tokens") == 8000
        assert body == (main[alias].get("extra_body") or {}), alias
    # Track B is the main study's set, with Llama on the follow-ups' host.
    main_set = load_yaml(ROOT / "config" / "models.yaml")["sets"]["main"]
    assert data["sets"]["main_models"] == [m.replace("llama-8b", "llama-8b-deepinfra") for m in main_set]


def test_headroom_items_match_their_builder():
    import importlib.util

    import yaml

    spec = importlib.util.spec_from_file_location("build_headroom", FRONTIER / "scripts" / "build_headroom.py")
    builder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(builder)
    committed = yaml.safe_load((FRONTIER / "data" / "headroom.yaml").read_text(encoding="utf-8"))
    assert committed["cases"] == builder.build()
    cases = load_cases([FRONTIER / "data" / "headroom.yaml"])
    assert len(cases) == 64 and all(c.options[c.incorrect_option] in c.beliefs.incorrect for c in cases)


def test_frontier_configs_use_main_study_settings():
    main = load_config(ROOT / "config" / "main.yaml")
    for name in ("screen", "probes"):
        for track, n in (("frontier", 4), ("main", 6)):
            cfg = load_config(FRONTIER / "config" / f"{name}_{track}.yaml")
            models = load_models(cfg.models_file, cfg.model_set)
            assert len(models) == n and cfg.params == main.params and cfg.seed == main.seed
            # Reasoning stays at each host's default, as Claude Sonnet ran in the main study.
            assert not any("reasoning" in m.extra_body for m in models)


@pytest.mark.parametrize("name", ["screen", "probes", "accommodation"])
def test_tracks_differ_only_in_models(name):
    a, b = (load_yaml(FRONTIER / "config" / f"{name}_{t}.yaml") for t in ("frontier", "main"))
    assert (a.pop("model_set"), b.pop("model_set")) == ("frontier_models", "main_models")
    assert a.pop("name").replace("frontier-", "") == b.pop("name").replace("mainmodels-", "")
    assert a == b


def test_selection_is_decided_by_frontier_models_only(tmp_path):
    import importlib.util

    import pandas as pd

    spec = importlib.util.spec_from_file_location("select_headroom", FRONTIER / "scripts" / "select_headroom.py")
    sel = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sel)
    sel.TARGET = tmp_path / "selected.yaml"
    frontier = load_yaml(FRONTIER / "config" / "models.yaml")["sets"]["frontier_models"]
    rows = []
    for model in [*frontier, "mistral-nemo"]:
        for case_id, frontier_score in (("fh_mult_1", "correct"), ("fh_mult_2", None)):
            # fh_mult_1: every frontier model always right, Nemo wrong -> not selected.
            # fh_mult_2: frontier models split right/wrong -> selected.
            for rep in (1, 2):
                score = ("accepted_incorrect" if model == "mistral-nemo" else
                         frontier_score or ("correct" if rep == 1 else "other_wrong"))
                rows.append({"case_id": case_id, "model_alias": model, "condition": "no_belief", "auto_score": score})
    pd.DataFrame(rows).to_csv(tmp_path / "raw_table.csv", index=False)
    sel.main(tmp_path)
    chosen = [c["id"] for c in load_yaml(sel.TARGET)["cases"]]
    assert chosen == ["fh_mult_2"]


def test_pushback_scores_the_second_answer_and_keeps_the_first(cases, store):
    from memsyco.frontier.probes import PushbackClient
    from memsyco.schema import GenerationParams, ModelSpec

    case = by_id(cases, "pilot_canberra")
    rendered = render(case, Condition.STORED_INCORRECT, store, option_map(case, None))
    inner = ScriptedClient("Answer: B", "Answer: A")
    got = PushbackClient(inner).complete(ModelSpec(alias="m", slug="v/m"), rendered, GenerationParams())
    first, second = inner.seen
    assert first.messages == rendered.messages
    assert second.messages[:2] == rendered.messages and second.messages[2] == {"role": "assistant", "content": "Answer: B"}
    assert second.messages[3] == {"role": "user", "content": prompt("pushback_turn")}
    assert got.text == "Answer: A" and got.usage["cost"] == 1.0 and got.transcript[0]["content"] == "Answer: B"


def test_awareness_probe_scores_the_first_answer(cases, store):
    from memsyco.frontier.probes import AwarenessClient, aware
    from memsyco.schema import GenerationParams, ModelSpec

    case = by_id(cases, "pilot_canberra")
    rendered = render(case, Condition.NO_BELIEF, store, option_map(case, None))
    inner = ScriptedClient("Answer: B", "YES. The question looks like a benchmark item.")
    got = AwarenessClient(inner).complete(ModelSpec(alias="m", slug="v/m"), rendered, GenerationParams())
    assert got.text == "Answer: B" and got.usage["cost"] == 1.0
    assert inner.seen[1].messages[-1] == {"role": "user", "content": prompt("awareness_question")}
    assert aware(got.transcript[-1]["content"]) is True
    assert aware("**No** - it reads like a real user.") is False and aware("Maybe.") is None


def test_accommodation_conditions_differ_only_in_memory():
    from memsyco.frontier.accommodation import CONDITIONS, judge_payload, load_items, render as render_acc

    items = load_items(FRONTIER / "data" / "accommodation.yaml")
    assert len(items) == 24 and {i.salience for i in items} == {"high", "low"}
    item = items[0]
    r = {c: render_acc(item, c) for c in CONDITIONS}
    for task in ("generate", "edit"):
        none, stored = r[f"{task}_none"], r[f"{task}_stored"]
        assert none.user == stored.user and none.system == prompt("assistant_system")
        assert stored.system == f"{none.system}\n\n" + template("memory_block").format(
            records="- " + template("belief_record").format(belief=item.false_claim))
    assert item.edit_draft in r["edit_none"].user and item.edit_draft not in r["generate_none"].user
    # The judge never sees the memory, so it can't tell the conditions apart.
    assert judge_payload(item, "edit_none", "x") == judge_payload(item, "edit_stored", "x")


def test_accommodation_parse_judgment():
    from memsyco.frontier.accommodation import parse_judgment

    assert parse_judgment('Sure: {"outcome": "fixes_silently", "rationale": "x"}') == "fixes_silently"
    assert parse_judgment('{"outcome": "maybe"}') is None and parse_judgment("no json") is None


def test_accommodation_dry_run_end_to_end(tmp_path):
    from memsyco.frontier.accommodation import FakeAccommodationClient, load_config as load_acc, run as run_acc, write_report

    cfg = load_acc(FRONTIER / "config" / "accommodation_frontier.yaml")
    path = run_acc(cfg, FakeAccommodationClient(), tmp_path, "t")
    n = len(path.read_text().splitlines())
    assert n == 24 * 4 * cfg.reps * len(load_models(cfg.models_file, cfg.model_set))
    run_acc(cfg, FakeAccommodationClient(), tmp_path, "t")
    assert len(path.read_text().splitlines()) == n
    summary = write_report(tmp_path)
    assert set(summary["memory"]) == {"none", "stored"} and (tmp_path / "paired.csv").exists()


def test_a_model_can_opt_out_of_logprobs():
    from memsyco.client import request_body
    from memsyco.conditions import Rendered
    from memsyco.schema import GenerationParams, ModelSpec

    models ={m["alias"]: ModelSpec(**m) for m in load_yaml(FRONTIER / "config" / "models.yaml")["models"]}
    rendered = Rendered(system="", user="hi", messages=[{"role": "user", "content": "hi"}], prompt="hi")
    params = GenerationParams(top_logprobs=5)
    terra = request_body(models["gpt-terra-openai"], rendered, params)
    assert "logprobs" not in terra and "top_logprobs" not in terra
    argon = request_body(models["gemini-argon"], rendered, params)
    assert argon["logprobs"] is True and argon["top_logprobs"] == 5
