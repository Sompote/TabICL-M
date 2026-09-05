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


def sample_reconstruction_mask(
    X: Tensor,
    d: Optional[Tensor] = None,
    rate_max: float = 0.3,
    p_apply: float = 0.5,
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

    Returns
    -------
    Tensor
        Boolean tensor of shape (B, T, H). True marks a cell to hide.
    """
    B, T, H = X.shape
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
