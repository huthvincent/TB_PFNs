# Ablation (fixed, Phase2) — last5 ROC-AUC, n=10 seeds

BASE (I+E): 0.8602 ± 0.0055

| subset (on top of I+E) | size | last5 | Δ vs I+E | paired t | p |
|---|---|---|---|---|---|
| title | 3 | 0.8650 ± 0.0035 | +0.0047 | +2.08 | 0.067 * |
| title+mesh_interv | 4 | 0.8669 ± 0.0044 | +0.0067 | +3.50 | 0.007 *** |
| title+summary | 4 | 0.8606 ± 0.0076 | +0.0004 | +0.15 | 0.886  |
| mesh_cond+mesh_interv | 4 | 0.8611 ± 0.0042 | +0.0009 | +0.48 | 0.642  |
| title+mesh_interv+summary+mesh_cond | 6 | 0.8602 ± 0.0042 | -0.0001 | -0.02 | 0.981  |
