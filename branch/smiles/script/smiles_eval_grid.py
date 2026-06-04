#!/usr/bin/env python3
"""
smiles_eval_grid.py — Comprehensive SMILES evaluation grid (mirror of
branch/mesh/script/mesh_eval_grid.py).

Frozen TabICLv2, Full Step 2. Baseline = tabular + I/E (Qwen3-Embedding-8B, 2
virtual tokens). Each SMILES cell adds the drug SMILES as 1 extra virtual token
(3 total; mean-pooled over a trial's SMILES), encoded by one of 4 chemistry
models. Evaluated across 5 tasks × Phase1-3, single seed (no variance).

Tasks (target, task-type, metric): same 5 as mesh grid.
SMILES encoders: chemberta_mlm, chemberta_mtr, molformer, mol2vec
  (data/smiles_embeddings_*.parquet, rebuilt to cover all 5 tasks via --subtasks).
I/E: data/ie_embeddings_qwen3.parquet (covers all trials).

Reuses run_cell / encode_labels / metric_of / primary from mesh_eval_grid, and
the TabICL multi-token plumbing from full_step2_tabicl_multi.

Output: results/smiles_grid_<ts>/grid.json
"""

from __future__ import annotations

import json
import sys
import time
from datetime import datetime
from pathlib import Path

import numpy as np
import torch

sys.path.insert(0, "/data2/zhu11/TB/branch/aggregate/script")
from full_step2_tabicl_multi import (  # noqa: E402
    load_token_lookup, align, build_sklearn_preprocessor, preprocess, load_split_generic,
)
sys.path.insert(0, "/data2/zhu11/TB/branch/mesh/script")
from mesh_eval_grid import run_cell, encode_labels, TASKS, PHASES, SEED  # noqa: E402

DEVICE = "cuda"
DATA = Path("/data2/zhu11/TB/branch/smiles/data")
RESULTS_ROOT = Path("/data2/zhu11/TB/branch/smiles/results")

IE_PARQUET = DATA / "ie_embeddings_qwen3.parquet"
SMILES_ENCODERS = ["chemberta_mlm", "chemberta_mtr", "molformer", "mol2vec"]


def main():
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = RESULTS_ROOT / f"smiles_grid_{ts}"
    out_dir.mkdir(parents=True, exist_ok=True)
    log_f = open(out_dir / "log.txt", "w")

    def echo(*x):
        line = " ".join(str(z) for z in x); print(line, flush=True); print(line, file=log_f, flush=True)

    echo(f"[smiles_grid] {ts}  tasks={len(TASKS)} phases={PHASES} encoders={SMILES_ENCODERS} seed={SEED}")
    t0 = time.time()

    echo("Loading I/E + SMILES lookups once ...")
    _, ie_I, d_ie = load_token_lookup(f"{IE_PARQUET}@I")
    _, ie_E, _ = load_token_lookup(f"{IE_PARQUET}@E")
    sm_lk = {}
    for enc in SMILES_ENCODERS:
        p = DATA / f"smiles_embeddings_{enc}.parquet"
        _, lk, d = load_token_lookup(str(p))   # list mean_emb, no @TYPE
        sm_lk[enc] = (lk, d)
        echo(f"  {enc}: d={d}  keys={len(lk):,}")
    echo(f"  I/E d={d_ie}  setup {time.time()-t0:.0f}s")

    grid = {}
    from tabicl import TabICLClassifier
    for task, target, ttype, metric_name in TASKS:
        for phase in PHASES:
            tag = f"{task}/{phase}"
            try:
                Xtr_df, ytr = load_split_generic(task, "train", target, [phase])
                Xte_df, yte = load_split_generic(task, "test", target, [phase])
            except Exception as e:
                echo(f"  !! {tag}: load failed {e}"); continue
            y_tr_int, y_te_int, n_classes, classes, y_te_cont, bin_centers = encode_labels(ytr, yte, ttype)
            Xtr_p, Xte_p = preprocess(Xtr_df, Xte_df)
            sk = build_sklearn_preprocessor(Xtr_p)
            X_tr_arr = sk.fit_transform(Xtr_p); X_te_arr = sk.transform(Xte_p)
            X_tr = torch.from_numpy(X_tr_arr.astype(np.float32))
            X_te = torch.from_numpy(X_te_arr.astype(np.float32))
            y_tr_t = torch.from_numpy(y_tr_int.astype(np.int64))
            n_train = X_tr.shape[0]
            qry = min(500, max(50, n_train // 4)); ctx = min(2000, n_train - qry)
            if ctx < n_classes:
                echo(f"  !! {tag}: n_train={n_train} too small, skip"); continue

            I_tr = align(Xtr_p, ie_I, d_ie); I_te = align(Xte_p, ie_I, d_ie)
            E_tr = align(Xtr_p, ie_E, d_ie); E_te = align(Xte_p, ie_E, d_ie)
            clf = TabICLClassifier(device=DEVICE, n_estimators=1, random_state=SEED, allow_auto_download=True)
            n_init = min(50, n_train)
            init_idx = np.concatenate([np.where(y_tr_int == c)[0][:max(1, n_init // n_classes)]
                                       for c in range(n_classes)])[:n_init]
            if len(init_idx) < n_classes:
                init_idx = np.arange(n_init)
            clf.fit(X_tr_arr[init_idx].astype(np.float32), y_tr_int[init_idx])
            base = clf.model_

            kw = dict(X_tr=X_tr, X_te=X_te, y_tr_t=y_tr_t, ctx=ctx, qry=qry, task_type=ttype,
                      n_classes=n_classes, y_te_int=y_te_int, y_te_cont=y_te_cont,
                      classes=classes, bin_centers=bin_centers)
            cells = {}
            sm_cov = {}
            cells["baseline"] = run_cell(base, [I_tr, E_tr], [I_te, E_te], [d_ie, d_ie], **kw)
            for enc in SMILES_ENCODERS:
                lk, d = sm_lk[enc]
                s_tr = align(Xtr_p, lk, d); s_te = align(Xte_p, lk, d)
                sm_cov[enc] = float((s_te.sum(1) != 0).mean())
                cells[enc] = run_cell(base, [I_tr, E_tr, s_tr], [I_te, E_te, s_te],
                                      [d_ie, d_ie, d], **kw)
            grid[tag] = {"task": task, "phase": phase, "metric": metric_name,
                         "n_train": int(n_train), "n_test": int(len(yte)),
                         "smiles_test_cov": sm_cov, "cells": cells}
            base_v = cells["baseline"]
            deltas = "  ".join(f"{e}:{cells[e]-base_v:+.4f}" for e in SMILES_ENCODERS)
            echo(f"  {tag} [{metric_name}] base={base_v:.4f}  cov={sm_cov.get('molformer',0)*100:.0f}%  {deltas}")
            (out_dir / "grid.json").write_text(json.dumps(grid, indent=2))

    echo(f"\nDone in {time.time()-t0:.0f}s. Saved {out_dir}/grid.json")
    log_f.close()


if __name__ == "__main__":
    main()
