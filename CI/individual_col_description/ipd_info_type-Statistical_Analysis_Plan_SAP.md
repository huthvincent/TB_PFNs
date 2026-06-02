# ipd_info_type-Statistical Analysis Plan (SAP)

- **Group:** `design_oversight`
- **Dtype:** indicator (0/1)
- **Description:** Statistical Analysis Plan is among the shared IPD document types.
- **Associated partners (from `association.md`):** 27
  - Direct **causes** (parents of this feature): **3**
  - Direct **effects** (children of this feature): **0**
  - Associated but **no direct** causal edge: **24**

This per-feature file enumerates only **associated** partners. All other columns in `DAG.json` were ruled independent in the Stage-1 association screen and do not appear here. See `association.md` for the screen.

---

## Direct causes (3)

### `sponsors/lead_sponsor/agency_class`

- **Association:** effect = 0.433 (eta), n_valid = 2,145
- **Mechanism:** `design_choice`
- **Provenance:** default_cross_tier

Sponsor design decision made at registration (sponsors/lead_sponsor/agency_class) that constrains a downstream design field (ipd_info_type-Statistical Analysis Plan (SAP)).

### `phase`

- **Association:** effect = 0.149 (eta), n_valid = 2,297
- **Mechanism:** `design_choice`
- **Provenance:** default_cross_tier

Sponsor design decision made at registration (phase) that constrains a downstream design field (ipd_info_type-Statistical Analysis Plan (SAP)).

### `intervention/intervention_type`

- **Association:** effect = 0.095 (abs_spearman), n_valid = 2,297
- **Mechanism:** `design_choice`
- **Provenance:** default_cross_tier

Sponsor design decision made at registration (intervention/intervention_type) that constrains a downstream design field (ipd_info_type-Statistical Analysis Plan (SAP)).

---

## Direct effects (0)

_(none)_

---

## Associated but no direct causal edge (24)

### `ipd_info_type-Study Protocol`

- **Association:** effect = 0.242 (abs_spearman), n_valid = 2,297
- **Provenance:** default_within_tier

Both in group 'design_oversight' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `ipd_info_type-Clinical Study Report (CSR)`

- **Association:** effect = 0.236 (abs_spearman), n_valid = 2,145
- **Provenance:** default_within_tier

Both in group 'design_oversight' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `responsible_party/responsible_party_type`

- **Association:** effect = 0.222 (eta), n_valid = 2,136
- **Provenance:** default_within_tier

Both in group 'design_oversight' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `location/facility/address/city`

- **Association:** effect = 0.221 (abs_spearman), n_valid = 2,297
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_oversight' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `sae_YN`

- **Association:** effect = 0.204 (abs_spearman), n_valid = 1,818
- **Provenance:** demoted_confounded

`ipd_info_type-Statistical Analysis Plan (SAP)` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `sae_YN`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `enrollment`

- **Association:** effect = 0.154 (abs_spearman), n_valid = 2,145
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_planning' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `approval_outcome`

- **Association:** effect = 0.131 (abs_spearman), n_valid = 746
- **Provenance:** demoted_confounded

`ipd_info_type-Statistical Analysis Plan (SAP)` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `approval_outcome`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `Experimental Arm Number`

- **Association:** effect = 0.128 (abs_spearman), n_valid = 2,290
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `sae_rate`

- **Association:** effect = 0.127 (abs_spearman), n_valid = 1,818
- **Provenance:** demoted_confounded

`ipd_info_type-Statistical Analysis Plan (SAP)` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `sae_rate`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `execution_fail`

- **Association:** effect = 0.103 (abs_spearman), n_valid = 2,257
- **Provenance:** demoted_confounded

`ipd_info_type-Statistical Analysis Plan (SAP)` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `execution_fail`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `execution_pass`

- **Association:** effect = 0.103 (abs_spearman), n_valid = 2,257
- **Provenance:** demoted_confounded

`ipd_info_type-Statistical Analysis Plan (SAP)` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `execution_pass`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `oversight_info/has_dmc`

- **Association:** effect = 0.090 (eta), n_valid = 2,059
- **Provenance:** default_within_tier

Both in group 'design_oversight' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `condition`

- **Association:** effect = 0.090 (abs_spearman), n_valid = 2,297
- **Provenance:** demoted_confounded

`condition` has no direct mechanism that sets the oversight / policy field `ipd_info_type-Statistical Analysis Plan (SAP)`; the association is confounded through sponsor class and trial type. (R8: confounded ->design_oversight.)

### `Procedure intervention Number`

- **Association:** effect = 0.085 (abs_spearman), n_valid = 2,145
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `icdcode`

- **Association:** effect = 0.083 (abs_spearman), n_valid = 2,297
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `dropout_YN`

- **Association:** effect = 0.082 (abs_spearman), n_valid = 2,105
- **Provenance:** demoted_confounded

`ipd_info_type-Statistical Analysis Plan (SAP)` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `dropout_YN`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `Behavioral intervention Number`

- **Association:** effect = 0.076 (abs_spearman), n_valid = 2,297
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `dropout_rate`

- **Association:** effect = 0.075 (abs_spearman), n_valid = 2,105
- **Provenance:** demoted_confounded

`ipd_info_type-Statistical Analysis Plan (SAP)` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `dropout_rate`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `intervention_browse/mesh_term`

- **Association:** effect = 0.069 (abs_spearman), n_valid = 2,297
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `brief_title`

- **Association:** effect = 0.064 (abs_spearman), n_valid = 2,297
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_planning' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `mortality_YN`

- **Association:** effect = 0.064 (abs_spearman), n_valid = 1,818
- **Provenance:** demoted_confounded

`ipd_info_type-Statistical Analysis Plan (SAP)` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `mortality_YN`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `Drug intervention Number`

- **Association:** effect = 0.062 (abs_spearman), n_valid = 2,297
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `No Intervention Arm Number`

- **Association:** effect = 0.060 (abs_spearman), n_valid = 2,139
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `number_of_arms`

- **Association:** effect = 0.056 (abs_spearman), n_valid = 2,290
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_oversight' and 'design_derived'); jointly determined by upstream design_top choices, no direct arrow.
