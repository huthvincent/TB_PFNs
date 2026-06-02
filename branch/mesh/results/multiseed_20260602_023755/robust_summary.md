# Robust multi-seed aggregation (mesh)

last5 = mean of last 5 eval epochs (preferred); best = max over evals; final = last epoch.
mean ± std across seeds. Δ = vs B' same metric/phase. Subset = intervention-MeSH-non-empty test trials.

## Phase2
_B' full-last5 noise floor: std=0.0060 (n=10 seeds)_

### Phase2 — metric=last5  (interv subset n=1041)

| Cell | Full | Δ vs B' | Interv-subset | Δ vs B' |
|---|---|---|---|---|
| B' (+I+E) | 0.8594 ± 0.0060 | — | 0.8589 ± 0.0080 | — |
| C: SapBERT | 0.8593 ± 0.0068 | -0.0001 | 0.8611 ± 0.0083 | +0.0022 |
| C: BioLORD-2023 | 0.8625 ± 0.0060 | +0.0031 | 0.8606 ± 0.0053 | +0.0016 |
| C: MedCPT | 0.8640 ± 0.0052 | +0.0046 | 0.8663 ± 0.0059 | +0.0073 |
| C: PubMedBERT | 0.8610 ± 0.0055 | +0.0016 | 0.8626 ± 0.0049 | +0.0037 |

### Phase2 — metric=best  (interv subset n=1041)

| Cell | Full | Δ vs B' | Interv-subset | Δ vs B' |
|---|---|---|---|---|
| B' (+I+E) | 0.8700 ± 0.0034 | — | 0.8721 ± 0.0043 | — |
| C: SapBERT | 0.8674 ± 0.0064 | -0.0026 | 0.8722 ± 0.0055 | +0.0002 |
| C: BioLORD-2023 | 0.8717 ± 0.0033 | +0.0018 | 0.8750 ± 0.0041 | +0.0030 |
| C: MedCPT | 0.8708 ± 0.0052 | +0.0009 | 0.8758 ± 0.0050 | +0.0037 |
| C: PubMedBERT | 0.8722 ± 0.0028 | +0.0022 | 0.8776 ± 0.0037 | +0.0055 |

### Phase2 — metric=final  (interv subset n=1041)

| Cell | Full | Δ vs B' | Interv-subset | Δ vs B' |
|---|---|---|---|---|
| B' (+I+E) | 0.8567 ± 0.0058 | — | 0.8566 ± 0.0078 | — |
| C: SapBERT | 0.8558 ± 0.0062 | -0.0010 | 0.8574 ± 0.0080 | +0.0008 |
| C: BioLORD-2023 | 0.8608 ± 0.0051 | +0.0041 | 0.8588 ± 0.0045 | +0.0021 |
| C: MedCPT | 0.8616 ± 0.0044 | +0.0048 | 0.8634 ± 0.0057 | +0.0068 |
| C: PubMedBERT | 0.8587 ± 0.0054 | +0.0020 | 0.8606 ± 0.0051 | +0.0039 |

## Phase3
_B' full-last5 noise floor: std=0.0072 (n=5 seeds)_

### Phase3 — metric=last5  (interv subset n=675)

| Cell | Full | Δ vs B' | Interv-subset | Δ vs B' |
|---|---|---|---|---|
| B' (+I+E) | 0.8901 ± 0.0072 | — | 0.9122 ± 0.0081 | — |
| C: SapBERT | 0.8893 ± 0.0040 | -0.0008 | 0.9080 ± 0.0066 | -0.0042 |
| C: BioLORD-2023 | 0.8918 ± 0.0051 | +0.0017 | 0.9169 ± 0.0063 | +0.0047 |
| C: MedCPT | 0.8880 ± 0.0055 | -0.0021 | 0.9127 ± 0.0055 | +0.0005 |
| C: PubMedBERT | 0.8893 ± 0.0055 | -0.0009 | 0.9094 ± 0.0073 | -0.0028 |

### Phase3 — metric=best  (interv subset n=675)

| Cell | Full | Δ vs B' | Interv-subset | Δ vs B' |
|---|---|---|---|---|
| B' (+I+E) | 0.9139 ± 0.0048 | — | 0.9300 ± 0.0056 | — |
| C: SapBERT | 0.9079 ± 0.0044 | -0.0060 | 0.9261 ± 0.0036 | -0.0038 |
| C: BioLORD-2023 | 0.9071 ± 0.0016 | -0.0068 | 0.9258 ± 0.0017 | -0.0041 |
| C: MedCPT | 0.9088 ± 0.0045 | -0.0051 | 0.9297 ± 0.0038 | -0.0003 |
| C: PubMedBERT | 0.9094 ± 0.0055 | -0.0045 | 0.9275 ± 0.0075 | -0.0024 |

### Phase3 — metric=final  (interv subset n=675)

| Cell | Full | Δ vs B' | Interv-subset | Δ vs B' |
|---|---|---|---|---|
| B' (+I+E) | 0.8894 ± 0.0069 | — | 0.9101 ± 0.0081 | — |
| C: SapBERT | 0.8878 ± 0.0056 | -0.0016 | 0.9050 ± 0.0060 | -0.0051 |
| C: BioLORD-2023 | 0.8899 ± 0.0042 | +0.0006 | 0.9151 ± 0.0067 | +0.0049 |
| C: MedCPT | 0.8883 ± 0.0048 | -0.0010 | 0.9124 ± 0.0060 | +0.0023 |
| C: PubMedBERT | 0.8872 ± 0.0079 | -0.0021 | 0.9054 ± 0.0081 | -0.0047 |
