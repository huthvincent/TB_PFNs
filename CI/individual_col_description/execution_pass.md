# execution_pass

- **Group:** `outcome_label`
- **Dtype:** boolean
- **Description:** True if the trial executed without operational failure (e.g., enrolled, completed).
- **Associated partners (from `association.md`):** 44
  - Direct **causes** (parents of this feature): **17**
  - Direct **effects** (children of this feature): **2**
  - Associated but **no direct** causal edge: **25**

This per-feature file enumerates only **associated** partners. All other columns in `DAG.json` were ruled independent in the Stage-1 association screen and do not appear here. See `association.md` for the screen.

---

## Direct causes (17)

### `dropout_YN`

- **Association:** effect = 0.940 (abs_spearman), n_valid = 38,302
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Realised safety outcome (dropout_YN) feeds the trial-success label (execution_pass) directly (e.g., 'safety' failure category, regulatory rejection).

### `failure_reason`

- **Association:** effect = 0.755 (eta), n_valid = 20,769
- **Mechanism:** `definitional`
- **Provenance:** explicit

TrialBench encodes execution_pass = False iff failure_reason = 'poor enrollment' (and related execution categories); failure_reason directly populates the boolean.

### `dropout_rate`

- **Association:** effect = 0.671 (abs_spearman), n_valid = 38,302
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Realised safety outcome (dropout_rate) feeds the trial-success label (execution_pass) directly (e.g., 'safety' failure category, regulatory rejection).

### `intervention/intervention_type`

- **Association:** effect = 0.377 (abs_spearman), n_valid = 52,772
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Sponsor design decision (intervention/intervention_type) that influences the trial-success label (execution_pass) through the trial's biological and regulatory pathway.

### `enrollment`

- **Association:** effect = 0.308 (abs_spearman), n_valid = 38,306
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Downstream-design field (enrollment) feeds the trial-success label (execution_pass) through biology, execution, or regulatory pathways.

### `sae_YN`

- **Association:** effect = 0.269 (abs_spearman), n_valid = 17,903
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Realised safety outcome (sae_YN) feeds the trial-success label (execution_pass) directly (e.g., 'safety' failure category, regulatory rejection).

### `phase`

- **Association:** effect = 0.261 (eta), n_valid = 52,772
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Sponsor design decision (phase) that influences the trial-success label (execution_pass) through the trial's biological and regulatory pathway.

### `sae_rate`

- **Association:** effect = 0.185 (abs_spearman), n_valid = 17,903
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Realised safety outcome (sae_rate) feeds the trial-success label (execution_pass) directly (e.g., 'safety' failure category, regulatory rejection).

### `mortality_YN`

- **Association:** effect = 0.145 (abs_spearman), n_valid = 17,903
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Realised safety outcome (mortality_YN) feeds the trial-success label (execution_pass) directly (e.g., 'safety' failure category, regulatory rejection).

### `duration_year`

- **Association:** effect = 0.141 (abs_spearman), n_valid = 20,062
- **Mechanism:** `operational`
- **Provenance:** default_cross_tier

Trial timing (duration_year) propagates into the post-hoc trial-success label (execution_pass).

### `duration_day`

- **Association:** effect = 0.141 (abs_spearman), n_valid = 20,062
- **Mechanism:** `operational`
- **Provenance:** default_cross_tier

Trial timing (duration_day) propagates into the post-hoc trial-success label (execution_pass).

### `duration_month`

- **Association:** effect = 0.141 (abs_spearman), n_valid = 20,062
- **Mechanism:** `operational`
- **Provenance:** default_cross_tier

Trial timing (duration_month) propagates into the post-hoc trial-success label (execution_pass).

### `completion_date`

- **Association:** effect = 0.139 (abs_spearman), n_valid = 20,062
- **Mechanism:** `operational`
- **Provenance:** default_cross_tier

Trial timing (completion_date) propagates into the post-hoc trial-success label (execution_pass).

### `study_design_info/masking`

- **Association:** effect = 0.124 (eta), n_valid = 52,422
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Sponsor design decision (study_design_info/masking) that influences the trial-success label (execution_pass) through the trial's biological and regulatory pathway.

### `mortality_rate`

- **Association:** effect = 0.111 (abs_spearman), n_valid = 17,903
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Realised safety outcome (mortality_rate) feeds the trial-success label (execution_pass) directly (e.g., 'safety' failure category, regulatory rejection).

### `study_design_info/allocation`

- **Association:** effect = 0.093 (eta), n_valid = 39,412
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Sponsor design decision (study_design_info/allocation) that influences the trial-success label (execution_pass) through the trial's biological and regulatory pathway.

### `intervention/intervention_name`

- **Association:** effect = 0.091 (abs_spearman), n_valid = 52,772
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Sponsor design decision (intervention/intervention_name) that influences the trial-success label (execution_pass) through the trial's biological and regulatory pathway.

---

## Direct effects (2)

### `execution_fail`

- **Association:** effect = 1.000 (abs_spearman), n_valid = 52,772
- **Mechanism:** `deterministic`
- **Provenance:** explicit

execution_fail = NOT execution_pass (definitional negation).

### `approval_outcome`

- **Association:** effect = 0.226 (abs_spearman), n_valid = 23,059
- **Mechanism:** `operational`
- **Provenance:** explicit

A trial that fails to execute (recruit, complete) cannot deliver the evidence for regulatory submission; execution_pass is a precondition for approval_outcome.

---

## Associated but no direct causal edge (25)

### `location/facility/address/city`

- **Association:** effect = 0.393 (abs_spearman), n_valid = 52,772
- **Provenance:** demoted_confounded

`location/facility/address/city` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `execution_pass`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `start_date`

- **Association:** effect = 0.177 (abs_spearman), n_valid = 20,062
- **Provenance:** demoted_confounded

`start_date` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `execution_pass`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `study_design_info/intervention_model`

- **Association:** effect = 0.176 (eta), n_valid = 52,169
- **Provenance:** demoted_confounded

`study_design_info/intervention_model` reaches the trial-success label `execution_pass` only through biology / efficacy and enrollment mediators already in the DAG (`biology_pass`, `failure_reason`, `enrollment`); no direct arrow. (R6: mediated design->label.)

### `oversight_info/is_fda_regulated_drug`

- **Association:** effect = 0.151 (eta), n_valid = 13,615
- **Provenance:** demoted_confounded

`oversight_info/is_fda_regulated_drug` is an oversight / regulatory flag that proxies for trial type and scale; its association with `execution_pass` is confounded through `intervention/intervention_type`, `phase`, and trial scale. The genuine oversight mechanisms (FDA-regulation -> approval_outcome; DMC early-stopping -> sae_rate / mortality_rate) are retained as explicit edges. (R10: confounded design_oversight->outcome.)

### `patient_data/sharing_ipd`

- **Association:** effect = 0.148 (eta), n_valid = 12,954
- **Provenance:** demoted_confounded

`patient_data/sharing_ipd` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `execution_pass`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `ipd_info_type-Informed Consent Form (ICF)`

- **Association:** effect = 0.147 (abs_spearman), n_valid = 2,105
- **Provenance:** demoted_confounded

`ipd_info_type-Informed Consent Form (ICF)` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `execution_pass`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `sponsors/lead_sponsor/agency_class`

- **Association:** effect = 0.145 (eta), n_valid = 42,207
- **Provenance:** demoted_confounded

`sponsors/lead_sponsor/agency_class` reaches the trial-success label `execution_pass` only through biology / efficacy and enrollment mediators already in the DAG (`biology_pass`, `failure_reason`, `enrollment`); no direct arrow. (R6: mediated design->label.)

### `biology_pass`

- **Association:** effect = 0.125 (abs_spearman), n_valid = 28,367
- **Provenance:** explicit

biology_pass and execution_pass are independent preconditions for approval — biology is about whether the drug works, execution is about whether the trial was run properly. They are both downstream of failure_reason but do not directly cause each other.

### `biology_fail`

- **Association:** effect = 0.125 (abs_spearman), n_valid = 28,367
- **Provenance:** explicit

Mediated through `biology_pass` (and the common parent `failure_reason`).

### `study_design_info/primary_purpose`

- **Association:** effect = 0.119 (eta), n_valid = 52,095
- **Provenance:** demoted_confounded

`study_design_info/primary_purpose` reaches the trial-success label `execution_pass` only through biology / efficacy and enrollment mediators already in the DAG (`biology_pass`, `failure_reason`, `enrollment`); no direct arrow. (R6: mediated design->label.)

### `eligibility/healthy_volunteers`

- **Association:** effect = 0.116 (eta), n_valid = 52,677
- **Provenance:** demoted_confounded

`eligibility/healthy_volunteers` reaches the trial-success label `execution_pass` only through biology / efficacy and enrollment mediators already in the DAG (`biology_pass`, `failure_reason`, `enrollment`); no direct arrow. (R6: mediated design->label.)

### `MaskingType-Investigator`

- **Association:** effect = 0.115 (abs_spearman), n_valid = 52,422
- **Provenance:** demoted_confounded

`MaskingType-Investigator` is a deterministic re-encoding / tally of `study_design_info/masking`; its association with `execution_pass` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `ipd_info_type-Statistical Analysis Plan (SAP)`

- **Association:** effect = 0.103 (abs_spearman), n_valid = 2,257
- **Provenance:** demoted_confounded

`ipd_info_type-Statistical Analysis Plan (SAP)` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `execution_pass`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `MaskingType-Participant`

- **Association:** effect = 0.102 (abs_spearman), n_valid = 52,422
- **Provenance:** demoted_confounded

`MaskingType-Participant` is a deterministic re-encoding / tally of `study_design_info/masking`; its association with `execution_pass` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `study_design_info/masking_num`

- **Association:** effect = 0.099 (abs_spearman), n_valid = 52,422
- **Provenance:** demoted_confounded

`study_design_info/masking_num` is a deterministic re-encoding / tally of `study_design_info/masking`; its association with `execution_pass` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `responsible_party/responsible_party_type`

- **Association:** effect = 0.098 (eta), n_valid = 40,560
- **Provenance:** demoted_confounded

`responsible_party/responsible_party_type` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `execution_pass`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `Placebo Comparator Arm Number`

- **Association:** effect = 0.079 (abs_spearman), n_valid = 50,684
- **Provenance:** demoted_confounded

`Placebo Comparator Arm Number` is a deterministic re-encoding / tally of `study_design_info/intervention_model`; its association with `execution_pass` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `intervention_browse/mesh_term`

- **Association:** effect = 0.077 (abs_spearman), n_valid = 52,772
- **Provenance:** demoted_confounded

`intervention_browse/mesh_term` is a deterministic re-encoding / tally of `intervention/intervention_name`; its association with `execution_pass` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `Drug intervention Number`

- **Association:** effect = 0.075 (abs_spearman), n_valid = 52,772
- **Provenance:** demoted_confounded

`Drug intervention Number` is a deterministic re-encoding / tally of `intervention/intervention_type`; its association with `execution_pass` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `MaskingType-Outcomes Assessor`

- **Association:** effect = 0.073 (abs_spearman), n_valid = 52,422
- **Provenance:** demoted_confounded

`MaskingType-Outcomes Assessor` is a deterministic re-encoding / tally of `study_design_info/masking`; its association with `execution_pass` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `MaskingType-Care Provider`

- **Association:** effect = 0.069 (abs_spearman), n_valid = 52,422
- **Provenance:** demoted_confounded

`MaskingType-Care Provider` is a deterministic re-encoding / tally of `study_design_info/masking`; its association with `execution_pass` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `number_of_arms`

- **Association:** effect = 0.063 (abs_spearman), n_valid = 50,684
- **Provenance:** demoted_confounded

`number_of_arms` reaches the trial-success label `execution_pass` only through biology / efficacy and enrollment mediators already in the DAG (`biology_pass`, `failure_reason`, `enrollment`); no direct arrow. (R6: mediated design->label.)

### `condition_browse/mesh_term`

- **Association:** effect = 0.062 (abs_spearman), n_valid = 52,772
- **Provenance:** demoted_confounded

`condition_browse/mesh_term` is a deterministic re-encoding / tally of `condition`; its association with `execution_pass` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `eligibility/gender`

- **Association:** effect = 0.058 (eta), n_valid = 42,207
- **Provenance:** demoted_confounded

`eligibility/gender` reaches the trial-success label `execution_pass` only through biology / efficacy and enrollment mediators already in the DAG (`biology_pass`, `failure_reason`, `enrollment`); no direct arrow. (R6: mediated design->label.)

### `smiless`

- **Association:** effect = 0.052 (abs_spearman), n_valid = 52,772
- **Provenance:** demoted_confounded

`smiless` is a deterministic re-encoding / tally of `intervention/intervention_name`; its association with `execution_pass` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)
