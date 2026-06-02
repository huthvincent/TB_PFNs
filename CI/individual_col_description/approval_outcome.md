# approval_outcome

- **Group:** `outcome_label`
- **Dtype:** float (0/1)
- **Description:** Whether the trial result led to a successful drug/device approval. Merged with `regulatory_pass` (effect=1.0, definitionally identical).
- **Associated partners (from `association.md`):** 37
  - Direct **causes** (parents of this feature): **14**
  - Direct **effects** (children of this feature): **0**
  - Associated but **no direct** causal edge: **23**

This per-feature file enumerates only **associated** partners. All other columns in `DAG.json` were ruled independent in the Stage-1 association screen and do not appear here. See `association.md` for the screen.

---

## Direct causes (14)

### `intervention/intervention_type`

- **Association:** effect = 0.464 (abs_spearman), n_valid = 30,683
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Sponsor design decision (intervention/intervention_type) that influences the trial-success label (approval_outcome) through the trial's biological and regulatory pathway.

### `completion_date`

- **Association:** effect = 0.333 (abs_spearman), n_valid = 9,263
- **Mechanism:** `operational`
- **Provenance:** default_cross_tier

Trial timing (completion_date) propagates into the post-hoc trial-success label (approval_outcome).

### `biology_pass`

- **Association:** effect = 0.295 (abs_spearman), n_valid = 27,420
- **Mechanism:** `regulatory`
- **Provenance:** explicit

Meeting the primary biological efficacy endpoint is a precondition for regulatory approval; biology_pass is the gating biology factor in approval_outcome.

### `enrollment`

- **Association:** effect = 0.288 (abs_spearman), n_valid = 20,273
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Downstream-design field (enrollment) feeds the trial-success label (approval_outcome) through biology, execution, or regulatory pathways.

### `sponsors/lead_sponsor/agency_class`

- **Association:** effect = 0.275 (eta), n_valid = 24,108
- **Mechanism:** `regulatory`
- **Provenance:** explicit

Industry trials are designed-for-approval; academic / NIH trials less often pursue or attain regulatory approval.

### `execution_pass`

- **Association:** effect = 0.226 (abs_spearman), n_valid = 23,059
- **Mechanism:** `operational`
- **Provenance:** explicit

A trial that fails to execute (recruit, complete) cannot deliver the evidence for regulatory submission; execution_pass is a precondition for approval_outcome.

### `sae_YN`

- **Association:** effect = 0.175 (abs_spearman), n_valid = 5,434
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Realised safety outcome (sae_YN) feeds the trial-success label (approval_outcome) directly (e.g., 'safety' failure category, regulatory rejection).

### `phase`

- **Association:** effect = 0.156 (eta), n_valid = 30,683
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Sponsor design decision (phase) that influences the trial-success label (approval_outcome) through the trial's biological and regulatory pathway.

### `dropout_YN`

- **Association:** effect = 0.154 (abs_spearman), n_valid = 14,131
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Realised safety outcome (dropout_YN) feeds the trial-success label (approval_outcome) directly (e.g., 'safety' failure category, regulatory rejection).

### `study_design_info/masking`

- **Association:** effect = 0.147 (eta), n_valid = 24,224
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Sponsor design decision (study_design_info/masking) that influences the trial-success label (approval_outcome) through the trial's biological and regulatory pathway.

### `dropout_rate`

- **Association:** effect = 0.143 (abs_spearman), n_valid = 14,131
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Realised safety outcome (dropout_rate) feeds the trial-success label (approval_outcome) directly (e.g., 'safety' failure category, regulatory rejection).

### `condition`

- **Association:** effect = 0.061 (abs_spearman), n_valid = 30,683
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Sponsor design decision (condition) that influences the trial-success label (approval_outcome) through the trial's biological and regulatory pathway.

### `intervention/intervention_name`

- **Association:** effect = 0.059 (abs_spearman), n_valid = 30,683
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Sponsor design decision (intervention/intervention_name) that influences the trial-success label (approval_outcome) through the trial's biological and regulatory pathway.

### `mortality_rate`

- **Association:** effect = 0.056 (abs_spearman), n_valid = 5,434
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Realised safety outcome (mortality_rate) feeds the trial-success label (approval_outcome) directly (e.g., 'safety' failure category, regulatory rejection).

---

## Direct effects (0)

_(none)_

---

## Associated but no direct causal edge (23)

### `location/facility/address/city`

- **Association:** effect = 0.360 (abs_spearman), n_valid = 30,683
- **Provenance:** demoted_confounded

`location/facility/address/city` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `approval_outcome`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `start_date`

- **Association:** effect = 0.296 (abs_spearman), n_valid = 9,263
- **Provenance:** demoted_confounded

`start_date` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `approval_outcome`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `biology_fail`

- **Association:** effect = 0.295 (abs_spearman), n_valid = 27,420
- **Provenance:** explicit

Mediated through `biology_pass`: biology_fail = NOT biology_pass, and biology_pass -> approval_outcome is the direct edge.

### `patient_data/sharing_ipd`

- **Association:** effect = 0.248 (eta), n_valid = 4,575
- **Provenance:** demoted_confounded

`patient_data/sharing_ipd` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `approval_outcome`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `execution_fail`

- **Association:** effect = 0.226 (abs_spearman), n_valid = 23,059
- **Provenance:** explicit

Mediated through `execution_pass`: execution_fail = NOT execution_pass, and execution_pass -> approval_outcome is the direct edge.

### `responsible_party/responsible_party_type`

- **Association:** effect = 0.147 (eta), n_valid = 21,870
- **Provenance:** demoted_confounded

`responsible_party/responsible_party_type` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `approval_outcome`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `ipd_info_type-Statistical Analysis Plan (SAP)`

- **Association:** effect = 0.131 (abs_spearman), n_valid = 746
- **Provenance:** demoted_confounded

`ipd_info_type-Statistical Analysis Plan (SAP)` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `approval_outcome`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `Experimental Arm Number`

- **Association:** effect = 0.121 (abs_spearman), n_valid = 28,187
- **Provenance:** demoted_confounded

`Experimental Arm Number` is a deterministic re-encoding / tally of `study_design_info/intervention_model`; its association with `approval_outcome` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `oversight_info/has_dmc`

- **Association:** effect = 0.116 (eta), n_valid = 21,810
- **Provenance:** demoted_confounded

`oversight_info/has_dmc` is an oversight / regulatory flag that proxies for trial type and scale; its association with `approval_outcome` is confounded through `intervention/intervention_type`, `phase`, and trial scale. The genuine oversight mechanisms (FDA-regulation -> approval_outcome; DMC early-stopping -> sae_rate / mortality_rate) are retained as explicit edges. (R10: confounded design_oversight->outcome.)

### `number_of_arms`

- **Association:** effect = 0.108 (abs_spearman), n_valid = 28,187
- **Provenance:** demoted_confounded

`number_of_arms` reaches the trial-success label `approval_outcome` only through biology / efficacy and enrollment mediators already in the DAG (`biology_pass`, `failure_reason`, `enrollment`); no direct arrow. (R6: mediated design->label.)

### `study_design_info/primary_purpose`

- **Association:** effect = 0.107 (eta), n_valid = 30,383
- **Provenance:** demoted_confounded

`study_design_info/primary_purpose` reaches the trial-success label `approval_outcome` only through biology / efficacy and enrollment mediators already in the DAG (`biology_pass`, `failure_reason`, `enrollment`); no direct arrow. (R6: mediated design->label.)

### `MaskingType-Investigator`

- **Association:** effect = 0.083 (abs_spearman), n_valid = 30,351
- **Provenance:** demoted_confounded

`MaskingType-Investigator` is a deterministic re-encoding / tally of `study_design_info/masking`; its association with `approval_outcome` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `Biological intervention Number`

- **Association:** effect = 0.081 (abs_spearman), n_valid = 30,683
- **Provenance:** demoted_confounded

`Biological intervention Number` is a deterministic re-encoding / tally of `intervention/intervention_type`; its association with `approval_outcome` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `Procedure intervention Number`

- **Association:** effect = 0.080 (abs_spearman), n_valid = 24,108
- **Provenance:** demoted_confounded

`Procedure intervention Number` is a deterministic re-encoding / tally of `intervention/intervention_type`; its association with `approval_outcome` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `study_design_info/masking_num`

- **Association:** effect = 0.074 (abs_spearman), n_valid = 30,351
- **Provenance:** demoted_confounded

`study_design_info/masking_num` is a deterministic re-encoding / tally of `study_design_info/masking`; its association with `approval_outcome` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `Other intervention Number`

- **Association:** effect = 0.072 (abs_spearman), n_valid = 24,108
- **Provenance:** demoted_confounded

`Other intervention Number` is a deterministic re-encoding / tally of `intervention/intervention_type`; its association with `approval_outcome` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `study_design_info/intervention_model`

- **Association:** effect = 0.072 (eta), n_valid = 30,122
- **Provenance:** demoted_confounded

`study_design_info/intervention_model` reaches the trial-success label `approval_outcome` only through biology / efficacy and enrollment mediators already in the DAG (`biology_pass`, `failure_reason`, `enrollment`); no direct arrow. (R6: mediated design->label.)

### `MaskingType-Participant`

- **Association:** effect = 0.071 (abs_spearman), n_valid = 30,351
- **Provenance:** demoted_confounded

`MaskingType-Participant` is a deterministic re-encoding / tally of `study_design_info/masking`; its association with `approval_outcome` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `Radiation intervention Number`

- **Association:** effect = 0.069 (abs_spearman), n_valid = 30,683
- **Provenance:** demoted_confounded

`Radiation intervention Number` is a deterministic re-encoding / tally of `intervention/intervention_type`; its association with `approval_outcome` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `eligibility/healthy_volunteers`

- **Association:** effect = 0.068 (eta), n_valid = 30,572
- **Provenance:** demoted_confounded

`eligibility/healthy_volunteers` reaches the trial-success label `approval_outcome` only through biology / efficacy and enrollment mediators already in the DAG (`biology_pass`, `failure_reason`, `enrollment`); no direct arrow. (R6: mediated design->label.)

### `eligibility/maximum_age`

- **Association:** effect = 0.067 (abs_spearman), n_valid = 13,782
- **Provenance:** demoted_confounded

`eligibility/maximum_age` reaches the trial-success label `approval_outcome` only through biology / efficacy and enrollment mediators already in the DAG (`biology_pass`, `failure_reason`, `enrollment`); no direct arrow. (R6: mediated design->label.)

### `No Intervention Arm Number`

- **Association:** effect = 0.066 (abs_spearman), n_valid = 22,770
- **Provenance:** demoted_confounded

`No Intervention Arm Number` is a deterministic re-encoding / tally of `study_design_info/intervention_model`; its association with `approval_outcome` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `Drug intervention Number`

- **Association:** effect = 0.056 (abs_spearman), n_valid = 30,683
- **Provenance:** demoted_confounded

`Drug intervention Number` is a deterministic re-encoding / tally of `intervention/intervention_type`; its association with `approval_outcome` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)
