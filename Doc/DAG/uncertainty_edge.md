# 20 Least-Confident Edges — post-R9 DAG (245 edges)

Re-audited against the **245-edge** DAG (after the full Stage-2b R1–R9 confounding-demotion pass). The previous flagged set (`intervention/intervention_type → city`, `phase → start_date`, `phase → brief_title`, `intervention_model → eligibility/healthy_volunteers`, …) was demoted by R9, so this is a fresh ranking of the *residual* weak edges among the 245 survivors. Ordered **most uncertain → less uncertain**.

## Where the remaining uncertainty now lives

R1–R9 cleaned: proxy/admin → outcomes, design→design_derived, methodology→safety, design→oversight, spurious design→planning/eligibility. **One structural gap remains uncovered:**

> **`design_oversight → outcome` is the new worst class.** R4 demoted *methodology* design → safety as confounded; R8 demoted *design → oversight*. But nobody demoted **oversight → outcome**. `oversight_info/is_fda_regulated_drug` is essentially a proxy for *"this is a drug/biologic trial"*, and `oversight_info/has_dmc` is a proxy for *"this is a large pivotal/high-risk trial"* — their edges into safety / efficacy / timing / labels are confounded through `intervention/intervention_type`, `phase`, and trial scale, exactly the pattern R4 was built to catch. ~17 such edges survived only because their source group is `design_oversight`.

The rest of the residual is the usual tail: R9-whitelist survivors that are mediated, and explicit edges with genuinely non-identifiable direction.

---

## The 20 edges

### 1. `oversight_info/has_dmc → biology_pass`  (eff=0.063, biological, default_cross_tier)  &  `→ biology_fail` (0.063)
A Data Monitoring Committee **cannot make a drug biologically effective**. This is pure confounding — DMCs are attached to large, late-stage pivotal trials, which are exactly the trials that already passed earlier biological filters. The mechanism label `biological` is nonsensical for a governance body. Clearest-wrong surviving edge.

### 2. `oversight_info/is_fda_regulated_drug → execution_fail`  (eff=0.151, biological)  &  `→ execution_pass` (0.151)
`is_fda_regulated_drug` is a near-proxy for `intervention/intervention_type ∈ {Drug, Biological}`. Execution success is driven by intervention modality, enrollment and trial scale — not by the regulatory flag itself. Confounded through `intervention/intervention_type`; same class R4 demotes, uncaught because the source is `design_oversight`.

### 3. `oversight_info/has_dmc → mortality_YN`  (eff=0.216, biological)
High effect, but sign-ambiguous and confounded: DMCs are preferentially assigned to high-risk / high-mortality trials, so this association most likely reflects *trial-type selection*, not a causal DMC effect. The truncation story (DMC stops a trial early) would push the *opposite* sign. `biological` label is wrong for a committee.

### 4. `oversight_info/has_dmc → sae_YN`  (eff=0.176, biological)
Same DMC-assignment confound and sign ambiguity as #3 for serious adverse events.

### 5. `oversight_info/is_fda_regulated_drug → failure_reason`  (eff=0.118, biological)
Confounded through `intervention/intervention_type` (drug trials fail for different reasons than device/behavioral). The regulation flag does not itself cause a failure category.

### 6. `oversight_info/has_dmc → approval_outcome`  (eff=0.116, biological)
Confounded: DMC presence co-occurs with large pivotal trials that are on an approval track. The committee does not causally produce approval; trial scale / phase does.

### 7. `oversight_info/is_fda_regulated_drug → sae_YN`  (eff=0.099)  &  `→ mortality_YN` (0.095)  &  `→ sae_rate` (0.097)
Drug/biologic trials have a different safety footprint than device/behavioral trials — but the cause is the *modality* (`intervention/intervention_type`), already in the DAG, not the FDA-jurisdiction flag. Confounded, near-threshold.

### 8. `oversight_info/is_fda_regulated_drug → duration_day / duration_month / duration_year`  (eff=0.090)
The regulatory flag does not set trial length; `phase` and `intervention/intervention_type` do. Mediated/confounded; `operational` label is a stretch.

### 9. `oversight_info/is_fda_regulated_device → sae_YN`  (eff=0.060, biological)
A near-proxy for "device trial". Device-trial safety differs, but the cause is `intervention/intervention_type`, not the regulation flag. Confounded and barely over threshold.

### 10. `oversight_info/has_dmc → dropout_rate / completion_date / failure_reason`  (eff≈0.06–0.10)
Same DMC-as-pivotal-trial-proxy confound; these are weak default edges with generic templates and no clean DMC mechanism.

### 11. `study_design_info/primary_purpose → eligibility/healthy_volunteers`  (eff=0.455, design_choice, R9-whitelisted)
Kept by the R9 whitelist (prevention/vaccine trials genuinely recruit healthy volunteers), **but** most of this very strong association is mediated through `phase` (Phase-1 first-in-human). The direct-arrow share is uncertain; arguably should be `no_direct` (mediated through phase).

### 12. `intervention/intervention_name → enrollment`  (eff=0.212, design_choice, R9-whitelisted)
Whitelisted (specific drug ↔ available patient pool), but (a) `intervention/intervention_name` is only represented by its **token count** in the screen — a coarse proxy — and (b) the real driver is `condition` (disease prevalence). Likely mediated.

### 13. `sae_rate → dropout_rate`  (eff=0.342, biological, explicit)
Direction is **non-identifiable**: disease severity is a common cause of both, and informative censoring (sicker patients drop out before an SAE is logged) can reverse the apparent sign.

### 14. `oversight_info/has_dmc → sae_rate`  (eff=0.174, operational, explicit)  &  `→ mortality_rate` (0.150, explicit)
Hand-authored as "DMC early-stopping truncates rates". Defensible, but DMCs are assigned to high-risk trials, so the raw association may carry the opposite sign; the net direction is genuinely uncertain.

### 15. `phase → eligibility/gender`  (eff=0.128, design_choice, R9-whitelisted)
Phase does not set sex eligibility — the disease (`condition`) does. Whitelisted defensively (Phase-1 cohorts), but the direct mechanism is weak; likely mediated through `condition`.

### 16. `phase → eligibility/maximum_age`  (eff=0.124, design_choice, R9-whitelisted)
Same as #15 — age bounds are set by the disease; phase's direct contribution (Phase-1 healthy-volunteer age caps) is small. Borderline keep.

### 17. `sae_YN → failure_reason`  (eff=0.240, biological, explicit)
Plausible (a safety signal triggers a `'safety'` failure), but `failure_reason` is a **post-hoc human label**. `sae_YN` may be a common-effect of the underlying safety mechanism rather than its cause; the arrow could be spurious.

### 18. `study_design_info/primary_purpose → intervention/intervention_type`  (eff=0.053, design_constraint, explicit)
Forced direction (purpose constrains type). Sponsors often choose the intervention first; the reverse is equally defensible and the effect is barely over threshold. Non-identifiable.

### 19. `condition → study_design_info/primary_purpose`  (eff=0.082, design_choice, explicit)
Defensible (disease shapes Treatment/Prevention/Diagnostic) but weak, and arguably jointly chosen by the sponsor rather than strictly caused.

### 20. `intervention/intervention_name → sae_rate (0.056) / approval_outcome (0.059) / dropout_YN (0.062)`  (biological, default_cross_tier)
Conceptually genuine (the specific compound drives toxicity/efficacy) **but** rests on the coarse `n_items` proxy (the name itself is not encoded), near threshold, and redundant with stronger parents (`intervention/intervention_type`, `biology_pass`) already in the DAG.

---

## Suggested remediation

- **Add a rule R10** — demote `design_oversight → outcome` (safety / timing / label / efficacy) **except** the two genuine mechanisms already hand-authored: `oversight_info/is_fda_regulated_{drug,device} → approval_outcome` (regulatory gate) and the explicit `oversight_info/has_dmc → {sae_rate, mortality_rate, execution_pass}` (operational early-stopping). This one principled pass removes #1–#10 (~25 edges) — the entire `is_fda_regulated_* / has_dmc → outcome` confounded cluster.
- **Tighten R9 whitelist** — drop `phase` from `eligibility/gender` and `eligibility/maximum_age` (disease, not phase, sets these); reconsider whether `primary_purpose → eligibility/healthy_volunteers` should be `no_direct` (mediated through phase). Handles #11, #15, #16.
- **Flag as non-identifiable (keep, annotate low-confidence)** — #13, #14, #17, #18, #19.
- **Demote redundant-proxy** — #20 (`intervention/intervention_name` n_items proxy; genuine pathway already via `intervention/intervention_type`).

I can apply R10 + the R9-whitelist tightening as another pass on `ci_build_dag.py` and re-render if you want the DAG tighter still.
