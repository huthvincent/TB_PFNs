# intervention/intervention_name

- **Group:** `design_top`
- **Dtype:** high_cardinality_text
- **Description:** Specific intervention name(s) — drug brand / generic, device model, behavioral programme, etc. Tested via token count.
- **Associated partners (from `association.md`):** 41
  - Direct **causes** (parents of this feature): **0**
  - Direct **effects** (children of this feature): **12**
  - Associated but **no direct** causal edge: **29**

This per-feature file enumerates only **associated** partners. All other columns in `DAG.json` were ruled independent in the Stage-1 association screen and do not appear here. See `association.md` for the screen.

---

## Direct causes (0)

_(none)_

---

## Direct effects (12)

### `intervention_browse/mesh_term`

- **Association:** effect = 0.394 (abs_spearman), n_valid = 81,786
- **Mechanism:** `definitional`
- **Provenance:** explicit

intervention_browse/mesh_term is the MeSH-vocabulary normalisation of the free-text intervention name.

### `smiless`

- **Association:** effect = 0.371 (abs_spearman), n_valid = 81,786
- **Mechanism:** `definitional`
- **Provenance:** explicit

SMILES strings are looked up from the drug name; NaN for non-small-molecule interventions.

### `enrollment`

- **Association:** effect = 0.212 (abs_spearman), n_valid = 44,446
- **Mechanism:** `design_choice`
- **Provenance:** default_cross_tier

Sponsor design decision made at registration (intervention/intervention_name) that constrains a downstream design field (enrollment).

### `mortality_YN`

- **Association:** effect = 0.102 (abs_spearman), n_valid = 17,916
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Sponsor design decision (intervention/intervention_name) that influences the realised safety outcome (mortality_YN) through biology, population, or operations.

### `mortality_rate`

- **Association:** effect = 0.097 (abs_spearman), n_valid = 17,916
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Sponsor design decision (intervention/intervention_name) that influences the realised safety outcome (mortality_rate) through biology, population, or operations.

### `execution_pass`

- **Association:** effect = 0.091 (abs_spearman), n_valid = 52,772
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Sponsor design decision (intervention/intervention_name) that influences the trial-success label (execution_pass) through the trial's biological and regulatory pathway.

### `execution_fail`

- **Association:** effect = 0.091 (abs_spearman), n_valid = 52,772
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Sponsor design decision (intervention/intervention_name) that influences the trial-success label (execution_fail) through the trial's biological and regulatory pathway.

### `sae_YN`

- **Association:** effect = 0.086 (abs_spearman), n_valid = 17,916
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Sponsor design decision (intervention/intervention_name) that influences the realised safety outcome (sae_YN) through biology, population, or operations.

### `dropout_YN`

- **Association:** effect = 0.062 (abs_spearman), n_valid = 38,302
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Sponsor design decision (intervention/intervention_name) that influences the realised safety outcome (dropout_YN) through biology, population, or operations.

### `approval_outcome`

- **Association:** effect = 0.059 (abs_spearman), n_valid = 30,683
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Sponsor design decision (intervention/intervention_name) that influences the trial-success label (approval_outcome) through the trial's biological and regulatory pathway.

### `sae_rate`

- **Association:** effect = 0.056 (abs_spearman), n_valid = 17,916
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Sponsor design decision (intervention/intervention_name) that influences the realised safety outcome (sae_rate) through biology, population, or operations.

### `completion_date`

- **Association:** effect = 0.054 (abs_spearman), n_valid = 42,855
- **Mechanism:** `design_choice`
- **Provenance:** default_cross_tier

Sponsor design decision (intervention/intervention_name) that drives the realised trial-duration timeline (completion_date).

---

## Associated but no direct causal edge (29)

### `Drug intervention Number`

- **Association:** effect = 0.668 (abs_spearman), n_valid = 81,786
- **Provenance:** demoted_confounded

`Drug intervention Number` is a deterministic descendant of its single definitional design parent; `intervention/intervention_name` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `number_of_arms`

- **Association:** effect = 0.440 (abs_spearman), n_valid = 78,123
- **Provenance:** demoted_confounded

`number_of_arms` is a deterministic descendant of its single definitional design parent; `intervention/intervention_name` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `MaskingType-Participant`

- **Association:** effect = 0.279 (abs_spearman), n_valid = 81,170
- **Provenance:** demoted_confounded

`MaskingType-Participant` is a deterministic descendant of its single definitional design parent; `intervention/intervention_name` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `MaskingType-Investigator`

- **Association:** effect = 0.271 (abs_spearman), n_valid = 81,170
- **Provenance:** demoted_confounded

`MaskingType-Investigator` is a deterministic descendant of its single definitional design parent; `intervention/intervention_name` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `study_design_info/masking_num`

- **Association:** effect = 0.265 (abs_spearman), n_valid = 81,170
- **Provenance:** demoted_confounded

`study_design_info/masking_num` is a deterministic descendant of its single definitional design parent; `intervention/intervention_name` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `Active Comparator Arm Number`

- **Association:** effect = 0.220 (abs_spearman), n_valid = 69,293
- **Provenance:** demoted_confounded

`Active Comparator Arm Number` is a deterministic descendant of its single definitional design parent; `intervention/intervention_name` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `Placebo Comparator Arm Number`

- **Association:** effect = 0.213 (abs_spearman), n_valid = 78,123
- **Provenance:** demoted_confounded

`Placebo Comparator Arm Number` is a deterministic descendant of its single definitional design parent; `intervention/intervention_name` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `Experimental Arm Number`

- **Association:** effect = 0.200 (abs_spearman), n_valid = 78,123
- **Provenance:** demoted_confounded

`Experimental Arm Number` is a deterministic descendant of its single definitional design parent; `intervention/intervention_name` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `study_design_info/intervention_model`

- **Association:** effect = 0.199 (eta), n_valid = 80,897
- **Provenance:** explicit

Both jointly chosen sponsor design decisions; no direct arrow.

### `Other intervention Number`

- **Association:** effect = 0.181 (abs_spearman), n_valid = 71,221
- **Provenance:** demoted_confounded

`Other intervention Number` is a deterministic descendant of its single definitional design parent; `intervention/intervention_name` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `MaskingType-Care Provider`

- **Association:** effect = 0.171 (abs_spearman), n_valid = 81,170
- **Provenance:** demoted_confounded

`MaskingType-Care Provider` is a deterministic descendant of its single definitional design parent; `intervention/intervention_name` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `MaskingType-Outcomes Assessor`

- **Association:** effect = 0.165 (abs_spearman), n_valid = 81,170
- **Provenance:** demoted_confounded

`MaskingType-Outcomes Assessor` is a deterministic descendant of its single definitional design parent; `intervention/intervention_name` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `Procedure intervention Number`

- **Association:** effect = 0.163 (abs_spearman), n_valid = 71,221
- **Provenance:** demoted_confounded

`Procedure intervention Number` is a deterministic descendant of its single definitional design parent; `intervention/intervention_name` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `No Intervention Arm Number`

- **Association:** effect = 0.148 (abs_spearman), n_valid = 69,293
- **Provenance:** demoted_confounded

`No Intervention Arm Number` is a deterministic descendant of its single definitional design parent; `intervention/intervention_name` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `Radiation intervention Number`

- **Association:** effect = 0.136 (abs_spearman), n_valid = 81,786
- **Provenance:** demoted_confounded

`Radiation intervention Number` is a deterministic descendant of its single definitional design parent; `intervention/intervention_name` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `study_design_info/masking`

- **Association:** effect = 0.136 (eta), n_valid = 75,043
- **Provenance:** explicit

Both jointly chosen sponsor design decisions; no direct arrow.

### `patient_data/sharing_ipd`

- **Association:** effect = 0.115 (eta), n_valid = 13,510
- **Provenance:** demoted_confounded

`intervention/intervention_name` has no direct mechanism that sets the oversight / policy field `patient_data/sharing_ipd`; the association is confounded through sponsor class and trial type. (R8: confounded ->design_oversight.)

### `location/facility/address/city`

- **Association:** effect = 0.109 (abs_spearman), n_valid = 81,786
- **Provenance:** demoted_confounded

`intervention/intervention_name` has no concrete causal mechanism that sets `location/facility/address/city`. Trial size, eligible population, calendar start date, site geography and the free-text title are not directly caused by `intervention/intervention_name`; the association is a jointly-chosen-design / sponsor-footprint / secular-trend confound. (R9: spurious design->planning/eligibility.)

### `study_design_info/allocation`

- **Association:** effect = 0.096 (eta), n_valid = 62,081
- **Provenance:** explicit

Both jointly chosen sponsor design decisions; no direct arrow.

### `brief_title`

- **Association:** effect = 0.094 (abs_spearman), n_valid = 81,786
- **Provenance:** demoted_confounded

`intervention/intervention_name` has no concrete causal mechanism that sets `brief_title`. Trial size, eligible population, calendar start date, site geography and the free-text title are not directly caused by `intervention/intervention_name`; the association is a jointly-chosen-design / sponsor-footprint / secular-trend confound. (R9: spurious design->planning/eligibility.)

### `phase`

- **Association:** effect = 0.081 (eta), n_valid = 81,786
- **Provenance:** explicit

Both reflect drug-development status (latent): intervention_name encodes which compound, and phase encodes how far it has progressed. No direct causal arrow at the column level — they are siblings under the unobserved 'drug pipeline status'.

### `icdcode`

- **Association:** effect = 0.078 (abs_spearman), n_valid = 81,786
- **Provenance:** demoted_confounded

`icdcode` is a deterministic descendant of its single definitional design parent; `intervention/intervention_name` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `Biological intervention Number`

- **Association:** effect = 0.074 (abs_spearman), n_valid = 81,786
- **Provenance:** demoted_confounded

`Biological intervention Number` is a deterministic descendant of its single definitional design parent; `intervention/intervention_name` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `oversight_info/is_fda_regulated_drug`

- **Association:** effect = 0.073 (eta), n_valid = 13,761
- **Provenance:** demoted_confounded

`intervention/intervention_name` has no direct mechanism that sets the oversight / policy field `oversight_info/is_fda_regulated_drug`; the association is confounded through sponsor class and trial type. (R8: confounded ->design_oversight.)

### `oversight_info/has_dmc`

- **Association:** effect = 0.067 (eta), n_valid = 45,926
- **Provenance:** demoted_confounded

`intervention/intervention_name` has no direct mechanism that sets the oversight / policy field `oversight_info/has_dmc`; the association is confounded through sponsor class and trial type. (R8: confounded ->design_oversight.)

### `responsible_party/responsible_party_type`

- **Association:** effect = 0.062 (eta), n_valid = 67,878
- **Provenance:** demoted_confounded

`intervention/intervention_name` has no direct mechanism that sets the oversight / policy field `responsible_party/responsible_party_type`; the association is confounded through sponsor class and trial type. (R8: confounded ->design_oversight.)

### `start_date`

- **Association:** effect = 0.062 (abs_spearman), n_valid = 42,855
- **Provenance:** demoted_confounded

`intervention/intervention_name` has no concrete causal mechanism that sets `start_date`. Trial size, eligible population, calendar start date, site geography and the free-text title are not directly caused by `intervention/intervention_name`; the association is a jointly-chosen-design / sponsor-footprint / secular-trend confound. (R9: spurious design->planning/eligibility.)

### `sponsors/lead_sponsor/agency_class`

- **Association:** effect = 0.062 (eta), n_valid = 71,221
- **Provenance:** explicit

Sponsor and specific drug correlate through portfolio (industry runs branded drugs, etc.) but neither directly causes the other.

### `Behavioral intervention Number`

- **Association:** effect = 0.050 (abs_spearman), n_valid = 81,786
- **Provenance:** demoted_confounded

`Behavioral intervention Number` is a deterministic descendant of its single definitional design parent; `intervention/intervention_name` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)
