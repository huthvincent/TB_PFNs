# Sham Comparator Arm Number

- **Group:** `design_derived`
- **Dtype:** float
- **Description:** Count of arms tagged 'Sham Comparator'.
- **Associated partners (from `association.md`):** 9
  - Direct **causes** (parents of this feature): **0**
  - Direct **effects** (children of this feature): **0**
  - Associated but **no direct** causal edge: **9**

This per-feature file enumerates only **associated** partners. All other columns in `DAG.json` were ruled independent in the Stage-1 association screen and do not appear here. See `association.md` for the screen.

---

## Direct causes (0)

_(none)_

---

## Direct effects (0)

_(none)_

---

## Associated but no direct causal edge (9)

### `study_design_info/masking`

- **Association:** effect = 0.135 (eta), n_valid = 64,055
- **Provenance:** demoted_confounded

`Sham Comparator Arm Number` is a deterministic descendant of its single definitional design parent; `study_design_info/masking` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `Device intervention Number`

- **Association:** effect = 0.118 (abs_spearman), n_valid = 69,293
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `oversight_info/is_fda_regulated_device`

- **Association:** effect = 0.110 (eta), n_valid = 11,246
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `MaskingType-Outcomes Assessor`

- **Association:** effect = 0.071 (abs_spearman), n_valid = 69,142
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `MaskingType-Participant`

- **Association:** effect = 0.067 (abs_spearman), n_valid = 69,142
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `study_design_info/masking_num`

- **Association:** effect = 0.064 (abs_spearman), n_valid = 69,142
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `study_design_info/intervention_model`

- **Association:** effect = 0.056 (eta), n_valid = 69,093
- **Provenance:** demoted_confounded

`Sham Comparator Arm Number` is a deterministic descendant of its single definitional design parent; `study_design_info/intervention_model` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `Procedure intervention Number`

- **Association:** effect = 0.055 (abs_spearman), n_valid = 69,293
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `Drug intervention Number`

- **Association:** effect = 0.052 (abs_spearman), n_valid = 69,293
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.
