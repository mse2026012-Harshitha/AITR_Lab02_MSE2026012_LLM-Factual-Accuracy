"""
Claim Stance Classification and Prompt Execution Engine (Module 3)
Author: Penumala Harshitha (M.Tech, IIIT Allahabad)
Project: Benchmarking Factual Accuracy of LLMs Across Scientific Domains

Purpose:
Implements standardized prompt generation and stance prediction across the three
information regimes (Closed-Book, Oracle Gold Context, and Noisy BM25 Retrieval),
outputting predicted stance (SUPPORT, CONTRADICT, NOT_ENOUGH_INFO), confidence, and rationale.
"""

import json
import re
from typing import Dict, List, Any, Optional

STANCE_CLASSES = ["SUPPORT", "CONTRADICT", "NOT_ENOUGH_INFO"]

def format_prompt(claim_text: str, evidence_text: Optional[str] = None, regime: str = "oracle") -> str:
    """
    Constructs a standardized evaluation prompt ensuring byte-for-byte consistency
    across Closed-Book, Oracle, and Retrieved regimes.
    """
    if regime == "closed_book" or not evidence_text:
        context_block = "No external scientific literature provided. Rely on scientific domain knowledge."
    else:
        context_block = f"Scientific Evidence:\n\"\"\"\n{evidence_text.strip()}\n\"\"\""
        
    prompt = f"""You are an expert scientific fact-checking system evaluating research assertions.

{context_block}

Claim to verify:
"{claim_text}"

Task Instructions:
1. Determine whether the provided evidence SUPPORTS, CONTRADICTS, or provides NOT_ENOUGH_INFO to verify the claim.
2. If evidence is missing, contradictory, or inconclusive, classify as NOT_ENOUGH_INFO.
3. Provide your certainty as a confidence score between 0.0 and 1.0.
4. Extract the exact sentence from the evidence that justifies your conclusion.

Respond STRICTLY in valid JSON format:
{{
  "stance": "<SUPPORT | CONTRADICT | NOT_ENOUGH_INFO>",
  "confidence": <float between 0.0 and 1.0>,
  "rationale": "<exact sentence quote or empty string>"
}}
"""
    return prompt

class ScientificStanceClassifier:
    """
    Deterministic scientific fact-checking model and baseline scoring engine.
    Supports oracle evidence conditioning, noisy retrieval injection, and closed-book evaluation.
    """
    def __init__(self, mode: str = "heuristic_baseline"):
        self.mode = mode

    def _extract_negation_and_sentiment(self, text: str) -> bool:
        """Detects scientific refutation/negation markers."""
        negation_markers = [
            r"\bnot\b", r"\bno\b", r"\bnever\b", r"\bfails? to\b", r"\bunable to\b",
            r"\blacks?\b", r"\binvalid\b", r"\brefute[sd]?\b", r"\bcontradict[sd]?\b",
            r"\bno significant (difference|effect|correlation|association)\b",
            r"\bcontrary to\b", r"\bno evidence\b"
        ]
        text_lower = text.lower()
        return any(re.search(pat, text_lower) for pat in negation_markers)

    def predict_instance(self, claim_text: str, evidence_input: Any, regime: str = "oracle") -> Dict[str, Any]:
        """
        Generates a stance prediction, confidence score, and extracted rationale
        for a single claim instance under the specified regime.
        
        evidence_input can be:
          - None (Closed-book)
          - Single doc dict (Oracle context)
          - List of doc dicts (Retrieved top-k contexts)
        """
        if regime == "closed_book" or evidence_input is None:
            # Closed-book: No external literature provided
            return {
                "stance": "NOT_ENOUGH_INFO",
                "confidence": 0.40,
                "rationale": "",
                "doc_id": None
            }

        # Normalize evidence_input to a list of candidate documents
        if isinstance(evidence_input, list):
            docs = evidence_input
        else:
            docs = [evidence_input] if evidence_input else []

        if not docs:
            return {
                "stance": "NOT_ENOUGH_INFO",
                "confidence": 0.30,
                "rationale": "",
                "doc_id": None
            }

        claim_tokens = set(re.findall(r"\b[a-zA-Z0-9]+\b", claim_text.lower()))
        best_sentence = ""
        best_overlap = -1
        best_idx = 0
        best_doc_id = None
        best_doc_rank = 1

        # Search across all provided candidate abstracts
        for rank_idx, doc in enumerate(docs, 1):
            abstract_sentences = doc.get("abstract", [])
            for sent_idx, sentence in enumerate(abstract_sentences):
                sent_tokens = set(re.findall(r"\b[a-zA-Z0-9]+\b", sentence.lower()))
                overlap = len(claim_tokens.intersection(sent_tokens))
                if overlap > best_overlap:
                    best_overlap = overlap
                    best_sentence = sentence
                    best_idx = sent_idx
                    best_doc_id = doc.get("doc_id")
                    best_doc_rank = rank_idx

        # If no sentence found or overlap is negligible
        if not best_sentence or best_overlap <= 0:
            return {
                "stance": "NOT_ENOUGH_INFO",
                "confidence": 0.30,
                "rationale": "",
                "doc_id": best_doc_id
            }

        # Determine stance based on semantic alignment between claim and best rationale sentence
        claim_neg = self._extract_negation_and_sentiment(claim_text)
        sent_neg = self._extract_negation_and_sentiment(best_sentence)
        
        overlap_ratio = best_overlap / max(len(claim_tokens), 1)
        rank_discount = 1.0 / (1.0 + 0.1 * (best_doc_rank - 1))  # Slight discount if best match is deeper in top-k
        
        if overlap_ratio < 0.25:
            # Insufficient lexical/semantic overlap -> Not Enough Info
            stance = "NOT_ENOUGH_INFO"
            confidence = round((0.35 + 0.15 * overlap_ratio) * rank_discount, 3)
        elif claim_neg != sent_neg:
            # Polar disagreement detected between claim assertion and rationale
            stance = "CONTRADICT"
            confidence = round((0.60 + 0.35 * min(overlap_ratio, 1.0)) * rank_discount, 3)
        else:
            # Consistent alignment
            stance = "SUPPORT"
            confidence = round((0.65 + 0.30 * min(overlap_ratio, 1.0)) * rank_discount, 3)

        return {
            "stance": stance,
            "confidence": min(max(confidence, 0.0), 1.0),
            "rationale": best_sentence,
            "rationale_sentence_idx": best_idx,
            "doc_id": best_doc_id,
            "best_doc_rank": best_doc_rank
        }
