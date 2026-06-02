# Aggregate branch — multiseed (last5 ROC-AUC, mean±std, paired t vs B')

## Phase2

| Cell | tokens | last5 ROC-AUC | Δ vs B' | paired t | p |
|---|---|---|---|---|---|
| B' (I+E) | 2 | 0.8585 ± 0.0054 (n=10) | — | — | — |
| +all text (I+E+9text) | 11 | 0.8532 ± 0.0066 (n=10) | -0.0053 | -2.10 | 0.065 * |
| ALL (+SMILES) | 12 | 0.8571 ± 0.0065 (n=10) | -0.0014 | -0.75 | 0.471  |

## Phase3

| Cell | tokens | last5 ROC-AUC | Δ vs B' | paired t | p |
|---|---|---|---|---|---|
| B' (I+E) | 2 | 0.8851 ± 0.0094 (n=10) | — | — | — |
| +all text (I+E+9text) | 11 | 0.8854 ± 0.0075 (n=10) | +0.0002 | +0.07 | 0.945  |
| ALL (+SMILES) | 12 | 0.8878 ± 0.0101 (n=10) | +0.0026 | +0.73 | 0.485  |
