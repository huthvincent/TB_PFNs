# Cascade Data Exploration Report

Generated: 2026-05-10T18:03:13

Per-phase analysis of the 6 TrialBench subtasks for the planned Execution → Biology → Regulatory cascade. All counts use train ∪ test (we will re-split later by completion_date).

## Phase1

**NCT counts per subtask**

| Subtask | n_NCT | n_X_cols | Coverage by trial-duration |
|---|---:|---:|---:|
| patient-dropout-event-forecasting | 4204 | 60 | 2063/4204 (49.1%) |
| trial-duration-forecasting | 13440 | 50 | 13440/13440 (100.0%) |
| serious-adverse-event-forecasting | 2014 | 60 | 1702/2014 (84.5%) |
| mortality-event-prediction | 2014 | 60 | 1702/2014 (84.5%) |
| trial-failure-reason-identification | 4316 | 44 | 1659/4316 (38.4%) |
| trial-approval-forecasting | 4482 | 57 | 1549/4482 (34.6%) |

**Per-cascade-layer label pools** (union of source subtasks):  
- L1 (dropout ∪ failure_reason): 8072, with completion_date: 3446  
- L2 (sae ∪ mortality ∪ failure_reason): 6048, with completion_date: 3118  
- L3 (approval): 4482, with completion_date: 1549  

**Full 6-way intersection**: 138 trials  
**5-way intersection** (excl. failure_reason, which only exists for failed trials): 253 trials  
**Joined wide table**: [18172, 18]  

**Label coverage in joined table**

| Label | n_non_null |
|---|---:|
| `dropout_YN` | 4204 |
| `dropout_rate` | 4204 |
| `start_date` | 13440 |
| `completion_date` | 13440 |
| `duration_day` | 13440 |
| `duration_month` | 13440 |
| `duration_year` | 13440 |
| `sae_YN` | 2014 |
| `sae_rate` | 2014 |
| `mortality_YN` | 2014 |
| `mortality_rate` | 2014 |
| `failure_reason` | 3238 |
| `approval_outcome` | 4482 |

**Per-layer trainable counts and class balance**

| Layer | n_trainable | class balance | note |
|---|---:|---|---|
| L1_execution_primary | 6994 | True=3633, False=3361 |  |
| L2_biology_primary | 1961 | True=1749, False=212 | L2 primary label = (failure_reason == 'efficacy'). Only failed trials have failure_reason → trainable subset is FAILED trials whose failure was NOT execution-related. |
| L3_regulatory_primary_strict | 1032 | False=1032 | Strict cascade: requires both L1 and L2 labels known AND both passing. Since L2 known implies failure_reason known (only for failed trials), this filter is effectively the subset of FAILED-but-not-for-{execution,efficacy} trials. It excludes ALL approved trials. |
| L3_regulatory_primary_relaxed | 2801 | True=1647, False=1154 | Relaxed cascade: trials with approval known AND not flagged as execution_fail / efficacy_fail (NaN treated as not-failed). Includes approved trials and unknown-status trials. Sample size is realistic but the gate is weaker. |

**Auxiliary-label pool sizes** (each gets its own model under option B)

| Aux label | n |
|---|---:|
| `aux_sae_YN` | 2014 |
| `aux_sae_rate` | 2014 |
| `aux_mortality_YN` | 2014 |
| `aux_mortality_rate` | 2014 |
| `aux_safety_failure` | 422 |
| `aux_efficacy_failure_known` | 3238 |
| `aux_duration_day` | 13440 |

**completion_date stats (for time split)**

```json
{
  "n_available": 13440,
  "min": "1992-07-01 00:00:00",
  "max": "2024-02-14 00:00:00",
  "median": "2019-09-11 00:00:00"
}
```

**start_date in X (per subtask)**

```json
{
  "patient-dropout-event-forecasting": false,
  "trial-duration-forecasting": false,
  "serious-adverse-event-forecasting": false,
  "mortality-event-prediction": false,
  "trial-failure-reason-identification": false,
  "trial-approval-forecasting": false
}
```

## Phase2

**NCT counts per subtask**

| Subtask | n_NCT | n_X_cols | Coverage by trial-duration |
|---|---:|---:|---:|
| patient-dropout-event-forecasting | 15770 | 60 | 6833/15770 (43.3%) |
| trial-duration-forecasting | 13213 | 50 | 13213/13213 (100.0%) |
| serious-adverse-event-forecasting | 8116 | 60 | 5800/8116 (71.5%) |
| mortality-event-prediction | 8116 | 60 | 5800/8116 (71.5%) |
| trial-failure-reason-identification | 8836 | 44 | 2949/8836 (33.4%) |
| trial-approval-forecasting | 12494 | 57 | 3861/12494 (30.9%) |

**Per-cascade-layer label pools** (union of source subtasks):  
- L1 (dropout ∪ failure_reason): 21113, with completion_date: 8138  
- L2 (sae ∪ mortality ∪ failure_reason): 15193, with completion_date: 7365  
- L3 (approval): 12494, with completion_date: 3861  

**Full 6-way intersection**: 937 trials  
**5-way intersection** (excl. failure_reason, which only exists for failed trials): 1950 trials  
**Joined wide table**: [27103, 18]  

**Label coverage in joined table**

| Label | n_non_null |
|---|---:|
| `dropout_YN` | 15770 |
| `dropout_rate` | 15770 |
| `start_date` | 13213 |
| `completion_date` | 13213 |
| `duration_day` | 13213 |
| `duration_month` | 13213 |
| `duration_year` | 13213 |
| `sae_YN` | 8116 |
| `sae_rate` | 8116 |
| `mortality_YN` | 8116 |
| `mortality_rate` | 8116 |
| `failure_reason` | 7380 |
| `approval_outcome` | 12494 |

**Per-layer trainable counts and class balance**

| Layer | n_trainable | class balance | note |
|---|---:|---|---|
| L1_execution_primary | 19657 | False=14501, True=5156 |  |
| L2_biology_primary | 2609 | True=1897, False=712 | L2 primary label = (failure_reason == 'efficacy'). Only failed trials have failure_reason → trainable subset is FAILED trials whose failure was NOT execution-related. |
| L3_regulatory_primary_strict | 1208 | False=1208 | Strict cascade: requires both L1 and L2 labels known AND both passing. Since L2 known implies failure_reason known (only for failed trials), this filter is effectively the subset of FAILED-but-not-for-{execution,efficacy} trials. It excludes ALL approved trials. |
| L3_regulatory_primary_relaxed | 4580 | True=2518, False=2062 | Relaxed cascade: trials with approval known AND not flagged as execution_fail / efficacy_fail (NaN treated as not-failed). Includes approved trials and unknown-status trials. Sample size is realistic but the gate is weaker. |

**Auxiliary-label pool sizes** (each gets its own model under option B)

| Aux label | n |
|---|---:|
| `aux_sae_YN` | 8116 |
| `aux_sae_rate` | 8116 |
| `aux_mortality_YN` | 8116 |
| `aux_mortality_rate` | 8116 |
| `aux_safety_failure` | 559 |
| `aux_efficacy_failure_known` | 7380 |
| `aux_duration_day` | 13213 |

**completion_date stats (for time split)**

```json
{
  "n_available": 13213,
  "min": "1991-07-01 00:00:00",
  "max": "2024-02-09 00:00:00",
  "median": "2019-06-26 00:00:00"
}
```

**start_date in X (per subtask)**

```json
{
  "patient-dropout-event-forecasting": false,
  "trial-duration-forecasting": false,
  "serious-adverse-event-forecasting": false,
  "mortality-event-prediction": false,
  "trial-failure-reason-identification": false,
  "trial-approval-forecasting": false
}
```

## Phase3

**NCT counts per subtask**

| Subtask | n_NCT | n_X_cols | Coverage by trial-duration |
|---|---:|---:|---:|
| patient-dropout-event-forecasting | 11461 | 60 | 4867/11461 (42.5%) |
| trial-duration-forecasting | 9104 | 50 | 9104/9104 (100.0%) |
| serious-adverse-event-forecasting | 4840 | 60 | 3752/4840 (77.5%) |
| mortality-event-prediction | 4840 | 60 | 3752/4840 (77.5%) |
| trial-failure-reason-identification | 4156 | 44 | 1314/4156 (31.6%) |
| trial-approval-forecasting | 9161 | 57 | 2744/9161 (30.0%) |

**Per-cascade-layer label pools** (union of source subtasks):  
- L1 (dropout ∪ failure_reason): 14259, with completion_date: 5512  
- L2 (sae ∪ mortality ∪ failure_reason): 8347, with completion_date: 4519  
- L3 (approval): 9161, with completion_date: 2744  

**Full 6-way intersection**: 354 trials  
**5-way intersection** (excl. failure_reason, which only exists for failed trials): 1352 trials  
**Joined wide table**: [18847, 18]  

**Label coverage in joined table**

| Label | n_non_null |
|---|---:|
| `dropout_YN` | 11461 |
| `dropout_rate` | 11461 |
| `start_date` | 9104 |
| `completion_date` | 9104 |
| `duration_day` | 9104 |
| `duration_month` | 9104 |
| `duration_year` | 9104 |
| `sae_YN` | 4840 |
| `sae_rate` | 4840 |
| `mortality_YN` | 4840 |
| `mortality_rate` | 4840 |
| `failure_reason` | 3417 |
| `approval_outcome` | 9161 |

**Per-layer trainable counts and class balance**

| Layer | n_trainable | class balance | note |
|---|---:|---|---|
| L1_execution_primary | 13520 | False=11505, True=2015 |  |
| L2_biology_primary | 1193 | True=856, False=337 | L2 primary label = (failure_reason == 'efficacy'). Only failed trials have failure_reason → trainable subset is FAILED trials whose failure was NOT execution-related. |
| L3_regulatory_primary_strict | 580 | False=580 | Strict cascade: requires both L1 and L2 labels known AND both passing. Since L2 known implies failure_reason known (only for failed trials), this filter is effectively the subset of FAILED-but-not-for-{execution,efficacy} trials. It excludes ALL approved trials. |
| L3_regulatory_primary_relaxed | 2762 | True=1664, False=1098 | Relaxed cascade: trials with approval known AND not flagged as execution_fail / efficacy_fail (NaN treated as not-failed). Includes approved trials and unknown-status trials. Sample size is realistic but the gate is weaker. |

**Auxiliary-label pool sizes** (each gets its own model under option B)

| Aux label | n |
|---|---:|
| `aux_sae_YN` | 4840 |
| `aux_sae_rate` | 4840 |
| `aux_mortality_YN` | 4840 |
| `aux_mortality_rate` | 4840 |
| `aux_safety_failure` | 284 |
| `aux_efficacy_failure_known` | 3417 |
| `aux_duration_day` | 9104 |

**completion_date stats (for time split)**

```json
{
  "n_available": 9104,
  "min": "1992-03-27 00:00:00",
  "max": "2024-02-06 00:00:00",
  "median": "2019-01-29 00:00:00"
}
```

**start_date in X (per subtask)**

```json
{
  "patient-dropout-event-forecasting": false,
  "trial-duration-forecasting": false,
  "serious-adverse-event-forecasting": false,
  "mortality-event-prediction": false,
  "trial-failure-reason-identification": false,
  "trial-approval-forecasting": false
}
```

## Phase4

**NCT counts per subtask**

| Subtask | n_NCT | n_X_cols | Coverage by trial-duration |
|---|---:|---:|---:|
| patient-dropout-event-forecasting | 6867 | 60 | 2399/6867 (34.9%) |
| trial-duration-forecasting | 7098 | 50 | 7098/7098 (100.0%) |
| serious-adverse-event-forecasting | 2946 | 60 | 2024/2946 (68.7%) |
| mortality-event-prediction | 2946 | 60 | 2024/2946 (68.7%) |
| trial-failure-reason-identification | 3461 | 44 | 982/3461 (28.4%) |
| trial-approval-forecasting | 4546 | 57 | 1109/4546 (24.4%) |

**Per-cascade-layer label pools** (union of source subtasks):  
- L1 (dropout ∪ failure_reason): 9328, with completion_date: 2966  
- L2 (sae ∪ mortality ∪ failure_reason): 5898, with completion_date: 2650  
- L3 (approval): 4546, with completion_date: 1109  

**Full 6-way intersection**: 206 trials  
**5-way intersection** (excl. failure_reason, which only exists for failed trials): 386 trials  
**Joined wide table**: [13674, 18]  

**Label coverage in joined table**

| Label | n_non_null |
|---|---:|
| `dropout_YN` | 6867 |
| `dropout_rate` | 6867 |
| `start_date` | 7098 |
| `completion_date` | 7098 |
| `duration_day` | 7098 |
| `duration_month` | 7098 |
| `duration_year` | 7098 |
| `sae_YN` | 2946 |
| `sae_rate` | 2946 |
| `mortality_YN` | 2946 |
| `mortality_rate` | 2946 |
| `failure_reason` | 2744 |
| `approval_outcome` | 4546 |

**Per-layer trainable counts and class balance**

| Layer | n_trainable | class balance | note |
|---|---:|---|---|
| L1_execution_primary | 8611 | False=6280, True=2331 |  |
| L2_biology_primary | 809 | True=717, False=92 | L2 primary label = (failure_reason == 'efficacy'). Only failed trials have failure_reason → trainable subset is FAILED trials whose failure was NOT execution-related. |
| L3_regulatory_primary_strict | 437 | False=437 | Strict cascade: requires both L1 and L2 labels known AND both passing. Since L2 known implies failure_reason known (only for failed trials), this filter is effectively the subset of FAILED-but-not-for-{execution,efficacy} trials. It excludes ALL approved trials. |
| L3_regulatory_primary_relaxed | 1685 | True=1014, False=671 | Relaxed cascade: trials with approval known AND not flagged as execution_fail / efficacy_fail (NaN treated as not-failed). Includes approved trials and unknown-status trials. Sample size is realistic but the gate is weaker. |

**Auxiliary-label pool sizes** (each gets its own model under option B)

| Aux label | n |
|---|---:|
| `aux_sae_YN` | 2946 |
| `aux_sae_rate` | 2946 |
| `aux_mortality_YN` | 2946 |
| `aux_mortality_rate` | 2946 |
| `aux_safety_failure` | 119 |
| `aux_efficacy_failure_known` | 2744 |
| `aux_duration_day` | 7098 |

**completion_date stats (for time split)**

```json
{
  "n_available": 7098,
  "min": "1997-05-01 00:00:00",
  "max": "2024-02-07 00:00:00",
  "median": "2019-07-02 00:00:00"
}
```

**start_date in X (per subtask)**

```json
{
  "patient-dropout-event-forecasting": false,
  "trial-duration-forecasting": false,
  "serious-adverse-event-forecasting": false,
  "mortality-event-prediction": false,
  "trial-failure-reason-identification": false,
  "trial-approval-forecasting": false
}
```
