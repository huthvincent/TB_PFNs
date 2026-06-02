# Diagnostic Test intervention Number

- **Group:** `design_derived`
- **Dtype:** float
- **Description:** Count of interventions tagged 'Diagnostic Test'.
- **Associated partners (from `association.md`):** 1
  - Direct **causes** (parents of this feature): **0**
  - Direct **effects** (children of this feature): **0**
  - Associated but **no direct** causal edge: **1**

This per-feature file enumerates only **associated** partners. All other columns in `DAG.json` were ruled independent in the Stage-1 association screen and do not appear here. See `association.md` for the screen.

---

## Direct causes (0)

_(none)_

---

## Direct effects (0)

_(none)_

---

## Associated but no direct causal edge (1)

### `study_design_info/primary_purpose`

- **Association:** effect = 0.083 (eta), n_valid = 70,604
- **Provenance:** demoted_confounded

`Diagnostic Test intervention Number` is a deterministic descendant of its single definitional design parent; `study_design_info/primary_purpose` reaches it only through that parent (mediated, not direct). (R7: mediated ->design_derived.)
