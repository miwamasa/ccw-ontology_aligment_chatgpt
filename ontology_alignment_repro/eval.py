#!/usr/bin/env python3
from typing import Set, Tuple, List

def evaluate_alignment(final_alignment: List[Tuple[str,str]], reference: List[Tuple[str,str]]):
    final_set = set(tuple(x) for x in final_alignment)
    ref_set = set(tuple(x) for x in reference)
    tp = len(final_set & ref_set)
    fp = len(final_set - ref_set)
    fn = len(ref_set - final_set)
    pr = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    re = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2*pr*re/(pr+re) if (pr+re) > 0 else 0.0
    return {"precision": pr, "recall": re, "f1": f1, "tp": tp, "fp": fp, "fn": fn}

def compute_oracle_diagnostics(mask, oracle_decisions, reference):
    mask_pairs = [ (s,t) for s,t,_ in mask ]
    ref_set = set(tuple(x) for x in reference)
    tp = sum(1 for p in mask_pairs if oracle_decisions.get(tuple(p), False) and tuple(p) in ref_set)
    tn = sum(1 for p in mask_pairs if (not oracle_decisions.get(tuple(p), False)) and tuple(p) not in ref_set)
    fp = sum(1 for p in mask_pairs if oracle_decisions.get(tuple(p), False) and tuple(p) not in ref_set)
    fn = sum(1 for p in mask_pairs if (not oracle_decisions.get(tuple(p), False)) and tuple(p) in ref_set)
    se = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    sp = tn / (tn + fp) if (tn + fp) > 0 else 0.0
    yi = se + sp - 1
    return {"sensitivity": se, "specificity": sp, "youden_index": yi, "tp": tp, "tn": tn, "fp": fp, "fn": fn}
