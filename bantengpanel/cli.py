"""Command-line entry points for the reproducible BantengPanel workflow."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml

from . import data
from .analysis import OUT, run_all
from .report import write_report


def main() -> None:
    parser = argparse.ArgumentParser(prog="bantengpanel", description="Population-aware cattle SNP panel evaluation")
    sub = parser.add_subparsers(dest="command", required=True)
    fetch = sub.add_parser("fetch", help="Verify and extract Figshare and Dryad source archives")
    fetch.add_argument("--dryad", type=Path, help="Path to the downloaded Dryad outer ZIP")
    prepare = sub.add_parser("prepare", help="Parse verified source data into compact local matrices")
    prepare.add_argument("--config", type=Path, default=data.ROOT / "configs/mvp.yaml")
    run = sub.add_parser("run", help="Run cross-validated equal-size panel benchmarks")
    run.add_argument("--config", type=Path, default=data.ROOT / "configs/mvp.yaml")
    run.add_argument("--folds", type=int)
    run.add_argument("--repeats", type=int)
    run.add_argument("--random-panels", type=int)
    sub.add_parser("report", help="Render Markdown evidence report from existing benchmark outputs")
    args = parser.parse_args()
    if args.command == "fetch":
        print(json.dumps(data.fetch(args.dryad), indent=2))
    elif args.command == "prepare":
        config = yaml.safe_load(args.config.read_text(encoding="utf-8"))
        print(json.dumps(data.prepare(config["sampleMissingMax"]), indent=2))
    elif args.command == "run":
        config = yaml.safe_load(args.config.read_text(encoding="utf-8"))
        scenarios = config["scenarios"]
        missing_rates = tuple(s["missingRate"] for s in scenarios if s["missingRate"] > 0)
        genotype_error = next((s["errorRate"] for s in scenarios if s["errorRate"] > 0), 0.0)
        result = run_all(seed=config["seed"], folds=args.folds or config["outerFolds"],
                         repeats=args.repeats or config["repeats"],
                         random_panels=args.random_panels or config["randomPanels"],
                         panel_sizes=tuple(config["panelSizes"]), min_distance=config["minDistanceBp"],
                         min_call_rate=config["snpCallMin"], min_maf=config["mafMin"],
                         sample_missing_max=config["sampleMissingMax"], missing_rates=missing_rates,
                         genotype_error_rate=genotype_error)
        write_report(result, OUT / "evidence_report.md")
        print(json.dumps({"output": str(OUT), "datasets": [{"name": d["dataset"], "nBali": d["nBali"], "sizes": len(d["results"])} for d in result["datasets"]]}, indent=2))
    elif args.command == "report":
        manifest = json.loads((OUT / "benchmark.json").read_text(encoding="utf-8"))
        print(write_report(manifest, OUT / "evidence_report.md"))


if __name__ == "__main__":
    main()
