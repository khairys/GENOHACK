# BantengPanel — Evidence report

Generated: 2026-10-23T19:33:18.153953+00:00

## Scope

This report summarizes in-silico Bali-versus-other-breed classification on two public cohorts analyzed separately. The results evaluate a computational marker-ranking workflow. They do not validate a genotyping assay or a breeding decision.

Protocol 1.0.0 · seed 20261024 · 4 folds × 5 repeats · 30 random panels per fold and size.

## Dryad cohort

1,542 animals; 20 Bali and 1,522 comparator animals; 43,042 source markers.

### Equal-size benchmark

| SNPs | Method | Balanced accuracy (mean ± SD) | Bali recall | Folds |
|---:|---|---:|---:|---:|
| 8 | BantengPanel | 0.962 ± 0.058 | 0.930 | 20 |
| 8 | Global-MAF | 0.940 ± 0.058 | 0.950 | 20 |
| 8 | Random-mean | 0.915 ± 0.033 | 0.935 | 20 |
| 16 | BantengPanel | 0.935 ± 0.072 | 0.880 | 20 |
| 16 | Global-MAF | 0.951 ± 0.048 | 0.930 | 20 |
| 16 | Random-mean | 0.941 ± 0.044 | 0.924 | 20 |
| 24 | BantengPanel | 0.949 ± 0.068 | 0.900 | 20 |
| 24 | Global-MAF | 0.958 ± 0.050 | 0.930 | 20 |
| 24 | Random-mean | 0.955 ± 0.041 | 0.934 | 20 |
| 48 | BantengPanel | 0.960 ± 0.068 | 0.920 | 20 |
| 48 | Global-MAF | 0.969 ± 0.047 | 0.940 | 20 |
| 48 | Random-mean | 0.962 ± 0.048 | 0.929 | 20 |
| 72 | BantengPanel | 0.955 ± 0.069 | 0.910 | 20 |
| 72 | Global-MAF | 0.974 ± 0.044 | 0.950 | 20 |
| 72 | Random-mean | 0.965 ± 0.043 | 0.933 | 20 |
| 96 | BantengPanel | 0.950 ± 0.069 | 0.900 | 20 |
| 96 | Global-MAF | 0.970 ± 0.047 | 0.940 | 20 |
| 96 | Random-mean | 0.968 ± 0.045 | 0.937 | 20 |
| 128 | BantengPanel | 0.950 ± 0.069 | 0.900 | 20 |
| 128 | Global-MAF | 0.980 ± 0.041 | 0.960 | 20 |
| 128 | Random-mean | 0.968 ± 0.046 | 0.937 | 20 |
| 156 | BantengPanel | 0.960 ± 0.068 | 0.920 | 20 |
| 156 | Global-MAF | 0.985 ± 0.037 | 0.970 | 20 |
| 156 | Random-mean | 0.968 ± 0.044 | 0.937 | 20 |
| 200 | BantengPanel | 0.960 ± 0.068 | 0.920 | 20 |
| 200 | Global-MAF | 0.980 ± 0.041 | 0.960 | 20 |
| 200 | Random-mean | 0.966 ± 0.048 | 0.932 | 20 |

### Key observation

At 48 SNP, BantengPanel reached 0.960 balanced accuracy, compared with 0.969 for Global-MAF and 0.962 for the random-panel mean. The population-aware ranking did not outperform Global-MAF at this size in this cohort. Treat the small-panel pattern as exploratory; repeated folds are not independent significance tests.


### Robustness at 48 SNP

| Perturbation | Balanced accuracy (mean ± SD) | Bali recall | Folds |
|---|---:|---:|---:|
| genotype_error_01 | 0.965 ± 0.067 | 0.930 | 20 |
| missing_05 | 0.960 ± 0.068 | 0.920 | 20 |
| missing_10 | 0.955 ± 0.069 | 0.910 | 20 |
| missing_20 | 0.940 ± 0.075 | 0.880 | 20 |

### Limitations

- Bali cohort is small; metrics are exploratory and have wide sampling uncertainty.
- Unknown close relatives may occur across random folds; no pedigree groups were supplied.
- Training-fold call-rate/MAF filtering and marker ranking avoid test-set selection leakage.
- Physical spacing is used as a simple redundancy guard; this MVP does not claim LD pruning.
- Repeated-fold standard deviations are descriptive, not inferential confidence intervals.

## Figshare cohort

107 animals; 16 Bali and 91 comparator animals; 52,886 source markers.

### Equal-size benchmark

| SNPs | Method | Balanced accuracy (mean ± SD) | Bali recall | Folds |
|---:|---|---:|---:|---:|
| 8 | BantengPanel | 0.996 ± 0.009 | 1.000 | 20 |
| 8 | Global-MAF | 0.969 ± 0.028 | 1.000 | 20 |
| 8 | Random-mean | 0.910 ± 0.014 | 0.974 | 20 |
| 16 | BantengPanel | 0.998 ± 0.007 | 1.000 | 20 |
| 16 | Global-MAF | 0.993 ± 0.012 | 1.000 | 20 |
| 16 | Random-mean | 0.961 ± 0.008 | 0.990 | 20 |
| 24 | BantengPanel | 1.000 ± 0.000 | 1.000 | 20 |
| 24 | Global-MAF | 0.999 ± 0.005 | 1.000 | 20 |
| 24 | Random-mean | 0.980 ± 0.007 | 0.997 | 20 |
| 48 | BantengPanel | 1.000 ± 0.000 | 1.000 | 20 |
| 48 | Global-MAF | 1.000 ± 0.000 | 1.000 | 20 |
| 48 | Random-mean | 0.996 ± 0.002 | 1.000 | 20 |
| 72 | BantengPanel | 1.000 ± 0.000 | 1.000 | 20 |
| 72 | Global-MAF | 1.000 ± 0.000 | 1.000 | 20 |
| 72 | Random-mean | 0.999 ± 0.001 | 1.000 | 20 |
| 96 | BantengPanel | 1.000 ± 0.000 | 1.000 | 20 |
| 96 | Global-MAF | 1.000 ± 0.000 | 1.000 | 20 |
| 96 | Random-mean | 1.000 ± 0.000 | 1.000 | 20 |
| 128 | BantengPanel | 1.000 ± 0.000 | 1.000 | 20 |
| 128 | Global-MAF | 1.000 ± 0.000 | 1.000 | 20 |
| 128 | Random-mean | 1.000 ± 0.000 | 1.000 | 20 |
| 156 | BantengPanel | 1.000 ± 0.000 | 1.000 | 20 |
| 156 | Global-MAF | 1.000 ± 0.000 | 1.000 | 20 |
| 156 | Random-mean | 1.000 ± 0.000 | 1.000 | 20 |
| 200 | BantengPanel | 1.000 ± 0.000 | 1.000 | 20 |
| 200 | Global-MAF | 1.000 ± 0.000 | 1.000 | 20 |
| 200 | Random-mean | 1.000 ± 0.000 | 1.000 | 20 |

### Key observation

At 48 SNP, BantengPanel reached 1.000 balanced accuracy, compared with 1.000 for Global-MAF and 0.996 for the random-panel mean. The population-aware ranking did not outperform Global-MAF at this size in this cohort. Treat the small-panel pattern as exploratory; repeated folds are not independent significance tests.


### Robustness at 48 SNP

| Perturbation | Balanced accuracy (mean ± SD) | Bali recall | Folds |
|---|---:|---:|---:|
| genotype_error_01 | 1.000 ± 0.000 | 1.000 | 20 |
| missing_05 | 1.000 ± 0.000 | 1.000 | 20 |
| missing_10 | 1.000 ± 0.000 | 1.000 | 20 |
| missing_20 | 1.000 ± 0.000 | 1.000 | 20 |

### Limitations

- Bali cohort is small; metrics are exploratory and have wide sampling uncertainty.
- Unknown close relatives may occur across random folds; no pedigree groups were supplied.
- Training-fold call-rate/MAF filtering and marker ranking avoid test-set selection leakage.
- Physical spacing is used as a simple redundancy guard; this MVP does not claim LD pruning.
- Repeated-fold standard deviations are descriptive, not inferential confidence intervals.

## Interpretation

Balanced accuracy and recall describe these source cohorts only. Repeated cross-validation folds overlap, and the small Bali groups and unknown pedigree relationships limit generalization. A full-cohort marker candidate is available as a separate CSV; it must be tested on an independent cohort before any performance claim. No statistical significance or assay-readiness claim is made.

## Reproducibility

Python 3.13.0 · scikit-learn 1.9.1 · source commit 4db10d10d5496b55aff291d851a3e2a823bfedc5.

See [Scientific Protocol](../../docs/SCIENTIFIC_PROTOCOL.md) and [Dataset Provenance](../../docs/DATA_PROVENANCE.md) for details.
