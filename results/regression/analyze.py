"""Regression against TabPFN-3: test-time variants, stage 4c/4d checkpoints. Writes summary.md and verdict.txt."""
import os, sys, glob
import pandas as pd, numpy as np
ROOT = os.path.dirname(os.path.abspath(__file__))
def load(cfg):
    frames = []
    for f in glob.glob(f"{ROOT}/*{cfg}/results.csv"):
        tag = os.path.basename(os.path.dirname(f)).replace(cfg, "").strip("_")   # '', 'tabpfn', 'stage4c', 'stage4d'
        d = pd.read_csv(f); d = d[d.error.isna()].copy()
        if tag.startswith("stage"): d["model"] = d.model + "_" + tag.replace("stage", "")
        frames.append(d)
    df = pd.concat(frames, ignore_index=True)
    return df[df.task == "regression"].drop_duplicates(subset=["dataset", "mechanism", "rate", "seed", "model"], keep="last")
lines = ["# Regression against TabPFN-3", "", "7 regression datasets, block and block_shift at 0.3 / 0.5, 5 seeds; rank 1 = best (lower RMSE). "
         "`block_shift` (a held-out source with its own measurement offset) is the case the source-aware parts target.", ""]
verdict = {}
for cfg, title in [("loso", "Leave-one-source-out"), ("random_split", "Random split")]:
    if not glob.glob(f"{ROOT}/*{cfg}/results.csv"): continue
    df = load(cfg); models = sorted(df.model.unique(), key=lambda m: (not m.startswith("tabicl"), m))
    groups = [(["block", "block_shift"], "all"), (["block_shift"], "with source offset"), (["block"], "no offset")]
    if cfg == "random_split": groups = [(["block", "block_shift"], "all")]
    for mechs, gname in groups:
        p = df[df.mechanism.isin(mechs)].pivot_table(index=["dataset", "mechanism", "rate", "seed"], columns="model", values="rmse")[models].dropna()
        if p.empty: continue
        ranks = p.rank(axis=1, ascending=True)
        lines += [f"## {title}, {gname}: {len(p)} conditions", "", "| model | mean rank | times first | vs `tabpfn3` wins/losses | datasets won |", "|---|---|---|---|---|"]
        for m in ranks.mean().sort_values().index:
            if "tabpfn3" in p:
                d = p["tabpfn3"] - p[m]; per = d.groupby(level="dataset").mean()
                vs = f"{int((d > 0).sum())}/{int((d < 0).sum())}"; won = f"{int((per > 0).sum())}/{len(per)}"
            else: vs = won = "—"
            lines.append(f"| `{m}` | {ranks[m].mean():.2f} | {int((ranks[m] == 1).sum())} | {vs} | {won} |")
        lines.append("")
        ours = [m for m in models if m.startswith("tabicl")]
        best = min(ours, key=lambda m: ranks[m].mean()) if ours else None
        ref = "tabpfn3_n32" if "tabpfn3_n32" in p else "tabpfn3"
        if best and ref in p:
            q = p[[best, ref]]; d = q[ref] - q[best]; per = d.groupby(level="dataset").mean()
            ahead = (d > 0).mean() > 0.5 and (per > 0).sum() > len(per) / 2
            key = cfg if gname == "all" else f"{cfg}[{gname.replace(' ', '_')}]"
            verdict[key] = "AHEAD" if ahead else "BEHIND"
            lines += [f"Best of ours `{best}` vs `{ref}`: {int((d > 0).sum())}/{int((d < 0).sum())} paired, "
                      f"datasets won {int((per > 0).sum())}/{len(per)}, mean RMSE gain {d.mean():+.3f} -> **{verdict[key]}**", ""]
    t = df[df.rate == 0.5].pivot_table(index=["dataset", "mechanism"], columns="model", values="rmse")[models]
    lines += [f"### {title}: per-dataset means at rate 0.5", "",
              "| dataset | mechanism | " + " | ".join(f"`{m}`" for m in models) + " |", "|---|---|" + "---|" * len(models)]
    for (ds, mech), r in t.iterrows():
        best_m = r.idxmin(); lines.append(f"| {ds} | {mech} | " + " | ".join(("**%.3f**" if m == best_m else "%.3f") % r[m] if r[m] == r[m] else "—" for m in models) + " |")
    lines.append("")
open(f"{ROOT}/summary.md", "w").write("\n".join(lines))
open(f"{ROOT}/verdict.txt", "w").write(" ".join(f"{k}={v}" for k, v in verdict.items()) + "\n")
print("\n".join(lines[:30])); print("VERDICT", verdict)
