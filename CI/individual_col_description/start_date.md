# start_date

- **Group:** `design_planning`
- **Dtype:** date (parsed to days)
- **Description:** Reported start date of the trial; parsed to days since 2000-01-01.
- **Associated partners (from `association.md`):** 46
  - Direct **causes** (parents of this feature): **0**
  - Direct **effects** (children of this feature): **2**
  - Associated but **no direct** causal edge: **44**

This per-feature file enumerates only **associated** partners. All other columns in `DAG.json` were ruled independent in the Stage-1 association screen and do not appear here. See `association.md` for the screen.

---

## Direct causes (0)

_(none)_

---

## Direct effects (2)

### `completion_date`

- **Association:** effect = 0.868 (abs_spearman), n_valid = 42,855
- **Mechanism:** `operational`
- **Provenance:** explicit

The trial cannot complete before it has started; start_date temporally precedes completion_date.

### `duration_day`

- **Association:** effect = 0.425 (abs_spearman), n_valid = 42,855
- **Mechanism:** `deterministic`
- **Provenance:** explicit

duration_day = completion_date - start_date (in days).

---

## Associated but no direct causal edge (44)

### `duration_month`

- **Association:** effect = 0.426 (abs_spearman), n_valid = 42,855
- **Provenance:** explicit

Mediated through duration_day: start_date -> duration_day -> duration_month.

### `duration_year`

- **Association:** effect = 0.425 (abs_spearman), n_valid = 42,855
- **Provenance:** explicit

Mediated through duration_day: start_date -> duration_day -> duration_year.

### `approval_outcome`

- **Association:** effect = 0.296 (abs_spearman), n_valid = 9,263
- **Provenance:** demoted_confounded

`start_date` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `approval_outcome`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `sae_rate`

- **Association:** effect = 0.257 (abs_spearman), n_valid = 13,278
- **Provenance:** demoted_confounded

`start_date` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `sae_rate`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `mortality_rate`

- **Association:** effect = 0.205 (abs_spearman), n_valid = 13,278
- **Provenance:** demoted_confounded

`start_date` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `mortality_rate`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `eligibility/healthy_volunteers`

- **Association:** effect = 0.198 (eta), n_valid = 42,833
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_eligibility' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `sae_YN`

- **Association:** effect = 0.198 (abs_spearman), n_valid = 13,278
- **Provenance:** demoted_confounded

`start_date` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `sae_YN`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `mortality_YN`

- **Association:** effect = 0.196 (abs_spearman), n_valid = 13,278
- **Provenance:** demoted_confounded

`start_date` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `mortality_YN`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `patient_data/sharing_ipd`

- **Association:** effect = 0.180 (eta), n_valid = 9,341
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_oversight' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `execution_pass`

- **Association:** effect = 0.177 (abs_spearman), n_valid = 20,062
- **Provenance:** demoted_confounded

`start_date` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `execution_pass`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `execution_fail`

- **Association:** effect = 0.177 (abs_spearman), n_valid = 20,062
- **Provenance:** demoted_confounded

`start_date` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `execution_fail`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `study_design_info/intervention_model`

- **Association:** effect = 0.174 (eta), n_valid = 42,592
- **Provenance:** demoted_confounded

`study_design_info/intervention_model` has no concrete causal mechanism that sets `start_date`. Trial size, eligible population, calendar start date, site geography and the free-text title are not directly caused by `study_design_info/intervention_model`; the association is a jointly-chosen-design / sponsor-footprint / secular-trend confound. (R9: spurious design->planning/eligibility.)

### `study_design_info/masking`

- **Association:** effect = 0.173 (eta), n_valid = 42,635
- **Provenance:** demoted_confounded

`study_design_info/masking` has no concrete causal mechanism that sets `start_date`. Trial size, eligible population, calendar start date, site geography and the free-text title are not directly caused by `study_design_info/masking`; the association is a jointly-chosen-design / sponsor-footprint / secular-trend confound. (R9: spurious design->planning/eligibility.)

### `intervention_browse/mesh_term`

- **Association:** effect = 0.164 (abs_spearman), n_valid = 42,855
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `phase`

- **Association:** effect = 0.156 (eta), n_valid = 42,855
- **Provenance:** demoted_confounded

`phase` has no concrete causal mechanism that sets `start_date`. Trial size, eligible population, calendar start date, site geography and the free-text title are not directly caused by `phase`; the association is a jointly-chosen-design / sponsor-footprint / secular-trend confound. (R9: spurious design->planning/eligibility.)

### `enrollment`

- **Association:** effect = 0.151 (abs_spearman), n_valid = 16,162
- **Provenance:** default_within_tier

Both in group 'design_planning' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `condition_browse/mesh_term`

- **Association:** effect = 0.145 (abs_spearman), n_valid = 42,855
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `dropout_rate`

- **Association:** effect = 0.131 (abs_spearman), n_valid = 16,162
- **Provenance:** demoted_confounded

`start_date` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `dropout_rate`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `smiless`

- **Association:** effect = 0.127 (abs_spearman), n_valid = 42,855
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `failure_reason`

- **Association:** effect = 0.123 (eta), n_valid = 6,904
- **Provenance:** demoted_confounded

`start_date` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `failure_reason`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `study_design_info/primary_purpose`

- **Association:** effect = 0.119 (eta), n_valid = 42,836
- **Provenance:** demoted_confounded

`study_design_info/primary_purpose` has no concrete causal mechanism that sets `start_date`. Trial size, eligible population, calendar start date, site geography and the free-text title are not directly caused by `study_design_info/primary_purpose`; the association is a jointly-chosen-design / sponsor-footprint / secular-trend confound. (R9: spurious design->planning/eligibility.)

### `ipd_info_type-Analytic Code`

- **Association:** effect = 0.107 (abs_spearman), n_valid = 1,728
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_oversight' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `ipd_info_type-Clinical Study Report (CSR)`

- **Association:** effect = 0.100 (abs_spearman), n_valid = 1,728
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_oversight' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `dropout_YN`

- **Association:** effect = 0.099 (abs_spearman), n_valid = 16,162
- **Provenance:** demoted_confounded

`start_date` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `dropout_YN`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `Radiation intervention Number`

- **Association:** effect = 0.089 (abs_spearman), n_valid = 42,855
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `ipd_info_type-Study Protocol`

- **Association:** effect = 0.085 (abs_spearman), n_valid = 1,728
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_oversight' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `sponsors/lead_sponsor/agency_class`

- **Association:** effect = 0.084 (eta), n_valid = 42,855
- **Provenance:** demoted_confounded

`sponsors/lead_sponsor/agency_class` has no concrete causal mechanism that sets `start_date`. Trial size, eligible population, calendar start date, site geography and the free-text title are not directly caused by `sponsors/lead_sponsor/agency_class`; the association is a jointly-chosen-design / sponsor-footprint / secular-trend confound. (R9: spurious design->planning/eligibility.)

### `ipd_info_type-Informed Consent Form (ICF)`

- **Association:** effect = 0.080 (abs_spearman), n_valid = 1,728
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_oversight' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `Procedure intervention Number`

- **Association:** effect = 0.078 (abs_spearman), n_valid = 42,855
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `study_design_info/masking_num`

- **Association:** effect = 0.076 (abs_spearman), n_valid = 42,635
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_planning' and 'design_derived'); jointly determined by upstream design_top choices, no direct arrow.

### `MaskingType-Care Provider`

- **Association:** effect = 0.076 (abs_spearman), n_valid = 42,635
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `MaskingType-Participant`

- **Association:** effect = 0.076 (abs_spearman), n_valid = 42,635
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `number_of_arms`

- **Association:** effect = 0.075 (abs_spearman), n_valid = 42,293
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `MaskingType-Outcomes Assessor`

- **Association:** effect = 0.075 (abs_spearman), n_valid = 42,635
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `location/facility/address/city`

- **Association:** effect = 0.070 (abs_spearman), n_valid = 42,855
- **Provenance:** default_within_tier

Both in group 'design_planning' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `icdcode`

- **Association:** effect = 0.070 (abs_spearman), n_valid = 42,855
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `responsible_party/responsible_party_type`

- **Association:** effect = 0.069 (eta), n_valid = 42,745
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_oversight' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `Combination Product intervention Number`

- **Association:** effect = 0.065 (abs_spearman), n_valid = 42,855
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `intervention/intervention_name`

- **Association:** effect = 0.062 (abs_spearman), n_valid = 42,855
- **Provenance:** demoted_confounded

`intervention/intervention_name` has no concrete causal mechanism that sets `start_date`. Trial size, eligible population, calendar start date, site geography and the free-text title are not directly caused by `intervention/intervention_name`; the association is a jointly-chosen-design / sponsor-footprint / secular-trend confound. (R9: spurious design->planning/eligibility.)

### `biology_pass`

- **Association:** effect = 0.059 (abs_spearman), n_valid = 10,917
- **Provenance:** demoted_confounded

`start_date` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `biology_pass`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `biology_fail`

- **Association:** effect = 0.059 (abs_spearman), n_valid = 10,917
- **Provenance:** demoted_confounded

`start_date` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `biology_fail`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `condition`

- **Association:** effect = 0.056 (abs_spearman), n_valid = 42,855
- **Provenance:** demoted_confounded

`condition` has no concrete causal mechanism that sets `start_date`. Trial size, eligible population, calendar start date, site geography and the free-text title are not directly caused by `condition`; the association is a jointly-chosen-design / sponsor-footprint / secular-trend confound. (R9: spurious design->planning/eligibility.)

### `MaskingType-Investigator`

- **Association:** effect = 0.055 (abs_spearman), n_valid = 42,635
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `eligibility/maximum_age`

- **Association:** effect = 0.053 (abs_spearman), n_valid = 24,161
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_eligibility' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.
