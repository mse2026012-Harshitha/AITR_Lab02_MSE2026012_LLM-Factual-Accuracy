# Benchmarking Scientific Claim Verification and Hallucination Mitigation under Distractor Accumulation and Selective Abstention

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Benchmark: SciFact](https://img.shields.io/badge/benchmark-SciFact-green.svg)](https://scifact.allenai.org/)
[![Reproducibility: Seed 42](https://img.shields.io/badge/reproducibility-seed_42-orange.svg)]()

**Author**: Penumala Harshitha (M.Tech, Department of Information Technology, IIIT Allahabad)  
**Email**: `mse2024012@iiita.ac.in`  
**Course**: AI Tools for Research (Post-Mid-Sem Implementation Project)  
**Manuscript**: Prepared for Overleaf in `paper/main.tex` (IEEEtran journal style)  

---

## 1. Project Overview

While Large Language Models (LLMs) demonstrate remarkable fluency in summarizing complex scientific literature, fluency does not ensure factual accuracy. In specialized biomedical domains, models frequently generate unsubstantiated statements, hallucinate unbacked assertions, and cite irrelevant evidence. Furthermore, standard accuracy evaluation penalizes uncertainty, mathematically incentivizing models to output low-confidence hallucinations rather than abstaining (Kalai et al., 2026, *Nature*).

This repository implements a fully reproducible empirical benchmark and mitigation framework evaluating claim verification on the expert-annotated **SciFact** dataset (300 evaluation claims, 5,183 candidate biomedical research abstracts):

1. **Distractor Accumulation**: We empirically demonstrate that expanding sparse BM25 retrieval depth from $k=1$ to $k=5$ degrades Stance Macro-F1 from 0.3273 to 0.2719 and causes the **Unfaithful Reasoning Rate** to surge from 24.81% to 36.29%, showing that over one-third of correct answers rely on irrelevant distractor rationales.
2. **Rationale-Grounded Evidence Verification (R-GEV)**: We introduce an isolated dual-gated verification architecture coupling an atomic lexical support filter ($\theta = 0.35$) with selective confidence abstention ($\tau = 0.70$).
3. **Statistical Significance**: Dual-Gated R-GEV boosts Stance Macro-F1 to **0.4153** (+52.7% relative gain over baseline, paired bootstrap $p < 0.001$, 95% CI: $[0.0934, 0.1920]$) and slashes unfaithful reasoning down to **16.78%**. Under selective prediction, claims answered at high confidence ($\tau \ge 0.80$) achieve **58.65% accuracy** (vs. 41.14% forced-choice).

---

## 2. Master Empirical Results

All metrics evaluated on the official SciFact validation set ($N = 300$ claims, 5,183 abstracts; random seed 42):

| Evaluation Regime / Arm | Description | Stance Macro-F1 ($\uparrow$) | Stance Accuracy ($\uparrow$) | Rationale Token-F1 ($\uparrow$) | Unfaithful Reasoning ($\downarrow$) | ECE ($\downarrow$) |
|---|---|:---:|:---:|:---:|:---:|:---:|
| **Closed-Book** | No external literature access ($d = \emptyset$) | 0.1812 | 0.3733 | 0.0000 | 0.00% | 0.0267* |
| **Oracle Evidence** | Exact gold cited abstract provided | **0.4266** | **0.5033** | **0.4550** | **1.99%** | 0.3390 |
| **BM25 ($k=1$)** | Top-1 sparse retrieved abstract | 0.3273 | 0.4433 | 0.3300 | 24.81% | 0.3504 |
| **Arm 1: BM25 ($k=3$)** | Unmodified Baseline (Control) | 0.2719 | 0.4133 | 0.3075 | 33.06% | 0.3578 |
| **BM25 ($k=5$)** | Distractor accumulation peak | 0.2719 | 0.4133 | 0.2975 | **36.29%** | 0.3500 |
| **Arm 2: Conf-Only** | Selective abstention only ($\tau = 0.70$) | 0.3443 | 0.4333 | 0.3075 | 20.00% | 0.3378 |
| **Arm 3: Rationale-Only** | Lexical support gating only ($\theta = 0.35$) | 0.4054 | 0.4900 | 0.3075 | 25.85% | 0.3327 |
| **Arm 4: Dual R-GEV** | Proposed dual-gated architecture ($\theta=0.35, \tau=0.70$) | **0.4153** | **0.4967** | **0.3075** | **16.78%** | **0.3260** |

*\*Note: Closed-Book ECE is an evaluation metric artifact caused by uniform low-confidence predictions ($\approx 0.37$) matching dataset base-rate accuracy.*

---

## 3. Repository Structure

```text
ATR-IMPLEMENTATION/
├── configs/
│   └── experiment_blueprint.md          # Frozen experimental protocol, equations, metrics
├── data/
│   ├── claims_dev.jsonl                 # SciFact evaluation claims (300 items)
│   ├── claims_train.jsonl               # SciFact training claims (809 items; leakage audited)
│   ├── corpus.jsonl                     # 5,183 scientific research abstracts
│   ├── dataset_selection_report.md      # Multi-dataset comparison (SciFact vs PubMedQA vs SciQ vs TruthfulQA)
│   └── dataset_and_baseline_validation.md # Schema, licensing, and leakage checklist
├── notebooks/                           # Exploratory inspection notebooks
├── src/                                 # Core modular Python packages
│   ├── data_loader.py                   # Verified JSONL parser and integrity validator
│   ├── retriever.py                     # Okapi BM25 sparse retrieval engine
│   ├── baseline_model.py                # Multi-document evidence verification and stance model
│   ├── abstention.py                    # Selective prediction and confidence thresholding engine
│   ├── evaluator.py                     # Multi-dimensional evaluation metrics (Macro-F1, F1, ECE)
│   └── rationale_verifier.py            # Isolated R-GEV dual-gating implementation
├── scripts/                             # Executable command-line scripts
│   ├── test_env.py                      # Environment and dependency sanity check
│   ├── run_baseline.py                  # Baseline execution across 5 information regimes
│   ├── run_ablation_study.py            # 4-arm ablation study execution and plot generation
│   ├── evaluate_results.py              # Pre-evaluation audit, bootstrap testing ($B=2,000$), heatmaps
│   └── test_debug_fix.py                # Regression unit test for multi-document context passing
├── results/                             # Immutable experimental data and figures
│   ├── baseline_results.csv             # Raw per-claim baseline predictions
│   ├── comparative_results.csv          # Per-claim predictions across 5 information regimes
│   ├── ablation_results.csv             # Raw per-claim predictions across 4 ablation arms
│   ├── master_results.csv               # Unified master experimental output table
│   ├── summary_metrics.json             # Key summary statistics
│   ├── statistical_test_report.json     # Paired bootstrap significance report ($p < 0.001$)
│   ├── fig1_ablation_comparison.pdf/.png
│   ├── fig2_unfaithful_suppression.pdf/.png
│   ├── fig3_risk_coverage_curve.pdf/.png
│   └── fig4_confusion_matrices.pdf/.png
├── paper/                               # Publication package
│   ├── main.tex                         # Complete IEEEtran LaTeX manuscript
│   ├── references.bib                   # 21 verified primary citations
│   ├── evidence_checklist.md            # Mapping every claim in paper to raw data files
│   ├── peer_review_report.md            # Critical technical peer review audit (Prompt 16)
│   ├── manuscript_revision_log.md       # Audit of manuscript revisions
│   └── figures/                         # Vector PDF and 300 DPI PNG figures for paper
├── requirements.txt                     # Pinned, tested dependencies
├── research_decisions.md                # Unbroken decision log (DEC-001 through DEC-019)
├── ai_assistance_log.md                 # Complete AI-human collaboration log
├── ai_provenance_report.md              # Research integrity and AI provenance audit (Gate G4)
└── README.md                            # Complete reproduction documentation
```

---

## 4. Environment Setup & Hardware Specifications

### Hardware Requirements
- **Tested Environment**: Standard academic workstation / laptop (Windows 11 / Linux / macOS).
- **CPU**: Standard x86_64 or Apple Silicon CPU (local evaluation does not require a discrete GPU).
- **RAM**: Minimum 4 GB RAM (peak memory consumption during BM25 indexing is ~450 MB).
- **Execution Time**: The complete 4-arm ablation study and bootstrap test over 300 claims runs in **under 45 seconds** on standard CPU.

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/penumala-harshitha/ATR-IMPLEMENTATION.git
   cd ATR-IMPLEMENTATION
   ```

2. Create and activate a clean virtual environment (Python 3.10+):
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Linux/macOS:
   source venv/bin/activate
   ```

3. Install verified dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```

4. Run environment diagnostic:
   ```bash
   python scripts/test_env.py
   ```
   *Expected output*: `Environment verification SUCCESSFUL! Seed determinism verified.`

---

## 5. Reproduction Protocol for a Second Student

Follow these sequential steps to reproduce all empirical tables, statistical tests, and publication figures from scratch:

### Step 1: Verify Dataset Integrity & Data Leakage
```bash
python -c "
import json
dev = [json.loads(line)['id'] for line in open('data/claims_dev.jsonl')]
train = [json.loads(line)['id'] for line in open('data/claims_train.jsonl')]
overlap = set(dev).intersection(set(train))
assert len(overlap) == 0, 'Data leakage detected!'
print(f'SUCCESS: Verified 0 overlapping claims. Dev={len(dev)}, Train={len(train)}.')
"
```

### Step 2: Run Baseline Across 5 Information Regimes
```bash
python scripts/run_baseline.py
```
*Output*: Generates `results/baseline_results.csv` and `results/comparative_results.csv`. Confirms Oracle Macro-F1 = 0.4266 and BM25 $k=3$ Macro-F1 = 0.2719.

### Step 3: Run the 4-Arm Ablation Study
```bash
python scripts/run_ablation_study.py
```
*Output*: Executes Arms 1–4, validates Dual-Gated R-GEV Macro-F1 = 0.4153, and exports `fig1_ablation_comparison.pdf` and `fig2_unfaithful_suppression.pdf`.

### Step 4: Run Statistical Significance & Evaluation Engine
```bash
python scripts/evaluate_results.py
```
*Output*:
- Executes paired bootstrap resampling ($B = 2,000$).
- Proves statistical significance ($p < 0.001$, 95% CI: $[0.0934, 0.1920]$).
- Generates `results/master_results.csv` and `results/statistical_test_report.json`.
- Exports `fig3_risk_coverage_curve.pdf` and `fig4_confusion_matrices.pdf`.

### Step 5: Verify Output Values
Open `results/master_results.csv` and confirm that all values match Section 2 of this README exactly.

---

## 6. Research Decisions and Academic Integrity

This project complies strictly with the academic integrity guidelines of IIIT Allahabad and the AI Tools for Research course. All AI assistance was logged transparently:
- **Decision Provenance**: Consult [research_decisions.md](research_decisions.md) for all 19 formal decisions and gate sign-offs.
- **AI Interaction Log**: Consult [ai_assistance_log.md](ai_assistance_log.md) for authentic prompts, proposals, human decisions, and verification steps.
- **AI Audit Report**: Consult [ai_provenance_report.md](ai_provenance_report.md) for a detailed audit of real errors, debugging notes, and cognitive division of labor.

---

## 7. Citation

If you use this benchmark or the R-GEV framework in your research, please cite:

```bibtex
@article{harshitha2026benchmarking,
  author    = {Penumala Harshitha},
  title     = {Benchmarking Scientific Claim Verification and Hallucination Mitigation under Distractor Accumulation and Selective Abstention: An Empirical Study on Biomedical Literature},
  journal   = {Department of Information Technology, Indian Institute of Information Technology, Allahabad},
  year      = {2026},
  note      = {M.Tech Research Implementation Project}
}
```
