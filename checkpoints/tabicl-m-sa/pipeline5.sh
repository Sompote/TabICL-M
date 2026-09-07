#!/bin/bash
# Stage 5: decide on regression. Wait for the test-time variants and stage 4c; if still behind TabPFN-3,
# stage 4d (regressor, 20k more steps on a mostly complete prior) and the best test-time recipe; write the verdict.
cd /workspace/TabICL-M; export HF_HOME=/workspace/.hf_home
log() { echo "=== $* $(date -u)"; }
log "pipeline5 start"
until grep -q "=== done" results/regression/runner.log 2>/dev/null && grep -q "=== pipeline4 done" checkpoints/tabicl-m-sa/pipeline4.log 2>/dev/null; do sleep 300; done
/venv/main/bin/python results/regression/analyze.py > results/regression/analyze.log 2>&1; log "analysis 1 exit=$? $(cat results/regression/verdict.txt)"
DS="--datasets diabetes openml:531 openml:189 openml:42225 openml:44970 openml:507 openml:560 --max_rows 3000"
if grep -q BEHIND results/regression/verdict.txt; then
    SRC=checkpoints/tabicl-m-sa-30k/reg/step-10000.ckpt; [ -f $SRC ] || SRC=checkpoints/tabicl-m-sa-20k/reg/step-10000.ckpt
    dir=checkpoints/tabicl-m-sa-50k; mkdir -p $dir/reg
    for attempt in 1 2 3 4 5; do
        [ -f $dir/reg/step-20000.ckpt ] && break
        log "4d reg attempt $attempt (from $SRC)"
        RELEASED_CKPT=$SRC LR=1e-5 P_APPLY=0.3 P_SHIFT=1.0 P_NOISE=0.8 MAX_SHIFT=1.2 MAX_NOISE=0.5 MIN_OBS_FRAC=0.2 P_CONTIGUOUS=0.9 \
            CONSISTENCY_SHIFT_MAX=1.2 CONSISTENCY_NOISE_MAX=0.5 CONSISTENCY_WEIGHT=0.3 \
            ARCH=source_aware DTYPE=bfloat16 N_JOBS=8 STEPS=20000 BATCH=32 CKPT_ROOT=$dir \
            bash scripts/train_v2_missing_stage4.sh reg >> $dir/reg/train.log 2>&1
        log "4d reg attempt $attempt exit=$?"
    done
    if [ -f $dir/reg/step-20000.ckpt ]; then
        for cfg in random_split loso; do
            split=source; [ $cfg = random_split ] && split=random
            log "4d eval $cfg"
            /venv/main/bin/python scripts/ablation_missingness.py --out results/regression/stage4d_$cfg $DS --mechanisms block block_shift \
                --rates 0.3 0.5 --seeds 0 1 2 3 4 --split $split --models tabicl_aware tabicl_aware_n32_ypow tabicl_aware_n32_ypow_qn \
                --aware_ckpt_reg $dir/reg/step-20000.ckpt --device cuda > results/regression/stage4d_$cfg.log 2>&1; log "4d eval $cfg exit=$?"
        done
        /venv/main/bin/python results/regression/analyze.py > results/regression/analyze.log 2>&1; log "analysis 2 exit=$? $(cat results/regression/verdict.txt)"
    else
        log "4d FAILED"
    fi
fi
/venv/main/bin/python results/regression/readme_update.py; log "readme exit=$?"
for d in results/regression/*/; do for f in results.csv summary.csv summary.md args.json; do [ -f $d$f ] && git add -f $d$f; done; done
git add -f results/regression/run.sh results/regression/analyze.py results/regression/readme_update.py results/regression/summary.md results/regression/verdict.txt checkpoints/tabicl-m-sa/pipeline5.sh README.md scripts/ablation_missingness.py
git commit -q -m "Regression against TabPFN-3: test-time variants, stage 4c/4d, verdict

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01DEzEXesiFKLR2RFiARW6AQ" && log "commit ok" || log "commit: nothing"
git push origin main >> checkpoints/tabicl-m-sa/push.log 2>&1 && log "push ok" || log "push FAILED"
log "pipeline5 done"
