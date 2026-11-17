#!/usr/bin/env python3
"""
Unit and Sanity Test for ScientificBM25Retriever (Module 2)
Author: Penumala Harshitha (M.Tech, IIIT Allahabad)
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_loader import SciFactDataLoader
from src.retriever import ScientificBM25Retriever

def test_retriever():
    print("=" * 65)
    print("RUNNING UNIT TEST: ScientificBM25Retriever (Module 2)")
    print("=" * 65)
    
    loader = SciFactDataLoader(data_dir="data")
    corpus = loader.load_corpus()
    claims = loader.load_claims()
    
    print("[*] Initializing BM25 index over 5,183 scientific abstracts...")
    retriever = ScientificBM25Retriever(corpus, k1=1.5, b=0.75)
    print("[+] BM25 index built successfully.")
    
    # 1. Test Single Query Retrieval
    sample_claim = claims[0]
    print(f"\n[*] Sample Claim (ID {sample_claim['claim_id']}):")
    print(f"    '{sample_claim['claim']}'")
    print(f"    Gold Cited Docs: {sample_claim['cited_doc_ids']}")
    
    top3 = retriever.retrieve(sample_claim["claim"], top_k=3)
    print(f"[+] Top-3 Retrieved Documents:")
    for r in top3:
        hit = " [GOLD HIT]" if r["doc_id"] in sample_claim["cited_doc_ids"] else ""
        print(f"    Rank {r['rank']}: Doc {r['doc_id']} (Score: {r['score']:.2f}){hit} - '{r['title'][:50]}...'")
        
    assert len(top3) == 3, "Expected 3 retrieved documents"
    assert top3[0]["score"] >= top3[1]["score"] >= top3[2]["score"], "Results must be ranked in descending order"
    
    # 2. Benchmark Corpus-Level Retrieval Recall across depths k=1, 3, 5
    print("\n--- Measuring Empirical Corpus Retrieval Recall ---")
    for k in [1, 3, 5]:
        res = retriever.evaluate_retrieval_recall(claims, top_k=k)
        pct = res["recall_at_k"] * 100
        print(f"  Recall@{k}: {res['hits']:3d} / {res['total_claims']:3d} claims ({pct:5.2f}%)")
        
    print("=" * 65)
    print("UNIT TEST STATUS: ALL CHECKS PASSED [OK]")
    print("=" * 65)
    return True

if __name__ == "__main__":
    test_retriever()
