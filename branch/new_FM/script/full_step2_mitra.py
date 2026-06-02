#!/usr/bin/env python3
"""
full_step2_mitra.py — Full Step 2 (virtual feature column injection) for **Mitra (Tab2D)**.

Architecturally inject 2 virtual feature columns into Mitra's Tab2D:
   - virtual col 1 = projected incl mean-pooled criterion embedding (768→d)
   - virtual col 2 = projected excl mean-pooled criterion embedding (768→d)

where d = Tab2D's `dim` (512 by default).

Freeze entire Tab2D base; train ONLY:
   - 2 × nn.Linear(768, d)
   - 2 × nn.Parameter(d)   ← virtual column embeddings

Injection point: between `x_embedding(x)` and the `einops.pack` that concatenates
y_emb with x_emb. We replicate the whole Tab2D.forward locally (else branch, no
flash_attn) so we control the column-axis composition end-to-end.

Mirrors `full_step2_train.py` (TabPFN) and `full_step2_tabicl.py` (TabICL).
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import warnings
from datetime import datetime
from pathlib import Path

import einops
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
from torch.utils.checkpoint import checkpoint

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
# Virtual injection wrapper for Mitra Tab2D
# -------------------------------------------------------------------------

class MitraVirtualInjection(nn.Module):
    """Wraps a Mitra `Tab2D` nn.Module. Freezes base. Adds 2 trainable Linear projections
    (768→d) + 2 trainable column embeddings (d,) that get injected between
    `x_embedding` and the einops.pack that combines y/x.

    Replicates the non-flash branch of Tab2D.forward.
    """

    def __init__(self, base, emb_dim: int = 768):
        super().__init__()
        self.base = base
        D = base.dim
        self.D = D
        self.proj_incl = nn.Linear(emb_dim, D, bias=False)
        self.proj_excl = nn.Linear(emb_dim, D, bias=False)
        nn.init.xavier_uniform_(self.proj_incl.weight)
        nn.init.xavier_uniform_(self.proj_excl.weight)
        self.virt_col_emb = nn.Parameter(torch.zeros(2, D))
        nn.init.normal_(self.virt_col_emb, std=0.02)

        # Freeze base.
        for p in self.base.parameters():
            p.requires_grad = False

    def _virt_4d(self, virt_n2_768: torch.Tensor, batch_size: int, out_dtype, device) -> torch.Tensor:
        """Project virt (n, 2, 768) → (b, n, 2, d) in out_dtype, broadcast over batch."""
        proj_dtype = self.proj_incl.weight.dtype
        v_in = virt_n2_768.to(device).to(proj_dtype)  # (n, 2, 768)
        i_nd = self.proj_incl(v_in[:, 0, :]) + self.virt_col_emb[0]  # (n, d)
        e_nd = self.proj_excl(v_in[:, 1, :]) + self.virt_col_emb[1]  # (n, d)
        v_n2d = torch.stack([i_nd, e_nd], dim=1).to(out_dtype)        # (n, 2, d)
        return v_n2d.unsqueeze(0).expand(batch_size, -1, -1, -1).contiguous()  # (b, n, 2, d)

    def forward(
        self,
        x_support: torch.Tensor,    # (b, n_s, f)
        y_support: torch.Tensor,    # (b, n_s)
        x_query:   torch.Tensor,    # (b, n_q, f)
        virt_train: torch.Tensor,   # (n_s, 2, 768)
        virt_test:  torch.Tensor,   # (n_q, 2, 768)
    ) -> torch.Tensor:
        """Replicates Tab2D.forward (else branch) with 2 virtual cols injected after x_embedding."""
        base = self.base
        from autogluon.tabular.models.mitra._internal.config.enums import Task

        b = x_support.shape[0]
        n_s = x_support.shape[1]
        n_q = x_query.shape[1]
        f = x_support.shape[2]

        # No padding for our single-table batches.
        padding_features = torch.zeros((b, f), dtype=torch.bool, device=x_support.device)
        padding_obs_support = torch.zeros((b, n_s), dtype=torch.bool, device=x_support.device)
        padding_obs_query   = torch.zeros((b, n_q), dtype=torch.bool, device=x_support.device)

        # 1. Quantile transform
        x_support, x_query_ = base.x_quantile(x_support, x_query, padding_obs_support, padding_features)

        # 2. X embedding (b, n, f) → (b, n, f, d)
        x_support = base.x_embedding(x_support)
        x_query_  = base.x_embedding(x_query_)

        # 2b. Inject 2 virtual feature columns. (b, n, f+2, d)
        out_dtype = x_support.dtype
        v_s_b_n2d = self._virt_4d(virt_train, b, out_dtype, x_support.device)  # (b, n_s, 2, d)
        v_q_b_n2d = self._virt_4d(virt_test,  b, out_dtype, x_query_.device)   # (b, n_q, 2, d)
        x_support = torch.cat([x_support, v_s_b_n2d], dim=2)
        x_query_  = torch.cat([x_query_,  v_q_b_n2d], dim=2)
        # Extend padding_features by 2 zeros (the virt cols are valid).
        padding_features = torch.cat(
            [padding_features, torch.zeros((b, 2), dtype=padding_features.dtype, device=padding_features.device)],
            dim=1,
        )

        # 3. Y embedding
        y_support_e, y_query_e = base.y_embedding(y_support, padding_obs_support, n_q)

        # 4. Pack y/x along col axis
        support, pack_s = einops.pack((y_support_e, x_support), 'b s * d')   # (b, n_s, f+1+2, d)
        query__, pack_q = einops.pack((y_query_e,  x_query_),  'b s * d')

        # 5. Extend padding_features with y column (no padding for y)
        padding_features_y = torch.zeros((b, 1), device=padding_features.device, dtype=padding_features.dtype)
        padding_features, _ = einops.pack((padding_features_y, padding_features), 'b *')  # (b, f+3)

        # 6. Layers (else branch — same as Tab2D.forward when use_flash_attn=False)
        for layer in base.layers:
            support, query__ = checkpoint(
                layer, support, query__, None, None,
                b, padding_obs_support, padding_obs_query, padding_features,
                use_reentrant=False,
            )

        # 7. Final layer norm + linear
        query__ = base.final_layer_norm(query__)
        query__ = base.final_layer(query__)  # (b, n_q, f+3, dim_output)

        # 8. Unpack
        y_query_, x_query_ = einops.unpack(query__, pack_q, 'b s * c')

        # 9. Return y_query in same shape as original
        if base.task == Task.REGRESSION:
            if base.dim_output == 1:
                y_query_ = y_query_[:, :, 0, 0]
            else:
                y_query_ = y_query_[:, :, 0, :]
        else:  # CLASSIFICATION
            y_query_ = y_query_[:, :, 0, :]
        return y_query_


# -------------------------------------------------------------------------
# Training / driver
# -------------------------------------------------------------------------

def _proba_from_logits(out: torch.Tensor, n_classes: int) -> torch.Tensor:
    """Mitra classifier output: (b, n_q, dim_output). Slice to n_classes + softmax."""
    return F.softmax(out[..., :n_classes].float(), dim=-1)


@torch.inference_mode()
def predict_full(wrap, X_train_t, y_train_t, X_test_t, virt_train, virt_test, n_classes, force_use_flash_attn=False):
    """Eval: x_support = full train, x_query = test. B=1."""
    X_s = X_train_t.unsqueeze(0).to(DEVICE)         # (1, n_s, f)
    X_q = X_test_t.unsqueeze(0).to(DEVICE)          # (1, n_q, f)
    y_s = y_train_t.float().unsqueeze(0).to(DEVICE) # (1, n_s)
    virt_s = virt_train.to(DEVICE)                   # (n_s, 2, 768)
    virt_q = virt_test.to(DEVICE)
    out = wrap(X_s, y_s, X_q, virt_s, virt_q)        # (1, n_q, dim_output)
    proba = _proba_from_logits(out, n_classes).cpu().numpy()
    return proba[0]


def main(args):
    safe_subtask = args.subtask.replace("/", "_")
    safe_target  = args.target.replace("/", "")
    run_id = f"full_step2_mitra_{safe_subtask}_{safe_target}_{args.phase}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    run_dir = RESULTS_ROOT / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    log_f = open(run_dir / "log.txt", "w")

    def echo(*parts):
        line = " ".join(str(p) for p in parts)
        print(line)
        print(line, file=log_f, flush=True)

    echo(f"[run_id] {run_id}")
    echo(f"[subtask] {args.subtask}  [target] {args.target}  [task-type] {args.task_type}  [phase] {args.phase}")

    # 1. Load + preprocess subtask data
    X_train_df, y_train = load_split_generic(args.subtask, "train", args.target, [args.phase])
    X_test_df,  y_test  = load_split_generic(args.subtask, "test",  args.target, [args.phase])
    echo(f"  train={X_train_df.shape}  test={X_test_df.shape}")

    # Label encoding / regression binning
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

    # 2. Mean-pool IE + align
    pool = mean_pool_per_trial(EMB_RUN)
    virt_train = align_virt_emb(X_train_p, pool)
    virt_test  = align_virt_emb(X_test_p,  pool)
    echo(f"  virt_train {virt_train.shape}  virt_test {virt_test.shape}")

    # 3. Load Mitra Tab2D directly from HF
    echo("Loading Tab2D from autogluon/mitra-classifier (HF) ...")
    from autogluon.tabular.models.mitra._internal.models.tab2d import Tab2D
    if args.task_type == "regression":
        # Regression in our quantile-binning setup actually uses Mitra's classifier head
        # (dim_output = K bins). Use the classifier HF model.
        repo = "autogluon/mitra-classifier"
        task_str = "CLASSIFICATION"
    else:
        repo = "autogluon/mitra-classifier"
        task_str = "CLASSIFICATION"
    base = Tab2D.from_pretrained(repo, device=DEVICE)
    base.use_flash_attn = False  # ensure non-flash code path
    echo(f"  Tab2D dim={base.dim}, n_layers={base.n_layers}, n_heads={base.n_heads}, task={base.task}, dim_output={base.dim_output}")
    n_base_params = sum(p.numel() for p in base.parameters())
    echo(f"  base params: {n_base_params:,}")

    # 4. Wrap + freeze
    wrap = MitraVirtualInjection(base, emb_dim=EMB_DIM).to(DEVICE)
    trainable_params = [p for p in wrap.parameters() if p.requires_grad]
    n_trainable = sum(p.numel() for p in trainable_params)
    echo(f"  trainable params: {n_trainable:,}")

    # 5. Tensors on device
    X_train_t = torch.from_numpy(X_train_arr.astype(np.float32))
    X_test_t  = torch.from_numpy(X_test_arr.astype(np.float32))
    y_train_t = torch.from_numpy(y_train_int.astype(np.int64))
    virt_train_t = torch.from_numpy(virt_train)
    virt_test_t  = torch.from_numpy(virt_test)

    def _metrics(y_true_int, proba):
        if args.task_type == "binary":
            return metrics_binary(y_true_int, proba)
        if args.task_type == "multiclass":
            return metrics_multiclass([classes[i] for i in y_true_int], proba, classes)
        y_pred = (proba * bin_centers[None, :]).sum(axis=1)
        return metrics_regression(y_test_continuous, y_pred)

    # 6. Initial eval (untrained projections)
    echo("\n--- Initial eval (random-init projections) ---")
    wrap.eval()
    t0 = time.time()
    # AMP autocast bfloat16 like Mitra default
    with torch.autocast(device_type="cuda", dtype=torch.bfloat16):
        proba0 = predict_full(wrap, X_train_t, y_train_t, X_test_t,
                              virt_train_t, virt_test_t, n_classes=n_classes)
    m0 = _metrics(y_test_int, proba0)
    echo(f"  predict {time.time()-t0:.1f}s")
    report_one(args.task_type, "initial", m0)

    # 7. Training loop
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
        X_qry = X_train_t[qry_idx]
        virt_ctx = virt_train_t[ctx_idx]
        virt_qry = virt_train_t[qry_idx]
        targets = y_train_t[qry_idx].long().to(DEVICE)

        X_s = X_ctx.unsqueeze(0).to(DEVICE)
        X_q = X_qry.unsqueeze(0).to(DEVICE)
        y_s = y_ctx.float().unsqueeze(0).to(DEVICE)

        with torch.autocast(device_type="cuda", dtype=torch.bfloat16):
            out = wrap(X_s, y_s, X_q, virt_ctx.to(DEVICE), virt_qry.to(DEVICE))  # (1, qry_size, dim_output)
            logits = out[0, :, :n_classes]
            loss = F.cross_entropy(logits, targets)

        opt.zero_grad()
        loss.backward()
        opt.step()

        if (epoch + 1) % args.eval_every == 0 or epoch == args.epochs - 1:
            wrap.eval()
            with torch.no_grad(), torch.autocast(device_type="cuda", dtype=torch.bfloat16):
                proba = predict_full(wrap, X_train_t, y_train_t, X_test_t,
                                     virt_train_t, virt_test_t, n_classes=n_classes)
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

    # 8. Save
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
                   help="For regression: number of quantile bins (max = Mitra dim_output)")
    p.add_argument("--epochs", type=int, default=30)
    p.add_argument("--lr", type=float, default=1e-3)
    p.add_argument("--weight-decay", type=float, default=1e-4)
    p.add_argument("--ctx-size", type=int, default=2000)
    p.add_argument("--qry-size", type=int, default=500)
    p.add_argument("--eval-every", type=int, default=2)
    p.add_argument("--seed", type=int, default=0)
    args = p.parse_args()
    main(args)
