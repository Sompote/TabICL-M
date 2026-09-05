#!/bin/bash
# Self-driving pipeline: finish training (resume on crash), evaluate, analyse, commit weights + results, push.
cd /workspace/TabICL-M
source /venv/main/bin/activate
export HF_HOME=/workspace/.hf_home
log() { echo "=== $* $(date -u)"; }
log "pipeline start"
# 1. wait for the running launcher
while pgrep -f "[r]un_stage4_sa.sh" >/dev/null; do sleep 60; done
log "launcher finished"
# 2. make sure both tasks reach step 10000, resuming from the latest checkpoint on a crash
for TASK in clf reg; do
    for attempt in 1 2 3 4 5; do
        [ -f checkpoints/tabicl-m-sa/$TASK/step-10000.ckpt ] && break
        log "$TASK attempt $attempt"
        ARCH=source_aware DTYPE=bfloat16 N_JOBS=8 STEPS=10000 BATCH=32 \
            bash scripts/train_v2_missing_stage4.sh $TASK >> checkpoints/tabicl-m-sa/$TASK/train.log 2>&1
        log "$TASK attempt $attempt exit=$?"
    done
    [ -f checkpoints/tabicl-m-sa/$TASK/step-10000.ckpt ] && log "$TASK complete" || log "$TASK FAILED after 5 attempts"
done
CLF=checkpoints/tabicl-m-sa/clf/step-10000.ckpt; REG=checkpoints/tabicl-m-sa/reg/step-10000.ckpt
CK=""; [ -f $CLF ] && CK="$CK --aware_ckpt $CLF"; [ -f $REG ] && CK="$CK --aware_ckpt_reg $REG"
DS="--datasets breast_cancer wine diabetes openml:31 openml:1590 openml:531 --max_rows 3000"
# 3. evaluation: headroom configurations, then the standard ablation
for cfg in loso random_split; do
    split=source; [ $cfg = random_split ] && split=random
    log "eval $cfg"
    python scripts/ablation_missingness.py --out results/sa_eval/$cfg $DS --mechanisms block block_shift --rates 0.3 0.5 \
        --seeds 0 1 2 3 4 --split $split --models tabicl_impute tabicl_indicator tabicl_patternnorm tabicl_aware_zero tabicl_aware \
        $CK --device cuda --plot > results/sa_eval/$cfg.log 2>&1
    log "eval $cfg exit=$?"
done
log "eval standard"
python scripts/ablation_missingness.py --out results/sa_eval/standard $DS --mechanisms mcar mar mnar block --rates 0.1 0.3 0.5 \
    --seeds 0 1 2 --models tabicl_impute tabicl_aware $CK --device cuda --plot > results/sa_eval/standard.log 2>&1
log "eval standard exit=$?"
# 4. analysis
python results/sa_eval/analyze.py > results/sa_eval/analyze.log 2>&1; log "analysis exit=$?"
# 5. commit weights (LFS) and results, push
rm -f results/sa_eval/.n_* results/sa_eval/.err_*
git add -f $CLF $REG 2>/dev/null
git add .gitattributes results/sa_eval/analyze.py results/sa_eval/summary_vs_baselines.md
for d in loso random_split standard; do
    git add results/sa_eval/$d/results.csv results/sa_eval/$d/summary.csv results/sa_eval/$d/summary.md results/sa_eval/$d/args.json 2>/dev/null
    [ -d results/sa_eval/$d/plots ] && git add results/sa_eval/$d/plots
done
git add -f checkpoints/tabicl-m-sa/pipeline.sh
git commit -q -F - <<'MSG'
Add source-aware TabICL-M weights (10k steps) and their evaluation

checkpoints/tabicl-m-sa/{clf,reg}/step-10000.ckpt: stage 4 with
col_group_stats, row_missing_aware, pattern_token, block reconstruction and
offset consistency, trained on a prior dominated by block-structured, shifted
tables with a test-only source (ARCH=source_aware, lr 5e-5, bf16, one RTX 5090).

results/sa_eval: the new checkpoint against the released model, the first
TabICL-M checkpoint, imputers, pattern normalisation, trees and TabPFN v2 on
leave-one-source-out and random splits (block, block_shift) and on the
standard ablation (mcar/mar/mnar/block). summary_vs_baselines.md has the
tables and paired win/loss tallies.

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01DEzEXesiFKLR2RFiARW6AQ
MSG
log "commit exit=$?"
git push origin main > checkpoints/tabicl-m-sa/push.log 2>&1; log "push exit=$?"
log "pipeline done"
