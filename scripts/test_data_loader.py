#!/usr/bin/env python3
"""
Unit and Sanity Test for SciFactDataLoader (Module 1)
Author: Penumala Harshitha (M.Tech, IIIT Allahabad)
"""

import sys
import os
import json

# Add project root to python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_loader import SciFactDataLoader

def test_loader():
    print("=" * 65)
    print("RUNNING UNIT TEST: SciFactDataLoader (Module 1)")
    print("=" * 65)
    
    loader = SciFactDataLoader(data_dir="data")
    
    # 1. Test Corpus Loading
    corpus = loader.load_corpus()
    print(f"[*] Loaded corpus abstracts: {len(corpus):,} documents")
    assert len(corpus) == 5183, f"Expected 5,183 abstracts, found {len(corpus)}"
    
    # Check sample document schema
    sample_doc_id = next(iter(corpus))
    sample_doc = corpus[sample_doc_id]
    assert "doc_id" in sample_doc, "Missing doc_id in corpus entry"
    assert "title" in sample_doc, "Missing title in corpus entry"
    assert "abstract" in sample_doc, "Missing abstract in corpus entry"
    assert isinstance(sample_doc["abstract"], list), "Abstract must be a list of sentences"
    assert "full_text" in sample_doc and len(sample_doc["full_text"]) > 0, "Empty full_text"
    print(f"[+] Sample Document (ID {sample_doc_id}): '{sample_doc['title'][:60]}...' ({len(sample_doc['abstract'])} sentences)")
    
    # 2. Test Claims Loading
    claims = loader.load_claims()
    print(f"[*] Loaded evaluation claims: {len(claims):,} claims")
    assert len(claims) == 300, f"Expected 300 dev claims, found {len(claims)}"
    
    # 3. Label Distribution Audit
    label_counts = {}
    for c in claims:
        lbl = c["ground_truth_stance"]
        label_counts[lbl] = label_counts.get(lbl, 0) + 1
        
    print("\n--- Ground Truth Stance Distribution (Dev Set) ---")
    for lbl, count in sorted(label_counts.items()):
        pct = (count / len(claims)) * 100
        print(f"  {lbl:18s}: {count:4d} ({pct:5.1f}%)")
        
    assert "SUPPORT" in label_counts, "Missing SUPPORT label in dev set"
    assert "CONTRADICT" in label_counts, "Missing CONTRADICT label in dev set"
    assert "NOT_ENOUGH_INFO" in label_counts, "Missing NOT_ENOUGH_INFO label in dev set"
    
    # 4. Sentence Index & Document Alignment Sanity Check
    verified_evidence_count = 0
    for c in claims:
        for doc_id_str, ev_list in c["evidence"].items():
            doc_id = int(doc_id_str)
            assert doc_id in corpus, f"Evidence document {doc_id} not found in corpus!"
            doc = corpus[doc_id]
            num_sentences = len(doc["abstract"])
            for ev in ev_list:
                for sent_idx in ev.get("sentences", []):
                    assert 0 <= sent_idx < num_sentences, (
                        f"Sentence index {sent_idx} out of range for doc {doc_id} (length {num_sentences})"
                    )
                    verified_evidence_count += 1
                    
    print(f"\n[+] Verified {verified_evidence_count} rationale sentence references across {len(claims)} claims.")
    print("=" * 65)
    print("UNIT TEST STATUS: ALL CHECKS PASSED [OK]")
    print("=" * 65)
    return True

if __name__ == "__main__":
    test_loader()
