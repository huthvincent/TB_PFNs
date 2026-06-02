# SAE Phase2 — token-configuration comparison

Frozen TabICLv2, Full Step 2. last5 test ROC-AUC (mean of last-5 eval epochs), mean ± std over n=10 seeds, all evaluated in one process / same seeds / shared base so deltas are properly paired. p = paired t-test vs *tabular + I/E*.

| Configuration | tokens | ROC-AUC | Δ vs tabular | Δ vs tabular+I/E (p) |
|---|---|---|---|---|
| tabular only (zero-shot) | 0 | 0.7810 ± 0.0000 | — | — |
| tabular + I/E | 2 | 0.8566 ± 0.0052 | +0.0756 | — |
| + brief_title | 3 | 0.8652 ± 0.0050 | +0.0842 | +0.0086 (p=0.005) *** |
| + title + intervention_MeSH  (BEST) | 4 | 0.8658 ± 0.0045 | +0.0848 | +0.0092 (p=0.001) *** |
| + condition + intervention MeSH | 4 | 0.8611 ± 0.0027 | +0.0800 | +0.0045 (p=0.050) ** |
| + all 9 text columns | 11 | 0.8551 ± 0.0044 | +0.0740 | -0.0015 (p=0.441)  |
| + all 9 text + SMILES (12 tokens) | 12 | 0.8530 ± 0.0060 | +0.0720 | -0.0036 (p=0.045) ** |
