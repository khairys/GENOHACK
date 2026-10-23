# MVP architecture

```text
Public source archives
        ↓ checksum validation and safe extraction
Python source parsers → int8 genotype matrices + sample/marker metadata
        ↓ train-fold quality control, marker ranking, equal-size evaluation
CSV + JSON evidence artifacts
        ↓ static file loading
Offline-capable dashboard and downloadable reports
```

The scientific pipeline is the source of truth. The dashboard never recomputes or invents metrics. It reads generated JSON/CSV files from `artifacts/public/`. There is no database, login, upload endpoint, or always-on API in the hackathon MVP. Raw genotype files and compact matrices remain local; only aggregate evidence and an explicitly reviewed marker list belong in a public package.

The CLI has three operations: `fetch` verifies/downloads and extracts sources; `prepare` parses source files; `run` creates fold-level and aggregate benchmarking artifacts. Python dependencies and the `bantengpanel` console script are declared in `pyproject.toml`.
