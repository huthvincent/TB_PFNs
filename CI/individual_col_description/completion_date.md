# completion_date

- **Group:** `outcome_timing`
- **Dtype:** date (parsed to days)
- **Description:** Reported completion date of the trial.
- **Associated partners (from `association.md`):** 28
  - Direct **causes** (parents of this feature): **6**
  - Direct **effects** (children of this feature): **7**
  - Associated but **no direct** causal edge: **15**

This per-feature file enumerates only **associated** partners. All other columns in `DAG.json` were ruled independent in the Stage-1 association screen and do not appear here. See `association.md` for the screen.

---

## Direct causes (6)

### `start_date`

- **Association:** effect = 0.868 (abs_spearman), n_valid = 42,855
- **Mechanism:** `operational`
- **Provenance:** explicit

The trial cannot complete before it has started; start_date temporally precedes completion_date.

### `study_design_info/intervention_model`

- **Association:** effect = 0.123 (eta), n_valid = 42,592
- **Mechanism:** `design_choice`
- **Provenance:** default_cross_tier

Sponsor design decision (study_design_info/intervention_model) that drives the realised trial-duration timeline (completion_date).

### `enrollment`

- **Association:** effect = 0.113 (abs_spearman), n_valid = 16,162
- **Mechanism:** `operational`
- **Provenance:** explicit

Larger planned enrollment requires a longer recruitment window plus follow-up, pushing completion_date later.

### `sponsors/lead_sponsor/agency_class`

- **Association:** effect = 0.103 (eta), n_valid = 42,855
- **Mechanism:** `design_choice`
- **Provenance:** default_cross_tier

Sponsor design decision (sponsors/lead_sponsor/agency_class) that drives the realised trial-duration timeline (completion_date).

### `phase`

- **Association:** effect = 0.081 (eta), n_valid = 42,855
- **Mechanism:** `design_choice`
- **Provenance:** default_cross_tier

Sponsor design decision (phase) that drives the realised trial-duration timeline (completion_date).

### `intervention/intervention_name`

- **Association:** effect = 0.054 (abs_spearman), n_valid = 42,855
- **Mechanism:** `design_choice`
- **Provenance:** default_cross_tier

Sponsor design decision (intervention/intervention_name) that drives the realised trial-duration timeline (completion_date).

---

## Direct effects (7)

### `approval_outcome`

- **Association:** effect = 0.333 (abs_spearman), n_valid = 9,263
- **Mechanism:** `operational`
- **Provenance:** default_cross_tier

Trial timing (completion_date) propagates into the post-hoc trial-success label (approval_outcome).

### `execution_fail`

- **Association:** effect = 0.139 (abs_spearman), n_valid = 20,062
- **Mechanism:** `operational`
- **Provenance:** default_cross_tier

Trial timing (completion_date) propagates into the post-hoc trial-success label (execution_fail).

### `execution_pass`

- **Association:** effect = 0.139 (abs_spearman), n_valid = 20,062
- **Mechanism:** `operational`
- **Provenance:** default_cross_tier

Trial timing (completion_date) propagates into the post-hoc trial-success label (execution_pass).

### `failure_reason`

- **Association:** effect = 0.115 (eta), n_valid = 6,904
- **Mechanism:** `operational`
- **Provenance:** default_cross_tier

Trial timing (completion_date) propagates into the post-hoc trial-success label (failure_reason).

### `biology_pass`

- **Association:** effect = 0.076 (abs_spearman), n_valid = 10,917
- **Mechanism:** `operational`
- **Provenance:** default_cross_tier

Trial timing (completion_date) propagates into the post-hoc trial-success label (biology_pass).

### `biology_fail`

- **Association:** effect = 0.076 (abs_spearman), n_valid = 10,917
- **Mechanism:** `operational`
- **Provenance:** default_cross_tier

Trial timing (completion_date) propagates into the post-hoc trial-success label (biology_fail).

### `dropout_YN`

- **Association:** effect = 0.053 (abs_spearman), n_valid = 16,162
- **Mechanism:** `operational`
- **Provenance:** default_cross_tier

Longer / later trial timing (completion_date) accrues more events, raising the realised safety outcome (dropout_YN).

---

## Associated but no direct causal edge (15)

### `patient_data/sharing_ipd`

- **Association:** effect = 0.200 (eta), n_valid = 9,341
- **Provenance:** demoted_confounded

`patient_data/sharing_ipd` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `completion_date`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `study_design_info/masking`

- **Association:** effect = 0.182 (eta), n_valid = 42,635
- **Provenance:** demoted_confounded

`study_design_info/masking` affects the trial timeline only through `enrollment` / `study_design_info/intervention_model`, the direct parents of trial duration; the marginal association with `completion_date` is mediated, not direct. (R5: mediated design->timing.)

### `ipd_info_type-Clinical Study Report (CSR)`

- **Association:** effect = 0.140 (abs_spearman), n_valid = 1,728
- **Provenance:** demoted_confounded

`ipd_info_type-Clinical Study Report (CSR)` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `completion_date`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `intervention_browse/mesh_term`

- **Association:** effect = 0.112 (abs_spearman), n_valid = 42,855
- **Provenance:** demoted_confounded

`intervention_browse/mesh_term` is a deterministic re-encoding / tally of `intervention/intervention_name`; its association with `completion_date` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `responsible_party/responsible_party_type`

- **Association:** effect = 0.109 (eta), n_valid = 42,745
- **Provenance:** demoted_confounded

`responsible_party/responsible_party_type` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `completion_date`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `oversight_info/has_dmc`

- **Association:** effect = 0.099 (eta), n_valid = 14,181
- **Provenance:** demoted_confounded

`oversight_info/has_dmc` is an oversight / regulatory flag that proxies for trial type and scale; its association with `completion_date` is confounded through `intervention/intervention_type`, `phase`, and trial scale. The genuine oversight mechanisms (FDA-regulation -> approval_outcome; DMC early-stopping -> sae_rate / mortality_rate) are retained as explicit edges. (R10: confounded design_oversight->outcome.)

### `ipd_info_type-Analytic Code`

- **Association:** effect = 0.092 (abs_spearman), n_valid = 1,728
- **Provenance:** demoted_confounded

`ipd_info_type-Analytic Code` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `completion_date`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `smiless`

- **Association:** effect = 0.090 (abs_spearman), n_valid = 42,855
- **Provenance:** demoted_confounded

`smiless` is a deterministic re-encoding / tally of `intervention/intervention_name`; its association with `completion_date` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `oversight_info/is_fda_regulated_drug`

- **Association:** effect = 0.087 (eta), n_valid = 9,820
- **Provenance:** demoted_confounded

`oversight_info/is_fda_regulated_drug` is an oversight / regulatory flag that proxies for trial type and scale; its association with `completion_date` is confounded through `intervention/intervention_type`, `phase`, and trial scale. The genuine oversight mechanisms (FDA-regulation -> approval_outcome; DMC early-stopping -> sae_rate / mortality_rate) are retained as explicit edges. (R10: confounded design_oversight->outcome.)

### `ipd_info_type-Informed Consent Form (ICF)`

- **Association:** effect = 0.086 (abs_spearman), n_valid = 1,728
- **Provenance:** demoted_confounded

`ipd_info_type-Informed Consent Form (ICF)` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `completion_date`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `ipd_info_type-Study Protocol`

- **Association:** effect = 0.077 (abs_spearman), n_valid = 1,728
- **Provenance:** demoted_confounded

`ipd_info_type-Study Protocol` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `completion_date`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `eligibility/healthy_volunteers`

- **Association:** effect = 0.060 (eta), n_valid = 42,833
- **Provenance:** demoted_confounded

`eligibility/healthy_volunteers` affects the trial timeline only through `enrollment` / `study_design_info/intervention_model`, the direct parents of trial duration; the marginal association with `completion_date` is mediated, not direct. (R5: mediated design->timing.)

### `Combination Product intervention Number`

- **Association:** effect = 0.054 (abs_spearman), n_valid = 42,855
- **Provenance:** demoted_confounded

`Combination Product intervention Number` is a deterministic re-encoding / tally of `intervention/intervention_type`; its association with `completion_date` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `MaskingType-Care Provider`

- **Association:** effect = 0.052 (abs_spearman), n_valid = 42,635
- **Provenance:** demoted_confounded

`MaskingType-Care Provider` is a deterministic re-encoding / tally of `study_design_info/masking`; its association with `completion_date` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `MaskingType-Outcomes Assessor`

- **Association:** effect = 0.051 (abs_spearman), n_valid = 42,635
- **Provenance:** demoted_confounded

`MaskingType-Outcomes Assessor` is a deterministic re-encoding / tally of `study_design_info/masking`; its association with `completion_date` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)
