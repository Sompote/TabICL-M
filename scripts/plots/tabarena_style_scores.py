"""Score the 20-dataset benchmark with TabArena's evaluator (bencheval): Elo with 95 % CI, normalised
score, rank, harmonic rank, improvability, win rate. Each (dataset, mechanism, rate) is a task, each seed a
repeat; metric_error is log loss for classification and RMSE for regression, as on TabArena.
Writes results/tabarena_style/leaderboard_<split>.csv and a figure of Elo against inference time."""
import os, sys, json
import numpy as np, pandas as pd

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = f"{REPO}/results/tabarena_style"; os.makedirs(OUT, exist_ok=True)
LABEL = {"tabicl_aware": "TabICL-M (ours)", "tabicl_impute": "TabICLv2", "tabpfn3": "TabPFN-3", "tabpfn25": "TabPFN 2.5", "catboost": "CatBoost"}

def long_table(cfg):
    df = pd.concat([pd.read_csv(f"{REPO}/results/broad/{cfg}/results.csv"), pd.read_csv(f"{REPO}/results/broad/tabpfn_{cfg}/results.csv")], ignore_index=True)
    df = df[df.error.isna() & df.model.isin(LABEL)].drop_duplicates(subset=["dataset", "mechanism", "rate", "seed", "model"], keep="last").copy()
    df["metric_error"] = np.where(df.task == "regression", df.rmse, df.logloss)
    df["task_id"] = df.dataset + "|" + df.mechanism + "|" + df.rate.astype(str)
    df["method"] = df.model.map(LABEL)
    t = df[["method", "task_id", "seed", "metric_error", "seconds"]].rename(columns={"task_id": "task"})
    t["time_train_s"] = t.seconds; t["time_infer_s"] = t.seconds  # the runner records fit + predict together
    t = t.drop(columns="seconds")
    # dense: keep (task, seed) cells that every method completed
    full = t.groupby(["task", "seed"]).method.nunique() == len(LABEL)
    keep = full[full].index
    t = t.set_index(["task", "seed"]).loc[keep].reset_index()
    return t.sort_values(["task", "seed", "method"]).reset_index(drop=True)

if __name__ == "__main__":
    from bencheval.evaluator import BenchmarkEvaluator
    boards = {}
    for cfg in ["loso", "random_split"]:
        data = long_table(cfg)
        arena = BenchmarkEvaluator(seed_column="seed")
        lb = arena.leaderboard(data=data, average_seeds=True, include_error=True, include_elo=True, include_winrate=True,
                               include_improvability=True, include_mrr=True,
                               elo_kwargs=dict(calibration_framework="TabICLv2", calibration_elo=1000), sort_by=["rank"])
        lb.to_csv(f"{OUT}/leaderboard_{cfg}.csv")
        boards[cfg] = lb
        print(f"\n=== {cfg}: {data.task.nunique()} tasks x {data.seed.nunique()} seeds, columns: {list(lb.columns)}")
        print(lb.to_string())

    # ---- figure: Elo (95 % CI) against inference time, TabArena style; and the tables
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt, matplotlib.ticker
    COLOR = {"TabICL-M (ours)": "#1b7f3b", "TabICLv2": "#4c72b0", "TabPFN-3": "#c44e52", "TabPFN 2.5": "#dd8452", "CatBoost": "#8c8c8c"}
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.4), sharey=False)
    for ax, (cfg, title) in zip(axes, [("loso", "held-out source (block + block_shift)"), ("random_split", "random split (block + block_shift)")]):
        lb = boards[cfg].sort_values("elo")
        lo, hi = (350, 1450) if cfg == "loso" else (150, 1750)
        prev_y = None
        for m, r in lb.iterrows():
            ax.errorbar(r["median_time_infer_s"], r["elo"], yerr=[[r["elo-"]], [r["elo+"]]], fmt="o", ms=9, color=COLOR[m], capsize=3, lw=1.4, zorder=3)
            dy = -3 if prev_y is None or abs(r["elo"] - prev_y) > 0.06 * (hi - lo) else 9  # stagger colliding labels
            ax.annotate(f"{m}  {r['elo']:.0f}", (r["median_time_infer_s"], r["elo"]), textcoords="offset points", xytext=(8, dy), fontsize=9, color=COLOR[m])
            prev_y = r["elo"]
        ax.set_ylim(lo, hi)
        if (lb["elo"] - lb["elo-"]).min() < lo:
            ax.text(0.02, 0.03, "CatBoost's lower CI extends below the axis", transform=ax.transAxes, fontsize=8, color="#8c8c8c")
        ax.set_xscale("log"); ax.set_xticks([0.2, 0.3, 0.5, 1.0]); ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:g}"))
        ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter()); ax.set_xlim(0.15, 1.6)
        ax.grid(alpha=0.3); ax.set_xlabel("median time per fit + predict, s (log)"); ax.set_title(title, fontsize=10)
        ax.axhline(1000, color="#4c72b0", lw=0.8, ls=":", alpha=0.7)
    axes[0].set_ylabel("Elo (TabICLv2 = 1000), 95 % CI  ↑ better")
    fig.suptitle("TabArena-style scoring (bencheval) of the 20-dataset benchmark: 100 tasks x 5 seeds per split", fontsize=10)
    fig.tight_layout()
    for ext in ("png", "svg"):
        fig.savefig(f"{OUT}/elo_vs_time.{ext}", dpi=150)
    for cfg in ["loso", "random_split"]:
        lb = boards[cfg]
        lines = [f"| model | Elo | 95 % CI | rank | win rate | improvability (%) | MRR | median s / fit |", "|---|---|---|---|---|---|---|---|"]
        for m, r in lb.iterrows():
            lines.append(f"| {m} | {r['elo']:.0f} | +{r['elo+']:.0f} / −{r['elo-']:.0f} | {r['rank']:.2f} | {r['winrate']:.2f} | {100*r['improvability']:.1f} | {r['mrr']:.2f} | {r['median_time_infer_s']:.2f} |")
        open(f"{OUT}/leaderboard_{cfg}.md", "w").write("\n".join(lines))
    print("figure and tables written to", OUT)
