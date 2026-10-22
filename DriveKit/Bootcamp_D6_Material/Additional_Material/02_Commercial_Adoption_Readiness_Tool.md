# Commercial Adoption Readiness Assessment Tool (CARAT): Overview & User Guide
**Source Document:** Commercial Adoption Readiness Assessment Tool (CARAT)  
**Version:** March 2023 (Official Release)  
**Authors:** Lucia Tian, Jacob Mees, Vanessa Chan (Office of Technology Transitions - DOE); William Dean (Office of Clean Energy Demonstrations - DOE)  
**Publishing Agency:** U.S. Department of Energy (DOE)  
**Reference Portal:** [energy.gov/technologytransitions/arl](https://energy.gov/technologytransitions/arl)  
**Context:** Standardized Operational Rubric for GENOHACK 2026 Deep-Tech Commercialization Audits  
**Total Pages:** 13  

---

## Executive Summary & Assessment Architecture

The **Commercial Adoption Readiness Assessment Tool (CARAT)** operationalizes the Adoption Readiness Level (ARL) framework. While Technology Readiness Levels (TRL) stage-gate whether an engineered solution works in a laboratory or simulated operational environment, **CARAT provides a standardized, fact-based rubric to evaluate whether the broader market, capital, regulatory, and industrial ecosystem is prepared to adopt and scale the technology.**

The assessment evaluates **17 discrete dimensions of adoption risk** grouped under four foundational categories:

```mermaid
flowchart TD
    subgraph The 4 CARAT Categories (17 Dimensions)
        A["A. Value Proposition<br/>(3 Dimensions: Cost, Performance, Ease of Use)"]
        B["B. Market Acceptance<br/>(3 Dimensions: Demand Maturity, TAM, Downstream Value Chain)"]
        C["C. Resource Maturity<br/>(6 Dimensions: Capital, Project Mgmt, Infrastructure, Supply Chain, Materials, Workforce)"]
        D["D. License to Operate<br/>(5 Dimensions: Regulation, Policy, Permitting, Safety, Community Perception)"]
    end
    A & B & C & D --> E["Risk Tallies<br/>(Count of High & Medium Risks)"]
    E --> F["ARL Look-Up Matrix<br/>(Power-Law Aggregation)"]
    F --> G["Final Adoption Readiness Level<br/><b>ARL Score: 1 to 9</b>"]
```

---

## User Instructions for Conducting an Assessment

### 1. Define the Assessment Scope
Similarly to TRL, a CARAT evaluation can be performed at multiple levels of abstraction. Evaluators must explicitly record:
* **Technology Scope:** Is the evaluation focused strictly on an isolated component (e.g., a proprietary sequencing enzyme, an algorithm), or on an integrated turnkey system (e.g., an automated benchtop diagnostic platform)?
* **Value Chain Scope:** Does the assessment evaluate only internal product manufacturing, or does it incorporate midstream distribution, cold-chain logistics, and hospital waste disposal?
* **Evaluation Time Horizon:** Standard best practice is to evaluate adoption feasibility over an active **3 to 5 year commercialization window** starting from the evaluation date.

### 2. Document the Baseline Policy & Regulatory Environment
Record the existing legislative, reimbursement, and policy landscape under which the venture operates. Assume current laws and regulations remain in effect without speculative assumptions of future bailouts or favorable subsidies.

### 3. Score Each Dimension (Low, Medium, High Risk, or N/A)
Evaluate the technology against every cell in the rubric. Document empirical justifications, customer quotes, reference studies, and data sources in the comments section.

### 4. Aggregate Scores into a Numerical ARL (1–9)
Tally the total number of "High Risk" and "Medium Risk" dimensions, then cross-reference the **CARAT Look-Up Matrix** to determine the final composite score.

---

## Complete CARAT Assessment Rubric (All 17 Dimensions)

### Category A: Value Proposition
*Focus: Evaluates whether the technology meets market functionality at a viable price point (Product-Market Fit).*

#### 1. Delivered Cost
*Risks associated with achieving delivered cost competitiveness when produced at full commercial scale (including amortization of development and capital costs, and customer switching costs).*

| Risk Level | Operational Evaluation Criteria |
| :--- | :--- |
| **LOW RISK** | Technology solution is either: (a) currently more cost-effective than incumbent or competing solutions, or (b) close to cost-parity and on a clear cost reduction curve to achieve parity within 3 years; and fundamental input costs are not exposed to severe market volatility. |
| **MEDIUM RISK** | Technology solution is $> 3$ years away from achieving cost parity with incumbents, but possesses a clear, validated pathway to cost-effectiveness; and/or some fundamental cost components remain exposed to commodity swings. |
| **HIGH RISK** | Technology solution is significantly more expensive than incumbents, and there is no credible pathway to cost competitiveness without substantial fundamental scientific/R&D breakthroughs. |
| **N/A** | Delivered cost is not a factor in market adoption (e.g., life-or-death unique clinical interventions with zero competitors). |

---

#### 2. Functional Performance
*Risks associated with meeting or exceeding the feature-set and performance of incumbents or unlocking new markets.*

| Risk Level | Operational Evaluation Criteria |
| :--- | :--- |
| **LOW RISK** | Solution delivers sustained, demonstrable performance improvements or clinical/operational benefits that fully justify any price premium in an existing or novel market application. |
| **MEDIUM RISK** | Solution provides performance parity with existing market solutions, or the performance improvement fails to justify the required price premium, or the performance differential cannot be sustained due to weak patent/IP protection. |
| **HIGH RISK** | Solution exhibits inferior functional performance, lower analytical accuracy, or higher error rates than existing fielded alternatives. |
| **N/A** | Performance parity is not evaluated. |

---

#### 3. Ease of Use / Complexity
*Risks associated with customer switching costs, personnel retraining, and operational friction.*

| Risk Level | Operational Evaluation Criteria |
| :--- | :--- |
| **LOW RISK** | Highly intuitive, easy to operate and maintain by standard technicians with minimal training; plug-and-play interoperability with existing customer infrastructure. |
| **MEDIUM RISK** | Operable by standard personnel following moderate training programs; compatible with existing hospital/lab workflows with minor procedural adjustments. |
| **HIGH RISK** | Requires extensive specialized retraining, creation of new job titles, or prohibitive integration costs to interface with customer IT/LIMS workflows. |
| **N/A** | Operational complexity does not impact adoption. |

---

### Category B: Market Acceptance
*Focus: Evaluates market demand certainty, channel access, and structural barriers erected by incumbents.*

#### 4. Demand Maturity / Market Openness
*Risks associated with demand certainty, off-take contracting mechanisms, and incumbent monopoly power.*

| Risk Level | Operational Evaluation Criteria |
| :--- | :--- |
| **LOW RISK** | Established, liquid market with transparent off-take contracts; diverse customer base with low concentration risk; zero structural barriers to market entry. |
| **MEDIUM RISK** | Emerging market demand with limited standardized contracting mechanisms; moderate customer concentration risk; or modest first-mover network effects from incumbents. |
| **HIGH RISK** | Illiquid or unproven market; severe customer concentration (single monopsony buyer); or entrenched incumbent monopolies possessing insurmountable switching barriers. |
| **N/A** | Market dynamics do not apply. |

---

#### 5. Market Size
*Risks associated with the overall magnitude and certainty of the Total Addressable Market (TAM).*

| Risk Level | Operational Evaluation Criteria |
| :--- | :--- |
| **LOW RISK** | Large, high-certainty addressable market that easily justifies commercialization capital investments and provides substantial headroom for growth. |
| **MEDIUM RISK** | Sizable market, but subject to macroeconomic volatility or uncertain customer expansion rates; requires adjacent market capture to sustain scale. |
| **HIGH RISK** | Niche, highly constrained addressable market that cannot generate venture-scale economic returns or amortize initial capital expenditures. |
| **N/A** | Market size is non-restrictive. |

---

#### 6. Downstream Value Chain
*Risks associated with moving products physically and logistically from manufacturing facilities to the ultimate customer.*

| Risk Level | Operational Evaluation Criteria |
| :--- | :--- |
| **LOW RISK** | Proven, robust, multi-vendor distribution channels exist (e.g., standard medical supply couriers, room-temperature shelf stability). |
| **MEDIUM RISK** | Distribution channels exist but require moderate operational modifications (e.g., specialized cold-chain $-20^\circ	ext{C}$ logistics, dedicated clinical handling). |
| **HIGH RISK** | Downstream distribution network is completely absent; requires constructing dedicated, specialized multi-island distribution infrastructure from scratch. |
| **N/A** | Downstream logistics are irrelevant (e.g., pure cloud SaaS). |

---

### Category C: Resource Maturity
*Focus: Evaluates availability of capital, supply chains, infrastructure, and human talent required to produce the solution.*

#### 7. Capital Flow
*Risks associated with securing commercial debt, equity, and project financing.*

| Risk Level | Operational Evaluation Criteria |
| :--- | :--- |
| **LOW RISK** | Ample commercial capital available; conservative institutional lenders and venture investors actively deploy non-recourse debt and growth equity into the sector. |
| **MEDIUM RISK** | Capital is available from specialized impact/venture investors, but traditional commercial banks and underwriters remain hesitant without public loan guarantees. |
| **HIGH RISK** | Private sector capital is virtually inaccessible; private investors perceive technology or adoption risk as prohibitive without $>80\%$ non-dilutive government subsidies. |
| **N/A** | Capital availability is non-critical. |

---

#### 8. Project Development, Integration & Management
*Risks associated with standardized engineering, site development, and deployment execution.*

| Risk Level | Operational Evaluation Criteria |
| :--- | :--- |
| **LOW RISK** | Standardized, repeatable deployment blueprints; numerous certified contractors and system integrators capable of on-time, on-budget execution. |
| **MEDIUM RISK** | Moderate project complexity; limited pool of experienced engineering contractors; occasional scheduling delays in system integration. |
| **HIGH RISK** | Highly bespoke, unstandardized installation processes; acute shortage of capable integration partners; persistent history of severe cost overruns. |
| **N/A** | Not applicable to single-unit manufactured goods. |

---

#### 9. Infrastructure
*Risks associated with large-scale external infrastructure required to support deployment.*

| Risk Level | Operational Evaluation Criteria |
| :--- | :--- |
| **LOW RISK** | All required external utilities, transport networks, broadband, and specialized disposal systems exist with abundant excess capacity. |
| **MEDIUM RISK** | Core infrastructure exists but requires localized upgrades or capacity expansions (e.g., dedicated hospital 3-phase power or backup generators). |
| **HIGH RISK** | Deployment is fundamentally bottlenecked by missing national infrastructure (e.g., lack of high-throughput sequencing network, missing genomic cloud pipelines). |
| **N/A** | External infrastructure is self-contained. |

---

#### 10. Manufacturing & Supply Chain
*Risks associated with specialized component manufacturers, CMOs, and industrial fabricators.*

| Risk Level | Operational Evaluation Criteria |
| :--- | :--- |
| **LOW RISK** | Robust, redundant ecosystem of certified contract manufacturers (CMOs) with ample spare capacity and rigorous ISO 13485 / CPOB compliance. |
| **MEDIUM RISK** | Limited number of qualified suppliers; single-source supplier dependencies for minor components; minor manufacturing lead-time bottlenecks. |
| **HIGH RISK** | Critical components can only be produced in-house on custom pilot lines; zero qualified commercial manufacturers exist globally or domestically. |
| **N/A** | Software-only solutions without physical supply chains. |

---

#### 11. Materials Sourcing
*Risks associated with availability, ethics, and geopolitical security of raw materials.*

| Risk Level | Operational Evaluation Criteria |
| :--- | :--- |
| **LOW RISK** | All raw materials, chemical precursors, and enzymes are commodity inputs available from multiple domestic and international suppliers at stable pricing. |
| **MEDIUM RISK** | Reliance on raw materials with moderate supply concentration or price volatility; alternative synthetic pathways exist but require validation. |
| **HIGH RISK** | Severe dependency on rare, embargoed, ethically fraught, or single-geography materials (e.g., rare earth metals, restricted proprietary primers). |
| **N/A** | Material inputs are negligible. |

---

#### 12. Workforce
*Risks associated with human capital, certified operators, and specialized technical talent.*

| Risk Level | Operational Evaluation Criteria |
| :--- | :--- |
| **LOW RISK** | Broad, readily accessible pool of certified operators, molecular biologists, and service engineers requiring standard on-the-job training. |
| **MEDIUM RISK** | Specialized talent required (e.g., clinical bioinformaticians); talent pool is small but growing through established university graduate pipelines. |
| **HIGH RISK** | Critical, systemic shortage of essential human capital; specialized skills cannot be hired or trained within reasonable project timeframes. |
| **N/A** | Workforce requirements are entirely automated. |

---

### Category D: License to Operate
*Focus: Evaluates non-economic, societal, legal, and environmental barriers to deployment.*

#### 13. Regulatory Environment
*Risks associated with securing marketing authorization, compliance certificates, and distribution permits.*

| Risk Level | Operational Evaluation Criteria |
| :--- | :--- |
| **LOW RISK** | Clear, transparent, highly standardized regulatory pathway (e.g., established Kemenkes Class B/C AKD permit or BPOM registered category); rapid review timelines. |
| **MEDIUM RISK** | Regulatory framework exists but review processes are bureaucratic and prone to procedural delays; requires dedicated regulatory consultants. |
| **HIGH RISK** | Novel technology lacks any existing regulatory category or standard (e.g., gene editing, autonomous AI diagnostics); requires novel legislation or multi-year agency reviews. |
| **N/A** | Products exempt from regulatory oversight. |

---

#### 14. Policy Environment
*Risks associated with government legislation, subsidies, and national procurement priorities.*

| Risk Level | Operational Evaluation Criteria |
| :--- | :--- |
| **LOW RISK** | Strong bipartisan policy alignment; product directly supported by national healthcare priorities (e.g., BGSi, TKDN mandates, e-Katalog preferences). |
| **MEDIUM RISK** | Dependent on temporary government subsidies or executive decrees that could expire or shift across political cycles. |
| **HIGH RISK** | Operates in direct conflict with existing government policies or faces adverse regulatory bans, high luxury taxes, or protective tariffs favoring incumbents. |
| **N/A** | Policy environment is completely neutral. |

---

#### 15. Permitting & Siting
*Risks associated with securing physical municipal, environmental, and building approvals.*

| Risk Level | Operational Evaluation Criteria |
| :--- | :--- |
| **LOW RISK** | Permitting and facility siting is standardized, well-understood, transparent, and rapidly repeatable across administrative jurisdictions. |
| **MEDIUM RISK** | Siting can be time-consuming, but jurisdictions and environmental review standards are clear; timeline accelerates with repeated applications. |
| **HIGH RISK** | Highly complex, contentious permitting involving multiple overlapping municipal, regional, and national agencies with conflicting jurisdictions. |
| **N/A** | Solution does not require physical facility construction. |

---

#### 16. Environmental & Safety
*Risks associated with hazardous side effects, toxicity, biohazard containment, or environmental degradation.*

| Risk Level | Operational Evaluation Criteria |
| :--- | :--- |
| **LOW RISK** | Inherently non-hazardous, non-toxic, and environmentally benign; zero biohazard waste or negative carbon footprint. |
| **MEDIUM RISK** | Moderate environmental or safety hazards (e.g., standard BSL-2 biological specimens or chemical solvents) that are fully controllable via standard SOPs. |
| **HIGH RISK** | Significant uncontrolled environmental degradation, dangerous pathogen exposure risk, high toxic emissions, or catastrophic clinical safety failure modes. |
| **N/A** | Environmental safety is non-applicable. |

---

#### 17. Community Perception
*Risks associated with public acceptance, consumer sentiment, and social license to operate.*

| Risk Level | Operational Evaluation Criteria |
| :--- | :--- |
| **LOW RISK** | Enthusiastically received by the general public, patients, and local communities; seen as an unalloyed public good. |
| **MEDIUM RISK** | Pockets of public skepticism or misunderstanding (e.g., data privacy concerns regarding DNA storage), but manageable through transparent education. |
| **HIGH RISK** | Fierce public backlash, active boycotts, or widespread ethical resistance (e.g., anti-GMO campaigns, perceived genetic discrimination) that threatens deployment. |
| **N/A** | Public perception has zero bearing on adoption. |

---

## CARAT Look-Up Matrix: Deriving the ARL Score (Slide 13)

The total number of **High Risk** dimensions and **Medium Risk** dimensions are cross-referenced in the official look-up table to determine the overall **Adoption Readiness Level (1–9)**:

| Count of Medium Risks $\downarrow$ / High Risks $ightarrow$ | **0 High** | **1 High** | **2 High** | **3 High** | **4 High** | **5 High** | **6 High** | **7 High** | **8+ High** |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **0 Medium** | **ARL 9** | **ARL 8** | **ARL 7** | **ARL 5** | **ARL 3** | **ARL 1** | **ARL 1** | **ARL 1** | **ARL 1** |
| **1 Medium** | **ARL 8** | **ARL 7** | **ARL 6** | **ARL 4** | **ARL 2** | **ARL 1** | **ARL 1** | **ARL 1** | **ARL 1** |
| **2 Medium** | **ARL 8** | **ARL 7** | **ARL 6** | **ARL 4** | **ARL 2** | **ARL 1** | **ARL 1** | **ARL 1** | **ARL 1** |
| **3 Medium** | **ARL 7** | **ARL 6** | **ARL 5** | **ARL 3** | **ARL 1** | **ARL 1** | **ARL 1** | **ARL 1** | **ARL 1** |
| **4 Medium** | **ARL 7** | **ARL 6** | **ARL 5** | **ARL 3** | **ARL 1** | **ARL 1** | **ARL 1** | **ARL 1** | **ARL 1** |
| **5 Medium** | **ARL 6** | **ARL 5** | **ARL 4** | **ARL 2** | **ARL 1** | **ARL 1** | **ARL 1** | **ARL 1** | **ARL 1** |
| **6 Medium** | **ARL 5** | **ARL 4** | **ARL 3** | **ARL 1** | **ARL 1** | **ARL 1** | **ARL 1** | **ARL 1** | **ARL 1** |
| **7 Medium** | **ARL 3** | **ARL 2** | **ARL 1** | **ARL 1** | **ARL 1** | **ARL 1** | **ARL 1** | **ARL 1** | **ARL 1** |
| **8+ Medium** | **ARL 1** | **ARL 1** | **ARL 1** | **ARL 1** | **ARL 1** | **ARL 1** | **ARL 1** | **ARL 1** | **ARL 1** |

### Readiness Tiers:
* **ARL 1 – 3 (Low Readiness):** Severe adoption barriers. Commercial liftoff cannot occur without fundamental structural, policy, or supply chain restructuring.
* **ARL 4 – 6 (Medium Readiness):** Transitional readiness. Commercial demonstration viable; active de-risking required on 2–4 critical bottlenecks.
* **ARL 7 – 9 (High Readiness):** Commercial Liftoff ready. Private capital and institutional customers can adopt and deploy with standard operational risk controls.

> **The Power-Law Principle of CARAT:** Notice that having **$\ge 5$ High Risk dimensions immediately drops the score to ARL 1**, regardless of how many Low Risk scores exist. In deep-tech commercialization, a single unmitigated fatal flaw (e.g., illegal under national regulations, or costing 10x incumbent price) completely halts private market adoption.

---

## Blank CARAT Audit Worksheet for GENOHACK Teams

```markdown
TEAM NAME: ____________________________ TRACK: [ ] 1  [ ] 2  [ ] 3
TECHNOLOGY / PRODUCT NAME: _________________________________________________
EVALUATION SCOPE: _________________________________________________________
DATE OF ASSESSMENT: ___________________ EVALUATOR(S): ______________________

---------------------------------------------------------------------------
DIMENSION                                | SCORE (L / M / H / NA) | RATIONALE / EVIDENCE
---------------------------------------------------------------------------
CATEGORY A: VALUE PROPOSITION
1. Delivered Cost                        | [      ]               | ____________________
2. Functional Performance                | [      ]               | ____________________
3. Ease of Use / Complexity              | [      ]               | ____________________

CATEGORY B: MARKET ACCEPTANCE
4. Demand Maturity / Market Openness     | [      ]               | ____________________
5. Market Size                           | [      ]               | ____________________
6. Downstream Value Chain                | [      ]               | ____________________

CATEGORY C: RESOURCE MATURITY
7. Capital Flow                          | [      ]               | ____________________
8. Project Development & Management      | [      ]               | ____________________
9. Infrastructure                        | [      ]               | ____________________
10. Manufacturing & Supply Chain         | [      ]               | ____________________
11. Materials Sourcing                   | [      ]               | ____________________
12. Workforce                            | [      ]               | ____________________

CATEGORY D: LICENSE TO OPERATE
13. Regulatory Environment               | [      ]               | ____________________
14. Policy Environment                   | [      ]               | ____________________
15. Permitting & Siting                  | [      ]               | ____________________
16. Environmental & Safety               | [      ]               | ____________________
17. Community Perception                 | [      ]               | ____________________
---------------------------------------------------------------------------

TOTAL TALLIES:
- Low Risk Dimensions:    ______
- Medium Risk Dimensions: ______
- High Risk Dimensions:   ______

COMPOSITE ARL SCORE (From Look-Up Table): ARL [ ______ ]
READINESS CLASSIFICATION: [ ] Low (1-3)  [ ] Medium (4-6)  [ ] High (7-9)

TOP 3 ADOPTION BOTTLENECK ACTIONS FOR NEXT 90 DAYS:
1. ________________________________________________________________________
2. ________________________________________________________________________
3. ________________________________________________________________________
```
