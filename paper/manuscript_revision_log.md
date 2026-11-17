# Manuscript Revision Log

**Manuscript Title**: Benchmarking Scientific Claim Verification and Hallucination Mitigation under Distractor Accumulation and Selective Abstention: An Empirical Study on Biomedical Literature  
**Author**: Penumala Harshitha (M.Tech, Department of Information Technology, IIIT Allahabad)  
**Revision Date**: 2026-11-17  
**Associated Report**: `paper/peer_review_report.md`  

---

## 1. Summary of Changes

In response to the critical peer review conducted under Prompt 16, the draft manuscript (`paper/main.tex`) has undergone rigorous revision to eliminate overclaims, qualify lexical heuristics, contextualize baseline comparisons, and scope empirical findings to the biomedical domain.

| Change ID | Reviewer Item | Affected Section | Original Draft Text | Revised Manuscript Text | Scientific Rationale |
|---|---|---|---|---|---|
| **REV-001** | Scope to Biomedical Literature | Title & Abstract | *"Benchmarking Scientific Claim Verification and Hallucination Mitigation under Distractor Accumulation and Selective Abstention"* | *"Benchmarking Scientific Claim Verification and Hallucination Mitigation under Distractor Accumulation and Selective Abstention: An Empirical Study on Biomedical Literature"* | Prevents unwarranted generalization to domains with formal mathematics or non-textual evidence. |
| **REV-002** | Qualify Lexical Support Gate | Sec. IV-B, IV-C | Gate 1 referred to as *"Atomic Evidence Support Gate"* | Renamed to *"Atomic Lexical Support Gate"*; explicitly noted that token intersection operates bag-of-words without syntactic dependency modeling. | Clarifies that Gate 1 is a lexical distractor filter rather than a neural natural language inference (NLI) model. |
| **REV-003** | Contextualize Oracle Upper Bound | Abstract, Sec. VI-B, Sec. VIII | *"nearly recovering the 0.4266 Oracle upper bound"* | *"approaching the Oracle stance Macro-F1 level (0.4153 vs. 0.4266) primarily through disciplined abstention, though rationale evidence attribution remains bounded by retrieval recall (Rationale F1: 0.3075 vs. 0.4550)"* | Eliminates misleading claim that retrieval distractor noise was completely solved. |
| **REV-004** | Justify Hyperparameters | Sec. IV-B, Sec. IV-C | Fixed constants $\theta=0.35, \tau=0.70$ and rank decay factor $0.10$ without explanation. | Added explicit linguistic justification for $\theta=0.35$ (three-token subject-predicate-object triad) and rank decay factor $0.10$ (10% penalty per rank step). | Addresses reviewer skepticism regarding arbitrary constant selection. |
| **REV-005** | Explain Closed-Book ECE Artifact | Sec. VI-A (Table I) | Reported Closed-Book ECE = 0.0267 without explanation. | Added explanatory text: *"We note that the apparently low ECE of the Closed-Book regime (0.0267) is an evaluation artifact: absent external evidence, the model uniformly outputs low confidence scores... matching dataset base accuracy."* | Prevents naive readers from assuming closed-book guessing is better calibrated than retrieval-augmented reasoning. |
| **REV-006** | Explain Residual Unfaithful Reasoning | Sec. VII-A, Sec. VII-B | Brief note on 16.78% unfaithful rate without mechanistic linkage. | Linked residual unfaithful rate directly to lexical overlap limits: token intersection cannot resolve syntactic negation (e.g., "failed to inhibit") or antonymous semantic inversion. | Provides a scientifically honest explanation grounded in the architecture's inherent properties. |

---

## 2. Verification of Numerical Consistency

All quantitative data in the revised manuscript were re-audited against `results/master_results.csv`, `results/summary_metrics.json`, and `results/statistical_test_report.json`:
- **Corpus size**: 5,183 abstracts `[VERIFIED]`
- **Dev claim count**: 300 claims `[VERIFIED]`
- **Arm 1 Macro-F1**: 0.2719, Accuracy: 0.4133, Unfaithful: 33.06%, ECE: 0.3578 `[VERIFIED]`
- **Arm 2 Macro-F1**: 0.3443, Accuracy: 0.4333, Unfaithful: 20.00%, ECE: 0.3378 `[VERIFIED]`
- **Arm 3 Macro-F1**: 0.4054, Accuracy: 0.4900, Unfaithful: 25.85%, ECE: 0.3327 `[VERIFIED]`
- **Arm 4 Macro-F1**: 0.4153, Accuracy: 0.4967, Unfaithful: 16.78%, ECE: 0.3260 `[VERIFIED]`
- **Paired Bootstrap**: $p < 0.001$ ($p = 0.00000$), 95% CI: $[0.0934, 0.1920]$ `[VERIFIED]`
- **Data Leakage**: 0 overlapping claims between dev and train partitions `[VERIFIED]`

---

## 3. Current Manuscript Status
- **LaTeX Source**: `paper/main.tex` (Revised, clean IEEEtran syntax, no markdown asterisks).
- **BibTeX Source**: `paper/references.bib` (21 verified primary citations).
- **Figures**: `paper/figures/fig1` through `fig4` (Vector PDF + 300 DPI PNG).
- **Readiness**: Ready for direct upload and compilation in Overleaf.
