# Dataset Selection Report: Benchmarking Factual Accuracy of LLMs Across Scientific Domains

**Author**: Penumala Harshitha (M.Tech, IIIT Allahabad)  
**Date**: 2026-11-16  
**Document Status**: Investigation Report for Student Review & Approval (Pre-Download)

---

## 1. Comparative Investigation of Candidate Datasets

We investigate the four candidate datasets strictly using their primary research papers, official repositories, and formal documentation:
1. **SciFact** (Wadden et al., 2020, EMNLP)
2. **PubMedQA** (Jin et al., 2019, EMNLP-IJCNLP)
3. **SciQ** (Welbl et al., 2017, CoNLL)
4. **TruthfulQA** (Lin et al., 2022, ACL)

---

### Dataset 1: SciFact (Wadden et al., 2020)

- **Domain Covered**: Biomedical and Life Sciences (oncology, genetics, pharmacology, virology, immunology).
- **Type of Factual Accuracy Measured**: **Evidence-Grounded Scientific Claim Verification & Stance Fidelity**. It tests whether a model can determine if scientific literature `SUPPORTS`, `CONTRADICTS`, or provides `NOT_ENOUGH_INFO` for a claim, and whether it can extract the exact sentence-level rationale.
- **Samples and Splits**:
  - Total Claims: 1,409 expert-written scientific claims derived from PubMed abstracts.
  - Candidate Research Corpus: 5,183 scientific abstracts from PubMed/Semantic Scholar.
  - Splits: Train (809 claims), Validation/Dev (300 claims with full gold rationales and stance labels), Test (300 claims held blind on private leaderboard).
- **Official Download Location**:
  - Direct S3 Bucket: `https://scifact.s3.amazonaws.com/claims_dev.jsonl` and `https://scifact.s3.amazonaws.com/corpus.jsonl`
  - GitHub: `https://github.com/allenai/scifact`
  - HuggingFace Datasets: `allenai/scifact`
- **License & Access Conditions**: **CC-BY-4.0** (Free, open access for research and modification with attribution). No authentication keys required.
- **Evaluation Metrics & Procedure**:
  - Abstract-Level Stance Macro-F1 across `SUPPORT`, `CONTRADICT`, `NOT_ENOUGH_INFO`.
  - Sentence-Level Rationale Selection (Precision, Recall, F1).
  - Evaluated on claims with gold abstracts (oracle) or open corpus retrieval.
- **Suitability for Comparing Multiple LLMs**: **Excellent**. Can be formatted cleanly into zero-shot, few-shot, or chain-of-thought prompts for any LLM (open or proprietary) as well as fine-tuned neural encoders.
- **Feasibility on Limited Compute**: **Very High**. Evaluating 300 dev claims against candidate abstracts takes < 15 minutes on a standard CPU or free Colab GPU.
- **Literature Review Overlap**: Directly highlighted in your literature review (§2.3, §3.5, §6.4, §7; Figure 3).

---

### Dataset 2: PubMedQA (Jin et al., 2019)

- **Domain Covered**: Clinical Medicine and Biomedical Research.
- **Type of Factual Accuracy Measured**: **Biomedical Abstract-Grounded Question Answering**. Models read a PubMed abstract and answer a specific research question with `yes`, `no`, or `maybe`, along with a long-form rationale.
- **Samples and Splits**:
  - Expert-Annotated Subset (PQA-L): 1,000 QA pairs labeled by medical experts (standard 500 train / 500 test split or 10-fold cross validation).
  - Unlabeled / Artificial: 61.2k unannotated (PQA-U) and 211.3k automatically generated (PQA-A).
- **Official Download Location**:
  - GitHub: `https://github.com/pubmedqa/pubmedqa`
  - HuggingFace Datasets: `pubmed_qa` (subset: `pqa_labeled`)
- **License & Access Conditions**: **MIT License** (Fully open and permissive).
- **Evaluation Metrics & Procedure**:
  - Accuracy and Macro-F1 across 3 classes (`yes` / `no` / `maybe`).
- **Suitability for Comparing Multiple LLMs**: **High**. Provides a clean clinical reasoning task with a natural abstention/uncertainty class (`maybe`).
- **Feasibility on Limited Compute**: **Very High**. 500 test samples can be evaluated rapidly.
- **Limitation for Our Core Question**: The abstract is always given directly in the prompt (closed context). It does not test corpus-level literature retrieval noise or open-domain degradation unless combined with external PubMed retrieval.

---

### Dataset 3: SciQ (Welbl et al., 2017)

- **Domain Covered**: General Elementary and Middle-School Science (General Physics, Chemistry, Biology, Earth Science).
- **Type of Factual Accuracy Measured**: **Multiple-Choice Fact Recall**. 4-option multiple-choice questions crowdsourced from textbook materials, each with an 80-word supporting passage.
- **Samples and Splits**:
  - Total: 13,679 questions.
  - Splits: Train (11,679), Validation (1,000), Test (1,000).
- **Official Download Location**:
  - AllenAI: `https://allenai.org/data/sciq`
  - HuggingFace Datasets: `allenai/sciq`
- **License & Access Conditions**: **CC-BY-NC-3.0** (Non-commercial research).
- **Evaluation Metrics & Procedure**: Top-1 Multiple Choice Accuracy.
- **Suitability for Comparing Multiple LLMs**: High for basic benchmarking, but **poor for scientific research rigor**.
- **Why It Fails Our Research Goal**:
  1. As emphasized in your Literature Review (§2.2, p. 3): multiple-choice educational questions *"do not reflect the complexity of scientific research today"* and allow models to guess using lexical overlap heuristics without scientific reasoning.
  2. It does not measure citation validity, abstention, or complex contradiction.

---

### Dataset 4: TruthfulQA (Lin et al., 2022)

- **Domain Covered**: Broad General Knowledge across 38 categories (Health, Law, History, Finance, Psychology, Science). Only a small minority (~10%) is STEM/science-related.
- **Type of Factual Accuracy Measured**: **Resistance to Human Misconceptions & Myth-busting**. Tests whether models parrot widespread human falsehoods vs. true facts.
- **Samples and Splits**: 817 questions total; no standard train/test split (designed as a zero-shot benchmark).
- **Official Download Location**:
  - GitHub: `https://github.com/sylinrl/TruthfulQA`
  - HuggingFace Datasets: `truthful_qa`
- **License & Access Conditions**: **Apache-2.0** (Open and permissive).
- **Evaluation Metrics & Procedure**:
  - Multiple Choice (MC1 / MC2 accuracy).
  - Generative: Automated GPT-judge fine-tuned on human truthfulness/informativeness annotations.
- **Suitability for Comparing Multiple LLMs**: High for general alignment, but **unsuitable as a primary scientific benchmark**.
- **Why It Fails Our Research Goal**:
  1. It is not domain-stratified scientific literature; it focuses on common urban myths and misconceptions.
  2. It lacks supporting research abstracts or literature citation verification.

---

## 2. Comparative Assessment Matrix

| Candidate Dataset | Primary Scientific Domain | Task Formulation | Evidence Grounded? | Includes Abstention Class? | Compute Feasibility | Alignment with Research Question |
|---|---|---|:---:|:---:|:---:|:---:|
| **SciFact** | Biomedical / Life Sciences | Claim Verification & Rationale Extraction | **Yes** (Corpus of 5,183 abstracts) | **Yes** (`NOT_ENOUGH_INFO`) | **Very High** (300 dev claims) | **Optimal (Primary)** |
| **PubMedQA** | Clinical Medicine | Context-based QA (`yes`/`no`/`maybe`) | Yes (Single Abstract) | **Yes** (`maybe`) | **Very High** (500 test items) | **Strong (Secondary/Validation)** |
| **SciQ** | Grade-School Science | 4-way Multiple Choice | Minimal (Short snippet) | No | High | **Low (Unsuitable)** |
| **TruthfulQA** | General Knowledge / Misconceptions | Open QA / MC | No | No | Moderate | **Low (Out of Domain)** |

---

## 3. Official Scientific Recommendation

### Recommended Primary Dataset: **SciFact** (Wadden et al., 2020)
* **Scientific Justification**:
  1. **Direct Alignment with Research Question**: Our study evaluates how retrieval noise affects stance accuracy and rationale faithfulness. SciFact is the only benchmark that pairs claims with both an isolated oracle abstract and an open corpus of 5,183 scientific abstracts.
  2. **Fine-Grained Evidence Faithfulness**: In addition to stance accuracy (`SUPPORT`/`CONTRADICT`), it includes sentence-level rationale annotations, allowing us to measure whether the model got the "right answer for the right scientific reason" (RQ3).
  3. **Natural Abstention Mechanism**: The presence of `NOT_ENOUGH_INFO` enables rigorous testing of the Kalai et al. (2026) hypothesis (selective prediction without artificial class mapping).
  4. **Strict Compute Feasibility**: 300 validation claims can be processed deterministically in minutes, perfectly suited for reproducible student research on accessible hardware.

### Optional Secondary Benchmark (If Justified Later): **PubMedQA**
* *Scope Boundary*: PubMedQA can serve in Phase IV as an out-of-domain clinical robustness check on medical QA, but should NOT be merged with SciFact into an arbitrary combined score because its task structure (question answering) differs fundamentally from claim verification.

---

## 4. Exact Official Download Instructions (To Be Executed After Approval)

When approved, the official SciFact files can be acquired via any of the following standard, verified paths:

### Method A (Direct Official S3 Download via PowerShell):
```powershell
Invoke-WebRequest -Uri "https://scifact.s3.amazonaws.com/claims_dev.jsonl" -OutFile "data/claims_dev.jsonl"
Invoke-WebRequest -Uri "https://scifact.s3.amazonaws.com/corpus.jsonl" -OutFile "data/corpus.jsonl"
```

### Method B (Via HuggingFace Datasets Python API):
```python
from datasets import load_dataset
scifact_claims = load_dataset("allenai/scifact", "claims")
scifact_corpus = load_dataset("allenai/scifact", "corpus")
```

---

> [!CAUTION]
> **No files will be downloaded or modified until your explicit approval of this dataset selection report.**
