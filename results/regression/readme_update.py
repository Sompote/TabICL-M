"""Write the regression-vs-TabPFN-3 block into the README between markers, from summary.md and verdict.txt."""
import os, re
ROOT = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(ROOT))
S, E = "<!-- regression:start -->", "<!-- regression:end -->"
summary = open(f"{ROOT}/summary.md").read(); verdict = open(f"{ROOT}/verdict.txt").read().strip()
tables = re.findall(r"(## .*?: \d+ conditions\n\n\| model.*?\n\n(?:Best of ours.*?\n\n)?)", summary, re.S)
body = "\n".join(t.replace("## ", "#### ") for t in tables)
block = (f"{S}\n\n### Regression against TabPFN-3 (auto-generated)\n\n"
         "Regression is the half of the benchmark where TabPFN-3 leads, so it was attacked separately on the seven regression "
         "datasets. Test-time levers: 32 ensemble members (`_n32`), the median instead of the mean (`_med`), a target "
         "power-transform ensemble (`_ypow`), an extra quantile-normalisation member (`_qn`). Training lever: the regressor "
         "continued on a prior with half the tables complete (`_4c3500`, a 3500-step probe). None of them changes the "
         "head-to-head outside the source-offset case: the probe moved the random split by nothing (85 wins / 90 losses "
         "against the 20k model), so the planned full continuation runs were stopped rather than spend 25 GPU-hours on a "
         "flat curve. TabPFN-3 gains nothing from 32 members either (74/66), so the comparison is saturated on both sides. "
         "The residual gap is base regression strength inherited from TabICLv2, whose released regressor is itself far "
         "behind TabPFN-3 here (mean rank 6.43 against 3.95). Two more probes closed the question "
         "(`results/regression/probes_summary.md`): a weight soup of the 10k and 20k regressors gains nothing, and the gap "
         "on kin8nm exists at every training-set size and narrows with data, so it is not a sample-efficiency problem "
         "of in-context learning. Test-time fine-tuning on the context rows, with TabPFN-3 given the same treatment, "
         "recovers a third of the kin8nm gap and then plateaus; TabPFN-3 gets slightly worse when fine-tuned and its "
         "zero-shot model stays the best on both datasets, so fine-tuning is a shared lever that does not change the "
         "ordering. Finally the regression head itself was replaced: a TabPFN-style histogram head (1000 "
         "per-table equal-mass buckets, log-density loss; `regression_method=\"bar\"`, results tagged `_bar`) trained "
         "for 20k steps from the 20k source-aware regressor is worse than the quantile head on every regression "
         "dataset on complete data (9 wins / 26 losses, 7 % higher RMSE) and on incomplete random splits (50 / 90), "
         "so the objective is not what separates TabPFN-3 from TabICL either. Full tables: `results/regression/summary.md`.\n\n"
         f"{body}\nVerdict (best of ours against TabPFN-3 at its best setting): **{verdict}**.\n\n{E}")
readme = open(f"{REPO}/README.md").read()
if S in readme: readme = readme[: readme.index(S)] + block + readme[readme.index(E) + len(E):]
else: readme = readme.replace("## What remains", block + "\n\n## What remains", 1)
open(f"{REPO}/README.md", "w").write(readme); print("README regression block written:", verdict)
