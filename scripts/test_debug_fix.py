#!/usr/bin/env python3
"""
Verification Test for Multi-Document Retrieval Debug Fix (Prompt 11)
Author: Penumala Harshitha (M.Tech, IIIT Allahabad)
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.baseline_model import ScientificStanceClassifier

def test_debug_fix():
    print("=" * 65)
    print("RUNNING VERIFICATION TEST: Multi-Document Retrieval Fix (Prompt 11)")
    print("=" * 65)
    
    classifier = ScientificStanceClassifier()
    claim = "GTP cyclohydrolase I fails to stimulate nitric oxide production."
    
    # Mock Document 1 (Irrelevant Distractor at Rank 1)
    doc1 = {
        "doc_id": 1001,
        "title": "Protein folding in yeast cells",
        "abstract": ["Yeast cells express various chaperone proteins during thermal stress."]
    }
    
    # Mock Document 2 (True Scientific Refutation at Rank 2)
    doc2 = {
        "doc_id": 2002,
        "title": "Role of GTP cyclohydrolase I in nitric oxide regulation",
        "abstract": ["GTP cyclohydrolase I expression significantly stimulates nitric oxide synthesis in endothelial cells."]
    }
    
    # Test 1: Empty retrieval edge case
    print("[*] Testing Edge Case 1: Empty retrieval list...")
    pred_empty = classifier.predict_instance(claim, [], regime="bm25_k1")
    assert pred_empty["stance"] == "NOT_ENOUGH_INFO", "Empty docs must yield NOT_ENOUGH_INFO"
    print("    [+] Handled correctly: Stance is NOT_ENOUGH_INFO")
    
    # Test 2: Single document (k=1, only distractor available)
    print("[*] Testing Condition k=1 (Distractor only)...")
    pred_k1 = classifier.predict_instance(claim, [doc1], regime="bm25_k1")
    print(f"    k=1 Output: Stance={pred_k1['stance']}, DocID={pred_k1['doc_id']}, Overlap DocRank={pred_k1.get('best_doc_rank')}")
    assert pred_k1["doc_id"] == 1001 or pred_k1["stance"] == "NOT_ENOUGH_INFO"
    
    # Test 3: Multi-document list (k=2, [doc1, doc2])
    print("[*] Testing Condition k=2 (Multi-document context with true evidence at Rank 2)...")
    pred_k2 = classifier.predict_instance(claim, [doc1, doc2], regime="bm25_k2")
    print(f"    k=2 Output: Stance={pred_k2['stance']}, DocID={pred_k2['doc_id']}, Overlap DocRank={pred_k2.get('best_doc_rank')}")
    print(f"    Rationale: \"{pred_k2['rationale']}\"")
    
    # Crucial assertion: With multi-document support, the model must locate doc2 (ID 2002) at Rank 2!
    assert pred_k2["doc_id"] == 2002, f"Expected doc_id 2002, got {pred_k2['doc_id']}"
    assert pred_k2["stance"] == "CONTRADICT", f"Expected CONTRADICT, got {pred_k2['stance']}"
    assert pred_k2["best_doc_rank"] == 2, f"Expected rank 2, got {pred_k2['best_doc_rank']}"
    print("    [+] Verified: Model correctly searched across multiple candidate abstracts and selected the true rationale at Rank 2!")
    
    print("=" * 65)
    print("VERIFICATION TEST STATUS: ALL CHECKS PASSED [OK]")
    print("=" * 65)
    return True

if __name__ == "__main__":
    test_debug_fix()
