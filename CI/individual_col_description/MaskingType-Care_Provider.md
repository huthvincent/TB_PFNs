# MaskingType-Care Provider

- **Group:** `design_derived`
- **Dtype:** indicator (0/1)
- **Description:** Care provider is masked.
- **Associated partners (from `association.md`):** 36
  - Direct **causes** (parents of this feature): **1**
  - Direct **effects** (children of this feature): **1**
  - Associated but **no direct** causal edge: **34**

This per-feature file enumerates only **associated** partners. All other columns in `DAG.json` were ruled independent in the Stage-1 association screen and do not appear here. See `association.md` for the screen.

---

## Direct causes (1)

### `study_design_info/masking`

- **Association:** effect = 1.000 (eta), n_valid = 75,043
- **Mechanism:** `deterministic`
- **Provenance:** explicit

Indicator is 1 iff 'Care Provider' appears in the parenthesised role list of the masking string.

---

## Direct effects (1)

### `study_design_info/masking_num`

- **Association:** effect = 0.779 (abs_spearman), n_valid = 81,170
- **Mechanism:** `deterministic`
- **Provenance:** explicit

masking_num is the sum of the four MaskingType-* indicators; this term is one summand.

---

## Associated but no direct causal edge (34)

### `MaskingType-Outcomes Assessor`

- **Association:** effect = 0.656 (abs_spearman), n_valid = 81,170
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `MaskingType-Participant`

- **Association:** effect = 0.638 (abs_spearman), n_valid = 81,170
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `MaskingType-Investigator`

- **Association:** effect = 0.634 (abs_spearman), n_valid = 81,170
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `Placebo Comparator Arm Number`

- **Association:** effect = 0.494 (abs_spearman), n_valid = 77,947
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `study_design_info/intervention_model`

- **Association:** effect = 0.345 (eta), n_valid = 80,702
- **Provenance:** demoted_confounded

`MaskingType-Care Provider` is a deterministic descendant of its single definitional design parent; `study_design_info/intervention_model` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `number_of_arms`

- **Association:** effect = 0.278 (abs_spearman), n_valid = 77,947
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `study_design_info/allocation`

- **Association:** effect = 0.269 (eta), n_valid = 61,818
- **Provenance:** demoted_confounded

`MaskingType-Care Provider` is a deterministic descendant of its single definitional design parent; `study_design_info/allocation` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `enrollment`

- **Association:** effect = 0.187 (abs_spearman), n_valid = 44,289
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `intervention/intervention_name`

- **Association:** effect = 0.171 (abs_spearman), n_valid = 81,170
- **Provenance:** demoted_confounded

`MaskingType-Care Provider` is a deterministic descendant of its single definitional design parent; `intervention/intervention_name` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `Drug intervention Number`

- **Association:** effect = 0.155 (abs_spearman), n_valid = 81,170
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `phase`

- **Association:** effect = 0.151 (eta), n_valid = 81,170
- **Provenance:** demoted_confounded

`MaskingType-Care Provider` is a deterministic descendant of its single definitional design parent; `phase` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `mortality_rate`

- **Association:** effect = 0.131 (abs_spearman), n_valid = 17,890
- **Provenance:** demoted_confounded

`MaskingType-Care Provider` is a deterministic re-encoding / tally of `study_design_info/masking`; its association with `mortality_rate` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `sae_rate`

- **Association:** effect = 0.112 (abs_spearman), n_valid = 17,890
- **Provenance:** demoted_confounded

`MaskingType-Care Provider` is a deterministic re-encoding / tally of `study_design_info/masking`; its association with `sae_rate` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `study_design_info/primary_purpose`

- **Association:** effect = 0.100 (eta), n_valid = 80,406
- **Provenance:** demoted_confounded

`MaskingType-Care Provider` is a deterministic descendant of its single definitional design parent; `study_design_info/primary_purpose` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `location/facility/address/city`

- **Association:** effect = 0.094 (abs_spearman), n_valid = 81,170
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `ipd_info_type-Analytic Code`

- **Association:** effect = 0.087 (abs_spearman), n_valid = 2,297
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `mortality_YN`

- **Association:** effect = 0.086 (abs_spearman), n_valid = 17,890
- **Provenance:** demoted_confounded

`MaskingType-Care Provider` is a deterministic re-encoding / tally of `study_design_info/masking`; its association with `mortality_YN` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `dropout_YN`

- **Association:** effect = 0.085 (abs_spearman), n_valid = 38,218
- **Provenance:** demoted_confounded

`MaskingType-Care Provider` is a deterministic re-encoding / tally of `study_design_info/masking`; its association with `dropout_YN` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `oversight_info/has_dmc`

- **Association:** effect = 0.084 (eta), n_valid = 45,821
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `Active Comparator Arm Number`

- **Association:** effect = 0.081 (abs_spearman), n_valid = 69,142
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `start_date`

- **Association:** effect = 0.076 (abs_spearman), n_valid = 42,635
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `Radiation intervention Number`

- **Association:** effect = 0.075 (abs_spearman), n_valid = 81,170
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `ipd_info_type-Clinical Study Report (CSR)`

- **Association:** effect = 0.074 (abs_spearman), n_valid = 2,145
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `Procedure intervention Number`

- **Association:** effect = 0.072 (abs_spearman), n_valid = 70,854
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `execution_pass`

- **Association:** effect = 0.069 (abs_spearman), n_valid = 52,422
- **Provenance:** demoted_confounded

`MaskingType-Care Provider` is a deterministic re-encoding / tally of `study_design_info/masking`; its association with `execution_pass` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `execution_fail`

- **Association:** effect = 0.069 (abs_spearman), n_valid = 52,422
- **Provenance:** demoted_confounded

`MaskingType-Care Provider` is a deterministic re-encoding / tally of `study_design_info/masking`; its association with `execution_fail` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `intervention_browse/mesh_term`

- **Association:** effect = 0.062 (abs_spearman), n_valid = 81,170
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `Other Arm Number`

- **Association:** effect = 0.060 (abs_spearman), n_valid = 77,947
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `Other intervention Number`

- **Association:** effect = 0.060 (abs_spearman), n_valid = 70,854
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `oversight_info/is_fda_regulated_device`

- **Association:** effect = 0.055 (eta), n_valid = 13,666
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `sponsors/lead_sponsor/agency_class`

- **Association:** effect = 0.055 (eta), n_valid = 70,854
- **Provenance:** demoted_confounded

`MaskingType-Care Provider` is a deterministic descendant of its single definitional design parent; `sponsors/lead_sponsor/agency_class` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `completion_date`

- **Association:** effect = 0.052 (abs_spearman), n_valid = 42,635
- **Provenance:** demoted_confounded

`MaskingType-Care Provider` is a deterministic re-encoding / tally of `study_design_info/masking`; its association with `completion_date` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `No Intervention Arm Number`

- **Association:** effect = 0.052 (abs_spearman), n_valid = 69,142
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `Device intervention Number`

- **Association:** effect = 0.050 (abs_spearman), n_valid = 70,854
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.
