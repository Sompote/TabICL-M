"""Bar (histogram) predictive distribution for regression.

The model outputs one logit per bucket. Bucket borders are fitted per table from the
training targets (equal-mass quantile borders, extended by one standard deviation
on each side), so the head is scale-free and the target may be standardised
arbitrarily. Training minimises the negative log-density of the piecewise-uniform
distribution at the true value, as in TabPFN. Statistics (mean, variance, median,
quantiles) are read off the histogram with linear interpolation inside a bucket.
"""

from __future__ import annotations

from typing import Union

import torch
import torch.nn.functional as F
from torch import Tensor


class BarDistribution:
    """Static helpers around per-table bucket borders of shape (B, K+1)."""

    def __init__(self, num_buckets: int, tail: float = 1.0, min_width: float = 1e-4):
        self.num_buckets = num_buckets
        self.tail = tail
        self.min_width = min_width

    def fit_borders(self, y_train: Tensor) -> Tensor:
        """Equal-mass borders from the training targets: (B, n) -> (B, K+1)."""
        y = y_train.float()
        B = y.shape[0]
        K = self.num_buckets
        alphas = torch.linspace(0.0, 1.0, K + 1, device=y.device, dtype=y.dtype)
        borders = torch.quantile(y, alphas, dim=1).T  # (B, K+1)
        std = y.std(dim=1, keepdim=True).clamp_min(self.min_width)
        borders[:, :1] = borders[:, :1] - self.tail * std
        borders[:, -1:] = borders[:, -1:] + self.tail * std
        # Ties in y_train collapse buckets; enforce a strictly increasing, min-width grid.
        steps = (borders[:, 1:] - borders[:, :-1]).clamp_min(self.min_width * std)
        borders = torch.cat([borders[:, :1], borders[:, :1] + steps.cumsum(dim=1)], dim=1)
        return borders

    @staticmethod
    def widths(borders: Tensor) -> Tensor:
        return borders[:, 1:] - borders[:, :-1]  # (B, K)

    @staticmethod
    def centers(borders: Tensor) -> Tensor:
        return 0.5 * (borders[:, 1:] + borders[:, :-1])  # (B, K)

    def bucket_index(self, y: Tensor, borders: Tensor) -> Tensor:
        """Index of the bucket containing each value, clamped to the edge buckets: (B, T) -> (B, T)."""
        idx = torch.searchsorted(borders[:, 1:-1].contiguous(), y.float().contiguous(), right=True)
        return idx.clamp(0, self.num_buckets - 1)

    def nll(self, logits: Tensor, y: Tensor, borders: Tensor) -> Tensor:
        """Mean negative log-density of the true values. logits (B, T, K), y (B, T)."""
        logp = F.log_softmax(logits.float(), dim=-1)
        idx = self.bucket_index(y, borders)
        logp_true = logp.gather(-1, idx.unsqueeze(-1)).squeeze(-1)
        logw = torch.log(self.widths(borders)).gather(1, idx)
        return -(logp_true - logw).mean()

    def mean(self, logits: Tensor, borders: Tensor) -> Tensor:
        p = F.softmax(logits.float(), dim=-1)
        return (p * self.centers(borders).unsqueeze(1)).sum(-1)

    def variance(self, logits: Tensor, borders: Tensor) -> Tensor:
        p = F.softmax(logits.float(), dim=-1)
        c = self.centers(borders).unsqueeze(1)
        w = self.widths(borders).unsqueeze(1)
        m = (p * c).sum(-1, keepdim=True)
        return (p * ((c - m) ** 2 + w**2 / 12.0)).sum(-1)

    def icdf(self, logits: Tensor, borders: Tensor, alpha: Union[Tensor, float]) -> Tensor:
        """Quantiles by linear interpolation inside the bucket: (B, T, K) -> (B, T, len(alpha)) or (B, T)."""
        scalar = not torch.is_tensor(alpha) or alpha.dim() == 0
        a = torch.as_tensor(alpha, device=logits.device, dtype=torch.float32).reshape(-1)
        p = F.softmax(logits.float(), dim=-1)
        cdf = p.cumsum(-1)  # (B, T, K)
        B, T, K = p.shape
        a_exp = a.view(1, 1, -1).expand(B, T, -1)
        idx = torch.searchsorted(cdf.contiguous(), a_exp.contiguous(), right=False).clamp(0, K - 1)
        cdf_lo = torch.cat([torch.zeros_like(cdf[..., :1]), cdf[..., :-1]], dim=-1).gather(-1, idx)
        p_k = p.gather(-1, idx).clamp_min(1e-12)
        lo = borders[:, :-1].unsqueeze(1).expand(B, T, K).gather(-1, idx)
        w = self.widths(borders).unsqueeze(1).expand(B, T, K).gather(-1, idx)
        q = lo + w * ((a_exp - cdf_lo) / p_k).clamp(0.0, 1.0)
        return q.squeeze(-1) if scalar else q
