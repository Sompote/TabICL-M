"""Tests for the regression levers: smooth-target prior, point loss flag, neighbour-based context."""

import argparse

import numpy as np
import pandas as pd
import pytest
import torch

from tabicl.prior._smooth_target import FAMILIES, SmoothTargetConfig, SmoothTargetTransform, apply_smooth_target
from tabicl._sklearn.knn_context import KNNContextRegressor


def _table(T=300, d=6, H=8, seed=0):
    g = torch.Generator().manual_seed(seed)
    X = torch.randn(T, H, generator=g)
    X[:, d:] = 0.0
    y = torch.randn(T, generator=g)
    return X, y


@pytest.mark.parametrize("family", FAMILIES)
def test_every_family_gives_a_standardised_finite_target(family):
    np.random.seed(0)
    X, y = _table()
    cfg = SmoothTargetConfig(enabled=True, p_apply=1.0, weights={family: 1.0})
    y_new, info = apply_smooth_target(X, y, 6, cfg)
    assert info["family"] == family
    assert torch.isfinite(y_new).all()
    assert abs(float(y_new.mean())) < 1e-3 and abs(float(y_new.std()) - 1) < 1e-2
    assert all(0 <= j < 6 for j in info["inputs"]), "only active features are used"
    assert not torch.allclose(y_new, y)


def test_target_is_a_function_of_the_features_up_to_noise():
    np.random.seed(1)
    X, y = _table()
    cfg = SmoothTargetConfig(enabled=True, p_apply=1.0, min_noise=1e-4, max_noise=1e-3, weights={"gp": 1.0})
    y_new, info = apply_smooth_target(X, y, 6, cfg)
    # duplicated rows must get (almost) the same target
    X2 = torch.cat([X, X[:5]])
    np.random.seed(1)
    y2, _ = apply_smooth_target(X2, torch.cat([y, y[:5]]), 6, cfg)
    assert torch.allclose(y2[:5], y2[-5:], atol=0.05)


def test_disabled_or_not_applied_returns_the_original_target():
    X, y = _table()
    assert apply_smooth_target(X, y, 6, SmoothTargetConfig(enabled=False))[0] is y
    np.random.seed(0)
    assert apply_smooth_target(X, y, 6, SmoothTargetConfig(enabled=True, p_apply=0.0))[0] is y
    assert apply_smooth_target(X, y, 0, SmoothTargetConfig(enabled=True, p_apply=1.0))[0] is y


def test_batch_transform_dense_and_nested():
    np.random.seed(0)
    X = torch.randn(3, 100, 5)
    y = torch.randn(3, 100)
    d = torch.tensor([5, 3, 4])
    tr = SmoothTargetTransform(SmoothTargetConfig(enabled=True, p_apply=1.0))
    out = tr(X, y, d)
    assert out.shape == y.shape and torch.isfinite(out).all()
    nested = torch.nested.nested_tensor([torch.randn(80, 5), torch.randn(120, 5)])
    ny = torch.nested.nested_tensor([torch.randn(80), torch.randn(120)])
    nout = tr(nested, ny, torch.tensor([5, 5]))
    assert nout.is_nested and [t.shape[0] for t in nout.unbind()] == [80, 120]


def test_config_round_trips_through_argparse():
    p = argparse.ArgumentParser()
    SmoothTargetConfig.add_args_to_parser(p)
    args = p.parse_args(["--smooth_enabled", "True", "--smooth_p_apply", "0.3", "--smooth_weights", "gp=1,mlp=0.5"])
    cfg = SmoothTargetConfig.from_args(args)
    assert cfg.enabled and cfg.p_apply == 0.3 and cfg.weights == {"gp": 1.0, "mlp": 0.5}
    with pytest.raises(ValueError):
        SmoothTargetConfig.from_args(p.parse_args(["--smooth_weights", "tree=1"]))


def test_train_config_has_point_loss_and_smooth_flags():
    from tabicl.train._train_config import build_parser

    args = build_parser().parse_args(["--point_loss_weight", "0.2", "--smooth_enabled", "True"])
    assert args.point_loss_weight == 0.2 and args.smooth_enabled is True


class _Dummy:
    """Stand-in for TabICLRegressor: mean of the context targets, so the context is observable."""

    def __init__(self, **kw):
        self.kw = kw

    def fit(self, X, y):
        self.mean_ = float(np.mean(y))
        self.n_ = len(y)
        return self

    def predict(self, X, output_type="mean", alphas=None):
        n = len(X)
        if isinstance(output_type, list):
            return {"mean": np.full(n, self.mean_), "quantiles": np.tile([self.mean_ - 1, self.mean_ + 1], (n, 1))}
        return np.full(n, self.mean_)


def test_knn_context_uses_local_rows_and_falls_back_on_small_tables(monkeypatch):
    monkeypatch.setattr(KNNContextRegressor, "_make_base", lambda self: _Dummy(**(self.base_kwargs or {})))
    rng = np.random.default_rng(0)
    X = rng.uniform(-3, 3, size=(3000, 2))
    y = X[:, 0]  # target increases with the first feature
    est = KNNContextRegressor(context_size=200, min_rows=1000, test_group_size=50).fit(X, y)
    assert est.local_
    X_te = np.array([[-2.5, 0.0]] * 60 + [[2.5, 0.0]] * 60)
    pred = est.predict(X_te)
    assert pred[:60].mean() < -1.5 and pred[60:].mean() > 1.5, "each group is predicted from its own neighbourhood"
    out = est.predict(X_te, output_type=["mean", "quantiles"], alphas=[0.1, 0.9])
    assert set(out) == {"mean", "quantiles"} and out["quantiles"].shape == (120, 2)
    small = KNNContextRegressor(context_size=200, min_rows=5000).fit(X, y)
    assert not small.local_ and np.allclose(small.predict(X_te), y.mean())


def test_knn_context_handles_nan_and_strings(monkeypatch):
    monkeypatch.setattr(KNNContextRegressor, "_make_base", lambda self: _Dummy())
    rng = np.random.default_rng(1)
    X = pd.DataFrame({"a": rng.normal(size=500), "b": rng.choice(["u", "v", None], size=500)})
    X.loc[::7, "a"] = np.nan
    y = rng.normal(size=500)
    est = KNNContextRegressor(context_size=50, min_rows=100, test_group_size=20).fit(X, y)
    pred = est.predict(X.iloc[:40])
    assert pred.shape == (40,) and np.isfinite(pred).all()
