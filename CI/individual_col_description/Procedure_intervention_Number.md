# Procedure intervention Number

- **Group:** `design_derived`
- **Dtype:** float
- **Description:** Count of interventions tagged 'Procedure'.
- **Associated partners (from `association.md`):** 37
  - Direct **causes** (parents of this feature): **0**
  - Direct **effects** (children of this feature): **0**
  - Associated but **no direct** causal edge: **37**

This per-feature file enumerates only **associated** partners. All other columns in `DAG.json` were ruled independent in the Stage-1 association screen and do not appear here. See `association.md` for the screen.

---

## Direct causes (0)

_(none)_

---

## Direct effects (0)

_(none)_

---

## Associated but no direct causal edge (37)

### `Radiation intervention Number`

- **Association:** effect = 0.211 (abs_spearman), n_valid = 71,221
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `intervention/intervention_name`

- **Association:** effect = 0.163 (abs_spearman), n_valid = 71,221
- **Provenance:** demoted_confounded

`Procedure intervention Number` is a deterministic descendant of its single definitional design parent; `intervention/intervention_name` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `sponsors/lead_sponsor/agency_class`

- **Association:** effect = 0.149 (eta), n_valid = 71,221
- **Provenance:** demoted_confounded

`Procedure intervention Number` is a deterministic descendant of its single definitional design parent; `sponsors/lead_sponsor/agency_class` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `duration_month`

- **Association:** effect = 0.104 (abs_spearman), n_valid = 42,855
- **Provenance:** demoted_confounded

`Procedure intervention Number` is a deterministic re-encoding / tally of `intervention/intervention_type`; its association with `duration_month` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `MaskingType-Investigator`

- **Association:** effect = 0.104 (abs_spearman), n_valid = 70,854
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `duration_year`

- **Association:** effect = 0.104 (abs_spearman), n_valid = 42,855
- **Provenance:** demoted_confounded

`Procedure intervention Number` is a deterministic re-encoding / tally of `intervention/intervention_type`; its association with `duration_year` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `duration_day`

- **Association:** effect = 0.104 (abs_spearman), n_valid = 42,855
- **Provenance:** demoted_confounded

`Procedure intervention Number` is a deterministic re-encoding / tally of `intervention/intervention_type`; its association with `duration_day` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `study_design_info/masking`

- **Association:** effect = 0.101 (eta), n_valid = 64,727
- **Provenance:** demoted_confounded

`Procedure intervention Number` is a deterministic descendant of its single definitional design parent; `study_design_info/masking` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `mortality_rate`

- **Association:** effect = 0.092 (abs_spearman), n_valid = 17,916
- **Provenance:** demoted_confounded

`Procedure intervention Number` is a deterministic re-encoding / tally of `intervention/intervention_type`; its association with `mortality_rate` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `Placebo Comparator Arm Number`

- **Association:** effect = 0.091 (abs_spearman), n_valid = 69,293
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `study_design_info/masking_num`

- **Association:** effect = 0.090 (abs_spearman), n_valid = 70,854
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `ipd_info_type-Statistical Analysis Plan (SAP)`

- **Association:** effect = 0.085 (abs_spearman), n_valid = 2,145
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `MaskingType-Participant`

- **Association:** effect = 0.085 (abs_spearman), n_valid = 70,854
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `approval_outcome`

- **Association:** effect = 0.080 (abs_spearman), n_valid = 24,108
- **Provenance:** demoted_confounded

`Procedure intervention Number` is a deterministic re-encoding / tally of `intervention/intervention_type`; its association with `approval_outcome` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `start_date`

- **Association:** effect = 0.078 (abs_spearman), n_valid = 42,855
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `failure_reason`

- **Association:** effect = 0.077 (eta), n_valid = 10,204
- **Provenance:** demoted_confounded

`Procedure intervention Number` is a deterministic re-encoding / tally of `intervention/intervention_type`; its association with `failure_reason` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `ipd_info_type-Clinical Study Report (CSR)`

- **Association:** effect = 0.076 (abs_spearman), n_valid = 2,145
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `ipd_info_type-Informed Consent Form (ICF)`

- **Association:** effect = 0.075 (abs_spearman), n_valid = 2,145
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `mortality_YN`

- **Association:** effect = 0.073 (abs_spearman), n_valid = 17,916
- **Provenance:** demoted_confounded

`Procedure intervention Number` is a deterministic re-encoding / tally of `intervention/intervention_type`; its association with `mortality_YN` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `condition`

- **Association:** effect = 0.073 (abs_spearman), n_valid = 71,221
- **Provenance:** demoted_confounded

`Procedure intervention Number` is a deterministic descendant of its single definitional design parent; `condition` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `MaskingType-Care Provider`

- **Association:** effect = 0.072 (abs_spearman), n_valid = 70,854
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `number_of_arms`

- **Association:** effect = 0.070 (abs_spearman), n_valid = 69,293
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `Genetic intervention Number`

- **Association:** effect = 0.069 (abs_spearman), n_valid = 71,221
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `enrollment`

- **Association:** effect = 0.067 (abs_spearman), n_valid = 44,446
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `study_design_info/primary_purpose`

- **Association:** effect = 0.067 (eta), n_valid = 70,604
- **Provenance:** demoted_confounded

`Procedure intervention Number` is a deterministic descendant of its single definitional design parent; `study_design_info/primary_purpose` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `patient_data/sharing_ipd`

- **Association:** effect = 0.062 (eta), n_valid = 13,510
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `study_design_info/intervention_model`

- **Association:** effect = 0.060 (eta), n_valid = 70,749
- **Provenance:** demoted_confounded

`Procedure intervention Number` is a deterministic descendant of its single definitional design parent; `study_design_info/intervention_model` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `responsible_party/responsible_party_type`

- **Association:** effect = 0.056 (eta), n_valid = 67,878
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `oversight_info/has_dmc`

- **Association:** effect = 0.056 (eta), n_valid = 37,612
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `Sham Comparator Arm Number`

- **Association:** effect = 0.055 (abs_spearman), n_valid = 69,293
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `Other intervention Number`

- **Association:** effect = 0.055 (abs_spearman), n_valid = 71,221
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `phase`

- **Association:** effect = 0.054 (eta), n_valid = 71,221
- **Provenance:** demoted_confounded

`Procedure intervention Number` is a deterministic descendant of its single definitional design parent; `phase` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `dropout_YN`

- **Association:** effect = 0.053 (abs_spearman), n_valid = 38,302
- **Provenance:** demoted_confounded

`Procedure intervention Number` is a deterministic re-encoding / tally of `intervention/intervention_type`; its association with `dropout_YN` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `eligibility/maximum_age`

- **Association:** effect = 0.052 (abs_spearman), n_valid = 37,908
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_eligibility'); jointly determined by upstream design_top choices, no direct arrow.

### `icdcode`

- **Association:** effect = 0.051 (abs_spearman), n_valid = 71,221
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `Experimental Arm Number`

- **Association:** effect = 0.051 (abs_spearman), n_valid = 69,293
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `eligibility/healthy_volunteers`

- **Association:** effect = 0.051 (eta), n_valid = 71,109
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_eligibility'); jointly determined by upstream design_top choices, no direct arrow.
