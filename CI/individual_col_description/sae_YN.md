# sae_YN

- **Group:** `outcome_safety`
- **Dtype:** float (0/1)
- **Description:** Binary indicator: above-threshold serious-adverse-event rate occurred.
- **Associated partners (from `association.md`):** 46
  - Direct **causes** (parents of this feature): **9**
  - Direct **effects** (children of this feature): **6**
  - Associated but **no direct** causal edge: **31**

This per-feature file enumerates only **associated** partners. All other columns in `DAG.json` were ruled independent in the Stage-1 association screen and do not appear here. See `association.md` for the screen.

---

## Direct causes (9)

### `sae_rate`

- **Association:** effect = 0.831 (abs_spearman), n_valid = 17,916
- **Mechanism:** `deterministic`
- **Provenance:** explicit

sae_YN is the thresholded version of sae_rate.

### `phase`

- **Association:** effect = 0.365 (eta), n_valid = 17,916
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Sponsor design decision (phase) that influences the realised safety outcome (sae_YN) through biology, population, or operations.

### `duration_year`

- **Association:** effect = 0.313 (abs_spearman), n_valid = 13,278
- **Mechanism:** `operational`
- **Provenance:** default_cross_tier

Longer / later trial timing (duration_year) accrues more events, raising the realised safety outcome (sae_YN).

### `duration_day`

- **Association:** effect = 0.313 (abs_spearman), n_valid = 13,278
- **Mechanism:** `operational`
- **Provenance:** default_cross_tier

Longer / later trial timing (duration_day) accrues more events, raising the realised safety outcome (sae_YN).

### `duration_month`

- **Association:** effect = 0.312 (abs_spearman), n_valid = 13,278
- **Mechanism:** `operational`
- **Provenance:** default_cross_tier

Longer / later trial timing (duration_month) accrues more events, raising the realised safety outcome (sae_YN).

### `eligibility/healthy_volunteers`

- **Association:** effect = 0.309 (eta), n_valid = 17,914
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Downstream-design field (eligibility/healthy_volunteers) shifts the realised safety outcome (sae_YN) through population biology or trial operations.

### `eligibility/maximum_age`

- **Association:** effect = 0.123 (abs_spearman), n_valid = 8,723
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Downstream-design field (eligibility/maximum_age) shifts the realised safety outcome (sae_YN) through population biology or trial operations.

### `eligibility/gender`

- **Association:** effect = 0.088 (eta), n_valid = 17,916
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Downstream-design field (eligibility/gender) shifts the realised safety outcome (sae_YN) through population biology or trial operations.

### `intervention/intervention_name`

- **Association:** effect = 0.086 (abs_spearman), n_valid = 17,916
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Sponsor design decision (intervention/intervention_name) that influences the realised safety outcome (sae_YN) through biology, population, or operations.

---

## Direct effects (6)

### `execution_fail`

- **Association:** effect = 0.269 (abs_spearman), n_valid = 17,903
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Realised safety outcome (sae_YN) feeds the trial-success label (execution_fail) directly (e.g., 'safety' failure category, regulatory rejection).

### `execution_pass`

- **Association:** effect = 0.269 (abs_spearman), n_valid = 17,903
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Realised safety outcome (sae_YN) feeds the trial-success label (execution_pass) directly (e.g., 'safety' failure category, regulatory rejection).

### `failure_reason`

- **Association:** effect = 0.240 (eta), n_valid = 3,199
- **Mechanism:** `biological`
- **Provenance:** explicit

A substantial SAE incidence drives the trial to be terminated for safety, populating failure_reason='safety'.

### `approval_outcome`

- **Association:** effect = 0.175 (abs_spearman), n_valid = 5,434
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Realised safety outcome (sae_YN) feeds the trial-success label (approval_outcome) directly (e.g., 'safety' failure category, regulatory rejection).

### `biology_pass`

- **Association:** effect = 0.083 (abs_spearman), n_valid = 5,792
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Realised safety outcome (sae_YN) feeds the trial-success label (biology_pass) directly (e.g., 'safety' failure category, regulatory rejection).

### `biology_fail`

- **Association:** effect = 0.083 (abs_spearman), n_valid = 5,792
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Realised safety outcome (sae_YN) feeds the trial-success label (biology_fail) directly (e.g., 'safety' failure category, regulatory rejection).

---

## Associated but no direct causal edge (31)

### `mortality_YN`

- **Association:** effect = 0.480 (abs_spearman), n_valid = 17,916
- **Provenance:** explicit

Common cause: both downstream of mortality_rate -> sae_rate -> sae_YN; no direct YN-to-YN arrow.

### `location/facility/address/city`

- **Association:** effect = 0.477 (abs_spearman), n_valid = 17,916
- **Provenance:** demoted_confounded

`location/facility/address/city` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `sae_YN`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `mortality_rate`

- **Association:** effect = 0.456 (abs_spearman), n_valid = 17,916
- **Provenance:** explicit

Mediated through sae_rate: mortality_rate -> sae_rate -> sae_YN.

### `enrollment`

- **Association:** effect = 0.355 (abs_spearman), n_valid = 17,881
- **Provenance:** demoted_confounded

A rate is invariant to sample size in expectation; `enrollment -> sae_YN` is a threshold-crossing artifact, not a causal effect of N on the safety rate. (R3: rate invariance. Genuine enrollment effects are kept for trial timing and the 'poor enrollment' execution-failure pathway.)

### `dropout_rate`

- **Association:** effect = 0.291 (abs_spearman), n_valid = 17,873
- **Provenance:** explicit

Mediated through sae_rate: sae_YN <- sae_rate -> dropout_rate.

### `dropout_YN`

- **Association:** effect = 0.290 (abs_spearman), n_valid = 17,873
- **Provenance:** explicit

Common cause via sae_rate -> dropout_rate -> dropout_YN.

### `sponsors/lead_sponsor/agency_class`

- **Association:** effect = 0.287 (eta), n_valid = 17,916
- **Provenance:** demoted_confounded

`sponsors/lead_sponsor/agency_class` is a sponsor / methodology design choice with no direct biological pathway to the realised safety rate `sae_YN`; the association is confounded through `intervention/intervention_type` and `condition` (what is being studied), which carry the genuine safety edges. (R4: confounded design->safety.)

### `study_design_info/primary_purpose`

- **Association:** effect = 0.280 (eta), n_valid = 17,911
- **Provenance:** demoted_confounded

`study_design_info/primary_purpose` is a sponsor / methodology design choice with no direct biological pathway to the realised safety rate `sae_YN`; the association is confounded through `intervention/intervention_type` and `condition` (what is being studied), which carry the genuine safety edges. (R4: confounded design->safety.)

### `responsible_party/responsible_party_type`

- **Association:** effect = 0.260 (eta), n_valid = 17,899
- **Provenance:** demoted_confounded

`responsible_party/responsible_party_type` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `sae_YN`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `patient_data/sharing_ipd`

- **Association:** effect = 0.251 (eta), n_valid = 9,941
- **Provenance:** demoted_confounded

`patient_data/sharing_ipd` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `sae_YN`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `study_design_info/intervention_model`

- **Association:** effect = 0.234 (eta), n_valid = 17,857
- **Provenance:** demoted_confounded

`study_design_info/intervention_model` is a sponsor / methodology design choice with no direct biological pathway to the realised safety rate `sae_YN`; the association is confounded through `intervention/intervention_type` and `condition` (what is being studied), which carry the genuine safety edges. (R4: confounded design->safety.)

### `ipd_info_type-Statistical Analysis Plan (SAP)`

- **Association:** effect = 0.204 (abs_spearman), n_valid = 1,818
- **Provenance:** demoted_confounded

`ipd_info_type-Statistical Analysis Plan (SAP)` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `sae_YN`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `start_date`

- **Association:** effect = 0.198 (abs_spearman), n_valid = 13,278
- **Provenance:** demoted_confounded

`start_date` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `sae_YN`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `oversight_info/has_dmc`

- **Association:** effect = 0.176 (eta), n_valid = 16,069
- **Provenance:** demoted_confounded

`oversight_info/has_dmc` is an oversight / regulatory flag that proxies for trial type and scale; its association with `sae_YN` is confounded through `intervention/intervention_type`, `phase`, and trial scale. The genuine oversight mechanisms (FDA-regulation -> approval_outcome; DMC early-stopping -> sae_rate / mortality_rate) are retained as explicit edges. (R10: confounded design_oversight->outcome.)

### `condition_browse/mesh_term`

- **Association:** effect = 0.163 (abs_spearman), n_valid = 17,916
- **Provenance:** demoted_confounded

`condition_browse/mesh_term` is a deterministic re-encoding / tally of `condition`; its association with `sae_YN` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `study_design_info/masking`

- **Association:** effect = 0.154 (eta), n_valid = 17,890
- **Provenance:** demoted_confounded

`study_design_info/masking` is a sponsor / methodology design choice with no direct biological pathway to the realised safety rate `sae_YN`; the association is confounded through `intervention/intervention_type` and `condition` (what is being studied), which carry the genuine safety edges. (R4: confounded design->safety.)

### `ipd_info_type-Informed Consent Form (ICF)`

- **Association:** effect = 0.153 (abs_spearman), n_valid = 1,818
- **Provenance:** demoted_confounded

`ipd_info_type-Informed Consent Form (ICF)` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `sae_YN`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `Biological intervention Number`

- **Association:** effect = 0.132 (abs_spearman), n_valid = 17,916
- **Provenance:** demoted_confounded

`Biological intervention Number` is a deterministic re-encoding / tally of `intervention/intervention_type`; its association with `sae_YN` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `Experimental Arm Number`

- **Association:** effect = 0.110 (abs_spearman), n_valid = 17,886
- **Provenance:** demoted_confounded

`Experimental Arm Number` is a deterministic re-encoding / tally of `study_design_info/intervention_model`; its association with `sae_YN` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `oversight_info/is_fda_regulated_drug`

- **Association:** effect = 0.099 (eta), n_valid = 10,445
- **Provenance:** demoted_confounded

`oversight_info/is_fda_regulated_drug` is an oversight / regulatory flag that proxies for trial type and scale; its association with `sae_YN` is confounded through `intervention/intervention_type`, `phase`, and trial scale. The genuine oversight mechanisms (FDA-regulation -> approval_outcome; DMC early-stopping -> sae_rate / mortality_rate) are retained as explicit edges. (R10: confounded design_oversight->outcome.)

### `ipd_info_type-Study Protocol`

- **Association:** effect = 0.094 (abs_spearman), n_valid = 1,818
- **Provenance:** demoted_confounded

`ipd_info_type-Study Protocol` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `sae_YN`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `ipd_info_type-Analytic Code`

- **Association:** effect = 0.076 (abs_spearman), n_valid = 1,818
- **Provenance:** demoted_confounded

`ipd_info_type-Analytic Code` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `sae_YN`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `has_expanded_access`

- **Association:** effect = 0.072 (eta), n_valid = 17,570
- **Provenance:** demoted_confounded

`has_expanded_access` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `sae_YN`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `brief_title`

- **Association:** effect = 0.070 (abs_spearman), n_valid = 17,916
- **Provenance:** demoted_confounded

`brief_title` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `sae_YN`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `Active Comparator Arm Number`

- **Association:** effect = 0.069 (abs_spearman), n_valid = 17,886
- **Provenance:** demoted_confounded

`Active Comparator Arm Number` is a deterministic re-encoding / tally of `study_design_info/intervention_model`; its association with `sae_YN` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `No Intervention Arm Number`

- **Association:** effect = 0.068 (abs_spearman), n_valid = 17,886
- **Provenance:** demoted_confounded

`No Intervention Arm Number` is a deterministic re-encoding / tally of `study_design_info/intervention_model`; its association with `sae_YN` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `Device intervention Number`

- **Association:** effect = 0.064 (abs_spearman), n_valid = 17,916
- **Provenance:** demoted_confounded

`Device intervention Number` is a deterministic re-encoding / tally of `intervention/intervention_type`; its association with `sae_YN` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `oversight_info/is_fda_regulated_device`

- **Association:** effect = 0.060 (eta), n_valid = 10,378
- **Provenance:** demoted_confounded

`oversight_info/is_fda_regulated_device` is an oversight / regulatory flag that proxies for trial type and scale; its association with `sae_YN` is confounded through `intervention/intervention_type`, `phase`, and trial scale. The genuine oversight mechanisms (FDA-regulation -> approval_outcome; DMC early-stopping -> sae_rate / mortality_rate) are retained as explicit edges. (R10: confounded design_oversight->outcome.)

### `Radiation intervention Number`

- **Association:** effect = 0.057 (abs_spearman), n_valid = 17,916
- **Provenance:** demoted_confounded

`Radiation intervention Number` is a deterministic re-encoding / tally of `intervention/intervention_type`; its association with `sae_YN` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `Other Arm Number`

- **Association:** effect = 0.057 (abs_spearman), n_valid = 17,886
- **Provenance:** demoted_confounded

`Other Arm Number` is a deterministic re-encoding / tally of `study_design_info/intervention_model`; its association with `sae_YN` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `Behavioral intervention Number`

- **Association:** effect = 0.055 (abs_spearman), n_valid = 17,916
- **Provenance:** demoted_confounded

`Behavioral intervention Number` is a deterministic re-encoding / tally of `intervention/intervention_type`; its association with `sae_YN` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)
