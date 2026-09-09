#!/bin/bash
# pipeline10 — four regression levers against TabPFN-3, hands-off (user request 2026-09-09):
#   1. function-class diagnostic (synthetic tasks; which function class do we lose on?)
#   2. smooth-target prior component  + 3. point (Huber) loss  -> regressor continued 10k steps
#   4. neighbour-based context on large tables (KNNContextRegressor), evaluated at up to 20k rows
#   then: analysis, docs, commit, push; finally the BeyondArena grouped run that pipeline9 could not do
#   (data-foundry was missing) and a second commit/push.
cd /workspace/TabICL-M; export HF_HOME=/workspace/.hf_home
source /venv/main/bin/activate   # torchrun/python for the training script
LOG=checkpoints/tabicl-m-sa/pipeline10.log
log(){ echo "=== $* $(date -u)" | tee -a $LOG; }
PY=/venv/main/bin/python; PY25=/venv/tabpfn25/bin/python; PYTA=/venv/tabarena/bin/python
SRC=checkpoints/tabicl-m-sa-20k/reg/step-10000.ckpt
DIR=checkpoints/tabicl-m-sa-smooth; mkdir -p $DIR/reg
NEW=$DIR/reg/step-10000.ckpt
DS="--datasets diabetes openml:531 openml:189 openml:42225 openml:44970 openml:507 openml:560 --max_rows 3000"
COMMON="$DS --mechanisms block block_shift --rates 0.3 0.5 --seeds 0 1 2 3 4"
LARGE="--datasets openml:189 openml:507 openml:42225 --max_rows 20000 --mechanisms block_shift --rates 0.3 --seeds 0 1 2 --split random"
KNN="--knn_context 4000 --knn_min_rows 4500 --knn_group 512"
commit(){ git commit -q -m "$1

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>" && log "commit ok" || log "commit: nothing"; git push origin main >> checkpoints/tabicl-m-sa/push.log 2>&1 && log "push ok" || log "push FAILED"; }
log "pipeline10 start"

# ---- 1. diagnostic ---------------------------------------------------------------
mkdir -p results/function_class
if [ ! -f results/function_class/summary.md ]; then
    log "diag tabicl"
    $PY scripts/diag/function_class.py --out results/function_class --models tabicl_released tabicl_m --aware_ckpt_reg $SRC --device cuda > results/function_class/tabicl.log 2>&1; log "diag tabicl exit=$?"
    log "diag tabpfn3"
    $PY25 scripts/diag/function_class.py --out results/function_class --models tabpfn3 --device cuda > results/function_class/tabpfn.log 2>&1; log "diag tabpfn exit=$?"
    $PY scripts/diag/function_class.py --out results/function_class --summarize > results/function_class/summarize.log 2>&1; log "diag summary exit=$?"
    git add -f results/function_class/summary.md results/function_class/verdict.json results/function_class/results_*.csv scripts/diag/function_class.py 2>/dev/null
    commit "Function-class diagnostic: where the regressor loses to TabPFN-3 on synthetic smooth targets"
fi

# ---- 2+3. training: smooth-target prior + point loss, 10k steps from the 20k regressor ----
attempt=0
while [ -z "${SKIP_TRAIN:-}" ] && [ ! -f $NEW ] && [ $attempt -lt 5 ]; do
    attempt=$((attempt+1)); log "smooth train attempt $attempt"
    RELEASED_CKPT=$SRC SMOOTH_P=0.4 POINT_LOSS=0.2 LR=3e-5 P_APPLY=0.5 P_SHIFT=1.0 P_NOISE=0.8 MAX_SHIFT=1.2 MAX_NOISE=0.5 MIN_OBS_FRAC=0.2 P_CONTIGUOUS=0.9 \
        ARCH=source_aware DTYPE=bfloat16 N_JOBS=8 STEPS=10000 BATCH=32 SAVE_TEMP=500 SAVE_PERM=2500 CKPT_ROOT=$DIR \
        bash scripts/train_v2_missing_stage4.sh reg >> $DIR/reg/train.log 2>&1
    log "smooth train attempt $attempt exit=$?"
    newest=$(ls -1t $DIR/reg/step-*.ckpt 2>/dev/null | head -1)
    [ -n "$newest" ] && ! $PY -c "import torch,sys; torch.load(sys.argv[1], map_location='cpu', weights_only=True)" $newest 2>/dev/null && { log "dropping corrupt $newest"; rm -f $newest; }
done
if [ -f $NEW ]; then
    # keep only the final checkpoint of this run (disk)
    ls $DIR/reg/step-*.ckpt | grep -v step-10000.ckpt | xargs -r rm -f
    for cfg in random_split loso; do
        split=source; [ $cfg = random_split ] && split=random
        [ -f results/regression/stagesmooth_$cfg/results.csv ] && [ "$(wc -l < results/regression/stagesmooth_$cfg/results.csv)" -gt 300 ] && continue
        log "smooth eval $cfg"
        $PY scripts/ablation_missingness.py --out results/regression/stagesmooth_$cfg $COMMON --split $split \
            --models tabicl_aware tabicl_aware_n32 --aware_ckpt_reg $NEW --device cuda > results/regression/stagesmooth_$cfg.log 2>&1; log "smooth eval $cfg exit=$?"
    done
else
    log "smooth train skipped (SKIP_TRAIN) or FAILED"
fi

# ---- 4. neighbour-based context at large n (plain vs knn, both regressors, TabPFN-3) ----
mkdir -p results/regression
log "large-n eval 20k regressor"
$PY scripts/ablation_missingness.py --out results/regression/large_n_20k $LARGE $KNN --models tabicl_aware tabicl_aware_knn --aware_ckpt_reg $SRC --device cuda > results/regression/large_n_20k.log 2>&1; log "large-n 20k exit=$?"
if [ -f $NEW ]; then
    log "large-n eval smooth regressor"
    $PY scripts/ablation_missingness.py --out results/regression/large_n_smooth $LARGE $KNN --models tabicl_aware tabicl_aware_knn --aware_ckpt_reg $NEW --device cuda > results/regression/large_n_smooth.log 2>&1; log "large-n smooth exit=$?"
fi
log "large-n eval tabpfn3"
$PY25 scripts/ablation_missingness.py --out results/regression/large_n_tabpfn $LARGE --models tabpfn3 --device cuda > results/regression/large_n_tabpfn.log 2>&1; log "large-n tabpfn exit=$?"

# ---- analysis, docs, commit ----------------------------------------------------------
$PY results/regression/analyze.py > results/regression/analyze.log 2>&1; log "analysis exit=$? $(cat results/regression/verdict.txt 2>/dev/null | tr '\n' ' ')"
$PY results/regression/analyze_large_n.py >> results/regression/analyze.log 2>&1; log "large-n analysis exit=$?"
$PY results/regression/readme_update.py >> results/regression/analyze.log 2>&1; log "readme exit=$?"
$PY results/sa_eval/readme_section.py >> results/regression/analyze.log 2>&1; log "docs exit=$?"
for d in results/regression/stagesmooth_random_split results/regression/stagesmooth_loso results/regression/large_n_20k results/regression/large_n_smooth results/regression/large_n_tabpfn; do
    for f in results.csv summary.csv summary.md args.json; do [ -f $d/$f ] && git add -f $d/$f; done; done
[ -f $NEW ] && git add -f $NEW
git add -f results/regression/summary.md results/regression/verdict.txt results/regression/large_n_summary.md results/regression/analyze_large_n.py README.md docs/results.md checkpoints/tabicl-m-sa/pipeline10.sh 2>/dev/null
commit "Regression levers: smooth-target prior + point loss regressor (10k steps), neighbour-based context at large n, verdicts against TabPFN-3"

# ---- BeyondArena grouped (needs data-foundry, installed 2026-09-09) ----------------------
log "beyondarena grouped core"
$PYTA scripts/tabarena/run_tabarena.py --suite beyondarena --subset core grouped '!large' --out results/beyondarena/grouped > results/beyondarena/grouped.log 2>&1; log "beyondarena grouped exit=$?"
for f in results/beyondarena/grouped/leaderboard.csv results/beyondarena/grouped/leaderboard.md; do [ -f $f ] && git add -f $f; done
commit "Benchmark TabICL-M on BeyondArena grouped splits"
log "pipeline10 done"
