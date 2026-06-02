# eligibility/healthy_volunteers

- **Group:** `design_eligibility`
- **Dtype:** categorical
- **Description:** Whether healthy volunteers are accepted: 'Accepts Healthy Volunteers' / 'No' / NaN.
- **Associated partners (from `association.md`):** 41
  - Direct **causes** (parents of this feature): **4**
  - Direct **effects** (children of this feature): **6**
  - Associated but **no direct** causal edge: **31**

This per-feature file enumerates only **associated** partners. All other columns in `DAG.json` were ruled independent in the Stage-1 association screen and do not appear here. See `association.md` for the screen.

---

## Direct causes (4)

### `study_design_info/primary_purpose`

- **Association:** effect = 0.455 (cramers_v), n_valid = 80,843
- **Mechanism:** `design_choice`
- **Provenance:** default_cross_tier

Sponsor design decision made at registration (study_design_info/primary_purpose) that constrains a downstream design field (eligibility/healthy_volunteers).

### `phase`

- **Association:** effect = 0.411 (cramers_v), n_valid = 81,613
- **Mechanism:** `design_choice`
- **Provenance:** default_cross_tier

Sponsor design decision made at registration (phase) that constrains a downstream design field (eligibility/healthy_volunteers).

### `intervention/intervention_type`

- **Association:** effect = 0.070 (eta), n_valid = 81,613
- **Mechanism:** `design_choice`
- **Provenance:** default_cross_tier

Sponsor design decision made at registration (intervention/intervention_type) that constrains a downstream design field (eligibility/healthy_volunteers).

### `condition`

- **Association:** effect = 0.058 (eta), n_valid = 81,613
- **Mechanism:** `design_choice`
- **Provenance:** default_cross_tier

Sponsor design decision made at registration (condition) that constrains a downstream design field (eligibility/healthy_volunteers).

---

## Direct effects (6)

### `sae_YN`

- **Association:** effect = 0.309 (eta), n_valid = 17,914
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Downstream-design field (eligibility/healthy_volunteers) shifts the realised safety outcome (sae_YN) through population biology or trial operations.

### `sae_rate`

- **Association:** effect = 0.261 (eta), n_valid = 17,914
- **Mechanism:** `biological`
- **Provenance:** explicit

Healthy-volunteer trials show systematically lower SAE rates than diseased-population trials (no disease-driven AE component).

### `mortality_YN`

- **Association:** effect = 0.256 (eta), n_valid = 17,914
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Downstream-design field (eligibility/healthy_volunteers) shifts the realised safety outcome (mortality_YN) through population biology or trial operations.

### `dropout_rate`

- **Association:** effect = 0.203 (eta), n_valid = 38,268
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Downstream-design field (eligibility/healthy_volunteers) shifts the realised safety outcome (dropout_rate) through population biology or trial operations.

### `mortality_rate`

- **Association:** effect = 0.184 (eta), n_valid = 17,914
- **Mechanism:** `biological`
- **Provenance:** explicit

Healthy-volunteer trials have near-zero background mortality.

### `dropout_YN`

- **Association:** effect = 0.166 (eta), n_valid = 38,268
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Downstream-design field (eligibility/healthy_volunteers) shifts the realised safety outcome (dropout_YN) through population biology or trial operations.

---

## Associated but no direct causal edge (31)

### `duration_month`

- **Association:** effect = 0.351 (eta), n_valid = 42,833
- **Provenance:** demoted_confounded

`eligibility/healthy_volunteers` affects the trial timeline only through `enrollment` / `study_design_info/intervention_model`, the direct parents of trial duration; the marginal association with `duration_month` is mediated, not direct. (R5: mediated design->timing.)

### `duration_day`

- **Association:** effect = 0.351 (eta), n_valid = 42,833
- **Provenance:** demoted_confounded

`eligibility/healthy_volunteers` affects the trial timeline only through `enrollment` / `study_design_info/intervention_model`, the direct parents of trial duration; the marginal association with `duration_day` is mediated, not direct. (R5: mediated design->timing.)

### `duration_year`

- **Association:** effect = 0.351 (eta), n_valid = 42,833
- **Provenance:** demoted_confounded

`eligibility/healthy_volunteers` affects the trial timeline only through `enrollment` / `study_design_info/intervention_model`, the direct parents of trial duration; the marginal association with `duration_year` is mediated, not direct. (R5: mediated design->timing.)

### `ipd_info_type-Informed Consent Form (ICF)`

- **Association:** effect = 0.332 (eta), n_valid = 2,145
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_eligibility' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `study_design_info/intervention_model`

- **Association:** effect = 0.293 (cramers_v), n_valid = 80,743
- **Provenance:** demoted_confounded

`study_design_info/intervention_model` has no concrete causal mechanism that sets `eligibility/healthy_volunteers`. Trial size, eligible population, calendar start date, site geography and the free-text title are not directly caused by `study_design_info/intervention_model`; the association is a jointly-chosen-design / sponsor-footprint / secular-trend confound. (R9: spurious design->planning/eligibility.)

### `condition_browse/mesh_term`

- **Association:** effect = 0.233 (eta), n_valid = 81,613
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_eligibility'); jointly determined by upstream design_top choices, no direct arrow.

### `eligibility/maximum_age`

- **Association:** effect = 0.224 (eta), n_valid = 42,674
- **Provenance:** default_within_tier

Both in group 'design_eligibility' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `number_of_arms`

- **Association:** effect = 0.210 (eta), n_valid = 78,060
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_eligibility' and 'design_derived'); jointly determined by upstream design_top choices, no direct arrow.

### `start_date`

- **Association:** effect = 0.198 (eta), n_valid = 42,833
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_eligibility' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `Experimental Arm Number`

- **Association:** effect = 0.177 (eta), n_valid = 78,060
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_eligibility'); jointly determined by upstream design_top choices, no direct arrow.

### `Biological intervention Number`

- **Association:** effect = 0.172 (eta), n_valid = 81,613
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_eligibility'); jointly determined by upstream design_top choices, no direct arrow.

### `eligibility/gender`

- **Association:** effect = 0.170 (cramers_v), n_valid = 71,109
- **Provenance:** default_within_tier

Both in group 'design_eligibility' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `location/facility/address/city`

- **Association:** effect = 0.122 (eta), n_valid = 81,613
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_eligibility' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `failure_reason`

- **Association:** effect = 0.118 (cramers_v), n_valid = 20,706
- **Provenance:** demoted_confounded

`eligibility/healthy_volunteers` reaches the trial-success label `failure_reason` only through biology / efficacy and enrollment mediators already in the DAG (`biology_pass`, `failure_reason`, `enrollment`); no direct arrow. (R6: mediated design->label.)

### `execution_pass`

- **Association:** effect = 0.116 (eta), n_valid = 52,677
- **Provenance:** demoted_confounded

`eligibility/healthy_volunteers` reaches the trial-success label `execution_pass` only through biology / efficacy and enrollment mediators already in the DAG (`biology_pass`, `failure_reason`, `enrollment`); no direct arrow. (R6: mediated design->label.)

### `execution_fail`

- **Association:** effect = 0.116 (eta), n_valid = 52,677
- **Provenance:** demoted_confounded

`eligibility/healthy_volunteers` reaches the trial-success label `execution_fail` only through biology / efficacy and enrollment mediators already in the DAG (`biology_pass`, `failure_reason`, `enrollment`); no direct arrow. (R6: mediated design->label.)

### `intervention_browse/mesh_term`

- **Association:** effect = 0.115 (eta), n_valid = 81,613
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_eligibility' and 'design_derived'); jointly determined by upstream design_top choices, no direct arrow.

### `oversight_info/has_dmc`

- **Association:** effect = 0.114 (cramers_v), n_valid = 45,906
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_eligibility' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `sponsors/lead_sponsor/agency_class`

- **Association:** effect = 0.112 (cramers_v), n_valid = 71,109
- **Provenance:** demoted_confounded

`sponsors/lead_sponsor/agency_class` has no concrete causal mechanism that sets `eligibility/healthy_volunteers`. Trial size, eligible population, calendar start date, site geography and the free-text title are not directly caused by `sponsors/lead_sponsor/agency_class`; the association is a jointly-chosen-design / sponsor-footprint / secular-trend confound. (R9: spurious design->planning/eligibility.)

### `study_design_info/masking`

- **Association:** effect = 0.108 (cramers_v), n_valid = 74,940
- **Provenance:** demoted_confounded

`study_design_info/masking` has no concrete causal mechanism that sets `eligibility/healthy_volunteers`. Trial size, eligible population, calendar start date, site geography and the free-text title are not directly caused by `study_design_info/masking`; the association is a jointly-chosen-design / sponsor-footprint / secular-trend confound. (R9: spurious design->planning/eligibility.)

### `oversight_info/is_fda_regulated_drug`

- **Association:** effect = 0.105 (cramers_v), n_valid = 13,761
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_eligibility' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `ipd_info_type-Clinical Study Report (CSR)`

- **Association:** effect = 0.097 (eta), n_valid = 2,145
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_eligibility' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `smiless`

- **Association:** effect = 0.092 (eta), n_valid = 81,613
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_eligibility' and 'design_derived'); jointly determined by upstream design_top choices, no direct arrow.

### `icdcode`

- **Association:** effect = 0.074 (eta), n_valid = 81,613
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_eligibility' and 'design_derived'); jointly determined by upstream design_top choices, no direct arrow.

### `brief_title`

- **Association:** effect = 0.072 (eta), n_valid = 81,613
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_planning' and 'design_eligibility'); jointly determined by upstream design_top choices, no direct arrow.

### `approval_outcome`

- **Association:** effect = 0.068 (eta), n_valid = 30,572
- **Provenance:** demoted_confounded

`eligibility/healthy_volunteers` reaches the trial-success label `approval_outcome` only through biology / efficacy and enrollment mediators already in the DAG (`biology_pass`, `failure_reason`, `enrollment`); no direct arrow. (R6: mediated design->label.)

### `Radiation intervention Number`

- **Association:** effect = 0.065 (eta), n_valid = 81,613
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_eligibility'); jointly determined by upstream design_top choices, no direct arrow.

### `completion_date`

- **Association:** effect = 0.060 (eta), n_valid = 42,833
- **Provenance:** demoted_confounded

`eligibility/healthy_volunteers` affects the trial timeline only through `enrollment` / `study_design_info/intervention_model`, the direct parents of trial duration; the marginal association with `completion_date` is mediated, not direct. (R5: mediated design->timing.)

### `Drug intervention Number`

- **Association:** effect = 0.059 (eta), n_valid = 81,613
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_eligibility'); jointly determined by upstream design_top choices, no direct arrow.

### `MaskingType-Participant`

- **Association:** effect = 0.058 (eta), n_valid = 81,014
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_eligibility'); jointly determined by upstream design_top choices, no direct arrow.

### `Procedure intervention Number`

- **Association:** effect = 0.051 (eta), n_valid = 71,109
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_eligibility'); jointly determined by upstream design_top choices, no direct arrow.
