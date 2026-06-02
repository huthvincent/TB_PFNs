# TrialBench × TabPFN-2.5 — **Per-phase** Tier-1 results

Generated: 2026-05-10T17:05:14  
Device: NVIDIA H200 NVL  
Run config: n_est_grid=[4, 8, 16, 32], lr_grid=[1e-05, 2e-05, 5e-05], ft_epochs=30, n_est_ft=2, ens_seeds=[0, 1, 2]

**Per-phase isolation**: each row uses ONLY that phase's train CSV (80/20 → train'/val for hp selection, then refit best config on full phase-train) and ONLY that phase's test CSV. No cross-phase mixing.

`vanilla` = best Phase-A baseline (no fine-tune, val-selected ckpt + n_estimators). `Tier-1` = full pipeline test result. `Δ` = Tier-1 − vanilla, both measured on the same per-phase test set.

## Binary classification (per phase, primary metric = `roc_auc`)

### mortality-event-prediction

| Phase | n_train | n_test | ROC-AUC vanilla | ROC-AUC Tier-1 | Δ | PR-AUC | LogLoss | Acc (tuned) | best_threshold | Selected config |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Phase1 | 1595 | 419 | 0.9450 | **0.9333** | -0.0117 | 0.8436 | 0.2944 | 0.8711 | 0.2500 | `phase=A ckpt=default n_est=8` |
| Phase2 | 6516 | 1600 | 0.8315 | **0.8302** | -0.0013 | 0.7945 | 0.5076 | 0.7675 | 0.5400 | `phase=B ckpt=default-2 n_est=4 lr=5e-05` |
| Phase3 | 3895 | 945 | 0.8560 | **0.8243** | -0.0317 | 0.8316 | 0.5189 | 0.7344 | 0.5500 | `phase=B ckpt=default n_est=8 lr=2e-05` |
| Phase4 | 2362 | 584 | 0.8290 | **0.8334** | +0.0044 | 0.5631 | 0.3456 | 0.8630 | 0.3700 | `phase=A ckpt=default n_est=16` |

### patient-dropout-event-forecasting

| Phase | n_train | n_test | ROC-AUC vanilla | ROC-AUC Tier-1 | Δ | PR-AUC | LogLoss | Acc (tuned) | best_threshold | Selected config |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Phase1 | 3321 | 883 | 0.7380 | **0.7467** | +0.0087 | 0.8100 | 0.5860 | 0.6908 | 0.5400 | `phase=B ckpt=default-2 n_est=16 lr=5e-05` |
| Phase2 | 12608 | 3162 | 0.7855 | **0.7735** | -0.0120 | 0.9203 | 0.4524 | 0.7837 | 0.5200 | `phase=A ckpt=default n_est=8` |
| Phase3 | 9129 | 2332 | 0.8109 | **0.8555** | +0.0447 | 0.9832 | 0.2273 | 0.9134 | 0.4300 | `phase=B ckpt=default n_est=16 lr=5e-05` |
| Phase4 | 5503 | 1364 | 0.7626 | **0.7414** | -0.0212 | 0.8761 | 0.5260 | 0.7243 | 0.5700 | `phase=B ckpt=default n_est=8 lr=5e-05` |

### serious-adverse-event-forecasting

| Phase | n_train | n_test | ROC-AUC vanilla | ROC-AUC Tier-1 | Δ | PR-AUC | LogLoss | Acc (tuned) | best_threshold | Selected config |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Phase1 | 1595 | 419 | 0.8727 | **0.9123** | +0.0396 | 0.8989 | 0.3696 | 0.8401 | 0.4200 | `phase=A ckpt=default-2 n_est=16` |
| Phase2 | 6516 | 1600 | 0.8156 | **0.8208** | +0.0052 | 0.9270 | 0.4320 | 0.8006 | 0.5300 | `phase=B ckpt=default n_est=32 lr=5e-05` |
| Phase3 | 3895 | 945 | 0.8992 | **0.8977** | -0.0014 | 0.9788 | 0.2703 | 0.8836 | 0.5500 | `phase=B ckpt=default-2 n_est=16 lr=2e-05` |
| Phase4 | 2362 | 584 | 0.8537 | **0.7987** | -0.0551 | 0.7366 | 0.5252 | 0.7295 | 0.5300 | `phase=B ckpt=default n_est=4 lr=2e-05` |

### trial-approval-forecasting

| Phase | n_train | n_test | ROC-AUC vanilla | ROC-AUC Tier-1 | Δ | PR-AUC | LogLoss | Acc (tuned) | best_threshold | Selected config |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Phase1 | 3586 | 896 | 0.8504 | **0.8266** | -0.0238 | 0.7455 | 0.4946 | 0.7455 | 0.4900 | `phase=B ckpt=default-2 n_est=32 lr=5e-05` |
| Phase2 | 9980 | 2514 | 0.8263 | **0.8201** | -0.0062 | 0.6892 | 0.4797 | 0.7363 | 0.4700 | `phase=A ckpt=default-2 n_est=16` |
| Phase3 | 7248 | 1913 | 0.8142 | **0.8125** | -0.0017 | 0.8250 | 0.5178 | 0.7360 | 0.5500 | `phase=B ckpt=default-2 n_est=8 lr=5e-05` |
| Phase4 | 3654 | 892 | 0.8675 | **0.8536** | -0.0139 | 0.7649 | 0.4511 | 0.7702 | 0.4800 | `phase=B ckpt=default n_est=8 lr=5e-05` |

## Multiclass classification (per phase, primary metric = `accuracy`)

### trial-failure-reason-identification

| Phase | n_classes | n_train | n_test | Acc vanilla | Acc Tier-1 | Δ | F1-macro | LogLoss | Selected config |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Phase1 | 4 | 3474 | 842 | 0.6014 | **0.6283** | +0.0268 | 0.2194 | 0.9701 | `phase=A ckpt=default n_est=8` |
| Phase2 | 4 | 7056 | 1780 | 0.4554 | **0.4567** | +0.0014 | 0.2672 | 1.1590 | `phase=A ckpt=default-2 n_est=8` |
| Phase3 | 4 | 3341 | 815 | 0.4798 | **0.4724** | -0.0074 | 0.2461 | 1.1534 | `phase=A ckpt=default n_est=32` |
| Phase4 | 4 | 2778 | 683 | 0.5396 | **0.4773** | -0.0623 | 0.2457 | 0.9658 | `phase=A ckpt=default n_est=16` |

## Regression (per phase, primary metric = `r2`)

### trial-duration-forecasting

| Phase | n_train | n_test | R² vanilla | R² Tier-1 | Δ | MAE | RMSE | Selected config |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| Phase1 | 10424 | 3016 | 0.4905 | **0.4466** | -0.0439 | 281.2527 | 450.4949 | `phase=A ckpt=default n_est=4 log=0` |
| Phase2 | 10623 | 2590 | 0.2289 | **0.1853** | -0.0436 | 467.3733 | 631.0253 | `phase=B ckpt=real n_est=8 lr=1e-05 log=0` |
| Phase3 | 7406 | 1698 | 0.1916 | **0.0936** | -0.0980 | 489.8036 | 658.8008 | `phase=B ckpt=default n_est=4 lr=1e-05 log=0` |
| Phase4 | 5735 | 1363 | 0.0554 | **0.0501** | -0.0053 | 456.5457 | 620.6377 | `phase=B ckpt=default n_est=8 lr=5e-05 log=0` |

## Not applicable

| Task | Reason |
|---|---|
| eligibility-criteria-design | Free-text generation task; not a tabular prediction problem. |
| drug-dose-prediction | Inputs are only SMILES strings and MeSH terms; needs molecular/ontology encoders (TrialBench uses MPNN + mesh_term2feature). No tabular features. |

## Methodology notes

- For each (subtask, phase): load only that phase's train/test CSVs. Split phase-train 80/20 → train'/val (stratified for classification). Run the same pipeline as `tier1_tune.py`: Phase A (baseline sweep), Phase B (fine-tune sweep with val early-stop), pick winner on val, Phase C (refit best config on full phase-train, k-seed ensemble), Phase D (binary: tune threshold on val_proba).
- `vanilla` column = the best Phase-A baseline (val-selected ckpt × n_estimators, no fine-tune). It already includes the 'just bump n_estimators + try both ckpts' improvements.
- `Tier-1` column = full pipeline (vanilla + fine-tune + 3-seed ensemble + threshold tuning where applicable).
- All hp/ckpt/threshold choices made on val. Test evaluated once.
- Per-(subtask, phase) full sweep details: `per_task/<subtask>__<phase>.json`.
