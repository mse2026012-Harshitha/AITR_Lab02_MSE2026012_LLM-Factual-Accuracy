# Contribution Pathway Analysis & Scientific Defense (Prompt 12)

**Author**: Penumala Harshitha (M.Tech, IIIT Allahabad)  
**Project**: Benchmarking Factual Accuracy of Large Language Models Across Scientific Domains  
**Primary Baseline Reference**: Wadden et al. (2020, EMNLP); Kalai et al. (2026, Nature); Dhuliawala et al. (2023); Min et al. (2023)  
**Date**: 2026-11-17  
**Status**: PROPOSAL & COMPARATIVE ANALYSIS (Pre-Implementation)

---

## 1. Context and Grounding from Validated Baseline Results

Our empirical baseline validation across the 300 SciFact dev claims revealed three verified phenomena:
1. `[VERIFIED]` **Open-Domain Degradation (RQ1)**: Stance Macro-F1 drops from **0.4266 on Oracle** to **0.2719 under BM25 retrieval** ($k=3, 5$).
2. `[VERIFIED]` **Distractor Accumulation & Unfaithful Reasoning (RQ3)**: While unfaithful reasoning was only **1.99% under Oracle**, it surged to **24.81% at $k=1$**, **33.06% at $k=3$**, and **36.29% at $k=5$**. In over one-third of instances under $k=5$, the model asserted a correct stance for an invalid distractor rationale.
3. `[VERIFIED]` **Selective Prediction Efficacy (RQ2 / Kalai et al., 2026)**: Introducing an explicit confidence abstention threshold ($\tau = 0.80$) increased selective accuracy on answered claims from **41.14% to 58.65%**, reducing risk from 58.86% to 41.35%.

---

## 2. Comprehensive Comparison of Three Feasible Pathways

### Pathway A: Reproduction Under a Justified New Condition (Cross-Task Clinical Transfer to PubMedQA)
* **Scientific Question**: Does the distractor degradation and selective prediction trade-off observed on SciFact claim verification transfer out-of-the-box to biomedical question answering on PubMedQA without retraining?
* **Expected Code Changes**: Create `src/pubmedqa_loader.py` to ingest 500 expert-labeled PubMedQA test samples (`pqa_labeled`); evaluate stance classifier and abstention filter on clinical QA.
* **Compute Burden**: Very low (~5 minutes on local CPU).
* **Advantages**: Tests cross-domain/cross-task generalization across two distinct biomedical benchmarks analyzed in your literature review (§2.3).
* **Failure Risks / Disadvantages**:
  1. SciFact is claim verification (`SUPPORT`/`CONTRADICT`), whereas PubMedQA is question answering (`yes`/`no`/`maybe`). Mapping between claim assertion and clinical QA introduces label ambiguity.
  2. It does not solve the primary failure mode discovered in our baseline: the 36.29% unfaithful reasoning surge.
* **Evidence Needed**: Accuracy, Macro-F1 across `yes`/`no`/`maybe`, Risk-Coverage curve on PubMedQA.

---

### Pathway B: Controlled Comparative Study (Dense Neural Embeddings vs. Sparse BM25 Retrieval)
* **Scientific Question**: Under identical downstream stance classification and abstention rules, does replacing sparse lexical retrieval (BM25) with dense semantic bi-encoder retrieval (e.g. `sentence-transformers/all-MiniLM-L6-v2`) reduce unfaithful reasoning and mitigate retrieval noise degradation?
* **Expected Code Changes**: Implement `src/dense_retriever.py` to precompute 384-dimensional dense vectors for all 5,183 corpus abstracts and query embeddings; evaluate identical downstream classifier at $k \in \{1, 3, 5\}$.
* **Compute Burden**: Moderate (~10–15 minutes CPU embedding computation or 1 minute on Colab GPU).
* **Advantages**: Completely controlled comparative study isolating the retriever variable (sparse vs. dense) while keeping the claim set, prompt envelopes, classifier, and metrics frozen.
* **Failure Risks / Disadvantages**:
  1. Dense embeddings retrieve semantically close abstracts that may discuss the same disease or protein, but lack the specific causal or polar claim, potentially increasing subtle semantic hallucinations.
  2. Does not fundamentally extend the reasoning or abstention capabilities of the system.
* **Evidence Needed**: Head-to-head retrieval recall (R@1, R@3, R@5), Stance Macro-F1 comparison, Rationale F1, and Unfaithful Reasoning Rate.

---

### Pathway C: Targeted Theoretically Motivated Modification (Rationale-Grounded Evidence Verification / R-GEV)
* **Scientific Question**: Does enforcing a two-stage **Rationale-Grounded Evidence Verification (R-GEV)** gate—which requires the model to verify that an extracted rationale sentence surpasses an explicit atomic support threshold before permitting an active stance classification—significantly suppress unfaithful hallucinations (reducing Type III errors) and improve stance Macro-F1 under noisy retrieval?
* **Theoretical Foundation**: Grounded directly in your literature review:
  * **Min et al. (2023, EMNLP) FActScore**: True factual precision requires decomposing assertions into atomic units and validating evidence support prior to drawing global conclusions (§3.4).
  * **Dhuliawala et al. (2023, CoVe)**: Systematic verification of intermediate rationales suppresses hallucinations (§4.3).
  * **Kalai et al. (2026, Nature)**: Abstaining when evidence is inconclusive or sub-threshold eliminates the incentive to output ungrounded assertions (§6.5).
* **Expected Code Changes**: Implement one isolated module `src/rationale_verifier.py`. It inspects candidate rationale sentences from retrieved abstracts; if the maximum sentence-level support overlap is below a tunable threshold $\theta$, it forces the system into `NOT_ENOUGH_INFO` (Abstain) before the stance classifier can guess.
* **Compute Burden**: Very low (runs on local CPU in seconds).
* **Advantages**:
  1. **Directly Targets the Primary Empirical Failure Mode**: In Prompt 11, we proved that unfaithful reasoning explodes from 1.99% to 36.29% as distractors accumulate. Pathway C directly attacks this specific failure mechanism.
  2. **High Methodological Rigor**: Isolates a single, mathematically defined modification ($\theta$-rationale gating) that can be ablated systematically.
  3. **Zero Risk of Baseline Corruption**: The original baseline implementation remains 100% untouched; R-GEV acts as an isolated pre-classification filter.
* **Failure Risks**: If the rationale threshold $\theta$ is set too high, recall on true `SUPPORT` and `CONTRADICT` claims could be harmed, causing over-abstention. This can be quantified and optimized via an ablation curve.
* **Evidence Needed**: Four-arm ablation table (Baseline vs. Rationale-Only vs. Confidence-Only vs. Combined R-GEV), Unfaithful Reasoning Rate reduction, Stance Macro-F1, Risk-Coverage curves.

---

## 3. Comparison Matrix of the Three Pathways

| Evaluation Dimension | Pathway A (Clinical Transfer) | Pathway B (Dense vs Sparse) | Pathway C (Rationale-Grounded Verification) |
|---|---|---|---|
| **Alignment with Literature Review** | Moderate (Tasks are distinct) | High (Addresses RAG noise) | **Highest** (Unifies FActScore, CoVe & Calibration) |
| **Directly Solves Discovered Bug/Failure** | No | Partially (Changes retrieved set) | **Yes** (Directly attacks 36.29% unfaithful rate) |
| **Compute & Resource Feasibility** | Very High (CPU) | High (Embeddings on CPU/Colab) | **Very High** (Local CPU, zero cost) |
| **Experimental Isolability** | Confounded by task shift | Clean comparative study | **Clean single-variable ablation** |
| **Publication Novelty / Contribution** | Routine benchmark evaluation | Standard retriever comparison | **Evidence-grounded selective reasoning** |

---

## 4. Official Mentor Recommendation

> [!TIP]
> **Recommended Pathway**: **Pathway C (Targeted Theoretically Motivated Modification: Rationale-Grounded Evidence Verification — R-GEV)**.

### Beginner-Friendly Explanation:
In plain terms: currently, when our system retrieves 5 scientific papers, it looks for any sentence that shares words with the claim. Even if the paper is talking about something completely different, the model often picks a distractor sentence, guesses the stance, and gets the "right answer for the wrong reason" 36% of the time! 

Under **Pathway C**, we add an intelligent gatekeeper (the **Rationale Verifier**). Before the system is allowed to declare `SUPPORT` or `CONTRADICT`, it must check: *"Does this sentence actually provide strong, direct scientific evidence for the claim?"* If the answer is no, it immediately abstains and outputs `NOT_ENOUGH_INFO`. This directly stops the model from hallucinating conclusions based on irrelevant distractor papers.
