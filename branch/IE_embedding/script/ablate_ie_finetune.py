#!/usr/bin/env python3
"""
ablate_ie_finetune.py — 4-cell ablation on SAE (or any binary subtask):
fine-tune × IE-features. Answers: do IE features still help on top of
fine-tuning, and does fine-tuning still help on top of IE features?

Cells:
  A. baseline X, no fine-tune          (matches existing project baseline 0.885)
  B. baseline X, fine-tune
  C. + IE X,    no fine-tune           (matches ablate_ie_features.py)
  D. + IE X,    fine-tune

Reuses preprocess from sae_finetune.py and add_ie_features from
ablate_ie_features.py. FT ckpts written to results/<run_id>/ft_ckpt_{B,D}/.
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
    log_loss,
    roc_auc_score,
)

sys.path.insert(0, "/data2/zhu11/TB/script")
from sae_finetune import preprocess  # noqa: E402

sys.path.insert(0, str(Path(__file__).parent))
from ablate_ie_features import load_split, add_ie_features  # noqa: E402

from tabpfn import TabPFNClassifier  # noqa: E402
from tabpfn.finetuning.finetuned_classifier import FinetunedTabPFNClassifier  # noqa: E402

CKPT = Path("/data2/zhu11/TB/TabPFN/models/tabpfn-v2.5-classifier-v2.5_default.ckpt")
RESULTS_ROOT = Path("/data2/zhu11/TB/branch/IE_embedding/results")


def metrics(y_true, proba):
    p1 = proba[:, 1]
    return {
        "roc_auc":  float(roc_auc_score(y_true, p1)),
        "pr_auc":   float(average_precision_score(y_true, p1)),
        "log_loss": float(log_loss(y_true, proba)),
        "accuracy": float(accuracy_score(y_true, p1 >= 0.5)),
    }


def report(name, m):
    print(f"[{name}] ROC-AUC={m['roc_auc']:.4f} PR-AUC={m['pr_auc']:.4f} "
          f"LogLoss={m['log_loss']:.4f} Acc={m['accuracy']:.4f}")


def fit_zero_shot(X_train, y_train, X_test, n_estimators, seed):
    clf = TabPFNClassifier(
        device="cuda",
        n_estimators=n_estimators,
        ignore_pretraining_limits=True,
        inference_config={"SUBSAMPLE_SAMPLES": 50_000},
        random_state=seed,
        model_path=str(CKPT),
    )
    t0 = time.perf_counter()
    clf.fit(X_train, y_train.values.astype(int))
    proba = clf.predict_proba(X_test)
    t = time.perf_counter() - t0
    del clf
    gc.collect()
    torch.cuda.empty_cache()
    return proba, t


def fit_finetune(X_train, y_train, X_test, n_estimators, epochs, lr, seed, ckpt_dir):
    ckpt_dir.mkdir(parents=True, exist_ok=True)
    ft = FinetunedTabPFNClassifier(
        device="cuda",
        epochs=epochs,
        learning_rate=lr,
        n_estimators_finetune=n_estimators,
        n_estimators_validation=n_estimators,
        n_estimators_final_inference=n_estimators,
        random_state=seed,
        extra_classifier_kwargs={
            "ignore_pretraining_limits": True,
            "inference_config": {"SUBSAMPLE_SAMPLES": 50_000},
            "model_path": str(CKPT),
        },
    )
    torch.cuda.reset_peak_memory_stats()
    t0 = time.perf_counter()
    ft.fit(X_train, y_train.values.astype(int), output_dir=ckpt_dir)
    proba = ft.predict_proba(X_test)
    t = time.perf_counter() - t0
    peak_gb = torch.cuda.max_memory_allocated() / 1e9
    del ft
    gc.collect()
    torch.cuda.empty_cache()
    return proba, t, peak_gb


def main(args):
    safe = args.subtask.replace("/", "_")
    run_id = f"ftab_ie_{safe}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    run_dir = RESULTS_ROOT / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    print(f"[run_id] {run_id}")
    print(f"[subtask] {args.subtask}  [target] {args.target}")

    X_train, y_train = load_split(args.subtask, "train", args.target)
    X_test,  y_test  = load_split(args.subtask, "test",  args.target)
    y_train = y_train.astype(int)
    y_test  = y_test.astype(int)
    print(f"  train={X_train.shape}  test={X_test.shape}")

    Xtr_p, Xte_p = preprocess(X_train, X_test)
    ie = pd.read_parquet(args.ie_features)
    Xtr_b, _ = add_ie_features(Xtr_p, ie)
    Xte_b, _ = add_ie_features(Xte_p, ie)
    print(f"  preprocessed: base train {Xtr_p.shape}  +IE train {Xtr_b.shape}")

    results = {}

    # ---------- A: baseline X, zero-shot ----------
    print("\n=== Cell A: baseline X, zero-shot ===")
    proba_a, t_a = fit_zero_shot(Xtr_p, y_train, Xte_p, args.n_estimators, args.seed)
    m_a = metrics(y_test.values, proba_a)
    report("A", m_a)
    results["A_baseline_zeroshot"] = {"time_s": t_a, **m_a}

    # ---------- B: baseline X, fine-tune ----------
    print(f"\n=== Cell B: baseline X, fine-tune ({args.epochs} ep, lr={args.lr}) ===")
    proba_b, t_b, peak_b = fit_finetune(Xtr_p, y_train, Xte_p, args.n_estimators,
                                        args.epochs, args.lr, args.seed,
                                        run_dir / "ft_ckpt_B")
    m_b = metrics(y_test.values, proba_b)
    print(f"  time={t_b:.1f}s  peak_vram={peak_b:.2f} GB")
    report("B", m_b)
    results["B_baseline_finetune"] = {"time_s": t_b, "peak_vram_gb": peak_b, **m_b}

    # ---------- C: + IE X, zero-shot ----------
    print("\n=== Cell C: + IE X, zero-shot ===")
    proba_c, t_c = fit_zero_shot(Xtr_b, y_train, Xte_b, args.n_estimators, args.seed)
    m_c = metrics(y_test.values, proba_c)
    report("C", m_c)
    results["C_ie_zeroshot"] = {"time_s": t_c, **m_c}

    # ---------- D: + IE X, fine-tune ----------
    print(f"\n=== Cell D: + IE X, fine-tune ({args.epochs} ep, lr={args.lr}) ===")
    proba_d, t_d, peak_d = fit_finetune(Xtr_b, y_train, Xte_b, args.n_estimators,
                                        args.epochs, args.lr, args.seed,
                                        run_dir / "ft_ckpt_D")
    m_d = metrics(y_test.values, proba_d)
    print(f"  time={t_d:.1f}s  peak_vram={peak_d:.2f} GB")
    report("D", m_d)
    results["D_ie_finetune"] = {"time_s": t_d, "peak_vram_gb": peak_d, **m_d}

    # ---------- Summary table ----------
    print("\n=== 4-cell ROC-AUC matrix ===")
    print(f"            no-FT     FT       Δ-FT")
    print(f"  baseline  {m_a['roc_auc']:.4f}  {m_b['roc_auc']:.4f}  {m_b['roc_auc']-m_a['roc_auc']:+.4f}")
    print(f"  +IE       {m_c['roc_auc']:.4f}  {m_d['roc_auc']:.4f}  {m_d['roc_auc']-m_c['roc_auc']:+.4f}")
    print(f"  Δ-IE      {m_c['roc_auc']-m_a['roc_auc']:+.4f}  {m_d['roc_auc']-m_b['roc_auc']:+.4f}")

    print("\n=== Are gains additive? ===")
    ie_no_ft   = m_c["roc_auc"] - m_a["roc_auc"]
    ft_no_ie   = m_b["roc_auc"] - m_a["roc_auc"]
    both       = m_d["roc_auc"] - m_a["roc_auc"]
    additive   = ie_no_ft + ft_no_ie
    print(f"  Δ(IE alone)         = {ie_no_ft:+.4f}")
    print(f"  Δ(FT alone)         = {ft_no_ie:+.4f}")
    print(f"  Δ(IE + FT) actual   = {both:+.4f}")
    print(f"  Δ(IE + FT) additive = {additive:+.4f}")
    print(f"  Synergy (actual - additive) = {both - additive:+.4f}")

    summary = {
        "run_id": run_id,
        "subtask": args.subtask, "target": args.target,
        "ie_features_path": str(args.ie_features),
        "n_train": int(len(X_train)),
        "n_test":  int(len(X_test)),
        "n_features_baseline": int(Xtr_p.shape[1]),
        "n_features_with_ie":  int(Xtr_b.shape[1]),
        "cells": results,
        "args": vars(args),
    }
    with (run_dir / "metrics.json").open("w") as f:
        json.dump(summary, f, indent=2)
    print(f"\nSaved: {run_dir / 'metrics.json'}")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--ie-features", required=True)
    p.add_argument("--subtask", default="serious-adverse-event-forecasting")
    p.add_argument("--target",  default="Y/N")
    p.add_argument("--epochs", type=int, default=10)
    p.add_argument("--lr", type=float, default=2e-5)
    p.add_argument("--n-estimators", type=int, default=2)
    p.add_argument("--seed", type=int, default=0)
    args = p.parse_args()
    main(args)
