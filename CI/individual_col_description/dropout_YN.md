# dropout_YN

- **Group:** `outcome_safety`
- **Dtype:** float (0/1)
- **Description:** Binary indicator: above-threshold dropout rate occurred.
- **Associated partners (from `association.md`):** 41
  - Direct **causes** (parents of this feature): **10**
  - Direct **effects** (children of this feature): **4**
  - Associated but **no direct** causal edge: **27**

This per-feature file enumerates only **associated** partners. All other columns in `DAG.json` were ruled independent in the Stage-1 association screen and do not appear here. See `association.md` for the screen.

---

## Direct causes (10)

### `dropout_rate`

- **Association:** effect = 0.715 (abs_spearman), n_valid = 38,302
- **Mechanism:** `deterministic`
- **Provenance:** explicit

dropout_YN is the thresholded version of dropout_rate.

### `phase`

- **Association:** effect = 0.252 (eta), n_valid = 38,302
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Sponsor design decision (phase) that influences the realised safety outcome (dropout_YN) through biology, population, or operations.

### `eligibility/healthy_volunteers`

- **Association:** effect = 0.166 (eta), n_valid = 38,268
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Downstream-design field (eligibility/healthy_volunteers) shifts the realised safety outcome (dropout_YN) through population biology or trial operations.

### `duration_year`

- **Association:** effect = 0.131 (abs_spearman), n_valid = 16,162
- **Mechanism:** `operational`
- **Provenance:** default_cross_tier

Longer / later trial timing (duration_year) accrues more events, raising the realised safety outcome (dropout_YN).

### `duration_day`

- **Association:** effect = 0.131 (abs_spearman), n_valid = 16,162
- **Mechanism:** `operational`
- **Provenance:** default_cross_tier

Longer / later trial timing (duration_day) accrues more events, raising the realised safety outcome (dropout_YN).

### `duration_month`

- **Association:** effect = 0.131 (abs_spearman), n_valid = 16,162
- **Mechanism:** `operational`
- **Provenance:** default_cross_tier

Longer / later trial timing (duration_month) accrues more events, raising the realised safety outcome (dropout_YN).

### `eligibility/gender`

- **Association:** effect = 0.062 (eta), n_valid = 38,302
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Downstream-design field (eligibility/gender) shifts the realised safety outcome (dropout_YN) through population biology or trial operations.

### `intervention/intervention_name`

- **Association:** effect = 0.062 (abs_spearman), n_valid = 38,302
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Sponsor design decision (intervention/intervention_name) that influences the realised safety outcome (dropout_YN) through biology, population, or operations.

### `completion_date`

- **Association:** effect = 0.053 (abs_spearman), n_valid = 16,162
- **Mechanism:** `operational`
- **Provenance:** default_cross_tier

Longer / later trial timing (completion_date) accrues more events, raising the realised safety outcome (dropout_YN).

### `eligibility/maximum_age`

- **Association:** effect = 0.053 (abs_spearman), n_valid = 18,312
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Downstream-design field (eligibility/maximum_age) shifts the realised safety outcome (dropout_YN) through population biology or trial operations.

---

## Direct effects (4)

### `execution_fail`

- **Association:** effect = 0.940 (abs_spearman), n_valid = 38,302
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Realised safety outcome (dropout_YN) feeds the trial-success label (execution_fail) directly (e.g., 'safety' failure category, regulatory rejection).

### `execution_pass`

- **Association:** effect = 0.940 (abs_spearman), n_valid = 38,302
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Realised safety outcome (dropout_YN) feeds the trial-success label (execution_pass) directly (e.g., 'safety' failure category, regulatory rejection).

### `approval_outcome`

- **Association:** effect = 0.154 (abs_spearman), n_valid = 14,131
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Realised safety outcome (dropout_YN) feeds the trial-success label (approval_outcome) directly (e.g., 'safety' failure category, regulatory rejection).

### `failure_reason`

- **Association:** effect = 0.127 (eta), n_valid = 6,299
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Realised safety outcome (dropout_YN) feeds the trial-success label (failure_reason) directly (e.g., 'safety' failure category, regulatory rejection).

---

## Associated but no direct causal edge (27)

### `enrollment`

- **Association:** effect = 0.364 (abs_spearman), n_valid = 38,301
- **Provenance:** demoted_confounded

A rate is invariant to sample size in expectation; `enrollment -> dropout_YN` is a threshold-crossing artifact, not a causal effect of N on the safety rate. (R3: rate invariance. Genuine enrollment effects are kept for trial timing and the 'poor enrollment' execution-failure pathway.)

### `sae_YN`

- **Association:** effect = 0.290 (abs_spearman), n_valid = 17,873
- **Provenance:** explicit

Common cause via sae_rate -> dropout_rate -> dropout_YN.

### `location/facility/address/city`

- **Association:** effect = 0.289 (abs_spearman), n_valid = 38,302
- **Provenance:** demoted_confounded

`location/facility/address/city` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `dropout_YN`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `study_design_info/intervention_model`

- **Association:** effect = 0.240 (eta), n_valid = 38,137
- **Provenance:** demoted_confounded

`study_design_info/intervention_model` is a sponsor / methodology design choice with no direct biological pathway to the realised safety rate `dropout_YN`; the association is confounded through `intervention/intervention_type` and `condition` (what is being studied), which carry the genuine safety edges. (R4: confounded design->safety.)

### `sponsors/lead_sponsor/agency_class`

- **Association:** effect = 0.213 (eta), n_valid = 38,302
- **Provenance:** demoted_confounded

`sponsors/lead_sponsor/agency_class` is a sponsor / methodology design choice with no direct biological pathway to the realised safety rate `dropout_YN`; the association is confounded through `intervention/intervention_type` and `condition` (what is being studied), which carry the genuine safety edges. (R4: confounded design->safety.)

### `sae_rate`

- **Association:** effect = 0.191 (abs_spearman), n_valid = 17,873
- **Provenance:** explicit

Mediated through dropout_rate.

### `patient_data/sharing_ipd`

- **Association:** effect = 0.177 (eta), n_valid = 12,952
- **Provenance:** demoted_confounded

`patient_data/sharing_ipd` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `dropout_YN`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `study_design_info/primary_purpose`

- **Association:** effect = 0.167 (eta), n_valid = 37,812
- **Provenance:** demoted_confounded

`study_design_info/primary_purpose` is a sponsor / methodology design choice with no direct biological pathway to the realised safety rate `dropout_YN`; the association is confounded through `intervention/intervention_type` and `condition` (what is being studied), which carry the genuine safety edges. (R4: confounded design->safety.)

### `ipd_info_type-Informed Consent Form (ICF)`

- **Association:** effect = 0.156 (abs_spearman), n_valid = 2,105
- **Provenance:** demoted_confounded

`ipd_info_type-Informed Consent Form (ICF)` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `dropout_YN`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `study_design_info/masking`

- **Association:** effect = 0.151 (eta), n_valid = 38,218
- **Provenance:** demoted_confounded

`study_design_info/masking` is a sponsor / methodology design choice with no direct biological pathway to the realised safety rate `dropout_YN`; the association is confounded through `intervention/intervention_type` and `condition` (what is being studied), which carry the genuine safety edges. (R4: confounded design->safety.)

### `mortality_YN`

- **Association:** effect = 0.150 (abs_spearman), n_valid = 17,873
- **Provenance:** explicit

Mediated chain through rates.

### `responsible_party/responsible_party_type`

- **Association:** effect = 0.145 (eta), n_valid = 36,674
- **Provenance:** demoted_confounded

`responsible_party/responsible_party_type` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `dropout_YN`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `MaskingType-Investigator`

- **Association:** effect = 0.137 (abs_spearman), n_valid = 38,218
- **Provenance:** demoted_confounded

`MaskingType-Investigator` is a deterministic re-encoding / tally of `study_design_info/masking`; its association with `dropout_YN` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `study_design_info/masking_num`

- **Association:** effect = 0.129 (abs_spearman), n_valid = 38,218
- **Provenance:** demoted_confounded

`study_design_info/masking_num` is a deterministic re-encoding / tally of `study_design_info/masking`; its association with `dropout_YN` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `MaskingType-Participant`

- **Association:** effect = 0.121 (abs_spearman), n_valid = 38,218
- **Provenance:** demoted_confounded

`MaskingType-Participant` is a deterministic re-encoding / tally of `study_design_info/masking`; its association with `dropout_YN` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `Placebo Comparator Arm Number`

- **Association:** effect = 0.114 (abs_spearman), n_valid = 38,016
- **Provenance:** demoted_confounded

`Placebo Comparator Arm Number` is a deterministic re-encoding / tally of `study_design_info/intervention_model`; its association with `dropout_YN` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `mortality_rate`

- **Association:** effect = 0.111 (abs_spearman), n_valid = 17,873
- **Provenance:** explicit

Mediated through dropout_rate.

### `start_date`

- **Association:** effect = 0.099 (abs_spearman), n_valid = 16,162
- **Provenance:** demoted_confounded

`start_date` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `dropout_YN`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `MaskingType-Care Provider`

- **Association:** effect = 0.085 (abs_spearman), n_valid = 38,218
- **Provenance:** demoted_confounded

`MaskingType-Care Provider` is a deterministic re-encoding / tally of `study_design_info/masking`; its association with `dropout_YN` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `MaskingType-Outcomes Assessor`

- **Association:** effect = 0.084 (abs_spearman), n_valid = 38,218
- **Provenance:** demoted_confounded

`MaskingType-Outcomes Assessor` is a deterministic re-encoding / tally of `study_design_info/masking`; its association with `dropout_YN` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `condition_browse/mesh_term`

- **Association:** effect = 0.084 (abs_spearman), n_valid = 38,302
- **Provenance:** demoted_confounded

`condition_browse/mesh_term` is a deterministic re-encoding / tally of `condition`; its association with `dropout_YN` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `number_of_arms`

- **Association:** effect = 0.083 (abs_spearman), n_valid = 38,016
- **Provenance:** demoted_confounded

`number_of_arms` is a sponsor / methodology design choice with no direct biological pathway to the realised safety rate `dropout_YN`; the association is confounded through `intervention/intervention_type` and `condition` (what is being studied), which carry the genuine safety edges. (R4: confounded design->safety.)

### `ipd_info_type-Statistical Analysis Plan (SAP)`

- **Association:** effect = 0.082 (abs_spearman), n_valid = 2,105
- **Provenance:** demoted_confounded

`ipd_info_type-Statistical Analysis Plan (SAP)` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `dropout_YN`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `study_design_info/allocation`

- **Association:** effect = 0.076 (eta), n_valid = 29,014
- **Provenance:** demoted_confounded

`study_design_info/allocation` is a sponsor / methodology design choice with no direct biological pathway to the realised safety rate `dropout_YN`; the association is confounded through `intervention/intervention_type` and `condition` (what is being studied), which carry the genuine safety edges. (R4: confounded design->safety.)

### `ipd_info_type-Study Protocol`

- **Association:** effect = 0.066 (abs_spearman), n_valid = 2,105
- **Provenance:** demoted_confounded

`ipd_info_type-Study Protocol` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `dropout_YN`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `Procedure intervention Number`

- **Association:** effect = 0.053 (abs_spearman), n_valid = 38,302
- **Provenance:** demoted_confounded

`Procedure intervention Number` is a deterministic re-encoding / tally of `intervention/intervention_type`; its association with `dropout_YN` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `Drug intervention Number`

- **Association:** effect = 0.052 (abs_spearman), n_valid = 38,302
- **Provenance:** demoted_confounded

`Drug intervention Number` is a deterministic re-encoding / tally of `intervention/intervention_type`; its association with `dropout_YN` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)
