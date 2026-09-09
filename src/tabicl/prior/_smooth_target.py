"""Smooth-target prior component for regression.

The SCM priors of TabICLv2 produce targets through random graphs of noisy,
often discontinuous edges. On smooth, low-noise nonlinear functions (robot
kinematics, spatial fields, multiplicative prices) the released regressor
trails TabPFN-3 at every training size, which points at the function class in
the prior rather than at capacity. This module replaces the target of a
fraction of regression tables with a smooth function of a few of its features:

* ``gp``         a Gaussian-process sample (random Fourier features, RBF kernel with
                 per-input lengthscales, optional periodic component)
* ``mlp``        a small random MLP with smooth activations (sin, tanh, GELU, softplus)
* ``product``    a product of affine terms of 2-3 features, optionally divided by another
* ``loglinear``  exp of a linear form (multiplicative, heavy right tail)
* ``kinematic``  a planar chain of links with the features as joint angles
                 (sum of sines of cumulative angles, as in the kin8nm task)

Inputs are standardised per column before the function is applied, a small
multiplicative output noise is added, and the new target is standardised like
every other prior target. Tables whose function turns out constant keep their
original target. The transform runs before the missingness transform so it sees
complete features.
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

import numpy as np
import torch
from torch import Tensor

FAMILIES = ("gp", "mlp", "product", "loglinear", "kinematic")


def _str2bool(v) -> bool:
    if isinstance(v, bool):
        return v
    return str(v).lower() in ("1", "true", "t", "yes", "y")


@dataclass
class SmoothTargetConfig:
    """Configuration of the smooth-target prior component.

    Parameters
    ----------
    enabled : bool
        Apply the transform (regression tables only).
    p_apply : float
        Probability that a table's target is replaced.
    weights : dict
        Relative sampling weights of the function families.
    max_inputs : int
        Upper bound on the number of features that enter the function.
    min_lengthscale, max_lengthscale : float
        Range (log-uniform) of the GP lengthscales, in column standard deviations.
    min_noise, max_noise : float
        Range (log-uniform) of the output noise level relative to the signal
        standard deviation.
    """

    enabled: bool = False
    p_apply: float = 0.4
    weights: Dict[str, float] = field(
        default_factory=lambda: {"gp": 0.35, "mlp": 0.25, "product": 0.15, "loglinear": 0.1, "kinematic": 0.15}
    )
    max_inputs: int = 8
    min_lengthscale: float = 0.3
    max_lengthscale: float = 3.0
    min_noise: float = 1e-3
    max_noise: float = 0.1

    @staticmethod
    def add_args_to_parser(parser: argparse.ArgumentParser) -> None:
        """Register ``--smooth_*`` command line options."""
        g = parser.add_argument_group("Smooth-target prior (regression)")
        g.add_argument("--smooth_enabled", default=False, type=_str2bool, help="Replace targets by smooth functions")
        g.add_argument("--smooth_p_apply", default=0.4, type=float, help="Probability a regression table is replaced")
        g.add_argument("--smooth_max_inputs", default=8, type=int, help="Max features entering the function")
        g.add_argument("--smooth_min_lengthscale", default=0.3, type=float, help="Min GP lengthscale (std units)")
        g.add_argument("--smooth_max_lengthscale", default=3.0, type=float, help="Max GP lengthscale (std units)")
        g.add_argument("--smooth_min_noise", default=1e-3, type=float, help="Min relative output noise")
        g.add_argument("--smooth_max_noise", default=0.1, type=float, help="Max relative output noise")
        g.add_argument(
            "--smooth_weights",
            default=None,
            type=str,
            help="Family weights as 'gp=0.35,mlp=0.25,product=0.15,loglinear=0.1,kinematic=0.15'",
        )

    @staticmethod
    def from_args(args) -> "SmoothTargetConfig":
        """Build a config from parsed arguments. Missing attributes fall back to defaults."""
        cfg = SmoothTargetConfig()
        for name in ("enabled", "p_apply", "max_inputs", "min_lengthscale", "max_lengthscale", "min_noise", "max_noise"):
            value = getattr(args, f"smooth_{name}", None)
            if value is not None:
                setattr(cfg, name, value)
        weights = getattr(args, "smooth_weights", None)
        if weights:
            parsed = {}
            for item in str(weights).split(","):
                k, v = item.split("=")
                if k.strip() not in FAMILIES:
                    raise ValueError(f"unknown smooth-target family {k!r}; choose from {FAMILIES}")
                parsed[k.strip()] = float(v)
            cfg.weights = parsed
        return cfg


# ---------------------------------------------------------------------------
# Function families. Each takes standardised inputs Z of shape (T, k), k >= 1,
# and returns a (T,) tensor. Hyperparameters are drawn from ``np.random`` so the
# transform follows the seeding of the rest of the prior.
# ---------------------------------------------------------------------------


def _randn(*shape) -> Tensor:
    return torch.from_numpy(np.random.randn(*shape).astype(np.float32))


def _gp(Z: Tensor, cfg: SmoothTargetConfig) -> Tensor:
    T, k = Z.shape
    n_feat = 256
    ls = np.exp(np.random.uniform(math.log(cfg.min_lengthscale), math.log(cfg.max_lengthscale), size=k))
    W = _randn(k, n_feat) / torch.from_numpy(ls.astype(np.float32)).view(k, 1)
    b = torch.from_numpy(np.random.uniform(0, 2 * math.pi, size=n_feat).astype(np.float32))
    a = _randn(n_feat)
    f = math.sqrt(2.0 / n_feat) * torch.cos(Z @ W + b) @ a
    if np.random.random() < 0.3:  # periodic component on one input
        j = np.random.randint(k)
        period = np.random.uniform(0.5, 2.0)
        amp = np.random.uniform(0.3, 1.0)
        f = f + amp * torch.sin(2 * math.pi * Z[:, j] / period + np.random.uniform(0, 2 * math.pi))
    return f


_ACTS = {
    "sin": torch.sin,
    "tanh": torch.tanh,
    "gelu": torch.nn.functional.gelu,
    "softplus": torch.nn.functional.softplus,
}


def _mlp(Z: Tensor, cfg: SmoothTargetConfig) -> Tensor:
    T, k = Z.shape
    n_layers = np.random.randint(1, 3)
    act = _ACTS[np.random.choice(list(_ACTS))]
    gain = np.random.uniform(0.8, 2.5)
    h = Z * np.random.uniform(0.5, 2.0)
    fan_in = k
    for _ in range(n_layers):
        width = int(np.random.randint(16, 65))
        W = _randn(fan_in, width) * (gain / math.sqrt(fan_in))
        b = _randn(width) * 0.5
        h = act(h @ W + b)
        fan_in = width
    w_out = _randn(fan_in) / math.sqrt(fan_in)
    return h @ w_out


def _product(Z: Tensor, cfg: SmoothTargetConfig) -> Tensor:
    T, k = Z.shape
    m = min(k, int(np.random.randint(2, 4)))
    idx = np.random.permutation(k)[:m]
    f = torch.ones(T)
    for j in idx:
        a = np.random.randn()
        b = np.random.uniform(0.5, 1.5) * np.random.choice([-1.0, 1.0])
        f = f * (a + b * Z[:, j])
    if k > m and np.random.random() < 0.4:  # ratio
        j = np.random.permutation([i for i in range(k) if i not in idx])[0]
        c = np.random.uniform(0.3, 1.5)
        f = f / (1.0 + (c * Z[:, j]).abs())
    return f


def _loglinear(Z: Tensor, cfg: SmoothTargetConfig) -> Tensor:
    T, k = Z.shape
    beta = torch.from_numpy(np.random.uniform(-0.6, 0.6, size=k).astype(np.float32))
    lin = Z @ beta
    lin = lin - lin.mean()
    return torch.exp(lin.clamp(max=6.0))


def _kinematic(Z: Tensor, cfg: SmoothTargetConfig) -> Tensor:
    T, k = Z.shape
    angles = Z * (math.pi / 2) * np.random.uniform(0.5, 1.0)
    cum = torch.cumsum(angles, dim=1)
    lengths = torch.from_numpy(np.random.uniform(0.5, 1.5, size=k).astype(np.float32))
    x = (torch.cos(cum) * lengths).sum(dim=1)
    y = (torch.sin(cum) * lengths).sum(dim=1)
    choice = np.random.random()
    if choice < 0.4:
        return torch.sqrt(x * x + y * y)  # distance of the end effector
    if choice < 0.7:
        return y
    return torch.atan2(y, x)


_FAMILY_FN = {"gp": _gp, "mlp": _mlp, "product": _product, "loglinear": _loglinear, "kinematic": _kinematic}


def _standardise_columns(X: Tensor) -> Tensor:
    mean = torch.nanmean(X, dim=0)
    centred = X - mean
    std = torch.sqrt(torch.nanmean(centred * centred, dim=0)).clamp(min=1e-6)
    return torch.nan_to_num(centred / std).clamp(-10, 10)


def apply_smooth_target(X: Tensor, y: Tensor, d: int, cfg: SmoothTargetConfig) -> Tuple[Tensor, dict]:
    """Replace the target of one table by a smooth function of a few of its features.

    Parameters
    ----------
    X : Tensor
        Features of shape (T, H); only the first ``d`` columns are active.
    y : Tensor
        Target of shape (T,).
    d : int
        Number of active features.
    cfg : SmoothTargetConfig

    Returns
    -------
    y_out : Tensor
        New target of shape (T,), standardised to zero mean and unit variance, or ``y``
        unchanged when the transform does not apply.
    info : dict
        ``family`` (or None), ``inputs`` (feature indices used), ``noise``.
    """
    info: dict = {"family": None, "inputs": None, "noise": None}
    d = int(d)
    if not cfg.enabled or d == 0 or np.random.random() >= cfg.p_apply:
        return y, info
    families = [f for f in FAMILIES if cfg.weights.get(f, 0) > 0]
    if not families:
        return y, info
    w = np.array([cfg.weights[f] for f in families], dtype=np.float64)
    family = str(np.random.choice(families, p=w / w.sum()))

    k_max = max(1, min(d, cfg.max_inputs))
    k_min = 2 if family in ("product", "kinematic") and d >= 2 else 1
    k = int(np.random.randint(k_min, k_max + 1)) if k_max >= k_min else k_max
    inputs = np.sort(np.random.permutation(d)[:k])
    Z = _standardise_columns(X[:, inputs].float())
    f = _FAMILY_FN[family](Z, cfg)
    f = torch.nan_to_num(f)
    scale = f.std()
    if not torch.isfinite(scale) or scale < 1e-6:
        return y, info
    noise = float(np.exp(np.random.uniform(math.log(cfg.min_noise), math.log(cfg.max_noise))))
    f = f + noise * scale * _randn(f.shape[0])
    f = (f - f.mean()) / f.std().clamp(min=1e-6)
    f = f.clamp(-10, 10)
    info.update(family=family, inputs=inputs.tolist(), noise=noise)
    return f.to(dtype=y.dtype, device=y.device), info


class SmoothTargetTransform:
    """Batch-level wrapper around :func:`apply_smooth_target` (dense or nested tensors)."""

    def __init__(self, config: Optional[SmoothTargetConfig] = None):
        self.config = config or SmoothTargetConfig()

    @property
    def enabled(self) -> bool:
        return bool(self.config.enabled)

    @torch.no_grad()
    def __call__(self, X, y, d: Tensor):
        if not self.enabled:
            return y
        if getattr(X, "is_nested", False):
            outs = [apply_smooth_target(xi, yi, int(d[i]), self.config)[0] for i, (xi, yi) in enumerate(zip(X.unbind(), y.unbind()))]
            return torch.nested.nested_tensor(outs, device=y.device)
        y_out = y.clone()
        for i in range(X.shape[0]):
            y_out[i] = apply_smooth_target(X[i], y[i], int(d[i]), self.config)[0]
        return y_out

    def __repr__(self) -> str:
        return f"SmoothTargetTransform({self.config})"
