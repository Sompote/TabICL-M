"""Which function class does the regressor lose on?  Controlled synthetic regression tasks.

The 20-dataset benchmark shows TabPFN-3 ahead of TabICL-M on plain regression, most on
smooth low-noise targets (kin8nm, space_ga, diamonds). This script separates the possible
causes with synthetic tasks whose function class, dimension, training size and noise are
known:

  families   gp_short / gp_long  Gaussian-process samples (random Fourier features, RBF,
                                 lengthscale 0.5 / 2.0 in std units)
             sine_mlp            one-hidden-layer MLP with sine activation
             product             product of affine terms of 3 features
             loglinear           exp of a linear form (multiplicative, heavy tail)
             kinematic           planar chain: distance of the end effector, joint angles
                                 from the features (the kin8nm structure)
             step                sum of axis-aligned step functions (tree-like)
             linear_noisy        linear target with 50 % noise
  dims       1 and 8 input features (plus 2 irrelevant noise features)
  sizes      300 / 1000 / 3000 training rows, 1000 test rows
  noise      1 % of the signal std unless the family says otherwise

Each model runs on identical data (seeded). Metric: RMSE / std(y_test) (lower is better).
Models: tabicl_released (TabICLv2 regressor), tabicl_m (--aware_ckpt_reg), tabpfn3
(needs the tabpfn 8.x environment; the script is meant to be run once per environment
with --models and merged with --summarize).

Usage:
  python scripts/diag/function_class.py --out results/function_class --models tabicl_released tabicl_m \
      --aware_ckpt_reg checkpoints/tabicl-m-sa-20k/reg/step-10000.ckpt --device cuda
  /venv/tabpfn25/bin/python scripts/diag/function_class.py --out results/function_class --models tabpfn3 --device cuda
  python scripts/diag/function_class.py --out results/function_class --summarize
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

FAMILIES = ["gp_short", "gp_long", "sine_mlp", "product", "loglinear", "kinematic", "step", "linear_noisy"]
DIMS = [1, 8]
SIZES = [300, 1000, 3000]
N_TEST = 1000


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------
def make_task(family: str, dim: int, n_train: int, seed: int):
    rng = np.random.default_rng(seed * 1000 + FAMILIES.index(family) * 37 + dim)  # deterministic across processes
    n = n_train + N_TEST
    X = rng.normal(size=(n, dim))
    noise = 0.01
    if family.startswith("gp"):
        ls = 0.5 if family == "gp_short" else 2.0
        K = 512
        W = rng.normal(size=(dim, K)) / ls
        b = rng.uniform(0, 2 * math.pi, size=K)
        a = rng.normal(size=K)
        f = math.sqrt(2.0 / K) * np.cos(X @ W + b) @ a
    elif family == "sine_mlp":
        width = 32
        W1 = rng.normal(size=(dim, width)) * (1.5 / math.sqrt(dim))
        b1 = rng.normal(size=width) * 0.5
        w2 = rng.normal(size=width) / math.sqrt(width)
        f = np.sin(X @ W1 + b1) @ w2
    elif family == "product":
        m = min(3, dim)
        f = np.ones(n)
        for j in range(m):
            f = f * (rng.normal() + rng.uniform(0.5, 1.5) * X[:, j])
    elif family == "loglinear":
        beta = rng.uniform(-0.6, 0.6, size=dim)
        f = np.exp(X @ beta)
    elif family == "kinematic":
        angles = X * (math.pi / 2) * 0.8
        cum = np.cumsum(angles, axis=1)
        L = rng.uniform(0.5, 1.5, size=dim)
        f = np.sqrt((np.cos(cum) * L).sum(1) ** 2 + (np.sin(cum) * L).sum(1) ** 2)
    elif family == "step":
        f = np.zeros(n)
        for _ in range(6):
            j = rng.integers(dim)
            f = f + rng.normal() * (X[:, j] > rng.normal(scale=0.7))
    elif family == "linear_noisy":
        beta = rng.normal(size=dim)
        f = X @ beta
        noise = 0.5
    else:
        raise ValueError(family)
    f = (f - f.mean()) / (f.std() + 1e-12)
    y = f + noise * rng.normal(size=n)
    X = np.concatenate([X, rng.normal(size=(n, 2))], axis=1)  # two irrelevant features
    return X[:n_train], y[:n_train], X[n_train:], y[n_train:]


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------
def make_model(name: str, args, seed: int):
    if name in ("tabicl_released", "tabicl_m"):
        from tabicl import TabICLRegressor

        path = None if name == "tabicl_released" else args.aware_ckpt_reg
        if name == "tabicl_m" and not path:
            raise RuntimeError("tabicl_m needs --aware_ckpt_reg")
        return TabICLRegressor(model_path=path, n_estimators=args.n_estimators, device=args.device, random_state=seed)
    if name in ("tabpfn3", "tabpfn25"):
        from huggingface_hub import hf_hub_download
        from tabpfn import TabPFNRegressor

        ver, repo = {"tabpfn25": ("v2.5", "Prior-Labs/tabpfn_2_5"), "tabpfn3": ("v3", "Prior-Labs/tabpfn_3")}[name]
        path = hf_hub_download(repo, f"tabpfn-{ver}-regressor-{ver}_default.ckpt")
        return TabPFNRegressor(model_path=path, device=args.device or "cpu", random_state=seed)
    raise ValueError(name)


def run(args):
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"results_{'_'.join(args.models)}.csv"
    done = set()
    rows = []
    if path.exists():
        prev = pd.read_csv(path)
        rows = prev.to_dict("records")
        done = {(r["family"], r["dim"], r["n_train"], r["seed"], r["model"]) for r in rows}
    for family in args.families:
        for dim in args.dims:
            for n_train in args.sizes:
                for seed in args.seeds:
                    X_tr, y_tr, X_te, y_te = make_task(family, dim, n_train, seed)
                    for name in args.models:
                        key = (family, dim, n_train, seed, name)
                        if key in done:
                            continue
                        t0 = time.time()
                        try:
                            est = make_model(name, args, seed)
                            est.fit(X_tr, y_tr)
                            pred = np.asarray(est.predict(X_te), dtype=float)
                            rmse = float(np.sqrt(np.mean((pred - y_te) ** 2)))
                            err = None
                        except Exception as e:  # noqa: BLE001
                            rmse, err = float("nan"), repr(e)[:200]
                        rows.append(
                            dict(family=family, dim=dim, n_train=n_train, seed=seed, model=name,
                                 nrmse=rmse / (y_te.std() + 1e-12), time=time.time() - t0, error=err)
                        )
                        print(f"  {family:12s} d={dim} n={n_train:4d} seed={seed} {name:16s} nrmse={rows[-1]['nrmse']:.4f} ({rows[-1]['time']:.1f}s)"
                              + (f" ERROR {err}" if err else ""), flush=True)
                        pd.DataFrame(rows).to_csv(path, index=False)
    pd.DataFrame(rows).to_csv(path, index=False)


def summarize(args):
    out = Path(args.out)
    frames = [pd.read_csv(f) for f in out.glob("results_*.csv")]
    if not frames:
        print("no results")
        return
    df = pd.concat(frames, ignore_index=True)
    df = df[df.error.isna()].drop_duplicates(subset=["family", "dim", "n_train", "seed", "model"], keep="last")
    models = [m for m in ["tabicl_released", "tabicl_m", "tabpfn25", "tabpfn3"] if m in df.model.unique()]
    lines = ["# Function-class diagnostic", "",
             "Synthetic regression tasks with a known function class; metric RMSE / std(y) on 1000 test rows, "
             f"mean over seeds {sorted(df.seed.unique().tolist())}. Lower is better. "
             "`gap` = (tabicl_m - tabpfn3) / tabpfn3 in %, positive = we are worse.", ""]
    piv = df.pivot_table(index=["family", "dim", "n_train"], columns="model", values="nrmse")[models]

    def block(title, table):
        lines.extend([f"## {title}", "", "| " + " | ".join(table.index.names) + " | " + " | ".join(f"`{m}`" for m in models) + " | gap |",
                      "|" + "---|" * (len(table.index.names) + len(models) + 1)])
        for idx, r in table.iterrows():
            idx = idx if isinstance(idx, tuple) else (idx,)
            gap = ""
            if "tabpfn3" in r and "tabicl_m" in r and r["tabpfn3"] > 0:
                gap = f"{100 * (r['tabicl_m'] - r['tabpfn3']) / r['tabpfn3']:+.1f} %"
            lines.append("| " + " | ".join(str(i) for i in idx) + " | " + " | ".join(f"{r[m]:.3f}" for m in models) + f" | {gap} |")
        lines.append("")

    block("By family (mean over dims and sizes)", piv.groupby(level="family").mean())
    block("By dimension", piv.groupby(level="dim").mean())
    block("By training size", piv.groupby(level="n_train").mean())
    block("Every condition", piv)
    if "tabpfn3" in piv and "tabicl_m" in piv:
        gap = 100 * (piv["tabicl_m"] - piv["tabpfn3"]) / piv["tabpfn3"]
        fam = gap.groupby(level="family").mean().sort_values(ascending=False)
        lines += ["## Reading", "",
                  f"Largest gap: `{fam.index[0]}` ({fam.iloc[0]:+.1f} %); smallest: `{fam.index[-1]}` ({fam.iloc[-1]:+.1f} %).",
                  f"Gap by dimension: " + ", ".join(f"d={d}: {g:+.1f} %" for d, g in gap.groupby(level='dim').mean().items()) + ".",
                  f"Gap by size: " + ", ".join(f"n={n}: {g:+.1f} %" for n, g in gap.groupby(level='n_train').mean().items()) + ".", ""]
        verdict = {"by_family": fam.round(2).to_dict(),
                   "by_dim": gap.groupby(level="dim").mean().round(2).to_dict(),
                   "by_size": gap.groupby(level="n_train").mean().round(2).to_dict()}
        (out / "verdict.json").write_text(json.dumps(verdict, indent=1, default=str))
    (out / "summary.md").write_text("\n".join(lines))
    print("\n".join(lines))


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--out", default="results/function_class")
    p.add_argument("--models", nargs="+", default=["tabicl_released", "tabicl_m"],
                   choices=["tabicl_released", "tabicl_m", "tabpfn25", "tabpfn3"])
    p.add_argument("--families", nargs="+", default=FAMILIES, choices=FAMILIES)
    p.add_argument("--dims", nargs="+", type=int, default=DIMS)
    p.add_argument("--sizes", nargs="+", type=int, default=SIZES)
    p.add_argument("--seeds", nargs="+", type=int, default=[0, 1, 2])
    p.add_argument("--aware_ckpt_reg", default=None)
    p.add_argument("--n_estimators", type=int, default=8)
    p.add_argument("--device", default=None)
    p.add_argument("--summarize", action="store_true")
    args = p.parse_args(argv)
    if args.summarize:
        summarize(args)
    else:
        run(args)


if __name__ == "__main__":
    main()
