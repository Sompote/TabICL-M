#!/bin/bash
cd /workspace/TabICL-M
source /venv/main/bin/activate
export HF_HOME=/workspace/.hf_home
COMMON="--models tabicl_impute tabicl_indicator tabicl_aware_zero tabicl_aware xgboost catboost \
  --aware_ckpt checkpoints/tabicl-m/clf/step-3000.ckpt --aware_ckpt_reg checkpoints/tabicl-m/reg/step-3000.ckpt \
  --mechanisms mcar mar mnar block --rates 0.1 0.3 0.5 --seeds 0 1 2 --device cuda --plot"
echo "=== builtin start $(date -u)"
python scripts/ablation_missingness.py --out results/ablation_m/builtin --datasets breast_cancer wine diabetes $COMMON > results/ablation_m/builtin.log 2>&1
echo "=== builtin exit=$? $(date -u)"
echo "=== openml start $(date -u)"
python scripts/ablation_missingness.py --out results/ablation_m/openml --datasets openml:31 openml:1590 openml:531 --max_rows 3000 $COMMON > results/ablation_m/openml.log 2>&1
echo "=== openml exit=$? $(date -u)"
echo "=== done"
