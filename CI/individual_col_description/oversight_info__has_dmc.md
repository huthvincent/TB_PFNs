# oversight_info/has_dmc

- **Group:** `design_oversight`
- **Dtype:** categorical (Yes/No)
- **Description:** Whether the trial has an independent Data Monitoring Committee.
- **Associated partners (from `association.md`):** 38
  - Direct **causes** (parents of this feature): **2**
  - Direct **effects** (children of this feature): **2**
  - Associated but **no direct** causal edge: **34**

This per-feature file enumerates only **associated** partners. All other columns in `DAG.json` were ruled independent in the Stage-1 association screen and do not appear here. See `association.md` for the screen.

---

## Direct causes (2)

### `sponsors/lead_sponsor/agency_class`

- **Association:** effect = 0.261 (cramers_v), n_valid = 37,612
- **Mechanism:** `design_choice`
- **Provenance:** default_cross_tier

Sponsor design decision made at registration (sponsors/lead_sponsor/agency_class) that constrains a downstream design field (oversight_info/has_dmc).

### `phase`

- **Association:** effect = 0.164 (cramers_v), n_valid = 45,926
- **Mechanism:** `design_choice`
- **Provenance:** default_cross_tier

Sponsor design decision made at registration (phase) that constrains a downstream design field (oversight_info/has_dmc).

---

## Direct effects (2)

### `sae_rate`

- **Association:** effect = 0.174 (eta), n_valid = 16,069
- **Mechanism:** `operational`
- **Provenance:** explicit

An active Data Monitoring Committee enforces early-stopping rules for safety, truncating realised SAE rates.

### `mortality_rate`

- **Association:** effect = 0.150 (eta), n_valid = 16,069
- **Mechanism:** `operational`
- **Provenance:** explicit

DMC-driven futility / safety stops cap accrued mortality before the protocol-defined endpoint.

---

## Associated but no direct causal edge (34)

### `duration_year`

- **Association:** effect = 0.228 (eta), n_valid = 14,181
- **Provenance:** demoted_confounded

`oversight_info/has_dmc` is an oversight / regulatory flag that proxies for trial type and scale; its association with `duration_year` is confounded through `intervention/intervention_type`, `phase`, and trial scale. The genuine oversight mechanisms (FDA-regulation -> approval_outcome; DMC early-stopping -> sae_rate / mortality_rate) are retained as explicit edges. (R10: confounded design_oversight->outcome.)

### `duration_day`

- **Association:** effect = 0.228 (eta), n_valid = 14,181
- **Provenance:** demoted_confounded

`oversight_info/has_dmc` is an oversight / regulatory flag that proxies for trial type and scale; its association with `duration_day` is confounded through `intervention/intervention_type`, `phase`, and trial scale. The genuine oversight mechanisms (FDA-regulation -> approval_outcome; DMC early-stopping -> sae_rate / mortality_rate) are retained as explicit edges. (R10: confounded design_oversight->outcome.)

### `duration_month`

- **Association:** effect = 0.228 (eta), n_valid = 14,181
- **Provenance:** demoted_confounded

`oversight_info/has_dmc` is an oversight / regulatory flag that proxies for trial type and scale; its association with `duration_month` is confounded through `intervention/intervention_type`, `phase`, and trial scale. The genuine oversight mechanisms (FDA-regulation -> approval_outcome; DMC early-stopping -> sae_rate / mortality_rate) are retained as explicit edges. (R10: confounded design_oversight->outcome.)

### `mortality_YN`

- **Association:** effect = 0.216 (eta), n_valid = 16,069
- **Provenance:** demoted_confounded

`oversight_info/has_dmc` is an oversight / regulatory flag that proxies for trial type and scale; its association with `mortality_YN` is confounded through `intervention/intervention_type`, `phase`, and trial scale. The genuine oversight mechanisms (FDA-regulation -> approval_outcome; DMC early-stopping -> sae_rate / mortality_rate) are retained as explicit edges. (R10: confounded design_oversight->outcome.)

### `sae_YN`

- **Association:** effect = 0.176 (eta), n_valid = 16,069
- **Provenance:** demoted_confounded

`oversight_info/has_dmc` is an oversight / regulatory flag that proxies for trial type and scale; its association with `sae_YN` is confounded through `intervention/intervention_type`, `phase`, and trial scale. The genuine oversight mechanisms (FDA-regulation -> approval_outcome; DMC early-stopping -> sae_rate / mortality_rate) are retained as explicit edges. (R10: confounded design_oversight->outcome.)

### `ipd_info_type-Clinical Study Report (CSR)`

- **Association:** effect = 0.143 (eta), n_valid = 1,919
- **Provenance:** default_within_tier

Both in group 'design_oversight' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `responsible_party/responsible_party_type`

- **Association:** effect = 0.140 (cramers_v), n_valid = 35,645
- **Provenance:** default_within_tier

Both in group 'design_oversight' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `study_design_info/primary_purpose`

- **Association:** effect = 0.125 (cramers_v), n_valid = 45,283
- **Provenance:** demoted_confounded

`study_design_info/primary_purpose` has no direct mechanism that sets the oversight / policy field `oversight_info/has_dmc`; the association is confounded through sponsor class and trial type. (R8: confounded ->design_oversight.)

### `study_design_info/intervention_model`

- **Association:** effect = 0.124 (cramers_v), n_valid = 45,679
- **Provenance:** demoted_confounded

`study_design_info/intervention_model` has no direct mechanism that sets the oversight / policy field `oversight_info/has_dmc`; the association is confounded through sponsor class and trial type. (R8: confounded ->design_oversight.)

### `ipd_info_type-Informed Consent Form (ICF)`

- **Association:** effect = 0.123 (eta), n_valid = 1,919
- **Provenance:** default_within_tier

Both in group 'design_oversight' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `approval_outcome`

- **Association:** effect = 0.116 (eta), n_valid = 21,810
- **Provenance:** demoted_confounded

`oversight_info/has_dmc` is an oversight / regulatory flag that proxies for trial type and scale; its association with `approval_outcome` is confounded through `intervention/intervention_type`, `phase`, and trial scale. The genuine oversight mechanisms (FDA-regulation -> approval_outcome; DMC early-stopping -> sae_rate / mortality_rate) are retained as explicit edges. (R10: confounded design_oversight->outcome.)

### `eligibility/healthy_volunteers`

- **Association:** effect = 0.114 (cramers_v), n_valid = 45,906
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_eligibility' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `oversight_info/is_fda_regulated_drug`

- **Association:** effect = 0.107 (cramers_v), n_valid = 12,404
- **Provenance:** default_within_tier

Both in group 'design_oversight' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `location/facility/address/city`

- **Association:** effect = 0.103 (eta), n_valid = 45,926
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_planning' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `study_design_info/masking`

- **Association:** effect = 0.102 (cramers_v), n_valid = 41,228
- **Provenance:** demoted_confounded

`study_design_info/masking` has no direct mechanism that sets the oversight / policy field `oversight_info/has_dmc`; the association is confounded through sponsor class and trial type. (R8: confounded ->design_oversight.)

### `completion_date`

- **Association:** effect = 0.099 (eta), n_valid = 14,181
- **Provenance:** demoted_confounded

`oversight_info/has_dmc` is an oversight / regulatory flag that proxies for trial type and scale; its association with `completion_date` is confounded through `intervention/intervention_type`, `phase`, and trial scale. The genuine oversight mechanisms (FDA-regulation -> approval_outcome; DMC early-stopping -> sae_rate / mortality_rate) are retained as explicit edges. (R10: confounded design_oversight->outcome.)

### `ipd_info_type-Statistical Analysis Plan (SAP)`

- **Association:** effect = 0.090 (eta), n_valid = 2,059
- **Provenance:** default_within_tier

Both in group 'design_oversight' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `MaskingType-Care Provider`

- **Association:** effect = 0.084 (eta), n_valid = 45,821
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `dropout_rate`

- **Association:** effect = 0.078 (eta), n_valid = 32,996
- **Provenance:** demoted_confounded

`oversight_info/has_dmc` is an oversight / regulatory flag that proxies for trial type and scale; its association with `dropout_rate` is confounded through `intervention/intervention_type`, `phase`, and trial scale. The genuine oversight mechanisms (FDA-regulation -> approval_outcome; DMC early-stopping -> sae_rate / mortality_rate) are retained as explicit edges. (R10: confounded design_oversight->outcome.)

### `Radiation intervention Number`

- **Association:** effect = 0.076 (eta), n_valid = 45,926
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `Other intervention Number`

- **Association:** effect = 0.074 (eta), n_valid = 37,612
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `condition_browse/mesh_term`

- **Association:** effect = 0.071 (eta), n_valid = 45,926
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `study_design_info/allocation`

- **Association:** effect = 0.071 (cramers_v), n_valid = 34,580
- **Provenance:** demoted_confounded

`study_design_info/allocation` has no direct mechanism that sets the oversight / policy field `oversight_info/has_dmc`; the association is confounded through sponsor class and trial type. (R8: confounded ->design_oversight.)

### `intervention/intervention_name`

- **Association:** effect = 0.067 (eta), n_valid = 45,926
- **Provenance:** demoted_confounded

`intervention/intervention_name` has no direct mechanism that sets the oversight / policy field `oversight_info/has_dmc`; the association is confounded through sponsor class and trial type. (R8: confounded ->design_oversight.)

### `patient_data/sharing_ipd`

- **Association:** effect = 0.065 (cramers_v), n_valid = 12,367
- **Provenance:** default_within_tier

Both in group 'design_oversight' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `failure_reason`

- **Association:** effect = 0.064 (cramers_v), n_valid = 13,941
- **Provenance:** demoted_confounded

`oversight_info/has_dmc` is an oversight / regulatory flag that proxies for trial type and scale; its association with `failure_reason` is confounded through `intervention/intervention_type`, `phase`, and trial scale. The genuine oversight mechanisms (FDA-regulation -> approval_outcome; DMC early-stopping -> sae_rate / mortality_rate) are retained as explicit edges. (R10: confounded design_oversight->outcome.)

### `biology_pass`

- **Association:** effect = 0.063 (eta), n_valid = 23,795
- **Provenance:** demoted_confounded

`oversight_info/has_dmc` is an oversight / regulatory flag that proxies for trial type and scale; its association with `biology_pass` is confounded through `intervention/intervention_type`, `phase`, and trial scale. The genuine oversight mechanisms (FDA-regulation -> approval_outcome; DMC early-stopping -> sae_rate / mortality_rate) are retained as explicit edges. (R10: confounded design_oversight->outcome.)

### `biology_fail`

- **Association:** effect = 0.063 (eta), n_valid = 23,795
- **Provenance:** demoted_confounded

`oversight_info/has_dmc` is an oversight / regulatory flag that proxies for trial type and scale; its association with `biology_fail` is confounded through `intervention/intervention_type`, `phase`, and trial scale. The genuine oversight mechanisms (FDA-regulation -> approval_outcome; DMC early-stopping -> sae_rate / mortality_rate) are retained as explicit edges. (R10: confounded design_oversight->outcome.)

### `study_design_info/masking_num`

- **Association:** effect = 0.060 (eta), n_valid = 45,821
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_oversight' and 'design_derived'); jointly determined by upstream design_top choices, no direct arrow.

### `MaskingType-Outcomes Assessor`

- **Association:** effect = 0.060 (eta), n_valid = 45,821
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `Procedure intervention Number`

- **Association:** effect = 0.056 (eta), n_valid = 37,612
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `Biological intervention Number`

- **Association:** effect = 0.054 (eta), n_valid = 45,926
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `condition`

- **Association:** effect = 0.054 (eta), n_valid = 45,926
- **Provenance:** demoted_confounded

`condition` has no direct mechanism that sets the oversight / policy field `oversight_info/has_dmc`; the association is confounded through sponsor class and trial type. (R8: confounded ->design_oversight.)

### `icdcode`

- **Association:** effect = 0.051 (eta), n_valid = 45,926
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.
