# patient_data/sharing_ipd

- **Group:** `design_oversight`
- **Dtype:** categorical
- **Description:** Plan for sharing Individual Participant Data: Yes / No / Undecided.
- **Associated partners (from `association.md`):** 35
  - Direct **causes** (parents of this feature): **2**
  - Direct **effects** (children of this feature): **0**
  - Associated but **no direct** causal edge: **33**

This per-feature file enumerates only **associated** partners. All other columns in `DAG.json` were ruled independent in the Stage-1 association screen and do not appear here. See `association.md` for the screen.

---

## Direct causes (2)

### `sponsors/lead_sponsor/agency_class`

- **Association:** effect = 0.319 (cramers_v), n_valid = 13,510
- **Mechanism:** `design_choice`
- **Provenance:** default_cross_tier

Sponsor design decision made at registration (sponsors/lead_sponsor/agency_class) that constrains a downstream design field (patient_data/sharing_ipd).

### `phase`

- **Association:** effect = 0.182 (cramers_v), n_valid = 13,510
- **Mechanism:** `design_choice`
- **Provenance:** default_cross_tier

Sponsor design decision made at registration (phase) that constrains a downstream design field (patient_data/sharing_ipd).

---

## Direct effects (0)

_(none)_

---

## Associated but no direct causal edge (33)

### `sae_YN`

- **Association:** effect = 0.251 (eta), n_valid = 9,941
- **Provenance:** demoted_confounded

`patient_data/sharing_ipd` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `sae_YN`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `approval_outcome`

- **Association:** effect = 0.248 (eta), n_valid = 4,575
- **Provenance:** demoted_confounded

`patient_data/sharing_ipd` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `approval_outcome`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `location/facility/address/city`

- **Association:** effect = 0.228 (eta), n_valid = 13,510
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_planning' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `responsible_party/responsible_party_type`

- **Association:** effect = 0.223 (cramers_v), n_valid = 13,499
- **Provenance:** default_within_tier

Both in group 'design_oversight' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `completion_date`

- **Association:** effect = 0.200 (eta), n_valid = 9,341
- **Provenance:** demoted_confounded

`patient_data/sharing_ipd` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `completion_date`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `Biological intervention Number`

- **Association:** effect = 0.187 (eta), n_valid = 13,510
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `start_date`

- **Association:** effect = 0.180 (eta), n_valid = 9,341
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_oversight' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `dropout_YN`

- **Association:** effect = 0.177 (eta), n_valid = 12,952
- **Provenance:** demoted_confounded

`patient_data/sharing_ipd` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `dropout_YN`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `Experimental Arm Number`

- **Association:** effect = 0.172 (eta), n_valid = 13,438
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `number_of_arms`

- **Association:** effect = 0.152 (eta), n_valid = 13,438
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `mortality_YN`

- **Association:** effect = 0.151 (eta), n_valid = 9,941
- **Provenance:** demoted_confounded

`patient_data/sharing_ipd` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `mortality_YN`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `execution_pass`

- **Association:** effect = 0.148 (eta), n_valid = 12,954
- **Provenance:** demoted_confounded

`patient_data/sharing_ipd` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `execution_pass`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `execution_fail`

- **Association:** effect = 0.148 (eta), n_valid = 12,954
- **Provenance:** demoted_confounded

`patient_data/sharing_ipd` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `execution_fail`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `failure_reason`

- **Association:** effect = 0.143 (cramers_v), n_valid = 2,274
- **Provenance:** demoted_confounded

`patient_data/sharing_ipd` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `failure_reason`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `eligibility/maximum_age`

- **Association:** effect = 0.129 (eta), n_valid = 6,857
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_eligibility' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `study_design_info/primary_purpose`

- **Association:** effect = 0.125 (cramers_v), n_valid = 13,490
- **Provenance:** demoted_confounded

`study_design_info/primary_purpose` has no direct mechanism that sets the oversight / policy field `patient_data/sharing_ipd`; the association is confounded through sponsor class and trial type. (R8: confounded ->design_oversight.)

### `study_design_info/masking`

- **Association:** effect = 0.124 (cramers_v), n_valid = 12,943
- **Provenance:** demoted_confounded

`study_design_info/masking` has no direct mechanism that sets the oversight / policy field `patient_data/sharing_ipd`; the association is confounded through sponsor class and trial type. (R8: confounded ->design_oversight.)

### `intervention/intervention_name`

- **Association:** effect = 0.115 (eta), n_valid = 13,510
- **Provenance:** demoted_confounded

`intervention/intervention_name` has no direct mechanism that sets the oversight / policy field `patient_data/sharing_ipd`; the association is confounded through sponsor class and trial type. (R8: confounded ->design_oversight.)

### `dropout_rate`

- **Association:** effect = 0.102 (eta), n_valid = 12,952
- **Provenance:** demoted_confounded

`patient_data/sharing_ipd` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `dropout_rate`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `study_design_info/intervention_model`

- **Association:** effect = 0.095 (cramers_v), n_valid = 13,425
- **Provenance:** demoted_confounded

`study_design_info/intervention_model` has no direct mechanism that sets the oversight / policy field `patient_data/sharing_ipd`; the association is confounded through sponsor class and trial type. (R8: confounded ->design_oversight.)

### `MaskingType-Investigator`

- **Association:** effect = 0.085 (eta), n_valid = 13,493
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `sae_rate`

- **Association:** effect = 0.078 (eta), n_valid = 9,941
- **Provenance:** demoted_confounded

`patient_data/sharing_ipd` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `sae_rate`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `brief_title`

- **Association:** effect = 0.076 (eta), n_valid = 13,510
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_planning' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `has_expanded_access`

- **Association:** effect = 0.073 (cramers_v), n_valid = 13,298
- **Provenance:** default_within_tier

Both in group 'design_oversight' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `oversight_info/is_fda_regulated_device`

- **Association:** effect = 0.068 (cramers_v), n_valid = 7,697
- **Provenance:** default_within_tier

Both in group 'design_oversight' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `Drug intervention Number`

- **Association:** effect = 0.066 (eta), n_valid = 13,510
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `oversight_info/is_fda_regulated_drug`

- **Association:** effect = 0.066 (cramers_v), n_valid = 7,749
- **Provenance:** default_within_tier

Both in group 'design_oversight' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `MaskingType-Participant`

- **Association:** effect = 0.066 (eta), n_valid = 13,493
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `oversight_info/has_dmc`

- **Association:** effect = 0.065 (cramers_v), n_valid = 12,367
- **Provenance:** default_within_tier

Both in group 'design_oversight' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `Procedure intervention Number`

- **Association:** effect = 0.062 (eta), n_valid = 13,510
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `icdcode`

- **Association:** effect = 0.059 (eta), n_valid = 13,510
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `No Intervention Arm Number`

- **Association:** effect = 0.058 (eta), n_valid = 13,438
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `Device intervention Number`

- **Association:** effect = 0.056 (eta), n_valid = 13,510
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.
