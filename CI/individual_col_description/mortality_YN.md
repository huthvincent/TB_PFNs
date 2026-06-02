# mortality_YN

- **Group:** `outcome_safety`
- **Dtype:** float (0/1)
- **Description:** Binary indicator: above-threshold mortality rate occurred.
- **Associated partners (from `association.md`):** 53
  - Direct **causes** (parents of this feature): **11**
  - Direct **effects** (children of this feature): **5**
  - Associated but **no direct** causal edge: **37**

This per-feature file enumerates only **associated** partners. All other columns in `DAG.json` were ruled independent in the Stage-1 association screen and do not appear here. See `association.md` for the screen.

---

## Direct causes (11)

### `mortality_rate`

- **Association:** effect = 0.960 (abs_spearman), n_valid = 17,916
- **Mechanism:** `deterministic`
- **Provenance:** explicit

mortality_YN is the thresholded version of mortality_rate.

### `duration_day`

- **Association:** effect = 0.359 (abs_spearman), n_valid = 13,278
- **Mechanism:** `operational`
- **Provenance:** default_cross_tier

Longer / later trial timing (duration_day) accrues more events, raising the realised safety outcome (mortality_YN).

### `duration_year`

- **Association:** effect = 0.359 (abs_spearman), n_valid = 13,278
- **Mechanism:** `operational`
- **Provenance:** default_cross_tier

Longer / later trial timing (duration_year) accrues more events, raising the realised safety outcome (mortality_YN).

### `duration_month`

- **Association:** effect = 0.359 (abs_spearman), n_valid = 13,278
- **Mechanism:** `operational`
- **Provenance:** default_cross_tier

Longer / later trial timing (duration_month) accrues more events, raising the realised safety outcome (mortality_YN).

### `eligibility/healthy_volunteers`

- **Association:** effect = 0.256 (eta), n_valid = 17,914
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Downstream-design field (eligibility/healthy_volunteers) shifts the realised safety outcome (mortality_YN) through population biology or trial operations.

### `eligibility/maximum_age`

- **Association:** effect = 0.242 (abs_spearman), n_valid = 8,723
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Downstream-design field (eligibility/maximum_age) shifts the realised safety outcome (mortality_YN) through population biology or trial operations.

### `phase`

- **Association:** effect = 0.238 (eta), n_valid = 17,916
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Sponsor design decision (phase) that influences the realised safety outcome (mortality_YN) through biology, population, or operations.

### `intervention/intervention_name`

- **Association:** effect = 0.102 (abs_spearman), n_valid = 17,916
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Sponsor design decision (intervention/intervention_name) that influences the realised safety outcome (mortality_YN) through biology, population, or operations.

### `condition`

- **Association:** effect = 0.085 (abs_spearman), n_valid = 17,916
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Sponsor design decision (condition) that influences the realised safety outcome (mortality_YN) through biology, population, or operations.

### `eligibility/gender`

- **Association:** effect = 0.072 (eta), n_valid = 17,916
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Downstream-design field (eligibility/gender) shifts the realised safety outcome (mortality_YN) through population biology or trial operations.

### `eligibility/minimum_age`

- **Association:** effect = 0.058 (abs_spearman), n_valid = 17,440
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Downstream-design field (eligibility/minimum_age) shifts the realised safety outcome (mortality_YN) through population biology or trial operations.

---

## Direct effects (5)

### `failure_reason`

- **Association:** effect = 0.153 (eta), n_valid = 3,199
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Realised safety outcome (mortality_YN) feeds the trial-success label (failure_reason) directly (e.g., 'safety' failure category, regulatory rejection).

### `execution_pass`

- **Association:** effect = 0.145 (abs_spearman), n_valid = 17,903
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Realised safety outcome (mortality_YN) feeds the trial-success label (execution_pass) directly (e.g., 'safety' failure category, regulatory rejection).

### `execution_fail`

- **Association:** effect = 0.145 (abs_spearman), n_valid = 17,903
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Realised safety outcome (mortality_YN) feeds the trial-success label (execution_fail) directly (e.g., 'safety' failure category, regulatory rejection).

### `biology_pass`

- **Association:** effect = 0.074 (abs_spearman), n_valid = 5,792
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Realised safety outcome (mortality_YN) feeds the trial-success label (biology_pass) directly (e.g., 'safety' failure category, regulatory rejection).

### `biology_fail`

- **Association:** effect = 0.074 (abs_spearman), n_valid = 5,792
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Realised safety outcome (mortality_YN) feeds the trial-success label (biology_fail) directly (e.g., 'safety' failure category, regulatory rejection).

---

## Associated but no direct causal edge (37)

### `sae_rate`

- **Association:** effect = 0.632 (abs_spearman), n_valid = 17,916
- **Provenance:** explicit

Mediated through mortality_rate: mortality_YN <- mortality_rate -> sae_rate.

### `sae_YN`

- **Association:** effect = 0.480 (abs_spearman), n_valid = 17,916
- **Provenance:** explicit

Common cause: both downstream of mortality_rate -> sae_rate -> sae_YN; no direct YN-to-YN arrow.

### `location/facility/address/city`

- **Association:** effect = 0.318 (abs_spearman), n_valid = 17,916
- **Provenance:** demoted_confounded

`location/facility/address/city` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `mortality_YN`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `dropout_rate`

- **Association:** effect = 0.266 (abs_spearman), n_valid = 17,873
- **Provenance:** explicit

Mediated through mortality_rate: mortality_YN <- mortality_rate -> dropout_rate.

### `enrollment`

- **Association:** effect = 0.249 (abs_spearman), n_valid = 17,881
- **Provenance:** demoted_confounded

A rate is invariant to sample size in expectation; `enrollment -> mortality_YN` is a threshold-crossing artifact, not a causal effect of N on the safety rate. (R3: rate invariance. Genuine enrollment effects are kept for trial timing and the 'poor enrollment' execution-failure pathway.)

### `oversight_info/has_dmc`

- **Association:** effect = 0.216 (eta), n_valid = 16,069
- **Provenance:** demoted_confounded

`oversight_info/has_dmc` is an oversight / regulatory flag that proxies for trial type and scale; its association with `mortality_YN` is confounded through `intervention/intervention_type`, `phase`, and trial scale. The genuine oversight mechanisms (FDA-regulation -> approval_outcome; DMC early-stopping -> sae_rate / mortality_rate) are retained as explicit edges. (R10: confounded design_oversight->outcome.)

### `study_design_info/primary_purpose`

- **Association:** effect = 0.198 (eta), n_valid = 17,911
- **Provenance:** demoted_confounded

`study_design_info/primary_purpose` is a sponsor / methodology design choice with no direct biological pathway to the realised safety rate `mortality_YN`; the association is confounded through `intervention/intervention_type` and `condition` (what is being studied), which carry the genuine safety edges. (R4: confounded design->safety.)

### `start_date`

- **Association:** effect = 0.196 (abs_spearman), n_valid = 13,278
- **Provenance:** demoted_confounded

`start_date` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `mortality_YN`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `study_design_info/masking`

- **Association:** effect = 0.189 (eta), n_valid = 17,890
- **Provenance:** demoted_confounded

`study_design_info/masking` is a sponsor / methodology design choice with no direct biological pathway to the realised safety rate `mortality_YN`; the association is confounded through `intervention/intervention_type` and `condition` (what is being studied), which carry the genuine safety edges. (R4: confounded design->safety.)

### `study_design_info/intervention_model`

- **Association:** effect = 0.186 (eta), n_valid = 17,857
- **Provenance:** demoted_confounded

`study_design_info/intervention_model` is a sponsor / methodology design choice with no direct biological pathway to the realised safety rate `mortality_YN`; the association is confounded through `intervention/intervention_type` and `condition` (what is being studied), which carry the genuine safety edges. (R4: confounded design->safety.)

### `MaskingType-Participant`

- **Association:** effect = 0.164 (abs_spearman), n_valid = 17,890
- **Provenance:** demoted_confounded

`MaskingType-Participant` is a deterministic re-encoding / tally of `study_design_info/masking`; its association with `mortality_YN` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `study_design_info/masking_num`

- **Association:** effect = 0.155 (abs_spearman), n_valid = 17,890
- **Provenance:** demoted_confounded

`study_design_info/masking_num` is a deterministic re-encoding / tally of `study_design_info/masking`; its association with `mortality_YN` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `patient_data/sharing_ipd`

- **Association:** effect = 0.151 (eta), n_valid = 9,941
- **Provenance:** demoted_confounded

`patient_data/sharing_ipd` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `mortality_YN`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `dropout_YN`

- **Association:** effect = 0.150 (abs_spearman), n_valid = 17,873
- **Provenance:** explicit

Mediated chain through rates.

### `MaskingType-Investigator`

- **Association:** effect = 0.140 (abs_spearman), n_valid = 17,890
- **Provenance:** demoted_confounded

`MaskingType-Investigator` is a deterministic re-encoding / tally of `study_design_info/masking`; its association with `mortality_YN` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `intervention_browse/mesh_term`

- **Association:** effect = 0.138 (abs_spearman), n_valid = 17,916
- **Provenance:** demoted_confounded

`intervention_browse/mesh_term` is a deterministic re-encoding / tally of `intervention/intervention_name`; its association with `mortality_YN` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `Placebo Comparator Arm Number`

- **Association:** effect = 0.137 (abs_spearman), n_valid = 17,886
- **Provenance:** demoted_confounded

`Placebo Comparator Arm Number` is a deterministic re-encoding / tally of `study_design_info/intervention_model`; its association with `mortality_YN` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `condition_browse/mesh_term`

- **Association:** effect = 0.128 (abs_spearman), n_valid = 17,916
- **Provenance:** demoted_confounded

`condition_browse/mesh_term` is a deterministic re-encoding / tally of `condition`; its association with `mortality_YN` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `ipd_info_type-Informed Consent Form (ICF)`

- **Association:** effect = 0.123 (abs_spearman), n_valid = 1,818
- **Provenance:** demoted_confounded

`ipd_info_type-Informed Consent Form (ICF)` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `mortality_YN`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `Radiation intervention Number`

- **Association:** effect = 0.119 (abs_spearman), n_valid = 17,916
- **Provenance:** demoted_confounded

`Radiation intervention Number` is a deterministic re-encoding / tally of `intervention/intervention_type`; its association with `mortality_YN` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `smiless`

- **Association:** effect = 0.113 (abs_spearman), n_valid = 17,916
- **Provenance:** demoted_confounded

`smiless` is a deterministic re-encoding / tally of `intervention/intervention_name`; its association with `mortality_YN` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `ipd_info_type-Clinical Study Report (CSR)`

- **Association:** effect = 0.112 (abs_spearman), n_valid = 1,818
- **Provenance:** demoted_confounded

`ipd_info_type-Clinical Study Report (CSR)` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `mortality_YN`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `responsible_party/responsible_party_type`

- **Association:** effect = 0.111 (eta), n_valid = 17,899
- **Provenance:** demoted_confounded

`responsible_party/responsible_party_type` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `mortality_YN`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `icdcode`

- **Association:** effect = 0.105 (abs_spearman), n_valid = 17,916
- **Provenance:** demoted_confounded

`icdcode` is a deterministic re-encoding / tally of `condition`; its association with `mortality_YN` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `MaskingType-Outcomes Assessor`

- **Association:** effect = 0.096 (abs_spearman), n_valid = 17,890
- **Provenance:** demoted_confounded

`MaskingType-Outcomes Assessor` is a deterministic re-encoding / tally of `study_design_info/masking`; its association with `mortality_YN` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `number_of_arms`

- **Association:** effect = 0.096 (abs_spearman), n_valid = 17,886
- **Provenance:** demoted_confounded

`number_of_arms` is a sponsor / methodology design choice with no direct biological pathway to the realised safety rate `mortality_YN`; the association is confounded through `intervention/intervention_type` and `condition` (what is being studied), which carry the genuine safety edges. (R4: confounded design->safety.)

### `oversight_info/is_fda_regulated_drug`

- **Association:** effect = 0.095 (eta), n_valid = 10,445
- **Provenance:** demoted_confounded

`oversight_info/is_fda_regulated_drug` is an oversight / regulatory flag that proxies for trial type and scale; its association with `mortality_YN` is confounded through `intervention/intervention_type`, `phase`, and trial scale. The genuine oversight mechanisms (FDA-regulation -> approval_outcome; DMC early-stopping -> sae_rate / mortality_rate) are retained as explicit edges. (R10: confounded design_oversight->outcome.)

### `MaskingType-Care Provider`

- **Association:** effect = 0.086 (abs_spearman), n_valid = 17,890
- **Provenance:** demoted_confounded

`MaskingType-Care Provider` is a deterministic re-encoding / tally of `study_design_info/masking`; its association with `mortality_YN` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `Biological intervention Number`

- **Association:** effect = 0.080 (abs_spearman), n_valid = 17,916
- **Provenance:** demoted_confounded

`Biological intervention Number` is a deterministic re-encoding / tally of `intervention/intervention_type`; its association with `mortality_YN` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `sponsors/lead_sponsor/agency_class`

- **Association:** effect = 0.078 (eta), n_valid = 17,916
- **Provenance:** demoted_confounded

`sponsors/lead_sponsor/agency_class` is a sponsor / methodology design choice with no direct biological pathway to the realised safety rate `mortality_YN`; the association is confounded through `intervention/intervention_type` and `condition` (what is being studied), which carry the genuine safety edges. (R4: confounded design->safety.)

### `Procedure intervention Number`

- **Association:** effect = 0.073 (abs_spearman), n_valid = 17,916
- **Provenance:** demoted_confounded

`Procedure intervention Number` is a deterministic re-encoding / tally of `intervention/intervention_type`; its association with `mortality_YN` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `ipd_info_type-Analytic Code`

- **Association:** effect = 0.067 (abs_spearman), n_valid = 1,818
- **Provenance:** demoted_confounded

`ipd_info_type-Analytic Code` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `mortality_YN`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `ipd_info_type-Study Protocol`

- **Association:** effect = 0.065 (abs_spearman), n_valid = 1,818
- **Provenance:** demoted_confounded

`ipd_info_type-Study Protocol` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `mortality_YN`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `study_design_info/allocation`

- **Association:** effect = 0.064 (eta), n_valid = 13,259
- **Provenance:** demoted_confounded

`study_design_info/allocation` is a sponsor / methodology design choice with no direct biological pathway to the realised safety rate `mortality_YN`; the association is confounded through `intervention/intervention_type` and `condition` (what is being studied), which carry the genuine safety edges. (R4: confounded design->safety.)

### `ipd_info_type-Statistical Analysis Plan (SAP)`

- **Association:** effect = 0.064 (abs_spearman), n_valid = 1,818
- **Provenance:** demoted_confounded

`ipd_info_type-Statistical Analysis Plan (SAP)` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `mortality_YN`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `has_expanded_access`

- **Association:** effect = 0.063 (eta), n_valid = 17,570
- **Provenance:** demoted_confounded

`has_expanded_access` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `mortality_YN`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `Drug intervention Number`

- **Association:** effect = 0.060 (abs_spearman), n_valid = 17,916
- **Provenance:** demoted_confounded

`Drug intervention Number` is a deterministic re-encoding / tally of `intervention/intervention_type`; its association with `mortality_YN` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)
