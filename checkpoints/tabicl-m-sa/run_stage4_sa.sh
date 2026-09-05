#!/bin/bash
# TabICL-M source-aware stage 4 on one RTX 5090: classifier then regressor, 10k steps each.
cd /workspace/TabICL-M
source /venv/main/bin/activate
export HF_HOME=/workspace/.hf_home
until grep -q "=== done" results/headroom/runner_patternnorm.log 2>/dev/null; do sleep 30; done   # wait for the GPU
export ARCH=source_aware DTYPE=bfloat16 N_JOBS=8 STEPS=10000 BATCH=32
for TASK in clf reg; do
    echo "=== $TASK start $(date -u)"
    bash scripts/train_v2_missing_stage4.sh $TASK > checkpoints/tabicl-m-sa/$TASK/train.log 2>&1
    echo "=== $TASK exit=$? $(date -u)"
done
echo "=== done"
