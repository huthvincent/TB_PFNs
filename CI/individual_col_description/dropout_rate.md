# dropout_rate

- **Group:** `outcome_safety`
- **Dtype:** float [0,1]
- **Description:** Observed patient-dropout rate.
- **Associated partners (from `association.md`):** 35
  - Direct **causes** (parents of this feature): **8**
  - Direct **effects** (children of this feature): **7**
  - Associated but **no direct** causal edge: **20**

This per-feature file enumerates only **associated** partners. All other columns in `DAG.json` were ruled independent in the Stage-1 association screen and do not appear here. See `association.md` for the screen.

---

## Direct causes (8)

### `sae_rate`

- **Association:** effect = 0.342 (abs_spearman), n_valid = 17,873
- **Mechanism:** `biological`
- **Provenance:** explicit

Participants with serious adverse events frequently withdraw from the trial (either by choice or by protocol mandate); SAEs are a causal driver of dropout.

### `mortality_rate`

- **Association:** effect = 0.275 (abs_spearman), n_valid = 17,873
- **Mechanism:** `definitional`
- **Provenance:** explicit

Deaths are by definition dropouts (the participant can no longer continue), so mortality contributes to dropout_rate.

### `duration_day`

- **Association:** effect = 0.252 (abs_spearman), n_valid = 16,162
- **Mechanism:** `operational`
- **Provenance:** explicit

Longer trials lose more participants to follow-up.

### `duration_year`

- **Association:** effect = 0.252 (abs_spearman), n_valid = 16,162
- **Mechanism:** `operational`
- **Provenance:** default_cross_tier

Longer / later trial timing (duration_year) accrues more events, raising the realised safety outcome (dropout_rate).

### `duration_month`

- **Association:** effect = 0.252 (abs_spearman), n_valid = 16,162
- **Mechanism:** `operational`
- **Provenance:** default_cross_tier

Longer / later trial timing (duration_month) accrues more events, raising the realised safety outcome (dropout_rate).

### `eligibility/healthy_volunteers`

- **Association:** effect = 0.203 (eta), n_valid = 38,268
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Downstream-design field (eligibility/healthy_volunteers) shifts the realised safety outcome (dropout_rate) through population biology or trial operations.

### `phase`

- **Association:** effect = 0.131 (eta), n_valid = 38,302
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Sponsor design decision (phase) that influences the realised safety outcome (dropout_rate) through biology, population, or operations.

### `eligibility/maximum_age`

- **Association:** effect = 0.110 (abs_spearman), n_valid = 18,312
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Downstream-design field (eligibility/maximum_age) shifts the realised safety outcome (dropout_rate) through population biology or trial operations.

---

## Direct effects (7)

### `dropout_YN`

- **Association:** effect = 0.715 (abs_spearman), n_valid = 38,302
- **Mechanism:** `deterministic`
- **Provenance:** explicit

dropout_YN is the thresholded version of dropout_rate.

### `execution_pass`

- **Association:** effect = 0.671 (abs_spearman), n_valid = 38,302
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Realised safety outcome (dropout_rate) feeds the trial-success label (execution_pass) directly (e.g., 'safety' failure category, regulatory rejection).

### `execution_fail`

- **Association:** effect = 0.671 (abs_spearman), n_valid = 38,302
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Realised safety outcome (dropout_rate) feeds the trial-success label (execution_fail) directly (e.g., 'safety' failure category, regulatory rejection).

### `approval_outcome`

- **Association:** effect = 0.143 (abs_spearman), n_valid = 14,131
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Realised safety outcome (dropout_rate) feeds the trial-success label (approval_outcome) directly (e.g., 'safety' failure category, regulatory rejection).

### `failure_reason`

- **Association:** effect = 0.111 (eta), n_valid = 6,299
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Realised safety outcome (dropout_rate) feeds the trial-success label (failure_reason) directly (e.g., 'safety' failure category, regulatory rejection).

### `biology_fail`

- **Association:** effect = 0.105 (abs_spearman), n_valid = 13,897
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Realised safety outcome (dropout_rate) feeds the trial-success label (biology_fail) directly (e.g., 'safety' failure category, regulatory rejection).

### `biology_pass`

- **Association:** effect = 0.105 (abs_spearman), n_valid = 13,897
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Realised safety outcome (dropout_rate) feeds the trial-success label (biology_pass) directly (e.g., 'safety' failure category, regulatory rejection).

---

## Associated but no direct causal edge (20)

### `sae_YN`

- **Association:** effect = 0.291 (abs_spearman), n_valid = 17,873
- **Provenance:** explicit

Mediated through sae_rate: sae_YN <- sae_rate -> dropout_rate.

### `location/facility/address/city`

- **Association:** effect = 0.268 (abs_spearman), n_valid = 38,302
- **Provenance:** demoted_confounded

`location/facility/address/city` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `dropout_rate`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `mortality_YN`

- **Association:** effect = 0.266 (abs_spearman), n_valid = 17,873
- **Provenance:** explicit

Mediated through mortality_rate: mortality_YN <- mortality_rate -> dropout_rate.

### `ipd_info_type-Informed Consent Form (ICF)`

- **Association:** effect = 0.178 (abs_spearman), n_valid = 2,105
- **Provenance:** demoted_confounded

`ipd_info_type-Informed Consent Form (ICF)` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `dropout_rate`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `study_design_info/intervention_model`

- **Association:** effect = 0.170 (eta), n_valid = 38,137
- **Provenance:** demoted_confounded

`study_design_info/intervention_model` is a sponsor / methodology design choice with no direct biological pathway to the realised safety rate `dropout_rate`; the association is confounded through `intervention/intervention_type` and `condition` (what is being studied), which carry the genuine safety edges. (R4: confounded design->safety.)

### `study_design_info/primary_purpose`

- **Association:** effect = 0.164 (eta), n_valid = 37,812
- **Provenance:** demoted_confounded

`study_design_info/primary_purpose` is a sponsor / methodology design choice with no direct biological pathway to the realised safety rate `dropout_rate`; the association is confounded through `intervention/intervention_type` and `condition` (what is being studied), which carry the genuine safety edges. (R4: confounded design->safety.)

### `study_design_info/masking`

- **Association:** effect = 0.156 (eta), n_valid = 38,218
- **Provenance:** demoted_confounded

`study_design_info/masking` is a sponsor / methodology design choice with no direct biological pathway to the realised safety rate `dropout_rate`; the association is confounded through `intervention/intervention_type` and `condition` (what is being studied), which carry the genuine safety edges. (R4: confounded design->safety.)

### `enrollment`

- **Association:** effect = 0.143 (abs_spearman), n_valid = 38,301
- **Provenance:** demoted_confounded

A rate is invariant to sample size in expectation; `enrollment -> dropout_rate` is a threshold-crossing artifact, not a causal effect of N on the safety rate. (R3: rate invariance. Genuine enrollment effects are kept for trial timing and the 'poor enrollment' execution-failure pathway.)

### `start_date`

- **Association:** effect = 0.131 (abs_spearman), n_valid = 16,162
- **Provenance:** demoted_confounded

`start_date` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `dropout_rate`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `study_design_info/allocation`

- **Association:** effect = 0.120 (eta), n_valid = 29,014
- **Provenance:** demoted_confounded

`study_design_info/allocation` is a sponsor / methodology design choice with no direct biological pathway to the realised safety rate `dropout_rate`; the association is confounded through `intervention/intervention_type` and `condition` (what is being studied), which carry the genuine safety edges. (R4: confounded design->safety.)

### `sponsors/lead_sponsor/agency_class`

- **Association:** effect = 0.115 (eta), n_valid = 38,302
- **Provenance:** demoted_confounded

`sponsors/lead_sponsor/agency_class` is a sponsor / methodology design choice with no direct biological pathway to the realised safety rate `dropout_rate`; the association is confounded through `intervention/intervention_type` and `condition` (what is being studied), which carry the genuine safety edges. (R4: confounded design->safety.)

### `patient_data/sharing_ipd`

- **Association:** effect = 0.102 (eta), n_valid = 12,952
- **Provenance:** demoted_confounded

`patient_data/sharing_ipd` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `dropout_rate`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `responsible_party/responsible_party_type`

- **Association:** effect = 0.094 (eta), n_valid = 36,674
- **Provenance:** demoted_confounded

`responsible_party/responsible_party_type` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `dropout_rate`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `oversight_info/is_fda_regulated_drug`

- **Association:** effect = 0.090 (eta), n_valid = 11,191
- **Provenance:** demoted_confounded

`oversight_info/is_fda_regulated_drug` is an oversight / regulatory flag that proxies for trial type and scale; its association with `dropout_rate` is confounded through `intervention/intervention_type`, `phase`, and trial scale. The genuine oversight mechanisms (FDA-regulation -> approval_outcome; DMC early-stopping -> sae_rate / mortality_rate) are retained as explicit edges. (R10: confounded design_oversight->outcome.)

### `condition_browse/mesh_term`

- **Association:** effect = 0.083 (abs_spearman), n_valid = 38,302
- **Provenance:** demoted_confounded

`condition_browse/mesh_term` is a deterministic re-encoding / tally of `condition`; its association with `dropout_rate` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `oversight_info/has_dmc`

- **Association:** effect = 0.078 (eta), n_valid = 32,996
- **Provenance:** demoted_confounded

`oversight_info/has_dmc` is an oversight / regulatory flag that proxies for trial type and scale; its association with `dropout_rate` is confounded through `intervention/intervention_type`, `phase`, and trial scale. The genuine oversight mechanisms (FDA-regulation -> approval_outcome; DMC early-stopping -> sae_rate / mortality_rate) are retained as explicit edges. (R10: confounded design_oversight->outcome.)

### `ipd_info_type-Statistical Analysis Plan (SAP)`

- **Association:** effect = 0.075 (abs_spearman), n_valid = 2,105
- **Provenance:** demoted_confounded

`ipd_info_type-Statistical Analysis Plan (SAP)` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `dropout_rate`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `Active Comparator Arm Number`

- **Association:** effect = 0.058 (abs_spearman), n_valid = 38,016
- **Provenance:** demoted_confounded

`Active Comparator Arm Number` is a deterministic re-encoding / tally of `study_design_info/intervention_model`; its association with `dropout_rate` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `has_expanded_access`

- **Association:** effect = 0.057 (eta), n_valid = 37,901
- **Provenance:** demoted_confounded

`has_expanded_access` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `dropout_rate`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `smiless`

- **Association:** effect = 0.051 (abs_spearman), n_valid = 38,302
- **Provenance:** demoted_confounded

`smiless` is a deterministic re-encoding / tally of `intervention/intervention_name`; its association with `dropout_rate` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)
