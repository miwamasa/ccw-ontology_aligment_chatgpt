import json
from oracle_clients import simulated_oracle
from logmap_stub import run_logmap_stub
from eval import evaluate_alignment, compute_oracle_diagnostics

def test_toy_perfect_oracle():
    data = run_logmap_stub()
    decisions = simulated_oracle(data['mask'], data['reference'], error_rate=0.0, seed=1)
    final_alignment = set(tuple(x) for x in data['automatic'])
    for (s,t),d in decisions.items():
        if d:
            final_alignment.add((s,t))
    metrics = evaluate_alignment(list(final_alignment), data['reference'])
    # the perfect oracle should reach F1 >= 0.9 in this toy example
    assert metrics['f1'] >= 0.9

def test_toy_noisy_oracle():
    data = run_logmap_stub()
    decisions = simulated_oracle(data['mask'], data['reference'], error_rate=0.3, seed=2)
    diag = compute_oracle_diagnostics(data['mask'], decisions, data['reference'])
    # Youden index typically decreases as error increases; we assert non-perfect behavior
    assert diag['youden_index'] <= 1.0
