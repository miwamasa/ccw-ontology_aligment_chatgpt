# Repro package for "Large Language Models as Oracles for Ontology Alignment"

This package contains a **repro instructions**, **implementation stubs**, **prompt templates**, and **testcases**
to reproduce the experiments and evaluation workflow described in the uploaded paper. The artifact was
created based on the paper you provided. See the paper for the experimental details.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest -q

# Run toy pipeline with perfect oracle
python run_pipeline.py --mode toy --oracle simulated --error-rate 0.0 --out result.json
```

## Documentation

- **[Overview](doc/overview.md)** - プロジェクト全体の詳細説明（日本語）
- **[Testing Guide](doc/testing.md)** - テストの詳細とトラブルシューティング（日本語）
- **[Quick Start](doc/quickstart.md)** - 5分で始めるガイド（日本語）
- **[Test Results Sample](doc/test_results_sample.md)** - テスト実行結果のサンプル（日本語）
- **[SPEC.md](SPEC.md)** - 詳細な技術仕様（英語）
- **[RUN_INSTRUCTIONS.md](RUN_INSTRUCTIONS.md)** - 実行手順（英語）

## Project Structure

```
ontology_alignment_repro/
├── README.md                 # This file
├── SPEC.md                   # Technical specification
├── RUN_INSTRUCTIONS.md       # Run instructions
├── requirements.txt          # Python dependencies
├── prompts.txt              # Prompt templates
├── run_pipeline.py          # Main pipeline
├── logmap_stub.py           # LogMap simulator
├── oracle_clients.py        # Oracle implementations
├── eval.py                  # Evaluation functions
├── tests/
│   ├── conftest.py         # pytest configuration
│   └── test_pipeline.py    # Test cases
└── doc/
    ├── overview.md         # Project overview (Japanese)
    ├── testing.md          # Testing guide (Japanese)
    ├── quickstart.md       # Quick start guide (Japanese)
    └── test_results_sample.md  # Test results samples (Japanese)
```

## Testing

All tests pass successfully:

```bash
$ pytest -v
============================= test session starts ==============================
tests/test_pipeline.py::test_toy_perfect_oracle PASSED                   [ 50%]
tests/test_pipeline.py::test_toy_noisy_oracle PASSED                     [100%]

============================== 2 passed in 0.02s
```

See [doc/testing.md](doc/testing.md) for detailed testing information.
