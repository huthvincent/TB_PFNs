"""Fine-tune TabPFN-v2.5 on TrialBench Serious Adverse Event Forecasting.

Uses the pre-defined train/test split from all four phases combined.
Reports baseline (no fine-tune) vs. fine-tuned metrics.
"""

from __future__ import annotations

import argparse
import gc
import json
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

from tabpfn import TabPFNClassifier
from tabpfn.finetuning.finetuned_classifier import FinetunedTabPFNClassifier

DATA_ROOT = Path("/data2/zhu11/TB/dataset/TrialBench/serious-adverse-event-forecasting")
CKPT = Path("/data2/zhu11/TB/TabPFN/models/tabpfn-v2.5-classifier-v2.5_default.ckpt")
RESULTS_ROOT = Path("/data2/zhu11/TB/results")
CKPT_ROOT = Path("/data2/zhu11/TB/model_checkpoint")
PHASES = ["Phase1", "Phase2", "Phase3", "Phase4"]
TARGET = "Y/N"

# Long free-text / list-valued / very-high-cardinality fields not useful as raw
# tabular features for TabPFN. Mirrors what the official preprocessing drops or
# encodes separately (sentence2vec / mesh / smiles / icd encoders).
TEXT_DROP = [
    "brief_summary/textblock",
    "brief_title",
    "condition",
    "condition_browse/mesh_term",
    "eligibility/criteria/textblock",
    "eligibility/study_pop/textblock",
    "intervention/description",
    "intervention/intervention_name",
    "intervention/other_name",
    "intervention_browse/mesh_term",
    "keyword",
    "location/facility/address/city",
    "smiless",
    "icdcode",
    "study_design_info/intervention_model_description",
    "study_design_info/masking_description",
    "eligibility/gender_description",
    "biospec_descr/textblock",
    "detailed_description/textblock",
]


def load_split(split: str) -> tuple[pd.DataFrame, pd.Series]:
    xs, ys = [], []
    for phase in PHASES:
        x = pd.read_csv(DATA_ROOT / phase / f"{split}_x.csv", index_col=0)
        y = pd.read_csv(DATA_ROOT / phase / f"{split}_y.csv", index_col=0)
        y = y.loc[x.index]
        x = x.assign(phase_split=phase)
        xs.append(x)
        ys.append(y[TARGET])
    X = pd.concat(xs, axis=0)
    y = pd.concat(ys, axis=0)
    return X, y


def preprocess(
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    drop_text = [c for c in TEXT_DROP if c in X_train.columns]
    X_train = X_train.drop(columns=drop_text)
    X_test = X_test.drop(columns=drop_text)

    # Drop columns missing in >50% of training rows (matches official preprocessing).
    nan_drop = [
        c for c in X_train.columns
        if X_train[c].isna().sum() > len(X_train) * 0.5
    ]
    X_train = X_train.drop(columns=nan_drop)
    X_test = X_test.drop(columns=nan_drop)

    # Cast all string columns to pandas category so TabPFN auto-handles them.
    for c in X_train.columns:
        if X_train[c].dtype == object:
            X_train[c] = X_train[c].astype("category")
            X_test[c] = X_test[c].astype("category")

    return X_train, X_test


def metrics(y_true: np.ndarray, proba: np.ndarray) -> dict[str, float]:
    p1 = proba[:, 1]
    return {
        "roc_auc": float(roc_auc_score(y_true, p1)),
        "pr_auc": float(average_precision_score(y_true, p1)),
        "log_loss": float(log_loss(y_true, proba)),
        "accuracy": float(accuracy_score(y_true, p1 >= 0.5)),
    }


def report(name: str, m: dict[str, float]) -> None:
    print(
        f"[{name}] ROC-AUC={m['roc_auc']:.4f} PR-AUC={m['pr_auc']:.4f} "
        f"LogLoss={m['log_loss']:.4f} Acc={m['accuracy']:.4f}"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", type=int, default=10)
    parser.add_argument("--lr", type=float, default=2e-5)
    parser.add_argument("--n-estimators", type=int, default=2)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()

    if not torch.cuda.is_available():
        raise RuntimeError("CUDA required.")

    run_id = f"sae_finetune_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    results_dir = RESULTS_ROOT / run_id
    ckpt_dir = CKPT_ROOT / run_id
    results_dir.mkdir(parents=True, exist_ok=True)
    ckpt_dir.mkdir(parents=True, exist_ok=True)

    print(f"Run: {run_id}")
    print(f"Device: {torch.cuda.get_device_name(0)}")
    print(f"Pretrained ckpt: {CKPT}")
    print(f"Results dir: {results_dir}")
    print(f"Checkpoint dir: {ckpt_dir}")

    print("Loading splits...")
    X_train, y_train = load_split("train")
    X_test, y_test = load_split("test")
    print(f"Raw train: {X_train.shape}, test: {X_test.shape}")
    print(f"Train Y/N counts: {y_train.value_counts().to_dict()}")
    print(f"Test  Y/N counts: {y_test.value_counts().to_dict()}")

    X_train, X_test = preprocess(X_train, X_test)
    print(f"After preprocess: train {X_train.shape}, test {X_test.shape}")
    print(f"Feature dtypes: {X_train.dtypes.value_counts().to_dict()}")

    common_kwargs = dict(
        device="cuda",
        n_estimators=args.n_estimators,
        ignore_pretraining_limits=True,
        inference_config={"SUBSAMPLE_SAMPLES": 50_000},
        random_state=args.seed,
        model_path=str(CKPT),
    )

    print("\n--- Baseline TabPFN (no fine-tune) ---")
    t0 = time.perf_counter()
    base = TabPFNClassifier(**common_kwargs)
    base.fit(X_train, y_train.values)
    base_proba = base.predict_proba(X_test)
    base_time = time.perf_counter() - t0
    base_metrics = metrics(y_test.values, base_proba)
    print(f"baseline fit+predict: {base_time:.1f}s")
    report("baseline", base_metrics)
    del base
    gc.collect()
    torch.cuda.empty_cache()

    print("\n--- Fine-tuning TabPFN ---")
    t0 = time.perf_counter()
    torch.cuda.reset_peak_memory_stats()
    ft = FinetunedTabPFNClassifier(
        device="cuda",
        epochs=args.epochs,
        learning_rate=args.lr,
        n_estimators_finetune=args.n_estimators,
        n_estimators_validation=args.n_estimators,
        n_estimators_final_inference=args.n_estimators,
        random_state=args.seed,
        extra_classifier_kwargs={
            "ignore_pretraining_limits": True,
            "inference_config": {"SUBSAMPLE_SAMPLES": 50_000},
            "model_path": str(CKPT),
        },
    )
    ft.fit(X_train, y_train.values, output_dir=ckpt_dir)
    ft_proba = ft.predict_proba(X_test)
    ft_time = time.perf_counter() - t0
    peak = torch.cuda.max_memory_allocated() / 1e9
    ft_metrics = metrics(y_test.values, ft_proba)
    print(f"fine-tune fit+predict: {ft_time:.1f}s, peak VRAM={peak:.2f} GB")
    report("finetuned", ft_metrics)

    saved_ckpts = sorted(ckpt_dir.glob("*.pth"))
    print(f"Fine-tune checkpoints written: {[p.name for p in saved_ckpts]}")

    summary = {
        "run_id": run_id,
        "device": torch.cuda.get_device_name(0),
        "pretrained_ckpt": str(CKPT),
        "args": vars(args),
        "n_train": int(len(X_train)),
        "n_test": int(len(X_test)),
        "n_features": int(X_train.shape[1]),
        "baseline": {"time_s": base_time, **base_metrics},
        "finetuned": {"time_s": ft_time, "peak_vram_gb": peak, **ft_metrics},
    }
    with open(results_dir / "metrics.json", "w") as f:
        json.dump(summary, f, indent=2)
    print(f"Saved metrics: {results_dir / 'metrics.json'}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
