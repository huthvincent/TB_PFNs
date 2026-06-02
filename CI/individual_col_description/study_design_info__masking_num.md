# study_design_info/masking_num

- **Group:** `design_derived`
- **Dtype:** float (0-4)
- **Description:** Count of masked roles; equals the sum of the four MaskingType-* indicators.
- **Associated partners (from `association.md`):** 42
  - Direct **causes** (parents of this feature): **5**
  - Direct **effects** (children of this feature): **0**
  - Associated but **no direct** causal edge: **37**

This per-feature file enumerates only **associated** partners. All other columns in `DAG.json` were ruled independent in the Stage-1 association screen and do not appear here. See `association.md` for the screen.

---

## Direct causes (5)

### `study_design_info/masking`

- **Association:** effect = 1.000 (eta), n_valid = 75,043
- **Mechanism:** `deterministic`
- **Provenance:** explicit

masking_num is the count of masked roles encoded in the masking string.

### `MaskingType-Participant`

- **Association:** effect = 0.915 (abs_spearman), n_valid = 81,170
- **Mechanism:** `deterministic`
- **Provenance:** explicit

masking_num is the sum of the four MaskingType-* indicators; this term is one summand.

### `MaskingType-Investigator`

- **Association:** effect = 0.892 (abs_spearman), n_valid = 81,170
- **Mechanism:** `deterministic`
- **Provenance:** explicit

masking_num is the sum of the four MaskingType-* indicators; this term is one summand.

### `MaskingType-Care Provider`

- **Association:** effect = 0.779 (abs_spearman), n_valid = 81,170
- **Mechanism:** `deterministic`
- **Provenance:** explicit

masking_num is the sum of the four MaskingType-* indicators; this term is one summand.

### `MaskingType-Outcomes Assessor`

- **Association:** effect = 0.748 (abs_spearman), n_valid = 81,170
- **Mechanism:** `deterministic`
- **Provenance:** explicit

masking_num is the sum of the four MaskingType-* indicators; this term is one summand.

---

## Direct effects (0)

_(none)_

---

## Associated but no direct causal edge (37)

### `Placebo Comparator Arm Number`

- **Association:** effect = 0.685 (abs_spearman), n_valid = 77,947
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `study_design_info/intervention_model`

- **Association:** effect = 0.508 (eta), n_valid = 80,702
- **Provenance:** demoted_confounded

`study_design_info/masking_num` is a deterministic descendant of its single definitional design parent; `study_design_info/intervention_model` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `number_of_arms`

- **Association:** effect = 0.446 (abs_spearman), n_valid = 77,947
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `study_design_info/allocation`

- **Association:** effect = 0.430 (eta), n_valid = 61,818
- **Provenance:** demoted_confounded

`study_design_info/masking_num` is a deterministic descendant of its single definitional design parent; `study_design_info/allocation` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `enrollment`

- **Association:** effect = 0.303 (abs_spearman), n_valid = 44,289
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_planning' and 'design_derived'); jointly determined by upstream design_top choices, no direct arrow.

### `intervention/intervention_name`

- **Association:** effect = 0.265 (abs_spearman), n_valid = 81,170
- **Provenance:** demoted_confounded

`study_design_info/masking_num` is a deterministic descendant of its single definitional design parent; `intervention/intervention_name` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `Drug intervention Number`

- **Association:** effect = 0.224 (abs_spearman), n_valid = 81,170
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `mortality_rate`

- **Association:** effect = 0.221 (abs_spearman), n_valid = 17,890
- **Provenance:** demoted_confounded

`study_design_info/masking_num` is a deterministic re-encoding / tally of `study_design_info/masking`; its association with `mortality_rate` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `sae_rate`

- **Association:** effect = 0.209 (abs_spearman), n_valid = 17,890
- **Provenance:** demoted_confounded

`study_design_info/masking_num` is a deterministic re-encoding / tally of `study_design_info/masking`; its association with `sae_rate` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `phase`

- **Association:** effect = 0.205 (eta), n_valid = 81,170
- **Provenance:** demoted_confounded

`study_design_info/masking_num` is a deterministic descendant of its single definitional design parent; `phase` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `mortality_YN`

- **Association:** effect = 0.155 (abs_spearman), n_valid = 17,890
- **Provenance:** demoted_confounded

`study_design_info/masking_num` is a deterministic re-encoding / tally of `study_design_info/masking`; its association with `mortality_YN` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `Active Comparator Arm Number`

- **Association:** effect = 0.141 (abs_spearman), n_valid = 69,142
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `dropout_YN`

- **Association:** effect = 0.129 (abs_spearman), n_valid = 38,218
- **Provenance:** demoted_confounded

`study_design_info/masking_num` is a deterministic re-encoding / tally of `study_design_info/masking`; its association with `dropout_YN` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `ipd_info_type-Clinical Study Report (CSR)`

- **Association:** effect = 0.128 (abs_spearman), n_valid = 2,145
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_oversight' and 'design_derived'); jointly determined by upstream design_top choices, no direct arrow.

### `study_design_info/primary_purpose`

- **Association:** effect = 0.121 (eta), n_valid = 80,406
- **Provenance:** demoted_confounded

`study_design_info/masking_num` is a deterministic descendant of its single definitional design parent; `study_design_info/primary_purpose` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `sponsors/lead_sponsor/agency_class`

- **Association:** effect = 0.118 (eta), n_valid = 70,854
- **Provenance:** demoted_confounded

`study_design_info/masking_num` is a deterministic descendant of its single definitional design parent; `sponsors/lead_sponsor/agency_class` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `Radiation intervention Number`

- **Association:** effect = 0.118 (abs_spearman), n_valid = 81,170
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `execution_pass`

- **Association:** effect = 0.099 (abs_spearman), n_valid = 52,422
- **Provenance:** demoted_confounded

`study_design_info/masking_num` is a deterministic re-encoding / tally of `study_design_info/masking`; its association with `execution_pass` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `execution_fail`

- **Association:** effect = 0.099 (abs_spearman), n_valid = 52,422
- **Provenance:** demoted_confounded

`study_design_info/masking_num` is a deterministic re-encoding / tally of `study_design_info/masking`; its association with `execution_fail` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `location/facility/address/city`

- **Association:** effect = 0.094 (abs_spearman), n_valid = 81,170
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_planning' and 'design_derived'); jointly determined by upstream design_top choices, no direct arrow.

### `Procedure intervention Number`

- **Association:** effect = 0.090 (abs_spearman), n_valid = 70,854
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `intervention_browse/mesh_term`

- **Association:** effect = 0.089 (abs_spearman), n_valid = 81,170
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `Other intervention Number`

- **Association:** effect = 0.088 (abs_spearman), n_valid = 70,854
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `duration_month`

- **Association:** effect = 0.086 (abs_spearman), n_valid = 42,635
- **Provenance:** demoted_confounded

`study_design_info/masking_num` is a deterministic re-encoding / tally of `study_design_info/masking`; its association with `duration_month` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `duration_day`

- **Association:** effect = 0.086 (abs_spearman), n_valid = 42,635
- **Provenance:** demoted_confounded

`study_design_info/masking_num` is a deterministic re-encoding / tally of `study_design_info/masking`; its association with `duration_day` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `duration_year`

- **Association:** effect = 0.086 (abs_spearman), n_valid = 42,635
- **Provenance:** demoted_confounded

`study_design_info/masking_num` is a deterministic re-encoding / tally of `study_design_info/masking`; its association with `duration_year` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `start_date`

- **Association:** effect = 0.076 (abs_spearman), n_valid = 42,635
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_planning' and 'design_derived'); jointly determined by upstream design_top choices, no direct arrow.

### `Other Arm Number`

- **Association:** effect = 0.076 (abs_spearman), n_valid = 77,947
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `approval_outcome`

- **Association:** effect = 0.074 (abs_spearman), n_valid = 30,351
- **Provenance:** demoted_confounded

`study_design_info/masking_num` is a deterministic re-encoding / tally of `study_design_info/masking`; its association with `approval_outcome` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `failure_reason`

- **Association:** effect = 0.069 (eta), n_valid = 20,495
- **Provenance:** demoted_confounded

`study_design_info/masking_num` is a deterministic re-encoding / tally of `study_design_info/masking`; its association with `failure_reason` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `Sham Comparator Arm Number`

- **Association:** effect = 0.064 (abs_spearman), n_valid = 69,142
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `oversight_info/is_fda_regulated_device`

- **Association:** effect = 0.060 (eta), n_valid = 13,666
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_oversight' and 'design_derived'); jointly determined by upstream design_top choices, no direct arrow.

### `oversight_info/has_dmc`

- **Association:** effect = 0.060 (eta), n_valid = 45,821
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_oversight' and 'design_derived'); jointly determined by upstream design_top choices, no direct arrow.

### `ipd_info_type-Analytic Code`

- **Association:** effect = 0.059 (abs_spearman), n_valid = 2,297
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_oversight' and 'design_derived'); jointly determined by upstream design_top choices, no direct arrow.

### `No Intervention Arm Number`

- **Association:** effect = 0.057 (abs_spearman), n_valid = 69,142
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `eligibility/minimum_age`

- **Association:** effect = 0.055 (abs_spearman), n_valid = 79,096
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_eligibility' and 'design_derived'); jointly determined by upstream design_top choices, no direct arrow.

### `eligibility/gender`

- **Association:** effect = 0.055 (eta), n_valid = 70,854
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_eligibility' and 'design_derived'); jointly determined by upstream design_top choices, no direct arrow.
