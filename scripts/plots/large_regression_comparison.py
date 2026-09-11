"""Plot recorded Large regression gains in a TabArena-inspired comparison layout.

Run from any directory: python scripts/plots/large_regression_comparison.py
Uses paired RMSE gains, not Elo or official TabArena leaderboard scores.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "docs/figures/benchmark"


def main():
    data = pd.read_csv(ROOT / "results/large_regression_20k_eval/comparison.csv")
    conditions = [
        ("random", "none", "Complete data"),
        ("random", "block", "Random split · block missingness"),
        ("random", "block_shift", "Random split · block + shift"),
        ("source", "block", "Held-out source · block missingness"),
        ("source", "block_shift", "Held-out source · block + shift"),
    ]
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.8), sharex=True, sharey=True)
    for ax, reference, title, color in zip(
        axes,
        ["original", "tabpfn3_archived"],
        ["Compared with TabICL-M", "Compared with TabPFN-3 (archived)"],
        ["#1b7f3b", "#c44e52"],
    ):
        for y, (split, mechanism, _) in enumerate(conditions):
            row = data.loc[(data.split == split) & (data.mechanism == mechanism)
                           & (data.reference == reference)].squeeze()
            gain = float(row.mean_gain_percent)
            ax.hlines(y, min(0, gain), max(0, gain), color=color, alpha=0.3, lw=4)
            ax.scatter(gain, y, s=75, color=color, zorder=3)
            ax.annotate(f"{gain:+.2f}%", (gain, y), xytext=(9 if gain >= 0 else -9, 0),
                        textcoords="offset points", va="center",
                        ha="left" if gain >= 0 else "right", fontsize=10, color=color)
        ax.axvline(0, color="#667085", lw=1, ls=":")
        ax.set_title(title, fontsize=11, pad=14)
        ax.set_xlabel("RMSE gain (%)   → lower error", labelpad=10)
        ax.set_xlim(-9, 19)
        ax.set_xticks([-5, 0, 5, 10, 15])
        ax.grid(axis="x", alpha=0.2)
        ax.set_axisbelow(True)
        ax.tick_params(axis="y", length=0)
        for spine in ax.spines.values():
            spine.set_visible(False)
    axes[0].set_yticks(range(len(conditions)), [c[2] for c in conditions], fontsize=10)
    axes[0].invert_yaxis()
    fig.suptitle("TabICL-M-Large · regression comparison", fontsize=16, fontweight="bold", y=0.97)
    fig.text(0.5, 0.035,
             "7 development datasets · 3 seeds · 3,000-row cap · 8 estimators\n"
             "Equal-dataset mean paired gains; positive is better. TabArena-inspired style; not Elo or an official leaderboard.",
             ha="center", fontsize=9, color="#475467", linespacing=1.6)
    fig.tight_layout(rect=(0, 0.14, 1, 0.92), w_pad=2)
    OUT.mkdir(parents=True, exist_ok=True)
    for extension in ("png", "svg"):
        fig.savefig(OUT / f"large_regression_comparison.{extension}", dpi=180, facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    main()
