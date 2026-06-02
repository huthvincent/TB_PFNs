# Robust multi-seed aggregation

Metrics: **last5** = mean of last 5 eval epochs (preferred, noise-robust); best = max over evals (optimistic); final = last epoch.
Reported as mean ± std across seeds. Δ = vs B' same-metric same-phase.

## Phase2
_B' full-last5 noise floor: std=0.0039 over n=5 seeds_

### Phase2 — metric=last5  (SMILES subset n=844)

| Cell | Full | Δ vs B' | SMILES-subset | Δ vs B' |
|---|---|---|---|---|
| B' (+I+E) | 0.8541 ± 0.0039 | — | 0.8543 ± 0.0032 | — |
| C: ChemBERTa-MLM | 0.8561 ± 0.0069 | +0.0020 | 0.8551 ± 0.0041 | +0.0009 |
| C: ChemBERTa-MTR | 0.8568 ± 0.0043 | +0.0027 | 0.8563 ± 0.0047 | +0.0020 |
| C: MolFormer | 0.8534 ± 0.0038 | -0.0007 | 0.8498 ± 0.0045 | -0.0044 |
| C: Mol2Vec | 0.8570 ± 0.0048 | +0.0029 | 0.8565 ± 0.0065 | +0.0022 |

### Phase2 — metric=best  (SMILES subset n=844)

| Cell | Full | Δ vs B' | SMILES-subset | Δ vs B' |
|---|---|---|---|---|
| B' (+I+E) | 0.8656 ± 0.0059 | — | 0.8675 ± 0.0055 | — |
| C: ChemBERTa-MLM | 0.8707 ± 0.0042 | +0.0051 | 0.8704 ± 0.0045 | +0.0029 |
| C: ChemBERTa-MTR | 0.8688 ± 0.0026 | +0.0032 | 0.8699 ± 0.0045 | +0.0024 |
| C: MolFormer | 0.8664 ± 0.0075 | +0.0008 | 0.8663 ± 0.0079 | -0.0012 |
| C: Mol2Vec | 0.8683 ± 0.0049 | +0.0027 | 0.8702 ± 0.0061 | +0.0027 |

### Phase2 — metric=final  (SMILES subset n=844)

| Cell | Full | Δ vs B' | SMILES-subset | Δ vs B' |
|---|---|---|---|---|
| B' (+I+E) | 0.8514 ± 0.0045 | — | 0.8515 ± 0.0038 | — |
| C: ChemBERTa-MLM | 0.8540 ± 0.0069 | +0.0025 | 0.8535 ± 0.0053 | +0.0020 |
| C: ChemBERTa-MTR | 0.8537 ± 0.0037 | +0.0022 | 0.8534 ± 0.0030 | +0.0020 |
| C: MolFormer | 0.8512 ± 0.0052 | -0.0002 | 0.8480 ± 0.0059 | -0.0035 |
| C: Mol2Vec | 0.8540 ± 0.0045 | +0.0026 | 0.8528 ± 0.0066 | +0.0013 |

## Phase3
_B' full-last5 noise floor: std=0.0033 over n=5 seeds_

### Phase3 — metric=last5  (SMILES subset n=470)

| Cell | Full | Δ vs B' | SMILES-subset | Δ vs B' |
|---|---|---|---|---|
| B' (+I+E) | 0.8925 ± 0.0033 | — | 0.9087 ± 0.0075 | — |
| C: ChemBERTa-MLM | 0.8858 ± 0.0066 | -0.0067 | 0.9044 ± 0.0052 | -0.0043 |
| C: ChemBERTa-MTR | 0.8887 ± 0.0103 | -0.0038 | 0.9009 ± 0.0079 | -0.0078 |
| C: MolFormer | 0.8915 ± 0.0060 | -0.0009 | 0.9110 ± 0.0060 | +0.0023 |
| C: Mol2Vec | 0.8898 ± 0.0054 | -0.0027 | 0.9076 ± 0.0049 | -0.0011 |

### Phase3 — metric=best  (SMILES subset n=470)

| Cell | Full | Δ vs B' | SMILES-subset | Δ vs B' |
|---|---|---|---|---|
| B' (+I+E) | 0.9150 ± 0.0051 | — | 0.9324 ± 0.0032 | — |
| C: ChemBERTa-MLM | 0.9099 ± 0.0026 | -0.0051 | 0.9242 ± 0.0058 | -0.0082 |
| C: ChemBERTa-MTR | 0.9091 ± 0.0066 | -0.0059 | 0.9231 ± 0.0047 | -0.0093 |
| C: MolFormer | 0.9106 ± 0.0037 | -0.0045 | 0.9269 ± 0.0016 | -0.0056 |
| C: Mol2Vec | 0.9130 ± 0.0024 | -0.0021 | 0.9309 ± 0.0032 | -0.0015 |

### Phase3 — metric=final  (SMILES subset n=470)

| Cell | Full | Δ vs B' | SMILES-subset | Δ vs B' |
|---|---|---|---|---|
| B' (+I+E) | 0.8909 ± 0.0044 | — | 0.9078 ± 0.0083 | — |
| C: ChemBERTa-MLM | 0.8851 ± 0.0071 | -0.0059 | 0.9034 ± 0.0077 | -0.0044 |
| C: ChemBERTa-MTR | 0.8858 ± 0.0107 | -0.0051 | 0.8993 ± 0.0081 | -0.0086 |
| C: MolFormer | 0.8905 ± 0.0046 | -0.0004 | 0.9108 ± 0.0061 | +0.0029 |
| C: Mol2Vec | 0.8862 ± 0.0057 | -0.0048 | 0.9058 ± 0.0076 | -0.0021 |
