# Ablation (fixed, Phase3) — last5 ROC-AUC, n=10 seeds

BASE (I+E): 0.8912 ± 0.0077

| subset (on top of I+E) | size | last5 | Δ vs I+E | paired t | p |
|---|---|---|---|---|---|
| title | 3 | 0.8974 ± 0.0077 | +0.0062 | +1.83 | 0.101  |
| title+mesh_interv | 4 | 0.8968 ± 0.0061 | +0.0056 | +1.66 | 0.131  |
| title+summary | 4 | 0.8946 ± 0.0037 | +0.0035 | +1.47 | 0.176  |
| mesh_cond+mesh_interv | 4 | 0.8916 ± 0.0057 | +0.0004 | +0.16 | 0.879  |
| title+mesh_interv+summary+mesh_cond | 6 | 0.8946 ± 0.0040 | +0.0034 | +1.33 | 0.215  |
