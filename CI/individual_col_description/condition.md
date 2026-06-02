# condition

- **Group:** `design_top`
- **Dtype:** high_cardinality_text
- **Description:** Sponsor-reported disease / condition label (free-text). Tested in the association screen via token count.
- **Associated partners (from `association.md`):** 28
  - Direct **causes** (parents of this feature): **0**
  - Direct **effects** (children of this feature): **11**
  - Associated but **no direct** causal edge: **17**

This per-feature file enumerates only **associated** partners. All other columns in `DAG.json` were ruled independent in the Stage-1 association screen and do not appear here. See `association.md` for the screen.

---

## Direct causes (0)

_(none)_

---

## Direct effects (11)

### `icdcode`

- **Association:** effect = 0.531 (abs_spearman), n_valid = 81,786
- **Mechanism:** `definitional`
- **Provenance:** explicit

ICD codes are tagged from the condition text by an external annotation pipeline.

### `condition_browse/mesh_term`

- **Association:** effect = 0.408 (abs_spearman), n_valid = 81,786
- **Mechanism:** `definitional`
- **Provenance:** explicit

condition_browse/mesh_term is the MeSH-vocabulary normalisation of the free-text condition; the codes are looked up from the condition string.

### `duration_month`

- **Association:** effect = 0.131 (abs_spearman), n_valid = 42,855
- **Mechanism:** `design_choice`
- **Provenance:** default_cross_tier

Sponsor design decision (condition) that drives the realised trial-duration timeline (duration_month).

### `duration_year`

- **Association:** effect = 0.131 (abs_spearman), n_valid = 42,855
- **Mechanism:** `design_choice`
- **Provenance:** default_cross_tier

Sponsor design decision (condition) that drives the realised trial-duration timeline (duration_year).

### `duration_day`

- **Association:** effect = 0.131 (abs_spearman), n_valid = 42,855
- **Mechanism:** `design_choice`
- **Provenance:** default_cross_tier

Sponsor design decision (condition) that drives the realised trial-duration timeline (duration_day).

### `mortality_rate`

- **Association:** effect = 0.110 (abs_spearman), n_valid = 17,916
- **Mechanism:** `biological`
- **Provenance:** explicit

Background disease mortality differs by orders of magnitude across conditions (oncology vs migraine); condition drives the realised mortality rate.

### `mortality_YN`

- **Association:** effect = 0.085 (abs_spearman), n_valid = 17,916
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Sponsor design decision (condition) that influences the realised safety outcome (mortality_YN) through biology, population, or operations.

### `study_design_info/primary_purpose`

- **Association:** effect = 0.082 (eta), n_valid = 80,983
- **Mechanism:** `design_choice`
- **Provenance:** explicit

The disease being studied directly determines whether a sponsor designs a Treatment, Prevention, Diagnostic, or Screening trial.

### `sae_rate`

- **Association:** effect = 0.081 (abs_spearman), n_valid = 17,916
- **Mechanism:** `biological`
- **Provenance:** explicit

Disease-related adverse events differ across conditions, shifting the realised SAE rate.

### `approval_outcome`

- **Association:** effect = 0.061 (abs_spearman), n_valid = 30,683
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Sponsor design decision (condition) that influences the trial-success label (approval_outcome) through the trial's biological and regulatory pathway.

### `eligibility/healthy_volunteers`

- **Association:** effect = 0.058 (eta), n_valid = 81,613
- **Mechanism:** `design_choice`
- **Provenance:** default_cross_tier

Sponsor design decision made at registration (condition) that constrains a downstream design field (eligibility/healthy_volunteers).

---

## Associated but no direct causal edge (17)

### `sponsors/lead_sponsor/agency_class`

- **Association:** effect = 0.177 (eta), n_valid = 71,221
- **Provenance:** explicit

Both jointly chosen; sponsors specialise in indication portfolios but neither column directly causes the other.

### `ipd_info_type-Informed Consent Form (ICF)`

- **Association:** effect = 0.128 (abs_spearman), n_valid = 2,145
- **Provenance:** demoted_confounded

`condition` has no direct mechanism that sets the oversight / policy field `ipd_info_type-Informed Consent Form (ICF)`; the association is confounded through sponsor class and trial type. (R8: confounded ->design_oversight.)

### `Other intervention Number`

- **Association:** effect = 0.093 (abs_spearman), n_valid = 71,221
- **Provenance:** demoted_confounded

`Other intervention Number` is a deterministic descendant of its single definitional design parent; `condition` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `ipd_info_type-Statistical Analysis Plan (SAP)`

- **Association:** effect = 0.090 (abs_spearman), n_valid = 2,297
- **Provenance:** demoted_confounded

`condition` has no direct mechanism that sets the oversight / policy field `ipd_info_type-Statistical Analysis Plan (SAP)`; the association is confounded through sponsor class and trial type. (R8: confounded ->design_oversight.)

### `study_design_info/intervention_model`

- **Association:** effect = 0.077 (eta), n_valid = 80,897
- **Provenance:** explicit

Both jointly chosen design decisions; no direct arrow.

### `study_design_info/masking`

- **Association:** effect = 0.076 (eta), n_valid = 75,043
- **Provenance:** explicit

Both jointly chosen design decisions; no direct arrow.

### `Procedure intervention Number`

- **Association:** effect = 0.073 (abs_spearman), n_valid = 71,221
- **Provenance:** demoted_confounded

`Procedure intervention Number` is a deterministic descendant of its single definitional design parent; `condition` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `intervention_browse/mesh_term`

- **Association:** effect = 0.065 (abs_spearman), n_valid = 81,786
- **Provenance:** demoted_confounded

`intervention_browse/mesh_term` is a deterministic descendant of its single definitional design parent; `condition` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `ipd_info_type-Clinical Study Report (CSR)`

- **Association:** effect = 0.065 (abs_spearman), n_valid = 2,145
- **Provenance:** demoted_confounded

`condition` has no direct mechanism that sets the oversight / policy field `ipd_info_type-Clinical Study Report (CSR)`; the association is confounded through sponsor class and trial type. (R8: confounded ->design_oversight.)

### `number_of_arms`

- **Association:** effect = 0.062 (abs_spearman), n_valid = 78,123
- **Provenance:** demoted_confounded

`number_of_arms` is a deterministic descendant of its single definitional design parent; `condition` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `MaskingType-Investigator`

- **Association:** effect = 0.059 (abs_spearman), n_valid = 81,170
- **Provenance:** demoted_confounded

`MaskingType-Investigator` is a deterministic descendant of its single definitional design parent; `condition` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `start_date`

- **Association:** effect = 0.056 (abs_spearman), n_valid = 42,855
- **Provenance:** demoted_confounded

`condition` has no concrete causal mechanism that sets `start_date`. Trial size, eligible population, calendar start date, site geography and the free-text title are not directly caused by `condition`; the association is a jointly-chosen-design / sponsor-footprint / secular-trend confound. (R9: spurious design->planning/eligibility.)

### `MaskingType-Participant`

- **Association:** effect = 0.055 (abs_spearman), n_valid = 81,170
- **Provenance:** demoted_confounded

`MaskingType-Participant` is a deterministic descendant of its single definitional design parent; `condition` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `oversight_info/has_dmc`

- **Association:** effect = 0.054 (eta), n_valid = 45,926
- **Provenance:** demoted_confounded

`condition` has no direct mechanism that sets the oversight / policy field `oversight_info/has_dmc`; the association is confounded through sponsor class and trial type. (R8: confounded ->design_oversight.)

### `phase`

- **Association:** effect = 0.051 (eta), n_valid = 81,786
- **Provenance:** explicit

Both jointly chosen at registration; a specific disease can be at any phase depending on the drug being tested.

### `Placebo Comparator Arm Number`

- **Association:** effect = 0.051 (abs_spearman), n_valid = 78,123
- **Provenance:** demoted_confounded

`Placebo Comparator Arm Number` is a deterministic descendant of its single definitional design parent; `condition` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `study_design_info/allocation`

- **Association:** effect = 0.051 (eta), n_valid = 62,081
- **Provenance:** explicit

Both jointly chosen design decisions; no direct arrow.
