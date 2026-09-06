#!/bin/bash
# TabPFN 2.5 / 2.6 / 3 (Hugging Face default checkpoints, tabpfn 8.5 in its own venv) on the headroom configurations.
cd /workspace/TabICL-M
source /venv/tabpfn25/bin/activate
export HF_HOME=/workspace/.hf_home
COMMON="--datasets breast_cancer wine diabetes openml:31 openml:1590 openml:531 --max_rows 3000 \
  --mechanisms block block_shift --rates 0.3 0.5 --seeds 0 1 2 3 4 --device cuda"
for m in tabpfn25 tabpfn26 tabpfn3; do
  for cfg in loso random_split; do
    split=source; [ $cfg = random_split ] && split=random
    echo "=== $m $cfg start $(date -u)"
    python scripts/ablation_missingness.py --out results/headroom/${m}_$cfg $COMMON --split $split --models $m > results/headroom/${m}_$cfg.log 2>&1
    echo "=== $m $cfg exit=$? $(date -u)"
  done
done
echo "=== done"
