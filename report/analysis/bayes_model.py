"""Bayesian hierarchical logistic model for model x condition. Run through run_all.sh.

Why this exists alongside GEE: Claude has no false answers at all and Gemma none at baseline, so
ordinary logistic maximum likelihood has no finite estimate for them (separation). Weakly
informative priors keep every estimate finite and let all six models stay in one model. For those
sparse models the log-odds effect is then mostly the prior, which the output reports explicitly.

Writes report/analysis/tables/t28_bayes_*.csv and bayes.json.
"""

from __future__ import annotations

import json
import os

os.environ.setdefault("XLA_FLAGS", "--xla_force_host_platform_device_count=4")

import jax
import jax.numpy as jnp
import numpy as np
import numpyro
import numpyro.distributions as dist
import pandas as pd
from jax.scipy.special import expit
from numpyro.diagnostics import summary
from numpyro.infer import MCMC, NUTS

from common import CONDITIONS, MODELS, SEED, TABLES, load_cases, load_run

numpyro.set_host_device_count(4)

df = load_run("r4_main", load_cases())
df = df[df.case_kind == "factual"].dropna(subset=["y"]).copy()
items = sorted(df.case_id.unique())
mi = df.model.map({m: i for i, m in enumerate(MODELS)}).to_numpy()
ci = df.condition.map({c: i for i, c in enumerate(CONDITIONS)}).to_numpy()
ii = df.case_id.map({c: i for i, c in enumerate(items)}).to_numpy()
fb = df.condition.isin(["stored_incorrect", "stated_incorrect", "stored_incorrect_labelled"]).astype(float).to_numpy()
y = df.y.to_numpy()
M, C, I = len(MODELS), len(CONDITIONS), len(items)


def eta_fn(alpha, beta_raw, s_u, s_v, s_w, u, v, w, mi, ci, ii, fb):
    beta = jnp.concatenate([jnp.zeros((M, 1)), beta_raw], axis=1)
    return alpha[mi] + beta[mi, ci] + s_u * u[ii] + s_v[mi % s_v.shape[0]] * v[mi, ii] + s_w[mi % s_w.shape[0]] * w[mi, ii] * fb


def model(sd, per_model=False, y=None):
    """per_model=True gives each model its own item-level spreads, which relaxes the shared-spread assumption."""
    alpha = numpyro.sample("alpha", dist.Normal(-2.0, 3.0).expand([M]).to_event(1))
    beta_raw = numpyro.sample("beta_raw", dist.Normal(0.0, sd).expand([M, C - 1]).to_event(2))
    s_u = numpyro.sample("s_u", dist.HalfNormal(1.5))  # item hardness shared across models
    shape = [M] if per_model else [1]
    s_v = numpyro.sample("s_v", dist.HalfNormal(1.5).expand(shape).to_event(1))  # item hardness specific to a model
    s_w = numpyro.sample("s_w", dist.HalfNormal(1.5).expand(shape).to_event(1))  # item-specific pull of a false belief
    u = numpyro.sample("u", dist.Normal(0, 1).expand([I]).to_event(1))
    v = numpyro.sample("v", dist.Normal(0, 1).expand([M, I]).to_event(2))
    w = numpyro.sample("w", dist.Normal(0, 1).expand([M, I]).to_event(2))
    numpyro.sample("y", dist.Bernoulli(logits=eta_fn(alpha, beta_raw, s_u, s_v, s_w, u, v, w, mi, ci, ii, fb)), obs=y)


def run(sd, seed, per_model=False):
    mcmc = MCMC(NUTS(model, target_accept_prob=0.92), num_warmup=1500, num_samples=1000, num_chains=4,
                chain_method="parallel", progress_bar=False)
    mcmc.run(jax.random.PRNGKey(seed), sd, per_model, y=jnp.asarray(y), extra_fields=("diverging",))
    return mcmc


def marginal_probs(s, draws=1000):
    """Population-averaged P(false answer) per model and condition over these 48 items."""
    n = s["alpha"].shape[0]
    pick = np.linspace(0, n - 1, draws).astype(int)
    out = np.zeros((draws, M, C))
    for k, t in enumerate(pick):
        beta = np.concatenate([np.zeros((M, 1)), np.asarray(s["beta_raw"][t])], axis=1)
        for m in range(M):
            for c in range(C):
                fb_c = float(CONDITIONS[c] in ("stored_incorrect", "stated_incorrect", "stored_incorrect_labelled"))
                sv, sw = s["s_v"][t], s["s_w"][t]
                eta = (s["alpha"][t][m] + beta[m, c] + s["s_u"][t] * s["u"][t] + sv[m % len(sv)] * s["v"][t][m] +
                       sw[m % len(sw)] * s["w"][t][m] * fb_c)
                out[k, m, c] = float(expit(eta).mean())
    return out


def q(x):
    return float(np.mean(x)), float(np.quantile(x, 0.025)), float(np.quantile(x, 0.975))


results, stored = {}, CONDITIONS.index("stored_incorrect") - 1
for tag, sd, seed, per_model in [("shared spreads, prior sd 2.5", 2.5, SEED, False), ("shared spreads, prior sd 5", 5.0, SEED + 1, False),
                                 ("per-model spreads, prior sd 2.5", 2.5, SEED + 2, True)]:
    mcmc = run(sd, seed, per_model)
    s = {k: np.asarray(v) for k, v in mcmc.get_samples().items()}
    grouped = mcmc.get_samples(group_by_chain=True)
    diag = summary({k: grouped[k] for k in ("alpha", "beta_raw", "s_u", "s_v", "s_w")}, group_by_chain=True)
    rhat = max(float(np.nanmax(v["r_hat"])) for v in diag.values())
    neff = min(float(np.nanmin(v["n_eff"])) for v in diag.values())
    div = int(np.asarray(mcmc.get_extra_fields()["diverging"]).sum())
    b = s["beta_raw"][:, :, stored]
    P = marginal_probs(s)
    rows = []
    for k, m in enumerate(MODELS):
        rd = P[:, k, CONDITIONS.index("stored_incorrect")] - P[:, k, CONDITIONS.index("no_belief")]
        l, lo, hi = q(b[:, k])
        r, rlo, rhi = q(rd)
        rows.append({"fit": tag, "model": m, "log_or": l, "log_or_low": lo, "log_or_high": hi,
                     "posterior_sd": float(b[:, k].std()), "prior_shrink": float(1 - b[:, k].var() / sd**2),
                     "marginal_rd": r, "rd_low": rlo, "rd_high": rhi})
    per_model_table = pd.DataFrame(rows)
    rows = []
    for a in range(M):
        for c in range(a + 1, M):
            d = b[:, a] - b[:, c]
            rd = (P[:, a, 1] - P[:, a, 0]) - (P[:, c, 1] - P[:, c, 0])
            l, lo, hi = q(d)
            r, rlo, rhi = q(rd)
            rows.append({"fit": tag, "contrast": f"{MODELS[a]} minus {MODELS[c]}", "log_or_diff": l, "low": lo, "high": hi,
                         "p_gt_0": float((d > 0).mean()), "rd_diff": r, "rd_low": rlo, "rd_high": rhi, "p_rd_gt_0": float((rd > 0).mean())})
    contrasts = pd.DataFrame(rows)
    results[tag] = {"rhat_max": rhat, "n_eff_min": neff, "divergences": div, "s_u": q(s["s_u"]),
                    "s_v": [q(s["s_v"][:, k]) for k in range(s["s_v"].shape[1])], "s_w": [q(s["s_w"][:, k]) for k in range(s["s_w"].shape[1])],
                    "per_model_table": per_model_table, "contrasts": contrasts}
    print(f"{tag}: rhat {rhat:.3f}, n_eff {neff:.0f}, divergences {div}")

pd.concat([results[k]["per_model_table"] for k in results]).to_csv(TABLES / "t28_bayes_stored_effect_by_model.csv", index=False)
pd.concat([results[k]["contrasts"] for k in results]).to_csv(TABLES / "t29_bayes_model_contrasts.csv", index=False)
(TABLES.parent / "bayes.json").write_text(json.dumps(
    {k: {x: y for x, y in v.items() if x not in ("per_model_table", "contrasts")} for k, v in results.items()}, indent=1))
