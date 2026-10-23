# Dataset provenance

| Cohort | Source | License | Included records | Format and allele coding | Processing |
|---|---|---|---|---|---|
| Worldwide cattle diversity | Decker et al. Dryad, DOI [10.5061/dryad.th092](https://doi.org/10.5061/dryad.th092) | CC0 | 1,543 animals, 43,043 SNPs, 134 breed labels; 20 rows labelled BALI | PED/MAP/PEDIND; genotype alleles are Illumina A/B coded 1/2; 0 is missing | Outer download is verified against the nested ZIP MD5 published by Dryad; source files are parsed in supplied order |
| Indonesian cattle | Sudrajad et al. Figshare, DOI [10.6084/m9.figshare.13083587](https://doi.org/10.6084/m9.figshare.13083587) | CC BY 4.0 | 107 animals, 52,886 markers; 16 rows labelled BALI | Long table with source minor/major allele codes 1/2; 0 is missing | Download checksum is verified before extraction; source breed codes are retained in sample metadata |

The two cohorts are analyzed separately. They are not merged because the numeric allele codes do not have the same meaning, and matching marker positions alone does not establish allele orientation. The Figshare breed mapping follows the source sample identifiers and sample counts: Madura (1), Jabres (2), Bali (3), Ongole (4), Kebumen Ongole (5). Preserve source IDs in output metadata.

Only autosomes 1–29 are retained. Dryad's map contains 25 repeated marker IDs at identical chromosome positions. The corresponding genotype calls sometimes disagree, so the parser preserves each source column and gives repeated IDs an explicit `__copyN` suffix. The 250 kb spacing rule prevents co-selecting markers at the same position. One Dryad individual exceeds the 10% sample-missingness threshold and is excluded before analysis; Figshare samples are all below the threshold.

## Checksums

- Dryad nested `WorldWideCattleDryad.zip` MD5: `0377a330590e4e8af07c1ebe416c975a`.
- Figshare `data_package.zip` MD5: `13f07b9bf8a0cb1e61d689cce08b30ec`.
- The pipeline writes locally computed SHA-256 values to `data/raw/manifest.json`.

Raw data and processed genotype arrays are ignored by Git. The user-supplied Dryad outer archive stays in the workspace and is not modified.
