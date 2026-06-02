#!/usr/bin/env python3
"""
full_step2_tabicl_multi.py — Full Step 2 for TabICLv2 with an ARBITRARY number
of virtual feature tokens, one per embedding source.

Aggregates every signal explored in sibling branches into one frozen-TabICL
model:
  - I, E      (Qwen3-Embedding-8B 4096-d, from smiles/IE branch)
  - SMILES    (chosen chem encoder, from smiles branch)
  - all text  (9 TrialBench text columns, Qwen3 4096-d, from All_text_embedding)

Each source → its own Linear(d_i, E=128) projection → 1 virtual feature column,
concatenated between TabICL's col_embedder and row_interactor (same injection
point as branch/smiles|mesh). Base TabICL (27.6M) frozen; only the projections
+ per-column embeddings train.

Token spec (`--virt-embs`, comma-separated):
    <parquet_path>[@TYPE]
  - plain path: a parquet with EITHER wide cols emb_0..emb_{d-1}  (All_text)
                OR a list column `mean_emb`                        (SMILES)
  - path@TYPE : a parquet with a `type` column + `mean_emb`; keep rows where
                type==TYPE (used for I/E: ie_...parquet@I and ...@E)

Unified loader auto-detects the format. Different sources may have different d.

Forked from branch/mesh/script/full_step2_tabicl_mesh.py (injection mechanics)
+ branch/All_text_embedding/script/full_step2_multi.py (N-column design).
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

RESULTS_ROOT = Path("/data2/zhu11/TB/branch/aggregate/results")
DEVICE       = "cuda"


# -------------------------------------------------------------------------
# Unified embedding loader (wide / list / list+type)
# -------------------------------------------------------------------------

def load_token_lookup(spec: str):
    """spec = '<path>' or '<path>@TYPE'. Returns (name, lookup, d) where
    lookup maps (trial_id, phase) -> np.float32 vector (d,)."""
    if "@" in spec:
        path, typ = spec.split("@", 1)
    else:
        path, typ = spec, None
    df = pd.read_parquet(path)
    emb_cols = [c for c in df.columns if c.startswith("emb_")]
    if emb_cols:                                  # wide format (All_text)
        d = len(emb_cols)
        mat = df[emb_cols].to_numpy(dtype=np.float32)
        keys = list(zip(df["trial_id"].astype(str), df["phase"].astype(str)))
        lookup = {k: mat[i] for i, k in enumerate(keys)}
        name = Path(path).stem
    elif "mean_emb" in df.columns:                # list format (SMILES / I-E)
        if typ is not None:
            if "type" not in df.columns:
                raise ValueError(f"{path} has no 'type' column but spec asked @{typ}")
            df = df[df["type"].astype(str) == typ]
        d = len(df.iloc[0]["mean_emb"])
        lookup = {(str(r.trial_id), str(r.phase)): np.asarray(r.mean_emb, dtype=np.float32)
                  for r in df.itertuples(index=False)}
        name = Path(path).stem + (f"@{typ}" if typ else "")
    else:
        raise ValueError(f"{path}: neither emb_* cols nor mean_emb column")
    return name, lookup, d


def align(X_df: pd.DataFrame, lookup: dict, d: int) -> np.ndarray:
    out = np.zeros((len(X_df), d), dtype=np.float32)
    for i, (tid, ph) in enumerate(zip(X_df.index.astype(str), X_df["phase_split"].astype(str))):
        v = lookup.get((tid, ph))
        if v is not None:
            out[i] = v
    return out


# -------------------------------------------------------------------------
# N-column virtual injection for TabICL
# -------------------------------------------------------------------------

class TabICLVirtualMulti(nn.Module):
    def __init__(self, base, emb_dims: list[int]):
        super().__init__()
        self.base = base
        E = base.embed_dim
        self.E = E
        self.n_virt = len(emb_dims)
        self.projs = nn.ModuleList([nn.Linear(d, E, bias=False) for d in emb_dims])
        for p in self.projs:
            nn.init.xavier_uniform_(p.weight)
        self.virt_col_emb = nn.Parameter(torch.zeros(self.n_virt, E))
        nn.init.normal_(self.virt_col_emb, std=0.02)
        for p in self.base.parameters():
            p.requires_grad = False

    def forward(self, X_BTH, y_train_BT, virt_list):
        """virt_list: list of (T, d_i) tensors, one per source. Empty list =>
        zero-shot (tabular only): no virtual columns concatenated."""
        col_out = self.base.col_embedder(X_BTH, y_train=y_train_BT, d=None, embed_with_test=False)
        if virt_list:
            proj_dtype = self.projs[0].weight.dtype
            toks = []
            for i, v in enumerate(virt_list):
                vd = v.to(col_out.device).to(proj_dtype)        # (T, d_i) fp32
                toks.append(self.projs[i](vd) + self.virt_col_emb[i])  # (T, E)
            virt_tne = torch.stack(toks, dim=1).to(col_out.dtype)      # (T, n_virt, E)
            B = col_out.shape[0]
            virt_btne = virt_tne.unsqueeze(0).expand(B, -1, -1, -1).contiguous()
            col_aug = torch.cat([col_out, virt_btne], dim=2)
        else:
            col_aug = col_out
        repr_ = self.base.row_interactor(col_aug, d=None)
        return self.base.icl_predictor(repr_, y_train=y_train_BT)


def _proba(out, n_classes):
    return F.softmax(out[..., :n_classes].float(), dim=-1)


@torch.inference_mode()
def predict_full(wrap, X_tr, y_tr, X_te, virt_tr, virt_te, n_classes):
    X = torch.cat([X_tr, X_te], dim=0).unsqueeze(0).to(DEVICE)
    y = y_tr.float().unsqueeze(0).to(DEVICE)
    virt = [torch.from_numpy(np.concatenate([vt, ve], axis=0)).to(DEVICE)
            for vt, ve in zip(virt_tr, virt_te)]
    out = wrap(X, y, virt)
    return _proba(out, n_classes).cpu().numpy()[0]


def main(args):
    safe_subtask = args.subtask.replace("/", "_")
    safe_target  = args.target.replace("/", "")
    run_id = (f"fs2multi_tabicl_{safe_subtask}_{safe_target}_{args.phase}_"
              f"{args.tag}_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
    run_dir = RESULTS_ROOT / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    log_f = open(run_dir / "log.txt", "w")

    def echo(*parts):
        line = " ".join(str(p) for p in parts)
        print(line); print(line, file=log_f, flush=True)

    specs = [s.strip() for s in args.virt_embs.split(",") if s.strip()]
    echo(f"[run_id] {run_id}")
    echo(f"[subtask] {args.subtask}  [phase] {args.phase}  [tag] {args.tag}  [n_tokens] {len(specs)}")

    # ---- 1. Data ----
    X_tr_df, y_tr = load_split_generic(args.subtask, "train", args.target, [args.phase])
    X_te_df, y_te = load_split_generic(args.subtask, "test",  args.target, [args.phase])
    echo(f"  train={X_tr_df.shape}  test={X_te_df.shape}")

    y_tr_cont = y_te_cont = bin_centers = None
    if args.task_type == "binary":
        y_tr_int = y_tr.astype(int).values; y_te_int = y_te.astype(int).values
        classes, n_classes = [0, 1], 2
    elif args.task_type == "multiclass":
        le = LabelEncoder(); y_tr_int = le.fit_transform(y_tr.values); y_te_int = le.transform(y_te.values)
        classes = le.classes_.tolist(); n_classes = len(classes)
    elif args.task_type == "regression":
        K = args.n_bins
        y_tr_cont = y_tr.values.astype(np.float32); y_te_cont = y_te.values.astype(np.float32)
        edges = np.quantile(y_tr_cont, np.linspace(0, 1, K + 1)); edges[0] -= 1e-6; edges[-1] += 1e-6
        bin_centers = ((edges[:-1] + edges[1:]) / 2).astype(np.float32)
        y_tr_int = np.clip(np.digitize(y_tr_cont, edges) - 1, 0, K - 1)
        y_te_int = np.clip(np.digitize(y_te_cont, edges) - 1, 0, K - 1)
        classes, n_classes = list(range(K)), K
    else:
        raise ValueError(args.task_type)

    X_tr_p, X_te_p = preprocess(X_tr_df, X_te_df)
    sk = build_sklearn_preprocessor(X_tr_p)
    X_tr_arr = sk.fit_transform(X_tr_p); X_te_arr = sk.transform(X_te_p)
    echo(f"  preprocessed: train {X_tr_arr.shape}  test {X_te_arr.shape}")

    # ---- 2. Load + align all token sources ----
    virt_tr, virt_te, emb_dims, names = [], [], [], []
    for spec in specs:
        nm, lookup, d = load_token_lookup(spec)
        vt = align(X_tr_p, lookup, d); ve = align(X_te_p, lookup, d)
        cov = (ve.sum(1) != 0).mean() * 100
        virt_tr.append(vt); virt_te.append(ve); emb_dims.append(d); names.append(nm)
        echo(f"  token[{len(names)-1}] {nm:55} d={d:5}  test cov {cov:.0f}%")

    # ---- 3. Bootstrap TabICL + wrap ----
    echo("Initializing TabICL ...")
    from tabicl import TabICLClassifier
    clf = TabICLClassifier(device=DEVICE, n_estimators=1, random_state=args.seed, allow_auto_download=True)
    n_init = min(50, len(X_tr_arr))
    init_idx = np.concatenate([np.where(y_tr_int == c)[0][:max(1, n_init // n_classes)]
                               for c in range(n_classes)])[:n_init]
    if len(init_idx) < n_classes:
        init_idx = np.arange(n_init)
    clf.fit(X_tr_arr[init_idx].astype(np.float32), y_tr_int[init_idx])
    base = clf.model_
    n_base = sum(p.numel() for p in base.parameters())
    wrap = TabICLVirtualMulti(base, emb_dims).to(DEVICE)
    n_train_params = sum(p.numel() for p in wrap.parameters() if p.requires_grad)
    echo(f"  n_virt={wrap.n_virt}  base={n_base:,}  trainable={n_train_params:,}")

    X_tr_t = torch.from_numpy(X_tr_arr.astype(np.float32))
    X_te_t = torch.from_numpy(X_te_arr.astype(np.float32))
    y_tr_t = torch.from_numpy(y_tr_int.astype(np.int64))

    def _metrics(proba):
        if args.task_type == "binary":
            return metrics_binary(y_te_int, proba)
        if args.task_type == "multiclass":
            return metrics_multiclass([classes[i] for i in y_te_int], proba, classes)
        return metrics_regression(y_te_cont, (proba * bin_centers[None, :]).sum(1))

    echo("\n--- Initial eval ---")
    wrap.eval()
    m0 = _metrics(predict_full(wrap, X_tr_t, y_tr_t, X_te_t, virt_tr, virt_te, n_classes))
    report_one(args.task_type, "initial", m0)

    # ---- 4. Train ----
    opt = torch.optim.AdamW([p for p in wrap.parameters() if p.requires_grad],
                            lr=args.lr, weight_decay=args.weight_decay)
    rng = np.random.RandomState(args.seed)
    n_train = X_tr_t.shape[0]
    history = []; best = {**m0, "epoch": -1}
    echo(f"\n--- Training: {args.epochs} epochs, lr={args.lr}, ctx={args.ctx_size}, qry={args.qry_size} ---")
    t0 = time.time()
    for ep in range(args.epochs):
        wrap.train()
        perm = rng.permutation(n_train)
        ci = perm[:args.ctx_size]; qi = perm[args.ctx_size:args.ctx_size + args.qry_size]
        X_b = torch.cat([X_tr_t[ci], X_tr_t[qi]], dim=0).unsqueeze(0).to(DEVICE)
        y_b = y_tr_t[ci].float().unsqueeze(0).to(DEVICE)
        virt_b = [torch.from_numpy(np.concatenate([vt[ci], vt[qi]], axis=0)).to(DEVICE) for vt in virt_tr]
        tgt = y_tr_t[qi].long().to(DEVICE)
        out = wrap(X_b, y_b, virt_b)
        loss = F.cross_entropy(out[0, :, :n_classes], tgt)
        opt.zero_grad(); loss.backward(); opt.step()
        if (ep + 1) % args.eval_every == 0 or ep == args.epochs - 1:
            wrap.eval()
            with torch.no_grad():
                m = _metrics(predict_full(wrap, X_tr_t, y_tr_t, X_te_t, virt_tr, virt_te, n_classes))
            history.append({"epoch": ep + 1, "train_loss": float(loss.item()), **m})
            mn = {"binary": "ROC-AUC", "multiclass": "macro-F1", "regression": "R²"}[args.task_type]
            pm = primary_metric(args.task_type, m)
            echo(f"  ep {ep+1:3d}/{args.epochs}  loss={loss.item():.4f}  test {mn}={pm:.4f}")
            if pm > primary_metric(args.task_type, best):
                best = {"epoch": ep + 1, **m}
    t_train = time.time() - t0

    summary = {
        "run_id": run_id, "subtask": args.subtask, "target": args.target,
        "task_type": args.task_type, "phase": args.phase, "tag": args.tag,
        "virt_specs": specs, "token_names": names, "emb_dims": emb_dims,
        "n_virtual_cols": len(specs),
        "n_train": int(n_train), "n_test": int(len(y_te)), "n_classes": int(n_classes),
        "n_base_params": int(n_base), "n_trainable_params": int(n_train_params),
        "elapsed_train_s": round(t_train, 1),
        "initial_metrics": m0, "best_metrics": best, "history": history, "args": vars(args),
    }
    (run_dir / "metrics.json").write_text(json.dumps(summary, indent=2))
    pm_name = {"binary": "ROC-AUC", "multiclass": "macro-F1", "regression": "R²"}[args.task_type]
    echo(f"\n=== {pm_name}: initial {primary_metric(args.task_type, m0):.4f} → "
         f"best {primary_metric(args.task_type, best):.4f} (epoch {best['epoch']}) ===")
    echo(f"Saved: {run_dir / 'metrics.json'}")
    log_f.close()


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--virt-embs", required=True, help="comma-sep specs: path or path@TYPE")
    p.add_argument("--tag", default="multi", help="short label for run_id (e.g. ie, text, all)")
    p.add_argument("--subtask", default="serious-adverse-event-forecasting")
    p.add_argument("--target", default="Y/N")
    p.add_argument("--task-type", choices=["binary", "multiclass", "regression"], default="binary")
    p.add_argument("--phase", required=True, choices=["Phase1", "Phase2", "Phase3", "Phase4"])
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
