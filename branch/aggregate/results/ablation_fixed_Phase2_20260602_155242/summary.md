# Ablation (fixed, Phase2) — last5 ROC-AUC, n=10 seeds

BASE (I+E): 0.8604 ± 0.0039

| subset (on top of I+E) | size | last5 | Δ vs I+E | paired t | p |
|---|---|---|---|---|---|
| title+mesh_interv_q3 | 4 | 0.8680 ± 0.0034 | +0.0076 | +5.23 | 0.001 *** |
| title+mesh_interv | 4 | 0.8698 ± 0.0030 | +0.0094 | +6.16 | 0.000 *** |
| mesh_cond_q3+mesh_interv_q3 | 4 | 0.8670 ± 0.0036 | +0.0066 | +3.81 | 0.004 *** |
| title+mesh_cond_q3+mesh_interv_q3 | 5 | 0.8667 ± 0.0043 | +0.0063 | +3.52 | 0.007 *** |
