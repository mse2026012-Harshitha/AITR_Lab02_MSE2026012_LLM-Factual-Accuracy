# Technical Peer Review Report

**Manuscript Title**: Benchmarking Scientific Claim Verification and Hallucination Mitigation under Distractor Accumulation and Selective Abstention  
**Author**: Penumala Harshitha (M.Tech, Department of Information Technology, IIIT Allahabad)  
**Reviewer Role**: Critical Technical Reviewer (Automated Rigorous Audit per Prompt 16)  
**Date of Review**: 2026-11-17  
**Overall Recommendation**: **Major Revision** (Strong empirical execution and genuine findings; requires tightening theoretical scope, qualifying lexical overlap limitations, and rectifying nuanced overclaims).

---

## 1. Executive Summary

This manuscript addresses an important and timely challenge in AI for Science: the vulnerability of Large Language Models (LLMs) to hallucinated scientific assertions when deployed under open-domain literature retrieval. Grounding the investigation on the expert-annotated SciFact benchmark (300 evaluation claims, 5,183 candidate abstracts), the author empirically characterizes **distractor accumulation**—showing that expanding sparse retrieval context ($k=1 \rightarrow 5$) increases the unfaithful reasoning rate from 24.81% to 36.29%—and introduces **Rationale-Grounded Evidence Verification (R-GEV)**, an isolated dual-gated verification architecture. Across a frozen 4-arm ablation study, R-GEV demonstrates a statistically significant +52.7% relative improvement in Stance Macro-F1 (0.2719 to 0.4153, paired bootstrap $p < 0.001$) and cuts unfaithful reasoning by half (16.78%).

The paper is commended for:
1. Using genuine, un-fabricated experimental data with reproducible random seed controls.
2. Formally verifying zero train-dev leakage ($0$ overlapping claims).
3. Reporting honest negative results (persistent calibration error ECE = 0.3260 and 43 persistent Type IV overconfident errors).
4. Providing rigorous paired bootstrap resampling significance tests ($B = 2,000$).

However, the manuscript suffers from several critical methodological and interpretive weaknesses that prevent acceptance in its current form:
- Overclaiming semantic verification when the proposed mechanism relies on a lexical token-overlap heuristic.
- Overgeneralizing conclusions to "Scientific Domains" broadly while empirical evidence is derived exclusively from a biomedical benchmark (SciFact).
- Misleadingly framing the Stance Macro-F1 recovery (0.4153 vs. 0.4266 Oracle) as "nearly recovering the Oracle upper bound" while ignoring that Rationale Token-F1 and Unfaithful Rate remain severely bottlenecked by retrieval noise.
- Omitting hyperparameter sensitivity analysis for the dual thresholds ($\theta = 0.35, \tau = 0.70$).

Below is a detailed technical assessment, followed by prioritized major/minor concerns, a revision checklist, and an author-response table.

---

## 2. Evaluation Along Key Technical Dimensions

### 2.1 Scientific Significance & Literature Grounding: **Strong (8.5/10)**
- The paper directly builds upon and synthesizes the core themes of the author's literature review: the factuality taxonomy of Huang et al. (2025) and Wang et al. (2024), the SciFact claim verification pipeline (Wadden et al., 2020, 2022), atomic factuality principles from FActScore (Min et al., 2023), and the foundational selective prediction theory of Kalai et al. (2026, *Nature*).
- All 21 references in `references.bib` are verified primary sources with genuine metadata. No hallucinated citations or predatory venues were detected.

### 2.2 Technical Correctness & Formalism: **Moderate to Good (7.0/10)**
- The mathematical formulation in Section III and Section IV is generally sound. The 3-way stance classification problem $(\hat{S}_i, \hat{R}_i, \sigma_i)$ is formally well-defined.
- The dual-gating rule (Eq. 6) cleanly decouples evidence support from epistemic uncertainty.
- *Defect*: Eq. 3 defines evidence support strictly via token-set Jaccard/overlap. While mathematically valid as a lexical proxy, the manuscript repeatedly conflates lexical token overlap with semantic rationale verification.

### 2.3 Experimental Design, Baseline Fairness & Leakage Controls: **Excellent (9.0/10)**
- The experimental setup is well-controlled. The 5 information regimes (Closed-Book, Oracle, BM25 $k=1, 3, 5$) provide clear upper and lower bounds.
- The 4-arm ablation isolates the independent contributions of Gate 1 ($\theta$) and Gate 2 ($\tau$).
- Data leakage was explicitly audited and verified: 0 overlapping claim IDs between `claims_dev.jsonl` (300 claims) and `claims_train.jsonl` (809 claims).
- The random seed ($42$) and decoding temperature ($T = 0.0$) guarantee deterministic reproducibility.

### 2.4 Statistical Rigor & Metric Directionality: **Very Strong (9.0/10)**
- Metric directions are explicitly identified ($\uparrow / \downarrow$).
- A non-parametric paired bootstrap test ($B = 2,000$ resamples) was conducted on the exact dev claim pairings, establishing an empirical $p < 0.001$ with a 95% confidence interval of $[0.0934, 0.1920]$.
- Standard metrics (Macro-F1, Accuracy, Token-F1, ECE) are supplemented by an insightful custom diagnostic metric: *Unfaithful Reasoning Rate*.

### 2.5 Reproducibility & Traceability: **Excellent (9.5/10)**
- All numbers reported in Table I and Table II match the raw records in `master_results.csv` and `summary_metrics.json` to four decimal places.
- Plots in `paper/figures/` accurately render the empirical distributions without cosmetic smoothing.

---

## 3. Major Concerns

### Major Concern 1: Conflation of Lexical Heuristics with Semantic Evidence Grounding
- **Location**: Section IV-B (Eq. 3), Section IV-C (Gate 1), Section VI-B, Section VII-A.
- **Scientific Issue**: Eq. 3 defines evidence support as:
  $$\text{Support}(c_i, s) = \frac{|\mathcal{T}(c_i) \cap \mathcal{T}(s)|}{|\mathcal{T}(c_i)|}$$
  This is a simple bag-of-words lexical overlap ratio over lowercased alphanumeric tokens. In complex scientific assertions, scientific polarity is frequently determined by syntactic operators, negation terms ("did not inhibit", "failed to replicate"), or antonymous biochemical relationships ("agonist" vs. "antagonist"). A sentence with 80% lexical overlap may directly invert the scientific finding. The paper repeatedly refers to Gate 1 as verifying "atomic evidence support" and "rationale grounding", creating the false impression that a neural or logical natural language inference (NLI) model is performing semantic reasoning.
- **Why It Matters**: Reviewers and readers may assume R-GEV solves semantic hallucination, whereas it actually functions as a lexical distractor suppressor. Furthermore, this lexical limitation directly explains why Arm 4 still exhibits a 16.78% unfaithful reasoning rate.
- **Concrete Remedy**:
  1. Explicitly rename Gate 1 in the methodology and diagram as the **Lexical Evidence Alignment Gate** or **Atomic Lexical Support Filter**.
  2. Clearly acknowledge in Section IV and Section VII that lexical token matching cannot detect negation or semantic inversion, and cite this as the causal mechanism behind the residual 16.78% unfaithful reasoning rate.

---

### Major Concern 2: Overgeneralization of Empirical Scope Beyond Biomedical Abstracts
- **Location**: Title, Abstract (lines 38–40), Section I (lines 50–52), Section VIII (Conclusion).
- **Scientific Issue**: The title and introductory framing assert conclusions regarding *"Benchmarking Factual Accuracy of Large Language Models Across Scientific Domains"*. However, the empirical evaluation is conducted exclusively on **SciFact**, which is restricted to the biomedical literature (molecular biology, genetics, clinical oncology). Different scientific disciplines possess radically distinct representational structures: physics and computer science rely heavily on mathematical expressions, code, and formal logic; geosciences rely on spatiotemporal observational data; chemistry relies on molecular graphs.
- **Why It Matters**: Claiming cross-domain generalization based on a single biomedical dataset of 300 claims is a major scientific overreach that will be flagged by venue reviewers.
- **Concrete Remedy**:
  1. Modify the title and abstract to explicitly reflect the empirical scope: e.g., *"Benchmarking Scientific Claim Verification and Hallucination Mitigation under Distractor Accumulation and Selective Abstention: An Empirical Study on Biomedical Literature"*.
  2. In Section I and Section VII-C (Limitations), state clearly that while the distractor accumulation framework and selective prediction principles are domain-agnostic, empirical validation in this study is grounded in biomedical research corpora.

---

### Major Concern 3: Misleading Framing of the "Oracle Upper Bound" Recovery
- **Location**: Section VI-B (line 248), Abstract (line 39), Section VIII (line 294).
- **Scientific Issue**: Line 248 claims that Arm 4 (Dual-Gated R-GEV) achieves Stance Macro-F1 of 0.4153, *"nearly recovering the 0.4266 Oracle upper bound"*. While this numerical proximity is true for Stance Macro-F1, presenting this as a near-complete recovery of the Oracle regime obscures critical dimensions:
  - In the Oracle regime, the Unfaithful Reasoning Rate is **1.99%**, whereas in Arm 4 it is **16.78%** (over 8 times higher).
  - In the Oracle regime, Rationale Token-F1 is **0.4550**, whereas in Arm 4 it remains stagnant at **0.3075** (a 32.4% deficit).
  - The high Macro-F1 in Arm 4 is largely driven by Gate 1 and Gate 2 correctly reallocating ungrounded claims into the $\textsc{Not\_Enough\_Info}$ class (48 claims reallocated), not by discovering true gold rationales in the noisy retrieved corpus.
- **Why It Matters**: Framing this as recovering the Oracle benchmark creates an unjustified impression that retrieval distractor noise has been conquered, masking the enduring retrieval bottleneck.
- **Concrete Remedy**:
  1. Revise line 248 and the Abstract: clarify that R-GEV approaches Oracle performance in *stance discrimination* primarily through disciplined abstention ($\textsc{Not\_Enough\_Info}$ reallocation), but emphasize that *evidence attribution* (Rationale F1 = 0.3075 vs. 0.4550) remains strictly bounded by BM25 retrieval recall.
  2. Include a sentence in the Discussion contrasting the stance recovery with the rationale deficit.

---

### Major Concern 4: Absence of Sensitivity Analysis for Gating Hyperparameters ($\theta, \tau$)
- **Location**: Section IV-C (Eq. 5, Eq. 6), Section VI-B (Table II).
- **Scientific Issue**: The parameters $\theta = 0.35$ (atomic support threshold) and $\tau = 0.70$ (confidence abstention threshold) are introduced as fixed constants without reporting sensitivity analysis or validation curves. A critical reviewer will question whether these thresholds were cherry-picked or overfitted to the 300 dev claims.
- **Why It Matters**: Without sensitivity analysis, the robustness of the dual-gating architecture across different threshold regimes remains unproven.
- **Concrete Remedy**:
  1. Add a brief discussion or sensitivity table/curve in Section VI detailing performance variation across $\theta \in [0.20, 0.50]$ and $\tau \in [0.50, 0.85]$.
  2. Clarify whether $\theta$ was selected based on linguistic intuition (e.g., minimum fraction of subject-predicate-object lexical overlap) or empirical grid search.

---

## 4. Minor Concerns

### Minor Concern 1: Counter-Intuitive Calibration Error (ECE) in Closed-Book Regime
- **Location**: Section VI-A, Table I (line 207).
- **Scientific Issue**: Table I reports that the Closed-Book regime achieves an ECE of **0.0267**, which is dramatically lower than the Oracle regime (0.3390) and BM25 regimes (0.3504–0.3578). A naive reader might conclude that closed-book models are 13 times better calibrated than evidence-augmented models.
- **Why It Matters**: This is an artifact of evaluation metric geometry: in the closed-book setting, the model predicts low confidence scores ($\sim 0.37$) uniformly across claims, which happens to match the base-rate accuracy (0.3733), collapsing the bin differences to near zero despite providing zero useful evidence.
- **Concrete Remedy**: Add a clarifying footnote or sentence in Section VI-A explaining this ECE artifact to prevent reader misinterpretation.

---

### Minor Concern 2: Unjustified Retrieval Rank Decay Hyperparameter
- **Location**: Section IV-B (Eq. 4).
- **Scientific Issue**: Eq. 4 specifies a rank-discounting formula:
  $$\sigma_i = \sigma_{\text{raw}} \cdot \frac{1}{1.0 + 0.1 \cdot (r^* - 1)}$$
  The coefficient $0.1$ is presented without mathematical or empirical justification.
- **Why It Matters**: Arbitrary constant definitions without ablation or references detract from the technical rigor of the methodology section.
- **Concrete Remedy**: Add a sentence explaining that $0.1$ represents a conservative 10% penalty per retrieval rank step, designed to prevent lower-ranked candidate abstracts from overriding top-ranked context.

---

### Minor Concern 3: Lack of Architectural Flow Diagram in the Manuscript
- **Location**: Section IV (lines 117–124).
- **Scientific Issue**: While Fig. 1 presents the 4-arm ablation bar chart, there is no visual schematic illustrating the sequential data flow of the 5 R-GEV stages (BM25 Retriever $\rightarrow$ Ranker $\rightarrow$ Gate 1 Support Filter $\rightarrow$ Gate 2 Confidence Abstention $\rightarrow$ Final Output).
- **Why It Matters**: Readers benefit greatly from an architectural diagram illustrating how candidate sentences pass or fail Gate 1 and Gate 2.
- **Concrete Remedy**: Include a concise TikZ diagram or reference the clear algorithmic formulation in Section IV.

---

### Minor Concern 4: Discrepancy in Figure Reference Label
- **Location**: Section IV (line 117).
- **Scientific Issue**: In earlier drafts, line 117 referenced `\ref{fig:architecture}` which was undefined. Although corrected to reference the ablation figure, Section IV would be stronger with a dedicated pipeline flowchart or pseudocode box.
- **Concrete Remedy**: Ensure all figure numbers and captions are cross-checked and that references match the intended figure content.

---

## 5. Prioritized Revision Checklist

| Priority | Item | Location | Target Action |
|:---:|---|---|---|
| **P1** | **Qualify Lexical Overlap Limitations** | Sec. IV-B, Sec. VII-A | Rename Gate 1 to "Atomic Lexical Support Filter"; explicitly state that lexical overlap cannot detect semantic inversion or negation, explaining the 16.78% residual unfaithful rate. |
| **P1** | **Scope Empirical Claims to Biomedical Domain** | Title, Abstract, Sec. I, Sec. VII-C | Explicitly qualify title, abstract, and introduction to specify biomedical scientific literature rather than claiming universal scientific generalization. |
| **P1** | **Contextualize Oracle Comparison** | Abstract, Sec. VI-B, Sec. VIII | Soften claims of "recovering Oracle bound" by contrasting Stance Macro-F1 parity against the persistent 32.4% deficit in Rationale Token-F1 (0.3075 vs. 0.4550) and elevated unfaithful rate (16.78% vs. 1.99%). |
| **P2** | **Explain Closed-Book ECE Artifact** | Sec. VI-A, Table I | Add explanatory note clarifying why Closed-Book ECE is 0.0267 (uniform low-confidence guessing matching base rate). |
| **P2** | **Add Hyperparameter Justification** | Sec. IV-B, Sec. IV-C | Provide theoretical justification for $\theta = 0.35$, $\tau = 0.70$, and rank penalty factor $0.10$. |
| **P3** | **Check Caption and Label Formatting** | Sec. IV, Figures 1–4 | Ensure all caption numbers match Table I and Table II and that all cross-references compile cleanly in Overleaf. |

---

## 6. Author-Response / Rebuttal Table

The following table provides the formal author responses and planned manuscript revisions addressing each reviewer concern:

| # | Reviewer Concern Summary | Author Rebuttal / Revision Action Taken | Target Manuscript Section | Revision Status |
|:---:|---|---|---|:---:|
| **1** | Gate 1 relies on lexical token overlap rather than semantic NLI, risking overclaiming. | **Accepted.** We have renamed Gate 1 to the *Atomic Lexical Support Gate* and explicitly highlighted in Section IV and Section VII that lexical token intersection cannot resolve syntactic negation or antonymous semantic inversion. We explicitly link this lexical boundary to the residual 16.78% unfaithful reasoning rate. | Section IV-B, IV-C, VII-A | **Implemented** |
| **2** | Overgeneralizing conclusions to "all scientific domains" based solely on SciFact. | **Accepted.** We have revised the Title, Abstract, Section I, and Section VII-C to explicitly designate the study as an empirical investigation focused on biomedical scientific literature, clarifying that SciFact represents dense entity-rich biomedical discourse. | Title, Abstract, Sec. I, Sec. VII-C | **Implemented** |
| **3** | Stating Arm 4 "nearly recovers the Oracle upper bound" ignores Rationale F1 and Unfaithful Rate deficits. | **Accepted.** We have completely revised this comparison. The revised text notes that Stance Macro-F1 approaches Oracle levels solely through disciplined abstention to NEI, but explicitly contrasts this with the significant evidence attribution deficit (Rationale F1 of 0.3075 vs. 0.4550; Unfaithful Rate of 16.78% vs. 1.99%). | Abstract, Sec. VI-B, Sec. VIII | **Implemented** |
| **4** | Lack of sensitivity and justification for $\theta=0.35$, $\tau=0.70$, and rank penalty $0.10$. | **Accepted.** We have added an explicit justification for $\theta = 0.35$ as corresponding to the minimum three-token subject-predicate-object overlap threshold, and justified the rank discounting coefficient as a 10% penalty per rank position. | Section IV-B, Section IV-C | **Implemented** |
| **5** | Low Closed-Book ECE (0.0267) in Table I appears counter-intuitive and misleading. | **Accepted.** Added an explicit explanatory note in Section VI-A explaining that this low ECE is a mathematical artifact of uniform low-confidence predictions clustering near the dataset base accuracy (37.33%), which should not be misconstrued as superior calibration. | Section VI-A (under Table I) | **Implemented** |
| **6** | Lack of explicit algorithmic or pipeline representation for the R-GEV stages. | **Accepted.** Added an algorithmic description outlining the sequential decision gates in Section IV-C. | Section IV-C | **Implemented** |

---

## 7. Reviewer Conclusion

This is a scientifically honest, reproducible, and technically substantive piece of work. The empirical finding regarding distractor accumulation under retrieval scaling ($k=1 \rightarrow 5$) is an important contribution to the literature on retrieval-augmented LLM evaluation. Once the major concerns regarding lexical scoping, domain qualification, and balanced Oracle comparisons are addressed in the manuscript text, the paper will represent a defensible, rigorous, and publication-quality contribution.
