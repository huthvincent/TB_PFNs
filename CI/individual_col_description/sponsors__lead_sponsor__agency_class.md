# sponsors/lead_sponsor/agency_class

- **Group:** `design_top`
- **Dtype:** categorical
- **Description:** Sponsor class: INDUSTRY / NIH / U.S. Fed / OTHER (academic, foundation, hospital).
- **Associated partners (from `association.md`):** 60
  - Direct **causes** (parents of this feature): **0**
  - Direct **effects** (children of this feature): **15**
  - Associated but **no direct** causal edge: **45**

This per-feature file enumerates only **associated** partners. All other columns in `DAG.json` were ruled independent in the Stage-1 association screen and do not appear here. See `association.md` for the screen.

---

## Direct causes (0)

_(none)_

---

## Direct effects (15)

### `ipd_info_type-Clinical Study Report (CSR)`

- **Association:** effect = 0.462 (eta), n_valid = 2,145
- **Mechanism:** `design_choice`
- **Provenance:** default_cross_tier

Sponsor design decision made at registration (sponsors/lead_sponsor/agency_class) that constrains a downstream design field (ipd_info_type-Clinical Study Report (CSR)).

### `ipd_info_type-Statistical Analysis Plan (SAP)`

- **Association:** effect = 0.433 (eta), n_valid = 2,145
- **Mechanism:** `design_choice`
- **Provenance:** default_cross_tier

Sponsor design decision made at registration (sponsors/lead_sponsor/agency_class) that constrains a downstream design field (ipd_info_type-Statistical Analysis Plan (SAP)).

### `responsible_party/responsible_party_type`

- **Association:** effect = 0.420 (cramers_v), n_valid = 67,878
- **Mechanism:** `design_choice`
- **Provenance:** default_cross_tier

Sponsor design decision made at registration (sponsors/lead_sponsor/agency_class) that constrains a downstream design field (responsible_party/responsible_party_type).

### `patient_data/sharing_ipd`

- **Association:** effect = 0.319 (cramers_v), n_valid = 13,510
- **Mechanism:** `design_choice`
- **Provenance:** default_cross_tier

Sponsor design decision made at registration (sponsors/lead_sponsor/agency_class) that constrains a downstream design field (patient_data/sharing_ipd).

### `duration_month`

- **Association:** effect = 0.282 (eta), n_valid = 42,855
- **Mechanism:** `design_choice`
- **Provenance:** default_cross_tier

Sponsor design decision (sponsors/lead_sponsor/agency_class) that drives the realised trial-duration timeline (duration_month).

### `duration_year`

- **Association:** effect = 0.282 (eta), n_valid = 42,855
- **Mechanism:** `design_choice`
- **Provenance:** default_cross_tier

Sponsor design decision (sponsors/lead_sponsor/agency_class) that drives the realised trial-duration timeline (duration_year).

### `duration_day`

- **Association:** effect = 0.282 (eta), n_valid = 42,855
- **Mechanism:** `design_choice`
- **Provenance:** default_cross_tier

Sponsor design decision (sponsors/lead_sponsor/agency_class) that drives the realised trial-duration timeline (duration_day).

### `approval_outcome`

- **Association:** effect = 0.275 (eta), n_valid = 24,108
- **Mechanism:** `regulatory`
- **Provenance:** explicit

Industry trials are designed-for-approval; academic / NIH trials less often pursue or attain regulatory approval.

### `oversight_info/has_dmc`

- **Association:** effect = 0.261 (cramers_v), n_valid = 37,612
- **Mechanism:** `design_choice`
- **Provenance:** default_cross_tier

Sponsor design decision made at registration (sponsors/lead_sponsor/agency_class) that constrains a downstream design field (oversight_info/has_dmc).

### `ipd_info_type-Study Protocol`

- **Association:** effect = 0.227 (eta), n_valid = 2,145
- **Mechanism:** `design_choice`
- **Provenance:** default_cross_tier

Sponsor design decision made at registration (sponsors/lead_sponsor/agency_class) that constrains a downstream design field (ipd_info_type-Study Protocol).

### `ipd_info_type-Analytic Code`

- **Association:** effect = 0.205 (eta), n_valid = 2,145
- **Mechanism:** `design_choice`
- **Provenance:** default_cross_tier

Sponsor design decision made at registration (sponsors/lead_sponsor/agency_class) that constrains a downstream design field (ipd_info_type-Analytic Code).

### `ipd_info_type-Informed Consent Form (ICF)`

- **Association:** effect = 0.162 (eta), n_valid = 2,145
- **Mechanism:** `design_choice`
- **Provenance:** default_cross_tier

Sponsor design decision made at registration (sponsors/lead_sponsor/agency_class) that constrains a downstream design field (ipd_info_type-Informed Consent Form (ICF)).

### `completion_date`

- **Association:** effect = 0.103 (eta), n_valid = 42,855
- **Mechanism:** `design_choice`
- **Provenance:** default_cross_tier

Sponsor design decision (sponsors/lead_sponsor/agency_class) that drives the realised trial-duration timeline (completion_date).

### `oversight_info/is_fda_regulated_drug`

- **Association:** effect = 0.080 (cramers_v), n_valid = 11,339
- **Mechanism:** `design_choice`
- **Provenance:** default_cross_tier

Sponsor design decision made at registration (sponsors/lead_sponsor/agency_class) that constrains a downstream design field (oversight_info/is_fda_regulated_drug).

### `has_expanded_access`

- **Association:** effect = 0.069 (cramers_v), n_valid = 70,125
- **Mechanism:** `design_choice`
- **Provenance:** default_cross_tier

Sponsor design decision made at registration (sponsors/lead_sponsor/agency_class) that constrains a downstream design field (has_expanded_access).

---

## Associated but no direct causal edge (45)

### `sae_YN`

- **Association:** effect = 0.287 (eta), n_valid = 17,916
- **Provenance:** demoted_confounded

`sponsors/lead_sponsor/agency_class` is a sponsor / methodology design choice with no direct biological pathway to the realised safety rate `sae_YN`; the association is confounded through `intervention/intervention_type` and `condition` (what is being studied), which carry the genuine safety edges. (R4: confounded design->safety.)

### `Experimental Arm Number`

- **Association:** effect = 0.247 (eta), n_valid = 69,293
- **Provenance:** demoted_confounded

`Experimental Arm Number` is a deterministic descendant of its single definitional design parent; `sponsors/lead_sponsor/agency_class` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `dropout_YN`

- **Association:** effect = 0.213 (eta), n_valid = 38,302
- **Provenance:** demoted_confounded

`sponsors/lead_sponsor/agency_class` is a sponsor / methodology design choice with no direct biological pathway to the realised safety rate `dropout_YN`; the association is confounded through `intervention/intervention_type` and `condition` (what is being studied), which carry the genuine safety edges. (R4: confounded design->safety.)

### `phase`

- **Association:** effect = 0.207 (cramers_v), n_valid = 71,221
- **Provenance:** explicit

Both jointly chosen at trial registration; correlated via drug-development economics but no direct arrow.

### `number_of_arms`

- **Association:** effect = 0.198 (eta), n_valid = 69,293
- **Provenance:** demoted_confounded

`number_of_arms` is a deterministic descendant of its single definitional design parent; `sponsors/lead_sponsor/agency_class` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `Other intervention Number`

- **Association:** effect = 0.185 (eta), n_valid = 71,221
- **Provenance:** demoted_confounded

`Other intervention Number` is a deterministic descendant of its single definitional design parent; `sponsors/lead_sponsor/agency_class` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `condition`

- **Association:** effect = 0.177 (eta), n_valid = 71,221
- **Provenance:** explicit

Both jointly chosen; sponsors specialise in indication portfolios but neither column directly causes the other.

### `location/facility/address/city`

- **Association:** effect = 0.174 (eta), n_valid = 71,221
- **Provenance:** demoted_confounded

`sponsors/lead_sponsor/agency_class` has no concrete causal mechanism that sets `location/facility/address/city`. Trial size, eligible population, calendar start date, site geography and the free-text title are not directly caused by `sponsors/lead_sponsor/agency_class`; the association is a jointly-chosen-design / sponsor-footprint / secular-trend confound. (R9: spurious design->planning/eligibility.)

### `intervention_browse/mesh_term`

- **Association:** effect = 0.174 (eta), n_valid = 71,221
- **Provenance:** demoted_confounded

`intervention_browse/mesh_term` is a deterministic descendant of its single definitional design parent; `sponsors/lead_sponsor/agency_class` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `failure_reason`

- **Association:** effect = 0.169 (cramers_v), n_valid = 10,204
- **Provenance:** demoted_confounded

`sponsors/lead_sponsor/agency_class` reaches the trial-success label `failure_reason` only through biology / efficacy and enrollment mediators already in the DAG (`biology_pass`, `failure_reason`, `enrollment`); no direct arrow. (R6: mediated design->label.)

### `MaskingType-Investigator`

- **Association:** effect = 0.153 (eta), n_valid = 70,854
- **Provenance:** demoted_confounded

`MaskingType-Investigator` is a deterministic descendant of its single definitional design parent; `sponsors/lead_sponsor/agency_class` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `Procedure intervention Number`

- **Association:** effect = 0.149 (eta), n_valid = 71,221
- **Provenance:** demoted_confounded

`Procedure intervention Number` is a deterministic descendant of its single definitional design parent; `sponsors/lead_sponsor/agency_class` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `execution_fail`

- **Association:** effect = 0.145 (eta), n_valid = 42,207
- **Provenance:** demoted_confounded

`sponsors/lead_sponsor/agency_class` reaches the trial-success label `execution_fail` only through biology / efficacy and enrollment mediators already in the DAG (`biology_pass`, `failure_reason`, `enrollment`); no direct arrow. (R6: mediated design->label.)

### `execution_pass`

- **Association:** effect = 0.145 (eta), n_valid = 42,207
- **Provenance:** demoted_confounded

`sponsors/lead_sponsor/agency_class` reaches the trial-success label `execution_pass` only through biology / efficacy and enrollment mediators already in the DAG (`biology_pass`, `failure_reason`, `enrollment`); no direct arrow. (R6: mediated design->label.)

### `icdcode`

- **Association:** effect = 0.144 (eta), n_valid = 71,221
- **Provenance:** demoted_confounded

`icdcode` is a deterministic descendant of its single definitional design parent; `sponsors/lead_sponsor/agency_class` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `study_design_info/masking`

- **Association:** effect = 0.138 (cramers_v), n_valid = 64,727
- **Provenance:** explicit

Both jointly chosen; sponsor class doesn't directly constrain masking choice.

### `No Intervention Arm Number`

- **Association:** effect = 0.137 (eta), n_valid = 69,293
- **Provenance:** demoted_confounded

`No Intervention Arm Number` is a deterministic descendant of its single definitional design parent; `sponsors/lead_sponsor/agency_class` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `Radiation intervention Number`

- **Association:** effect = 0.134 (eta), n_valid = 71,221
- **Provenance:** demoted_confounded

`Radiation intervention Number` is a deterministic descendant of its single definitional design parent; `sponsors/lead_sponsor/agency_class` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `condition_browse/mesh_term`

- **Association:** effect = 0.129 (eta), n_valid = 71,221
- **Provenance:** demoted_confounded

`condition_browse/mesh_term` is a deterministic descendant of its single definitional design parent; `sponsors/lead_sponsor/agency_class` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `Behavioral intervention Number`

- **Association:** effect = 0.128 (eta), n_valid = 71,221
- **Provenance:** demoted_confounded

`Behavioral intervention Number` is a deterministic descendant of its single definitional design parent; `sponsors/lead_sponsor/agency_class` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `study_design_info/masking_num`

- **Association:** effect = 0.118 (eta), n_valid = 70,854
- **Provenance:** demoted_confounded

`study_design_info/masking_num` is a deterministic descendant of its single definitional design parent; `sponsors/lead_sponsor/agency_class` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `MaskingType-Participant`

- **Association:** effect = 0.118 (eta), n_valid = 70,854
- **Provenance:** demoted_confounded

`MaskingType-Participant` is a deterministic descendant of its single definitional design parent; `sponsors/lead_sponsor/agency_class` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `Active Comparator Arm Number`

- **Association:** effect = 0.116 (eta), n_valid = 69,293
- **Provenance:** demoted_confounded

`Active Comparator Arm Number` is a deterministic descendant of its single definitional design parent; `sponsors/lead_sponsor/agency_class` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `dropout_rate`

- **Association:** effect = 0.115 (eta), n_valid = 38,302
- **Provenance:** demoted_confounded

`sponsors/lead_sponsor/agency_class` is a sponsor / methodology design choice with no direct biological pathway to the realised safety rate `dropout_rate`; the association is confounded through `intervention/intervention_type` and `condition` (what is being studied), which carry the genuine safety edges. (R4: confounded design->safety.)

### `brief_title`

- **Association:** effect = 0.113 (eta), n_valid = 71,221
- **Provenance:** demoted_confounded

`sponsors/lead_sponsor/agency_class` has no concrete causal mechanism that sets `brief_title`. Trial size, eligible population, calendar start date, site geography and the free-text title are not directly caused by `sponsors/lead_sponsor/agency_class`; the association is a jointly-chosen-design / sponsor-footprint / secular-trend confound. (R9: spurious design->planning/eligibility.)

### `eligibility/healthy_volunteers`

- **Association:** effect = 0.112 (cramers_v), n_valid = 71,109
- **Provenance:** demoted_confounded

`sponsors/lead_sponsor/agency_class` has no concrete causal mechanism that sets `eligibility/healthy_volunteers`. Trial size, eligible population, calendar start date, site geography and the free-text title are not directly caused by `sponsors/lead_sponsor/agency_class`; the association is a jointly-chosen-design / sponsor-footprint / secular-trend confound. (R9: spurious design->planning/eligibility.)

### `mortality_rate`

- **Association:** effect = 0.111 (eta), n_valid = 17,916
- **Provenance:** demoted_confounded

`sponsors/lead_sponsor/agency_class` is a sponsor / methodology design choice with no direct biological pathway to the realised safety rate `mortality_rate`; the association is confounded through `intervention/intervention_type` and `condition` (what is being studied), which carry the genuine safety edges. (R4: confounded design->safety.)

### `sae_rate`

- **Association:** effect = 0.110 (eta), n_valid = 17,916
- **Provenance:** demoted_confounded

`sponsors/lead_sponsor/agency_class` is a sponsor / methodology design choice with no direct biological pathway to the realised safety rate `sae_rate`; the association is confounded through `intervention/intervention_type` and `condition` (what is being studied), which carry the genuine safety edges. (R4: confounded design->safety.)

### `Placebo Comparator Arm Number`

- **Association:** effect = 0.104 (eta), n_valid = 69,293
- **Provenance:** demoted_confounded

`Placebo Comparator Arm Number` is a deterministic descendant of its single definitional design parent; `sponsors/lead_sponsor/agency_class` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `Biological intervention Number`

- **Association:** effect = 0.102 (eta), n_valid = 71,221
- **Provenance:** demoted_confounded

`Biological intervention Number` is a deterministic descendant of its single definitional design parent; `sponsors/lead_sponsor/agency_class` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `smiless`

- **Association:** effect = 0.101 (eta), n_valid = 71,221
- **Provenance:** demoted_confounded

`smiless` is a deterministic descendant of its single definitional design parent; `sponsors/lead_sponsor/agency_class` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `study_design_info/intervention_model`

- **Association:** effect = 0.100 (cramers_v), n_valid = 70,749
- **Provenance:** explicit

Both jointly chosen.

### `study_design_info/primary_purpose`

- **Association:** effect = 0.090 (cramers_v), n_valid = 70,604
- **Provenance:** explicit

Both jointly chosen.

### `Drug intervention Number`

- **Association:** effect = 0.089 (eta), n_valid = 71,221
- **Provenance:** demoted_confounded

`Drug intervention Number` is a deterministic descendant of its single definitional design parent; `sponsors/lead_sponsor/agency_class` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `eligibility/gender`

- **Association:** effect = 0.084 (cramers_v), n_valid = 71,221
- **Provenance:** demoted_confounded

`sponsors/lead_sponsor/agency_class` has no concrete causal mechanism that sets `eligibility/gender`. Trial size, eligible population, calendar start date, site geography and the free-text title are not directly caused by `sponsors/lead_sponsor/agency_class`; the association is a jointly-chosen-design / sponsor-footprint / secular-trend confound. (R9: spurious design->planning/eligibility.)

### `start_date`

- **Association:** effect = 0.084 (eta), n_valid = 42,855
- **Provenance:** demoted_confounded

`sponsors/lead_sponsor/agency_class` has no concrete causal mechanism that sets `start_date`. Trial size, eligible population, calendar start date, site geography and the free-text title are not directly caused by `sponsors/lead_sponsor/agency_class`; the association is a jointly-chosen-design / sponsor-footprint / secular-trend confound. (R9: spurious design->planning/eligibility.)

### `biology_fail`

- **Association:** effect = 0.082 (eta), n_valid = 23,862
- **Provenance:** demoted_confounded

`sponsors/lead_sponsor/agency_class` reaches the trial-success label `biology_fail` only through biology / efficacy and enrollment mediators already in the DAG (`biology_pass`, `failure_reason`, `enrollment`); no direct arrow. (R6: mediated design->label.)

### `biology_pass`

- **Association:** effect = 0.082 (eta), n_valid = 23,862
- **Provenance:** demoted_confounded

`sponsors/lead_sponsor/agency_class` reaches the trial-success label `biology_pass` only through biology / efficacy and enrollment mediators already in the DAG (`biology_pass`, `failure_reason`, `enrollment`); no direct arrow. (R6: mediated design->label.)

### `mortality_YN`

- **Association:** effect = 0.078 (eta), n_valid = 17,916
- **Provenance:** demoted_confounded

`sponsors/lead_sponsor/agency_class` is a sponsor / methodology design choice with no direct biological pathway to the realised safety rate `mortality_YN`; the association is confounded through `intervention/intervention_type` and `condition` (what is being studied), which carry the genuine safety edges. (R4: confounded design->safety.)

### `MaskingType-Outcomes Assessor`

- **Association:** effect = 0.062 (eta), n_valid = 70,854
- **Provenance:** demoted_confounded

`MaskingType-Outcomes Assessor` is a deterministic descendant of its single definitional design parent; `sponsors/lead_sponsor/agency_class` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `intervention/intervention_name`

- **Association:** effect = 0.062 (eta), n_valid = 71,221
- **Provenance:** explicit

Sponsor and specific drug correlate through portfolio (industry runs branded drugs, etc.) but neither directly causes the other.

### `Dietary Supplement intervention Number`

- **Association:** effect = 0.061 (eta), n_valid = 71,221
- **Provenance:** demoted_confounded

`Dietary Supplement intervention Number` is a deterministic descendant of its single definitional design parent; `sponsors/lead_sponsor/agency_class` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `study_design_info/allocation`

- **Association:** effect = 0.059 (cramers_v), n_valid = 54,376
- **Provenance:** explicit

Both jointly chosen.

### `Device intervention Number`

- **Association:** effect = 0.055 (eta), n_valid = 71,221
- **Provenance:** demoted_confounded

`Device intervention Number` is a deterministic descendant of its single definitional design parent; `sponsors/lead_sponsor/agency_class` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `MaskingType-Care Provider`

- **Association:** effect = 0.055 (eta), n_valid = 70,854
- **Provenance:** demoted_confounded

`MaskingType-Care Provider` is a deterministic descendant of its single definitional design parent; `sponsors/lead_sponsor/agency_class` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)
