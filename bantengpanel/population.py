"""Descriptive PCA, separate from held-out predictive evaluation."""
from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA

from .data import load


def describe_population(name, seed, min_distance, min_call, min_maf, atypical):
    from .analysis import OUT, _scores, _independent_markers
    x, samples, markers = load(name)
    breeds = ["BALI", "MAD", "ONG", "ACE", "PES", "BRE", "THA", "SAHW", "GIR", "RSIN"] if name == "dryad" else sorted(samples.breed.unique())
    keep = samples.breed.isin(breeds).to_numpy()
    x, samples = x[keep], samples.loc[keep].reset_index(drop=True)
    y = (samples.breed == "BALI").to_numpy()
    call, maf, _ = _scores(x, y)
    eligible = np.flatnonzero((call >= min_call) & (maf >= min_maf))
    indices = _independent_markers(eligible, markers, maf, 3000, min_distance)
    z = x[:, indices].astype(float)
    valid = z >= 0
    p = np.where(valid, z, 0).sum(axis=0) / np.maximum(valid.sum(axis=0), 1) / 2
    z = (np.where(valid, z, 2*p) - 2*p) / np.sqrt(np.maximum(2*p*(1-p), 1e-8))
    pca = PCA(n_components=2, svd_solver="randomized", random_state=seed)
    coordinates = pca.fit_transform(z)
    flags = {str(a["sampleId"]) for a in atypical if a["atypicalReview"]}
    points = [{"sampleId": str(row.sampleId), "breed": str(row.breed), "pc1": float(coordinates[i, 0]),
               "pc2": float(coordinates[i, 1]), "atypicalReview": str(row.sampleId) in flags} for i, row in samples.iterrows()]
    pd.DataFrame(points).to_csv(OUT / f"{name}_pca.csv", index=False)
    return {"method": "HWE-scaled mean-imputed PCA on full descriptive subset; MAF ranking + 250 kb spacing",
            "predictiveValidation": False, "nAnimals": len(samples), "nMarkers": len(indices),
            "includedBreeds": breeds, "explainedVarianceRatio": pca.explained_variance_ratio_.tolist(), "points": points,
            "caveat": "Descriptive structure only; axes and flagged animals do not prove introgression. Not used to select or validate panels."}
