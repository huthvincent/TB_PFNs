# phase

- **Group:** `design_top`
- **Dtype:** categorical
- **Description:** Clinical trial phase: Phase 1 / 2 / 3 / 4. Set at registration; reflects the drug-development maturity (first-in-human safety -> mid-stage efficacy -> pivotal -> post-market).
- **Associated partners (from `association.md`):** 59
  - Direct **causes** (parents of this feature): **0**
  - Direct **effects** (children of this feature): **31**
  - Associated but **no direct** causal edge: **28**

This per-feature file enumerates only **associated** partners. All other columns in `DAG.json` were ruled independent in the Stage-1 association screen and do not appear here. See `association.md` for the screen.

---

## Direct causes (0)

_(none)_

---

## Direct effects (31)

### `eligibility/healthy_volunteers`

- **Association:** effect = 0.411 (cramers_v), n_valid = 81,613
- **Mechanism:** `design_choice`
- **Provenance:** default_cross_tier

Sponsor design decision made at registration (phase) that constrains a downstream design field (eligibility/healthy_volunteers).

### `sae_YN`

- **Association:** effect = 0.365 (eta), n_valid = 17,916
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Sponsor design decision (phase) that influences the realised safety outcome (sae_YN) through biology, population, or operations.

### `execution_fail`

- **Association:** effect = 0.261 (eta), n_valid = 52,772
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Sponsor design decision (phase) that influences the trial-success label (execution_fail) through the trial's biological and regulatory pathway.

### `execution_pass`

- **Association:** effect = 0.261 (eta), n_valid = 52,772
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Sponsor design decision (phase) that influences the trial-success label (execution_pass) through the trial's biological and regulatory pathway.

### `dropout_YN`

- **Association:** effect = 0.252 (eta), n_valid = 38,302
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Sponsor design decision (phase) that influences the realised safety outcome (dropout_YN) through biology, population, or operations.

### `study_design_info/allocation`

- **Association:** effect = 0.250 (cramers_v), n_valid = 62,081
- **Mechanism:** `design_choice`
- **Provenance:** explicit

Phase 1 trials are usually non-randomised single-group; Phase 3 trials are typically randomised. Phase drives the allocation decision.

### `study_design_info/intervention_model`

- **Association:** effect = 0.245 (cramers_v), n_valid = 80,897
- **Mechanism:** `design_choice`
- **Provenance:** explicit

Phase 1 first-in-human trials are predominantly Single Group Assignment (no comparator yet); Phase 3 pivotal trials are Parallel Assignment for randomised comparison. Phase shapes the model choice.

### `mortality_YN`

- **Association:** effect = 0.238 (eta), n_valid = 17,916
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Sponsor design decision (phase) that influences the realised safety outcome (mortality_YN) through biology, population, or operations.

### `duration_month`

- **Association:** effect = 0.224 (eta), n_valid = 42,855
- **Mechanism:** `design_choice`
- **Provenance:** default_cross_tier

Sponsor design decision (phase) that drives the realised trial-duration timeline (duration_month).

### `duration_day`

- **Association:** effect = 0.223 (eta), n_valid = 42,855
- **Mechanism:** `design_choice`
- **Provenance:** default_cross_tier

Sponsor design decision (phase) that drives the realised trial-duration timeline (duration_day).

### `duration_year`

- **Association:** effect = 0.223 (eta), n_valid = 42,855
- **Mechanism:** `design_choice`
- **Provenance:** default_cross_tier

Sponsor design decision (phase) that drives the realised trial-duration timeline (duration_year).

### `sae_rate`

- **Association:** effect = 0.223 (eta), n_valid = 17,916
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Sponsor design decision (phase) that influences the realised safety outcome (sae_rate) through biology, population, or operations.

### `responsible_party/responsible_party_type`

- **Association:** effect = 0.209 (cramers_v), n_valid = 67,878
- **Mechanism:** `design_choice`
- **Provenance:** default_cross_tier

Sponsor design decision made at registration (phase) that constrains a downstream design field (responsible_party/responsible_party_type).

### `ipd_info_type-Informed Consent Form (ICF)`

- **Association:** effect = 0.209 (eta), n_valid = 2,145
- **Mechanism:** `design_choice`
- **Provenance:** default_cross_tier

Sponsor design decision made at registration (phase) that constrains a downstream design field (ipd_info_type-Informed Consent Form (ICF)).

### `mortality_rate`

- **Association:** effect = 0.204 (eta), n_valid = 17,916
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Sponsor design decision (phase) that influences the realised safety outcome (mortality_rate) through biology, population, or operations.

### `study_design_info/primary_purpose`

- **Association:** effect = 0.194 (cramers_v), n_valid = 80,983
- **Mechanism:** `design_choice`
- **Provenance:** explicit

Phase 1 skews Treatment / Basic Science; Phase 4 picks up Supportive Care / Health Services Research. Phase shifts the typical purpose distribution.

### `patient_data/sharing_ipd`

- **Association:** effect = 0.182 (cramers_v), n_valid = 13,510
- **Mechanism:** `design_choice`
- **Provenance:** default_cross_tier

Sponsor design decision made at registration (phase) that constrains a downstream design field (patient_data/sharing_ipd).

### `oversight_info/has_dmc`

- **Association:** effect = 0.164 (cramers_v), n_valid = 45,926
- **Mechanism:** `design_choice`
- **Provenance:** default_cross_tier

Sponsor design decision made at registration (phase) that constrains a downstream design field (oversight_info/has_dmc).

### `study_design_info/masking`

- **Association:** effect = 0.161 (cramers_v), n_valid = 75,043
- **Mechanism:** `design_choice`
- **Provenance:** explicit

Phase 1 trials are commonly Open Label; Phase 3 confirmatory trials are commonly Double / Quadruple blinded. Phase drives the masking choice.

### `approval_outcome`

- **Association:** effect = 0.156 (eta), n_valid = 30,683
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Sponsor design decision (phase) that influences the trial-success label (approval_outcome) through the trial's biological and regulatory pathway.

### `ipd_info_type-Statistical Analysis Plan (SAP)`

- **Association:** effect = 0.149 (eta), n_valid = 2,297
- **Mechanism:** `design_choice`
- **Provenance:** default_cross_tier

Sponsor design decision made at registration (phase) that constrains a downstream design field (ipd_info_type-Statistical Analysis Plan (SAP)).

### `oversight_info/is_fda_regulated_drug`

- **Association:** effect = 0.144 (cramers_v), n_valid = 13,761
- **Mechanism:** `design_choice`
- **Provenance:** default_cross_tier

Sponsor design decision made at registration (phase) that constrains a downstream design field (oversight_info/is_fda_regulated_drug).

### `dropout_rate`

- **Association:** effect = 0.131 (eta), n_valid = 38,302
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Sponsor design decision (phase) that influences the realised safety outcome (dropout_rate) through biology, population, or operations.

### `failure_reason`

- **Association:** effect = 0.127 (cramers_v), n_valid = 20,769
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Sponsor design decision (phase) that influences the trial-success label (failure_reason) through the trial's biological and regulatory pathway.

### `ipd_info_type-Clinical Study Report (CSR)`

- **Association:** effect = 0.123 (eta), n_valid = 2,145
- **Mechanism:** `design_choice`
- **Provenance:** default_cross_tier

Sponsor design decision made at registration (phase) that constrains a downstream design field (ipd_info_type-Clinical Study Report (CSR)).

### `ipd_info_type-Analytic Code`

- **Association:** effect = 0.114 (eta), n_valid = 2,297
- **Mechanism:** `design_choice`
- **Provenance:** default_cross_tier

Sponsor design decision made at registration (phase) that constrains a downstream design field (ipd_info_type-Analytic Code).

### `enrollment`

- **Association:** effect = 0.111 (eta), n_valid = 44,446
- **Mechanism:** `design_choice`
- **Provenance:** explicit

Phase 1 sizes trials at tens; Phase 2 ~100; Phase 3 hundreds-to-thousands; Phase 4 large pragmatic cohorts. Phase is the dominant design driver of N.

### `biology_fail`

- **Association:** effect = 0.098 (eta), n_valid = 34,427
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Sponsor design decision (phase) that influences the trial-success label (biology_fail) through the trial's biological and regulatory pathway.

### `biology_pass`

- **Association:** effect = 0.098 (eta), n_valid = 34,427
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Sponsor design decision (phase) that influences the trial-success label (biology_pass) through the trial's biological and regulatory pathway.

### `completion_date`

- **Association:** effect = 0.081 (eta), n_valid = 42,855
- **Mechanism:** `design_choice`
- **Provenance:** default_cross_tier

Sponsor design decision (phase) that drives the realised trial-duration timeline (completion_date).

### `oversight_info/is_fda_regulated_device`

- **Association:** effect = 0.054 (cramers_v), n_valid = 13,676
- **Mechanism:** `design_choice`
- **Provenance:** default_cross_tier

Sponsor design decision made at registration (phase) that constrains a downstream design field (oversight_info/is_fda_regulated_device).

---

## Associated but no direct causal edge (28)

### `Experimental Arm Number`

- **Association:** effect = 0.279 (eta), n_valid = 78,123
- **Provenance:** demoted_confounded

`Experimental Arm Number` is a deterministic descendant of its single definitional design parent; `phase` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `location/facility/address/city`

- **Association:** effect = 0.274 (eta), n_valid = 81,786
- **Provenance:** demoted_confounded

`phase` has no concrete causal mechanism that sets `location/facility/address/city`. Trial size, eligible population, calendar start date, site geography and the free-text title are not directly caused by `phase`; the association is a jointly-chosen-design / sponsor-footprint / secular-trend confound. (R9: spurious design->planning/eligibility.)

### `Active Comparator Arm Number`

- **Association:** effect = 0.227 (eta), n_valid = 69,293
- **Provenance:** demoted_confounded

`Active Comparator Arm Number` is a deterministic descendant of its single definitional design parent; `phase` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `sponsors/lead_sponsor/agency_class`

- **Association:** effect = 0.207 (cramers_v), n_valid = 71,221
- **Provenance:** explicit

Both jointly chosen at trial registration; correlated via drug-development economics but no direct arrow.

### `study_design_info/masking_num`

- **Association:** effect = 0.205 (eta), n_valid = 81,170
- **Provenance:** demoted_confounded

`study_design_info/masking_num` is a deterministic descendant of its single definitional design parent; `phase` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `MaskingType-Investigator`

- **Association:** effect = 0.185 (eta), n_valid = 81,170
- **Provenance:** demoted_confounded

`MaskingType-Investigator` is a deterministic descendant of its single definitional design parent; `phase` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `MaskingType-Participant`

- **Association:** effect = 0.173 (eta), n_valid = 81,170
- **Provenance:** demoted_confounded

`MaskingType-Participant` is a deterministic descendant of its single definitional design parent; `phase` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `MaskingType-Outcomes Assessor`

- **Association:** effect = 0.159 (eta), n_valid = 81,170
- **Provenance:** demoted_confounded

`MaskingType-Outcomes Assessor` is a deterministic descendant of its single definitional design parent; `phase` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `start_date`

- **Association:** effect = 0.156 (eta), n_valid = 42,855
- **Provenance:** demoted_confounded

`phase` has no concrete causal mechanism that sets `start_date`. Trial size, eligible population, calendar start date, site geography and the free-text title are not directly caused by `phase`; the association is a jointly-chosen-design / sponsor-footprint / secular-trend confound. (R9: spurious design->planning/eligibility.)

### `MaskingType-Care Provider`

- **Association:** effect = 0.151 (eta), n_valid = 81,170
- **Provenance:** demoted_confounded

`MaskingType-Care Provider` is a deterministic descendant of its single definitional design parent; `phase` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `condition_browse/mesh_term`

- **Association:** effect = 0.149 (eta), n_valid = 81,786
- **Provenance:** demoted_confounded

`condition_browse/mesh_term` is a deterministic descendant of its single definitional design parent; `phase` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `number_of_arms`

- **Association:** effect = 0.148 (eta), n_valid = 78,123
- **Provenance:** demoted_confounded

`number_of_arms` is a deterministic descendant of its single definitional design parent; `phase` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `brief_title`

- **Association:** effect = 0.139 (eta), n_valid = 81,786
- **Provenance:** demoted_confounded

`phase` has no concrete causal mechanism that sets `brief_title`. Trial size, eligible population, calendar start date, site geography and the free-text title are not directly caused by `phase`; the association is a jointly-chosen-design / sponsor-footprint / secular-trend confound. (R9: spurious design->planning/eligibility.)

### `eligibility/gender`

- **Association:** effect = 0.128 (cramers_v), n_valid = 71,221
- **Provenance:** demoted_confounded

`phase` has no concrete causal mechanism that sets `eligibility/gender`. Trial size, eligible population, calendar start date, site geography and the free-text title are not directly caused by `phase`; the association is a jointly-chosen-design / sponsor-footprint / secular-trend confound. (R9: spurious design->planning/eligibility.)

### `eligibility/maximum_age`

- **Association:** effect = 0.124 (eta), n_valid = 42,760
- **Provenance:** demoted_confounded

`phase` has no concrete causal mechanism that sets `eligibility/maximum_age`. Trial size, eligible population, calendar start date, site geography and the free-text title are not directly caused by `phase`; the association is a jointly-chosen-design / sponsor-footprint / secular-trend confound. (R9: spurious design->planning/eligibility.)

### `intervention_browse/mesh_term`

- **Association:** effect = 0.123 (eta), n_valid = 81,786
- **Provenance:** demoted_confounded

`intervention_browse/mesh_term` is a deterministic descendant of its single definitional design parent; `phase` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `Placebo Comparator Arm Number`

- **Association:** effect = 0.094 (eta), n_valid = 78,123
- **Provenance:** demoted_confounded

`Placebo Comparator Arm Number` is a deterministic descendant of its single definitional design parent; `phase` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `No Intervention Arm Number`

- **Association:** effect = 0.090 (eta), n_valid = 69,293
- **Provenance:** demoted_confounded

`No Intervention Arm Number` is a deterministic descendant of its single definitional design parent; `phase` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `intervention/intervention_name`

- **Association:** effect = 0.081 (eta), n_valid = 81,786
- **Provenance:** explicit

Both reflect drug-development status (latent): intervention_name encodes which compound, and phase encodes how far it has progressed. No direct causal arrow at the column level — they are siblings under the unobserved 'drug pipeline status'.

### `Radiation intervention Number`

- **Association:** effect = 0.080 (eta), n_valid = 81,786
- **Provenance:** demoted_confounded

`Radiation intervention Number` is a deterministic descendant of its single definitional design parent; `phase` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `Device intervention Number`

- **Association:** effect = 0.078 (eta), n_valid = 71,221
- **Provenance:** demoted_confounded

`Device intervention Number` is a deterministic descendant of its single definitional design parent; `phase` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `Biological intervention Number`

- **Association:** effect = 0.076 (eta), n_valid = 81,786
- **Provenance:** demoted_confounded

`Biological intervention Number` is a deterministic descendant of its single definitional design parent; `phase` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `smiless`

- **Association:** effect = 0.069 (eta), n_valid = 81,786
- **Provenance:** demoted_confounded

`smiless` is a deterministic descendant of its single definitional design parent; `phase` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `Other Arm Number`

- **Association:** effect = 0.061 (eta), n_valid = 78,123
- **Provenance:** demoted_confounded

`Other Arm Number` is a deterministic descendant of its single definitional design parent; `phase` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `Drug intervention Number`

- **Association:** effect = 0.058 (eta), n_valid = 81,786
- **Provenance:** demoted_confounded

`Drug intervention Number` is a deterministic descendant of its single definitional design parent; `phase` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `Procedure intervention Number`

- **Association:** effect = 0.054 (eta), n_valid = 71,221
- **Provenance:** demoted_confounded

`Procedure intervention Number` is a deterministic descendant of its single definitional design parent; `phase` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `icdcode`

- **Association:** effect = 0.054 (eta), n_valid = 81,786
- **Provenance:** demoted_confounded

`icdcode` is a deterministic descendant of its single definitional design parent; `phase` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)

### `condition`

- **Association:** effect = 0.051 (eta), n_valid = 81,786
- **Provenance:** explicit

Both jointly chosen at registration; a specific disease can be at any phase depending on the drug being tested.
