# Manuscript Section Outline and Evidence Checklist (Prompt 15)

**Paper Title**: Benchmarking Scientific Claim Verification and Hallucination Mitigation under Distractor Accumulation and Selective Abstention  
**Target Venue / Style**: IEEE Transactions / ACM Conference Style (6–10 pages)  
**Author**: Penumala Harshitha (M.Tech, Department of Information Technology, IIIT Allahabad)  
**Date**: 2026-11-17  

---

## 1. Section Outline

* **Title, Authors, Affiliation**
* **Abstract**: Synthesized last to match exact empirical evidence.
* **1. Introduction**:
  * The challenge of factuality in scientific NLP (fluency $\neq$ accuracy).
  * The open-domain retrieval gap and distractor interference.
  * The hallucination incentive under forced-choice evaluation (Kalai et al., 2026).
  * Our core contributions: (1) Empirical characterization of distractor degradation on SciFact, (2) Proposed R-GEV dual-gating architecture, (3) Formal statistical validation.
* **2. Related Work**:
  * Scientific Factuality & Hallucination Taxonomy (Huang et al., 2025; Wang et al., 2024).
  * Scientific Reasoning and Claim Benchmarks (SciFact, SciFact-Open, PubMedQA, GPQA, MMLU).
  * Atomic Factuality & Verification Prompting (FActScore, CoVe, SelfCheckGPT).
  * Selective Classification and Conformal Calibration (Kalai et al., 2026).
* **3. Problem Formulation & Research Questions**:
  * Mathematical definition of scientific claim verification (3-way stance + rationale extraction).
  * Formal statement of RQ1 (Retrieval Noise), RQ2 (Abstention), and RQ3 (Rationale Faithfulness).
* **4. Methodology: The R-GEV Framework**:
  * Corpus Indexing & Sparse Retrieval (BM25 Okapi formulation).
  * Evidence-Conditioned Prompting and Parsing.
  * Atomic Rationale Support Gating ($\theta$-thresholding).
  * Confidence Calibration and Selective Abstention ($\tau$-thresholding).
  * Dual-Gated Decision Rule.
* **5. Experimental Setup**:
  * Benchmark Dataset: SciFact dev split (300 claims) and corpus (5,183 abstracts).
  * Evaluation Metrics: Stance Macro-F1, Accuracy, Rationale Token-F1, Unfaithful Reasoning Rate, ECE.
  * Reproducibility & Integrity Controls: Random seed 42, greedy decoding $T=0.0$, 0% train-dev leakage.
* **6. Experimental Results & Ablation Analysis**:
  * Cross-Regime Baseline Performance (Closed-Book vs. Oracle vs. BM25 $k=1, 3, 5$).
  * The 4-Arm Ablation Study (Baseline, Conf-Only, Rationale-Only, Dual R-GEV).
  * Paired Bootstrap Statistical Significance Testing ($B=2,000, p < 0.001$).
  * Selective Prediction Risk-Coverage Curves.
* **7. Discussion & Limitations**:
  * Distractor interference mechanisms and rationale faithfulness.
  * Honest negative findings: Persistent calibration error (ECE = 0.3260).
  * Methodological limitations.
  * Three prioritized future directions.
* **8. Conclusion**:
  * Summary of scientific takeaways.
* **References**: 21 verified citations from literature review.

---

## 2. Evidence Mapping Checklist

| Paper Claim / Section | Required Evidence Source | Verification Status | Artifact Location |
|---|---|:---:|---|
| Dev set size and partition | SciFact `claims_dev.jsonl` (300 claims) | `[VERIFIED]` | `data/claims_dev.jsonl` |
| Corpus size | SciFact `corpus.jsonl` (5,183 abstracts) | `[VERIFIED]` | `data/corpus.jsonl` |
| Retrieval recall drop | R@1=52.33%, R@3=69.33%, R@5=75.67% | `[VERIFIED]` | `results/summary_metrics.json` |
| Oracle Stance Macro-F1 | 0.4266 (Accuracy: 0.5033, Unfaithful: 1.99%) | `[VERIFIED]` | `results/comparative_results.csv` |
| BM25 k=3 Baseline Macro-F1 | 0.2719 (Accuracy: 0.4133, Unfaithful: 33.06%) | `[VERIFIED]` | `results/ablation_results.csv` |
| BM25 k=5 Unfaithful Rate | 36.29% (Distractor accumulation surge) | `[VERIFIED]` | `results/comparative_results.csv` |
| Arm 2 Conf-Only Macro-F1 | 0.3443 (Accuracy: 0.4333, Unfaithful: 20.00%) | `[VERIFIED]` | `results/ablation_results.csv` |
| Arm 3 Rationale-Only Macro-F1 | 0.4054 (Accuracy: 0.4900, Unfaithful: 25.85%) | `[VERIFIED]` | `results/ablation_results.csv` |
| Arm 4 Dual R-GEV Macro-F1 | 0.4153 (Accuracy: 0.4967, Unfaithful: 16.78%) | `[VERIFIED]` | `results/ablation_results.csv` |
| Paired Bootstrap p-value | $p < 0.001$ ($p = 0.00000$, 95% CI: $[0.0934, 0.1920]$) | `[VERIFIED]` | `results/statistical_test_report.json` |
| Selective Accuracy Gain | 41.14% @ 99.7% coverage $\rightarrow$ 58.65% @ 34.7% coverage | `[VERIFIED]` | `results/summary_metrics.json` |
| Calibration ECE | ECE = 0.3260 (Reported as negative finding / limitation) | `[VERIFIED]` | `results/results_and_discussion.md` |
| 0% Train-Dev Leakage | 0 overlapping claim IDs verified programmatically | `[VERIFIED]` | `scripts/evaluate_results.py` log |
