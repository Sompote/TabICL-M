"""Tests for the bar (histogram) regression head."""

import numpy as np
import pytest
import torch

from tabicl._model.bar_dist import BarDistribution
from tabicl._model.tabicl import TabICL

SMALL = dict(embed_dim=16, col_num_blocks=2, col_nhead=2, col_num_inds=4, row_num_blocks=1, row_nhead=2, icl_num_blocks=1, icl_nhead=2)


def test_borders_are_increasing_and_cover_training_targets():
    d = BarDistribution(50)
    y = torch.cat([torch.randn(1, 200), torch.zeros(1, 200)])  # second table: all ties
    b = d.fit_borders(y)
    assert b.shape == (2, 51)
    assert (b[:, 1:] > b[:, :-1]).all(), "strictly increasing, even with ties"
    assert (b[:, 0] < y.min(dim=1).values).all() and (b[:, -1] > y.max(dim=1).values).all()


def test_nll_is_finite_and_prefers_the_true_bucket():
    d = BarDistribution(20)
    y_train = torch.randn(1, 500)
    b = d.fit_borders(y_train)
    y = torch.tensor([[0.0, 3.0, -50.0]])  # inside, in the tail, far outside (clamped to an edge bucket)
    uniform = torch.zeros(1, 3, 20)
    assert torch.isfinite(d.nll(uniform, y, b))
    peaked = uniform.clone()
    peaked[0, 0, d.bucket_index(y, b)[0, 0]] = 10.0
    assert d.nll(peaked[:, :1], y[:, :1], b) < d.nll(uniform[:, :1], y[:, :1], b)


def test_statistics_of_a_peaked_histogram():
    d = BarDistribution(100)
    b = d.fit_borders(torch.randn(1, 1000))
    logits = torch.zeros(1, 1, 100)
    k = 60
    logits[0, 0, k] = 30.0
    c = d.centers(b)[0, k]
    assert abs(d.mean(logits, b)[0, 0] - c) < 1e-3
    assert abs(d.icdf(logits, b, 0.5)[0, 0] - c) < d.widths(b)[0, k]
    q = d.icdf(logits, b, torch.tensor([0.1, 0.5, 0.9]))
    assert q.shape == (1, 1, 3) and (q[..., 1:] >= q[..., :-1]).all()
    # equal-mass borders: a uniform histogram reproduces the training distribution, so its
    # 10 % / 90 % quantiles are those of y_train (about -1.28 / +1.28 for N(0, 1))
    u = torch.zeros(1, 1, 100)
    qu = d.icdf(u, b, torch.tensor([0.1, 0.9]))
    assert abs(qu[0, 0, 0] + 1.28) < 0.3 and abs(qu[0, 0, 1] - 1.28) < 0.3
    assert d.variance(u, b)[0, 0] > d.variance(logits, b)[0, 0]


def _data():
    g = torch.Generator().manual_seed(0)
    X = torch.randn(2, 80, 5, generator=g)
    y = X[..., 0] * 2 + 0.1 * torch.randn(2, 80, generator=g)
    return X, y


@pytest.mark.parametrize("mode", ["train", "eval"])
def test_bar_model_shapes_and_stats(mode):
    torch.manual_seed(0)
    m = TabICL(**SMALL, max_classes=0, num_quantiles=9, regression_method="bar", num_buckets=32)
    X, y = _data()
    m.train(mode == "train")
    with torch.no_grad():
        out = m(X, y[:, :60])
    assert out.shape == (2, 20, 32)
    m.eval()
    with torch.no_grad():
        stats = m.predict_stats(X, y[:, :60], output_type=["mean", "median", "variance", "quantiles"], alphas=[0.1, 0.9])
    assert stats["mean"].shape == (2, 20) and stats["quantiles"].shape == (2, 20, 2)
    assert (stats["quantiles"][..., 1] >= stats["quantiles"][..., 0]).all()
    assert torch.isfinite(stats["variance"]).all() and (stats["variance"] > 0).all()


def test_quantile_checkpoint_loads_into_bar_model_with_uniform_start():
    torch.manual_seed(0)
    quant = TabICL(**SMALL, max_classes=0, num_quantiles=9)
    bar = TabICL(**SMALL, max_classes=0, num_quantiles=9, regression_method="bar", num_buckets=32, col_missing_aware=True)
    kept = bar.load_pretrained_state_dict(quant.state_dict())
    assert any("decoder" in k for k in kept), "the mismatched output layer is reported as reset"
    assert torch.all(bar.icl_predictor.decoder[-1].weight == 0)
    # shared weights are identical
    assert torch.equal(bar.col_embedder.in_linear.weight, quant.col_embedder.in_linear.weight)
    X, y = _data()
    bar.eval()
    with torch.no_grad():
        out = bar(X, y[:, :60])
        stats = bar.predict_stats(X, y[:, :60], output_type=["mean", "quantiles"], alphas=[0.1, 0.9])
    assert torch.allclose(out, torch.zeros_like(out)), "zero head -> uniform histogram"
    # a uniform histogram over equal-mass buckets predicts the training-target distribution
    y_mean = y[:, :60].mean(dim=1, keepdim=True).expand(-1, 20)
    assert torch.allclose(stats["mean"], y_mean, atol=0.25 * y[:, :60].std())


def test_sklearn_regressor_round_trip_with_bar_checkpoint(tmp_path):
    from tabicl import TabICLRegressor

    torch.manual_seed(0)
    m = TabICL(**SMALL, max_classes=0, num_quantiles=9, regression_method="bar", num_buckets=32)
    cfg = dict(SMALL, max_classes=0, num_quantiles=9, regression_method="bar", num_buckets=32)
    p = tmp_path / "bar.ckpt"
    torch.save({"config": cfg, "state_dict": m.state_dict()}, p)
    rng = np.random.default_rng(0)
    X = rng.normal(size=(120, 4))
    y = X[:, 0] * 3 + rng.normal(scale=0.1, size=120)
    reg = TabICLRegressor(model_path=str(p), device="cpu", n_estimators=2).fit(X[:90], y[:90])
    out = reg.predict(X[90:], output_type=["mean", "quantiles"], alphas=[0.1, 0.9])
    assert out["mean"].shape == (30,) and np.isfinite(out["mean"]).all()
    assert (out["quantiles"][:, 1] >= out["quantiles"][:, 0]).all()
    reg2 = TabICLRegressor(model_path=str(p), device="cpu", n_estimators=2, kv_cache=True).fit(X[:90], y[:90])
    assert np.isfinite(reg2.predict(X[90:])).all()
