#!/bin/bash
# Second self-driving stage. Phase B: ablate each source-aware part (classifier, 3000 steps each,
# one switch off). Phase C: continue both source-aware checkpoints to 20k steps (stage 4b).
# Each phase evaluates, analyses, writes the README section, commits and pushes.
cd /workspace/TabICL-M
source /venv/main/bin/activate
export HF_HOME=/workspace/.hf_home
log() { echo "=== $* $(date -u)"; }
commit_push() {  # $1 = message; the rest = paths (weights need -f)
    msg=$1; shift
    for p in "$@"; do git add -f "$p" 2>/dev/null; done
    git add .gitattributes README.md 2>/dev/null
    git commit -q -m "$msg

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01DEzEXesiFKLR2RFiARW6AQ" && log "commit ok" || log "commit: nothing to commit"
    git push origin main >> checkpoints/tabicl-m-sa/push.log 2>&1 && log "push ok" || log "push FAILED (see push.log)"
}
add_results() { for d in "$@"; do for f in results.csv summary.csv summary.md args.json; do [ -f $d/$f ] && git add -f $d/$f; done; [ -d $d/plots ] && git add -f $d/plots; done; }
log "pipeline2 start"
until grep -q "=== pipeline done" checkpoints/tabicl-m-sa/pipeline.log 2>/dev/null; do sleep 120; done
log "phase B: ablations"
DS_CLF="--datasets breast_cancer wine openml:31 openml:1590 --max_rows 3000"
train_variant() {
    name=$1; shift
    dir=checkpoints/tabicl-m-sa-ablation/$name; mkdir -p $dir results/sa_ablation/$name
    for attempt in 1 2 3; do
        [ -f $dir/clf/step-3000.ckpt ] && break
        log "$name attempt $attempt"
        env "$@" ARCH=source_aware DTYPE=bfloat16 N_JOBS=8 STEPS=3000 BATCH=32 CKPT_ROOT=$dir \
            bash scripts/train_v2_missing_stage4.sh clf >> $dir/clf.log 2>&1
        log "$name attempt $attempt exit=$?"
    done
    [ -f $dir/clf/step-3000.ckpt ] || { log "$name FAILED"; return; }
    for cfg in loso random_split; do
        split=source; [ $cfg = random_split ] && split=random
        python scripts/ablation_missingness.py --out results/sa_ablation/$name/$cfg $DS_CLF --mechanisms block block_shift \
            --rates 0.3 0.5 --seeds 0 1 2 3 4 --split $split --models tabicl_aware --aware_ckpt $dir/clf/step-3000.ckpt \
            --device cuda > results/sa_ablation/$name/$cfg.log 2>&1
        log "$name eval $cfg exit=$?"
    done
    rm -f $dir/clf/step-*[!0]0.ckpt 2>/dev/null   # keep only step-3000 to save disk
}
train_variant full_3k
train_variant no_group_stats   COL_GROUP_STATS=False
train_variant no_row_mask      ROW_MISSING_AWARE=False
train_variant no_pattern_token PATTERN_TOKEN=False
train_variant no_objectives    RECON_MODE=cell CONSISTENCY_WEIGHT=0
train_variant arch_off         COL_GROUP_STATS=False ROW_MISSING_AWARE=False PATTERN_TOKEN=False RECON_MODE=cell CONSISTENCY_WEIGHT=0
python results/sa_ablation/analyze.py > results/sa_ablation/analyze.log 2>&1; log "ablation analysis exit=$?"
python results/sa_eval/readme_section.py; log "readme exit=$?"
add_results results/sa_ablation/*/loso results/sa_ablation/*/random_split
commit_push "Add per-part ablation of the source-aware architecture (classifier, 3k steps each)" results/sa_ablation/analyze.py results/sa_ablation/summary.md results/sa_eval/readme_section.py checkpoints/tabicl-m-sa/pipeline2.sh
log "phase C: stage 4b, continue to 20k steps"
DS="--datasets breast_cancer wine diabetes openml:31 openml:1590 openml:531 --max_rows 3000"
for TASK in clf reg; do
    SRC=checkpoints/tabicl-m-sa/$TASK/step-10000.ckpt
    [ -f $SRC ] || { log "$TASK: no 10k checkpoint, skipping stage 4b"; continue; }
    dir=checkpoints/tabicl-m-sa-20k; mkdir -p $dir/$TASK
    for attempt in 1 2 3 4 5; do
        [ -f $dir/$TASK/step-10000.ckpt ] && break
        log "4b $TASK attempt $attempt"
        RELEASED_CKPT=$SRC LR=2e-5 ARCH=source_aware DTYPE=bfloat16 N_JOBS=8 STEPS=10000 BATCH=32 CKPT_ROOT=$dir \
            bash scripts/train_v2_missing_stage4.sh $TASK >> $dir/$TASK/train.log 2>&1
        log "4b $TASK attempt $attempt exit=$?"
    done
done
CLF=checkpoints/tabicl-m-sa-20k/clf/step-10000.ckpt; REG=checkpoints/tabicl-m-sa-20k/reg/step-10000.ckpt
CK=""; [ -f $CLF ] && CK="$CK --aware_ckpt $CLF"; [ -f $REG ] && CK="$CK --aware_ckpt_reg $REG"
if [ -n "$CK" ]; then
    mkdir -p results/sa_eval_20k && cp results/sa_eval/analyze.py results/sa_eval_20k/analyze.py
    for cfg in loso random_split; do
        split=source; [ $cfg = random_split ] && split=random
        log "4b eval $cfg"
        python scripts/ablation_missingness.py --out results/sa_eval_20k/$cfg $DS --mechanisms block block_shift --rates 0.3 0.5 \
            --seeds 0 1 2 3 4 --split $split --models tabicl_impute tabicl_aware_zero tabicl_aware $CK --device cuda --plot \
            > results/sa_eval_20k/$cfg.log 2>&1; log "4b eval $cfg exit=$?"
    done
    log "4b eval standard"
    python scripts/ablation_missingness.py --out results/sa_eval_20k/standard $DS --mechanisms mcar mar mnar block --rates 0.1 0.3 0.5 \
        --seeds 0 1 2 --models tabicl_impute tabicl_aware $CK --device cuda --plot > results/sa_eval_20k/standard.log 2>&1
    log "4b eval standard exit=$?"
    python results/sa_eval_20k/analyze.py > results/sa_eval_20k/analyze.log 2>&1; log "4b analysis exit=$?"
    python results/sa_eval/readme_section.py; log "readme exit=$?"
    add_results results/sa_eval_20k/loso results/sa_eval_20k/random_split results/sa_eval_20k/standard
    commit_push "Add stage-4b evaluation (source-aware checkpoints continued to 20k steps)" results/sa_eval_20k/analyze.py results/sa_eval_20k/summary_vs_baselines.md
    commit_push "Add source-aware TabICL-M weights at 20k steps (git LFS)" $CLF $REG
fi
log "pipeline2 done"
