# Dataset Validation Record

**Project**: Benchmarking Factual Accuracy of Large Language Models Across Scientific Domains  
**Primary Dataset Selected**: SciFact (Wadden et al., 2020)  
**Verification Date**: 2026-11-16  
**Status**: VERIFIED & FROZEN (Pending Student Download Authorization)

---

## 1. Specification and Metadata

| Attribute | Verified Value | Verification Source |
|---|---|---|
| **Dataset Name** | SciFact: Fact or Fiction: Verifying Scientific Claims | Wadden et al. (2020, EMNLP) |
| **Official Repository** | `https://github.com/allenai/scifact` | Allen Institute for AI |
| **Official HuggingFace Card** | `https://huggingface.co/datasets/allenai/scifact` | HuggingFace Hub |
| **License** | Creative Commons Attribution 4.0 International (CC-BY-4.0) | Official Dataset Metadata |
| **Domain** | Biomedical & Life Sciences Literature (PubMed) | Primary Publication |
| **Task Category** | Scientific Claim Verification & Rationale Extraction | Benchmark Specification |
| **Ground Truth Stance Labels** | `SUPPORT`, `CONTRADICT`, `NOT_ENOUGH_INFO` | `claims_dev.jsonl` Schema |
| **Corpus Size** | 5,183 Scientific Abstracts | `corpus.jsonl` Schema |
| **Evaluation Set Size** | 300 Expert-Annotated Claims | `claims_dev.jsonl` Schema |

---

## 2. Compatibility & Integrity Verification

1. **Task Compatibility**: Matches the requirements of Gate G1, Gate G2, and Gate G3. Enables measuring:
   - Stance Macro-F1 across 3 classes.
   - Sentence-level rationale overlap (Token F1 / Rationale Recall).
   - Abstention performance on claims labeled `NOT_ENOUGH_INFO`.
2. **Leakage Safety**: The 300 dev claims are isolated from the corpus text. Retrieval is evaluated against the 5,183-abstract corpus, mirroring realistic RAG conditions without test-set contamination.
3. **Download State**: **HELD** — Pending student confirmation per instruction.
