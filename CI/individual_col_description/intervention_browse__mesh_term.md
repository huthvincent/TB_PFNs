# intervention_browse/mesh_term

- **Group:** `design_derived`
- **Dtype:** high_cardinality_text
- **Description:** MeSH-normalized term(s) for the intervention name.
- **Associated partners (from `association.md`):** 41
  - Direct **causes** (parents of this feature): **1**
  - Direct **effects** (children of this feature): **0**
  - Associated but **no direct** causal edge: **40**

This per-feature file enumerates only **associated** partners. All other columns in `DAG.json` were ruled independent in the Stage-1 association screen and do not appear here. See `association.md` for the screen.

---

## Direct causes (1)

### `intervention/intervention_name`

- **Association:** effect = 0.394 (abs_spearman), n_valid = 81,786
- **Mechanism:** `definitional`
- **Provenance:** explicit

intervention_browse/mesh_term is the MeSH-vocabulary normalisation of the free-text intervention name.

---

## Direct effects (0)

_(none)_

---

## Associated but no direct causal edge (40)

### `smiless`

- **Association:** effect = 0.550 (abs_spearman), n_valid = 81,786
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `Drug intervention Number`

- **Association:** effect = 0.442 (abs_spearman), n_valid = 81,786
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `Active Comparator Arm Number`

- **Association:** effect = 0.217 (abs_spearman), n_valid = 69,293
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `sponsors/lead_sponsor/agency_class`

- **Association:** effect = 0.174 (eta), n_valid = 71,221
- **Provenance:** demoted_confounded

`intervention_browse/mesh_term` is a deterministic descendant of its single definitional design parent; `sponsors/lead_sponsor/agency_class` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `mortality_rate`

- **Association:** effect = 0.166 (abs_spearman), n_valid = 17,916
- **Provenance:** demoted_confounded

`intervention_browse/mesh_term` is a deterministic re-encoding / tally of `intervention/intervention_name`; its association with `mortality_rate` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `ipd_info_type-Clinical Study Report (CSR)`

- **Association:** effect = 0.165 (abs_spearman), n_valid = 2,145
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `start_date`

- **Association:** effect = 0.164 (abs_spearman), n_valid = 42,855
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `Placebo Comparator Arm Number`

- **Association:** effect = 0.142 (abs_spearman), n_valid = 78,123
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `mortality_YN`

- **Association:** effect = 0.138 (abs_spearman), n_valid = 17,916
- **Provenance:** demoted_confounded

`intervention_browse/mesh_term` is a deterministic re-encoding / tally of `intervention/intervention_name`; its association with `mortality_YN` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `duration_month`

- **Association:** effect = 0.134 (abs_spearman), n_valid = 42,855
- **Provenance:** demoted_confounded

`intervention_browse/mesh_term` is a deterministic re-encoding / tally of `intervention/intervention_name`; its association with `duration_month` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `duration_day`

- **Association:** effect = 0.133 (abs_spearman), n_valid = 42,855
- **Provenance:** demoted_confounded

`intervention_browse/mesh_term` is a deterministic re-encoding / tally of `intervention/intervention_name`; its association with `duration_day` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `duration_year`

- **Association:** effect = 0.133 (abs_spearman), n_valid = 42,855
- **Provenance:** demoted_confounded

`intervention_browse/mesh_term` is a deterministic re-encoding / tally of `intervention/intervention_name`; its association with `duration_year` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `phase`

- **Association:** effect = 0.123 (eta), n_valid = 81,786
- **Provenance:** demoted_confounded

`intervention_browse/mesh_term` is a deterministic descendant of its single definitional design parent; `phase` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `ipd_info_type-Informed Consent Form (ICF)`

- **Association:** effect = 0.117 (abs_spearman), n_valid = 2,145
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `eligibility/healthy_volunteers`

- **Association:** effect = 0.115 (eta), n_valid = 81,613
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_eligibility' and 'design_derived'); jointly determined by upstream design_top choices, no direct arrow.

### `completion_date`

- **Association:** effect = 0.112 (abs_spearman), n_valid = 42,855
- **Provenance:** demoted_confounded

`intervention_browse/mesh_term` is a deterministic re-encoding / tally of `intervention/intervention_name`; its association with `completion_date` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `study_design_info/masking`

- **Association:** effect = 0.110 (eta), n_valid = 75,043
- **Provenance:** demoted_confounded

`intervention_browse/mesh_term` is a deterministic descendant of its single definitional design parent; `study_design_info/masking` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `icdcode`

- **Association:** effect = 0.101 (abs_spearman), n_valid = 81,786
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `sae_rate`

- **Association:** effect = 0.098 (abs_spearman), n_valid = 17,916
- **Provenance:** demoted_confounded

`intervention_browse/mesh_term` is a deterministic re-encoding / tally of `intervention/intervention_name`; its association with `sae_rate` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `Device intervention Number`

- **Association:** effect = 0.094 (abs_spearman), n_valid = 71,221
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `MaskingType-Participant`

- **Association:** effect = 0.094 (abs_spearman), n_valid = 81,170
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `study_design_info/primary_purpose`

- **Association:** effect = 0.094 (eta), n_valid = 80,983
- **Provenance:** demoted_confounded

`intervention_browse/mesh_term` is a deterministic descendant of its single definitional design parent; `study_design_info/primary_purpose` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `study_design_info/masking_num`

- **Association:** effect = 0.089 (abs_spearman), n_valid = 81,170
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `MaskingType-Investigator`

- **Association:** effect = 0.083 (abs_spearman), n_valid = 81,170
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `failure_reason`

- **Association:** effect = 0.079 (eta), n_valid = 20,769
- **Provenance:** demoted_confounded

`intervention_browse/mesh_term` is a deterministic re-encoding / tally of `intervention/intervention_name`; its association with `failure_reason` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `execution_pass`

- **Association:** effect = 0.077 (abs_spearman), n_valid = 52,772
- **Provenance:** demoted_confounded

`intervention_browse/mesh_term` is a deterministic re-encoding / tally of `intervention/intervention_name`; its association with `execution_pass` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `execution_fail`

- **Association:** effect = 0.077 (abs_spearman), n_valid = 52,772
- **Provenance:** demoted_confounded

`intervention_browse/mesh_term` is a deterministic re-encoding / tally of `intervention/intervention_name`; its association with `execution_fail` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `oversight_info/is_fda_regulated_drug`

- **Association:** effect = 0.074 (eta), n_valid = 13,761
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `study_design_info/intervention_model`

- **Association:** effect = 0.073 (eta), n_valid = 80,897
- **Provenance:** demoted_confounded

`intervention_browse/mesh_term` is a deterministic descendant of its single definitional design parent; `study_design_info/intervention_model` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `ipd_info_type-Statistical Analysis Plan (SAP)`

- **Association:** effect = 0.069 (abs_spearman), n_valid = 2,297
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `Radiation intervention Number`

- **Association:** effect = 0.068 (abs_spearman), n_valid = 81,786
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `condition`

- **Association:** effect = 0.065 (abs_spearman), n_valid = 81,786
- **Provenance:** demoted_confounded

`intervention_browse/mesh_term` is a deterministic descendant of its single definitional design parent; `condition` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `Biological intervention Number`

- **Association:** effect = 0.062 (abs_spearman), n_valid = 81,786
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `MaskingType-Care Provider`

- **Association:** effect = 0.062 (abs_spearman), n_valid = 81,170
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `eligibility/gender`

- **Association:** effect = 0.061 (eta), n_valid = 71,221
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_eligibility' and 'design_derived'); jointly determined by upstream design_top choices, no direct arrow.

### `MaskingType-Outcomes Assessor`

- **Association:** effect = 0.056 (abs_spearman), n_valid = 81,170
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `condition_browse/mesh_term`

- **Association:** effect = 0.054 (abs_spearman), n_valid = 81,786
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `enrollment`

- **Association:** effect = 0.052 (abs_spearman), n_valid = 44,446
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_planning' and 'design_derived'); jointly determined by upstream design_top choices, no direct arrow.

### `responsible_party/responsible_party_type`

- **Association:** effect = 0.051 (eta), n_valid = 67,878
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `Experimental Arm Number`

- **Association:** effect = 0.051 (abs_spearman), n_valid = 78,123
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.
