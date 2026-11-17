"""
Rationale-Grounded Evidence Verifier (R-GEV Module)
Author: Penumala Harshitha (M.Tech, IIIT Allahabad)
Project: Benchmarking Factual Accuracy of LLMs Across Scientific Domains

Theoretical Grounding:
Combines atomic evidence decomposition (Min et al., 2023, FActScore),
intermediate rationale verification (Dhuliawala et al., 2023, CoVe), and
selective prediction (Kalai et al., 2026, Nature) into an isolated pre-classification
verification gatekeeper.
"""

import re
from typing import Dict, List, Any, Optional

class RationaleGroundedVerifier:
    def __init__(self, theta_threshold: float = 0.35):
        """
        Initializes the R-GEV verifier.
        theta_threshold: Minimum atomic evidence support score (token overlap ratio)
                         required to accept an extracted rationale as valid evidence.
        """
        self.theta_threshold = theta_threshold

    def calculate_sentence_support(self, claim_text: str, sentence_text: str) -> float:
        """Calculates token overlap ratio between claim and candidate rationale sentence."""
        if not sentence_text or not claim_text:
            return 0.0
        claim_tokens = set(re.findall(r"\b[a-zA-Z0-9]+\b", claim_text.lower()))
        sent_tokens = set(re.findall(r"\b[a-zA-Z0-9]+\b", sentence_text.lower()))
        if not claim_tokens:
            return 0.0
        overlap = len(claim_tokens.intersection(sent_tokens))
        return overlap / len(claim_tokens)

    def verify_and_gate(self, prediction: Dict[str, Any], claim_text: str,
                        theta: Optional[float] = None) -> Dict[str, Any]:
        """
        Applies Rationale-Grounded Verification gating:
        If the extracted rationale sentence fails the theta support threshold,
        the model is prevented from making an active stance assertion on distractor text
        and is forced to abstain (effective_stance = 'NOT_ENOUGH_INFO').
        """
        threshold = theta if theta is not None else self.theta_threshold
        rationale = prediction.get("rationale", "")
        support_ratio = self.calculate_sentence_support(claim_text, rationale)
        
        gated_pred = dict(prediction)
        gated_pred["support_ratio"] = round(support_ratio, 4)
        gated_pred["theta_applied"] = threshold

        # Decision Rule: Reject low-support distractor rationales
        if support_ratio < threshold:
            gated_pred["effective_stance"] = "NOT_ENOUGH_INFO"
            gated_pred["rationale_verified"] = False
            gated_pred["gating_reason"] = f"Atomic evidence support ({support_ratio:.3f}) below threshold ({threshold})"
            gated_pred["confidence"] = min(prediction.get("confidence", 0.5), 0.35)
        else:
            gated_pred["effective_stance"] = prediction["stance"]
            gated_pred["rationale_verified"] = True
            gated_pred["gating_reason"] = f"Atomic evidence verified ({support_ratio:.3f} >= {threshold})"

        return gated_pred

    def apply_dual_gate(self, prediction: Dict[str, Any], claim_text: str,
                        theta: float = 0.35, tau: float = 0.70) -> Dict[str, Any]:
        """
        Applies Dual-Gated R-GEV (Rationale verification + Confidence thresholding):
        An active stance (SUPPORT or CONTRADICT) is asserted IF AND ONLY IF:
          1. support_ratio >= theta (Evidence Grounding Gate)
          2. confidence >= tau (Uncertainty Abstention Gate)
        Otherwise, the system safely abstains to 'NOT_ENOUGH_INFO'.
        """
        # Step 1: Apply rationale evidence gate
        first_gate = self.verify_and_gate(prediction, claim_text, theta=theta)
        
        # Step 2: Apply confidence calibration gate
        dual_pred = dict(first_gate)
        conf = prediction.get("confidence", 0.0)
        
        if not first_gate["rationale_verified"]:
            dual_pred["effective_stance"] = "NOT_ENOUGH_INFO"
            dual_pred["dual_gated"] = True
            dual_pred["dual_reason"] = "Rejected by Rationale Gate"
        elif conf < tau:
            dual_pred["effective_stance"] = "NOT_ENOUGH_INFO"
            dual_pred["dual_gated"] = True
            dual_pred["dual_reason"] = f"Rejected by Confidence Gate ({conf:.2f} < {tau})"
        else:
            dual_pred["effective_stance"] = first_gate["effective_stance"]
            dual_pred["dual_gated"] = False
            dual_pred["dual_reason"] = "Accepted by Dual Gates"

        return dual_pred
