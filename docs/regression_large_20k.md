# TabICL-M-Large: 20k regression training

**Completed:** 20,000 continuation steps in 26h 52m 38s.
The model is **TabICL-M-Large**, where M means Missing.
[Model guide](model_variants.md) · [Evaluation](../results/large_regression_20k_eval/report.md).

User-directed replacement of the 1,000-step depth pilot: train the 18-block,
41.5M-parameter regressor for 20,000 optimizer steps. The pilot was stopped before
its first checkpoint, so this run starts from the verified identity-expanded
checkpoint `results/large_regression/initial_18.ckpt`.

The instance-specific runner is `scripts/train_large_regression_full.py`; it
requires the source checkpoint and pilot preparation artifacts recorded in its
manifest. On the training instance the
Supervisor service is `tabicl-regression-large-20k`; the previous
`tabicl-regression-large` pilot is stopped. There is no automatic control run or
benchmark after training.

Settings retain the Large pilot recipe: batch 32, bf16, maximum sequence length
8,192, original graph prior with source-aware missingness, pinball loss without
MSE or smooth-target replacement, reconstruction weight 0.1, consistency weight
0.3, Muon, and gradient checkpointing. Learning rate peaks at 3e-5 with 5% warmup
and a fresh 20k-step cosine schedule. The initial checkpoint's optimizer state is
not used. Subsequent restarts resume local optimizer and scheduler state.

Output directory: `results/large_regression_20k`. The manifest records source
checkpoint hash and settings. Logs are in `train.log`, status in `status.json`,
and weights in `checkpoints/reg/`. Temporary checkpoints are saved every 250
steps and permanent checkpoints every 2,500 steps. The final artifact is
`checkpoints/reg/step-20000.ckpt`. The subsequent evaluation is linked above; the original checkpoint remains
available. The Large artifact is local and ignored by Git, so it must be
published separately to make it available to other users.
