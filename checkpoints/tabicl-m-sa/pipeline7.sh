#!/bin/bash
# Regression ablation: six regressor variants (3000 steps each from the released TabICLv2 regressor, one switch off
# at a time), evaluated on the seven regression datasets, leave-one-source-out and random split, 5 seeds.
cd /workspace/TabICL-M
source /venv/main/bin/activate
export HF_HOME=/workspace/.hf_home PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
log() { echo "=== $* $(date -u)"; }
DS="--datasets diabetes openml:531 openml:189 openml:42225 openml:44970 openml:507 openml:560 --max_rows 3000"
train_variant() {
    name=$1; shift
    dir=checkpoints/tabicl-m-sa-ablation-reg/$name; mkdir -p $dir/reg results/sa_ablation_reg/$name
    for attempt in 1 2 3; do
        [ -f $dir/reg/step-3000.ckpt ] && break
        log "$name attempt $attempt"
        env "$@" ARCH=source_aware DTYPE=bfloat16 N_JOBS=8 STEPS=3000 BATCH=32 SAVE_TEMP=500 SAVE_PERM=1500 CKPT_ROOT=$dir \
            bash scripts/train_v2_missing_stage4.sh reg >> $dir/reg.log 2>&1
        log "$name attempt $attempt exit=$?"
        newest=$(ls -1t $dir/reg/step-*.ckpt 2>/dev/null | head -1)
        [ -n "$newest" ] && ! python -c "import torch,sys; torch.load(sys.argv[1], map_location='cpu', weights_only=True)" $newest 2>/dev/null && { log "dropping corrupt $newest"; rm -f $newest; }
    done
    [ -f $dir/reg/step-3000.ckpt ] || { log "$name FAILED"; return; }
    for cfg in loso random_split; do
        split=source; [ $cfg = random_split ] && split=random
        python scripts/ablation_missingness.py --out results/sa_ablation_reg/$name/$cfg $DS --mechanisms block block_shift \
            --rates 0.3 0.5 --seeds 0 1 2 3 4 --split $split --models tabicl_aware --aware_ckpt_reg $dir/reg/step-3000.ckpt \
            --device cuda > results/sa_ablation_reg/$name/$cfg.log 2>&1
        log "$name eval $cfg exit=$?"
    done
    find $dir/reg -name 'step-*.ckpt' ! -name 'step-3000.ckpt' -delete
}
log "pipeline7 start"
train_variant full_3k
train_variant no_group_stats   COL_GROUP_STATS=False
train_variant no_row_mask      ROW_MISSING_AWARE=False
train_variant no_pattern_token PATTERN_TOKEN=False
train_variant no_objectives    RECON_MODE=cell CONSISTENCY_WEIGHT=0
train_variant arch_off         COL_GROUP_STATS=False ROW_MISSING_AWARE=False PATTERN_TOKEN=False RECON_MODE=cell CONSISTENCY_WEIGHT=0
python results/sa_ablation_reg/analyze.py > results/sa_ablation_reg/analyze.log 2>&1; log "analysis exit=$?"
for d in results/sa_ablation_reg/*/loso results/sa_ablation_reg/*/random_split; do for f in results.csv summary.csv summary.md args.json; do [ -f $d/$f ] && git add -f $d/$f; done; done
git add -f results/sa_ablation_reg/analyze.py results/sa_ablation_reg/summary.md checkpoints/tabicl-m-sa/pipeline7.sh
git commit -q -m "Add the regression ablation of the source-aware parts (regressor, 3k steps each, 7 datasets)

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>" && log "commit ok" || log "commit: nothing"
git push origin main >> checkpoints/tabicl-m-sa/push.log 2>&1 && log "push ok" || log "push FAILED"
log "pipeline7 done"
