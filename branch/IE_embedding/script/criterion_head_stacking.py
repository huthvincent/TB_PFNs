#!/usr/bin/env python3
"""
criterion_head_stacking.py — Train a small MLP head on top of frozen MedCPT
criterion embeddings to predict trial-level `droupout_rate` (sic; the column is
typo'd in TrialBench), with 5-fold OOF on labeled trials and a full-data model
for the rest. Aggregate per-criterion predictions into 8 per-trial features
(mean/max/std/count × {I, E}) saved as a parquet that downstream subtasks can
left-join into their train_x.csv.

Inputs:
  --emb-run  branch/IE_embedding/results/encode_medcpt_<TS>/
              ├─ embeddings.npy        (N, 768) float16
              └─ metadata.parquet      cols: trial_id, phase, type, idx, text

  patient-dropout-event-forecasting/{Phase1..4}/{train_y,test_y}.csv
              droupout_rate ∈ [0, 1]

Outputs:
  branch/IE_embedding/results/criterion_head_<TS>/
    ie_features.parquet         (trial_id, phase, incl_mean, incl_max, incl_std,
                                 incl_n, excl_mean, excl_max, excl_std, excl_n)
    oof_predictions.npy         (N,) float32 — per-criterion risk score, aligned
                                with metadata.parquet from the embedding run
    fold_metrics.json           per-fold MAE/RMSE/R^2 on held-out criteria
    run_info.json               args, timing, model name, etc.

Notes:
  - 5-fold split is on TRIALS (KFold over unique (trial_id, phase) in dropout
    train), so all criteria of one trial stay in one fold. Prevents
    criterion-level leakage.
  - Labels are broadcast: every criterion of trial T gets label = T.droupout_rate.
    This is weak supervision by design — see README §4.
  - For trials in dropout-test or in other subtasks (no dropout label), we use a
    single "full" model trained on all labeled criteria.
  - User explicitly opted out of cross-subtask trial dedup, so a trial in
    dropout-train may also appear in e.g. SAE-test — the full model trained on
    such trials is mildly biased, but downstream stacking still uses OOF for
    its own train and full-model for its own test.
"""

from __future__ import annotations

import argparse
import json
import time
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from sklearn.model_selection import KFold

DROPOUT_DIR  = Path("/data2/zhu11/TB/dataset/TrialBench/patient-dropout-event-forecasting")
RESULTS_ROOT = Path("/data2/zhu11/TB/branch/IE_embedding/results")
PHASES       = ["Phase1", "Phase2", "Phase3", "Phase4"]


# -------------------------------------------------------------------------
# Data loading
# -------------------------------------------------------------------------

def load_dropout_labels() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return (train_labels, test_labels) DataFrames with cols [trial_id, phase, dropout_rate]."""
    def _load(split):
        frames = []
        for ph in PHASES:
            df = pd.read_csv(DROPOUT_DIR / ph / f"{split}_y.csv")
            df.columns.values[0] = "trial_id"
            df = df.rename(columns={"droupout_rate": "dropout_rate"})
            df = df[["trial_id", "dropout_rate"]].copy()
            df["phase"] = ph
            df["dropout_rate"] = df["dropout_rate"].astype(np.float32)
            frames.append(df)
        return pd.concat(frames, ignore_index=True)
    return _load("train"), _load("test")


def load_embeddings_run(emb_run: Path):
    """Load embeddings.npy and metadata.parquet aligned row-by-row."""
    emb = np.load(emb_run / "embeddings.npy", mmap_mode="r")
    meta = pd.read_parquet(emb_run / "metadata.parquet")
    assert len(meta) == emb.shape[0], f"mismatch: emb {emb.shape} vs meta {len(meta)}"
    return emb, meta


# -------------------------------------------------------------------------
# Model
# -------------------------------------------------------------------------

class CriterionHead(nn.Module):
    def __init__(self, in_dim=768, hidden=256, dropout=0.2):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_dim, hidden),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(hidden, hidden),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(hidden, 1),
        )

    def forward(self, x):
        return self.net(x).squeeze(-1)


def train_head(
    X_train: torch.Tensor,    # (n_train, 768) on GPU
    y_train: torch.Tensor,    # (n_train,) on GPU
    X_val: torch.Tensor | None,
    y_val: torch.Tensor | None,
    *,
    epochs: int,
    batch_size: int,
    lr: float,
    weight_decay: float,
    device: str,
    verbose: bool = False,
) -> CriterionHead:
    model = CriterionHead().to(device)
    opt = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=weight_decay)
    loss_fn = nn.MSELoss()
    n = X_train.shape[0]

    for ep in range(epochs):
        model.train()
        perm = torch.randperm(n, device=device)
        total_loss = 0.0
        for s in range(0, n, batch_size):
            idx = perm[s:s + batch_size]
            xb = X_train[idx]
            yb = y_train[idx]
            pred = model(xb.float())
            loss = loss_fn(pred, yb)
            opt.zero_grad()
            loss.backward()
            opt.step()
            total_loss += loss.item() * len(idx)
        avg = total_loss / n
        if verbose and (ep == 0 or (ep + 1) % 5 == 0 or ep == epochs - 1):
            line = f"    epoch {ep+1:3d}/{epochs}  train_mse={avg:.5f}"
            if X_val is not None:
                model.eval()
                with torch.inference_mode():
                    vp = model(X_val.float())
                    vmse = ((vp - y_val) ** 2).mean().item()
                line += f"  val_mse={vmse:.5f}"
            print(line)
    return model


@torch.inference_mode()
def predict(model: CriterionHead, X: torch.Tensor, batch_size: int = 4096) -> np.ndarray:
    model.eval()
    preds = []
    for s in range(0, X.shape[0], batch_size):
        preds.append(model(X[s:s + batch_size].float()).float().cpu().numpy())
    return np.concatenate(preds)


# -------------------------------------------------------------------------
# Aggregation
# -------------------------------------------------------------------------

def aggregate_to_trial_features(meta: pd.DataFrame, scores: np.ndarray) -> pd.DataFrame:
    """Given per-criterion scores aligned to meta, produce one row per (trial_id, phase)
    with mean/max/std/n for inclusion and exclusion."""
    df = meta[["trial_id", "phase", "type"]].copy()
    df["score"] = scores

    def _agg(sub):
        return pd.Series({
            "mean": float(sub["score"].mean()) if len(sub) else np.nan,
            "max":  float(sub["score"].max())  if len(sub) else np.nan,
            "std":  float(sub["score"].std(ddof=0)) if len(sub) > 1 else 0.0,
            "n":    int(len(sub)),
        })

    grouped = df.groupby(["trial_id", "phase", "type"]).apply(_agg).unstack("type")
    # grouped columns: MultiIndex (stat, type) — flatten
    grouped.columns = [f"{'incl' if t == 'I' else 'excl'}_{stat}" for stat, t in grouped.columns]
    # Ensure all 8 columns exist (some trials may lack I or E entirely)
    for c in ["incl_mean", "incl_max", "incl_std", "incl_n",
              "excl_mean", "excl_max", "excl_std", "excl_n"]:
        if c not in grouped.columns:
            grouped[c] = np.nan
    grouped[["incl_n", "excl_n"]] = grouped[["incl_n", "excl_n"]].fillna(0).astype(int)
    return grouped.reset_index()[["trial_id", "phase",
                                  "incl_mean", "incl_max", "incl_std", "incl_n",
                                  "excl_mean", "excl_max", "excl_std", "excl_n"]]


# -------------------------------------------------------------------------
# Main
# -------------------------------------------------------------------------

def main(args):
    run_id = f"criterion_head_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    run_dir = RESULTS_ROOT / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    print(f"[run_id] {run_id}")
    print(f"[run_dir] {run_dir}")
    t_start = time.time()

    # ----- Load embeddings & metadata -----
    emb_run = Path(args.emb_run)
    print(f"Loading embeddings from {emb_run} ...")
    emb_np, meta = load_embeddings_run(emb_run)
    n_crit = len(meta)
    print(f"  embeddings: {emb_np.shape}  meta rows: {n_crit:,}")

    # ----- Load dropout labels -----
    print("Loading dropout labels ...")
    train_y, test_y = load_dropout_labels()
    train_y_keys = set(zip(train_y["trial_id"], train_y["phase"]))
    test_y_keys  = set(zip(test_y["trial_id"], test_y["phase"]))
    print(f"  dropout train trials: {len(train_y_keys):,}  test trials: {len(test_y_keys):,}")

    # ----- Build per-criterion labels (broadcast trial-level rate) -----
    meta_key = list(zip(meta["trial_id"], meta["phase"]))
    train_lookup = dict(zip(zip(train_y["trial_id"], train_y["phase"]), train_y["dropout_rate"]))

    is_labeled_train = np.array([k in train_lookup for k in meta_key])
    crit_labels = np.array([train_lookup.get(k, np.nan) for k in meta_key], dtype=np.float32)
    n_labeled = int(is_labeled_train.sum())
    print(f"  criteria with dropout-train labels: {n_labeled:,} / {n_crit:,}")

    # ----- Move embeddings to GPU once (they fit comfortably) -----
    device = args.device
    print(f"Moving embeddings to {device} ...")
    emb_t = torch.from_numpy(np.ascontiguousarray(emb_np)).to(device)   # float16
    print(f"  GPU emb tensor: {tuple(emb_t.shape)} {emb_t.dtype}  "
          f"({emb_t.element_size()*emb_t.nelement()/1e9:.2f} GB)")

    # ----- 5-fold CV on TRIALS within dropout-train -----
    labeled_keys = sorted(train_y_keys)  # deterministic
    kf = KFold(n_splits=args.folds, shuffle=True, random_state=args.seed)
    oof = np.full(n_crit, np.nan, dtype=np.float32)
    fold_metrics = []

    for fold, (tr_idx, va_idx) in enumerate(kf.split(labeled_keys)):
        print(f"\n=== Fold {fold+1}/{args.folds} ===")
        tr_keys = set(labeled_keys[i] for i in tr_idx)
        va_keys = set(labeled_keys[i] for i in va_idx)
        tr_mask = np.array([k in tr_keys for k in meta_key])
        va_mask = np.array([k in va_keys for k in meta_key])
        print(f"  train criteria: {tr_mask.sum():,}  val criteria: {va_mask.sum():,}")

        Xtr_idx = np.where(tr_mask)[0]
        Xva_idx = np.where(va_mask)[0]
        Xtr = emb_t[torch.from_numpy(Xtr_idx).to(device)]
        ytr = torch.from_numpy(crit_labels[Xtr_idx]).to(device)
        Xva = emb_t[torch.from_numpy(Xva_idx).to(device)]
        yva = torch.from_numpy(crit_labels[Xva_idx]).to(device)

        model = train_head(
            Xtr, ytr, Xva, yva,
            epochs=args.epochs, batch_size=args.batch_size,
            lr=args.lr, weight_decay=args.weight_decay,
            device=device, verbose=True,
        )
        va_pred = predict(model, Xva, batch_size=args.eval_batch_size)
        oof[Xva_idx] = va_pred

        va_true = crit_labels[Xva_idx]
        mae  = float(np.abs(va_pred - va_true).mean())
        rmse = float(np.sqrt(((va_pred - va_true) ** 2).mean()))
        ss_res = float(((va_pred - va_true) ** 2).sum())
        ss_tot = float(((va_true - va_true.mean()) ** 2).sum())
        r2 = 1 - ss_res / ss_tot if ss_tot > 0 else float("nan")
        fold_metrics.append({"fold": fold, "n_val": int(len(va_true)),
                             "mae": mae, "rmse": rmse, "r2": r2})
        print(f"  fold {fold+1} criterion-level: MAE={mae:.4f}  RMSE={rmse:.4f}  R^2={r2:.4f}")

    # ----- Full model on all labeled criteria; predict unlabeled -----
    print("\n=== Full model (all labeled criteria) ===")
    labeled_idx = np.where(is_labeled_train)[0]
    unlabeled_idx = np.where(~is_labeled_train)[0]
    print(f"  train: {len(labeled_idx):,}  inference target: {len(unlabeled_idx):,}")
    Xall = emb_t[torch.from_numpy(labeled_idx).to(device)]
    yall = torch.from_numpy(crit_labels[labeled_idx]).to(device)
    full_model = train_head(
        Xall, yall, None, None,
        epochs=args.epochs, batch_size=args.batch_size,
        lr=args.lr, weight_decay=args.weight_decay,
        device=device, verbose=True,
    )
    full_pred_unlabeled = predict(full_model, emb_t[torch.from_numpy(unlabeled_idx).to(device)],
                                  batch_size=args.eval_batch_size)
    all_scores = oof.copy()
    all_scores[unlabeled_idx] = full_pred_unlabeled
    n_nan = int(np.isnan(all_scores).sum())
    print(f"  remaining NaN scores: {n_nan}")

    # ----- Aggregate to per-trial features -----
    print("\nAggregating per-trial features ...")
    feats = aggregate_to_trial_features(meta, all_scores)
    print(f"  {len(feats):,} (trial_id, phase) rows")
    print(feats.head(3).to_string())

    # ----- Save -----
    np.save(run_dir / "oof_predictions.npy", all_scores)
    feats.to_parquet(run_dir / "ie_features.parquet", index=False)
    with (run_dir / "fold_metrics.json").open("w") as f:
        json.dump({
            "per_fold": fold_metrics,
            "mean_mae":  float(np.mean([m["mae"] for m in fold_metrics])),
            "mean_rmse": float(np.mean([m["rmse"] for m in fold_metrics])),
            "mean_r2":   float(np.mean([m["r2"] for m in fold_metrics])),
        }, f, indent=2)
    info = {
        "run_id": run_id,
        "emb_run": str(emb_run),
        "n_criteria": int(n_crit),
        "n_labeled_train_criteria": int(n_labeled),
        "n_trials_with_features": int(len(feats)),
        "elapsed_s": round(time.time() - t_start, 2),
        "args": vars(args),
    }
    with (run_dir / "run_info.json").open("w") as f:
        json.dump(info, f, indent=2)
    print(f"\nDone in {info['elapsed_s']:.1f}s")
    print(f"  ie_features:    {run_dir / 'ie_features.parquet'}")
    print(f"  oof_pred:       {run_dir / 'oof_predictions.npy'}")
    print(f"  fold_metrics:   {run_dir / 'fold_metrics.json'}")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--emb-run", required=True, help="Path to encode_medcpt_<TS> run directory")
    p.add_argument("--folds", type=int, default=5)
    p.add_argument("--epochs", type=int, default=20)
    p.add_argument("--batch-size", type=int, default=4096)
    p.add_argument("--eval-batch-size", type=int, default=16384)
    p.add_argument("--lr", type=float, default=1e-3)
    p.add_argument("--weight-decay", type=float, default=1e-4)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--device", default="cuda")
    args = p.parse_args()
    main(args)
