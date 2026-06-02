# study_design_info/masking

- **Group:** `design_top`
- **Dtype:** categorical
- **Description:** Blinding level: None (Open Label) / Single / Double / Triple / Quadruple, with the masked role(s) listed in parentheses.
- **Associated partners (from `association.md`):** 58
  - Direct **causes** (parents of this feature): **1**
  - Direct **effects** (children of this feature): **9**
  - Associated but **no direct** causal edge: **48**

This per-feature file enumerates only **associated** partners. All other columns in `DAG.json` were ruled independent in the Stage-1 association screen and do not appear here. See `association.md` for the screen.

---

## Direct causes (1)

### `phase`

- **Association:** effect = 0.161 (cramers_v), n_valid = 75,043
- **Mechanism:** `design_choice`
- **Provenance:** explicit

Phase 1 trials are commonly Open Label; Phase 3 confirmatory trials are commonly Double / Quadruple blinded. Phase drives the masking choice.

---

## Direct effects (9)

### `MaskingType-Participant`

- **Association:** effect = 1.000 (eta), n_valid = 75,043
- **Mechanism:** `deterministic`
- **Provenance:** explicit

Indicator is 1 iff 'Participant' appears in the parenthesised role list of the masking string.

### `MaskingType-Care Provider`

- **Association:** effect = 1.000 (eta), n_valid = 75,043
- **Mechanism:** `deterministic`
- **Provenance:** explicit

Indicator is 1 iff 'Care Provider' appears in the parenthesised role list of the masking string.

### `MaskingType-Investigator`

- **Association:** effect = 1.000 (eta), n_valid = 75,043
- **Mechanism:** `deterministic`
- **Provenance:** explicit

Indicator is 1 iff 'Investigator' appears in the parenthesised role list of the masking string.

### `MaskingType-Outcomes Assessor`

- **Association:** effect = 1.000 (eta), n_valid = 75,043
- **Mechanism:** `deterministic`
- **Provenance:** explicit

Indicator is 1 iff 'Outcomes Assessor' appears in the parenthesised role list of the masking string.

### `study_design_info/masking_num`

- **Association:** effect = 1.000 (eta), n_valid = 75,043
- **Mechanism:** `deterministic`
- **Provenance:** explicit

masking_num is the count of masked roles encoded in the masking string.

### `approval_outcome`

- **Association:** effect = 0.147 (eta), n_valid = 24,224
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Sponsor design decision (study_design_info/masking) that influences the trial-success label (approval_outcome) through the trial's biological and regulatory pathway.

### `execution_fail`

- **Association:** effect = 0.124 (eta), n_valid = 52,422
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Sponsor design decision (study_design_info/masking) that influences the trial-success label (execution_fail) through the trial's biological and regulatory pathway.

### `execution_pass`

- **Association:** effect = 0.124 (eta), n_valid = 52,422
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Sponsor design decision (study_design_info/masking) that influences the trial-success label (execution_pass) through the trial's biological and regulatory pathway.

### `failure_reason`

- **Association:** effect = 0.058 (cramers_v), n_valid = 20,495
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Sponsor design decision (study_design_info/masking) that influences the trial-success label (failure_reason) through the trial's biological and regulatory pathway.

---

## Associated but no direct causal edge (48)

### `Placebo Comparator Arm Number`

- **Association:** effect = 0.616 (eta), n_valid = 72,860
- **Provenance:** demoted_confounded

`Placebo Comparator Arm Number` is a deterministic descendant of its single definitional design parent; `study_design_info/masking` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `study_design_info/allocation`

- **Association:** effect = 0.488 (cramers_v), n_valid = 56,864
- **Provenance:** explicit

Both methodological choices made jointly; no direct arrow.

### `sae_rate`

- **Association:** effect = 0.313 (eta), n_valid = 17,890
- **Provenance:** demoted_confounded

`study_design_info/masking` is a sponsor / methodology design choice with no direct biological pathway to the realised safety rate `sae_rate`; the association is confounded through `intervention/intervention_type` and `condition` (what is being studied), which carry the genuine safety edges. (R4: confounded design->safety.)

### `number_of_arms`

- **Association:** effect = 0.293 (eta), n_valid = 72,860
- **Provenance:** demoted_confounded

`number_of_arms` is a deterministic descendant of its single definitional design parent; `study_design_info/masking` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `study_design_info/intervention_model`

- **Association:** effect = 0.282 (cramers_v), n_valid = 74,651
- **Provenance:** explicit

Both methodological choices made jointly; no direct arrow at this DAG resolution.

### `mortality_rate`

- **Association:** effect = 0.279 (eta), n_valid = 17,890
- **Provenance:** demoted_confounded

`study_design_info/masking` is a sponsor / methodology design choice with no direct biological pathway to the realised safety rate `mortality_rate`; the association is confounded through `intervention/intervention_type` and `condition` (what is being studied), which carry the genuine safety edges. (R4: confounded design->safety.)

### `Active Comparator Arm Number`

- **Association:** effect = 0.201 (eta), n_valid = 64,055
- **Provenance:** demoted_confounded

`Active Comparator Arm Number` is a deterministic descendant of its single definitional design parent; `study_design_info/masking` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `mortality_YN`

- **Association:** effect = 0.189 (eta), n_valid = 17,890
- **Provenance:** demoted_confounded

`study_design_info/masking` is a sponsor / methodology design choice with no direct biological pathway to the realised safety rate `mortality_YN`; the association is confounded through `intervention/intervention_type` and `condition` (what is being studied), which carry the genuine safety edges. (R4: confounded design->safety.)

### `completion_date`

- **Association:** effect = 0.182 (eta), n_valid = 42,635
- **Provenance:** demoted_confounded

`study_design_info/masking` affects the trial timeline only through `enrollment` / `study_design_info/intervention_model`, the direct parents of trial duration; the marginal association with `completion_date` is mediated, not direct. (R5: mediated design->timing.)

### `Drug intervention Number`

- **Association:** effect = 0.178 (eta), n_valid = 75,043
- **Provenance:** demoted_confounded

`Drug intervention Number` is a deterministic descendant of its single definitional design parent; `study_design_info/masking` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `start_date`

- **Association:** effect = 0.173 (eta), n_valid = 42,635
- **Provenance:** demoted_confounded

`study_design_info/masking` has no concrete causal mechanism that sets `start_date`. Trial size, eligible population, calendar start date, site geography and the free-text title are not directly caused by `study_design_info/masking`; the association is a jointly-chosen-design / sponsor-footprint / secular-trend confound. (R9: spurious design->planning/eligibility.)

### `dropout_rate`

- **Association:** effect = 0.156 (eta), n_valid = 38,218
- **Provenance:** demoted_confounded

`study_design_info/masking` is a sponsor / methodology design choice with no direct biological pathway to the realised safety rate `dropout_rate`; the association is confounded through `intervention/intervention_type` and `condition` (what is being studied), which carry the genuine safety edges. (R4: confounded design->safety.)

### `duration_year`

- **Association:** effect = 0.156 (eta), n_valid = 42,635
- **Provenance:** demoted_confounded

`study_design_info/masking` affects the trial timeline only through `enrollment` / `study_design_info/intervention_model`, the direct parents of trial duration; the marginal association with `duration_year` is mediated, not direct. (R5: mediated design->timing.)

### `duration_day`

- **Association:** effect = 0.156 (eta), n_valid = 42,635
- **Provenance:** demoted_confounded

`study_design_info/masking` affects the trial timeline only through `enrollment` / `study_design_info/intervention_model`, the direct parents of trial duration; the marginal association with `duration_day` is mediated, not direct. (R5: mediated design->timing.)

### `duration_month`

- **Association:** effect = 0.155 (eta), n_valid = 42,635
- **Provenance:** demoted_confounded

`study_design_info/masking` affects the trial timeline only through `enrollment` / `study_design_info/intervention_model`, the direct parents of trial duration; the marginal association with `duration_month` is mediated, not direct. (R5: mediated design->timing.)

### `sae_YN`

- **Association:** effect = 0.154 (eta), n_valid = 17,890
- **Provenance:** demoted_confounded

`study_design_info/masking` is a sponsor / methodology design choice with no direct biological pathway to the realised safety rate `sae_YN`; the association is confounded through `intervention/intervention_type` and `condition` (what is being studied), which carry the genuine safety edges. (R4: confounded design->safety.)

### `dropout_YN`

- **Association:** effect = 0.151 (eta), n_valid = 38,218
- **Provenance:** demoted_confounded

`study_design_info/masking` is a sponsor / methodology design choice with no direct biological pathway to the realised safety rate `dropout_YN`; the association is confounded through `intervention/intervention_type` and `condition` (what is being studied), which carry the genuine safety edges. (R4: confounded design->safety.)

### `sponsors/lead_sponsor/agency_class`

- **Association:** effect = 0.138 (cramers_v), n_valid = 64,727
- **Provenance:** explicit

Both jointly chosen; sponsor class doesn't directly constrain masking choice.

### `intervention/intervention_name`

- **Association:** effect = 0.136 (eta), n_valid = 75,043
- **Provenance:** explicit

Both jointly chosen sponsor design decisions; no direct arrow.

### `Sham Comparator Arm Number`

- **Association:** effect = 0.135 (eta), n_valid = 64,055
- **Provenance:** demoted_confounded

`Sham Comparator Arm Number` is a deterministic descendant of its single definitional design parent; `study_design_info/masking` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `No Intervention Arm Number`

- **Association:** effect = 0.134 (eta), n_valid = 64,055
- **Provenance:** demoted_confounded

`No Intervention Arm Number` is a deterministic descendant of its single definitional design parent; `study_design_info/masking` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `Device intervention Number`

- **Association:** effect = 0.132 (eta), n_valid = 64,727
- **Provenance:** demoted_confounded

`Device intervention Number` is a deterministic descendant of its single definitional design parent; `study_design_info/masking` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `Behavioral intervention Number`

- **Association:** effect = 0.132 (eta), n_valid = 75,043
- **Provenance:** demoted_confounded

`Behavioral intervention Number` is a deterministic descendant of its single definitional design parent; `study_design_info/masking` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `responsible_party/responsible_party_type`

- **Association:** effect = 0.131 (cramers_v), n_valid = 63,064
- **Provenance:** demoted_confounded

`study_design_info/masking` has no direct mechanism that sets the oversight / policy field `responsible_party/responsible_party_type`; the association is confounded through sponsor class and trial type. (R8: confounded ->design_oversight.)

### `patient_data/sharing_ipd`

- **Association:** effect = 0.124 (cramers_v), n_valid = 12,943
- **Provenance:** demoted_confounded

`study_design_info/masking` has no direct mechanism that sets the oversight / policy field `patient_data/sharing_ipd`; the association is confounded through sponsor class and trial type. (R8: confounded ->design_oversight.)

### `oversight_info/is_fda_regulated_device`

- **Association:** effect = 0.117 (cramers_v), n_valid = 13,530
- **Provenance:** demoted_confounded

`study_design_info/masking` has no direct mechanism that sets the oversight / policy field `oversight_info/is_fda_regulated_device`; the association is confounded through sponsor class and trial type. (R8: confounded ->design_oversight.)

### `location/facility/address/city`

- **Association:** effect = 0.116 (eta), n_valid = 75,043
- **Provenance:** demoted_confounded

`study_design_info/masking` has no concrete causal mechanism that sets `location/facility/address/city`. Trial size, eligible population, calendar start date, site geography and the free-text title are not directly caused by `study_design_info/masking`; the association is a jointly-chosen-design / sponsor-footprint / secular-trend confound. (R9: spurious design->planning/eligibility.)

### `Radiation intervention Number`

- **Association:** effect = 0.115 (eta), n_valid = 75,043
- **Provenance:** demoted_confounded

`Radiation intervention Number` is a deterministic descendant of its single definitional design parent; `study_design_info/masking` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `intervention_browse/mesh_term`

- **Association:** effect = 0.110 (eta), n_valid = 75,043
- **Provenance:** demoted_confounded

`intervention_browse/mesh_term` is a deterministic descendant of its single definitional design parent; `study_design_info/masking` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `eligibility/healthy_volunteers`

- **Association:** effect = 0.108 (cramers_v), n_valid = 74,940
- **Provenance:** demoted_confounded

`study_design_info/masking` has no concrete causal mechanism that sets `eligibility/healthy_volunteers`. Trial size, eligible population, calendar start date, site geography and the free-text title are not directly caused by `study_design_info/masking`; the association is a jointly-chosen-design / sponsor-footprint / secular-trend confound. (R9: spurious design->planning/eligibility.)

### `oversight_info/has_dmc`

- **Association:** effect = 0.102 (cramers_v), n_valid = 41,228
- **Provenance:** demoted_confounded

`study_design_info/masking` has no direct mechanism that sets the oversight / policy field `oversight_info/has_dmc`; the association is confounded through sponsor class and trial type. (R8: confounded ->design_oversight.)

### `Procedure intervention Number`

- **Association:** effect = 0.101 (eta), n_valid = 64,727
- **Provenance:** demoted_confounded

`Procedure intervention Number` is a deterministic descendant of its single definitional design parent; `study_design_info/masking` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `eligibility/minimum_age`

- **Association:** effect = 0.095 (eta), n_valid = 73,073
- **Provenance:** demoted_confounded

`study_design_info/masking` has no concrete causal mechanism that sets `eligibility/minimum_age`. Trial size, eligible population, calendar start date, site geography and the free-text title are not directly caused by `study_design_info/masking`; the association is a jointly-chosen-design / sponsor-footprint / secular-trend confound. (R9: spurious design->planning/eligibility.)

### `oversight_info/is_fda_regulated_drug`

- **Association:** effect = 0.094 (cramers_v), n_valid = 13,609
- **Provenance:** demoted_confounded

`study_design_info/masking` has no direct mechanism that sets the oversight / policy field `oversight_info/is_fda_regulated_drug`; the association is confounded through sponsor class and trial type. (R8: confounded ->design_oversight.)

### `Experimental Arm Number`

- **Association:** effect = 0.083 (eta), n_valid = 72,860
- **Provenance:** demoted_confounded

`Experimental Arm Number` is a deterministic descendant of its single definitional design parent; `study_design_info/masking` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `intervention/intervention_type`

- **Association:** effect = 0.080 (eta), n_valid = 75,043
- **Provenance:** explicit

Both jointly chosen design decisions; no direct arrow.

### `condition`

- **Association:** effect = 0.076 (eta), n_valid = 75,043
- **Provenance:** explicit

Both jointly chosen design decisions; no direct arrow.

### `Other intervention Number`

- **Association:** effect = 0.075 (eta), n_valid = 64,727
- **Provenance:** demoted_confounded

`Other intervention Number` is a deterministic descendant of its single definitional design parent; `study_design_info/masking` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `eligibility/maximum_age`

- **Association:** effect = 0.072 (eta), n_valid = 39,233
- **Provenance:** demoted_confounded

`study_design_info/masking` has no concrete causal mechanism that sets `eligibility/maximum_age`. Trial size, eligible population, calendar start date, site geography and the free-text title are not directly caused by `study_design_info/masking`; the association is a jointly-chosen-design / sponsor-footprint / secular-trend confound. (R9: spurious design->planning/eligibility.)

### `icdcode`

- **Association:** effect = 0.063 (eta), n_valid = 75,043
- **Provenance:** demoted_confounded

`icdcode` is a deterministic descendant of its single definitional design parent; `study_design_info/masking` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `condition_browse/mesh_term`

- **Association:** effect = 0.063 (eta), n_valid = 75,043
- **Provenance:** demoted_confounded

`condition_browse/mesh_term` is a deterministic descendant of its single definitional design parent; `study_design_info/masking` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `study_design_info/primary_purpose`

- **Association:** effect = 0.060 (cramers_v), n_valid = 74,379
- **Provenance:** explicit

Both jointly chosen design decisions.

### `Dietary Supplement intervention Number`

- **Association:** effect = 0.059 (eta), n_valid = 75,043
- **Provenance:** demoted_confounded

`Dietary Supplement intervention Number` is a deterministic descendant of its single definitional design parent; `study_design_info/masking` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `smiless`

- **Association:** effect = 0.059 (eta), n_valid = 75,043
- **Provenance:** demoted_confounded

`smiless` is a deterministic descendant of its single definitional design parent; `study_design_info/masking` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `enrollment`

- **Association:** effect = 0.059 (eta), n_valid = 38,225
- **Provenance:** demoted_confounded

`study_design_info/masking` has no concrete causal mechanism that sets `enrollment`. Trial size, eligible population, calendar start date, site geography and the free-text title are not directly caused by `study_design_info/masking`; the association is a jointly-chosen-design / sponsor-footprint / secular-trend confound. (R9: spurious design->planning/eligibility.)

### `eligibility/gender`

- **Association:** effect = 0.057 (cramers_v), n_valid = 64,727
- **Provenance:** demoted_confounded

`study_design_info/masking` has no concrete causal mechanism that sets `eligibility/gender`. Trial size, eligible population, calendar start date, site geography and the free-text title are not directly caused by `study_design_info/masking`; the association is a jointly-chosen-design / sponsor-footprint / secular-trend confound. (R9: spurious design->planning/eligibility.)

### `Other Arm Number`

- **Association:** effect = 0.056 (eta), n_valid = 72,860
- **Provenance:** demoted_confounded

`Other Arm Number` is a deterministic descendant of its single definitional design parent; `study_design_info/masking` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `brief_title`

- **Association:** effect = 0.053 (eta), n_valid = 75,043
- **Provenance:** demoted_confounded

`study_design_info/masking` has no concrete causal mechanism that sets `brief_title`. Trial size, eligible population, calendar start date, site geography and the free-text title are not directly caused by `study_design_info/masking`; the association is a jointly-chosen-design / sponsor-footprint / secular-trend confound. (R9: spurious design->planning/eligibility.)
