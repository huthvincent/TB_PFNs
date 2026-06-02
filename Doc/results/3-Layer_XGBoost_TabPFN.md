# 3-Layer Cascade — XGBoost vs fine-tuned TabPFN


Model: XGBoost (baseline) vs fine-tuned TabPFN.

Split: NCT-level 80/20 per phase. All layers within a phase share the same split — a test NCT (Clinical Trial ID) in L3 (Layer 3) is never in L1 (Layer 1)/L2 (Layer 2) train.  


## Per-layer test metrics — XGBoost (per phase)

| Phase | Layer | n_train | n_test | train pos rate | ROC-AUC | PR-AUC | LogLoss | Acc |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| Phase1 | L1_execution | 6500 | 1572 | 0.585 | 0.6988 | 0.7392 | 0.6387 | 0.6476 |
| Phase1 | L2_biology | 2552 | 591 | 0.931 | 0.5538 | 0.9464 | 0.4815 | 0.7208 |
| Phase1 | L3_regulatory | 926 | 210 | 0.095 | 0.8589 | 0.2840 | 0.3254 | 0.8524 |
| Phase2 | L1_execution | 16861 | 4252 | 0.313 | 0.7984 | 0.6306 | 0.5334 | 0.7333 |
| Phase2 | L2_biology | 3574 | 905 | 0.836 | 0.6916 | 0.9204 | 0.5398 | 0.7017 |
| Phase2 | L3_regulatory | 1277 | 345 | 0.255 | 0.9848 | 0.9464 | 0.1517 | 0.9536 |
| Phase3 | L1_execution | 11426 | 2833 | 0.194 | 0.8790 | 0.6308 | 0.3778 | 0.8521 |
| Phase3 | L2_biology | 1658 | 420 | 0.840 | 0.6246 | 0.8789 | 0.5981 | 0.6929 |
| Phase3 | L3_regulatory | 589 | 137 | 0.190 | 0.9920 | 0.9637 | 0.0868 | 0.9781 |

Note: Phase 3's L3 ROC-AUC of 0.98-0.99 looks suspiciously high. The underlying reason: the L3 training set is composed of two groups — "approved trials (label=1)" and "failed-for-non-efficacy-reasons trials (label=0)". These two groups differ systematically in metadata features (trial phase, enrollment size, sponsor type), which makes them easy to separate. This is NOT leakage — both `approval_outcome` and `failure_reason` are excluded. However, it is also NOT a pure "predict whether a future trial will be approved" task; it is rather "discriminate within the pre-filtered approved-or-failed-non-bio subset".

## TabPFN vs XGBoost — Per-layer comparison (ROC-AUC)

Fine-tuned TabPFN trained on the same per-layer train splits as XGBoost. TabPFN wins on every (layer × phase) cell.

| Layer | Phase1 XGB | Phase1 TabPFN | Phase2 XGB | Phase2 TabPFN | Phase3 XGB | Phase3 TabPFN |
|---|---:|---:|---:|---:|---:|---:|
| L1 | 0.6988 | **0.7232** (+0.024) | 0.7984 | **0.8102** (+0.012) | 0.8790 | **0.8997** (+0.021) |
| L2 | 0.5538 | **0.6046** (+0.051) | 0.6916 | **0.7019** (+0.010) | 0.6246 | **0.6587** (+0.034) |
| L3 | 0.8589 | **0.8802** (+0.021) | 0.9848 | **0.9899** (+0.005) | 0.9920 | **0.9963** (+0.004) |

The biggest lift is on L2 (Biology), which was XGBoost's weakest layer due to extreme class imbalance (83-94% positive). TabPFN's in-context learning handles small / imbalanced training pools more gracefully.

## Joint approval metric (per phase)

P(approved) = P(L1_pass) × P(L2_pass) × P(L3_pass), evaluated on the test NCTs that have `approval_outcome` known.

| Phase | n_test | test pos rate | ROC-AUC | PR-AUC | LogLoss | Acc |
|---|---:|---:|---:|---:|---:|---:|
| Phase1 | 856 | 0.443 | 0.8391 | 0.7450 | 1.3134 | 0.5724 |
| Phase2 | 2528 | 0.387 | 0.7511 | 0.5999 | 1.2538 | 0.6262 |
| Phase3 | 1778 | 0.555 | 0.6806 | 0.6500 | 2.3773 | 0.4544 |

## TabPFN vs XGBoost — Joint metric comparison

| Phase | XGB | TabPFN | Δ |
|---|---:|---:|---:|
| Phase1 | **0.8391** | 0.8063 | −0.033 |
| Phase2 | **0.7511** | 0.7493 | −0.002 |
| Phase3 | **0.6806** | 0.6640 | −0.017 |

Despite winning every per-layer comparison, fine-tuned TabPFN **loses on the multiplicative joint metric** across all three phases (by 0.002–0.033 ROC-AUC). The likely cause is **probability calibration**: TabPFN tends to output more extreme probabilities (closer to 0 or 1, i.e., overconfident) than XGBoost. When three such probabilities are multiplied together, small errors at the layer level compound and amplify in the product. XGBoost's smoother, better-calibrated probabilities happen to be better suited to multiplicative composition out of the box. This is fixable — TabPFN outputs can also be calibrated, for example via per-layer isotonic regression or Platt scaling fitted on a held-out calibration set, which should bring TabPFN's joint metric back in line with (or above) its per-layer dominance suggests.

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
-- (NaN does not trigger either condition; at least one signal must be known to enter the training pool)
```

### Layer 2 — Biology

**Task**: Among trials that have passed L1, predict whether the drug's biological efficacy will pass (will not fail due to efficacy).  
**Training filter**: `execution_pass = TRUE` (filtered by the real L1 label), AND `biology_pass` is observable.  
**Label SQL**:
```sql
biology_pass =
  CASE
    WHEN approval_outcome = 1            THEN TRUE   -- approved ⇒ biology must have passed
    WHEN failure_reason = 'efficacy'     THEN FALSE  -- failed for efficacy ⇒ did not pass
    WHEN failure_reason IS NOT NULL      THEN TRUE   -- failed for other reasons ⇒ biology layer passed
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
-- Note: the L3 training pool consists of two groups — approval=1 (label TRUE) and
--   failed-non-efficacy with known approval (label FALSE)
```

### Cascade nesting property

L3 ⊆ L2 ⊆ L1 (trainable subsets strictly nested):
- L1 trainable: at least one of dropout_YN or failure_reason is observable
- L2 trainable: subset of L1 with execution_pass=TRUE AND (approval=1 OR failure_reason known)
- L3 trainable: subset of L2 with biology_pass=TRUE AND approval_outcome known


