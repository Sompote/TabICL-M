"""Mean rank on the 20-dataset benchmark against median inference time per fit and against parameter count.

Reads results/broad/{loso,random_split} (+ tabpfn_*) and docs/figures/benchmark/params.json; writes
docs/figures/benchmark/rank_vs_time_params.{png,svg} and prints the table used in the README.
"""
import json, os
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.ticker
import matplotlib.pyplot as plt

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LABEL = {"tabicl_aware": "TabICL-M (ours)", "tabicl_impute": "TabICLv2", "tabpfn3": "TabPFN-3", "tabpfn25": "TabPFN 2.5", "catboost": "CatBoost"}
COLOR = {"tabicl_aware": "#1b7f3b", "tabicl_impute": "#4c72b0", "tabpfn3": "#c44e52", "tabpfn25": "#dd8452", "catboost": "#8c8c8c"}
params = json.load(open(f"{REPO}/docs/figures/benchmark/params.json"))
PARAMS = {"tabicl_aware": (params["tabicl_aware_clf"] + params["tabicl_aware_reg"]) / 2, "tabicl_impute": (params["tabicl_impute_clf"] + params["tabicl_impute_reg"]) / 2,
          "tabpfn3": (params["tabpfn3_clf"] + params["tabpfn3_reg"]) / 2, "tabpfn25": (params["tabpfn25_clf"] + params["tabpfn25_reg"]) / 2}

def load(cfg):
    df = pd.concat([pd.read_csv(f"{REPO}/results/broad/{cfg}/results.csv"), pd.read_csv(f"{REPO}/results/broad/tabpfn_{cfg}/results.csv")], ignore_index=True)
    df = df[df.error.isna()].copy()
    for c in ("rmse", "auc"):
        if c not in df: df[c] = np.nan
    df["metric"] = np.where(df.task == "regression", df.rmse, df.auc)
    return df.drop_duplicates(subset=["dataset", "mechanism", "rate", "seed", "model"], keep="last")

rows = {}
for cfg in ["loso", "random_split"]:
    df = load(cfg)
    inc = df[df.mechanism.isin(["block", "block_shift"])]
    p = inc.pivot_table(index=["dataset", "mechanism", "rate", "seed"], columns="model", values="metric")[list(LABEL)].dropna()
    reg = p.index.get_level_values("dataset").isin(df[df.task == "regression"].dataset.unique())
    ranks = p.mul(np.where(reg, -1.0, 1.0), axis=0).rank(axis=1, ascending=False).mean()
    secs = df.groupby("model").seconds.median()
    auc = df[df.task == "classification"].groupby("model").auc.mean()
    for m in LABEL:
        rows.setdefault(m, {}).update({f"rank_{cfg}": ranks[m], f"sec_{cfg}": secs[m], f"auc_{cfg}": auc[m]})
tab = pd.DataFrame(rows).T
tab["params"] = pd.Series(PARAMS)
tab["seconds"] = tab[["sec_loso", "sec_random_split"]].mean(axis=1)

fig, axes = plt.subplots(1, 2, figsize=(11, 4.4))
for ax, xkey, xlabel in [(axes[0], "seconds", "median time per fit + predict, s (log)"), (axes[1], "params", "parameters (log)")]:
    for m in LABEL:
        x = tab.loc[m, xkey]
        if pd.isna(x): continue
        ax.scatter(x, tab.loc[m, "rank_loso"], s=90, color=COLOR[m], marker="o", zorder=3, label=LABEL[m] if ax is axes[0] else None)
        ax.scatter(x, tab.loc[m, "rank_random_split"], s=90, facecolors="none", edgecolors=COLOR[m], linewidths=2, marker="o", zorder=3)
        ax.annotate(LABEL[m], (x, tab.loc[m, "rank_loso"]), textcoords="offset points", xytext=(7, -3), fontsize=9, color=COLOR[m])
    ax.set_xscale("log"); ax.invert_yaxis(); ax.grid(alpha=0.3); ax.set_xlabel(xlabel)
    ticks = [0.1, 0.2, 0.3, 0.5, 1.0] if xkey == "seconds" else [1e7, 2e7, 3e7, 5e7, 1e8]
    fmt = (lambda v, _: f"{v:g}") if xkey == "seconds" else (lambda v, _: f"{v/1e6:.0f}M")
    ax.set_xticks(ticks); ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(fmt)); ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
axes[0].set_ylabel("mean rank over 5 models (1 = best)  ↑ better")
axes[0].set_title("Rank vs inference time — filled: held-out source, hollow: random split", fontsize=10)
axes[1].set_title("Rank vs model size (CatBoost has no parameter count)", fontsize=10)
axes[0].legend(loc="lower right", fontsize=8, frameon=False)
fig.suptitle("20 datasets, block and block_shift missingness at 30 % / 50 %, 5 seeds (results/broad)", fontsize=10)
fig.tight_layout()
for ext in ("png", "svg"):
    fig.savefig(f"{REPO}/docs/figures/benchmark/rank_vs_time_params.{ext}", dpi=150)

lines = ["| model | parameters | median s / fit | mean rank, held-out source | mean rank, random split | mean AUC, held-out source (13 clf datasets) |", "|---|---|---|---|---|---|"]
for m in ["tabicl_aware", "tabpfn3", "tabpfn25", "tabicl_impute", "catboost"]:
    r = tab.loc[m]
    pstr = f"{r['params']/1e6:.1f} M" if not pd.isna(r["params"]) else "—"
    lines.append(f"| {LABEL[m]} | {pstr} | {r['seconds']:.1f} | {r['rank_loso']:.2f} | {r['rank_random_split']:.2f} | {r['auc_loso']:.3f} |")
open(f"{REPO}/docs/figures/benchmark/table.md", "w").write("\n".join(lines))
print("\n".join(lines))
