"""S1: held-out, unlinked Mendelian simulation; relative two-reference q only."""
from __future__ import annotations

import json
import numpy as np
import pandas as pd
from sklearn.model_selection import RepeatedStratifiedKFold

from .data import load

TRUTH = {"F1": .5, "BC1": .75, "BC2": .875}


def allele_frequency(x: np.ndarray) -> np.ndarray:
    """Jeffreys-smoothed frequency, from reference TRAINING animals only."""
    called = x >= 0
    return (np.where(called, x, 0).sum(axis=0) + .5) / (2*called.sum(axis=0) + 1)


def estimate_q(x: np.ndarray, p_bali: np.ndarray, p_donor: np.ndarray) -> np.ndarray:
    """Binomial composite-likelihood grid MLE. Missing loci contribute zero.

    This is a relative reference-mixture coefficient, not a calibrated ancestry
    percentage in real animals. HWE and locus independence are approximations.
    """
    grid = np.linspace(0, 1, 101)
    p = np.clip(p_donor[:, None] + (p_bali-p_donor)[:, None]*grid, 1e-6, 1-1e-6)
    called = x >= 0
    g = np.where(called, x, 0).astype(float)
    ll = g @ np.log(p) + np.where(called, 2-g, 0) @ np.log1p(-p)
    result = grid[ll.argmax(axis=1)]
    result[~called.any(axis=1)] = np.nan
    return result


def simulate_generations(bali: np.ndarray, donor: np.ndarray, p_bali: np.ndarray,
                         p_donor: np.ndarray, n: int, rng: np.random.Generator) -> dict[str, np.ndarray]:
    """Choose test parents with replacement; transmit independent alleles per locus.

    Missing parental dosages are drawn using their TRAINING reference frequency.
    BC1 and BC2 backcross to a held-out Bali parent. Pedigree q is the target;
    realized genomic ancestry varies, especially for tiny panels.
    """
    def gamete(parents, p):
        g = parents[rng.integers(len(parents), size=n)].copy()
        missing = g < 0
        if missing.any():
            fill = rng.binomial(2, np.broadcast_to(p, g.shape)).astype(np.int8)
            g[missing] = fill[missing]
        return rng.binomial(1, g/2).astype(np.int8)
    f1 = gamete(bali, p_bali) + gamete(donor, p_donor)
    bc1 = rng.binomial(1, f1/2).astype(np.int8) + gamete(bali, p_bali)
    bc2 = rng.binomial(1, bc1/2).astype(np.int8) + gamete(bali, p_bali)
    return {"F1": f1, "BC1": bc1, "BC2": bc2}


def sensitivity_at_specificity(pure_q, bc2_q, target=.95):
    """Oracle test-ROC operating point, reported DESCRIPTIVELY, never deployed.

    Threshold uses held-out controls to characterize the ROC. It is not an
    independently calibrated decision threshold. Small control n is disclosed.
    """
    thresholds = np.unique(np.concatenate(([0.0], pure_q, bc2_q, [1.0])))
    specificity = (pure_q[:, None] >= thresholds).mean(axis=0)
    sensitivity = (bc2_q[:, None] < thresholds).mean(axis=0)
    eligible = np.flatnonzero(specificity >= target)
    best = eligible[np.argmax(sensitivity[eligible])]
    return float(sensitivity[best]), float(specificity[best]), float(thresholds[best])


def run_ancestry(name, seed, folds, repeats, random_panels, panel_sizes,
                 min_distance, min_call, min_maf, settings):
    from .analysis import OUT, select_training_panels, random_spaced_panel
    x, samples, markers = load(name)
    y = (samples.breed == "BALI").astype(np.int8).to_numpy()
    n_children = int(settings.get("offspringPerGeneration", 64))
    donor_breeds = settings.get("donorBreeds", {}).get(name, ["ONG", "MAD"])
    rows, prediction_rows, exclusions = [], [], []
    splits = RepeatedStratifiedKFold(n_splits=folds, n_repeats=repeats, random_state=seed)
    for fold, (tr, te) in enumerate(splits.split(x, y), 1):
        print(f"{name}: S1 fold {fold}/{folds*repeats}", flush=True)
        for donor_i, donor in enumerate(donor_breeds):
            train_b = tr[y[tr] == 1]
            train_d = tr[samples.iloc[tr].breed.to_numpy() == donor]
            test_b = te[y[te] == 1]
            test_d = te[samples.iloc[te].breed.to_numpy() == donor]
            if len(train_d) < 3 or len(test_d) == 0:
                exclusions.append({"fold": fold, "donorBreed": donor, "reason": "Need >=3 training and >=1 test donor"})
                continue
            reference_train = np.concatenate((train_b, train_d))
            eligible, bp, gm = select_training_panels(x, y, markers, reference_train, max(panel_sizes), min_distance, min_call, min_maf)
            rng = np.random.default_rng(np.random.SeedSequence([seed, fold, donor_i, 3]))
            random_choices = [random_spaced_panel(eligible, markers, max(panel_sizes), min_distance, rng) for _ in range(random_panels)]
            if min(len(bp), len(gm), *(len(c) for c in random_choices)) < max(panel_sizes):
                raise ValueError(f"{name}/{donor}: insufficient spaced S1 markers")
            # Generate one shared set of test offspring at the union of selected loci.
            # Every method/size receives the SAME simulated animal at its chosen loci.
            union = np.unique(np.concatenate((bp, gm, *random_choices)))
            pb = allele_frequency(x[train_b][:, union]); pdonor = allele_frequency(x[train_d][:, union])
            sim_rng = np.random.default_rng(np.random.SeedSequence([seed, fold, donor_i, 4]))
            children = simulate_generations(x[test_b][:, union], x[test_d][:, union], pb, pdonor, n_children, sim_rng)
            pure = x[test_b][:, union]
            combined = np.concatenate([pure, *(children[g] for g in TRUTH)])
            truth = np.concatenate([np.ones(len(pure)), *(np.full(n_children, q) for q in TRUTH.values())])
            categories = np.array(["BALI-control"]*len(pure) + [g for g in TRUTH for _ in range(n_children)])
            lookup = {int(v): i for i, v in enumerate(union)}
            for method, choices in [("BantengPanel", [bp]), ("Global-MAF", [gm]), ("Random-mean", random_choices)]:
                for k in panel_sizes:
                    replicate_metrics = []
                    for replicate, choice in enumerate(choices):
                        cols = np.array([lookup[int(v)] for v in choice[:k]])
                        qhat = estimate_q(combined[:, cols], pb[cols], pdonor[cols])
                        masks = {g: categories == g for g in ["BALI-control", *TRUTH]}
                        sens, spec, threshold = sensitivity_at_specificity(qhat[masks["BALI-control"]], qhat[masks["BC2"]])
                        metrics = {"mae": float(np.abs(qhat[len(pure):]-truth[len(pure):]).mean()),
                                   "pureMAE": float(np.abs(qhat[:len(pure)]-1).mean()),
                                   "f1MAE": float(np.abs(qhat[masks["F1"]]-.5).mean()),
                                   "bc1MAE": float(np.abs(qhat[masks["BC1"]]-.75).mean()),
                                   "bc2MAE": float(np.abs(qhat[masks["BC2"]]-.875).mean()),
                                   "bc2SensitivityAt95Specificity": sens, "achievedSpecificity": spec,
                                   "oracleThreshold": threshold}
                        replicate_metrics.append(metrics)
                        # Full simulated predictions for ranked methods at 8/48/200; random replicates stay aggregate.
                        if method != "Random-mean" and k in [8, 48, 200]:
                            prediction_rows.extend({"fold": fold, "donorBreed": donor, "method": method, "size": k,
                                                    "simulationIndex": i, "generation": str(categories[i]),
                                                    "pedigreeQ": float(truth[i]), "estimatedQ": float(qhat[i])}
                                                   for i in range(len(qhat)))
                    rows.append({"dataset": name, "fold": fold, "donorBreed": donor, "size": k, "method": method,
                                 "pureControls": len(pure), "offspringPerGeneration": n_children,
                                 "testDonorParents": len(test_d), "trainingBali": len(train_b), "trainingDonor": len(train_d),
                                 **{key: float(np.mean([r[key] for r in replicate_metrics])) for key in replicate_metrics[0]}})
    frame = pd.DataFrame(rows)
    metrics = ["mae", "pureMAE", "f1MAE", "bc1MAE", "bc2MAE", "bc2SensitivityAt95Specificity", "achievedSpecificity"]
    summary = []
    for (donor, size, method), group in frame.groupby(["donorBreed", "size", "method"]):
        summary.append({"donorBreed": donor, "size": int(size), "method": method, "folds": len(group),
                        "pureControlsPerFoldMin": int(group.pureControls.min()),
                        **{key+"Mean": float(group[key].mean()) for key in metrics},
                        **{key+"SD": float(group[key].std()) if len(group) > 1 else None for key in metrics}})
    result = {"experiment": "S1", "simulationOnly": True, "offspringPerGenerationPerFold": n_children,
              "donorBreeds": donor_breeds, "qGridStep": .01, "results": summary, "skippedFolds": exclusions,
              "assumptions": ["Held-out parents only; independent Mendelian gametes per locus (unlinked approximation).",
                              "q is expected pedigree mixture relative to Bali and each donor breed, not absolute banteng ancestry.",
                              "MAD is already admixed; all source BALI labels are assumed controls, not confirmed pure.",
                              "Composite likelihood assumes HWE and independent loci; 250 kb spacing is not LD pruning.",
                              "Test-ROC sensitivity at >=95% empirical specificity is an oracle descriptive operating point, not a calibrated deployment threshold.",
                              "Only 4–5 Bali controls per fold; folds and simulated descendants share parents and are not independent replicates.",
                              "Simulated offspring are not independent real cattle; no field-validity or purity certification claim."]}
    frame.to_csv(OUT / f"{name}_ancestry_folds.csv", index=False)
    pd.DataFrame(summary).to_csv(OUT / f"{name}_ancestry_summary.csv", index=False)
    pd.DataFrame(prediction_rows).to_csv(OUT / f"{name}_ancestry_simulated_predictions.csv", index=False)
    (OUT / f"{name}_ancestry.json").write_text(json.dumps(result, indent=2, allow_nan=False), encoding="utf-8")
    return result
