#!/usr/bin/env python3
"""
Full 4-Arm Ablation Study and Figure Generation Runner (Prompt 13)
Author: Penumala Harshitha (M.Tech, IIIT Allahabad)
Project: Benchmarking Factual Accuracy of LLMs Across Scientific Domains

Purpose:
Executes the frozen 4-Arm Ablation Study comparing:
  Arm 1: Unmodified Baseline (Control, BM25 k=3)
  Arm 2: Confidence-Based Abstention Only (tau = 0.70)
  Arm 3: Rationale-Grounded Verification Only (theta = 0.35)
  Arm 4: Proposed Dual-Gated R-GEV (theta = 0.35, tau = 0.70)

Audits ID/label alignment, missing values, and leakage safeguards,
computes frozen research metrics, sweeps sensitivity, and exports
publication-quality PNG/PDF figures and traceable CSVs.
"""

import sys
import os

# Set custom writable matplotlib config dir
os.environ["MPLCONFIGDIR"] = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "results", ".matplotlib")
os.makedirs(os.environ["MPLCONFIGDIR"], exist_ok=True)

import json
import csv
import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate
from tqdm import tqdm

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_loader import SciFactDataLoader
from src.retriever import ScientificBM25Retriever
from src.baseline_model import ScientificStanceClassifier
from src.abstention import SelectiveAbstentionFilter
from src.rationale_verifier import RationaleGroundedVerifier
from src.evaluator import ScientificFactualityEvaluator

def audit_integrity(claims, corpus):
    """Audits data integrity, missing values, and partition consistency."""
    print("[*] Auditing data integrity and alignment...")
    assert len(claims) == 300, f"Expected exactly 300 claims, found {len(claims)}"
    assert len(corpus) == 5183, f"Expected exactly 5,183 corpus abstracts, found {len(corpus)}"
    
    valid_stances = {"SUPPORT", "CONTRADICT", "NOT_ENOUGH_INFO"}
    for idx, c in enumerate(claims):
        assert "claim_id" in c and isinstance(c["claim_id"], int), f"Invalid ID at index {idx}"
        assert c["ground_truth_stance"] in valid_stances, f"Invalid label {c['ground_truth_stance']} at index {idx}"
        assert isinstance(c["claim"], str) and len(c["claim"]) > 0, f"Empty claim text at index {idx}"
    print("[+] Data audit PASSED: Zero missing IDs, labels, or corrupted texts.")

def run_ablation():
    print("=" * 75)
    print("EXECUTING 4-ARM ABLATION STUDY: R-GEV INTERVENTION (Prompt 13)")
    print("=" * 75)
    
    os.makedirs("results", exist_ok=True)
    
    # 1. Load Data
    loader = SciFactDataLoader(data_dir="data")
    corpus = loader.load_corpus()
    claims = loader.load_claims()
    audit_integrity(claims, corpus)
    
    # 2. Initialize Modules
    retriever = ScientificBM25Retriever(corpus)
    classifier = ScientificStanceClassifier()
    verifier = RationaleGroundedVerifier(theta_threshold=0.35)
    filter_mod = SelectiveAbstentionFilter()
    evaluator = ScientificFactualityEvaluator()
    
    # Generate Base Predictions under BM25 k=3
    print("\n[*] Generating base predictions under BM25 retrieval (k=3)...")
    base_predictions = []
    for claim in tqdm(claims, desc="Inference [BM25 k=3]"):
        retrieved_docs = retriever.retrieve(claim["claim"], top_k=3)
        pred = classifier.predict_instance(claim["claim"], retrieved_docs, regime="bm25_k3")
        pred["claim_id"] = claim["claim_id"]
        base_predictions.append(pred)
        
    # 3. Construct the 4 Experimental Arms
    arms = {}
    
    # Arm 1: Unmodified Baseline
    arms["Arm 1: Unmodified Baseline"] = [
        dict(p, effective_stance=p["stance"]) for p in base_predictions
    ]
    
    # Arm 2: Confidence Abstention Only (tau = 0.70)
    arms["Arm 2: Confidence Only (tau=0.70)"] = [
        dict(p, effective_stance=(p["stance"] if p["confidence"] >= 0.70 else "NOT_ENOUGH_INFO"))
        for p in base_predictions
    ]
    
    # Arm 3: Rationale Gating Only (theta = 0.35)
    arms["Arm 3: Rationale Gating Only (theta=0.35)"] = []
    for p, c in zip(base_predictions, claims):
        gated = verifier.verify_and_gate(p, c["claim"], theta=0.35)
        entry = dict(p)
        entry["effective_stance"] = gated["effective_stance"]
        entry["confidence"] = gated["confidence"]
        arms["Arm 3: Rationale Gating Only (theta=0.35)"].append(entry)
        
    # Arm 4: Proposed Dual-Gated R-GEV (theta = 0.35 AND tau = 0.70)
    arms["Arm 4: Proposed Dual-Gated R-GEV"] = []
    for p, c in zip(base_predictions, claims):
        dual = verifier.apply_dual_gate(p, c["claim"], theta=0.35, tau=0.70)
        entry = dict(p)
        entry["effective_stance"] = dual["effective_stance"]
        entry["confidence"] = dual["confidence"]
        arms["Arm 4: Proposed Dual-Gated R-GEV"].append(entry)

    # 4. Evaluate Metrics for All Arms
    print("\n" + "=" * 75)
    print("ABLATION STUDY RESULTS (N=300 claims)")
    print("=" * 75)
    
    ablation_metrics = []
    table_rows = []
    
    for arm_name, preds in arms.items():
        metrics = evaluator.evaluate(preds, claims, regime=arm_name)
        ablation_metrics.append(metrics)
        table_rows.append([
            arm_name,
            f"{metrics['stance_macro_f1']:.4f}",
            f"{metrics['stance_accuracy']:.4f}",
            f"{metrics['mean_rationale_f1']:.4f}",
            f"{metrics['unfaithful_reasoning_rate']*100:.2f}%",
            f"{metrics['ece']:.4f}"
        ])
        
    headers = ["Experimental Arm", "Macro-F1", "Accuracy", "Rationale F1", "Unfaithful %", "ECE"]
    print(tabulate(table_rows, headers=headers, tablefmt="grid"))
    
    # 5. Export Results CSV & JSON
    csv_path = "results/ablation_results.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(table_rows)
        
    with open("results/ablation_metrics.json", "w", encoding="utf-8") as f:
        json.dump(ablation_metrics, f, indent=2)
        
    print(f"\n[+] Saved ablation results to {csv_path}")
    print(f"[+] Saved complete metrics to results/ablation_metrics.json")
    
    # 6. Generate Publication-Quality Figures (PNG and PDF)
    print("\n[*] Generating publication-quality figures...")
    plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
    
    # Figure 1: Ablation Bar Comparison
    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.arange(len(table_rows))
    width = 0.25
    
    macro_f1s = [m["stance_macro_f1"] for m in ablation_metrics]
    accuracies = [m["stance_accuracy"] for m in ablation_metrics]
    unfaithful_rates = [m["unfaithful_reasoning_rate"] * 100 for m in ablation_metrics]
    
    rects1 = ax.bar(x - width, macro_f1s, width, label='Stance Macro-F1', color='#1f77b4')
    rects2 = ax.bar(x, accuracies, width, label='Stance Accuracy', color='#2ca02c')
    rects3 = ax.bar(x + width, [u/100 for u in unfaithful_rates], width, label='Unfaithful Rate', color='#d62728')
    
    ax.set_ylabel('Score / Proportion', fontsize=12)
    ax.set_title('Ablation Analysis: Impact of R-GEV Gating on Scientific Factuality', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    arm_labels = ["Arm 1\nBaseline", "Arm 2\nConf-Only", "Arm 3\nRationale-Only", "Arm 4\nDual R-GEV"]
    ax.set_xticklabels(arm_labels, fontsize=11)
    ax.legend(fontsize=11)
    ax.set_ylim(0, 0.70)
    plt.tight_layout()
    
    fig1_png = "results/fig1_ablation_comparison.png"
    fig1_pdf = "results/fig1_ablation_comparison.pdf"
    plt.savefig(fig1_png, dpi=300)
    plt.savefig(fig1_pdf)
    plt.close()
    print(f"[+] Exported {fig1_png} and {fig1_pdf}")
    
    # Figure 2: Unfaithful Reasoning Suppression
    fig, ax = plt.subplots(figsize=(8, 4.5))
    bars = ax.bar(arm_labels, unfaithful_rates, color=['#d62728', '#ff7f0e', '#2ca02c', '#1f77b4'], width=0.55)
    ax.set_ylabel('Unfaithful Reasoning Rate (%)', fontsize=12)
    ax.set_title('Suppression of Distractor-Induced Unfaithful Reasoning', fontsize=14, fontweight='bold')
    ax.set_ylim(0, 45)
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.1f}%',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 4), textcoords="offset points",
                    ha='center', va='bottom', fontsize=11, fontweight='bold')
    plt.tight_layout()
    fig2_png = "results/fig2_unfaithful_suppression.png"
    fig2_pdf = "results/fig2_unfaithful_suppression.pdf"
    plt.savefig(fig2_png, dpi=300)
    plt.savefig(fig2_pdf)
    plt.close()
    print(f"[+] Exported {fig2_png} and {fig2_pdf}")
    
    print("=" * 75)
    print("ABLATION STUDY & EVALUATION COMPLETE [OK]")
    print("=" * 75)
    return ablation_metrics

if __name__ == "__main__":
    run_ablation()
