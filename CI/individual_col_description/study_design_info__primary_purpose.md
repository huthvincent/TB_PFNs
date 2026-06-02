# study_design_info/primary_purpose

- **Group:** `design_top`
- **Dtype:** categorical
- **Description:** Primary purpose: Treatment / Prevention / Diagnostic / Supportive Care / Screening / Health Services Research / Basic Science / Device Feasibility / Other.
- **Associated partners (from `association.md`):** 55
  - Direct **causes** (parents of this feature): **2**
  - Direct **effects** (children of this feature): **2**
  - Associated but **no direct** causal edge: **51**

This per-feature file enumerates only **associated** partners. All other columns in `DAG.json` were ruled independent in the Stage-1 association screen and do not appear here. See `association.md` for the screen.

---

## Direct causes (2)

### `phase`

- **Association:** effect = 0.194 (cramers_v), n_valid = 80,983
- **Mechanism:** `design_choice`
- **Provenance:** explicit

Phase 1 skews Treatment / Basic Science; Phase 4 picks up Supportive Care / Health Services Research. Phase shifts the typical purpose distribution.

### `condition`

- **Association:** effect = 0.082 (eta), n_valid = 80,983
- **Mechanism:** `design_choice`
- **Provenance:** explicit

The disease being studied directly determines whether a sponsor designs a Treatment, Prevention, Diagnostic, or Screening trial.

---

## Direct effects (2)

### `eligibility/healthy_volunteers`

- **Association:** effect = 0.455 (cramers_v), n_valid = 80,843
- **Mechanism:** `design_choice`
- **Provenance:** default_cross_tier

Sponsor design decision made at registration (study_design_info/primary_purpose) that constrains a downstream design field (eligibility/healthy_volunteers).

### `intervention/intervention_type`

- **Association:** effect = 0.053 (eta), n_valid = 80,983
- **Mechanism:** `design_constraint`
- **Provenance:** explicit

Diagnostic primary purpose forces intervention_type='Diagnostic Test'; Treatment is realised through Drug / Biological / Device / Behavioral / Procedure. Purpose constrains the feasible type set.

---

## Associated but no direct causal edge (51)

### `Biological intervention Number`

- **Association:** effect = 0.330 (eta), n_valid = 80,983
- **Provenance:** demoted_confounded

`Biological intervention Number` is a deterministic descendant of its single definitional design parent; `study_design_info/primary_purpose` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `sae_YN`

- **Association:** effect = 0.280 (eta), n_valid = 17,911
- **Provenance:** demoted_confounded

`study_design_info/primary_purpose` is a sponsor / methodology design choice with no direct biological pathway to the realised safety rate `sae_YN`; the association is confounded through `intervention/intervention_type` and `condition` (what is being studied), which carry the genuine safety edges. (R4: confounded design->safety.)

### `eligibility/maximum_age`

- **Association:** effect = 0.233 (eta), n_valid = 42,342
- **Provenance:** demoted_confounded

`study_design_info/primary_purpose` has no concrete causal mechanism that sets `eligibility/maximum_age`. Trial size, eligible population, calendar start date, site geography and the free-text title are not directly caused by `study_design_info/primary_purpose`; the association is a jointly-chosen-design / sponsor-footprint / secular-trend confound. (R9: spurious design->planning/eligibility.)

### `sae_rate`

- **Association:** effect = 0.208 (eta), n_valid = 17,911
- **Provenance:** demoted_confounded

`study_design_info/primary_purpose` is a sponsor / methodology design choice with no direct biological pathway to the realised safety rate `sae_rate`; the association is confounded through `intervention/intervention_type` and `condition` (what is being studied), which carry the genuine safety edges. (R4: confounded design->safety.)

### `mortality_YN`

- **Association:** effect = 0.198 (eta), n_valid = 17,911
- **Provenance:** demoted_confounded

`study_design_info/primary_purpose` is a sponsor / methodology design choice with no direct biological pathway to the realised safety rate `mortality_YN`; the association is confounded through `intervention/intervention_type` and `condition` (what is being studied), which carry the genuine safety edges. (R4: confounded design->safety.)

### `duration_month`

- **Association:** effect = 0.195 (eta), n_valid = 42,836
- **Provenance:** demoted_confounded

`study_design_info/primary_purpose` affects the trial timeline only through `enrollment` / `study_design_info/intervention_model`, the direct parents of trial duration; the marginal association with `duration_month` is mediated, not direct. (R5: mediated design->timing.)

### `duration_day`

- **Association:** effect = 0.195 (eta), n_valid = 42,836
- **Provenance:** demoted_confounded

`study_design_info/primary_purpose` affects the trial timeline only through `enrollment` / `study_design_info/intervention_model`, the direct parents of trial duration; the marginal association with `duration_day` is mediated, not direct. (R5: mediated design->timing.)

### `duration_year`

- **Association:** effect = 0.195 (eta), n_valid = 42,836
- **Provenance:** demoted_confounded

`study_design_info/primary_purpose` affects the trial timeline only through `enrollment` / `study_design_info/intervention_model`, the direct parents of trial duration; the marginal association with `duration_year` is mediated, not direct. (R5: mediated design->timing.)

### `Drug intervention Number`

- **Association:** effect = 0.179 (eta), n_valid = 80,983
- **Provenance:** demoted_confounded

`Drug intervention Number` is a deterministic descendant of its single definitional design parent; `study_design_info/primary_purpose` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `mortality_rate`

- **Association:** effect = 0.169 (eta), n_valid = 17,911
- **Provenance:** demoted_confounded

`study_design_info/primary_purpose` is a sponsor / methodology design choice with no direct biological pathway to the realised safety rate `mortality_rate`; the association is confounded through `intervention/intervention_type` and `condition` (what is being studied), which carry the genuine safety edges. (R4: confounded design->safety.)

### `dropout_YN`

- **Association:** effect = 0.167 (eta), n_valid = 37,812
- **Provenance:** demoted_confounded

`study_design_info/primary_purpose` is a sponsor / methodology design choice with no direct biological pathway to the realised safety rate `dropout_YN`; the association is confounded through `intervention/intervention_type` and `condition` (what is being studied), which carry the genuine safety edges. (R4: confounded design->safety.)

### `dropout_rate`

- **Association:** effect = 0.164 (eta), n_valid = 37,812
- **Provenance:** demoted_confounded

`study_design_info/primary_purpose` is a sponsor / methodology design choice with no direct biological pathway to the realised safety rate `dropout_rate`; the association is confounded through `intervention/intervention_type` and `condition` (what is being studied), which carry the genuine safety edges. (R4: confounded design->safety.)

### `condition_browse/mesh_term`

- **Association:** effect = 0.162 (eta), n_valid = 80,983
- **Provenance:** demoted_confounded

`condition_browse/mesh_term` is a deterministic descendant of its single definitional design parent; `study_design_info/primary_purpose` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `study_design_info/intervention_model`

- **Association:** effect = 0.142 (cramers_v), n_valid = 80,137
- **Provenance:** explicit

Both jointly chosen; primary purpose doesn't strictly constrain intervention model.

### `oversight_info/has_dmc`

- **Association:** effect = 0.125 (cramers_v), n_valid = 45,283
- **Provenance:** demoted_confounded

`study_design_info/primary_purpose` has no direct mechanism that sets the oversight / policy field `oversight_info/has_dmc`; the association is confounded through sponsor class and trial type. (R8: confounded ->design_oversight.)

### `patient_data/sharing_ipd`

- **Association:** effect = 0.125 (cramers_v), n_valid = 13,490
- **Provenance:** demoted_confounded

`study_design_info/primary_purpose` has no direct mechanism that sets the oversight / policy field `patient_data/sharing_ipd`; the association is confounded through sponsor class and trial type. (R8: confounded ->design_oversight.)

### `study_design_info/masking_num`

- **Association:** effect = 0.121 (eta), n_valid = 80,406
- **Provenance:** demoted_confounded

`study_design_info/masking_num` is a deterministic descendant of its single definitional design parent; `study_design_info/primary_purpose` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `start_date`

- **Association:** effect = 0.119 (eta), n_valid = 42,836
- **Provenance:** demoted_confounded

`study_design_info/primary_purpose` has no concrete causal mechanism that sets `start_date`. Trial size, eligible population, calendar start date, site geography and the free-text title are not directly caused by `study_design_info/primary_purpose`; the association is a jointly-chosen-design / sponsor-footprint / secular-trend confound. (R9: spurious design->planning/eligibility.)

### `execution_pass`

- **Association:** effect = 0.119 (eta), n_valid = 52,095
- **Provenance:** demoted_confounded

`study_design_info/primary_purpose` reaches the trial-success label `execution_pass` only through biology / efficacy and enrollment mediators already in the DAG (`biology_pass`, `failure_reason`, `enrollment`); no direct arrow. (R6: mediated design->label.)

### `execution_fail`

- **Association:** effect = 0.119 (eta), n_valid = 52,095
- **Provenance:** demoted_confounded

`study_design_info/primary_purpose` reaches the trial-success label `execution_fail` only through biology / efficacy and enrollment mediators already in the DAG (`biology_pass`, `failure_reason`, `enrollment`); no direct arrow. (R6: mediated design->label.)

### `oversight_info/is_fda_regulated_device`

- **Association:** effect = 0.116 (cramers_v), n_valid = 13,675
- **Provenance:** demoted_confounded

`study_design_info/primary_purpose` has no direct mechanism that sets the oversight / policy field `oversight_info/is_fda_regulated_device`; the association is confounded through sponsor class and trial type. (R8: confounded ->design_oversight.)

### `MaskingType-Participant`

- **Association:** effect = 0.115 (eta), n_valid = 80,406
- **Provenance:** demoted_confounded

`MaskingType-Participant` is a deterministic descendant of its single definitional design parent; `study_design_info/primary_purpose` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `number_of_arms`

- **Association:** effect = 0.114 (eta), n_valid = 77,416
- **Provenance:** demoted_confounded

`number_of_arms` is a deterministic descendant of its single definitional design parent; `study_design_info/primary_purpose` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `enrollment`

- **Association:** effect = 0.107 (eta), n_valid = 43,857
- **Provenance:** demoted_confounded

`study_design_info/primary_purpose` has no concrete causal mechanism that sets `enrollment`. Trial size, eligible population, calendar start date, site geography and the free-text title are not directly caused by `study_design_info/primary_purpose`; the association is a jointly-chosen-design / sponsor-footprint / secular-trend confound. (R9: spurious design->planning/eligibility.)

### `approval_outcome`

- **Association:** effect = 0.107 (eta), n_valid = 30,383
- **Provenance:** demoted_confounded

`study_design_info/primary_purpose` reaches the trial-success label `approval_outcome` only through biology / efficacy and enrollment mediators already in the DAG (`biology_pass`, `failure_reason`, `enrollment`); no direct arrow. (R6: mediated design->label.)

### `study_design_info/allocation`

- **Association:** effect = 0.105 (cramers_v), n_valid = 61,425
- **Provenance:** explicit

Both jointly chosen design decisions.

### `smiless`

- **Association:** effect = 0.104 (eta), n_valid = 80,983
- **Provenance:** demoted_confounded

`smiless` is a deterministic descendant of its single definitional design parent; `study_design_info/primary_purpose` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `MaskingType-Investigator`

- **Association:** effect = 0.103 (eta), n_valid = 80,406
- **Provenance:** demoted_confounded

`MaskingType-Investigator` is a deterministic descendant of its single definitional design parent; `study_design_info/primary_purpose` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `MaskingType-Care Provider`

- **Association:** effect = 0.100 (eta), n_valid = 80,406
- **Provenance:** demoted_confounded

`MaskingType-Care Provider` is a deterministic descendant of its single definitional design parent; `study_design_info/primary_purpose` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `oversight_info/is_fda_regulated_drug`

- **Association:** effect = 0.099 (cramers_v), n_valid = 13,761
- **Provenance:** demoted_confounded

`study_design_info/primary_purpose` has no direct mechanism that sets the oversight / policy field `oversight_info/is_fda_regulated_drug`; the association is confounded through sponsor class and trial type. (R8: confounded ->design_oversight.)

### `MaskingType-Outcomes Assessor`

- **Association:** effect = 0.097 (eta), n_valid = 80,406
- **Provenance:** demoted_confounded

`MaskingType-Outcomes Assessor` is a deterministic descendant of its single definitional design parent; `study_design_info/primary_purpose` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `eligibility/gender`

- **Association:** effect = 0.097 (cramers_v), n_valid = 70,604
- **Provenance:** demoted_confounded

`study_design_info/primary_purpose` has no concrete causal mechanism that sets `eligibility/gender`. Trial size, eligible population, calendar start date, site geography and the free-text title are not directly caused by `study_design_info/primary_purpose`; the association is a jointly-chosen-design / sponsor-footprint / secular-trend confound. (R9: spurious design->planning/eligibility.)

### `intervention_browse/mesh_term`

- **Association:** effect = 0.094 (eta), n_valid = 80,983
- **Provenance:** demoted_confounded

`intervention_browse/mesh_term` is a deterministic descendant of its single definitional design parent; `study_design_info/primary_purpose` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `Experimental Arm Number`

- **Association:** effect = 0.092 (eta), n_valid = 77,416
- **Provenance:** demoted_confounded

`Experimental Arm Number` is a deterministic descendant of its single definitional design parent; `study_design_info/primary_purpose` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `sponsors/lead_sponsor/agency_class`

- **Association:** effect = 0.090 (cramers_v), n_valid = 70,604
- **Provenance:** explicit

Both jointly chosen.

### `Dietary Supplement intervention Number`

- **Association:** effect = 0.089 (eta), n_valid = 80,983
- **Provenance:** demoted_confounded

`Dietary Supplement intervention Number` is a deterministic descendant of its single definitional design parent; `study_design_info/primary_purpose` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `icdcode`

- **Association:** effect = 0.087 (eta), n_valid = 80,983
- **Provenance:** demoted_confounded

`icdcode` is a deterministic descendant of its single definitional design parent; `study_design_info/primary_purpose` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `Device intervention Number`

- **Association:** effect = 0.087 (eta), n_valid = 70,604
- **Provenance:** demoted_confounded

`Device intervention Number` is a deterministic descendant of its single definitional design parent; `study_design_info/primary_purpose` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `Active Comparator Arm Number`

- **Association:** effect = 0.085 (eta), n_valid = 68,722
- **Provenance:** demoted_confounded

`Active Comparator Arm Number` is a deterministic descendant of its single definitional design parent; `study_design_info/primary_purpose` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `location/facility/address/city`

- **Association:** effect = 0.084 (eta), n_valid = 80,983
- **Provenance:** demoted_confounded

`study_design_info/primary_purpose` has no concrete causal mechanism that sets `location/facility/address/city`. Trial size, eligible population, calendar start date, site geography and the free-text title are not directly caused by `study_design_info/primary_purpose`; the association is a jointly-chosen-design / sponsor-footprint / secular-trend confound. (R9: spurious design->planning/eligibility.)

### `Diagnostic Test intervention Number`

- **Association:** effect = 0.083 (eta), n_valid = 70,604
- **Provenance:** demoted_confounded

`Diagnostic Test intervention Number` is a deterministic descendant of its single definitional design parent; `study_design_info/primary_purpose` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `Other Arm Number`

- **Association:** effect = 0.082 (eta), n_valid = 77,416
- **Provenance:** demoted_confounded

`Other Arm Number` is a deterministic descendant of its single definitional design parent; `study_design_info/primary_purpose` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `No Intervention Arm Number`

- **Association:** effect = 0.078 (eta), n_valid = 68,722
- **Provenance:** demoted_confounded

`No Intervention Arm Number` is a deterministic descendant of its single definitional design parent; `study_design_info/primary_purpose` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `Placebo Comparator Arm Number`

- **Association:** effect = 0.077 (eta), n_valid = 77,416
- **Provenance:** demoted_confounded

`Placebo Comparator Arm Number` is a deterministic descendant of its single definitional design parent; `study_design_info/primary_purpose` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `Other intervention Number`

- **Association:** effect = 0.075 (eta), n_valid = 70,604
- **Provenance:** demoted_confounded

`Other intervention Number` is a deterministic descendant of its single definitional design parent; `study_design_info/primary_purpose` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `responsible_party/responsible_party_type`

- **Association:** effect = 0.069 (cramers_v), n_valid = 67,490
- **Provenance:** demoted_confounded

`study_design_info/primary_purpose` has no direct mechanism that sets the oversight / policy field `responsible_party/responsible_party_type`; the association is confounded through sponsor class and trial type. (R8: confounded ->design_oversight.)

### `Procedure intervention Number`

- **Association:** effect = 0.067 (eta), n_valid = 70,604
- **Provenance:** demoted_confounded

`Procedure intervention Number` is a deterministic descendant of its single definitional design parent; `study_design_info/primary_purpose` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `Behavioral intervention Number`

- **Association:** effect = 0.066 (eta), n_valid = 80,983
- **Provenance:** demoted_confounded

`Behavioral intervention Number` is a deterministic descendant of its single definitional design parent; `study_design_info/primary_purpose` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `study_design_info/masking`

- **Association:** effect = 0.060 (cramers_v), n_valid = 74,379
- **Provenance:** explicit

Both jointly chosen design decisions.

### `Radiation intervention Number`

- **Association:** effect = 0.058 (eta), n_valid = 80,983
- **Provenance:** demoted_confounded

`Radiation intervention Number` is a deterministic descendant of its single definitional design parent; `study_design_info/primary_purpose` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `failure_reason`

- **Association:** effect = 0.055 (cramers_v), n_valid = 20,561
- **Provenance:** demoted_confounded

`study_design_info/primary_purpose` reaches the trial-success label `failure_reason` only through biology / efficacy and enrollment mediators already in the DAG (`biology_pass`, `failure_reason`, `enrollment`); no direct arrow. (R6: mediated design->label.)
