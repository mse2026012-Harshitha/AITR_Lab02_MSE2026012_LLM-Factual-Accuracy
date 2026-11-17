"""
Scientific Corpus BM25 Sparse Retriever Module
Author: Penumala Harshitha (M.Tech, IIIT Allahabad)
Project: Benchmarking Factual Accuracy of LLMs Across Scientific Domains

Purpose:
Builds a BM25 index over the 5,183 scientific research abstracts in the SciFact corpus,
enabling deterministic sparse retrieval to simulate open literature search and measure
retrieval noise degradation (RQ1).
"""

import re
from typing import Dict, List, Any, Tuple
from rank_bm25 import BM25Okapi

def tokenize(text: str) -> List[str]:
    """Simple alphanumeric lowercased tokenizer for consistent BM25 indexing."""
    return re.findall(r"\b[a-zA-Z0-9]+\b", text.lower())

class ScientificBM25Retriever:
    def __init__(self, corpus: Dict[int, Dict[str, Any]], k1: float = 1.5, b: float = 0.75):
        """
        Initializes BM25 retriever with standard Okapi parameters:
        k1 = 1.5 (term frequency saturation)
        b = 0.75 (document length normalization)
        """
        self.k1 = k1
        self.b = b
        self.corpus = corpus
        self.doc_ids = list(corpus.keys())
        
        # Tokenize all corpus documents
        self.tokenized_corpus = [
            tokenize(self.corpus[doc_id]["full_text"])
            for doc_id in self.doc_ids
        ]
        
        # Build BM25 index
        self.bm25 = BM25Okapi(self.tokenized_corpus, k1=self.k1, b=self.b)

    def retrieve(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Retrieves the top_k most relevant documents for a given query string.
        Returns a list of dicts with doc_id, score, title, abstract, and rank.
        """
        query_tokens = tokenize(query)
        if not query_tokens:
            return []
            
        doc_scores = self.bm25.get_scores(query_tokens)
        
        # Get top-k indices
        top_indices = sorted(range(len(doc_scores)), key=lambda i: doc_scores[i], reverse=True)[:top_k]
        
        results = []
        for rank, idx in enumerate(top_indices, 1):
            doc_id = self.doc_ids[idx]
            doc = self.corpus[doc_id]
            results.append({
                "rank": rank,
                "doc_id": doc_id,
                "score": float(doc_scores[idx]),
                "title": doc["title"],
                "abstract": doc["abstract"],
                "full_text": doc["full_text"]
            })
        return results

    def evaluate_retrieval_recall(self, claims: List[Dict[str, Any]], top_k: int = 3) -> Dict[str, float]:
        """
        Measures gold document retrieval recall@k across all claims with cited documents.
        Recall@k = (claims where at least one cited_doc_id is in top_k) / (claims with cited_docs)
        """
        total_evaluable = 0
        hits = 0
        
        for claim in claims:
            cited_ids = set(claim["cited_doc_ids"])
            if not cited_ids:
                continue
                
            total_evaluable += 1
            retrieved = self.retrieve(claim["claim"], top_k=top_k)
            retrieved_ids = {r["doc_id"] for r in retrieved}
            
            if len(cited_ids.intersection(retrieved_ids)) > 0:
                hits += 1
                
        recall_at_k = (hits / total_evaluable) if total_evaluable > 0 else 0.0
        return {
            "top_k": top_k,
            "total_claims": total_evaluable,
            "hits": hits,
            "recall_at_k": round(recall_at_k, 4)
        }
