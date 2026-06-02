# Drug intervention Number

- **Group:** `design_derived`
- **Dtype:** float
- **Description:** Count of interventions tagged 'Drug'.
- **Associated partners (from `association.md`):** 48
  - Direct **causes** (parents of this feature): **1**
  - Direct **effects** (children of this feature): **0**
  - Associated but **no direct** causal edge: **47**

This per-feature file enumerates only **associated** partners. All other columns in `DAG.json` were ruled independent in the Stage-1 association screen and do not appear here. See `association.md` for the screen.

---

## Direct causes (1)

### `intervention/intervention_type`

- **Association:** effect = 0.061 (abs_spearman), n_valid = 81,786
- **Mechanism:** `deterministic`
- **Provenance:** explicit

Per-type intervention count is a tally over intervention_type's multi-valued list.

---

## Direct effects (0)

_(none)_

---

## Associated but no direct causal edge (47)

### `intervention/intervention_name`

- **Association:** effect = 0.668 (abs_spearman), n_valid = 81,786
- **Provenance:** demoted_confounded

`Drug intervention Number` is a deterministic descendant of its single definitional design parent; `intervention/intervention_name` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `smiless`

- **Association:** effect = 0.510 (abs_spearman), n_valid = 81,786
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `intervention_browse/mesh_term`

- **Association:** effect = 0.442 (abs_spearman), n_valid = 81,786
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `Biological intervention Number`

- **Association:** effect = 0.386 (abs_spearman), n_valid = 81,786
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `number_of_arms`

- **Association:** effect = 0.323 (abs_spearman), n_valid = 78,123
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `MaskingType-Investigator`

- **Association:** effect = 0.250 (abs_spearman), n_valid = 81,170
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `MaskingType-Participant`

- **Association:** effect = 0.235 (abs_spearman), n_valid = 81,170
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `study_design_info/masking_num`

- **Association:** effect = 0.224 (abs_spearman), n_valid = 81,170
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `Placebo Comparator Arm Number`

- **Association:** effect = 0.208 (abs_spearman), n_valid = 78,123
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `study_design_info/intervention_model`

- **Association:** effect = 0.200 (eta), n_valid = 80,897
- **Provenance:** demoted_confounded

`Drug intervention Number` is a deterministic descendant of its single definitional design parent; `study_design_info/intervention_model` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `Device intervention Number`

- **Association:** effect = 0.180 (abs_spearman), n_valid = 71,221
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `study_design_info/primary_purpose`

- **Association:** effect = 0.179 (eta), n_valid = 80,983
- **Provenance:** demoted_confounded

`Drug intervention Number` is a deterministic descendant of its single definitional design parent; `study_design_info/primary_purpose` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `study_design_info/masking`

- **Association:** effect = 0.178 (eta), n_valid = 75,043
- **Provenance:** demoted_confounded

`Drug intervention Number` is a deterministic descendant of its single definitional design parent; `study_design_info/masking` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `ipd_info_type-Informed Consent Form (ICF)`

- **Association:** effect = 0.171 (abs_spearman), n_valid = 2,145
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `Other intervention Number`

- **Association:** effect = 0.156 (abs_spearman), n_valid = 71,221
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `MaskingType-Care Provider`

- **Association:** effect = 0.155 (abs_spearman), n_valid = 81,170
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `Active Comparator Arm Number`

- **Association:** effect = 0.151 (abs_spearman), n_valid = 69,293
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `Experimental Arm Number`

- **Association:** effect = 0.151 (abs_spearman), n_valid = 78,123
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `enrollment`

- **Association:** effect = 0.145 (abs_spearman), n_valid = 44,446
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `No Intervention Arm Number`

- **Association:** effect = 0.122 (abs_spearman), n_valid = 69,293
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `MaskingType-Outcomes Assessor`

- **Association:** effect = 0.113 (abs_spearman), n_valid = 81,170
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `location/facility/address/city`

- **Association:** effect = 0.112 (abs_spearman), n_valid = 81,786
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `Dietary Supplement intervention Number`

- **Association:** effect = 0.107 (abs_spearman), n_valid = 81,786
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `oversight_info/is_fda_regulated_drug`

- **Association:** effect = 0.103 (eta), n_valid = 13,761
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `oversight_info/is_fda_regulated_device`

- **Association:** effect = 0.097 (eta), n_valid = 13,676
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `Combination Product intervention Number`

- **Association:** effect = 0.097 (abs_spearman), n_valid = 81,786
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `icdcode`

- **Association:** effect = 0.091 (abs_spearman), n_valid = 81,786
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `sponsors/lead_sponsor/agency_class`

- **Association:** effect = 0.089 (eta), n_valid = 71,221
- **Provenance:** demoted_confounded

`Drug intervention Number` is a deterministic descendant of its single definitional design parent; `sponsors/lead_sponsor/agency_class` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `study_design_info/allocation`

- **Association:** effect = 0.088 (eta), n_valid = 62,081
- **Provenance:** demoted_confounded

`Drug intervention Number` is a deterministic descendant of its single definitional design parent; `study_design_info/allocation` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `Behavioral intervention Number`

- **Association:** effect = 0.083 (abs_spearman), n_valid = 81,786
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `execution_pass`

- **Association:** effect = 0.075 (abs_spearman), n_valid = 52,772
- **Provenance:** demoted_confounded

`Drug intervention Number` is a deterministic re-encoding / tally of `intervention/intervention_type`; its association with `execution_pass` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `execution_fail`

- **Association:** effect = 0.075 (abs_spearman), n_valid = 52,772
- **Provenance:** demoted_confounded

`Drug intervention Number` is a deterministic re-encoding / tally of `intervention/intervention_type`; its association with `execution_fail` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `eligibility/maximum_age`

- **Association:** effect = 0.070 (abs_spearman), n_valid = 42,760
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_eligibility'); jointly determined by upstream design_top choices, no direct arrow.

### `responsible_party/responsible_party_type`

- **Association:** effect = 0.067 (eta), n_valid = 67,878
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `patient_data/sharing_ipd`

- **Association:** effect = 0.066 (eta), n_valid = 13,510
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `Other Arm Number`

- **Association:** effect = 0.065 (abs_spearman), n_valid = 78,123
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `failure_reason`

- **Association:** effect = 0.065 (eta), n_valid = 20,769
- **Provenance:** demoted_confounded

`Drug intervention Number` is a deterministic re-encoding / tally of `intervention/intervention_type`; its association with `failure_reason` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `brief_title`

- **Association:** effect = 0.064 (abs_spearman), n_valid = 81,786
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `ipd_info_type-Statistical Analysis Plan (SAP)`

- **Association:** effect = 0.062 (abs_spearman), n_valid = 2,297
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `mortality_YN`

- **Association:** effect = 0.060 (abs_spearman), n_valid = 17,916
- **Provenance:** demoted_confounded

`Drug intervention Number` is a deterministic re-encoding / tally of `intervention/intervention_type`; its association with `mortality_YN` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `eligibility/minimum_age`

- **Association:** effect = 0.059 (abs_spearman), n_valid = 79,650
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_eligibility'); jointly determined by upstream design_top choices, no direct arrow.

### `eligibility/healthy_volunteers`

- **Association:** effect = 0.059 (eta), n_valid = 81,613
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_eligibility'); jointly determined by upstream design_top choices, no direct arrow.

### `phase`

- **Association:** effect = 0.058 (eta), n_valid = 81,786
- **Provenance:** demoted_confounded

`Drug intervention Number` is a deterministic descendant of its single definitional design parent; `phase` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `mortality_rate`

- **Association:** effect = 0.058 (abs_spearman), n_valid = 17,916
- **Provenance:** demoted_confounded

`Drug intervention Number` is a deterministic re-encoding / tally of `intervention/intervention_type`; its association with `mortality_rate` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `approval_outcome`

- **Association:** effect = 0.056 (abs_spearman), n_valid = 30,683
- **Provenance:** demoted_confounded

`Drug intervention Number` is a deterministic re-encoding / tally of `intervention/intervention_type`; its association with `approval_outcome` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `Sham Comparator Arm Number`

- **Association:** effect = 0.052 (abs_spearman), n_valid = 69,293
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `dropout_YN`

- **Association:** effect = 0.052 (abs_spearman), n_valid = 38,302
- **Provenance:** demoted_confounded

`Drug intervention Number` is a deterministic re-encoding / tally of `intervention/intervention_type`; its association with `dropout_YN` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)
