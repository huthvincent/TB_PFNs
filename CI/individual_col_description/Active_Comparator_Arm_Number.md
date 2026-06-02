# Active Comparator Arm Number

- **Group:** `design_derived`
- **Dtype:** float
- **Description:** Count of arms tagged 'Active Comparator'.
- **Associated partners (from `association.md`):** 28
  - Direct **causes** (parents of this feature): **0**
  - Direct **effects** (children of this feature): **1**
  - Associated but **no direct** causal edge: **27**

This per-feature file enumerates only **associated** partners. All other columns in `DAG.json` were ruled independent in the Stage-1 association screen and do not appear here. See `association.md` for the screen.

---

## Direct causes (0)

_(none)_

---

## Direct effects (1)

### `number_of_arms`

- **Association:** effect = 0.278 (abs_spearman), n_valid = 69,293
- **Mechanism:** `deterministic`
- **Provenance:** explicit

number_of_arms is the sum of the six Arm-Number columns; this term is one summand.

---

## Associated but no direct causal edge (27)

### `Experimental Arm Number`

- **Association:** effect = 0.404 (abs_spearman), n_valid = 69,293
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `study_design_info/intervention_model`

- **Association:** effect = 0.338 (eta), n_valid = 69,093
- **Provenance:** demoted_confounded

`Active Comparator Arm Number` is a deterministic descendant of its single definitional design parent; `study_design_info/intervention_model` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `phase`

- **Association:** effect = 0.227 (eta), n_valid = 69,293
- **Provenance:** demoted_confounded

`Active Comparator Arm Number` is a deterministic descendant of its single definitional design parent; `phase` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `enrollment`

- **Association:** effect = 0.222 (abs_spearman), n_valid = 43,117
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `intervention/intervention_name`

- **Association:** effect = 0.220 (abs_spearman), n_valid = 69,293
- **Provenance:** demoted_confounded

`Active Comparator Arm Number` is a deterministic descendant of its single definitional design parent; `intervention/intervention_name` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `intervention_browse/mesh_term`

- **Association:** effect = 0.217 (abs_spearman), n_valid = 69,293
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `study_design_info/masking`

- **Association:** effect = 0.201 (eta), n_valid = 64,055
- **Provenance:** demoted_confounded

`Active Comparator Arm Number` is a deterministic descendant of its single definitional design parent; `study_design_info/masking` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `study_design_info/allocation`

- **Association:** effect = 0.167 (eta), n_valid = 52,870
- **Provenance:** demoted_confounded

`Active Comparator Arm Number` is a deterministic descendant of its single definitional design parent; `study_design_info/allocation` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `Drug intervention Number`

- **Association:** effect = 0.151 (abs_spearman), n_valid = 69,293
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `study_design_info/masking_num`

- **Association:** effect = 0.141 (abs_spearman), n_valid = 69,142
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `smiless`

- **Association:** effect = 0.140 (abs_spearman), n_valid = 69,293
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `responsible_party/responsible_party_type`

- **Association:** effect = 0.120 (eta), n_valid = 66,924
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `MaskingType-Participant`

- **Association:** effect = 0.120 (abs_spearman), n_valid = 69,142
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `sponsors/lead_sponsor/agency_class`

- **Association:** effect = 0.116 (eta), n_valid = 69,293
- **Provenance:** demoted_confounded

`Active Comparator Arm Number` is a deterministic descendant of its single definitional design parent; `sponsors/lead_sponsor/agency_class` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `MaskingType-Outcomes Assessor`

- **Association:** effect = 0.115 (abs_spearman), n_valid = 69,142
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `sae_rate`

- **Association:** effect = 0.111 (abs_spearman), n_valid = 17,886
- **Provenance:** demoted_confounded

`Active Comparator Arm Number` is a deterministic re-encoding / tally of `study_design_info/intervention_model`; its association with `sae_rate` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `MaskingType-Investigator`

- **Association:** effect = 0.096 (abs_spearman), n_valid = 69,142
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `Other Arm Number`

- **Association:** effect = 0.088 (abs_spearman), n_valid = 69,293
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `study_design_info/primary_purpose`

- **Association:** effect = 0.085 (eta), n_valid = 68,722
- **Provenance:** demoted_confounded

`Active Comparator Arm Number` is a deterministic descendant of its single definitional design parent; `study_design_info/primary_purpose` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `MaskingType-Care Provider`

- **Association:** effect = 0.081 (abs_spearman), n_valid = 69,142
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `failure_reason`

- **Association:** effect = 0.071 (eta), n_valid = 10,089
- **Provenance:** demoted_confounded

`Active Comparator Arm Number` is a deterministic re-encoding / tally of `study_design_info/intervention_model`; its association with `failure_reason` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `sae_YN`

- **Association:** effect = 0.069 (abs_spearman), n_valid = 17,886
- **Provenance:** demoted_confounded

`Active Comparator Arm Number` is a deterministic re-encoding / tally of `study_design_info/intervention_model`; its association with `sae_YN` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `brief_title`

- **Association:** effect = 0.064 (abs_spearman), n_valid = 69,293
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `ipd_info_type-Analytic Code`

- **Association:** effect = 0.062 (abs_spearman), n_valid = 2,139
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `dropout_rate`

- **Association:** effect = 0.058 (abs_spearman), n_valid = 38,016
- **Provenance:** demoted_confounded

`Active Comparator Arm Number` is a deterministic re-encoding / tally of `study_design_info/intervention_model`; its association with `dropout_rate` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `Placebo Comparator Arm Number`

- **Association:** effect = 0.054 (abs_spearman), n_valid = 69,293
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `Behavioral intervention Number`

- **Association:** effect = 0.053 (abs_spearman), n_valid = 69,293
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.
