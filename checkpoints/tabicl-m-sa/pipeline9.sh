#!/bin/bash
# Stage 6: benchmark TabICL-M on TabArena-Lite and BeyondArena (grouped splits) with the TabArena framework,
# compare to the cached leaderboards, commit the results. Waits for the bar-head retrain (GPU) and the install.
cd /workspace/TabICL-M
export HF_HOME=/workspace/.hf_home PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
log() { echo "=== $* $(date -u)"; }
log "pipeline9 start"
until grep -q "=== pipeline8 done" checkpoints/tabicl-m-sa/pipeline8.log 2>/dev/null; do sleep 300; done
until /venv/tabarena/bin/python -c "import tabarena, tabicl" 2>/dev/null; do log "waiting for /venv/tabarena"; sleep 300; done
export TABICLM_CLF=$PWD/checkpoints/tabicl-m-sa-20k/clf/step-10000.ckpt
export TABICLM_REG=$PWD/$(/venv/main/bin/python scripts/tabarena/select_regressor.py 2>>checkpoints/tabicl-m-sa/pipeline9.log)
log "regressor: $TABICLM_REG"
mkdir -p results/tabarena results/beyondarena
log "tabarena lite"
/venv/tabarena/bin/python scripts/tabarena/run_tabarena.py --suite tabarena --subset lite --out results/tabarena/lite > results/tabarena/lite.log 2>&1; log "tabarena lite exit=$?"
log "beyondarena grouped core"
/venv/tabarena/bin/python scripts/tabarena/run_tabarena.py --suite beyondarena --subset core grouped '!large' --out results/beyondarena/grouped > results/beyondarena/grouped.log 2>&1; log "beyondarena grouped exit=$?"
for f in results/tabarena/lite/leaderboard.csv results/tabarena/lite/leaderboard.md results/beyondarena/grouped/leaderboard.csv results/beyondarena/grouped/leaderboard.md; do [ -f $f ] && git add -f $f; done
git add -f scripts/tabarena checkpoints/tabicl-m-sa/pipeline9.sh
git commit -q -m "Benchmark TabICL-M on TabArena-Lite and BeyondArena grouped splits with the TabArena framework

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>" && log "commit ok" || log "commit: nothing"
git push origin main >> checkpoints/tabicl-m-sa/push.log 2>&1 && log "push ok" || log "push FAILED"
log "pipeline9 done"
