# oversight_info/is_fda_regulated_drug

- **Group:** `design_oversight`
- **Dtype:** categorical (Yes/No)
- **Description:** Whether the trial falls under FDA drug regulation.
- **Associated partners (from `association.md`):** 35
  - Direct **causes** (parents of this feature): **3**
  - Direct **effects** (children of this feature): **0**
  - Associated but **no direct** causal edge: **32**

This per-feature file enumerates only **associated** partners. All other columns in `DAG.json` were ruled independent in the Stage-1 association screen and do not appear here. See `association.md` for the screen.

---

## Direct causes (3)

### `phase`

- **Association:** effect = 0.144 (cramers_v), n_valid = 13,761
- **Mechanism:** `design_choice`
- **Provenance:** default_cross_tier

Sponsor design decision made at registration (phase) that constrains a downstream design field (oversight_info/is_fda_regulated_drug).

### `intervention/intervention_type`

- **Association:** effect = 0.133 (eta), n_valid = 13,761
- **Mechanism:** `regulatory`
- **Provenance:** explicit

Type in {Drug, Biological} triggers FDA drug regulation (NDA / BLA pathway) by definition.

### `sponsors/lead_sponsor/agency_class`

- **Association:** effect = 0.080 (cramers_v), n_valid = 11,339
- **Mechanism:** `design_choice`
- **Provenance:** default_cross_tier

Sponsor design decision made at registration (sponsors/lead_sponsor/agency_class) that constrains a downstream design field (oversight_info/is_fda_regulated_drug).

---

## Direct effects (0)

_(none)_

---

## Associated but no direct causal edge (32)

### `ipd_info_type-Informed Consent Form (ICF)`

- **Association:** effect = 0.171 (eta), n_valid = 1,457
- **Provenance:** default_within_tier

Both in group 'design_oversight' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `execution_fail`

- **Association:** effect = 0.151 (eta), n_valid = 13,615
- **Provenance:** demoted_confounded

`oversight_info/is_fda_regulated_drug` is an oversight / regulatory flag that proxies for trial type and scale; its association with `execution_fail` is confounded through `intervention/intervention_type`, `phase`, and trial scale. The genuine oversight mechanisms (FDA-regulation -> approval_outcome; DMC early-stopping -> sae_rate / mortality_rate) are retained as explicit edges. (R10: confounded design_oversight->outcome.)

### `execution_pass`

- **Association:** effect = 0.151 (eta), n_valid = 13,615
- **Provenance:** demoted_confounded

`oversight_info/is_fda_regulated_drug` is an oversight / regulatory flag that proxies for trial type and scale; its association with `execution_pass` is confounded through `intervention/intervention_type`, `phase`, and trial scale. The genuine oversight mechanisms (FDA-regulation -> approval_outcome; DMC early-stopping -> sae_rate / mortality_rate) are retained as explicit edges. (R10: confounded design_oversight->outcome.)

### `failure_reason`

- **Association:** effect = 0.118 (cramers_v), n_valid = 4,623
- **Provenance:** demoted_confounded

`oversight_info/is_fda_regulated_drug` is an oversight / regulatory flag that proxies for trial type and scale; its association with `failure_reason` is confounded through `intervention/intervention_type`, `phase`, and trial scale. The genuine oversight mechanisms (FDA-regulation -> approval_outcome; DMC early-stopping -> sae_rate / mortality_rate) are retained as explicit edges. (R10: confounded design_oversight->outcome.)

### `Device intervention Number`

- **Association:** effect = 0.116 (eta), n_valid = 11,339
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `location/facility/address/city`

- **Association:** effect = 0.108 (eta), n_valid = 13,761
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_planning' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `oversight_info/has_dmc`

- **Association:** effect = 0.107 (cramers_v), n_valid = 12,404
- **Provenance:** default_within_tier

Both in group 'design_oversight' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `eligibility/healthy_volunteers`

- **Association:** effect = 0.105 (cramers_v), n_valid = 13,761
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_eligibility' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `Drug intervention Number`

- **Association:** effect = 0.103 (eta), n_valid = 13,761
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `sae_YN`

- **Association:** effect = 0.099 (eta), n_valid = 10,445
- **Provenance:** demoted_confounded

`oversight_info/is_fda_regulated_drug` is an oversight / regulatory flag that proxies for trial type and scale; its association with `sae_YN` is confounded through `intervention/intervention_type`, `phase`, and trial scale. The genuine oversight mechanisms (FDA-regulation -> approval_outcome; DMC early-stopping -> sae_rate / mortality_rate) are retained as explicit edges. (R10: confounded design_oversight->outcome.)

### `study_design_info/primary_purpose`

- **Association:** effect = 0.099 (cramers_v), n_valid = 13,761
- **Provenance:** demoted_confounded

`study_design_info/primary_purpose` has no direct mechanism that sets the oversight / policy field `oversight_info/is_fda_regulated_drug`; the association is confounded through sponsor class and trial type. (R8: confounded ->design_oversight.)

### `sae_rate`

- **Association:** effect = 0.097 (eta), n_valid = 10,445
- **Provenance:** demoted_confounded

`oversight_info/is_fda_regulated_drug` is an oversight / regulatory flag that proxies for trial type and scale; its association with `sae_rate` is confounded through `intervention/intervention_type`, `phase`, and trial scale. The genuine oversight mechanisms (FDA-regulation -> approval_outcome; DMC early-stopping -> sae_rate / mortality_rate) are retained as explicit edges. (R10: confounded design_oversight->outcome.)

### `oversight_info/is_fda_regulated_device`

- **Association:** effect = 0.096 (cramers_v), n_valid = 13,554
- **Provenance:** default_within_tier

Both in group 'design_oversight' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `mortality_YN`

- **Association:** effect = 0.095 (eta), n_valid = 10,445
- **Provenance:** demoted_confounded

`oversight_info/is_fda_regulated_drug` is an oversight / regulatory flag that proxies for trial type and scale; its association with `mortality_YN` is confounded through `intervention/intervention_type`, `phase`, and trial scale. The genuine oversight mechanisms (FDA-regulation -> approval_outcome; DMC early-stopping -> sae_rate / mortality_rate) are retained as explicit edges. (R10: confounded design_oversight->outcome.)

### `study_design_info/masking`

- **Association:** effect = 0.094 (cramers_v), n_valid = 13,609
- **Provenance:** demoted_confounded

`study_design_info/masking` has no direct mechanism that sets the oversight / policy field `oversight_info/is_fda_regulated_drug`; the association is confounded through sponsor class and trial type. (R8: confounded ->design_oversight.)

### `duration_day`

- **Association:** effect = 0.090 (eta), n_valid = 9,820
- **Provenance:** demoted_confounded

`oversight_info/is_fda_regulated_drug` is an oversight / regulatory flag that proxies for trial type and scale; its association with `duration_day` is confounded through `intervention/intervention_type`, `phase`, and trial scale. The genuine oversight mechanisms (FDA-regulation -> approval_outcome; DMC early-stopping -> sae_rate / mortality_rate) are retained as explicit edges. (R10: confounded design_oversight->outcome.)

### `duration_year`

- **Association:** effect = 0.090 (eta), n_valid = 9,820
- **Provenance:** demoted_confounded

`oversight_info/is_fda_regulated_drug` is an oversight / regulatory flag that proxies for trial type and scale; its association with `duration_year` is confounded through `intervention/intervention_type`, `phase`, and trial scale. The genuine oversight mechanisms (FDA-regulation -> approval_outcome; DMC early-stopping -> sae_rate / mortality_rate) are retained as explicit edges. (R10: confounded design_oversight->outcome.)

### `duration_month`

- **Association:** effect = 0.090 (eta), n_valid = 9,820
- **Provenance:** demoted_confounded

`oversight_info/is_fda_regulated_drug` is an oversight / regulatory flag that proxies for trial type and scale; its association with `duration_month` is confounded through `intervention/intervention_type`, `phase`, and trial scale. The genuine oversight mechanisms (FDA-regulation -> approval_outcome; DMC early-stopping -> sae_rate / mortality_rate) are retained as explicit edges. (R10: confounded design_oversight->outcome.)

### `dropout_rate`

- **Association:** effect = 0.090 (eta), n_valid = 11,191
- **Provenance:** demoted_confounded

`oversight_info/is_fda_regulated_drug` is an oversight / regulatory flag that proxies for trial type and scale; its association with `dropout_rate` is confounded through `intervention/intervention_type`, `phase`, and trial scale. The genuine oversight mechanisms (FDA-regulation -> approval_outcome; DMC early-stopping -> sae_rate / mortality_rate) are retained as explicit edges. (R10: confounded design_oversight->outcome.)

### `completion_date`

- **Association:** effect = 0.087 (eta), n_valid = 9,820
- **Provenance:** demoted_confounded

`oversight_info/is_fda_regulated_drug` is an oversight / regulatory flag that proxies for trial type and scale; its association with `completion_date` is confounded through `intervention/intervention_type`, `phase`, and trial scale. The genuine oversight mechanisms (FDA-regulation -> approval_outcome; DMC early-stopping -> sae_rate / mortality_rate) are retained as explicit edges. (R10: confounded design_oversight->outcome.)

### `ipd_info_type-Clinical Study Report (CSR)`

- **Association:** effect = 0.083 (eta), n_valid = 1,457
- **Provenance:** default_within_tier

Both in group 'design_oversight' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `mortality_rate`

- **Association:** effect = 0.080 (eta), n_valid = 10,445
- **Provenance:** demoted_confounded

`oversight_info/is_fda_regulated_drug` is an oversight / regulatory flag that proxies for trial type and scale; its association with `mortality_rate` is confounded through `intervention/intervention_type`, `phase`, and trial scale. The genuine oversight mechanisms (FDA-regulation -> approval_outcome; DMC early-stopping -> sae_rate / mortality_rate) are retained as explicit edges. (R10: confounded design_oversight->outcome.)

### `intervention_browse/mesh_term`

- **Association:** effect = 0.074 (eta), n_valid = 13,761
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `intervention/intervention_name`

- **Association:** effect = 0.073 (eta), n_valid = 13,761
- **Provenance:** demoted_confounded

`intervention/intervention_name` has no direct mechanism that sets the oversight / policy field `oversight_info/is_fda_regulated_drug`; the association is confounded through sponsor class and trial type. (R8: confounded ->design_oversight.)

### `smiless`

- **Association:** effect = 0.069 (eta), n_valid = 13,761
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_oversight' and 'design_derived'); jointly determined by upstream design_top choices, no direct arrow.

### `patient_data/sharing_ipd`

- **Association:** effect = 0.066 (cramers_v), n_valid = 7,749
- **Provenance:** default_within_tier

Both in group 'design_oversight' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `biology_pass`

- **Association:** effect = 0.065 (eta), n_valid = 5,975
- **Provenance:** demoted_confounded

`oversight_info/is_fda_regulated_drug` is an oversight / regulatory flag that proxies for trial type and scale; its association with `biology_pass` is confounded through `intervention/intervention_type`, `phase`, and trial scale. The genuine oversight mechanisms (FDA-regulation -> approval_outcome; DMC early-stopping -> sae_rate / mortality_rate) are retained as explicit edges. (R10: confounded design_oversight->outcome.)

### `biology_fail`

- **Association:** effect = 0.065 (eta), n_valid = 5,975
- **Provenance:** demoted_confounded

`oversight_info/is_fda_regulated_drug` is an oversight / regulatory flag that proxies for trial type and scale; its association with `biology_fail` is confounded through `intervention/intervention_type`, `phase`, and trial scale. The genuine oversight mechanisms (FDA-regulation -> approval_outcome; DMC early-stopping -> sae_rate / mortality_rate) are retained as explicit edges. (R10: confounded design_oversight->outcome.)

### `eligibility/gender`

- **Association:** effect = 0.065 (cramers_v), n_valid = 11,339
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_eligibility' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `study_design_info/intervention_model`

- **Association:** effect = 0.060 (cramers_v), n_valid = 13,721
- **Provenance:** demoted_confounded

`study_design_info/intervention_model` has no direct mechanism that sets the oversight / policy field `oversight_info/is_fda_regulated_drug`; the association is confounded through sponsor class and trial type. (R8: confounded ->design_oversight.)

### `condition_browse/mesh_term`

- **Association:** effect = 0.059 (eta), n_valid = 13,761
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `Placebo Comparator Arm Number`

- **Association:** effect = 0.050 (eta), n_valid = 13,735
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.
