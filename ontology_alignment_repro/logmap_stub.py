#!/usr/bin/env python3
# Minimal simulator for LogMap outputs for toy runs.
# Produces:
# - automatic: high-confidence mappings (list of [s,t])
# - mask: uncertain candidate mappings (list of [s,t, score])
# - reference: set of true mappings (list of [s,t])

def run_logmap_stub():
    # small toy example: two simple ontologies with overlapping concepts
    automatic = [
        ["O1:Cell", "O2:Cell"],  # high confidence - correct
        ["O1:Tissue", "O2:Tissue"]  # high confidence - correct
    ]
    # mask contains uncertain candidates (we include both true and false entries)
    mask = [
        ["O1:AlveolusEpithelium", "O2:AlveolarEpithelium", 0.45],
        ["O1:LungEpithelium", "O2:Epithelium", 0.5],
        ["O1:MouseGeneX", "O2:HumanGeneY", 0.4]
    ]
    # reference alignment - ground truth
    reference = [
        ["O1:Cell", "O2:Cell"],
        ["O1:Tissue", "O2:Tissue"],
        ["O1:AlveolusEpithelium", "O2:AlveolarEpithelium"],
        ["O1:LungEpithelium", "O2:Epithelium"]
    ]
    return {"automatic": automatic, "mask": mask, "reference": reference}
