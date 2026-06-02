#!/usr/bin/env python3
"""
aggregate_robust.py — Post-hoc robust aggregation of a multiseed run.

`run_multiseed.py` reports best-epoch ROC-AUC (= max over ~15 noisy eval points),
which is optimistically biased upward by the CUDA noise. This script re-reads
every child run's metrics.json history and computes THREE metrics per run, for
both full test set and SMILES-non-empty subset:

  - best   : max over eval epochs           (matches new_FM §3; noise-inflated)
  - final  : last eval epoch                (single converged point)
  - last5  : mean of last 5 eval epochs     (robust converged estimate ← preferred)

then aggregates mean±std across seeds per (phase, cell), and prints Δ vs B'
alongside the measured noise floor so deltas can be judged for significance.

Usage:
  python aggregate_robust.py <multiseed_run_dir>
  # e.g. .../results/multiseed_20260602_0030xx
If omitted, uses the newest multiseed_* dir.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

RESULTS_ROOT = Path("/data2/zhu11/TB/branch/smiles/results")
CELL_ORDER = ["Bprime", "chemberta_mlm", "chemberta_mtr", "molformer", "mol2vec"]
CELL_LABEL = {"Bprime": "B' (+I+E)", "chemberta_mlm": "C: ChemBERTa-MLM",
              "chemberta_mtr": "C: ChemBERTa-MTR", "molformer": "C: MolFormer",
              "mol2vec": "C: Mol2Vec"}
LAST_K = 5


def metric_from_history(history: list, key_path: tuple, kind: str) -> float | None:
    """Extract a per-epoch ROC-AUC series and reduce by kind∈{best,final,last5}.
    key_path: ('roc_auc',) for full, ('subset','roc_auc') for subset."""
    series = []
    for h in history:
        node = h
        ok = True
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
    if kind == "best":
        return float(arr.max())
    if kind == "final":
        return float(arr[-1])
    if kind == "last5":
        return float(arr[-LAST_K:].mean())
    raise ValueError(kind)


def agg(values):
    v = np.array([x for x in values if x is not None], dtype=float)
    if len(v) == 0:
        return None
    return {"mean": float(v.mean()),
            "std": float(v.std(ddof=1)) if len(v) > 1 else 0.0,
            "n": int(len(v))}


def main():
    if len(sys.argv) > 1:
        run_dir = Path(sys.argv[1])
    else:
        cands = sorted(RESULTS_ROOT.glob("multiseed_*"))
        if not cands:
            sys.exit("No multiseed_* dirs found.")
        run_dir = cands[-1]
    print(f"[aggregate] {run_dir}")

    raw = [json.loads(l) for l in (run_dir / "raw_runs.jsonl").read_text().splitlines() if l.strip()]
    raw = [r for r in raw if "error" not in r]

    # Attach robust metrics by reading each child metrics.json history.
    for r in raw:
        child = RESULTS_ROOT / r["run_id"] / "metrics.json"
        m = json.loads(child.read_text())
        hist = m["history"]
        for kind in ("best", "final", "last5"):
            r[f"full_{kind}"]   = metric_from_history(hist, ("roc_auc",), kind)
            r[f"subset_{kind}"] = metric_from_history(hist, ("subset", "roc_auc"), kind)

    phases = sorted({r["phase"] for r in raw})
    # Noise floor: std across seeds of B' full-last5 (cleanest repeated-config estimate).
    out_lines = ["# Robust multi-seed aggregation", "",
                 f"Metrics: **last5** = mean of last {LAST_K} eval epochs (preferred, "
                 "noise-robust); best = max over evals (optimistic); final = last epoch.",
                 f"Reported as mean ± std across seeds. Δ = vs B' same-metric same-phase.", ""]

    summary = {}
    for phase in phases:
        bp_rows = [r for r in raw if r["phase"] == phase and r["cell"] == "Bprime"]
        noise = agg([r["full_last5"] for r in bp_rows])
        out_lines.append(f"## {phase}")
        if noise:
            out_lines.append(f"_B' full-last5 noise floor: std={noise['std']:.4f} over n={noise['n']} seeds_")
        out_lines.append("")
        for metric in ("last5", "best", "final"):
            sub_n = next((r.get("subset_n") for r in bp_rows if r.get("subset_n")), None)
            out_lines += [f"### {phase} — metric={metric}  (SMILES subset n={sub_n})", "",
                          "| Cell | Full | Δ vs B' | SMILES-subset | Δ vs B' |",
                          "|---|---|---|---|---|"]
            bp_full = agg([r[f"full_{metric}"] for r in bp_rows])
            bp_sub  = agg([r[f"subset_{metric}"] for r in bp_rows])
            for cell in CELL_ORDER:
                rs = [r for r in raw if r["phase"] == phase and r["cell"] == cell]
                if not rs:
                    continue
                af = agg([r[f"full_{metric}"] for r in rs])
                asb = agg([r[f"subset_{metric}"] for r in rs])
                df = (f"{af['mean']-bp_full['mean']:+.4f}" if (af and bp_full and cell != "Bprime") else "—")
                ds = (f"{asb['mean']-bp_sub['mean']:+.4f}" if (asb and bp_sub and cell != "Bprime") else "—")
                ff = f"{af['mean']:.4f} ± {af['std']:.4f}" if af else "—"
                fs = f"{asb['mean']:.4f} ± {asb['std']:.4f}" if asb else "—"
                out_lines.append(f"| {CELL_LABEL[cell]} | {ff} | {df} | {fs} | {ds} |")
                summary[f"{phase}/{cell}/{metric}"] = {"full": af, "subset": asb}
            out_lines.append("")

    (run_dir / "robust_summary.md").write_text("\n".join(out_lines))
    (run_dir / "robust_summary.json").write_text(json.dumps(summary, indent=2))
    print("\n".join(out_lines))
    print(f"\nSaved: {run_dir / 'robust_summary.md'}")


if __name__ == "__main__":
    main()
