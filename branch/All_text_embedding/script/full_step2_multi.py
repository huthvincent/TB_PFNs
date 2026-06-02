#!/usr/bin/env python3
"""
full_step2_multi.py — Generalized Full Step 2: inject N virtual feature columns
into a frozen TabPFN, one per text-column embedding.

Generalizes branch/IE_embedding/script/full_step2_train.py (which hard-codes 2
virtual columns incl/excl) to an arbitrary list of per-trial embedding parquets.
Each parquet → one virtual token via its own Linear(d_i, 192) projection.

Inputs:
  --virt-embs  comma-separated parquet paths. Each parquet has columns
               trial_id, phase, emb_0..emb_{d-1}. Different parquets may have
               different d.
  --subtask --target --task-type --phases  (same as IE_embedding full_step2_train)

Frozen TabPFN backbone; trains only the N projections + N column embeddings +
decoder head (--unfreeze-decoder). Differential LR: projections 1e-3, decoder 2e-5.

Output: results/<run_id>/metrics.json
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
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    accuracy_score, average_precision_score, f1_score, log_loss,
    mean_absolute_error, mean_squared_error, r2_score, roc_auc_score,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler

sys.path.insert(0, "/data2/zhu11/TB/script")
from sae_finetune import preprocess  # noqa: E402
sys.path.insert(0, "/data2/zhu11/TB/branch/IE_embedding/script")
from ablate_ie_features import load_split as load_split_generic  # noqa: E402

warnings.filterwarnings("ignore", category=UserWarning)

CKPT         = "/data2/zhu11/TB/TabPFN/models/tabpfn-v2.5-classifier-v2.5_default.ckpt"
RESULTS_ROOT = Path("/data2/zhu11/TB/branch/All_text_embedding/results")
DEVICE       = "cuda"


# -------------------------------------------------------------------------
# Virtual embedding parquets
# -------------------------------------------------------------------------

def load_virt_parquet(path: str) -> tuple[dict, int]:
    """Return (lookup dict (trial_id,phase)->np.array, embed_dim)."""
    df = pd.read_parquet(path)
    emb_cols = [c for c in df.columns if c.startswith("emb_")]
    d = len(emb_cols)
    mat = df[emb_cols].to_numpy(dtype=np.float32)
    lookup = {}
    for i, (tid, ph) in enumerate(zip(df["trial_id"].astype(str), df["phase"].astype(str))):
        lookup[(tid, ph)] = mat[i]
    return lookup, d


def align_virt(X_df: pd.DataFrame, lookup: dict, d: int) -> np.ndarray:
    """(n_rows, d) array aligned to X_df rows; missing trials → zero vector."""
    out = np.zeros((len(X_df), d), dtype=np.float32)
    for i, (tid, ph) in enumerate(zip(X_df.index.astype(str),
                                      X_df["phase_split"].astype(str))):
        v = lookup.get((tid, ph))
        if v is not None:
            out[i] = v
    return out


def build_sklearn_preprocessor(X_train: pd.DataFrame) -> ColumnTransformer:
    skip = {"phase_split"}
    num_cols = [c for c in X_train.columns
                if c not in skip and pd.api.types.is_numeric_dtype(X_train[c])]
    cat_cols = [c for c in X_train.columns
                if c not in skip and not pd.api.types.is_numeric_dtype(X_train[c])]
    num_pipe = Pipeline([("imp", SimpleImputer(strategy="median")),
                         ("scale", StandardScaler())])
    cat_pipe = Pipeline([("imp", SimpleImputer(strategy="most_frequent")),
                         ("ohe", OneHotEncoder(handle_unknown="ignore",
                                               sparse_output=False, max_categories=20))])
    return ColumnTransformer([("num", num_pipe, num_cols),
                              ("cat", cat_pipe, cat_cols)], remainder="drop")


# -------------------------------------------------------------------------
# Metrics
# -------------------------------------------------------------------------

def metrics_binary(y_true, proba):
    p1 = proba[:, 1]
    return {"roc_auc": float(roc_auc_score(y_true, p1)),
            "pr_auc": float(average_precision_score(y_true, p1)),
            "log_loss": float(log_loss(y_true, proba)),
            "accuracy": float(accuracy_score(y_true, p1 >= 0.5))}


def metrics_multiclass(y_true, proba, classes):
    pred = np.asarray(classes)[proba.argmax(axis=1)]
    return {"accuracy": float(accuracy_score(y_true, pred)),
            "macro_f1": float(f1_score(y_true, pred, average="macro")),
            "weighted_f1": float(f1_score(y_true, pred, average="weighted")),
            "log_loss": float(log_loss(y_true, proba, labels=list(classes)))}


def metrics_regression(y_true, y_pred):
    return {"mae": float(mean_absolute_error(y_true, y_pred)),
            "rmse": float(np.sqrt(mean_squared_error(y_true, y_pred))),
            "r2": float(r2_score(y_true, y_pred))}


def primary_metric(task_type, m):
    return {"binary": "roc_auc", "multiclass": "macro_f1", "regression": "r2"}[task_type], \
           m[{"binary": "roc_auc", "multiclass": "macro_f1", "regression": "r2"}[task_type]]


# -------------------------------------------------------------------------
# Virtual injection wrapper (N columns)
# -------------------------------------------------------------------------

class VirtualInjectionMulti(nn.Module):
    def __init__(self, base_model, emb_dims: list[int], unfreeze_decoder=False):
        super().__init__()
        self.base = base_model
        E = base_model.emsize
        self.n_virt = len(emb_dims)
        self.projs = nn.ModuleList([nn.Linear(d, E, bias=False) for d in emb_dims])
        for p in self.projs:
            nn.init.xavier_uniform_(p.weight)
        self.virt_col_emb = nn.Parameter(torch.zeros(self.n_virt, E))
        nn.init.normal_(self.virt_col_emb, std=0.02)

        for p in self.base.parameters():
            p.requires_grad = False
        if unfreeze_decoder:
            for p in self.base.decoder_dict.parameters():
                p.requires_grad = True

        self._virt = None  # list of (s, d_i) tensors
        self._orig_add_embeddings = base_model.add_embeddings
        base_model.add_embeddings = self._patched_add_embeddings

    def _patched_add_embeddings(self, embedded_x, embedded_y, *a, **kw):
        ex, ey = self._orig_add_embeddings(embedded_x, embedded_y, *a, **kw)
        if self._virt is None:
            return ex, ey
        b, s, _, e = ex.shape
        toks = []
        for i, v in enumerate(self._virt):           # v: (s, d_i)
            vd = v.to(ex.device).to(ex.dtype)
            toks.append(self.projs[i](vd) + self.virt_col_emb[i])   # (s, e)
        virt = torch.stack(toks, dim=1)              # (s, n_virt, e)
        virt = virt.unsqueeze(0).expand(b, -1, -1, -1).contiguous()
        return torch.cat([ex, virt], dim=2), ey

    def forward(self, x_main_sBC, y_main_sB, virt_list, perf_opts=None):
        self._virt = [v[:, 0, :] for v in virt_list]   # each (s, d_i)
        try:
            kwargs = {"performance_options": perf_opts} if perf_opts is not None else {}
            out = self.base({"main": x_main_sBC}, {"main": y_main_sB}, **kwargs)
        finally:
            self._virt = None
        return out


def _logits(out, n_classes):
    if out.dim() == 3:
        return out[:, 0, :n_classes] if out.shape[1] == 1 else out[0][..., :n_classes]
    return out[..., :n_classes]


@torch.inference_mode()
def predict_full(wrap, X_tr, y_tr, X_te, virt_tr_list, virt_te_list, n_classes):
    x = torch.cat([X_tr, X_te], dim=0).unsqueeze(1).to(DEVICE)
    y = y_tr.float().unsqueeze(1).to(DEVICE)
    virt = [torch.from_numpy(np.concatenate([vt, ve], axis=0)).unsqueeze(1)
            for vt, ve in zip(virt_tr_list, virt_te_list)]
    out = wrap(x, y, virt)
    return F.softmax(_logits(out, n_classes).float(), dim=-1).cpu().numpy()


# -------------------------------------------------------------------------
# Main
# -------------------------------------------------------------------------

def main(args):
    safe = args.subtask.replace("/", "_") + "_" + args.target.replace("/", "")
    run_id = f"fs2multi_{safe}_{args.phases.replace(',','-')}_{datetime.now():%Y%m%d_%H%M%S}"
    run_dir = RESULTS_ROOT / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    print(f"[run_id] {run_id}")
    print(f"[subtask] {args.subtask} [target] {args.target} [task] {args.task_type} [phases] {args.phases}")

    virt_paths = [p.strip() for p in args.virt_embs.split(",")]
    print(f"[virtual columns] {len(virt_paths)}:")
    for p in virt_paths:
        print(f"  - {Path(p).name}")

    phases = [p.strip() for p in args.phases.split(",")]
    X_tr_df, y_tr = load_split_generic(args.subtask, "train", args.target, phases)
    X_te_df, y_te = load_split_generic(args.subtask, "test", args.target, phases)

    bin_centers = y_te_cont = None
    if args.task_type == "binary":
        y_tr_int, y_te_int = y_tr.astype(int).values, y_te.astype(int).values
        classes, n_classes = [0, 1], 2
    elif args.task_type == "multiclass":
        le = LabelEncoder()
        y_tr_int = le.fit_transform(y_tr.values)
        y_te_int = le.transform(y_te.values)
        classes = le.classes_.tolist(); n_classes = len(classes)
    else:  # regression
        K = args.n_bins
        y_tr_cont = y_tr.values.astype(np.float32)
        y_te_cont = y_te.values.astype(np.float32)
        edges = np.quantile(y_tr_cont, np.linspace(0, 1, K + 1))
        edges[0] -= 1e-6; edges[-1] += 1e-6
        bin_centers = ((edges[:-1] + edges[1:]) / 2).astype(np.float32)
        y_tr_int = np.clip(np.digitize(y_tr_cont, edges) - 1, 0, K - 1)
        y_te_int = np.clip(np.digitize(y_te_cont, edges) - 1, 0, K - 1)
        classes, n_classes = list(range(K)), K
    print(f"  train={X_tr_df.shape} test={X_te_df.shape} n_classes={n_classes}")

    X_tr_p, X_te_p = preprocess(X_tr_df, X_te_df)
    sk = build_sklearn_preprocessor(X_tr_p)
    X_tr_arr = sk.fit_transform(X_tr_p)
    X_te_arr = sk.transform(X_te_p)
    print(f"  preprocessed: train {X_tr_arr.shape} test {X_te_arr.shape}")

    # Load + align virtual embeddings
    virt_tr, virt_te, emb_dims = [], [], []
    for p in virt_paths:
        lookup, d = load_virt_parquet(p)
        emb_dims.append(d)
        vt = align_virt(X_tr_p, lookup, d)
        ve = align_virt(X_te_p, lookup, d)
        cov_tr = (vt.sum(1) != 0).mean() * 100
        virt_tr.append(vt); virt_te.append(ve)
        print(f"  {Path(p).name}: d={d}  coverage train {cov_tr:.0f}%")

    # Bootstrap TabPFN
    from tabpfn import TabPFNClassifier
    clf = TabPFNClassifier(model_path=CKPT, n_estimators=1, device=DEVICE,
                           ignore_pretraining_limits=True, random_state=args.seed)
    clf.fit(X_tr_p.iloc[:10], y_tr_int[:10])
    base = clf.model_
    wrap = VirtualInjectionMulti(base, emb_dims, unfreeze_decoder=args.unfreeze_decoder).to(DEVICE)
    n_train_params = sum(p.numel() for p in wrap.parameters() if p.requires_grad)
    print(f"  underlying: {type(base).__name__}  trainable params: {n_train_params:,}")

    X_tr_t = torch.from_numpy(X_tr_arr.astype(np.float32))
    X_te_t = torch.from_numpy(X_te_arr.astype(np.float32))
    y_tr_t = torch.from_numpy(y_tr_int.astype(np.int64))

    def _metrics(proba):
        if args.task_type == "binary":
            return metrics_binary(y_te_int, proba)
        if args.task_type == "multiclass":
            return metrics_multiclass([classes[i] for i in y_te_int], proba, classes)
        return metrics_regression(y_te_cont, (proba * bin_centers[None, :]).sum(1))

    # Initial eval
    proba0 = predict_full(wrap, X_tr_t, y_tr_t, X_te_t, virt_tr, virt_te, n_classes)
    m0 = _metrics(proba0)
    pm_name, pm0 = primary_metric(args.task_type, m0)
    print(f"\n[initial] {pm_name}={pm0:.4f}")

    # Training
    from tabpfn.architectures.interface import PerformanceOptions
    perf = PerformanceOptions(force_recompute_layer=True)
    proj_params = [p for n, p in wrap.named_parameters() if p.requires_grad and not n.startswith("base.")]
    base_params = [p for n, p in wrap.named_parameters() if p.requires_grad and n.startswith("base.")]
    groups = [{"params": proj_params, "lr": args.lr}]
    if base_params:
        groups.append({"params": base_params, "lr": args.lr_base})
    opt = torch.optim.AdamW(groups, weight_decay=args.weight_decay)
    rng = np.random.RandomState(args.seed)
    n_train = X_tr_t.shape[0]
    history, best = [], {"epoch": -1, **m0}
    t0 = time.time()

    for ep in range(args.epochs):
        wrap.train()
        perm = rng.permutation(n_train)
        ci = perm[:args.ctx_size]; qi = perm[args.ctx_size:args.ctx_size + args.qry_size]
        x = torch.cat([X_tr_t[ci], X_tr_t[qi]], dim=0).unsqueeze(1).to(DEVICE)
        y = y_tr_t[ci].float().unsqueeze(1).to(DEVICE)
        virt = [torch.from_numpy(np.concatenate([vt[ci], vt[qi]], 0)).unsqueeze(1)
                for vt in virt_tr]
        out = wrap(x, y, virt, perf_opts=perf)
        loss = F.cross_entropy(_logits(out, n_classes), y_tr_t[qi].long().to(DEVICE))
        opt.zero_grad(); loss.backward(); opt.step()

        if (ep + 1) % args.eval_every == 0 or ep == args.epochs - 1:
            with torch.no_grad():
                proba = predict_full(wrap, X_tr_t, y_tr_t, X_te_t, virt_tr, virt_te, n_classes)
            m = _metrics(proba)
            _, pm = primary_metric(args.task_type, m)
            history.append({"epoch": ep + 1, "train_loss": float(loss.item()), **m})
            print(f"  ep {ep+1:3d}/{args.epochs}  loss={loss.item():.4f}  {pm_name}={pm:.4f}")
            if pm > primary_metric(args.task_type, best)[1]:
                best = {"epoch": ep + 1, **m}

    summary = {
        "run_id": run_id, "subtask": args.subtask, "target": args.target,
        "task_type": args.task_type, "phases": args.phases,
        "virt_embs": virt_paths, "emb_dims": emb_dims, "n_virtual_cols": len(virt_paths),
        "n_train": int(n_train), "n_test": int(len(y_te)), "n_classes": int(n_classes),
        "n_trainable_params": int(n_train_params),
        "elapsed_train_s": round(time.time() - t0, 1),
        "initial_metrics": m0, "best_metrics": best, "history": history,
        "args": vars(args),
    }
    with (run_dir / "metrics.json").open("w") as f:
        json.dump(summary, f, indent=2)
    _, pmb = primary_metric(args.task_type, best)
    print(f"\n=== {pm_name}: initial {pm0:.4f} → best {pmb:.4f} (epoch {best['epoch']}) ===")
    print(f"Saved: {run_dir/'metrics.json'}")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--virt-embs", required=True, help="comma-sep parquet paths")
    p.add_argument("--subtask", required=True)
    p.add_argument("--target", required=True)
    p.add_argument("--task-type", choices=["binary", "multiclass", "regression"], required=True)
    p.add_argument("--phases", default="Phase2")
    p.add_argument("--epochs", type=int, default=30)
    p.add_argument("--lr", type=float, default=1e-3)
    p.add_argument("--lr-base", type=float, default=2e-5)
    p.add_argument("--weight-decay", type=float, default=1e-4)
    p.add_argument("--ctx-size", type=int, default=3000)
    p.add_argument("--qry-size", type=int, default=500)
    p.add_argument("--eval-every", type=int, default=3)
    p.add_argument("--n-bins", type=int, default=10)
    p.add_argument("--unfreeze-decoder", action="store_true")
    p.add_argument("--seed", type=int, default=0)
    args = p.parse_args()
    main(args)
