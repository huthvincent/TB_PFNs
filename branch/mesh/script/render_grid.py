#!/usr/bin/env python3
"""render_grid.py — turn mesh_eval_grid grid.json into the markdown tables for
final_readme.md. Per-task tables (phases × baseline+5 encoder Δ) + an aggregate
summary (mean Δ and win-rate per encoder)."""
import json
import sys
from pathlib import Path
import numpy as np

RR = Path("/data2/zhu11/TB/branch/mesh/results")
ENCS = ["sapbert", "biolord", "medcpt", "pubmedbert", "qwen3"]
ENC_LABEL = {"sapbert": "SapBERT", "biolord": "BioLORD", "medcpt": "MedCPT",
             "pubmedbert": "PubMedBERT", "qwen3": "Qwen3-8B"}
TASK_LABEL = {
    "serious-adverse-event-forecasting": "serious-adverse-event (binary, ROC-AUC)",
    "mortality-event-prediction": "mortality-event (binary, ROC-AUC)",
    "patient-dropout-event-forecasting": "patient-dropout (binary, ROC-AUC)",
    "trial-duration-forecasting": "trial-duration (regression, R²)",
    "trial-failure-reason-identification": "trial-failure-reason (multiclass, macro-F1)",
}
TASK_ORDER = list(TASK_LABEL)
PHASES = ["Phase1", "Phase2", "Phase3"]


def main():
    d = Path(sys.argv[1]) if len(sys.argv) > 1 else sorted(RR.glob("mesh_grid_*"))[-1]
    grid = json.loads((d / "grid.json").read_text())
    out = []
    out.append("Frozen TabICLv2, Full Step 2. **Baseline = tabular + I/E** (Qwen3-Embedding-8B, "
               "2 virtual tokens). Each MeSH column adds **condition + intervention MeSH as 2 extra "
               "virtual tokens** (4 total), encoded by the named model. **Single seed** (seed=0); "
               "metric = mean of last-5 eval-epoch primary metric. Δ = MeSH − baseline (same cell). "
               "Bold = best encoder in that row.")
    out.append("")
    out.append("> ⚠️ Single-seed point estimates. From the earlier multi-seed study the run-to-run "
               "noise floor is ~±0.005–0.010 (binary/regression) on this setup, so |Δ| below ~0.01 "
               "is within noise — read the *patterns across phases/tasks*, not individual cells.")
    out.append("")

    all_delta = {e: [] for e in ENCS}
    for task in TASK_ORDER:
        out.append(f"### {TASK_LABEL[task]}")
        out.append("")
        out.append("| Phase | baseline (tab+I/E) | " + " | ".join(f"+{ENC_LABEL[e]} Δ" for e in ENCS) + " |")
        out.append("|---|---|" + "---|" * len(ENCS))
        for ph in PHASES:
            key = f"{task}/{ph}"
            if key not in grid:
                out.append(f"| {ph} | (n/a) | " + " | ".join("—" for _ in ENCS) + " |")
                continue
            cells = grid[key]["cells"]
            base = cells["baseline"]
            deltas = {e: cells[e] - base for e in ENCS}
            for e in ENCS:
                all_delta[e].append(deltas[e])
            best_e = max(ENCS, key=lambda e: deltas[e])
            cellstrs = []
            for e in ENCS:
                s = f"{deltas[e]:+.4f}"
                if e == best_e and deltas[e] > 0:
                    s = f"**{s}**"
                cellstrs.append(s)
            out.append(f"| {ph} | {base:.4f} | " + " | ".join(cellstrs) + " |")
        out.append("")

    # aggregate
    out.append("### Aggregate across all 15 task×phase cells")
    out.append("")
    out.append("| Encoder | mean Δ | median Δ | win-rate (Δ>0) | #cells Δ>+0.01 | #cells Δ<−0.01 |")
    out.append("|---|---|---|---|---|---|")
    for e in ENCS:
        a = np.array(all_delta[e])
        out.append(f"| {ENC_LABEL[e]} | {a.mean():+.4f} | {np.median(a):+.4f} | "
                   f"{(a>0).mean()*100:.0f}% ({(a>0).sum()}/{len(a)}) | "
                   f"{(a>0.01).sum()} | {(a<-0.01).sum()} |")
    out.append("")
    print("\n".join(out))


if __name__ == "__main__":
    main()
