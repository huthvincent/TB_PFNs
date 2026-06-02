# ipd_info_type-Informed Consent Form (ICF)

- **Group:** `design_oversight`
- **Dtype:** indicator (0/1)
- **Description:** Informed Consent Form is among the shared IPD document types.
- **Associated partners (from `association.md`):** 35
  - Direct **causes** (parents of this feature): **2**
  - Direct **effects** (children of this feature): **0**
  - Associated but **no direct** causal edge: **33**

This per-feature file enumerates only **associated** partners. All other columns in `DAG.json` were ruled independent in the Stage-1 association screen and do not appear here. See `association.md` for the screen.

---

## Direct causes (2)

### `phase`

- **Association:** effect = 0.209 (eta), n_valid = 2,145
- **Mechanism:** `design_choice`
- **Provenance:** default_cross_tier

Sponsor design decision made at registration (phase) that constrains a downstream design field (ipd_info_type-Informed Consent Form (ICF)).

### `sponsors/lead_sponsor/agency_class`

- **Association:** effect = 0.162 (eta), n_valid = 2,145
- **Mechanism:** `design_choice`
- **Provenance:** default_cross_tier

Sponsor design decision made at registration (sponsors/lead_sponsor/agency_class) that constrains a downstream design field (ipd_info_type-Informed Consent Form (ICF)).

---

## Direct effects (0)

_(none)_

---

## Associated but no direct causal edge (33)

### `eligibility/healthy_volunteers`

- **Association:** effect = 0.332 (eta), n_valid = 2,145
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_eligibility' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `eligibility/maximum_age`

- **Association:** effect = 0.297 (abs_spearman), n_valid = 1,034
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_eligibility' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `location/facility/address/city`

- **Association:** effect = 0.244 (abs_spearman), n_valid = 2,145
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_oversight' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `Biological intervention Number`

- **Association:** effect = 0.244 (abs_spearman), n_valid = 2,145
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `ipd_info_type-Clinical Study Report (CSR)`

- **Association:** effect = 0.209 (abs_spearman), n_valid = 2,145
- **Provenance:** default_within_tier

Both in group 'design_oversight' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `dropout_rate`

- **Association:** effect = 0.178 (abs_spearman), n_valid = 2,105
- **Provenance:** demoted_confounded

`ipd_info_type-Informed Consent Form (ICF)` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `dropout_rate`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `Drug intervention Number`

- **Association:** effect = 0.171 (abs_spearman), n_valid = 2,145
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `oversight_info/is_fda_regulated_drug`

- **Association:** effect = 0.171 (eta), n_valid = 1,457
- **Provenance:** default_within_tier

Both in group 'design_oversight' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `dropout_YN`

- **Association:** effect = 0.156 (abs_spearman), n_valid = 2,105
- **Provenance:** demoted_confounded

`ipd_info_type-Informed Consent Form (ICF)` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `dropout_YN`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `sae_YN`

- **Association:** effect = 0.153 (abs_spearman), n_valid = 1,818
- **Provenance:** demoted_confounded

`ipd_info_type-Informed Consent Form (ICF)` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `sae_YN`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `study_design_info/intervention_model`

- **Association:** effect = 0.152 (eta), n_valid = 2,140
- **Provenance:** demoted_confounded

`study_design_info/intervention_model` has no direct mechanism that sets the oversight / policy field `ipd_info_type-Informed Consent Form (ICF)`; the association is confounded through sponsor class and trial type. (R8: confounded ->design_oversight.)

### `execution_pass`

- **Association:** effect = 0.147 (abs_spearman), n_valid = 2,105
- **Provenance:** demoted_confounded

`ipd_info_type-Informed Consent Form (ICF)` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `execution_pass`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `execution_fail`

- **Association:** effect = 0.147 (abs_spearman), n_valid = 2,105
- **Provenance:** demoted_confounded

`ipd_info_type-Informed Consent Form (ICF)` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `execution_fail`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `responsible_party/responsible_party_type`

- **Association:** effect = 0.130 (eta), n_valid = 2,136
- **Provenance:** default_within_tier

Both in group 'design_oversight' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `condition`

- **Association:** effect = 0.128 (abs_spearman), n_valid = 2,145
- **Provenance:** demoted_confounded

`condition` has no direct mechanism that sets the oversight / policy field `ipd_info_type-Informed Consent Form (ICF)`; the association is confounded through sponsor class and trial type. (R8: confounded ->design_oversight.)

### `enrollment`

- **Association:** effect = 0.127 (abs_spearman), n_valid = 2,145
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_planning' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `mortality_YN`

- **Association:** effect = 0.123 (abs_spearman), n_valid = 1,818
- **Provenance:** demoted_confounded

`ipd_info_type-Informed Consent Form (ICF)` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `mortality_YN`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `oversight_info/has_dmc`

- **Association:** effect = 0.123 (eta), n_valid = 1,919
- **Provenance:** default_within_tier

Both in group 'design_oversight' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `mortality_rate`

- **Association:** effect = 0.120 (abs_spearman), n_valid = 1,818
- **Provenance:** demoted_confounded

`ipd_info_type-Informed Consent Form (ICF)` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `mortality_rate`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `intervention_browse/mesh_term`

- **Association:** effect = 0.117 (abs_spearman), n_valid = 2,145
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `sae_rate`

- **Association:** effect = 0.107 (abs_spearman), n_valid = 1,818
- **Provenance:** demoted_confounded

`ipd_info_type-Informed Consent Form (ICF)` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `sae_rate`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `condition_browse/mesh_term`

- **Association:** effect = 0.107 (abs_spearman), n_valid = 2,145
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `brief_title`

- **Association:** effect = 0.094 (abs_spearman), n_valid = 2,145
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_planning' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `Placebo Comparator Arm Number`

- **Association:** effect = 0.090 (abs_spearman), n_valid = 2,139
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `completion_date`

- **Association:** effect = 0.086 (abs_spearman), n_valid = 1,728
- **Provenance:** demoted_confounded

`ipd_info_type-Informed Consent Form (ICF)` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `completion_date`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `eligibility/minimum_age`

- **Association:** effect = 0.082 (abs_spearman), n_valid = 2,103
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_eligibility' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `start_date`

- **Association:** effect = 0.080 (abs_spearman), n_valid = 1,728
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_oversight' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `smiless`

- **Association:** effect = 0.079 (abs_spearman), n_valid = 2,145
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_oversight' and 'design_derived'); jointly determined by upstream design_top choices, no direct arrow.

### `Procedure intervention Number`

- **Association:** effect = 0.075 (abs_spearman), n_valid = 2,145
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `ipd_info_type-Study Protocol`

- **Association:** effect = 0.070 (abs_spearman), n_valid = 2,145
- **Provenance:** default_within_tier

Both in group 'design_oversight' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `MaskingType-Investigator`

- **Association:** effect = 0.069 (abs_spearman), n_valid = 2,145
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `has_expanded_access`

- **Association:** effect = 0.066 (eta), n_valid = 2,123
- **Provenance:** default_within_tier

Both in group 'design_oversight' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `MaskingType-Participant`

- **Association:** effect = 0.064 (abs_spearman), n_valid = 2,145
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.
