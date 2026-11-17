# Evidence-Based Results and Discussion Outline (Prompt 14)

**Project**: Benchmarking Factual Accuracy of Large Language Models Across Scientific Domains  
**Author**: Penumala Harshitha (M.Tech, IIIT Allahabad)  
**Dataset**: SciFact (`claims_dev.jsonl`, N=300 claims; `corpus.jsonl`, 5,183 abstracts)  
**Evaluated Systems**: Baseline vs. Dual-Gated R-GEV (4-Arm Ablation Study)  
**Date**: 2026-11-17  
**Gate Status**: Milestone Gate G3 Satisfied

---

## 1. Summary of Genuine Experimental Findings

| Experimental Arm | Stance Macro-F1 | Stance Accuracy | Rationale Token-F1 | Unfaithful Reasoning Rate (%) | ECE |
|---|:---:|:---:|:---:|:---:|:---:|
| **Arm 1: Unmodified Baseline (Control)** | 0.2719 | 0.4133 | 0.3075 | 33.06% | 0.3578 |
| **Arm 2: Confidence Only ($\tau = 0.70$)** | 0.3443 | 0.4333 | 0.3075 | 20.00% | 0.3378 |
| **Arm 3: Rationale Gating Only ($\theta = 0.35$)** | 0.4054 | 0.4900 | 0.3075 | 25.85% | 0.3327 |
| **Arm 4: Proposed Dual-Gated R-GEV** | **0.4153** | **0.4967** | **0.3075** | **16.78%** | **0.3260** |

*Artifacts*:
* Results CSV: [results/ablation_results.csv](file:///c:/Users/Admin/Desktop/ATR-IMPLEMENTATION/results/ablation_results.csv)
* Master CSV: [results/master_results.csv](file:///c:/Users/Admin/Desktop/ATR-IMPLEMENTATION/results/master_results.csv)
* Full JSON Metrics: [results/ablation_metrics.json](file:///c:/Users/Admin/Desktop/ATR-IMPLEMENTATION/results/ablation_metrics.json)
* Statistical Report: [results/statistical_test_report.json](file:///c:/Users/Admin/Desktop/ATR-IMPLEMENTATION/results/statistical_test_report.json)
* Figures:
  - Figure 1: [results/fig1_ablation_comparison.png](file:///c:/Users/Admin/Desktop/ATR-IMPLEMENTATION/results/fig1_ablation_comparison.png) | [PDF](file:///c:/Users/Admin/Desktop/ATR-IMPLEMENTATION/results/fig1_ablation_comparison.pdf)
  - Figure 2: [results/fig2_unfaithful_suppression.png](file:///c:/Users/Admin/Desktop/ATR-IMPLEMENTATION/results/fig2_unfaithful_suppression.png) | [PDF](file:///c:/Users/Admin/Desktop/ATR-IMPLEMENTATION/results/fig2_unfaithful_suppression.pdf)
  - Figure 3: [results/fig3_risk_coverage_curve.png](file:///c:/Users/Admin/Desktop/ATR-IMPLEMENTATION/results/fig3_risk_coverage_curve.png) | [PDF](file:///c:/Users/Admin/Desktop/ATR-IMPLEMENTATION/results/fig3_risk_coverage_curve.pdf)
  - Figure 4: [results/fig4_confusion_matrices.png](file:///c:/Users/Admin/Desktop/ATR-IMPLEMENTATION/results/fig4_confusion_matrices.png) | [PDF](file:///c:/Users/Admin/Desktop/ATR-IMPLEMENTATION/results/fig4_confusion_matrices.pdf)

---

## 2. Resource Efficiency and Stability Analysis

| Dimension | Measured Parameter | Analysis & Assessment |
|---|---|---|
| **Computational Runtime** | ~14.5 seconds for 300 claims | Entire pipeline (BM25 retrieval + R-GEV gating + evaluation) executes in under 15 seconds on local host CPU. |
| **Peak RAM Usage** | < 250 MB | Inverted BM25 index over 5,183 abstracts and evaluation data structure requires negligible memory footprint. |
| **Cross-Run Stability** | 0.00% variance ($\sigma = 0.0$) | Strict greedy decoding ($T = 0.0$) and seed control ($42$) yields 100% deterministic reproducibility across runs. |
| **Error Taxonomy Breakdown (Arm 4)** | Type II: 54, Type III: 25, Type IV: 43 | Type III unfaithful reasoning errors slashed by half; Type II stance flips reduced from 65 to 54. |

---

## 2. In-Depth Analysis of Research Questions

### RQ1: Retrieval Noise Degradation & Distractor Interference
* **Direct Observations**:
  * Shifting from Oracle evidence to BM25 retrieved abstracts drops Macro-F1 from **0.4266 to 0.2719** (a relative decline of 36.3%).
  * Expanding retrieval depth from $k=1$ to $k=5$ increases distractor exposure, causing unfaithful reasoning to surge from **24.81% to 36.29%**.
* **Underlying Mechanism**: Sparse BM25 retrieval matches general biomedical terminology (e.g., protein names, cell types), but does not guarantee the retrieved abstract addresses the specific experimental condition or polar relationship asserted in the claim. The baseline classifier attempts to find the closest sentence, latching onto distractor sentences that share vocabulary but lack evidential relevance.
* **Alternative Explanations**: Could the performance drop be due to vocabulary mismatch rather than distractor interference? No: BM25 Recall@3 is 69.33%, meaning the true abstract is present in the majority of cases, yet the model is distracted by irrelevant higher-ranked candidate text.
* **Unsupported Claims to Avoid**: We cannot claim that retrieval noise causes complete model failure; accuracy remains above majority-class guessing (41.33% vs 37.33%).

---

### RQ2: Selective Prediction & Abstention (Kalai et al., 2026 Hypothesis)
* **Direct Observations**:
  * In the unconstrained baseline (Arm 1), the model almost never abstained: `NOT_ENOUGH_INFO` recall was **0.0089** (only 1 out of 112 claims).
  * Introducing confidence thresholding (Arm 2) improved Macro-F1 from **0.2719 to 0.3443**.
  * Combining confidence thresholding with atomic rationale gating (Arm 4) increased `NOT_ENOUGH_INFO` recall to **0.4286**, boosting Macro-F1 to **0.4153**.
  * In selective prediction, claims with confidence $\sigma \ge 0.80$ achieved **58.65% accuracy**, and claims with $\sigma \ge 0.90$ reached **66.67% accuracy**.
* **Underlying Mechanism**: Confirming Kalai et al. (2026), forced-choice accuracy maximization compels language systems to guess when evidence is weak or absent. Providing an explicit abstention path eliminates high-risk hallucinations on unsupported scientific queries.
* **Limitations**: The model still suffers from residual overconfidence on 43 claims (Type IV errors), indicating that verbalized confidence scores alone do not achieve perfect calibration (ECE = 0.3260).

---

### RQ3: Rationale Faithfulness vs. Stance Correctness
* **Direct Observations**:
  * In Arm 1, 33.06% of correct stance predictions were unfaithful (the model output the right stance but selected a sentence with zero token overlap to gold evidence).
  * Gating predictions via R-GEV (Arm 4) slashed the unfaithful reasoning rate by **49.2%** (down to **16.78%**).
* **Underlying Mechanism**: R-GEV enforces an atomic evidence threshold ($\theta = 0.35$). If no candidate sentence provides sufficient lexical and semantic overlap with the claim, the system rejects the candidate rationale and abstains, preventing "right answers for the wrong reasons."
* **Unsupported Claims to Avoid**: We do not claim that R-GEV guarantees 100% semantic faithfulness; ~16.8% of claims remain unfaithful due to superficial lexical overlap between claims and unrelated sentences.

---

## 3. Supported, Contradicted, and Unresolved Hypotheses

| Hypothesis | Status | Empirical Grounding |
|---|:---:|---|
| **H1: Open-domain retrieval noise degrades scientific stance classification and rationale quality.** | **SUPPORTED** | Macro-F1 drops from 0.4266 to 0.2719; unfaithful reasoning surges to 36.29% at $k=5$. |
| **H2: Enforcing an atomic rationale support threshold suppresses unfaithful reasoning.** | **SUPPORTED** | Arm 3 and Arm 4 reduce unfaithful reasoning from 33.06% to 16.78%. |
| **H3: Confidence-based abstention (selective prediction) improves factual precision on answered claims.** | **SUPPORTED** | Selective accuracy rises from 41.14% at full coverage to 58.65% at 34.7% coverage ($\tau=0.80$). |
| **H4: Rationale gating alone achieves perfect calibration (ECE < 0.10).** | **CONTRADICTED** | ECE improved modestly (0.3578 $\rightarrow$ 0.3260), but remained far from zero due to verbalized confidence bias. |
| **H5: Cross-encoder re-ranking eliminates all Type I retrieval errors.** | **UNRESOLVED** | Unresolved because our study evaluated BM25 sparse retrieval; testing neural cross-encoders remains future work. |

---

## 4. Methodological Limitations

1. **Domain Focus**: Evaluated exclusively on the SciFact benchmark (biomedical and life sciences). Transferability to formal sciences (mathematics, theoretical CS) requires separate empirical validation.
2. **Lexical Rationale Approximation**: Sentence-level support is computed via token overlap and negation alignment. While transparent and reproducible without GPU overhead, it does not capture complex multi-sentence clinical syllogisms.
3. **Corpus Size**: The SciFact corpus contains 5,183 abstracts. While realistic for targeted literature review benchmarks, massive open-web corpora (e.g., millions of PubMed papers) will present even higher distractor density.

---

## 5. Three High-Value Follow-Up Experiments (Ranked by Cost & Value)

1. **Rank 1 (Low Cost / High Value)**: *Cross-Encoder Neural Re-ranking*. Integrate a compact cross-encoder (e.g., `cross-encoder/ms-marco-MiniLM-L-6-v2`) to re-rank top-10 BM25 abstracts prior to R-GEV gating, testing whether neural re-ranking further cuts Type I retrieval failures.
2. **Rank 2 (Low Cost / High Value)**: *Logit-Margin Calibration vs. Verbalized Confidence*. Compare verbalized confidence thresholds against normalized output logit margins to systematically lower the Expected Calibration Error (ECE).
3. **Rank 3 (Moderate Cost / High Value)**: *Instruction-Tuned LLM Scaling*. Run the identical 4-arm protocol using an open 8B LLM (e.g., `Llama-3.1-8B-Instruct` or `Qwen2.5-7B-Instruct`) via Google Colab T4 GPU to evaluate whether larger parametric models amplify or mitigate distractor interference.
