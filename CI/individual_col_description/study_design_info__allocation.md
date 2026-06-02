# study_design_info/allocation

- **Group:** `design_top`
- **Dtype:** categorical
- **Description:** Randomized / Non-Randomized / N/A (N/A is consistent with single-group designs).
- **Associated partners (from `association.md`):** 32
  - Direct **causes** (parents of this feature): **2**
  - Direct **effects** (children of this feature): **2**
  - Associated but **no direct** causal edge: **28**

This per-feature file enumerates only **associated** partners. All other columns in `DAG.json` were ruled independent in the Stage-1 association screen and do not appear here. See `association.md` for the screen.

---

## Direct causes (2)

### `study_design_info/intervention_model`

- **Association:** effect = 0.554 (cramers_v), n_valid = 61,697
- **Mechanism:** `design_constraint`
- **Provenance:** explicit

Single Group Assignment forces allocation='N/A'; Parallel / Crossover / Factorial designs require Randomized or Non-Randomized allocation. The intervention model strictly constrains the feasible allocation.

### `phase`

- **Association:** effect = 0.250 (cramers_v), n_valid = 62,081
- **Mechanism:** `design_choice`
- **Provenance:** explicit

Phase 1 trials are usually non-randomised single-group; Phase 3 trials are typically randomised. Phase drives the allocation decision.

---

## Direct effects (2)

### `execution_fail`

- **Association:** effect = 0.093 (eta), n_valid = 39,412
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Sponsor design decision (study_design_info/allocation) that influences the trial-success label (execution_fail) through the trial's biological and regulatory pathway.

### `execution_pass`

- **Association:** effect = 0.093 (eta), n_valid = 39,412
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Sponsor design decision (study_design_info/allocation) that influences the trial-success label (execution_pass) through the trial's biological and regulatory pathway.

---

## Associated but no direct causal edge (28)

### `study_design_info/masking`

- **Association:** effect = 0.488 (cramers_v), n_valid = 56,864
- **Provenance:** explicit

Both methodological choices made jointly; no direct arrow.

### `MaskingType-Participant`

- **Association:** effect = 0.436 (eta), n_valid = 61,818
- **Provenance:** demoted_confounded

`MaskingType-Participant` is a deterministic descendant of its single definitional design parent; `study_design_info/allocation` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `study_design_info/masking_num`

- **Association:** effect = 0.430 (eta), n_valid = 61,818
- **Provenance:** demoted_confounded

`study_design_info/masking_num` is a deterministic descendant of its single definitional design parent; `study_design_info/allocation` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `MaskingType-Investigator`

- **Association:** effect = 0.405 (eta), n_valid = 61,818
- **Provenance:** demoted_confounded

`MaskingType-Investigator` is a deterministic descendant of its single definitional design parent; `study_design_info/allocation` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `MaskingType-Care Provider`

- **Association:** effect = 0.269 (eta), n_valid = 61,818
- **Provenance:** demoted_confounded

`MaskingType-Care Provider` is a deterministic descendant of its single definitional design parent; `study_design_info/allocation` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `MaskingType-Outcomes Assessor`

- **Association:** effect = 0.268 (eta), n_valid = 61,818
- **Provenance:** demoted_confounded

`MaskingType-Outcomes Assessor` is a deterministic descendant of its single definitional design parent; `study_design_info/allocation` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `Placebo Comparator Arm Number`

- **Association:** effect = 0.261 (eta), n_valid = 59,269
- **Provenance:** demoted_confounded

`Placebo Comparator Arm Number` is a deterministic descendant of its single definitional design parent; `study_design_info/allocation` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `sae_rate`

- **Association:** effect = 0.200 (eta), n_valid = 13,259
- **Provenance:** demoted_confounded

`study_design_info/allocation` is a sponsor / methodology design choice with no direct biological pathway to the realised safety rate `sae_rate`; the association is confounded through `intervention/intervention_type` and `condition` (what is being studied), which carry the genuine safety edges. (R4: confounded design->safety.)

### `Active Comparator Arm Number`

- **Association:** effect = 0.167 (eta), n_valid = 52,870
- **Provenance:** demoted_confounded

`Active Comparator Arm Number` is a deterministic descendant of its single definitional design parent; `study_design_info/allocation` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `mortality_rate`

- **Association:** effect = 0.148 (eta), n_valid = 13,259
- **Provenance:** demoted_confounded

`study_design_info/allocation` is a sponsor / methodology design choice with no direct biological pathway to the realised safety rate `mortality_rate`; the association is confounded through `intervention/intervention_type` and `condition` (what is being studied), which carry the genuine safety edges. (R4: confounded design->safety.)

### `Experimental Arm Number`

- **Association:** effect = 0.146 (eta), n_valid = 59,269
- **Provenance:** demoted_confounded

`Experimental Arm Number` is a deterministic descendant of its single definitional design parent; `study_design_info/allocation` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `dropout_rate`

- **Association:** effect = 0.120 (eta), n_valid = 29,014
- **Provenance:** demoted_confounded

`study_design_info/allocation` is a sponsor / methodology design choice with no direct biological pathway to the realised safety rate `dropout_rate`; the association is confounded through `intervention/intervention_type` and `condition` (what is being studied), which carry the genuine safety edges. (R4: confounded design->safety.)

### `study_design_info/primary_purpose`

- **Association:** effect = 0.105 (cramers_v), n_valid = 61,425
- **Provenance:** explicit

Both jointly chosen design decisions.

### `ipd_info_type-Clinical Study Report (CSR)`

- **Association:** effect = 0.097 (eta), n_valid = 1,724
- **Provenance:** demoted_confounded

`study_design_info/allocation` has no direct mechanism that sets the oversight / policy field `ipd_info_type-Clinical Study Report (CSR)`; the association is confounded through sponsor class and trial type. (R8: confounded ->design_oversight.)

### `intervention/intervention_name`

- **Association:** effect = 0.096 (eta), n_valid = 62,081
- **Provenance:** explicit

Both jointly chosen sponsor design decisions; no direct arrow.

### `duration_day`

- **Association:** effect = 0.092 (eta), n_valid = 32,550
- **Provenance:** demoted_confounded

`study_design_info/allocation` affects the trial timeline only through `enrollment` / `study_design_info/intervention_model`, the direct parents of trial duration; the marginal association with `duration_day` is mediated, not direct. (R5: mediated design->timing.)

### `duration_year`

- **Association:** effect = 0.092 (eta), n_valid = 32,550
- **Provenance:** demoted_confounded

`study_design_info/allocation` affects the trial timeline only through `enrollment` / `study_design_info/intervention_model`, the direct parents of trial duration; the marginal association with `duration_year` is mediated, not direct. (R5: mediated design->timing.)

### `duration_month`

- **Association:** effect = 0.092 (eta), n_valid = 32,550
- **Provenance:** demoted_confounded

`study_design_info/allocation` affects the trial timeline only through `enrollment` / `study_design_info/intervention_model`, the direct parents of trial duration; the marginal association with `duration_month` is mediated, not direct. (R5: mediated design->timing.)

### `Drug intervention Number`

- **Association:** effect = 0.088 (eta), n_valid = 62,081
- **Provenance:** demoted_confounded

`Drug intervention Number` is a deterministic descendant of its single definitional design parent; `study_design_info/allocation` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `dropout_YN`

- **Association:** effect = 0.076 (eta), n_valid = 29,014
- **Provenance:** demoted_confounded

`study_design_info/allocation` is a sponsor / methodology design choice with no direct biological pathway to the realised safety rate `dropout_YN`; the association is confounded through `intervention/intervention_type` and `condition` (what is being studied), which carry the genuine safety edges. (R4: confounded design->safety.)

### `location/facility/address/city`

- **Association:** effect = 0.074 (eta), n_valid = 62,081
- **Provenance:** demoted_confounded

`study_design_info/allocation` has no concrete causal mechanism that sets `location/facility/address/city`. Trial size, eligible population, calendar start date, site geography and the free-text title are not directly caused by `study_design_info/allocation`; the association is a jointly-chosen-design / sponsor-footprint / secular-trend confound. (R9: spurious design->planning/eligibility.)

### `oversight_info/has_dmc`

- **Association:** effect = 0.071 (cramers_v), n_valid = 34,580
- **Provenance:** demoted_confounded

`study_design_info/allocation` has no direct mechanism that sets the oversight / policy field `oversight_info/has_dmc`; the association is confounded through sponsor class and trial type. (R8: confounded ->design_oversight.)

### `responsible_party/responsible_party_type`

- **Association:** effect = 0.071 (cramers_v), n_valid = 51,309
- **Provenance:** demoted_confounded

`study_design_info/allocation` has no direct mechanism that sets the oversight / policy field `responsible_party/responsible_party_type`; the association is confounded through sponsor class and trial type. (R8: confounded ->design_oversight.)

### `mortality_YN`

- **Association:** effect = 0.064 (eta), n_valid = 13,259
- **Provenance:** demoted_confounded

`study_design_info/allocation` is a sponsor / methodology design choice with no direct biological pathway to the realised safety rate `mortality_YN`; the association is confounded through `intervention/intervention_type` and `condition` (what is being studied), which carry the genuine safety edges. (R4: confounded design->safety.)

### `sponsors/lead_sponsor/agency_class`

- **Association:** effect = 0.059 (cramers_v), n_valid = 54,376
- **Provenance:** explicit

Both jointly chosen.

### `Other intervention Number`

- **Association:** effect = 0.058 (eta), n_valid = 54,376
- **Provenance:** demoted_confounded

`Other intervention Number` is a deterministic descendant of its single definitional design parent; `study_design_info/allocation` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `eligibility/minimum_age`

- **Association:** effect = 0.054 (eta), n_valid = 60,725
- **Provenance:** demoted_confounded

`study_design_info/allocation` has no concrete causal mechanism that sets `eligibility/minimum_age`. Trial size, eligible population, calendar start date, site geography and the free-text title are not directly caused by `study_design_info/allocation`; the association is a jointly-chosen-design / sponsor-footprint / secular-trend confound. (R9: spurious design->planning/eligibility.)

### `condition`

- **Association:** effect = 0.051 (eta), n_valid = 62,081
- **Provenance:** explicit

Both jointly chosen design decisions; no direct arrow.
