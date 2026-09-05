"""Masked-cell reconstruction for pre-training.

A fraction of the observed cells of each table is hidden (set to NaN) before the
forward pass. The model predicts the target as usual and, through
:meth:`tabicl._model.tabicl.TabICL.reconstruction_loss`, reconstructs the hidden
cells from the per-feature token outputs of the row-wise interaction. This forces
the row-wise block to learn cross-feature dependence explicitly, so that at test
time it can fill in absent features implicitly.

Requires ``col_missing_aware=True`` and ``reconstruction=True`` on the model.
"""

from __future__ import annotations

from typing import Optional

import torch
from torch import Tensor


def sample_block_mask(
    X: Tensor,
    d: Optional[Tensor] = None,
    rows_max: float = 0.5,
    cols_max: float = 0.5,
    p_apply: float = 0.5,
) -> Tensor:
    """Sample a block of cells to hide: a pseudo-source loses a subset of its columns.

    For each table, a random subset of rows (contiguous or scattered, 5 % to
    ``rows_max`` of the rows) loses a random subset of the active columns (10 % to
    ``cols_max``). Reconstructing such a block means completing a source's absent
    features from the other sources, which is the target case of TabICL-M.
    """
    B, T, H = X.shape
    mask = torch.zeros(B, T, H, dtype=torch.bool, device=X.device)
    for b in range(B):
        if torch.rand(()) >= p_apply:
            continue
        H_eff = int(d[b].item()) if d is not None else H
        n_rows = max(1, int(T * (0.05 + torch.rand(()).item() * max(rows_max - 0.05, 0.0))))
        if torch.rand(()) < 0.5:
            start = int(torch.randint(0, T - n_rows + 1, (1,)).item())
            rows = torch.arange(start, start + n_rows, device=X.device)
        else:
            rows = torch.randperm(T, device=X.device)[:n_rows]
        n_cols = max(1, int(H_eff * (0.1 + torch.rand(()).item() * max(cols_max - 0.1, 0.0))))
        cols = torch.randperm(H_eff, device=X.device)[:n_cols]
        mask[b, rows.unsqueeze(1), cols.unsqueeze(0)] = True
    mask &= ~torch.isnan(X)
    return mask


def sample_reconstruction_mask(
    X: Tensor,
    d: Optional[Tensor] = None,
    rate_max: float = 0.3,
    p_apply: float = 0.5,
    mode: str = "cell",
    block_rows_max: float = 0.5,
    block_cols_max: float = 0.5,
) -> Tensor:
    """Sample cells to hide for reconstruction.

    Parameters
    ----------
    X : Tensor
        Features of shape (B, T, H). NaN cells are already missing and are never
        selected.

    d : Optional[Tensor], default=None
        Number of active features per table of shape (B,). Padded columns beyond
        ``d`` are never selected. If None, all columns are eligible.

    rate_max : float, default=0.3
        Upper bound of the per-table hide rate. Each table draws its rate uniformly
        from ``[0, rate_max]``.

    p_apply : float, default=0.5
        Probability that a table receives any hidden cells at all.

    mode : str, default="cell"
        ``"cell"``: independent cells at a per-table rate. ``"block"``: a pseudo-source
        loses a subset of columns (:func:`sample_block_mask`). ``"mixed"``: each table
        draws one of the two with equal probability.

    block_rows_max, block_cols_max : float
        Bounds of the block size in ``"block"`` and ``"mixed"`` modes.

    Returns
    -------
    Tensor
        Boolean tensor of shape (B, T, H). True marks a cell to hide.
    """
    B, T, H = X.shape
    if mode == "block":
        return sample_block_mask(X, d, block_rows_max, block_cols_max, p_apply)
    if mode == "mixed":
        cell = sample_reconstruction_mask(X, d, rate_max, p_apply, mode="cell")
        block = sample_block_mask(X, d, block_rows_max, block_cols_max, p_apply)
        pick_block = (torch.rand(B, 1, 1, device=X.device) < 0.5)
        return torch.where(pick_block, block, cell)
    if mode != "cell":
        raise ValueError(f"unknown reconstruction mode {mode!r}; expected 'cell', 'block' or 'mixed'")
    rates = torch.rand(B, 1, 1, device=X.device) * rate_max
    apply = torch.rand(B, 1, 1, device=X.device) < p_apply
    mask = (torch.rand(B, T, H, device=X.device) < rates) & apply
    mask &= ~torch.isnan(X)
    if d is not None:
        cols = torch.arange(H, device=X.device).view(1, 1, H)
        mask &= cols < d.to(X.device).view(B, 1, 1)
    return mask


def hide_cells(X: Tensor, mask: Tensor) -> Tensor:
    """Return a copy of ``X`` with the masked cells set to NaN."""
    return X.masked_fill(mask, float("nan"))
