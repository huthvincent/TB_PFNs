# location/facility/address/city

- **Group:** `design_planning`
- **Dtype:** high_cardinality_text
- **Description:** City/cities where the trial is conducted (tested via token count).
- **Associated partners (from `association.md`):** 46
  - Direct **causes** (parents of this feature): **0**
  - Direct **effects** (children of this feature): **0**
  - Associated but **no direct** causal edge: **46**

This per-feature file enumerates only **associated** partners. All other columns in `DAG.json` were ruled independent in the Stage-1 association screen and do not appear here. See `association.md` for the screen.

---

## Direct causes (0)

_(none)_

---

## Direct effects (0)

_(none)_

---

## Associated but no direct causal edge (46)

### `intervention/intervention_type`

- **Association:** effect = 0.566 (abs_spearman), n_valid = 81,786
- **Provenance:** demoted_confounded

`intervention/intervention_type` has no concrete causal mechanism that sets `location/facility/address/city`. Trial size, eligible population, calendar start date, site geography and the free-text title are not directly caused by `intervention/intervention_type`; the association is a jointly-chosen-design / sponsor-footprint / secular-trend confound. (R9: spurious design->planning/eligibility.)

### `sae_YN`

- **Association:** effect = 0.477 (abs_spearman), n_valid = 17,916
- **Provenance:** demoted_confounded

`location/facility/address/city` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `sae_YN`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `enrollment`

- **Association:** effect = 0.456 (abs_spearman), n_valid = 44,446
- **Provenance:** default_within_tier

Both in group 'design_planning' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `execution_pass`

- **Association:** effect = 0.393 (abs_spearman), n_valid = 52,772
- **Provenance:** demoted_confounded

`location/facility/address/city` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `execution_pass`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `execution_fail`

- **Association:** effect = 0.393 (abs_spearman), n_valid = 52,772
- **Provenance:** demoted_confounded

`location/facility/address/city` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `execution_fail`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `sae_rate`

- **Association:** effect = 0.371 (abs_spearman), n_valid = 17,916
- **Provenance:** demoted_confounded

`location/facility/address/city` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `sae_rate`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `approval_outcome`

- **Association:** effect = 0.360 (abs_spearman), n_valid = 30,683
- **Provenance:** demoted_confounded

`location/facility/address/city` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `approval_outcome`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `mortality_YN`

- **Association:** effect = 0.318 (abs_spearman), n_valid = 17,916
- **Provenance:** demoted_confounded

`location/facility/address/city` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `mortality_YN`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `dropout_YN`

- **Association:** effect = 0.289 (abs_spearman), n_valid = 38,302
- **Provenance:** demoted_confounded

`location/facility/address/city` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `dropout_YN`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `phase`

- **Association:** effect = 0.274 (eta), n_valid = 81,786
- **Provenance:** demoted_confounded

`phase` has no concrete causal mechanism that sets `location/facility/address/city`. Trial size, eligible population, calendar start date, site geography and the free-text title are not directly caused by `phase`; the association is a jointly-chosen-design / sponsor-footprint / secular-trend confound. (R9: spurious design->planning/eligibility.)

### `dropout_rate`

- **Association:** effect = 0.268 (abs_spearman), n_valid = 38,302
- **Provenance:** demoted_confounded

`location/facility/address/city` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `dropout_rate`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `mortality_rate`

- **Association:** effect = 0.265 (abs_spearman), n_valid = 17,916
- **Provenance:** demoted_confounded

`location/facility/address/city` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `mortality_rate`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `duration_year`

- **Association:** effect = 0.256 (abs_spearman), n_valid = 42,855
- **Provenance:** demoted_confounded

`location/facility/address/city` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `duration_year`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `duration_day`

- **Association:** effect = 0.256 (abs_spearman), n_valid = 42,855
- **Provenance:** demoted_confounded

`location/facility/address/city` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `duration_day`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `duration_month`

- **Association:** effect = 0.255 (abs_spearman), n_valid = 42,855
- **Provenance:** demoted_confounded

`location/facility/address/city` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `duration_month`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `ipd_info_type-Informed Consent Form (ICF)`

- **Association:** effect = 0.244 (abs_spearman), n_valid = 2,145
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_oversight' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `patient_data/sharing_ipd`

- **Association:** effect = 0.228 (eta), n_valid = 13,510
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_planning' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `ipd_info_type-Statistical Analysis Plan (SAP)`

- **Association:** effect = 0.221 (abs_spearman), n_valid = 2,297
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_oversight' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `sponsors/lead_sponsor/agency_class`

- **Association:** effect = 0.174 (eta), n_valid = 71,221
- **Provenance:** demoted_confounded

`sponsors/lead_sponsor/agency_class` has no concrete causal mechanism that sets `location/facility/address/city`. Trial size, eligible population, calendar start date, site geography and the free-text title are not directly caused by `sponsors/lead_sponsor/agency_class`; the association is a jointly-chosen-design / sponsor-footprint / secular-trend confound. (R9: spurious design->planning/eligibility.)

### `ipd_info_type-Clinical Study Report (CSR)`

- **Association:** effect = 0.166 (abs_spearman), n_valid = 2,145
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_oversight' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `failure_reason`

- **Association:** effect = 0.160 (eta), n_valid = 20,769
- **Provenance:** demoted_confounded

`location/facility/address/city` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `failure_reason`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `responsible_party/responsible_party_type`

- **Association:** effect = 0.146 (eta), n_valid = 67,878
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_planning' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `study_design_info/intervention_model`

- **Association:** effect = 0.140 (eta), n_valid = 80,897
- **Provenance:** demoted_confounded

`study_design_info/intervention_model` has no concrete causal mechanism that sets `location/facility/address/city`. Trial size, eligible population, calendar start date, site geography and the free-text title are not directly caused by `study_design_info/intervention_model`; the association is a jointly-chosen-design / sponsor-footprint / secular-trend confound. (R9: spurious design->planning/eligibility.)

### `eligibility/healthy_volunteers`

- **Association:** effect = 0.122 (eta), n_valid = 81,613
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_eligibility' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `Experimental Arm Number`

- **Association:** effect = 0.122 (abs_spearman), n_valid = 78,123
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `study_design_info/masking`

- **Association:** effect = 0.116 (eta), n_valid = 75,043
- **Provenance:** demoted_confounded

`study_design_info/masking` has no concrete causal mechanism that sets `location/facility/address/city`. Trial size, eligible population, calendar start date, site geography and the free-text title are not directly caused by `study_design_info/masking`; the association is a jointly-chosen-design / sponsor-footprint / secular-trend confound. (R9: spurious design->planning/eligibility.)

### `Drug intervention Number`

- **Association:** effect = 0.112 (abs_spearman), n_valid = 81,786
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `MaskingType-Investigator`

- **Association:** effect = 0.111 (abs_spearman), n_valid = 81,170
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `intervention/intervention_name`

- **Association:** effect = 0.109 (abs_spearman), n_valid = 81,786
- **Provenance:** demoted_confounded

`intervention/intervention_name` has no concrete causal mechanism that sets `location/facility/address/city`. Trial size, eligible population, calendar start date, site geography and the free-text title are not directly caused by `intervention/intervention_name`; the association is a jointly-chosen-design / sponsor-footprint / secular-trend confound. (R9: spurious design->planning/eligibility.)

### `oversight_info/is_fda_regulated_drug`

- **Association:** effect = 0.108 (eta), n_valid = 13,761
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_planning' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `oversight_info/has_dmc`

- **Association:** effect = 0.103 (eta), n_valid = 45,926
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_planning' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `ipd_info_type-Analytic Code`

- **Association:** effect = 0.101 (abs_spearman), n_valid = 2,297
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_oversight' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `condition_browse/mesh_term`

- **Association:** effect = 0.098 (abs_spearman), n_valid = 81,786
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `study_design_info/masking_num`

- **Association:** effect = 0.094 (abs_spearman), n_valid = 81,170
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_planning' and 'design_derived'); jointly determined by upstream design_top choices, no direct arrow.

### `MaskingType-Care Provider`

- **Association:** effect = 0.094 (abs_spearman), n_valid = 81,170
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `number_of_arms`

- **Association:** effect = 0.091 (abs_spearman), n_valid = 78,123
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_planning' and 'design_derived'); jointly determined by upstream design_top choices, no direct arrow.

### `MaskingType-Participant`

- **Association:** effect = 0.088 (abs_spearman), n_valid = 81,170
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `study_design_info/primary_purpose`

- **Association:** effect = 0.084 (eta), n_valid = 80,983
- **Provenance:** demoted_confounded

`study_design_info/primary_purpose` has no concrete causal mechanism that sets `location/facility/address/city`. Trial size, eligible population, calendar start date, site geography and the free-text title are not directly caused by `study_design_info/primary_purpose`; the association is a jointly-chosen-design / sponsor-footprint / secular-trend confound. (R9: spurious design->planning/eligibility.)

### `MaskingType-Outcomes Assessor`

- **Association:** effect = 0.077 (abs_spearman), n_valid = 81,170
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `ipd_info_type-Study Protocol`

- **Association:** effect = 0.077 (abs_spearman), n_valid = 2,297
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_oversight' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `Placebo Comparator Arm Number`

- **Association:** effect = 0.076 (abs_spearman), n_valid = 78,123
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `study_design_info/allocation`

- **Association:** effect = 0.074 (eta), n_valid = 62,081
- **Provenance:** demoted_confounded

`study_design_info/allocation` has no concrete causal mechanism that sets `location/facility/address/city`. Trial size, eligible population, calendar start date, site geography and the free-text title are not directly caused by `study_design_info/allocation`; the association is a jointly-chosen-design / sponsor-footprint / secular-trend confound. (R9: spurious design->planning/eligibility.)

### `start_date`

- **Association:** effect = 0.070 (abs_spearman), n_valid = 42,855
- **Provenance:** default_within_tier

Both in group 'design_planning' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `No Intervention Arm Number`

- **Association:** effect = 0.063 (abs_spearman), n_valid = 69,293
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `eligibility/maximum_age`

- **Association:** effect = 0.062 (abs_spearman), n_valid = 42,760
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_eligibility' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `has_expanded_access`

- **Association:** effect = 0.056 (eta), n_valid = 70,125
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_oversight' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.
