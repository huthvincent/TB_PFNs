# TrialBench × TabPFN-2.5 — Tier 1 tuning results

Generated: 2026-05-10T13:40:44  
Device: NVIDIA H200 NVL  
Run config: n_est_grid=[4, 8, 16, 32], lr_grid=[1e-05, 2e-05, 5e-05], ft_epochs=30, n_est_ft=2, ens_seeds=[0, 1, 2]

All hyperparameter and checkpoint choices made on a 80/20 val split of TRAIN. Test set used exactly once per task at the end. Tier-0 column = the 10-epoch fine-tune from `results/TrialBench_TabPFN_baseline/`.

## Headline: Tier 1 vs. Tier 0 (primary metric only)

| Task | Type | Metric | Tier-0 baseline (n_est=2) | Tier-0 ft (10ep) | **Tier-1 test** | Δ vs. Tier-0 baseline | Selected config |
|---|---|---|---:|---:|---:|---:|---|
| trial-approval-forecasting | binary | roc_auc | 0.8305 | 0.8304 | **0.8318** | +0.0012 | `phase=B ckpt=default n_est=32 lr=2e-05` |
| trial-duration-forecasting | regression | r2 | 0.2682 | 0.2759 | **0.2805** | +0.0123 | `phase=B ckpt=default n_est=8 lr=2e-05 log=0` |
| patient-dropout-event-forecasting | binary | roc_auc | 0.8126 | 0.8115 | **0.8140** | +0.0015 | `phase=A ckpt=default n_est=8` |
| serious-adverse-event-forecasting | binary | roc_auc | 0.8851 | 0.8840 | **0.8852** | +0.0001 | `phase=B ckpt=default n_est=32 lr=2e-05` |
| mortality-event-prediction | binary | roc_auc | 0.8576 | 0.8572 | **0.8586** | +0.0011 | `phase=A ckpt=default n_est=16` |
| trial-failure-reason-identification | multiclass | accuracy | 0.4956 | 0.4951 | **0.4922** | -0.0034 | `phase=A ckpt=default n_est=4` |

## Binary classification (test)

| Task | n_train | n_test | ROC-AUC | PR-AUC | LogLoss | Acc (default 0.5) | Acc (tuned) | best_threshold |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| trial-approval-forecasting | 24468 | 6215 | 0.8318 | 0.7693 | 0.4866 | 0.7421 | 0.7443 | 0.4600 |
| patient-dropout-event-forecasting | 30561 | 7741 | 0.8140 | 0.9404 | 0.4116 | 0.8033 | 0.8036 | 0.5500 |
| serious-adverse-event-forecasting | 14368 | 3548 | 0.8852 | 0.9397 | 0.3926 | 0.8213 | 0.8210 | 0.4700 |
| mortality-event-prediction | 14368 | 3548 | 0.8586 | 0.8001 | 0.4577 | 0.7889 | 0.7875 | 0.5200 |

## Multiclass classification (test)

| Task | n_classes | n_train | n_test | Acc | F1-macro | LogLoss |
|---|---:|---:|---:|---:|---:|---:|
| trial-failure-reason-identification | 4 | 16649 | 4120 | 0.4922 | 0.2689 | 1.0858 |

## Regression (test)

| Task | n_train | n_test | MAE | RMSE | R² |
|---|---:|---:|---:|---:|---:|
| trial-duration-forecasting | 34188 | 8667 | 404.6352 | 574.2397 | 0.2805 |

## Not applicable

| Task | Reason |
|---|---|
| eligibility-criteria-design | Free-text generation task; not a tabular prediction problem. |
| drug-dose-prediction | Inputs are only SMILES strings and MeSH terms; needs molecular/ontology encoders (TrialBench uses MPNN + mesh_term2feature). No tabular features. |

## Methodology notes

- **No test leakage**: the 80/20 train/val split is fixed at `random_state=0`. All hp choices (ckpt, n_est, lr, y_log, threshold) are made on val.
- **Phase A** (baseline, no fine-tune): sweep `n_est_grid` × ckpts (classifier: `default`, `default-2`; regressor: `default`, `real`); regression additionally tries `log1p(y)`. All evaluated on val.
- **Phase B** (fine-tune): per ckpt, fine-tune on (train', val) at each lr in `lr_grid` with `n_estimators_finetune={args.n_est_ft}` and val-based early stopping (best-on-val ckpt). If fine-tune cannot beat the initial val metric, the row is marked `no_improvement` and treated as the corresponding Phase A baseline.
- **Phase C** (final model): for each seed in [0, 1, 2], refit the val-winning config on the **full train (train' + val)** — Phase A wins → re-fit in-context with full train; Phase B wins → re-fine-tune on full train (no val, fixed `epochs=30`, `early_stopping=False`). Test predictions averaged across seeds.
- **Phase D** (binary only): tune classification threshold on the val_proba saved by Phase A/B for the winning config; apply to the Phase C test ensemble.
- Caveat: val is used for both fine-tune early stopping AND hp grid selection. With only ~12 candidate configs per task the over-selection risk is small.
- Per-task full sweep details: `per_task/<name>.json`.
- Raw aggregate: `all_metrics.json`.
