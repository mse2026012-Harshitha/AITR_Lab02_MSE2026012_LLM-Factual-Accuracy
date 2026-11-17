#!/usr/bin/env python3
"""
Complete Baseline Reproduction and Experimental Pipeline Runner
Author: Penumala Harshitha (M.Tech, IIIT Allahabad)
Project: Benchmarking Factual Accuracy of LLMs Across Scientific Domains

Purpose:
Executes the frozen 5-module pipeline across the three experimental regimes
(Closed-Book, Oracle Context, BM25 Retrieved k=1, 3, 5), logs raw predictions,
computes metrics, and saves traceable evaluation artifacts.
"""

import sys
import os
import json
import csv
from tabulate import tabulate
from tqdm import tqdm

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_loader import SciFactDataLoader
from src.retriever import ScientificBM25Retriever
from src.baseline_model import ScientificStanceClassifier
from src.abstention import SelectiveAbstentionFilter
from src.evaluator import ScientificFactualityEvaluator

def run_pipeline():
    print("=" * 75)
    print("EXECUTING SCIENTIFIC FACTUALITY BENCHMARK PIPELINE")
    print("=" * 75)
    
    os.makedirs("results", exist_ok=True)
    
    # 1. Load Data
    loader = SciFactDataLoader(data_dir="data")
    corpus = loader.load_corpus()
    claims = loader.load_claims()
    print(f"[*] Loaded {len(corpus):,} corpus abstracts and {len(claims):,} dev claims.")
    
    # 2. Initialize Modules
    retriever = ScientificBM25Retriever(corpus)
    classifier = ScientificStanceClassifier()
    filter_mod = SelectiveAbstentionFilter()
    evaluator = ScientificFactualityEvaluator()
    
    regimes = ["closed_book", "oracle", "bm25_k1", "bm25_k3", "bm25_k5"]
    all_results = []
    saved_predictions = {}
    
    for regime in regimes:
        print(f"\n[*] Evaluating Regime: {regime}...")
        predictions = []
        
        for claim in tqdm(claims, desc=f"Inference [{regime}]"):
            claim_text = claim["claim"]
            
            if regime == "closed_book":
                pred = classifier.predict_instance(claim_text, None, regime="closed_book")
            elif regime == "oracle":
                # Find gold cited document if exists
                cited_ids = claim.get("cited_doc_ids", [])
                gold_doc = corpus.get(cited_ids[0]) if cited_ids and cited_ids[0] in corpus else None
                pred = classifier.predict_instance(claim_text, gold_doc, regime="oracle")
            elif regime.startswith("bm25"):
                k = int(regime.split("_k")[1])
                retrieved_docs = retriever.retrieve(claim_text, top_k=k)
                pred = classifier.predict_instance(claim_text, retrieved_docs, regime=regime)
                
            pred["claim_id"] = claim["claim_id"]
            predictions.append(pred)
            
        saved_predictions[regime] = predictions
        
        # Evaluate regime metrics
        metrics = evaluator.evaluate(predictions, claims, regime=regime)
        all_results.append(metrics)
        
    # 3. Print Results Summary Table
    print("\n" + "=" * 75)
    print("BENCHMARK COMPARATIVE RESULTS SUMMARY")
    print("=" * 75)
    
    table_rows = []
    for r in all_results:
        table_rows.append([
            r["regime"],
            f"{r['stance_macro_f1']:.4f}",
            f"{r['stance_accuracy']:.4f}",
            f"{r['mean_rationale_f1']:.4f}",
            f"{r['unfaithful_reasoning_rate']*100:.2f}%",
            f"{r['ece']:.4f}"
        ])
        
    headers = ["Regime", "Macro-F1", "Accuracy", "Rationale F1", "Unfaithful %", "ECE"]
    print(tabulate(table_rows, headers=headers, tablefmt="grid"))
    
    # 4. Selective Prediction & Abstention Analysis (Kalai et al., 2026 test on bm25_k3)
    print("\n" + "=" * 75)
    print("SELECTIVE PREDICTION & ABSTENTION ANALYSIS (Kalai et al., 2026 on bm25_k3)")
    print("=" * 75)
    
    gold_labels = [c["ground_truth_stance"] for c in claims]
    risk_curve = filter_mod.compute_risk_coverage_curve(saved_predictions["bm25_k3"], gold_labels)
    
    curve_rows = []
    for pt in risk_curve:
        curve_rows.append([
            pt["tau"],
            f"{pt['coverage']*100:.1f}%",
            f"{pt['selective_accuracy']*100:.2f}%",
            f"{pt['risk']*100:.2f}%",
            pt["active_count"]
        ])
    print(tabulate(curve_rows, headers=["Tau", "Coverage", "Selective Acc", "Risk", "Answered Count"], tablefmt="grid"))
    
    # 5. Export Traceable Results
    results_summary_path = "results/summary_metrics.json"
    with open(results_summary_path, "w", encoding="utf-8") as f:
        json.dump({"regimes": all_results, "risk_curve_bm25_k3": risk_curve}, f, indent=2)
        
    csv_path = "results/comparative_results.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(table_rows)
        
    print(f"\n[+] Saved summary metrics to {results_summary_path}")
    print(f"[+] Saved CSV comparison to {csv_path}")
    print("=" * 75)
    print("BENCHMARK PIPELINE EXECUTION COMPLETE [OK]")
    print("=" * 75)
    return all_results

if __name__ == "__main__":
    run_pipeline()
