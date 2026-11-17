# SciFact Benchmark Dataset: Access & Documentation

This directory documents the benchmark dataset used in this study: **SciFact** (Wadden et al., EMNLP 2020), an expert-annotated corpus for verifying scientific assertions against peer-reviewed biomedical literature.

---

## 1. Dataset Overview

- **Source Corpus**: Research abstracts from PubMed and semantic search indexing.
- **Evaluation Task**: Given a scientific claim $c_i$ and a candidate corpus of research abstracts $\mathcal{D}$, retrieve relevant documents, select sentence-level rationales $\hat{R}_i$, and predict a categorical stance $\hat{S}_i \in \{\textsc{Support}, \textsc{Contradict}, \textsc{Not\_Enough\_Info}\}$.
- **License**: Creative Commons Attribution 4.0 International (CC-BY-4.0).
- **Official Repository**: [https://github.com/allenai/scifact](https://github.com/allenai/scifact)
- **Primary Publication**: Wadden et al., *"Fact or Fiction: Verifying Scientific Claims"*, EMNLP 2020.

---

## 2. Partition Splits & Dataset Schema

| Partition File | Sample Count | Format | Description |
|---|:---:|:---:|---|
| `data/claims_dev.jsonl` | 300 claims | JSON Lines | Official evaluation/validation partition evaluated in this benchmark. |
| `data/claims_train.jsonl` | 809 claims | JSON Lines | Training claims partition (used exclusively for leakage auditing; 0% overlap). |
| `data/claims_test.jsonl` | 339 claims | JSON Lines | Blind test set (unlabeled stances; evaluated on AllenAI leaderboard). |
| `data/corpus.jsonl` | 5,183 abstracts | JSON Lines | Target scientific corpus indexed via BM25 Okapi for open-domain retrieval. |

### Claim Record Schema (`claims_dev.jsonl`):
```json
{
  "id": 1,
  "claim": "0-dimensional biomaterials show inductive properties.",
  "evidence": {
    "31715818": [
      {
        "sentences": [4],
        "label": "SUPPORT"
      }
    ]
  },
  "cited_doc_ids": [31715818]
}
```

### Corpus Record Schema (`corpus.jsonl`):
```json
{
  "doc_id": 31715818,
  "title": "Real-time observation of carbon dots driving cellular differentiation...",
  "abstract": [
    "Sentence 0 text...",
    "Sentence 1 text...",
    "Sentence 4 text demonstrating inductive properties."
  ],
  "structured": false
}
```

---

## 3. Official Acquisition & Extraction Instructions

To download the verified, authentic SciFact release from the official AllenAI AWS S3 endpoint:

```bash
# 1. Download official release archive (3.1 MB)
curl -o data.tar.gz https://scifact.s3-us-west-2.amazonaws.com/release/latest/data.tar.gz

# 2. Extract archive
tar -xzf data.tar.gz

# 3. Verify files and move to data/ directory if nested
# Required files: claims_dev.jsonl (300 lines), corpus.jsonl (5,183 lines)
```

---

## 4. Integrity and Leakage Controls

Prior to benchmark execution, data integrity was programmatically verified:
1. **0% Train-Dev Overlap**:
   ```python
   import json
   dev_ids = {json.loads(l)["id"] for l in open("data/claims_dev.jsonl")}
   train_ids = {json.loads(l)["id"] for l in open("data/claims_train.jsonl")}
   assert len(dev_ids.intersection(train_ids)) == 0, "Data leakage detected!"
   ```
2. **Deterministic Preprocessing**: Whitespace normalization and lowercased alphanumeric tokenization are applied uniformly across all evaluation scripts without test-set tuning.
