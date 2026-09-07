#!/bin/bash
# Stage 4c (regressor only): continue the 20k regressor on a prior with half the tables complete, to recover
# base regression strength while keeping the source-aware parts; then evaluate on the regression datasets.
cd /workspace/TabICL-M
source /venv/main/bin/activate
export HF_HOME=/workspace/.hf_home
log() { echo "=== $* $(date -u)"; }
log "pipeline4 start"
SRC=checkpoints/tabicl-m-sa-20k/reg/step-10000.ckpt; dir=checkpoints/tabicl-m-sa-30k; mkdir -p $dir/reg
for attempt in 1 2 3 4 5; do
    [ -f $dir/reg/step-10000.ckpt ] && break
    log "4c reg attempt $attempt"
    RELEASED_CKPT=$SRC LR=2e-5 P_APPLY=0.5 P_SHIFT=1.0 P_NOISE=0.8 MAX_SHIFT=1.2 MAX_NOISE=0.5 MIN_OBS_FRAC=0.2 P_CONTIGUOUS=0.9 \
        CONSISTENCY_SHIFT_MAX=1.2 CONSISTENCY_NOISE_MAX=0.5 CONSISTENCY_WEIGHT=0.3 \
        ARCH=source_aware DTYPE=bfloat16 N_JOBS=8 STEPS=10000 BATCH=32 CKPT_ROOT=$dir \
        bash scripts/train_v2_missing_stage4.sh reg >> $dir/reg/train.log 2>&1
    log "4c reg attempt $attempt exit=$?"
done
[ -f $dir/reg/step-10000.ckpt ] || { log "4c reg FAILED"; log "pipeline4 done"; exit 0; }
DS="--datasets diabetes openml:531 openml:189 openml:42225 openml:44970 openml:507 openml:560 --max_rows 3000"
for cfg in random_split loso; do
    split=source; [ $cfg = random_split ] && split=random
    log "4c eval $cfg"
    python scripts/ablation_missingness.py --out results/regression/stage4c_$cfg $DS --mechanisms block block_shift --rates 0.3 0.5 \
        --seeds 0 1 2 3 4 --split $split --models tabicl_aware tabicl_aware_n32 --aware_ckpt_reg $dir/reg/step-10000.ckpt --device cuda \
        > results/regression/stage4c_$cfg.log 2>&1; log "4c eval $cfg exit=$?"
done
for d in results/regression/stage4c_random_split results/regression/stage4c_loso; do for f in results.csv summary.csv summary.md args.json; do [ -f $d/$f ] && git add -f $d/$f; done; done
git add -f checkpoints/tabicl-m-sa/pipeline4.sh
git commit -q -m "Add stage-4c regressor evaluation (continued on a half-complete prior)

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01DEzEXesiFKLR2RFiARW6AQ" && log "commit ok" || log "commit: nothing"
git push origin main >> checkpoints/tabicl-m-sa/push.log 2>&1 && log "push ok" || log "push FAILED"
log "pipeline4 done"
