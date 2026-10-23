"""Generate a human-readable evidence report from measured benchmark artifacts."""
from __future__ import annotations

from pathlib import Path


def write_report(manifest: dict, output: Path) -> Path:
    lines = [
        "# BantengPanel — Evidence report", "",
        f"Generated: {manifest['generatedAt']}", "",
        "## Scope", "",
        "This report summarizes in-silico Bali-versus-other-breed classification on two public cohorts analyzed separately. The results evaluate a computational marker-ranking workflow. They do not validate a genotyping assay or a breeding decision.", "",
        f"Protocol {manifest['protocolVersion']} · seed {manifest['seed']} · {manifest['folds']} folds × {manifest['repeats']} repeats · {manifest['randomPanelsPerFoldAndSize']} random panels per fold and size.", "",
    ]
    for d in manifest["datasets"]:
        lines.extend([f"## {d['dataset'].title()} cohort", "", f"{d['nSamples']:,} animals; {d['nBali']} Bali and {d['nComparator']:,} comparator animals; {d['nMarkers']:,} source markers.", "", "### Equal-size benchmark", "", "| SNPs | Method | Balanced accuracy (mean ± SD) | Bali recall | Folds |", "|---:|---|---:|---:|---:|"])
        for r in sorted(d["results"], key=lambda z: (z["size"], z["method"])):
            sd = "—" if r["balancedAccuracySD"] is None else f"{r['balancedAccuracySD']:.3f}"
            lines.append(f"| {r['size']} | {r['method']} | {r['balancedAccuracyMean']:.3f} ± {sd} | {r['baliRecallMean']:.3f} | {r['folds']} |")
        at48 = {r["method"]: r for r in d["results"] if r["size"] == 48}
        if {"BantengPanel", "Global-MAF", "Random-mean"}.issubset(at48):
            bp, gm, rnd = (at48[name]["balancedAccuracyMean"] for name in ("BantengPanel", "Global-MAF", "Random-mean"))
            lines.extend(["", "### Key observation", "", f"At 48 SNP, BantengPanel reached {bp:.3f} balanced accuracy, compared with {gm:.3f} for Global-MAF and {rnd:.3f} for the random-panel mean. The population-aware ranking did not outperform Global-MAF at this size in this cohort. Treat the small-panel pattern as exploratory; repeated folds are not independent significance tests.", ""])
        lines.extend(["", "### Robustness at 48 SNP", "", "| Perturbation | Balanced accuracy (mean ± SD) | Bali recall | Folds |", "|---|---:|---:|---:|"])
        for r in d["robustness"]:
            sd = "—" if r["balancedAccuracySD"] is None else f"{r['balancedAccuracySD']:.3f}"
            lines.append(f"| {r['scenario']} | {r['balancedAccuracyMean']:.3f} ± {sd} | {r['baliRecallMean']:.3f} | {r['folds']} |")
        lines.extend(["", "### Limitations", ""])
        lines.extend(f"- {item}" for item in d["limitations"])
        lines.append("")
    lines.extend(["## Interpretation", "", "Balanced accuracy and recall describe these source cohorts only. Repeated cross-validation folds overlap, and the small Bali groups and unknown pedigree relationships limit generalization. A full-cohort marker candidate is available as a separate CSV; it must be tested on an independent cohort before any performance claim. No statistical significance or assay-readiness claim is made.", "", "## Reproducibility", "", f"Python {manifest['python']} · scikit-learn {manifest['scikitLearn']} · source commit {manifest['gitCommit'] or 'not available'}.", "", "See [Scientific Protocol](../../docs/SCIENTIFIC_PROTOCOL.md) and [Dataset Provenance](../../docs/DATA_PROVENANCE.md) for details.", ""])
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")
    return output
