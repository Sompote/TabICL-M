#!/bin/bash
# Full TabICL-M stage-4 run on one RTX 5090: classifier then regressor.
cd /workspace/TabICL-M
source /venv/main/bin/activate
export HF_HOME=/workspace/.hf_home
export DTYPE=bfloat16 N_JOBS=8
for TASK in clf reg; do
    echo "=== $TASK start $(date) ==="
    bash scripts/train_v2_missing_stage4.sh $TASK > checkpoints/tabicl-m/$TASK/train.log 2>&1
    echo "=== $TASK exit=$? $(date) ==="
done
