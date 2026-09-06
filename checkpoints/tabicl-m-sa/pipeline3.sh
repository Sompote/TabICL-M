#!/bin/bash
# Stage 3: broad benchmark (20 datasets) of the best source-aware checkpoint against TabPFN 2.5 / 3,
# the released model and CatBoost, on leave-one-source-out and random splits. Runs after stage 2.
cd /workspace/TabICL-M
export HF_HOME=/workspace/.hf_home
log() { echo "=== $* $(date -u)"; }
log "pipeline3 start"
until grep -q "=== pipeline2 done" checkpoints/tabicl-m-sa/pipeline2.log 2>/dev/null; do sleep 300; done
CLF=checkpoints/tabicl-m-sa-20k/clf/step-10000.ckpt; REG=checkpoints/tabicl-m-sa-20k/reg/step-10000.ckpt; TAG=20k
[ -f $CLF ] || { CLF=checkpoints/tabicl-m-sa/clf/step-10000.ckpt; TAG=10k; }
[ -f $REG ] || REG=checkpoints/tabicl-m-sa/reg/step-10000.ckpt
log "using $TAG checkpoints"
DS="--datasets breast_cancer wine diabetes openml:31 openml:1590 openml:531 openml:1461 openml:1494 openml:40701 openml:1063 openml:40994 openml:1480 openml:37 openml:1067 openml:23 openml:507 openml:189 openml:42225 openml:44970 openml:560 --max_rows 3000"
COMMON="$DS --mechanisms block block_shift --rates 0.3 0.5 --seeds 0 1 2 3 4"
mkdir -p results/broad
for cfg in loso random_split; do
    split=source; [ $cfg = random_split ] && split=random
    log "broad $cfg tabicl"
    /venv/main/bin/python scripts/ablation_missingness.py --out results/broad/$cfg $COMMON --split $split \
        --models tabicl_impute tabicl_aware tabicl_aware_ewt tabicl_aware_si catboost --aware_ckpt $CLF --aware_ckpt_reg $REG --device cuda \
        > results/broad/$cfg.log 2>&1; log "broad $cfg tabicl exit=$?"
    log "broad $cfg tabpfn"
    /venv/tabpfn25/bin/python scripts/ablation_missingness.py --out results/broad/tabpfn_$cfg $COMMON --split $split \
        --models tabpfn25 tabpfn3 --device cuda > results/broad/tabpfn_$cfg.log 2>&1; log "broad $cfg tabpfn exit=$?"
done
/venv/main/bin/python results/broad/analyze.py > results/broad/analyze.log 2>&1; log "broad analysis exit=$?"
/venv/main/bin/python results/sa_eval/readme_section.py; log "readme exit=$?"
for d in results/broad/loso results/broad/random_split results/broad/tabpfn_loso results/broad/tabpfn_random_split; do
    for f in results.csv summary.csv summary.md args.json; do [ -f $d/$f ] && git add -f $d/$f; done
done
git add -f results/broad/analyze.py results/broad/summary.md checkpoints/tabicl-m-sa/pipeline3.sh README.md 2>/dev/null
git commit -q -m "Add the 20-dataset benchmark against TabPFN 2.5 and TabPFN-3 (LOSO and random split)

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01DEzEXesiFKLR2RFiARW6AQ" && log "commit ok" || log "commit: nothing"
git push origin main >> checkpoints/tabicl-m-sa/push.log 2>&1 && log "push ok" || log "push FAILED"
log "pipeline3 done"
