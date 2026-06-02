# Other Arm Number

- **Group:** `design_derived`
- **Dtype:** float
- **Description:** Count of arms tagged 'Other'.
- **Associated partners (from `association.md`):** 16
  - Direct **causes** (parents of this feature): **0**
  - Direct **effects** (children of this feature): **0**
  - Associated but **no direct** causal edge: **16**

This per-feature file enumerates only **associated** partners. All other columns in `DAG.json` were ruled independent in the Stage-1 association screen and do not appear here. See `association.md` for the screen.

---

## Direct causes (0)

_(none)_

---

## Direct effects (0)

_(none)_

---

## Associated but no direct causal edge (16)

### `Experimental Arm Number`

- **Association:** effect = 0.222 (abs_spearman), n_valid = 78,123
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `Placebo Comparator Arm Number`

- **Association:** effect = 0.101 (abs_spearman), n_valid = 78,123
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `Active Comparator Arm Number`

- **Association:** effect = 0.088 (abs_spearman), n_valid = 69,293
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `study_design_info/primary_purpose`

- **Association:** effect = 0.082 (eta), n_valid = 77,416
- **Provenance:** demoted_confounded

`Other Arm Number` is a deterministic descendant of its single definitional design parent; `study_design_info/primary_purpose` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `MaskingType-Participant`

- **Association:** effect = 0.080 (abs_spearman), n_valid = 77,947
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `MaskingType-Investigator`

- **Association:** effect = 0.077 (abs_spearman), n_valid = 77,947
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `study_design_info/masking_num`

- **Association:** effect = 0.076 (abs_spearman), n_valid = 77,947
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `Other intervention Number`

- **Association:** effect = 0.072 (abs_spearman), n_valid = 69,293
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `Drug intervention Number`

- **Association:** effect = 0.065 (abs_spearman), n_valid = 78,123
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `phase`

- **Association:** effect = 0.061 (eta), n_valid = 78,123
- **Provenance:** demoted_confounded

`Other Arm Number` is a deterministic descendant of its single definitional design parent; `phase` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `study_design_info/intervention_model`

- **Association:** effect = 0.061 (eta), n_valid = 77,887
- **Provenance:** demoted_confounded

`Other Arm Number` is a deterministic descendant of its single definitional design parent; `study_design_info/intervention_model` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `MaskingType-Care Provider`

- **Association:** effect = 0.060 (abs_spearman), n_valid = 77,947
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `ipd_info_type-Study Protocol`

- **Association:** effect = 0.060 (abs_spearman), n_valid = 2,290
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `sae_YN`

- **Association:** effect = 0.057 (abs_spearman), n_valid = 17,886
- **Provenance:** demoted_confounded

`Other Arm Number` is a deterministic re-encoding / tally of `study_design_info/intervention_model`; its association with `sae_YN` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `study_design_info/masking`

- **Association:** effect = 0.056 (eta), n_valid = 72,860
- **Provenance:** demoted_confounded

`Other Arm Number` is a deterministic descendant of its single definitional design parent; `study_design_info/masking` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `sae_rate`

- **Association:** effect = 0.055 (abs_spearman), n_valid = 17,886
- **Provenance:** demoted_confounded

`Other Arm Number` is a deterministic re-encoding / tally of `study_design_info/intervention_model`; its association with `sae_rate` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)
