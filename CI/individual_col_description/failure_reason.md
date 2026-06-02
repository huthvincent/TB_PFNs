# failure_reason

- **Group:** `outcome_label`
- **Dtype:** categorical
- **Description:** Reason a trial failed: 'poor enrollment' / 'efficacy' / 'safety' / 'Others' / NaN (no failure or unknown).
- **Associated partners (from `association.md`):** 41
  - Direct **causes** (parents of this feature): **13**
  - Direct **effects** (children of this feature): **2**
  - Associated but **no direct** causal edge: **26**

This per-feature file enumerates only **associated** partners. All other columns in `DAG.json` were ruled independent in the Stage-1 association screen and do not appear here. See `association.md` for the screen.

---

## Direct causes (13)

### `sae_YN`

- **Association:** effect = 0.240 (eta), n_valid = 3,199
- **Mechanism:** `biological`
- **Provenance:** explicit

A substantial SAE incidence drives the trial to be terminated for safety, populating failure_reason='safety'.

### `mortality_YN`

- **Association:** effect = 0.153 (eta), n_valid = 3,199
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Realised safety outcome (mortality_YN) feeds the trial-success label (failure_reason) directly (e.g., 'safety' failure category, regulatory rejection).

### `enrollment`

- **Association:** effect = 0.134 (eta), n_valid = 6,304
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Downstream-design field (enrollment) feeds the trial-success label (failure_reason) through biology, execution, or regulatory pathways.

### `dropout_YN`

- **Association:** effect = 0.127 (eta), n_valid = 6,299
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Realised safety outcome (dropout_YN) feeds the trial-success label (failure_reason) directly (e.g., 'safety' failure category, regulatory rejection).

### `phase`

- **Association:** effect = 0.127 (cramers_v), n_valid = 20,769
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Sponsor design decision (phase) that influences the trial-success label (failure_reason) through the trial's biological and regulatory pathway.

### `completion_date`

- **Association:** effect = 0.115 (eta), n_valid = 6,904
- **Mechanism:** `operational`
- **Provenance:** default_cross_tier

Trial timing (completion_date) propagates into the post-hoc trial-success label (failure_reason).

### `dropout_rate`

- **Association:** effect = 0.111 (eta), n_valid = 6,299
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Realised safety outcome (dropout_rate) feeds the trial-success label (failure_reason) directly (e.g., 'safety' failure category, regulatory rejection).

### `intervention/intervention_type`

- **Association:** effect = 0.110 (eta), n_valid = 20,769
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Sponsor design decision (intervention/intervention_type) that influences the trial-success label (failure_reason) through the trial's biological and regulatory pathway.

### `duration_day`

- **Association:** effect = 0.096 (eta), n_valid = 6,904
- **Mechanism:** `operational`
- **Provenance:** default_cross_tier

Trial timing (duration_day) propagates into the post-hoc trial-success label (failure_reason).

### `duration_year`

- **Association:** effect = 0.096 (eta), n_valid = 6,904
- **Mechanism:** `operational`
- **Provenance:** default_cross_tier

Trial timing (duration_year) propagates into the post-hoc trial-success label (failure_reason).

### `duration_month`

- **Association:** effect = 0.096 (eta), n_valid = 6,904
- **Mechanism:** `operational`
- **Provenance:** default_cross_tier

Trial timing (duration_month) propagates into the post-hoc trial-success label (failure_reason).

### `mortality_rate`

- **Association:** effect = 0.072 (eta), n_valid = 3,199
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Realised safety outcome (mortality_rate) feeds the trial-success label (failure_reason) directly (e.g., 'safety' failure category, regulatory rejection).

### `study_design_info/masking`

- **Association:** effect = 0.058 (cramers_v), n_valid = 20,495
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Sponsor design decision (study_design_info/masking) that influences the trial-success label (failure_reason) through the trial's biological and regulatory pathway.

---

## Direct effects (2)

### `biology_pass`

- **Association:** effect = 1.000 (eta), n_valid = 20,769
- **Mechanism:** `definitional`
- **Provenance:** explicit

TrialBench encodes biology_pass = False iff failure_reason in {'efficacy', 'safety'}; the categorical failure_reason directly populates the boolean.

### `execution_pass`

- **Association:** effect = 0.755 (eta), n_valid = 20,769
- **Mechanism:** `definitional`
- **Provenance:** explicit

TrialBench encodes execution_pass = False iff failure_reason = 'poor enrollment' (and related execution categories); failure_reason directly populates the boolean.

---

## Associated but no direct causal edge (26)

### `biology_fail`

- **Association:** effect = 1.000 (eta), n_valid = 20,769
- **Provenance:** default_within_tier

Both in group 'outcome_label' (tier 4); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `execution_fail`

- **Association:** effect = 0.755 (eta), n_valid = 20,769
- **Provenance:** default_within_tier

Both in group 'outcome_label' (tier 4); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `sponsors/lead_sponsor/agency_class`

- **Association:** effect = 0.169 (cramers_v), n_valid = 10,204
- **Provenance:** demoted_confounded

`sponsors/lead_sponsor/agency_class` reaches the trial-success label `failure_reason` only through biology / efficacy and enrollment mediators already in the DAG (`biology_pass`, `failure_reason`, `enrollment`); no direct arrow. (R6: mediated design->label.)

### `location/facility/address/city`

- **Association:** effect = 0.160 (eta), n_valid = 20,769
- **Provenance:** demoted_confounded

`location/facility/address/city` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `failure_reason`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `patient_data/sharing_ipd`

- **Association:** effect = 0.143 (cramers_v), n_valid = 2,274
- **Provenance:** demoted_confounded

`patient_data/sharing_ipd` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `failure_reason`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `Experimental Arm Number`

- **Association:** effect = 0.134 (eta), n_valid = 18,919
- **Provenance:** demoted_confounded

`Experimental Arm Number` is a deterministic re-encoding / tally of `study_design_info/intervention_model`; its association with `failure_reason` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `start_date`

- **Association:** effect = 0.123 (eta), n_valid = 6,904
- **Provenance:** demoted_confounded

`start_date` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `failure_reason`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `eligibility/healthy_volunteers`

- **Association:** effect = 0.118 (cramers_v), n_valid = 20,706
- **Provenance:** demoted_confounded

`eligibility/healthy_volunteers` reaches the trial-success label `failure_reason` only through biology / efficacy and enrollment mediators already in the DAG (`biology_pass`, `failure_reason`, `enrollment`); no direct arrow. (R6: mediated design->label.)

### `oversight_info/is_fda_regulated_drug`

- **Association:** effect = 0.118 (cramers_v), n_valid = 4,623
- **Provenance:** demoted_confounded

`oversight_info/is_fda_regulated_drug` is an oversight / regulatory flag that proxies for trial type and scale; its association with `failure_reason` is confounded through `intervention/intervention_type`, `phase`, and trial scale. The genuine oversight mechanisms (FDA-regulation -> approval_outcome; DMC early-stopping -> sae_rate / mortality_rate) are retained as explicit edges. (R10: confounded design_oversight->outcome.)

### `number_of_arms`

- **Association:** effect = 0.108 (eta), n_valid = 18,919
- **Provenance:** demoted_confounded

`number_of_arms` reaches the trial-success label `failure_reason` only through biology / efficacy and enrollment mediators already in the DAG (`biology_pass`, `failure_reason`, `enrollment`); no direct arrow. (R6: mediated design->label.)

### `responsible_party/responsible_party_type`

- **Association:** effect = 0.107 (cramers_v), n_valid = 10,039
- **Provenance:** demoted_confounded

`responsible_party/responsible_party_type` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `failure_reason`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `intervention_browse/mesh_term`

- **Association:** effect = 0.079 (eta), n_valid = 20,769
- **Provenance:** demoted_confounded

`intervention_browse/mesh_term` is a deterministic re-encoding / tally of `intervention/intervention_name`; its association with `failure_reason` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `Procedure intervention Number`

- **Association:** effect = 0.077 (eta), n_valid = 10,204
- **Provenance:** demoted_confounded

`Procedure intervention Number` is a deterministic re-encoding / tally of `intervention/intervention_type`; its association with `failure_reason` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `MaskingType-Investigator`

- **Association:** effect = 0.071 (eta), n_valid = 20,495
- **Provenance:** demoted_confounded

`MaskingType-Investigator` is a deterministic re-encoding / tally of `study_design_info/masking`; its association with `failure_reason` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `Active Comparator Arm Number`

- **Association:** effect = 0.071 (eta), n_valid = 10,089
- **Provenance:** demoted_confounded

`Active Comparator Arm Number` is a deterministic re-encoding / tally of `study_design_info/intervention_model`; its association with `failure_reason` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `study_design_info/masking_num`

- **Association:** effect = 0.069 (eta), n_valid = 20,495
- **Provenance:** demoted_confounded

`study_design_info/masking_num` is a deterministic re-encoding / tally of `study_design_info/masking`; its association with `failure_reason` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `Placebo Comparator Arm Number`

- **Association:** effect = 0.069 (eta), n_valid = 18,919
- **Provenance:** demoted_confounded

`Placebo Comparator Arm Number` is a deterministic re-encoding / tally of `study_design_info/intervention_model`; its association with `failure_reason` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `MaskingType-Participant`

- **Association:** effect = 0.065 (eta), n_valid = 20,495
- **Provenance:** demoted_confounded

`MaskingType-Participant` is a deterministic re-encoding / tally of `study_design_info/masking`; its association with `failure_reason` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `Drug intervention Number`

- **Association:** effect = 0.065 (eta), n_valid = 20,769
- **Provenance:** demoted_confounded

`Drug intervention Number` is a deterministic re-encoding / tally of `intervention/intervention_type`; its association with `failure_reason` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `oversight_info/has_dmc`

- **Association:** effect = 0.064 (cramers_v), n_valid = 13,941
- **Provenance:** demoted_confounded

`oversight_info/has_dmc` is an oversight / regulatory flag that proxies for trial type and scale; its association with `failure_reason` is confounded through `intervention/intervention_type`, `phase`, and trial scale. The genuine oversight mechanisms (FDA-regulation -> approval_outcome; DMC early-stopping -> sae_rate / mortality_rate) are retained as explicit edges. (R10: confounded design_oversight->outcome.)

### `Radiation intervention Number`

- **Association:** effect = 0.061 (eta), n_valid = 20,769
- **Provenance:** demoted_confounded

`Radiation intervention Number` is a deterministic re-encoding / tally of `intervention/intervention_type`; its association with `failure_reason` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `smiless`

- **Association:** effect = 0.061 (eta), n_valid = 20,769
- **Provenance:** demoted_confounded

`smiless` is a deterministic re-encoding / tally of `intervention/intervention_name`; its association with `failure_reason` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `Device intervention Number`

- **Association:** effect = 0.060 (eta), n_valid = 10,204
- **Provenance:** demoted_confounded

`Device intervention Number` is a deterministic re-encoding / tally of `intervention/intervention_type`; its association with `failure_reason` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `brief_title`

- **Association:** effect = 0.055 (eta), n_valid = 20,769
- **Provenance:** demoted_confounded

`brief_title` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `failure_reason`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `study_design_info/primary_purpose`

- **Association:** effect = 0.055 (cramers_v), n_valid = 20,561
- **Provenance:** demoted_confounded

`study_design_info/primary_purpose` reaches the trial-success label `failure_reason` only through biology / efficacy and enrollment mediators already in the DAG (`biology_pass`, `failure_reason`, `enrollment`); no direct arrow. (R6: mediated design->label.)

### `study_design_info/intervention_model`

- **Association:** effect = 0.053 (cramers_v), n_valid = 20,298
- **Provenance:** demoted_confounded

`study_design_info/intervention_model` reaches the trial-success label `failure_reason` only through biology / efficacy and enrollment mediators already in the DAG (`biology_pass`, `failure_reason`, `enrollment`); no direct arrow. (R6: mediated design->label.)
