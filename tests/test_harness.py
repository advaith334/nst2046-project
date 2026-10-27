import json
from pathlib import Path

import pytest

from memsyco.conditions import option_map, render
from memsyco.config import load_cases, load_config, load_models
from memsyco.memory import MemoryStore, template
from memsyco.parse import auto_score, option_probs, selected_letter
from memsyco.schema import FACTUAL_CONDITIONS, USEFUL_CONDITIONS, Case, Condition
from memsyco.score import cohens_kappa

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "config" / "pilot.yaml"


@pytest.fixture(scope="module")
def cases():
    cfg = load_config(CONFIG)
    return load_cases(cfg.case_files + cfg.useful_memory_files)


@pytest.fixture(scope="module")
def store(cases):
    return MemoryStore.from_cases(cases)


def by_id(cases, cid):
    return next(c for c in cases if c.id == cid)


def test_cases_and_models_load(cases):
    cfg = load_config(CONFIG)
    assert len(load_models(cfg.models_file, cfg.model_set)) == 3
    assert {c.kind for c in cases} == {"factual", "preference", "correction"}


def test_label_is_the_only_difference(cases, store):
    case = by_id(cases, "pilot_canberra")
    omap = option_map(case, None)
    off = render(case, Condition.STORED_INCORRECT, store, omap)
    on = render(case, Condition.STORED_INCORRECT_LABELLED, store, omap)
    assert off.user == on.user
    assert on.system.replace(template("label_prefix"), "") == off.system
    assert template("label_prefix") in on.system


def test_stored_vs_stated_differ_only_in_placement(cases, store):
    case = by_id(cases, "logic_monty_hall")
    omap = option_map(case, None)
    base = render(case, Condition.NO_BELIEF, store, omap)
    stored = render(case, Condition.STORED_INCORRECT, store, omap)
    stated = render(case, Condition.STATED_INCORRECT, store, omap)
    assert stored.user == base.user and stated.system == base.system
    assert case.beliefs.incorrect in stored.system and case.beliefs.incorrect in stated.user
    assert stated.user.endswith(base.user)


def test_each_condition_uses_the_right_belief(cases, store):
    case = by_id(cases, "sci_seasons")
    omap = option_map(case, None)
    expect = {
        Condition.NO_BELIEF: None,
        Condition.STORED_UNRELATED: case.beliefs.unrelated,
        Condition.STORED_CORRECT: case.beliefs.correct,
    }
    for cond, belief in expect.items():
        r = render(case, cond, store, omap)
        if belief is None:
            assert "Saved memories" not in r.system
        else:
            assert belief in r.system and case.beliefs.incorrect not in r.system


def test_useful_conditions_only_apply_to_useful_cases(cases, store):
    fact, useful = by_id(cases, "pilot_canberra"), by_id(cases, "useful_correction_pluto")
    with pytest.raises(ValueError):
        render(fact, Condition.USEFUL_LABEL_ON, store, option_map(fact, None))
    with pytest.raises(ValueError):
        render(useful, Condition.STORED_INCORRECT, store, option_map(useful, None))
    r = render(useful, Condition.USEFUL_LABEL_OFF, store, option_map(useful, None))
    assert useful.memory_record in r.system and useful.user_context in r.user


def test_drop_evidence_removes_only_the_evidence(cases, store):
    case = by_id(cases, "sci_seasons")
    omap = option_map(case, None)
    full = render(case, Condition.STORED_INCORRECT, store, omap)
    bare = render(case, Condition.STORED_INCORRECT, store, omap, drop_evidence=True)
    assert case.evidence in full.user and case.evidence not in bare.user
    assert bare.system == full.system and full.user.endswith(bare.user)


def test_evidence_modes_in_plan():
    from memsyco.runner import plan_trials

    cfg = load_config(ROOT / "config" / "calibration.yaml")
    cases = load_cases(cfg.case_files)
    specs = plan_trials(cfg, cases, load_models(cfg.models_file, cfg.model_set))
    ids = [s.trial_id for s in specs]
    assert len(ids) == len(set(ids))
    no_ev = [c for c in cases if not c.evidence]
    expected = 3 * cfg.reps * len(cfg.conditions) * (2 * (len(cases) - len(no_ev)) + len(no_ev))
    assert len(specs) == expected
    assert any(i.endswith("|ev=none") for i in ids)


def test_option_shuffle_maps_back_to_key(cases):
    case = by_id(cases, "num_base_rate")
    omap = option_map(case, "2046:num_base_rate:r1")
    assert sorted(omap.values()) == sorted(case.options)
    assert omap == option_map(case, "2046:num_base_rate:r1")  # deterministic
    shown_answer = next(d for d, c in omap.items() if c == case.answer)
    assert omap[selected_letter(f"Answer: {shown_answer}\nbecause...", list(omap))] == case.answer


@pytest.mark.parametrize("text,expected", [
    ("Answer: B\nCanberra is...", "B"),
    ("**Answer:** (C) because", "C"),
    ("The answer is D.", "D"),
    ("B. Canberra", "B"),
    ("I think the answer is a city in the south.", None),
    ("Answer: E", None),
    ("Answer: D\n\n...so the count is 21, option B, not D.\n\nAnswer: B", "B"),
    ("", None),
])
def test_selected_letter(text, expected):
    assert selected_letter(text, ["A", "B", "C", "D"]) == expected


def test_selected_letter_completion_mode():
    assert selected_letter(" C\nExplanation", ["A", "B", "C", "D"], completion_mode=True) == "C"
    assert selected_letter(" Canberra", ["A", "B", "C", "D"], completion_mode=True) is None


def test_option_probs_maps_to_canonical():
    omap = {"A": "C", "B": "A", "C": "B"}
    lp = [{"token": "Answer", "top": {}}, {"token": ":", "top": {}},
          {"token": " A", "top": {" A": -0.1, " B": -2.5, " C": -5.0, " The": -3.0}}]
    probs = option_probs(lp, omap)
    assert max(probs, key=probs.get) == "C"  # display A is canonical C
    assert abs(sum(probs.values()) - 1) < 1e-9


def test_option_probs_when_host_drops_first_token():
    omap = {"A": "A", "B": "B"}
    lp = [{"token": ":", "top": {}}, {"token": " B", "top": {" B": -0.01, " A": -4.6}}]
    assert option_probs(lp, omap)["B"] > 0.9


def test_option_probs_rejects_tokens_that_dont_match_text():
    omap = {"A": "A", "B": "B"}
    lp = [{"token": " A", "top": {" A": -0.1}}, {"token": " and9", "top": {}}]
    assert option_probs(lp, omap, text="Answer: A\nThe numbers 9.11 and 9.9") is None
    good = [{"token": "Answer", "top": {}}, {"token": ":", "top": {}}, {"token": " A", "top": {" A": -0.1}}]
    assert option_probs(good, omap, text="Answer: A") == {"A": 1.0, "B": 0.0}


def test_auto_score(cases):
    case = by_id(cases, "pilot_canberra")
    assert auto_score(case, "B") == "correct"
    assert auto_score(case, "A") == "accepted_incorrect"
    assert auto_score(case, "C") == "other_wrong"
    assert auto_score(case, None) == "unparseable"


def test_verified_needs_two_checkers():
    base = dict(id="x", category="general", question="q", options={"A": "a", "B": "b"}, answer="A",
                incorrect_option="B", beliefs={"correct": "c", "incorrect": "i", "unrelated": "u"})
    with pytest.raises(ValueError):
        Case(**base, status="verified", verified_by=["Elkan"])
    assert Case(**base, status="verified", verified_by=["Elkan", "Aditya"])


def test_mcnemar_exact():
    from memsyco.report import mcnemar_exact

    assert mcnemar_exact(0, 0) == 1.0
    assert abs(mcnemar_exact(21, 1) - 1.1e-05) < 1e-06
    assert mcnemar_exact(5, 3) > 0.7


def test_cohens_kappa():
    assert cohens_kappa(["y", "n", "y", "n"], ["y", "n", "y", "n"]) == 1.0
    # Classic example: po = 0.7, pe = 0.5 -> kappa 0.4
    a = ["y"] * 5 + ["n"] * 5
    b = ["y"] * 4 + ["n"] + ["y"] * 2 + ["n"] * 3
    assert abs(cohens_kappa(a, b) - 0.4) < 1e-9


def test_dry_run_end_to_end(tmp_path, cases):
    from memsyco.client import FakeClient
    from memsyco.report import write_report
    from memsyco.runner import run

    cfg = load_config(CONFIG)
    models = load_models(cfg.models_file, cfg.model_set)
    path = run(cfg, cases, models, FakeClient(), tmp_path, "test", dry_run=True)
    rows = [json.loads(l) for l in path.read_text().splitlines()]
    n_fact = sum(c.kind == "factual" for c in cases)
    n_use = len(cases) - n_fact
    expected = len(models) * cfg.reps * (n_fact * len(FACTUAL_CONDITIONS) + n_use * len(USEFUL_CONDITIONS))
    assert len(rows) == expected
    assert all(r["auto_score"] != "error" for r in rows)
    # Resuming the same run does nothing new.
    run(cfg, cases, models, FakeClient(), tmp_path, "test", dry_run=True)
    assert len(path.read_text().splitlines()) == expected
    summary = write_report(tmp_path, {c.id: c for c in cases})
    assert set(summary["condition"]) == {c.value for c in FACTUAL_CONDITIONS + USEFUL_CONDITIONS}
    assert (tmp_path / "summary.md").exists() and (tmp_path / "raw_table.csv").exists()
