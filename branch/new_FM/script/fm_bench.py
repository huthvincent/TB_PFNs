#!/usr/bin/env python3
"""
fm_bench.py — three-way zero-shot comparison on a TrialBench subtask:

  TabPFN-v2.5  (current baseline; non-commercial weights)
  TabICLv2     (BSD-3, INRIA Soda)
  TabDPT-v1.1  (Apache-2.0, Layer 6 AI)

Uses the same data loader and `preprocess()` as branch/IE_embedding/script/ablate_ie_features.py
so numbers are directly comparable to project history.

Category dtype handling: TabPFN takes pandas with category natively; TabICL/TabDPT
take numeric arrays, so we encode categories → integer codes (NaN preserved).
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

# Reuse existing project plumbing.
sys.path.insert(0, "/data2/zhu11/TB/script")
sys.path.insert(0, "/data2/zhu11/TB/branch/IE_embedding/script")
from sae_finetune import preprocess  # noqa: E402
from ablate_ie_features import (  # noqa: E402
    load_split,
    metrics_binary,
    metrics_multiclass,
    metrics_regression,
    report,
)

DATA_ROOT    = Path("/data2/zhu11/TB/dataset/TrialBench")
CKPT_CLS     = Path("/data2/zhu11/TB/TabPFN/models/tabpfn-v2.5-classifier-v2.5_default.ckpt")
CKPT_REG     = Path("/data2/zhu11/TB/TabPFN/models/tabpfn-v2.5-regressor-v2.5_default.ckpt")
RESULTS_ROOT = Path("/data2/zhu11/TB/branch/new_FM/results")


# ---------- category → numeric for TabICL / TabDPT ----------

def to_numeric_array(
    X_train: pd.DataFrame, X_test: pd.DataFrame
) -> tuple[np.ndarray, np.ndarray, list[str]]:
    """Convert preprocess()-output DataFrames to float32 ndarrays for TabICL/TabDPT.

    Categorical / string / object columns → category codes built on train+test
    union (so a test-only category does not collide with -1=missing). NaN preserved
    as np.nan. Numeric columns → float32.
    """
    assert list(X_train.columns) == list(X_test.columns), "column mismatch"
    cols = list(X_train.columns)
    n_tr, n_te = len(X_train), len(X_test)
    out_tr = np.empty((n_tr, len(cols)), dtype=np.float32)
    out_te = np.empty((n_te, len(cols)), dtype=np.float32)
    for i, c in enumerate(cols):
        ctr, cte = X_train[c], X_test[c]
        if pd.api.types.is_numeric_dtype(ctr) and pd.api.types.is_numeric_dtype(cte):
            out_tr[:, i] = ctr.astype(np.float32).values
            out_te[:, i] = cte.astype(np.float32).values
        else:
            # union categorical: stable codes across train/test
            combined = pd.concat([ctr.astype("object"), cte.astype("object")], axis=0)
            cat = combined.astype("category")
            codes = np.asarray(cat.cat.codes, dtype=np.float32).copy()
            codes[codes == -1.0] = np.nan
            out_tr[:, i] = codes[:n_tr]
            out_te[:, i] = codes[n_tr:]
    return out_tr, out_te, cols


# ---------- runners ----------

def run_tabpfn(X_train, y_train, X_test, *, task_type, n_estimators, seed):
    """Pandas in (category-aware); returns (proba_or_pred, classes_or_None, elapsed)."""
    if task_type == "regression":
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
    else:
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
        pred = clf.predict_proba(X_test)
        classes = list(clf.classes_)
        elapsed = time.perf_counter() - t0
        del clf
        gc.collect(); torch.cuda.empty_cache()
        return pred, classes, elapsed
    gc.collect(); torch.cuda.empty_cache()
    return pred, None, elapsed


def run_tabicl(X_train_arr, y_train, X_test_arr, *, task_type, n_estimators, seed):
    """ndarray in; n_estimators=8 by default in library, we expose it for fairness."""
    if task_type == "regression":
        from tabicl import TabICLRegressor
        reg = TabICLRegressor(
            device="cuda",
            n_estimators=n_estimators,
            random_state=seed,
            allow_auto_download=True,
        )
        t0 = time.perf_counter()
        reg.fit(X_train_arr, y_train)
        pred = reg.predict(X_test_arr)
        elapsed = time.perf_counter() - t0
        del reg
        gc.collect(); torch.cuda.empty_cache()
        return pred, None, elapsed
    else:
        from tabicl import TabICLClassifier
        clf = TabICLClassifier(
            device="cuda",
            n_estimators=n_estimators,
            random_state=seed,
            allow_auto_download=True,
        )
        t0 = time.perf_counter()
        clf.fit(X_train_arr, y_train)
        proba = clf.predict_proba(X_test_arr)
        classes = list(clf.classes_)
        elapsed = time.perf_counter() - t0
        del clf
        gc.collect(); torch.cuda.empty_cache()
        return proba, classes, elapsed


def run_tabdpt(X_train_arr, y_train, X_test_arr, *, task_type, context_size, seed, compile_):
    """ndarray in; default 8 ensembles, torch.compile gated by `compile_`.

    TabDPT (unlike TabICL) does *not* run a LabelEncoder internally, so for
    multiclass we encode string labels to int here and report the proba columns
    back in the original class order.
    """
    if task_type == "regression":
        from tabdpt import TabDPTRegressor
        reg = TabDPTRegressor(device="cuda", verbose=False, compile=compile_)
        t0 = time.perf_counter()
        reg.fit(X_train_arr, y_train)
        pred = reg.predict(X_test_arr, context_size=context_size, seed=seed)
        elapsed = time.perf_counter() - t0
        del reg
        gc.collect(); torch.cuda.empty_cache()
        return pred, None, elapsed
    else:
        from tabdpt import TabDPTClassifier
        # Encode labels to int (handles both binary-int and multiclass-string).
        classes = np.unique(y_train)
        cls_to_int = {c: i for i, c in enumerate(classes)}
        y_train_int = np.asarray([cls_to_int[v] for v in y_train], dtype=np.int64)
        clf = TabDPTClassifier(device="cuda", verbose=False, compile=compile_)
        t0 = time.perf_counter()
        clf.fit(X_train_arr, y_train_int)
        proba = clf.predict_proba(X_test_arr, context_size=context_size, seed=seed)
        elapsed = time.perf_counter() - t0
        del clf
        gc.collect(); torch.cuda.empty_cache()
        return proba, list(classes), elapsed


# ---------- driver ----------

def compute_metrics(task_type, y_true, pred_or_proba, classes):
    if task_type == "binary":
        return metrics_binary(np.asarray(y_true).astype(int), pred_or_proba)
    if task_type == "multiclass":
        return metrics_multiclass(np.asarray(y_true), pred_or_proba, classes)
    if task_type == "regression":
        return metrics_regression(np.asarray(y_true).astype(np.float32),
                                  np.asarray(pred_or_proba).astype(np.float32))
    raise ValueError(task_type)


def main(args):
    safe_subtask = args.subtask.replace("/", "_")
    safe_target  = args.target.replace("/", "")
    run_id = f"fm_bench_{safe_subtask}_{safe_target}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    run_dir = RESULTS_ROOT / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    log_path = run_dir / "log.txt"
    log_f = open(log_path, "w")

    def echo(*parts):
        line = " ".join(str(p) for p in parts)
        print(line)
        print(line, file=log_f, flush=True)

    echo(f"[run_id] {run_id}")
    echo(f"[subtask] {args.subtask}  [target] {args.target}  [task-type] {args.task_type}")

    phases = [p.strip() for p in args.phases.split(",")] if args.phases else None
    echo(f"  phases: {phases or ['Phase1','Phase2','Phase3','Phase4']}")

    echo("Loading splits ...")
    X_train, y_train = load_split(args.subtask, "train", args.target, phases)
    X_test,  y_test  = load_split(args.subtask, "test",  args.target, phases)
    echo(f"  train={X_train.shape}  test={X_test.shape}")
    if args.task_type in ("binary", "multiclass"):
        echo(f"  train target counts: {y_train.value_counts().to_dict()}")
        echo(f"  test  target counts: {y_test.value_counts().to_dict()}")
    else:
        echo(f"  train target mean={float(y_train.mean()):.1f} std={float(y_train.std()):.1f}")
        echo(f"  test  target mean={float(y_test.mean()):.1f} std={float(y_test.std()):.1f}")

    X_train_p, X_test_p = preprocess(X_train, X_test)
    echo(f"  after preprocess: train {X_train_p.shape}  test {X_test_p.shape}")
    n_non_numeric = sum(
        not pd.api.types.is_numeric_dtype(X_train_p[c]) for c in X_train_p.columns
    )
    echo(f"  non-numeric columns (will be ordinal-encoded for ICL/DPT): "
         f"{n_non_numeric} / {X_train_p.shape[1]}")

    # Numeric copies for TabICL/TabDPT (TabPFN takes pandas-with-strings natively).
    X_train_arr, X_test_arr, _ = to_numeric_array(X_train_p, X_test_p)
    nan_train = int(np.isnan(X_train_arr).sum())
    nan_test  = int(np.isnan(X_test_arr).sum())
    echo(f"  numeric array: train {X_train_arr.shape}  test {X_test_arr.shape}  "
         f"NaN train={nan_train} test={nan_test}")

    # Cast y for binary so TabPFN gets integer labels (project convention).
    if args.task_type == "binary":
        y_train_for_model = y_train.to_numpy().astype(int)
    elif args.task_type == "regression":
        y_train_for_model = y_train.to_numpy().astype(np.float32)
    else:  # multiclass — keep labels; force np.ndarray (PyArrow strings break TabDPT)
        y_train_for_model = np.asarray(y_train.to_numpy(), dtype=object)
    y_test_arr = np.asarray(y_test.to_numpy()) if args.task_type != "multiclass" \
                 else np.asarray(y_test.to_numpy(), dtype=object)

    results = {}

    # ----- TabPFN -----
    if "tabpfn" in args.models:
        echo("\n--- TabPFN-v2.5 ---")
        pred, classes, t = run_tabpfn(
            X_train_p, y_train_for_model, X_test_p,
            task_type=args.task_type, n_estimators=args.tabpfn_n_estimators, seed=args.seed,
        )
        m = compute_metrics(args.task_type, y_test_arr, pred, classes)
        echo(f"[tabpfn] time={t:.1f}s  " + " ".join(f"{k}={v:.4f}" for k, v in m.items()))
        results["tabpfn"] = {"time_s": t, "n_estimators": args.tabpfn_n_estimators, **m}

    # ----- TabICL -----
    if "tabicl" in args.models:
        echo("\n--- TabICLv2 ---")
        pred, classes, t = run_tabicl(
            X_train_arr, y_train_for_model, X_test_arr,
            task_type=args.task_type, n_estimators=args.tabicl_n_estimators, seed=args.seed,
        )
        m = compute_metrics(args.task_type, y_test_arr, pred, classes)
        echo(f"[tabicl] time={t:.1f}s  " + " ".join(f"{k}={v:.4f}" for k, v in m.items()))
        results["tabicl"] = {"time_s": t, "n_estimators": args.tabicl_n_estimators, **m}

    # ----- TabDPT -----
    if "tabdpt" in args.models:
        echo("\n--- TabDPT-v1.1 ---")
        pred, classes, t = run_tabdpt(
            X_train_arr, y_train_for_model, X_test_arr,
            task_type=args.task_type, context_size=args.tabdpt_context_size,
            seed=args.seed, compile_=args.tabdpt_compile,
        )
        m = compute_metrics(args.task_type, y_test_arr, pred, classes)
        echo(f"[tabdpt] time={t:.1f}s  " + " ".join(f"{k}={v:.4f}" for k, v in m.items()))
        results["tabdpt"] = {"time_s": t, "context_size": args.tabdpt_context_size, **m}

    summary = {
        "run_id": run_id,
        "subtask": args.subtask,
        "target": args.target,
        "task_type": args.task_type,
        "n_train": int(len(X_train)),
        "n_test":  int(len(X_test)),
        "n_features_after_preprocess": int(X_train_p.shape[1]),
        "n_non_numeric_columns": int(n_non_numeric),
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
    p.add_argument("--phases", default=None, help="Comma-sep subset of Phase1..4 (default: all 4)")
    p.add_argument("--models", default="tabpfn,tabicl,tabdpt",
                   help="Comma-sep subset of {tabpfn,tabicl,tabdpt}")
    p.add_argument("--tabpfn-n-estimators", type=int, default=2,
                   help="Match IE_embedding ablate default (project baseline ROC-AUC 0.8851)")
    p.add_argument("--tabicl-n-estimators", type=int, default=8,
                   help="TabICL library default")
    p.add_argument("--tabdpt-context-size", type=int, default=2048,
                   help="TabDPT library default; ensemble is hardcoded to 8")
    p.add_argument("--tabdpt-compile", action="store_true",
                   help="Pass compile=True to TabDPT (triton autotune; off by default — "
                        "we hit CUDA invalid-argument on H200 with this on)")
    p.add_argument("--seed", type=int, default=0)
    args = p.parse_args()
    args.models = [m.strip() for m in args.models.split(",") if m.strip()]
    main(args)
