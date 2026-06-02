# Ablation (fixed, Phase3) — last5 ROC-AUC, n=10 seeds

BASE (I+E): 0.8907 ± 0.0074

| subset (on top of I+E) | size | last5 | Δ vs I+E | paired t | p |
|---|---|---|---|---|---|
| title+mesh_interv_q3 | 4 | 0.8977 ± 0.0032 | +0.0070 | +2.88 | 0.018 ** |
| title+mesh_interv | 4 | 0.8974 ± 0.0076 | +0.0067 | +1.61 | 0.141  |
| mesh_cond_q3+mesh_interv_q3 | 4 | 0.8901 ± 0.0076 | -0.0006 | -0.23 | 0.826  |
| title+mesh_cond_q3+mesh_interv_q3 | 5 | 0.8911 ± 0.0052 | +0.0004 | +0.13 | 0.901  |
