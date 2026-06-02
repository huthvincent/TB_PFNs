# text_2_col — structured columns derived from `eligibility/criteria/textblock`

`eligibility/criteria/textblock` is currently **excluded** from the DAG (free text). Plan: parse the criteria text into the columns below, each capturing one aspect of **recruitment accessibility** (how narrow the eligible/willing pool is). These are distinct from the already-structured `eligibility/{minimum_age,maximum_age,gender,healthy_volunteers}` — do **not** re-extract age/sex here.

**Orientation convention:** every column is oriented so that **higher = harder to recruit = lower accessibility**, so signs in the DAG stay consistent.

## The 7 columns (+ 1 optional composite)

| Column | What it expresses | dtype / range | Why it is a distinct, causally-relevant dimension |
|---|---|---|---|
| `elig_n_inclusion` | Number of inclusion criteria | int (≥0) | Most basic funnel-narrowing signal |
| `elig_n_exclusion` | Number of exclusion criteria | int (≥0) | Exclusion count predicts low accrual more strongly than inclusion count in the literature — **keep separate from inclusion** |
| `elig_comorbidity_exclusion` | Degree to which comorbid / concurrent diseases are excluded ("no diabetes / no cardiac history / no prior cancer") | ordinal 0–3 | Real-world patients usually have comorbidities; this removes the most pool, and is *not* the same as raw criteria count (few but severe comorbidity bars ≠ many trivial criteria) |
| `elig_prior_treatment_restriction` | Prior/concomitant-therapy limits + washout / treatment-naive-only | ordinal 0–3 | Most patients are already treated; both shrinks the pool and adds washout logistics — drives `enrollment` *and* `dropout_rate` |
| `elig_lab_biomarker_strictness` | Narrowness of lab thresholds + whether a biomarker / genetic test is required | ordinal 0–3 | Narrow physiologic window + marker screening shrinks the eligible fraction and adds screening burden (precision-medicine trials) |
| `elig_performance_status_req` | Whether a minimum functional/performance status is required (ECOG / Karnofsky / NYHA) and how strict | ordinal 0–2 | Excludes the sicker majority; a "who-qualifies" axis independent of the above |
| `elig_logistical_burden` | Participant-side commitment (frequent visits, biopsies/invasive procedures, caregiver requirement, contraception/adherence) | ordinal 0–3 | "Who is **willing/able to comply**" rather than "who qualifies" — orthogonal; mainly drives willingness & `dropout_rate` |
| *(optional)* `elig_restrictiveness_score` | Normalised composite of the above, overall accessibility | float [0,1] | Single headline node; **collinear** with the 7 — use the composite *or* the components, not both, in any model |

> `elig_criteria_textlen` (raw length / readability proxy) is a cheap baseline only — keep it as a sanity check, **not** a DAG node.

**Extraction note:** score the ordinal dimensions with an LLM against a fixed 0–3 rubric (explicit anchors per level) rather than regex — inclusion/exclusion section headers in the criteria text are too irregular for reliable rule-based counting; the rubric makes it reproducible.

---

## How to add these as 7 nodes to the current DAG

The current DAG is **71 nodes / 217 edges** built by the two-stage pipeline (`ci_pairwise_association.py` → `ci_build_dag.py` → `ci_render_feature_mds.py`). Adding the 7 columns is **not** a hand-edit of `DAG.json`; re-run the pipeline so they pass the same association screen and the same R1–R10 review. Concrete steps:

### 1. Produce the data
Extract the 7 (+composite) columns into a parquet keyed by the same trial id, aligned row-for-row with `TrialBench_joined`. (One-off script in `script/`, output to `results/<run_id>/`.) The columns are all numeric/ordinal, so they need no special preprocessing in the screen.

### 2. Stage 1 — let them earn their edges (don't assume)
Add the 7 columns to the retained set in `ci_pairwise_association.py` (and drop `eligibility/criteria/textblock` from the exclusion list once parsed). Re-run the screen → the new columns get tested against all 71 existing nodes. **Only pairs that pass `effect>0.05 & FDR<0.01` become edge candidates.** This is the guardrail: a dimension with no real signal will simply not get edges.

### 3. Stage 2 — node metadata + group + tier
In `ci_build_dag.py` `NODE_METADATA`, add 7 entries with:
- `group: "design_eligibility"` (they are eligibility-criteria attributes)
- `tier 1` (inherited from `design_eligibility` in `GROUP_TIER`) — so by default they sit downstream of `design_top` and upstream of all outcomes.

### 4. Stage 2 — wire the genuine mechanisms (avoid R9 false-demotion)
By the tier rule they'd point at outcomes; but R5/R6 demote `eligibility → timing/label` as mediated, and R9 governs `→ design_planning/eligibility`. To keep the **genuine** edges, add explicit edges / whitelist entries:

- **Parents → these columns** (they are *caused by* upstream design): add `condition → elig_*`, `phase → elig_*`, `intervention/intervention_type → elig_*` as `EXPLICIT_DIRECT_EDGES` where a real mechanism exists (sponsors write stricter criteria for certain diseases / phases / modalities). Mechanism: `design_choice`.
- **These columns → `enrollment`**: the headline mechanism. Add each `elig_*` to the **R9 whitelist for `enrollment`** so `elig_* → enrollment` is *not* demoted (stricter criteria ⇒ smaller eligible pool ⇒ harder to enrol). Consider making these `EXPLICIT_DIRECT_EDGES` (mechanism `design_choice`) with a written rationale.
- **These columns → `dropout_rate` / `duration_day` / `failure_reason`**: add as `EXPLICIT_DIRECT_EDGES` for the dimensions with a real mechanism — esp. `elig_prior_treatment_restriction` and `elig_logistical_burden → dropout_rate`; any `elig_* → failure_reason` (the `'poor enrollment'` pathway) and `→ duration_day` (longer recruitment). Otherwise R5/R6 will (correctly, by default) demote them as mediated.
- Leave everything else to default + R1–R10 — e.g. `elig_* → sae_rate` will be screened/demoted like other eligibility→safety edges unless you assert a mechanism.

### 5. Re-run + verify
`ci_pairwise_association.py` → `ci_render_association_md.py` → `ci_build_dag.py` → `ci_render_feature_mds.py`. Check: DAG still acyclic; `n_nodes` = 78; the new `elig_*` nodes have sensible fan-out into `enrollment`/`dropout_rate`/`duration_day`/`failure_reason` and fan-in from `condition`/`phase`/`intervention_type`; `eligibility/criteria/textblock` no longer in the excluded list. Then regenerate `DAG_node.md` and `DAG_report.md`.

**Key principle:** add them as data + metadata + a few explicit mechanism edges, then let the existing association screen and R1–R10 review decide the rest — same discipline as every other node, so the new columns are not privileged.
