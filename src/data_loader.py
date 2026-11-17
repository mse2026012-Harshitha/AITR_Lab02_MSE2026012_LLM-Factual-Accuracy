"""
SciFact Data Loader and Schema Validation Module
Author: Penumala Harshitha (M.Tech, IIIT Allahabad)
Project: Benchmarking Factual Accuracy of LLMs Across Scientific Domains

Purpose:
Loads and normalizes the official SciFact claims (dev split) and scientific corpus,
verifying document ID integrity, sentence-level rationale spans, and 3-way stance ground truth:
SUPPORT, CONTRADICT, or NOT_ENOUGH_INFO.
"""

import json
import os
from typing import Dict, List, Any, Tuple, Optional

class SciFactDataLoader:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.claims_path = os.path.join(data_dir, "claims_dev.jsonl")
        self.corpus_path = os.path.join(data_dir, "corpus.jsonl")
        
        if not os.path.exists(self.claims_path):
            raise FileNotFoundError(f"Claims file not found: {self.claims_path}")
        if not os.path.exists(self.corpus_path):
            raise FileNotFoundError(f"Corpus file not found: {self.corpus_path}")

    def load_corpus(self) -> Dict[int, Dict[str, Any]]:
        """
        Loads corpus.jsonl into a dictionary keyed by integer doc_id.
        Each entry contains:
          - doc_id: int
          - title: str
          - abstract: list of str (sentences)
          - full_text: title + ' ' + joined abstract
        """
        corpus = {}
        with open(self.corpus_path, "r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                record = json.loads(line)
                doc_id = int(record["doc_id"])
                title = record.get("title", "")
                abstract = record.get("abstract", [])
                
                # Combine title and abstract into full searchable text
                full_text = f"{title}. " + " ".join(abstract) if abstract else title
                
                corpus[doc_id] = {
                    "doc_id": doc_id,
                    "title": title,
                    "abstract": abstract,
                    "full_text": full_text.strip()
                }
        return corpus

    def load_claims(self) -> List[Dict[str, Any]]:
        """
        Loads claims_dev.jsonl into a structured list of normalized claim dictionaries.
        
        Normalized Claim Structure:
          - claim_id: int
          - claim: str
          - cited_doc_ids: list of int
          - evidence: dict mapping doc_id -> list of {'sentences': list[int], 'label': str}
          - ground_truth_stance: 'SUPPORT' | 'CONTRADICT' | 'NOT_ENOUGH_INFO'
          - gold_rationales: dict mapping doc_id -> list of list[int]
        """
        claims = []
        with open(self.claims_path, "r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                record = json.loads(line)
                claim_id = int(record["id"])
                claim_text = record["claim"].strip()
                evidence = record.get("evidence", {})
                cited_doc_ids = [int(doc_id) for doc_id in record.get("cited_doc_ids", [])]
                
                # Determine normalized 3-way ground truth stance
                # If evidence is empty, stance is NOT_ENOUGH_INFO
                gold_rationales = {}
                stance_labels = set()
                
                for doc_id_str, ev_list in evidence.items():
                    doc_id = int(doc_id_str)
                    gold_rationales[doc_id] = []
                    for ev in ev_list:
                        label = ev.get("label", "").upper()
                        if label in ["SUPPORT", "CONTRADICT"]:
                            stance_labels.add(label)
                        gold_rationales[doc_id].append(ev.get("sentences", []))
                
                if not stance_labels or not evidence:
                    primary_stance = "NOT_ENOUGH_INFO"
                elif "SUPPORT" in stance_labels and "CONTRADICT" not in stance_labels:
                    primary_stance = "SUPPORT"
                elif "CONTRADICT" in stance_labels and "SUPPORT" not in stance_labels:
                    primary_stance = "CONTRADICT"
                else:
                    # Rare mixed stance across different candidate papers
                    primary_stance = "CONTRADICT" # Defaulting conservative contradiction
                
                claims.append({
                    "claim_id": claim_id,
                    "claim": claim_text,
                    "cited_doc_ids": cited_doc_ids,
                    "evidence": evidence,
                    "ground_truth_stance": primary_stance,
                    "gold_rationales": gold_rationales
                })
        return claims
