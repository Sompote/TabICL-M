"""Tests for the source-aware additions of TabICL-M.

- col_group_stats: source-relative value encoding in the column embedder
- row_missing_aware: observed-only row attention
- pattern_token: pattern read-out in the row-wise interaction
- block reconstruction and offset-consistency objectives
"""

import pytest
import torch

from tabicl._model.tabicl import TabICL
from tabicl._model.embedding import ColEmbedding
from tabicl.train._reconstruction import sample_reconstruction_mask, sample_block_mask
from tabicl.train._consistency import shift_by_pattern, consistency_loss

SMALL = dict(embed_dim=16, col_num_blocks=2, col_nhead=2, col_num_inds=4, row_num_blocks=2, row_nhead=2, icl_num_blocks=1, icl_nhead=2)
FLAGS = [
    dict(col_group_stats=True),
    dict(row_missing_aware=True),
    dict(pattern_token=True),
    dict(col_group_stats=True, row_missing_aware=True, pattern_token=True),
]


def _pair(**flags):
    torch.manual_seed(0)
    plain = TabICL(**SMALL)
    torch.manual_seed(0)
    aware = TabICL(**SMALL, col_missing_aware=True, **flags)
    kept = aware.load_pretrained_state_dict(plain.state_dict())
    return plain, aware, kept


def _data():
    g = torch.Generator().manual_seed(1)
    X = torch.randn(2, 60, 7, generator=g)
    y = torch.randint(0, 3, (2, 45), generator=g).float()
    Xn = X.clone()
    Xn[0, :30, 1] = float("nan")  # source 1 lacks feature 1
    Xn[0, 30:, 2] = float("nan")  # source 2 lacks feature 2
    Xn[1, 3, :] = float("nan")  # a fully missing row
    Xn[1, :, 4] = float("nan")  # a fully missing column
    return X, Xn, y


@pytest.mark.parametrize("flags", FLAGS, ids=lambda f: "+".join(f))
@pytest.mark.parametrize("mode", ["train", "eval"])
def test_complete_data_unchanged_and_nan_finite(flags, mode):
    plain, aware, kept = _pair(**flags)
    assert kept, "new parameters are reported as kept at init"
    X, Xn, y = _data()
    plain.train(mode == "train")
    aware.train(mode == "train")
    with torch.no_grad():
        assert torch.allclose(plain(X, y), aware(X, y), atol=1e-6)
        assert torch.isfinite(aware(Xn, y)).all()


def test_flags_require_missing_aware():
    with pytest.raises(ValueError):
        TabICL(**SMALL, row_missing_aware=True)


def test_group_relative_values_remove_source_offsets():
    X = torch.randn(1, 200, 4, 1)
    X[0, :100, 0] += 5.0  # source 1 has an offset on column 0
    X[0, 100:, 1] = float("nan")  # and the two sources differ by pattern
    X[0, :100, 2] = float("nan")
    ids = ColEmbedding.pattern_ids(torch.isnan(X[..., 0]))
    assert set(ids.unique().tolist()) == {1, 2}
    rel = ColEmbedding.group_relative_values(X, ids)
    assert abs(rel[0, :100, 0, 0].mean()) < 1e-4 and abs(rel[0, 100:, 0, 0].mean()) < 1e-4
    assert abs(rel[0, :100, 0, 0].std() - 1.0) < 0.05
    assert (rel[0, 100:, 1, 0] == 0).all(), "missing cells give zero"
    # rare patterns fall back to table-wide statistics
    X[0, 0, 3] = float("nan")
    ids = ColEmbedding.pattern_ids(torch.isnan(X[..., 0]))
    assert ids[0, 0] == 0


def test_observed_only_rows_ignore_absent_tokens():
    """With row_missing_aware, a fully absent token cannot influence the row representation."""
    _, aware, _ = _pair(row_missing_aware=True)
    aware.eval()
    X, Xn, y = _data()
    absent = aware._absent_groups(Xn)
    assert absent is not None and absent.shape == (2, 60, 7)
    assert absent[1, 3].all(), "fully missing row -> every token absent"
    assert not absent[0, :30].all(dim=-1).any(), "partially observed rows keep tokens"


def test_pattern_token_changes_output_once_trained():
    _, aware, _ = _pair(pattern_token=True)
    X, Xn, y = _data()
    aware.eval()
    with torch.no_grad():
        before = aware(Xn, y)
        torch.nn.init.normal_(aware.row_interactor.pattern_out.weight, std=0.1)
        after = aware(Xn, y)
    assert not torch.allclose(before, after)


def test_block_mask_hides_a_row_and_column_block():
    X = torch.randn(3, 100, 10)
    X[:, :, 0] = float("nan")
    mask = sample_block_mask(X, rows_max=0.5, cols_max=0.5, p_apply=1.0)
    assert mask.shape == X.shape and not mask[:, :, 0].any()
    for b in range(3):
        rows = mask[b].any(dim=1)
        cols = mask[b].any(dim=0)
        assert 1 <= rows.sum() <= 50 and 1 <= cols.sum() <= 5
        assert (mask[b][rows][:, cols]).all(), "a full block"
    mixed = sample_reconstruction_mask(X, mode="mixed", p_apply=1.0)
    assert mixed.shape == X.shape and not torch.isnan(X)[mixed].any()
    with pytest.raises(ValueError):
        sample_reconstruction_mask(X, mode="nope")


def test_shift_by_pattern_offsets_numeric_columns_per_source():
    torch.manual_seed(0)
    X = torch.randn(1, 200, 3)
    X[0, :, 2] = torch.randint(0, 3, (200,)).float()  # categorical, untouched
    X[0, :100, 1] = float("nan")
    Xs = shift_by_pattern(X, shift_max=2.0, noise_max=0.0)
    assert torch.equal(torch.isnan(Xs), torch.isnan(X))
    assert torch.equal(Xs[0, :, 2], X[0, :, 2])
    delta = Xs[0, :, 0] - X[0, :, 0]
    assert torch.allclose(delta[:100], delta[0]) and torch.allclose(delta[100:], delta[100])


def test_consistency_loss_zero_when_identical():
    p = torch.randn(2, 5, 4)
    assert consistency_loss(p, p, regression=False).abs() < 1e-6
    # per-row mean, not a sum over rows
    big = torch.randn(1, 4000, 4)
    assert consistency_loss(big + 0.5 * torch.randn_like(big), big, regression=False) < 1.0
    assert consistency_loss(p, p, regression=True) == 0
    assert consistency_loss(p + 1.0, p, regression=True) > 0
