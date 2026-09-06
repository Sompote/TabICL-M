#!/usr/bin/env python
"""Ablation runner: how models cope with incomplete features.

Takes complete tables, deletes cells under a stated mechanism at a stated rate,
and compares models that handle the gaps in different ways. Also supports a real
multi-source table with leave-one-source-out (LOSO) splits and its natural
missingness.

Mechanisms
----------
mcar   cells removed independently of the data
mar    logistic in another observed column, intercept solved for the target rate
mnar   logistic in the column's own value (self-masking)
block  rows belong to K sources, each source lacks its own subset of columns
block_shift
       as block, and each source also carries an additive offset and extra noise on
       its numeric features (the per-source measurement effects of the prior)

Models
------
tabicl_impute      released TabICL, NaN mean-imputed by the sklearn wrapper (baseline)
tabicl_indicator   as above, plus one 0/1 missing-indicator column per incomplete feature
tabicl_iterimpute  released TabICL, NaN filled by sklearn's IterativeImputer fitted on train
tabicl_knnimpute   released TabICL, NaN filled by sklearn's KNNImputer fitted on train
tabicl_patternnorm released TabICL after pattern-conditional normalisation: rows sharing a
                   missingness pattern are one source, and every column is standardised
                   within its source (train and test pooled, no labels used); rare patterns
                   fall back to the pooled statistics. Tests whether the offset of a
                   held-out source can be removed by preprocessing alone.
tabicl_aware_zero  released weights inside the missing-aware architecture, new parameters
                   at zero: the architecture change alone, without any training
tabicl_aware       a checkpoint trained with --col_missing_aware (pass --aware_ckpt)
xgboost            native NaN handling
catboost           native NaN handling
tabpfn             TabPFN v2, native NaN handling (public weights, tabpfn==2.2.1)
tabpfn25 / tabpfn26 / tabpfn3
                   TabPFN 2.5 / 2.6 / 3 default checkpoints from Hugging Face (needs the
                   tabpfn>=8 package; weights are fetched with hf_hub_download)

Examples
--------
Synthetic ablation on built-in datasets::

    python scripts/ablation_missingness.py --out results/ablation \\
        --aware_ckpt checkpoints/tabicl-m.ckpt

Real multi-source table, leave-one-source-out, natural missingness::

    python scripts/ablation_missingness.py --out results/loso \\
        --csv data/compaction.csv --target rho_d_max --task regression \\
        --source_col lab --loso --natural

Splits
------
random   stratified random train/test split (default)
source   with block mechanisms: one whole synthetic source is held out as the test
         set (leave-one-source-out). The test rows then come from a source whose
         feature subset and measurement offset were never seen in the context.
         Other mechanisms fall back to the random split.

Outputs ``results.csv`` (one row per fit), ``summary.csv`` and ``summary.md``
(mean and standard deviation over seeds), and optional plots.
"""

from __future__ import annotations

import argparse
import json
import multiprocessing as mp
import sys
import time
import warnings
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)


# ---------------------------------------------------------------------------
# Missingness injection (numpy, exact target rate)
# ---------------------------------------------------------------------------


def _standardize(x: np.ndarray) -> np.ndarray:
    s = np.nanstd(x)
    if not np.isfinite(s) or s < 1e-8:
        return np.zeros_like(x, dtype=float)
    return (x - np.nanmean(x)) / s


def _sigmoid(z):
    return 1.0 / (1.0 + np.exp(-z))


def _logistic_mask(z: np.ndarray, rate: float, steepness: float, sign: float, rng) -> np.ndarray:
    """Bernoulli mask with p = sigmoid(sign * steepness * z + c), c solved so mean(p) = rate."""
    logits = sign * steepness * np.nan_to_num(z)
    lo, hi = -30.0, 30.0
    for _ in range(40):
        c = 0.5 * (lo + hi)
        if _sigmoid(logits + c).mean() < rate:
            lo = c
        else:
            hi = c
    p = _sigmoid(logits + 0.5 * (lo + hi))
    return rng.random(len(z)) < p


def inject_missingness(
    X: np.ndarray, mechanism: str, rate: float, rng: np.random.Generator, source: Optional[np.ndarray] = None
) -> Tuple[np.ndarray, Optional[np.ndarray]]:
    """Return (mask, source) where mask is True at cells to delete.

    ``X`` must be numeric and complete. The overall fraction of deleted cells is
    close to ``rate`` for every mechanism.
    """
    n, p = X.shape
    mask = np.zeros((n, p), dtype=bool)
    if rate <= 0:
        return mask, source

    if mechanism == "mcar":
        mask = rng.random((n, p)) < rate

    elif mechanism in ("mar", "mnar"):
        steep = 2.0
        for j in range(p):
            if mechanism == "mnar" or p == 1:
                driver = X[:, j]
            else:
                k = rng.choice([c for c in range(p) if c != j])
                driver = X[:, k]
            sign = 1.0 if rng.random() < 0.5 else -1.0
            mask[:, j] = _logistic_mask(_standardize(driver.astype(float)), rate, steep, sign, rng)

    elif mechanism in ("block", "block_shift"):
        K = int(rng.integers(2, 6))
        if source is None:
            source = rng.integers(0, K, size=n)
        else:
            K = int(source.max()) + 1
        n_drop = int(round(rate * p))
        n_drop = min(max(n_drop, 1 if rate > 0 else 0), p - 1)
        obs = np.ones((K, p), dtype=bool)
        for k in range(K):
            obs[k, rng.choice(p, size=n_drop, replace=False)] = False
        for j in range(p):  # every feature observed by at least one source
            if not obs[:, j].any():
                obs[rng.integers(K), j] = True
        mask = ~obs[source]

    else:
        raise ValueError(f"unknown mechanism {mechanism}")

    # Safety: keep at least two observed cells per column and one per row.
    for j in range(p):
        if (~mask[:, j]).sum() < 2:
            rows = np.flatnonzero(mask[:, j])
            mask[rng.choice(rows, size=min(2, len(rows)), replace=False), j] = False
    for i in range(n):
        if mask[i].all():
            mask[i, rng.integers(p)] = False
    return mask, source


def apply_source_shift(
    X: np.ndarray,
    source: np.ndarray,
    rng: np.random.Generator,
    shift_scale: float = 0.5,
    noise_scale: float = 0.3,
    max_categories: int = 20,
) -> np.ndarray:
    """Per-source additive offset and extra noise on numeric features.

    Mirrors the measurement effects of the prior (``tabicl.prior._missingness``):
    every source draws an offset ``N(0, shift_scale * std_j)`` per numeric feature
    ``j`` and a noise level ``U(0, noise_scale) * std_j``. Columns with at most
    ``max_categories`` distinct values are treated as categorical and left alone.
    """
    X = X.astype(float).copy()
    K = int(source.max()) + 1
    numeric = [j for j in range(X.shape[1]) if len(np.unique(X[:, j])) > max_categories]
    if not numeric:
        return X
    std = np.maximum(X[:, numeric].std(axis=0), 1e-8)
    offsets = rng.normal(size=(K, len(numeric))) * shift_scale * std
    X[:, numeric] += offsets[source]
    if noise_scale > 0:
        sigma = rng.random((K, 1)) * noise_scale * std
        X[:, numeric] += rng.normal(size=(len(X), len(numeric))) * sigma[source]
    return X


def split_by_source(source: np.ndarray, held_out: int) -> Tuple[np.ndarray, np.ndarray]:
    """Train on every source but ``held_out``, test on ``held_out``."""
    te = np.flatnonzero(source == held_out)
    tr = np.flatnonzero(source != held_out)
    return tr, te


def pattern_normalize(X_tr: np.ndarray, X_te: np.ndarray, min_rows: int = 8) -> Tuple[np.ndarray, np.ndarray]:
    """Standardise each column within the rows that share its missingness pattern.

    Train and test rows are pooled (only their features, never labels), so a source
    that appears only in the test set is centred on its own statistics. Patterns with
    fewer than ``min_rows`` rows, and columns with fewer than two observed cells in a
    group, use the pooled statistics of the whole table.
    """
    X = np.vstack([X_tr, X_te]).astype(float)
    pattern = np.isnan(X)
    keys, inverse, counts = np.unique(pattern, axis=0, return_inverse=True, return_counts=True)
    inverse = inverse.reshape(-1)
    g_mean, g_std = np.nanmean(X, axis=0), np.nanstd(X, axis=0)
    g_mean = np.nan_to_num(g_mean)
    g_std = np.where(np.isfinite(g_std) & (g_std > 1e-8), g_std, 1.0)
    out = (X - g_mean) / g_std
    for k in range(len(keys)):
        if counts[k] < min_rows:
            continue
        rows = inverse == k
        obs_cols = ~keys[k]
        sub = X[rows][:, obs_cols]
        m, sd = np.nanmean(sub, axis=0), np.nanstd(sub, axis=0)
        ok = (np.sum(~np.isnan(sub), axis=0) >= 2) & np.isfinite(sd) & (sd > 1e-8)
        cols = np.flatnonzero(obs_cols)[ok]
        out[np.ix_(rows, cols)] = (sub[:, ok] - m[ok]) / sd[ok]
    return out[: len(X_tr)], out[len(X_tr) :]


def add_indicators(X_tr: np.ndarray, X_te: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Append a 0/1 missing-indicator column for every feature with a NaN in train or test."""
    cols = np.flatnonzero(np.isnan(X_tr).any(axis=0) | np.isnan(X_te).any(axis=0))
    if len(cols) == 0:
        return X_tr, X_te
    return (
        np.hstack([X_tr, np.isnan(X_tr[:, cols]).astype(float)]),
        np.hstack([X_te, np.isnan(X_te[:, cols]).astype(float)]),
    )


# ---------------------------------------------------------------------------
# Datasets
# ---------------------------------------------------------------------------


def load_dataset(name: str, target: Optional[str], source_col: Optional[str], max_rows: int, rng):
    """Return dict(X, y, task, source, name). X is a float array; categoricals are ordinal-coded."""
    from sklearn import datasets as skd
    from sklearn.preprocessing import OrdinalEncoder

    source = None
    if name.startswith("csv:"):
        df = pd.read_csv(name[4:])
        assert target is not None, "--target is required for csv datasets"
        y = df[target].values
        if source_col is not None:
            source = df[source_col].astype(str).values
            df = df.drop(columns=[source_col])
        Xdf = df.drop(columns=[target])
        obj = Xdf.select_dtypes(exclude="number").columns
        if len(obj):
            Xdf[obj] = OrdinalEncoder(
                handle_unknown="use_encoded_value", unknown_value=-1, encoded_missing_value=np.nan
            ).fit_transform(Xdf[obj].astype(object))
        X = Xdf.values.astype(float)
        task = "classification" if (y.dtype.kind in "OUb" or len(np.unique(y)) <= 10) else "regression"
    elif name.startswith("openml:"):
        d = skd.fetch_openml(data_id=int(name[7:]), as_frame=True)
        Xdf, y = d.data, d.target.values
        obj = Xdf.select_dtypes(exclude="number").columns
        if len(obj):
            Xdf[obj] = OrdinalEncoder(
                handle_unknown="use_encoded_value", unknown_value=-1, encoded_missing_value=np.nan
            ).fit_transform(Xdf[obj].astype(object))
        X = Xdf.values.astype(float)
        task = "classification" if (y.dtype.kind in "OUb" or len(np.unique(y)) <= 10) else "regression"
    else:
        loaders = {
            "breast_cancer": (skd.load_breast_cancer, "classification"),
            "wine": (skd.load_wine, "classification"),
            "iris": (skd.load_iris, "classification"),
            "digits": (skd.load_digits, "classification"),
            "diabetes": (skd.load_diabetes, "regression"),
            "california": (getattr(skd, "fetch_california_housing", None), "regression"),
        }
        if name not in loaders or loaders[name][0] is None:
            raise ValueError(f"unknown dataset {name}; known: {sorted(loaders)}, csv:<path>, openml:<id>")
        d, task = loaders[name]
        d = d()
        X, y = np.asarray(d.data, dtype=float), np.asarray(d.target)

    if task == "classification":
        _, y = np.unique(y, return_inverse=True)
    else:
        y = y.astype(float)

    if max_rows and X.shape[0] > max_rows:
        idx = rng.choice(X.shape[0], size=max_rows, replace=False)
        X, y = X[idx], y[idx]
        source = source[idx] if source is not None else None
    # Drop constant columns and rows with NaN target
    keep = np.nanstd(X, axis=0) > 0
    X = X[:, keep]
    ok = ~np.isnan(y) if task == "regression" else np.ones(len(y), bool)
    X, y = X[ok], y[ok]
    source = source[ok] if source is not None else None
    return dict(X=X, y=y, task=task, source=source, name=name)


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


def _tree_worker(name: str, task: str, X_tr, y_tr, X_te, seed: int) -> Dict[str, np.ndarray]:
    """Fit a gradient-boosting baseline. Runs in a child process that never imports torch,
    because the Intel OpenMP runtime loaded by torch and the LLVM OpenMP runtime loaded by
    XGBoost deadlock when they share a process on macOS."""
    if name == "xgboost":
        import xgboost as xgb

        if task == "regression":
            est = xgb.XGBRegressor(n_estimators=300, learning_rate=0.05, max_depth=6, random_state=seed)
            est.fit(X_tr, y_tr)
            return {"mean": est.predict(X_te)}
        est = xgb.XGBClassifier(n_estimators=300, learning_rate=0.05, max_depth=6, random_state=seed)
        est.fit(X_tr, y_tr)
        return {"proba": est.predict_proba(X_te)}
    if name == "catboost":
        import catboost as cb

        kw = dict(iterations=500, learning_rate=0.05, depth=6, random_seed=seed, verbose=False)
        if task == "regression":
            est = cb.CatBoostRegressor(**kw)
            est.fit(X_tr, y_tr)
            return {"mean": est.predict(X_te)}
        est = cb.CatBoostClassifier(**kw)
        est.fit(X_tr, y_tr)
        return {"proba": est.predict_proba(X_te)}
    raise ValueError(name)


class ModelZoo:
    """Builds and runs the compared models. Returns predictions in a common format."""

    def __init__(self, args):
        self.args = args
        self._aware_zero_ckpt: Dict[str, Path] = {}
        self._pool = None

    def _tree_pool(self):
        if self._pool is None:
            self._pool = mp.get_context("spawn").Pool(1)
        return self._pool

    def close(self):
        if self._pool is not None:
            self._pool.close()
            self._pool.join()
            self._pool = None

    # -- checkpoints ---------------------------------------------------------
    def _plain_ckpt(self, task: str) -> Optional[str]:
        return self.args.plain_ckpt_reg if task == "regression" else self.args.plain_ckpt

    def _aware_ckpt(self, task: str) -> Optional[str]:
        return self.args.aware_ckpt_reg if task == "regression" else self.args.aware_ckpt

    def _aware_zero_ckpt_path(self, task: str) -> Path:
        """Released weights inside the missing-aware architecture, new parameters at zero."""
        if task in self._aware_zero_ckpt:
            return self._aware_zero_ckpt[task]
        import torch
        from tabicl import TabICLClassifier, TabICLRegressor
        from tabicl._model.tabicl import TabICL

        est = (TabICLRegressor if task == "regression" else TabICLClassifier)(
            model_path=self._plain_ckpt(task), device=self.args.device
        )
        est._load_model()  # resolves the released checkpoint (downloads if needed)
        ckpt = torch.load(est.model_path_, map_location="cpu", weights_only=True)
        config = dict(ckpt["config"])
        config["col_missing_aware"] = True
        model = TabICL(**config)
        kept = model.load_pretrained_state_dict(ckpt["state_dict"])
        out = Path(self.args.out) / f"aware_zero_{task}.ckpt"
        torch.save({"config": config, "state_dict": model.state_dict()}, out)
        print(f"[aware_zero] built {out} from {est.model_path_}; zero-initialised: {kept}")
        self._aware_zero_ckpt[task] = out
        return out

    # -- runners -------------------------------------------------------------
    def _tabicl(self, task, ckpt, seed):
        from tabicl import TabICLClassifier, TabICLRegressor

        cls = TabICLRegressor if task == "regression" else TabICLClassifier
        kw = dict(model_path=ckpt, n_estimators=self.args.n_estimators, device=self.args.device, random_state=seed)
        return cls(**kw)

    def run(self, name: str, task: str, X_tr, y_tr, X_te, seed: int) -> Dict[str, np.ndarray]:
        """Fit and predict. Returns dict with 'proba' (clf) or 'mean' and optional 'q10','q90' (reg)."""
        if name == "tabicl_indicator":
            X_tr, X_te = add_indicators(X_tr, X_te)
        elif name == "tabicl_patternnorm":
            X_tr, X_te = pattern_normalize(X_tr, X_te)
        elif name in ("tabicl_iterimpute", "tabicl_knnimpute"):
            from sklearn.experimental import enable_iterative_imputer  # noqa: F401
            from sklearn.impute import IterativeImputer, KNNImputer

            if name == "tabicl_iterimpute":
                imp = IterativeImputer(max_iter=10, random_state=seed, keep_empty_features=True)
            else:
                imp = KNNImputer(n_neighbors=5, keep_empty_features=True)
            X_tr = imp.fit_transform(X_tr)
            X_te = imp.transform(X_te)

        if name in (
            "tabicl_impute", "tabicl_indicator", "tabicl_patternnorm", "tabicl_iterimpute", "tabicl_knnimpute",
            "tabicl_aware", "tabicl_aware_zero",
        ):
            if name == "tabicl_aware":
                ckpt = self._aware_ckpt(task)
                if ckpt is None:
                    raise RuntimeError("tabicl_aware needs --aware_ckpt / --aware_ckpt_reg")
            elif name == "tabicl_aware_zero":
                ckpt = self._aware_zero_ckpt_path(task)
            else:
                ckpt = self._plain_ckpt(task)
            est = self._tabicl(task, ckpt, seed)
            est.fit(X_tr, y_tr)
            if task == "regression":
                out = est.predict(X_te, output_type=["mean", "quantiles"], alphas=[0.1, 0.9])
                return {"mean": out["mean"], "q10": out["quantiles"][:, 0], "q90": out["quantiles"][:, 1]}
            return {"proba": est.predict_proba(X_te)}

        if name in ("xgboost", "catboost"):
            if self.args.no_isolation:
                return _tree_worker(name, task, X_tr, y_tr, X_te, seed)
            return self._tree_pool().apply(_tree_worker, (name, task, X_tr, y_tr, X_te, seed))

        if name in ("tabpfn", "tabpfn25", "tabpfn26", "tabpfn3"):
            from tabpfn import TabPFNClassifier, TabPFNRegressor

            kw = dict(device=self.args.device or "cpu", random_state=seed)
            if name != "tabpfn":
                from huggingface_hub import hf_hub_download

                ver, repo = {
                    "tabpfn25": ("v2.5", "Prior-Labs/tabpfn_2_5"),
                    "tabpfn26": ("v2.6", "Prior-Labs/tabpfn_2_6"),
                    "tabpfn3": ("v3", "Prior-Labs/tabpfn_3"),
                }[name]
                kind = "regressor" if task == "regression" else "classifier"
                kw["model_path"] = hf_hub_download(repo, f"tabpfn-{ver}-{kind}-{ver}_default.ckpt")
            if task == "regression":
                est = TabPFNRegressor(**kw)
                est.fit(X_tr, y_tr)
                return {"mean": est.predict(X_te)}
            est = TabPFNClassifier(**kw)
            est.fit(X_tr, y_tr)
            return {"proba": est.predict_proba(X_te)}

        raise ValueError(f"unknown model {name}")


# ---------------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------------


def score(task: str, y_te: np.ndarray, out: Dict[str, np.ndarray], n_classes: int) -> Dict[str, float]:
    from sklearn.metrics import accuracy_score, log_loss, mean_squared_error, r2_score, roc_auc_score

    if task == "classification":
        proba = np.clip(out["proba"], 1e-7, 1 - 1e-7)
        proba = proba / proba.sum(axis=1, keepdims=True)
        pred = proba.argmax(axis=1)
        m = {"acc": accuracy_score(y_te, pred), "logloss": log_loss(y_te, proba, labels=np.arange(n_classes))}
        try:
            if n_classes == 2:
                m["auc"] = roc_auc_score(y_te, proba[:, 1])
            else:
                m["auc"] = roc_auc_score(y_te, proba, multi_class="ovr", average="macro", labels=np.arange(n_classes))
        except ValueError:
            m["auc"] = np.nan
        return m
    mean = out["mean"]
    m = {"rmse": float(np.sqrt(mean_squared_error(y_te, mean))), "r2": r2_score(y_te, mean)}
    if "q10" in out:
        inside = (y_te >= out["q10"]) & (y_te <= out["q90"])
        m["coverage80"] = float(inside.mean())
        m["width80"] = float(np.mean(out["q90"] - out["q10"]) / (np.std(y_te) + 1e-12))
    else:
        m["coverage80"] = np.nan
        m["width80"] = np.nan
    return m


# ---------------------------------------------------------------------------
# Experiment loops
# ---------------------------------------------------------------------------


def _split(n: int, test_size: float, rng, y=None, task="classification"):
    from sklearn.model_selection import train_test_split

    idx = np.arange(n)
    strat = y if (task == "classification" and y is not None) else None
    tr, te = train_test_split(idx, test_size=test_size, random_state=int(rng.integers(1 << 31)), stratify=strat)
    return tr, te


def run_synthetic(args, zoo: ModelZoo, data: dict, rows: List[dict]):
    X, y, task = data["X"], data["y"], data["task"]
    n_classes = len(np.unique(y)) if task == "classification" else 0
    mechanisms = ["none"] + args.mechanisms if args.include_complete else args.mechanisms
    split = getattr(args, "split", "random")
    for seed in args.seeds:
        rng = np.random.default_rng(seed)
        tr_rand, te_rand = _split(len(y), args.test_size, rng, y, task)
        for mech in mechanisms:
            rates = [0.0] if mech == "none" else args.rates
            for rate in rates:
                rng_m = np.random.default_rng(seed * 1000 + int(rate * 100))
                tr, te, held_out, source = tr_rand, te_rand, None, None
                Xs = X.astype(float)
                if mech in ("block", "block_shift"):
                    K = int(rng_m.integers(2, 6))
                    source = rng_m.integers(0, K, size=len(y))
                    if split == "source":
                        held_out = int(rng_m.integers(K))
                        tr, te = split_by_source(source, held_out)
                    if mech == "block_shift":
                        Xs = apply_source_shift(X, source, rng_m, args.shift_scale, args.noise_scale)
                mask, _ = inject_missingness(X, "mcar" if mech == "none" else mech, rate, rng_m, source=source)
                Xm = Xs.copy()
                Xm[mask] = np.nan
                if getattr(args, "add_source_col", False) and source is not None:
                    Xm = np.hstack([Xm, source[:, None].astype(float)])
                X_tr, X_te, y_tr, y_te = Xm[tr], Xm[te], y[tr], y[te]
                if task == "classification" and len(np.unique(y_tr)) < 2:
                    print(f"  ! skipping {data['name']}/{mech}/{rate}/seed{seed}: one class in train", file=sys.stderr)
                    continue
                for model in args.models:
                    t0 = time.time()
                    try:
                        out = zoo.run(model, task, X_tr, y_tr, X_te, seed)
                        metrics = score(task, y_te, out, n_classes)
                        err = ""
                    except Exception as e:  # keep going, record the failure
                        metrics, err = {}, f"{type(e).__name__}: {e}"
                        print(f"  ! {model} failed on {data['name']}/{mech}/{rate}/seed{seed}: {err}", file=sys.stderr)
                    rows.append(
                        dict(
                            dataset=data["name"],
                            task=task,
                            n_train=len(tr),
                            n_features=X.shape[1],
                            mechanism=mech,
                            rate=rate,
                            actual_rate=float(mask.mean()),
                            seed=seed,
                            split=split if mech in ("block", "block_shift") else "random",
                            held_out_source=held_out,
                            model=model,
                            seconds=time.time() - t0,
                            error=err,
                            **metrics,
                        )
                    )
                    print(
                        f"  {data['name']:>14} {mech:>5} rate={rate:.2f} seed={seed} {model:>18} "
                        + " ".join(f"{k}={v:.3f}" for k, v in metrics.items() if v == v)
                        + f"  ({time.time() - t0:.1f}s)",
                        flush=True,
                    )


def run_loso(args, zoo: ModelZoo, data: dict, rows: List[dict]):
    """Leave-one-source-out on a real multi-source table."""
    X, y, task, source = data["X"], data["y"], data["task"], data["source"]
    assert source is not None, "--loso needs --source_col"
    n_classes = len(np.unique(y)) if task == "classification" else 0
    sources, counts = np.unique(source, return_counts=True)
    held = [s for s, c in zip(sources, counts) if c >= args.min_source_rows]
    print(f"LOSO over {len(held)} sources with >= {args.min_source_rows} rows (of {len(sources)})")
    mechanisms = ["natural"] if args.natural else args.mechanisms
    for seed in args.seeds:
        for mech in mechanisms:
            rates = [0.0] if mech == "natural" else args.rates
            for rate in rates:
                Xm = X.astype(float).copy()
                if mech != "natural":
                    # inject on top of the natural gaps, using the real sources for block
                    _, src_codes = np.unique(source, return_inverse=True)
                    comp = np.where(np.isnan(Xm), np.nanmean(Xm, axis=0), Xm)
                    mask, _ = inject_missingness(comp, mech, rate, np.random.default_rng(seed), source=src_codes)
                    Xm[mask] = np.nan
                for s in held:
                    te = np.flatnonzero(source == s)
                    tr = np.flatnonzero(source != s)
                    if task == "classification" and len(np.unique(y[te])) < 1:
                        continue
                    for model in args.models:
                        t0 = time.time()
                        try:
                            out = zoo.run(model, task, Xm[tr], y[tr], Xm[te], seed)
                            metrics = score(task, y[te], out, n_classes)
                            err = ""
                        except Exception as e:
                            metrics, err = {}, f"{type(e).__name__}: {e}"
                            print(f"  ! {model} failed on source {s}: {err}", file=sys.stderr)
                        rows.append(
                            dict(
                                dataset=data["name"],
                                task=task,
                                n_train=len(tr),
                                n_features=X.shape[1],
                                mechanism=mech,
                                rate=rate,
                                actual_rate=float(np.isnan(Xm).mean()),
                                seed=seed,
                                model=model,
                                source=str(s),
                                n_test=len(te),
                                seconds=time.time() - t0,
                                error=err,
                                **metrics,
                            )
                        )
                        print(
                            f"  source={s!s:>12} n={len(te):>4} {model:>18} "
                            + " ".join(f"{k}={v:.3f}" for k, v in metrics.items() if v == v),
                            flush=True,
                        )


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------


def summarize(df: pd.DataFrame, out: Path):
    metric_cols = [c for c in ("auc", "acc", "logloss", "rmse", "r2", "coverage80", "width80") if c in df]
    keys = ["dataset", "task", "mechanism", "rate", "model"]
    ok = df[df["error"] == ""]
    if ok.empty:
        print("no successful fits to summarise")
        return
    g = ok.groupby(keys)[metric_cols]
    summary = g.mean().join(g.std(), rsuffix="_std").join(g.size().rename("n_fits")).reset_index()
    summary.to_csv(out / "summary.csv", index=False)

    has_source = "source" in df.columns and df["source"].notna().any()
    spread = "seeds and held-out sources" if has_source else "seeds"
    lines = ["# Missingness ablation", ""]
    for (ds, task), sub in summary.groupby(["dataset", "task"]):
        main = "auc" if task == "classification" else "rmse"
        if main not in sub:
            continue
        lines += [f"## {ds} ({task}), {main} mean ± std over {spread}", ""]
        piv = sub.pivot_table(index=["mechanism", "rate"], columns="model", values=main)
        piv_std = sub.pivot_table(
            index=["mechanism", "rate"], columns="model", values=f"{main}_std", dropna=False
        ).reindex(index=piv.index, columns=piv.columns)
        header = "| mechanism | rate | " + " | ".join(piv.columns) + " |"
        lines += [header, "|" + "---|" * (len(piv.columns) + 2)]
        for idx, r in piv.iterrows():
            cells = []
            for m in piv.columns:
                v, s = r[m], piv_std.loc[idx, m]
                cells.append("" if v != v else (f"{v:.3f} ± {s:.3f}" if s == s else f"{v:.3f}"))
            lines.append(f"| {idx[0]} | {idx[1]:.2f} | " + " | ".join(cells) + " |")
        lines.append("")
        if task == "regression" and "coverage80" in sub:
            cov = sub.pivot_table(index=["mechanism", "rate"], columns="model", values="coverage80")
            lines += ["Coverage of the 80 % interval (target 0.80):", ""]
            lines += ["| mechanism | rate | " + " | ".join(cov.columns) + " |", "|" + "---|" * (len(cov.columns) + 2)]
            for idx, r in cov.iterrows():
                lines.append(
                    f"| {idx[0]} | {idx[1]:.2f} | " + " | ".join("" if v != v else f"{v:.2f}" for v in r.values) + " |"
                )
            lines.append("")
    if has_source:
        lines += ["## Per held-out source", ""]
        for (ds, task, mech, rate), sub in ok.groupby(["dataset", "task", "mechanism", "rate"]):
            main = "auc" if task == "classification" else "rmse"
            if main not in sub:
                continue
            piv = sub.pivot_table(index="source", columns="model", values=main)
            n_te = sub.groupby("source")["n_test"].first().reindex(piv.index)
            lines += [f"{ds} · {mech} · rate {rate:.2f} · {main} (mean over seeds)", ""]
            lines += ["| source | n_test | " + " | ".join(piv.columns) + " |", "|" + "---|" * (len(piv.columns) + 2)]
            for src, r in piv.iterrows():
                lines.append(
                    f"| {src} | {int(n_te[src])} | " + " | ".join("" if v != v else f"{v:.3f}" for v in r.values) + " |"
                )
            lines.append("")
    failures = df[df["error"] != ""]
    if not failures.empty:
        lines += ["## Failed fits", ""]
        for _, r in failures.iterrows():
            lines.append(f"- {r['dataset']} / {r['mechanism']} / {r['rate']} / seed {r['seed']} / {r['model']}: {r['error']}")
    (out / "summary.md").write_text("\n".join(lines))
    print("\n".join(lines))


def plot(df: pd.DataFrame, out: Path):
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not installed, skipping plots")
        return
    ok = df[df["error"] == ""]
    (out / "plots").mkdir(exist_ok=True)
    for (ds, task), sub in ok.groupby(["dataset", "task"]):
        main = "auc" if task == "classification" else "rmse"
        if main not in sub:
            continue
        mechs = sorted(m for m in sub["mechanism"].unique() if m != "none")
        if not mechs:
            continue
        complete = sub[sub["mechanism"] == "none"]  # complete-data point at rate 0 on every panel
        fig, axes = plt.subplots(1, len(mechs), figsize=(4.2 * len(mechs), 3.4), sharey=True, squeeze=False)
        for ax, mech in zip(axes[0], mechs):
            s = pd.concat([complete, sub[sub["mechanism"] == mech]])
            for model, sm in s.groupby("model"):
                g = sm.groupby("rate")[main]
                ax.errorbar(g.mean().index, g.mean().values, yerr=g.std().values, marker="o", capsize=3, label=model)
            ax.set_title(f"{ds} · {mech}")
            ax.set_xlabel("fraction of cells deleted")
            ax.grid(alpha=0.3)
        axes[0][0].set_ylabel(main)
        axes[0][-1].legend(fontsize=8)
        fig.tight_layout()
        fig.savefig(out / "plots" / f"{ds.replace(':', '_').replace('/', '_')}_{main}.png", dpi=150)
        plt.close(fig)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--out", required=True, help="Output directory")
    p.add_argument(
        "--datasets",
        nargs="+",
        default=["breast_cancer", "wine", "diabetes"],
        help="Built-in names, openml:<id>, or csv:<path> (with --target)",
    )
    p.add_argument("--target", default=None, help="Target column for csv datasets")
    p.add_argument("--source_col", default=None, help="Source / provenance column for csv datasets")
    p.add_argument("--task", default=None, choices=[None, "classification", "regression"], help="Override task")
    p.add_argument("--max_rows", type=int, default=2000, help="Subsample larger datasets to this many rows")
    p.add_argument("--test_size", type=float, default=0.3)
    p.add_argument(
        "--mechanisms", nargs="+", default=["mcar", "mnar", "block"], choices=["mcar", "mar", "mnar", "block", "block_shift"]
    )
    p.add_argument(
        "--split",
        default="random",
        choices=["random", "source"],
        help="'source': with block mechanisms hold out one whole synthetic source as the test set",
    )
    p.add_argument("--shift_scale", type=float, default=0.5, help="block_shift: per-source offset, in column std units")
    p.add_argument("--noise_scale", type=float, default=0.3, help="block_shift: upper bound of per-source noise, in std units")
    p.add_argument("--add_source_col", action="store_true", help="Append the source id as a feature (block mechanisms)")
    p.add_argument("--rates", nargs="+", type=float, default=[0.1, 0.3, 0.5])
    p.add_argument("--seeds", nargs="+", type=int, default=[0, 1, 2])
    p.add_argument("--include_complete", type=lambda s: s.lower() == "true", default=True, help="Also run on complete data")
    p.add_argument(
        "--models",
        nargs="+",
        default=["tabicl_impute", "tabicl_indicator", "tabicl_aware_zero", "xgboost"],
        choices=[
            "tabicl_impute", "tabicl_indicator", "tabicl_patternnorm", "tabicl_iterimpute", "tabicl_knnimpute",
            "tabicl_aware", "tabicl_aware_zero", "xgboost", "catboost", "tabpfn", "tabpfn25", "tabpfn26", "tabpfn3",
        ],
    )
    p.add_argument("--plain_ckpt", default=None, help="Released classifier checkpoint (default: auto-download)")
    p.add_argument("--plain_ckpt_reg", default=None, help="Released regressor checkpoint (default: auto-download)")
    p.add_argument("--aware_ckpt", default=None, help="Missing-aware classifier checkpoint (for tabicl_aware)")
    p.add_argument("--aware_ckpt_reg", default=None, help="Missing-aware regressor checkpoint (for tabicl_aware)")
    p.add_argument("--n_estimators", type=int, default=8, help="TabICL ensemble size")
    p.add_argument("--device", default=None)
    p.add_argument("--loso", action="store_true", help="Leave-one-source-out on a csv dataset with --source_col")
    p.add_argument("--natural", action="store_true", help="With --loso: use the natural missingness, inject nothing")
    p.add_argument("--min_source_rows", type=int, default=20, help="With --loso: skip smaller sources")
    p.add_argument("--plot", action="store_true")
    p.add_argument("--resummarize", action="store_true", help="Only rebuild summary/plots from <out>/results.csv")
    p.add_argument(
        "--no_isolation",
        action="store_true",
        help="Run xgboost/catboost in-process instead of a spawned child (may deadlock on macOS with torch)",
    )
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "args.json").write_text(json.dumps(vars(args), indent=2, default=str))

    if args.resummarize:
        df = pd.read_csv(out / "results.csv", keep_default_na=True)
        df["error"] = df["error"].fillna("")
        summarize(df, out)
        if args.plot:
            plot(df, out)
        return

    zoo = ModelZoo(args)
    rows: List[dict] = []
    for name in args.datasets:
        data = load_dataset(name, args.target, args.source_col, args.max_rows, np.random.default_rng(0))
        if args.task:
            data["task"] = args.task
        print(f"\n=== {name}: {data['X'].shape[0]} rows, {data['X'].shape[1]} features, {data['task']}", flush=True)
        if args.loso:
            run_loso(args, zoo, data, rows)
        else:
            run_synthetic(args, zoo, data, rows)
        pd.DataFrame(rows).to_csv(out / "results.csv", index=False)  # checkpoint after each dataset

    zoo.close()
    df = pd.DataFrame(rows)
    df.to_csv(out / "results.csv", index=False)
    summarize(df, out)
    if args.plot:
        plot(df, out)
    print(f"\nwrote {out / 'results.csv'}, {out / 'summary.csv'}, {out / 'summary.md'}")


if __name__ == "__main__":
    main()
