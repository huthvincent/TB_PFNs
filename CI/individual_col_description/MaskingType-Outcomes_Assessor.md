# MaskingType-Outcomes Assessor

- **Group:** `design_derived`
- **Dtype:** indicator (0/1)
- **Description:** Outcomes assessor is masked.
- **Associated partners (from `association.md`):** 33
  - Direct **causes** (parents of this feature): **1**
  - Direct **effects** (children of this feature): **1**
  - Associated but **no direct** causal edge: **31**

This per-feature file enumerates only **associated** partners. All other columns in `DAG.json` were ruled independent in the Stage-1 association screen and do not appear here. See `association.md` for the screen.

---

## Direct causes (1)

### `study_design_info/masking`

- **Association:** effect = 1.000 (eta), n_valid = 75,043
- **Mechanism:** `deterministic`
- **Provenance:** explicit

Indicator is 1 iff 'Outcomes Assessor' appears in the parenthesised role list of the masking string.

---

## Direct effects (1)

### `study_design_info/masking_num`

- **Association:** effect = 0.748 (abs_spearman), n_valid = 81,170
- **Mechanism:** `deterministic`
- **Provenance:** explicit

masking_num is the sum of the four MaskingType-* indicators; this term is one summand.

---

## Associated but no direct causal edge (31)

### `MaskingType-Care Provider`

- **Association:** effect = 0.656 (abs_spearman), n_valid = 81,170
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `MaskingType-Participant`

- **Association:** effect = 0.554 (abs_spearman), n_valid = 81,170
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `MaskingType-Investigator`

- **Association:** effect = 0.547 (abs_spearman), n_valid = 81,170
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `Placebo Comparator Arm Number`

- **Association:** effect = 0.412 (abs_spearman), n_valid = 77,947
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `study_design_info/intervention_model`

- **Association:** effect = 0.352 (eta), n_valid = 80,702
- **Provenance:** demoted_confounded

`MaskingType-Outcomes Assessor` is a deterministic descendant of its single definitional design parent; `study_design_info/intervention_model` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `number_of_arms`

- **Association:** effect = 0.277 (abs_spearman), n_valid = 77,947
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `study_design_info/allocation`

- **Association:** effect = 0.268 (eta), n_valid = 61,818
- **Provenance:** demoted_confounded

`MaskingType-Outcomes Assessor` is a deterministic descendant of its single definitional design parent; `study_design_info/allocation` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `enrollment`

- **Association:** effect = 0.196 (abs_spearman), n_valid = 44,289
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `intervention/intervention_name`

- **Association:** effect = 0.165 (abs_spearman), n_valid = 81,170
- **Provenance:** demoted_confounded

`MaskingType-Outcomes Assessor` is a deterministic descendant of its single definitional design parent; `intervention/intervention_name` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `phase`

- **Association:** effect = 0.159 (eta), n_valid = 81,170
- **Provenance:** demoted_confounded

`MaskingType-Outcomes Assessor` is a deterministic descendant of its single definitional design parent; `phase` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `sae_rate`

- **Association:** effect = 0.144 (abs_spearman), n_valid = 17,890
- **Provenance:** demoted_confounded

`MaskingType-Outcomes Assessor` is a deterministic re-encoding / tally of `study_design_info/masking`; its association with `sae_rate` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `mortality_rate`

- **Association:** effect = 0.142 (abs_spearman), n_valid = 17,890
- **Provenance:** demoted_confounded

`MaskingType-Outcomes Assessor` is a deterministic re-encoding / tally of `study_design_info/masking`; its association with `mortality_rate` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `Active Comparator Arm Number`

- **Association:** effect = 0.115 (abs_spearman), n_valid = 69,142
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `Drug intervention Number`

- **Association:** effect = 0.113 (abs_spearman), n_valid = 81,170
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `study_design_info/primary_purpose`

- **Association:** effect = 0.097 (eta), n_valid = 80,406
- **Provenance:** demoted_confounded

`MaskingType-Outcomes Assessor` is a deterministic descendant of its single definitional design parent; `study_design_info/primary_purpose` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `mortality_YN`

- **Association:** effect = 0.096 (abs_spearman), n_valid = 17,890
- **Provenance:** demoted_confounded

`MaskingType-Outcomes Assessor` is a deterministic re-encoding / tally of `study_design_info/masking`; its association with `mortality_YN` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `dropout_YN`

- **Association:** effect = 0.084 (abs_spearman), n_valid = 38,218
- **Provenance:** demoted_confounded

`MaskingType-Outcomes Assessor` is a deterministic re-encoding / tally of `study_design_info/masking`; its association with `dropout_YN` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `location/facility/address/city`

- **Association:** effect = 0.077 (abs_spearman), n_valid = 81,170
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `Radiation intervention Number`

- **Association:** effect = 0.077 (abs_spearman), n_valid = 81,170
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `start_date`

- **Association:** effect = 0.075 (abs_spearman), n_valid = 42,635
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `execution_fail`

- **Association:** effect = 0.073 (abs_spearman), n_valid = 52,422
- **Provenance:** demoted_confounded

`MaskingType-Outcomes Assessor` is a deterministic re-encoding / tally of `study_design_info/masking`; its association with `execution_fail` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `execution_pass`

- **Association:** effect = 0.073 (abs_spearman), n_valid = 52,422
- **Provenance:** demoted_confounded

`MaskingType-Outcomes Assessor` is a deterministic re-encoding / tally of `study_design_info/masking`; its association with `execution_pass` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `Sham Comparator Arm Number`

- **Association:** effect = 0.071 (abs_spearman), n_valid = 69,142
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `sponsors/lead_sponsor/agency_class`

- **Association:** effect = 0.062 (eta), n_valid = 70,854
- **Provenance:** demoted_confounded

`MaskingType-Outcomes Assessor` is a deterministic descendant of its single definitional design parent; `sponsors/lead_sponsor/agency_class` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `oversight_info/has_dmc`

- **Association:** effect = 0.060 (eta), n_valid = 45,821
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `ipd_info_type-Analytic Code`

- **Association:** effect = 0.059 (abs_spearman), n_valid = 2,297
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `Other intervention Number`

- **Association:** effect = 0.058 (abs_spearman), n_valid = 70,854
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `intervention_browse/mesh_term`

- **Association:** effect = 0.056 (abs_spearman), n_valid = 81,170
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `responsible_party/responsible_party_type`

- **Association:** effect = 0.054 (eta), n_valid = 67,639
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `eligibility/gender`

- **Association:** effect = 0.052 (eta), n_valid = 70,854
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_eligibility'); jointly determined by upstream design_top choices, no direct arrow.

### `completion_date`

- **Association:** effect = 0.051 (abs_spearman), n_valid = 42,635
- **Provenance:** demoted_confounded

`MaskingType-Outcomes Assessor` is a deterministic re-encoding / tally of `study_design_info/masking`; its association with `completion_date` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)
