"""Leakage-aware exploratory SNP panel benchmarking for public cattle cohorts."""
from __future__ import annotations

import json
import hashlib
import platform
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import sklearn
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import balanced_accuracy_score, recall_score
from sklearn.model_selection import RepeatedStratifiedKFold

from .data import PROCESSED, ROOT, load

OUT = ROOT / "artifacts/public"


def _independent_markers(indices: np.ndarray, markers: pd.DataFrame, scores: np.ndarray,
                         limit: int, min_distance: int) -> np.ndarray:
    """Greedy score ranking with a conservative same-chromosome spacing rule."""
    order = indices[np.lexsort((markers.iloc[indices].markerId.astype(str).to_numpy(), -scores[indices]))]
    return _spaced_order(order, markers, limit, min_distance)


def _spaced_order(order: np.ndarray, markers: pd.DataFrame, limit: int, min_distance: int) -> np.ndarray:
    selected: list[int] = []
    positions: dict[str, list[int]] = {}
    chromosomes = markers.chromosome.astype(str).to_numpy()
    coordinates = markers.position.to_numpy(dtype=int)
    for i in order:
        chrom, pos = chromosomes[i], int(coordinates[i])
        if any(abs(pos - old) < min_distance for old in positions.get(chrom, [])):
            continue
        selected.append(int(i))
        positions.setdefault(chrom, []).append(pos)
        if len(selected) >= limit:
            break
    return np.asarray(selected, dtype=int)


def random_spaced_panel(eligible: np.ndarray, markers: pd.DataFrame, limit: int,
                        min_distance: int, rng: np.random.Generator) -> np.ndarray:
    """Random priority followed by the same spacing rule as both ranked panels."""
    return _spaced_order(rng.permutation(eligible), markers, limit, min_distance)


def select_training_panels(x: np.ndarray, y: np.ndarray, markers: pd.DataFrame,
                           train_indices: np.ndarray, max_size: int, min_distance: int,
                           min_call_rate: float, min_maf: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """The sole selection boundary: only explicitly supplied training rows are read."""
    call, maf, delta = _scores(x[train_indices], y[train_indices])
    eligible = np.flatnonzero((call >= min_call_rate) & (maf >= min_maf) & np.isfinite(delta))
    return (eligible, _independent_markers(eligible, markers, delta, max_size, min_distance),
            _independent_markers(eligible, markers, maf, max_size, min_distance))


def _scores(train: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    valid = train >= 0
    call = valid.mean(axis=0)
    x = np.where(valid, train, 0).astype(np.float64)
    denom = np.maximum(valid.sum(axis=0), 1)
    freq = (x * valid).sum(axis=0) / denom / 2.0
    bali = y == 1
    other = y == 0
    fb = (x[bali] * valid[bali]).sum(axis=0) / np.maximum(valid[bali].sum(axis=0), 1) / 2
    fo = (x[other] * valid[other]).sum(axis=0) / np.maximum(valid[other].sum(axis=0), 1) / 2
    maf = np.minimum(freq, 1 - freq)
    delta = np.where((valid[bali].sum(axis=0) > 0) & (valid[other].sum(axis=0) > 0), np.abs(fb - fo), np.nan)
    return call, maf, delta


def _fit_score(train_x: np.ndarray, train_y: np.ndarray, test_x: np.ndarray, test_y: np.ndarray) -> tuple[float, float]:
    imputer, model = _fit_classifier(train_x, train_y)
    pred = model.predict(imputer.transform(np.where(test_x < 0, np.nan, test_x)))
    return _classification_scores(test_y, pred)


def _fit_classifier(train_x: np.ndarray, train_y: np.ndarray):
    imputer = SimpleImputer(strategy="most_frequent")
    a = imputer.fit_transform(np.where(train_x < 0, np.nan, train_x))
    model = LogisticRegression(class_weight="balanced", C=0.1, solver="liblinear", max_iter=300, random_state=20261024)
    model.fit(a, train_y)
    return imputer, model


def _classification_scores(test_y: np.ndarray, pred: np.ndarray) -> tuple[float, float]:
    return float(balanced_accuracy_score(test_y, pred)), float(recall_score(test_y, pred, pos_label=1, zero_division=0))


def _git_commit() -> str | None:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return None


def _git_dirty() -> bool | None:
    try:
        return bool(subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT, text=True, stderr=subprocess.DEVNULL).strip())
    except Exception:
        return None


def benchmark(name: str, seed: int = 20261024, folds: int = 4, repeats: int = 2,
              panel_sizes: tuple[int, ...] = (8, 16, 24, 48, 72, 96, 128, 156, 200),
              random_panels: int = 10, min_distance: int = 250_000,
              min_call_rate: float = 0.90, min_maf: float = 0.01,
              missing_rates: tuple[float, ...] = (0.05, 0.10, 0.20), genotype_error_rate: float = 0.01) -> dict:
    x, samples, markers = load(name)
    y = (samples.breed.astype(str).str.upper() == "BALI").astype(np.int8).to_numpy()
    counts = {str(k): int(v) for k, v in pd.Series(y).value_counts().sort_index().items()}
    if min(counts.values()) < folds:
        raise ValueError(f"Need at least {folds} examples per class; observed {counts}")
    splitter = RepeatedStratifiedKFold(n_splits=folds, n_repeats=repeats, random_state=seed)
    rows: list[dict] = []
    robustness: list[dict] = []
    marker_records: dict[int, dict] = {}
    fold_info = []
    predictions = []
    for fold, (tr, te) in enumerate(splitter.split(x, y), start=1):
        print(f"{name}: classification fold {fold}/{folds*repeats}", flush=True)
        rng = np.random.default_rng(np.random.SeedSequence([seed, fold, 1]))
        noise_rng = np.random.default_rng(np.random.SeedSequence([seed, fold, 2]))
        train, test = x[tr], x[te]
        yt, yv = y[tr], y[te]
        eligible, selected, global_rank = select_training_panels(x, y, markers, tr, max(panel_sizes), min_distance, min_call_rate, min_maf)
        if not len(eligible):
            raise ValueError("No SNP passed training-fold QC")
        if min(len(selected), len(global_rank)) < max(panel_sizes):
            raise ValueError("Not enough spaced markers for all requested panel sizes")
        random_choices = [random_spaced_panel(eligible, markers, max(panel_sizes), min_distance, rng) for _ in range(random_panels)]
        if any(len(p) < max(panel_sizes) for p in random_choices):
            raise ValueError("Random panel spacing left too few markers")
        fold_info.append({"fold": fold, "train": len(tr), "test": len(te), "eligibleMarkers": len(eligible), "baliTest": int(yv.sum())})
        for k in panel_sizes:
            if k > len(selected):
                continue
            opt = selected[:k]
            imputer, model = _fit_classifier(train[:, opt], yt)
            clean_imputed = imputer.transform(np.where(test[:, opt] < 0, np.nan, test[:, opt]))
            pred = model.predict(clean_imputed)
            score, recall = _classification_scores(yv, pred)
            rows.append({"dataset": name, "fold": fold, "size": k, "method": "BantengPanel", "balancedAccuracy": score, "baliRecall": recall})
            g = global_rank[:k]
            gs, gr = _fit_score(train[:, g], yt, test[:, g], yv)
            rows.append({"dataset": name, "fold": fold, "size": k, "method": "Global-MAF", "balancedAccuracy": gs, "baliRecall": gr})
            random_scores, random_recalls = [], []
            for random_choice in random_choices:
                chosen = random_choice[:k]
                rs, rr = _fit_score(train[:, chosen], yt, test[:, chosen], yv)
                random_scores.append(rs); random_recalls.append(rr)
            rows.append({"dataset": name, "fold": fold, "size": k, "method": "Random-mean", "balancedAccuracy": float(np.mean(random_scores)), "baliRecall": float(np.mean(random_recalls)), "randomPanels": random_panels})
            if k == min(48, max(panel_sizes)):
                # Reuse the training-fitted imputer and classifier; perturb only held-out calls.
                clean_test = test[:, opt].copy()
                probabilities = model.predict_proba(clean_imputed)[:, 1]
                predictions.extend({"sampleId": str(samples.iloc[idx].sampleId), "breed": str(samples.iloc[idx].breed),
                                    "fold": fold, "size": k, "observedBali": int(yv[j]), "predictedBali": int(pred[j]),
                                    "classifierProbability": float(probabilities[j])} for j, idx in enumerate(te))
                for rate in missing_rates:
                    noisy = clean_test.copy()
                    called = noisy >= 0
                    mask = (noise_rng.random(noisy.shape) < rate) & called
                    noisy[mask] = -1
                    ns, nr = _classification_scores(yv, model.predict(imputer.transform(np.where(noisy < 0, np.nan, noisy))))
                    robustness.append({"fold": fold, "scenario": f"missing_{int(rate*100):02d}", "balancedAccuracy": ns, "baliRecall": nr})
                noisy = clean_test.copy()
                flip = (noise_rng.random(noisy.shape) < genotype_error_rate) & (noisy >= 0)
                for r, c in zip(*np.where(flip)):
                    noisy[r, c] = int(noise_rng.choice([v for v in (0, 1, 2) if v != noisy[r, c]]))
                es, er = _classification_scores(yv, model.predict(imputer.transform(np.where(noisy < 0, np.nan, noisy))))
                robustness.append({"fold": fold, "scenario": f"genotype_error_{int(genotype_error_rate*100):02d}", "balancedAccuracy": es, "baliRecall": er})
    # A full-cohort design candidate is exported separately from CV panels.
    # It is a post-benchmark candidate and has no independent validation claim.
    full_call, full_maf, full_delta = _scores(x, y)
    full_eligible = np.flatnonzero((full_call >= min_call_rate) & (full_maf >= min_maf) & np.isfinite(full_delta))
    final_indices = _independent_markers(full_eligible, markers, full_delta, max(panel_sizes), min_distance)
    marker_records = {int(idx): {"sourceMarkerId": str(markers.iloc[idx].get("sourceMarkerId", markers.iloc[idx].get("sourceId", ""))), "markerId": str(markers.iloc[idx].markerId), "chromosome": str(markers.iloc[idx].chromosome), "position": int(markers.iloc[idx].position), "score": float(full_delta[idx])} for idx in final_indices}
    df = pd.DataFrame(rows)
    summary = df.groupby(["size", "method"], as_index=False).agg(
        balancedAccuracyMean=("balancedAccuracy", "mean"), balancedAccuracySD=("balancedAccuracy", "std"),
        baliRecallMean=("baliRecall", "mean"), baliRecallSD=("baliRecall", "std"), folds=("fold", "nunique"))
    # Aggregate results are descriptive: repeated folds overlap and are not independent replicates.
    robustness_summary = pd.DataFrame(robustness).groupby("scenario", as_index=False).agg(
        balancedAccuracyMean=("balancedAccuracy", "mean"), balancedAccuracySD=("balancedAccuracy", "std"),
        baliRecallMean=("baliRecall", "mean"), folds=("fold", "nunique")) if robustness else pd.DataFrame()
    result = {
        "dataset": name, "nSamples": len(samples), "nBali": int(y.sum()), "nComparator": int((1-y).sum()),
        "nMarkers": int(x.shape[1]), "markerSizes": panel_sizes, "folds": fold_info,
        "results": summary.replace({np.nan: None}).to_dict(orient="records"),
        "robustness": robustness_summary.replace({np.nan: None}).to_dict(orient="records"),
        "selectedMarkers": [marker_records[int(idx)] for idx in final_indices],
        "limitations": ["Bali cohort is small; metrics are exploratory and have wide sampling uncertainty.", "Unknown close relatives may occur across random folds; no pedigree groups were supplied.", "Training-fold call-rate/MAF filtering and marker ranking avoid test-set selection leakage.", "Physical spacing is used as a simple redundancy guard; this MVP does not claim LD pruning.", "Repeated-fold standard deviations are descriptive, not inferential confidence intervals."],
    }
    OUT.mkdir(parents=True, exist_ok=True)
    pred_df = pd.DataFrame(predictions)
    pred_df.to_csv(OUT / f"{name}_heldout_predictions.csv", index=False)
    atypical = _atypical_records(x, y, samples, final_indices, pred_df)
    pd.DataFrame(atypical).to_csv(OUT / f"{name}_atypical_samples.csv", index=False)
    result["atypicalSamples"] = atypical
    result["pairedComparisons"] = paired_comparisons(df)
    result["randomPanelPolicy"] = f"{random_panels} random-priority panels per fold; nested prefixes across sizes; same {min_distance} bp spacing as ranked methods."
    result["limitations"].append("Modal imputation is fitted on pooled training animals and may favor the much larger comparator group.")
    df.to_csv(OUT / f"{name}_fold_results.csv", index=False)
    robustness_summary.to_csv(OUT / f"{name}_robustness.csv", index=False)
    pd.DataFrame([{**marker_records[int(idx)], "panelSize": k, "rank": rank}
                  for k in panel_sizes for rank, idx in enumerate(final_indices[:k], start=1)]).to_csv(OUT / f"{name}_panel_candidates.csv", index=False)
    (OUT / f"{name}_benchmark.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


def paired_comparisons(df: pd.DataFrame) -> list[dict]:
    paired = df.pivot(index=["fold", "size"], columns="method", values="balancedAccuracy").reset_index()
    result = []
    for size, frame in paired.groupby("size"):
        diff = frame["BantengPanel"] - frame["Global-MAF"]
        result.append({"size": int(size), "meanDifference": float(diff.mean()),
                       "wins": int((diff > 1e-10).sum()), "ties": int((np.abs(diff) <= 1e-10).sum()),
                       "losses": int((diff < -1e-10).sum()), "folds": len(frame)})
    return result


def _atypical_records(x, y, samples, chosen, predictions):
    if predictions.empty:
        return []
    xb, xo = x[y == 1][:, chosen], x[y == 0][:, chosen]
    b = np.where(xb >= 0, xb, 0).sum(axis=0) / np.maximum((xb >= 0).sum(axis=0), 1)
    o = np.where(xo >= 0, xo, 0).sum(axis=0) / np.maximum((xo >= 0).sum(axis=0), 1)
    z = x[:, chosen]
    closeness = (np.abs(z-b) < np.abs(z-o)) & (z >= 0)
    similarity = closeness.sum(axis=1) / np.maximum((z >= 0).sum(axis=1), 1)
    records = []
    for i in np.flatnonzero(samples.breed.isin(["BALI", "MAD"]).to_numpy()):
        p = predictions[predictions.sampleId == str(samples.iloc[i].sampleId)]
        errors = int((p.observedBali != p.predictedBali).sum())
        records.append({"sampleId": str(samples.iloc[i].sampleId), "breed": str(samples.iloc[i].breed),
                        "panelSize": int(p.iloc[0]["size"]), "misclassifiedRepeats": errors, "evaluations": len(p),
                        "baliSimilarity": float(similarity[i]), "similarityMarkers": len(chosen),
                        "atypicalReview": bool(y[i] == 1 and errors >= max(1, len(p)/2))})
    return records


def run_all(seed: int = 20261024, folds: int = 4, repeats: int = 2, random_panels: int = 10,
            panel_sizes: tuple[int, ...] = (8, 16, 24, 48, 72, 96, 128, 156, 200),
            min_distance: int = 250_000, min_call_rate: float = 0.90, min_maf: float = 0.01,
            sample_missing_max: float = 0.10,
            missing_rates: tuple[float, ...] = (0.05, 0.10, 0.20), genotype_error_rate: float = 0.01,
            include_extensions: bool = True, ancestry_config: dict | None = None,
            config_path: Path | None = None) -> dict:
    # Capture before ANY output mutation. Generated files cannot dirty their own source identity.
    source_commit, source_dirty = _git_commit(), _git_dirty()
    science_paths = sorted((ROOT / "bantengpanel").glob("*.py")) + [config_path or ROOT / "configs/mvp.yaml", ROOT / "pyproject.toml"]
    source_hashes = {(str(p.relative_to(ROOT)).replace("\\", "/") if p.is_relative_to(ROOT) else p.name):
                     hashlib.sha256(p.read_text(encoding="utf-8-sig").replace("\r\n", "\n").encode()).hexdigest() for p in science_paths}
    results = []
    for name in ("dryad", "figshare"):
        results.append(benchmark(name, seed=seed, folds=folds, repeats=repeats, random_panels=random_panels,
                                 panel_sizes=panel_sizes, min_distance=min_distance,
                                 min_call_rate=min_call_rate, min_maf=min_maf,
                                 missing_rates=missing_rates, genotype_error_rate=genotype_error_rate))
        if include_extensions:
            from .ancestry import run_ancestry
            from .population import describe_population
            results[-1]["ancestry"] = run_ancestry(name, seed, folds, repeats, random_panels, panel_sizes,
                                                   min_distance, min_call_rate, min_maf, ancestry_config or {})
            results[-1]["population"] = describe_population(name, seed, min_distance, min_call_rate, min_maf,
                                                          results[-1]["atypicalSamples"])
            (OUT / f"{name}_benchmark.json").write_text(json.dumps(results[-1], indent=2, allow_nan=False), encoding="utf-8")
    manifest = {
        "product": "BantengPanel", "protocolVersion": "2.0.0", "generatedAt": datetime.now(timezone.utc).isoformat(),
        "seed": seed, "folds": folds, "repeats": repeats, "randomPanelsPerFoldAndSize": random_panels,
        "python": platform.python_version(), "scikitLearn": sklearn.__version__, "gitCommit": source_commit, "gitDirty": source_dirty,
        "sourceFilesSha256": source_hashes, "sourceHashPolicy": "UTF-8 without BOM, LF line endings", "identityCapturedBeforeWrites": True,
        "configSha256": hashlib.sha256((config_path or ROOT / "configs/mvp.yaml").read_bytes()).hexdigest(),
        "sourceManifest": json.loads((ROOT / "data/raw/manifest.json").read_text(encoding="utf-8")),
        "processingQC": json.loads((PROCESSED / "summary.json").read_text(encoding="utf-8")),
        "parameters": {"panelSizes": panel_sizes, "sampleMissingMax": sample_missing_max, "snpCallMin": min_call_rate, "mafMin": min_maf, "minDistanceBp": min_distance, "robustnessMissingRates": missing_rates, "genotypeErrorRate": genotype_error_rate},
        "datasets": results,
        "claimBoundary": "Research-use-only computational evaluation; no assay, breeding-value, parentage, or field-validation claim.",
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "benchmark.json").write_text(json.dumps(manifest, indent=2, allow_nan=False), encoding="utf-8")
    return manifest
