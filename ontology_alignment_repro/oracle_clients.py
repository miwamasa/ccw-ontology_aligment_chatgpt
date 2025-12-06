#!/usr/bin/env python3
import random, os
from typing import List, Tuple, Dict

def simulated_oracle(mask, reference, error_rate=0.0, seed=42):
    """
    mask: list of [s,t,score]
    reference: list of [s,t]
    error_rate: probability to flip the correct answer
    Returns dict { (s,t) : bool }
    """
    random.seed(seed)
    ref_set = set((s,t) for s,t in reference)
    out = {}
    for s,t,score in mask:
        correct = (s,t) in ref_set
        if random.random() < error_rate:
            correct = not correct
        out[(s,t)] = bool(correct)
    return out

def get_oracle_decisions(mask, reference, mode="simulated", error_rate=0.0):
    if mode == "simulated":
        return simulated_oracle(mask, reference, error_rate=error_rate)
    elif mode == "openai":
        raise NotImplementedError("OpenAI client is a placeholder. Insert API calls here (see SPEC.md).")
    elif mode == "gemini":
        raise NotImplementedError("Gemini client is a placeholder. Insert API calls here (see SPEC.md).")
    else:
        raise ValueError("Unknown oracle mode: " + str(mode))
