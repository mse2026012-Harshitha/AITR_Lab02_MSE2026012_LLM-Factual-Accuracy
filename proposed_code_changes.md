# Proposed Code Changes Specification (Prompt 12)

**Status**: SPECIFICATION ONLY (No code will be executed or modified until student approval)  
**Author**: Penumala Harshitha (M.Tech, IIIT Allahabad)  
**Date**: 2026-11-17  

---

## 1. Code Preservation Principle

In strict compliance with Course Guidelines (§3, Pathway C) and your instructions:
* **The original baseline code remains 100% UNTOUCHED**:
  * `src/data_loader.py` — Unmodified.
  * `src/retriever.py` — Unmodified.
  * `src/baseline_model.py` — Unmodified.
  * `src/abstention.py` — Unmodified.
  * `src/evaluator.py` — Unmodified.
  * `scripts/run_baseline.py` — Preserved as the historical baseline executable.

All proposed modifications are implemented strictly as **new, modular, non-destructive files**.

---

## 2. New File 1: `src/rationale_verifier.py`

### Proposed Architecture & Logic:
```python
"""
Rationale-Grounded Evidence Verifier (R-GEV) Module
Acts as an isolated pre-classification verification gatekeeper.
"""
from typing import Dict, List, Any, Tuple

class RationaleGroundedVerifier:
    def __init__(self, theta_threshold: float = 0.35):
        """
        theta_threshold: Minimum atomic evidence support score required
        to accept an extracted rationale sentence as valid evidence.
        """
        self.theta_threshold = theta_threshold

    def verify_and_gate(self, prediction: Dict[str, Any], candidate_sentence_overlap: float) -> Dict[str, Any]:
        """
        Decision Rule:
        If overlap < theta_threshold:
            Override stance to 'NOT_ENOUGH_INFO' (Evidence insufficient/distractor)
            Set rationale_verified = False
        Else:
            Retain predicted stance
            Set rationale_verified = True
        """
        gated_pred = dict(prediction)
        if candidate_sentence_overlap < self.theta_threshold:
            gated_pred["effective_stance"] = "NOT_ENOUGH_INFO"
            gated_pred["rationale_verified"] = False
            gated_pred["gating_reason"] = "Sub-threshold atomic evidence (Distractor rejected)"
        else:
            gated_pred["rationale_verified"] = True
            gated_pred["gating_reason"] = "Evidence verified"
            
        return gated_pred
```

---

## 3. New File 2: `scripts/run_ablation_study.py`

### Purpose:
Executes the frozen 4-Arm Ablation Study:
* **Arm 1**: Unmodified Baseline (BM25 $k=3, 5$)
* **Arm 2**: Baseline + Confidence Thresholding only ($\tau = 0.70$)
* **Arm 3**: Baseline + Rationale-Grounded Verification only ($\theta = 0.35$)
* **Arm 4**: Proposed Dual-Gated R-GEV ($\theta = 0.35$ AND $\tau = 0.70$)

Outputs generated:
* `results/ablation_results.csv`
* `results/ablation_metrics.json`
* Automated comparative markdown tables and ablation bar chart data.

---

## 4. Verification and Safeguards
1. **Zero Data Leakage**: Evaluates the identical, frozen `claims_dev.jsonl` (300 items) and BM25 index.
2. **Determinism**: Same random seed (`42`) and temperature (`0.0`).
3. **Rollback Safety**: Since all changes are contained in new files, deleting `src/rationale_verifier.py` and `scripts/run_ablation_study.py` immediately restores the repository to its exact baseline state.
