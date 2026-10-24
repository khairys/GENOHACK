"""Generate the evidence narrative from the JSON also consumed by dashboard/deck."""
from pathlib import Path


def write_report(manifest: dict, output: Path) -> Path:
    lines = ["# BantengPanel — Evidence report", "", f"Generated: {manifest['generatedAt']}", "",
             "## Scope and claim boundary", "",
             "Research prototype for minimal SNP panel design. Binary source-label classification is a sanity check. S1 estimates expected pedigree mixture in simulation; PCA and atypical-animal review are descriptive. None establishes genetic purity or introgression in real cattle.", "",
             f"Protocol {manifest['protocolVersion']} · seed {manifest['seed']} · {manifest['folds']} folds × {manifest['repeats']} repeats · {manifest['randomPanelsPerFoldAndSize']} random spaced panels per fold.", "",
             "All methods use the same spacing rule. Random panels use nested prefixes across sizes. S1 uses separate training references for each donor breed and shared test offspring across methods. Modal classification imputation is training-only but may favor the majority comparator group.", ""]
    for d in manifest["datasets"]:
        lines += [f"## {d['dataset'].title()} cohort", "", f"{d['nSamples']:,} animals after QC; {d['nBali']} Bali, {d['nComparator']:,} comparators, {d['nMarkers']:,} autosomal source markers.", "",
                  "### Equal-size source-label classification", "", "| SNP | Method | BA mean ± SD | Bali recall | Folds |", "|---:|---|---:|---:|---:|"]
        for r in d["results"]:
            lines.append(f"| {r['size']} | {r['method']} | {r['balancedAccuracyMean']:.3f} ± {(r['balancedAccuracySD'] or 0):.3f} | {r['baliRecallMean']:.3f} | {r['folds']} |")
        lines += ["", "### Paired folds: BantengPanel minus Global-MAF", "", "| SNP | Mean difference | Win / tie / loss |", "|---:|---:|---|"]
        for r in d.get("pairedComparisons", []):
            lines.append(f"| {r['size']} | {r['meanDifference']:+.3f} | {r['wins']} / {r['ties']} / {r['losses']} |")
        for size in [8, 48]:
            v = {r["method"]: r["balancedAccuracyMean"] for r in d["results"] if r["size"] == size}
            if "BantengPanel" in v:
                lines += ["", f"At {size} SNP: BantengPanel {v['BantengPanel']:.3f}; Global-MAF {v['Global-MAF']:.3f}; random mean {v['Random-mean']:.3f}. This is descriptive; overlapping folds are not independent significance tests."]
        lines += ["", "### Atypical-animal review", "", "Similarity uses full-cohort 200-marker candidates (post-hoc), not cross-validated ancestry. Errors are held-out predictions at 48 SNP, once per repeat. A flag requires confirmation; it does not prove introgression.", "", "| Animal ID | Breed | Misclassified / evaluations | Bali similarity | Review flag |", "|---|---|---:|---:|---|"]
        for r in d.get("atypicalSamples", []):
            if r["breed"] == "BALI" or r["misclassifiedRepeats"]:
                lines.append(f"| {r['sampleId']} | {r['breed']} | {r['misclassifiedRepeats']} / {r['evaluations']} | {r['baliSimilarity']:.3f} | {r['atypicalReview']} |")
        lines += ["", "### Robustness: 48 SNP", "", "| Scenario | BA mean ± SD | Bali recall |", "|---|---:|---:|"]
        for r in d["robustness"]:
            lines.append(f"| {r['scenario']} | {r['balancedAccuracyMean']:.3f} ± {(r['balancedAccuracySD'] or 0):.3f} | {r['baliRecallMean']:.3f} |")
        ancestry = d.get("ancestry")
        if ancestry:
            lines += ["", "### S1: simulated ancestry mixtures", "", f"{ancestry['offspringPerGenerationPerFold']} F1, BC1 and BC2 offspring per donor/fold; expected Bali pedigree q = 0.50, 0.75 and 0.875. q is relative to each training reference pair; MAD and ONG are not ancestry-free or interchangeable references.", "",
                      "MAE averages F1/BC1/BC2. BC2 sensitivity is at an **oracle held-out ROC** point with empirical specificity ≥95%; the threshold uses test controls to describe the ROC, not to propose a deployable threshold. Only 4–5 controls per fold and shared parents limit interpretation.", "",
                      "| Donor | SNP | Method | q MAE ± SD | BC2 sensitivity | Specificity | Folds |", "|---|---:|---|---:|---:|---:|---:|"]
            for r in ancestry["results"]:
                if r["size"] in [8, 24, 48, 200]:
                    lines.append(f"| {r['donorBreed']} | {r['size']} | {r['method']} | {r['maeMean']:.3f} ± {(r['maeSD'] or 0):.3f} | {r['bc2SensitivityAt95SpecificityMean']:.3f} | {r['achievedSpecificityMean']:.3f} | {r['folds']} |")
            lines += ["", f"Skipped donor-fold combinations: {len(ancestry['skippedFolds'])} (insufficient donor animals).", "", *[f"- {a}" for a in ancestry["assumptions"]]]
        pop = d.get("population")
        if pop:
            pc = pop["explainedVarianceRatio"]
            lines += ["", "### Descriptive population PCA", "", f"{pop['nAnimals']} animals, {pop['nMarkers']} spaced markers; PC1 {pc[0]:.1%}, PC2 {pc[1]:.1%} variance. Included source codes: {', '.join(pop['includedBreeds'])}. {pop['caveat']}"]
        lines += ["", "### Limitations", "", *[f"- {s}" for s in d["limitations"]], ""]
    lines += ["## Reproducibility", "", f"Source commit: `{manifest['gitCommit']}`; dirty at invocation: `{manifest['gitDirty']}`; identity captured before writes: `{manifest.get('identityCapturedBeforeWrites', False)}`.", "",
              f"Python {manifest['python']}; scikit-learn {manifest['scikitLearn']}. Scientific source/config SHA-256, archive checksums and QC counts are embedded in benchmark.json. The source tag identifies clean generation code; the release tag includes generated artifacts.", "",
              "## Primary references", "",
              "- [Decker et al. 2014: source cohort](https://doi.org/10.1371/journal.pgen.1004254)",
              "- [Sudrajad et al. 2020: Indonesian cattle diversity](https://doi.org/10.1371/journal.pone.0241038)",
              "- [Mohamad et al. 2009: no zebu introgression detected in the five Bali populations studied](https://doi.org/10.1371/journal.pone.0005490)",
              "- [Wang et al. 2025: heterogeneous introgression history](https://doi.org/10.1038/s41467-025-62692-z)", "",
              "These studies motivate this question; they do not validate this panel. See [Scientific protocol](../../docs/SCIENTIFIC_PROTOCOL.md).", ""]
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")
    return output
