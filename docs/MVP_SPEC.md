# BantengPanel MVP specification

## Goal

Show, with public cattle genotype data, whether a Bali-aware SNP ranking can preserve Bali-versus-other-breed classification performance with fewer markers than same-size alternatives. The tool supports research panel design. It does not make breeding decisions, certify parentage, or validate a wet-lab assay.

## Users and workflow

The primary user is a livestock genetics researcher or laboratory analyst evaluating marker panels. They choose a public cohort, inspect data quality and breed counts, compare panel sizes against equal-size random and global-MAF baselines, inspect the marker list and limitations, and download the results for review.

## MVP outputs

- Verified source archives and a machine-readable provenance manifest.
- Cross-validated metrics for 8, 16, 24, 48, 72, 96, 128, 156, and 200 SNP panels where the training data support the size.
- Baselines with exactly the same marker count.
- Per-fold CSV, aggregate JSON, marker CSV, and this evidence report.
- Offline-capable static dashboard backed by generated artifacts.

## Success criteria

The pipeline runs from the downloaded Dryad archive, fetches and verifies the Figshare archive, builds usable genotype matrices, emits reproducible benchmark artifacts, and the dashboard can display those artifacts without a backend service. Scientific claims must match the measured results and limitations.

## Product boundaries

The evaluation target is Bali-versus-non-Bali breed discrimination, not genomic prediction of growth, fertility, disease resistance, or breeding value. Model performance is not a claim of assay transferability. The public cohorts are small for Bali cattle and were not collected as a prospective validation set.

## Deferred

Authenticated dataset uploads, multi-tenant storage, production API, wet-lab assay design, genotype calling from sequencing, field trials, and commercial pricing validation are outside this 40-hour prototype.
