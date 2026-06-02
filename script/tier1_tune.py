"""Tier 1 professional tuning of TabPFN on TrialBench subtasks.

Per task (all decisions made on a held-out val split from train; test untouched
until final eval):

  Phase A — baseline sweep over (ckpt × n_estimators); regression also tries log1p target.
  Phase B — fine-tune both ckpts at lr ∈ {1e-5, 2e-5, 5e-5} with X_val early stop.
  Phase C — ensemble seeds {0,1,2} of the val-winning config.
  Phase D — binary tasks: tune classification threshold on val for accuracy.
  Final  — single test eval; compare against the original Tier-0 baseline.

Outputs to /data2/zhu11/TB/results/TrialBench_TabPFN_tier1/.
Does NOT keep model checkpoints (fine-tune ckpts use a tempdir).
"""

from __future__ import annotations

import argparse
import gc
import json
import sys
import tempfile
import time
import traceback
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
from sklearn.model_selection import train_test_split

from tabpfn import TabPFNClassifier, TabPFNRegressor
from tabpfn.finetuning.finetuned_classifier import FinetunedTabPFNClassifier
from tabpfn.finetuning.finetuned_regressor import FinetunedTabPFNRegressor

# Reuse config + helpers from the Tier-0 sweep.
sys.path.insert(0, str(Path(__file__).parent))
from trialbench_zero_shot_table import (  # noqa: E402
    TASKS,
    NOT_APPLICABLE,
    load_split,
    preprocess,
    drop_y_nan,
)

OUT_DIR = Path("/data2/zhu11/TB/results/TrialBench_TabPFN_tier1")
PER_TASK_DIR = OUT_DIR / "per_task"

CLASSIFIER_CKPTS = {
    "default": "/data2/zhu11/TB/TabPFN/models/tabpfn-v2.5-classifier-v2.5_default.ckpt",
    "default-2": "/data2/zhu11/TB/TabPFN/models/tabpfn-v2.5-classifier-v2.5_default-2.ckpt",
}
REGRESSOR_CKPTS = {
    "default": "/data2/zhu11/TB/TabPFN/models/tabpfn-v2.5-regressor-v2.5_default.ckpt",
    "real": "/data2/zhu11/TB/TabPFN/models/tabpfn-v2.5-regressor-v2.5_real.ckpt",
}

INFERENCE_CONFIG = {"SUBSAMPLE_SAMPLES": 50_000}

# The numbers driving the headline comparison ("primary" = higher is better).
PRIMARY = {"binary": "roc_auc", "multiclass": "accuracy", "regression": "r2"}


# ----------------------------------------------------------------------------
# Metric helpers
# ----------------------------------------------------------------------------

def cls_metrics(y_true, proba, classes) -> dict:
    pred = classes[proba.argmax(axis=1)]
    out = {
        "accuracy": float(accuracy_score(y_true, pred)),
        "log_loss": float(log_loss(y_true, proba, labels=list(classes))),
    }
    if len(classes) == 2:
        p_pos = proba[:, 1]
        out["roc_auc"] = float(roc_auc_score(y_true == classes[1], p_pos))
        out["pr_auc"] = float(
            average_precision_score(y_true == classes[1], p_pos)
        )
    else:
        out["f1_macro"] = float(f1_score(y_true, pred, average="macro"))
    return out


def reg_metrics(y_true, y_pred) -> dict:
    return {
        "mae": float(mean_absolute_error(y_true, y_pred)),
        "rmse": float(np.sqrt(mean_squared_error(y_true, y_pred))),
        "r2": float(r2_score(y_true, y_pred)),
    }


# ----------------------------------------------------------------------------
# Per-config evaluators
# ----------------------------------------------------------------------------

def cls_predict_proba(
    X_train_p, y_train_p, X_eval, *, ckpt_path: str, n_est: int, seed: int
) -> tuple[np.ndarray, np.ndarray]:
    clf = TabPFNClassifier(
        device="cuda",
        n_estimators=n_est,
        ignore_pretraining_limits=True,
        inference_config=INFERENCE_CONFIG,
        random_state=seed,
        model_path=ckpt_path,
    )
    clf.fit(X_train_p, y_train_p)
    proba = clf.predict_proba(X_eval)
    classes = clf.classes_
    del clf
    gc.collect()
    torch.cuda.empty_cache()
    return proba, classes


def reg_predict(
    X_train_p, y_train_p, X_eval, *, ckpt_path: str, n_est: int, seed: int,
    y_log: bool,
) -> np.ndarray:
    y_fit = np.log1p(y_train_p) if y_log else y_train_p
    reg = TabPFNRegressor(
        device="cuda",
        n_estimators=n_est,
        ignore_pretraining_limits=True,
        inference_config=INFERENCE_CONFIG,
        random_state=seed,
        model_path=ckpt_path,
    )
    reg.fit(X_train_p, y_fit)
    pred = reg.predict(X_eval)
    if y_log:
        pred = np.expm1(pred)
    del reg
    gc.collect()
    torch.cuda.empty_cache()
    return pred


def cls_finetune(
    X_train_p, y_train_p, X_val, y_val, *,
    ckpt_path: str, lr: float, epochs: int, n_est_ft: int, seed: int,
    tmp_dir: Path,
) -> str | None:
    """Fine-tune classifier on (train', val); returns path to best-on-val ckpt."""
    ft = FinetunedTabPFNClassifier(
        device="cuda",
        epochs=epochs,
        learning_rate=lr,
        n_estimators_finetune=n_est_ft,
        n_estimators_validation=n_est_ft,
        n_estimators_final_inference=n_est_ft,
        random_state=seed,
        extra_classifier_kwargs={
            "ignore_pretraining_limits": True,
            "inference_config": INFERENCE_CONFIG,
            "model_path": ckpt_path,
        },
    )
    ft.fit(X_train_p, y_train_p, X_val=X_val, y_val=y_val, output_dir=tmp_dir)
    best = sorted(tmp_dir.glob("*_best.pth"), key=lambda p: p.stat().st_mtime)
    del ft
    gc.collect()
    torch.cuda.empty_cache()
    return str(best[-1]) if best else None


def cls_finetune_full(
    X_full, y_full, *,
    ckpt_path: str, lr: float, epochs: int, n_est_ft: int, seed: int,
    tmp_dir: Path,
) -> str:
    """Refit fine-tune on the full train set (no val). Returns path to last ckpt."""
    ft = FinetunedTabPFNClassifier(
        device="cuda",
        epochs=epochs,
        learning_rate=lr,
        n_estimators_finetune=n_est_ft,
        n_estimators_validation=n_est_ft,
        n_estimators_final_inference=n_est_ft,
        random_state=seed,
        early_stopping=False,
        save_checkpoint_interval=epochs,  # save once at the very end
        extra_classifier_kwargs={
            "ignore_pretraining_limits": True,
            "inference_config": INFERENCE_CONFIG,
            "model_path": ckpt_path,
        },
    )
    ft.fit(X_full, y_full, output_dir=tmp_dir)
    saved = sorted(tmp_dir.glob("*.pth"), key=lambda p: p.stat().st_mtime)
    del ft
    gc.collect()
    torch.cuda.empty_cache()
    if not saved:
        raise RuntimeError(f"Full-train refit produced no checkpoint in {tmp_dir}")
    return str(saved[-1])


def reg_finetune(
    X_train_p, y_train_p, X_val, y_val, *,
    ckpt_path: str, lr: float, epochs: int, n_est_ft: int, seed: int,
    tmp_dir: Path, y_log: bool,
) -> str | None:
    y_fit = np.log1p(y_train_p) if y_log else y_train_p
    y_val_fit = np.log1p(y_val) if y_log else y_val
    ft = FinetunedTabPFNRegressor(
        device="cuda",
        epochs=epochs,
        learning_rate=lr,
        n_estimators_finetune=n_est_ft,
        n_estimators_validation=n_est_ft,
        n_estimators_final_inference=n_est_ft,
        random_state=seed,
        extra_regressor_kwargs={
            "ignore_pretraining_limits": True,
            "inference_config": INFERENCE_CONFIG,
            "model_path": ckpt_path,
        },
    )
    ft.fit(X_train_p, y_fit, X_val=X_val, y_val=y_val_fit, output_dir=tmp_dir)
    best = sorted(tmp_dir.glob("*_best.pth"), key=lambda p: p.stat().st_mtime)
    del ft
    gc.collect()
    torch.cuda.empty_cache()
    return str(best[-1]) if best else None


def reg_finetune_full(
    X_full, y_full, *,
    ckpt_path: str, lr: float, epochs: int, n_est_ft: int, seed: int,
    tmp_dir: Path, y_log: bool,
) -> str:
    y_fit = np.log1p(y_full) if y_log else y_full
    ft = FinetunedTabPFNRegressor(
        device="cuda",
        epochs=epochs,
        learning_rate=lr,
        n_estimators_finetune=n_est_ft,
        n_estimators_validation=n_est_ft,
        n_estimators_final_inference=n_est_ft,
        random_state=seed,
        early_stopping=False,
        save_checkpoint_interval=epochs,
        extra_regressor_kwargs={
            "ignore_pretraining_limits": True,
            "inference_config": INFERENCE_CONFIG,
            "model_path": ckpt_path,
        },
    )
    ft.fit(X_full, y_fit, output_dir=tmp_dir)
    saved = sorted(tmp_dir.glob("*.pth"), key=lambda p: p.stat().st_mtime)
    del ft
    gc.collect()
    torch.cuda.empty_cache()
    if not saved:
        raise RuntimeError(f"Full-train refit produced no checkpoint in {tmp_dir}")
    return str(saved[-1])


# ----------------------------------------------------------------------------
# Main per-task pipeline
# ----------------------------------------------------------------------------

def run_classification_task(task, args) -> dict:
    name, t_type = task["name"], task["type"]
    primary = PRIMARY[t_type]
    print(f"\n=== {name} ({t_type}) ===")

    X_train, y_train = load_split(task, "train")
    X_test, y_test = load_split(task, "test")
    X_train, y_train = drop_y_nan(X_train, y_train)
    X_test, y_test = drop_y_nan(X_test, y_test)
    X_train, X_test = preprocess(X_train, X_test)
    y_train_arr = y_train.values
    y_test_arr = y_test.values

    X_tp, X_val, y_tp, y_val = train_test_split(
        X_train, y_train_arr,
        test_size=0.2, random_state=args.seed,
        stratify=y_train_arr,
    )
    print(f"  train' {X_tp.shape}, val {X_val.shape}, test {X_test.shape}")

    record = {
        "task": name, "type": t_type, "target": task["target"],
        "n_classes": int(pd.Series(y_train_arr).nunique()),
        "n_train_full": int(len(X_train)),
        "n_train_p": int(len(X_tp)),
        "n_val": int(len(X_val)),
        "n_test": int(len(X_test)),
        "phase_a": [], "phase_b": [], "phase_c": None, "test": None,
    }

    # val_probas indexed by config key — used by Phase D for threshold tuning.
    val_probas: dict[tuple, np.ndarray] = {}
    classes_ref: np.ndarray | None = None

    # ---------- Phase A: baseline sweep ----------
    print("  Phase A — baseline sweep (ckpt × n_estimators)")
    for ckpt_name, ckpt_path in CLASSIFIER_CKPTS.items():
        for n_est in args.n_est_grid:
            t0 = time.perf_counter()
            proba, classes = cls_predict_proba(
                X_tp, y_tp, X_val,
                ckpt_path=ckpt_path, n_est=n_est, seed=args.seed,
            )
            m = cls_metrics(y_val, proba, classes)
            m.update({"ckpt": ckpt_name, "n_estimators": n_est,
                      "time_s": time.perf_counter() - t0})
            record["phase_a"].append(m)
            val_probas[("A", ckpt_name, n_est)] = proba
            classes_ref = classes
            print(f"    A: ckpt={ckpt_name} n_est={n_est:>2} val[{primary}]={m[primary]:.4f}")

    # ---------- Phase B: fine-tune sweep ----------
    print("  Phase B — fine-tune sweep (ckpt × lr)")
    # Pick best n_est for inference from Phase A (per ckpt) — use same ckpt's best.
    a_by_ckpt: dict[str, dict] = {}
    for r in record["phase_a"]:
        cur = a_by_ckpt.get(r["ckpt"])
        if cur is None or r[primary] > cur[primary]:
            a_by_ckpt[r["ckpt"]] = r

    for ckpt_name, ckpt_path in CLASSIFIER_CKPTS.items():
        n_est_inf = a_by_ckpt[ckpt_name]["n_estimators"]
        baseline_for_ckpt = a_by_ckpt[ckpt_name]
        for lr in args.lr_grid:
            with tempfile.TemporaryDirectory() as tmp_str:
                tmp = Path(tmp_str)
                t0 = time.perf_counter()
                try:
                    best_path = cls_finetune(
                        X_tp, y_tp, X_val, y_val,
                        ckpt_path=ckpt_path, lr=lr, epochs=args.ft_epochs,
                        n_est_ft=args.n_est_ft, seed=args.seed, tmp_dir=tmp,
                    )
                    if best_path is None:
                        m = {k: v for k, v in baseline_for_ckpt.items()
                             if k not in ("ckpt", "n_estimators", "time_s")}
                        m.update({"ckpt": ckpt_name, "lr": lr,
                                  "n_estimators": n_est_inf,
                                  "time_s": time.perf_counter() - t0,
                                  "no_improvement": True})
                    else:
                        proba, classes = cls_predict_proba(
                            X_tp, y_tp, X_val,
                            ckpt_path=best_path, n_est=n_est_inf, seed=args.seed,
                        )
                        m = cls_metrics(y_val, proba, classes)
                        m.update({"ckpt": ckpt_name, "lr": lr,
                                  "n_estimators": n_est_inf,
                                  "time_s": time.perf_counter() - t0,
                                  "best_ckpt_basename": Path(best_path).name})
                        val_probas[("B", ckpt_name, lr, n_est_inf)] = proba
                except Exception as e:  # noqa: BLE001
                    m = {"ckpt": ckpt_name, "lr": lr, "n_estimators": n_est_inf,
                         "error": f"{type(e).__name__}: {e}",
                         "time_s": time.perf_counter() - t0}
            record["phase_b"].append(m)
            tag = " (no improvement; falls back to baseline)" if m.get("no_improvement") else ""
            line = (f"    B: ckpt={ckpt_name} lr={lr:.0e} n_est={n_est_inf:>2} "
                    f"val[{primary}]=" +
                    (f"{m[primary]:.4f}{tag}" if primary in m else f"ERR ({m['error']})"))
            print(line)

    # ---------- Pick best config ----------
    candidates = []
    for r in record["phase_a"]:
        candidates.append({**r, "phase": "A"})
    for r in record["phase_b"]:
        if primary in r:
            candidates.append({**r, "phase": "B"})
    best = max(candidates, key=lambda r: r[primary])
    # Phase B "no improvement" rows mirror their baseline; treat as Phase A.
    effective_phase = "A" if best.get("no_improvement") else best["phase"]
    record["best_on_val"] = best
    print(f"  Best on val ({primary}={best[primary]:.4f}): "
          f"phase={best['phase']} ckpt={best['ckpt']} "
          f"n_est={best['n_estimators']}"
          + (f" lr={best['lr']:.0e}" if 'lr' in best else "")
          + (" [no improvement -> baseline]" if best.get("no_improvement") else ""))

    # ---------- Phase C: seed ensemble, FULL-TRAIN refit, test predictions only ----------
    print("  Phase C — seed ensemble; refit best config on full train (train' + val)")
    seeds_used = list(args.ens_seeds)
    test_probas = []
    ckpt_path = CLASSIFIER_CKPTS[best["ckpt"]]

    for seed in seeds_used:
        if effective_phase == "A":
            t_p, classes = cls_predict_proba(
                X_train, y_train_arr, X_test,
                ckpt_path=ckpt_path, n_est=best["n_estimators"], seed=seed,
            )
        else:
            with tempfile.TemporaryDirectory() as tmp_str:
                tmp = Path(tmp_str)
                ft_full = cls_finetune_full(
                    X_train, y_train_arr,
                    ckpt_path=ckpt_path, lr=best["lr"],
                    epochs=args.ft_epochs, n_est_ft=args.n_est_ft, seed=seed,
                    tmp_dir=tmp,
                )
                t_p, classes = cls_predict_proba(
                    X_train, y_train_arr, X_test, ckpt_path=ft_full,
                    n_est=best["n_estimators"], seed=seed,
                )
        if classes_ref is None:
            classes_ref = classes
        test_probas.append(t_p)

    test_proba_ens = np.mean(test_probas, axis=0)
    test_m_default = cls_metrics(y_test_arr, test_proba_ens, classes_ref)

    # ---------- Phase D: threshold tuning (binary only) using winner's val_proba ----------
    if t_type == "binary":
        if best.get("no_improvement"):
            key = ("A", best["ckpt"], best["n_estimators"])
        elif best["phase"] == "A":
            key = ("A", best["ckpt"], best["n_estimators"])
        else:
            key = ("B", best["ckpt"], best["lr"], best["n_estimators"])
        winner_val_proba = val_probas[key]
        thresholds = np.linspace(0.01, 0.99, 99)
        accs = [
            accuracy_score(y_val == classes_ref[1], winner_val_proba[:, 1] >= t)
            for t in thresholds
        ]
        best_t = float(thresholds[int(np.argmax(accs))])
        test_pred_thr_lbl = np.where(
            test_proba_ens[:, 1] >= best_t, classes_ref[1], classes_ref[0]
        )
        test_m_thr = dict(test_m_default)
        test_m_thr["accuracy"] = float(accuracy_score(y_test_arr, test_pred_thr_lbl))
        test_m_thr["best_threshold"] = best_t
        record["phase_c"] = {
            "seeds": seeds_used,
            "test_default_threshold": test_m_default,
            "test_tuned_threshold": test_m_thr,
            "refit_on": "full_train",
        }
        record["test"] = {**test_m_default,
                          "accuracy_tuned": test_m_thr["accuracy"],
                          "best_threshold": best_t}
    else:
        record["phase_c"] = {"seeds": seeds_used, "test": test_m_default,
                             "refit_on": "full_train"}
        record["test"] = test_m_default

    print(f"  Final test[{primary}]={record['test'][primary]:.4f} "
          f"(val-selected best[{primary}]={best[primary]:.4f})")
    return record


def run_regression_task(task, args) -> dict:
    name = task["name"]
    primary = PRIMARY["regression"]
    print(f"\n=== {name} (regression) ===")

    X_train, y_train = load_split(task, "train")
    X_test, y_test = load_split(task, "test")
    X_train, y_train = drop_y_nan(X_train, y_train)
    X_test, y_test = drop_y_nan(X_test, y_test)
    X_train, X_test = preprocess(X_train, X_test)
    y_train_arr = y_train.values.astype(float)
    y_test_arr = y_test.values.astype(float)

    X_tp, X_val, y_tp, y_val = train_test_split(
        X_train, y_train_arr, test_size=0.2, random_state=args.seed,
    )
    print(f"  train' {X_tp.shape}, val {X_val.shape}, test {X_test.shape}")

    record = {
        "task": name, "type": "regression", "target": task["target"],
        "n_train_full": int(len(X_train)),
        "n_train_p": int(len(X_tp)),
        "n_val": int(len(X_val)),
        "n_test": int(len(X_test)),
        "phase_a": [], "phase_b": [], "phase_c": None, "test": None,
    }

    # Phase A: baseline sweep over ckpt × n_est × y_log
    print("  Phase A — baseline sweep")
    for ckpt_name, ckpt_path in REGRESSOR_CKPTS.items():
        for y_log in [False, True]:
            for n_est in args.n_est_grid:
                t0 = time.perf_counter()
                pred = reg_predict(
                    X_tp, y_tp, X_val, ckpt_path=ckpt_path,
                    n_est=n_est, seed=args.seed, y_log=y_log,
                )
                m = reg_metrics(y_val, pred)
                m.update({"ckpt": ckpt_name, "n_estimators": n_est, "y_log": y_log,
                          "time_s": time.perf_counter() - t0})
                record["phase_a"].append(m)
                print(f"    A: ckpt={ckpt_name} log={int(y_log)} n_est={n_est:>2} val[r2]={m['r2']:.4f}")

    # Phase B: fine-tune per ckpt at chosen y_log/n_est, lr sweep
    a_by_ckpt: dict[str, dict] = {}
    for r in record["phase_a"]:
        cur = a_by_ckpt.get(r["ckpt"])
        if cur is None or r[primary] > cur[primary]:
            a_by_ckpt[r["ckpt"]] = r

    print("  Phase B — fine-tune sweep")
    for ckpt_name, ckpt_path in REGRESSOR_CKPTS.items():
        cfg = a_by_ckpt[ckpt_name]
        n_est_inf, y_log = cfg["n_estimators"], cfg["y_log"]
        for lr in args.lr_grid:
            with tempfile.TemporaryDirectory() as tmp_str:
                tmp = Path(tmp_str)
                t0 = time.perf_counter()
                try:
                    best_path = reg_finetune(
                        X_tp, y_tp, X_val, y_val,
                        ckpt_path=ckpt_path, lr=lr, epochs=args.ft_epochs,
                        n_est_ft=args.n_est_ft, seed=args.seed,
                        tmp_dir=tmp, y_log=y_log,
                    )
                    if best_path is None:
                        m = {k: v for k, v in cfg.items()
                             if k not in ("ckpt", "n_estimators", "y_log", "time_s")}
                        m.update({"ckpt": ckpt_name, "lr": lr,
                                  "n_estimators": n_est_inf, "y_log": y_log,
                                  "time_s": time.perf_counter() - t0,
                                  "no_improvement": True})
                    else:
                        pred = reg_predict(
                            X_tp, y_tp, X_val, ckpt_path=best_path,
                            n_est=n_est_inf, seed=args.seed, y_log=y_log,
                        )
                        m = reg_metrics(y_val, pred)
                        m.update({"ckpt": ckpt_name, "lr": lr,
                                  "n_estimators": n_est_inf, "y_log": y_log,
                                  "time_s": time.perf_counter() - t0,
                                  "best_ckpt_basename": Path(best_path).name})
                except Exception as e:  # noqa: BLE001
                    m = {"ckpt": ckpt_name, "lr": lr, "n_estimators": n_est_inf,
                         "y_log": y_log, "error": f"{type(e).__name__}: {e}",
                         "time_s": time.perf_counter() - t0}
            record["phase_b"].append(m)
            tag = " (no improvement)" if m.get("no_improvement") else ""
            print(f"    B: ckpt={ckpt_name} lr={lr:.0e} log={int(y_log)} n_est={n_est_inf:>2} "
                  f"val[r2]=" + (f"{m['r2']:.4f}{tag}" if 'r2' in m else f"ERR"))

    # Pick best
    candidates = [{**r, "phase": "A"} for r in record["phase_a"]] + \
                 [{**r, "phase": "B"} for r in record["phase_b"] if primary in r]
    best = max(candidates, key=lambda r: r[primary])
    effective_phase = "A" if best.get("no_improvement") else best["phase"]
    record["best_on_val"] = best
    print(f"  Best on val (r2={best[primary]:.4f}): phase={best['phase']} "
          f"ckpt={best['ckpt']} log={int(best['y_log'])} n_est={best['n_estimators']}"
          + (f" lr={best['lr']:.0e}" if 'lr' in best else "")
          + (" [no improvement -> baseline]" if best.get("no_improvement") else ""))

    # Phase C: seed ensemble; refit on FULL train (train' + val)
    print("  Phase C — seed ensemble; refit best config on full train")
    test_preds = []
    seeds_used = list(args.ens_seeds)
    ckpt_path = REGRESSOR_CKPTS[best["ckpt"]]
    for seed in seeds_used:
        if effective_phase == "A":
            t = reg_predict(
                X_train, y_train_arr, X_test, ckpt_path=ckpt_path,
                n_est=best["n_estimators"], seed=seed, y_log=best["y_log"],
            )
        else:
            with tempfile.TemporaryDirectory() as tmp_str:
                tmp = Path(tmp_str)
                ft_full = reg_finetune_full(
                    X_train, y_train_arr,
                    ckpt_path=ckpt_path, lr=best["lr"],
                    epochs=args.ft_epochs, n_est_ft=args.n_est_ft, seed=seed,
                    tmp_dir=tmp, y_log=best["y_log"],
                )
                t = reg_predict(
                    X_train, y_train_arr, X_test, ckpt_path=ft_full,
                    n_est=best["n_estimators"], seed=seed, y_log=best["y_log"],
                )
        test_preds.append(t)
    test_pred_ens = np.mean(test_preds, axis=0)
    test_m = reg_metrics(y_test_arr, test_pred_ens)
    record["phase_c"] = {"seeds": seeds_used, "test": test_m, "refit_on": "full_train"}
    record["test"] = test_m
    print(f"  Final test[r2]={test_m['r2']:.4f} "
          f"(val-selected best[r2]={best[primary]:.4f})")
    return record


def run_task(task, args) -> dict:
    if task["type"] in ("binary", "multiclass"):
        return run_classification_task(task, args)
    return run_regression_task(task, args)


# ----------------------------------------------------------------------------
# Reporting
# ----------------------------------------------------------------------------

# Tier-0 numbers from results/TrialBench_TabPFN_baseline/all_metrics.json (baseline,
# no-ft, n_estimators=2). Hard-coded here for the comparison header — read from
# disk on init so we stay in sync if Tier-0 is re-run.
TIER0_PATH = Path("/data2/zhu11/TB/results/TrialBench_TabPFN_baseline/all_metrics.json")


def load_tier0() -> dict:
    if not TIER0_PATH.is_file():
        return {}
    data = json.loads(TIER0_PATH.read_text())
    by_name = {}
    for r in data.get("tasks", []):
        if r.get("error"):
            continue
        by_name[r["name"]] = r
    return by_name


def fmt(x):
    return f"{x:.4f}" if isinstance(x, float) else str(x)


def write_markdown(records: list[dict], args, tier0: dict) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    lines = []
    lines.append("# TrialBench × TabPFN-2.5 — Tier 1 tuning results\n")
    lines.append(
        f"Generated: {datetime.now().isoformat(timespec='seconds')}  \n"
        f"Device: {torch.cuda.get_device_name(0)}  \n"
        f"Run config: n_est_grid={args.n_est_grid}, lr_grid={args.lr_grid}, "
        f"ft_epochs={args.ft_epochs}, n_est_ft={args.n_est_ft}, "
        f"ens_seeds={args.ens_seeds}\n"
    )
    lines.append(
        "All hyperparameter and checkpoint choices made on a 80/20 val split of "
        "TRAIN. Test set used exactly once per task at the end. Tier-0 column = "
        "the 10-epoch fine-tune from `results/TrialBench_TabPFN_baseline/`.\n"
    )

    headline_rows = []
    for r in records:
        if r.get("error"):
            continue
        primary = PRIMARY[r["type"]]
        t0 = tier0.get(r["task"], {})
        t0_baseline = t0.get("baseline", {}).get(primary)
        t0_ft = t0.get("finetuned", {}).get(primary)
        tier1_test = r["test"][primary]
        delta = tier1_test - (t0_baseline if t0_baseline is not None else 0.0)
        best = r["best_on_val"]
        cfg = (
            f"phase={best['phase']} ckpt={best['ckpt']} n_est={best['n_estimators']}"
            + (f" lr={best['lr']:.0e}" if 'lr' in best else "")
            + (f" log={int(best['y_log'])}" if 'y_log' in best else "")
        )
        headline_rows.append((
            r["task"], r["type"], primary,
            t0_baseline, t0_ft, tier1_test, delta, cfg,
        ))

    lines.append("## Headline: Tier 1 vs. Tier 0 (primary metric only)\n")
    lines.append("| Task | Type | Metric | Tier-0 baseline (n_est=2) | Tier-0 ft (10ep) | **Tier-1 test** | Δ vs. Tier-0 baseline | Selected config |")
    lines.append("|---|---|---|---:|---:|---:|---:|---|")
    for row in headline_rows:
        task_, type_, metric, t0b, t0f, t1, delta, cfg = row
        lines.append(
            f"| {task_} | {type_} | {metric} | "
            f"{fmt(t0b) if t0b is not None else '—'} | "
            f"{fmt(t0f) if t0f is not None else '—'} | "
            f"**{fmt(t1)}** | "
            f"{('+' if delta >= 0 else '')}{delta:.4f} | "
            f"`{cfg}` |"
        )
    lines.append("")

    # Per-type detailed tables
    binary_rows, multi_rows, reg_rows = [], [], []
    for r in records:
        if r.get("error"):
            continue
        t = r["test"]
        if r["type"] == "binary":
            binary_rows.append((
                r["task"], r["n_train_full"], r["n_test"],
                t["roc_auc"], t["pr_auc"], t["log_loss"],
                t["accuracy"], t.get("accuracy_tuned", t["accuracy"]),
                t.get("best_threshold", 0.5),
            ))
        elif r["type"] == "multiclass":
            multi_rows.append((
                r["task"], r["n_classes"], r["n_train_full"], r["n_test"],
                t["accuracy"], t["f1_macro"], t["log_loss"],
            ))
        else:
            reg_rows.append((
                r["task"], r["n_train_full"], r["n_test"],
                t["mae"], t["rmse"], t["r2"],
            ))

    if binary_rows:
        lines.append("## Binary classification (test)\n")
        lines.append("| Task | n_train | n_test | ROC-AUC | PR-AUC | LogLoss | Acc (default 0.5) | Acc (tuned) | best_threshold |")
        lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|")
        for row in binary_rows:
            lines.append("| " + " | ".join(fmt(x) for x in row) + " |")
        lines.append("")

    if multi_rows:
        lines.append("## Multiclass classification (test)\n")
        lines.append("| Task | n_classes | n_train | n_test | Acc | F1-macro | LogLoss |")
        lines.append("|---|---:|---:|---:|---:|---:|---:|")
        for row in multi_rows:
            lines.append("| " + " | ".join(fmt(x) for x in row) + " |")
        lines.append("")

    if reg_rows:
        lines.append("## Regression (test)\n")
        lines.append("| Task | n_train | n_test | MAE | RMSE | R² |")
        lines.append("|---|---:|---:|---:|---:|---:|")
        for row in reg_rows:
            lines.append("| " + " | ".join(fmt(x) for x in row) + " |")
        lines.append("")

    lines.append("## Not applicable\n")
    lines.append("| Task | Reason |")
    lines.append("|---|---|")
    for name, reason in NOT_APPLICABLE:
        lines.append(f"| {name} | {reason} |")
    lines.append("")

    lines.append("## Methodology notes\n")
    lines.append(
        "- **No test leakage**: the 80/20 train/val split is fixed at "
        f"`random_state={args.seed}`. All hp choices (ckpt, n_est, lr, "
        "y_log, threshold) are made on val.\n"
        "- **Phase A** (baseline, no fine-tune): sweep `n_est_grid` × ckpts "
        "(classifier: `default`, `default-2`; regressor: `default`, `real`); "
        "regression additionally tries `log1p(y)`. All evaluated on val.\n"
        "- **Phase B** (fine-tune): per ckpt, fine-tune on (train', val) at "
        "each lr in `lr_grid` with `n_estimators_finetune={args.n_est_ft}` and "
        "val-based early stopping (best-on-val ckpt). If fine-tune cannot beat "
        "the initial val metric, the row is marked `no_improvement` and treated "
        "as the corresponding Phase A baseline.\n"
        "- **Phase C** (final model): for each seed in "
        f"{list(args.ens_seeds)}, refit the val-winning config on the **full "
        "train (train' + val)** — Phase A wins → re-fit in-context with full "
        "train; Phase B wins → re-fine-tune on full train (no val, fixed "
        f"`epochs={args.ft_epochs}`, `early_stopping=False`). Test predictions "
        "averaged across seeds.\n"
        "- **Phase D** (binary only): tune classification threshold on the "
        "val_proba saved by Phase A/B for the winning config; apply to the "
        "Phase C test ensemble.\n"
        "- Caveat: val is used for both fine-tune early stopping AND hp grid "
        "selection. With only ~12 candidate configs per task the over-selection "
        "risk is small.\n"
        "- Per-task full sweep details: `per_task/<name>.json`.\n"
        "- Raw aggregate: `all_metrics.json`.\n"
    )

    (OUT_DIR / "zero_shot_tier1.md").write_text("\n".join(lines))


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n-est-grid", type=int, nargs="+", default=[4, 8, 16, 32])
    parser.add_argument("--lr-grid", type=float, nargs="+", default=[1e-5, 2e-5, 5e-5])
    parser.add_argument("--ft-epochs", type=int, default=30)
    parser.add_argument("--n-est-ft", type=int, default=2)
    parser.add_argument("--ens-seeds", type=int, nargs="+", default=[0, 1, 2])
    parser.add_argument("--seed", type=int, default=0,
                        help="Seed for the train/val split.")
    parser.add_argument("--only", type=str, default=None,
                        help="Comma-separated subtask substrings to run (debug).")
    args = parser.parse_args()

    if not torch.cuda.is_available():
        raise RuntimeError("CUDA required.")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    PER_TASK_DIR.mkdir(parents=True, exist_ok=True)

    tasks = TASKS
    if args.only:
        keys = [k.strip() for k in args.only.split(",") if k.strip()]
        tasks = [t for t in TASKS if any(k in t["name"] for k in keys)]

    print(f"Device: {torch.cuda.get_device_name(0)}")
    print(f"Output: {OUT_DIR}")
    print(f"Tasks: {[t['name'] for t in tasks]}")
    print(f"args: {vars(args)}")

    tier0 = load_tier0()
    records: list[dict] = []
    aggregate = {
        "generated": datetime.now().isoformat(timespec="seconds"),
        "device": torch.cuda.get_device_name(0),
        "args": vars(args),
        "tasks": [],
    }

    for task in tasks:
        try:
            rec = run_task(task, args)
        except Exception as e:  # noqa: BLE001
            print(f"  ERROR on {task['name']}: {e}")
            traceback.print_exc()
            rec = {"task": task["name"], "type": task["type"],
                   "error": f"{type(e).__name__}: {e}"}
        records.append(rec)
        aggregate["tasks"].append(rec)
        # Save per-task and aggregate snapshots.
        (PER_TASK_DIR / f"{task['name']}.json").write_text(json.dumps(rec, indent=2))
        (OUT_DIR / "all_metrics.json").write_text(json.dumps(aggregate, indent=2))
        write_markdown(records, args, tier0)

    print(f"\nWrote {OUT_DIR / 'zero_shot_tier1.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
