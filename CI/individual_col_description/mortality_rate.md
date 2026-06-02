# mortality_rate

- **Group:** `outcome_safety`
- **Dtype:** float [0,1]
- **Description:** Observed mortality rate.
- **Associated partners (from `association.md`):** 49
  - Direct **causes** (parents of this feature): **9**
  - Direct **effects** (children of this feature): **9**
  - Associated but **no direct** causal edge: **31**

This per-feature file enumerates only **associated** partners. All other columns in `DAG.json` were ruled independent in the Stage-1 association screen and do not appear here. See `association.md` for the screen.

---

## Direct causes (9)

### `duration_day`

- **Association:** effect = 0.377 (abs_spearman), n_valid = 13,278
- **Mechanism:** `operational`
- **Provenance:** explicit

Longer follow-up in advanced-disease populations accrues more deaths.

### `duration_year`

- **Association:** effect = 0.377 (abs_spearman), n_valid = 13,278
- **Mechanism:** `operational`
- **Provenance:** default_cross_tier

Longer / later trial timing (duration_year) accrues more events, raising the realised safety outcome (mortality_rate).

### `duration_month`

- **Association:** effect = 0.377 (abs_spearman), n_valid = 13,278
- **Mechanism:** `operational`
- **Provenance:** default_cross_tier

Longer / later trial timing (duration_month) accrues more events, raising the realised safety outcome (mortality_rate).

### `eligibility/maximum_age`

- **Association:** effect = 0.253 (abs_spearman), n_valid = 8,723
- **Mechanism:** `biological`
- **Provenance:** explicit

Older eligibility envelopes raise background mortality.

### `phase`

- **Association:** effect = 0.204 (eta), n_valid = 17,916
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Sponsor design decision (phase) that influences the realised safety outcome (mortality_rate) through biology, population, or operations.

### `eligibility/healthy_volunteers`

- **Association:** effect = 0.184 (eta), n_valid = 17,914
- **Mechanism:** `biological`
- **Provenance:** explicit

Healthy-volunteer trials have near-zero background mortality.

### `oversight_info/has_dmc`

- **Association:** effect = 0.150 (eta), n_valid = 16,069
- **Mechanism:** `operational`
- **Provenance:** explicit

DMC-driven futility / safety stops cap accrued mortality before the protocol-defined endpoint.

### `condition`

- **Association:** effect = 0.110 (abs_spearman), n_valid = 17,916
- **Mechanism:** `biological`
- **Provenance:** explicit

Background disease mortality differs by orders of magnitude across conditions (oncology vs migraine); condition drives the realised mortality rate.

### `intervention/intervention_name`

- **Association:** effect = 0.097 (abs_spearman), n_valid = 17,916
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Sponsor design decision (intervention/intervention_name) that influences the realised safety outcome (mortality_rate) through biology, population, or operations.

---

## Direct effects (9)

### `mortality_YN`

- **Association:** effect = 0.960 (abs_spearman), n_valid = 17,916
- **Mechanism:** `deterministic`
- **Provenance:** explicit

mortality_YN is the thresholded version of mortality_rate.

### `sae_rate`

- **Association:** effect = 0.666 (abs_spearman), n_valid = 17,916
- **Mechanism:** `definitional`
- **Provenance:** explicit

ICH-GCP defines death as a serious adverse event, so mortality is a strict subset of SAE: any death contributes to sae_rate.

### `dropout_rate`

- **Association:** effect = 0.275 (abs_spearman), n_valid = 17,873
- **Mechanism:** `definitional`
- **Provenance:** explicit

Deaths are by definition dropouts (the participant can no longer continue), so mortality contributes to dropout_rate.

### `execution_fail`

- **Association:** effect = 0.111 (abs_spearman), n_valid = 17,903
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Realised safety outcome (mortality_rate) feeds the trial-success label (execution_fail) directly (e.g., 'safety' failure category, regulatory rejection).

### `execution_pass`

- **Association:** effect = 0.111 (abs_spearman), n_valid = 17,903
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Realised safety outcome (mortality_rate) feeds the trial-success label (execution_pass) directly (e.g., 'safety' failure category, regulatory rejection).

### `biology_fail`

- **Association:** effect = 0.081 (abs_spearman), n_valid = 5,792
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Realised safety outcome (mortality_rate) feeds the trial-success label (biology_fail) directly (e.g., 'safety' failure category, regulatory rejection).

### `biology_pass`

- **Association:** effect = 0.081 (abs_spearman), n_valid = 5,792
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Realised safety outcome (mortality_rate) feeds the trial-success label (biology_pass) directly (e.g., 'safety' failure category, regulatory rejection).

### `failure_reason`

- **Association:** effect = 0.072 (eta), n_valid = 3,199
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Realised safety outcome (mortality_rate) feeds the trial-success label (failure_reason) directly (e.g., 'safety' failure category, regulatory rejection).

### `approval_outcome`

- **Association:** effect = 0.056 (abs_spearman), n_valid = 5,434
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Realised safety outcome (mortality_rate) feeds the trial-success label (approval_outcome) directly (e.g., 'safety' failure category, regulatory rejection).

---

## Associated but no direct causal edge (31)

### `sae_YN`

- **Association:** effect = 0.456 (abs_spearman), n_valid = 17,916
- **Provenance:** explicit

Mediated through sae_rate: mortality_rate -> sae_rate -> sae_YN.

### `study_design_info/masking`

- **Association:** effect = 0.279 (eta), n_valid = 17,890
- **Provenance:** demoted_confounded

`study_design_info/masking` is a sponsor / methodology design choice with no direct biological pathway to the realised safety rate `mortality_rate`; the association is confounded through `intervention/intervention_type` and `condition` (what is being studied), which carry the genuine safety edges. (R4: confounded design->safety.)

### `location/facility/address/city`

- **Association:** effect = 0.265 (abs_spearman), n_valid = 17,916
- **Provenance:** demoted_confounded

`location/facility/address/city` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `mortality_rate`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `MaskingType-Participant`

- **Association:** effect = 0.230 (abs_spearman), n_valid = 17,890
- **Provenance:** demoted_confounded

`MaskingType-Participant` is a deterministic re-encoding / tally of `study_design_info/masking`; its association with `mortality_rate` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `study_design_info/masking_num`

- **Association:** effect = 0.221 (abs_spearman), n_valid = 17,890
- **Provenance:** demoted_confounded

`study_design_info/masking_num` is a deterministic re-encoding / tally of `study_design_info/masking`; its association with `mortality_rate` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `MaskingType-Investigator`

- **Association:** effect = 0.205 (abs_spearman), n_valid = 17,890
- **Provenance:** demoted_confounded

`MaskingType-Investigator` is a deterministic re-encoding / tally of `study_design_info/masking`; its association with `mortality_rate` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `start_date`

- **Association:** effect = 0.205 (abs_spearman), n_valid = 13,278
- **Provenance:** demoted_confounded

`start_date` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `mortality_rate`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `study_design_info/intervention_model`

- **Association:** effect = 0.202 (eta), n_valid = 17,857
- **Provenance:** demoted_confounded

`study_design_info/intervention_model` is a sponsor / methodology design choice with no direct biological pathway to the realised safety rate `mortality_rate`; the association is confounded through `intervention/intervention_type` and `condition` (what is being studied), which carry the genuine safety edges. (R4: confounded design->safety.)

### `Placebo Comparator Arm Number`

- **Association:** effect = 0.182 (abs_spearman), n_valid = 17,886
- **Provenance:** demoted_confounded

`Placebo Comparator Arm Number` is a deterministic re-encoding / tally of `study_design_info/intervention_model`; its association with `mortality_rate` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `study_design_info/primary_purpose`

- **Association:** effect = 0.169 (eta), n_valid = 17,911
- **Provenance:** demoted_confounded

`study_design_info/primary_purpose` is a sponsor / methodology design choice with no direct biological pathway to the realised safety rate `mortality_rate`; the association is confounded through `intervention/intervention_type` and `condition` (what is being studied), which carry the genuine safety edges. (R4: confounded design->safety.)

### `intervention_browse/mesh_term`

- **Association:** effect = 0.166 (abs_spearman), n_valid = 17,916
- **Provenance:** demoted_confounded

`intervention_browse/mesh_term` is a deterministic re-encoding / tally of `intervention/intervention_name`; its association with `mortality_rate` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `ipd_info_type-Clinical Study Report (CSR)`

- **Association:** effect = 0.159 (abs_spearman), n_valid = 1,818
- **Provenance:** demoted_confounded

`ipd_info_type-Clinical Study Report (CSR)` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `mortality_rate`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `enrollment`

- **Association:** effect = 0.152 (abs_spearman), n_valid = 17,881
- **Provenance:** demoted_confounded

A rate is invariant to sample size in expectation; `enrollment -> mortality_rate` is a threshold-crossing artifact, not a causal effect of N on the safety rate. (R3: rate invariance. Genuine enrollment effects are kept for trial timing and the 'poor enrollment' execution-failure pathway.)

### `study_design_info/allocation`

- **Association:** effect = 0.148 (eta), n_valid = 13,259
- **Provenance:** demoted_confounded

`study_design_info/allocation` is a sponsor / methodology design choice with no direct biological pathway to the realised safety rate `mortality_rate`; the association is confounded through `intervention/intervention_type` and `condition` (what is being studied), which carry the genuine safety edges. (R4: confounded design->safety.)

### `Radiation intervention Number`

- **Association:** effect = 0.146 (abs_spearman), n_valid = 17,916
- **Provenance:** demoted_confounded

`Radiation intervention Number` is a deterministic re-encoding / tally of `intervention/intervention_type`; its association with `mortality_rate` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `number_of_arms`

- **Association:** effect = 0.145 (abs_spearman), n_valid = 17,886
- **Provenance:** demoted_confounded

`number_of_arms` is a sponsor / methodology design choice with no direct biological pathway to the realised safety rate `mortality_rate`; the association is confounded through `intervention/intervention_type` and `condition` (what is being studied), which carry the genuine safety edges. (R4: confounded design->safety.)

### `MaskingType-Outcomes Assessor`

- **Association:** effect = 0.142 (abs_spearman), n_valid = 17,890
- **Provenance:** demoted_confounded

`MaskingType-Outcomes Assessor` is a deterministic re-encoding / tally of `study_design_info/masking`; its association with `mortality_rate` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `smiless`

- **Association:** effect = 0.139 (abs_spearman), n_valid = 17,916
- **Provenance:** demoted_confounded

`smiless` is a deterministic re-encoding / tally of `intervention/intervention_name`; its association with `mortality_rate` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `condition_browse/mesh_term`

- **Association:** effect = 0.134 (abs_spearman), n_valid = 17,916
- **Provenance:** demoted_confounded

`condition_browse/mesh_term` is a deterministic re-encoding / tally of `condition`; its association with `mortality_rate` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `MaskingType-Care Provider`

- **Association:** effect = 0.131 (abs_spearman), n_valid = 17,890
- **Provenance:** demoted_confounded

`MaskingType-Care Provider` is a deterministic re-encoding / tally of `study_design_info/masking`; its association with `mortality_rate` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `icdcode`

- **Association:** effect = 0.123 (abs_spearman), n_valid = 17,916
- **Provenance:** demoted_confounded

`icdcode` is a deterministic re-encoding / tally of `condition`; its association with `mortality_rate` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `ipd_info_type-Informed Consent Form (ICF)`

- **Association:** effect = 0.120 (abs_spearman), n_valid = 1,818
- **Provenance:** demoted_confounded

`ipd_info_type-Informed Consent Form (ICF)` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `mortality_rate`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `dropout_YN`

- **Association:** effect = 0.111 (abs_spearman), n_valid = 17,873
- **Provenance:** explicit

Mediated through dropout_rate.

### `sponsors/lead_sponsor/agency_class`

- **Association:** effect = 0.111 (eta), n_valid = 17,916
- **Provenance:** demoted_confounded

`sponsors/lead_sponsor/agency_class` is a sponsor / methodology design choice with no direct biological pathway to the realised safety rate `mortality_rate`; the association is confounded through `intervention/intervention_type` and `condition` (what is being studied), which carry the genuine safety edges. (R4: confounded design->safety.)

### `Procedure intervention Number`

- **Association:** effect = 0.092 (abs_spearman), n_valid = 17,916
- **Provenance:** demoted_confounded

`Procedure intervention Number` is a deterministic re-encoding / tally of `intervention/intervention_type`; its association with `mortality_rate` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `Biological intervention Number`

- **Association:** effect = 0.083 (abs_spearman), n_valid = 17,916
- **Provenance:** demoted_confounded

`Biological intervention Number` is a deterministic re-encoding / tally of `intervention/intervention_type`; its association with `mortality_rate` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `oversight_info/is_fda_regulated_drug`

- **Association:** effect = 0.080 (eta), n_valid = 10,445
- **Provenance:** demoted_confounded

`oversight_info/is_fda_regulated_drug` is an oversight / regulatory flag that proxies for trial type and scale; its association with `mortality_rate` is confounded through `intervention/intervention_type`, `phase`, and trial scale. The genuine oversight mechanisms (FDA-regulation -> approval_outcome; DMC early-stopping -> sae_rate / mortality_rate) are retained as explicit edges. (R10: confounded design_oversight->outcome.)

### `ipd_info_type-Study Protocol`

- **Association:** effect = 0.068 (abs_spearman), n_valid = 1,818
- **Provenance:** demoted_confounded

`ipd_info_type-Study Protocol` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `mortality_rate`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `ipd_info_type-Analytic Code`

- **Association:** effect = 0.064 (abs_spearman), n_valid = 1,818
- **Provenance:** demoted_confounded

`ipd_info_type-Analytic Code` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `mortality_rate`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `Drug intervention Number`

- **Association:** effect = 0.058 (abs_spearman), n_valid = 17,916
- **Provenance:** demoted_confounded

`Drug intervention Number` is a deterministic re-encoding / tally of `intervention/intervention_type`; its association with `mortality_rate` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `has_expanded_access`

- **Association:** effect = 0.054 (eta), n_valid = 17,570
- **Provenance:** demoted_confounded

`has_expanded_access` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `mortality_rate`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)
