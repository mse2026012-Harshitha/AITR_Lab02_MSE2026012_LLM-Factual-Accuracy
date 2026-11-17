# AI Provenance and Research Integrity Report (Gate G4)

**Project Title**: Benchmarking Scientific Claim Verification and Hallucination Mitigation under Distractor Accumulation and Selective Abstention: An Empirical Study on Biomedical Literature  
**Author / Investigator**: Penumala Harshitha (M.Tech, Department of Information Technology, IIIT Allahabad)  
**Enrollment**: `mse2024012@iiita.ac.in`  
**Course**: AI Tools for Research (Post-Mid-Sem Implementation Project)  
**Reporting Date**: 2026-11-17  
**Academic Integrity Certification**: In accordance with Course Assignment §10 and Gate G4 requirements, this document provides an honest, authentic audit of human–AI collaboration across all 6 phases of the research lifecycle. Zero fabricated logs, phantom tools, or imagined execution traces are contained herein.

---

## 1. Executive Summary & Attribution Statement

This research project transitioned an academic literature review into an empirical, reproducible implementation studying factual claim verification on the SciFact biomedical benchmark (300 evaluation claims, 5,183 candidate abstracts). 

An AI pair-programming assistant (Google Antigravity / Claude 3.5 / Gemini) was utilized across the project lifecycle under strict **human-in-the-loop governance**. The human investigator retained sole intellectual ownership over:
1. Research question framing and scientific hypothesis formulation.
2. Go/No-Go feasibility decisions at Phase I (Gate G1).
3. The selection of SciFact over candidate benchmarks (PubMedQA, SciQ, TruthfulQA) at Phase II/III (Gate G2).
4. Code discrepancy auditing, bug diagnosis, and rejection of false plateaus at Phase III.
5. Contribution pathway selection (choosing isolated Pathway C R-GEV over brute-force comparison) at Phase IV (Gate G3).
6. Technical peer review critique, qualification of lexical heuristics, and final manuscript sign-off at Phase V/VI (Gate G4).

At no point was code executed, a dataset downloaded, or an extension implemented without prior human validation and explicit gate sign-off.

---

## 2. Comprehensive Human–AI Interaction Ledger

The following table records every significant AI-assisted activity across the six project phases:

| Phase & Prompt | Task | AI Tool / Mode | AI Proposal / Draft | Human Decision & Verification Method | Code & Result Change | Final Outcome |
|---|---|---|---|---|---|---|
| **Phase I: Prompt 01** | Repository & Tracking Setup | Anthropic Claude / Shell Sandboxed | Proposed directory layout, `research_decisions.md` template, and `ai_assistance_log.md` structure. | **Approved.** Verified that paths complied with Windows OS and course directory guidelines. | Created `configs/`, `data/`, `notebooks/`, `src/`, `scripts/`, `results/`, `paper/`. | Standardized, traceable repository structure established. |
| **Phase I: Prompts 02–03** | Gap Extraction & Experiment Mapping | Anthropic Claude | Extracted 5 candidate gaps from literature review; mapped 3 published methods (SciFact, SelfCheckGPT, CoVe). | **Modified.** Audited extracted gaps against primary citations. Selected Gap 1 (retrieval distractor interference) as most grounded in review. | Created DEC-003 and DEC-004 in `research_decisions.md`. | Frozen experimental candidate pathways A, B, and C. |
| **Phase I: Prompts 04–05** | Feasibility Audit & Gate G1 Problem Brief | Local Python 3.13 / Claude | Proposed running 8B parameter models locally on Windows laptop. | **Rejected & Corrected.** Ran system diagnostics; detected no local CUDA GPU. Decided to benchmark using sparse retrieval and algorithmic evaluation locally. | Formulated Gate G1 One-Page Problem Brief with 3 formal RQs. | Gate G1 successfully passed with resource-realistic boundaries. |
| **Phase II: Prompts 06–07** | Dataset Audit & Protocol Freeze | Claude / Markdown Generator | Drafted dataset audit and mathematical blueprint with directional indicators ($\uparrow / \downarrow$). | **Audited.** Verified SciFact CC-BY-4.0 license, 3-way stance schema, and strict 0% train-dev claim overlap safeguard. | Authored `configs/experiment_blueprint.md` and `data/dataset_and_baseline_validation.md`. | Protocol completely frozen prior to viewing any baseline outputs. |
| **Phase III: Prompt 08** | Multi-Dataset Audit & Environment Test | Python 3.13 / PowerShell | Evaluated SciFact, PubMedQA, SciQ, TruthfulQA. Drafted `scripts/test_env.py`. | **Approved SciFact Only.** Confirmed SciQ is educational and TruthfulQA lacks corpus retrieval. Authorized dependency installation (`numpy`, `pandas`, `rank-bm25`, `scikit-learn`). | Executed `scripts/test_env.py` (exit code 0). Seed determinism verified. | Environment verified; candidate dataset report delivered. |
| **Phase III: Prompt 09** | Vibe-Coding 5 Baseline Modules | Python Pair-Programming | Generated minimal modules: `data_loader`, `retriever`, `baseline_model`, `abstention`, `evaluator`. | **Unit Tested.** Verified input/output shapes using dedicated unit test scripts (`test_data_loader.py`, `test_retriever.py`). | Implemented 5 modules in `src/`. Ran `scripts/run_baseline.py`. | Working baseline generated in short, verifiable cycles. |
| **Phase III: Prompts 10–11** | Baseline Audit & Debugging Discrepancy | Python Debugger / Trace Audit | Output showed identical metrics for BM25 $k=1, 3, 5$ (Macro-F1 plateaued at 0.3273). | **Manual Code Audit.** Caught that AI had hardcoded `retrieved_docs[0]` in baseline runner. Refused to accept plateau. Demanded multi-doc fix. | Modified `src/baseline_model.py` and `scripts/run_baseline.py`. Verified via `scripts/test_debug_fix.py`. | Real phenomenon revealed: unfaithful reasoning surged from 24.81% ($k=1$) to 36.29% ($k=5$). Gate G2 passed. |
| **Phase IV: Prompt 12** | Contribution Pathway Selection | Markdown Planning / Strategy | Compared Pathway A (Reproduction), B (Comparative Study), and C (Targeted Modification). Recommended Pathway C (R-GEV). | **Approved Pathway C.** Verified that R-GEV isolates the scientific contribution without modifying baseline code. | Authored `contribution_pathway.md`, `experimental_comparison_plan.md`, `proposed_code_changes.md`. | Isolated modification plan approved prior to implementation. |
| **Phase IV: Prompts 13–14** | 4-Arm Ablation & Statistical Testing | Python 3.13 / Matplotlib / SciPy | Generated `src/rationale_verifier.py`, executed 4-arm ablation, paired bootstrap ($B=2,000$), and exported 4 figures. | **Statistical Verification.** Confirmed zero dev-train leakage programmatically. Verified $p < 0.001$ ($95\%$ CI: $[0.0934, 0.1920]$). Audited figures. | Produced `results/master_results.csv`, `statistical_test_report.json`, and 4 vector PDFs. | Gate G3 milestone completed: Macro-F1 boosted to 0.4153, unfaithful rate halved to 16.78%. |
| **Phase V: Prompt 15** | LaTeX Manuscript Drafting | LaTeX Generator / BibTeX Compiler | Drafted `paper/main.tex` and `references.bib` with 21 verified references. | **Format & Citation Check.** Verified all 21 references were authentic. Eliminated markdown syntax (`**`) in LaTeX. Verified tables match `master_results.csv`. | Created `paper/main.tex`, `references.bib`, `evidence_checklist.md`, and staged figures. | Full 6–10 page IEEEtran manuscript ready for Overleaf. |
| **Phase V: Prompt 16** | Technical Peer Review & Rebuttal | Adversarial Reviewer Persona | Identified 4 major concerns: lexical heuristic vs. NLI, cross-domain overclaiming, Oracle recovery framing, hyperparameter justification. | **Revisions Implemented.** Renamed to "Atomic Lexical Support Gate", scoped title to biomedical literature, softened Oracle claims, added ECE artifact note. | Created `paper/peer_review_report.md`, `manuscript_revision_log.md`, and updated `main.tex`. | Manuscript hardened against academic critique. |
| **Phase VI: Prompt 18** | Human–AI Collaboration Audit | Self-Reflection / Meta-Audit | Proposed auditing the full 6-phase trajectory, logging real errors, and formalizing Gate G4 deliverables. | **Validated.** Ensured every recorded error was factual and traceable in conversation logs and Git diffs. | Authored `ai_provenance_report.md` and updated `README.md`. | Complete research integrity portfolio established (Gate G4). |

---

## 3. Real Examples of AI Limitations, Manual Corrections, and Verification

In adherence to strict academic honesty, we report five genuine instances during this project where the AI system failed, introduced bugs, or required critical human intervention:

### Example 1: The Hardcoded Retrieval Window Bug (Prompt 10 / Prompt 11)
- **AI Failure**: When vibe-coding `scripts/run_baseline.py` in Prompt 09, the AI wrote code that passed `retrieved_docs[0]` into `classify_and_extract()` regardless of whether $k=1, 3,$ or $5$. Consequently, the model evaluated only the single top-ranked document for all retrieval depths, producing completely identical Macro-F1 scores (0.3273) and flatlining all comparative metrics.
- **Human Detection**: During the Prompt 10 audit, the human investigator questioned how expanding from 1 to 5 documents could result in zero metric variance. Code inspection traced the bug to line 78 of `scripts/run_baseline.py`.
- **Manual Correction**: The human directed the AI to refactor `src/baseline_model.py` to accept a list of multiple abstracts and concatenate their token pools. A dedicated test script (`scripts/test_debug_fix.py`) verified the correction before re-running the benchmark.
- **Scientific Consequence**: Resolving this bug uncovered the paper's core empirical finding: expanding retrieval context from $k=1$ to $k=5$ caused unfaithful reasoning to surge from 24.81% to 36.29%, proving the reality of distractor accumulation.

### Example 2: Phantom SciFact Download Endpoints (Prompt 08)
- **AI Failure**: The AI initially generated a `curl` download command pointing to a deprecated AllenAI URL (`https://allenai-data-release.s3.amazonaws.com/scifact/...`) which returned an HTTP 403 Forbidden error.
- **Human Detection & Correction**: Rather than allowing the AI to hallucinate alternative endpoints, the human located the authentic download endpoint in the official HuggingFace Datasets `scifact.py` repository: `https://scifact.s3-us-west-2.amazonaws.com/release/latest/data.tar.gz`.
- **Verification**: The 3.1 MB archive was downloaded and unpacked. The human detected that the tar archive extracted into a nested directory `data/data/` with hidden macOS metadata (`._data`). The files were manually moved to root `data/` and verified with MD5 checksums and line counts (300 dev claims, 5,183 corpus abstracts).

### Example 3: The Closed-Book Calibration (ECE) Paradox (Prompt 13 / Prompt 14)
- **AI Limitation**: In the automated evaluation table, the Closed-Book regime showed an Expected Calibration Error (ECE) of **0.0267**, while Oracle Grounding had an ECE of **0.3390**. An uncritical AI could have concluded that "models are 13 times better calibrated when deprived of external scientific literature".
- **Human Critical Scrutiny**: The human recognized this as an artifact of calibration metric geometry. In closed-book mode, the model uniformly outputs low confidence scores ($\approx 0.37$) across all claims, which coincidentally matches the base-rate accuracy of the majority class (37.33%). The calibration bins collapsed to near zero error despite the model producing zero evidence.
- **Correction**: The human mandated that this counter-intuitive result be explicitly flagged in the Peer Review Report (Minor Concern 1) and added an explanatory warning under Table I in `paper/main.tex` to prevent reader misinterpretation.

### Example 4: Lexical Overlap Conflated with Semantic Reasoning (Prompt 16)
- **AI Limitation**: In drafting the methodology and results, the AI repeatedly claimed that R-GEV verified "atomic evidence support" and "grounded reasoning", obscuring the fact that Gate 1 uses a bag-of-words token overlap formula:
  $$\text{Support}(c_i, s) = \frac{|\mathcal{T}(c_i) \cap \mathcal{T}(s)|}{|\mathcal{T}(c_i)|}$$
- **Human Correction**: During the technical peer review, the human forced the AI to confront the reality that token overlap cannot distinguish syntactic negation (e.g., *"drug X failed to inhibit tumor growth"* vs. *"drug X inhibits tumor growth"*). The gate was officially renamed to the **Atomic Lexical Support Gate**, and this lexical boundary was explicitly cited in the Discussion as the direct cause of the residual 16.78% unfaithful reasoning rate.

### Example 5: Markdown Asterisks in LaTeX Code (Prompt 15)
- **AI Error**: The initial draft of `paper/main.tex` contained markdown bolding syntax (`**0.4153**`, `**SciFact**`) embedded in LaTeX paragraphs. In Overleaf, this would compile into literal asterisks rather than bold text.
- **Human Detection & Correction**: A programmatic scan (`Select-String -Pattern "\*\*"`) caught all five instances, which were promptly replaced with standard `\textbf{...}` tags before Overleaf compilation.

---

## 4. Division of Cognitive Labor: Genuine Human Decisions

While AI tools excelled at rapid syntax scaffolding, statistical plotting scripts, and LaTeX formatting, the substantive scientific conclusions of this paper depended entirely on human critical judgment:

1. **Rejection of Multiple-Choice Benchmarks**: The decision to bypass SciQ and TruthfulQA in favor of SciFact was driven by the human insight that multiple-choice tests measure entity memorization and exploit lexical shortcuts, whereas open-domain scientific claim verification requires evaluating evidence attribution.
2. **Adoption of Selective Abstention (Kalai et al., 2026)**: The realization that forced-choice accuracy creates an active incentive to hallucinate was grounded in the human's literature review analysis. Structuring Gate 2 around epistemic confidence thresholding ($\tau$) was a direct conceptual decision, not an automated proposal.
3. **Refusal to Declare "Novelty" for Routine Hyperparameter Tuning**: When selecting Pathway C (R-GEV), the human strictly forbade claiming "novel machine learning architectures", insisting on framing the contribution honestly as an *isolated dual-gating verification protocol* tested under fair ablation conditions.
4. **Honest Reporting of Negative Calibration Findings**: When empirical testing showed that verbalized confidence failed to resolve calibration error (ECE remained 0.3260 with 43 Type IV errors), the human refused to spin this as a success, mandating that it be presented transparently as an honest negative result in Section VII.

---

## 5. Methodological Reflections on "Vibe Coding" in Research

Pair-programming with large language models ("vibe coding") offers enormous productivity gains for research software engineering, but introduces severe epistemic hazards if unmanaged:

- **The Illusion of Running Code**: An LLM will enthusiastically present plausible Python scripts that execute without syntax errors while containing subtle logical flaws (such as the hardcoded `retrieved_docs[0]` bug). "If it runs, it must be right" is a lethal fallacy in empirical research.
- **The Necessity of Short-Cycle Unit Tests**: Vibe coding is only defensible when executed in tight test-driven cycles (Prompt 09 protocol): implement one minimal module, explain input/output tensor shapes, write an independent unit test, and verify actual execution output before moving to the next component.
- **The Risk of Overclaiming in Generated Prose**: LLMs are trained to generate persuasive, confident academic text. Left unchecked, they naturally drift into hyperbole—claiming "state-of-the-art breakthroughs", "comprehensive cross-domain validation", or "solving hallucinations". Rigorous peer review and adversarial prompting are essential to force the prose back into alignment with actual empirical data.

---

## 6. Residual Risks & Epistemic Boundaries

To maintain research integrity, we explicitly acknowledge the residual limitations of this study:
1. **Domain Boundary**: All empirical conclusions are grounded in the biomedical partition of SciFact. Generalization to formal mathematical proofs, software verification, or observational geosciences remains unverified.
2. **Lexical Boundary**: R-GEV's Gate 1 operates as a fast lexical filter. It does not perform deep semantic or syntactic parsing. Resolving subtle negation and polarity inversion will require fine-tuned cross-encoder NLI models.
3. **Confidence Calibration Boundary**: Verbalized LLM confidence scores remain uncalibrated under standard prompting. Deploying selective prediction in high-stakes clinical settings will require formal split-conformal prediction guarantees rather than heuristic thresholding.

---

## 7. Gate G4 Compliance & Readiness Checklist

The five core deliverables required for **Gate G4 (Paper and Reproducibility)** have been audited and verified:

- [x] **Deliverable 1: Paper LaTeX + PDF Source**: Complete, verified IEEEtran manuscript in `paper/main.tex`, `paper/references.bib` (21 verified citations), `paper/evidence_checklist.md`, and 4 publication-quality vector figures in `paper/figures/`.
- [x] **Deliverable 2: GitHub-Ready Repository**: Clean directory structure (`configs/`, `data/`, `src/`, `scripts/`, `results/`, `paper/`), verified `requirements.txt`, environment diagnostics (`scripts/test_env.py`), and updated `README.md` with complete reproduction commands.
- [x] **Deliverable 3: Experimental Evidence Portfolio**: Traceable, non-fabricated result files (`results/master_results.csv`, `results/ablation_results.csv`, `results/summary_metrics.json`, `results/statistical_test_report.json`, and run logs).
- [x] **Deliverable 4: Research Provenance Logs**: Complete, unbroken decision history in `research_decisions.md` (DEC-001 through DEC-019), `ai_assistance_log.md` (Entries 001 through 015), and `ai_provenance_report.md`.
- [x] **Deliverable 5: Viva Demonstration Readiness**: All scripts are executable from the command line (`python scripts/run_ablation_study.py`, `python scripts/evaluate_results.py`); all figures can be reproduced from raw data in under 60 seconds on CPU.
