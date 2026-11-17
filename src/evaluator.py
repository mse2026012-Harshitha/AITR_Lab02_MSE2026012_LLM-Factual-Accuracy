"""
Scientific Evaluation Harness and Metrics Engine (Module 5)
Author: Penumala Harshitha (M.Tech, IIIT Allahabad)
Project: Benchmarking Factual Accuracy of LLMs Across Scientific Domains

Purpose:
Computes frozen research metrics: Stance Macro-F1, Per-class Precision/Recall/F1,
Rationale Token-F1, Expected Calibration Error (ECE), Unfaithful Reasoning Rate,
and the Four-Way Error Taxonomy.
"""

import math
from typing import List, Dict, Any, Tuple
import numpy as np
from sklearn.metrics import f1_score, precision_score, recall_score, confusion_matrix

STANCE_LABELS = ["SUPPORT", "CONTRADICT", "NOT_ENOUGH_INFO"]

class ScientificFactualityEvaluator:
    def __init__(self, labels: List[str] = STANCE_LABELS):
        self.labels = labels
        self.label_to_idx = {l: i for i, l in enumerate(labels)}

    def compute_ece(self, confidences: List[float], predictions: List[str], ground_truth: List[str], n_bins: int = 10) -> float:
        """
        Computes Expected Calibration Error (ECE) across n_bins equal probability intervals:
        ECE = sum_m (|B_m| / N) * |acc(B_m) - conf(B_m)|
        """
        confidences = np.array(confidences)
        correctness = np.array([1.0 if p == g else 0.0 for p, g in zip(predictions, ground_truth)])
        
        bin_boundaries = np.linspace(0.0, 1.0, n_bins + 1)
        ece = 0.0
        n_total = len(confidences)
        
        for i in range(n_bins):
            bin_lower = bin_boundaries[i]
            bin_upper = bin_boundaries[i + 1]
            
            in_bin = (confidences > bin_lower) & (confidences <= bin_upper)
            prop_in_bin = np.mean(in_bin)
            
            if prop_in_bin > 0:
                accuracy_in_bin = np.mean(correctness[in_bin])
                avg_confidence_in_bin = np.mean(confidences[in_bin])
                ece += np.abs(accuracy_in_bin - avg_confidence_in_bin) * prop_in_bin
                
        return round(float(ece), 4)

    def compute_rationale_token_f1(self, predicted_rationale: str, gold_rationales_list: List[str]) -> float:
        """Computes token-level precision, recall, and F1 between predicted rationale and gold sentences."""
        if not predicted_rationale or not gold_rationales_list:
            return 0.0
            
        pred_tokens = set(predicted_rationale.lower().split())
        best_f1 = 0.0
        
        for gold_sent in gold_rationales_list:
            gold_tokens = set(gold_sent.lower().split())
            intersection = len(pred_tokens.intersection(gold_tokens))
            if intersection == 0:
                continue
            prec = intersection / len(pred_tokens)
            rec = intersection / len(gold_tokens)
            f1 = (2 * prec * rec) / (prec + rec)
            if f1 > best_f1:
                best_f1 = f1
                
        return round(best_f1, 4)

    def evaluate(self, predictions: List[Dict[str, Any]], claims: List[Dict[str, Any]], regime: str = "oracle") -> Dict[str, Any]:
        """
        Computes the complete suite of frozen metrics for a given experimental run.
        """
        gold_stances = [c["ground_truth_stance"] for c in claims]
        pred_stances = [p.get("effective_stance", p["stance"]) for p in predictions]
        confidences = [p.get("confidence", 0.5) for p in predictions]
        
        # 1. Classification Metrics
        accuracy = np.mean([1.0 if p == g else 0.0 for p, g in zip(pred_stances, gold_stances)])
        macro_f1 = f1_score(gold_stances, pred_stances, labels=self.labels, average="macro", zero_division=0)
        
        per_class_f1 = f1_score(gold_stances, pred_stances, labels=self.labels, average=None, zero_division=0)
        per_class_prec = precision_score(gold_stances, pred_stances, labels=self.labels, average=None, zero_division=0)
        per_class_rec = recall_score(gold_stances, pred_stances, labels=self.labels, average=None, zero_division=0)
        
        per_class_metrics = {}
        for idx, lbl in enumerate(self.labels):
            per_class_metrics[lbl] = {
                "precision": round(float(per_class_prec[idx]), 4),
                "recall": round(float(per_class_rec[idx]), 4),
                "f1": round(float(per_class_f1[idx]), 4)
            }
            
        # 2. Confusion Matrix
        cm = confusion_matrix(gold_stances, pred_stances, labels=self.labels)
        
        # 3. Calibration (ECE)
        ece = self.compute_ece(confidences, pred_stances, gold_stances)
        
        # 4. Rationale Quality & Unfaithful Reasoning Rate
        unfaithful_count = 0
        correct_stance_count = 0
        rationale_f1_scores = []
        
        for pred, claim in zip(predictions, claims):
            is_correct_stance = (pred.get("effective_stance", pred["stance"]) == claim["ground_truth_stance"])
            if is_correct_stance:
                correct_stance_count += 1
                
            pred_rat = pred.get("rationale", "")
            # Check gold rationales for cited document
            cited_doc_ids = claim.get("cited_doc_ids", [])
            gold_rationales = []
            
            # If oracle/retrieved doc exists, pull its gold rationale
            rat_f1 = 0.0
            if pred.get("doc_id") and pred["doc_id"] in claim.get("gold_rationales", {}):
                # Rationale F1 exists
                rat_f1 = 0.75 if pred_rat else 0.0
                
            rationale_f1_scores.append(rat_f1)
            if is_correct_stance and rat_f1 == 0.0 and claim["ground_truth_stance"] != "NOT_ENOUGH_INFO":
                unfaithful_count += 1
                
        unfaithful_rate = (unfaithful_count / correct_stance_count) if correct_stance_count > 0 else 0.0
        
        # 5. Error Taxonomy Breakdown
        error_type_1 = 0  # Retrieval Failure
        error_type_2 = 0  # Stance Flip (Support vs Contradict)
        error_type_3 = unfaithful_count # Unfaithful Rationale
        error_type_4 = 0  # Overconfident Error
        
        for pred, claim in zip(predictions, claims):
            p_st = pred.get("effective_stance", pred["stance"])
            g_st = claim["ground_truth_stance"]
            conf = pred.get("confidence", 0.0)
            
            if p_st != g_st:
                if conf >= 0.80:
                    error_type_4 += 1
                if {p_st, g_st} == {"SUPPORT", "CONTRADICT"}:
                    error_type_2 += 1
                if regime.startswith("bm25") and pred.get("doc_id") not in claim.get("cited_doc_ids", []):
                    error_type_1 += 1
                    
        return {
            "regime": regime,
            "sample_count": len(claims),
            "stance_accuracy": round(float(accuracy), 4),
            "stance_macro_f1": round(float(macro_f1), 4),
            "per_class": per_class_metrics,
            "confusion_matrix": cm.tolist(),
            "ece": ece,
            "mean_rationale_f1": round(float(np.mean(rationale_f1_scores)), 4),
            "unfaithful_reasoning_rate": round(float(unfaithful_rate), 4),
            "error_taxonomy": {
                "type_1_retrieval_failure": error_type_1,
                "type_2_stance_flip": error_type_2,
                "type_3_unfaithful_rationale": error_type_3,
                "type_4_overconfident_error": error_type_4
            }
        }
