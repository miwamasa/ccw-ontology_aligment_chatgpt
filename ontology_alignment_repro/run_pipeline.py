#!/usr/bin/env python3
import argparse, os, json
from logmap_stub import run_logmap_stub
from oracle_clients import get_oracle_decisions
from eval import evaluate_alignment

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--mode", choices=["toy","from_logmap"], default="toy",
                   help="toy: run the offline toy pipeline. from_logmap: consume LogMap JSON output.")
    p.add_argument("--oracle", choices=["simulated","openai","gemini"], default="simulated")
    p.add_argument("--error-rate", type=float, default=0.0, help="error rate for simulated oracle (0.0 = perfect)")
    p.add_argument("--out", default="run_result.json")
    args = p.parse_args()

    if args.mode == "toy":
        # run a simulated LogMap and get candidate alignments + Mask and reference
        data = run_logmap_stub()
    else:
        raise NotImplementedError("from_logmap mode expects a LogMap JSON export. See SPEC.md to adapt.")

    # Query oracle for Mask decisions (returns dict mapping pair->True/False)
    oracle_decisions = get_oracle_decisions(data['mask'], data['reference'], mode=args.oracle, error_rate=args.error_rate)

    # Apply oracle decisions: accept mappings labelled True, reject False.
    final_alignment = set()
    # Keep automatic high-confidence mappings
    for m in data['automatic']:
        final_alignment.add(tuple(m))
    # Add those accepted by oracle
    for m,dec in oracle_decisions.items():
        if dec:
            final_alignment.add(tuple(m))

    metrics = evaluate_alignment(final_alignment, data['reference'])
    out = {
        "final_alignment": list(final_alignment),
        "metrics": metrics,
        "oracle_decisions": {f"{k[0]}|||{k[1]}": v for k,v in oracle_decisions.items()}
    }
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print(json.dumps(metrics, indent=2))

if __name__ == '__main__':
    main()
