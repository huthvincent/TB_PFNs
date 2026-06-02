# sae_rate

- **Group:** `outcome_safety`
- **Dtype:** float [0,1]
- **Description:** Observed serious-adverse-event rate.
- **Associated partners (from `association.md`):** 56
  - Direct **causes** (parents of this feature): **11**
  - Direct **effects** (children of this feature): **6**
  - Associated but **no direct** causal edge: **39**

This per-feature file enumerates only **associated** partners. All other columns in `DAG.json` were ruled independent in the Stage-1 association screen and do not appear here. See `association.md` for the screen.

---

## Direct causes (11)

### `mortality_rate`

- **Association:** effect = 0.666 (abs_spearman), n_valid = 17,916
- **Mechanism:** `definitional`
- **Provenance:** explicit

ICH-GCP defines death as a serious adverse event, so mortality is a strict subset of SAE: any death contributes to sae_rate.

### `duration_year`

- **Association:** effect = 0.430 (abs_spearman), n_valid = 13,278
- **Mechanism:** `operational`
- **Provenance:** default_cross_tier

Longer / later trial timing (duration_year) accrues more events, raising the realised safety outcome (sae_rate).

### `duration_day`

- **Association:** effect = 0.430 (abs_spearman), n_valid = 13,278
- **Mechanism:** `operational`
- **Provenance:** explicit

Longer follow-up accumulates more adverse events; realised SAE rate increases with duration.

### `duration_month`

- **Association:** effect = 0.429 (abs_spearman), n_valid = 13,278
- **Mechanism:** `operational`
- **Provenance:** default_cross_tier

Longer / later trial timing (duration_month) accrues more events, raising the realised safety outcome (sae_rate).

### `eligibility/healthy_volunteers`

- **Association:** effect = 0.261 (eta), n_valid = 17,914
- **Mechanism:** `biological`
- **Provenance:** explicit

Healthy-volunteer trials show systematically lower SAE rates than diseased-population trials (no disease-driven AE component).

### `phase`

- **Association:** effect = 0.223 (eta), n_valid = 17,916
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Sponsor design decision (phase) that influences the realised safety outcome (sae_rate) through biology, population, or operations.

### `eligibility/maximum_age`

- **Association:** effect = 0.178 (abs_spearman), n_valid = 8,723
- **Mechanism:** `biological`
- **Provenance:** explicit

Older eligibility envelopes admit more comorbid participants and elevate background SAE rate.

### `oversight_info/has_dmc`

- **Association:** effect = 0.174 (eta), n_valid = 16,069
- **Mechanism:** `operational`
- **Provenance:** explicit

An active Data Monitoring Committee enforces early-stopping rules for safety, truncating realised SAE rates.

### `condition`

- **Association:** effect = 0.081 (abs_spearman), n_valid = 17,916
- **Mechanism:** `biological`
- **Provenance:** explicit

Disease-related adverse events differ across conditions, shifting the realised SAE rate.

### `eligibility/gender`

- **Association:** effect = 0.078 (eta), n_valid = 17,916
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Downstream-design field (eligibility/gender) shifts the realised safety outcome (sae_rate) through population biology or trial operations.

### `intervention/intervention_name`

- **Association:** effect = 0.056 (abs_spearman), n_valid = 17,916
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Sponsor design decision (intervention/intervention_name) that influences the realised safety outcome (sae_rate) through biology, population, or operations.

---

## Direct effects (6)

### `sae_YN`

- **Association:** effect = 0.831 (abs_spearman), n_valid = 17,916
- **Mechanism:** `deterministic`
- **Provenance:** explicit

sae_YN is the thresholded version of sae_rate.

### `dropout_rate`

- **Association:** effect = 0.342 (abs_spearman), n_valid = 17,873
- **Mechanism:** `biological`
- **Provenance:** explicit

Participants with serious adverse events frequently withdraw from the trial (either by choice or by protocol mandate); SAEs are a causal driver of dropout.

### `execution_fail`

- **Association:** effect = 0.185 (abs_spearman), n_valid = 17,903
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Realised safety outcome (sae_rate) feeds the trial-success label (execution_fail) directly (e.g., 'safety' failure category, regulatory rejection).

### `execution_pass`

- **Association:** effect = 0.185 (abs_spearman), n_valid = 17,903
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Realised safety outcome (sae_rate) feeds the trial-success label (execution_pass) directly (e.g., 'safety' failure category, regulatory rejection).

### `biology_fail`

- **Association:** effect = 0.084 (abs_spearman), n_valid = 5,792
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Realised safety outcome (sae_rate) feeds the trial-success label (biology_fail) directly (e.g., 'safety' failure category, regulatory rejection).

### `biology_pass`

- **Association:** effect = 0.084 (abs_spearman), n_valid = 5,792
- **Mechanism:** `biological`
- **Provenance:** explicit

An unacceptable SAE rate forces biology_pass=False via the 'safety' failure category.

---

## Associated but no direct causal edge (39)

### `mortality_YN`

- **Association:** effect = 0.632 (abs_spearman), n_valid = 17,916
- **Provenance:** explicit

Mediated through mortality_rate: mortality_YN <- mortality_rate -> sae_rate.

### `location/facility/address/city`

- **Association:** effect = 0.371 (abs_spearman), n_valid = 17,916
- **Provenance:** demoted_confounded

`location/facility/address/city` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `sae_rate`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `study_design_info/masking`

- **Association:** effect = 0.313 (eta), n_valid = 17,890
- **Provenance:** demoted_confounded

`study_design_info/masking` is a sponsor / methodology design choice with no direct biological pathway to the realised safety rate `sae_rate`; the association is confounded through `intervention/intervention_type` and `condition` (what is being studied), which carry the genuine safety edges. (R4: confounded design->safety.)

### `study_design_info/intervention_model`

- **Association:** effect = 0.271 (eta), n_valid = 17,857
- **Provenance:** demoted_confounded

`study_design_info/intervention_model` is a sponsor / methodology design choice with no direct biological pathway to the realised safety rate `sae_rate`; the association is confounded through `intervention/intervention_type` and `condition` (what is being studied), which carry the genuine safety edges. (R4: confounded design->safety.)

### `start_date`

- **Association:** effect = 0.257 (abs_spearman), n_valid = 13,278
- **Provenance:** demoted_confounded

`start_date` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `sae_rate`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `MaskingType-Participant`

- **Association:** effect = 0.220 (abs_spearman), n_valid = 17,890
- **Provenance:** demoted_confounded

`MaskingType-Participant` is a deterministic re-encoding / tally of `study_design_info/masking`; its association with `sae_rate` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `study_design_info/masking_num`

- **Association:** effect = 0.209 (abs_spearman), n_valid = 17,890
- **Provenance:** demoted_confounded

`study_design_info/masking_num` is a deterministic re-encoding / tally of `study_design_info/masking`; its association with `sae_rate` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `study_design_info/primary_purpose`

- **Association:** effect = 0.208 (eta), n_valid = 17,911
- **Provenance:** demoted_confounded

`study_design_info/primary_purpose` is a sponsor / methodology design choice with no direct biological pathway to the realised safety rate `sae_rate`; the association is confounded through `intervention/intervention_type` and `condition` (what is being studied), which carry the genuine safety edges. (R4: confounded design->safety.)

### `study_design_info/allocation`

- **Association:** effect = 0.200 (eta), n_valid = 13,259
- **Provenance:** demoted_confounded

`study_design_info/allocation` is a sponsor / methodology design choice with no direct biological pathway to the realised safety rate `sae_rate`; the association is confounded through `intervention/intervention_type` and `condition` (what is being studied), which carry the genuine safety edges. (R4: confounded design->safety.)

### `dropout_YN`

- **Association:** effect = 0.191 (abs_spearman), n_valid = 17,873
- **Provenance:** explicit

Mediated through dropout_rate.

### `condition_browse/mesh_term`

- **Association:** effect = 0.184 (abs_spearman), n_valid = 17,916
- **Provenance:** demoted_confounded

`condition_browse/mesh_term` is a deterministic re-encoding / tally of `condition`; its association with `sae_rate` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `MaskingType-Investigator`

- **Association:** effect = 0.182 (abs_spearman), n_valid = 17,890
- **Provenance:** demoted_confounded

`MaskingType-Investigator` is a deterministic re-encoding / tally of `study_design_info/masking`; its association with `sae_rate` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `number_of_arms`

- **Association:** effect = 0.160 (abs_spearman), n_valid = 17,886
- **Provenance:** demoted_confounded

`number_of_arms` is a sponsor / methodology design choice with no direct biological pathway to the realised safety rate `sae_rate`; the association is confounded through `intervention/intervention_type` and `condition` (what is being studied), which carry the genuine safety edges. (R4: confounded design->safety.)

### `Placebo Comparator Arm Number`

- **Association:** effect = 0.154 (abs_spearman), n_valid = 17,886
- **Provenance:** demoted_confounded

`Placebo Comparator Arm Number` is a deterministic re-encoding / tally of `study_design_info/intervention_model`; its association with `sae_rate` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `MaskingType-Outcomes Assessor`

- **Association:** effect = 0.144 (abs_spearman), n_valid = 17,890
- **Provenance:** demoted_confounded

`MaskingType-Outcomes Assessor` is a deterministic re-encoding / tally of `study_design_info/masking`; its association with `sae_rate` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `ipd_info_type-Statistical Analysis Plan (SAP)`

- **Association:** effect = 0.127 (abs_spearman), n_valid = 1,818
- **Provenance:** demoted_confounded

`ipd_info_type-Statistical Analysis Plan (SAP)` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `sae_rate`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `enrollment`

- **Association:** effect = 0.123 (abs_spearman), n_valid = 17,881
- **Provenance:** demoted_confounded

A rate is invariant to sample size in expectation; `enrollment -> sae_rate` is a threshold-crossing artifact, not a causal effect of N on the safety rate. (R3: rate invariance. Genuine enrollment effects are kept for trial timing and the 'poor enrollment' execution-failure pathway.)

### `MaskingType-Care Provider`

- **Association:** effect = 0.112 (abs_spearman), n_valid = 17,890
- **Provenance:** demoted_confounded

`MaskingType-Care Provider` is a deterministic re-encoding / tally of `study_design_info/masking`; its association with `sae_rate` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `Active Comparator Arm Number`

- **Association:** effect = 0.111 (abs_spearman), n_valid = 17,886
- **Provenance:** demoted_confounded

`Active Comparator Arm Number` is a deterministic re-encoding / tally of `study_design_info/intervention_model`; its association with `sae_rate` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `sponsors/lead_sponsor/agency_class`

- **Association:** effect = 0.110 (eta), n_valid = 17,916
- **Provenance:** demoted_confounded

`sponsors/lead_sponsor/agency_class` is a sponsor / methodology design choice with no direct biological pathway to the realised safety rate `sae_rate`; the association is confounded through `intervention/intervention_type` and `condition` (what is being studied), which carry the genuine safety edges. (R4: confounded design->safety.)

### `ipd_info_type-Informed Consent Form (ICF)`

- **Association:** effect = 0.107 (abs_spearman), n_valid = 1,818
- **Provenance:** demoted_confounded

`ipd_info_type-Informed Consent Form (ICF)` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `sae_rate`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `Biological intervention Number`

- **Association:** effect = 0.105 (abs_spearman), n_valid = 17,916
- **Provenance:** demoted_confounded

`Biological intervention Number` is a deterministic re-encoding / tally of `intervention/intervention_type`; its association with `sae_rate` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `Radiation intervention Number`

- **Association:** effect = 0.098 (abs_spearman), n_valid = 17,916
- **Provenance:** demoted_confounded

`Radiation intervention Number` is a deterministic re-encoding / tally of `intervention/intervention_type`; its association with `sae_rate` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `ipd_info_type-Study Protocol`

- **Association:** effect = 0.098 (abs_spearman), n_valid = 1,818
- **Provenance:** demoted_confounded

`ipd_info_type-Study Protocol` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `sae_rate`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `intervention_browse/mesh_term`

- **Association:** effect = 0.098 (abs_spearman), n_valid = 17,916
- **Provenance:** demoted_confounded

`intervention_browse/mesh_term` is a deterministic re-encoding / tally of `intervention/intervention_name`; its association with `sae_rate` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `oversight_info/is_fda_regulated_drug`

- **Association:** effect = 0.097 (eta), n_valid = 10,445
- **Provenance:** demoted_confounded

`oversight_info/is_fda_regulated_drug` is an oversight / regulatory flag that proxies for trial type and scale; its association with `sae_rate` is confounded through `intervention/intervention_type`, `phase`, and trial scale. The genuine oversight mechanisms (FDA-regulation -> approval_outcome; DMC early-stopping -> sae_rate / mortality_rate) are retained as explicit edges. (R10: confounded design_oversight->outcome.)

### `icdcode`

- **Association:** effect = 0.086 (abs_spearman), n_valid = 17,916
- **Provenance:** demoted_confounded

`icdcode` is a deterministic re-encoding / tally of `condition`; its association with `sae_rate` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `ipd_info_type-Analytic Code`

- **Association:** effect = 0.078 (abs_spearman), n_valid = 1,818
- **Provenance:** demoted_confounded

`ipd_info_type-Analytic Code` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `sae_rate`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `patient_data/sharing_ipd`

- **Association:** effect = 0.078 (eta), n_valid = 9,941
- **Provenance:** demoted_confounded

`patient_data/sharing_ipd` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `sae_rate`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `ipd_info_type-Clinical Study Report (CSR)`

- **Association:** effect = 0.078 (abs_spearman), n_valid = 1,818
- **Provenance:** demoted_confounded

`ipd_info_type-Clinical Study Report (CSR)` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `sae_rate`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `smiless`

- **Association:** effect = 0.075 (abs_spearman), n_valid = 17,916
- **Provenance:** demoted_confounded

`smiless` is a deterministic re-encoding / tally of `intervention/intervention_name`; its association with `sae_rate` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `responsible_party/responsible_party_type`

- **Association:** effect = 0.071 (eta), n_valid = 17,899
- **Provenance:** demoted_confounded

`responsible_party/responsible_party_type` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `sae_rate`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `No Intervention Arm Number`

- **Association:** effect = 0.069 (abs_spearman), n_valid = 17,886
- **Provenance:** demoted_confounded

`No Intervention Arm Number` is a deterministic re-encoding / tally of `study_design_info/intervention_model`; its association with `sae_rate` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `Behavioral intervention Number`

- **Association:** effect = 0.066 (abs_spearman), n_valid = 17,916
- **Provenance:** demoted_confounded

`Behavioral intervention Number` is a deterministic re-encoding / tally of `intervention/intervention_type`; its association with `sae_rate` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `has_expanded_access`

- **Association:** effect = 0.064 (eta), n_valid = 17,570
- **Provenance:** demoted_confounded

`has_expanded_access` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `sae_rate`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `Experimental Arm Number`

- **Association:** effect = 0.060 (abs_spearman), n_valid = 17,886
- **Provenance:** demoted_confounded

`Experimental Arm Number` is a deterministic re-encoding / tally of `study_design_info/intervention_model`; its association with `sae_rate` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `brief_title`

- **Association:** effect = 0.060 (abs_spearman), n_valid = 17,916
- **Provenance:** demoted_confounded

`brief_title` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `sae_rate`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)

### `Other Arm Number`

- **Association:** effect = 0.055 (abs_spearman), n_valid = 17,886
- **Provenance:** demoted_confounded

`Other Arm Number` is a deterministic re-encoding / tally of `study_design_info/intervention_model`; its association with `sae_rate` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)

### `Device intervention Number`

- **Association:** effect = 0.053 (abs_spearman), n_valid = 17,916
- **Provenance:** demoted_confounded

`Device intervention Number` is a deterministic re-encoding / tally of `intervention/intervention_type`; its association with `sae_rate` is fully mediated through that definitional parent, which carries the genuine causal edge. (R1: proxy source.)
