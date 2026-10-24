"""Reproduce the additional legacy-QC finding without changing any benchmark."""
import json
import sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from bantengpanel.data import ROOT, load
from bantengpanel.analysis import _scores

result = {"purpose": "Full-cohort descriptive review, not an additional validation metric", "datasets": {}}
for name in ["dryad", "figshare"]:
    x, samples, markers = load(name)
    y = (samples.breed == "BALI").to_numpy()
    call, maf, delta = _scores(x, y)
    pooled = (call >= .9) & (maf >= .01)
    no_bali = pooled & ((x[y] >= 0).sum(axis=0) == 0)
    result["datasets"][name] = {"pooledPassingButNoBaliCalls": int(no_bali.sum()),
                                 "markers": markers.loc[no_bali, "markerId"].tolist(),
                                 "policy": "Missing class frequency is undefined and excluded, never set to zero"}
path = ROOT / "artifacts/public/data_quality_review.json"
path.write_text(json.dumps(result, indent=2), encoding="utf-8")
print(path)
