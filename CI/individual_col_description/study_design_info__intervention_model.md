# study_design_info/intervention_model

- **Group:** `design_top`
- **Dtype:** categorical
- **Description:** How participants are assigned to arms: Single Group / Parallel / Crossover / Factorial / Sequential.
- **Associated partners (from `association.md`):** 58
  - Direct **causes** (parents of this feature): **1**
  - Direct **effects** (children of this feature): **7**
  - Associated but **no direct** causal edge: **50**

This per-feature file enumerates only **associated** partners. All other columns in `DAG.json` were ruled independent in the Stage-1 association screen and do not appear here. See `association.md` for the screen.

---

## Direct causes (1)

### `phase`

- **Association:** effect = 0.245 (cramers_v), n_valid = 80,897
- **Mechanism:** `design_choice`
- **Provenance:** explicit

Phase 1 first-in-human trials are predominantly Single Group Assignment (no comparator yet); Phase 3 pivotal trials are Parallel Assignment for randomised comparison. Phase shapes the model choice.

---

## Direct effects (7)

### `study_design_info/allocation`

- **Association:** effect = 0.554 (cramers_v), n_valid = 61,697
- **Mechanism:** `design_constraint`
- **Provenance:** explicit

Single Group Assignment forces allocation='N/A'; Parallel / Crossover / Factorial designs require Randomized or Non-Randomized allocation. The intervention model strictly constrains the feasible allocation.

### `number_of_arms`

- **Association:** effect = 0.451 (eta), n_valid = 77,887
- **Mechanism:** `design_constraint`
- **Provenance:** explicit

'Single Group Assignment' forces number_of_arms=1; 'Parallel' / 'Crossover' force >=2; 'Factorial' typically >=4. The intervention model strictly constrains the number of arms.

### `duration_month`

- **Association:** effect = 0.249 (eta), n_valid = 42,592
- **Mechanism:** `design_choice`
- **Provenance:** default_cross_tier

Sponsor design decision (study_design_info/intervention_model) that drives the realised trial-duration timeline (duration_month).

### `duration_year`

- **Association:** effect = 0.249 (eta), n_valid = 42,592
- **Mechanism:** `design_choice`
- **Provenance:** default_cross_tier

Sponsor design decision (study_design_info/intervention_model) that drives the realised trial-duration timeline (duration_year).

### `duration_day`

- **Association:** effect = 0.249 (eta), n_valid = 42,592
- **Mechanism:** `design_choice`
- **Provenance:** default_cross_tier

Sponsor design decision (study_design_info/intervention_model) that drives the realised trial-duration timeline (duration_day).

### `completion_date`

- **Association:** effect = 0.123 (eta), n_valid = 42,592
- **Mechanism:** `design_choice`
- **Provenance:** default_cross_tier

Sponsor design decision (study_design_info/intervention_model) that drives the realised trial-duration timeline (completion_date).

### `enrollment`

- **Association:** effect = 0.080 (eta), n_valid = 44,158
- **Mechanism:** `design_choice`
- **Provenance:** default_cross_tier

Sponsor design decision made at registration (study_design_info/intervention_model) that constrains a downstream design field (enrollment).

---

## Associated but no direct causal edge (50)

### `MaskingType-Participant`

- **Association:** effect = 0.512 (eta), n_valid = 80,702
- **Provenance:** demoted_confounded

`MaskingType-Participant` is a deterministic descendant of its single definitional design parent; `study_design_info/intervention_model` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `study_design_info/masking_num`

- **Association:** effect = 0.508 (eta), n_valid = 80,702
- **Provenance:** demoted_confounded

`study_design_info/masking_num` is a deterministic descendant of its single definitional design parent; `study_design_info/intervention_model` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `MaskingType-Investigator`

- **Association:** effect = 0.479 (eta), n_valid = 80,702
- **Provenance:** demoted_confounded

`MaskingType-Investigator` is a deterministic descendant of its single definitional design parent; `study_design_info/intervention_model` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `MaskingType-Outcomes Assessor`

- **Association:** effect = 0.352 (eta), n_valid = 80,702
- **Provenance:** demoted_confounded

`MaskingType-Outcomes Assessor` is a deterministic descendant of its single definitional design parent; `study_design_info/intervention_model` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `MaskingType-Care Provider`

- **Association:** effect = 0.345 (eta), n_valid = 80,702
- **Provenance:** demoted_confounded

`MaskingType-Care Provider` is a deterministic descendant of its single definitional design parent; `study_design_info/intervention_model` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `Placebo Comparator Arm Number`

- **Association:** effect = 0.341 (eta), n_valid = 77,887
- **Provenance:** demoted_confounded

`Placebo Comparator Arm Number` is a deterministic descendant of its single definitional design parent; `study_design_info/intervention_model` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `Active Comparator Arm Number`

- **Association:** effect = 0.338 (eta), n_valid = 69,093
- **Provenance:** demoted_confounded

`Active Comparator Arm Number` is a deterministic descendant of its single definitional design parent; `study_design_info/intervention_model` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `eligibility/healthy_volunteers`

- **Association:** effect = 0.293 (cramers_v), n_valid = 80,743
- **Provenance:** demoted_confounded

`study_design_info/intervention_model` has no concrete causal mechanism that sets `eligibility/healthy_volunteers`. Trial size, eligible population, calendar start date, site geography and the free-text title are not directly caused by `study_design_info/intervention_model`; the association is a jointly-chosen-design / sponsor-footprint / secular-trend confound. (R9: spurious design->planning/eligibility.)

### `study_design_info/masking`

- **Association:** effect = 0.282 (cramers_v), n_valid = 74,651
- **Provenance:** explicit

Both methodological choices made jointly; no direct arrow at this DAG resolution.

### `sae_rate`

- **Association:** effect = 0.271 (eta), n_valid = 17,857
- **Provenance:** demoted_confounded

`study_design_info/intervention_model` is a sponsor / methodology design choice with no direct biological pathway to the realised safety rate `sae_rate`; the association is confounded through `intervention/intervention_type` and `condition` (what is being studied), which carry the genuine safety edges. (R4: confounded design->safety.)

### `Experimental Arm Number`

- **Association:** effect = 0.250 (eta), n_valid = 77,887
- **Provenance:** demoted_confounded

`Experimental Arm Number` is a deterministic descendant of its single definitional design parent; `study_design_info/intervention_model` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `dropout_YN`

- **Association:** effect = 0.240 (eta), n_valid = 38,137
- **Provenance:** demoted_confounded

`study_design_info/intervention_model` is a sponsor / methodology design choice with no direct biological pathway to the realised safety rate `dropout_YN`; the association is confounded through `intervention/intervention_type` and `condition` (what is being studied), which carry the genuine safety edges. (R4: confounded design->safety.)

### `sae_YN`

- **Association:** effect = 0.234 (eta), n_valid = 17,857
- **Provenance:** demoted_confounded

`study_design_info/intervention_model` is a sponsor / methodology design choice with no direct biological pathway to the realised safety rate `sae_YN`; the association is confounded through `intervention/intervention_type` and `condition` (what is being studied), which carry the genuine safety edges. (R4: confounded design->safety.)

### `mortality_rate`

- **Association:** effect = 0.202 (eta), n_valid = 17,857
- **Provenance:** demoted_confounded

`study_design_info/intervention_model` is a sponsor / methodology design choice with no direct biological pathway to the realised safety rate `mortality_rate`; the association is confounded through `intervention/intervention_type` and `condition` (what is being studied), which carry the genuine safety edges. (R4: confounded design->safety.)

### `Drug intervention Number`

- **Association:** effect = 0.200 (eta), n_valid = 80,897
- **Provenance:** demoted_confounded

`Drug intervention Number` is a deterministic descendant of its single definitional design parent; `study_design_info/intervention_model` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `intervention/intervention_name`

- **Association:** effect = 0.199 (eta), n_valid = 80,897
- **Provenance:** explicit

Both jointly chosen sponsor design decisions; no direct arrow.

### `mortality_YN`

- **Association:** effect = 0.186 (eta), n_valid = 17,857
- **Provenance:** demoted_confounded

`study_design_info/intervention_model` is a sponsor / methodology design choice with no direct biological pathway to the realised safety rate `mortality_YN`; the association is confounded through `intervention/intervention_type` and `condition` (what is being studied), which carry the genuine safety edges. (R4: confounded design->safety.)

### `execution_pass`

- **Association:** effect = 0.176 (eta), n_valid = 52,169
- **Provenance:** demoted_confounded

`study_design_info/intervention_model` reaches the trial-success label `execution_pass` only through biology / efficacy and enrollment mediators already in the DAG (`biology_pass`, `failure_reason`, `enrollment`); no direct arrow. (R6: mediated design->label.)

### `execution_fail`

- **Association:** effect = 0.176 (eta), n_valid = 52,169
- **Provenance:** demoted_confounded

`study_design_info/intervention_model` reaches the trial-success label `execution_fail` only through biology / efficacy and enrollment mediators already in the DAG (`biology_pass`, `failure_reason`, `enrollment`); no direct arrow. (R6: mediated design->label.)

### `start_date`

- **Association:** effect = 0.174 (eta), n_valid = 42,592
- **Provenance:** demoted_confounded

`study_design_info/intervention_model` has no concrete causal mechanism that sets `start_date`. Trial size, eligible population, calendar start date, site geography and the free-text title are not directly caused by `study_design_info/intervention_model`; the association is a jointly-chosen-design / sponsor-footprint / secular-trend confound. (R9: spurious design->planning/eligibility.)

### `dropout_rate`

- **Association:** effect = 0.170 (eta), n_valid = 38,137
- **Provenance:** demoted_confounded

`study_design_info/intervention_model` is a sponsor / methodology design choice with no direct biological pathway to the realised safety rate `dropout_rate`; the association is confounded through `intervention/intervention_type` and `condition` (what is being studied), which carry the genuine safety edges. (R4: confounded design->safety.)

### `ipd_info_type-Informed Consent Form (ICF)`

- **Association:** effect = 0.152 (eta), n_valid = 2,140
- **Provenance:** demoted_confounded

`study_design_info/intervention_model` has no direct mechanism that sets the oversight / policy field `ipd_info_type-Informed Consent Form (ICF)`; the association is confounded through sponsor class and trial type. (R8: confounded ->design_oversight.)

### `study_design_info/primary_purpose`

- **Association:** effect = 0.142 (cramers_v), n_valid = 80,137
- **Provenance:** explicit

Both jointly chosen; primary purpose doesn't strictly constrain intervention model.

### `location/facility/address/city`

- **Association:** effect = 0.140 (eta), n_valid = 80,897
- **Provenance:** demoted_confounded

`study_design_info/intervention_model` has no concrete causal mechanism that sets `location/facility/address/city`. Trial size, eligible population, calendar start date, site geography and the free-text title are not directly caused by `study_design_info/intervention_model`; the association is a jointly-chosen-design / sponsor-footprint / secular-trend confound. (R9: spurious design->planning/eligibility.)

### `condition_browse/mesh_term`

- **Association:** effect = 0.134 (eta), n_valid = 80,897
- **Provenance:** demoted_confounded

`condition_browse/mesh_term` is a deterministic descendant of its single definitional design parent; `study_design_info/intervention_model` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `oversight_info/has_dmc`

- **Association:** effect = 0.124 (cramers_v), n_valid = 45,679
- **Provenance:** demoted_confounded

`study_design_info/intervention_model` has no direct mechanism that sets the oversight / policy field `oversight_info/has_dmc`; the association is confounded through sponsor class and trial type. (R8: confounded ->design_oversight.)

### `Behavioral intervention Number`

- **Association:** effect = 0.108 (eta), n_valid = 80,897
- **Provenance:** demoted_confounded

`Behavioral intervention Number` is a deterministic descendant of its single definitional design parent; `study_design_info/intervention_model` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `ipd_info_type-Clinical Study Report (CSR)`

- **Association:** effect = 0.100 (eta), n_valid = 2,140
- **Provenance:** demoted_confounded

`study_design_info/intervention_model` has no direct mechanism that sets the oversight / policy field `ipd_info_type-Clinical Study Report (CSR)`; the association is confounded through sponsor class and trial type. (R8: confounded ->design_oversight.)

### `sponsors/lead_sponsor/agency_class`

- **Association:** effect = 0.100 (cramers_v), n_valid = 70,749
- **Provenance:** explicit

Both jointly chosen.

### `No Intervention Arm Number`

- **Association:** effect = 0.099 (eta), n_valid = 69,093
- **Provenance:** demoted_confounded

`No Intervention Arm Number` is a deterministic descendant of its single definitional design parent; `study_design_info/intervention_model` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `patient_data/sharing_ipd`

- **Association:** effect = 0.095 (cramers_v), n_valid = 13,425
- **Provenance:** demoted_confounded

`study_design_info/intervention_model` has no direct mechanism that sets the oversight / policy field `patient_data/sharing_ipd`; the association is confounded through sponsor class and trial type. (R8: confounded ->design_oversight.)

### `Radiation intervention Number`

- **Association:** effect = 0.089 (eta), n_valid = 80,897
- **Provenance:** demoted_confounded

`Radiation intervention Number` is a deterministic descendant of its single definitional design parent; `study_design_info/intervention_model` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `Biological intervention Number`

- **Association:** effect = 0.088 (eta), n_valid = 80,897
- **Provenance:** demoted_confounded

`Biological intervention Number` is a deterministic descendant of its single definitional design parent; `study_design_info/intervention_model` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `eligibility/gender`

- **Association:** effect = 0.087 (cramers_v), n_valid = 70,749
- **Provenance:** demoted_confounded

`study_design_info/intervention_model` has no concrete causal mechanism that sets `eligibility/gender`. Trial size, eligible population, calendar start date, site geography and the free-text title are not directly caused by `study_design_info/intervention_model`; the association is a jointly-chosen-design / sponsor-footprint / secular-trend confound. (R9: spurious design->planning/eligibility.)

### `brief_title`

- **Association:** effect = 0.085 (eta), n_valid = 80,897
- **Provenance:** demoted_confounded

`study_design_info/intervention_model` has no concrete causal mechanism that sets `brief_title`. Trial size, eligible population, calendar start date, site geography and the free-text title are not directly caused by `study_design_info/intervention_model`; the association is a jointly-chosen-design / sponsor-footprint / secular-trend confound. (R9: spurious design->planning/eligibility.)

### `condition`

- **Association:** effect = 0.077 (eta), n_valid = 80,897
- **Provenance:** explicit

Both jointly chosen design decisions; no direct arrow.

### `intervention_browse/mesh_term`

- **Association:** effect = 0.073 (eta), n_valid = 80,897
- **Provenance:** demoted_confounded

`intervention_browse/mesh_term` is a deterministic descendant of its single definitional design parent; `study_design_info/intervention_model` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `approval_outcome`

- **Association:** effect = 0.072 (eta), n_valid = 30,122
- **Provenance:** demoted_confounded

`study_design_info/intervention_model` reaches the trial-success label `approval_outcome` only through biology / efficacy and enrollment mediators already in the DAG (`biology_pass`, `failure_reason`, `enrollment`); no direct arrow. (R6: mediated design->label.)

### `smiless`

- **Association:** effect = 0.069 (eta), n_valid = 80,897
- **Provenance:** demoted_confounded

`smiless` is a deterministic descendant of its single definitional design parent; `study_design_info/intervention_model` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `responsible_party/responsible_party_type`

- **Association:** effect = 0.062 (cramers_v), n_valid = 67,576
- **Provenance:** demoted_confounded

`study_design_info/intervention_model` has no direct mechanism that sets the oversight / policy field `responsible_party/responsible_party_type`; the association is confounded through sponsor class and trial type. (R8: confounded ->design_oversight.)

### `icdcode`

- **Association:** effect = 0.061 (eta), n_valid = 80,897
- **Provenance:** demoted_confounded

`icdcode` is a deterministic descendant of its single definitional design parent; `study_design_info/intervention_model` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `eligibility/minimum_age`

- **Association:** effect = 0.061 (eta), n_valid = 78,839
- **Provenance:** demoted_confounded

`study_design_info/intervention_model` has no concrete causal mechanism that sets `eligibility/minimum_age`. Trial size, eligible population, calendar start date, site geography and the free-text title are not directly caused by `study_design_info/intervention_model`; the association is a jointly-chosen-design / sponsor-footprint / secular-trend confound. (R9: spurious design->planning/eligibility.)

### `Other Arm Number`

- **Association:** effect = 0.061 (eta), n_valid = 77,887
- **Provenance:** demoted_confounded

`Other Arm Number` is a deterministic descendant of its single definitional design parent; `study_design_info/intervention_model` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `Procedure intervention Number`

- **Association:** effect = 0.060 (eta), n_valid = 70,749
- **Provenance:** demoted_confounded

`Procedure intervention Number` is a deterministic descendant of its single definitional design parent; `study_design_info/intervention_model` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `oversight_info/is_fda_regulated_drug`

- **Association:** effect = 0.060 (cramers_v), n_valid = 13,721
- **Provenance:** demoted_confounded

`study_design_info/intervention_model` has no direct mechanism that sets the oversight / policy field `oversight_info/is_fda_regulated_drug`; the association is confounded through sponsor class and trial type. (R8: confounded ->design_oversight.)

### `Sham Comparator Arm Number`

- **Association:** effect = 0.056 (eta), n_valid = 69,093
- **Provenance:** demoted_confounded

`Sham Comparator Arm Number` is a deterministic descendant of its single definitional design parent; `study_design_info/intervention_model` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `Other intervention Number`

- **Association:** effect = 0.054 (eta), n_valid = 70,749
- **Provenance:** demoted_confounded

`Other intervention Number` is a deterministic descendant of its single definitional design parent; `study_design_info/intervention_model` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `failure_reason`

- **Association:** effect = 0.053 (cramers_v), n_valid = 20,298
- **Provenance:** demoted_confounded

`study_design_info/intervention_model` reaches the trial-success label `failure_reason` only through biology / efficacy and enrollment mediators already in the DAG (`biology_pass`, `failure_reason`, `enrollment`); no direct arrow. (R6: mediated design->label.)

### `Dietary Supplement intervention Number`

- **Association:** effect = 0.051 (eta), n_valid = 80,897
- **Provenance:** demoted_confounded

`Dietary Supplement intervention Number` is a deterministic descendant of its single definitional design parent; `study_design_info/intervention_model` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `eligibility/maximum_age`

- **Association:** effect = 0.051 (eta), n_valid = 42,360
- **Provenance:** demoted_confounded

`study_design_info/intervention_model` has no concrete causal mechanism that sets `eligibility/maximum_age`. Trial size, eligible population, calendar start date, site geography and the free-text title are not directly caused by `study_design_info/intervention_model`; the association is a jointly-chosen-design / sponsor-footprint / secular-trend confound. (R9: spurious design->planning/eligibility.)
