# TabICL-Large: ordinary regression continuation

This run continues the completed TabICL-M-Large regressor for **20,000 additional
steps** on ordinary synthetic regression. It retains the 18-block, 41,539,682-parameter
predictor and its pretrained weights, removing only the unused 387-parameter
reconstruction head (41,539,295 parameters remain). The name identifies the new training
regime; it does not mean the inherited missing-aware components were removed or
that the model was pretrained from scratch exclusively on complete data.

- Original graph-SCM synthetic prior; no injected missingness or source offsets/noise.
- Pinball regression loss only; reconstruction and consistency weights are zero.
- No smooth-target replacement, added MSE loss, or auxiliary masking.
- Batch 32, maximum sequence length 8,192, bf16, activation checkpointing.
- Muon, learning rate 3e-5, 5% warmup, fresh 20k-step cosine schedule; seed 44.
- Starts from `results/large_regression_20k/checkpoints/reg/step-20000.ckpt`,
  loading model weights only. Later restarts resume this run's optimizer/scheduler.

Runner: `python scripts/train_large_ordinary_regression.py`.
Use `--prepare-only` to validate the source and write the recipe without training.
The instance service is `tabicl-regression-ordinary-20k`.

Outputs are under `results/large_ordinary_regression_20k/`: `manifest.json`,
`status.json`, `train.log`, and `checkpoints/reg/`. Save temporary checkpoints every
250 steps and permanent checkpoints every 2,500 steps. The planned final checkpoint
is `checkpoints/reg/step-20000.ckpt`. Weights remain local and Git-ignored.

This is a separate ordinary-only run, not the previously suggested 50/50 mixture.
The original missing-aware checkpoints are preserved. Quality must be evaluated
after training; this run does not establish an improvement over TabPFN-3.
