#!/bin/bash
# Stage 5: retrain the regressor with the bar head (from the 20k source-aware regressor; body reused, head from zero),
# mostly on TabICL's own prior (P_APPLY=0.3) with the source-aware parts kept on; then evaluate against TabPFN-3,
# write the verdict into the README and docs, commit the weights (LFS) and results, push. Waits for the regression ablation.
cd /workspace/TabICL-M
source /venv/main/bin/activate
export HF_HOME=/workspace/.hf_home PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
log() { echo "=== $* $(date -u)"; }
log "pipeline8 start"
until grep -q "=== pipeline7 done" checkpoints/tabicl-m-sa/pipeline7.log 2>/dev/null; do sleep 300; done
DIR=checkpoints/tabicl-m-sa-bar; mkdir -p $DIR/reg
janitor() { while true; do ls -1t $DIR/reg/step-*.ckpt 2>/dev/null | grep -v step-20000 | tail -n +4 | xargs -r rm -f; sleep 120; done; }
janitor & JAN=$!
for attempt in 1 2 3 4 5; do
    [ -f $DIR/reg/step-20000.ckpt ] && break
    log "bar train attempt $attempt"
    RELEASED_CKPT=checkpoints/tabicl-m-sa-20k/reg/step-10000.ckpt HEAD=bar NUM_BUCKETS=1000 \
        ARCH=source_aware LR=5e-5 P_APPLY=0.3 P_SHIFT=1.0 P_NOISE=0.8 MAX_SHIFT=1.2 MAX_NOISE=0.5 MIN_OBS_FRAC=0.2 P_CONTIGUOUS=0.9 \
        CONSISTENCY_WEIGHT=0.1 CONSISTENCY_SHIFT_MAX=1.2 CONSISTENCY_NOISE_MAX=0.5 \
        DTYPE=bfloat16 N_JOBS=8 STEPS=20000 BATCH=32 SAVE_TEMP=500 SAVE_PERM=5000 CKPT_ROOT=$DIR \
        bash scripts/train_v2_missing_stage4.sh reg >> $DIR/reg/train.log 2>&1
    log "bar train attempt $attempt exit=$?"
    newest=$(ls -1t $DIR/reg/step-*.ckpt 2>/dev/null | head -1)
    [ -n "$newest" ] && ! python -c "import torch,sys; torch.load(sys.argv[1], map_location='cpu', weights_only=True)" $newest 2>/dev/null && { log "dropping corrupt $newest"; rm -f $newest; }
done
kill $JAN 2>/dev/null
CK=$DIR/reg/step-20000.ckpt
if [ -f $CK ]; then
    DS="--datasets diabetes openml:531 openml:189 openml:42225 openml:44970 openml:507 openml:560 --max_rows 3000"
    for cfg in random_split loso; do
        split=source; [ $cfg = random_split ] && split=random
        log "bar eval $cfg"
        python scripts/ablation_missingness.py --out results/regression/stagebar_$cfg $DS --mechanisms block block_shift --rates 0.3 0.5 \
            --seeds 0 1 2 3 4 --split $split --models tabicl_aware tabicl_aware_n32 --aware_ckpt_reg $CK --device cuda \
            > results/regression/stagebar_$cfg.log 2>&1; log "bar eval $cfg exit=$?"
    done
else
    log "bar train FAILED after 5 attempts"
fi
python results/regression/analyze.py > results/regression/analyze.log 2>&1; log "analysis exit=$? $(cat results/regression/verdict.txt)"
python results/regression/readme_update.py >> results/regression/analyze.log 2>&1; log "readme exit=$?"
python results/sa_eval/readme_section.py >> results/regression/analyze.log 2>&1; log "docs exit=$?"
for d in results/regression/stagebar_random_split results/regression/stagebar_loso; do for f in results.csv summary.csv summary.md args.json; do [ -f $d/$f ] && git add -f $d/$f; done; done
[ -f $CK ] && git add -f $CK
git add -f results/regression/summary.md results/regression/verdict.txt README.md docs/results.md checkpoints/tabicl-m-sa/pipeline8.sh
git commit -q -m "Add the bar-head regressor (20k steps from the source-aware regressor) and its verdict against TabPFN-3

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>" && log "commit ok" || log "commit: nothing"
git push origin main >> checkpoints/tabicl-m-sa/push.log 2>&1 && log "push ok" || log "push FAILED"
log "pipeline8 done"
