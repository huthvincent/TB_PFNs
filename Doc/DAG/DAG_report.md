# Causal-Inference DAG for TrialBench_joined — Pipeline Report


**Goal.** : Create general purpose Causal Inference DAG for clinical trial domain 

---

## Stage 1 — Data-driven association screen

The screen prunes the edge candidate set: under faithfulness, two features that are **not associated in data cannot be causally linked**, so we filter pairs by marginal effect size before applying any domain knowledge.

| Quantity | Value |
|---|---|
| **DAG nodes** | **71** |
| **Feature pairs tested** | **2,485** (= 71 × 70 / 2) |
| **Pairs marked associated** | **1,169 (47.0 %)** |
| Pairs ruled independent | 1,316 (53.0 %) |

**Tests by type pair.** num × num → \|Spearman ρ\|; cat × cat → Cramér's V; num × cat → η (= √η²). All rescaled to [0, 1]. p-values BH-FDR-adjusted across all 2,485 tests.

**Association threshold.** `effect_size > 0.05` AND `FDR-adjusted p < 0.01`. With n ≈ 80k, an effect-size threshold is essential — p-values alone admit clinically trivial signals.

---

## Stage 2 — Causal-direction assignment (Claude + clinical-trial knowledge, no data peeking)

For each of the 1,169 associated pairs, the pair was classified into one of three categories using only general clinical-trial domain knowledge, **after** a per-pair confounding-demotion review (Stage 2b below):

| Category | Count | Share |
|---|---|---|
| **Directed causal edge `A → B`** | **217** | 18.6 % |
| **Associated but no direct causal edge** | **952** | 81.4 % |
| Total | 1,169 | 100 % |

The resulting DAG is **acyclic** (verified by topological sort over the 71 nodes).

**Edge provenance.** 60 edges come from hand-authored domain rules (definitional / deterministic / regulatory constraints such as sum-of-arms, MeSH lookups, FDA regulation pathways); the remaining 157 edges are tier-ordering defaults that **survived** the Stage-2b confounding review (genuine design→outcome mechanisms — e.g., `phase → sae_rate`, `condition → mortality_rate`, `duration_day → dropout_rate`).

**Edge mechanism distribution (217 surviving edges).**

| Mechanism | Edges |
|---|---|
| biological | 87 |
| design_choice | 49 |
| operational | 45 |
| deterministic | 22 |
| definitional | 8 |
| design_constraint | 3 |
| regulatory | 3 |

---

## Stage 2b — Confounding-demotion review

The tier default rule only assigns a *direction*; it implicitly assumes every cross-tier associated pair is causal. That over-claims. A second pass applied **10 documented, conservative rules (R1–R10)** that demote a default edge `src → tgt` to *associated but no direct* when `src` has no plausible **direct** causal mechanism to `tgt` (the association is mediated through a definitional parent, or confounded by sponsor class / trial era / indication mix).

**556 of the 713 default edges (78 %) were demoted.** Breakdown by rule:

| Rule | Demoted | What it catches |
|---|---|---|
| R1 | 147 | Re-encoding / tally source (mesh_term, icdcode, smiless, MaskingType-\*, per-type & arm counts) — mediated through its definitional parent |
| R7 | 144 | `… → design_derived`: a deterministic descendant is reached only through its single definitional parent |
| R2 | 88 | No-mechanism source (IPD-policy, responsible_party, has_expanded_access, brief_title, city, start_date) → outcome — confounded |
| R9 | 38 | `design_top → {enrollment, eligibility/*, start_date, city, brief_title}` with no concrete mechanism (whitelist keeps e.g. `phase→enrollment`, `phase→eligibility/healthy_volunteers`) |
| R4 | 33 | Methodology / sponsor design → safety — confounded through *what is studied* |
| R8 | 27 | `… → design_oversight` with no policy-setting mechanism |
| R10 | 26 | `design_oversight → outcome` (is_fda_regulated_\*, has_dmc) — oversight flag is a proxy for trial type/scale; confounded |
| R6 | 24 | Methodology / eligibility → trial-success label — mediated through biology / enrollment |
| R5 | 23 | Methodology / eligibility → trial timing — mediated through enrollment / intervention model |
| R3 | 6  | `enrollment → safety rate/YN` — rate is invariant to N (threshold artifact) |

R9 and R10 are *selective*: R9 demotes design→planning/eligibility edges with no concrete mechanism (e.g. `intervention/intervention_type → location/.../city`, `phase → start_date`, `phase → eligibility/gender`) while a whitelist preserves the clinically-sensible ones (trial size driven by phase/disease/sponsor/intervention; healthy-volunteer eligibility by phase/purpose/condition). R10 demotes the `oversight_info/is_fda_regulated_* / has_dmc → outcome` confounded cluster but the two genuine oversight mechanisms — FDA-regulation → `approval_outcome` and DMC early-stopping → `sae_rate`/`mortality_rate` — are kept as hand-authored explicit edges. Every demoted pair stays in `DAG.json` under `associated_no_direct` with its rule-tagged reason, so the decision is fully auditable.

---

## Concrete examples

### A → B (causal, directed edge)

| Pair | Mechanism | Why |
|---|---|---|
| `start_date → completion_date` | operational | A trial cannot finish before it has started; start temporally precedes completion. |
| `phase → enrollment` | design_choice | Phase 1 trials enroll tens of participants; Phase 3 pivotal trials enroll hundreds to thousands. Phase is the dominant design-time driver of N. |
| `intervention/intervention_type → sae_rate` | biological | Drug / Biological interventions carry pharmacology-driven adverse events; Behavioral or Dietary Supplement interventions do not. The modality directly drives the realised SAE rate. |
| `failure_reason → biology_pass` | definitional | TrialBench encodes `biology_pass = False` iff `failure_reason ∈ {'efficacy', 'safety'}` — the categorical label deterministically populates the boolean. |
| `MaskingType-Participant → study_design_info/masking_num` | deterministic | `masking_num` equals the sum of the four `MaskingType-*` indicators; this is a hard arithmetic constraint. |
| `biology_pass → approval_outcome` | regulatory | Meeting the primary biological efficacy endpoint is a precondition for regulatory approval. |

### Associated but **no direct causal edge** (statistical signal without a direct arrow)

| Pair | Why associated yet not causally linked |
|---|---|
| `MaskingType-Investigator ↔ MaskingType-Participant` (effect = 0.878) | Both are derived from the same parent `study_design_info/masking`. They share a common cause; no direct arrow between siblings. |
| `duration_month ↔ duration_year` (effect = 1.0) | Both are deterministic unit conversions of `duration_day`. Perfect correlation, common-parent structure. |
| `phase ↔ sponsors/lead_sponsor/agency_class` (effect = 0.207) | Jointly chosen at trial registration. Correlated through drug-pipeline economics (industry runs more Phase 3 pivotals), but neither column directly causes the other. |
| `mortality_YN ↔ sae_YN` (effect = 0.480) | Mediated through their respective rates and through the inclusion `mortality ⊂ SAE`. The direct edges live one layer down (rate → YN, mortality_rate → sae_rate). |
| `location/facility/address/city ↔ sae_YN` (effect = 0.477) | **Demoted in Stage 2b (R2).** A trial's city has no biological pathway to serious adverse events; the strong association is confounded — specific indications and oncology centres cluster in specific cities, and *those* drive SAE. |
| `enrollment ↔ sae_YN` (effect = 0.355) | **Demoted in Stage 2b (R3).** A rate is invariant to sample size in expectation; the `enrollment → sae_YN` association is a threshold-crossing artifact, not a causal effect of N on the safety rate. |

### Independent at Stage 1 (filtered out — no association in data, hence no causal claim)

| Pair | Stage-1 statistics |
|---|---|
| `Diagnostic Test intervention Number ↔ duration_day` | effect = 0.000, p-adj = 0.99 — Diagnostic Test trials' duration is statistically indistinguishable from other trials' duration. |
| `Sham Comparator Arm Number ↔ enrollment` | effect = 0.002, p-adj = 0.67 — having a sham comparator arm is uncorrelated with planned trial size. |
| `Genetic intervention Number ↔ mortality_rate` | effect = 0.015, p-adj = 0.06 — too few genetic-intervention trials carry mortality signal to claim association. |
| `brief_title ↔ mortality_rate` | effect = 0.039, p-adj < 1e-6 — p-value strongly significant on 18 k rows, but the effect is below the 0.05 threshold (the n-large effect-size guardrail). Title length is not informative about mortality. |

---

## Final DAG at a glance

- **Nodes:** 71 trial features.
- **Directed edges:** 217 (acyclic) — down from 773 before the Stage-2b confounding review (R1–R10).
- **Non-directional associations:** 952 (kept in `DAG.json` under `associated_no_direct` with a documented, rule-tagged reason; 556 of these are Stage-2b demotions).
- **Top fan-out (causes of many things):** `phase` (31), `sponsors/lead_sponsor/agency_class` (15), `intervention/intervention_name` (12), `duration_day` (11), `condition` (11).
- **Top fan-in (caused by many things):** `execution_pass` (17), `execution_fail` (17), `approval_outcome` (14), `failure_reason` (13), `mortality_YN` (11), `sae_rate` (11).

The fan-out / fan-in profile matches the intuitive picture: sponsor design choices are upstream causes; clinical safety and trial-success labels are downstream effects. After the confounding review the DAG is deliberately **sparse and conservative** — only edges with a defensible direct mechanism survive; everything merely correlated is recorded as `associated_no_direct`.

---

## Outputs & file layout

```
/data2/zhu11/TB/
├── DAG_report.md          ← this file (pipeline overview)
├── DAG_node.md            ← catalogue of all 71 nodes + descriptions, grouped by tier
├── uncertainty_edge.md    ← 20 least-confident edges (NOTE: written against the
│                            post-R9 245-edge DAG; one revision behind the current
│                            217-edge R10 DAG — regenerate on request)
├── CI/
│   ├── DAG.json                      ← the DAG: 71 nodes, 217 directed edges,
│   │                                   952 associated_no_direct (rule-tagged)
│   ├── association.md                ← Stage-1 association screen report
│   ├── text_2_col.md                 ← design for 7 eligibility-criteria columns
│   │                                   to be parsed from `eligibility/criteria/
│   │                                   textblock` (NOT yet added to the DAG)
│   ├── individual_col_description/    ← 71 per-node .md files (one per feature,
│   │                                   causes / effects / no-direct partners)
│   └── md_backup_20260511_212933/    ← pre-pipeline manual draft (archived)
└── script/
    ├── ci_pairwise_association.py    ← Stage 1: pairwise association screen
    ├── ci_render_association_md.py   ← renders association.md
    ├── ci_build_dag.py              ← Stage 2 + 2b: direction + R1–R10 demotion
    └── ci_render_feature_mds.py     ← renders individual_col_description/*.md
```

**Reproduce the DAG:** run, in order,
`ci_pairwise_association.py` → `ci_render_association_md.py` → `ci_build_dag.py` → `ci_render_feature_mds.py`.
All Stage-2 / Stage-2b domain knowledge (node metadata, explicit edges, R1–R10
demotion rules, R9 whitelist) lives in `ci_build_dag.py` and is fully auditable;
every edge and every demoted pair carries a `provenance` tag and a rule-tagged
reason in `DAG.json`.
