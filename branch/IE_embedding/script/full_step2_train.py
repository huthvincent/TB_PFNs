#!/usr/bin/env python3
"""
full_step2_train.py — Full Step 2 (virtual feature column injection).

Architecturally inject 2 virtual feature columns into TabPFN:
   - virtual col 1 = projected incl mean-pooled criterion embedding (768→192)
   - virtual col 2 = projected excl mean-pooled criterion embedding (768→192)

Freeze entire TabPFN; train ONLY:
   - 2 × nn.Linear(768, emsize=192)  ←projection layers
   - 2 × nn.Parameter(192)           ←column embeddings for the virtual cols

Pipeline:
   1. Load SAE train/test (uses sae_finetune.load_split)
   2. Preprocess via sklearn ColumnTransformer (numeric impute+scale, cat one-hot)
      — skips TabPFN's own preprocessing because we need to call model.forward
        directly with our own preprocessed tensor.
   3. Aggregate per-trial mean-pooled 768-d incl/excl embeddings (from
      branch/IE_embedding/results/encode_medcpt_*/)
   4. Load pre-fitted TabPFNClassifier just to extract the underlying
      PerFeatureTransformer model + weights (via clf.fit on tiny init data).
   5. Wrap with VirtualInjection: freezes base, adds projections + col embs,
      monkey-patches `add_embeddings` to concat 2 virtual tokens along feature dim.
   6. Custom training loop:
        - Random ctx/qry split from train rows
        - Forward → cross-entropy on qry predictions
        - Update only projection + col emb params
   7. Final eval: ctx = full train, qry = test → ROC-AUC.

NOTE: this is the prototype "Tier C-Lite" — single estimator, no AMP, no DDP,
single fixed-size split per step. It's a working POC to compare against
Step 2-Lite (current best 0.9164 on SAE). If it shows meaningful gain or loss,
we iterate.
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

sys.path.insert(0, str(Path(__file__).parent))
from ablate_ie_features import load_split as load_split_generic  # noqa: E402

warnings.filterwarnings("ignore", category=UserWarning)

CKPT          = "/data2/zhu11/TB/TabPFN/models/tabpfn-v2.5-classifier-v2.5_default.ckpt"
EMB_RUN       = Path("/data2/zhu11/TB/branch/IE_embedding/results/encode_medcpt_20260520_154921")
RESULTS_ROOT  = Path("/data2/zhu11/TB/branch/IE_embedding/results")
EMB_DIM       = 768
DEVICE        = "cuda"


# -------------------------------------------------------------------------
# Data
# -------------------------------------------------------------------------

def mean_pool_per_trial(emb_path: Path) -> dict:
    """Return dict (trial_id, phase) → np.array shape (2, 768) for (incl, excl)
    mean-pooled embeddings. Trials missing one type get a zero vector for it."""
    emb = np.load(emb_path / "embeddings.npy")
    meta = pd.read_parquet(emb_path / "metadata.parquet")
    composite = (meta["trial_id"].astype(str) + "|" +
                 meta["phase"].astype(str) + "|" + meta["type"].astype(str))
    codes, uniques = pd.factorize(composite, sort=True)
    n_groups = len(uniques)

    # GPU scatter-add mean
    e_t = torch.from_numpy(emb.astype(np.float32)).to(DEVICE)
    c_t = torch.from_numpy(codes.astype(np.int64)).to(DEVICE)
    sums = torch.zeros(n_groups, emb.shape[1], device=DEVICE)
    cnts = torch.zeros(n_groups, device=DEVICE)
    sums.index_add_(0, c_t, e_t)
    cnts.index_add_(0, c_t, torch.ones_like(c_t, dtype=torch.float32))
    pooled = (sums / cnts.unsqueeze(1)).cpu().numpy()

    out = {}
    for i, key in enumerate(uniques):
        tid, ph, typ = key.split("|")
        if (tid, ph) not in out:
            out[(tid, ph)] = np.zeros((2, emb.shape[1]), dtype=np.float32)
        out[(tid, ph)][0 if typ == "I" else 1] = pooled[i]
    return out


def align_virt_emb(X_df: pd.DataFrame, pool: dict) -> np.ndarray:
    """Return (n_rows, 2, 768) tensor of virt embeddings aligned to X rows.
    X_df.index must be trial_id; X_df must have 'phase_split' col."""
    out = np.zeros((len(X_df), 2, EMB_DIM), dtype=np.float32)
    for i, (tid, ph) in enumerate(zip(X_df.index.astype(str), X_df["phase_split"].astype(str))):
        if (tid, ph) in pool:
            out[i] = pool[(tid, ph)]
    return out


def build_sklearn_preprocessor(X_train: pd.DataFrame) -> ColumnTransformer:
    # X has already been through sae_finetune.preprocess. Strictly: numeric =
    # is_numeric_dtype, else treat as categorical (covers category/object/string).
    skip = {"phase_split"}
    num_cols = [c for c in X_train.columns
                if c not in skip and pd.api.types.is_numeric_dtype(X_train[c])]
    cat_cols = [c for c in X_train.columns
                if c not in skip and not pd.api.types.is_numeric_dtype(X_train[c])]
    print(f"  num cols: {len(num_cols)}, cat cols: {len(cat_cols)}")
    num_pipe = Pipeline([
        ("imp", SimpleImputer(strategy="median")),
        ("scale", StandardScaler()),
    ])
    cat_pipe = Pipeline([
        ("imp", SimpleImputer(strategy="most_frequent")),
        ("ohe", OneHotEncoder(handle_unknown="ignore", sparse_output=False, max_categories=20)),
    ])
    ct = ColumnTransformer([
        ("num", num_pipe, num_cols),
        ("cat", cat_pipe, cat_cols),
    ], remainder="drop")
    return ct


# -------------------------------------------------------------------------
# Virtual injection wrapper
# -------------------------------------------------------------------------

class VirtualInjection(nn.Module):
    """Wraps a `PerFeatureTransformer`; monkey-patches its `add_embeddings`
    to concat 2 virtual feature columns produced by 2 trainable Linear projections.

    Freezes all base model parameters at init."""

    def __init__(self, base_model: nn.Module, emb_dim: int = 768,
                 unfreeze_decoder: bool = False):
        super().__init__()
        self.base = base_model
        E = base_model.emsize
        self.E = E
        self.proj_incl = nn.Linear(emb_dim, E, bias=False)
        self.proj_excl = nn.Linear(emb_dim, E, bias=False)
        nn.init.xavier_uniform_(self.proj_incl.weight)
        nn.init.xavier_uniform_(self.proj_excl.weight)
        self.virt_col_emb = nn.Parameter(torch.zeros(2, E))
        nn.init.normal_(self.virt_col_emb, std=0.02)

        # Freeze base model
        for p in self.base.parameters():
            p.requires_grad = False

        # Optionally unfreeze the output MLP head (decoder_dict).
        # Cheap (~78K params) but lets the head re-calibrate for the modified
        # target-token representation after virtual tokens are injected.
        if unfreeze_decoder:
            for p in self.base.decoder_dict.parameters():
                p.requires_grad = True

        # Storage for virt embeddings (set per forward)
        self._virt = None

        # Monkey-patch add_embeddings
        self._orig_add_embeddings = base_model.add_embeddings
        base_model.add_embeddings = self._patched_add_embeddings

    def _patched_add_embeddings(self, embedded_x, embedded_y, *args, **kwargs):
        """Inject 2 virtual feature columns into embedded_x AFTER original
        add_embeddings (which adds column positional embeddings).

        embedded_x shape: (b, s, f, e)
        embedded_y shape: (b, s, e)
        """
        ex, ey = self._orig_add_embeddings(embedded_x, embedded_y, *args, **kwargs)
        v = self._virt
        if v is None:
            return ex, ey
        # v shape: (s, 2, 768)  — same row order as embedded_x's s dim
        b, s, _, e = ex.shape
        assert v.shape[0] == s, f"virt seq len {v.shape[0]} != embedded seq len {s}"

        v_dev = v.to(ex.device).to(ex.dtype)
        incl_se = self.proj_incl(v_dev[:, 0, :]) + self.virt_col_emb[0]  # (s, e)
        excl_se = self.proj_excl(v_dev[:, 1, :]) + self.virt_col_emb[1]  # (s, e)
        # Expand to (b, s, 1, e) and concat along feature dim
        virt_bs2e = torch.stack([incl_se, excl_se], dim=1)  # (s, 2, e)
        virt_bs2e = virt_bs2e.unsqueeze(0).expand(b, -1, -1, -1).contiguous()  # (b, s, 2, e)
        ex_aug = torch.cat([ex, virt_bs2e], dim=2)
        return ex_aug, ey

    def forward(self, x_main_sBC, y_main_sB, virt_sB2_768, perf_opts=None):
        """Run the model with virt injection.

        Args:
            x_main_sBC: (s, B, C) features, both ctx and qry rows
            y_main_sB:  (s_ctx, B) labels for ctx only (model predicts the rest)
            virt_sB2_768: (s, B, 2, 768)
            perf_opts: optional PerformanceOptions (for gradient checkpointing during training)
        """
        assert virt_sB2_768.shape[1] == 1, "Only B=1 supported in this POC"
        self._virt = virt_sB2_768[:, 0, :, :]  # (s, 2, 768)
        try:
            kwargs = {}
            if perf_opts is not None:
                kwargs["performance_options"] = perf_opts
            out = self.base({"main": x_main_sBC}, {"main": y_main_sB}, **kwargs)
        finally:
            self._virt = None
        return out


# -------------------------------------------------------------------------
# Training
# -------------------------------------------------------------------------

def metrics_binary(y_true, proba):
    p1 = proba[:, 1]
    return {
        "roc_auc":  float(roc_auc_score(y_true, p1)),
        "pr_auc":   float(average_precision_score(y_true, p1)),
        "log_loss": float(log_loss(y_true, proba)),
        "accuracy": float(accuracy_score(y_true, p1 >= 0.5)),
    }


def metrics_multiclass(y_true, proba, classes):
    pred_int = proba.argmax(axis=1)
    pred_label = np.asarray(classes)[pred_int]
    return {
        "accuracy":    float(accuracy_score(y_true, pred_label)),
        "macro_f1":    float(f1_score(y_true, pred_label, average="macro")),
        "weighted_f1": float(f1_score(y_true, pred_label, average="weighted")),
        "log_loss":    float(log_loss(y_true, proba, labels=list(classes))),
    }


def metrics_regression(y_true, y_pred):
    return {
        "mae":  float(mean_absolute_error(y_true, y_pred)),
        "rmse": float(np.sqrt(mean_squared_error(y_true, y_pred))),
        "r2":   float(r2_score(y_true, y_pred)),
    }


def _logits_from_model_out(out, n_classes=2):
    """TabPFN classifier raw output is (M, B, 10) with up to 10 class slots.
    Slice to the actual n_classes and squeeze batch."""
    if out.dim() == 3:
        if out.shape[1] == 1:  # (M, 1, 10)
            logits = out[:, 0, :n_classes]
        else:  # (1, ?, ?)
            logits = out[0]
            if logits.shape[-1] >= n_classes:
                logits = logits[..., :n_classes]
    else:
        logits = out[..., :n_classes]
    return logits


@torch.inference_mode()
def predict_full(wrap, X_train_t, y_train_t, X_test_t, virt_train, virt_test, n_classes=2):
    """ctx = full train, qry = test."""
    x = torch.cat([X_train_t, X_test_t], dim=0).unsqueeze(1).to(DEVICE)
    y = y_train_t.float().unsqueeze(1).to(DEVICE)
    virt_all = np.concatenate([virt_train, virt_test], axis=0)
    virt = torch.from_numpy(virt_all).unsqueeze(1)  # (s, 1, 2, 768)
    out = wrap(x, y, virt)
    logits = _logits_from_model_out(out, n_classes=n_classes)
    proba = F.softmax(logits.float(), dim=-1).cpu().numpy()
    return proba


def report_one(task_type, name, m):
    if task_type == "binary":
        print(f"[{name}] ROC-AUC={m['roc_auc']:.4f} PR-AUC={m['pr_auc']:.4f} "
              f"LogLoss={m['log_loss']:.4f} Acc={m['accuracy']:.4f}")
    elif task_type == "multiclass":
        print(f"[{name}] Acc={m['accuracy']:.4f} macro-F1={m['macro_f1']:.4f} "
              f"weighted-F1={m['weighted_f1']:.4f} LogLoss={m['log_loss']:.4f}")
    else:  # regression
        print(f"[{name}] MAE={m['mae']:.4f} RMSE={m['rmse']:.4f} R²={m['r2']:.4f}")


def primary_metric(task_type, m):
    if task_type == "binary":
        return m["roc_auc"]
    if task_type == "multiclass":
        return m["macro_f1"]
    return m["r2"]  # regression


def main(args):
    safe_subtask = args.subtask.replace("/", "_")
    safe_target  = args.target.replace("/", "")
    run_id = f"full_step2_{safe_subtask}_{safe_target}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    run_dir = RESULTS_ROOT / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    print(f"[run_id] {run_id}")
    print(f"[run_dir] {run_dir}")
    print(f"[subtask] {args.subtask}  [target] {args.target}  [task-type] {args.task_type}")

    # 1. Load subtask data (parametric)
    phases = [p.strip() for p in args.phases.split(",")] if args.phases else None
    print(f"Loading splits (phases: {phases or 'all 4'}) ...")
    X_train_df, y_train = load_split_generic(args.subtask, "train", args.target, phases)
    X_test_df,  y_test  = load_split_generic(args.subtask, "test",  args.target, phases)

    # Encode labels: binary/multiclass → int; regression → quantile-bin to multiclass + keep continuous
    y_train_continuous = None
    y_test_continuous  = None
    bin_centers        = None
    if args.task_type == "binary":
        y_train_int = y_train.astype(int).values
        y_test_int  = y_test.astype(int).values
        n_classes   = 2
        classes     = [0, 1]
    elif args.task_type == "multiclass":
        le = LabelEncoder()
        y_train_int = le.fit_transform(y_train.values)
        y_test_int  = le.transform(y_test.values)
        classes     = le.classes_.tolist()
        n_classes   = len(classes)
    elif args.task_type == "regression":
        # Quantile binning into K bins. TabPFN classifier head has n_out=10 slots.
        K = args.n_bins
        y_train_continuous = y_train.values.astype(np.float32)
        y_test_continuous  = y_test.values.astype(np.float32)
        bin_edges  = np.quantile(y_train_continuous, np.linspace(0, 1, K + 1))
        bin_edges[0]  -= 1e-6  # ensure min included
        bin_edges[-1] += 1e-6
        bin_centers = ((bin_edges[:-1] + bin_edges[1:]) / 2).astype(np.float32)
        y_train_int = np.clip(np.digitize(y_train_continuous, bin_edges) - 1, 0, K - 1)
        y_test_int  = np.clip(np.digitize(y_test_continuous,  bin_edges) - 1, 0, K - 1)
        classes = list(range(K))
        n_classes = K
        print(f"  quantile bins ({K}): edges={bin_edges.round(1).tolist()}, centers={bin_centers.round(1).tolist()}")
    else:
        raise ValueError(f"Unsupported task_type {args.task_type}")
    print(f"  n_classes={n_classes}, classes preview: {str(classes)[:80]}")

    X_train_p, X_test_p = preprocess(X_train_df, X_test_df)
    print(f"  train={X_train_p.shape}  test={X_test_p.shape}")

    # 2. Sklearn preprocessing (numeric impute+scale, cat one-hot)
    print("Building sklearn preprocessor ...")
    sk = build_sklearn_preprocessor(X_train_p)
    X_train_arr = sk.fit_transform(X_train_p)
    X_test_arr  = sk.transform(X_test_p)
    print(f"  preprocessed: train {X_train_arr.shape}  test {X_test_arr.shape}")

    # 3. Mean-pool embeddings + align
    print("Mean-pooling criterion embeddings ...")
    pool = mean_pool_per_trial(EMB_RUN)
    virt_train = align_virt_emb(X_train_p, pool)
    virt_test  = align_virt_emb(X_test_p,  pool)
    print(f"  virt_train {virt_train.shape}  virt_test {virt_test.shape}")
    print(f"  trials with any non-zero virt: train "
          f"{(virt_train.sum((1,2)) != 0).sum()}/{len(virt_train)}, "
          f"test {(virt_test.sum((1,2)) != 0).sum()}/{len(virt_test)}")

    # 4. Bootstrap TabPFN to get the underlying model with weights loaded
    print(f"Initializing TabPFN from {CKPT} ...")
    from tabpfn import TabPFNClassifier
    clf = TabPFNClassifier(model_path=CKPT, n_estimators=1, device=DEVICE,
                           ignore_pretraining_limits=True, random_state=args.seed)
    # tiny init fit just to populate clf.model_
    init_X = X_train_p.iloc[:10]
    clf.fit(init_X, y_train.values[:10])
    base = clf.model_
    print(f"  underlying model: {type(base).__name__}, emsize={base.emsize}")
    n_base_params = sum(p.numel() for p in base.parameters())
    print(f"  base params: {n_base_params:,}")

    # 5. Wrap + freeze
    wrap = VirtualInjection(base, emb_dim=EMB_DIM,
                            unfreeze_decoder=args.unfreeze_decoder).to(DEVICE)
    trainable_params = [p for p in wrap.parameters() if p.requires_grad]
    n_trainable = sum(p.numel() for p in trainable_params)
    trainable_names = {n.rsplit(".", 1)[0] for n, p in wrap.named_parameters() if p.requires_grad}
    print(f"  trainable params: {n_trainable:,}  (modules: {sorted(trainable_names)[:6]}...)")

    # 6. Tensors on device
    X_train_t = torch.from_numpy(X_train_arr.astype(np.float32))
    X_test_t  = torch.from_numpy(X_test_arr.astype(np.float32))
    y_train_t = torch.from_numpy(y_train_int.astype(np.int64))
    print(f"  X_train_t {X_train_t.shape}  X_test_t {X_test_t.shape}")

    # Helper closures for metric / report (capture task_type + classes)
    def _metrics(y_true_int, proba):
        if args.task_type == "binary":
            return metrics_binary(y_true_int, proba)
        if args.task_type == "multiclass":
            return metrics_multiclass([classes[i] for i in y_true_int], proba, classes)
        # regression: convert proba over bins to continuous prediction via prob-weighted bin centers
        y_pred = (proba * bin_centers[None, :]).sum(axis=1)
        return metrics_regression(y_test_continuous, y_pred)

    # 7. Initial eval (untrained projections)
    print("\n--- Initial eval (random-init projections) ---")
    t0 = time.time()
    proba0 = predict_full(wrap, X_train_t, y_train_t, X_test_t,
                          virt_train, virt_test, n_classes=n_classes)
    m0 = _metrics(y_test_int, proba0)
    t_init = time.time() - t0
    print(f"  predict {t_init:.1f}s")
    report_one(args.task_type, "initial", m0)

    # 8. Training loop
    from tabpfn.architectures.interface import PerformanceOptions
    train_perf_opts = PerformanceOptions(force_recompute_layer=True)
    # Differential learning rates: random-init projections need high lr,
    # pretrained decoder (if unfrozen) needs low lr.
    proj_params = [p for n, p in wrap.named_parameters()
                   if p.requires_grad and not n.startswith("base.")]
    base_params = [p for n, p in wrap.named_parameters()
                   if p.requires_grad and n.startswith("base.")]
    param_groups = [{"params": proj_params, "lr": args.lr}]
    if base_params:
        param_groups.append({"params": base_params, "lr": args.lr_base})
    print(f"\n--- Training: {args.epochs} epochs, lr_proj={args.lr}, lr_base={args.lr_base}, "
          f"ctx_size={args.ctx_size}, qry_size={args.qry_size}, grad_ckpt=True ---")
    print(f"  proj params: {sum(p.numel() for p in proj_params):,}, "
          f"unfrozen base params: {sum(p.numel() for p in base_params):,}")
    opt = torch.optim.AdamW(param_groups, weight_decay=args.weight_decay)
    rng = np.random.RandomState(args.seed)
    n_train = X_train_t.shape[0]

    history = []
    best = {**m0, "epoch": -1}
    t_train_start = time.time()

    for epoch in range(args.epochs):
        wrap.train()
        perm = rng.permutation(n_train)
        ctx_idx = perm[:args.ctx_size]
        qry_idx = perm[args.ctx_size:args.ctx_size + args.qry_size]
        X_ctx = X_train_t[ctx_idx]; y_ctx = y_train_t[ctx_idx]
        X_qry = X_train_t[qry_idx]; y_qry = y_train_t[qry_idx]
        virt_ctx = virt_train[ctx_idx]; virt_qry = virt_train[qry_idx]

        x = torch.cat([X_ctx, X_qry], dim=0).unsqueeze(1).to(DEVICE)
        y = y_ctx.float().unsqueeze(1).to(DEVICE)
        virt = torch.from_numpy(np.concatenate([virt_ctx, virt_qry], axis=0)).unsqueeze(1)

        out = wrap(x, y, virt, perf_opts=train_perf_opts)
        logits = _logits_from_model_out(out, n_classes=n_classes)
        targets = y_qry.long().to(DEVICE)
        loss = F.cross_entropy(logits, targets)

        opt.zero_grad()
        loss.backward()
        opt.step()

        if (epoch + 1) % args.eval_every == 0 or epoch == args.epochs - 1:
            with torch.no_grad():
                proba = predict_full(wrap, X_train_t, y_train_t, X_test_t,
                                     virt_train, virt_test, n_classes=n_classes)
            m = _metrics(y_test_int, proba)
            history.append({"epoch": epoch + 1, "train_loss": float(loss.item()), **m})
            pm = primary_metric(args.task_type, m)
            metric_name = {"binary": "ROC-AUC", "multiclass": "macro-F1", "regression": "R²"}[args.task_type]
            extra = f"  LogLoss={m['log_loss']:.4f}" if args.task_type != "regression" else \
                    f"  MAE={m['mae']:.1f}  RMSE={m['rmse']:.1f}"
            print(f"  ep {epoch+1:3d}/{args.epochs}  train_loss={loss.item():.4f}  "
                  f"test {metric_name}={pm:.4f}{extra}")
            if pm > primary_metric(args.task_type, best):
                best = {"epoch": epoch + 1, **m}

    t_train = time.time() - t_train_start

    # 9. Save
    summary = {
        "run_id": run_id,
        "subtask": args.subtask, "target": args.target, "task_type": args.task_type,
        "n_train": int(n_train),
        "n_test": int(len(y_test)),
        "n_classes": int(n_classes),
        "n_baseline_features": int(X_train_arr.shape[1]),
        "n_virtual_cols": 2,
        "n_base_params": int(n_base_params),
        "n_trainable_params": int(n_trainable),
        "elapsed_train_s": round(t_train, 1),
        "initial_metrics": m0,
        "best_metrics": best,
        "history": history,
        "args": vars(args),
    }
    with (run_dir / "metrics.json").open("w") as f:
        json.dump(summary, f, indent=2)

    pm_name = "ROC-AUC" if args.task_type == "binary" else "macro-F1"
    print("\n=== Summary ===")
    print(f"  Initial   {pm_name}: {primary_metric(args.task_type, m0):.4f}")
    print(f"  Best      {pm_name}: {primary_metric(args.task_type, best):.4f}  (at epoch {best['epoch']})")
    print(f"  Saved: {run_dir / 'metrics.json'}")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--subtask", default="serious-adverse-event-forecasting")
    p.add_argument("--target", default="Y/N")
    p.add_argument("--task-type", choices=["binary", "multiclass", "regression"], default="binary")
    p.add_argument("--phases", default=None,
                   help="Comma-sep subset of Phase1,Phase2,Phase3,Phase4 (default: all 4)")
    p.add_argument("--n-bins", type=int, default=10,
                   help="For task-type=regression: number of quantile bins (max 10 due to TabPFN head)")
    p.add_argument("--epochs", type=int, default=30)
    p.add_argument("--lr", type=float, default=1e-3, help="LR for random-init projection layers")
    p.add_argument("--lr-base", type=float, default=2e-5, help="LR for unfrozen pretrained base modules (decoder etc.)")
    p.add_argument("--weight-decay", type=float, default=1e-4)
    p.add_argument("--ctx-size", type=int, default=2000, help="train context rows per step")
    p.add_argument("--qry-size", type=int, default=500,  help="train query rows per step")
    p.add_argument("--eval-every", type=int, default=2)
    p.add_argument("--unfreeze-decoder", action="store_true",
                   help="Also train the output MLP head (~78K params).")
    p.add_argument("--seed", type=int, default=0)
    args = p.parse_args()
    main(args)
