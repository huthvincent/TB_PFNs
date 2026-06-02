# has_expanded_access

- **Group:** `design_oversight`
- **Dtype:** categorical (Yes/No)
- **Description:** Whether an expanded-access (compassionate use) program is associated with this drug.
- **Associated partners (from `association.md`):** 9
  - Direct **causes** (parents of this feature): **1**
  - Direct **effects** (children of this feature): **0**
  - Associated but **no direct** causal edge: **8**

This per-feature file enumerates only **associated** partners. All other columns in `DAG.json` were ruled independent in the Stage-1 association screen and do not appear here. See `association.md` for the screen.

---

## Direct causes (1)

### `sponsors/lead_sponsor/agency_class`

- **Association:** effect = 0.069 (cramers_v), n_valid = 70,125
- **Mechanism:** `design_choice`
- **Provenance:** default_cross_tier

Sponsor design decision made at registration (sponsors/lead_sponsor/agency_class) that constrains a downstream design field (has_expanded_access).

---

## Direct effects (0)

_(none)_

---

## Associated but no direct causal edge (8)

### `patient_data/sharing_ipd`

- **Association:** effect = 0.073 (cramers_v), n_valid = 13,298
- **Provenance:** default_within_tier

Both in group 'design_oversight' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `sae_YN`

- **Association:** effect = 0.072 (eta), n_valid = 17,570
- **Provenance:** demoted_confounded

`has_expanded_access` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `sae_YN`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `ipd_info_type-Informed Consent Form (ICF)`

- **Association:** effect = 0.066 (eta), n_valid = 2,123
- **Provenance:** default_within_tier

Both in group 'design_oversight' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `sae_rate`

- **Association:** effect = 0.064 (eta), n_valid = 17,570
- **Provenance:** demoted_confounded

`has_expanded_access` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `sae_rate`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `mortality_YN`

- **Association:** effect = 0.063 (eta), n_valid = 17,570
- **Provenance:** demoted_confounded

`has_expanded_access` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `mortality_YN`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `dropout_rate`

- **Association:** effect = 0.057 (eta), n_valid = 37,901
- **Provenance:** demoted_confounded

`has_expanded_access` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `dropout_rate`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `location/facility/address/city`

- **Association:** effect = 0.056 (eta), n_valid = 70,125
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_oversight' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `mortality_rate`

- **Association:** effect = 0.054 (eta), n_valid = 17,570
- **Provenance:** demoted_confounded

`has_expanded_access` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `mortality_rate`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)
