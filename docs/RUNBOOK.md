# Local runbook

## Requirements

Python 3.11 or newer. The Dryad archive downloaded by the team should be present at the repository root, or pass its path to `fetch`. Internet access is needed once to retrieve the Figshare package. After source acquisition, parsing and benchmark execution run locally.

## Install and run

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e .
python -m bantengpanel.cli fetch --dryad .\doi_10_5061_dryad_th092__v20150214.zip
python -m bantengpanel.cli prepare
python -m bantengpanel.cli run
```

Open `apps/dashboard/index.html` in a local web server rooted at the repository (for example `python -m http.server 8000`) so the browser can load the JSON artifact. The dashboard lives at `http://localhost:8000/apps/dashboard/`.

Generated outputs: `artifacts/public/benchmark.json`, per-cohort benchmark JSON and fold CSV. Raw downloads and compact matrices live under ignored `data/`. The pipeline checks checksums before unpacking, prevents archive path traversal, and rejects malformed genotype records or ambiguous IDs.

If the public cohort fetch is unavailable, do not hand-edit or fabricate a result. The Dryad cohort can be prepared and benchmarked independently by using the Python API; record that the Figshare acquisition failed and include the error in the submission notes.
