# Run instructions (summary)

## Quick offline toy run
1. Create Python venv and install requirements:
   python3 -m venv venv
   . venv/bin/activate
   pip install -r requirements.txt

2. Run the toy pipeline (simulated oracle, perfect):
   python run_pipeline.py --mode toy --oracle simulated --error-rate 0.0 --out run_result_perfect.json

3. Run pytest:
   pytest -q

## To integrate with real LogMap and LLMs
- Follow SPEC.md for detailed steps. You will need to:
  - Download the OAEI datasets and reference alignments.
  - Install LogMap (Java) and run it to produce candidate mappings with confidence scores.
  - Replace `run_logmap_stub()` with a parser that reads LogMap output and generates the same JSON structure.
  - Implement the `openai`/`gemini` branches in `oracle_clients.py` with your API calls and strict output parsing.
