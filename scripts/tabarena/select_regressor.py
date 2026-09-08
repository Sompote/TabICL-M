"""Print the regressor checkpoint to submit: the bar-head model if it beats the 20k source-aware one
head-to-head (paired RMSE over shared conditions, random split and leave-one-source-out), else the 20k one."""
import os, sys
import pandas as pd, numpy as np
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "results", "regression")
SA = "checkpoints/tabicl-m-sa-20k/reg/step-10000.ckpt"; BAR = "checkpoints/tabicl-m-sa-bar/reg/step-20000.ckpt"
wins = losses = 0
for cfg in ["random_split", "loso"]:
    a, b = f"{R}/{cfg}/results.csv", f"{R}/stagebar_{cfg}/results.csv"
    if not (os.path.exists(a) and os.path.exists(b)):
        continue
    da = pd.read_csv(a); da = da[(da.model == "tabicl_aware") & da.error.isna()]
    db = pd.read_csv(b); db = db[(db.model == "tabicl_aware") & db.error.isna()]
    m = da.merge(db, on=["dataset", "mechanism", "rate", "seed"], suffixes=("_sa", "_bar"))
    wins += int((m.rmse_bar < m.rmse_sa).sum()); losses += int((m.rmse_bar > m.rmse_sa).sum())
choice = BAR if (wins > losses and os.path.exists(BAR)) else SA
print(f"bar vs sa20k: {wins} wins / {losses} losses -> {choice}", file=sys.stderr)
print(choice)
