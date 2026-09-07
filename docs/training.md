# Training TabICL-M

This file holds the training details that were moved out of the README: the stage-4
recipe and its run, the source-aware recipe (stage 4 and stage 4b), the ablation
recipe, the self-driving pipelines, and hardware and timing. Results are in
[results.md](results.md); the architecture is in
[tabicl_m_architecture.md](tabicl_m_architecture.md).

## Continued pre-training (stage 4)

TabICL-M is trained by continuing from the released TabICLv2 weights with the
three parts switched on. The new parameters are zero at step 0, so the run starts
exactly at the released model on complete data. One GPU with 32 GB is enough for
the default settings with `DTYPE=bfloat16`; in float32 the attention falls back to
memory-hungry kernels when FlashAttention-3 is not available and runs out of memory
at `--max_seq_len 8192`.

```bash
pip install -e ".[pretrain]"
python -c "from tabicl import TabICLClassifier, TabICLRegressor; TabICLClassifier()._load_model(); TabICLRegressor()._load_model()"
bash scripts/train_v2_missing_stage4.sh clf
bash scripts/train_v2_missing_stage4.sh reg
```

The script copies the stage-3 recipe of TabICLv2 and adds:

```
--missing_enabled True        # block-structured and cell-wise missingness in the prior
--col_missing_aware True      # observed-only column embedding with absence vector
--recon_weight 0.1            # masked-cell reconstruction, hide up to 30 % of observed cells
--checkpoint_path <released>  --only_load_model True
```

Environment variables override the defaults, for example `STEPS=6000 BATCH=64
NUM_GPUS=4 RECON_WEIGHT=0.05 DTYPE=bfloat16 RECOMPUTE=True`. The trainer logs the task loss and the
reconstruction loss separately. The task loss should stay near its starting value.
The reconstruction loss should fall. Checkpoints are written to
`checkpoints/tabicl-m/<task>/step-*.ckpt` and load directly into the estimators.

The run that produced the committed checkpoints (`checkpoints/tabicl-m/run_stage4.sh`,
one RTX 5090, bfloat16, 3000 steps, batch 32, `--max_seq_len 8192`, 2 h 20 min per
task) behaved as intended. Averaged over 250-step windows:

| Task | Task loss, steps 0 to 249 | Task loss, steps 2750 to 2999 | Reconstruction, first window | Reconstruction, last window |
|---|---|---|---|---|
| classifier | cross-entropy 0.82 (accuracy 0.73) | 0.55 (0.78) | 0.24 | 0.19 |
| regressor | pinball 0.084 | 0.080 | 0.24 | 0.20 |

The classifier's task loss falls at first because the released model has never seen
tables with gaps; the regressor's stays flat. The reconstruction loss falls in both.

All `--missing_*` options are listed by `python -m tabicl.train --help`. The
same options apply to `python -m tabicl.prior` when tables are pre-generated to
disk, and the missingness configuration is written to the dataset `metadata.json`.

![Where the missingness transform sits in the pre-training pipeline](./docs/figures/missingness_prior/pipeline.svg)

*The missingness transform runs on every batch right after the structural causal
model prior, whether tables are generated on the fly or written to disk. It is a
bypass unless `--missing_enabled True` is passed.*

## Source-aware stage 4 (`ARCH=source_aware`)

The source-aware checkpoints add a representation of the *source* a row comes from,
using the fact that rows sharing a missingness pattern come from the same source.
All additions are zero-initialised or identity on complete data, so the run still
starts exactly at the released model (`tests/test_source_aware.py`):

| stage | addition | flag |
|---|---|---|
| column embedder | every observed cell is also fed standardised within the rows of its own pattern group (source-relative value) | `col_group_stats` |
| row interaction | feature tokens whose cells are all missing are excluded from the attention keys (observed-only rows) | `row_missing_aware` |
| row interaction | a learned query reads out which features a row lacks and adds it to the row representation (pattern token) | `pattern_token` |
| training | a pseudo-source loses a block of columns and the model reconstructs it; a view with per-source offset and noise must give the same predictions as the clean view | `--recon_mode`, `--consistency_weight` |
| prior | most incomplete tables are block-structured, shifted, with a source that appears only in the test rows; stage 4b uses stronger shifts and sources with as few as 20 % of the features | `ARCH=source_aware` |

Each part has its own switch so that it can be ablated: `COL_GROUP_STATS`,
`ROW_MISSING_AWARE`, `PATTERN_TOKEN` (`True`/`False`), `RECON_MODE`
(`cell|block|mixed`), `CONSISTENCY_WEIGHT` (`0` = off). The trainer options behind
them are `--col_group_stats`, `--row_missing_aware`, `--pattern_token`,
`--recon_mode`, `--recon_block_rows_max`, `--recon_block_cols_max`,
`--consistency_weight`, `--consistency_p`, `--consistency_shift_max`,
`--consistency_noise_max`, `--consistency_max_seq_len` (the second view is skipped
on tables longer than this, 2048 by default, to fit in memory).

**Prior regime.** With `ARCH=source_aware` the script sets `--missing_p_apply 0.7
--missing_p_cell 0.4 --missing_p_block 0.9 --missing_p_contiguous_sources 0.75
--missing_p_source_shift 0.8 --missing_p_source_noise 0.6`, so most incomplete
tables are block-structured, shifted, and contain a source that appears only in the
test rows. Learning rate 5e-5 (1e-5 for the baseline recipe).

**Stage 4 run** (`checkpoints/tabicl-m-sa/run_stage4_sa.sh`, one RTX 5090, bf16,
10 000 steps, batch 32, `--max_seq_len 8192`, about 9.5 h per task). Averaged over
1000-step windows the classifier's task loss went 0.60 to 0.57 and the
reconstruction loss 0.21 to 0.19 while the consistency loss stayed near 0.005; the
regressor's pinball loss stayed near 0.08. The first launch crashed at step 374
because an OOM-skipped last micro-batch left the DDP reducer waiting; gradients are
now averaged by hand after the micro-batch loop (`Trainer._all_reduce_grads`),
which makes skipped micro-batches and unused parameters harmless.

**Stage 4b** (`checkpoints/tabicl-m-sa/pipeline2.sh`, phase C) continues both
10k checkpoints for 10 000 more steps with a fresh cosine cycle at lr 3e-5 on
stronger source effects, because the 10k model's consistency loss showed it was
already invariant to the small shifts of the stage-4 prior but not to the larger
ones of the evaluation: `P_SHIFT=1.0 P_NOISE=0.8 MAX_SHIFT=1.2 MAX_NOISE=0.5
MIN_OBS_FRAC=0.2 P_CONTIGUOUS=0.9 CONSISTENCY_SHIFT_MAX=1.2 CONSISTENCY_NOISE_MAX=0.5
CONSISTENCY_WEIGHT=0.3` (`--missing_max_shift_scale`, `--missing_max_noise_scale`
and `--missing_min_obs_frac` are the prior options behind `MAX_SHIFT`, `MAX_NOISE`
and `MIN_OBS_FRAC`). The resulting checkpoints,
`checkpoints/tabicl-m-sa-20k/<task>/step-10000.ckpt`, are the ones to use.

## Ablation recipe

`pipeline2.sh`, phase B: six classifier runs of 3000 steps on the source-aware
prior, one switch off at a time (`full_3k`, `no_group_stats`, `no_row_mask`,
`no_pattern_token`, `no_objectives`, `arch_off`), each evaluated on the four
classification datasets of the headroom study, leave-one-source-out and random
split. Checkpoints under `checkpoints/tabicl-m-sa-ablation/` are not committed.

## Self-driving pipelines

The whole run after the first stage-4 checkpoint was executed by three scripts under
`checkpoints/tabicl-m-sa/`, each waiting for the previous one, resuming a crashed
training run from its last checkpoint, and committing and pushing its results:

| script | does |
|---|---|
| `pipeline.sh` | finishes stage 4 (both tasks), evaluates on the headroom configurations and the standard ablation (`results/sa_eval/`), commits the 10k weights |
| `pipeline2.sh` | phase B, the per-part ablation (`results/sa_ablation/`); phase C, stage 4b and its evaluation (`results/sa_eval_20k/`), commits the 20k weights |
| `pipeline3.sh` | the 20-dataset benchmark against TabPFN 2.5 and TabPFN-3 (`results/broad/`) |

`results/sa_eval/readme_section.py` regenerates the auto-generated part of
[results.md](results.md) from the summary files. TabPFN 2.5, 2.6 and 3 run from a
separate environment (`tabpfn>=8` conflicts with the `transformers` version the
trainer uses): `results/headroom/run_tabpfn_new.sh`.

## Hardware and timing

One NVIDIA RTX 5090 (32 GB). `DTYPE=bfloat16` is required: in float32 the attention
falls back to memory-hungry kernels when FlashAttention-3 is not available and runs
out of memory at `--max_seq_len 8192`. About 2.7 to 3.3 s per step at batch 32
(the second view of the consistency loss adds roughly 15 %), so 3000 steps take
about 2 h 20 min and 10 000 steps about 9.5 h per task. Prior generation runs on
8 CPU workers and never stalls the GPU. About 0.2 % of micro-batches are skipped on
OOM at the longest tables, which is harmless with the manual gradient averaging.
