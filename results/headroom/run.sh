#!/bin/bash
# Headroom experiment: does any missingness regime leave room over mean imputation?
# Block missingness with and without per-source shift, random split vs leave-one-source-out.
cd /workspace/TabICL-M
source /venv/main/bin/activate
export HF_HOME=/workspace/.hf_home
COMMON="--datasets breast_cancer wine diabetes openml:31 openml:1590 openml:531 --max_rows 3000 \
  --mechanisms block block_shift --rates 0.3 0.5 --seeds 0 1 2 3 4 \
  --models tabicl_impute tabicl_indicator tabicl_iterimpute tabicl_knnimpute tabicl_aware_zero tabicl_aware xgboost catboost \
  --aware_ckpt checkpoints/tabicl-m/clf/step-3000.ckpt --aware_ckpt_reg checkpoints/tabicl-m/reg/step-3000.ckpt --device cuda --plot"
run() { echo "=== $1 start $(date -u)"; python scripts/ablation_missingness.py --out results/headroom/$1 $COMMON "${@:2}" > results/headroom/$1.log 2>&1; echo "=== $1 exit=$? $(date -u)"; }
run random_split --split random
run loso         --split source
run loso_srccol  --split source --add_source_col
echo "=== done"
