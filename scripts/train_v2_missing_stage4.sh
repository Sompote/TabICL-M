#!/bin/bash
# TabICL-M: continued pre-training of the released TabICLv2 checkpoint with
#   (1) the block-structured missingness prior      (--missing_enabled True)
#   (2) the missing-aware column embedding          (--col_missing_aware True)
#   (3) the masked-cell reconstruction objective    (--recon_weight 0.1)
#
# This is "Stage 4": it starts from the released Stage 3 weights. The new parameters
# (mask_linear, absence vector, reconstruction head) are zero at step 0, so the run
# starts exactly at the released model on complete data. Everything else copies the
# Stage 3 recipe (scripts/train_v2_clf_stage3.sh) with a lower learning rate, fewer
# steps and a smaller maximum sequence length so that it fits on one GPU.
#
# Usage:
#   bash scripts/train_v2_missing_stage4.sh clf     # classifier
#   bash scripts/train_v2_missing_stage4.sh reg     # regressor
#
# Requirements: pip install "tabicl[pretrain]"  (adds wandb, transformers, xgboost)
# Hardware: one NVIDIA GPU with >= 24 GB. With --max_seq_len 8192 and --batch_size 32
# an A100/H100 does roughly 1.5 to 3 steps per second; 3000 steps is about half an
# hour of training plus prior generation on the CPU workers (--n_jobs).
# Set --use_flash_attn3 True only on Hopper GPUs with flash-attn 3 installed.

set -euo pipefail

TASK=${1:-clf}                                   # clf | reg
NUM_GPUS=${NUM_GPUS:-1}
STEPS=${STEPS:-3000}
MAX_SEQ_LEN=${MAX_SEQ_LEN:-8192}
BATCH=${BATCH:-32}
LR=${LR:-1e-5}
RECON_WEIGHT=${RECON_WEIGHT:-0.1}
DTYPE=${DTYPE:-float32}                          # float32 | bfloat16 (autocast; bf16 needed without FA3 on 24-32 GB GPUs)
RECOMPUTE=${RECOMPUTE:-False}                    # activation checkpointing to cut memory
N_JOBS=${N_JOBS:-8}                              # CPU workers generating prior tables
CKPT_ROOT=${CKPT_ROOT:-checkpoints/tabicl-m}

# Released Stage 3 checkpoints (auto-downloaded to the Hugging Face cache by the
# sklearn estimators; or pass RELEASED_CKPT=/path/to/file.ckpt).
if [ "$TASK" = "clf" ]; then
    RELEASED_NAME=tabicl-classifier-v2-20260212.ckpt
    TASK_ARGS="--max_classes 10 --np_seed 42 --torch_seed 42"
elif [ "$TASK" = "reg" ]; then
    RELEASED_NAME=tabicl-regressor-v2-20260212.ckpt
    TASK_ARGS="--regression_method quantile --num_quantiles 999 --norm_type layernorm_nobias --np_seed 43 --torch_seed 43"
else
    echo "usage: $0 clf|reg"; exit 1
fi
RELEASED_CKPT=${RELEASED_CKPT:-$(ls "${HF_HOME:-$HOME/.cache/huggingface}"/hub/models--jingang--TabICL/snapshots/*/$RELEASED_NAME 2>/dev/null | head -1)}
if [ -z "$RELEASED_CKPT" ]; then
    echo "Released checkpoint not found. Run once in Python:  from tabicl import TabICLClassifier; TabICLClassifier()._load_model()"
    echo "or set RELEASED_CKPT=/path/to/$RELEASED_NAME"; exit 1
fi
CKPT_DIR=$CKPT_ROOT/$TASK
mkdir -p "$CKPT_DIR"

# Load the released weights only on the first launch; later launches resume from
# CKPT_DIR with optimizer state (passing --checkpoint_path would override that).
RESUME_ARGS="--checkpoint_path $RELEASED_CKPT --only_load_model True"
if ls "$CKPT_DIR"/step-*.ckpt >/dev/null 2>&1; then
    RESUME_ARGS=""
fi

torchrun --standalone --nproc_per_node=$NUM_GPUS -m tabicl.train \
            --wandb_log False \
            --wandb_project TabICL-M \
            --wandb_name tabicl_m_${TASK}_stage4 \
            --device cuda \
            --dtype $DTYPE \
            $TASK_ARGS \
            --max_steps $STEPS \
            --batch_size $BATCH \
            --micro_batch_size 1 \
            --lr $LR \
            --muon True \
            --beta1 0.9 \
            --weight_decay 0.01 \
            --use_cautious_wd False \
            --scheduler cosine_with_restarts \
            --warmup_proportion 0.05 \
            --cosine_num_cycles 1 \
            --cosine_amplitude_decay 1 \
            --cosine_lr_end 1e-7 \
            --gradient_clipping 1.0 \
            --prior_type graph_scm \
            --prior_device cpu \
            --n_jobs $N_JOBS \
            --batch_size_per_gp 1 \
            --min_features 1 \
            --max_features 100 \
            --min_seq_len 400 \
            --max_seq_len $MAX_SEQ_LEN \
            --log_seq_len True \
            --min_train_size 0.79 \
            --max_train_size 0.81 \
            --seq_len_per_gp True \
            --graph_noise False \
            --filter_unpredictable_graphs True \
            --filter_unpredictable_datasets True \
            --allow_act_warping False \
            --min_n_nodes 2 \
            --max_n_nodes 32 \
            --cauchy_dag_offset 0.0 \
            --missing_enabled True \
            --missing_p_apply 0.6 \
            --missing_p_cell 0.6 \
            --missing_p_block 0.6 \
            --missing_max_sources 8 \
            --missing_p_contiguous_sources 0.25 \
            --missing_p_source_shift 0.5 \
            --missing_p_source_noise 0.5 \
            --missing_p_source_column 0.5 \
            --col_missing_aware True \
            --recon_weight $RECON_WEIGHT \
            --recon_rate_max 0.3 \
            --recon_p_apply 0.5 \
            --embed_dim 128 \
            --col_num_blocks 3 \
            --col_nhead 8 \
            --col_num_inds 128 \
            --col_affine False \
            --col_feature_group same \
            --col_feature_group_size 3 \
            --col_target_aware True \
            --col_ssmax True \
            --row_num_blocks 3 \
            --row_nhead 8 \
            --row_num_cls 4 \
            --row_rope_base 100000 \
            --row_rope_interleaved False \
            --icl_num_blocks 12 \
            --icl_nhead 8 \
            --icl_ssmax True \
            --ssmax_type qassmax-mlp-elementwise \
            --ff_factor 2 \
            --norm_first True \
            --zero_init False \
            --use_flash_attn3 False \
            --recompute $RECOMPUTE \
            --checkpoint_dir $CKPT_DIR \
            $RESUME_ARGS \
            --save_temp_every 50 \
            --save_perm_every 500
