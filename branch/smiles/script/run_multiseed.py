#!/usr/bin/env python3
"""
run_multiseed.py — Drive full_step2_tabicl_smiles.py across {cells × phases × seeds}
and aggregate into mean±std tables.

WHY: TabICL forward/backward is CUDA-nondeterministic. Same config + same --seed
gives best-epoch ROC-AUC spread of ~0.01 (measured: 0.8655/0.8724/0.8748 on
Phase2 B'). That noise floor is the SAME ORDER as the SMILES effect we're trying
to measure, so single-run deltas are meaningless. We run N seeds per cell and
report mean±std.

Cells:
  B'                = +I+E (Qwen3), no SMILES token. Uses --report-subset-emb so it
                      still reports the SMILES-non-empty subset (clean Cell-D baseline).
  C:<encoder>       = +I+E+SMILES, one per chemistry encoder.

Metric reported: best-epoch test ROC-AUC (matches new_FM §3 convention), on
  - full test set
  - SMILES-non-empty test subset (Cell D)

Outputs:
  branch/smiles/results/multiseed_<YYYYMMDD_HHMMSS>/
    raw_runs.jsonl      # one line per run: cell, phase, seed, full_best, subset_best, run_id
    summary.json        # mean/std per (cell, phase)
    summary.md          # markdown tables
    log.txt

Each child run still writes its own results/<run_id>/metrics.json as usual.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import numpy as np

BRANCH = Path("/data2/zhu11/TB/branch/smiles")
DATA   = BRANCH / "data"
SCRIPT = BRANCH / "script" / "full_step2_tabicl_smiles.py"
RESULTS_ROOT = BRANCH / "results"
PY = "/data2/zhu11/miniconda3/envs/tabpfn/bin/python"

# Mask source for B' subset reporting (coverage identical across encoders).
MASK_PARQUET = DATA / "smiles_embeddings_chemberta_mlm.parquet"

# cell key → (--smiles-emb value or None)
ENCODERS = {
    "chemberta_mlm": DATA / "smiles_embeddings_chemberta_mlm.parquet",
    "chemberta_mtr": DATA / "smiles_embeddings_chemberta_mtr.parquet",
    "molformer":     DATA / "smiles_embeddings_molformer.parquet",
    "mol2vec":       DATA / "smiles_embeddings_mol2vec.parquet",
}


def run_one(cell: str, phase: str, seed: int, epochs: int) -> dict:
    """Run a single child training job, parse its metrics.json. Returns a dict
    with full_best / subset_best ROC-AUC."""
    cmd = [PY, str(SCRIPT), "--phase", phase, "--epochs", str(epochs), "--seed", str(seed)]
    if cell == "Bprime":
        cmd += ["--report-subset-emb", str(MASK_PARQUET)]
    else:
        cmd += ["--smiles-emb", str(ENCODERS[cell])]

    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        return {"cell": cell, "phase": phase, "seed": seed, "error": proc.stderr[-2000:]}

    # Find the run_dir from the "Saved:" line.
    saved = None
    for line in proc.stdout.splitlines():
        if "Saved:" in line:
            saved = line.split("Saved:")[-1].strip()
    if saved is None:
        return {"cell": cell, "phase": phase, "seed": seed, "error": "no Saved: line",
                "stdout_tail": proc.stdout[-1000:]}
    m = json.loads(Path(saved).read_text())
    return {
        "cell": cell, "phase": phase, "seed": seed,
        "run_id": m["run_id"],
        "full_best":   m["best_metrics"]["roc_auc"],
        "full_best_epoch": m["best_metrics"]["epoch"],
        "subset_best": (m["best_metrics_subset"]["roc_auc"]
                        if m.get("best_metrics_subset") else None),
        "subset_n":    m.get("smiles_test_subset_size"),
        "n_virt":      m["n_virtual_cols"],
    }


def main(args):
    run_id  = f"multiseed_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    out_dir = RESULTS_ROOT / run_id
    out_dir.mkdir(parents=True, exist_ok=True)
    log_f = open(out_dir / "log.txt", "w")
    raw_f = open(out_dir / "raw_runs.jsonl", "w")

    def echo(*parts):
        line = " ".join(str(p) for p in parts)
        print(line, flush=True)
        print(line, file=log_f, flush=True)

    cells  = ["Bprime"] + list(ENCODERS.keys())
    phases = args.phases.split(",")
    seeds  = list(range(args.seeds))
    echo(f"[multiseed] {run_id}")
    echo(f"  cells={cells}")
    echo(f"  phases={phases}  seeds={seeds}  epochs={args.epochs}")
    echo(f"  total runs: {len(cells) * len(phases) * len(seeds)}")

    raw = []
    for phase in phases:
        for cell in cells:
            for seed in seeds:
                r = run_one(cell, phase, seed, args.epochs)
                raw.append(r)
                raw_f.write(json.dumps(r) + "\n"); raw_f.flush()
                if "error" in r:
                    echo(f"  !! {cell:14} {phase} seed{seed}  ERROR: {r['error'][:120]}")
                else:
                    sub = f"{r['subset_best']:.4f}" if r["subset_best"] is not None else "  -  "
                    echo(f"  {cell:14} {phase} seed{seed}  "
                         f"full={r['full_best']:.4f} (ep{r['full_best_epoch']})  subset={sub}")

    # ---- Aggregate ----
    def agg(values):
        v = np.array([x for x in values if x is not None], dtype=float)
        if len(v) == 0:
            return None
        return {"mean": float(v.mean()), "std": float(v.std(ddof=1) if len(v) > 1 else 0.0),
                "min": float(v.min()), "max": float(v.max()), "n": int(len(v))}

    summary = {}
    for phase in phases:
        for cell in cells:
            rs = [r for r in raw if r.get("phase") == phase and r.get("cell") == cell and "error" not in r]
            summary[f"{phase}/{cell}"] = {
                "full":   agg([r["full_best"] for r in rs]),
                "subset": agg([r["subset_best"] for r in rs]),
                "subset_n": rs[0]["subset_n"] if rs else None,
            }
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2))

    # ---- Markdown ----
    def fmt(a):
        return f"{a['mean']:.4f} ± {a['std']:.4f}" if a else "—"

    cell_label = {"Bprime": "B' (+I+E)", "chemberta_mlm": "C: ChemBERTa-MLM",
                  "chemberta_mtr": "C: ChemBERTa-MTR", "molformer": "C: MolFormer",
                  "mol2vec": "C: Mol2Vec"}
    lines = [f"# Multi-seed summary ({run_id})", "",
             f"seeds={seeds}, epochs={args.epochs}, metric=best-epoch test ROC-AUC (mean ± std)", ""]
    for phase in phases:
        bp = summary[f"{phase}/Bprime"]
        lines += [f"## {phase}  (full test; SMILES subset n={bp['subset_n']})", "",
                  "| Cell | Full ROC-AUC | Δ vs B' (full) | SMILES-subset ROC-AUC | Δ vs B' (subset) |",
                  "|---|---|---|---|---|"]
        bp_full = bp["full"]["mean"] if bp["full"] else None
        bp_sub  = bp["subset"]["mean"] if bp["subset"] else None
        for cell in cells:
            s = summary[f"{phase}/{cell}"]
            d_full = (f"{s['full']['mean']-bp_full:+.4f}" if (s['full'] and bp_full is not None and cell != 'Bprime') else "—")
            d_sub  = (f"{s['subset']['mean']-bp_sub:+.4f}" if (s['subset'] and bp_sub is not None and cell != 'Bprime') else "—")
            lines.append(f"| {cell_label[cell]} | {fmt(s['full'])} | {d_full} | {fmt(s['subset'])} | {d_sub} |")
        lines.append("")
    (out_dir / "summary.md").write_text("\n".join(lines))

    echo("\n=== SUMMARY ===")
    echo("\n".join(lines))
    echo(f"\nSaved: {out_dir}/summary.md")
    log_f.close(); raw_f.close()


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--phases", default="Phase2,Phase3")
    p.add_argument("--seeds", type=int, default=5, help="Run seeds 0..N-1")
    p.add_argument("--epochs", type=int, default=30)
    args = p.parse_args()
    main(args)
