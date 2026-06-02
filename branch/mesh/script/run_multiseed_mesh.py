#!/usr/bin/env python3
"""
run_multiseed_mesh.py — multiseed driver for mesh branch (fork of
branch/smiles/script/run_multiseed.py). See that file's docstring for the
rationale (TabICL is CUDA-nondeterministic; ~0.01 noise floor → must multi-seed).

Cells: B' (+I+E, 2 token) + one per MeSH encoder (+I+E+condition+intervention,
4 token). B' reports the intervention-non-empty subset via --report-subset-mesh
so it's a clean Cell-D baseline.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime
from pathlib import Path

import numpy as np

BRANCH = Path("/data2/zhu11/TB/branch/mesh")
DATA   = BRANCH / "data"
SCRIPT = BRANCH / "script" / "full_step2_tabicl_mesh.py"
RESULTS_ROOT = BRANCH / "results"
PY = "/data2/zhu11/miniconda3/envs/tabpfn/bin/python"

MASK_PARQUET = DATA / "mesh_embeddings_sapbert.parquet"  # intervention-nonempty mask (same across encoders)

ENCODERS = {
    "sapbert":    DATA / "mesh_embeddings_sapbert.parquet",
    "biolord":    DATA / "mesh_embeddings_biolord.parquet",
    "medcpt":     DATA / "mesh_embeddings_medcpt.parquet",
    "pubmedbert": DATA / "mesh_embeddings_pubmedbert.parquet",
    "qwen3":      DATA / "mesh_embeddings_qwen3.parquet",
}


def run_one(cell, phase, seed, epochs):
    cmd = [PY, str(SCRIPT), "--phase", phase, "--epochs", str(epochs), "--seed", str(seed)]
    if cell == "Bprime":
        cmd += ["--report-subset-mesh", str(MASK_PARQUET)]
    else:
        cmd += ["--mesh-emb", str(ENCODERS[cell])]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        return {"cell": cell, "phase": phase, "seed": seed, "error": proc.stderr[-2000:]}
    saved = None
    for line in proc.stdout.splitlines():
        if "Saved:" in line:
            saved = line.split("Saved:")[-1].strip()
    if saved is None:
        return {"cell": cell, "phase": phase, "seed": seed, "error": "no Saved: line",
                "stdout_tail": proc.stdout[-1000:]}
    m = json.loads(Path(saved).read_text())
    return {
        "cell": cell, "phase": phase, "seed": seed, "run_id": m["run_id"],
        "full_best": m["best_metrics"]["roc_auc"],
        "full_best_epoch": m["best_metrics"]["epoch"],
        "subset_best": (m["best_metrics_subset"]["roc_auc"] if m.get("best_metrics_subset") else None),
        "subset_n": m.get("interv_test_subset_size"),
        "n_virt": m["n_virtual_cols"],
    }


def main(args):
    if args.append_to:
        out_dir = Path(args.append_to)
        if not out_dir.exists():
            raise FileNotFoundError(out_dir)
        run_id = out_dir.name
    else:
        run_id  = f"multiseed_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        out_dir = RESULTS_ROOT / run_id
        out_dir.mkdir(parents=True, exist_ok=True)
    log_f = open(out_dir / "log.txt", "a" if args.append_to else "w")
    raw_f = open(out_dir / "raw_runs.jsonl", "a" if args.append_to else "w")

    def echo(*parts):
        line = " ".join(str(p) for p in parts)
        print(line, flush=True); print(line, file=log_f, flush=True)

    cells  = args.cells.split(",") if args.cells else (["Bprime"] + list(ENCODERS.keys()))
    phases = args.phases.split(",")
    seeds  = list(range(args.seed_start, args.seed_start + args.seeds))
    echo(f"[multiseed-mesh] {run_id}  cells={cells}  phases={phases}  seeds={seeds}  epochs={args.epochs}")
    echo(f"  total runs: {len(cells) * len(phases) * len(seeds)}")

    raw = []
    for phase in phases:
        for cell in cells:
            for seed in seeds:
                r = run_one(cell, phase, seed, args.epochs)
                raw.append(r)
                raw_f.write(json.dumps(r) + "\n"); raw_f.flush()
                if "error" in r:
                    echo(f"  !! {cell:12} {phase} seed{seed}  ERROR: {r['error'][:120]}")
                else:
                    sub = f"{r['subset_best']:.4f}" if r["subset_best"] is not None else "  -  "
                    echo(f"  {cell:12} {phase} seed{seed}  full={r['full_best']:.4f} (ep{r['full_best_epoch']})  subset={sub}")

    def agg(values):
        v = np.array([x for x in values if x is not None], dtype=float)
        if len(v) == 0:
            return None
        return {"mean": float(v.mean()), "std": float(v.std(ddof=1)) if len(v) > 1 else 0.0, "n": int(len(v))}

    summary = {}
    for phase in phases:
        for cell in cells:
            rs = [r for r in raw if r.get("phase") == phase and r.get("cell") == cell and "error" not in r]
            summary[f"{phase}/{cell}"] = {
                "full": agg([r["full_best"] for r in rs]),
                "subset": agg([r["subset_best"] for r in rs]),
                "subset_n": rs[0]["subset_n"] if rs else None,
            }
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2))
    echo(f"\nDONE. Saved raw_runs.jsonl + summary.json to {out_dir}")
    echo("Run aggregate_robust_mesh.py for last5/best/final mean±std tables.")
    log_f.close(); raw_f.close()


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--phases", default="Phase2,Phase3")
    p.add_argument("--seeds", type=int, default=5)
    p.add_argument("--seed-start", type=int, default=0, help="First seed (seeds = start..start+seeds-1)")
    p.add_argument("--append-to", default=None, help="Existing multiseed dir to append raw_runs.jsonl into")
    p.add_argument("--cells", default=None, help="comma-list of cells to run (default: Bprime + all encoders)")
    p.add_argument("--epochs", type=int, default=30)
    args = p.parse_args()
    main(args)
