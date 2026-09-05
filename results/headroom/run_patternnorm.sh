#!/bin/bash
# Level 0: pattern-conditional normalisation in front of the released TabICLv2, on the headroom configurations.
cd /workspace/TabICL-M
source /venv/main/bin/activate
export HF_HOME=/workspace/.hf_home
P=/tmp/claude-0/-workspace-TabICL-M/53d1cc77-4eb2-48ce-a6a2-d3f11554faee/scratchpad/pilot/clf.log
until tr '\r' '\n' < $P 2>/dev/null | grep -qE "200/200 \[|Traceback|RuntimeError"; do sleep 15; done; sleep 20   # wait for the GPU
COMMON="--datasets breast_cancer wine diabetes openml:31 openml:1590 openml:531 --max_rows 3000 \
  --mechanisms block block_shift --rates 0.3 0.5 --seeds 0 1 2 3 4 --models tabicl_patternnorm --device cuda"
run() { echo "=== $1 start $(date -u)"; python scripts/ablation_missingness.py --out results/headroom/patternnorm_$1 $COMMON "${@:2}" > results/headroom/patternnorm_$1.log 2>&1; echo "=== $1 exit=$? $(date -u)"; }
run loso         --split source
run random_split --split random
echo "=== done"
