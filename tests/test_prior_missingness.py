"""Tests for the block-structured and cell-wise missingness prior."""

import argparse

import numpy as np
import pytest
import torch

from tabicl.prior import PriorDataset, MissingnessConfig
from tabicl.prior._missingness import (
    MissingnessTransform,
    apply_missingness,
    block_mask,
    cell_mask,
    _logistic_mask,
)


def _table(T=400, d=8, H=12, seed=0):
    g = torch.Generator().manual_seed(seed)
    X = torch.zeros(T, H)
    X[:, :d] = torch.randn(T, d, generator=g)
    if d > 2:
        X[:, 2] = torch.randint(0, 3, (T,), generator=g).float()  # one categorical column
    return X


def test_disabled_returns_input_unchanged():
    X = _table()
    cfg = MissingnessConfig(enabled=False)
    X_out, d_out, info = apply_missingness(X, 8, 200, cfg)
    assert X_out is X
    assert d_out == 8
    assert info["mode"] == "none"


def test_logistic_mask_hits_target_rate():
    torch.manual_seed(0)
    z = torch.randn(20000)
    for rate in (0.05, 0.3, 0.6):
        m = _logistic_mask(z, rate, steepness=2.0, sign=1.0)
        assert abs(m.float().mean().item() - rate) < 0.02
        # Higher z must be more likely missing when sign is positive.
        assert z[m].mean() > z[~m].mean()


def test_cell_mask_respects_active_columns_and_rate_bound():
    np.random.seed(1)
    torch.manual_seed(1)
    X = _table()
    cfg = MissingnessConfig(enabled=True, max_cell_rate=0.5)
    for _ in range(20):
        m = cell_mask(X, 8, cfg)
        assert m.shape == X.shape
        assert not m[:, 8:].any(), "padded columns must never be masked"
        assert m[:, :8].float().mean(dim=0).max() <= 0.5 + 0.1


def test_block_mask_is_constant_within_source():
    np.random.seed(2)
    torch.manual_seed(2)
    X = _table()
    cfg = MissingnessConfig(enabled=True, p_source_shift=0.0, p_source_noise=0.0)
    m, X_shift, source = block_mask(X, 8, cfg)
    assert torch.equal(X_shift, X), "no shift or noise requested"
    assert not m[:, 8:].any()
    for k in source.unique().tolist():
        rows = m[source == k, :8]
        assert (rows == rows[0]).all(), "missing pattern must be identical within a source"
    # every feature observed by at least one source
    assert (~m[:, :8]).any(dim=0).all()


def test_block_shift_leaves_categorical_columns_untouched():
    np.random.seed(3)
    torch.manual_seed(3)
    X = _table()
    cfg = MissingnessConfig(enabled=True, p_source_shift=1.0, p_source_noise=1.0)
    m, X_shift, source = block_mask(X, 8, cfg)
    assert torch.equal(X_shift[:, 2], X[:, 2]), "categorical column must not be shifted"
    assert not torch.equal(X_shift[:, 0], X[:, 0]), "numeric column must be shifted"
    assert torch.equal(X_shift[:, 8:], X[:, 8:])


def test_apply_missingness_constraints_and_source_column():
    np.random.seed(4)
    torch.manual_seed(4)
    X = _table()
    train_size = 200
    cfg = MissingnessConfig(enabled=True, p_apply=1.0, p_cell=1.0, p_block=1.0, p_source_column=1.0)
    seen_source_col = False
    for _ in range(30):
        X_out, d_out, info = apply_missingness(X, 8, train_size, cfg)
        assert info["mode"] == "both"
        nan = torch.isnan(X_out)
        assert not nan[:, d_out:].any(), "padding must stay finite"
        # min observed training cells per active column
        assert ((~nan[:train_size, :d_out]).sum(dim=0) >= cfg.min_train_observed).all()
        # min observed features per row
        assert ((~nan[:, :d_out]).sum(dim=1) >= cfg.min_row_observed).all()
        if info["source_column"]:
            seen_source_col = True
            assert d_out == 9
            # one of the active columns holds integer source ids with no NaN
            src = info["source"]
            found = any(
                (not torch.isnan(X_out[:, j]).any()) and torch.equal(X_out[:, j].long(), src)
                for j in range(d_out)
            )
            assert found, "source id column must be present among active columns"
    assert seen_source_col


def test_mnar_censoring_removes_a_tail():
    np.random.seed(5)
    torch.manual_seed(5)
    X = _table(T=2000, d=1, H=1)
    cfg = MissingnessConfig(
        enabled=True,
        mechanism_probs=(0.0, 0.0, 1.0),
        p_censor=1.0,
        min_col_frac=1.0,
        max_col_frac=1.0,
        max_cell_rate=0.3,
        cell_rate_beta=(50.0, 50.0),  # rate close to 0.15
    )
    m = cell_mask(X, 1, cfg)[:, 0]
    x = X[:, 0]
    assert 0.05 < m.float().mean().item() < 0.3
    # censored values are all above or all below the observed ones
    assert (x[m].min() >= x[~m].max()) or (x[m].max() <= x[~m].min())


def test_transform_dense_and_nested():
    np.random.seed(6)
    torch.manual_seed(6)
    cfg = MissingnessConfig(enabled=True, p_apply=1.0)
    tfm = MissingnessTransform(cfg)
    B, T, H = 4, 100, 10
    X = torch.randn(B, T, H)
    d = torch.tensor([10, 6, 3, 8])
    X[1, :, 6:] = 0
    X[2, :, 3:] = 0
    X[3, :, 8:] = 0
    train_sizes = torch.tensor([50, 50, 50, 50])
    X_out, d_out = tfm(X, d, train_sizes)
    assert X_out.shape == X.shape
    assert torch.isnan(X_out).any()
    assert (d_out >= d).all()
    # nested tensors
    Xn = torch.nested.nested_tensor([torch.randn(80, H), torch.randn(120, H)])
    dn = torch.tensor([10, 10])
    Xn_out, dn_out = tfm(Xn, dn, torch.tensor([40, 60]))
    assert Xn_out.is_nested
    assert [t.shape for t in Xn_out.unbind()] == [(80, H), (120, H)]


def test_prior_dataset_dummy_with_missingness():
    np.random.seed(7)
    torch.manual_seed(7)
    cfg = MissingnessConfig(enabled=True, p_apply=1.0)
    ds = PriorDataset(
        batch_size=16, min_features=3, max_features=20, max_seq_len=128, prior_type="dummy", missingness=cfg
    )
    X, y, d, seq_lens, train_sizes = ds.get_batch()
    assert torch.isnan(X).any()
    assert not torch.isnan(y).any(), "targets must never be masked"
    frac = torch.isnan(X).float().mean().item()
    assert 0.0 < frac < 0.9
    # no all-NaN training column among active features
    for i in range(X.shape[0]):
        act = X[i, : train_sizes[i], : d[i]]
        assert (~torch.isnan(act)).sum(dim=0).min() >= cfg.min_train_observed


def test_prior_dataset_default_is_complete():
    ds = PriorDataset(batch_size=4, min_features=3, max_features=10, max_seq_len=64, prior_type="dummy")
    X, *_ = ds.get_batch()
    assert not torch.isnan(X).any()


def test_config_args_roundtrip():
    parser = argparse.ArgumentParser()
    MissingnessConfig.add_args_to_parser(parser)
    args = parser.parse_args(["--missing_enabled", "true", "--missing_max_sources", "5", "--missing_p_apply", "0.9"])
    cfg = MissingnessConfig.from_args(args)
    assert cfg.enabled is True
    assert cfg.max_sources == 5
    assert cfg.p_apply == pytest.approx(0.9)
    # defaults survive when attributes are absent
    cfg2 = MissingnessConfig.from_args(argparse.Namespace())
    assert cfg2.enabled is False
