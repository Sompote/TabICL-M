"""Benchmark TabICL-M on TabArena or BeyondArena and compare to the cached leaderboard.

    python scripts/tabarena/run_tabarena.py --suite tabarena --subset lite --out results/tabarena/lite
    python scripts/tabarena/run_tabarena.py --suite beyondarena --subset core grouped !large --out results/beyondarena/grouped

Runs in-process (``debug_mode=True``), which is the simplest GPU-safe backend on one machine.
Writes the leaderboard (website format) as CSV and Markdown into ``--out``.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tabiclm_model import TabICLMModel  # noqa: E402


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--suite", choices=["tabarena", "beyondarena"], default="tabarena")
    p.add_argument("--subset", nargs="+", default=["lite"])
    p.add_argument("--out", required=True)
    p.add_argument("--datasets", nargs="*", default=None, help="Optional dataset-name filter")
    p.add_argument("--expname", default=None, help="Results cache directory (default: <out>/experiments)")
    args = p.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    expname = args.expname or str(out / "experiments")
    TabICLMModel.prefetch_weights()

    if args.suite == "tabarena":
        from tabarena.benchmark.experiment import TabArenaV0pt1ExperimentBundle
        from tabarena.contexts import TabArenaContext

        bundle, context = TabArenaV0pt1ExperimentBundle, TabArenaContext()
    else:
        from tabarena.benchmark.experiment import BeyondArenaExperimentBundle
        from tabarena.contexts import BeyondArenaContext

        bundle, context = BeyondArenaExperimentBundle, BeyondArenaContext()

    experiments = bundle(models=[(TabICLMModel.config_generator(), 0)]).build_experiments()
    subset = args.subset[0] if len(args.subset) == 1 else args.subset
    build_kwargs = {"dataset_names": args.datasets} if args.datasets else None
    context.build_and_run_jobs(
        experiments,
        expname=expname,
        subset=subset,
        build_kwargs=build_kwargs,
        new_result_prefix="[New] ",
        debug_mode=True,
    )
    leaderboard = context.compare(output_dir=out / "eval")
    leaderboard.to_csv(out / "leaderboard.csv")
    try:
        website = context.leaderboard_to_website_format(leaderboard=leaderboard)
        (out / "leaderboard.md").write_text(website.to_markdown(index=False))
        print(website.to_markdown(index=False))
    except Exception as e:  # BeyondArena has no website format
        (out / "leaderboard.md").write_text(leaderboard.to_markdown())
        print(leaderboard.to_markdown())
        print(f"(website format unavailable: {e})")


if __name__ == "__main__":
    main()
