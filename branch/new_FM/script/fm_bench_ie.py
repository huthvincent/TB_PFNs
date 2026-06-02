#!/usr/bin/env python3
"""
fm_bench_ie.py — IE A/B (baseline vs +IE 8 cols) on a TrialBench subtask,
single-phase, across all commercial-friendly tabular FMs available locally.

Supports three task types via --task-type:
  binary       (TabPFNClassifier ... MitraClassifier)
                 - serious-adverse-event-forecasting   --target Y/N
                 - mortality-event-prediction          --target Y/N
                 - patient-dropout-event-forecasting   --target Y/N
                 - trial-approval-forecasting          --target outcome
  multiclass   (same classifier path, K classes)
                 - trial-failure-reason-identification --target failure_reason
  regression   (TabPFNRegressor ... MitraRegressor)
                 - trial-duration-forecasting          --target time_day

Models tested (all zero-shot / in-context):
  TabPFN-v2.5     (project anchor; Prior Labs License — weights non-commercial)
  TabICLv2        (BSD-3 / MIT — INRIA Soda)
  TabDPT-v1.1     (Apache-2.0  — Layer 6 AI)
  Mitra           (Apache-2.0  — AWS / AutoGluon)

Pipeline mirrors branch/IE_embedding/script/ablate_ie_features.py:
  - same load_split + preprocess + add_ie_features
  - numeric-array conversion done once for non-TabPFN models (TabPFN handles
    pandas string dtype natively; the others need numeric ndarray)
  - y is LabelEncoded to int for classification (consistent column order across
    all four FMs) and cast to float32 for regression
  - IE features parquet defaults to criterion_head_20260520_155333/ie_features.parquet
    (8 cols: incl/excl × mean/max/std/n)
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
sys.path.insert(0, "/data2/zhu11/TB/branch/IE_embedding/script")
from sae_finetune import preprocess  # noqa: E402
from ablate_ie_features import (  # noqa: E402
    add_ie_features as _add_ie_pandas,
    load_split,
)

DATA_ROOT    = Path("/data2/zhu11/TB/dataset/TrialBench")
CKPT_CLS     = Path("/data2/zhu11/TB/TabPFN/models/tabpfn-v2.5-classifier-v2.5_default.ckpt")
CKPT_REG     = Path("/data2/zhu11/TB/TabPFN/models/tabpfn-v2.5-regressor-v2.5_default.ckpt")
RESULTS_ROOT = Path("/data2/zhu11/TB/branch/new_FM/results")
IE_FEATURES  = Path("/data2/zhu11/TB/branch/IE_embedding/results/criterion_head_20260520_155333/ie_features.parquet")


# ---------- preprocessing helpers ----------

def to_numeric_array(X_train: pd.DataFrame, X_test: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    """Convert preprocess()-output DataFrames to float32 ndarrays.

    Non-numeric columns → integer codes built on train+test union (NaN preserved).
    Numeric columns     → float32.
    """
    assert list(X_train.columns) == list(X_test.columns), "column mismatch"
    cols = list(X_train.columns)
    n_tr, n_te = len(X_train), len(X_test)
    out_tr = np.empty((n_tr, len(cols)), dtype=np.float32)
    out_te = np.empty((n_te, len(cols)), dtype=np.float32)
    for i, c in enumerate(cols):
        if pd.api.types.is_numeric_dtype(X_train[c]) and pd.api.types.is_numeric_dtype(X_test[c]):
            out_tr[:, i] = X_train[c].astype(np.float32).values
            out_te[:, i] = X_test[c].astype(np.float32).values
        else:
            combined = pd.concat([X_train[c].astype("object"), X_test[c].astype("object")], axis=0)
            codes = np.asarray(combined.astype("category").cat.codes, dtype=np.float32).copy()
            codes[codes == -1.0] = np.nan
            out_tr[:, i] = codes[:n_tr]
            out_te[:, i] = codes[n_tr:]
    return out_tr, out_te


def encode_y(y_train: pd.Series, y_test: pd.Series, task_type: str
             ) -> tuple[np.ndarray, np.ndarray, list | None]:
    """Encode y consistently across all FMs.

    binary      → int  (0/1)
    multiclass  → int  (0..K-1, sorted-unique order); returns label list
    regression  → float32
    """
    if task_type == "binary":
        return y_train.to_numpy().astype(int), y_test.to_numpy().astype(int), None
    if task_type == "regression":
        return (y_train.to_numpy().astype(np.float32),
                y_test.to_numpy().astype(np.float32), None)
    # multiclass
    classes = sorted(set(y_train.tolist()) | set(y_test.tolist()))
    cls_to_int = {c: i for i, c in enumerate(classes)}
    y_tr = np.asarray([cls_to_int[v] for v in y_train], dtype=np.int64)
    y_te = np.asarray([cls_to_int[v] for v in y_test], dtype=np.int64)
    return y_tr, y_te, classes


# ---------- metrics ----------

def metrics_binary(y_true, proba):
    p1 = proba[:, 1]
    return {
        "roc_auc":  float(roc_auc_score(y_true, p1)),
        "pr_auc":   float(average_precision_score(y_true, p1)),
        "log_loss": float(log_loss(y_true, proba)),
        "accuracy": float(accuracy_score(y_true, p1 >= 0.5)),
    }


def metrics_multiclass(y_true, proba, n_classes):
    pred = proba.argmax(axis=1)
    return {
        "accuracy":      float(accuracy_score(y_true, pred)),
        "macro_f1":      float(f1_score(y_true, pred, average="macro")),
        "weighted_f1":   float(f1_score(y_true, pred, average="weighted")),
        "log_loss":      float(log_loss(y_true, proba, labels=list(range(n_classes)))),
    }


def metrics_regression(y_true, pred):
    return {
        "mae":  float(mean_absolute_error(y_true, pred)),
        "rmse": float(np.sqrt(mean_squared_error(y_true, pred))),
        "r2":   float(r2_score(y_true, pred)),
    }


def compute_metrics(task_type, y_true, pred_or_proba, n_classes):
    if task_type == "binary":
        return metrics_binary(y_true, pred_or_proba)
    if task_type == "multiclass":
        return metrics_multiclass(y_true, pred_or_proba, n_classes)
    return metrics_regression(y_true, pred_or_proba)


# ---------- runners ----------

def _maybe_align_proba(proba: np.ndarray, classes_: np.ndarray | None, n_classes: int) -> np.ndarray:
    """Reorder proba columns to match [0, 1, ..., n_classes-1] order.

    If some class is missing in y_train (e.g. failure_reason "safety" rare in
    Phase3), pad with zeros so log_loss has full label support.
    """
    if classes_ is None:
        # no class info — assume already in [0..K-1] order
        return proba
    out = np.zeros((proba.shape[0], n_classes), dtype=np.float64)
    for col, c in enumerate(classes_):
        out[:, int(c)] = proba[:, col]
    return out


def run_tabpfn(X_train_df, y_train, X_test_df, *, task_type, n_estimators, seed, n_classes):
    if task_type == "regression":
        from tabpfn import TabPFNRegressor
        reg = TabPFNRegressor(
            device="cuda", n_estimators=n_estimators, ignore_pretraining_limits=True,
            inference_config={"SUBSAMPLE_SAMPLES": 50_000}, random_state=seed,
            model_path=str(CKPT_REG),
        )
        t0 = time.perf_counter()
        reg.fit(X_train_df, y_train)
        pred = reg.predict(X_test_df)
        elapsed = time.perf_counter() - t0
        del reg
        gc.collect(); torch.cuda.empty_cache()
        return pred, elapsed
    from tabpfn import TabPFNClassifier
    clf = TabPFNClassifier(
        device="cuda", n_estimators=n_estimators, ignore_pretraining_limits=True,
        inference_config={"SUBSAMPLE_SAMPLES": 50_000}, random_state=seed,
        model_path=str(CKPT_CLS),
    )
    t0 = time.perf_counter()
    clf.fit(X_train_df, y_train)
    proba = clf.predict_proba(X_test_df)
    proba = _maybe_align_proba(proba, np.asarray(clf.classes_), n_classes)
    elapsed = time.perf_counter() - t0
    del clf
    gc.collect(); torch.cuda.empty_cache()
    return proba, elapsed


def run_tabicl(X_train_arr, y_train, X_test_arr, *, task_type, n_estimators, seed, n_classes):
    if task_type == "regression":
        from tabicl import TabICLRegressor
        reg = TabICLRegressor(device="cuda", n_estimators=n_estimators,
                              random_state=seed, allow_auto_download=True)
        t0 = time.perf_counter()
        reg.fit(X_train_arr, y_train)
        pred = reg.predict(X_test_arr)
        elapsed = time.perf_counter() - t0
        del reg
        gc.collect(); torch.cuda.empty_cache()
        return pred, elapsed
    from tabicl import TabICLClassifier
    clf = TabICLClassifier(device="cuda", n_estimators=n_estimators,
                           random_state=seed, allow_auto_download=True)
    t0 = time.perf_counter()
    clf.fit(X_train_arr, y_train)
    proba = clf.predict_proba(X_test_arr)
    proba = _maybe_align_proba(proba, np.asarray(clf.classes_), n_classes)
    elapsed = time.perf_counter() - t0
    del clf
    gc.collect(); torch.cuda.empty_cache()
    return proba, elapsed


def run_tabdpt(X_train_arr, y_train, X_test_arr, *, task_type, context_size, seed, n_classes):
    if task_type == "regression":
        from tabdpt import TabDPTRegressor
        reg = TabDPTRegressor(device="cuda", verbose=False, compile=False)
        t0 = time.perf_counter()
        reg.fit(X_train_arr, y_train)
        pred = reg.predict(X_test_arr, context_size=context_size, seed=seed)
        elapsed = time.perf_counter() - t0
        del reg
        gc.collect(); torch.cuda.empty_cache()
        return pred, elapsed
    from tabdpt import TabDPTClassifier
    # We already encoded y to int — but TabDPT also re-uses its own class index
    classes_seen = np.unique(y_train)
    clf = TabDPTClassifier(device="cuda", verbose=False, compile=False)
    t0 = time.perf_counter()
    clf.fit(X_train_arr, y_train.astype(np.int64))
    proba = clf.predict_proba(X_test_arr, context_size=context_size, seed=seed)
    proba = _maybe_align_proba(proba, classes_seen, n_classes)
    elapsed = time.perf_counter() - t0
    del clf
    gc.collect(); torch.cuda.empty_cache()
    return proba, elapsed


def run_mitra(X_train_arr, y_train, X_test_arr, *, task_type, n_estimators, seed, n_classes):
    if task_type == "regression":
        from autogluon.tabular.models.mitra.sklearn_interface import MitraRegressor
        reg = MitraRegressor(device="cuda", fine_tune=False, n_estimators=n_estimators,
                             seed=seed, verbose=False)
        t0 = time.perf_counter()
        reg.fit(X_train_arr, y_train)
        pred = reg.predict(X_test_arr)
        elapsed = time.perf_counter() - t0
        del reg
        gc.collect(); torch.cuda.empty_cache()
        return pred, elapsed
    from autogluon.tabular.models.mitra.sklearn_interface import MitraClassifier
    classes_seen = np.unique(y_train)
    clf = MitraClassifier(device="cuda", fine_tune=False, n_estimators=n_estimators,
                          seed=seed, verbose=False)
    t0 = time.perf_counter()
    clf.fit(X_train_arr, y_train.astype(np.int64))
    proba = clf.predict_proba(X_test_arr)
    proba = _maybe_align_proba(proba, classes_seen, n_classes)
    elapsed = time.perf_counter() - t0
    del clf
    gc.collect(); torch.cuda.empty_cache()
    return proba, elapsed


# ---------- driver ----------

def main(args):
    safe_subtask = args.subtask.replace("/", "_")
    safe_target  = args.target.replace("/", "")
    run_id = f"fm_bench_ie_{safe_subtask}_{safe_target}_{args.phase}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
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
    echo(f"[ie_features] {args.ie_features}")

    X_train, y_train_raw = load_split(args.subtask, "train", args.target, [args.phase])
    X_test,  y_test_raw  = load_split(args.subtask, "test",  args.target, [args.phase])
    echo(f"  train={X_train.shape}  test={X_test.shape}")
    if args.task_type in ("binary", "multiclass"):
        echo(f"  train target counts: {y_train_raw.value_counts().to_dict()}")
        echo(f"  test  target counts: {y_test_raw.value_counts().to_dict()}")
    else:
        echo(f"  train target mean={float(y_train_raw.mean()):.1f} std={float(y_train_raw.std()):.1f}")
        echo(f"  test  target mean={float(y_test_raw.mean()):.1f} std={float(y_test_raw.std()):.1f}")

    # Baseline preprocess.
    X_train_p, X_test_p = preprocess(X_train, X_test)
    n_non_numeric = sum(not pd.api.types.is_numeric_dtype(X_train_p[c]) for c in X_train_p.columns)
    echo(f"  after preprocess: train {X_train_p.shape}  test {X_test_p.shape}  "
         f"non-numeric cols {n_non_numeric}/{X_train_p.shape[1]}")

    # +IE variant.
    ie = pd.read_parquet(args.ie_features)
    X_train_b, feat_cols = _add_ie_pandas(X_train_p, ie)
    X_test_b,  _         = _add_ie_pandas(X_test_p,  ie)
    nan_train = int(X_train_b[feat_cols].isna().sum().sum())
    nan_test  = int(X_test_b[feat_cols].isna().sum().sum())
    echo(f"  +IE: {len(feat_cols)} IE cols; NaN cells train={nan_train} test={nan_test}; "
         f"shapes train {X_train_b.shape}  test {X_test_b.shape}")

    # Numeric arrays for non-TabPFN models.
    X_tr_arr_a, X_te_arr_a = to_numeric_array(X_train_p, X_test_p)
    X_tr_arr_b, X_te_arr_b = to_numeric_array(X_train_b, X_test_b)

    # y encoding (shared by all models).
    y_tr, y_te, classes = encode_y(y_train_raw, y_test_raw, args.task_type)
    n_classes = len(classes) if classes is not None else (2 if args.task_type == "binary" else 1)
    if args.task_type == "multiclass":
        echo(f"  multiclass label set ({n_classes}): {classes}")

    runners = {
        "tabpfn": lambda Xtr_df, Xte_df, Xtr_arr, Xte_arr:
            run_tabpfn(Xtr_df, y_tr, Xte_df, task_type=args.task_type,
                       n_estimators=args.tabpfn_n_estimators, seed=args.seed,
                       n_classes=n_classes),
        "tabicl": lambda Xtr_df, Xte_df, Xtr_arr, Xte_arr:
            run_tabicl(Xtr_arr, y_tr, Xte_arr, task_type=args.task_type,
                       n_estimators=args.tabicl_n_estimators, seed=args.seed,
                       n_classes=n_classes),
        "tabdpt": lambda Xtr_df, Xte_df, Xtr_arr, Xte_arr:
            run_tabdpt(Xtr_arr, y_tr, Xte_arr, task_type=args.task_type,
                       context_size=args.tabdpt_context_size, seed=args.seed,
                       n_classes=n_classes),
        "mitra":  lambda Xtr_df, Xte_df, Xtr_arr, Xte_arr:
            run_mitra(Xtr_arr, y_tr, Xte_arr, task_type=args.task_type,
                      n_estimators=args.mitra_n_estimators, seed=args.seed,
                      n_classes=n_classes),
    }

    results: dict[str, dict[str, dict]] = {}
    for model in args.models:
        echo(f"\n=== {model.upper()} ===")
        pred_a, t_a = runners[model](X_train_p, X_test_p, X_tr_arr_a, X_te_arr_a)
        m_a = compute_metrics(args.task_type, y_te, pred_a, n_classes)
        echo(f"[{model}] baseline t={t_a:.1f}s  " + " ".join(f"{k}={v:.4f}" for k, v in m_a.items()))
        pred_b, t_b = runners[model](X_train_b, X_test_b, X_tr_arr_b, X_te_arr_b)
        m_b = compute_metrics(args.task_type, y_te, pred_b, n_classes)
        echo(f"[{model}] + IE     t={t_b:.1f}s  " + " ".join(f"{k}={v:.4f}" for k, v in m_b.items()))
        # Deltas (signs depend on metric direction).
        lower_is_better = {"log_loss", "mae", "rmse"}
        delta = {k: float(m_b[k] - m_a[k]) for k in m_a}
        echo("[{}] Δ {}".format(model,
            "  ".join(f"{k}={d:+.4f}" + ("(better)" if (d < 0) == (k in lower_is_better) else "(worse)")
                     for k, d in delta.items())))
        results[model] = {
            "baseline": {"time_s": t_a, **m_a},
            "with_ie":  {"time_s": t_b, **m_b},
            "delta":    delta,
        }

    summary = {
        "run_id": run_id,
        "subtask": args.subtask,
        "target": args.target,
        "task_type": args.task_type,
        "phase": args.phase,
        "ie_features_path": str(args.ie_features),
        "n_train": int(len(X_train)),
        "n_test":  int(len(X_test)),
        "n_features_baseline": int(X_train_p.shape[1]),
        "n_features_with_ie": int(X_train_b.shape[1]),
        "n_non_numeric_baseline": int(n_non_numeric),
        "multiclass_classes": classes,
        "models": results,
        "args": vars(args),
    }
    out = run_dir / "metrics.json"
    out.write_text(json.dumps(summary, indent=2))
    echo(f"\nSaved: {out}")
    log_f.close()


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--subtask", required=True)
    p.add_argument("--target",  required=True)
    p.add_argument("--task-type", choices=["binary", "multiclass", "regression"], required=True)
    p.add_argument("--phase",   required=True, choices=["Phase1", "Phase2", "Phase3", "Phase4"])
    p.add_argument("--ie-features", default=str(IE_FEATURES))
    p.add_argument("--models", default="tabpfn,tabicl,tabdpt,mitra",
                   help="Comma-sep subset of {tabpfn,tabicl,tabdpt,mitra}")
    p.add_argument("--tabpfn-n-estimators",  type=int, default=2)
    p.add_argument("--tabicl-n-estimators",  type=int, default=8)
    p.add_argument("--tabdpt-context-size",  type=int, default=2048)
    p.add_argument("--mitra-n-estimators",   type=int, default=1)
    p.add_argument("--seed", type=int, default=0)
    args = p.parse_args()
    args.models = [m.strip() for m in args.models.split(",") if m.strip()]
    main(args)
