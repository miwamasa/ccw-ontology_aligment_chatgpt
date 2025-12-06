# SPECIFICATION: Reproduction of "LLMs as Oracles for Ontology Alignment"

## Goal
Reproduce the experiments where an ontology alignment system (LogMap) delegates uncertain mappings (Mask)
to an LLM-based Oracle, following the workflow and prompt templates described in the paper.

## High-level pipeline steps
1. Run an automatic matcher (e.g., LogMap) on (O1, O2) to obtain candidate alignment MS and a subset Mask of uncertain mappings.
2. For each mapping m in Mask, build an ontology-driven prompt using one of six templates (P, PEC, PNLF, PNLF_EC, PNLF_S, PNLF_EC+S).
3. Query the Oracle (LLM) for a binary decision (True/False) for each mapping. Optionally, use a short system prompt for framing.
4. Inject Oracle decisions back into the alignment selection stage of LogMap and compute the final alignment.
5. Compare final alignment against reference alignment(s) (MRA) using Precision/Recall/F-score, and evaluate Oracle diagnostics (Sensitivity, Specificity, Youden's index).
6. Repeat experiments across datasets, LLMs, prompt templates, and simulated Oracles with varying error rates.

## Datasets (as used in the paper)
- OAEI Anatomy (mouse-human)
- OAEI Bio-ML (NCIT-DOID, OMIM-ORDO, SNOMED variants)
- LargeBio (FMA, NCI, SNOMED combinations)
> NOTE: the actual OAEI datasets are large and must be downloaded separately (links in the paper and supporting repo).
The package includes a **toy** dataset for quick offline verification in `testcases/`.

## Prompt templates (placeholders)
See `prompts.txt`. The six canonical prompt templates are provided with placeholders you should populate from the ontology:
- label(e), synonyms(e), direct parent(e), parent^2(e) (extended context).

## Oracle modalities
- `simulated`: uses the reference alignment MRA to provide perfect or noisy answers (configurable error rate), used to reproduce Or0, Or10, Or20, Or30 experiments.
- `openai` / `gemini` (placeholders): example client stubs showing how to call an LLM API. You must provide API keys and adapt to your API environment. Output parsing expects a strict "True" or "False".

## Mask selection (as in LogMap)
- LogMap identifies a Mask of uncertain mappings (implementation detail inside LogMap).
- In the toy stub, Mask is simulated: candidate mappings with confidence inside a configurable band (e.g., [0.3, 0.7]) are placed in Mask.

## Evaluation metrics
- Alignment-level: Precision, Recall, F1 (standard).
- Oracle diagnostics on Mask: Sensitivity (Se), Specificity (Sp), Youden's index YI = Se + Sp − 1.
- Statistical tests: paired t-test / Wilcoxon between variants (not included in toy run; use R/Python to compute when running full experiments).

## Repro steps for full experiments
1. Obtain OAEI datasets and reference alignments.
2. Install LogMap and run it in automatic mode to obtain MS and detailed confidence scores.
3. Extract Mask (mappings with low confidence or flagged uncertain).
4. Populate prompts for each m ∈ Mask and query the Oracle (LLM) or simulated oracle.
5. Merge Oracle decisions and run LogMap's selection stage (or emulate the selection logic).
6. Compute metrics and aggregate results as in the paper (Tables 2-3, Figures 3-6).

## Notes on determinism & repeatability
- Use consistent seed in simulated oracles and prompt batching.
- Rate limits and API variations add nondeterminism for real LLMs; run several independent runs to compute variance (paper used multiple runs to measure YI variability).
