# TrialBench × TabPFN-2.5 — Baseline vs. 10-epoch Fine-tune

Generated: 2026-05-10T10:57:34  
Device: NVIDIA H200 NVL  
Pretrained classifier ckpt: `/data2/zhu11/TB/TabPFN/models/tabpfn-v2.5-classifier-v2.5_default.ckpt`  
Run config: epochs=10, lr=2e-05, n_estimators=2, seed=0

Baseline = TabPFN in-context learning (no gradient updates). Fine-tuned = `FinetunedTabPFNClassifier`/`...Regressor` for 10 epochs. Same train/test split (TrialBench default, all phases concatenated).

## Binary classification

| Task | n_train | n_test | ROC-AUC base | ROC-AUC ft | PR-AUC base | PR-AUC ft | LogLoss base | LogLoss ft | Acc base | Acc ft |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| trial-approval-forecasting | 24468 | 6215 | 0.8305 | 0.8304 | 0.7649 | 0.7649 | 0.4898 | 0.4901 | 0.7459 | 0.7440 |
| patient-dropout-event-forecasting | 30561 | 7741 | 0.8126 | 0.8115 | 0.9399 | 0.9395 | 0.4136 | 0.4137 | 0.8012 | 0.8030 |
| serious-adverse-event-forecasting | 14368 | 3548 | 0.8851 | 0.8840 | 0.9396 | 0.9389 | 0.3929 | 0.3955 | 0.8247 | 0.8224 |
| mortality-event-prediction | 14368 | 3548 | 0.8576 | 0.8572 | 0.7990 | 0.7983 | 0.4600 | 0.4653 | 0.7875 | 0.7878 |

## Multiclass classification

| Task | n_classes | n_train | n_test | Acc base | Acc ft | F1-macro base | F1-macro ft | LogLoss base | LogLoss ft |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| trial-failure-reason-identification | 4 | 16649 | 4120 | 0.4956 | 0.4951 | 0.2750 | 0.2686 | 1.0859 | 1.0846 |

## Regression

| Task | n_train | n_test | MAE base | MAE ft | RMSE base | RMSE ft | R² base | R² ft |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| trial-duration-forecasting | 34188 | 8667 | 401.6967 | 404.0621 | 579.1373 | 576.0957 | 0.2682 | 0.2759 |

## Not applicable

| Task | Reason |
|---|---|
| eligibility-criteria-design | Free-text generation task; not a tabular prediction problem. |
| drug-dose-prediction | Inputs are only SMILES strings and MeSH terms; needs molecular/ontology encoders (TrialBench uses MPNN + mesh_term2feature). No tabular features. |

## Errored runs

(none)

## Notes

- For `trial-duration-forecasting` we report the `time_day` target.
- All phases (Phase1–Phase4) are concatenated for tasks that have phases.
- Long free-text columns are dropped before feeding to TabPFN; see `TEXT_DROP` in `script/trialbench_zero_shot_table.py`.
- Raw metrics dump: `all_metrics.json` in this directory.
