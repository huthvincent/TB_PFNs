# Placebo Comparator Arm Number

- **Group:** `design_derived`
- **Dtype:** float
- **Description:** Count of arms tagged 'Placebo Comparator'.
- **Associated partners (from `association.md`):** 41
  - Direct **causes** (parents of this feature): **0**
  - Direct **effects** (children of this feature): **1**
  - Associated but **no direct** causal edge: **40**

This per-feature file enumerates only **associated** partners. All other columns in `DAG.json` were ruled independent in the Stage-1 association screen and do not appear here. See `association.md` for the screen.

---

## Direct causes (0)

_(none)_

---

## Direct effects (1)

### `number_of_arms`

- **Association:** effect = 0.352 (abs_spearman), n_valid = 78,123
- **Mechanism:** `deterministic`
- **Provenance:** explicit

number_of_arms is the sum of the six Arm-Number columns; this term is one summand.

---

## Associated but no direct causal edge (40)

### `MaskingType-Participant`

- **Association:** effect = 0.687 (abs_spearman), n_valid = 77,947
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `study_design_info/masking_num`

- **Association:** effect = 0.685 (abs_spearman), n_valid = 77,947
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `MaskingType-Investigator`

- **Association:** effect = 0.675 (abs_spearman), n_valid = 77,947
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `study_design_info/masking`

- **Association:** effect = 0.616 (eta), n_valid = 72,860
- **Provenance:** demoted_confounded

`Placebo Comparator Arm Number` is a deterministic descendant of its single definitional design parent; `study_design_info/masking` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `MaskingType-Care Provider`

- **Association:** effect = 0.494 (abs_spearman), n_valid = 77,947
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `MaskingType-Outcomes Assessor`

- **Association:** effect = 0.412 (abs_spearman), n_valid = 77,947
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `study_design_info/intervention_model`

- **Association:** effect = 0.341 (eta), n_valid = 77,887
- **Provenance:** demoted_confounded

`Placebo Comparator Arm Number` is a deterministic descendant of its single definitional design parent; `study_design_info/intervention_model` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `study_design_info/allocation`

- **Association:** effect = 0.261 (eta), n_valid = 59,269
- **Provenance:** demoted_confounded

`Placebo Comparator Arm Number` is a deterministic descendant of its single definitional design parent; `study_design_info/allocation` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `intervention/intervention_name`

- **Association:** effect = 0.213 (abs_spearman), n_valid = 78,123
- **Provenance:** demoted_confounded

`Placebo Comparator Arm Number` is a deterministic descendant of its single definitional design parent; `intervention/intervention_name` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `Drug intervention Number`

- **Association:** effect = 0.208 (abs_spearman), n_valid = 78,123
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `enrollment`

- **Association:** effect = 0.202 (abs_spearman), n_valid = 43,117
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `mortality_rate`

- **Association:** effect = 0.182 (abs_spearman), n_valid = 17,886
- **Provenance:** demoted_confounded

`Placebo Comparator Arm Number` is a deterministic re-encoding / tally of `study_design_info/intervention_model`; its association with `mortality_rate` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `sae_rate`

- **Association:** effect = 0.154 (abs_spearman), n_valid = 17,886
- **Provenance:** demoted_confounded

`Placebo Comparator Arm Number` is a deterministic re-encoding / tally of `study_design_info/intervention_model`; its association with `sae_rate` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `intervention_browse/mesh_term`

- **Association:** effect = 0.142 (abs_spearman), n_valid = 78,123
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `mortality_YN`

- **Association:** effect = 0.137 (abs_spearman), n_valid = 17,886
- **Provenance:** demoted_confounded

`Placebo Comparator Arm Number` is a deterministic re-encoding / tally of `study_design_info/intervention_model`; its association with `mortality_YN` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `Other intervention Number`

- **Association:** effect = 0.114 (abs_spearman), n_valid = 69,293
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `ipd_info_type-Clinical Study Report (CSR)`

- **Association:** effect = 0.114 (abs_spearman), n_valid = 2,139
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `dropout_YN`

- **Association:** effect = 0.114 (abs_spearman), n_valid = 38,016
- **Provenance:** demoted_confounded

`Placebo Comparator Arm Number` is a deterministic re-encoding / tally of `study_design_info/intervention_model`; its association with `dropout_YN` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `sponsors/lead_sponsor/agency_class`

- **Association:** effect = 0.104 (eta), n_valid = 69,293
- **Provenance:** demoted_confounded

`Placebo Comparator Arm Number` is a deterministic descendant of its single definitional design parent; `sponsors/lead_sponsor/agency_class` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `Other Arm Number`

- **Association:** effect = 0.101 (abs_spearman), n_valid = 78,123
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `phase`

- **Association:** effect = 0.094 (eta), n_valid = 78,123
- **Provenance:** demoted_confounded

`Placebo Comparator Arm Number` is a deterministic descendant of its single definitional design parent; `phase` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `No Intervention Arm Number`

- **Association:** effect = 0.093 (abs_spearman), n_valid = 69,293
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `Procedure intervention Number`

- **Association:** effect = 0.091 (abs_spearman), n_valid = 69,293
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `ipd_info_type-Informed Consent Form (ICF)`

- **Association:** effect = 0.090 (abs_spearman), n_valid = 2,139
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `Radiation intervention Number`

- **Association:** effect = 0.087 (abs_spearman), n_valid = 78,123
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `execution_pass`

- **Association:** effect = 0.079 (abs_spearman), n_valid = 50,684
- **Provenance:** demoted_confounded

`Placebo Comparator Arm Number` is a deterministic re-encoding / tally of `study_design_info/intervention_model`; its association with `execution_pass` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `execution_fail`

- **Association:** effect = 0.079 (abs_spearman), n_valid = 50,684
- **Provenance:** demoted_confounded

`Placebo Comparator Arm Number` is a deterministic re-encoding / tally of `study_design_info/intervention_model`; its association with `execution_fail` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `study_design_info/primary_purpose`

- **Association:** effect = 0.077 (eta), n_valid = 77,416
- **Provenance:** demoted_confounded

`Placebo Comparator Arm Number` is a deterministic descendant of its single definitional design parent; `study_design_info/primary_purpose` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `location/facility/address/city`

- **Association:** effect = 0.076 (abs_spearman), n_valid = 78,123
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `Device intervention Number`

- **Association:** effect = 0.072 (abs_spearman), n_valid = 69,293
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `failure_reason`

- **Association:** effect = 0.069 (eta), n_valid = 18,919
- **Provenance:** demoted_confounded

`Placebo Comparator Arm Number` is a deterministic re-encoding / tally of `study_design_info/intervention_model`; its association with `failure_reason` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `oversight_info/is_fda_regulated_device`

- **Association:** effect = 0.065 (eta), n_valid = 13,650
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `Dietary Supplement intervention Number`

- **Association:** effect = 0.060 (abs_spearman), n_valid = 78,123
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `Experimental Arm Number`

- **Association:** effect = 0.059 (abs_spearman), n_valid = 78,123
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `smiless`

- **Association:** effect = 0.057 (abs_spearman), n_valid = 78,123
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `eligibility/minimum_age`

- **Association:** effect = 0.054 (abs_spearman), n_valid = 76,141
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_eligibility'); jointly determined by upstream design_top choices, no direct arrow.

### `Active Comparator Arm Number`

- **Association:** effect = 0.054 (abs_spearman), n_valid = 69,293
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `Biological intervention Number`

- **Association:** effect = 0.053 (abs_spearman), n_valid = 78,123
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `condition`

- **Association:** effect = 0.051 (abs_spearman), n_valid = 78,123
- **Provenance:** demoted_confounded

`Placebo Comparator Arm Number` is a deterministic descendant of its single definitional design parent; `condition` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `oversight_info/is_fda_regulated_drug`

- **Association:** effect = 0.050 (eta), n_valid = 13,735
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.
