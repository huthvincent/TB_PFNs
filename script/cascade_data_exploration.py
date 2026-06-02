"""Data exploration for the 3-layer cascade (Execution → Biology → Regulatory).

Per phase, reports:
  - NCT counts per subtask and pairwise/full intersections
  - Availability of completion_date / start_date for time-based split
  - Class balance of derived layer labels (execution_pass, biology_pass,
    regulatory_pass) on the maximal joinable subset
  - Sample-size implications for each layer's training set

Writes a markdown report to:
  /data2/zhu11/TB/results/cascade_data_exploration/exploration.md
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd

DATA_ROOT = Path("/data2/zhu11/TB/dataset/TrialBench")
OUT_DIR = Path("/data2/zhu11/TB/results/cascade_data_exploration")
PHASES = ["Phase1", "Phase2", "Phase3", "Phase4"]

# Subtasks we care about for the cascade.
SUBTASKS = {
    "patient-dropout-event-forecasting": {
        "y_filename": "y", "phases": PHASES,
        "labels": ["Y/N", "droupout_rate"],
        "expose_as": {"Y/N": "dropout_YN", "droupout_rate": "dropout_rate"},
    },
    "trial-duration-forecasting": {
        "y_filename": "y", "phases": PHASES,
        "labels": ["start_date", "completion_date", "time_day", "month", "year"],
        "expose_as": {
            "start_date": "start_date", "completion_date": "completion_date",
            "time_day": "duration_day", "month": "duration_month", "year": "duration_year",
        },
    },
    "serious-adverse-event-forecasting": {
        "y_filename": "y", "phases": PHASES,
        "labels": ["Y/N", "serious_adverse_rate"],
        "expose_as": {"Y/N": "sae_YN", "serious_adverse_rate": "sae_rate"},
    },
    "mortality-event-prediction": {
        "y_filename": "y", "phases": PHASES,
        "labels": ["Y/N", "mortality_rate"],
        "expose_as": {"Y/N": "mortality_YN", "mortality_rate": "mortality_rate"},
    },
    "trial-failure-reason-identification": {
        "y_filename": "y", "phases": PHASES,
        "labels": ["failure_reason"],
        "expose_as": {"failure_reason": "failure_reason"},
    },
    "trial-approval-forecasting": {
        "y_filename": "y", "phases": PHASES,
        "labels": ["outcome"],
        "expose_as": {"outcome": "approval_outcome"},
    },
}


def load_subtask_phase(subtask: str, phase: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Concat train + test for one subtask × phase. Returns (X, y), index = NCT."""
    cfg = SUBTASKS[subtask]
    y_suffix = cfg["y_filename"]
    xs, ys, splits = [], [], []
    for split in ["train", "test"]:
        x_path = DATA_ROOT / subtask / phase / f"{split}_x.csv"
        y_path = DATA_ROOT / subtask / phase / f"{split}_{y_suffix}.csv"
        x = pd.read_csv(x_path, index_col=0)
        y = pd.read_csv(y_path, index_col=0)
        y = y.loc[x.index]
        xs.append(x)
        ys.append(y)
        splits.extend([split] * len(x))
    X = pd.concat(xs, axis=0)
    y = pd.concat(ys, axis=0)
    X["__orig_split__"] = splits
    return X, y


def derive_layer_labels(joined: pd.DataFrame) -> pd.DataFrame:
    """Compute layer-PRIMARY labels per user spec.

      L1 primary fail = (dropout_YN==1) OR (failure_reason=='poor enrollment')
      L2 primary fail = (failure_reason == 'efficacy')
      L3 primary       = (approval_outcome == 1)

    Aux labels (sae_YN/sae_rate/mortality_YN/mortality_rate/failure_reason=='safety'
    /duration_day) get their OWN models (option B); not folded into the gate filter.
    """
    out = pd.DataFrame(index=joined.index)

    has_dropout = joined["dropout_YN"].notna() if "dropout_YN" in joined.columns \
        else pd.Series(False, index=joined.index)
    has_failreason = joined["failure_reason"].notna() if "failure_reason" in joined.columns \
        else pd.Series(False, index=joined.index)

    # ---- Layer 1 primary ----
    has_signal_L1 = has_dropout | has_failreason
    dropout_fail = (joined.get("dropout_YN", pd.Series(np.nan, index=joined.index)) == 1).astype("boolean")
    dropout_fail[~has_dropout] = pd.NA
    poor_enroll = (joined.get("failure_reason", pd.Series(np.nan, index=joined.index)) == "poor enrollment").astype("boolean")
    poor_enroll[~has_failreason] = pd.NA

    exec_fail = (dropout_fail.fillna(False) | poor_enroll.fillna(False)).astype("boolean")
    exec_fail[~has_signal_L1] = pd.NA
    out["execution_fail"] = exec_fail
    out["execution_pass"] = (~exec_fail).astype("boolean")

    # ---- Layer 2 primary: failure_reason == 'efficacy' ----
    fr = joined.get("failure_reason", pd.Series(np.nan, index=joined.index))
    bio_fail = (fr == "efficacy").astype("boolean")
    bio_fail[~has_failreason] = pd.NA
    out["biology_fail"] = bio_fail
    out["biology_pass"] = (~bio_fail).astype("boolean")

    # ---- Layer 3 primary ----
    if "approval_outcome" in joined.columns:
        ao = joined["approval_outcome"]
        out["regulatory_pass"] = (ao == 1).astype("boolean")
        out.loc[ao.isna(), "regulatory_pass"] = pd.NA
    else:
        out["regulatory_pass"] = pd.NA

    return out


def explore_phase(phase: str) -> dict:
    print(f"\n=== {phase} ===")
    nct_sets: dict[str, set] = {}
    label_frames: dict[str, pd.DataFrame] = {}
    feature_columns_per_subtask: dict[str, list[str]] = {}

    for subtask, cfg in SUBTASKS.items():
        X, y = load_subtask_phase(subtask, phase)
        nct_sets[subtask] = set(X.index)
        feature_columns_per_subtask[subtask] = sorted(c for c in X.columns
                                                     if c != "__orig_split__")
        renamed = y.rename(columns=cfg["expose_as"])
        renamed = renamed[list(cfg["expose_as"].values())]
        label_frames[subtask] = renamed
        print(f"  {subtask:50s} n_NCT={len(X):6d}  y_cols={list(renamed.columns)}")

    # Pairwise intersections
    subtasks = list(nct_sets.keys())
    pairwise = {}
    for i in range(len(subtasks)):
        for j in range(i + 1, len(subtasks)):
            a, b = subtasks[i], subtasks[j]
            pairwise[(a, b)] = len(nct_sets[a] & nct_sets[b])

    # Coverage of each subtask BY trial-duration (which holds completion_date).
    duration_set = nct_sets["trial-duration-forecasting"]
    duration_coverage = {
        st: {
            "n_in_subtask": len(nct_sets[st]),
            "n_also_in_duration": len(nct_sets[st] & duration_set),
            "fraction_covered": (
                len(nct_sets[st] & duration_set) / len(nct_sets[st])
                if nct_sets[st] else 0.0
            ),
        }
        for st in subtasks
    }
    print("  Coverage by trial-duration (for time-split feasibility):")
    for st, c in duration_coverage.items():
        print(f"    {st:50s} {c['n_also_in_duration']}/{c['n_in_subtask']} = {c['fraction_covered']:.2%}")

    # Full intersection (all 6)
    full_intersect = set.intersection(*nct_sets.values())
    print(f"  Full intersection (all 6 subtasks): {len(full_intersect)} trials")

    # 5-way (drop trial-failure-reason since it is failed-only by definition)
    five_way = set.intersection(*[s for k, s in nct_sets.items()
                                  if k != "trial-failure-reason-identification"])
    print(f"  5-way intersection (excl. failure_reason): {len(five_way)} trials")

    # Per-cascade-layer source pools (union, not intersection)
    L1_pool = nct_sets["patient-dropout-event-forecasting"] | nct_sets["trial-failure-reason-identification"]
    L2_pool = (
        nct_sets["serious-adverse-event-forecasting"]
        | nct_sets["mortality-event-prediction"]
        | nct_sets["trial-failure-reason-identification"]
    )
    L3_pool = nct_sets["trial-approval-forecasting"]
    print(f"  L1 label-pool (dropout ∪ failure_reason): {len(L1_pool)}")
    print(f"  L2 label-pool (sae ∪ mortality ∪ failure_reason): {len(L2_pool)}")
    print(f"  L3 label-pool (approval): {len(L3_pool)}")
    print(f"  L1 ∩ duration: {len(L1_pool & duration_set)}")
    print(f"  L2 ∩ duration: {len(L2_pool & duration_set)}")
    print(f"  L3 ∩ duration: {len(L3_pool & duration_set)}")

    # Build wide table on the union of all NCTs from the 5 always-available subtasks
    five_subtasks = [k for k in nct_sets if k != "trial-failure-reason-identification"]
    five_union = set.union(*[nct_sets[k] for k in five_subtasks])
    joined = pd.DataFrame(index=sorted(five_union))
    for subtask in subtasks:
        renamed = label_frames[subtask]
        joined = joined.join(renamed, how="left")
    print(f"  Wide table: {joined.shape}, cols: {list(joined.columns)}")

    # Coverage stats per label
    coverage = {c: int(joined[c].notna().sum()) for c in joined.columns}

    # Derive layer labels
    layer_labels = derive_layer_labels(joined)
    joined = joined.join(layer_labels)

    # ---- Per-layer training counts under user's spec ----
    layer_stats = {}

    # Layer 1: trainable = trials with L1 label observable; no upstream filter
    L1_mask = joined["execution_pass"].notna()
    L1_class_balance = joined.loc[L1_mask, "execution_pass"].value_counts(dropna=False).to_dict()
    layer_stats["L1_execution_primary"] = {
        "n_trainable": int(L1_mask.sum()),
        "class_balance": {str(k): int(v) for k, v in L1_class_balance.items()},
    }

    # Layer 2 primary: trainable = (L1==pass) AND (L2 label known)
    # L2 label = (failure_reason == 'efficacy'), so L2 known means failure_reason known.
    L2_mask = joined["execution_pass"].eq(True) & joined["biology_pass"].notna()
    L2_class_balance = joined.loc[L2_mask, "biology_pass"].value_counts(dropna=False).to_dict()
    layer_stats["L2_biology_primary"] = {
        "n_trainable": int(L2_mask.sum()),
        "class_balance": {str(k): int(v) for k, v in L2_class_balance.items()},
        "note": ("L2 primary label = (failure_reason == 'efficacy'). "
                 "Only failed trials have failure_reason → trainable subset is "
                 "FAILED trials whose failure was NOT execution-related."),
    }

    # Layer 3: trainable = (L1==pass) AND (L2==pass) AND (approval_outcome known)
    L3_mask = (
        joined["execution_pass"].eq(True)
        & joined["biology_pass"].eq(True)
        & joined["regulatory_pass"].notna()
    )
    L3_class_balance = joined.loc[L3_mask, "regulatory_pass"].value_counts(dropna=False).to_dict()
    layer_stats["L3_regulatory_primary_strict"] = {
        "n_trainable": int(L3_mask.sum()),
        "class_balance": {str(k): int(v) for k, v in L3_class_balance.items()},
        "note": ("Strict cascade: requires both L1 and L2 labels known AND "
                 "both passing. Since L2 known implies failure_reason known "
                 "(only for failed trials), this filter is effectively the "
                 "subset of FAILED-but-not-for-{execution,efficacy} trials. "
                 "It excludes ALL approved trials."),
    }

    # Layer 3 RELAXED: include trials where biology_fail can be reasonably set False
    # without requiring failure_reason. We do this by treating approval_outcome==1 as
    # implicit evidence of biology_pass=True (approved drugs presumably did not fail
    # for efficacy). Combined with L1==pass (or L1 unknown), this is more inclusive.
    bio_fail_relaxed = joined["biology_fail"].fillna(False)  # NaN → assume not failed
    bio_pass_relaxed = ~bio_fail_relaxed.astype(bool)
    exec_fail_relaxed = joined["execution_fail"].fillna(False)
    exec_pass_relaxed = ~exec_fail_relaxed.astype(bool)
    L3_relaxed_mask = (
        exec_pass_relaxed & bio_pass_relaxed & joined["regulatory_pass"].notna()
    )
    L3r_class_balance = joined.loc[L3_relaxed_mask, "regulatory_pass"].value_counts(dropna=False).to_dict()
    layer_stats["L3_regulatory_primary_relaxed"] = {
        "n_trainable": int(L3_relaxed_mask.sum()),
        "class_balance": {str(k): int(v) for k, v in L3r_class_balance.items()},
        "note": ("Relaxed cascade: trials with approval known AND not flagged "
                 "as execution_fail / efficacy_fail (NaN treated as not-failed). "
                 "Includes approved trials and unknown-status trials. Sample "
                 "size is realistic but the gate is weaker."),
    }

    # Aux models (each trained on its own pool)
    aux_pools = {}
    if "sae_YN" in joined.columns:
        aux_pools["aux_sae_YN"] = int(joined["sae_YN"].notna().sum())
        aux_pools["aux_sae_rate"] = int(joined["sae_rate"].notna().sum())
    if "mortality_YN" in joined.columns:
        aux_pools["aux_mortality_YN"] = int(joined["mortality_YN"].notna().sum())
        aux_pools["aux_mortality_rate"] = int(joined["mortality_rate"].notna().sum())
    if "failure_reason" in joined.columns:
        aux_pools["aux_safety_failure"] = int((joined["failure_reason"] == "safety").sum())
        aux_pools["aux_efficacy_failure_known"] = int(joined["failure_reason"].notna().sum())
    if "duration_day" in joined.columns:
        aux_pools["aux_duration_day"] = int(joined["duration_day"].notna().sum())
    layer_stats["aux_pool_sizes"] = aux_pools

    # completion_date availability — for time-split feasibility
    if "completion_date" in joined.columns:
        cd = pd.to_datetime(joined["completion_date"], errors="coerce")
        cd_stats = {
            "n_available": int(cd.notna().sum()),
            "min": str(cd.min()) if cd.notna().any() else None,
            "max": str(cd.max()) if cd.notna().any() else None,
            "median": str(cd.median()) if cd.notna().any() else None,
        }
    else:
        cd_stats = {"n_available": 0}

    # Check whether start_date is in feature CSVs (would help if completion_date sparse)
    start_date_in_x = {}
    for st, cols in feature_columns_per_subtask.items():
        start_date_in_x[st] = any("start_date" in c.lower() for c in cols)

    return {
        "phase": phase,
        "subtask_n_nct": {k: len(v) for k, v in nct_sets.items()},
        "feature_n_cols": {k: len(v) for k, v in feature_columns_per_subtask.items()},
        "pairwise_intersections": {f"{a} ∩ {b}": v for (a, b), v in pairwise.items()},
        "duration_coverage": duration_coverage,
        "full_intersection_size": len(full_intersect),
        "five_way_intersection_size": len(five_way),
        "L1_pool_size": len(L1_pool),
        "L2_pool_size": len(L2_pool),
        "L3_pool_size": len(L3_pool),
        "L1_pool_with_completion_date": len(L1_pool & duration_set),
        "L2_pool_with_completion_date": len(L2_pool & duration_set),
        "L3_pool_with_completion_date": len(L3_pool & duration_set),
        "joined_table_shape": list(joined.shape),
        "label_coverage": coverage,
        "layer_stats": layer_stats,
        "completion_date_stats": cd_stats,
        "start_date_in_X": start_date_in_x,
    }


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # Quick check: do any X CSVs contain a start_date column? (only need 1 phase)
    print("--- Inspecting X feature columns for start_date / completion_date ---")
    for st in SUBTASKS:
        x = pd.read_csv(DATA_ROOT / st / PHASES[0] / "train_x.csv", index_col=0,
                        nrows=5)
        sd_cols = [c for c in x.columns if "start_date" in c.lower()
                   or "completion_date" in c.lower()
                   or "primary_completion_date" in c.lower()]
        print(f"  {st:50s} date-related X cols: {sd_cols}")

    all_phase_stats = {}
    for phase in PHASES:
        all_phase_stats[phase] = explore_phase(phase)

    # Write JSON
    (OUT_DIR / "exploration.json").write_text(
        json.dumps(all_phase_stats, indent=2, default=str)
    )

    # Write Markdown
    lines = []
    lines.append("# Cascade Data Exploration Report\n")
    lines.append(f"Generated: {datetime.now().isoformat(timespec='seconds')}\n")
    lines.append(
        "Per-phase analysis of the 6 TrialBench subtasks for the planned "
        "Execution → Biology → Regulatory cascade. All counts use train ∪ test "
        "(we will re-split later by completion_date).\n"
    )

    for phase, stats in all_phase_stats.items():
        lines.append(f"## {phase}\n")
        lines.append("**NCT counts per subtask**\n")
        lines.append("| Subtask | n_NCT | n_X_cols | Coverage by trial-duration |")
        lines.append("|---|---:|---:|---:|")
        for k in SUBTASKS:
            cov = stats["duration_coverage"][k]
            cov_str = f"{cov['n_also_in_duration']}/{cov['n_in_subtask']} ({cov['fraction_covered']:.1%})"
            lines.append(
                f"| {k} | {stats['subtask_n_nct'][k]} | {stats['feature_n_cols'][k]} | {cov_str} |"
            )
        lines.append("")

        lines.append(
            f"**Per-cascade-layer label pools** (union of source subtasks):  \n"
            f"- L1 (dropout ∪ failure_reason): {stats['L1_pool_size']}, "
            f"with completion_date: {stats['L1_pool_with_completion_date']}  \n"
            f"- L2 (sae ∪ mortality ∪ failure_reason): {stats['L2_pool_size']}, "
            f"with completion_date: {stats['L2_pool_with_completion_date']}  \n"
            f"- L3 (approval): {stats['L3_pool_size']}, "
            f"with completion_date: {stats['L3_pool_with_completion_date']}  \n"
        )

        lines.append(
            f"**Full 6-way intersection**: {stats['full_intersection_size']} trials  \n"
            f"**5-way intersection** (excl. failure_reason, which only exists for failed trials): "
            f"{stats['five_way_intersection_size']} trials  \n"
            f"**Joined wide table**: {stats['joined_table_shape']}  \n"
        )

        lines.append("**Label coverage in joined table**\n")
        lines.append("| Label | n_non_null |")
        lines.append("|---|---:|")
        for k, v in stats["label_coverage"].items():
            lines.append(f"| `{k}` | {v} |")
        lines.append("")

        lines.append("**Per-layer trainable counts and class balance**\n")
        lines.append("| Layer | n_trainable | class balance | note |")
        lines.append("|---|---:|---|---|")
        for layer, s in stats["layer_stats"].items():
            if layer == "aux_pool_sizes":
                continue
            cb = ", ".join(f"{k}={v}" for k, v in s["class_balance"].items())
            note = s.get("note", "")
            lines.append(f"| {layer} | {s['n_trainable']} | {cb} | {note} |")
        lines.append("")
        if "aux_pool_sizes" in stats["layer_stats"]:
            lines.append("**Auxiliary-label pool sizes** (each gets its own model under option B)\n")
            lines.append("| Aux label | n |")
            lines.append("|---|---:|")
            for k, v in stats["layer_stats"]["aux_pool_sizes"].items():
                lines.append(f"| `{k}` | {v} |")
            lines.append("")

        lines.append("**completion_date stats (for time split)**\n")
        lines.append(f"```json\n{json.dumps(stats['completion_date_stats'], indent=2)}\n```\n")

        lines.append("**start_date in X (per subtask)**\n")
        lines.append("```json\n" + json.dumps(stats["start_date_in_X"], indent=2) + "\n```\n")

    (OUT_DIR / "exploration.md").write_text("\n".join(lines))
    print(f"\nWrote {OUT_DIR / 'exploration.md'}")


if __name__ == "__main__":
    main()
