# biology_pass

- **Group:** `outcome_label`
- **Dtype:** boolean
- **Description:** True if the intervention met its primary biological efficacy endpoint.
- **Associated partners (from `association.md`):** 16
  - Direct **causes** (parents of this feature): **8**
  - Direct **effects** (children of this feature): **2**
  - Associated but **no direct** causal edge: **6**

This per-feature file enumerates only **associated** partners. All other columns in `DAG.json` were ruled independent in the Stage-1 association screen and do not appear here. See `association.md` for the screen.

---

## Direct causes (8)

### `failure_reason`

- **Association:** effect = 1.000 (eta), n_valid = 20,769
- **Mechanism:** `definitional`
- **Provenance:** explicit

TrialBench encodes biology_pass = False iff failure_reason in {'efficacy', 'safety'}; the categorical failure_reason directly populates the boolean.

### `dropout_rate`

- **Association:** effect = 0.105 (abs_spearman), n_valid = 13,897
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Realised safety outcome (dropout_rate) feeds the trial-success label (biology_pass) directly (e.g., 'safety' failure category, regulatory rejection).

### `phase`

- **Association:** effect = 0.098 (eta), n_valid = 34,427
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Sponsor design decision (phase) that influences the trial-success label (biology_pass) through the trial's biological and regulatory pathway.

### `sae_rate`

- **Association:** effect = 0.084 (abs_spearman), n_valid = 5,792
- **Mechanism:** `biological`
- **Provenance:** explicit

An unacceptable SAE rate forces biology_pass=False via the 'safety' failure category.

### `sae_YN`

- **Association:** effect = 0.083 (abs_spearman), n_valid = 5,792
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Realised safety outcome (sae_YN) feeds the trial-success label (biology_pass) directly (e.g., 'safety' failure category, regulatory rejection).

### `mortality_rate`

- **Association:** effect = 0.081 (abs_spearman), n_valid = 5,792
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Realised safety outcome (mortality_rate) feeds the trial-success label (biology_pass) directly (e.g., 'safety' failure category, regulatory rejection).

### `completion_date`

- **Association:** effect = 0.076 (abs_spearman), n_valid = 10,917
- **Mechanism:** `operational`
- **Provenance:** default_cross_tier

Trial timing (completion_date) propagates into the post-hoc trial-success label (biology_pass).

### `mortality_YN`

- **Association:** effect = 0.074 (abs_spearman), n_valid = 5,792
- **Mechanism:** `biological`
- **Provenance:** default_cross_tier

Realised safety outcome (mortality_YN) feeds the trial-success label (biology_pass) directly (e.g., 'safety' failure category, regulatory rejection).

---

## Direct effects (2)

### `biology_fail`

- **Association:** effect = 1.000 (abs_spearman), n_valid = 34,427
- **Mechanism:** `deterministic`
- **Provenance:** explicit

biology_fail = NOT biology_pass (definitional negation).

### `approval_outcome`

- **Association:** effect = 0.295 (abs_spearman), n_valid = 27,420
- **Mechanism:** `regulatory`
- **Provenance:** explicit

Meeting the primary biological efficacy endpoint is a precondition for regulatory approval; biology_pass is the gating biology factor in approval_outcome.

---

## Associated but no direct causal edge (6)

### `execution_pass`

- **Association:** effect = 0.125 (abs_spearman), n_valid = 28,367
- **Provenance:** explicit

biology_pass and execution_pass are independent preconditions for approval — biology is about whether the drug works, execution is about whether the trial was run properly. They are both downstream of failure_reason but do not directly cause each other.

### `execution_fail`

- **Association:** effect = 0.125 (abs_spearman), n_valid = 28,367
- **Provenance:** explicit

Mediated through `execution_pass` (and the common parent `failure_reason`).

### `sponsors/lead_sponsor/agency_class`

- **Association:** effect = 0.082 (eta), n_valid = 23,862
- **Provenance:** demoted_confounded

`sponsors/lead_sponsor/agency_class` reaches the trial-success label `biology_pass` only through biology / efficacy and enrollment mediators already in the DAG (`biology_pass`, `failure_reason`, `enrollment`); no direct arrow. (R6: mediated design->label.)

### `oversight_info/is_fda_regulated_drug`

- **Association:** effect = 0.065 (eta), n_valid = 5,975
- **Provenance:** demoted_confounded

`oversight_info/is_fda_regulated_drug` is an oversight / regulatory flag that proxies for trial type and scale; its association with `biology_pass` is confounded through `intervention/intervention_type`, `phase`, and trial scale. The genuine oversight mechanisms (FDA-regulation -> approval_outcome; DMC early-stopping -> sae_rate / mortality_rate) are retained as explicit edges. (R10: confounded design_oversight->outcome.)

### `oversight_info/has_dmc`

- **Association:** effect = 0.063 (eta), n_valid = 23,795
- **Provenance:** demoted_confounded

`oversight_info/has_dmc` is an oversight / regulatory flag that proxies for trial type and scale; its association with `biology_pass` is confounded through `intervention/intervention_type`, `phase`, and trial scale. The genuine oversight mechanisms (FDA-regulation -> approval_outcome; DMC early-stopping -> sae_rate / mortality_rate) are retained as explicit edges. (R10: confounded design_oversight->outcome.)

### `start_date`

- **Association:** effect = 0.059 (abs_spearman), n_valid = 10,917
- **Provenance:** demoted_confounded

`start_date` is an administrative / policy / calendar / site-geography attribute with no direct biological or operational pathway to `biology_pass`; the association is confounded by sponsor class, trial era, or indication mix. (R2: no-mechanism source.)
