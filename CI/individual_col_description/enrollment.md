# enrollment

- **Group:** `design_planning`
- **Dtype:** float
- **Description:** Planned (or actual-reported) participant enrollment count.
- **Associated partners (from `association.md`):** 38
  - Direct **causes** (parents of this feature): **3**
  - Direct **effects** (children of this feature): **8**
  - Associated but **no direct** causal edge: **27**

This per-feature file enumerates only **associated** partners. All other columns in `DAG.json` were ruled independent in the Stage-1 association screen and do not appear here. See `association.md` for the screen.

---

## Direct causes (3)

### `intervention/intervention_name`

- **Association:** effect = 0.212 (abs_spearman), n_valid = 44,446
- **Mechanism:** `design_choice`
- **Provenance:** default_cross_tier

Sponsor design decision made at registration (intervention/intervention_name) that constrains a downstream design field (enrollment).

### `phase`

- **Association:** effect = 0.111 (eta), n_valid = 44,446
- **Mechanism:** `design_choice`
- **Provenance:** explicit

Phase 1 sizes trials at tens; Phase 2 ~100; Phase 3 hundreds-to-thousands; Phase 4 large pragmatic cohorts. Phase is the dominant design driver of N.

### `study_design_info/intervention_model`

- **Association:** effect = 0.080 (eta), n_valid = 44,158
- **Mechanism:** `design_choice`
- **Provenance:** default_cross_tier

Sponsor design decision made at registration (study_design_info/intervention_model) that constrains a downstream design field (enrollment).

---

## Direct effects (8)

### `execution_pass`

- **Association:** effect = 0.308 (abs_spearman), n_valid = 38,306
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Downstream-design field (enrollment) feeds the trial-success label (execution_pass) through biology, execution, or regulatory pathways.

### `execution_fail`

- **Association:** effect = 0.308 (abs_spearman), n_valid = 38,306
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Downstream-design field (enrollment) feeds the trial-success label (execution_fail) through biology, execution, or regulatory pathways.

### `approval_outcome`

- **Association:** effect = 0.288 (abs_spearman), n_valid = 20,273
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Downstream-design field (enrollment) feeds the trial-success label (approval_outcome) through biology, execution, or regulatory pathways.

### `failure_reason`

- **Association:** effect = 0.134 (eta), n_valid = 6,304
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Downstream-design field (enrollment) feeds the trial-success label (failure_reason) through biology, execution, or regulatory pathways.

### `completion_date`

- **Association:** effect = 0.113 (abs_spearman), n_valid = 16,162
- **Mechanism:** `operational`
- **Provenance:** explicit

Larger planned enrollment requires a longer recruitment window plus follow-up, pushing completion_date later.

### `duration_day`

- **Association:** effect = 0.111 (abs_spearman), n_valid = 16,162
- **Mechanism:** `operational`
- **Provenance:** explicit

Larger N requires more recruitment time and (typically) longer follow-up; enrollment is a direct driver of trial duration.

### `duration_year`

- **Association:** effect = 0.111 (abs_spearman), n_valid = 16,162
- **Mechanism:** `operational`
- **Provenance:** default_cross_tier

Downstream-design field (enrollment) shifts the operational timeline of the trial (duration_year).

### `duration_month`

- **Association:** effect = 0.110 (abs_spearman), n_valid = 16,162
- **Mechanism:** `operational`
- **Provenance:** default_cross_tier

Downstream-design field (enrollment) shifts the operational timeline of the trial (duration_month).

---

## Associated but no direct causal edge (27)

### `location/facility/address/city`

- **Association:** effect = 0.456 (abs_spearman), n_valid = 44,446
- **Provenance:** default_within_tier

Both in group 'design_planning' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `dropout_YN`

- **Association:** effect = 0.364 (abs_spearman), n_valid = 38,301
- **Provenance:** demoted_confounded

A rate is invariant to sample size in expectation; `enrollment -> dropout_YN` is a threshold-crossing artifact, not a causal effect of N on the safety rate. (R3: rate invariance. Genuine enrollment effects are kept for trial timing and the 'poor enrollment' execution-failure pathway.)

### `sae_YN`

- **Association:** effect = 0.355 (abs_spearman), n_valid = 17,881
- **Provenance:** demoted_confounded

A rate is invariant to sample size in expectation; `enrollment -> sae_YN` is a threshold-crossing artifact, not a causal effect of N on the safety rate. (R3: rate invariance. Genuine enrollment effects are kept for trial timing and the 'poor enrollment' execution-failure pathway.)

### `number_of_arms`

- **Association:** effect = 0.350 (abs_spearman), n_valid = 43,117
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_planning' and 'design_derived'); jointly determined by upstream design_top choices, no direct arrow.

### `study_design_info/masking_num`

- **Association:** effect = 0.303 (abs_spearman), n_valid = 44,289
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_planning' and 'design_derived'); jointly determined by upstream design_top choices, no direct arrow.

### `MaskingType-Investigator`

- **Association:** effect = 0.287 (abs_spearman), n_valid = 44,289
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `MaskingType-Participant`

- **Association:** effect = 0.279 (abs_spearman), n_valid = 44,289
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `mortality_YN`

- **Association:** effect = 0.249 (abs_spearman), n_valid = 17,881
- **Provenance:** demoted_confounded

A rate is invariant to sample size in expectation; `enrollment -> mortality_YN` is a threshold-crossing artifact, not a causal effect of N on the safety rate. (R3: rate invariance. Genuine enrollment effects are kept for trial timing and the 'poor enrollment' execution-failure pathway.)

### `Active Comparator Arm Number`

- **Association:** effect = 0.222 (abs_spearman), n_valid = 43,117
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `Placebo Comparator Arm Number`

- **Association:** effect = 0.202 (abs_spearman), n_valid = 43,117
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `MaskingType-Outcomes Assessor`

- **Association:** effect = 0.196 (abs_spearman), n_valid = 44,289
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `MaskingType-Care Provider`

- **Association:** effect = 0.187 (abs_spearman), n_valid = 44,289
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `ipd_info_type-Clinical Study Report (CSR)`

- **Association:** effect = 0.159 (abs_spearman), n_valid = 2,145
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_planning' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `ipd_info_type-Statistical Analysis Plan (SAP)`

- **Association:** effect = 0.154 (abs_spearman), n_valid = 2,145
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_planning' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `mortality_rate`

- **Association:** effect = 0.152 (abs_spearman), n_valid = 17,881
- **Provenance:** demoted_confounded

A rate is invariant to sample size in expectation; `enrollment -> mortality_rate` is a threshold-crossing artifact, not a causal effect of N on the safety rate. (R3: rate invariance. Genuine enrollment effects are kept for trial timing and the 'poor enrollment' execution-failure pathway.)

### `start_date`

- **Association:** effect = 0.151 (abs_spearman), n_valid = 16,162
- **Provenance:** default_within_tier

Both in group 'design_planning' (tier 1); within-group pairs are siblings under common design parents or jointly-set sponsor decisions and have no direct causal arrow at this DAG resolution.

### `Drug intervention Number`

- **Association:** effect = 0.145 (abs_spearman), n_valid = 44,446
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `dropout_rate`

- **Association:** effect = 0.143 (abs_spearman), n_valid = 38,301
- **Provenance:** demoted_confounded

A rate is invariant to sample size in expectation; `enrollment -> dropout_rate` is a threshold-crossing artifact, not a causal effect of N on the safety rate. (R3: rate invariance. Genuine enrollment effects are kept for trial timing and the 'poor enrollment' execution-failure pathway.)

### `ipd_info_type-Informed Consent Form (ICF)`

- **Association:** effect = 0.127 (abs_spearman), n_valid = 2,145
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_planning' and 'design_oversight'); jointly determined by upstream design_top choices, no direct arrow.

### `sae_rate`

- **Association:** effect = 0.123 (abs_spearman), n_valid = 17,881
- **Provenance:** demoted_confounded

A rate is invariant to sample size in expectation; `enrollment -> sae_rate` is a threshold-crossing artifact, not a causal effect of N on the safety rate. (R3: rate invariance. Genuine enrollment effects are kept for trial timing and the 'poor enrollment' execution-failure pathway.)

### `Experimental Arm Number`

- **Association:** effect = 0.111 (abs_spearman), n_valid = 43,117
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `study_design_info/primary_purpose`

- **Association:** effect = 0.107 (eta), n_valid = 43,857
- **Provenance:** demoted_confounded

`study_design_info/primary_purpose` has no concrete causal mechanism that sets `enrollment`. Trial size, eligible population, calendar start date, site geography and the free-text title are not directly caused by `study_design_info/primary_purpose`; the association is a jointly-chosen-design / sponsor-footprint / secular-trend confound. (R9: spurious design->planning/eligibility.)

### `Biological intervention Number`

- **Association:** effect = 0.072 (abs_spearman), n_valid = 44,446
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `Procedure intervention Number`

- **Association:** effect = 0.067 (abs_spearman), n_valid = 44,446
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `study_design_info/masking`

- **Association:** effect = 0.059 (eta), n_valid = 38,225
- **Provenance:** demoted_confounded

`study_design_info/masking` has no concrete causal mechanism that sets `enrollment`. Trial size, eligible population, calendar start date, site geography and the free-text title are not directly caused by `study_design_info/masking`; the association is a jointly-chosen-design / sponsor-footprint / secular-trend confound. (R9: spurious design->planning/eligibility.)

### `Radiation intervention Number`

- **Association:** effect = 0.057 (abs_spearman), n_valid = 44,446
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_derived' and 'design_planning'); jointly determined by upstream design_top choices, no direct arrow.

### `intervention_browse/mesh_term`

- **Association:** effect = 0.052 (abs_spearman), n_valid = 44,446
- **Provenance:** default_within_tier

Both in tier 1 (downstream-design sub-groups 'design_planning' and 'design_derived'); jointly determined by upstream design_top choices, no direct arrow.
