# duration_year

- **Group:** `outcome_timing`
- **Dtype:** float
- **Description:** Total trial duration in years (duration_day / 365.25).
- **Associated partners (from `association.md`):** 40
  - Direct **causes** (parents of this feature): **7**
  - Direct **effects** (children of this feature): **9**
  - Associated but **no direct** causal edge: **24**

This per-feature file enumerates only **associated** partners. All other columns in `DAG.json` were ruled independent in the Stage-1 association screen and do not appear here. See `association.md` for the screen.

---

## Direct causes (7)

### `duration_day`

- **Association:** effect = 1.000 (abs_spearman), n_valid = 42,855
- **Mechanism:** `deterministic`
- **Provenance:** explicit

Unit conversion: duration_year = duration_day / 365.25.

### `sponsors/lead_sponsor/agency_class`

- **Association:** effect = 0.282 (eta), n_valid = 42,855
- **Mechanism:** `design_choice`
- **Provenance:** default_cross_tier

Sponsor design decision (sponsors/lead_sponsor/agency_class) that drives the realised trial-duration timeline (duration_year).

### `study_design_info/intervention_model`

- **Association:** effect = 0.249 (eta), n_valid = 42,592
- **Mechanism:** `design_choice`
- **Provenance:** default_cross_tier

Sponsor design decision (study_design_info/intervention_model) that drives the realised trial-duration timeline (duration_year).

### `phase`

- **Association:** effect = 0.223 (eta), n_valid = 42,855
- **Mechanism:** `design_choice`
- **Provenance:** default_cross_tier

Sponsor design decision (phase) that drives the realised trial-duration timeline (duration_year).

### `number_of_arms`

- **Association:** effect = 0.161 (abs_spearman), n_valid = 42,293
- **Mechanism:** `operational`
- **Provenance:** default_cross_tier

Downstream-design field (number_of_arms) shifts the operational timeline of the trial (duration_year).

### `condition`

- **Association:** effect = 0.131 (abs_spearman), n_valid = 42,855
- **Mechanism:** `design_choice`
- **Provenance:** default_cross_tier

Sponsor design decision (condition) that drives the realised trial-duration timeline (duration_year).

### `enrollment`

- **Association:** effect = 0.111 (abs_spearman), n_valid = 16,162
- **Mechanism:** `operational`
- **Provenance:** default_cross_tier

Downstream-design field (enrollment) shifts the operational timeline of the trial (duration_year).

---

## Direct effects (9)

### `sae_rate`

- **Association:** effect = 0.430 (abs_spearman), n_valid = 13,278
- **Mechanism:** `operational`
- **Provenance:** default_cross_tier

Longer / later trial timing (duration_year) accrues more events, raising the realised safety outcome (sae_rate).

### `mortality_rate`

- **Association:** effect = 0.377 (abs_spearman), n_valid = 13,278
- **Mechanism:** `operational`
- **Provenance:** default_cross_tier

Longer / later trial timing (duration_year) accrues more events, raising the realised safety outcome (mortality_rate).

### `mortality_YN`

- **Association:** effect = 0.359 (abs_spearman), n_valid = 13,278
- **Mechanism:** `operational`
- **Provenance:** default_cross_tier

Longer / later trial timing (duration_year) accrues more events, raising the realised safety outcome (mortality_YN).

### `sae_YN`

- **Association:** effect = 0.313 (abs_spearman), n_valid = 13,278
- **Mechanism:** `operational`
- **Provenance:** default_cross_tier

Longer / later trial timing (duration_year) accrues more events, raising the realised safety outcome (sae_YN).

### `dropout_rate`

- **Association:** effect = 0.252 (abs_spearman), n_valid = 16,162
- **Mechanism:** `operational`
- **Provenance:** default_cross_tier

Longer / later trial timing (duration_year) accrues more events, raising the realised safety outcome (dropout_rate).

### `execution_fail`

- **Association:** effect = 0.141 (abs_spearman), n_valid = 20,062
- **Mechanism:** `operational`
- **Provenance:** default_cross_tier

Trial timing (duration_year) propagates into the post-hoc trial-success label (execution_fail).

### `execution_pass`

- **Association:** effect = 0.141 (abs_spearman), n_valid = 20,062
- **Mechanism:** `operational`
- **Provenance:** default_cross_tier

Trial timing (duration_year) propagates into the post-hoc trial-success label (execution_pass).

### `dropout_YN`

- **Association:** effect = 0.131 (abs_spearman), n_valid = 16,162
- **Mechanism:** `operational`
- **Provenance:** default_cross_tier

Longer / later trial timing (duration_year) accrues more events, raising the realised safety outcome (dropout_YN).

### `failure_reason`

- **Association:** effect = 0.096 (eta), n_valid = 6,904
- **Mechanism:** `operational`
- **Provenance:** default_cross_tier

Trial timing (duration_year) propagates into the post-hoc trial-success label (failure_reason).

---

## Associated but no direct causal edge (24)

### `duration_month`

- **Association:** effect = 1.000 (abs_spearman), n_valid = 42,855
- **Provenance:** explicit

Both are deterministic unit conversions of duration_day; siblings under common parent duration_day, no direct causal arrow.

### `start_date`

- **Association:** effect = 0.425 (abs_spearman), n_valid = 42,855
- **Provenance:** explicit

Mediated through duration_day: start_date -> duration_day -> duration_year.

### `eligibility/healthy_volunteers`

- **Association:** effect = 0.351 (eta), n_valid = 42,833
- **Provenance:** demoted_confounded

`eligibility/healthy_volunteers` affects the trial timeline only through `enrollment` / `study_design_info/intervention_model`, the direct parents of trial duration; the marginal association with `duration_year` is mediated, not direct. (R5: mediated design->timing.)

### `condition_browse/mesh_term`

- **Association:** effect = 0.276 (abs_spearman), n_valid = 42,855
- **Provenance:** demoted_confounded

`condition_browse/mesh_term` is a deterministic re-encoding / tally of `condition`; its association with `duration_year` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `location/facility/address/city`

- **Association:** effect = 0.256 (abs_spearman), n_valid = 42,855
- **Provenance:** demoted_confounded

`location/facility/address/city` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `duration_year`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `oversight_info/has_dmc`

- **Association:** effect = 0.228 (eta), n_valid = 14,181
- **Provenance:** demoted_confounded

`oversight_info/has_dmc` is an oversight / regulatory flag that proxies for trial type and scale; its association with `duration_year` is confounded through `intervention/intervention_type`, `phase`, and trial scale. The genuine oversight mechanisms (FDA-regulation -> approval_outcome; DMC early-stopping -> sae_rate / mortality_rate) are retained as explicit edges. (R10: confounded design_oversight->outcome.)

### `eligibility/maximum_age`

- **Association:** effect = 0.202 (abs_spearman), n_valid = 24,161
- **Provenance:** demoted_confounded

`eligibility/maximum_age` affects the trial timeline only through `enrollment` / `study_design_info/intervention_model`, the direct parents of trial duration; the marginal association with `duration_year` is mediated, not direct. (R5: mediated design->timing.)

### `study_design_info/primary_purpose`

- **Association:** effect = 0.195 (eta), n_valid = 42,836
- **Provenance:** demoted_confounded

`study_design_info/primary_purpose` affects the trial timeline only through `enrollment` / `study_design_info/intervention_model`, the direct parents of trial duration; the marginal association with `duration_year` is mediated, not direct. (R5: mediated design->timing.)

### `study_design_info/masking`

- **Association:** effect = 0.156 (eta), n_valid = 42,635
- **Provenance:** demoted_confounded

`study_design_info/masking` affects the trial timeline only through `enrollment` / `study_design_info/intervention_model`, the direct parents of trial duration; the marginal association with `duration_year` is mediated, not direct. (R5: mediated design->timing.)

### `intervention_browse/mesh_term`

- **Association:** effect = 0.133 (abs_spearman), n_valid = 42,855
- **Provenance:** demoted_confounded

`intervention_browse/mesh_term` is a deterministic re-encoding / tally of `intervention/intervention_name`; its association with `duration_year` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `Radiation intervention Number`

- **Association:** effect = 0.131 (abs_spearman), n_valid = 42,855
- **Provenance:** demoted_confounded

`Radiation intervention Number` is a deterministic re-encoding / tally of `intervention/intervention_type`; its association with `duration_year` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `Experimental Arm Number`

- **Association:** effect = 0.120 (abs_spearman), n_valid = 42,293
- **Provenance:** demoted_confounded

`Experimental Arm Number` is a deterministic re-encoding / tally of `study_design_info/intervention_model`; its association with `duration_year` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `Procedure intervention Number`

- **Association:** effect = 0.104 (abs_spearman), n_valid = 42,855
- **Provenance:** demoted_confounded

`Procedure intervention Number` is a deterministic re-encoding / tally of `intervention/intervention_type`; its association with `duration_year` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `eligibility/gender`

- **Association:** effect = 0.104 (eta), n_valid = 42,855
- **Provenance:** demoted_confounded

`eligibility/gender` affects the trial timeline only through `enrollment` / `study_design_info/intervention_model`, the direct parents of trial duration; the marginal association with `duration_year` is mediated, not direct. (R5: mediated design->timing.)

### `icdcode`

- **Association:** effect = 0.103 (abs_spearman), n_valid = 42,855
- **Provenance:** demoted_confounded

`icdcode` is a deterministic re-encoding / tally of `condition`; its association with `duration_year` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `MaskingType-Participant`

- **Association:** effect = 0.102 (abs_spearman), n_valid = 42,635
- **Provenance:** demoted_confounded

`MaskingType-Participant` is a deterministic re-encoding / tally of `study_design_info/masking`; its association with `duration_year` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `study_design_info/allocation`

- **Association:** effect = 0.092 (eta), n_valid = 32,550
- **Provenance:** demoted_confounded

`study_design_info/allocation` affects the trial timeline only through `enrollment` / `study_design_info/intervention_model`, the direct parents of trial duration; the marginal association with `duration_year` is mediated, not direct. (R5: mediated design->timing.)

### `smiless`

- **Association:** effect = 0.090 (abs_spearman), n_valid = 42,855
- **Provenance:** demoted_confounded

`smiless` is a deterministic re-encoding / tally of `intervention/intervention_name`; its association with `duration_year` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `oversight_info/is_fda_regulated_drug`

- **Association:** effect = 0.090 (eta), n_valid = 9,820
- **Provenance:** demoted_confounded

`oversight_info/is_fda_regulated_drug` is an oversight / regulatory flag that proxies for trial type and scale; its association with `duration_year` is confounded through `intervention/intervention_type`, `phase`, and trial scale. The genuine oversight mechanisms (FDA-regulation -> approval_outcome; DMC early-stopping -> sae_rate / mortality_rate) are retained as explicit edges. (R10: confounded design_oversight->outcome.)

### `study_design_info/masking_num`

- **Association:** effect = 0.086 (abs_spearman), n_valid = 42,635
- **Provenance:** demoted_confounded

`study_design_info/masking_num` is a deterministic re-encoding / tally of `study_design_info/masking`; its association with `duration_year` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `MaskingType-Investigator`

- **Association:** effect = 0.084 (abs_spearman), n_valid = 42,635
- **Provenance:** demoted_confounded

`MaskingType-Investigator` is a deterministic re-encoding / tally of `study_design_info/masking`; its association with `duration_year` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `eligibility/minimum_age`

- **Association:** effect = 0.077 (abs_spearman), n_valid = 41,982
- **Provenance:** demoted_confounded

`eligibility/minimum_age` affects the trial timeline only through `enrollment` / `study_design_info/intervention_model`, the direct parents of trial duration; the marginal association with `duration_year` is mediated, not direct. (R5: mediated design->timing.)

### `responsible_party/responsible_party_type`

- **Association:** effect = 0.075 (eta), n_valid = 42,745
- **Provenance:** demoted_confounded

`responsible_party/responsible_party_type` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `duration_year`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `Other intervention Number`

- **Association:** effect = 0.057 (abs_spearman), n_valid = 42,855
- **Provenance:** demoted_confounded

`Other intervention Number` is a deterministic re-encoding / tally of `intervention/intervention_type`; its association with `duration_year` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)
