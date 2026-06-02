# oversight_info/is_fda_regulated_device

- **Group:** `design_oversight`
- **Dtype:** categorical (Yes/No)
- **Description:** Whether the trial falls under FDA device regulation.
- **Associated partners (from `association.md`):** 16
  - Direct **causes** (parents of this feature): **1**
  - Direct **effects** (children of this feature): **0**
  - Associated but **no direct** causal edge: **15**

This per-feature file enumerates only **associated** partners. All other columns in `DAG.json` were ruled independent in the Stage-1 association screen and do not appear here. See `association.md` for the screen.

---

## Direct causes (1)

### `phase`

- **Association:** effect = 0.054 (cramers_v), n_valid = 13,676
- **Mechanism:** `design_choice`
- **Provenance:** default_cross_tier

Sponsor design decision made at registration (phase) that constrains a downstream design field (oversight_info/is_fda_regulated_device).

---

## Direct effects (0)

_(none)_

---

## Associated but no direct causal edge (15)

### `Device intervention Number`

- **Association:** effect = 0.637 (eta), n_valid = 11,258
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `Combination Product intervention Number`

- **Association:** effect = 0.182 (eta), n_valid = 13,676
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `study_design_info/masking`

- **Association:** effect = 0.117 (cramers_v), n_valid = 13,530
- **Provenance:** demoted_confounded

`study_design_info/masking` has no direct mechanism that sets the oversight / policy field `oversight_info/is_fda_regulated_device`; the association is confounded through sponsor class and trial type. (R8: confounded ->design_oversight.)

### `study_design_info/primary_purpose`

- **Association:** effect = 0.116 (cramers_v), n_valid = 13,675
- **Provenance:** demoted_confounded

`study_design_info/primary_purpose` has no direct mechanism that sets the oversight / policy field `oversight_info/is_fda_regulated_device`; the association is confounded through sponsor class and trial type. (R8: confounded ->design_oversight.)

### `Sham Comparator Arm Number`

- **Association:** effect = 0.110 (eta), n_valid = 11,246
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `Drug intervention Number`

- **Association:** effect = 0.097 (eta), n_valid = 13,676
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `oversight_info/is_fda_regulated_drug`

- **Association:** effect = 0.096 (cramers_v), n_valid = 13,554
- **Provenance:** default_within_tier

Both in group 'design_oversight' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `MaskingType-Investigator`

- **Association:** effect = 0.074 (eta), n_valid = 13,666
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `patient_data/sharing_ipd`

- **Association:** effect = 0.068 (cramers_v), n_valid = 7,697
- **Provenance:** default_within_tier

Both in group 'design_oversight' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `Placebo Comparator Arm Number`

- **Association:** effect = 0.065 (eta), n_valid = 13,650
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `Radiation intervention Number`

- **Association:** effect = 0.065 (eta), n_valid = 13,676
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `sae_YN`

- **Association:** effect = 0.060 (eta), n_valid = 10,378
- **Provenance:** demoted_confounded

`oversight_info/is_fda_regulated_device` is an oversight / regulatory flag that proxies for trial type and scale; its association with `sae_YN` is confounded through `intervention/intervention_type`, `phase`, and trial scale. The genuine oversight mechanisms (FDA-regulation -> approval_outcome; DMC early-stopping -> sae_rate / mortality_rate) are retained as explicit edges. (R10: confounded design_oversight->outcome.)

### `study_design_info/masking_num`

- **Association:** effect = 0.060 (eta), n_valid = 13,666
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_oversight' and 'design_derived'); jointly determined by upstream design_top choices, no direct arrow.

### `MaskingType-Care Provider`

- **Association:** effect = 0.055 (eta), n_valid = 13,666
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `MaskingType-Participant`

- **Association:** effect = 0.055 (eta), n_valid = 13,666
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.
