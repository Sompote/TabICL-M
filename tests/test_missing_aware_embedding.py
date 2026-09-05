"""Tests for the missing-aware column embedding (col_missing_aware=True)."""

import numpy as np
import pandas as pd
import pytest
import torch

from tabicl import TabICLClassifier, TabICLRegressor
from tabicl._model.tabicl import TabICL
from tabicl._model.layers import InducedSelfAttentionBlock
from tabicl._sklearn.preprocessing import TransformToNumerical, EnsembleGenerator

SMALL = dict(
    embed_dim=16,
    col_num_blocks=2,
    col_nhead=2,
    col_num_inds=4,
    row_num_blocks=1,
    row_nhead=2,
    icl_num_blocks=1,
    icl_nhead=2,
)


def _pair(seed=0, **overrides):
    """Two models with identical weights, one plain and one missing-aware."""
    kw = {**SMALL, **overrides}
    torch.manual_seed(seed)
    plain = TabICL(**kw)
    aware = TabICL(**kw, col_missing_aware=True)
    result = aware.load_state_dict(plain.state_dict(), strict=False)
    assert set(result.missing_keys) == {"col_embedder.absence", "col_embedder.mask_linear.weight"}
    assert not result.unexpected_keys
    return plain, aware


def _data(seed=0, B=2, T=40, H=5, train=30, classes=3):
    g = torch.Generator().manual_seed(seed)
    X = torch.randn(B, T, H, generator=g)
    y = torch.randint(0, classes, (B, train), generator=g).float()
    Xn = X.clone()
    Xn[0, 3:10, 1] = float("nan")  # scattered cells
    Xn[1, :, 2] = float("nan")  # whole column, train and test
    Xn[1, 5, :] = float("nan")  # whole row
    return X, Xn, y


@pytest.mark.parametrize("mode", ["train", "eval"])
@pytest.mark.parametrize("regression", [False, True])
def test_complete_data_unchanged(mode, regression):
    plain, aware = _pair(max_classes=0 if regression else 10, num_quantiles=9 if regression else 999)
    X, _, y = _data()
    if regression:
        y = torch.randn_like(y)
    for m in (plain, aware):
        m.train(mode == "train")
    with torch.no_grad():
        out_plain = plain(X, y)
        out_aware = aware(X, y)
    assert torch.allclose(out_plain, out_aware, atol=1e-6)


@pytest.mark.parametrize("mode", ["train", "eval"])
@pytest.mark.parametrize("feature_group", ["same", False])
def test_nan_input_is_finite(mode, feature_group):
    _, aware = _pair(col_feature_group=feature_group, col_affine=not feature_group)
    _, Xn, y = _data()
    aware.train(mode == "train")
    with torch.no_grad():
        out = aware(Xn, y)
    assert torch.isfinite(out).all()
    assert out.shape[:2] == (2, 10)


def test_nan_changes_output_only_where_present():
    plain, aware = _pair(zero_init=False)
    X, Xn, y = _data()
    aware.train()  # float32 path; inference mode runs under bfloat16 autocast
    with torch.no_grad():
        out_complete = aware(X, y)
        out_missing = aware(Xn, y)
    # table 0 has NaN, table 1 has NaN: both differ from the complete run
    assert not torch.allclose(out_complete, out_missing)
    # a table without NaN inside a batch with NaN is unaffected
    Xh = X.clone()
    Xh[1, 5:8, 0] = float("nan")
    with torch.no_grad():
        out_half = aware(Xh, y)
    assert torch.allclose(out_half[0], out_complete[0], atol=1e-5)


def test_plain_model_rejects_nothing_but_produces_nan():
    plain, _ = _pair()
    _, Xn, y = _data()
    plain.eval()
    with torch.no_grad():
        out = plain(Xn, y)
    assert torch.isnan(out).any(), "the plain model has no NaN path, which is why the flag exists"


def test_gradients_reach_new_parameters():
    _, aware = _pair(zero_init=False)
    _, Xn, y = _data()
    aware.train()
    out = aware(Xn, y)
    out.sum().backward()
    assert aware.col_embedder.mask_linear.weight.grad.abs().sum() > 0
    assert aware.col_embedder.absence.grad.abs().sum() > 0


def test_variable_feature_count_path():
    """Training path with d given (no feature grouping) must handle NaN."""
    _, aware = _pair(col_feature_group=False, col_affine=True)
    _, Xn, y = _data()
    d = torch.tensor([5, 3])
    Xn[1, :, 3:] = 0.0
    aware.train()
    out = aware(Xn, y, d=d)
    assert torch.isfinite(out).all()


def test_all_nan_training_column_is_guarded():
    _, aware = _pair(col_feature_group=False, col_affine=True)
    X, _, y = _data()
    X[:, :30, 1] = float("nan")  # column missing in every training row of both tables
    aware.eval()
    with torch.no_grad():
        out = aware(X, y)
    assert torch.isfinite(out).all()


def test_isab_masked_keys_are_excluded():
    torch.manual_seed(1)
    blk = InducedSelfAttentionBlock(d_model=16, nhead=2, dim_feedforward=32, num_inds=4, zero_init=False).eval()
    src = torch.randn(3, 20, 16)
    kpm = torch.zeros(3, 20, dtype=torch.bool)
    kpm[:, 5:9] = True
    keep = ~kpm[0]
    src_garbage = src.clone()
    src_garbage[:, 5:9] += 100.0
    with torch.no_grad():
        a = blk(src, None, kpm)
        b = blk(src_garbage, None, kpm)
        c = blk(src[:, keep], None, None)
        d = blk(src, 12, kpm)
        e = blk(src_garbage, 12, kpm)
    assert torch.allclose(a[:, keep], b[:, keep], atol=1e-5)
    assert torch.allclose(a[:, keep], c, atol=1e-5)
    assert torch.allclose(d[:, keep], e[:, keep], atol=1e-5)


def test_kv_cache_matches_plain_forward_with_nan():
    _, aware = _pair(zero_init=False)
    _, Xn, y = _data()
    aware.eval()
    train = y.shape[1]
    with torch.no_grad():
        ref = aware(Xn, y, return_logits=True)
        aware.forward_with_cache(X_train=Xn[:, :train], y_train=y, use_cache=False, store_cache=True)
        out = aware.forward_with_cache(
            X_test=Xn[:, train:], cache=aware._cache, use_cache=True, store_cache=False, return_logits=True
        )
    assert torch.isfinite(out).all()
    assert torch.allclose(ref.float(), out.float(), atol=5e-2)


def test_pretrained_loading_tolerates_only_new_params():
    plain, aware = _pair()
    kept = aware.load_pretrained_state_dict(plain.state_dict())
    assert kept == ["col_embedder.absence", "col_embedder.mask_linear.weight"]
    assert plain.load_pretrained_state_dict(plain.state_dict()) == []

    bad = {k: v for k, v in plain.state_dict().items() if "icl_predictor" not in k}
    with pytest.raises(RuntimeError):
        aware.load_pretrained_state_dict(bad)


# ---------------------------------------------------------------------------
# sklearn wrapper
# ---------------------------------------------------------------------------


def _save_checkpoint(path, missing_aware, regression=False):
    kw = {**SMALL, "col_missing_aware": missing_aware}
    if regression:
        kw.update(max_classes=0, num_quantiles=9)
    torch.manual_seed(0)
    model = TabICL(**kw)
    torch.save({"config": kw, "state_dict": model.state_dict()}, path)
    return path


def _frame(seed=0, n=60):
    rng = np.random.default_rng(seed)
    df = pd.DataFrame(
        {
            "a": rng.normal(size=n),
            "b": rng.normal(size=n),
            "c": rng.choice(["x", "y", "z"], size=n),
        }
    )
    df.loc[rng.random(n) < 0.3, "a"] = np.nan
    df.loc[rng.random(n) < 0.2, "c"] = np.nan
    y = (df["b"] > 0).astype(int).values
    return df, y


def test_transform_to_numerical_keeps_nan_when_not_imputing():
    df, _ = _frame()
    kept = TransformToNumerical(impute=False).fit_transform(df)
    imputed = TransformToNumerical(impute=True).fit_transform(df)
    assert np.isnan(kept).any()
    assert not np.isnan(imputed).any()
    # categorical NaN becomes NaN, not -1
    cat_col = kept[:, 0]  # ColumnTransformer puts categorical first
    assert np.isnan(cat_col).any()


def test_ensemble_generator_preserves_nan_positions():
    df, y = _frame()
    X = TransformToNumerical(impute=False).fit_transform(df)
    eg = EnsembleGenerator(classification=True, n_estimators=4, norm_methods=["none", "power"], random_state=0)
    eg.fit(X, y)
    data = eg.transform(X, mode="both")
    for norm, (Xs, ys) in data.items():
        assert np.isnan(Xs).any(), norm
        finite = ~np.isnan(Xs)
        assert np.isfinite(Xs[finite]).all(), norm


@pytest.mark.parametrize("kv_cache", [False, True])
def test_classifier_passes_nan_to_missing_aware_model(tmp_path, kv_cache):
    ckpt = _save_checkpoint(tmp_path / "aware.ckpt", missing_aware=True)
    df, y = _frame()
    clf = TabICLClassifier(model_path=str(ckpt), n_estimators=2, device="cpu", kv_cache=kv_cache)
    clf.fit(df, y)
    assert clf.X_encoder_.impute is False
    proba = clf.predict_proba(df)
    assert proba.shape == (len(df), 2)
    assert np.isfinite(proba).all()
    assert np.allclose(proba.sum(axis=1), 1.0, atol=1e-5)


def test_classifier_imputes_for_plain_model(tmp_path):
    ckpt = _save_checkpoint(tmp_path / "plain.ckpt", missing_aware=False)
    df, y = _frame()
    clf = TabICLClassifier(model_path=str(ckpt), n_estimators=2, device="cpu")
    clf.fit(df, y)
    assert clf.X_encoder_.impute is True
    proba = clf.predict_proba(df)
    assert np.isfinite(proba).all()


def test_regressor_passes_nan_to_missing_aware_model(tmp_path):
    ckpt = _save_checkpoint(tmp_path / "aware_reg.ckpt", missing_aware=True, regression=True)
    df, _ = _frame()
    y = df["b"].values + np.nan_to_num(df["a"].values)
    reg = TabICLRegressor(model_path=str(ckpt), n_estimators=2, device="cpu")
    reg.fit(df, y)
    assert reg.X_encoder_.impute is False
    pred = reg.predict(df)
    assert pred.shape == (len(df),)
    assert np.isfinite(pred).all()
