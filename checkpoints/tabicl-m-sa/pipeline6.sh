#!/bin/bash
# Regression endgame, restartable and disk-safe:
#   1. evaluate the partial stage-4c checkpoint (is a more complete prior moving regression at all?)
#   2. finish stage 4c, evaluate
#   3. if still behind TabPFN-3 on the random split, run stage 4d (mostly complete prior), evaluate
#   4. verdict, README section, commit, push
# A janitor keeps only the newest checkpoints of the active run: a 10k-step run otherwise writes ~11 GB.
cd /workspace/TabICL-M
export HF_HOME=/workspace/.hf_home PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
PY=/venv/main/bin/python
log() { echo "=== $* $(date -u)"; }
DS="--datasets diabetes openml:531 openml:189 openml:42225 openml:44970 openml:507 openml:560 --max_rows 3000"
EVOPTS="--mechanisms block block_shift --rates 0.3 0.5 --seeds 0 1 2 3 4 --models tabicl_aware tabicl_aware_n32_ypow --device cuda"
janitor() {  # $1 = dir to prune, keep the 3 newest checkpoints
    while true; do
        ls -1t $1/step-*.ckpt 2>/dev/null | tail -n +4 | xargs -r rm -f
        df --output=avail -k / | tail -1 | awk '{if ($1 < 5000000) print "=== LOW DISK"}'
        sleep 120
    done
}
evaluate() {  # $1 = ckpt, $2 = tag
    for cfg in random_split loso; do
        split=source; [ $cfg = random_split ] && split=random
        $PY scripts/ablation_missingness.py --out results/regression/$2_$cfg $DS $EVOPTS --split $split \
            --aware_ckpt_reg $1 > results/regression/$2_$cfg.log 2>&1
        log "eval $2 $cfg exit=$?"
    done
}
train() {  # $1 = source ckpt, $2 = out dir, $3 = steps, $4 = lr, $5 = p_apply, $6 = final ckpt name
    mkdir -p $2/reg; janitor $2/reg & JAN=$!
    for attempt in 1 2 3; do
        [ -f $2/reg/$6 ] && break
        log "train $2 attempt $attempt"
        RELEASED_CKPT=$1 LR=$4 P_APPLY=$5 P_SHIFT=1.0 P_NOISE=0.8 MAX_SHIFT=1.2 MAX_NOISE=0.5 MIN_OBS_FRAC=0.2 \
            P_CONTIGUOUS=0.9 CONSISTENCY_SHIFT_MAX=1.2 CONSISTENCY_NOISE_MAX=0.5 CONSISTENCY_WEIGHT=0.3 \
            SAVE_TEMP=500 SAVE_PERM=2500 ARCH=source_aware DTYPE=bfloat16 N_JOBS=8 STEPS=$3 BATCH=32 CKPT_ROOT=$2 \
            bash scripts/train_v2_missing_stage4.sh reg >> $2/reg/train.log 2>&1
        log "train $2 attempt $attempt exit=$?"
        # a truncated checkpoint (disk pressure) breaks every resume: drop the newest and retry
        newest=$(ls -1t $2/reg/step-*.ckpt 2>/dev/null | head -1)
        [ -n "$newest" ] && ! $PY -c "import torch,sys; torch.load(sys.argv[1], map_location='cpu', weights_only=True)" $newest 2>/dev/null && { log "dropping corrupt $newest"; rm -f $newest; }
    done
    kill $JAN 2>/dev/null
}
finish() {  # analysis, README, commit, push
    $PY results/regression/analyze.py > results/regression/analyze.log 2>&1; log "analysis exit=$? $(cat results/regression/verdict.txt 2>/dev/null)"
    $PY results/regression/readme_update.py >> results/regression/analyze.log 2>&1; log "readme exit=$?"
    for d in results/regression/*/; do for f in results.csv summary.csv summary.md args.json; do [ -f $d$f ] && git add -f $d$f; done; done
    git add -f results/regression/summary.md results/regression/verdict.txt results/regression/analyze.py README.md \
        scripts/train_v2_missing_stage4.sh checkpoints/tabicl-m-sa/pipeline6.sh 2>/dev/null
    git commit -q -m "$1

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01DEzEXesiFKLR2RFiARW6AQ" && log "commit ok" || log "commit: nothing"
    git push origin main >> checkpoints/tabicl-m-sa/push.log 2>&1 && log "push ok" || log "push FAILED"
}
log "pipeline6 start"
[ -f checkpoints/tabicl-m-sa-30k/reg/step-3500.ckpt ] && { log "eval partial stage 4c (step 3500)"; evaluate checkpoints/tabicl-m-sa-30k/reg/step-3500.ckpt stage4c3500; }
finish "Add the partial stage-4c regressor evaluation (3500 steps on a half-complete prior)"
log "finish stage 4c"
train checkpoints/tabicl-m-sa-20k/reg/step-10000.ckpt checkpoints/tabicl-m-sa-30k 10000 2e-5 0.5 step-10000.ckpt
[ -f checkpoints/tabicl-m-sa-30k/reg/step-10000.ckpt ] && evaluate checkpoints/tabicl-m-sa-30k/reg/step-10000.ckpt stage4c || log "stage 4c FAILED"
finish "Add the stage-4c regressor (10k steps on a half-complete prior) and its evaluation"
if grep -q "random_split=BEHIND" results/regression/verdict.txt 2>/dev/null; then
    log "still behind on the random split: stage 4d"
    SRC=checkpoints/tabicl-m-sa-30k/reg/step-10000.ckpt; [ -f $SRC ] || SRC=checkpoints/tabicl-m-sa-20k/reg/step-10000.ckpt
    train $SRC checkpoints/tabicl-m-sa-50k 20000 1e-5 0.3 step-20000.ckpt
    [ -f checkpoints/tabicl-m-sa-50k/reg/step-20000.ckpt ] && evaluate checkpoints/tabicl-m-sa-50k/reg/step-20000.ckpt stage4d || log "stage 4d FAILED"
    finish "Add the stage-4d regressor (20k steps on a mostly complete prior) and the final regression verdict"
fi
log "pipeline6 done"
