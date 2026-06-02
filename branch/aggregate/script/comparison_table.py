#!/usr/bin/env python3
"""
comparison_table.py — One-process, same-seed, shared-base comparison of the
best vs suboptimal token configurations vs the two baselines, for SAE Phase 2.

WHY single-process: TabICL is CUDA-nondeterministic, so each separate run's
zero-shot/I+E base drifts by ~noise. To get a CLEAN comparison table (best combo
vs suboptimal vs baselines, with deltas), every configuration must be evaluated
in ONE process with the SAME seeds against the SAME base — then all Δ are
properly paired. (Cross-run absolute numbers are NOT directly comparable.)

Configs (each = full token list; 0-token = zero-shot tabular):
  tabular only                       : []
  tabular + I/E                      : I,E
  + brief_title                      : I,E,title
  + title + intervention_MeSH (best) : I,E,title,mesh_interv
  + condition + intervention MeSH    : I,E,mesh_cond,mesh_interv
  + all 9 text                       : I,E,<9 text>
  + all 9 text + SMILES (12 tok)     : I,E,<9 text>,smiles

Reports mean±std last5 ROC-AUC over n seeds, Δ vs tabular, Δ vs tabular+I/E,
and paired-t p vs tabular+I/E. Writes results/comparison_<phase>_<ts>/summary.md.
"""

from __future__ import annotations

import json
import sys
import time
from datetime import datetime
from pathlib import Path

import numpy as np
from scipy import stats

sys.path.insert(0, "/data2/zhu11/TB/branch/aggregate/script")
from ablation_search import PhaseData, train_eval, RESULTS_ROOT  # noqa: E402

TEXT9 = ["summary", "title", "condition", "detail", "interv_desc",
         "interv_name", "keyword", "sd_interv_model", "sd_masking"]

CONFIGS = [
    ("tabular only (zero-shot)",                 []),
    ("tabular + I/E",                            ["I", "E"]),
    ("+ brief_title",                            ["I", "E", "title"]),
    ("+ title + intervention_MeSH  (BEST)",      ["I", "E", "title", "mesh_interv"]),
    ("+ condition + intervention MeSH",          ["I", "E", "mesh_cond", "mesh_interv"]),
    ("+ all 9 text columns",                     ["I", "E"] + TEXT9),
    ("+ all 9 text + SMILES (12 tokens)",        ["I", "E"] + TEXT9 + ["smiles"]),
]


def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--phase", default="Phase2", choices=["Phase2", "Phase3"])
    p.add_argument("--subtask", default="serious-adverse-event-forecasting")
    p.add_argument("--target", default="Y/N")
    p.add_argument("--seeds", type=int, default=10)
    p.add_argument("--epochs", type=int, default=30)
    args = p.parse_args()

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = RESULTS_ROOT / f"comparison_{args.phase}_{ts}"
    out_dir.mkdir(parents=True, exist_ok=True)
    log_f = open(out_dir / "log.txt", "w"); raw_f = open(out_dir / "raw.jsonl", "w")

    def echo(*x):
        line = " ".join(str(z) for z in x); print(line, flush=True); print(line, file=log_f, flush=True)

    echo(f"[comparison] {args.phase}  seeds={args.seeds}  epochs={args.epochs}")
    echo("Preparing (load tokens + bootstrap once) ...")
    t0 = time.time()
    pd_ = PhaseData(args.subtask, args.target, args.phase, echo)
    seeds = list(range(args.seeds))
    echo(f"setup {time.time()-t0:.0f}s")

    vals = {}
    for label, names in CONFIGS:
        vs = []
        for s in seeds:
            v = train_eval(pd_, names, s, epochs=args.epochs)
            vs.append(v)
            raw_f.write(json.dumps({"label": label, "names": names, "seed": s, "last5": v}) + "\n"); raw_f.flush()
        vals[label] = vs
        echo(f"  {label:42} {np.mean(vs):.4f} ± {np.std(vs, ddof=1):.4f}")

    tab = np.array(vals[CONFIGS[0][0]])     # tabular only
    tabie = np.array(vals[CONFIGS[1][0]])   # tabular + I/E
    lines = [f"# SAE {args.phase} — token-configuration comparison",
             "",
             f"Frozen TabICLv2, Full Step 2. last5 test ROC-AUC (mean of last-5 eval epochs), "
             f"mean ± std over n={args.seeds} seeds, all evaluated in one process / same seeds / "
             f"shared base so deltas are properly paired. p = paired t-test vs *tabular + I/E*.",
             "",
             "| Configuration | tokens | ROC-AUC | Δ vs tabular | Δ vs tabular+I/E (p) |",
             "|---|---|---|---|---|"]
    for label, names in CONFIGS:
        a = np.array(vals[label]); m, sd = a.mean(), a.std(ddof=1)
        ntok = len(names)
        d_tab = m - tab.mean()
        if label == CONFIGS[0][0]:
            d_tab_s, d_tabie_s = "—", "—"
        elif label == CONFIGS[1][0]:
            d_tab_s = f"{d_tab:+.4f}"; d_tabie_s = "—"
        else:
            t, pp = stats.ttest_rel(a, tabie)
            sig = "***" if pp < 0.01 else "**" if pp < 0.05 else "*" if pp < 0.1 else ""
            d_tab_s = f"{d_tab:+.4f}"
            d_tabie_s = f"{(m - tabie.mean()):+.4f} (p={pp:.3f}) {sig}"
        lines.append(f"| {label} | {ntok} | {m:.4f} ± {sd:.4f} | {d_tab_s} | {d_tabie_s} |")
    lines.append("")
    (out_dir / "summary.md").write_text("\n".join(lines))
    echo("\n" + "\n".join(lines))
    echo(f"\nSaved: {out_dir/'summary.md'}")
    log_f.close(); raw_f.close()


if __name__ == "__main__":
    main()
