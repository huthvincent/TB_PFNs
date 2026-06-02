# icdcode

- **Group:** `design_derived`
- **Dtype:** high_cardinality_text
- **Description:** ICD code(s) tagged from `condition` by an external annotation pipeline.
- **Associated partners (from `association.md`):** 27
  - Direct **causes** (parents of this feature): **1**
  - Direct **effects** (children of this feature): **0**
  - Associated but **no direct** causal edge: **26**

This per-feature file enumerates only **associated** partners. All other columns in `DAG.json` were ruled independent in the Stage-1 association screen and do not appear here. See `association.md` for the screen.

---

## Direct causes (1)

### `condition`

- **Association:** effect = 0.531 (abs_spearman), n_valid = 81,786
- **Mechanism:** `definitional`
- **Provenance:** explicit

ICD codes are tagged from the condition text by an external annotation pipeline.

---

## Direct effects (0)

_(none)_

---

## Associated but no direct causal edge (26)

### `condition_browse/mesh_term`

- **Association:** effect = 0.289 (abs_spearman), n_valid = 81,786
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `sponsors/lead_sponsor/agency_class`

- **Association:** effect = 0.144 (eta), n_valid = 71,221
- **Provenance:** demoted_confounded

`icdcode` is a deterministic descendant of its single definitional design parent; `sponsors/lead_sponsor/agency_class` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `mortality_rate`

- **Association:** effect = 0.123 (abs_spearman), n_valid = 17,916
- **Provenance:** demoted_confounded

`icdcode` is a deterministic re-encoding / tally of `condition`; its association with `mortality_rate` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `eligibility/maximum_age`

- **Association:** effect = 0.113 (abs_spearman), n_valid = 42,760
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_eligibility' and 'design_derived'); jointly determined by upstream design_top choices, no direct arrow.

### `mortality_YN`

- **Association:** effect = 0.105 (abs_spearman), n_valid = 17,916
- **Provenance:** demoted_confounded

`icdcode` is a deterministic re-encoding / tally of `condition`; its association with `mortality_YN` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `duration_day`

- **Association:** effect = 0.103 (abs_spearman), n_valid = 42,855
- **Provenance:** demoted_confounded

`icdcode` is a deterministic re-encoding / tally of `condition`; its association with `duration_day` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `duration_year`

- **Association:** effect = 0.103 (abs_spearman), n_valid = 42,855
- **Provenance:** demoted_confounded

`icdcode` is a deterministic re-encoding / tally of `condition`; its association with `duration_year` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `duration_month`

- **Association:** effect = 0.103 (abs_spearman), n_valid = 42,855
- **Provenance:** demoted_confounded

`icdcode` is a deterministic re-encoding / tally of `condition`; its association with `duration_month` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `intervention_browse/mesh_term`

- **Association:** effect = 0.101 (abs_spearman), n_valid = 81,786
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `smiless`

- **Association:** effect = 0.100 (abs_spearman), n_valid = 81,786
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `Drug intervention Number`

- **Association:** effect = 0.091 (abs_spearman), n_valid = 81,786
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `study_design_info/primary_purpose`

- **Association:** effect = 0.087 (eta), n_valid = 80,983
- **Provenance:** demoted_confounded

`icdcode` is a deterministic descendant of its single definitional design parent; `study_design_info/primary_purpose` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `sae_rate`

- **Association:** effect = 0.086 (abs_spearman), n_valid = 17,916
- **Provenance:** demoted_confounded

`icdcode` is a deterministic re-encoding / tally of `condition`; its association with `sae_rate` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `ipd_info_type-Statistical Analysis Plan (SAP)`

- **Association:** effect = 0.083 (abs_spearman), n_valid = 2,297
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `Other intervention Number`

- **Association:** effect = 0.081 (abs_spearman), n_valid = 71,221
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `intervention/intervention_name`

- **Association:** effect = 0.078 (abs_spearman), n_valid = 81,786
- **Provenance:** demoted_confounded

`icdcode` is a deterministic descendant of its single definitional design parent; `intervention/intervention_name` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `eligibility/healthy_volunteers`

- **Association:** effect = 0.074 (eta), n_valid = 81,613
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_eligibility' and 'design_derived'); jointly determined by upstream design_top choices, no direct arrow.

### `ipd_info_type-Clinical Study Report (CSR)`

- **Association:** effect = 0.072 (abs_spearman), n_valid = 2,145
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `start_date`

- **Association:** effect = 0.070 (abs_spearman), n_valid = 42,855
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `study_design_info/masking`

- **Association:** effect = 0.063 (eta), n_valid = 75,043
- **Provenance:** demoted_confounded

`icdcode` is a deterministic descendant of its single definitional design parent; `study_design_info/masking` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `study_design_info/intervention_model`

- **Association:** effect = 0.061 (eta), n_valid = 80,897
- **Provenance:** demoted_confounded

`icdcode` is a deterministic descendant of its single definitional design parent; `study_design_info/intervention_model` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `patient_data/sharing_ipd`

- **Association:** effect = 0.059 (eta), n_valid = 13,510
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `phase`

- **Association:** effect = 0.054 (eta), n_valid = 81,786
- **Provenance:** demoted_confounded

`icdcode` is a deterministic descendant of its single definitional design parent; `phase` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `Radiation intervention Number`

- **Association:** effect = 0.052 (abs_spearman), n_valid = 81,786
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `Procedure intervention Number`

- **Association:** effect = 0.051 (abs_spearman), n_valid = 71,221
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `oversight_info/has_dmc`

- **Association:** effect = 0.051 (eta), n_valid = 45,926
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.
