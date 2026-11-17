import json

cells = []

def add_md(text):
    cells.append({
        'cell_type': 'markdown',
        'metadata': {},
        'source': [line + '\n' for line in text.strip().split('\n')]
    })

def add_code(code):
    cells.append({
        'cell_type': 'code',
        'execution_count': None,
        'metadata': {},
        'outputs': [],
        'source': [line + '\n' for line in code.strip().split('\n')]
    })

add_md('''# Scientific Claim Verification & Hallucination Mitigation (SciFact Benchmark)
**Author**: Penumala Harshitha (M.Tech, Department of Information Technology, IIIT Allahabad)  
**Project**: AI Tools for Research (Post-Mid-Sem Implementation)  
**Dataset**: SciFact (300 Dev Claims, 5,183 Biomedical Abstracts)

This notebook provides an interactive exploration of the end-to-end research pipeline:
1. Environment setup and package validation
2. Data loading and class distribution analysis
3. BM25 sparse retrieval and distractor inspection
4. R-GEV dual-gating verification logic
5. Visualizing empirical master results and publication figures
''')

add_code('''import sys
import os
import json
import numpy as np
import pandas as pd
from tabulate import tabulate
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Add project root to Python module path
sys.path.append(os.path.abspath('..'))

from src.data_loader import DataLoader
from src.retriever import BM25Retriever
from src.baseline_model import BaselineClaimVerifier
from src.rationale_verifier import RationaleGroundedVerifier
from src.evaluator import ClaimEvaluator

print("All packages and src modules successfully imported!")''')

add_md('''## 1. Data Inspection and Leakage Verification
We load `data/claims_dev.jsonl` (300 evaluation claims) and `data/corpus.jsonl` (5,183 candidate abstracts).
We also verify zero overlap with `data/claims_train.jsonl` (0% data leakage).''')

add_code('''loader = DataLoader()
dev_claims, corpus = loader.load_data('../data/claims_dev.jsonl', '../data/corpus.jsonl')
train_claims, _ = loader.load_data('../data/claims_train.jsonl')

print(f"Dev Claims:    {len(dev_claims)}")
print(f"Train Claims:  {len(train_claims)}")
print(f"Corpus Size:   {len(corpus)} abstracts")

# Audit train-dev leakage
dev_ids = {c['id'] for c in dev_claims}
train_ids = {c['id'] for c in train_claims}
overlap = dev_ids.intersection(train_ids)
assert len(overlap) == 0, "Data leakage detected!"
print("Leakage Check: 0 overlapping claims verified.")

# Stance distribution
stances = {}
for c in dev_claims:
    s = c.get('claim_label', 'NOT_ENOUGH_INFO')
    stances[s] = stances.get(s, 0) + 1
print("\\nGround Truth Stance Distribution in Dev Set:")
for s, count in sorted(stances.items()):
    print(f"  - {s:16s}: {count:3d} ({count/len(dev_claims)*100:.1f}%)")''')

add_md('''## 2. Inspecting BM25 Sparse Retrieval and Distractor Interference
We build the BM25 index over the 5,183 candidate abstracts and query a sample claim to observe how top-k search returns candidate abstracts with high keyword overlap that may act as distractors.''')

add_code('''retriever = BM25Retriever(corpus)
sample_claim = dev_claims[0]
print("Sample Claim ID:", sample_claim['id'])
print("Claim Text:    ", sample_claim['claim'])
print("True Label:    ", sample_claim['claim_label'])
print("Gold Cited Doc:", sample_claim.get('cited_doc_ids'))

retrieved = retriever.retrieve(sample_claim['claim'], top_k=3)
print(f"\\nTop-3 BM25 Retrieved Documents:")
for rank, (doc_id, score) in enumerate(retrieved, 1):
    doc = corpus[doc_id]
    title = doc.get('title', 'No Title')
    print(f"  [Rank {rank}] Doc ID: {doc_id} | Score: {score:.3f} | Title: {title[:70]}...")''')

add_md('''## 3. Comparing Baseline Decision vs. R-GEV Dual-Gating
Here we demonstrate the core algorithmic difference between:
1. **Unmodified Baseline**: Forces a prediction on the top candidate abstract without evidence support gating.
2. **R-GEV Dual-Gating**: Applies atomic lexical support ($\\\\theta = 0.35$) and confidence thresholding ($\\\\tau = 0.70$), converting ungrounded predictions into disciplined abstention (`NOT_ENOUGH_INFO`).''')

add_code('''baseline = BaselineClaimVerifier()
rgev = RationaleGroundedVerifier(theta=0.35, tau=0.70)

retrieved_docs = [corpus[doc_id] for doc_id, _ in retrieved]
raw_pred = baseline.classify_and_extract(sample_claim['claim'], retrieved_docs, k=3)
gated_pred = rgev.verify_and_gate(sample_claim['claim'], raw_pred, retrieved_docs)

print("=== Unmodified Baseline Output ===")
print("  Predicted Stance: ", raw_pred['stance'])
print("  Raw Confidence:   ", f"{raw_pred['confidence']:.3f}")
print("  Extracted Sentence:", raw_pred['extracted_rationale'][:100] + "...")

print("\\n=== R-GEV Dual-Gated Output ===")
print("  Effective Stance: ", gated_pred['effective_stance'])
print("  Support Ratio:    ", f"{gated_pred['support_ratio']:.3f}")
print("  Gate 1 Support:   ", "PASS" if gated_pred['support_passed'] else "FAIL (Distractor Filtered)")
print("  Gate 2 Confidence:", "PASS" if gated_pred['confidence_passed'] else "FAIL (Abstained)")''')

add_md('''## 4. Master Empirical Results Summary
We load the immutable evaluation results from `results/master_results.csv` and display the cross-regime and ablation comparisons.''')

add_code('''results_df = pd.read_csv('../results/master_results.csv')
print(tabulate(results_df, headers='keys', tablefmt='psql', showindex=False))''')

add_md('''## 5. Visualizing Publication Figures
We display the four publication figures generated during the evaluation phase:
- **Figure 1**: Four-Arm Ablation Comparison (Macro-F1, Accuracy, Unfaithful Rate)
- **Figure 2**: Distractor-Induced Unfaithful Reasoning Suppression
- **Figure 3**: Selective Prediction Risk-Coverage Curve (Kalai et al., 2026)
- **Figure 4**: Confusion Matrix Heatmaps (Baseline Over-Assertion vs. R-GEV Abstention)''')

add_code('''fig, axes = plt.subplots(2, 2, figsize=(16, 14))

img1 = mpimg.imread('../results/fig1_ablation_comparison.png')
axes[0, 0].imshow(img1)
axes[0, 0].set_title('Figure 1: 4-Arm Ablation Comparison', fontsize=14, fontweight='bold')
axes[0, 0].axis('off')

img2 = mpimg.imread('../results/fig2_unfaithful_suppression.png')
axes[0, 1].imshow(img2)
axes[0, 1].set_title('Figure 2: Unfaithful Reasoning Suppression', fontsize=14, fontweight='bold')
axes[0, 1].axis('off')

img3 = mpimg.imread('../results/fig3_risk_coverage_curve.png')
axes[1, 0].imshow(img3)
axes[1, 0].set_title('Figure 3: Selective Prediction Risk-Coverage Curve', fontsize=14, fontweight='bold')
axes[1, 0].axis('off')

img4 = mpimg.imread('../results/fig4_confusion_matrices.png')
axes[1, 1].imshow(img4)
axes[1, 1].set_title('Figure 4: Baseline vs. R-GEV Confusion Matrices', fontsize=14, fontweight='bold')
axes[1, 1].axis('off')

plt.tight_layout()
plt.show()''')

add_md('''## 6. Key Takeaways
1. **Distractor Accumulation**: Expanding retrieval window from $k=1$ to $k=5$ drives unfaithful reasoning from 24.81% to 36.29%.
2. **R-GEV Dual-Gating**: Decoupling lexical support ($\\\\theta=0.35$) from confidence thresholding ($\\\\tau=0.70$) boosts Macro-F1 from 0.2719 to **0.4153** (+52.7% relative gain, paired bootstrap $p < 0.001$) and halves unfaithful reasoning to **16.78%**.
3. **Selective Prediction**: Restricting answering to high confidence ($\\\\tau \\\\ge 0.80$) raises accuracy to **58.65%** compared to 41.14% under forced choice, validating Kalai et al. (2026).
4. **Honest Negative Finding**: Verbalized confidence alone does not resolve overconfidence (ECE remains 0.3260 with 43 Type IV errors), proving the need for formal conformal prediction.
''')

nb = {
    'cells': cells,
    'metadata': {
        'language_info': {
            'name': 'python',
            'version': '3.13.7'
        }
    },
    'nbformat': 4,
    'nbformat_minor': 2
}

with open('notebooks/exploration_and_demonstration.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=2)

print('Successfully created notebooks/exploration_and_demonstration.ipynb')
