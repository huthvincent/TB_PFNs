# Biological intervention Number

- **Group:** `design_derived`
- **Dtype:** float
- **Description:** Count of interventions tagged 'Biological'.
- **Associated partners (from `association.md`):** 26
  - Direct **causes** (parents of this feature): **0**
  - Direct **effects** (children of this feature): **0**
  - Associated but **no direct** causal edge: **26**

This per-feature file enumerates only **associated** partners. All other columns in `DAG.json` were ruled independent in the Stage-1 association screen and do not appear here. See `association.md` for the screen.

---

## Direct causes (0)

_(none)_

---

## Direct effects (0)

_(none)_

---

## Associated but no direct causal edge (26)

### `Drug intervention Number`

- **Association:** effect = 0.386 (abs_spearman), n_valid = 81,786
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `study_design_info/primary_purpose`

- **Association:** effect = 0.330 (eta), n_valid = 80,983
- **Provenance:** demoted_confounded

`Biological intervention Number` is a deterministic descendant of its single definitional design parent; `study_design_info/primary_purpose` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `ipd_info_type-Informed Consent Form (ICF)`

- **Association:** effect = 0.244 (abs_spearman), n_valid = 2,145
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `smiless`

- **Association:** effect = 0.197 (abs_spearman), n_valid = 81,786
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `patient_data/sharing_ipd`

- **Association:** effect = 0.187 (eta), n_valid = 13,510
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `eligibility/healthy_volunteers`

- **Association:** effect = 0.172 (eta), n_valid = 81,613
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_eligibility'); jointly determined by upstream design_top choices, no direct arrow.

### `eligibility/maximum_age`

- **Association:** effect = 0.136 (abs_spearman), n_valid = 42,760
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_eligibility'); jointly determined by upstream design_top choices, no direct arrow.

### `sae_YN`

- **Association:** effect = 0.132 (abs_spearman), n_valid = 17,916
- **Provenance:** demoted_confounded

`Biological intervention Number` is a deterministic re-encoding / tally of `intervention/intervention_type`; its association with `sae_YN` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `sae_rate`

- **Association:** effect = 0.105 (abs_spearman), n_valid = 17,916
- **Provenance:** demoted_confounded

`Biological intervention Number` is a deterministic re-encoding / tally of `intervention/intervention_type`; its association with `sae_rate` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `sponsors/lead_sponsor/agency_class`

- **Association:** effect = 0.102 (eta), n_valid = 71,221
- **Provenance:** demoted_confounded

`Biological intervention Number` is a deterministic descendant of its single definitional design parent; `sponsors/lead_sponsor/agency_class` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `eligibility/minimum_age`

- **Association:** effect = 0.099 (abs_spearman), n_valid = 79,650
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_eligibility'); jointly determined by upstream design_top choices, no direct arrow.

### `Experimental Arm Number`

- **Association:** effect = 0.094 (abs_spearman), n_valid = 78,123
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `study_design_info/intervention_model`

- **Association:** effect = 0.088 (eta), n_valid = 80,897
- **Provenance:** demoted_confounded

`Biological intervention Number` is a deterministic descendant of its single definitional design parent; `study_design_info/intervention_model` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `responsible_party/responsible_party_type`

- **Association:** effect = 0.083 (eta), n_valid = 67,878
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `mortality_rate`

- **Association:** effect = 0.083 (abs_spearman), n_valid = 17,916
- **Provenance:** demoted_confounded

`Biological intervention Number` is a deterministic re-encoding / tally of `intervention/intervention_type`; its association with `mortality_rate` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `approval_outcome`

- **Association:** effect = 0.081 (abs_spearman), n_valid = 30,683
- **Provenance:** demoted_confounded

`Biological intervention Number` is a deterministic re-encoding / tally of `intervention/intervention_type`; its association with `approval_outcome` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `mortality_YN`

- **Association:** effect = 0.080 (abs_spearman), n_valid = 17,916
- **Provenance:** demoted_confounded

`Biological intervention Number` is a deterministic re-encoding / tally of `intervention/intervention_type`; its association with `mortality_YN` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `ipd_info_type-Analytic Code`

- **Association:** effect = 0.079 (abs_spearman), n_valid = 2,297
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `phase`

- **Association:** effect = 0.076 (eta), n_valid = 81,786
- **Provenance:** demoted_confounded

`Biological intervention Number` is a deterministic descendant of its single definitional design parent; `phase` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `intervention/intervention_name`

- **Association:** effect = 0.074 (abs_spearman), n_valid = 81,786
- **Provenance:** demoted_confounded

`Biological intervention Number` is a deterministic descendant of its single definitional design parent; `intervention/intervention_name` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `Other intervention Number`

- **Association:** effect = 0.073 (abs_spearman), n_valid = 71,221
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `enrollment`

- **Association:** effect = 0.072 (abs_spearman), n_valid = 44,446
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `brief_title`

- **Association:** effect = 0.065 (abs_spearman), n_valid = 81,786
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `intervention_browse/mesh_term`

- **Association:** effect = 0.062 (abs_spearman), n_valid = 81,786
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `oversight_info/has_dmc`

- **Association:** effect = 0.054 (eta), n_valid = 45,926
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `Placebo Comparator Arm Number`

- **Association:** effect = 0.053 (abs_spearman), n_valid = 78,123
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.
