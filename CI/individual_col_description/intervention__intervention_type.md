# intervention/intervention_type

- **Group:** `design_top`
- **Dtype:** categorical_multivalued
- **Description:** Modality(ies) of intervention: Drug / Biological / Device / Behavioral / Procedure / Radiation / Dietary Supplement / Genetic / Diagnostic Test / Combination Product / Other.
- **Associated partners (from `association.md`):** 17
  - Direct **causes** (parents of this feature): **1**
  - Direct **effects** (children of this feature): **9**
  - Associated but **no direct** causal edge: **7**

This per-feature file enumerates only **associated** partners. All other columns in `DAG.json` were ruled independent in the Stage-1 association screen and do not appear here. See `association.md` for the screen.

---

## Direct causes (1)

### `study_design_info/primary_purpose`

- **Association:** effect = 0.053 (eta), n_valid = 80,983
- **Mechanism:** `design_constraint`
- **Provenance:** explicit

Diagnostic primary purpose forces intervention_type='Diagnostic Test'; Treatment is realised through Drug / Biological / Device / Behavioral / Procedure. Purpose constrains the feasible type set.

---

## Direct effects (9)

### `approval_outcome`

- **Association:** effect = 0.464 (abs_spearman), n_valid = 30,683
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Sponsor design decision (intervention/intervention_type) that influences the trial-success label (approval_outcome) through the trial's biological and regulatory pathway.

### `execution_pass`

- **Association:** effect = 0.377 (abs_spearman), n_valid = 52,772
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Sponsor design decision (intervention/intervention_type) that influences the trial-success label (execution_pass) through the trial's biological and regulatory pathway.

### `execution_fail`

- **Association:** effect = 0.377 (abs_spearman), n_valid = 52,772
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Sponsor design decision (intervention/intervention_type) that influences the trial-success label (execution_fail) through the trial's biological and regulatory pathway.

### `oversight_info/is_fda_regulated_drug`

- **Association:** effect = 0.133 (eta), n_valid = 13,761
- **Mechanism:** `regulatory`
- **Provenance:** explicit

Type in {Drug, Biological} triggers FDA drug regulation (NDA / BLA pathway) by definition.

### `failure_reason`

- **Association:** effect = 0.110 (eta), n_valid = 20,769
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Sponsor design decision (intervention/intervention_type) that influences the trial-success label (failure_reason) through the trial's biological and regulatory pathway.

### `ipd_info_type-Statistical Analysis Plan (SAP)`

- **Association:** effect = 0.095 (abs_spearman), n_valid = 2,297
- **Mechanism:** `design_choice`
- **Provenance:** default_cross_tier

Sponsor design decision made at registration (intervention/intervention_type) that constrains a downstream design field (ipd_info_type-Statistical Analysis Plan (SAP)).

### `ipd_info_type-Analytic Code`

- **Association:** effect = 0.077 (abs_spearman), n_valid = 2,297
- **Mechanism:** `design_choice`
- **Provenance:** default_cross_tier

Sponsor design decision made at registration (intervention/intervention_type) that constrains a downstream design field (ipd_info_type-Analytic Code).

### `eligibility/healthy_volunteers`

- **Association:** effect = 0.070 (eta), n_valid = 81,613
- **Mechanism:** `design_choice`
- **Provenance:** default_cross_tier

Sponsor design decision made at registration (intervention/intervention_type) that constrains a downstream design field (eligibility/healthy_volunteers).

### `Drug intervention Number`

- **Association:** effect = 0.061 (abs_spearman), n_valid = 81,786
- **Mechanism:** `deterministic`
- **Provenance:** explicit

Per-type intervention count is a tally over intervention_type's multi-valued list.

---

## Associated but no direct causal edge (7)

### `location/facility/address/city`

- **Association:** effect = 0.566 (abs_spearman), n_valid = 81,786
- **Provenance:** demoted_confounded

`intervention/intervention_type` has no concrete causal mechanism that sets `location/facility/address/city`. Trial size, eligible population, calendar start date, site geography and the free-text title are not directly caused by `intervention/intervention_type`; the association is a jointly-chosen-design / sponsor-footprint / secular-trend confound. (R9: spurious design->planning/eligibility.)

### `study_design_info/masking`

- **Association:** effect = 0.080 (eta), n_valid = 75,043
- **Provenance:** explicit

Both jointly chosen design decisions; no direct arrow.

### `Experimental Arm Number`

- **Association:** effect = 0.076 (abs_spearman), n_valid = 78,123
- **Provenance:** demoted_confounded

`Experimental Arm Number` is a deterministic descendant of its single definitional design parent; `intervention/intervention_type` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `number_of_arms`

- **Association:** effect = 0.071 (abs_spearman), n_valid = 78,123
- **Provenance:** demoted_confounded

`number_of_arms` is a deterministic descendant of its single definitional design parent; `intervention/intervention_type` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `MaskingType-Participant`

- **Association:** effect = 0.064 (abs_spearman), n_valid = 81,170
- **Provenance:** demoted_confounded

`MaskingType-Participant` is a deterministic descendant of its single definitional design parent; `intervention/intervention_type` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `MaskingType-Investigator`

- **Association:** effect = 0.064 (abs_spearman), n_valid = 81,170
- **Provenance:** demoted_confounded

`MaskingType-Investigator` is a deterministic descendant of its single definitional design parent; `intervention/intervention_type` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `eligibility/maximum_age`

- **Association:** effect = 0.054 (abs_spearman), n_valid = 42,760
- **Provenance:** demoted_confounded

`intervention/intervention_type` has no concrete causal mechanism that sets `eligibility/maximum_age`. Trial size, eligible population, calendar start date, site geography and the free-text title are not directly caused by `intervention/intervention_type`; the association is a jointly-chosen-design / sponsor-footprint / secular-trend confound. (R9: spurious design->planning/eligibility.)
