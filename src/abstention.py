"""
Selective Prediction and Confidence-Based Abstention Filter (Module 4)
Author: Penumala Harshitha (M.Tech, IIIT Allahabad)
Project: Benchmarking Factual Accuracy of LLMs Across Scientific Domains

Theoretical Grounding:
Kalai et al. (2026, Nature): Forcing language models to answer under high uncertainty
incentivizes hallucination. This module implements selective prediction by introducing
an explicit abstention threshold tau:
  y_selective = y_pred if confidence >= tau else 'NOT_ENOUGH_INFO'
"""

from typing import List, Dict, Any, Tuple
import numpy as np

class SelectiveAbstentionFilter:
    def __init__(self, default_tau: float = 0.50):
        self.default_tau = default_tau

    def apply_threshold(self, predictions: List[Dict[str, Any]], tau: float) -> List[Dict[str, Any]]:
        """
        Applies confidence threshold tau to a list of prediction instances.
        If confidence < tau, the prediction is mapped to 'NOT_ENOUGH_INFO' (Abstained).
        """
        filtered_preds = []
        for pred in predictions:
            conf = pred.get("confidence", 0.0)
            orig_stance = pred["stance"]
            
            if conf < tau:
                effective_stance = "NOT_ENOUGH_INFO"
                abstained = True
            else:
                effective_stance = orig_stance
                abstained = False
                
            entry = dict(pred)
            entry["effective_stance"] = effective_stance
            entry["abstained"] = abstained
            entry["applied_tau"] = tau
            filtered_preds.append(entry)
        return filtered_preds

    def compute_risk_coverage_curve(self, predictions: List[Dict[str, Any]], gold_labels: List[str],
                                    thresholds: List[float] = None) -> List[Dict[str, Any]]:
        """
        Sweeps thresholds tau in [0.0, 0.95] to generate the Risk-Coverage Curve:
        - Coverage (C): % of claims where model asserted an active claim (did not abstain)
        - Selective Accuracy (Acc@C): Accuracy on those asserted claims
        - Risk: 1.0 - Selective Accuracy
        """
        if thresholds is None:
            thresholds = [0.0, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.85, 0.9]
            
        curve = []
        n_total = len(predictions)
        
        for tau in thresholds:
            filtered = self.apply_threshold(predictions, tau)
            
            # Active (non-abstained) predictions
            active_indices = [i for i, f in enumerate(filtered) if not f["abstained"] and f["effective_stance"] != "NOT_ENOUGH_INFO"]
            
            coverage = len(active_indices) / n_total if n_total > 0 else 0.0
            
            if len(active_indices) > 0:
                correct = sum(1 for i in active_indices if filtered[i]["effective_stance"] == gold_labels[i])
                selective_acc = correct / len(active_indices)
            else:
                selective_acc = 1.0  # Zero risk when fully abstaining
                
            curve.append({
                "tau": tau,
                "coverage": round(coverage, 4),
                "selective_accuracy": round(selective_acc, 4),
                "risk": round(1.0 - selective_acc, 4),
                "active_count": len(active_indices),
                "total_count": n_total
            })
            
        return curve
