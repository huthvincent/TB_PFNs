# number_of_arms

- **Group:** `design_derived`
- **Dtype:** float
- **Description:** Total number of arms in the trial. Sum of the six Arm Number columns.
- **Associated partners (from `association.md`):** 43
  - Direct **causes** (parents of this feature): **5**
  - Direct **effects** (children of this feature): **3**
  - Associated but **no direct** causal edge: **35**

This per-feature file enumerates only **associated** partners. All other columns in `DAG.json` were ruled independent in the Stage-1 association screen and do not appear here. See `association.md` for the screen.

---

## Direct causes (5)

### `Experimental Arm Number`

- **Association:** effect = 0.488 (abs_spearman), n_valid = 78,123
- **Mechanism:** `deterministic`
- **Provenance:** explicit

number_of_arms is the sum of the six Arm-Number columns; this term is one summand.

### `study_design_info/intervention_model`

- **Association:** effect = 0.451 (eta), n_valid = 77,887
- **Mechanism:** `design_constraint`
- **Provenance:** explicit

'Single Group Assignment' forces number_of_arms=1; 'Parallel' / 'Crossover' force >=2; 'Factorial' typically >=4. The intervention model strictly constrains the number of arms.

### `Placebo Comparator Arm Number`

- **Association:** effect = 0.352 (abs_spearman), n_valid = 78,123
- **Mechanism:** `deterministic`
- **Provenance:** explicit

number_of_arms is the sum of the six Arm-Number columns; this term is one summand.

### `Active Comparator Arm Number`

- **Association:** effect = 0.278 (abs_spearman), n_valid = 69,293
- **Mechanism:** `deterministic`
- **Provenance:** explicit

number_of_arms is the sum of the six Arm-Number columns; this term is one summand.

### `No Intervention Arm Number`

- **Association:** effect = 0.057 (abs_spearman), n_valid = 69,293
- **Mechanism:** `deterministic`
- **Provenance:** explicit

number_of_arms is the sum of the six Arm-Number columns; this term is one summand.

---

## Direct effects (3)

### `duration_month`

- **Association:** effect = 0.161 (abs_spearman), n_valid = 42,293
- **Mechanism:** `operational`
- **Provenance:** default_cross_tier

Downstream-design field (number_of_arms) shifts the operational timeline of the trial (duration_month).

### `duration_day`

- **Association:** effect = 0.161 (abs_spearman), n_valid = 42,293
- **Mechanism:** `operational`
- **Provenance:** default_cross_tier

Downstream-design field (number_of_arms) shifts the operational timeline of the trial (duration_day).

### `duration_year`

- **Association:** effect = 0.161 (abs_spearman), n_valid = 42,293
- **Mechanism:** `operational`
- **Provenance:** default_cross_tier

Downstream-design field (number_of_arms) shifts the operational timeline of the trial (duration_year).

---

## Associated but no direct causal edge (35)

### `study_design_info/masking_num`

- **Association:** effect = 0.446 (abs_spearman), n_valid = 77,947
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `MaskingType-Participant`

- **Association:** effect = 0.443 (abs_spearman), n_valid = 77,947
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `intervention/intervention_name`

- **Association:** effect = 0.440 (abs_spearman), n_valid = 78,123
- **Provenance:** demoted_confounded

`number_of_arms` is a deterministic descendant of its single definitional design parent; `intervention/intervention_name` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `MaskingType-Investigator`

- **Association:** effect = 0.419 (abs_spearman), n_valid = 77,947
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `enrollment`

- **Association:** effect = 0.350 (abs_spearman), n_valid = 43,117
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_planning' and 'design_derived'); jointly determined by upstream design_top choices, no direct arrow.

### `Drug intervention Number`

- **Association:** effect = 0.323 (abs_spearman), n_valid = 78,123
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `study_design_info/masking`

- **Association:** effect = 0.293 (eta), n_valid = 72,860
- **Provenance:** demoted_confounded

`number_of_arms` is a deterministic descendant of its single definitional design parent; `study_design_info/masking` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `MaskingType-Care Provider`

- **Association:** effect = 0.278 (abs_spearman), n_valid = 77,947
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `MaskingType-Outcomes Assessor`

- **Association:** effect = 0.277 (abs_spearman), n_valid = 77,947
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `eligibility/healthy_volunteers`

- **Association:** effect = 0.210 (eta), n_valid = 78,060
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_eligibility' and 'design_derived'); jointly determined by upstream design_top choices, no direct arrow.

### `sponsors/lead_sponsor/agency_class`

- **Association:** effect = 0.198 (eta), n_valid = 69,293
- **Provenance:** demoted_confounded

`number_of_arms` is a deterministic descendant of its single definitional design parent; `sponsors/lead_sponsor/agency_class` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `sae_rate`

- **Association:** effect = 0.160 (abs_spearman), n_valid = 17,886
- **Provenance:** demoted_confounded

`number_of_arms` is a sponsor / methodology design choice with no direct biological pathway to the realised safety rate `sae_rate`; the association is confounded through `intervention/intervention_type` and `condition` (what is being studied), which carry the genuine safety edges. (R4: confounded design->safety.)

### `patient_data/sharing_ipd`

- **Association:** effect = 0.152 (eta), n_valid = 13,438
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `phase`

- **Association:** effect = 0.148 (eta), n_valid = 78,123
- **Provenance:** demoted_confounded

`number_of_arms` is a deterministic descendant of its single definitional design parent; `phase` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `mortality_rate`

- **Association:** effect = 0.145 (abs_spearman), n_valid = 17,886
- **Provenance:** demoted_confounded

`number_of_arms` is a sponsor / methodology design choice with no direct biological pathway to the realised safety rate `mortality_rate`; the association is confounded through `intervention/intervention_type` and `condition` (what is being studied), which carry the genuine safety edges. (R4: confounded design->safety.)

### `ipd_info_type-Clinical Study Report (CSR)`

- **Association:** effect = 0.123 (abs_spearman), n_valid = 2,139
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_oversight' and 'design_derived'); jointly determined by upstream design_top choices, no direct arrow.

### `study_design_info/primary_purpose`

- **Association:** effect = 0.114 (eta), n_valid = 77,416
- **Provenance:** demoted_confounded

`number_of_arms` is a deterministic descendant of its single definitional design parent; `study_design_info/primary_purpose` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `responsible_party/responsible_party_type`

- **Association:** effect = 0.110 (eta), n_valid = 66,924
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `approval_outcome`

- **Association:** effect = 0.108 (abs_spearman), n_valid = 28,187
- **Provenance:** demoted_confounded

`number_of_arms` reaches the trial-success label `approval_outcome` only through biology / efficacy and enrollment mediators already in the DAG (`biology_pass`, `failure_reason`, `enrollment`); no direct arrow. (R6: mediated design->label.)

### `failure_reason`

- **Association:** effect = 0.108 (eta), n_valid = 18,919
- **Provenance:** demoted_confounded

`number_of_arms` reaches the trial-success label `failure_reason` only through biology / efficacy and enrollment mediators already in the DAG (`biology_pass`, `failure_reason`, `enrollment`); no direct arrow. (R6: mediated design->label.)

### `mortality_YN`

- **Association:** effect = 0.096 (abs_spearman), n_valid = 17,886
- **Provenance:** demoted_confounded

`number_of_arms` is a sponsor / methodology design choice with no direct biological pathway to the realised safety rate `mortality_YN`; the association is confounded through `intervention/intervention_type` and `condition` (what is being studied), which carry the genuine safety edges. (R4: confounded design->safety.)

### `Radiation intervention Number`

- **Association:** effect = 0.093 (abs_spearman), n_valid = 78,123
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `location/facility/address/city`

- **Association:** effect = 0.091 (abs_spearman), n_valid = 78,123
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_planning' and 'design_derived'); jointly determined by upstream design_top choices, no direct arrow.

### `dropout_YN`

- **Association:** effect = 0.083 (abs_spearman), n_valid = 38,016
- **Provenance:** demoted_confounded

`number_of_arms` is a sponsor / methodology design choice with no direct biological pathway to the realised safety rate `dropout_YN`; the association is confounded through `intervention/intervention_type` and `condition` (what is being studied), which carry the genuine safety edges. (R4: confounded design->safety.)

### `condition_browse/mesh_term`

- **Association:** effect = 0.079 (abs_spearman), n_valid = 78,123
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `start_date`

- **Association:** effect = 0.075 (abs_spearman), n_valid = 42,293
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `intervention/intervention_type`

- **Association:** effect = 0.071 (abs_spearman), n_valid = 78,123
- **Provenance:** demoted_confounded

`number_of_arms` is a deterministic descendant of its single definitional design parent; `intervention/intervention_type` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `Procedure intervention Number`

- **Association:** effect = 0.070 (abs_spearman), n_valid = 69,293
- **Provenance:** default_within_tier

Both in group 'design_derived' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `ipd_info_type-Study Protocol`

- **Association:** effect = 0.064 (abs_spearman), n_valid = 2,290
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_oversight' and 'design_derived'); jointly determined by upstream design_top choices, no direct arrow.

### `execution_pass`

- **Association:** effect = 0.063 (abs_spearman), n_valid = 50,684
- **Provenance:** demoted_confounded

`number_of_arms` reaches the trial-success label `execution_pass` only through biology / efficacy and enrollment mediators already in the DAG (`biology_pass`, `failure_reason`, `enrollment`); no direct arrow. (R6: mediated design->label.)

### `execution_fail`

- **Association:** effect = 0.063 (abs_spearman), n_valid = 50,684
- **Provenance:** demoted_confounded

`number_of_arms` reaches the trial-success label `execution_fail` only through biology / efficacy and enrollment mediators already in the DAG (`biology_pass`, `failure_reason`, `enrollment`); no direct arrow. (R6: mediated design->label.)

### `condition`

- **Association:** effect = 0.062 (abs_spearman), n_valid = 78,123
- **Provenance:** demoted_confounded

`number_of_arms` is a deterministic descendant of its single definitional design parent; `condition` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `eligibility/maximum_age`

- **Association:** effect = 0.061 (abs_spearman), n_valid = 41,114
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_eligibility' and 'design_derived'); jointly determined by upstream design_top choices, no direct arrow.

### `ipd_info_type-Statistical Analysis Plan (SAP)`

- **Association:** effect = 0.056 (abs_spearman), n_valid = 2,290
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_oversight' and 'design_derived'); jointly determined by upstream design_top choices, no direct arrow.

### `brief_title`

- **Association:** effect = 0.053 (abs_spearman), n_valid = 78,123
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_planning' and 'design_derived'); jointly determined by upstream design_top choices, no direct arrow.
