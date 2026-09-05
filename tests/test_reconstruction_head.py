"""Tests for the masked-cell reconstruction head (reconstruction=True)."""

import pytest
import torch

from tabicl._model.tabicl import TabICL
from tabicl.train._reconstruction import sample_reconstruction_mask, hide_cells

SMALL = dict(
    embed_dim=16,
    col_num_blocks=1,
    col_nhead=2,
    col_num_inds=4,
    row_num_blocks=2,
    row_nhead=2,
    icl_num_blocks=1,
    icl_nhead=2,
    zero_init=False,
)


def _model(seed=0, **overrides):
    torch.manual_seed(seed)
    return TabICL(**{**SMALL, **overrides}, col_missing_aware=True, reconstruction=True)


def _data(seed=0, B=2, T=40, H=5, train=30):
    g = torch.Generator().manual_seed(seed)
    X = torch.randn(B, T, H, generator=g)
    y = torch.randint(0, 3, (B, train), generator=g).float()
    return X, y


def test_reconstruction_requires_missing_aware():
    with pytest.raises(ValueError):
        TabICL(**SMALL, col_missing_aware=False, reconstruction=True)


def test_sample_mask_respects_observed_and_active_columns():
    torch.manual_seed(0)
    X = torch.randn(4, 100, 8)
    X[0, :, 2] = float("nan")
    X[1, 10:20, :] = float("nan")
    d = torch.tensor([8, 8, 5, 3])
    mask = sample_reconstruction_mask(X, d, rate_max=0.5, p_apply=1.0)
    assert mask.shape == X.shape
    assert not (mask & torch.isnan(X)).any(), "never hide an already missing cell"
    assert not mask[2, :, 5:].any() and not mask[3, :, 3:].any(), "never hide padded columns"
    assert mask.float().mean() <= 0.5
    assert mask.any()
    none = sample_reconstruction_mask(X, d, rate_max=0.5, p_apply=0.0)
    assert not none.any()


def test_hide_cells_sets_nan_only_on_mask():
    X = torch.randn(2, 10, 3)
    mask = torch.zeros_like(X, dtype=torch.bool)
    mask[0, 1, 2] = True
    Xh = hide_cells(X, mask)
    assert torch.isnan(Xh[0, 1, 2])
    assert torch.equal(Xh[~mask], X[~mask])
    assert not torch.isnan(X).any(), "input must not be modified"


@pytest.mark.parametrize("feature_group", ["same", False])
def test_prediction_unchanged_by_token_return(feature_group):
    m = _model(col_feature_group=feature_group, col_affine=not feature_group).train()
    X, y = _data()
    mask = sample_reconstruction_mask(X, None, rate_max=0.3, p_apply=1.0)
    Xh = hide_cells(X, mask)
    with torch.no_grad():
        pred_only = m(Xh, y)
        pred, tokens = m(Xh, y, return_tokens=True)
    assert torch.allclose(pred_only, pred, atol=1e-5)
    G = 5 if feature_group else 5
    assert tokens.shape == (2, 40, G, 16)


@pytest.mark.parametrize("feature_group", ["same", False])
def test_reconstruction_loss_values_and_gradients(feature_group):
    m = _model(col_feature_group=feature_group, col_affine=not feature_group).train()
    X, y = _data()
    X[1, :, 3] = float("nan")  # prior-missing column: never in the loss
    mask = sample_reconstruction_mask(X, None, rate_max=0.3, p_apply=1.0)
    pred, tokens = m(hide_cells(X, mask), y, return_tokens=True)
    loss = m.reconstruction_loss(tokens, X, mask)
    assert torch.isfinite(loss) and loss > 0
    loss.backward()
    assert m.recon_head.weight.grad.abs().sum() > 0
    row_grads = [p.grad for p in m.row_interactor.parameters() if p.grad is not None]
    assert row_grads and sum(g.abs().sum() for g in row_grads) > 0, "loss must reach the row-wise block"
    # empty mask gives a zero loss without error
    zero = m.reconstruction_loss(tokens.detach(), X, torch.zeros_like(mask))
    assert zero.item() == 0.0


def test_loss_ignores_cells_missing_in_target():
    m = _model().train()
    X, y = _data()
    mask = torch.zeros_like(X, dtype=torch.bool)
    mask[0, :5, 0] = True
    X_target = X.clone()
    X_target[0, :5, 0] = float("nan")  # the hidden cells are NaN in the target
    with torch.no_grad():
        _, tokens = m(hide_cells(X, mask), y, return_tokens=True)
    assert m.reconstruction_loss(tokens, X_target, mask).item() == 0.0


def test_inference_ignores_reconstruction_head():
    aware = _model()
    plain = TabICL(**SMALL, col_missing_aware=True, reconstruction=False)
    plain.load_state_dict({k: v for k, v in aware.state_dict().items() if not k.startswith("recon_head.")})
    X, y = _data()
    X[0, 2:6, 1] = float("nan")
    aware.eval()
    plain.eval()
    with torch.no_grad():
        assert torch.allclose(aware(X, y), plain(X, y), atol=1e-6)


def test_pretrained_loading_keeps_recon_head():
    torch.manual_seed(0)
    plain = TabICL(**SMALL)
    m = _model()
    kept = m.load_pretrained_state_dict(plain.state_dict())
    assert kept == [
        "col_embedder.absence",
        "col_embedder.mask_linear.weight",
        "recon_head.bias",
        "recon_head.weight",
    ]


def test_reconstruction_is_learnable():
    """On a table where column 1 equals column 0, hiding column-1 cells must become predictable."""
    m = _model(seed=1).train()
    opt = torch.optim.Adam(m.parameters(), lr=3e-3)
    g = torch.Generator().manual_seed(3)
    X = torch.randn(4, 64, 4, generator=g)
    X[:, :, 1] = X[:, :, 0]
    y = torch.randint(0, 2, (4, 48), generator=g).float()
    mask = torch.zeros_like(X, dtype=torch.bool)
    mask[:, :, 1] = torch.rand(4, 64, generator=g) < 0.4

    def step():
        _, tokens = m(hide_cells(X, mask), y, return_tokens=True)
        loss = m.reconstruction_loss(tokens, X, mask)
        opt.zero_grad()
        loss.backward()
        opt.step()
        return loss.item()

    first = step()
    for _ in range(60):
        last = step()
    assert last < 0.5 * first, (first, last)
