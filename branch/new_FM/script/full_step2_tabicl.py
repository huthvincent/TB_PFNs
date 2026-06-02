#!/usr/bin/env python3
"""
full_step2_tabicl.py — Full Step 2 (virtual feature column injection) for **TabICLv2**.

Architecturally inject 2 virtual feature columns into TabICL:
   - virtual col 1 = projected incl mean-pooled criterion embedding (768→E)
   - virtual col 2 = projected excl mean-pooled criterion embedding (768→E)

where E = TabICL's `embed_dim` (default 128).

Freeze entire TabICL; train ONLY:
   - 2 × nn.Linear(768, E)
   - 2 × nn.Parameter(E)   ← virtual column embeddings

Injection point: between `col_embedder` and `row_interactor` in TabICL's forward.
`col_embedder(X, y_train)` returns shape (B, T, G+C, E) where G is feature
groups and C is reserve CLS tokens. We concat 2 virtual columns to get
(B, T, G+C+2, E), then call `row_interactor` and `icl_predictor` as usual.

Mirrors `/data2/zhu11/TB/branch/IE_embedding/script/full_step2_train.py` (TabPFN
version). Reuses its data-loading and preprocessing utilities verbatim.
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
from sklearn.metrics import (
    accuracy_score, average_precision_score, f1_score, log_loss,
    mean_absolute_error, mean_squared_error, r2_score, roc_auc_score,
)
from sklearn.preprocessing import LabelEncoder

# Reuse TabPFN Full Step 2 plumbing.
sys.path.insert(0, "/data2/zhu11/TB/branch/IE_embedding/script")
from full_step2_train import (  # noqa: E402
    mean_pool_per_trial, align_virt_emb, build_sklearn_preprocessor,
    metrics_binary, metrics_multiclass, metrics_regression,
    report_one, primary_metric, EMB_RUN, EMB_DIM,
)
sys.path.insert(0, "/data2/zhu11/TB/script")
from sae_finetune import preprocess  # noqa: E402
sys.path.insert(0, "/data2/zhu11/TB/branch/IE_embedding/script")
from ablate_ie_features import load_split as load_split_generic  # noqa: E402

warnings.filterwarnings("ignore", category=UserWarning)

RESULTS_ROOT = Path("/data2/zhu11/TB/branch/new_FM/results")
DEVICE       = "cuda"


# -------------------------------------------------------------------------
# Virtual injection wrapper for TabICL
# -------------------------------------------------------------------------

class TabICLVirtualInjection(nn.Module):
    """Wraps a TabICL nn.Module. Freezes base. Adds 2 trainable Linear projections
    (768→E) + 2 trainable column embeddings (E,) that get injected as virtual
    feature columns between `col_embedder` and `row_interactor`.

    The trick: we bypass the normal TabICLClassifier inference path (which does
    ensembling/shuffling) and call the base TabICL submodules directly.
    """

    def __init__(self, base, emb_dim: int = 768):
        super().__init__()
        self.base = base
        E = base.embed_dim
        self.E = E
        self.proj_incl = nn.Linear(emb_dim, E, bias=False)
        self.proj_excl = nn.Linear(emb_dim, E, bias=False)
        nn.init.xavier_uniform_(self.proj_incl.weight)
        nn.init.xavier_uniform_(self.proj_excl.weight)
        self.virt_col_emb = nn.Parameter(torch.zeros(2, E))
        nn.init.normal_(self.virt_col_emb, std=0.02)

        # Freeze base model.
        for p in self.base.parameters():
            p.requires_grad = False

    def forward(self, X_BTH, y_train_BT, virt_T2_768):
        """One forward pass.

        Args:
            X_BTH         : (B=1, T, H) raw feature tensor (already preprocessed)
            y_train_BT    : (B=1, train_size) — training labels for ICL context
            virt_T2_768   : (T, 2, 768) — I-mean and E-mean per row, aligned with X_BTH's T axis

        Returns:
            preds: (B, test_size, out_dim) — same as TabICL._inference_forward
                  but with virtual cols injected.
        """
        # 1. Run col_embedder normally → (B, T, G+C, E).
        # In *training* mode this calls _train_forward; in *eval* mode it
        # calls _inference_forward. Both go through the same forward(...) public API.
        col_out = self.base.col_embedder(
            X_BTH, y_train=y_train_BT, d=None, embed_with_test=False,
        )  # (B, T, G+C, E)
        # 2. Build 2 virtual column embeddings.
        # TabICL runs base in fp16/AMP; keep proj in fp32 for stability then cast
        # the result back to col_out.dtype before concat.
        proj_dtype = self.proj_incl.weight.dtype
        v_in = virt_T2_768.to(col_out.device).to(proj_dtype)  # (T, 2, 768) in fp32
        incl_te = self.proj_incl(v_in[:, 0, :]) + self.virt_col_emb[0]  # (T, E)
        excl_te = self.proj_excl(v_in[:, 1, :]) + self.virt_col_emb[1]  # (T, E)
        virt_t2e = torch.stack([incl_te, excl_te], dim=1).to(col_out.dtype)  # (T, 2, E)
        B = col_out.shape[0]
        virt_bt2e = virt_t2e.unsqueeze(0).expand(B, -1, -1, -1).contiguous()  # (B, T, 2, E)
        # 3. Concat along the column dim → (B, T, G+C+2, E)
        col_aug = torch.cat([col_out, virt_bt2e], dim=2)
        # 4. row_interactor + icl_predictor (no `d` because we have a single dataset)
        repr_ = self.base.row_interactor(col_aug, d=None)
        out = self.base.icl_predictor(repr_, y_train=y_train_BT)
        return out


# -------------------------------------------------------------------------
# Training / driver
# -------------------------------------------------------------------------

def _proba_from_logits(out: torch.Tensor, n_classes: int) -> torch.Tensor:
    """TabICL classifier output: (B, test_size, max_classes). Slice to actual n_classes."""
    return F.softmax(out[..., :n_classes].float(), dim=-1)


@torch.inference_mode()
def predict_full(wrap, X_train_t, y_train_t, X_test_t, virt_train, virt_test, n_classes):
    """ctx = full train, qry = test. B=1.

    TabICL expects (B, T, H) with the FIRST train_size positions being train;
    train_size is inferred from y_train.shape[1].
    """
    X = torch.cat([X_train_t, X_test_t], dim=0).unsqueeze(0).to(DEVICE)         # (1, T, H)
    y = y_train_t.float().unsqueeze(0).to(DEVICE)                                # (1, train_size)
    virt_all = torch.from_numpy(np.concatenate([virt_train, virt_test], axis=0)).to(DEVICE)  # (T, 2, 768)
    out = wrap(X, y, virt_all)  # (B, test_size, ...)
    proba = _proba_from_logits(out, n_classes).cpu().numpy()
    return proba[0]  # (test_size, n_classes)


def main(args):
    safe_subtask = args.subtask.replace("/", "_")
    safe_target  = args.target.replace("/", "")
    run_id = f"full_step2_tabicl_{safe_subtask}_{safe_target}_{args.phase}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    run_dir = RESULTS_ROOT / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    log_path = run_dir / "log.txt"
    log_f = open(log_path, "w")

    def echo(*parts):
        line = " ".join(str(p) for p in parts)
        print(line)
        print(line, file=log_f, flush=True)

    echo(f"[run_id] {run_id}")
    echo(f"[subtask] {args.subtask}  [target] {args.target}  [task-type] {args.task_type}  [phase] {args.phase}")

    # ---- 1. Load + preprocess subtask data ----
    X_train_df, y_train = load_split_generic(args.subtask, "train", args.target, [args.phase])
    X_test_df,  y_test  = load_split_generic(args.subtask, "test",  args.target, [args.phase])
    echo(f"  train={X_train_df.shape}  test={X_test_df.shape}")

    # Label encoding (TabICL handles ints fine; for multiclass + regression we
    # quantile-bin like the TabPFN script).
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
        K = args.n_bins
        y_train_continuous = y_train.values.astype(np.float32)
        y_test_continuous  = y_test.values.astype(np.float32)
        bin_edges  = np.quantile(y_train_continuous, np.linspace(0, 1, K + 1))
        bin_edges[0]  -= 1e-6
        bin_edges[-1] += 1e-6
        bin_centers = ((bin_edges[:-1] + bin_edges[1:]) / 2).astype(np.float32)
        y_train_int = np.clip(np.digitize(y_train_continuous, bin_edges) - 1, 0, K - 1)
        y_test_int  = np.clip(np.digitize(y_test_continuous,  bin_edges) - 1, 0, K - 1)
        classes = list(range(K))
        n_classes = K
        echo(f"  quantile bins ({K}): centers={bin_centers.round(1).tolist()}")
    else:
        raise ValueError(args.task_type)

    X_train_p, X_test_p = preprocess(X_train_df, X_test_df)
    echo(f"  after preprocess: train {X_train_p.shape}  test {X_test_p.shape}")

    # Sklearn preprocessing (numeric impute+scale, cat one-hot) — same as TabPFN script
    sk = build_sklearn_preprocessor(X_train_p)
    X_train_arr = sk.fit_transform(X_train_p)
    X_test_arr  = sk.transform(X_test_p)
    echo(f"  preprocessed: train {X_train_arr.shape}  test {X_test_arr.shape}")

    # ---- 2. Mean-pool IE embeddings + align ----
    pool = mean_pool_per_trial(EMB_RUN)
    virt_train = align_virt_emb(X_train_p, pool)
    virt_test  = align_virt_emb(X_test_p,  pool)
    echo(f"  virt_train {virt_train.shape}  virt_test {virt_test.shape}")
    echo(f"  trials with any non-zero virt: train "
         f"{(virt_train.sum((1,2)) != 0).sum()}/{len(virt_train)}, "
         f"test {(virt_test.sum((1,2)) != 0).sum()}/{len(virt_test)}")

    # ---- 3. Bootstrap TabICLClassifier to populate model_ ----
    echo("Initializing TabICL ...")
    from tabicl import TabICLClassifier
    # max_classes is read from the checkpoint config; for 4-class multiclass and
    # for our regression-by-binning (n_bins=K), we may need K classes <= model
    # max. TabICL v2 default max_classes is 10 — OK for K up to 10.
    clf = TabICLClassifier(
        device=DEVICE, n_estimators=1, random_state=args.seed, allow_auto_download=True,
    )
    # tiny init fit to populate clf.model_ (real weights, then we own forward path)
    n_init = min(50, len(X_train_arr))
    # Make sure all classes seen so model_ is fit appropriately
    init_idx = np.concatenate([np.where(y_train_int == c)[0][:max(1, n_init // n_classes)]
                               for c in range(n_classes)])[:n_init]
    if len(init_idx) < n_classes:
        init_idx = np.arange(n_init)
    clf.fit(X_train_arr[init_idx].astype(np.float32), y_train_int[init_idx])
    base = clf.model_
    echo(f"  underlying TabICL: embed_dim={base.embed_dim}, "
         f"col blocks={base.col_num_blocks}, row blocks={base.row_num_blocks}, "
         f"icl blocks={base.icl_num_blocks}")
    n_base_params = sum(p.numel() for p in base.parameters())
    echo(f"  base params: {n_base_params:,}")

    # ---- 4. Wrap + freeze ----
    wrap = TabICLVirtualInjection(base, emb_dim=EMB_DIM).to(DEVICE)
    trainable_params = [p for p in wrap.parameters() if p.requires_grad]
    n_trainable = sum(p.numel() for p in trainable_params)
    echo(f"  trainable params: {n_trainable:,}")

    # ---- 5. Tensors on device ----
    X_train_t = torch.from_numpy(X_train_arr.astype(np.float32))
    X_test_t  = torch.from_numpy(X_test_arr.astype(np.float32))
    y_train_t = torch.from_numpy(y_train_int.astype(np.int64))

    def _metrics(y_true_int, proba):
        if args.task_type == "binary":
            return metrics_binary(y_true_int, proba)
        if args.task_type == "multiclass":
            return metrics_multiclass([classes[i] for i in y_true_int], proba, classes)
        # regression: prob-weighted bin centers
        y_pred = (proba * bin_centers[None, :]).sum(axis=1)
        return metrics_regression(y_test_continuous, y_pred)

    # ---- 6. Initial eval (untrained projections) ----
    echo("\n--- Initial eval (random-init projections) ---")
    wrap.eval()
    t0 = time.time()
    proba0 = predict_full(wrap, X_train_t, y_train_t, X_test_t,
                          virt_train, virt_test, n_classes=n_classes)
    m0 = _metrics(y_test_int, proba0)
    t_init = time.time() - t0
    echo(f"  predict {t_init:.1f}s")
    report_one(args.task_type, "initial", m0)

    # ---- 7. Training loop ----
    opt = torch.optim.AdamW(trainable_params, lr=args.lr, weight_decay=args.weight_decay)
    rng = np.random.RandomState(args.seed)
    n_train = X_train_t.shape[0]
    history = []
    best = {**m0, "epoch": -1}
    echo(f"\n--- Training: {args.epochs} epochs, lr={args.lr}, "
         f"ctx_size={args.ctx_size}, qry_size={args.qry_size} ---")
    t_train_start = time.time()
    for epoch in range(args.epochs):
        wrap.train()
        perm = rng.permutation(n_train)
        ctx_idx = perm[:args.ctx_size]
        qry_idx = perm[args.ctx_size:args.ctx_size + args.qry_size]
        X_ctx = X_train_t[ctx_idx]; y_ctx = y_train_t[ctx_idx]
        X_qry = X_train_t[qry_idx]; y_qry = y_train_t[qry_idx]
        virt_ctx = virt_train[ctx_idx]; virt_qry = virt_train[qry_idx]

        X_b = torch.cat([X_ctx, X_qry], dim=0).unsqueeze(0).to(DEVICE)  # (1, T, H)
        y_b = y_ctx.float().unsqueeze(0).to(DEVICE)                     # (1, ctx_size)
        virt_b = torch.from_numpy(np.concatenate([virt_ctx, virt_qry], axis=0)).to(DEVICE)
        targets = y_qry.long().to(DEVICE)

        out = wrap(X_b, y_b, virt_b)                                    # (1, qry_size, max_classes)
        logits = out[0, :, :n_classes]                                  # (qry_size, n_classes)
        loss = F.cross_entropy(logits, targets)

        opt.zero_grad()
        loss.backward()
        opt.step()

        if (epoch + 1) % args.eval_every == 0 or epoch == args.epochs - 1:
            wrap.eval()
            with torch.no_grad():
                proba = predict_full(wrap, X_train_t, y_train_t, X_test_t,
                                     virt_train, virt_test, n_classes=n_classes)
            m = _metrics(y_test_int, proba)
            history.append({"epoch": epoch + 1, "train_loss": float(loss.item()), **m})
            pm = primary_metric(args.task_type, m)
            metric_name = {"binary": "ROC-AUC", "multiclass": "macro-F1", "regression": "R²"}[args.task_type]
            extra = f"  LogLoss={m['log_loss']:.4f}" if args.task_type != "regression" else \
                    f"  MAE={m['mae']:.1f}  RMSE={m['rmse']:.1f}"
            echo(f"  ep {epoch+1:3d}/{args.epochs}  train_loss={loss.item():.4f}  "
                 f"test {metric_name}={pm:.4f}{extra}")
            if pm > primary_metric(args.task_type, best):
                best = {"epoch": epoch + 1, **m}
    t_train = time.time() - t_train_start

    # ---- 8. Save ----
    summary = {
        "run_id": run_id,
        "subtask": args.subtask, "target": args.target, "task_type": args.task_type,
        "phase": args.phase,
        "n_train": int(n_train), "n_test": int(len(y_test)), "n_classes": int(n_classes),
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
    (run_dir / "metrics.json").write_text(json.dumps(summary, indent=2))
    pm_name = {"binary": "ROC-AUC", "multiclass": "macro-F1", "regression": "R²"}[args.task_type]
    echo("\n=== Summary ===")
    echo(f"  Initial   {pm_name}: {primary_metric(args.task_type, m0):.4f}")
    echo(f"  Best      {pm_name}: {primary_metric(args.task_type, best):.4f}  (at epoch {best['epoch']})")
    echo(f"  Saved: {run_dir / 'metrics.json'}")
    log_f.close()


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--subtask", default="serious-adverse-event-forecasting")
    p.add_argument("--target", default="Y/N")
    p.add_argument("--task-type", choices=["binary", "multiclass", "regression"], default="binary")
    p.add_argument("--phase", required=True, choices=["Phase1", "Phase2", "Phase3", "Phase4"])
    p.add_argument("--n-bins", type=int, default=10,
                   help="For regression: number of quantile bins (max 10)")
    p.add_argument("--epochs", type=int, default=30)
    p.add_argument("--lr", type=float, default=1e-3)
    p.add_argument("--weight-decay", type=float, default=1e-4)
    p.add_argument("--ctx-size", type=int, default=2000)
    p.add_argument("--qry-size", type=int, default=500)
    p.add_argument("--eval-every", type=int, default=2)
    p.add_argument("--seed", type=int, default=0)
    args = p.parse_args()
    main(args)
