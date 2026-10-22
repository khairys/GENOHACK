# GENOHACK 2026 – PATHGEN INDUSTRY CHALLENGE
## Affordable Hotspot Panels for Indonesian Breast Cancer Patients

- **Source File:** `Hackathon/GENOHACK 2026 – PATHGEN INDUSTRY CHALLENGE.pdf`
- **Partner / Sponsor:** PathGen Diagnostik Teknologi
- **Target Audience:** Hackathon Participants, Deeptech Genomics Researchers, AI Agents
- **Context:** Precision Diagnostic Track, GENOHACK 2026

---

## 1. Problem Highlight

Breast cancer is the most common cancer in Indonesia, with **65,858 new cases and 22,430 deaths in 2020**, meaning deaths equal about one-third of new cases. Its molecular heterogeneity limits one-size-fits-all therapy, which is why molecular profiling matters: it identifies the genomic alterations that can guide treatment, including targeted therapy for eligible patients.

### The Population Bias & Reference Data Problem
The core problem is that the reference data behind breast cancer mutation panels come mainly from Western populations:
- In **TCGA-BRCA**, the most widely used reference, only **57 of 1,084 samples (about 5%)** are from Asian patients.
- Indonesian patients remain heavily underrepresented in current research.
- Where Asian cohorts have been studied (Korea, Malaysia, China), subtype and mutation patterns differ significantly from Western cohorts.
- An Indonesian cohort reported **PIK3CA mutations in 32.9% of cases**, with a peculiarly high frequency of **H1047L**.
- Consequently, a gene panel designed solely on Western genomic data may not perform equally well in Indonesian patients, leading to missed actionable targets and poor therapeutic outcomes.

### Clinical Actionability vs. Raw Frequency
Frequency alone is not enough to design a clinically viable panel:
- Alterations in genes such as **PIK3CA, ESR1, AKT1, and ERBB2** can have therapeutic implications in specific clinical settings, but not every mutation in these genes is actionable.
- Robust panel design must combine **how often a variant occurs in the target population** with **clinical evidence for its relevance to treatment selection** (e.g., levels of evidence in CIViC, ClinVar, ESMO/NCCN guidelines).

### The Cost Constraint
Cost is the final constraint:
- A large comprehensive genomic profiling (CGP) panel is far too expensive for routine healthcare use or BPJS reimbursement in Indonesia.
- A compact hotspot panel keeps testing affordable, accessible, and fast in regional diagnostic laboratories.
- This challenge asks teams to design a **compact panel that balances population fit, clinical actionability, and cost**.

---

## 2. The Challenge Statement

> **Design a compact, low-cost mutation panel (up to 15 targets) for breast cancer, optimized for patients in Indonesia and Southeast/East Asia. Show how the panel performs for Asian patients compared with a panel designed from Western data alone.**

---

## 3. Intended Use

- **Clinical Purpose:** Molecular profiling to support treatment selection in patients with a confirmed breast cancer diagnosis.
- **Out of Scope:** Screening and primary cancer diagnosis are strictly out of scope.
- **Priority:** Panels must prioritize **clinically actionable variants**, not merely frequent non-actionable polymorphisms.

---

## 4. Design Constraints

1. **Maximum of 15 targets.** (Fewer targets is better if clinical coverage holds).
2. **Target Nature:** Targets must be primarily **somatic variants**.
3. **Assay Format Neutral:** Must be suitable for either a targeted PCR-based assay (e.g., qPCR, multiplex PCR, dPCR) or a small targeted NGS panel. Teams must explicitly state which platform they assume.
4. **Cost Proxy:** Cost is proxied by the **number of targets** (and, optionally, the estimated number of multiplex reactions / primer pairs required).

---

## 5. Key Expectations & Deliverables

1. **Ranked Panel with Clinical Evidence:** Ranked list of target variants with documented clinical evidence for each target (using databases such as CIViC, ClinVar, OncoKB, PharmGKB).
2. **Coverage Curve:** Cumulative percentage of patients harboring at least one actionable variant plotted against the number of targets (1 to 15).
3. **Population Comparison:**
   - The same panel evaluated in Asian vs. Western cohorts.
   - Comparison between a panel designed purely from Asian data vs. a panel designed from Western data.
4. **Validation Methodology:** Train/design the panel on one discovery cohort, and evaluate/validate performance on an independent validation cohort.
5. **Indonesian / Southeast Asian Reality Check (Encouraged):** Compare the panel with published Indonesian and Southeast Asian findings (e.g., PIK3CA mutation spectrum including H1047L) and explicitly state what mutations the panel would capture vs. miss.
6. **Limitations & Next Steps:** Explain what *in silico* computational analysis cannot show, and outline what analytical validation (limit of detection, analytical specificity, reproducibility) and clinical validation (clinical sensitivity, therapeutic response correlation) would be required.
7. **The Indonesian Clinical Use Case:** Outline how this diagnostic test fits into Indonesian oncology workflows, laboratory infrastructure, turnaround time requirements, and health economics.

---

## 6. Public Data Sources (No Registration Required)

- **TCGA-BRCA PanCancer Atlas via cBioPortal:** 1,084 samples, includes patient demographic and race metadata:  
  [https://www.cbioportal.org/](https://www.cbioportal.org/)
- **Korean Breast Cancer Cohort (SMC, Asian, Whole-Exome Sequenced):** Listed on cBioPortal / CCDI:  
  [https://datacatalog.ccdi.cancer.gov/dataset/cBioPortal-BRCA_SMC](https://datacatalog.ccdi.cancer.gov/dataset/cBioPortal-BRCA_SMC)
- **cBioPortal Datahub (Bulk study files repository):**  
  [https://github.com/cBioPortal/datahub/](https://github.com/cBioPortal/datahub/)
- **ClinVar Database:**  
  [https://www.ncbi.nlm.nih.gov/clinvar/](https://www.ncbi.nlm.nih.gov/clinvar/)
- **CIViC (Clinical Interpretation of Variants in Cancer):**  
  [https://civicdb.org/](https://civicdb.org/)
- **Chinese Multi-Omics Cohort (Nature Cancer 2024):** Public resource paper with accession links:  
  [https://pubmed.ncbi.nlm.nih.gov/38347143/](https://pubmed.ncbi.nlm.nih.gov/38347143/)
- **Indonesian PIK3CA Mutation Data:** Reality check paper:  
  [https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12052133/](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12052133/)

---

## 7. Key Literature References

1. **SMC Korean Cohort:** *Multi-omics profiling of younger Asian breast cancers reveals distinctive molecular signatures.* Nat Commun. 2018; 9:4129. DOI: `10.1038/s41467-018-04129-4`.
2. **Malaysian Cohort:** Cancer Research Malaysia. *Genomic analysis of Malaysian breast cancers unravels molecular differences from Caucasian breast cancers.* ESMO Asia 2019, abstract 368P.
3. **Chinese Multiomic Cohort:** *Integrated multiomic profiling of breast cancer in the Chinese population reveals patient stratification and therapeutic vulnerabilities.* Nat Cancer. 2024; 5(4):673–690.
4. **Indonesian PIK3CA Study:** *High frequency of the PIK3CA H1047L mutation in Indonesian breast cancer across molecular subtypes.* Indonesian Journal of Cancer, 2023; PMC12052133.
5. **Ethnic Landscape in TCGA-BRCA:** Garibaldi-Ríos AF, et al. *Genomic Landscape of Breast Cancer: Study Across Diverse Ethnic Groups.* Diseases. 2025; 13(3):86.
