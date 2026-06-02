#!/usr/bin/env python3
"""
ablate_ie_features.py — A/B test: TabPFN on a TrialBench subtask, with and
without the 8 IE features (mean/max/std/n × {I, E}) from
criterion_head_stacking.

Supports three task types via --task-type:
  binary        TabPFNClassifier, ROC-AUC / PR-AUC / log-loss / accuracy
                 - serious-adverse-event-forecasting   --target Y/N
                 - mortality-event-prediction          --target Y/N
                 - patient-dropout-event-forecasting   --target Y/N
                 - trial-approval-forecasting          --target outcome
  multiclass    TabPFNClassifier, accuracy / macro-F1 / log-loss
                 - trial-failure-reason-identification --target failure_reason
  regression    TabPFNRegressor,  MAE / RMSE / R²
                 - trial-duration-forecasting          --target time_day

Reuses sae_finetune.preprocess for the X side; defines its own load_split.
"""

from __future__ import annotations

import argparse
import gc
import json
import sys
import time
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    f1_score,
    log_loss,
    mean_absolute_error,
    mean_squared_error,
    r2_score,
    roc_auc_score,
)

sys.path.insert(0, "/data2/zhu11/TB/script")
from sae_finetune import preprocess  # noqa: E402

DATA_ROOT    = Path("/data2/zhu11/TB/dataset/TrialBench")
CKPT_CLS     = Path("/data2/zhu11/TB/TabPFN/models/tabpfn-v2.5-classifier-v2.5_default.ckpt")
CKPT_REG     = Path("/data2/zhu11/TB/TabPFN/models/tabpfn-v2.5-regressor-v2.5_default.ckpt")
RESULTS_ROOT = Path("/data2/zhu11/TB/branch/IE_embedding/results")
PHASES       = ["Phase1", "Phase2", "Phase3", "Phase4"]
# Reserved (non-feature) columns in any ie_features parquet
META_COLS    = {"trial_id", "phase"}


# ---------- data loading ----------

def load_split(subtask: str, split: str, target: str, phases: list[str] | None = None):
    xs, ys = [], []
    for phase in (phases or PHASES):
        phase_dir = DATA_ROOT / subtask / phase
        if not phase_dir.is_dir():
            continue
        x = pd.read_csv(phase_dir / f"{split}_x.csv", index_col=0)
        y = pd.read_csv(phase_dir / f"{split}_y.csv", index_col=0)
        y = y.loc[x.index]
        x = x.assign(phase_split=phase)
        xs.append(x)
        ys.append(y[target])
    return pd.concat(xs, axis=0), pd.concat(ys, axis=0)


def add_ie_features(X: pd.DataFrame, ie: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    """Left-join `ie` (must have columns trial_id, phase, + numeric features) into X.
    Auto-detects feature columns as everything in `ie` except META_COLS.
    Returns (augmented_X, list_of_feature_cols)."""
    feat_cols = [c for c in ie.columns if c not in META_COLS]
    phase_str = X["phase_split"].astype(str)
    key = pd.DataFrame({"trial_id": X.index.astype(str), "phase": phase_str.values})
    merged = key.merge(ie, on=["trial_id", "phase"], how="left")
    out = X.copy()
    for c in feat_cols:
        out[c] = merged[c].astype(np.float32).values
    return out, feat_cols


# ---------- metrics ----------

def metrics_binary(y_true, proba):
    p1 = proba[:, 1]
    return {
        "roc_auc":  float(roc_auc_score(y_true, p1)),
        "pr_auc":   float(average_precision_score(y_true, p1)),
        "log_loss": float(log_loss(y_true, proba)),
        "accuracy": float(accuracy_score(y_true, p1 >= 0.5)),
    }


def metrics_multiclass(y_true, proba, labels):
    pred = proba.argmax(axis=1)
    pred_label = np.asarray(labels)[pred]
    return {
        "accuracy":      float(accuracy_score(y_true, pred_label)),
        "macro_f1":      float(f1_score(y_true, pred_label, average="macro")),
        "weighted_f1":   float(f1_score(y_true, pred_label, average="weighted")),
        "log_loss":      float(log_loss(y_true, proba, labels=list(labels))),
    }


def metrics_regression(y_true, pred):
    return {
        "mae":  float(mean_absolute_error(y_true, pred)),
        "rmse": float(np.sqrt(mean_squared_error(y_true, pred))),
        "r2":   float(r2_score(y_true, pred)),
    }


def report(name: str, m: dict[str, float]) -> None:
    parts = " ".join(f"{k}={v:.4f}" for k, v in m.items())
    print(f"[{name}] {parts}")


# ---------- TabPFN runners ----------

def run_classifier(X_train, y_train, X_test, *, n_estimators, seed):
    from tabpfn import TabPFNClassifier
    clf = TabPFNClassifier(
        device="cuda",
        n_estimators=n_estimators,
        ignore_pretraining_limits=True,
        inference_config={"SUBSAMPLE_SAMPLES": 50_000},
        random_state=seed,
        model_path=str(CKPT_CLS),
    )
    t0 = time.perf_counter()
    clf.fit(X_train, y_train)
    proba = clf.predict_proba(X_test)
    elapsed = time.perf_counter() - t0
    classes = list(clf.classes_)
    del clf
    gc.collect()
    torch.cuda.empty_cache()
    return proba, classes, elapsed


def run_regressor(X_train, y_train, X_test, *, n_estimators, seed):
    from tabpfn import TabPFNRegressor
    reg = TabPFNRegressor(
        device="cuda",
        n_estimators=n_estimators,
        ignore_pretraining_limits=True,
        inference_config={"SUBSAMPLE_SAMPLES": 50_000},
        random_state=seed,
        model_path=str(CKPT_REG),
    )
    t0 = time.perf_counter()
    reg.fit(X_train, y_train)
    pred = reg.predict(X_test)
    elapsed = time.perf_counter() - t0
    del reg
    gc.collect()
    torch.cuda.empty_cache()
    return pred, elapsed


# ---------- main ----------

def run_one(task_type, X_train, y_train, X_test, y_test, *, n_estimators, seed, label):
    if task_type == "binary":
        proba, classes, t = run_classifier(X_train, y_train.values.astype(int),
                                           X_test, n_estimators=n_estimators, seed=seed)
        m = metrics_binary(y_test.values.astype(int), proba)
    elif task_type == "multiclass":
        proba, classes, t = run_classifier(X_train, y_train.values,
                                           X_test, n_estimators=n_estimators, seed=seed)
        m = metrics_multiclass(y_test.values, proba, classes)
    elif task_type == "regression":
        pred, t = run_regressor(X_train, y_train.values.astype(np.float32),
                                X_test, n_estimators=n_estimators, seed=seed)
        m = metrics_regression(y_test.values.astype(np.float32), pred)
    else:
        raise ValueError(task_type)
    print(f"[{label}] fit+predict: {t:.1f}s")
    report(label, m)
    return m, t


def main(args):
    safe_subtask = args.subtask.replace("/", "_")
    safe_target  = args.target.replace("/", "")
    run_id = f"ablate_ie_{safe_subtask}_{safe_target}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    run_dir = RESULTS_ROOT / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    print(f"[run_id] {run_id}")
    print(f"[subtask] {args.subtask}  [target] {args.target}  [task-type] {args.task_type}")

    phases = [p.strip() for p in args.phases.split(",")] if args.phases else None
    print(f"  phases: {phases or PHASES}")
    print("Loading splits ...")
    X_train, y_train = load_split(args.subtask, "train", args.target, phases)
    X_test,  y_test  = load_split(args.subtask, "test",  args.target, phases)
    print(f"  train={X_train.shape}  test={X_test.shape}")
    if args.task_type in ("binary", "multiclass"):
        print(f"  train target counts: {y_train.value_counts().to_dict()}")
        print(f"  test  target counts: {y_test.value_counts().to_dict()}")
    else:
        print(f"  train target mean={y_train.mean():.1f} std={y_train.std():.1f}")
        print(f"  test  target mean={y_test.mean():.1f} std={y_test.std():.1f}")

    X_train_p, X_test_p = preprocess(X_train, X_test)
    print(f"  after preprocess: train {X_train_p.shape}  test {X_test_p.shape}")

    print("\n--- Variant A: baseline (no IE features) ---")
    m_a, t_a = run_one(args.task_type, X_train_p, y_train, X_test_p, y_test,
                       n_estimators=args.n_estimators, seed=args.seed, label="baseline")

    print("\n--- Variant B: + IE features ---")
    ie = pd.read_parquet(args.ie_features)
    X_train_b, feat_cols = add_ie_features(X_train_p, ie)
    X_test_b,  _         = add_ie_features(X_test_p,  ie)
    nan_train = int(X_train_b[feat_cols].isna().sum().sum())
    nan_test  = int(X_test_b[feat_cols].isna().sum().sum())
    print(f"  + {len(feat_cols)} IE feature columns from {args.ie_features}")
    print(f"  IE NaN cells (after join): train={nan_train}  test={nan_test}")
    print(f"  shapes: train {X_train_b.shape}  test {X_test_b.shape}")
    m_b, t_b = run_one(args.task_type, X_train_b, y_train, X_test_b, y_test,
                       n_estimators=args.n_estimators, seed=args.seed, label="with-IE")

    print("\n--- Delta (B - A) ---")
    lower_is_better = {"log_loss", "mae", "rmse"}
    for k in m_a:
        d = m_b[k] - m_a[k]
        if k in lower_is_better:
            note = "(better)" if d < 0 else "(worse)" if d > 0 else ""
        else:
            note = "(better)" if d > 0 else "(worse)" if d < 0 else ""
        print(f"  {k:<12s}: {m_a[k]:.4f} → {m_b[k]:.4f}  Δ={d:+.4f}  {note}")

    summary = {
        "run_id": run_id,
        "subtask": args.subtask, "target": args.target, "task_type": args.task_type,
        "ie_features_path": str(args.ie_features),
        "n_train": int(len(X_train)),
        "n_test":  int(len(X_test)),
        "n_features_baseline": int(X_train_p.shape[1]),
        "n_features_with_ie":  int(X_train_b.shape[1]),
        "baseline": {"time_s": t_a, **m_a},
        "with_ie":  {"time_s": t_b, **m_b},
        "delta":    {k: float(m_b[k] - m_a[k]) for k in m_a},
        "args":     vars(args),
    }
    with (run_dir / "metrics.json").open("w") as f:
        json.dump(summary, f, indent=2)
    print(f"\nSaved: {run_dir / 'metrics.json'}")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--ie-features", required=True)
    p.add_argument("--subtask", default="serious-adverse-event-forecasting")
    p.add_argument("--target",  default="Y/N")
    p.add_argument("--task-type", choices=["binary", "multiclass", "regression"], default="binary")
    p.add_argument("--phases", default=None,
                   help="Comma-sep subset of Phase1,Phase2,Phase3,Phase4 (default: all 4 concatenated)")
    p.add_argument("--n-estimators", type=int, default=2)
    p.add_argument("--seed", type=int, default=0)
    args = p.parse_args()
    main(args)
