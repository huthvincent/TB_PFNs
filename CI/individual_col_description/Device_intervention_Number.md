# Device intervention Number

- **Group:** `design_derived`
- **Dtype:** float
- **Description:** Count of interventions tagged 'Device'.
- **Associated partners (from `association.md`):** 18
  - Direct **causes** (parents of this feature): **0**
  - Direct **effects** (children of this feature): **0**
  - Associated but **no direct** causal edge: **18**

This per-feature file enumerates only **associated** partners. All other columns in `DAG.json` were ruled independent in the Stage-1 association screen and do not appear here. See `association.md` for the screen.

---

## Direct causes (0)

_(none)_

---

## Direct effects (0)

_(none)_

---

## Associated but no direct causal edge (18)

### `oversight_info/is_fda_regulated_device`

- **Association:** effect = 0.637 (eta), n_valid = 11,258
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `Drug intervention Number`

- **Association:** effect = 0.180 (abs_spearman), n_valid = 71,221
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `study_design_info/masking`

- **Association:** effect = 0.132 (eta), n_valid = 64,727
- **Provenance:** demoted_confounded

`Device intervention Number` is a deterministic descendant of its single definitional design parent; `study_design_info/masking` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `Sham Comparator Arm Number`

- **Association:** effect = 0.118 (abs_spearman), n_valid = 69,293
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `oversight_info/is_fda_regulated_drug`

- **Association:** effect = 0.116 (eta), n_valid = 11,339
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `smiless`

- **Association:** effect = 0.098 (abs_spearman), n_valid = 71,221
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `intervention_browse/mesh_term`

- **Association:** effect = 0.094 (abs_spearman), n_valid = 71,221
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `study_design_info/primary_purpose`

- **Association:** effect = 0.087 (eta), n_valid = 70,604
- **Provenance:** demoted_confounded

`Device intervention Number` is a deterministic descendant of its single definitional design parent; `study_design_info/primary_purpose` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `phase`

- **Association:** effect = 0.078 (eta), n_valid = 71,221
- **Provenance:** demoted_confounded

`Device intervention Number` is a deterministic descendant of its single definitional design parent; `phase` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `MaskingType-Investigator`

- **Association:** effect = 0.076 (abs_spearman), n_valid = 70,854
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `Placebo Comparator Arm Number`

- **Association:** effect = 0.072 (abs_spearman), n_valid = 69,293
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `sae_YN`

- **Association:** effect = 0.064 (abs_spearman), n_valid = 17,916
- **Provenance:** demoted_confounded

`Device intervention Number` is a deterministic re-encoding / tally of `intervention/intervention_type`; its association with `sae_YN` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `failure_reason`

- **Association:** effect = 0.060 (eta), n_valid = 10,204
- **Provenance:** demoted_confounded

`Device intervention Number` is a deterministic re-encoding / tally of `intervention/intervention_type`; its association with `failure_reason` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `Experimental Arm Number`

- **Association:** effect = 0.060 (abs_spearman), n_valid = 69,293
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `patient_data/sharing_ipd`

- **Association:** effect = 0.056 (eta), n_valid = 13,510
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `sponsors/lead_sponsor/agency_class`

- **Association:** effect = 0.055 (eta), n_valid = 71,221
- **Provenance:** demoted_confounded

`Device intervention Number` is a deterministic descendant of its single definitional design parent; `sponsors/lead_sponsor/agency_class` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `sae_rate`

- **Association:** effect = 0.053 (abs_spearman), n_valid = 17,916
- **Provenance:** demoted_confounded

`Device intervention Number` is a deterministic re-encoding / tally of `intervention/intervention_type`; its association with `sae_rate` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `MaskingType-Care Provider`

- **Association:** effect = 0.050 (abs_spearman), n_valid = 70,854
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.
