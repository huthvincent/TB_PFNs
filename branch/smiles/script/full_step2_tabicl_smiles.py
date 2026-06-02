#!/usr/bin/env python3
"""
full_step2_tabicl_smiles.py — Full Step 2 (virtual feature column injection)
for **TabICLv2**, with 2 or 3 virtual feature columns:

   - virtual col 1 = projected incl mean-pooled criterion embedding (d_ie → E)
   - virtual col 2 = projected excl mean-pooled criterion embedding (d_ie → E)
   - virtual col 3 = projected SMILES mean-pooled embedding         (d_sm → E)
                     (only when --smiles-emb is provided)

where E = TabICL's `embed_dim` (default 128). Dimensions d_ie and d_sm are
auto-detected from the parquet files (Qwen3-Embedding-8B I/E gives 4096;
SMILES encoders vary: ChemBERTa 384, MolFormer 768, Mol2Vec 300).

Freeze entire TabICL; train ONLY:
   - 2 or 3 × nn.Linear(d_in, E)
   - 2 or 3 × nn.Parameter(E)   ← virtual column embeddings

Forked from /data2/zhu11/TB/branch/new_FM/script/full_step2_tabicl.py with two
new ideas:
  (1) IE source is the Qwen3 parquet at branch/smiles/data/ie_embeddings_qwen3.parquet
      (replaces MedCPT 768-d). Path is configurable via --ie-emb.
  (2) Optional SMILES virtual token via --smiles-emb <parquet>.
  (3) When SMILES is provided, also report metrics on the test-SMILES-non-empty
      subset (Cell D in the smiles branch design).
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

# Reuse plumbing from sibling branches.
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

DEFAULT_IE_PARQUET = Path("/data2/zhu11/TB/branch/smiles/data/ie_embeddings_qwen3.parquet")
RESULTS_ROOT       = Path("/data2/zhu11/TB/branch/smiles/results")
DEVICE             = "cuda"


# -------------------------------------------------------------------------
# Embedding loaders + aligners
# -------------------------------------------------------------------------

def load_ie_lookup(path: Path) -> tuple[dict, int]:
    """Load {(trial_id, phase) → (incl_emb, excl_emb)} from a parquet with
    columns trial_id, phase, type∈{I,E}, mean_emb. Trials missing one type
    get a zero vector for it. Returns (lookup, d_ie)."""
    df = pd.read_parquet(path)
    # Detect dim from first row
    d_ie = len(df.iloc[0]["mean_emb"])
    out: dict[tuple, np.ndarray] = {}
    for r in df.itertuples(index=False):
        key = (str(r.trial_id), str(r.phase))
        if key not in out:
            out[key] = np.zeros((2, d_ie), dtype=np.float32)
        slot = 0 if r.type == "I" else 1
        out[key][slot] = np.asarray(r.mean_emb, dtype=np.float32)
    return out, d_ie


def load_smiles_lookup(path: Path) -> tuple[dict, int]:
    """Load {(trial_id, phase) → mean_emb} from a parquet with columns
    trial_id, phase, mean_emb. Returns (lookup, d_sm)."""
    df = pd.read_parquet(path)
    d_sm = len(df.iloc[0]["mean_emb"])
    out = {(str(r.trial_id), str(r.phase)): np.asarray(r.mean_emb, dtype=np.float32)
           for r in df.itertuples(index=False)}
    return out, d_sm


def align_ie(X_df: pd.DataFrame, ie_lookup: dict, d_ie: int) -> np.ndarray:
    out = np.zeros((len(X_df), 2, d_ie), dtype=np.float32)
    for i, (tid, ph) in enumerate(zip(X_df.index.astype(str),
                                      X_df["phase_split"].astype(str))):
        if (tid, ph) in ie_lookup:
            out[i] = ie_lookup[(tid, ph)]
    return out


def align_smiles(X_df: pd.DataFrame, sm_lookup: dict, d_sm: int):
    """Returns (emb_array, has_smiles_mask). emb is zero-fill where missing."""
    out  = np.zeros((len(X_df), d_sm), dtype=np.float32)
    mask = np.zeros(len(X_df), dtype=bool)
    for i, (tid, ph) in enumerate(zip(X_df.index.astype(str),
                                      X_df["phase_split"].astype(str))):
        if (tid, ph) in sm_lookup:
            out[i] = sm_lookup[(tid, ph)]
            mask[i] = True
    return out, mask


# -------------------------------------------------------------------------
# Virtual injection wrapper for TabICL (2 or 3 columns)
# -------------------------------------------------------------------------

class TabICLVirtualInjection(nn.Module):
    """Wraps a TabICL nn.Module. Freezes base. Adds trainable Linear
    projections (d_in → E) + trainable column embeddings (n_virt, E) that
    get injected as virtual feature columns between `col_embedder` and
    `row_interactor`. Supports n_virt=2 (I, E) or n_virt=3 (I, E, SMILES).
    """

    def __init__(self, base, d_ie: int, d_sm: int | None = None):
        super().__init__()
        self.base = base
        E = base.embed_dim
        self.E = E
        self.use_smiles = d_sm is not None
        self.n_virt = 3 if self.use_smiles else 2

        self.proj_incl = nn.Linear(d_ie, E, bias=False)
        self.proj_excl = nn.Linear(d_ie, E, bias=False)
        nn.init.xavier_uniform_(self.proj_incl.weight)
        nn.init.xavier_uniform_(self.proj_excl.weight)
        if self.use_smiles:
            self.proj_smiles = nn.Linear(d_sm, E, bias=False)
            nn.init.xavier_uniform_(self.proj_smiles.weight)
        self.virt_col_emb = nn.Parameter(torch.zeros(self.n_virt, E))
        nn.init.normal_(self.virt_col_emb, std=0.02)

        for p in self.base.parameters():
            p.requires_grad = False

    def forward(self, X_BTH, y_train_BT, ie_T2_d, sm_T_d=None):
        """
        Args:
            X_BTH      : (B=1, T, H) preprocessed feature tensor
            y_train_BT : (B=1, train_size)
            ie_T2_d    : (T, 2, d_ie) — incl and excl mean-pooled embeddings
            sm_T_d     : (T, d_sm) — SMILES mean-pooled embedding (optional)
        """
        col_out = self.base.col_embedder(
            X_BTH, y_train=y_train_BT, d=None, embed_with_test=False,
        )  # (B, T, G+C, E)

        proj_dtype = self.proj_incl.weight.dtype  # fp32 projection for stability
        v_ie = ie_T2_d.to(col_out.device).to(proj_dtype)  # (T, 2, d_ie)
        incl_te = self.proj_incl(v_ie[:, 0, :]) + self.virt_col_emb[0]
        excl_te = self.proj_excl(v_ie[:, 1, :]) + self.virt_col_emb[1]
        cols = [incl_te, excl_te]
        if self.use_smiles:
            assert sm_T_d is not None
            v_sm = sm_T_d.to(col_out.device).to(proj_dtype)  # (T, d_sm)
            sm_te = self.proj_smiles(v_sm) + self.virt_col_emb[2]
            cols.append(sm_te)
        virt_tne = torch.stack(cols, dim=1).to(col_out.dtype)  # (T, n_virt, E)

        B = col_out.shape[0]
        virt_btne = virt_tne.unsqueeze(0).expand(B, -1, -1, -1).contiguous()
        col_aug = torch.cat([col_out, virt_btne], dim=2)
        repr_ = self.base.row_interactor(col_aug, d=None)
        out = self.base.icl_predictor(repr_, y_train=y_train_BT)
        return out


# -------------------------------------------------------------------------
# Eval / training helpers
# -------------------------------------------------------------------------

def _proba_from_logits(out: torch.Tensor, n_classes: int) -> torch.Tensor:
    return F.softmax(out[..., :n_classes].float(), dim=-1)


@torch.inference_mode()
def predict_full(wrap, X_train_t, y_train_t, X_test_t,
                 ie_train, ie_test, sm_train, sm_test, n_classes: int):
    X = torch.cat([X_train_t, X_test_t], dim=0).unsqueeze(0).to(DEVICE)
    y = y_train_t.float().unsqueeze(0).to(DEVICE)
    ie_all = torch.from_numpy(np.concatenate([ie_train, ie_test], axis=0)).to(DEVICE)
    sm_all = None
    if wrap.use_smiles:
        sm_all = torch.from_numpy(np.concatenate([sm_train, sm_test], axis=0)).to(DEVICE)
    out = wrap(X, y, ie_all, sm_all)
    return _proba_from_logits(out, n_classes).cpu().numpy()[0]  # (test_size, n_classes)


# -------------------------------------------------------------------------
# Main
# -------------------------------------------------------------------------

def main(args):
    safe_subtask = args.subtask.replace("/", "_")
    safe_target  = args.target.replace("/", "")
    sm_short = "no_smiles"
    if args.smiles_emb:
        sm_short = Path(args.smiles_emb).stem.replace("smiles_embeddings_", "smi_")
    tag = f"{safe_subtask}_{safe_target}_{args.phase}_{sm_short}"
    run_id = f"full_step2_tabicl_smiles_{tag}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    run_dir = RESULTS_ROOT / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    log_f = open(run_dir / "log.txt", "w")

    def echo(*parts):
        line = " ".join(str(p) for p in parts)
        print(line)
        print(line, file=log_f, flush=True)

    echo(f"[run_id] {run_id}")
    echo(f"[subtask] {args.subtask}  [target] {args.target}  [task-type] {args.task_type}  [phase] {args.phase}")
    echo(f"[ie-emb] {args.ie_emb}")
    echo(f"[smiles-emb] {args.smiles_emb}")

    # ---- 1. Subtask data ----
    X_train_df, y_train = load_split_generic(args.subtask, "train", args.target, [args.phase])
    X_test_df,  y_test  = load_split_generic(args.subtask, "test",  args.target, [args.phase])
    echo(f"  train={X_train_df.shape}  test={X_test_df.shape}")

    # Label encoding
    y_train_continuous = y_test_continuous = bin_centers = None
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
    else:
        raise ValueError(args.task_type)

    X_train_p, X_test_p = preprocess(X_train_df, X_test_df)
    sk = build_sklearn_preprocessor(X_train_p)
    X_train_arr = sk.fit_transform(X_train_p)
    X_test_arr  = sk.transform(X_test_p)
    echo(f"  preprocessed: train {X_train_arr.shape}  test {X_test_arr.shape}")

    # ---- 2. Load + align I/E embeddings ----
    ie_path = Path(args.ie_emb)
    ie_lookup, d_ie = load_ie_lookup(ie_path)
    ie_train = align_ie(X_train_p, ie_lookup, d_ie)
    ie_test  = align_ie(X_test_p,  ie_lookup, d_ie)
    echo(f"  I/E d={d_ie}  ie_train {ie_train.shape}  ie_test {ie_test.shape}")
    echo(f"  trials with non-zero I/E: train "
         f"{(ie_train.sum((1,2)) != 0).sum()}/{len(ie_train)}, "
         f"test {(ie_test.sum((1,2)) != 0).sum()}/{len(ie_test)}")

    # ---- 2b. Load + align SMILES embeddings (optional) ----
    d_sm = None
    sm_train = sm_test = None
    has_sm_test = np.zeros(len(X_test_p), dtype=bool)
    if args.smiles_emb:
        sm_path = Path(args.smiles_emb)
        sm_lookup, d_sm = load_smiles_lookup(sm_path)
        sm_train, has_sm_train = align_smiles(X_train_p, sm_lookup, d_sm)
        sm_test,  has_sm_test  = align_smiles(X_test_p,  sm_lookup, d_sm)
        echo(f"  SMILES d={d_sm}  sm_train {sm_train.shape}  "
             f"({has_sm_train.sum()}/{len(has_sm_train)} non-zero), "
             f"sm_test ({has_sm_test.sum()}/{len(has_sm_test)} non-zero)")
    elif args.report_subset_emb:
        # Cell B' baseline: do NOT inject SMILES, but still report metrics on the
        # SMILES-non-empty test subset so it's a clean baseline for Cell D.
        _, d_mask = load_smiles_lookup(Path(args.report_subset_emb))
        _sm_lookup, _ = load_smiles_lookup(Path(args.report_subset_emb))
        _, has_sm_test = align_smiles(X_test_p, _sm_lookup, d_mask)
        echo(f"  [report-subset only] test SMILES-non-empty subset: "
             f"{has_sm_test.sum()}/{len(has_sm_test)}")

    # Report subset metrics whenever we have a mask (either via injected SMILES
    # or via --report-subset-emb for the B' baseline).
    report_subset = bool(args.smiles_emb or args.report_subset_emb)

    # ---- 3. Bootstrap TabICL ----
    echo("Initializing TabICL ...")
    from tabicl import TabICLClassifier
    clf = TabICLClassifier(device=DEVICE, n_estimators=1,
                           random_state=args.seed, allow_auto_download=True)
    n_init = min(50, len(X_train_arr))
    init_idx = np.concatenate([np.where(y_train_int == c)[0][:max(1, n_init // n_classes)]
                               for c in range(n_classes)])[:n_init]
    if len(init_idx) < n_classes:
        init_idx = np.arange(n_init)
    clf.fit(X_train_arr[init_idx].astype(np.float32), y_train_int[init_idx])
    base = clf.model_
    n_base_params = sum(p.numel() for p in base.parameters())
    echo(f"  base embed_dim={base.embed_dim}  base params: {n_base_params:,}")

    # ---- 4. Wrap + freeze ----
    wrap = TabICLVirtualInjection(base, d_ie=d_ie, d_sm=d_sm).to(DEVICE)
    n_trainable = sum(p.numel() for p in wrap.parameters() if p.requires_grad)
    echo(f"  n_virt_cols={wrap.n_virt}  trainable params: {n_trainable:,}")

    # ---- 5. Tensors ----
    X_train_t = torch.from_numpy(X_train_arr.astype(np.float32))
    X_test_t  = torch.from_numpy(X_test_arr.astype(np.float32))
    y_train_t = torch.from_numpy(y_train_int.astype(np.int64))

    def _metrics_full(proba):
        if args.task_type == "binary":
            return metrics_binary(y_test_int, proba)
        if args.task_type == "multiclass":
            return metrics_multiclass([classes[i] for i in y_test_int], proba, classes)
        y_pred = (proba * bin_centers[None, :]).sum(axis=1)
        return metrics_regression(y_test_continuous, y_pred)

    def _metrics_subset(proba, mask):
        if not mask.any():
            return None
        if args.task_type == "binary":
            return metrics_binary(y_test_int[mask], proba[mask])
        if args.task_type == "multiclass":
            return metrics_multiclass([classes[i] for i in y_test_int[mask]],
                                      proba[mask], classes)
        y_pred = (proba * bin_centers[None, :]).sum(axis=1)
        return metrics_regression(y_test_continuous[mask], y_pred[mask])

    # ---- 6. Initial eval ----
    echo("\n--- Initial eval (random-init projections) ---")
    wrap.eval()
    t0 = time.time()
    proba0 = predict_full(wrap, X_train_t, y_train_t, X_test_t,
                          ie_train, ie_test, sm_train, sm_test, n_classes)
    m0 = _metrics_full(proba0)
    m0_subset = _metrics_subset(proba0, has_sm_test) if report_subset else None
    echo(f"  predict {time.time() - t0:.1f}s")
    report_one(args.task_type, "initial-full", m0)
    if m0_subset is not None:
        report_one(args.task_type, "initial-smiles-subset", m0_subset)

    # ---- 7. Train ----
    opt = torch.optim.AdamW([p for p in wrap.parameters() if p.requires_grad],
                            lr=args.lr, weight_decay=args.weight_decay)
    rng = np.random.RandomState(args.seed)
    n_train = X_train_t.shape[0]
    history = []
    best        = {**m0, "epoch": -1}
    best_subset = {**m0_subset, "epoch": -1} if m0_subset is not None else None
    echo(f"\n--- Training: {args.epochs} epochs, lr={args.lr}, ctx={args.ctx_size}, qry={args.qry_size} ---")
    t_train_start = time.time()
    for epoch in range(args.epochs):
        wrap.train()
        perm = rng.permutation(n_train)
        ctx_idx = perm[:args.ctx_size]
        qry_idx = perm[args.ctx_size:args.ctx_size + args.qry_size]
        X_ctx = X_train_t[ctx_idx]; y_ctx = y_train_t[ctx_idx]
        X_qry = X_train_t[qry_idx]; y_qry = y_train_t[qry_idx]
        ie_ctx = ie_train[ctx_idx]; ie_qry = ie_train[qry_idx]
        if args.smiles_emb:
            sm_ctx = sm_train[ctx_idx]; sm_qry = sm_train[qry_idx]

        X_b  = torch.cat([X_ctx, X_qry], dim=0).unsqueeze(0).to(DEVICE)
        y_b  = y_ctx.float().unsqueeze(0).to(DEVICE)
        ie_b = torch.from_numpy(np.concatenate([ie_ctx, ie_qry], axis=0)).to(DEVICE)
        sm_b = (torch.from_numpy(np.concatenate([sm_ctx, sm_qry], axis=0)).to(DEVICE)
                if args.smiles_emb else None)
        targets = y_qry.long().to(DEVICE)

        out = wrap(X_b, y_b, ie_b, sm_b)
        logits = out[0, :, :n_classes]
        loss = F.cross_entropy(logits, targets)
        opt.zero_grad(); loss.backward(); opt.step()

        if (epoch + 1) % args.eval_every == 0 or epoch == args.epochs - 1:
            wrap.eval()
            with torch.no_grad():
                proba = predict_full(wrap, X_train_t, y_train_t, X_test_t,
                                     ie_train, ie_test, sm_train, sm_test, n_classes)
            m = _metrics_full(proba)
            m_sub = _metrics_subset(proba, has_sm_test) if report_subset else None
            entry = {"epoch": epoch + 1, "train_loss": float(loss.item()), **m}
            if m_sub is not None:
                entry["subset"] = m_sub
            history.append(entry)
            metric_name = {"binary": "ROC-AUC", "multiclass": "macro-F1", "regression": "R²"}[args.task_type]
            pm = primary_metric(args.task_type, m)
            extra = f"  LogLoss={m['log_loss']:.4f}" if args.task_type != "regression" else \
                    f"  MAE={m['mae']:.1f}  RMSE={m['rmse']:.1f}"
            if m_sub is not None:
                extra += f"  | subset {metric_name}={primary_metric(args.task_type, m_sub):.4f}"
            echo(f"  ep {epoch+1:3d}/{args.epochs}  loss={loss.item():.4f}  "
                 f"test {metric_name}={pm:.4f}{extra}")
            if pm > primary_metric(args.task_type, best):
                best = {"epoch": epoch + 1, **m}
            if m_sub is not None and primary_metric(args.task_type, m_sub) > primary_metric(args.task_type, best_subset):
                best_subset = {"epoch": epoch + 1, **m_sub}
    t_train = time.time() - t_train_start

    # ---- 8. Save ----
    summary = {
        "run_id":              run_id,
        "subtask": args.subtask, "target": args.target, "task_type": args.task_type,
        "phase": args.phase,
        "n_train": int(n_train), "n_test": int(len(y_test)), "n_classes": int(n_classes),
        "n_baseline_features": int(X_train_arr.shape[1]),
        "n_virtual_cols":      int(wrap.n_virt),
        "d_ie":                int(d_ie),
        "d_smiles":            (int(d_sm) if d_sm else None),
        "ie_emb_path":         str(args.ie_emb),
        "smiles_emb_path":     (str(args.smiles_emb) if args.smiles_emb else None),
        "smiles_test_subset_size": int(has_sm_test.sum()) if report_subset else None,
        "smiles_test_subset_frac": float(has_sm_test.mean()) if report_subset else None,
        "n_base_params":       int(n_base_params),
        "n_trainable_params":  int(n_trainable),
        "elapsed_train_s":     round(t_train, 1),
        "initial_metrics":        m0,
        "initial_metrics_subset": m0_subset,
        "best_metrics":           best,
        "best_metrics_subset":    best_subset,
        "history":             history,
        "args":                vars(args),
    }
    (run_dir / "metrics.json").write_text(json.dumps(summary, indent=2))
    pm_name = {"binary": "ROC-AUC", "multiclass": "macro-F1", "regression": "R²"}[args.task_type]
    echo("\n=== Summary ===")
    echo(f"  Initial  {pm_name}: {primary_metric(args.task_type, m0):.4f}")
    echo(f"  Best     {pm_name}: {primary_metric(args.task_type, best):.4f}  (epoch {best['epoch']})")
    if best_subset is not None:
        echo(f"  Best (SMILES subset, n={int(has_sm_test.sum())})  "
             f"{pm_name}: {primary_metric(args.task_type, best_subset):.4f}  "
             f"(epoch {best_subset['epoch']})")
    echo(f"  Saved: {run_dir / 'metrics.json'}")
    log_f.close()


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--subtask", default="serious-adverse-event-forecasting")
    p.add_argument("--target", default="Y/N")
    p.add_argument("--task-type", choices=["binary", "multiclass", "regression"], default="binary")
    p.add_argument("--phase", required=True, choices=["Phase1", "Phase2", "Phase3", "Phase4"])
    p.add_argument("--ie-emb", default=str(DEFAULT_IE_PARQUET),
                   help="Path to I/E embedding parquet (cols: trial_id, phase, type, mean_emb)")
    p.add_argument("--smiles-emb", default=None,
                   help="Path to SMILES embedding parquet. Omit for Cell B' (+I+E only).")
    p.add_argument("--report-subset-emb", default=None,
                   help="For Cell B' baseline: a SMILES parquet used ONLY to define the "
                        "SMILES-non-empty test subset for reporting (no SMILES token injected). "
                        "Lets B' report a clean Cell-D-comparable subset metric.")
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
