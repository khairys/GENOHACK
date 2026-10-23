# BantengPanel MVP Implementation Blueprint

**Executive Technical Decision:** We propose an end-to-end **Python-based analysis pipeline** that selects population-specific SNP panels and a minimal web frontend for demonstration. The **primary dataset** will be the Bali cattle Illumina SNP50 genotypes (102 animals) reported by Sudrajad *et al.* (2022), complemented by a **baseline** dataset: the publicly available “WorldWideCattleDryad.zip” from Decker *et al.* (2014) (1,543 animals, 43,043 SNPs). We will **not** attempt whole-genome raw reads (PRJNA1108075) due to compute constraints. For implementation, use **PLINK2** for QC/LD pruning and **Python/Pandas/Scikit-learn** for selection and benchmarking. The backend API (FastAPI) will serve computed results to a simple Next.js/Tailwind dashboard. The MVP prioritizes the *scientific engine* (data processing and evidence) over UI polish. All components must be reproducible and data-driven, with no unverified claims.  

**Key Architectural Choices:** 
- **Data & QC:** Use PLINK2 (or PLINK 1.9) for genotype filtering (MAF, call rate, HWE) and LD pruning.  
- **SNP Selection:** Implement feature-selection (e.g. F<sub>ST</sub>-ranking or Random Forest importance) in Python.  
- **Benchmarking:** Compare optimized panels vs. random/global panels on held-out Bali genotypes. Measure classification accuracy/AUC for breed assignment.  
- **Tech Stack:** Python scientific stack (NumPy, Pandas, SciPy, Scikit-learn, or R if preferred) for computation; FastAPI for minimal backend; Next.js with Recharts for frontend visualization.  
- **Workflow:** The pipeline outputs CSV/JSON reports (selected SNP lists, performance metrics) that the backend reads. The frontend uses simple REST endpoints to fetch and display charts (performance vs SNP count, panel vs baseline).  

---

## Verified Dataset Selection  

- **Bali SNP50 (Sudrajad 2022):** *Description:* Illumina BovineSNP50 data from 102 Bali cattle (48 from a breeding center, 54 from farmers). *Format:* Genotypes (53K SNPs per animal). *Access:* Data are not directly linked, but the article is open-access under CC BY 4.0. Raw genotypes may require contacting authors. *Population:* Bali cattle. *Notes:* This is our **primary target dataset** (representing the local Bali panel). *Fallback:* If unavailable, we will extract the Bali subset from Decker’s Dryad file (the Dryad file includes 20 Bali individuals) or simulate a comparable dataset.  

- **WorldWideCattleDryad.zip (Decker 2014):** *Description:* Global cattle diversity genotypes (1,543 animals, 43,043 SNPs on Illumina BovineSNP50). *Link:* DOI 10.5061/dryad.th092. *Format:* ZIP containing text genotype matrix (see README). *License:* CC0 (public domain). *Population:* 134 breeds worldwide (includes some Bali). *Use:* **Baseline/control** dataset. We will use it to construct “global” or random panels of the same size as optimized panels. *Compatibility:* SNPs are Illumina IDs; we must map them to the Bali dataset (common SNP IDs). *Download:* e.g. `wget https://datadryad.org/stash/downloads/doi:10.5061/dryad.th092/WorldWideCattleDryad.zip`.  

- **Indonesian WGS (PRJNA1108075):** *Description:* Whole-genome sequencing of Indonesian cattle (SRA project cited in Narasimhan *et al.* 2025). *Format:* FASTQ reads. *Use:* **Not used** in MVP (too large to process in 40h). We mention it for completeness but do not attempt to derive genotypes.  

**Summary:** The **Sudrajad SNP50** and **Decker Dryad** datasets are legally open and contain the required SNP data. If Sudrajad’s raw genotypes cannot be obtained in time, we will use the overlapping SNPs from Dryad as a substitute “Bali” panel. We will ensure SNP coordinates/IDs are harmonized (e.g. using reference map or genomic positions) to allow fair comparison between panels.  

---

## Scientific Pipeline Blueprint  

**Overall Pipeline:** *Raw Data → QC → Population Analysis → Marker Selection → Benchmark → Evaluation Report.*

1. **Import Data:** Convert genotype files to PLINK binary (BED/BIM/FAM) or a NumPy matrix. For Dryad (text format), parse it into a DataFrame with individuals × SNP.  

2. **Quality Control (QC):** Using PLINK2:  
   - **Sample QC:** Remove individuals with >10% missing genotypes.  
   - **SNP QC:** Remove SNPs with call rate <90%, MAF <1%, or HWE p-value <1e-4.  
   - **Result:** A cleaned genotype matrix. *Tools:* `plink2 --bfile raw --geno 0.1 --maf 0.01 --hwe 1e-4 --make-bed --out qc`.  

3. **Population Structure Check:** Perform PCA or MDS (e.g. with `plink2 --pca` or scikit-learn `PCA`) to confirm that Bali cattle cluster together and are separable from others. This ensures population differentiation exists. If no structure, warn team.  

4. **Train/Test Split:** Randomly split Bali samples into training and held-out sets (e.g. 70% train, 30% test) to avoid overfitting. Fix a random seed for reproducibility. Ensure related individuals are not split (if known).  

5. **Marker Selection (for various panel sizes):**  
   - For each target panel size (e.g. 48, 72, 96, 128, 156, 200 SNP):  
     - **Approach A (F<sub>ST</sub> ranking):** Compute per-SNP F<sub>ST</sub> between Bali vs. all other cattle (using training genotypes). Rank SNPs by F<sub>ST</sub>, select top-*k*.  
     - **Approach B (Feature Importance):** Train a simple classifier (e.g. Random Forest or Logistic Regression) to distinguish Bali vs. others on training set. Use feature importance or coefficients to rank SNPs. Select top-*k*.  
     - **Approach C (LD-aware):** Ensure selected SNPs are not in high LD (via pruning) to maximize independent information. Can incorporate LD-pruning as PLINK step (`--indep-pairwise`).  
     - We will likely implement one approach (e.g. F<sub>ST</sub>) as proof of concept, since F<sub>ST</sub> is intuitive and fast.  

6. **Baseline Panels:** Create comparison panels of equal size *k*:  
   - **Random Panel:** Randomly pick *k* SNPs (repeat 5–10 times for variability).  
   - **Global Informed Panel:** Pick *k* SNPs that maximize global differentiation (e.g. top F<sub>ST</sub> from worldwide dataset or from Bali vs. others in Dryad).  
   - **Standard Parentage Panel (if available):** If there is an ICAR/ISAG-recommended SNP list (≈200 SNP), we will use the overlapping subset as a “standard panel.” However, we assume none is directly given for Bali, so this is optional.  

7. **Benchmark (Ancestry Discrimination):** For each panel (optimized vs baseline) of size *k*:  
   - Apply the panel to held-out Bali and non-Bali samples.  
   - **Metric:** Compute classification accuracy or AUC of a classifier (e.g. logistic regression) distinguishing Bali vs. non-Bali using only these SNPs. Also report F<sub>ST</sub> of panel as a sanity check.  
   - **Cross-validation:** Repeat train/test split or use k-fold CV to estimate variability.  

8. **Benchmark (Parentage, Optional):** If time permits, simulate offspring to test pedigree inference:  
   - Take two held-out Bali “parents”, simulate an offspring genotype by Mendelian inheritance at the panel SNPs. Then check if the panel identifies the correct parents (exclusion check).  
   - We note that simulation results are approximate (not field test) and must be clearly labeled as such.  

9. **Results & Reporting:** Generate output tables/JSON containing: selected SNP IDs for each panel, classification metrics (accuracy, precision/recall), F<sub>ST</sub> values, and notes on robustness (e.g. performance under ~5% random genotype dropout). The performance vs. *k* graph is critical.  

**Algorithm References:** Our filtering mirrors Sudrajad *et al.* (2022) use of PLINK for SNP QC. Using ~100–200 SNP is reasonable given prior work: e.g. ~100 high-quality SNP can give ~95% parentage accuracy in simple cases, but complex populations may need 300–500. This guides our panel size choices.  

---

## System Architecture  

- **Project Structure:**  
  ```
  bantengpanel/
  ├── data/               # Raw and processed genotype files (PLINK, CSV)
  ├── scripts/
  │   ├── qc_pipeline.py  # SNP and sample filtering (using PLINK via subprocess or pyPLINK)
  │   ├── select_snps.py  # Algorithm for ranking/selecting SNPs
  │   ├── benchmark.py    # Runs benchmarking experiments and computes metrics
  │   └── utils.py        # Helper functions (e.g. load genotype, compute Fst)
  ├── backend/
  │   ├── main.py         # FastAPI app exposing REST endpoints
  │   └── models.py       # Data models (Pydantic) for API I/O/Output
  ├── frontend/
  │   ├── pages/index.js  # Next.js page (results dashboard)
  │   └── components/     # React components for charts, tables
  ├── requirements.txt    # Python dependencies (numpy, pandas, scikit-learn, fastapi, uvicorn)
  ├── package.json        # Frontend dependencies (next, react, recharts, tailwindcss)
  └── README.md
  ```
- **Workflow:** The Python scripts in `scripts/` will be run offline (locally or in cloud notebook) to produce result files (`.json`, `.csv`) in `data/` or `backend/` folder. The FastAPI backend (`main.py`) reads these result files on startup and provides endpoints like `GET /api/panels` (returns panel configurations and metrics) and `GET /api/plot-data` (returns arrays for charts). The Next.js frontend fetches from these endpoints to render charts (e.g. SNP count vs. accuracy, comparison bar chart of optimized vs baseline for each *k*) using Recharts or similar.  

- **Data Flow:** `scripts/` → generate `data/results_*` → `backend/main.py` loads `data/results_*` → frontend fetches JSON → display. No database or authentication is needed.  

- **API Contract Examples:**  
  - **GET** `/api/panels` → returns JSON list: `[{"panel_size":96, "opt_accuracy":0.85, "baseline_accuracy":0.78, "selected_snps": ["rs1",...], ...}, ...]`.  
  - **GET** `/api/snp-performance?size=96` → returns JSON with arrays of accuracies vs. repeats for optimized vs random panels (for plotting error bars).  

- **Libraries/Tools:** PLINK2 (for genotype QC and LD pruning) – invoked via command line. Python libs: `pandas` (data I/O), `numpy` (array ops), `scikit-learn` (PCA, classifiers), `statsmodels` or custom (F<sub>ST</sub> calculation). FastAPI for backend. Frontend: Next.js, React, Recharts, Tailwind CSS.  

---

## MVP Feature Specification  

- **Must-Have:**  
  - **Dataset selection:** The team uses pre-processed data (Bali vs. non-Bali) by default. No need for upload feature.  
  - **SNP Optimization Process (hidden):** The UI shows the *result* of the optimization (no need to re-run heavy computation in browser).  
  - **Performance Comparison:** A clear chart of panel size (x-axis) vs performance metric (y-axis) for Optimized vs. Baseline panels. E.g. line graph with 96,128,... SNP on x-axis, accuracy on y-axis.  
  - **Panel Detail Display:** For a selected panel size (e.g. 96), show the list of optimized SNP IDs and the baseline SNP IDs. Also show numeric metrics (accuracy, F<sub>ST</sub>) for each.  
  - **Evidence Report:** A brief text or list summarizing results: e.g. “At 96 SNP, optimized panel gave 85% accuracy vs. 78% for baseline (p<0.01)”. Provide a download (CSV/JSON) of the selected SNP list.  

- **Nice-to-Have:**  
  - **Interactive parameter slider:** Allow demo user to adjust panel size (48–200) and dynamically update the chart (if performance data already precomputed).  
  - **Multiple Baselines:** Option to toggle between “Random baseline” vs “Global baseline” panels in the chart.  
  - **PCA Plot:** A scatterplot of first two PCs colored by breed, to visually show discrimination (not required but persuasive).  

- **Post-Hackathon (Future) – Out of Scope:**  
  - Integration with actual lab/genotyping pipeline (wet lab).  
  - User authentication or multi-user.  
  - Extensive error handling (focus on success path).  
  - Packaging as a production SaaS (deliver prototype only).  

- **Explicitly Excluded:**  
  - No smartphone app or VR.  
  - No database back-end; static file serving is sufficient.  
  - We will not implement the wet-lab component or actual ICAR certification.  
  - We will not claim the optimized 96 SNP panel is “ICAR-certified” or fully equivalent to standard tests. Instead, we show benchmarking results.

---

## Benchmark & Validation Protocol  

**Benchmark Experiment:** Perform an **equal-budget SNP test** on held-out Bali genotypes. For example, compare the optimized 96-SNP panel vs a baseline 96-SNP panel (random or global) on the same test set. 

- **Null Hypothesis (H0):** The optimized panel does *not* achieve higher discriminative performance (Bali vs non-Bali) than the baseline panel of equal size.  
- **Alternative (H1):** The optimized panel has significantly better performance.  

**Metrik Utama:** Classification accuracy or AUC of distinguishing Bali vs others. We will compute accuracy on the test set for multiple random splits (e.g. 5-fold CV) and report mean±SD. Also compute the average pairwise F<sub>ST</sub> (or fixation index) among panels. 

**Statistical Test:** Use a paired t-test or bootstrap to compare optimized vs. baseline accuracies across splits. Significance (e.g. p<0.05) indicates *meaningful* improvement. 

**Performance Graphs:**  
- **Panel Size vs. Accuracy:** Plot *k* (48,72,96,128,156,200) on x-axis, accuracy on y-axis for both optimized and baseline (with error bars). Look for diverging curves.  
- **Random Baseline Distribution:** Show a boxplot or shaded range of accuracies for ~10 random panels of size *k*, vs. optimized.  

**Interpretation:**  
- If optimized panel consistently outperforms baseline (e.g. +5–10% accuracy), that supports the hypothesis.  
- If optimized ≈ baseline, we conclude no strong advantage; then we must **not** overstate performance – the product may only match existing tools.  
- If optimized < baseline, we may have to pivot (e.g. try different selection method or highlight that this was an exploratory result).  

**Parentage Test (optional):** We may simulate simple parent-offspring pairs to see if the panel can exclude non-parents. E.g. given true parent genotypes, count how often random unrelated “candidate” animals are excluded by the panel (mismatch in a required proportion of SNPs). However, this is secondary; the demo should emphasize ancestry/breed discrimination, which is directly supported by our dataset. 

---

## Development Roadmap  

Prioritize the **scientific core first**, then UI. Assume a 40-hour hackathon, 3 devs.

1. **Day 0 (Preparation):** Each member sets up the environment: install Python 3.9+, PLINK2 (conda or binary), Node.js (for frontend). Clone repo skeleton (as above).  

2. **Task A – Dataset Acquisition & QC (Team 1, 6h):**  
   - **Data download:** Team 1 downloads the Dryad ZIP and extracts genotype files. If possible, also requests the Sudrajad 102-sample genotype (or uses the Dryad subset as proxy).  
   - **Format conversion:** Convert genotype text to PLINK format (create .ped/.map or .bed). *Deliverable:* `data/cattle.bed` with all 1543 samples (or at least the Bali subset).  
   - **QC Filtering:** Run PLINK2 for QC: remove low-MAF SNPs and poor-quality samples. *Deliverable:* `data/cattle_qc.bed` and logs of SNP/sample counts.  
   - **Check:** Confirm the cleaned data loads into pandas (e.g. run `plink2 --freq` to verify allele frequencies).

3. **Task B – SNP Selection & Benchmark (Team 2, 12h):**  
   - **Algorithm prototyping:** Write `select_snps.py` to compute F<sub>ST</sub> (using training set). As a fallback, use an existing library or simple allele-frequency difference. Test on small k (e.g. 48,96).  
   - **Generate Panels:** For each k, output a CSV of selected SNP IDs. Also generate one random panel per k.  
   - **Benchmarking code:** Implement `benchmark.py` that takes a panel list and computes accuracy on test set. Use scikit-learn logistic regression or random forest. Output accuracy. Repeat for 5 folds.  
   - **Run experiments:** Produce `results/benchmarks.json` containing accuracy (mean, SD) for optimized vs random panels at each k. *Acceptance:* Clear numbers showing any gain.  
   - **Unit test:** Check that removing a SNP changes result (sanity) and that reproducibility holds (fixed seed).  

4. **Task C – Backend Integration (Team 2, 4h):**  
   - **API endpoints:** Develop FastAPI in `backend/main.py`. On startup, it loads `results/benchmarks.json`.  
   - **Implement routes:** e.g. `/api/panels` returns panel summaries (size, accuracies, SNP lists). `/api/plot` returns series data for plotting.  
   - **Acceptance:** Using `curl` or Postman, verify endpoints return correct JSON (fields match expectation).  

5. **Task D – Frontend Dashboard (Team 3, 12h):**  
   - **Static mockup:** Create `pages/index.js` with placeholders.  
   - **Charts:** Using Recharts, implement a line chart (panel size vs accuracy) and bar charts. Data fetched from `/api/panels`.  
   - **Panel details:** List of SNPs and metrics for a selected size (e.g. dropdown or tabs for different k).  
   - **Styling:** Use Tailwind for a clean look. Keep it simple (no login, just results view).  
   - **Acceptance:** The demo shows the charts populated with real data from the backend.  

6. **Task E – Testing & Reproducibility (Team 1&2, 6h):**  
   - **Re-run pipeline:** Use a Python notebook to re-run all steps from raw data to final JSON, to ensure no manual steps.  
   - **Edge cases:** Test with missing data (e.g. drop 10% of genotypes) to ensure metrics code tolerates it.  
   - **Demo prep:** Ensure the demo script (maybe a simple `run_demo.sh`) can build data, start backend and frontend.  
   - **Acceptance:** One command builds everything; results match earlier runs.  

**Dependencies:** Tasks A → B (need QC data before selection), B → C (benchmarks before API), C → D (API before frontend). All teams should sync daily.  

**Division of Labor:**  
- **Dev 1:** Focus on data & QC (Tasks A, part of E).  
- **Dev 2:** Algorithm & backend (Tasks B, C).  
- **Dev 3:** Frontend UI (Task D, assist with E).  

---

## Risks & Fallbacks  

- **Data access risk:** If Sudradjad’s Bali genotypes cannot be obtained, fallback to using the 20 Bali samples from Dryad or simulate additional samples. In that case, we must note the limitation (small sample size) in the report.  
- **Compatibility risk:** If SNP IDs in Bali vs Dryad datasets do not match (different arrays/versions), fallback: intersect on chromosome–position (if known) or use only common SNPs. Document any reduction in SNP count.  
- **No performance gain:** If optimized panel does not outperform baseline, do *not* force the narrative. Instead, highlight that the exercise created an evidence report and mention that BioTrace (or other solutions) could be reconsidered. The frontend can still show that “performance is equivalent.”  
- **Compute/time risk:** Feature selection on 43K × 1543 may be slow. Fallback: downsample SNPs by LD pruning first (`plink2 --indep-pairwise 50 5 0.5`) to <10K, then select. Also use efficient libraries (NumPy vector ops, avoid loops).  
- **Integration risk:** If FastAPI deployment takes too long, fallback: serve static JSON files and use simple Node.js/Express or even plain file serving.  
- **Frontend risk:** If Recharts integration is difficult, fallback: render static plots using Python (matplotlib) and embed as images (though less dynamic).  

In all cases, the fallback should be “graceful degradation” but the core deliverable remains: a working prototype that illustrates the SNP optimization concept with real data (or simulated surrogate).

---

## Implementation Checklist  

1. **[ ] Dataset:** Acquire and verify genotype data (Dryad & Bali).  
2. **[ ] Environment:** Install PLINK2, Python (with `pandas, scikit-learn, numpy`), Node.js (with Next.js, Recharts).  
3. **[ ] QC Pipeline:** Implement and run SNP/sample filtering. Check final SNP count (aim ~40K). (Use `--geno`, `--maf` filters in PLINK.)  
4. **[ ] SNP Selection Code:** Write script to rank SNPs (e.g. compute F<sub>ST</sub>) and output top-*k*.  
5. **[ ] Benchmark Script:** Compute accuracy of each panel vs. baseline; produce JSON output.  
6. **[ ] API Endpoints:** FastAPI app serves the JSON results and SNP lists.  
7. **[ ] Frontend Dashboard:** Fetch data from backend and display: performance vs panel size; table of SNPs.  
8. **[ ] Testing:** Verify end-to-end with a small example; ensure reproducibility (fixed seeds, docs).  
9. **[ ] Documentation:** Comment code and write a brief README (pipeline steps, how to run demo).  
10. **[ ] Pitch Preparation:** Prepare a short demo script highlighting the key innovation (optimized vs baseline) and mention next steps (e.g. lab validation).

---

## First Actions  

1. **Download and inspect datasets:** Run  
   ```bash
   wget https://datadryad.org/stash/downloads/doi:10.5061/dryad.th092/WorldWideCattleDryad.zip
   unzip WorldWideCattleDryad.zip
   ```  
   Review the contents (it includes a README and genotype text file). Confirm format (likely SNP-by-sample matrix).  

2. **Prepare PLINK inputs:** If data is text, convert it to PED/MAP or VCF. For example, use `plink2 --23file cattle.txt --make-bed` (if formatted) or write a small Python script to generate PED/MAP and then `plink`. Ensure the genome build is consistent.  

3. **Install tools:** Install PLINK2 (`conda install -c bioconda plink2`) and Python libraries:  
   ```bash
   pip install numpy pandas scikit-learn fastapi uvicorn
   ```  
   For frontend:  
   ```bash
   npx create-next-app frontend
   cd frontend
   npm install recharts tailwindcss
   ```  

4. **Run initial QC:** Execute a test QC on a subset. For example:  
   ```bash
   plink2 --bfile cattle_raw --maf 0.01 --geno 0.1 --make-bed --out cattle_qc
   ```  
   Check the log to see how many SNPs pass. This confirms PLINK setup and data integrity.  

5. **Prototype SNP ranking:** Quickly compute allele frequencies for Bali vs others (using PLINK’s `--freq case-control`) and calculate F<sub>ST</sub> by hand or using a tool. Identify the top ~10 SNP to ensure the selection code works.  

By completing these actions, the team ensures the core data and tools are in place so that the rest of the MVP can build on a solid foundation. These steps also yield initial numbers (e.g. “Raw data had 53K SNP, QC retained ~45K SNP”) that can be cited in progress reports.