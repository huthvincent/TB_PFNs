# 3-Layer Cascade × fine-tuned TabPFN — baseline



Model: fine-tuned TabPFN (FinetunedTabPFNClassifier on `tabpfn-v2.5-classifier-v2.5_default.ckpt`, epochs=30, lr=2e-05, n_estimators=4 (shared across fine-tune/val/inference), no early stopping).  

Split: NCT-level 80/20 per phase (seed=42). All layers within a phase share the same split — a test NCT in L3 is never in L1/L2 train.  
Cascade filter uses **real upstream labels** (not predictions) — avoids contaminating downstream layers with upstream-model errors.

## Per-layer test metrics (per phase)

| Phase | Layer | n_train | n_test | train pos rate | ROC-AUC | PR-AUC | LogLoss | Acc |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| Phase1 | L1_execution | 6500 | 1572 | 0.585 | 0.7232 | 0.7693 | 0.6030 | 0.6743 |
| Phase1 | L2_biology | 2552 | 591 | 0.931 | 0.6046 | 0.9528 | 0.2282 | 0.9374 |
| Phase1 | L3_regulatory | 926 | 210 | 0.095 | 0.8802 | 0.3302 | 0.1876 | 0.9095 |
| Phase2 | L1_execution | 16861 | 4252 | 0.313 | 0.8102 | 0.6462 | 0.4804 | 0.7742 |
| Phase2 | L2_biology | 3574 | 905 | 0.836 | 0.7019 | 0.9210 | 0.3628 | 0.8641 |
| Phase2 | L3_regulatory | 1277 | 345 | 0.255 | 0.9899 | 0.9643 | 0.1052 | 0.9507 |
| Phase3 | L1_execution | 11426 | 2833 | 0.194 | 0.8997 | 0.6988 | 0.2961 | 0.8782 |
| Phase3 | L2_biology | 1658 | 420 | 0.840 | 0.6587 | 0.9006 | 0.4422 | 0.8286 |
| Phase3 | L3_regulatory | 589 | 137 | 0.190 | 0.9963 | 0.9875 | 0.0663 | 0.9854 |

Note: when L3 reports very high ROC-AUC, recall (per `cascade_xgboost/cascade_results.md`) that L3's training pool consists of two systematically different groups — "approved trials (label=1)" and "failed-for-non-efficacy-reasons trials (label=0)". These differ in metadata features (trial phase, enrollment size, sponsor type) and are therefore easy to separate. This is NOT leakage (both `approval_outcome` and `failure_reason` are excluded via `LABEL_DROP`); rather, it is a discrimination problem within a pre-filtered subset, not a pure "predict whether a future trial will be approved" task.

## Joint approval metric (per phase)

P(approved) = P(L1_pass) × P(L2_pass) × P(L3_pass), evaluated on the test NCTs that have `approval_outcome` known.

| Phase | n_test | test pos rate | ROC-AUC | PR-AUC | LogLoss | Acc |
|---|---:|---:|---:|---:|---:|---:|
| Phase1 | 856 | 0.443 | 0.8063 | 0.6930 | 1.1112 | 0.5584 |
| Phase2 | 2528 | 0.387 | 0.7493 | 0.5997 | 1.2660 | 0.6131 |
| Phase3 | 1778 | 0.555 | 0.6640 | 0.6308 | 2.5280 | 0.4483 |

## Layer definitions

Cascade is **strictly nested**: every L3-trainable trial is in L2's pool, every L2-trainable trial is in L1's pool. Cascade filters use **real upstream labels**, not predictions.

### Layer 1 — Execution

**Task**: Using trial registration-time metadata features, predict whether the trial will fail at the execution layer (high dropout or unable to enroll).  
**Training filter**: No upstream filter; samples only need to have an L1 label signal observable.  
**Label SQL**:
```sql
execution_fail = (dropout_YN = 1) OR (failure_reason = 'poor enrollment')
execution_pass = NOT execution_fail
-- observable when: dropout_YN IS NOT NULL OR failure_reason IS NOT NULL
-- (NaN does not trigger either condition; at least one signal must be known
--  to enter the training pool)
```

### Layer 2 — Biology

**Task**: Among trials that have passed L1, predict whether the drug's biological efficacy will pass (will not fail due to efficacy).  
**Training filter**: `execution_pass = TRUE` (filtered by the real L1 label), AND `biology_pass` is observable.  
**Label SQL**:
```sql
biology_pass =
  CASE
    WHEN approval_outcome = 1            THEN TRUE   -- approved => biology must have passed
    WHEN failure_reason = 'efficacy'     THEN FALSE  -- failed for efficacy => did not pass
    WHEN failure_reason IS NOT NULL      THEN TRUE   -- failed for other reasons => biology passed
    ELSE NULL
  END
-- observable when: approval_outcome = 1 OR failure_reason IS NOT NULL
```

### Layer 3 — Regulatory

**Task**: Among trials that have passed both L1 and L2, predict whether the trial will be approved by regulators.  
**Training filter**: `execution_pass = TRUE` AND `biology_pass = TRUE` (double real-label filter), AND `approval_outcome` is known.  
**Label SQL**:
```sql
regulatory_pass = (approval_outcome = 1)
-- observable when: approval_outcome IS NOT NULL
-- Note: the L3 training pool consists of two groups — approval=1 (label TRUE)
--   and failed-non-efficacy with known approval (label FALSE)
```

### Cascade nesting property

L3 ⊆ L2 ⊆ L1 (trainable subsets strictly nested):
- L1 trainable: at least one of dropout_YN or failure_reason is observable
- L2 trainable: subset of L1 with execution_pass=TRUE AND (approval=1 OR failure_reason known)
- L3 trainable: subset of L2 with biology_pass=TRUE AND approval_outcome known
