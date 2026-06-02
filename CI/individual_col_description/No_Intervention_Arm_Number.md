# No Intervention Arm Number

- **Group:** `design_derived`
- **Dtype:** float
- **Description:** Count of arms tagged 'No Intervention'.
- **Associated partners (from `association.md`):** 22
  - Direct **causes** (parents of this feature): **0**
  - Direct **effects** (children of this feature): **1**
  - Associated but **no direct** causal edge: **21**

This per-feature file enumerates only **associated** partners. All other columns in `DAG.json` were ruled independent in the Stage-1 association screen and do not appear here. See `association.md` for the screen.

---

## Direct causes (0)

_(none)_

---

## Direct effects (1)

### `number_of_arms`

- **Association:** effect = 0.057 (abs_spearman), n_valid = 69,293
- **Mechanism:** `deterministic`
- **Provenance:** explicit

number_of_arms is the sum of the six Arm-Number columns; this term is one summand.

---

## Associated but no direct causal edge (21)

### `intervention/intervention_name`

- **Association:** effect = 0.148 (abs_spearman), n_valid = 69,293
- **Provenance:** demoted_confounded

`No Intervention Arm Number` is a deterministic descendant of its single definitional design parent; `intervention/intervention_name` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `sponsors/lead_sponsor/agency_class`

- **Association:** effect = 0.137 (eta), n_valid = 69,293
- **Provenance:** demoted_confounded

`No Intervention Arm Number` is a deterministic descendant of its single definitional design parent; `sponsors/lead_sponsor/agency_class` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `study_design_info/masking`

- **Association:** effect = 0.134 (eta), n_valid = 64,055
- **Provenance:** demoted_confounded

`No Intervention Arm Number` is a deterministic descendant of its single definitional design parent; `study_design_info/masking` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `Drug intervention Number`

- **Association:** effect = 0.122 (abs_spearman), n_valid = 69,293
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `responsible_party/responsible_party_type`

- **Association:** effect = 0.113 (eta), n_valid = 66,924
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `study_design_info/intervention_model`

- **Association:** effect = 0.099 (eta), n_valid = 69,093
- **Provenance:** demoted_confounded

`No Intervention Arm Number` is a deterministic descendant of its single definitional design parent; `study_design_info/intervention_model` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `Placebo Comparator Arm Number`

- **Association:** effect = 0.093 (abs_spearman), n_valid = 69,293
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `phase`

- **Association:** effect = 0.090 (eta), n_valid = 69,293
- **Provenance:** demoted_confounded

`No Intervention Arm Number` is a deterministic descendant of its single definitional design parent; `phase` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `MaskingType-Investigator`

- **Association:** effect = 0.079 (abs_spearman), n_valid = 69,142
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `study_design_info/primary_purpose`

- **Association:** effect = 0.078 (eta), n_valid = 68,722
- **Provenance:** demoted_confounded

`No Intervention Arm Number` is a deterministic descendant of its single definitional design parent; `study_design_info/primary_purpose` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `Experimental Arm Number`

- **Association:** effect = 0.073 (abs_spearman), n_valid = 69,293
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `MaskingType-Participant`

- **Association:** effect = 0.073 (abs_spearman), n_valid = 69,142
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `Behavioral intervention Number`

- **Association:** effect = 0.070 (abs_spearman), n_valid = 69,293
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `sae_rate`

- **Association:** effect = 0.069 (abs_spearman), n_valid = 17,886
- **Provenance:** demoted_confounded

`No Intervention Arm Number` is a deterministic re-encoding / tally of `study_design_info/intervention_model`; its association with `sae_rate` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `sae_YN`

- **Association:** effect = 0.068 (abs_spearman), n_valid = 17,886
- **Provenance:** demoted_confounded

`No Intervention Arm Number` is a deterministic re-encoding / tally of `study_design_info/intervention_model`; its association with `sae_YN` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `approval_outcome`

- **Association:** effect = 0.066 (abs_spearman), n_valid = 22,770
- **Provenance:** demoted_confounded

`No Intervention Arm Number` is a deterministic re-encoding / tally of `study_design_info/intervention_model`; its association with `approval_outcome` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `location/facility/address/city`

- **Association:** effect = 0.063 (abs_spearman), n_valid = 69,293
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `ipd_info_type-Statistical Analysis Plan (SAP)`

- **Association:** effect = 0.060 (abs_spearman), n_valid = 2,139
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `patient_data/sharing_ipd`

- **Association:** effect = 0.058 (eta), n_valid = 13,438
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `study_design_info/masking_num`

- **Association:** effect = 0.057 (abs_spearman), n_valid = 69,142
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `MaskingType-Care Provider`

- **Association:** effect = 0.052 (abs_spearman), n_valid = 69,142
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.
