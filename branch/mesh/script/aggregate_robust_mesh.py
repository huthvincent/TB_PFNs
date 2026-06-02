#!/usr/bin/env python3
"""
aggregate_robust_mesh.py — robust aggregation of a mesh multiseed run.
Fork of branch/smiles/script/aggregate_robust.py (same last5/best/final logic;
mesh cell labels + results root). See that file for rationale.

last5 = mean of last 5 eval epochs (noise-robust, preferred);
best = max over evals (optimistic); final = last epoch.
Reported mean±std across seeds, Δ vs B'.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

RESULTS_ROOT = Path("/data2/zhu11/TB/branch/mesh/results")
CELL_ORDER = ["Bprime", "sapbert", "biolord", "medcpt", "pubmedbert", "qwen3"]
CELL_LABEL = {"Bprime": "B' (+I+E)", "sapbert": "C: SapBERT", "biolord": "C: BioLORD-2023",
              "medcpt": "C: MedCPT", "pubmedbert": "C: PubMedBERT", "qwen3": "C: Qwen3-8B"}
LAST_K = 5


def metric_from_history(history, key_path, kind):
    series = []
    for h in history:
        node = h; ok = True
        for k in key_path:
            if isinstance(node, dict) and k in node and node[k] is not None:
                node = node[k]
            else:
                ok = False; break
        if ok and isinstance(node, (int, float)):
            series.append(float(node))
    if not series:
        return None
    arr = np.array(series, dtype=float)
    return {"best": float(arr.max()), "final": float(arr[-1]),
            "last5": float(arr[-LAST_K:].mean())}[kind]


def agg(values):
    v = np.array([x for x in values if x is not None], dtype=float)
    if len(v) == 0:
        return None
    return {"mean": float(v.mean()), "std": float(v.std(ddof=1)) if len(v) > 1 else 0.0, "n": int(len(v))}


def main():
    if len(sys.argv) > 1:
        run_dir = Path(sys.argv[1])
    else:
        cands = sorted(RESULTS_ROOT.glob("multiseed_*"))
        if not cands:
            sys.exit("No multiseed_* dirs found.")
        run_dir = cands[-1]
    print(f"[aggregate-mesh] {run_dir}")

    raw = [json.loads(l) for l in (run_dir / "raw_runs.jsonl").read_text().splitlines() if l.strip()]
    raw = [r for r in raw if "error" not in r]
    for r in raw:
        m = json.loads((RESULTS_ROOT / r["run_id"] / "metrics.json").read_text())
        hist = m["history"]
        for kind in ("best", "final", "last5"):
            r[f"full_{kind}"]   = metric_from_history(hist, ("roc_auc",), kind)
            r[f"subset_{kind}"] = metric_from_history(hist, ("subset", "roc_auc"), kind)

    phases = sorted({r["phase"] for r in raw})
    out = ["# Robust multi-seed aggregation (mesh)", "",
           f"last5 = mean of last {LAST_K} eval epochs (preferred); best = max over evals; final = last epoch.",
           "mean ± std across seeds. Δ = vs B' same metric/phase. Subset = intervention-MeSH-non-empty test trials.", ""]
    summary = {}
    for phase in phases:
        bp_rows = [r for r in raw if r["phase"] == phase and r["cell"] == "Bprime"]
        noise = agg([r["full_last5"] for r in bp_rows])
        out.append(f"## {phase}")
        if noise:
            out.append(f"_B' full-last5 noise floor: std={noise['std']:.4f} (n={noise['n']} seeds)_")
        out.append("")
        for metric in ("last5", "best", "final"):
            sub_n = next((r.get("subset_n") for r in bp_rows if r.get("subset_n")), None)
            out += [f"### {phase} — metric={metric}  (interv subset n={sub_n})", "",
                    "| Cell | Full | Δ vs B' | Interv-subset | Δ vs B' |", "|---|---|---|---|---|"]
            bpf = agg([r[f"full_{metric}"] for r in bp_rows])
            bps = agg([r[f"subset_{metric}"] for r in bp_rows])
            for cell in CELL_ORDER:
                rs = [r for r in raw if r["phase"] == phase and r["cell"] == cell]
                if not rs:
                    continue
                af = agg([r[f"full_{metric}"] for r in rs])
                asb = agg([r[f"subset_{metric}"] for r in rs])
                df = (f"{af['mean']-bpf['mean']:+.4f}" if (af and bpf and cell != "Bprime") else "—")
                ds = (f"{asb['mean']-bps['mean']:+.4f}" if (asb and bps and cell != "Bprime") else "—")
                ff = f"{af['mean']:.4f} ± {af['std']:.4f}" if af else "—"
                fs = f"{asb['mean']:.4f} ± {asb['std']:.4f}" if asb else "—"
                out.append(f"| {CELL_LABEL[cell]} | {ff} | {df} | {fs} | {ds} |")
                summary[f"{phase}/{cell}/{metric}"] = {"full": af, "subset": asb}
            out.append("")
    (run_dir / "robust_summary.md").write_text("\n".join(out))
    (run_dir / "robust_summary.json").write_text(json.dumps(summary, indent=2))
    print("\n".join(out))
    print(f"\nSaved: {run_dir / 'robust_summary.md'}")


if __name__ == "__main__":
    main()
