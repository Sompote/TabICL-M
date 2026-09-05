"""Tests for the missingness injection used by scripts/ablation_missingness.py."""

import importlib.util
from pathlib import Path

import numpy as np
import pytest

_SPEC = importlib.util.spec_from_file_location(
    "ablation_missingness", Path(__file__).resolve().parents[1] / "scripts" / "ablation_missingness.py"
)
abl = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(abl)


def _table(n=2000, p=8, seed=0):
    return np.random.default_rng(seed).normal(size=(n, p))


@pytest.mark.parametrize("mechanism", ["mcar", "mar", "mnar", "block", "block_shift"])
@pytest.mark.parametrize("rate", [0.1, 0.3, 0.5])
def test_rate_is_hit(mechanism, rate):
    X = _table()
    mask, _ = abl.inject_missingness(X, mechanism, rate, np.random.default_rng(1))
    assert mask.shape == X.shape
    tol = 0.08 if mechanism.startswith("block") else 0.03
    assert abs(mask.mean() - rate) < tol, (mechanism, rate, mask.mean())
    # safety rules
    assert ((~mask).sum(axis=0) >= 2).all()
    assert (~mask).any(axis=1).all()


def test_zero_rate_is_complete():
    mask, _ = abl.inject_missingness(_table(), "mcar", 0.0, np.random.default_rng(0))
    assert not mask.any()


def test_mnar_depends_on_own_value():
    X = _table()
    mask, _ = abl.inject_missingness(X, "mnar", 0.3, np.random.default_rng(2))
    # for each column, missing and observed values must have clearly different means
    for j in range(X.shape[1]):
        gap = abs(X[mask[:, j], j].mean() - X[~mask[:, j], j].mean())
        assert gap > 0.5, (j, gap)


def test_mcar_does_not_depend_on_value():
    X = _table()
    mask, _ = abl.inject_missingness(X, "mcar", 0.3, np.random.default_rng(3))
    gaps = [abs(X[mask[:, j], j].mean() - X[~mask[:, j], j].mean()) for j in range(X.shape[1])]
    assert max(gaps) < 0.2


def test_block_pattern_is_constant_within_source():
    X = _table()
    mask, source = abl.inject_missingness(X, "block", 0.3, np.random.default_rng(4))
    assert source is not None and len(source) == len(X)
    for s in np.unique(source):
        rows = mask[source == s]
        assert (rows == rows[0]).all()
    # a supplied source vector is respected
    src = np.repeat(np.arange(3), len(X) // 3 + 1)[: len(X)]
    mask2, source2 = abl.inject_missingness(X, "block", 0.3, np.random.default_rng(5), source=src)
    assert np.array_equal(source2, src)
    assert (~mask2).any(axis=0).all(), "every feature observed by at least one source"


def test_add_indicators_only_for_incomplete_columns():
    X_tr = _table(50, 4)
    X_te = _table(20, 4, seed=1)
    X_tr[0, 1] = np.nan
    X_te[3, 3] = np.nan
    A, B = abl.add_indicators(X_tr, X_te)
    assert A.shape == (50, 6) and B.shape == (20, 6)
    assert A[0, 4] == 1.0 and A[1:, 4].sum() == 0
    assert B[3, 5] == 1.0
    C, D = abl.add_indicators(_table(10, 3), _table(5, 3))
    assert C.shape == (10, 3) and D.shape == (5, 3)


def test_score_classification_and_regression():
    y = np.array([0, 1, 1, 0, 1])
    proba = np.array([[0.9, 0.1], [0.2, 0.8], [0.3, 0.7], [0.6, 0.4], [0.1, 0.9]])
    m = abl.score("classification", y, {"proba": proba}, 2)
    assert m["acc"] == 1.0 and m["auc"] == 1.0 and m["logloss"] > 0
    yr = np.array([1.0, 2.0, 3.0])
    out = {"mean": yr + 0.1, "q10": yr - 1, "q90": yr + 1}
    r = abl.score("regression", yr, out, 0)
    assert abs(r["rmse"] - 0.1) < 1e-9 and r["coverage80"] == 1.0
    r2 = abl.score("regression", yr, {"mean": yr}, 0)
    assert np.isnan(r2["coverage80"])


def test_source_shift_offsets_numeric_columns_per_source():
    X = _table(3000, 4)
    X[:, 3] = np.random.default_rng(0).integers(0, 3, size=3000)  # categorical, must be untouched
    source = np.repeat(np.arange(3), 1000)
    Xs = abl.apply_source_shift(X, source, np.random.default_rng(1), shift_scale=1.0, noise_scale=0.0)
    assert np.array_equal(Xs[:, 3], X[:, 3])
    delta = Xs[:, :3] - X[:, :3]
    for k in range(3):  # constant offset within a source, no noise
        assert np.allclose(delta[source == k], delta[source == k][0])
    offsets = np.stack([delta[source == k][0] for k in range(3)])
    assert np.abs(offsets).max() > 0.3, "offsets of order one std"
    Xn = abl.apply_source_shift(X, source, np.random.default_rng(2), shift_scale=0.0, noise_scale=0.5)
    assert not np.allclose(Xn[:, 0], X[:, 0]) and np.allclose(Xn[:, :3].mean(axis=0), X[:, :3].mean(axis=0), atol=0.1)


def test_split_by_source_is_leave_one_source_out():
    source = np.array([0, 1, 2, 0, 1, 2, 2])
    tr, te = abl.split_by_source(source, 2)
    assert set(te) == {2, 5, 6} and set(tr) == {0, 1, 3, 4}
    assert not set(tr) & set(te)


def test_pattern_normalize_centres_each_source():
    rng = np.random.default_rng(0)
    X = rng.normal(size=(300, 3))
    X[:150, 0] += 4.0  # source A has an offset on column 0
    X[:150, 2] = np.nan  # and lacks column 2; source B lacks column 1
    X[150:, 1] = np.nan
    A, B = abl.pattern_normalize(X[:200], X[200:])
    Z = np.vstack([A, B])
    assert np.array_equal(np.isnan(Z), np.isnan(X))
    assert abs(np.nanmean(Z[:150, 0])) < 1e-6 and abs(np.nanmean(Z[150:, 0])) < 1e-6
    assert abs(np.nanstd(Z[:150, 0]) - 1) < 1e-6
    # a rare pattern falls back to pooled statistics and stays finite
    X[0, 1] = np.nan
    A, B = abl.pattern_normalize(X[:200], X[200:])
    assert np.isfinite(A[0, 0])
