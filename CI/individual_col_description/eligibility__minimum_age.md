# eligibility/minimum_age

- **Group:** `design_eligibility`
- **Dtype:** numeric (years, parsed)
- **Description:** Lower age bound parsed to years.
- **Associated partners (from `association.md`):** 16
  - Direct **causes** (parents of this feature): **0**
  - Direct **effects** (children of this feature): **1**
  - Associated but **no direct** causal edge: **15**

This per-feature file enumerates only **associated** partners. All other columns in `DAG.json` were ruled independent in the Stage-1 association screen and do not appear here. See `association.md` for the screen.

---

## Direct causes (0)

_(none)_

---

## Direct effects (1)

### `mortality_YN`

- **Association:** effect = 0.058 (abs_spearman), n_valid = 17,440
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Downstream-design field (eligibility/minimum_age) shifts the realised safety outcome (mortality_YN) through population biology or trial operations.

---

## Associated but no direct causal edge (15)

### `eligibility/maximum_age`

- **Association:** effect = 0.465 (abs_spearman), n_valid = 41,854
- **Provenance:** default_within_tier

Both in group 'design_eligibility' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `Biological intervention Number`

- **Association:** effect = 0.099 (abs_spearman), n_valid = 79,650
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_eligibility'); jointly determined by upstream design_top choices, no direct arrow.

### `study_design_info/masking`

- **Association:** effect = 0.095 (eta), n_valid = 73,073
- **Provenance:** demoted_confounded

`study_design_info/masking` has no concrete causal mechanism that sets `eligibility/minimum_age`. Trial size, eligible population, calendar start date, site geography and the free-text title are not directly caused by `study_design_info/masking`; the association is a jointly-chosen-design / sponsor-footprint / secular-trend confound. (R9: spurious design->planning/eligibility.)

### `ipd_info_type-Informed Consent Form (ICF)`

- **Association:** effect = 0.082 (abs_spearman), n_valid = 2,103
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_eligibility' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `duration_year`

- **Association:** effect = 0.077 (abs_spearman), n_valid = 41,982
- **Provenance:** demoted_confounded

`eligibility/minimum_age` affects the trial timeline only through `enrollment` / `study_design_info/intervention_model`, the direct parents of trial duration; the marginal association with `duration_year` is mediated, not direct. (R5: mediated design->timing.)

### `duration_day`

- **Association:** effect = 0.077 (abs_spearman), n_valid = 41,982
- **Provenance:** demoted_confounded

`eligibility/minimum_age` affects the trial timeline only through `enrollment` / `study_design_info/intervention_model`, the direct parents of trial duration; the marginal association with `duration_day` is mediated, not direct. (R5: mediated design->timing.)

### `duration_month`

- **Association:** effect = 0.077 (abs_spearman), n_valid = 41,982
- **Provenance:** demoted_confounded

`eligibility/minimum_age` affects the trial timeline only through `enrollment` / `study_design_info/intervention_model`, the direct parents of trial duration; the marginal association with `duration_month` is mediated, not direct. (R5: mediated design->timing.)

### `MaskingType-Participant`

- **Association:** effect = 0.064 (abs_spearman), n_valid = 79,096
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_eligibility'); jointly determined by upstream design_top choices, no direct arrow.

### `study_design_info/intervention_model`

- **Association:** effect = 0.061 (eta), n_valid = 78,839
- **Provenance:** demoted_confounded

`study_design_info/intervention_model` has no concrete causal mechanism that sets `eligibility/minimum_age`. Trial size, eligible population, calendar start date, site geography and the free-text title are not directly caused by `study_design_info/intervention_model`; the association is a jointly-chosen-design / sponsor-footprint / secular-trend confound. (R9: spurious design->planning/eligibility.)

### `eligibility/gender`

- **Association:** effect = 0.060 (eta), n_valid = 69,489
- **Provenance:** default_within_tier

Both in group 'design_eligibility' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `Drug intervention Number`

- **Association:** effect = 0.059 (abs_spearman), n_valid = 79,650
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_eligibility'); jointly determined by upstream design_top choices, no direct arrow.

### `study_design_info/masking_num`

- **Association:** effect = 0.055 (abs_spearman), n_valid = 79,096
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_eligibility' and 'design_derived'); jointly determined by upstream design_top choices, no direct arrow.

### `Placebo Comparator Arm Number`

- **Association:** effect = 0.054 (abs_spearman), n_valid = 76,141
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_eligibility'); jointly determined by upstream design_top choices, no direct arrow.

### `study_design_info/allocation`

- **Association:** effect = 0.054 (eta), n_valid = 60,725
- **Provenance:** demoted_confounded

`study_design_info/allocation` has no concrete causal mechanism that sets `eligibility/minimum_age`. Trial size, eligible population, calendar start date, site geography and the free-text title are not directly caused by `study_design_info/allocation`; the association is a jointly-chosen-design / sponsor-footprint / secular-trend confound. (R9: spurious design->planning/eligibility.)

### `MaskingType-Investigator`

- **Association:** effect = 0.052 (abs_spearman), n_valid = 79,096
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_eligibility'); jointly determined by upstream design_top choices, no direct arrow.
