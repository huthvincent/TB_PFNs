# eligibility/maximum_age

- **Group:** `design_eligibility`
- **Dtype:** numeric (years, parsed)
- **Description:** Upper age bound parsed to years from strings like '65 Years' / '6 Months' / 'N/A'.
- **Associated partners (from `association.md`):** 31
  - Direct **causes** (parents of this feature): **0**
  - Direct **effects** (children of this feature): **6**
  - Associated but **no direct** causal edge: **25**

This per-feature file enumerates only **associated** partners. All other columns in `DAG.json` were ruled independent in the Stage-1 association screen and do not appear here. See `association.md` for the screen.

---

## Direct causes (0)

_(none)_

---

## Direct effects (6)

### `mortality_rate`

- **Association:** effect = 0.253 (abs_spearman), n_valid = 8,723
- **Mechanism:** `biological`
- **Provenance:** explicit

Older eligibility envelopes raise background mortality.

### `mortality_YN`

- **Association:** effect = 0.242 (abs_spearman), n_valid = 8,723
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Downstream-design field (eligibility/maximum_age) shifts the realised safety outcome (mortality_YN) through population biology or trial operations.

### `sae_rate`

- **Association:** effect = 0.178 (abs_spearman), n_valid = 8,723
- **Mechanism:** `biological`
- **Provenance:** explicit

Older eligibility envelopes admit more comorbid participants and elevate background SAE rate.

### `sae_YN`

- **Association:** effect = 0.123 (abs_spearman), n_valid = 8,723
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Downstream-design field (eligibility/maximum_age) shifts the realised safety outcome (sae_YN) through population biology or trial operations.

### `dropout_rate`

- **Association:** effect = 0.110 (abs_spearman), n_valid = 18,312
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Downstream-design field (eligibility/maximum_age) shifts the realised safety outcome (dropout_rate) through population biology or trial operations.

### `dropout_YN`

- **Association:** effect = 0.053 (abs_spearman), n_valid = 18,312
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Downstream-design field (eligibility/maximum_age) shifts the realised safety outcome (dropout_YN) through population biology or trial operations.

---

## Associated but no direct causal edge (25)

### `eligibility/minimum_age`

- **Association:** effect = 0.465 (abs_spearman), n_valid = 41,854
- **Provenance:** default_within_tier

Both in group 'design_eligibility' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `ipd_info_type-Informed Consent Form (ICF)`

- **Association:** effect = 0.297 (abs_spearman), n_valid = 1,034
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_eligibility' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `ipd_info_type-Clinical Study Report (CSR)`

- **Association:** effect = 0.280 (abs_spearman), n_valid = 1,034
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_eligibility' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `study_design_info/primary_purpose`

- **Association:** effect = 0.233 (eta), n_valid = 42,342
- **Provenance:** demoted_confounded

`study_design_info/primary_purpose` has no concrete causal mechanism that sets `eligibility/maximum_age`. Trial size, eligible population, calendar start date, site geography and the free-text title are not directly caused by `study_design_info/primary_purpose`; the association is a jointly-chosen-design / sponsor-footprint / secular-trend confound. (R9: spurious design->planning/eligibility.)

### `eligibility/healthy_volunteers`

- **Association:** effect = 0.224 (eta), n_valid = 42,674
- **Provenance:** default_within_tier

Both in group 'design_eligibility' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `duration_day`

- **Association:** effect = 0.202 (abs_spearman), n_valid = 24,161
- **Provenance:** demoted_confounded

`eligibility/maximum_age` affects the trial timeline only through `enrollment` / `study_design_info/intervention_model`, the direct parents of trial duration; the marginal association with `duration_day` is mediated, not direct. (R5: mediated design->timing.)

### `duration_year`

- **Association:** effect = 0.202 (abs_spearman), n_valid = 24,161
- **Provenance:** demoted_confounded

`eligibility/maximum_age` affects the trial timeline only through `enrollment` / `study_design_info/intervention_model`, the direct parents of trial duration; the marginal association with `duration_year` is mediated, not direct. (R5: mediated design->timing.)

### `duration_month`

- **Association:** effect = 0.202 (abs_spearman), n_valid = 24,161
- **Provenance:** demoted_confounded

`eligibility/maximum_age` affects the trial timeline only through `enrollment` / `study_design_info/intervention_model`, the direct parents of trial duration; the marginal association with `duration_month` is mediated, not direct. (R5: mediated design->timing.)

### `condition_browse/mesh_term`

- **Association:** effect = 0.148 (abs_spearman), n_valid = 42,760
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_eligibility'); jointly determined by upstream design_top choices, no direct arrow.

### `Biological intervention Number`

- **Association:** effect = 0.136 (abs_spearman), n_valid = 42,760
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_eligibility'); jointly determined by upstream design_top choices, no direct arrow.

### `patient_data/sharing_ipd`

- **Association:** effect = 0.129 (eta), n_valid = 6,857
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_eligibility' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `phase`

- **Association:** effect = 0.124 (eta), n_valid = 42,760
- **Provenance:** demoted_confounded

`phase` has no concrete causal mechanism that sets `eligibility/maximum_age`. Trial size, eligible population, calendar start date, site geography and the free-text title are not directly caused by `phase`; the association is a jointly-chosen-design / sponsor-footprint / secular-trend confound. (R9: spurious design->planning/eligibility.)

### `icdcode`

- **Association:** effect = 0.113 (abs_spearman), n_valid = 42,760
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_eligibility' and 'design_derived'); jointly determined by upstream design_top choices, no direct arrow.

### `study_design_info/masking`

- **Association:** effect = 0.072 (eta), n_valid = 39,233
- **Provenance:** demoted_confounded

`study_design_info/masking` has no concrete causal mechanism that sets `eligibility/maximum_age`. Trial size, eligible population, calendar start date, site geography and the free-text title are not directly caused by `study_design_info/masking`; the association is a jointly-chosen-design / sponsor-footprint / secular-trend confound. (R9: spurious design->planning/eligibility.)

### `Drug intervention Number`

- **Association:** effect = 0.070 (abs_spearman), n_valid = 42,760
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_eligibility'); jointly determined by upstream design_top choices, no direct arrow.

### `eligibility/gender`

- **Association:** effect = 0.068 (eta), n_valid = 37,908
- **Provenance:** default_within_tier

Both in group 'design_eligibility' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `approval_outcome`

- **Association:** effect = 0.067 (abs_spearman), n_valid = 13,782
- **Provenance:** demoted_confounded

`eligibility/maximum_age` reaches the trial-success label `approval_outcome` only through biology / efficacy and enrollment mediators already in the DAG (`biology_pass`, `failure_reason`, `enrollment`); no direct arrow. (R6: mediated design->label.)

### `location/facility/address/city`

- **Association:** effect = 0.062 (abs_spearman), n_valid = 42,760
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_eligibility' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `number_of_arms`

- **Association:** effect = 0.061 (abs_spearman), n_valid = 41,114
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_eligibility' and 'design_derived'); jointly determined by upstream design_top choices, no direct arrow.

### `Radiation intervention Number`

- **Association:** effect = 0.060 (abs_spearman), n_valid = 42,760
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_eligibility'); jointly determined by upstream design_top choices, no direct arrow.

### `Experimental Arm Number`

- **Association:** effect = 0.054 (abs_spearman), n_valid = 41,114
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_eligibility'); jointly determined by upstream design_top choices, no direct arrow.

### `intervention/intervention_type`

- **Association:** effect = 0.054 (abs_spearman), n_valid = 42,760
- **Provenance:** demoted_confounded

`intervention/intervention_type` has no concrete causal mechanism that sets `eligibility/maximum_age`. Trial size, eligible population, calendar start date, site geography and the free-text title are not directly caused by `intervention/intervention_type`; the association is a jointly-chosen-design / sponsor-footprint / secular-trend confound. (R9: spurious design->planning/eligibility.)

### `start_date`

- **Association:** effect = 0.053 (abs_spearman), n_valid = 24,161
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_eligibility' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `Procedure intervention Number`

- **Association:** effect = 0.052 (abs_spearman), n_valid = 37,908
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_eligibility'); jointly determined by upstream design_top choices, no direct arrow.

### `study_design_info/intervention_model`

- **Association:** effect = 0.051 (eta), n_valid = 42,360
- **Provenance:** demoted_confounded

`study_design_info/intervention_model` has no concrete causal mechanism that sets `eligibility/maximum_age`. Trial size, eligible population, calendar start date, site geography and the free-text title are not directly caused by `study_design_info/intervention_model`; the association is a jointly-chosen-design / sponsor-footprint / secular-trend confound. (R9: spurious design->planning/eligibility.)
