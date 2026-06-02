# Multi-seed summary (multiseed_20260602_002504)

seeds=[0, 1, 2, 3, 4], epochs=30, metric=best-epoch test ROC-AUC (mean ± std)

## Phase2  (full test; SMILES subset n=844)

| Cell | Full ROC-AUC | Δ vs B' (full) | SMILES-subset ROC-AUC | Δ vs B' (subset) |
|---|---|---|---|---|
| B' (+I+E) | 0.8656 ± 0.0059 | — | 0.8675 ± 0.0055 | — |
| C: ChemBERTa-MLM | 0.8707 ± 0.0042 | +0.0051 | 0.8704 ± 0.0045 | +0.0029 |
| C: ChemBERTa-MTR | 0.8688 ± 0.0026 | +0.0032 | 0.8699 ± 0.0045 | +0.0024 |
| C: MolFormer | 0.8664 ± 0.0075 | +0.0008 | 0.8663 ± 0.0079 | -0.0012 |
| C: Mol2Vec | 0.8683 ± 0.0049 | +0.0027 | 0.8702 ± 0.0061 | +0.0027 |

## Phase3  (full test; SMILES subset n=470)

| Cell | Full ROC-AUC | Δ vs B' (full) | SMILES-subset ROC-AUC | Δ vs B' (subset) |
|---|---|---|---|---|
| B' (+I+E) | 0.9150 ± 0.0051 | — | 0.9324 ± 0.0032 | — |
| C: ChemBERTa-MLM | 0.9099 ± 0.0026 | -0.0051 | 0.9255 ± 0.0040 | -0.0069 |
| C: ChemBERTa-MTR | 0.9091 ± 0.0066 | -0.0059 | 0.9231 ± 0.0047 | -0.0093 |
| C: MolFormer | 0.9106 ± 0.0037 | -0.0045 | 0.9276 ± 0.0016 | -0.0048 |
| C: Mol2Vec | 0.9130 ± 0.0024 | -0.0021 | 0.9309 ± 0.0032 | -0.0015 |
