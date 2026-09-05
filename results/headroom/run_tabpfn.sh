#!/bin/bash
# TabPFN v2 (public HF weights, tabpfn==2.2.1) on the same three headroom configurations.
cd /workspace/TabICL-M
source /venv/main/bin/activate
export HF_HOME=/workspace/.hf_home
until grep -q "=== done" results/headroom/runner.log; do sleep 15; done   # wait for the GPU
COMMON="--datasets breast_cancer wine diabetes openml:31 openml:1590 openml:531 --max_rows 3000 \
  --mechanisms block block_shift --rates 0.3 0.5 --seeds 0 1 2 3 4 --models tabpfn --device cuda"
run() { echo "=== $1 start $(date -u)"; python scripts/ablation_missingness.py --out results/headroom/tabpfn_$1 $COMMON "${@:2}" > results/headroom/tabpfn_$1.log 2>&1; echo "=== $1 exit=$? $(date -u)"; }
run random_split --split random
run loso         --split source
run loso_srccol  --split source --add_source_col
echo "=== done"
