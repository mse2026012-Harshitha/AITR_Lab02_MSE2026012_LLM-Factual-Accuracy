# Dataset and Baseline Validation Sheet

This document records the official verification of datasets, baselines, comparators, licensing, partition protocols, and data leakage safeguards for Phase II (Prompt 06).

---

## 1. Primary Dataset: SciFact (Wadden et al., 2020)

### Official Source & Hosting
- **Official Repository**: Allen Institute for AI (`allenai/scifact`)
- **Public Hosting**: HuggingFace Datasets (`allenai/scifact`) and direct S3 distribution (`https://scifact.s3.amazonaws.com/`)
- **License**: **CC-BY-4.0** (Creative Commons Attribution 4.0 International). Permitted for open research, reproduction, and modification with appropriate citation.
- **Verification Status**: `[VERIFIED]` from Wadden et al. (2020, EMNLP) and official dataset card.

### File Structure and Schemas
1. **`claims_dev.jsonl`** (300 expert-annotated scientific claims):
   ```json
   {
     "id": 12,
     "claim": "0-dimensional nanocarriers fail to enhance the cellular uptake of anti-cancer drugs.",
     "evidence": {
       "4171202": [
         {
           "sentences": [2, 3],
           "label": "CONTRADICT"
         }
       ]
     },
     "cited_doc_ids": [4171202]
   }
   ```
2. **`corpus.jsonl`** (5,183 scientific abstracts from biomedical literature):
   ```json
   {
     "doc_id": 4171202,
     "title": "Subcellular targeting of nanocarriers for cancer therapy",
     "abstract": [
       "Nanocarriers have emerged as...",
       "Specifically, zero-dimensional nanostructures significantly enhance drug penetration and cellular internalization...",
       "These results demonstrate efficient anti-cancer efficacy."
     ],
     "structured": false
   }
   ```

### Benchmark Protocol & Splits
- **Training Set (`claims_train.jsonl`)**: 809 claims (used for fine-tuning baseline encoders if applicable).
- **Validation Set (`claims_dev.jsonl`)**: 300 claims with complete public gold rationales and stance labels (`SUPPORT`, `CONTRADICT`, `NOT_ENOUGH_INFO`). This is our frozen evaluation split.
- **Test Set (`claims_test.jsonl`)**: Blind evaluation set evaluated via AllenAI private test server.

---

## 2. Baseline Methods & Comparators

### Baseline 1: Closed-Book LLM Stance Predictor (Parametric Control)
- **Methodology**: Direct zero-shot / few-shot prompting of an instruction-tuned model (e.g. `Qwen2.5-7B-Instruct` or `Llama-3.1-8B-Instruct` or `microsoft/deberta-v3-base`) with no access to external literature.
- **Purpose**: Establishes the lower-bound baseline measuring internal parametric memorization and hallucination rates in the absence of evidence.
- **Compute**: ~5–10 minutes for 300 claims.

### Baseline 2: Oracle Context Grounding (Faithfulness Ceiling)
- **Methodology**: The model is provided the exact gold scientific abstract cited in `claims_dev.jsonl` directly in the prompt context.
- **Purpose**: Measures the model's upper-bound capacity to reason faithfully over clean, uncorrupted scientific evidence without retrieval errors.
- **Compute**: ~10–15 minutes for 300 claims.

### Comparator 1: Noisy BM25 Retrieval ($k \in \{1, 3, 5\}$)
- **Methodology**: Sparse lexical retrieval (Rank-BM25 / Lucene) queries the entire 5,183-abstract corpus with the claim text. Top-$k$ abstracts are concatenated into the prompt context.
- **Purpose**: Simulates real-world open scientific RAG pipelines and measures accuracy degradation caused by distractor/irrelevant abstracts.

### Comparator 2: Selective Prediction & Confidence Abstention
- **Methodology**: The model outputs a categorical stance alongside a confidence score $\sigma \in [0, 1]$ (or softmax margin). Claims with confidence $\sigma < \tau$ are classified as `NOT_ENOUGH_INFO` (Abstain).
- **Purpose**: Directly evaluates the Kalai et al. (2026) hypothesis: does allowing explicit abstention eliminate false assertions on uncertain/noisy claims?

---

## 3. Data Leakage & Integrity Safeguards

1. **Document-Level Partition Separation**: The SciFact corpus contains 5,183 unique documents. Evaluation claims in `claims_dev.jsonl` are evaluated strictly against their paired gold citations or the corpus index; no test claims are used during index calibration or prompt tuning.
2. **Fixed Prompt Invariance**: Prompt instructions are frozen prior to running experiments across all three conditions to prevent post-hoc prompt engineering ("prompt leakage").
3. **No Test-Set Tuning**: All hyperparameters (e.g., BM25 parameters $k_1=1.5, b=0.75$, temperature $T=0.0$) are fixed in `configs/` before viewing evaluation predictions.

---

## 4. Independent Verification Checklist

- [ ] `claims_dev.jsonl` verified: exactly 300 claims present with integer IDs and valid labels.
- [ ] `corpus.jsonl` verified: 5,183 JSON entries, each with `doc_id`, `title`, and `abstract` sentence list.
- [ ] Stance labels verified: only `SUPPORT`, `CONTRADICT`, and `NOT_ENOUGH_INFO` exist in ground truth.
- [ ] BM25 index built deterministically with fixed tokenization (whitespace/lowercase/punctuation stripping).
- [ ] Deterministic inference verified: temperature $T = 0.0$ and fixed seed $42$ produces identical outputs across repeated runs.
