#!/usr/bin/env python3
"""
mesh_eval_grid.py — Comprehensive MeSH evaluation grid.

Frozen TabICLv2, Full Step 2. Baseline = tabular + I/E (Qwen3-Embedding-8B, 2
virtual tokens). Each MeSH cell adds condition + intervention MeSH as 2 more
virtual tokens (4 total), encoded by one of 5 embedding models. Evaluated across
5 tasks × Phase1-3.

Tasks (target, task-type, primary metric):
  serious-adverse-event-forecasting  Y/N           binary       ROC-AUC
  mortality-event-prediction         Y/N           binary       ROC-AUC
  patient-dropout-event-forecasting  Y/N           binary       ROC-AUC
  trial-duration-forecasting         time_day      regression   R²
  trial-failure-reason-identification failure_reason multiclass  macro-F1

MeSH encoders: sapbert, biolord, medcpt, pubmedbert, qwen3 (data/mesh_embeddings_*.parquet,
rebuilt to cover all 5 tasks). I/E: data/ie_embeddings_qwen3.parquet (covers all trials).

Single seed (no multi-seed / variance) per user request. Metric = mean of last-5
eval-epoch primary metric (a stable single-run point estimate). ctx/qry adapt to
small phases (Phase1).

In-process: I/E + all MeSH lookups loaded ONCE; per (task,phase) bootstrap TabICL
once and evaluate baseline + 5 MeSH cells.

Output: results/mesh_grid_<ts>/grid.json + grid.md (the table for final_readme).
"""

from __future__ import annotations

import json
import sys
import time
from datetime import datetime
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F
from sklearn.preprocessing import LabelEncoder

sys.path.insert(0, "/data2/zhu11/TB/branch/aggregate/script")
from full_step2_tabicl_multi import (  # noqa: E402
    TabICLVirtualMulti, load_token_lookup, align, predict_full,
    build_sklearn_preprocessor, preprocess, load_split_generic,
    metrics_binary, metrics_multiclass, metrics_regression,
)

DEVICE = "cuda"
MESH = Path("/data2/zhu11/TB/branch/mesh/data")
RESULTS_ROOT = Path("/data2/zhu11/TB/branch/mesh/results")

IE_PARQUET = MESH / "ie_embeddings_qwen3.parquet"
MESH_ENCODERS = ["sapbert", "biolord", "medcpt", "pubmedbert", "qwen3"]

TASKS = [
    ("serious-adverse-event-forecasting",   "Y/N",            "binary",      "ROC-AUC"),
    ("mortality-event-prediction",          "Y/N",            "binary",      "ROC-AUC"),
    ("patient-dropout-event-forecasting",   "Y/N",            "binary",      "ROC-AUC"),
    ("trial-duration-forecasting",          "time_day",       "regression",  "R²"),
    ("trial-failure-reason-identification", "failure_reason", "multiclass",  "macro-F1"),
]
PHASES = ["Phase1", "Phase2", "Phase3"]
EPOCHS = 30
SEED = 0
N_BINS = 10


def primary(task_type, m):
    return m["roc_auc"] if task_type == "binary" else m["macro_f1"] if task_type == "multiclass" else m["r2"]


def encode_labels(y_tr, y_te, task_type):
    """Returns (y_tr_int, y_te_int, n_classes, classes, y_te_cont, bin_centers)."""
    if task_type == "binary":
        return y_tr.astype(int).values, y_te.astype(int).values, 2, [0, 1], None, None
    if task_type == "multiclass":
        le = LabelEncoder()
        a = le.fit_transform(y_tr.values)
        # map test labels; unseen -> will error, but TrialBench classes are shared
        b = le.transform(y_te.values)
        return a, b, len(le.classes_), le.classes_.tolist(), None, None
    # regression: quantile-bin
    ytr = y_tr.values.astype(np.float32); yte = y_te.values.astype(np.float32)
    edges = np.quantile(ytr, np.linspace(0, 1, N_BINS + 1)); edges[0] -= 1e-6; edges[-1] += 1e-6
    centers = ((edges[:-1] + edges[1:]) / 2).astype(np.float32)
    a = np.clip(np.digitize(ytr, edges) - 1, 0, N_BINS - 1)
    b = np.clip(np.digitize(yte, edges) - 1, 0, N_BINS - 1)
    return a, b, N_BINS, list(range(N_BINS)), yte, centers


def metric_of(task_type, proba, y_te_int, y_te_cont, classes, bin_centers):
    if task_type == "binary":
        return metrics_binary(y_te_int, proba)
    if task_type == "multiclass":
        return metrics_multiclass([classes[i] for i in y_te_int], proba, classes)
    return metrics_regression(y_te_cont, (proba * bin_centers[None, :]).sum(1))


def run_cell(base, virt_tr, virt_te, emb_dims, X_tr, X_te, y_tr_t, ctx, qry,
             task_type, n_classes, y_te_int, y_te_cont, classes, bin_centers):
    """Train projections for one token subset, return last5 primary metric."""
    wrap = TabICLVirtualMulti(base, emb_dims).to(DEVICE)
    trainable = [p for p in wrap.parameters() if p.requires_grad and p.numel() > 0]
    opt = torch.optim.AdamW(trainable, lr=1e-3, weight_decay=1e-4)
    rng = np.random.RandomState(SEED)
    n_train = X_tr.shape[0]
    hist = []
    for ep in range(EPOCHS):
        wrap.train()
        perm = rng.permutation(n_train)
        ci = perm[:ctx]; qi = perm[ctx:ctx + qry]
        X_b = torch.cat([X_tr[ci], X_tr[qi]], 0).unsqueeze(0).to(DEVICE)
        y_b = y_tr_t[ci].float().unsqueeze(0).to(DEVICE)
        vb = [torch.from_numpy(np.concatenate([vt[ci], vt[qi]], 0)).to(DEVICE) for vt in virt_tr]
        tgt = y_tr_t[qi].long().to(DEVICE)
        out = wrap(X_b, y_b, vb)
        loss = F.cross_entropy(out[0, :, :n_classes], tgt)
        opt.zero_grad(); loss.backward(); opt.step()
        if (ep + 1) % 2 == 0 or ep == EPOCHS - 1:
            wrap.eval()
            with torch.no_grad():
                proba = predict_full(wrap, X_tr, y_tr_t, X_te, virt_tr, virt_te, n_classes)
            m = metric_of(task_type, proba, y_te_int, y_te_cont, classes, bin_centers)
            hist.append(primary(task_type, m))
    del wrap; torch.cuda.empty_cache()
    return float(np.mean(hist[-5:]))


def main():
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = RESULTS_ROOT / f"mesh_grid_{ts}"
    out_dir.mkdir(parents=True, exist_ok=True)
    log_f = open(out_dir / "log.txt", "w")

    def echo(*x):
        line = " ".join(str(z) for z in x); print(line, flush=True); print(line, file=log_f, flush=True)

    echo(f"[mesh_grid] {ts}  tasks={len(TASKS)} phases={PHASES} encoders={MESH_ENCODERS} seed={SEED}")
    t0 = time.time()

    echo("Loading I/E + MeSH lookups once ...")
    _, ie_I, d_ie = load_token_lookup(f"{IE_PARQUET}@I")
    _, ie_E, _ = load_token_lookup(f"{IE_PARQUET}@E")
    mesh_lk = {}
    for enc in MESH_ENCODERS:
        p = MESH / f"mesh_embeddings_{enc}.parquet"
        _, cond, dm = load_token_lookup(f"{p}@condition")
        _, interv, _ = load_token_lookup(f"{p}@intervention")
        mesh_lk[enc] = (cond, interv, dm)
        echo(f"  {enc}: d={dm}  cond_keys={len(cond):,} interv_keys={len(interv):,}")
    echo(f"  I/E d={d_ie}  setup {time.time()-t0:.0f}s")

    grid = {}  # (task, phase) -> {cell: metric}
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
            # adaptive ctx/qry for small phases
            qry = min(500, max(50, n_train // 4))
            ctx = min(2000, n_train - qry)
            if ctx < n_classes:
                echo(f"  !! {tag}: n_train={n_train} too small, skip"); continue
            # align tokens
            I_tr = align(Xtr_p, ie_I, d_ie); I_te = align(Xte_p, ie_I, d_ie)
            E_tr = align(Xtr_p, ie_E, d_ie); E_te = align(Xte_p, ie_E, d_ie)
            # bootstrap base for this task/phase
            clf = TabICLClassifier(device=DEVICE, n_estimators=1, random_state=SEED, allow_auto_download=True)
            n_init = min(50, n_train)
            init_idx = np.concatenate([np.where(y_tr_int == c)[0][:max(1, n_init // n_classes)]
                                       for c in range(n_classes)])[:n_init]
            if len(init_idx) < n_classes:
                init_idx = np.arange(n_init)
            clf.fit(X_tr_arr[init_idx].astype(np.float32), y_tr_int[init_idx])
            base = clf.model_

            cells = {}
            kw = dict(X_tr=X_tr, X_te=X_te, y_tr_t=y_tr_t, ctx=ctx, qry=qry, task_type=ttype,
                      n_classes=n_classes, y_te_int=y_te_int, y_te_cont=y_te_cont,
                      classes=classes, bin_centers=bin_centers)
            cells["baseline"] = run_cell(base, [I_tr, E_tr], [I_te, E_te], [d_ie, d_ie], **kw)
            for enc in MESH_ENCODERS:
                cond, interv, dm = mesh_lk[enc]
                c_tr = align(Xtr_p, cond, dm); c_te = align(Xte_p, cond, dm)
                v_tr = align(Xtr_p, interv, dm); v_te = align(Xte_p, interv, dm)
                cells[enc] = run_cell(base, [I_tr, E_tr, c_tr, v_tr], [I_te, E_te, c_te, v_te],
                                      [d_ie, d_ie, dm, dm], **kw)
            grid[tag] = {"task": task, "phase": phase, "metric": metric_name,
                         "n_train": int(n_train), "n_test": int(len(yte)),
                         "ctx": ctx, "qry": qry, "cells": cells}
            base_v = cells["baseline"]
            deltas = "  ".join(f"{e}:{cells[e]-base_v:+.4f}" for e in MESH_ENCODERS)
            echo(f"  {tag} [{metric_name}] base={base_v:.4f}  {deltas}")
            (out_dir / "grid.json").write_text(json.dumps(grid, indent=2))

    echo(f"\nDone in {time.time()-t0:.0f}s. Saved {out_dir}/grid.json")
    log_f.close()


if __name__ == "__main__":
    main()
