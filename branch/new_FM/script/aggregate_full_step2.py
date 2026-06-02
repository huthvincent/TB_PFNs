#!/usr/bin/env python3
"""
aggregate_full_step2.py — pull together all Full Step 2 results from 3 FMs
(TabPFN, TabICL, Mitra) × 6 subtasks × 2 phases, and pair them with each FM's
zero-shot baseline (from prior fm_bench_ie.py runs).

Outputs a markdown-ready table to stdout.
"""

from __future__ import annotations

import glob
import json
from collections import defaultdict
from pathlib import Path


SUBTASKS = [
    ("serious-adverse-event-forecasting",   "binary",     "roc_auc"),
    ("mortality-event-prediction",          "binary",     "roc_auc"),
    ("patient-dropout-event-forecasting",   "binary",     "roc_auc"),
    ("trial-approval-forecasting",          "binary",     "roc_auc"),
    ("trial-failure-reason-identification", "multiclass", "macro_f1"),
    ("trial-duration-forecasting",          "regression", "r2"),
]
PHASES = ["Phase2", "Phase3"]
FMS    = ["tabpfn", "tabicl", "mitra"]
METRIC_NAME = {"roc_auc": "ROC-AUC", "macro_f1": "macro-F1", "r2": "R²"}


def _latest(paths):
    return max(paths, key=lambda p: Path(p).stat().st_mtime)


def load_baseline_per_fm():
    """For each (subtask, phase, fm), pick the latest fm_bench_ie metrics.json
    and extract `models[fm].baseline.<metric>`."""
    out = {}
    runs = sorted(glob.glob("/data2/zhu11/TB/branch/new_FM/results/fm_bench_ie_*/metrics.json"))
    by_key = {}
    for p in runs:
        d = json.load(open(p))
        key = (d["subtask"], d["phase"])
        by_key.setdefault(key, []).append(p)
    for (sub, ph), paths in by_key.items():
        d = json.load(open(_latest(paths)))
        for fm in FMS:
            row = d["models"].get(fm)
            if row is None:
                continue
            out[(fm, sub, ph)] = row["baseline"]
    return out


def load_full_step2_tabpfn():
    """Pull all full_step2_<subtask>_<target>_<ts>/metrics.json in IE_embedding."""
    out = {}
    by_key = {}
    for p in sorted(glob.glob("/data2/zhu11/TB/branch/IE_embedding/results/full_step2_*/metrics.json")):
        d = json.load(open(p))
        args = d.get("args", {})
        # TabPFN script's --phases is a comma-sep string; we restricted to single phase
        ph_arg = args.get("phases")
        if not ph_arg:
            continue
        sub = d["subtask"]
        # ph_arg could be "Phase2" or "Phase2,Phase3"; we use single-phase runs
        if "," in ph_arg:
            continue
        by_key.setdefault((sub, ph_arg), []).append(p)
    for (sub, ph), paths in by_key.items():
        d = json.load(open(_latest(paths)))
        out[("tabpfn", sub, ph)] = d["best_metrics"]
    return out


def load_full_step2_other(fm: str):
    """Pull all full_step2_<fm>_<subtask>_<target>_<phase>_<ts>/metrics.json."""
    out = {}
    by_key = {}
    for p in sorted(glob.glob(f"/data2/zhu11/TB/branch/new_FM/results/full_step2_{fm}_*/metrics.json")):
        d = json.load(open(p))
        sub = d["subtask"]
        ph  = d["phase"]
        by_key.setdefault((sub, ph), []).append(p)
    for (sub, ph), paths in by_key.items():
        d = json.load(open(_latest(paths)))
        out[(fm, sub, ph)] = d["best_metrics"]
    return out


def main():
    baselines = load_baseline_per_fm()
    fs2 = {}
    fs2.update(load_full_step2_tabpfn())
    fs2.update(load_full_step2_other("tabicl"))
    fs2.update(load_full_step2_other("mitra"))

    print(f"loaded baselines: {len(baselines)}")
    print(f"loaded full_step2 cells: {len(fs2)} (expect {len(FMS)*len(SUBTASKS)*len(PHASES)}={len(FMS)*len(SUBTASKS)*len(PHASES)})\n")

    # Wide table per phase
    for ph in PHASES:
        print(f"### {ph}\n")
        cols = ["Subtask", "task", "metric"]
        for fm in FMS:
            cols += [f"{fm} base", f"{fm} +IE", f"Δ"]
        print("| " + " | ".join(cols) + " |")
        print("|" + "|".join(["---"] * len(cols)) + "|")
        for sub, tt, metric in SUBTASKS:
            row = [sub, tt, METRIC_NAME[metric]]
            for fm in FMS:
                b = baselines.get((fm, sub, ph), {}).get(metric)
                e = fs2.get((fm, sub, ph), {}).get(metric)
                if b is None or e is None:
                    row += ["?", "?", "?"]
                else:
                    d = e - b
                    row += [f"{b:.4f}", f"{e:.4f}", f"{d:+.4f}"]
            print("| " + " | ".join(row) + " |")
        print()


if __name__ == "__main__":
    main()
