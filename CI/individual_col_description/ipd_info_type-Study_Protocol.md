# ipd_info_type-Study Protocol

- **Group:** `design_oversight`
- **Dtype:** indicator (0/1)
- **Description:** Study Protocol is among the shared IPD document types.
- **Associated partners (from `association.md`):** 16
  - Direct **causes** (parents of this feature): **1**
  - Direct **effects** (children of this feature): **0**
  - Associated but **no direct** causal edge: **15**

This per-feature file enumerates only **associated** partners. All other columns in `DAG.json` were ruled independent in the Stage-1 association screen and do not appear here. See `association.md` for the screen.

---

## Direct causes (1)

### `sponsors/lead_sponsor/agency_class`

- **Association:** effect = 0.227 (eta), n_valid = 2,145
- **Mechanism:** `design_choice`
- **Provenance:** default_cross_tier

Sponsor design decision made at registration (sponsors/lead_sponsor/agency_class) that constrains a downstream design field (ipd_info_type-Study Protocol).

---

## Direct effects (0)

_(none)_

---

## Associated but no direct causal edge (15)

### `ipd_info_type-Statistical Analysis Plan (SAP)`

- **Association:** effect = 0.242 (abs_spearman), n_valid = 2,297
- **Provenance:** default_within_tier

Both in group 'design_oversight' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `responsible_party/responsible_party_type`

- **Association:** effect = 0.161 (eta), n_valid = 2,136
- **Provenance:** default_within_tier

Both in group 'design_oversight' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `sae_rate`

- **Association:** effect = 0.098 (abs_spearman), n_valid = 1,818
- **Provenance:** demoted_confounded

`ipd_info_type-Study Protocol` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `sae_rate`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `sae_YN`

- **Association:** effect = 0.094 (abs_spearman), n_valid = 1,818
- **Provenance:** demoted_confounded

`ipd_info_type-Study Protocol` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `sae_YN`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `start_date`

- **Association:** effect = 0.085 (abs_spearman), n_valid = 1,728
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_oversight' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `completion_date`

- **Association:** effect = 0.077 (abs_spearman), n_valid = 1,728
- **Provenance:** demoted_confounded

`ipd_info_type-Study Protocol` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `completion_date`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `location/facility/address/city`

- **Association:** effect = 0.077 (abs_spearman), n_valid = 2,297
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_oversight' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `ipd_info_type-Informed Consent Form (ICF)`

- **Association:** effect = 0.070 (abs_spearman), n_valid = 2,145
- **Provenance:** default_within_tier

Both in group 'design_oversight' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `ipd_info_type-Analytic Code`

- **Association:** effect = 0.069 (abs_spearman), n_valid = 2,297
- **Provenance:** default_within_tier

Both in group 'design_oversight' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `mortality_rate`

- **Association:** effect = 0.068 (abs_spearman), n_valid = 1,818
- **Provenance:** demoted_confounded

`ipd_info_type-Study Protocol` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `mortality_rate`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `dropout_YN`

- **Association:** effect = 0.066 (abs_spearman), n_valid = 2,105
- **Provenance:** demoted_confounded

`ipd_info_type-Study Protocol` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `dropout_YN`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `mortality_YN`

- **Association:** effect = 0.065 (abs_spearman), n_valid = 1,818
- **Provenance:** demoted_confounded

`ipd_info_type-Study Protocol` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `mortality_YN`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `number_of_arms`

- **Association:** effect = 0.064 (abs_spearman), n_valid = 2,290
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_oversight' and 'design_derived'); jointly determined by upstream design_top choices, no direct arrow.

### `Other Arm Number`

- **Association:** effect = 0.060 (abs_spearman), n_valid = 2,290
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `Experimental Arm Number`

- **Association:** effect = 0.059 (abs_spearman), n_valid = 2,290
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.
