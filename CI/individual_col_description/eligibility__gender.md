# eligibility/gender

- **Group:** `design_eligibility`
- **Dtype:** categorical
- **Description:** Eligible sex / gender: All / Male / Female.
- **Associated partners (from `association.md`):** 24
  - Direct **causes** (parents of this feature): **0**
  - Direct **effects** (children of this feature): **4**
  - Associated but **no direct** causal edge: **20**

This per-feature file enumerates only **associated** partners. All other columns in `DAG.json` were ruled independent in the Stage-1 association screen and do not appear here. See `association.md` for the screen.

---

## Direct causes (0)

_(none)_

---

## Direct effects (4)

### `sae_YN`

- **Association:** effect = 0.088 (eta), n_valid = 17,916
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Downstream-design field (eligibility/gender) shifts the realised safety outcome (sae_YN) through population biology or trial operations.

### `sae_rate`

- **Association:** effect = 0.078 (eta), n_valid = 17,916
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Downstream-design field (eligibility/gender) shifts the realised safety outcome (sae_rate) through population biology or trial operations.

### `mortality_YN`

- **Association:** effect = 0.072 (eta), n_valid = 17,916
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Downstream-design field (eligibility/gender) shifts the realised safety outcome (mortality_YN) through population biology or trial operations.

### `dropout_YN`

- **Association:** effect = 0.062 (eta), n_valid = 38,302
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Downstream-design field (eligibility/gender) shifts the realised safety outcome (dropout_YN) through population biology or trial operations.

---

## Associated but no direct causal edge (20)

### `eligibility/healthy_volunteers`

- **Association:** effect = 0.170 (cramers_v), n_valid = 71,109
- **Provenance:** default_within_tier

Both in group 'design_eligibility' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `phase`

- **Association:** effect = 0.128 (cramers_v), n_valid = 71,221
- **Provenance:** demoted_confounded

`phase` has no concrete causal mechanism that sets `eligibility/gender`. Trial size, eligible population, calendar start date, site geography and the free-text title are not directly caused by `phase`; the association is a jointly-chosen-design / sponsor-footprint / secular-trend confound. (R9: spurious design->planning/eligibility.)

### `condition_browse/mesh_term`

- **Association:** effect = 0.123 (eta), n_valid = 71,221
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_eligibility'); jointly determined by upstream design_top choices, no direct arrow.

### `duration_month`

- **Association:** effect = 0.104 (eta), n_valid = 42,855
- **Provenance:** demoted_confounded

`eligibility/gender` affects the trial timeline only through `enrollment` / `study_design_info/intervention_model`, the direct parents of trial duration; the marginal association with `duration_month` is mediated, not direct. (R5: mediated design->timing.)

### `duration_day`

- **Association:** effect = 0.104 (eta), n_valid = 42,855
- **Provenance:** demoted_confounded

`eligibility/gender` affects the trial timeline only through `enrollment` / `study_design_info/intervention_model`, the direct parents of trial duration; the marginal association with `duration_day` is mediated, not direct. (R5: mediated design->timing.)

### `duration_year`

- **Association:** effect = 0.104 (eta), n_valid = 42,855
- **Provenance:** demoted_confounded

`eligibility/gender` affects the trial timeline only through `enrollment` / `study_design_info/intervention_model`, the direct parents of trial duration; the marginal association with `duration_year` is mediated, not direct. (R5: mediated design->timing.)

### `study_design_info/primary_purpose`

- **Association:** effect = 0.097 (cramers_v), n_valid = 70,604
- **Provenance:** demoted_confounded

`study_design_info/primary_purpose` has no concrete causal mechanism that sets `eligibility/gender`. Trial size, eligible population, calendar start date, site geography and the free-text title are not directly caused by `study_design_info/primary_purpose`; the association is a jointly-chosen-design / sponsor-footprint / secular-trend confound. (R9: spurious design->planning/eligibility.)

### `study_design_info/intervention_model`

- **Association:** effect = 0.087 (cramers_v), n_valid = 70,749
- **Provenance:** demoted_confounded

`study_design_info/intervention_model` has no concrete causal mechanism that sets `eligibility/gender`. Trial size, eligible population, calendar start date, site geography and the free-text title are not directly caused by `study_design_info/intervention_model`; the association is a jointly-chosen-design / sponsor-footprint / secular-trend confound. (R9: spurious design->planning/eligibility.)

### `sponsors/lead_sponsor/agency_class`

- **Association:** effect = 0.084 (cramers_v), n_valid = 71,221
- **Provenance:** demoted_confounded

`sponsors/lead_sponsor/agency_class` has no concrete causal mechanism that sets `eligibility/gender`. Trial size, eligible population, calendar start date, site geography and the free-text title are not directly caused by `sponsors/lead_sponsor/agency_class`; the association is a jointly-chosen-design / sponsor-footprint / secular-trend confound. (R9: spurious design->planning/eligibility.)

### `eligibility/maximum_age`

- **Association:** effect = 0.068 (eta), n_valid = 37,908
- **Provenance:** default_within_tier

Both in group 'design_eligibility' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `Experimental Arm Number`

- **Association:** effect = 0.067 (eta), n_valid = 69,293
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_eligibility'); jointly determined by upstream design_top choices, no direct arrow.

### `oversight_info/is_fda_regulated_drug`

- **Association:** effect = 0.065 (cramers_v), n_valid = 11,339
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_eligibility' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `intervention_browse/mesh_term`

- **Association:** effect = 0.061 (eta), n_valid = 71,221
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_eligibility' and 'design_derived'); jointly determined by upstream design_top choices, no direct arrow.

### `eligibility/minimum_age`

- **Association:** effect = 0.060 (eta), n_valid = 69,489
- **Provenance:** default_within_tier

Both in group 'design_eligibility' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `responsible_party/responsible_party_type`

- **Association:** effect = 0.059 (cramers_v), n_valid = 67,878
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_eligibility' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `execution_fail`

- **Association:** effect = 0.058 (eta), n_valid = 42,207
- **Provenance:** demoted_confounded

`eligibility/gender` reaches the trial-success label `execution_fail` only through biology / efficacy and enrollment mediators already in the DAG (`biology_pass`, `failure_reason`, `enrollment`); no direct arrow. (R6: mediated design->label.)

### `execution_pass`

- **Association:** effect = 0.058 (eta), n_valid = 42,207
- **Provenance:** demoted_confounded

`eligibility/gender` reaches the trial-success label `execution_pass` only through biology / efficacy and enrollment mediators already in the DAG (`biology_pass`, `failure_reason`, `enrollment`); no direct arrow. (R6: mediated design->label.)

### `study_design_info/masking`

- **Association:** effect = 0.057 (cramers_v), n_valid = 64,727
- **Provenance:** demoted_confounded

`study_design_info/masking` has no concrete causal mechanism that sets `eligibility/gender`. Trial size, eligible population, calendar start date, site geography and the free-text title are not directly caused by `study_design_info/masking`; the association is a jointly-chosen-design / sponsor-footprint / secular-trend confound. (R9: spurious design->planning/eligibility.)

### `study_design_info/masking_num`

- **Association:** effect = 0.055 (eta), n_valid = 70,854
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_eligibility' and 'design_derived'); jointly determined by upstream design_top choices, no direct arrow.

### `MaskingType-Outcomes Assessor`

- **Association:** effect = 0.052 (eta), n_valid = 70,854
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_eligibility'); jointly determined by upstream design_top choices, no direct arrow.
