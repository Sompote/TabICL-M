#!/bin/bash
# Regression-specific test-time variants on the 7 regression datasets, random split and LOSO.
cd /workspace/TabICL-M; export HF_HOME=/workspace/.hf_home
DS="--datasets diabetes openml:531 openml:189 openml:42225 openml:44970 openml:507 openml:560 --max_rows 3000"
COMMON="$DS --mechanisms block block_shift --rates 0.3 0.5 --seeds 0 1 2 3 4"
CK="--aware_ckpt checkpoints/tabicl-m-sa-20k/clf/step-10000.ckpt --aware_ckpt_reg checkpoints/tabicl-m-sa-20k/reg/step-10000.ckpt"
for cfg in random_split loso; do
  split=source; [ $cfg = random_split ] && split=random
  echo "=== $cfg tabicl start $(date -u)"
  /venv/main/bin/python scripts/ablation_missingness.py --out results/regression/$cfg $COMMON --split $split \
    --models tabicl_aware tabicl_aware_n32 tabicl_aware_med tabicl_aware_ypow tabicl_aware_n32_ypow $CK --device cuda > results/regression/$cfg.log 2>&1
  echo "=== $cfg tabicl exit=$? $(date -u)"
  echo "=== $cfg tabpfn start $(date -u)"
  /venv/tabpfn25/bin/python scripts/ablation_missingness.py --out results/regression/tabpfn_$cfg $COMMON --split $split \
    --models tabpfn3 tabpfn3_n32 --device cuda > results/regression/tabpfn_$cfg.log 2>&1
  echo "=== $cfg tabpfn exit=$? $(date -u)"
done
echo "=== done"
