"""TabArena wrapper for TabICL-M.

Subclasses TabArena's TabICLv2 wrapper and points the estimators at the TabICL-M
checkpoints through the ``model_path`` hyperparameter, which the estimators prefer
over ``checkpoint_version``. Everything else (bagging, refit, memory estimate, GPU
handling) is inherited, so TabICL-M is evaluated under exactly the protocol used for
TabICLv2 on the leaderboard. The module must be importable (not defined in
``__main__``) so that Ray-backed runs can unpickle it.

Checkpoints default to the source-aware 20k weights; override with the environment
variables ``TABICLM_CLF`` and ``TABICLM_REG``.
"""

from __future__ import annotations

import os
from pathlib import Path

from tabarena.models.tabicl.model import TabICLv2Model
from tabarena.utils.config_utils import ConfigGenerator

REPO = Path(__file__).resolve().parents[2]
DEFAULT_CLF = REPO / "checkpoints/tabicl-m-sa-20k/clf/step-10000.ckpt"
DEFAULT_REG = REPO / "checkpoints/tabicl-m-sa-20k/reg/step-10000.ckpt"


class TabICLMModel(TabICLv2Model):
    """TabICL-M: TabICLv2 with source-aware handling of incomplete, multi-source tables."""

    ag_key = "TA-TABICLM"
    ag_name = "TA-TabICL-M"
    _supported_problem_types = ["binary", "multiclass", "regression"]

    @classmethod
    def checkpoint_paths(cls) -> tuple[str, str]:
        return (
            os.environ.get("TABICLM_CLF", str(DEFAULT_CLF)),
            os.environ.get("TABICLM_REG", str(DEFAULT_REG)),
        )

    def _get_model_params(self) -> dict:
        params = super()._get_model_params()
        clf, reg = self.checkpoint_paths()
        params["model_path"] = reg if self.problem_type == "regression" else clf
        return params

    @classmethod
    def prefetch_weights(cls) -> None:
        for p in cls.checkpoint_paths():
            if not Path(p).exists():
                raise FileNotFoundError(f"TabICL-M checkpoint not found: {p} (run `git lfs pull`)")

    @classmethod
    def config_generator(cls) -> ConfigGenerator:
        """Default configuration only; TabICL-M is evaluated zero-shot like the other foundation models."""
        return ConfigGenerator(model_cls=cls, manual_configs=[{}], search_space={})
