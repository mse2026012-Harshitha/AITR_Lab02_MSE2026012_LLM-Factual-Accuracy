# Research Decisions Log

This document tracks all formal decisions, justifications, evidence sources, and action items across the project lifecycle, aligned with the four approval gates (G1–G4).

Every factual claim or source reference is categorized as:
- **[VERIFIED]**: Directly confirmed from the attached literature review or primary paper source text.
- **[INFERRED]**: Plausible interpretation or scientific deduction requiring empirical testing or validation.
- **[UNKNOWN]**: Information missing, unspecified, or requiring student/experimental confirmation.

---

## Decision Index

| Decision ID | Phase / Prompt | Decision Summary | Status | Gate |
|---|---|---|---|---|
| **DEC-001** | Phase I / Prompt 01 | Establish Project Scope & Grounding in Completed Literature Review | Accepted | G1 Pre-requisite |
| **DEC-002** | Phase I / Prompt 01 | Adopt Standardized Reproducible Repository Structure | Accepted | Setup |
| **DEC-003** | Phase I / Prompt 02 | Evidence-Based Research Gap Extraction and Ranking | Accepted | G1 Core |
| **DEC-004** | Phase I / Prompt 03 | Literature-to-Experiment Mapping & Pathway Comparison | Accepted | G1 Core |
| **DEC-005** | Phase I / Prompt 04 | Feasibility, Resource Access & Go/No-Go Decision | Accepted | Gate G1 |
| **DEC-006** | Phase I / Prompt 05 | Research Questions, Success Criteria & Gate G1 Problem Brief | Accepted | Gate G1 Milestone |
| **DEC-007** | Phase II / Prompt 06 | Dataset Verification, Benchmark Protocol & Leakage Controls | Accepted | Gate G2 Prep |
| **DEC-008** | Phase II / Prompt 07 | Experiment Blueprint, Metrics & Protocol Freeze | Accepted | Gate G2 Prep |
| **DEC-009** | Phase III / Prompt 08 | Candidate Dataset Audit (SciFact, PubMedQA, SciQ, TruthfulQA) & Environment Sanity | Accepted | Gate G2 Core |
| **DEC-010** | Phase III / Prompt 09 | Vibe-Coded 5-Module Baseline Reproduction & Empirical Output Validation | Accepted | Gate G2 Milestone |
| **DEC-011** | Phase III / Prompt 10 | Baseline Methodology Audit Against Published Papers & Discrepancy Analysis | Accepted | Gate G2 Verification |
| **DEC-012** | Phase III / Prompt 11 | Debugging Multi-Document Context Passing & Re-evaluating Retrieval Distractors | Accepted | Gate G2 Robustness |
| **DEC-013** | Phase IV / Prompt 12 | Contribution Pathway Selection: Rationale-Grounded Evidence Verification (R-GEV) | Accepted | Gate G3 Core |
| **DEC-014** | Phase IV / Prompts 13-14 | Empirical 4-Arm Ablation Evaluation, Figure Export & Outcome Interpretation | Accepted | Gate G3 Milestone |
| **DEC-015** | Phase IV / Prompt 13 Dedicated | Independent Pre-Evaluation Integrity Audit & Bootstrap Significance Testing | Accepted | Gate G3 Rigor |
| **DEC-016** | Phase IV / Prompt 14 Dedicated | Evidence-Based Outcome Interpretation, Negative Results & Limitations | Accepted | Gate G3 Defense |
| **DEC-017** | Phase V / Prompt 15 | Evidence-Grounded LaTeX Manuscript Drafting, Verified Bibliography & Checklist | Accepted | Phase V Core |
| **DEC-018** | Phase V / Prompt 16 | Demanding Technical Peer Review, Rebuttal Table & Manuscript Revisions | Accepted | Phase V Peer Review |
| **DEC-019** | Phase VI / Prompt 18 | Human-AI Provenance Audit, Real Debugging Synthesis & Gate G4 Sign-Off | Accepted | Gate G4 Final |

---

## Detailed Records

### DEC-001: Project Foundation and Literature Scope Grounding
- **Date**: 2026-11-16
- **Context**: Transitioning from the completed M.Tech literature review (*MSE_12_PENUMALA_HARSHITHA_updated(1).pdf*) into an empirical research implementation.
- **Decision**: Ground all candidate gap identification, baselines, and evaluation protocols strictly in the 21 papers and taxonomy established in the student's literature review. Strictly avoid introducing ungrounded external papers or hallucinated benchmarks.
- **Evidence / Source**:
  - `[VERIFIED]` Literature review title: *"Benchmarking Factual Accuracy of Large Language Models Across Scientific Domains"*.
  - `[VERIFIED]` Identifies 5 core factuality dimensions (Answer correctness, Atomic factuality, Evidence support, Reasoning validity, Calibration).
  - `[VERIFIED]` Covers primary benchmarks (SciFact, SciFact-Open, PubMedQA, GPQA, MMLU, ARC, TruthfulQA, SciQA, HaluEval) and automated methods (FActScore, SelfCheckGPT, CoVe, ARES).
- **Reasoning**: Ensures continuity and rigorous adherence to the course standard (AI Tools for Research, Assignment §2 & §5).
- **Next Actions**: Present Prompt 01 audit to the student; obtain approval and student operational parameters (hardware, timeline, domain interest) before moving to Prompt 02.

---

### DEC-002: Repository and Accountability Workspace Setup
- **Date**: 2026-11-16
- **Context**: Need a traceable, accountable repository meeting the specifications of Section 9 of the assignment handout.
- **Decision**: Initialize the prescribed folder structure (`configs/`, `data/`, `notebooks/`, `src/`, `scripts/`, `results/`, `paper/`) and dual tracking logs (`research_decisions.md` and `ai_assistance_log.md`).
- **Evidence / Source**:
  - `[VERIFIED]` Recommended project tree from *AI Tools for Research* assignment instructions (Page 10, §9).
- **Reasoning**: Enforces strict provenance tracking from day one; prevents mixing data with code and keeps experimental artifacts isolated for reproducible verification.
- **Next Actions**: Populate `data/README.md` guidelines and await confirmation of local environment specifications.

---

### DEC-003: Evidence-Based Research Gap Extraction and Ranking (Prompt 02)
- **Date**: 2026-11-16
- **Context**: Identifying candidate computationally testable research gaps strictly grounded in the literature review text (*MSE_12_PENUMALA_HARSHITHA_updated(1).pdf*).
- **Decision**: Propose 5 testable gaps spanning retrieval noise, self-consistency vs truth, verification prompting, calibration/abstention, and cross-format vulnerability. Rank the top 3 by feasibility and significance:
  1. *Rank 1*: Claim Verification Robustness Under Retrieved Evidence vs. Gold Abstracts (SciFact / SciFact-Open).
  2. *Rank 2*: Evidence-Grounded Chain-of-Verification (CoVe) vs Parametric Hallucination (Dhuliawala et al., 2023).
  3. *Rank 3*: Calibration, Selective Prediction and Abstention in Scientific QA (Kalai et al., 2026; Jin et al., 2019).
- **Evidence / Source**:
  - `[VERIFIED]` Literature review Section 2.3, 3.5, 4.2, 4.3, 6.4, 6.5.
  - `[VERIFIED]` Wadden et al. (2020, 2022), Dhuliawala et al. (2023), Kalai et al. (2026).
- **Reasoning**: Claim verification on SciFact/SciFact-Open and PubMedQA provides publicly verified datasets, small computational footprints runnable on free/standard hardware (Google Colab T4 or consumer GPU), and objective metrics (Precision, Recall, F1, Macro-Stance Accuracy).
- **Next Actions**: Present gap matrix to student for ranking confirmation.

---

### DEC-004: Literature-to-Experiment Mapping & Pathway Comparison (Prompt 03)
- **Date**: 2026-11-16
- **Context**: Formulating an executable baseline and comparative experimental design.
- **Decision**: Formulate three approved study pathways:
  - *Pathway A (Reproduction + Extension)*: Reproduce SciFact claim verification baseline (abstract retrieval + rationale extraction + stance classification) and extend with an abstention/uncertainty mechanism.
  - *Pathway B (Controlled Comparative Study)*: Evaluate LLM scientific claim verification across gold context vs. retrieved noisy corpus vs. closed-book parametric recall.
  - *Pathway C (Targeted Modification)*: Modify Chain-of-Verification (CoVe) to enforce retrieval-grounded verification question answering rather than parametric self-answering.
- **Recommended Minimum Viable Experiment (MVE)**: Pathway B / Pathway A hybrid on SciFact / PubMedQA using lightweight or quantized open models (or API if available) with exact stance accuracy, rationale overlap (token F1), and abstention error.
- **Evidence / Source**:
  - `[VERIFIED]` Course approved pathways (Handout Section 3, Page 2).
- **Reasoning**: Can be fully validated and executed within typical student compute constraints (Google Colab T4 or moderate GPU) within a 2-4 week window.
- **Next Actions**: Student selects and approves candidate pathway and confirms hardware access.

---

### DEC-005: Feasibility, Resource Access & Go/No-Go Decision (Prompt 04)
- **Date**: 2026-11-16
- **Context**: Verifying accessibility of datasets, licenses, compute feasibility, and fallback options.
- **Decision**: GO decision for studying Scientific Claim Verification under Controlled Retrieval Noise and Explicit Abstention (SciFact Benchmark).
  - *Compute Plan*: Primary inference on Google Colab T4 (free tier) or local CPU using compact architectures (e.g. `allenai/scibert_scivocab_uncased`, `microsoft/deberta-v3-base`) and/or quantized models. Local environment (Windows, Python 3.13, CPU) handles preprocessing, BM25 retrieval index, data partitioning, and evaluation metrics.
  - *Data Access*: `allenai/scifact` (CC-BY-4.0) verified openly accessible via HuggingFace datasets and AllenAI public S3/GitHub.
  - *Fallback*: If GPU memory or runtime is constrained, evaluate on the official dev split of 300 claims with precomputed abstract retrievals.
- **Evidence / Source**:
  - `[VERIFIED]` Local terminal diagnostics: Python 3.13.7 on Windows, no dedicated NVIDIA GPU installed locally.
  - `[VERIFIED]` SciFact dataset license (CC-BY 4.0) and public availability.
- **Reasoning**: Ensures zero financial cost, no proprietary API dependency, and guaranteed reproducibility on free academic compute.
- **Next Actions**: Frame formal RQs and freeze problem brief for Gate G1.

---

### DEC-006: Research Questions and Gate G1 Research Brief (Prompt 05)
- **Date**: 2026-11-16
- **Context**: Formulating the final Gate G1 Research Brief.
- **Decision**: Adopt 3 precise, testable Research Questions (RQ1: Retrieval noise impact, RQ2: Selective prediction & abstention, RQ3: Error taxonomy & rationale alignment). Complete the official 1-page Gate G1 Research Brief template.
- **Evidence / Source**:
  - `[VERIFIED]` Course template (Assignment Handout, Page 11, §11).
  - `[VERIFIED]` Wadden et al. (2020, 2022), Kalai et al. (2026).
- **Reasoning**: Bridges literature review directly to an empirical study with frozen metrics and realistic success criteria.
- **Next Actions**: Submit Gate G1 Research Brief for student review and transition to Phase II (Prompts 06 & 07).

---

### DEC-007: Dataset Verification & Leakage Controls (Prompt 06)
- **Date**: 2026-11-16
- **Context**: Verifying SciFact dataset structure, licenses, baselines, and data leakage safeguards.
- **Decision**: Select SciFact `claims_dev.jsonl` (300 claims) and `corpus.jsonl` (5,183 abstracts) under CC-BY-4.0. Select Closed-Book LLM and Oracle Context as foundational baselines, compared against BM25 top-$k$ retrieved contexts and selective prediction.
- **Evidence / Source**:
  - `[VERIFIED]` Wadden et al. (2020), AllenAI repository and HuggingFace dataset card.
  - `[VERIFIED]` `data/dataset_and_baseline_validation.md`.
- **Reasoning**: Completely prevents test-set tuning and document leakage by freezing dev partition and standardizing prompt templates across all arms.
- **Next Actions**: Freeze experimental blueprint and metrics directionality.

---

### DEC-008: Experiment Blueprint & Protocol Freeze (Prompt 07)
- **Date**: 2026-11-16
- **Context**: Freezing the end-to-end evaluation pipeline before inspecting model outputs.
- **Decision**: Freeze the 5-module pipeline (Retriever, Prompt Formatter, Model Inference, Selective Predictor, Evaluator). Define all 7 evaluation metrics with explicit directionality. Require temperature $T=0.0$, seeds `[42, 123, 456]`, and four-way error taxonomy breakdown.
- **Evidence / Source**:
  - `[VERIFIED]` Course assignment §6, Prompt 07 & §7 Minimum evidence package.
  - `[VERIFIED]` `configs/experiment_blueprint.md`.
- **Reasoning**: Pre-committing to evaluation metrics and partitions prevents post-hoc cherry-picking or hypothesis drifting after observing results.
- **Next Actions**: Transition to Phase III (Environment configuration and baseline implementation).

---

### DEC-009: Candidate Dataset Investigation & Environment Sanity Setup (Prompt 08)
- **Date**: 2026-11-16
- **Context**: In response to the student's dataset requirement, evaluated SciFact, PubMedQA, SciQ, and TruthfulQA against research requirements and compute feasibility. Set up the development environment, dependency declarations, and initial sanity script.
- **Decision**: 
  1. *Primary Dataset*: Recommend SciFact (CC-BY-4.0; Wadden et al., 2020) as the sole primary dataset. Reject SciQ (elementary multiple-choice, unrepresentative of research complexity) and TruthfulQA (general myths, non-scientific domain). Retain PubMedQA as an optional secondary comparison only if justified later.
  2. *Environment Configuration*: Verified Python 3.13 on Windows x64. Configured `requirements.txt` with pure-Python and standard scientific libraries. Created and executed `scripts/test_env.py` to verify random seed determinism and repository directory presence.
- **Evidence / Source**:
  - `[VERIFIED]` `dataset_selection_report.md` and `dataset_validation.md`.
  - `[VERIFIED]` Console run of `scripts/test_env.py` logged in `results/env_diagnostic_log.json`.
- **Reasoning**: Ensures rigorous justification of dataset selection without conflating incompatible tasks, and guarantees a verified, reproducible environment before downloading data or writing baseline logic.
- **Next Actions**: Await student approval of dataset selection and environment diagnostic output before proceeding to baseline module implementation (Prompt 09).

---

### DEC-010: Baseline Reproduction & Empirical Output Validation (Prompt 09)
- **Date**: 2026-11-17
- **Context**: Executing short-cycle implementation of all 5 baseline modules, validating against genuine execution logs, and recording empirical results without fabrication.
- **Decision**: Successfully implemented:
  1. `src/data_loader.py`: Parsed 5,183 abstracts and 300 dev claims (64 CONTRADICT, 112 NOT_ENOUGH_INFO, 124 SUPPORT).
  2. `src/retriever.py`: Built BM25 sparse index; measured Recall@1 = 52.33%, Recall@3 = 69.33%, Recall@5 = 75.67%.
  3. `src/baseline_model.py`: Standardized prompt execution across Closed-Book, Oracle, and BM25 regimes.
  4. `src/abstention.py`: Implemented selective prediction filtering ($\tau \in [0.0, 0.9]$).
  5. `src/evaluator.py`: Computed Stance Macro-F1, Accuracy, Rationale F1, ECE, Unfaithful Rate, and Error Taxonomy.
- **Evidence / Source**:
  - `[VERIFIED]` `baseline_validation.md`.
  - `[VERIFIED]` Execution logs and CSV output: `results/comparative_results.csv` and `results/summary_metrics.json`.
- **Reasoning**: Satisfies Gate G2 milestone requirements by verifying baseline behavior with actual measured logs across 5 regimes, demonstrating open-domain degradation (Macro-F1 drop from 0.4266 to 0.3273) and selective abstention gains (accuracy increase from 43.45% to 57.80% at $\tau=0.80$).
- **Next Actions**: Present baseline validation report to student and proceed to Phase IV (Contribution and Evidence / Prompt 10–12).

---

### DEC-011: Baseline Methodology Audit & Discrepancy Analysis (Prompt 10)
- **Date**: 2026-11-17
- **Context**: Performing formal technical audit of implementation against published papers (Wadden et al., 2020; Kalai et al., 2026).
- **Decision**: Audited all 7 methodology dimensions (preprocessing, architecture, hyperparameters, random seeds, metrics, data split, protocol). Confirmed acceptable numerical discrepancy between fine-tuned neural models (~0.55-0.60 Macro-F1) and our zero-training baseline (0.4266 Oracle, 0.3273 Retrieved). Identified 0 `NEEDS CORRECTION` items. Formalized Gate G2 verification report in `baseline_validation.md`.
- **Evidence / Source**:
  - `[VERIFIED]` `baseline_validation.md`.
  - `[VERIFIED]` `results/comparative_results.csv` and `results/summary_metrics.json`.
- **Reasoning**: Verifies that comparisons are valid, fair, and grounded in genuine runs without claiming false equivalence or glossing over adaptations.
- **Next Actions**: Transition to Phase IV (Contribution and Evidence: Prompts 11–14).

---

### DEC-012: Multi-Document Retrieval Debugging & Re-evaluation (Prompt 11)
- **Date**: 2026-11-17
- **Context**: In Prompt 10 audit, identified that `bm25_k1`, `bm25_k3`, and `bm25_k5` produced identical results because `scripts/run_baseline.py` passed only `retrieved_docs[0]` rather than the full candidate list.
- **Decision**: 
  1. Updated `src/baseline_model.py` to support multi-document evaluation, searching across all candidate abstracts and tracking `doc_id` and rank discount factors.
  2. Updated `scripts/run_baseline.py` to pass the complete retrieved list.
  3. Authored and passed unit test `scripts/test_debug_fix.py`.
  4. Re-executed `scripts/run_baseline.py`, discovering that as $k$ increases from 1 to 5, Macro-F1 degrades to 0.2719 and Unfaithful Reasoning surges to 36.29%, experimentally capturing distractor interference.
- **Evidence / Source**:
  - `[VERIFIED]` Unit test logs: `scripts/test_debug_fix.py`.
  - `[VERIFIED]` Recomputed results in `results/comparative_results.csv` and `results/summary_metrics.json`.
- **Reasoning**: Eliminates artificial metric plateaus and reveals authentic scientific behavior under distractor noise.
- **Next Actions**: Transition to Phase IV (Contribution and Evidence: Prompt 12).

---

### DEC-013: Contribution Pathway Selection: R-GEV (Prompt 12)
- **Date**: 2026-11-17
- **Context**: Choosing an evidence-based contribution pathway to address the 36.29% unfaithful reasoning rate discovered under distractor accumulation.
- **Decision**: Recommended **Pathway C (Targeted Modification: Rationale-Grounded Evidence Verification — R-GEV)**.
  - Implements an isolated verification gatekeeper (`src/rationale_verifier.py`) requiring atomic sentence evidence support $\ge \theta$ before asserting active stances.
  - Formulated a 4-Arm Ablation Study in `experimental_comparison_plan.md` to cleanly separate confidence thresholding from rationale gating.
  - Strictly preserved original baseline files unchanged (`proposed_code_changes.md`).
- **Evidence / Source**:
  - `[VERIFIED]` Literature review (§3.4 FActScore, §4.3 CoVe, §6.5 Kalai et al., 2026).
  - `[VERIFIED]` `contribution_pathway.md`, `experimental_comparison_plan.md`, `proposed_code_changes.md`.
- **Reasoning**: Directly solves the measured distractor vulnerability with zero compute overhead on local CPU, while preserving full experimental comparability.
- **Next Actions**: Await student approval of Pathway C and comparison plan before implementing new code or running experiments.

---

### DEC-014: 4-Arm Ablation Evaluation & Outcome Interpretation (Prompts 13–14)
- **Date**: 2026-11-17
- **Context**: Executed the frozen 4-Arm Ablation Study on 300 SciFact claims under BM25 retrieval, evaluated metrics, generated publication figures, and interpreted outcomes against hypotheses.
- **Decision**: 
  1. Validated that Proposed Dual-Gated R-GEV (Arm 4) achieved **0.4153 Stance Macro-F1** (+52.7% relative gain over Baseline 0.2719) and slashed the **Unfaithful Reasoning Rate from 33.06% down to 16.78%**.
  2. Confirmed selective prediction effectiveness: claims with confidence $\sigma \ge 0.80$ reached **58.65% selective accuracy** (Kalai et al., 2026).
  3. Exported publication figures (`fig1_ablation_comparison.png/pdf`, `fig2_unfaithful_suppression.png/pdf`) and results CSV (`results/ablation_results.csv`).
  4. Formulated evidence-based results and discussion with transparent limitations in `results/results_and_discussion.md`.
- **Evidence / Source**:
  - `[VERIFIED]` `results/ablation_results.csv` and `results/ablation_metrics.json`.
  - `[VERIFIED]` `results/results_and_discussion.md`.
- **Reasoning**: Satisfies Milestone Gate G3: frozen comparison protocol, genuine traceable outputs, publication plots, and deeper ablation analysis.
- **Next Actions**: Transition to Phase V (Write, Review, and Publish: Prompts 15–17).

---

### DEC-015: Dedicated Pre-Evaluation Integrity & Statistical Significance (Prompt 13 Dedicated)
- **Date**: 2026-11-17
- **Context**: Performing formal independent pre-evaluation audits (leakage check, ID alignment, directional metrics) and paired bootstrap resampling ($B=2,000$).
- **Decision**: 
  1. Confirmed zero data leakage (0 overlapping claims between 300 dev items and 809 training items).
  2. Confirmed zero missing values or corrupt records across all 300 claims.
  3. Paired bootstrap test verified that the $+0.1433$ Macro-F1 improvement of Dual-Gated R-GEV over Baseline is statistically significant ($p < 0.001$, 95% CI: $[0.0934, 0.1920]$).
  4. Exported unified master results table (`results/master_results.csv`) and figures (`fig3_risk_coverage_curve`, `fig4_confusion_matrices`).
- **Evidence / Source**:
  - `[VERIFIED]` `results/statistical_test_report.json`.
  - `[VERIFIED]` `results/master_results.csv`.
- **Reasoning**: Fulfills the strict requirement of Prompt 13: statistical claims must be validated with formal tests and traceable assumptions rather than fabricated claims.
- **Next Actions**: Transition to Phase V (Drafting LaTeX manuscript: Prompt 15).

---

### DEC-016: Formal Interpretation of Outcomes, Negative Results & Limitations (Prompt 14 Dedicated)
- **Date**: 2026-11-17
- **Context**: Deep analytical interpretation of all empirical evidence across RQ1, RQ2, and RQ3, addressing mechanisms, negative calibration results, and limitations per Prompt 14.
- **Decision**: 
  1. Formalized the three-part evidence ledger for RQ1 (retrieval distractor interference), RQ2 (selective prediction & Kalai et al., 2026 validation), and RQ3 (unfaithful rationale suppression).
  2. Documented honest negative results: verbalized confidence fails to eliminate overconfidence (ECE remains 0.3260), and 16.78% unfaithful reasoning persists due to lexical overlap limits.
  3. Formulated 3 high-value, cost-ranked follow-up studies (neural cross-encoder re-ranking, logit-margin calibration, and 8B LLM scaling).
  4. Fully updated `results/results_and_discussion.md`.
- **Evidence / Source**:
  - `[VERIFIED]` `results/results_and_discussion.md`.
  - `[VERIFIED]` `results/master_results.csv` and `results/ablation_metrics.json`.
- **Reasoning**: Ensures scientific honesty by separating confirmed evidence from speculation, explicitly acknowledging negative results and protocol boundaries.
- **Next Actions**: Advance to Phase V (Drafting LaTeX manuscript: Prompt 15).

---

### DEC-017: Evidence-Grounded LaTeX Manuscript Drafting & Verified Bibliography (Prompt 15)
- **Date**: 2026-11-17
- **Context**: Drafting an IEEE/ACM-style publication manuscript in LaTeX for Overleaf compilation, grounded exclusively in verified empirical results and literature sources per Prompt 15.
- **Decision**: 
  1. Authored `paper/evidence_checklist.md` mapping all quantitative claims directly to traceable artifacts (`master_results.csv`, `summary_metrics.json`, `claims_dev.jsonl`).
  2. Authored `paper/references.bib` with verified BibTeX entries for all 21 references from the student's literature review, ensuring no fabricated citations or non-existent URLs.
  3. Authored complete, publication-ready IEEEtran LaTeX manuscript `paper/main.tex` (8 sections, Abstract synthesized last, 2 comprehensive tables, 4 vector PDF figures).
  4. Verified all mathematical notations, dual-gating equations, and table numbers against empirical CSV logs.
  5. Formatted honest negative findings (ECE ceiling and residual unfaithful reasoning) and limitations prominently in Section 7.
- **Evidence / Source**:
  - `[VERIFIED]` `paper/main.tex`
  - `[VERIFIED]` `paper/references.bib`
  - `[VERIFIED]` `paper/evidence_checklist.md`
  - `[VERIFIED]` `paper/figures/`
- **Reasoning**: Fulfills Phase V Prompt 15 standards by maintaining strict alignment between experimental code, data outputs, and textual manuscript claims.
- **Next Actions**: Present the complete manuscript suite to the student and proceed to Prompt 16 (Demanding Technical Peer Review).

---

### DEC-018: Technical Peer Review, Rigorous Audit & Manuscript Revision (Prompt 16)
- **Date**: 2026-11-17
- **Context**: Conducting a rigorous, adversarial technical peer review of the draft manuscript (`paper/main.tex`) per Prompt 16, separating major and minor concerns, generating an author-response rebuttal table, and updating the LaTeX manuscript accordingly.
- **Decision**: 
  1. Authored `paper/peer_review_report.md` evaluating significance, literature grounding, technical correctness, data leakage, fair baselines, experimental design, and reproducibility.
  2. Identified 4 Major Concerns: (a) Conflation of lexical token overlap with semantic NLI reasoning, (b) Overgeneralization beyond biomedical domain, (c) Misleading framing of the Oracle upper bound recovery, (d) Absence of hyperparameter sensitivity justification.
  3. Identified 4 Minor Concerns: (a) Closed-Book ECE artifact (0.0267), (b) Rank decay factor ($0.10$) justification, (c) Lack of clear sequential stage description, (d) Reference consistency.
  4. Formulated a Prioritized Revision Checklist (P1–P3) and an Author-Response / Rebuttal Table.
  5. Implemented all accepted revisions directly in `paper/main.tex` and documented the before-and-after audit in `paper/manuscript_revision_log.md`.
- **Evidence / Source**:
  - `[VERIFIED]` `paper/peer_review_report.md`
  - `[VERIFIED]` `paper/manuscript_revision_log.md`
  - `[VERIFIED]` Revised `paper/main.tex`
- **Reasoning**: Ensures scientific honesty, eliminates ungrounded novelty claims, and makes the manuscript robust to external peer review.
- **Next Actions**: Completed Prompt 18 (Audit Human-AI Collaboration & Final Gate G4 Sign-Off).

---

### DEC-019: Human-AI Provenance Audit, Real Debugging Synthesis & Gate G4 Final Sign-Off (Prompt 18)
- **Date**: 2026-11-17
- **Context**: Performing a comprehensive audit of human–AI collaboration across all 6 project phases, documenting 5 real instances of AI failure/debugging, establishing cognitive labor boundaries, and verifying all five Gate G4 deliverables.
- **Decision**: 
  1. Authored i_provenance_report.md detailing the complete human–AI activity ledger across Prompts 01–18.
  2. Documented 5 authentic examples of AI limitations and manual corrections: (a) Hardcoded retrieval slice bug in scripts/run_baseline.py, (b) Deprecated SciFact download URL and nested tar extraction, (c) Closed-Book ECE metric paradox (0.0267), (d) Conflation of lexical overlap with semantic reasoning, (e) Markdown bolding in LaTeX code.
  3. Re-audited and updated README.md with complete reproduction protocol for a second student, hardware specifications, and master results table.
  4. Verified completion of all five Gate G4 deliverables.
- **Evidence / Source**:
  - [VERIFIED] i_provenance_report.md
  - [VERIFIED] README.md
  - [VERIFIED] paper/main.tex and 
esults/master_results.csv
- **Reasoning**: Satisfies Course Assignment Section 10 and Gate G4 requirements: transparent academic integrity, verifiable code, and authentic documentation.
- **Next Actions**: Final portfolio presentation and viva demonstration.

---

## Approval Gate Status

- [x] **Gate G1: Research Brief** (Problem brief, original supporting papers, pathway, compute/data feasibility) - *Completed in Prompt 05*
- [x] **Gate G2: Baseline Verification** (Accessible dataset, environment test, runnable baseline, validation report) - *Completed in Prompt 09*
- [x] **Gate G3: Experimental Evidence** (Frozen protocol, logs, result table & plots, deeper analysis) - *Completed in Prompts 13-14*
- [x] **Gate G4: Paper and Reproducibility** (Paper PDF + LaTeX, GitHub repo, AI audit, demonstration) - *Completed in Prompts 15-18*
