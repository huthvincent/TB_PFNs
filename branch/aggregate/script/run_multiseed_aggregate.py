#!/usr/bin/env python3
"""
run_multiseed_aggregate.py — multiseed driver + robust aggregation + paired
t-test for the aggregate branch.

Cells (all on frozen TabICLv2, Full Step 2):
  Bprime : I + E                         (2 tokens)   — baseline
  text   : I + E + 9 All_text columns    (11 tokens)  — +all text
  all    : I + E + 9 text + SMILES       (12 tokens)  — everything

Metric: last5 = mean of last 5 eval epochs (noise-robust; TabICL Full-Step-2 is
CUDA-nondeterministic — see branch/smiles). Reports mean±std across seeds and a
paired t-test (per seed) of text/all vs Bprime.

Supports --seed-start / --append-to for incremental seed top-ups (same as
branch/mesh/script/run_multiseed_mesh.py).
"""

from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime
from pathlib import Path

import numpy as np
from scipy import stats

BRANCH = Path("/data2/zhu11/TB/branch/aggregate")
DATA   = BRANCH / "data"
SCRIPT = BRANCH / "script" / "full_step2_tabicl_multi.py"
RESULTS_ROOT = BRANCH / "results"
PY = "/data2/zhu11/miniconda3/envs/tabpfn/bin/python"

IE   = [f"{DATA}/ie_embeddings_qwen3.parquet@I", f"{DATA}/ie_embeddings_qwen3.parquet@E"]
TEXT = sorted(str(p) for p in DATA.glob("emb_*_qwen.parquet"))
SM   = [f"{DATA}/smiles_embeddings_molformer.parquet"]

CELLS = {
    "Bprime": IE,
    "text":   IE + TEXT,
    "all":    IE + TEXT + SM,
}


def run_one(cell, phase, seed, epochs):
    specs = ",".join(CELLS[cell])
    cmd = [PY, str(SCRIPT), "--phase", phase, "--epochs", str(epochs),
           "--seed", str(seed), "--tag", cell, "--virt-embs", specs]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        return {"cell": cell, "phase": phase, "seed": seed, "error": proc.stderr[-2000:]}
    saved = None
    for line in proc.stdout.splitlines():
        if "Saved:" in line:
            saved = line.split("Saved:")[-1].strip()
    if saved is None:
        return {"cell": cell, "phase": phase, "seed": seed, "error": "no Saved: line"}
    m = json.loads(Path(saved).read_text())
    hist = m["history"]
    last5 = float(np.mean([h["roc_auc"] for h in hist][-5:]))
    return {"cell": cell, "phase": phase, "seed": seed, "run_id": m["run_id"],
            "n_tokens": m["n_virtual_cols"], "n_trainable": m["n_trainable_params"],
            "best": m["best_metrics"]["roc_auc"], "last5": last5}


def agg(vals):
    v = np.array([x for x in vals if x is not None], float)
    return None if len(v) == 0 else {"mean": float(v.mean()),
                                     "std": float(v.std(ddof=1)) if len(v) > 1 else 0.0,
                                     "n": int(len(v))}


def main(args):
    if args.append_to:
        out_dir = Path(args.append_to); run_id = out_dir.name
    else:
        run_id = f"multiseed_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        out_dir = RESULTS_ROOT / run_id; out_dir.mkdir(parents=True, exist_ok=True)
    log_f = open(out_dir / "log.txt", "a" if args.append_to else "w")
    raw_f = open(out_dir / "raw_runs.jsonl", "a" if args.append_to else "w")

    def echo(*p):
        line = " ".join(str(x) for x in p); print(line, flush=True); print(line, file=log_f, flush=True)

    cells = args.cells.split(",")
    phases = args.phases.split(",")
    seeds = list(range(args.seed_start, args.seed_start + args.seeds))
    echo(f"[aggregate-multiseed] {run_id}  cells={cells}  phases={phases}  seeds={seeds}  epochs={args.epochs}")
    for c in cells:
        echo(f"  cell {c}: {len(CELLS[c])} tokens")

    raw = []
    for phase in phases:
        for cell in cells:
            for seed in seeds:
                r = run_one(cell, phase, seed, args.epochs)
                raw.append(r); raw_f.write(json.dumps(r) + "\n"); raw_f.flush()
                if "error" in r:
                    echo(f"  !! {cell:7} {phase} s{seed} ERROR {r['error'][:100]}")
                else:
                    echo(f"  {cell:7} {phase} s{seed}  last5={r['last5']:.4f} best={r['best']:.4f} ({r['n_tokens']}tok)")

    # ---- aggregate all rows in dir (include appended) ----
    all_raw = [json.loads(l) for l in (out_dir / "raw_runs.jsonl").read_text().splitlines() if l.strip()]
    all_raw = [r for r in all_raw if "error" not in r]
    phases_seen = sorted({r["phase"] for r in all_raw})
    lines = [f"# Aggregate branch — multiseed (last5 ROC-AUC, mean±std, paired t vs B')", ""]
    for phase in phases_seen:
        bp = {r["seed"]: r for r in all_raw if r["phase"] == phase and r["cell"] == "Bprime"}
        lines += [f"## {phase}", "",
                  "| Cell | tokens | last5 ROC-AUC | Δ vs B' | paired t | p |", "|---|---|---|---|---|---|"]
        for cell in ["Bprime", "text", "all"]:
            rs = {r["seed"]: r for r in all_raw if r["phase"] == phase and r["cell"] == cell}
            if not rs:
                continue
            a = agg([r["last5"] for r in rs.values()])
            ntok = next(iter(rs.values()))["n_tokens"]
            if cell == "Bprime":
                lines.append(f"| B' (I+E) | {ntok} | {a['mean']:.4f} ± {a['std']:.4f} (n={a['n']}) | — | — | — |")
            else:
                seeds_common = sorted(set(bp) & set(rs))
                x = [rs[s]["last5"] for s in seeds_common]; y = [bp[s]["last5"] for s in seeds_common]
                d = np.mean(np.array(x) - np.array(y))
                t, p = stats.ttest_rel(x, y) if len(seeds_common) > 1 else (float("nan"), float("nan"))
                sig = "***" if p < 0.01 else "**" if p < 0.05 else "*" if p < 0.1 else ""
                label = {"text": "+all text (I+E+9text)", "all": "ALL (+SMILES)"}[cell]
                lines.append(f"| {label} | {ntok} | {a['mean']:.4f} ± {a['std']:.4f} (n={a['n']}) | "
                             f"{d:+.4f} | {t:+.2f} | {p:.3f} {sig} |")
        lines.append("")
    (out_dir / "summary.md").write_text("\n".join(lines))
    echo("\n" + "\n".join(lines))
    echo(f"Saved: {out_dir / 'summary.md'}")
    log_f.close(); raw_f.close()


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--cells", default="Bprime,text,all")
    p.add_argument("--phases", default="Phase2,Phase3")
    p.add_argument("--seeds", type=int, default=5)
    p.add_argument("--seed-start", type=int, default=0)
    p.add_argument("--append-to", default=None)
    p.add_argument("--epochs", type=int, default=30)
    args = p.parse_args()
    main(args)
