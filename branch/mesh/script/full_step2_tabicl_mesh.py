#!/usr/bin/env python3
"""
full_step2_tabicl_mesh.py — Full Step 2 virtual feature column injection for
TabICLv2, with 2 or 4 virtual feature columns:

   col 1 = proj_incl(incl_mean)      + col_emb[0]   # Qwen3 I/E (always)
   col 2 = proj_excl(excl_mean)      + col_emb[1]
   col 3 = proj_cond(condition_mean) + col_emb[2]   # MeSH (only with --mesh-emb)
   col 4 = proj_interv(interv_mean)  + col_emb[3]

condition / intervention MeSH are two SEMANTICALLY DISTINCT entity types
(disease vs drug), so they get two separate virtual tokens (like I and E).
d_ie auto-detected from the I/E parquet (Qwen3 = 4096); d_mesh from the MeSH
parquet (all four candidate encoders are 768-d).

Freeze entire TabICL; train ONLY the projections + per-virtual-column embeddings
(2 cols ≈ 1.05M params; 4 cols ≈ 1.10M).

Cell D subset = trials whose INTERVENTION MeSH is non-empty (the lower-coverage,
drug-side signal; condition is ~95% so its subset ≈ full). B' baseline can report
the same subset via --report-subset-mesh.

Forked from branch/smiles/script/full_step2_tabicl_smiles.py.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import warnings
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
from sklearn.preprocessing import LabelEncoder

sys.path.insert(0, "/data2/zhu11/TB/branch/IE_embedding/script")
from full_step2_train import (  # noqa: E402
    build_sklearn_preprocessor,
    metrics_binary, metrics_multiclass, metrics_regression,
    report_one, primary_metric,
)
sys.path.insert(0, "/data2/zhu11/TB/script")
from sae_finetune import preprocess  # noqa: E402
sys.path.insert(0, "/data2/zhu11/TB/branch/IE_embedding/script")
from ablate_ie_features import load_split as load_split_generic  # noqa: E402

warnings.filterwarnings("ignore", category=UserWarning)

DEFAULT_IE_PARQUET = Path("/data2/zhu11/TB/branch/mesh/data/ie_embeddings_qwen3.parquet")
RESULTS_ROOT       = Path("/data2/zhu11/TB/branch/mesh/results")
DEVICE             = "cuda"


# -------------------------------------------------------------------------
# Embedding loaders + aligners
# -------------------------------------------------------------------------

def load_ie_lookup(path: Path):
    df = pd.read_parquet(path)
    d_ie = len(df.iloc[0]["mean_emb"])
    out = {}
    for r in df.itertuples(index=False):
        key = (str(r.trial_id), str(r.phase))
        if key not in out:
            out[key] = np.zeros((2, d_ie), dtype=np.float32)
        out[key][0 if r.type == "I" else 1] = np.asarray(r.mean_emb, dtype=np.float32)
    return out, d_ie


def load_mesh_lookup(path: Path):
    """parquet cols: trial_id, phase, type∈{condition,intervention}, mean_emb.
    Returns {(tid,ph) → (cond_emb, interv_emb)} (zero where a type is missing), d_mesh."""
    df = pd.read_parquet(path)
    d_mesh = len(df.iloc[0]["mean_emb"])
    out = {}
    for r in df.itertuples(index=False):
        key = (str(r.trial_id), str(r.phase))
        if key not in out:
            out[key] = np.zeros((2, d_mesh), dtype=np.float32)
        out[key][0 if r.type == "condition" else 1] = np.asarray(r.mean_emb, dtype=np.float32)
    return out, d_mesh


def align_ie(X_df, ie_lookup, d_ie):
    out = np.zeros((len(X_df), 2, d_ie), dtype=np.float32)
    for i, (tid, ph) in enumerate(zip(X_df.index.astype(str), X_df["phase_split"].astype(str))):
        if (tid, ph) in ie_lookup:
            out[i] = ie_lookup[(tid, ph)]
    return out


def align_mesh(X_df, mesh_lookup, d_mesh):
    """Returns mesh array (n, 2, d_mesh) [condition, intervention], plus per-type
    non-empty masks (has_cond, has_interv)."""
    out = np.zeros((len(X_df), 2, d_mesh), dtype=np.float32)
    has_cond   = np.zeros(len(X_df), dtype=bool)
    has_interv = np.zeros(len(X_df), dtype=bool)
    for i, (tid, ph) in enumerate(zip(X_df.index.astype(str), X_df["phase_split"].astype(str))):
        if (tid, ph) in mesh_lookup:
            vec = mesh_lookup[(tid, ph)]
            out[i] = vec
            has_cond[i]   = bool(np.any(vec[0] != 0))
            has_interv[i] = bool(np.any(vec[1] != 0))
    return out, has_cond, has_interv


# -------------------------------------------------------------------------
# Virtual injection wrapper (2 or 4 columns)
# -------------------------------------------------------------------------

class TabICLVirtualInjection(nn.Module):
    def __init__(self, base, d_ie: int, d_mesh: int | None = None):
        super().__init__()
        self.base = base
        E = base.embed_dim
        self.E = E
        self.use_mesh = d_mesh is not None
        self.n_virt = 4 if self.use_mesh else 2

        self.proj_incl = nn.Linear(d_ie, E, bias=False)
        self.proj_excl = nn.Linear(d_ie, E, bias=False)
        nn.init.xavier_uniform_(self.proj_incl.weight)
        nn.init.xavier_uniform_(self.proj_excl.weight)
        if self.use_mesh:
            self.proj_cond   = nn.Linear(d_mesh, E, bias=False)
            self.proj_interv = nn.Linear(d_mesh, E, bias=False)
            nn.init.xavier_uniform_(self.proj_cond.weight)
            nn.init.xavier_uniform_(self.proj_interv.weight)
        self.virt_col_emb = nn.Parameter(torch.zeros(self.n_virt, E))
        nn.init.normal_(self.virt_col_emb, std=0.02)

        for p in self.base.parameters():
            p.requires_grad = False

    def forward(self, X_BTH, y_train_BT, ie_T2_d, mesh_T2_d=None):
        col_out = self.base.col_embedder(X_BTH, y_train=y_train_BT, d=None, embed_with_test=False)
        proj_dtype = self.proj_incl.weight.dtype
        v_ie = ie_T2_d.to(col_out.device).to(proj_dtype)
        cols = [self.proj_incl(v_ie[:, 0, :]) + self.virt_col_emb[0],
                self.proj_excl(v_ie[:, 1, :]) + self.virt_col_emb[1]]
        if self.use_mesh:
            assert mesh_T2_d is not None
            v_m = mesh_T2_d.to(col_out.device).to(proj_dtype)
            cols.append(self.proj_cond(v_m[:, 0, :])   + self.virt_col_emb[2])
            cols.append(self.proj_interv(v_m[:, 1, :]) + self.virt_col_emb[3])
        virt_tne = torch.stack(cols, dim=1).to(col_out.dtype)  # (T, n_virt, E)
        B = col_out.shape[0]
        virt_btne = virt_tne.unsqueeze(0).expand(B, -1, -1, -1).contiguous()
        col_aug = torch.cat([col_out, virt_btne], dim=2)
        repr_ = self.base.row_interactor(col_aug, d=None)
        return self.base.icl_predictor(repr_, y_train=y_train_BT)


def _proba(out, n_classes):
    return F.softmax(out[..., :n_classes].float(), dim=-1)


@torch.inference_mode()
def predict_full(wrap, X_train_t, y_train_t, X_test_t, ie_train, ie_test,
                 mesh_train, mesh_test, n_classes):
    X = torch.cat([X_train_t, X_test_t], dim=0).unsqueeze(0).to(DEVICE)
    y = y_train_t.float().unsqueeze(0).to(DEVICE)
    ie_all = torch.from_numpy(np.concatenate([ie_train, ie_test], axis=0)).to(DEVICE)
    mesh_all = None
    if wrap.use_mesh:
        mesh_all = torch.from_numpy(np.concatenate([mesh_train, mesh_test], axis=0)).to(DEVICE)
    out = wrap(X, y, ie_all, mesh_all)
    return _proba(out, n_classes).cpu().numpy()[0]


def main(args):
    safe_subtask = args.subtask.replace("/", "_")
    safe_target  = args.target.replace("/", "")
    mesh_short = "no_mesh"
    if args.mesh_emb:
        mesh_short = Path(args.mesh_emb).stem.replace("mesh_embeddings_", "mesh_")
    tag = f"{safe_subtask}_{safe_target}_{args.phase}_{mesh_short}"
    run_id = f"full_step2_tabicl_mesh_{tag}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    run_dir = RESULTS_ROOT / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    log_f = open(run_dir / "log.txt", "w")

    def echo(*parts):
        line = " ".join(str(p) for p in parts)
        print(line); print(line, file=log_f, flush=True)

    echo(f"[run_id] {run_id}")
    echo(f"[subtask] {args.subtask}  [phase] {args.phase}  [ie] {args.ie_emb}  [mesh] {args.mesh_emb}")

    # ---- 1. Data ----
    X_train_df, y_train = load_split_generic(args.subtask, "train", args.target, [args.phase])
    X_test_df,  y_test  = load_split_generic(args.subtask, "test",  args.target, [args.phase])
    echo(f"  train={X_train_df.shape}  test={X_test_df.shape}")

    y_train_continuous = y_test_continuous = bin_centers = None
    if args.task_type == "binary":
        y_train_int = y_train.astype(int).values; y_test_int = y_test.astype(int).values
        n_classes = 2; classes = [0, 1]
    elif args.task_type == "multiclass":
        le = LabelEncoder()
        y_train_int = le.fit_transform(y_train.values); y_test_int = le.transform(y_test.values)
        classes = le.classes_.tolist(); n_classes = len(classes)
    elif args.task_type == "regression":
        K = args.n_bins
        y_train_continuous = y_train.values.astype(np.float32)
        y_test_continuous  = y_test.values.astype(np.float32)
        edges = np.quantile(y_train_continuous, np.linspace(0, 1, K + 1))
        edges[0] -= 1e-6; edges[-1] += 1e-6
        bin_centers = ((edges[:-1] + edges[1:]) / 2).astype(np.float32)
        y_train_int = np.clip(np.digitize(y_train_continuous, edges) - 1, 0, K - 1)
        y_test_int  = np.clip(np.digitize(y_test_continuous,  edges) - 1, 0, K - 1)
        classes = list(range(K)); n_classes = K
    else:
        raise ValueError(args.task_type)

    X_train_p, X_test_p = preprocess(X_train_df, X_test_df)
    sk = build_sklearn_preprocessor(X_train_p)
    X_train_arr = sk.fit_transform(X_train_p); X_test_arr = sk.transform(X_test_p)
    echo(f"  preprocessed: train {X_train_arr.shape}  test {X_test_arr.shape}")

    # ---- 2. I/E ----
    ie_lookup, d_ie = load_ie_lookup(Path(args.ie_emb))
    ie_train = align_ie(X_train_p, ie_lookup, d_ie)
    ie_test  = align_ie(X_test_p,  ie_lookup, d_ie)
    echo(f"  I/E d={d_ie}  non-zero test {int((ie_test.sum((1,2))!=0).sum())}/{len(ie_test)}")

    # ---- 2b. MeSH (optional) ----
    d_mesh = None; mesh_train = mesh_test = None
    has_interv_test = np.zeros(len(X_test_p), dtype=bool)
    if args.mesh_emb:
        mesh_lookup, d_mesh = load_mesh_lookup(Path(args.mesh_emb))
        mesh_train, hc_tr, hi_tr = align_mesh(X_train_p, mesh_lookup, d_mesh)
        mesh_test,  hc_te, hi_te = align_mesh(X_test_p,  mesh_lookup, d_mesh)
        has_interv_test = hi_te
        echo(f"  MeSH d={d_mesh}  test condition non-empty {hc_te.sum()}/{len(hc_te)}  "
             f"intervention non-empty {hi_te.sum()}/{len(hi_te)}")
    elif args.report_subset_mesh:
        _lookup, _d = load_mesh_lookup(Path(args.report_subset_mesh))
        _, _hc, has_interv_test = align_mesh(X_test_p, _lookup, _d)
        echo(f"  [report-subset only] intervention-non-empty test subset: "
             f"{has_interv_test.sum()}/{len(has_interv_test)}")

    report_subset = bool(args.mesh_emb or args.report_subset_mesh)

    # ---- 3. Bootstrap TabICL ----
    echo("Initializing TabICL ...")
    from tabicl import TabICLClassifier
    clf = TabICLClassifier(device=DEVICE, n_estimators=1, random_state=args.seed, allow_auto_download=True)
    n_init = min(50, len(X_train_arr))
    init_idx = np.concatenate([np.where(y_train_int == c)[0][:max(1, n_init // n_classes)]
                               for c in range(n_classes)])[:n_init]
    if len(init_idx) < n_classes:
        init_idx = np.arange(n_init)
    clf.fit(X_train_arr[init_idx].astype(np.float32), y_train_int[init_idx])
    base = clf.model_
    n_base_params = sum(p.numel() for p in base.parameters())

    wrap = TabICLVirtualInjection(base, d_ie=d_ie, d_mesh=d_mesh).to(DEVICE)
    n_trainable = sum(p.numel() for p in wrap.parameters() if p.requires_grad)
    echo(f"  n_virt_cols={wrap.n_virt}  trainable params: {n_trainable:,}")

    X_train_t = torch.from_numpy(X_train_arr.astype(np.float32))
    X_test_t  = torch.from_numpy(X_test_arr.astype(np.float32))
    y_train_t = torch.from_numpy(y_train_int.astype(np.int64))

    def _metrics_full(proba):
        if args.task_type == "binary":
            return metrics_binary(y_test_int, proba)
        if args.task_type == "multiclass":
            return metrics_multiclass([classes[i] for i in y_test_int], proba, classes)
        return metrics_regression(y_test_continuous, (proba * bin_centers[None, :]).sum(axis=1))

    def _metrics_subset(proba, mask):
        if not mask.any():
            return None
        if args.task_type == "binary":
            return metrics_binary(y_test_int[mask], proba[mask])
        if args.task_type == "multiclass":
            return metrics_multiclass([classes[i] for i in y_test_int[mask]], proba[mask], classes)
        yp = (proba * bin_centers[None, :]).sum(axis=1)
        return metrics_regression(y_test_continuous[mask], yp[mask])

    # ---- Initial eval ----
    echo("\n--- Initial eval ---")
    wrap.eval()
    proba0 = predict_full(wrap, X_train_t, y_train_t, X_test_t, ie_train, ie_test,
                          mesh_train, mesh_test, n_classes)
    m0 = _metrics_full(proba0)
    m0_subset = _metrics_subset(proba0, has_interv_test) if report_subset else None
    report_one(args.task_type, "initial-full", m0)
    if m0_subset is not None:
        report_one(args.task_type, "initial-interv-subset", m0_subset)

    # ---- Train ----
    opt = torch.optim.AdamW([p for p in wrap.parameters() if p.requires_grad],
                            lr=args.lr, weight_decay=args.weight_decay)
    rng = np.random.RandomState(args.seed)
    n_train = X_train_t.shape[0]
    history = []
    best = {**m0, "epoch": -1}
    best_subset = {**m0_subset, "epoch": -1} if m0_subset is not None else None
    echo(f"\n--- Training: {args.epochs} epochs, lr={args.lr}, ctx={args.ctx_size}, qry={args.qry_size} ---")
    t0 = time.time()
    for epoch in range(args.epochs):
        wrap.train()
        perm = rng.permutation(n_train)
        ci = perm[:args.ctx_size]; qi = perm[args.ctx_size:args.ctx_size + args.qry_size]
        X_b  = torch.cat([X_train_t[ci], X_train_t[qi]], dim=0).unsqueeze(0).to(DEVICE)
        y_b  = y_train_t[ci].float().unsqueeze(0).to(DEVICE)
        ie_b = torch.from_numpy(np.concatenate([ie_train[ci], ie_train[qi]], axis=0)).to(DEVICE)
        mesh_b = (torch.from_numpy(np.concatenate([mesh_train[ci], mesh_train[qi]], axis=0)).to(DEVICE)
                  if args.mesh_emb else None)
        targets = y_train_t[qi].long().to(DEVICE)

        out = wrap(X_b, y_b, ie_b, mesh_b)
        loss = F.cross_entropy(out[0, :, :n_classes], targets)
        opt.zero_grad(); loss.backward(); opt.step()

        if (epoch + 1) % args.eval_every == 0 or epoch == args.epochs - 1:
            wrap.eval()
            with torch.no_grad():
                proba = predict_full(wrap, X_train_t, y_train_t, X_test_t, ie_train, ie_test,
                                     mesh_train, mesh_test, n_classes)
            m = _metrics_full(proba)
            m_sub = _metrics_subset(proba, has_interv_test) if report_subset else None
            entry = {"epoch": epoch + 1, "train_loss": float(loss.item()), **m}
            if m_sub is not None:
                entry["subset"] = m_sub
            history.append(entry)
            mn = {"binary": "ROC-AUC", "multiclass": "macro-F1", "regression": "R²"}[args.task_type]
            pm = primary_metric(args.task_type, m)
            extra = (f"  | subset={primary_metric(args.task_type, m_sub):.4f}" if m_sub else "")
            echo(f"  ep {epoch+1:3d}/{args.epochs}  loss={loss.item():.4f}  test {mn}={pm:.4f}{extra}")
            if pm > primary_metric(args.task_type, best):
                best = {"epoch": epoch + 1, **m}
            if m_sub is not None and primary_metric(args.task_type, m_sub) > primary_metric(args.task_type, best_subset):
                best_subset = {"epoch": epoch + 1, **m_sub}
    t_train = time.time() - t0

    summary = {
        "run_id": run_id, "subtask": args.subtask, "target": args.target,
        "task_type": args.task_type, "phase": args.phase,
        "n_train": int(n_train), "n_test": int(len(y_test)), "n_classes": int(n_classes),
        "n_baseline_features": int(X_train_arr.shape[1]),
        "n_virtual_cols": int(wrap.n_virt), "d_ie": int(d_ie),
        "d_mesh": (int(d_mesh) if d_mesh else None),
        "ie_emb_path": str(args.ie_emb), "mesh_emb_path": (str(args.mesh_emb) if args.mesh_emb else None),
        "interv_test_subset_size": int(has_interv_test.sum()) if report_subset else None,
        "interv_test_subset_frac": float(has_interv_test.mean()) if report_subset else None,
        "n_base_params": int(n_base_params), "n_trainable_params": int(n_trainable),
        "elapsed_train_s": round(t_train, 1),
        "initial_metrics": m0, "initial_metrics_subset": m0_subset,
        "best_metrics": best, "best_metrics_subset": best_subset,
        "history": history, "args": vars(args),
    }
    (run_dir / "metrics.json").write_text(json.dumps(summary, indent=2))
    pm_name = {"binary": "ROC-AUC", "multiclass": "macro-F1", "regression": "R²"}[args.task_type]
    echo("\n=== Summary ===")
    echo(f"  Initial  {pm_name}: {primary_metric(args.task_type, m0):.4f}")
    echo(f"  Best     {pm_name}: {primary_metric(args.task_type, best):.4f}  (epoch {best['epoch']})")
    if best_subset is not None:
        echo(f"  Best (interv subset, n={int(has_interv_test.sum())})  "
             f"{pm_name}: {primary_metric(args.task_type, best_subset):.4f}  (epoch {best_subset['epoch']})")
    echo(f"  Saved: {run_dir / 'metrics.json'}")
    log_f.close()


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--subtask", default="serious-adverse-event-forecasting")
    p.add_argument("--target", default="Y/N")
    p.add_argument("--task-type", choices=["binary", "multiclass", "regression"], default="binary")
    p.add_argument("--phase", required=True, choices=["Phase1", "Phase2", "Phase3", "Phase4"])
    p.add_argument("--ie-emb", default=str(DEFAULT_IE_PARQUET))
    p.add_argument("--mesh-emb", default=None,
                   help="MeSH embedding parquet (cols: trial_id,phase,type,mean_emb). Omit for Cell B'.")
    p.add_argument("--report-subset-mesh", default=None,
                   help="For Cell B': a MeSH parquet used ONLY to define the intervention-non-empty "
                        "test subset for reporting (no MeSH token injected).")
    p.add_argument("--n-bins", type=int, default=10)
    p.add_argument("--epochs", type=int, default=30)
    p.add_argument("--lr", type=float, default=1e-3)
    p.add_argument("--weight-decay", type=float, default=1e-4)
    p.add_argument("--ctx-size", type=int, default=2000)
    p.add_argument("--qry-size", type=int, default=500)
    p.add_argument("--eval-every", type=int, default=2)
    p.add_argument("--seed", type=int, default=0)
    args = p.parse_args()
    main(args)
