# Scientific protocol and claim boundaries

## Data and harmonization

The pipeline reads the Dryad Decker cattle PED/MAP/PEDIND files and the Sudrajad et al. Figshare text package as separate cohorts. It keeps their allele encodings separate. Dryad stores Illumina A/B alleles; Figshare encodes source minor/major alleles. Marker positions use UMD3.1. Do not combine dosage values across these sources without strand and allele-orientation harmonization.

## Target and metrics

The binary target is the source population label `BALI` versus all other recorded breeds. Balanced accuracy and Bali recall are reported. For every outer fold, the training split alone determines SNP call rate, pooled MAF, Bali-versus-comparator allele-frequency contrast, and panel ranking. The held-out split is used only for metric calculation. Logistic regression uses class weighting and a fixed regularization setting.

## Panel ranking and controls

Only autosomes 1–29 are retained; samples with over 10% missing genotypes are removed before splitting. Eligible markers pass 90% training-fold call rate and 1% pooled MAF. The ranking score is the absolute allele-frequency difference between Bali and the pooled comparator group. A greedy 250 kb within-chromosome spacing rule reduces obvious local redundancy. Controls are same-size random panels and same-size panels ranked by pooled global MAF. The spacing rule is not LD pruning; no claim of LD independence is made.

## Splitting and uncertainty

Repeated stratified folds are used because only 16 Bali animals appear in Figshare and 20 in Dryad. Pedigree or validated kinship groups are not available in the input files, so close relatives may cross folds. Fold means and standard deviations are descriptive; repeated folds overlap and must not be treated as independent replicates for significance testing. Small Bali sample counts create wide uncertainty.

## Interpretation

An apparent gain is a hypothesis for independent validation, not proof of a population-wide advantage. A full-cohort marker list is a design candidate, separate from the cross-validation results; it has not itself been externally validated. No panel is assay-ready: marker IDs and coordinates are supplied for research review, without validated probe design, strand, reference/alternate allele, or wet-lab performance. No recommendation should be used as a breeding, parentage, conservation, or animal-health decision without independent expert and field validation.

## Planned follow-up

1. Obtain a larger, unrelated and geographically representative Bali cohort.
2. Acquire pedigree or genomic kinship information and use grouped outer validation.
3. Freeze panel design before external validation and report calibration and subgroup performance.
4. Harmonize alleles and probe sequences against a chosen reference and assay platform.
5. Run wet-lab call-rate, reproducibility, and cost studies with a partner laboratory.
