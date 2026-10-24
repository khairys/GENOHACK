# BantengPanel — Evidence report

Generated: 2026-10-24T02:21:02.720130+00:00

## Scope and claim boundary

Research prototype for minimal SNP panel design. Binary source-label classification is a sanity check. S1 estimates expected pedigree mixture in simulation; PCA and atypical-animal review are descriptive. None establishes genetic purity or introgression in real cattle.

Protocol 2.0.0 · seed 20261024 · 4 folds × 5 repeats · 30 random spaced panels per fold.

All methods use the same spacing rule. Random panels use nested prefixes across sizes. S1 uses separate training references for each donor breed and shared test offspring across methods. Modal classification imputation is training-only but may favor the majority comparator group.

## Dryad cohort

1,542 animals after QC; 20 Bali, 1,522 comparators, 43,042 autosomal source markers.

### Equal-size source-label classification

| SNP | Method | BA mean ± SD | Bali recall | Folds |
|---:|---|---:|---:|---:|
| 8 | BantengPanel | 0.945 ± 0.074 | 0.900 | 20 |
| 8 | Global-MAF | 0.944 ± 0.055 | 0.960 | 20 |
| 8 | Random-mean | 0.914 ± 0.033 | 0.933 | 20 |
| 16 | BantengPanel | 0.949 ± 0.069 | 0.900 | 20 |
| 16 | Global-MAF | 0.951 ± 0.048 | 0.930 | 20 |
| 16 | Random-mean | 0.942 ± 0.042 | 0.930 | 20 |
| 24 | BantengPanel | 0.950 ± 0.069 | 0.900 | 20 |
| 24 | Global-MAF | 0.958 ± 0.049 | 0.930 | 20 |
| 24 | Random-mean | 0.952 ± 0.045 | 0.927 | 20 |
| 48 | BantengPanel | 0.960 ± 0.068 | 0.920 | 20 |
| 48 | Global-MAF | 0.969 ± 0.047 | 0.940 | 20 |
| 48 | Random-mean | 0.963 ± 0.046 | 0.931 | 20 |
| 72 | BantengPanel | 0.955 ± 0.069 | 0.910 | 20 |
| 72 | Global-MAF | 0.974 ± 0.044 | 0.950 | 20 |
| 72 | Random-mean | 0.967 ± 0.044 | 0.937 | 20 |
| 96 | BantengPanel | 0.950 ± 0.069 | 0.900 | 20 |
| 96 | Global-MAF | 0.970 ± 0.047 | 0.940 | 20 |
| 96 | Random-mean | 0.968 ± 0.043 | 0.938 | 20 |
| 128 | BantengPanel | 0.955 ± 0.069 | 0.910 | 20 |
| 128 | Global-MAF | 0.980 ± 0.041 | 0.960 | 20 |
| 128 | Random-mean | 0.967 ± 0.046 | 0.935 | 20 |
| 156 | BantengPanel | 0.960 ± 0.068 | 0.920 | 20 |
| 156 | Global-MAF | 0.985 ± 0.037 | 0.970 | 20 |
| 156 | Random-mean | 0.967 ± 0.045 | 0.936 | 20 |
| 200 | BantengPanel | 0.960 ± 0.068 | 0.920 | 20 |
| 200 | Global-MAF | 0.980 ± 0.041 | 0.960 | 20 |
| 200 | Random-mean | 0.968 ± 0.046 | 0.936 | 20 |

### Paired folds: BantengPanel minus Global-MAF

| SNP | Mean difference | Win / tie / loss |
|---:|---:|---|
| 8 | +0.002 | 14 / 0 / 6 |
| 16 | -0.001 | 16 / 0 / 4 |
| 24 | -0.008 | 15 / 1 / 4 |
| 48 | -0.009 | 10 / 7 / 3 |
| 72 | -0.019 | 8 / 8 / 4 |
| 96 | -0.020 | 4 / 12 / 4 |
| 128 | -0.025 | 3 / 13 / 4 |
| 156 | -0.025 | 1 / 15 / 4 |
| 200 | -0.020 | 0 / 16 / 4 |

At 8 SNP: BantengPanel 0.945; Global-MAF 0.944; random mean 0.914. This is descriptive; overlapping folds are not independent significance tests.

At 48 SNP: BantengPanel 0.960; Global-MAF 0.969; random mean 0.963. This is descriptive; overlapping folds are not independent significance tests.

### Atypical-animal review

Similarity uses full-cohort 200-marker candidates (post-hoc), not cross-validated ancestry. Errors are held-out predictions at 48 SNP, once per repeat. A flag requires confirmation; it does not prove introgression.

| Animal ID | Breed | Misclassified / evaluations | Bali similarity | Review flag |
|---|---|---:|---:|---|
| 615:615520410 | BALI | 0 / 5 | 0.995 | False |
| 615:615520420 | BALI | 0 / 5 | 0.995 | False |
| 615:615520430 | BALI | 0 / 5 | 0.995 | False |
| 615:615520440 | BALI | 0 / 5 | 1.000 | False |
| 615:615520450 | BALI | 0 / 5 | 0.995 | False |
| 615:615520460 | BALI | 0 / 5 | 0.995 | False |
| 615:615520480 | BALI | 0 / 5 | 1.000 | False |
| 615:615520490 | BALI | 0 / 5 | 1.000 | False |
| 615:615520510 | BALI | 0 / 5 | 1.000 | False |
| 615:615520520 | BALI | 0 / 5 | 1.000 | False |
| 615:615520530 | BALI | 0 / 5 | 1.000 | False |
| 615:615520540 | BALI | 0 / 5 | 1.000 | False |
| 615:615520550 | BALI | 0 / 5 | 1.000 | False |
| 615:615520640 | BALI | 0 / 5 | 0.995 | False |
| 615:615520660 | BALI | 0 / 5 | 0.995 | False |
| 615:615520670 | BALI | 5 / 5 | 0.490 | True |
| 615:615520680 | BALI | 0 / 5 | 0.784 | False |
| 615:615520690 | BALI | 3 / 5 | 0.581 | True |
| 615:615520700 | BALI | 0 / 5 | 0.994 | False |
| 615:615520710 | BALI | 0 / 5 | 0.995 | False |
| 618:618521020 | MAD | 1 / 5 | 0.339 | False |
| 618:618521080 | MAD | 2 / 5 | 0.319 | False |

### Robustness: 48 SNP

| Scenario | BA mean ± SD | Bali recall |
|---|---:|---:|
| genotype_error_01 | 0.960 ± 0.068 | 0.920 |
| missing_05 | 0.955 ± 0.069 | 0.910 |
| missing_10 | 0.955 ± 0.069 | 0.910 |
| missing_20 | 0.935 ± 0.067 | 0.870 |

### S1: simulated ancestry mixtures

64 F1, BC1 and BC2 offspring per donor/fold; expected Bali pedigree q = 0.50, 0.75 and 0.875. q is relative to each training reference pair; MAD and ONG are not ancestry-free or interchangeable references.

MAE averages F1/BC1/BC2. BC2 sensitivity is at an **oracle held-out ROC** point with empirical specificity ≥95%; the threshold uses test controls to describe the ROC, not to propose a deployable threshold. Only 4–5 controls per fold and shared parents limit interpretation.

| Donor | SNP | Method | q MAE ± SD | BC2 sensitivity | Specificity | Folds |
|---|---:|---|---:|---:|---:|---:|
| MAD | 8 | BantengPanel | 0.087 ± 0.016 | 0.352 | 1.000 | 18 |
| MAD | 8 | Global-MAF | 0.240 ± 0.061 | 0.151 | 1.000 | 18 |
| MAD | 8 | Random-mean | 0.225 ± 0.012 | 0.158 | 1.000 | 18 |
| MAD | 24 | BantengPanel | 0.070 ± 0.012 | 0.328 | 1.000 | 18 |
| MAD | 24 | Global-MAF | 0.157 ± 0.032 | 0.212 | 1.000 | 18 |
| MAD | 24 | Random-mean | 0.163 ± 0.014 | 0.199 | 1.000 | 18 |
| MAD | 48 | BantengPanel | 0.072 ± 0.017 | 0.391 | 1.000 | 18 |
| MAD | 48 | Global-MAF | 0.132 ± 0.029 | 0.229 | 1.000 | 18 |
| MAD | 48 | Random-mean | 0.144 ± 0.015 | 0.218 | 1.000 | 18 |
| MAD | 200 | BantengPanel | 0.090 ± 0.014 | 0.444 | 1.000 | 18 |
| MAD | 200 | Global-MAF | 0.119 ± 0.018 | 0.225 | 1.000 | 18 |
| MAD | 200 | Random-mean | 0.130 ± 0.018 | 0.263 | 1.000 | 18 |
| ONG | 8 | BantengPanel | 0.080 ± 0.017 | 0.397 | 1.000 | 20 |
| ONG | 8 | Global-MAF | 0.122 ± 0.024 | 0.244 | 1.000 | 20 |
| ONG | 8 | Random-mean | 0.223 ± 0.022 | 0.185 | 1.000 | 20 |
| ONG | 24 | BantengPanel | 0.070 ± 0.022 | 0.386 | 1.000 | 20 |
| ONG | 24 | Global-MAF | 0.099 ± 0.022 | 0.299 | 1.000 | 20 |
| ONG | 24 | Random-mean | 0.158 ± 0.020 | 0.240 | 1.000 | 20 |
| ONG | 48 | BantengPanel | 0.068 ± 0.025 | 0.377 | 1.000 | 20 |
| ONG | 48 | Global-MAF | 0.092 ± 0.021 | 0.325 | 1.000 | 20 |
| ONG | 48 | Random-mean | 0.136 ± 0.020 | 0.244 | 1.000 | 20 |
| ONG | 200 | BantengPanel | 0.070 ± 0.025 | 0.420 | 1.000 | 20 |
| ONG | 200 | Global-MAF | 0.090 ± 0.019 | 0.382 | 1.000 | 20 |
| ONG | 200 | Random-mean | 0.119 ± 0.024 | 0.280 | 1.000 | 20 |

Skipped donor-fold combinations: 2 (insufficient donor animals).

- Held-out parents only; independent Mendelian gametes per locus (unlinked approximation).
- q is expected pedigree mixture relative to Bali and each donor breed, not absolute banteng ancestry.
- MAD is already admixed; all source BALI labels are assumed controls, not confirmed pure.
- Composite likelihood assumes HWE and independent loci; 250 kb spacing is not LD pruning.
- Test-ROC sensitivity at >=95% empirical specificity is an oracle descriptive operating point, not a calibrated deployment threshold.
- Only 4–5 Bali controls per fold; folds and simulated descendants share parents and are not independent replicates.
- Simulated offspring are not independent real cattle; no field-validity or purity certification claim.

### Descriptive population PCA

133 animals, 3000 spaced markers; PC1 24.5%, PC2 3.5% variance. Included source codes: BALI, MAD, ONG, ACE, PES, BRE, THA, SAHW, GIR, RSIN. Descriptive structure only; axes and flagged animals do not prove introgression. Not used to select or validate panels.

### Limitations

- Bali cohort is small; metrics are exploratory and have wide sampling uncertainty.
- Unknown close relatives may occur across random folds; no pedigree groups were supplied.
- Training-fold call-rate/MAF filtering and marker ranking avoid test-set selection leakage.
- Physical spacing is used as a simple redundancy guard; this MVP does not claim LD pruning.
- Repeated-fold standard deviations are descriptive, not inferential confidence intervals.
- Modal imputation is fitted on pooled training animals and may favor the much larger comparator group.

## Figshare cohort

107 animals after QC; 16 Bali, 91 comparators, 52,886 autosomal source markers.

### Equal-size source-label classification

| SNP | Method | BA mean ± SD | Bali recall | Folds |
|---:|---|---:|---:|---:|
| 8 | BantengPanel | 0.996 ± 0.009 | 1.000 | 20 |
| 8 | Global-MAF | 0.969 ± 0.028 | 1.000 | 20 |
| 8 | Random-mean | 0.909 ± 0.016 | 0.972 | 20 |
| 16 | BantengPanel | 0.998 ± 0.007 | 1.000 | 20 |
| 16 | Global-MAF | 0.993 ± 0.012 | 1.000 | 20 |
| 16 | Random-mean | 0.964 ± 0.009 | 0.993 | 20 |
| 24 | BantengPanel | 1.000 ± 0.000 | 1.000 | 20 |
| 24 | Global-MAF | 0.999 ± 0.005 | 1.000 | 20 |
| 24 | Random-mean | 0.982 ± 0.004 | 1.000 | 20 |
| 48 | BantengPanel | 1.000 ± 0.000 | 1.000 | 20 |
| 48 | Global-MAF | 1.000 ± 0.000 | 1.000 | 20 |
| 48 | Random-mean | 0.997 ± 0.002 | 1.000 | 20 |
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

### Paired folds: BantengPanel minus Global-MAF

| SNP | Mean difference | Win / tie / loss |
|---:|---:|---|
| 8 | +0.026 | 13 / 6 / 1 |
| 16 | +0.004 | 4 / 16 / 0 |
| 24 | +0.001 | 1 / 19 / 0 |
| 48 | +0.000 | 0 / 20 / 0 |
| 72 | +0.000 | 0 / 20 / 0 |
| 96 | +0.000 | 0 / 20 / 0 |
| 128 | +0.000 | 0 / 20 / 0 |
| 156 | +0.000 | 0 / 20 / 0 |
| 200 | +0.000 | 0 / 20 / 0 |

At 8 SNP: BantengPanel 0.996; Global-MAF 0.969; random mean 0.909. This is descriptive; overlapping folds are not independent significance tests.

At 48 SNP: BantengPanel 1.000; Global-MAF 1.000; random mean 0.997. This is descriptive; overlapping folds are not independent significance tests.

### Atypical-animal review

Similarity uses full-cohort 200-marker candidates (post-hoc), not cross-validated ancestry. Errors are held-out predictions at 48 SNP, once per repeat. A flag requires confirmation; it does not prove introgression.

| Animal ID | Breed | Misclassified / evaluations | Bali similarity | Review flag |
|---|---|---:|---:|---|
| B01 | BALI | 0 / 5 | 0.975 | False |
| B02 | BALI | 0 / 5 | 1.000 | False |
| B03 | BALI | 0 / 5 | 0.995 | False |
| B04 | BALI | 0 / 5 | 0.985 | False |
| B05 | BALI | 0 / 5 | 1.000 | False |
| B06 | BALI | 0 / 5 | 0.995 | False |
| B07 | BALI | 0 / 5 | 1.000 | False |
| B08 | BALI | 0 / 5 | 0.975 | False |
| B09 | BALI | 0 / 5 | 0.990 | False |
| B10 | BALI | 0 / 5 | 0.980 | False |
| B11 | BALI | 0 / 5 | 0.975 | False |
| B12 | BALI | 0 / 5 | 0.985 | False |
| B14 | BALI | 0 / 5 | 1.000 | False |
| B15 | BALI | 0 / 5 | 0.995 | False |
| B17 | BALI | 0 / 5 | 0.985 | False |
| B18 | BALI | 0 / 5 | 0.990 | False |

### Robustness: 48 SNP

| Scenario | BA mean ± SD | Bali recall |
|---|---:|---:|
| genotype_error_01 | 1.000 ± 0.000 | 1.000 |
| missing_05 | 1.000 ± 0.000 | 1.000 |
| missing_10 | 1.000 ± 0.000 | 1.000 |
| missing_20 | 1.000 ± 0.000 | 1.000 |

### S1: simulated ancestry mixtures

64 F1, BC1 and BC2 offspring per donor/fold; expected Bali pedigree q = 0.50, 0.75 and 0.875. q is relative to each training reference pair; MAD and ONG are not ancestry-free or interchangeable references.

MAE averages F1/BC1/BC2. BC2 sensitivity is at an **oracle held-out ROC** point with empirical specificity ≥95%; the threshold uses test controls to describe the ROC, not to propose a deployable threshold. Only 4–5 controls per fold and shared parents limit interpretation.

| Donor | SNP | Method | q MAE ± SD | BC2 sensitivity | Specificity | Folds |
|---|---:|---|---:|---:|---:|---:|
| MAD | 8 | BantengPanel | 0.061 ± 0.005 | 0.768 | 1.000 | 20 |
| MAD | 8 | Global-MAF | 0.100 ± 0.012 | 0.639 | 1.000 | 20 |
| MAD | 8 | Random-mean | 0.209 ± 0.009 | 0.286 | 1.000 | 20 |
| MAD | 24 | BantengPanel | 0.043 ± 0.004 | 0.955 | 1.000 | 20 |
| MAD | 24 | Global-MAF | 0.064 ± 0.008 | 0.870 | 1.000 | 20 |
| MAD | 24 | Random-mean | 0.129 ± 0.005 | 0.521 | 1.000 | 20 |
| MAD | 48 | BantengPanel | 0.037 ± 0.003 | 0.998 | 1.000 | 20 |
| MAD | 48 | Global-MAF | 0.047 ± 0.006 | 0.955 | 1.000 | 20 |
| MAD | 48 | Random-mean | 0.099 ± 0.004 | 0.690 | 1.000 | 20 |
| MAD | 200 | BantengPanel | 0.026 ± 0.004 | 1.000 | 1.000 | 20 |
| MAD | 200 | Global-MAF | 0.030 ± 0.004 | 1.000 | 1.000 | 20 |
| MAD | 200 | Random-mean | 0.066 ± 0.005 | 0.955 | 1.000 | 20 |
| ONG | 8 | BantengPanel | 0.061 ± 0.006 | 0.737 | 1.000 | 20 |
| ONG | 8 | Global-MAF | 0.092 ± 0.021 | 0.595 | 1.000 | 20 |
| ONG | 8 | Random-mean | 0.182 ± 0.009 | 0.329 | 1.000 | 20 |
| ONG | 24 | BantengPanel | 0.038 ± 0.006 | 0.963 | 1.000 | 20 |
| ONG | 24 | Global-MAF | 0.062 ± 0.018 | 0.838 | 1.000 | 20 |
| ONG | 24 | Random-mean | 0.110 ± 0.004 | 0.607 | 1.000 | 20 |
| ONG | 48 | BantengPanel | 0.030 ± 0.005 | 0.998 | 1.000 | 20 |
| ONG | 48 | Global-MAF | 0.053 ± 0.016 | 0.916 | 1.000 | 20 |
| ONG | 48 | Random-mean | 0.085 ± 0.004 | 0.769 | 1.000 | 20 |
| ONG | 200 | BantengPanel | 0.025 ± 0.006 | 1.000 | 1.000 | 20 |
| ONG | 200 | Global-MAF | 0.040 ± 0.013 | 0.997 | 1.000 | 20 |
| ONG | 200 | Random-mean | 0.059 ± 0.007 | 0.985 | 1.000 | 20 |

Skipped donor-fold combinations: 0 (insufficient donor animals).

- Held-out parents only; independent Mendelian gametes per locus (unlinked approximation).
- q is expected pedigree mixture relative to Bali and each donor breed, not absolute banteng ancestry.
- MAD is already admixed; all source BALI labels are assumed controls, not confirmed pure.
- Composite likelihood assumes HWE and independent loci; 250 kb spacing is not LD pruning.
- Test-ROC sensitivity at >=95% empirical specificity is an oracle descriptive operating point, not a calibrated deployment threshold.
- Only 4–5 Bali controls per fold; folds and simulated descendants share parents and are not independent replicates.
- Simulated offspring are not independent real cattle; no field-validity or purity certification claim.

### Descriptive population PCA

107 animals, 3000 spaced markers; PC1 28.9%, PC2 5.0% variance. Included source codes: BALI, JABRES, KBO, MAD, ONG. Descriptive structure only; axes and flagged animals do not prove introgression. Not used to select or validate panels.

### Limitations

- Bali cohort is small; metrics are exploratory and have wide sampling uncertainty.
- Unknown close relatives may occur across random folds; no pedigree groups were supplied.
- Training-fold call-rate/MAF filtering and marker ranking avoid test-set selection leakage.
- Physical spacing is used as a simple redundancy guard; this MVP does not claim LD pruning.
- Repeated-fold standard deviations are descriptive, not inferential confidence intervals.
- Modal imputation is fitted on pooled training animals and may favor the much larger comparator group.

## Reproducibility

Source commit: `2796296a92c1f736faaa71f0f9b1138ccafd4a61`; dirty at invocation: `False`; identity captured before writes: `True`.

Python 3.13.0; scikit-learn 1.9.1. Scientific source/config SHA-256, archive checksums and QC counts are embedded in benchmark.json. The source tag identifies clean generation code; the release tag includes generated artifacts.

## Primary references

- [Decker et al. 2014: source cohort](https://doi.org/10.1371/journal.pgen.1004254)
- [Sudrajad et al. 2020: Indonesian cattle diversity](https://doi.org/10.1371/journal.pone.0241038)
- [Mohamad et al. 2009: no zebu introgression detected in the five Bali populations studied](https://doi.org/10.1371/journal.pone.0005490)
- [Wang et al. 2025: heterogeneous introgression history](https://doi.org/10.1038/s41467-025-62692-z)

These studies motivate this question; they do not validate this panel. See [Scientific protocol](../../docs/SCIENTIFIC_PROTOCOL.md).
