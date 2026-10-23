# Pitch script and judge Q&A

Target: 6 minutes for the track round. Each slide has the longer narration in its PowerPoint speaker notes. Metrics below match the completed benchmark in `artifacts/public/evidence_report.md`.

## Six-minute flow

| Time | Slide | Message |
|---:|---|---|
| 0:25 | 1 | BantengPanel tests whether a smaller marker set can retain useful information for Bali cattle. |
| 0:45 | 2 | Population-specific usefulness is a hypothesis; customer and assay evidence are not yet available. |
| 0:45 | 3 | A reproducible pipeline performs QC, train-fold marker ranking, equal-size comparison, and reporting. |
| 0:50 | 4 | Two verified public cohorts provide 20 and 16 Bali animals and are kept separate. |
| 1:15 | 5 | Dryad at 48 SNP: 0.960 vs 0.969 Global-MAF and 0.962 random. State that the method does not yet show a gain at this size. |
| 0:50 | 6 | Start with a research design service; interview evidence and economics remain to be collected. |
| 1:10 | 7 | Request an independent Bali cohort and a laboratory partner for the next validation stages. |

## Demo sequence

1. Open the dashboard at the Dryad cohort and point to the animal and SNP counts.
2. Compare the three equal-size baseline curves at 48 SNP; report the exact displayed values from the evidence report.
3. Switch to Figshare to show a second, separately analyzed cohort.
4. Open the robustness table and marker explorer; download the candidate CSV.
5. State that the panel is a computational candidate only, then show the 12-month validation steps.

Keep a local browser tab ready. The dashboard does not run a live analysis; it displays versioned outputs created by the CLI.

## Current measured finding

In Dryad, the 8-SNP BantengPanel mean is 0.962 balanced accuracy versus 0.940 Global-MAF and 0.915 random. At 16–200 SNP, Global-MAF is higher than BantengPanel. At 48 SNP the values are 0.960, 0.969, and 0.962 respectively. In Figshare, all three methods approach 1.000 at larger panel sizes. These are descriptive repeated-fold means from 20 overlapping test folds, with only 20 and 16 Bali animals; they do not establish statistical significance or population-wide superiority.

## Likely judge questions

**Why only 20 or 16 Bali animals?** These are the public raw genotype records available in the two verified sources. The reported 102-animal study does not link all raw genotypes. The cohort size limits precision, so we present this as an exploratory prototype and request a larger independent cohort.

**Does this prove the panel is ready for breeding use?** No. The target is Bali-versus-other-breed label discrimination. We have not tested breeding values, parentage, field outcomes, probe design, or wet-lab calls.

**Why should we trust the comparison?** SNP quality filtering and ranking happen in each training fold. The held-out samples measure performance. Global-MAF and random baselines use the same panel size. Repeated-fold SD is descriptive because folds overlap.

**Does the method prove a performance gain?** No consistent gain is shown. In Dryad, the 8-SNP result is promising but uncertain; Global-MAF is higher from 16 to 200 SNP, and the Figshare cohort quickly reaches a ceiling for all methods. We use this result to guide the next method and cohort, not claim superiority.

**Where is the cost reduction?** It has not been measured. A smaller candidate panel may reduce genotyping costs, but probe and laboratory costs, call rates, and turnaround must be measured with a partner before claiming savings.

**Who pays?** Our first customer hypothesis is a livestock-genetics PI or lab head; users are geneticists and analysts. We need interviews to confirm the workflow, buyer, budget path, and willingness to adopt.

**Can results from Dryad and Figshare be combined?** Not safely at this stage. Their numeric allele codes differ. We report both cohorts independently until allele orientation and assay mapping are harmonized.

**What is the immediate next experiment?** Freeze the panel candidate, acquire an unrelated Bali cohort with provenance and group information, and evaluate it once using a pre-registered grouped protocol. Then review assay feasibility with a laboratory.
