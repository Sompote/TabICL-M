"""Offset-consistency objective for pre-training.

Rows that share a missingness pattern are treated as one source. A second view of
the table is built in which every source receives its own additive offset and extra
noise on the numeric features, as in the prior. The model's prediction on the shifted
view is pulled towards its prediction on the clean view, which trains invariance to
per-source measurement effects explicitly.
"""

from __future__ import annotations

import torch
from torch import Tensor
import torch.nn.functional as F

from tabicl._model.embedding import ColEmbedding


def shift_by_pattern(
    X: Tensor, shift_max: float = 0.5, noise_max: float = 0.3, max_categories: int = 20, min_count: int = 8
) -> Tensor:
    """Return a copy of ``X`` (B, T, H, NaN at missing cells) with per-source offset and noise.

    Sources are the missingness-pattern groups of :meth:`ColEmbedding.pattern_ids`.
    Every source draws an offset ``N(0, s * std_j)`` per numeric column ``j`` with
    ``s ~ U(0, shift_max)`` and a noise level ``U(0, noise_max) * std_j``. Columns
    with at most ``max_categories`` distinct observed values are left alone.
    """
    B, T, H = X.shape
    X_out = X.clone()
    ids = ColEmbedding.pattern_ids(torch.isnan(X), min_count=min_count)
    for b in range(B):
        obs = ~torch.isnan(X[b])
        numeric = [j for j in range(H) if torch.unique(X[b, obs[:, j], j]).numel() > max_categories]
        if not numeric:
            continue
        cols = torch.as_tensor(numeric, device=X.device)
        x = torch.nan_to_num(X[b][:, cols], nan=0.0)
        o = obs[:, cols].to(x.dtype)
        cnt = o.sum(0).clamp_min(1.0)
        mean = (x * o).sum(0) / cnt
        std = torch.sqrt(((x - mean) ** 2 * o).sum(0) / cnt).clamp_min(1e-8)
        P = int(ids[b].max().item()) + 1
        shift_scale = float(torch.rand(()).item()) * shift_max
        noise_scale = float(torch.rand(()).item()) * noise_max
        offsets = torch.randn(P, len(numeric), device=X.device, dtype=X.dtype) * shift_scale * std
        sigma = torch.rand(P, 1, device=X.device, dtype=X.dtype) * noise_scale * std
        delta = offsets[ids[b]] + torch.randn(T, len(numeric), device=X.device, dtype=X.dtype) * sigma[ids[b]]
        X_out[b][:, cols] = X[b][:, cols] + delta  # NaN stays NaN
    return X_out


def consistency_loss(pred_shifted: Tensor, pred_clean: Tensor, regression: bool) -> Tensor:
    """Distance between the prediction on the shifted view and the (detached) clean one."""
    target = pred_clean.detach()
    if regression:
        return F.mse_loss(pred_shifted, target)
    # Mean KL per test row (flatten the table and row dimensions first).
    logp = F.log_softmax(pred_shifted, dim=-1).flatten(end_dim=-2)
    p = F.softmax(target, dim=-1).flatten(end_dim=-2)
    return F.kl_div(logp, p, reduction="batchmean")
