# Combination Product intervention Number

- **Group:** `design_derived`
- **Dtype:** float
- **Description:** Count of interventions tagged 'Combination Product'.
- **Associated partners (from `association.md`):** 4
  - Direct **causes** (parents of this feature): **0**
  - Direct **effects** (children of this feature): **0**
  - Associated but **no direct** causal edge: **4**

This per-feature file enumerates only **associated** partners. All other columns in `DAG.json` were ruled independent in the Stage-1 association screen and do not appear here. See `association.md` for the screen.

---

## Direct causes (0)

_(none)_

---

## Direct effects (0)

_(none)_

---

## Associated but no direct causal edge (4)

### `oversight_info/is_fda_regulated_device`

- **Association:** effect = 0.182 (eta), n_valid = 13,676
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `Drug intervention Number`

- **Association:** effect = 0.097 (abs_spearman), n_valid = 81,786
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `start_date`

- **Association:** effect = 0.065 (abs_spearman), n_valid = 42,855
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `completion_date`

- **Association:** effect = 0.054 (abs_spearman), n_valid = 42,855
- **Provenance:** demoted_confounded

`Combination Product intervention Number` is a deterministic re-encoding / tally of `intervention/intervention_type`; its association with `completion_date` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)
