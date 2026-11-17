#!/usr/bin/env python3
"""
Unit and Sanity Test for RationaleGroundedVerifier (R-GEV)
Author: Penumala Harshitha (M.Tech, IIIT Allahabad)
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.rationale_verifier import RationaleGroundedVerifier

def test_verifier():
    print("=" * 65)
    print("RUNNING UNIT TEST: RationaleGroundedVerifier (R-GEV Module)")
    print("=" * 65)
    
    verifier = RationaleGroundedVerifier(theta_threshold=0.35)
    claim = "GTP cyclohydrolase I expression stimulates nitric oxide synthesis."
    
    # Case 1: Low-overlap distractor rationale sentence
    distractor_sent = "Yeast cells express various molecular chaperones during heat shock."
    pred_distractor = {
        "stance": "SUPPORT",
        "confidence": 0.75,
        "rationale": distractor_sent,
        "doc_id": 999
    }
    
    print("[*] Testing Case 1: Distractor rationale with low atomic overlap...")
    gated_distractor = verifier.verify_and_gate(pred_distractor, claim, theta=0.35)
    print(f"    Original Stance: {pred_distractor['stance']} -> Gated Stance: {gated_distractor['effective_stance']}")
    print(f"    Support Ratio:   {gated_distractor['support_ratio']:.3f} (Threshold: {gated_distractor['theta_applied']})")
    print(f"    Rationale Verified: {gated_distractor['rationale_verified']}")
    assert gated_distractor["effective_stance"] == "NOT_ENOUGH_INFO", "Distractor must be overridden to NOT_ENOUGH_INFO"
    assert not gated_distractor["rationale_verified"], "Rationale must not be verified"
    print("    [+] Handled correctly: Model prevented from asserting ungrounded claim!")
    
    # Case 2: High-overlap true scientific rationale sentence
    true_sent = "GTP cyclohydrolase I overexpression significantly stimulates endothelial nitric oxide synthesis."
    pred_true = {
        "stance": "SUPPORT",
        "confidence": 0.85,
        "rationale": true_sent,
        "doc_id": 123
    }
    
    print("\n[*] Testing Case 2: True scientific rationale with high atomic overlap...")
    gated_true = verifier.verify_and_gate(pred_true, claim, theta=0.35)
    print(f"    Original Stance: {pred_true['stance']} -> Gated Stance: {gated_true['effective_stance']}")
    print(f"    Support Ratio:   {gated_true['support_ratio']:.3f} (Threshold: {gated_true['theta_applied']})")
    print(f"    Rationale Verified: {gated_true['rationale_verified']}")
    assert gated_true["effective_stance"] == "SUPPORT", "Valid evidence must retain SUPPORT"
    assert gated_true["rationale_verified"], "Rationale must be verified"
    print("    [+] Handled correctly: Stance retained with verified evidence grounding!")
    
    # Case 3: Dual Gate Test
    print("\n[*] Testing Case 3: Dual Gate interaction (Rationale + Confidence)...")
    # Low confidence but valid rationale
    pred_low_conf = {
        "stance": "SUPPORT",
        "confidence": 0.55,  # Below tau=0.70
        "rationale": true_sent,
        "doc_id": 123
    }
    dual_gated = verifier.apply_dual_gate(pred_low_conf, claim, theta=0.35, tau=0.70)
    assert dual_gated["effective_stance"] == "NOT_ENOUGH_INFO", "Low confidence must be rejected by confidence gate"
    print(f"    [+] Low confidence correctly rejected: Reason: {dual_gated['dual_reason']}")
    
    dual_gated_pass = verifier.apply_dual_gate(pred_true, claim, theta=0.35, tau=0.70)
    assert dual_gated_pass["effective_stance"] == "SUPPORT", "High support and high confidence must pass both gates"
    print(f"    [+] High support & high confidence accepted: Reason: {dual_gated_pass['dual_reason']}")
    
    print("=" * 65)
    print("UNIT TEST STATUS: ALL CHECKS PASSED [OK]")
    print("=" * 65)
    return True

if __name__ == "__main__":
    test_verifier()
