"""Write the regression-vs-TabPFN-3 block into the README between markers, from summary.md and verdict.txt."""
import os, re
ROOT = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(ROOT))
S, E = "<!-- regression:start -->", "<!-- regression:end -->"
summary = open(f"{ROOT}/summary.md").read(); verdict = open(f"{ROOT}/verdict.txt").read().strip()
tables = re.findall(r"(## .*?: \d+ conditions\n\n\| model.*?\n\n(?:Best of ours.*?\n\n)?)", summary, re.S)
body = "\n".join(t.replace("## ", "#### ") for t in tables)
block = (f"{S}\n\n### Regression against TabPFN-3 (auto-generated)\n\n"
         "Regression is where TabPFN-3 leads. The levers tried, hands-off: 32 ensemble members (`_n32`), the median instead of the mean (`_med`), "
         "a target power-transform ensemble (`_ypow`), an extra `quantile` normalisation member (`_qn`), a regressor continued on a half-complete prior "
         "(`_4c`) and, if still behind, on a mostly complete prior (`_4d`). Full tables: `results/regression/summary.md`.\n\n"
         f"{body}\nVerdict (best of ours against TabPFN-3 at its best setting): **{verdict}**.\n\n{E}")
readme = open(f"{REPO}/README.md").read()
if S in readme: readme = readme[: readme.index(S)] + block + readme[readme.index(E) + len(E):]
else: readme = readme.replace("## What remains", block + "\n\n## What remains", 1)
open(f"{REPO}/README.md", "w").write(readme); print("README regression block written:", verdict)
