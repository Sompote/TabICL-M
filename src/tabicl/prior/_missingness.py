"""Block-structured and cell-wise missingness for synthetic prior datasets.

Real tables are rarely complete. Two kinds of incompleteness dominate:

1. **Cell-wise missingness.** Individual cells are absent. The mechanism may be
   independent of the data (MCAR), driven by another observed column (MAR), or
   driven by the value that is missing (MNAR, including detection-limit censoring).

2. **Block-structured missingness.** The table is a merge of several *sources*
   (laboratories, sites, campaigns, studies). Each source measured its own subset
   of features, so whole blocks of the table are absent. Sources may also carry
   their own measurement offset and noise, so the feature-to-target relation
   shifts between sources.

The released TabICL prior generates complete tables only. This module applies
missingness *after* a complete table has been generated, so it works with every
prior type (``mlp_scm``, ``tree_scm``, ``graph_scm``, ``dummy``). Missing cells
are written as ``NaN``. The target ``y`` and padded feature columns are never
touched.

Notes
-----
The current TabICL model does not accept ``NaN`` inputs. Enabling this module is
only useful together with a missingness-aware column embedding. It is disabled by
default.
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass, asdict
from typing import Dict, Optional, Tuple

import numpy as np
import torch
from torch import Tensor


def _str2bool(value: str) -> bool:
    return str(value).lower() in ("true", "1", "yes")


@dataclass
class MissingnessConfig:
    """Configuration of the missingness process applied to prior datasets.

    All probabilities are per dataset unless stated otherwise. Rates are sampled
    per dataset so that the model sees a wide range of incompleteness.

    Parameters
    ----------
    enabled : bool, default=False
        Master switch. If False, tables are returned complete.

    p_apply : float, default=0.6
        Probability that a dataset receives any missingness at all. The
        remainder stays complete so the model does not forget complete data.

    p_cell : float, default=0.6
        Given missingness is applied, probability of applying cell-wise masking.

    p_block : float, default=0.6
        Given missingness is applied, probability of applying block-structured
        (multi-source) masking. If neither cell nor block is drawn, block is used.

    max_cell_rate : float, default=0.7
        Upper bound of the per-column missing rate for cell-wise masking.

    cell_rate_beta : tuple of float, default=(0.7, 2.5)
        Beta distribution parameters for the per-column missing rate, scaled by
        ``max_cell_rate``. The default gives a mean rate near 0.15.

    min_col_frac, max_col_frac : float
        Range of the fraction of feature columns that receive cell-wise masking.

    mechanism_probs : tuple of float, default=(0.4, 0.3, 0.3)
        Probabilities of MCAR, MAR and MNAR for cell-wise masking. One mechanism
        is drawn per dataset.

    p_censor : float, default=0.3
        Within MNAR, probability of quantile censoring (values beyond a threshold
        are removed, like a detection limit) instead of logistic self-masking.

    min_steepness, max_steepness : float
        Range of the logistic slope for MAR and MNAR masking. Larger values give
        a sharper dependence of missingness on the driver value.

    min_sources, max_sources : int
        Range of the number of sources for block-structured masking.

    min_obs_frac : float, default=0.3
        Lower bound of the fraction of features each source observes.

    max_core_frac : float, default=0.5
        Upper bound of the fraction of features observed by every source
        (for example, index properties every laboratory reports).

    p_contiguous_sources : float, default=0.25
        Probability that rows are grouped by source in contiguous blocks. Because
        the train/test split is positional, this puts some sources entirely in the
        test part, which mimics a leave-one-source-out evaluation.

    p_source_shift : float, default=0.5
        Probability that sources carry an additive offset on numeric features.

    max_shift_scale : float, default=0.5
        Upper bound of the offset scale, in units of the column standard deviation.

    p_source_noise : float, default=0.5
        Probability that sources carry extra Gaussian noise on numeric features.

    max_noise_scale : float, default=0.3
        Upper bound of the noise scale, in units of the column standard deviation.

    p_source_column : float, default=0.5
        Probability of appending the source id as an extra categorical feature.
        Only possible when the table has spare padded columns.

    max_categories : int, default=20
        Integer-valued columns with at most this many unique values are treated as
        categorical. Source shift and noise are not applied to them.

    min_train_observed : int, default=2
        Minimum number of observed cells per feature within the training rows.
        Cells are un-masked at random to satisfy this bound.

    min_row_observed : int, default=1
        Minimum number of observed features per row.
    """

    enabled: bool = False
    p_apply: float = 0.6
    p_cell: float = 0.6
    p_block: float = 0.6
    # cell-wise
    max_cell_rate: float = 0.7
    cell_rate_beta: Tuple[float, float] = (0.7, 2.5)
    min_col_frac: float = 0.1
    max_col_frac: float = 1.0
    mechanism_probs: Tuple[float, float, float] = (0.4, 0.3, 0.3)
    p_censor: float = 0.3
    min_steepness: float = 0.5
    max_steepness: float = 4.0
    # block-structured
    min_sources: int = 2
    max_sources: int = 8
    min_obs_frac: float = 0.3
    max_core_frac: float = 0.5
    p_contiguous_sources: float = 0.25
    p_source_shift: float = 0.5
    max_shift_scale: float = 0.5
    p_source_noise: float = 0.5
    max_noise_scale: float = 0.3
    p_source_column: float = 0.5
    # safety
    max_categories: int = 20
    min_train_observed: int = 2
    min_row_observed: int = 1

    def to_dict(self) -> Dict:
        return asdict(self)

    @staticmethod
    def add_args_to_parser(parser: argparse.ArgumentParser) -> None:
        """Register ``--missing_*`` command line options."""
        g = parser.add_argument_group("Missingness prior (block-structured and cell-wise)")
        g.add_argument("--missing_enabled", default=False, type=_str2bool, help="Apply missingness to prior tables")
        g.add_argument("--missing_p_apply", default=0.6, type=float, help="Probability a dataset gets missingness")
        g.add_argument("--missing_p_cell", default=0.6, type=float, help="Probability of cell-wise masking")
        g.add_argument("--missing_p_block", default=0.6, type=float, help="Probability of block (multi-source) masking")
        g.add_argument("--missing_max_cell_rate", default=0.7, type=float, help="Max per-column cell missing rate")
        g.add_argument("--missing_min_sources", default=2, type=int, help="Min number of sources")
        g.add_argument("--missing_max_sources", default=8, type=int, help="Max number of sources")
        g.add_argument("--missing_min_obs_frac", default=0.3, type=float, help="Min fraction of features per source")
        g.add_argument(
            "--missing_p_contiguous_sources",
            default=0.25,
            type=float,
            help="Probability that sources occupy contiguous row blocks (some sources test-only)",
        )
        g.add_argument("--missing_p_source_shift", default=0.5, type=float, help="Probability of per-source offset")
        g.add_argument("--missing_p_source_noise", default=0.5, type=float, help="Probability of per-source noise")
        g.add_argument(
            "--missing_max_shift_scale", default=0.5, type=float, help="Max per-source offset, in column std units"
        )
        g.add_argument(
            "--missing_max_noise_scale", default=0.3, type=float, help="Max per-source noise level, in column std units"
        )
        g.add_argument(
            "--missing_p_source_column", default=0.5, type=float, help="Probability of appending a source-id column"
        )

    @staticmethod
    def from_args(args) -> "MissingnessConfig":
        """Build a config from parsed arguments. Missing attributes fall back to defaults."""
        cfg = MissingnessConfig()
        for name in (
            "enabled",
            "p_apply",
            "p_cell",
            "p_block",
            "max_cell_rate",
            "min_sources",
            "max_sources",
            "min_obs_frac",
            "p_contiguous_sources",
            "p_source_shift",
            "p_source_noise",
            "max_shift_scale",
            "max_noise_scale",
            "p_source_column",
        ):
            value = getattr(args, f"missing_{name}", None)
            if value is not None:
                setattr(cfg, name, value)
        return cfg


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _standardize(x: Tensor) -> Tensor:
    """Standardize a 1D tensor, robust to constant columns."""
    std = x.std()
    if not torch.isfinite(std) or std < 1e-8:
        return torch.zeros_like(x)
    return (x - x.mean()) / std


def _logistic_mask(z: Tensor, rate: float, steepness: float, sign: float) -> Tensor:
    """Bernoulli mask with ``p = sigmoid(sign * steepness * z + c)``.

    The intercept ``c`` is found by bisection so that the mean probability
    equals ``rate``. This is the standard construction for MAR/MNAR masking with
    a controlled overall rate.
    """
    logits = sign * steepness * z
    lo, hi = -30.0, 30.0
    for _ in range(40):
        c = 0.5 * (lo + hi)
        if torch.sigmoid(logits + c).mean().item() < rate:
            lo = c
        else:
            hi = c
    p = torch.sigmoid(logits + 0.5 * (lo + hi))
    return torch.rand_like(p) < p


def _censor_mask(x: Tensor, rate: float) -> Tensor:
    """Remove the top or bottom ``rate`` quantile of a column (detection-limit censoring)."""
    if rate <= 0:
        return torch.zeros_like(x, dtype=torch.bool)
    upper = np.random.random() < 0.5
    q = torch.quantile(x, 1.0 - rate if upper else rate)
    return (x >= q) if upper else (x <= q)


def _is_categorical(x: Tensor, max_categories: int) -> bool:
    if not torch.all(x == torch.round(x)):
        return False
    return torch.unique(x).numel() <= max_categories


# ---------------------------------------------------------------------------
# Cell-wise mechanism
# ---------------------------------------------------------------------------


def cell_mask(X: Tensor, d: int, cfg: MissingnessConfig) -> Tensor:
    """Cell-wise missingness mask for one complete table.

    Parameters
    ----------
    X : Tensor
        Complete features of shape (T, H). Only the first ``d`` columns are used.

    d : int
        Number of active features.

    cfg : MissingnessConfig

    Returns
    -------
    Tensor
        Boolean mask of shape (T, H). True marks a missing cell.
    """
    T, H = X.shape
    mask = torch.zeros(T, H, dtype=torch.bool, device=X.device)
    if d == 0:
        return mask

    mechanism = np.random.choice(["mcar", "mar", "mnar"], p=cfg.mechanism_probs)
    col_frac = np.random.uniform(cfg.min_col_frac, cfg.max_col_frac)
    n_cols = max(1, int(round(col_frac * d)))
    cols = np.random.choice(d, size=n_cols, replace=False)
    a, b = cfg.cell_rate_beta

    for j in cols:
        rate = float(cfg.max_cell_rate * np.random.beta(a, b))
        if rate <= 0:
            continue
        xj = X[:, j]

        if mechanism == "mcar":
            mask[:, j] = torch.rand(T, device=X.device) < rate

        elif mechanism == "mar":
            if d == 1:
                mask[:, j] = torch.rand(T, device=X.device) < rate
                continue
            # Driver is another column of the complete table.
            k = int(np.random.choice([c for c in range(d) if c != j]))
            z = _standardize(X[:, k])
            steep = np.random.uniform(cfg.min_steepness, cfg.max_steepness)
            sign = 1.0 if np.random.random() < 0.5 else -1.0
            mask[:, j] = _logistic_mask(z, rate, steep, sign)

        else:  # mnar
            if np.random.random() < cfg.p_censor and not _is_categorical(xj, cfg.max_categories):
                mask[:, j] = _censor_mask(xj, rate)
            else:
                z = _standardize(xj)
                steep = np.random.uniform(cfg.min_steepness, cfg.max_steepness)
                sign = 1.0 if np.random.random() < 0.5 else -1.0
                mask[:, j] = _logistic_mask(z, rate, steep, sign)

    return mask


# ---------------------------------------------------------------------------
# Block-structured (multi-source) mechanism
# ---------------------------------------------------------------------------


def block_mask(X: Tensor, d: int, cfg: MissingnessConfig) -> Tuple[Tensor, Tensor, Tensor]:
    """Block-structured missingness from a multi-source merge.

    Parameters
    ----------
    X : Tensor
        Complete features of shape (T, H). Only the first ``d`` columns are used.

    d : int
        Number of active features.

    cfg : MissingnessConfig

    Returns
    -------
    mask : Tensor
        Boolean mask of shape (T, H). True marks a missing cell.

    X_shifted : Tensor
        Copy of ``X`` with per-source offset and noise applied to numeric
        features. Equal to ``X`` when neither effect is drawn.

    source : Tensor
        Source id per row of shape (T,), dtype long.
    """
    T, H = X.shape
    mask = torch.zeros(T, H, dtype=torch.bool, device=X.device)
    X_out = X.clone()
    if d == 0:
        return mask, X_out, torch.zeros(T, dtype=torch.long, device=X.device)

    K = int(np.random.randint(cfg.min_sources, cfg.max_sources + 1))
    K = max(1, min(K, T))

    # Row-to-source assignment with unequal source sizes.
    concentration = float(np.random.choice([0.5, 1.0, 3.0]))
    props = np.random.dirichlet(np.full(K, concentration))
    counts = np.random.multinomial(T, props)
    source_np = np.repeat(np.arange(K), counts)
    if np.random.random() >= cfg.p_contiguous_sources:
        np.random.shuffle(source_np)
    source = torch.as_tensor(source_np, device=X.device, dtype=torch.long)

    # Feature subset observed by each source: (K, d).
    n_core = int(np.random.randint(0, int(math.floor(cfg.max_core_frac * d)) + 1))
    core = np.random.choice(d, size=n_core, replace=False) if n_core > 0 else np.array([], dtype=int)
    obs = np.zeros((K, d), dtype=bool)
    for k in range(K):
        frac = np.random.uniform(cfg.min_obs_frac, 1.0)
        obs[k] = np.random.random(d) < frac
    obs[:, core] = True
    # Every source observes at least one feature.
    for k in range(K):
        if not obs[k].any():
            obs[k, np.random.randint(d)] = True
    # Every feature is observed by at least one source.
    for j in range(d):
        if not obs[:, j].any():
            obs[np.random.randint(K), j] = True
    obs_t = torch.as_tensor(obs, device=X.device)

    mask[:, :d] = ~obs_t[source]

    # Per-source measurement effects on numeric features.
    apply_shift = np.random.random() < cfg.p_source_shift
    apply_noise = np.random.random() < cfg.p_source_noise
    if apply_shift or apply_noise:
        shift_scale = np.random.uniform(0.0, cfg.max_shift_scale) if apply_shift else 0.0
        noise_scale = np.random.uniform(0.0, cfg.max_noise_scale) if apply_noise else 0.0
        numeric = [j for j in range(d) if not _is_categorical(X[:, j], cfg.max_categories)]
        if numeric:
            cols = torch.as_tensor(numeric, device=X.device)
            std = X[:, cols].std(dim=0).clamp_min(1e-8)  # (n,)
            offsets = torch.randn(K, len(numeric), device=X.device) * shift_scale * std  # (K, n)
            X_out[:, cols] = X_out[:, cols] + offsets[source]
            if noise_scale > 0:
                sigma = torch.rand(K, 1, device=X.device) * noise_scale * std  # (K, n)
                X_out[:, cols] = X_out[:, cols] + torch.randn(T, len(numeric), device=X.device) * sigma[source]

    return mask, X_out, source


# ---------------------------------------------------------------------------
# Composition and safety constraints
# ---------------------------------------------------------------------------


def _enforce_min_observed(mask: Tensor, d: int, train_size: int, cfg: MissingnessConfig) -> Tensor:
    """Un-mask cells at random so that every feature has at least ``min_train_observed``
    observed training cells and every row has at least ``min_row_observed`` observed features."""
    T, _ = mask.shape
    if d == 0:
        return mask
    train_size = int(min(max(train_size, 0), T))

    # Columns: guarantee observed cells inside the training rows.
    need = min(cfg.min_train_observed, train_size)
    if need > 0:
        observed = (~mask[:train_size, :d]).sum(dim=0)  # (d,)
        for j in torch.nonzero(observed < need).flatten().tolist():
            missing_rows = torch.nonzero(mask[:train_size, j]).flatten()
            n_fix = int(need - observed[j].item())
            pick = missing_rows[torch.randperm(missing_rows.numel(), device=mask.device)[:n_fix]]
            mask[pick, j] = False

    # Rows: guarantee at least one observed feature.
    need_row = min(cfg.min_row_observed, d)
    if need_row > 0:
        observed = (~mask[:, :d]).sum(dim=1)  # (T,)
        for i in torch.nonzero(observed < need_row).flatten().tolist():
            missing_cols = torch.nonzero(mask[i, :d]).flatten()
            n_fix = int(need_row - observed[i].item())
            pick = missing_cols[torch.randperm(missing_cols.numel(), device=mask.device)[:n_fix]]
            mask[i, pick] = False
    return mask


def apply_missingness(
    X: Tensor, d: int, train_size: int, cfg: MissingnessConfig
) -> Tuple[Tensor, int, Dict[str, object]]:
    """Apply missingness to one complete table.

    Parameters
    ----------
    X : Tensor
        Complete features of shape (T, H). Columns ``>= d`` are padding.

    d : int
        Number of active features.

    train_size : int
        Position of the train/test split. Used only for the safety constraint on
        observed training cells.

    cfg : MissingnessConfig

    Returns
    -------
    X_out : Tensor
        Features of shape (T, H) with ``NaN`` at missing cells.

    d_out : int
        Number of active features. Equal to ``d + 1`` if a source-id column was appended.

    info : dict
        Description of what was applied: ``mode`` in {"none", "cell", "block", "both"},
        ``source`` (row source ids or None), ``mask`` (bool tensor), ``source_column`` (bool).
    """
    T, H = X.shape
    d = int(d)
    info: Dict[str, object] = {"mode": "none", "source": None, "mask": None, "source_column": False}
    if not cfg.enabled or d == 0 or np.random.random() >= cfg.p_apply:
        return X, d, info

    use_cell = np.random.random() < cfg.p_cell
    use_block = np.random.random() < cfg.p_block
    if not use_cell and not use_block:
        use_block = True

    X_out = X.clone()
    mask = torch.zeros(T, H, dtype=torch.bool, device=X.device)
    source = None

    if use_block:
        m_block, X_out, source = block_mask(X, d, cfg)
        mask |= m_block

    if use_cell:
        mask |= cell_mask(X, d, cfg)

    mask = _enforce_min_observed(mask, d, train_size, cfg)

    d_out = d
    source_column = False
    if use_block and source is not None and d < H and np.random.random() < cfg.p_source_column:
        # Append the source id as a categorical feature, then shuffle the active
        # columns so that the source column has no fixed position.
        X_out[:, d] = source.to(X_out.dtype)
        mask[:, d] = False
        d_out = d + 1
        source_column = True
        perm = torch.randperm(d_out, device=X.device)
        X_out[:, :d_out] = X_out[:, perm]
        mask[:, :d_out] = mask[:, perm]

    X_out = X_out.masked_fill(mask, float("nan"))

    info.update(
        {
            "mode": "both" if (use_cell and use_block) else ("cell" if use_cell else "block"),
            "source": source,
            "mask": mask,
            "source_column": source_column,
        }
    )
    return X_out, d_out, info


class MissingnessTransform:
    """Batch-level wrapper that applies :func:`apply_missingness` to each dataset.

    Works with dense tensors of shape (B, T, H) and with nested tensors of
    variable sequence length. Returns tensors of the same kind.
    """

    def __init__(self, config: Optional[MissingnessConfig] = None):
        self.config = config or MissingnessConfig()

    @property
    def enabled(self) -> bool:
        return bool(self.config.enabled)

    @torch.no_grad()
    def __call__(self, X, d: Tensor, train_sizes: Tensor):
        if not self.enabled:
            return X, d

        d_out = d.clone()
        if getattr(X, "is_nested", False):
            outs = []
            for i, xi in enumerate(X.unbind()):
                xo, di, _ = apply_missingness(xi, int(d[i]), int(train_sizes[i]), self.config)
                outs.append(xo)
                d_out[i] = di
            X_out = torch.nested.nested_tensor(outs, device=X.device)
        else:
            X_out = X.clone()
            for i in range(X.shape[0]):
                xo, di, _ = apply_missingness(X[i], int(d[i]), int(train_sizes[i]), self.config)
                X_out[i] = xo
                d_out[i] = di
        return X_out, d_out

    def __repr__(self) -> str:
        return f"MissingnessTransform({self.config})"
