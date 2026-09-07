#!/bin/bash
# Serialise the GPU work: finish the cheap test-time regression variants, then run stage 4c.
cd /workspace/TabICL-M
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
echo "=== driver start $(date -u)"
while pgrep -f "[r]egression/run.sh" > /dev/null; do sleep 60; done
echo "=== variants finished $(date -u)"
bash checkpoints/tabicl-m-sa/pipeline4.sh > checkpoints/tabicl-m-sa/pipeline4.log 2>&1
echo "=== driver done $(date -u)"
