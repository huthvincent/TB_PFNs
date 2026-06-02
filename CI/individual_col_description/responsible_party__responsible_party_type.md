# responsible_party/responsible_party_type

- **Group:** `design_oversight`
- **Dtype:** categorical
- **Description:** Who is responsible for the trial: Sponsor / Sponsor-Investigator / Principal Investigator.
- **Associated partners (from `association.md`):** 42
  - Direct **causes** (parents of this feature): **2**
  - Direct **effects** (children of this feature): **0**
  - Associated but **no direct** causal edge: **40**

This per-feature file enumerates only **associated** partners. All other columns in `DAG.json` were ruled independent in the Stage-1 association screen and do not appear here. See `association.md` for the screen.

---

## Direct causes (2)

### `sponsors/lead_sponsor/agency_class`

- **Association:** effect = 0.420 (cramers_v), n_valid = 67,878
- **Mechanism:** `design_choice`
- **Provenance:** default_cross_tier

Sponsor design decision made at registration (sponsors/lead_sponsor/agency_class) that constrains a downstream design field (responsible_party/responsible_party_type).

### `phase`

- **Association:** effect = 0.209 (cramers_v), n_valid = 67,878
- **Mechanism:** `design_choice`
- **Provenance:** default_cross_tier

Sponsor design decision made at registration (phase) that constrains a downstream design field (responsible_party/responsible_party_type).

---

## Direct effects (0)

_(none)_

---

## Associated but no direct causal edge (40)

### `ipd_info_type-Clinical Study Report (CSR)`

- **Association:** effect = 0.315 (eta), n_valid = 2,136
- **Provenance:** default_within_tier

Both in group 'design_oversight' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `sae_YN`

- **Association:** effect = 0.260 (eta), n_valid = 17,899
- **Provenance:** demoted_confounded

`responsible_party/responsible_party_type` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `sae_YN`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `patient_data/sharing_ipd`

- **Association:** effect = 0.223 (cramers_v), n_valid = 13,499
- **Provenance:** default_within_tier

Both in group 'design_oversight' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `ipd_info_type-Statistical Analysis Plan (SAP)`

- **Association:** effect = 0.222 (eta), n_valid = 2,136
- **Provenance:** default_within_tier

Both in group 'design_oversight' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `Experimental Arm Number`

- **Association:** effect = 0.179 (eta), n_valid = 66,924
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `ipd_info_type-Study Protocol`

- **Association:** effect = 0.161 (eta), n_valid = 2,136
- **Provenance:** default_within_tier

Both in group 'design_oversight' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `approval_outcome`

- **Association:** effect = 0.147 (eta), n_valid = 21,870
- **Provenance:** demoted_confounded

`responsible_party/responsible_party_type` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `approval_outcome`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `location/facility/address/city`

- **Association:** effect = 0.146 (eta), n_valid = 67,878
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_planning' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `dropout_YN`

- **Association:** effect = 0.145 (eta), n_valid = 36,674
- **Provenance:** demoted_confounded

`responsible_party/responsible_party_type` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `dropout_YN`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `oversight_info/has_dmc`

- **Association:** effect = 0.140 (cramers_v), n_valid = 35,645
- **Provenance:** default_within_tier

Both in group 'design_oversight' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `study_design_info/masking`

- **Association:** effect = 0.131 (cramers_v), n_valid = 63,064
- **Provenance:** demoted_confounded

`study_design_info/masking` has no direct mechanism that sets the oversight / policy field `responsible_party/responsible_party_type`; the association is confounded through sponsor class and trial type. (R8: confounded ->design_oversight.)

### `ipd_info_type-Informed Consent Form (ICF)`

- **Association:** effect = 0.130 (eta), n_valid = 2,136
- **Provenance:** default_within_tier

Both in group 'design_oversight' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `ipd_info_type-Analytic Code`

- **Association:** effect = 0.127 (eta), n_valid = 2,136
- **Provenance:** default_within_tier

Both in group 'design_oversight' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `Active Comparator Arm Number`

- **Association:** effect = 0.120 (eta), n_valid = 66,924
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `No Intervention Arm Number`

- **Association:** effect = 0.113 (eta), n_valid = 66,924
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `mortality_YN`

- **Association:** effect = 0.111 (eta), n_valid = 17,899
- **Provenance:** demoted_confounded

`responsible_party/responsible_party_type` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `mortality_YN`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `number_of_arms`

- **Association:** effect = 0.110 (eta), n_valid = 66,924
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `completion_date`

- **Association:** effect = 0.109 (eta), n_valid = 42,745
- **Provenance:** demoted_confounded

`responsible_party/responsible_party_type` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `completion_date`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `failure_reason`

- **Association:** effect = 0.107 (cramers_v), n_valid = 10,039
- **Provenance:** demoted_confounded

`responsible_party/responsible_party_type` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `failure_reason`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `brief_title`

- **Association:** effect = 0.106 (eta), n_valid = 67,878
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_planning' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `execution_fail`

- **Association:** effect = 0.098 (eta), n_valid = 40,560
- **Provenance:** demoted_confounded

`responsible_party/responsible_party_type` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `execution_fail`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `execution_pass`

- **Association:** effect = 0.098 (eta), n_valid = 40,560
- **Provenance:** demoted_confounded

`responsible_party/responsible_party_type` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `execution_pass`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `dropout_rate`

- **Association:** effect = 0.094 (eta), n_valid = 36,674
- **Provenance:** demoted_confounded

`responsible_party/responsible_party_type` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `dropout_rate`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `Biological intervention Number`

- **Association:** effect = 0.083 (eta), n_valid = 67,878
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `Behavioral intervention Number`

- **Association:** effect = 0.078 (eta), n_valid = 67,878
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `duration_month`

- **Association:** effect = 0.075 (eta), n_valid = 42,745
- **Provenance:** demoted_confounded

`responsible_party/responsible_party_type` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `duration_month`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `duration_day`

- **Association:** effect = 0.075 (eta), n_valid = 42,745
- **Provenance:** demoted_confounded

`responsible_party/responsible_party_type` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `duration_day`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `duration_year`

- **Association:** effect = 0.075 (eta), n_valid = 42,745
- **Provenance:** demoted_confounded

`responsible_party/responsible_party_type` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `duration_year`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `sae_rate`

- **Association:** effect = 0.071 (eta), n_valid = 17,899
- **Provenance:** demoted_confounded

`responsible_party/responsible_party_type` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `sae_rate`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `study_design_info/allocation`

- **Association:** effect = 0.071 (cramers_v), n_valid = 51,309
- **Provenance:** demoted_confounded

`study_design_info/allocation` has no direct mechanism that sets the oversight / policy field `responsible_party/responsible_party_type`; the association is confounded through sponsor class and trial type. (R8: confounded ->design_oversight.)

### `start_date`

- **Association:** effect = 0.069 (eta), n_valid = 42,745
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_oversight' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `study_design_info/primary_purpose`

- **Association:** effect = 0.069 (cramers_v), n_valid = 67,490
- **Provenance:** demoted_confounded

`study_design_info/primary_purpose` has no direct mechanism that sets the oversight / policy field `responsible_party/responsible_party_type`; the association is confounded through sponsor class and trial type. (R8: confounded ->design_oversight.)

### `Drug intervention Number`

- **Association:** effect = 0.067 (eta), n_valid = 67,878
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `intervention/intervention_name`

- **Association:** effect = 0.062 (eta), n_valid = 67,878
- **Provenance:** demoted_confounded

`intervention/intervention_name` has no direct mechanism that sets the oversight / policy field `responsible_party/responsible_party_type`; the association is confounded through sponsor class and trial type. (R8: confounded ->design_oversight.)

### `study_design_info/intervention_model`

- **Association:** effect = 0.062 (cramers_v), n_valid = 67,576
- **Provenance:** demoted_confounded

`study_design_info/intervention_model` has no direct mechanism that sets the oversight / policy field `responsible_party/responsible_party_type`; the association is confounded through sponsor class and trial type. (R8: confounded ->design_oversight.)

### `eligibility/gender`

- **Association:** effect = 0.059 (cramers_v), n_valid = 67,878
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_eligibility' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `Procedure intervention Number`

- **Association:** effect = 0.056 (eta), n_valid = 67,878
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `MaskingType-Outcomes Assessor`

- **Association:** effect = 0.054 (eta), n_valid = 67,639
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `Dietary Supplement intervention Number`

- **Association:** effect = 0.054 (eta), n_valid = 67,878
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `intervention_browse/mesh_term`

- **Association:** effect = 0.051 (eta), n_valid = 67,878
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.
