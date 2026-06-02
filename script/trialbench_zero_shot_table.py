"""Sweep TabPFN baseline + 10-epoch fine-tune over all TrialBench subtasks.

Writes a comparison table to
/data2/zhu11/TB/results/TrialBench_TabPFN_baseline/zero_shot.md
and the raw metrics dump to all_metrics.json in the same directory.

Does NOT save model checkpoints (per user request).
"""

from __future__ import annotations

import argparse
import gc
import json
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

from tabpfn import TabPFNClassifier, TabPFNRegressor
from tabpfn.finetuning.finetuned_classifier import FinetunedTabPFNClassifier
from tabpfn.finetuning.finetuned_regressor import FinetunedTabPFNRegressor

DATA_ROOT = Path("/data2/zhu11/TB/dataset/TrialBench")
CLASSIFIER_CKPT = Path(
    "/data2/zhu11/TB/TabPFN/models/tabpfn-v2.5-classifier-v2.5_default.ckpt"
)
REGRESSOR_CKPT = Path(
    "/data2/zhu11/TB/TabPFN/models/tabpfn-v2.5-regressor-v2.5_default.ckpt"
)
OUT_DIR = Path("/data2/zhu11/TB/results/TrialBench_TabPFN_baseline")

# Long free-text / list-valued / very-high-cardinality fields.
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

# Per-subtask config. (eligibility-criteria-design omitted — text generation.)
TASKS = [
    {
        "name": "trial-approval-forecasting",
        "type": "binary",
        "target": "outcome",
        "phases": ["Phase1", "Phase2", "Phase3", "Phase4"],
        "y_suffix": "",
    },
    {
        "name": "trial-duration-forecasting",
        "type": "regression",
        "target": "time_day",
        "phases": ["Phase1", "Phase2", "Phase3", "Phase4"],
        "y_suffix": "",
    },
    {
        "name": "patient-dropout-event-forecasting",
        "type": "binary",
        "target": "Y/N",
        "phases": ["Phase1", "Phase2", "Phase3", "Phase4"],
        "y_suffix": "",
    },
    {
        "name": "serious-adverse-event-forecasting",
        "type": "binary",
        "target": "Y/N",
        "phases": ["Phase1", "Phase2", "Phase3", "Phase4"],
        "y_suffix": "",
    },
    {
        "name": "mortality-event-prediction",
        "type": "binary",
        "target": "Y/N",
        "phases": ["Phase1", "Phase2", "Phase3", "Phase4"],
        "y_suffix": "",
    },
    {
        "name": "trial-failure-reason-identification",
        "type": "multiclass",
        "target": "failure_reason",
        "phases": ["Phase1", "Phase2", "Phase3", "Phase4"],
        "y_suffix": "",
    },
]

# Subtasks not applicable to raw-tabular TabPFN (need text/molecular encoders).
NOT_APPLICABLE = [
    (
        "eligibility-criteria-design",
        "Free-text generation task; not a tabular prediction problem.",
    ),
    (
        "drug-dose-prediction",
        "Inputs are only SMILES strings and MeSH terms; needs molecular/ontology "
        "encoders (TrialBench uses MPNN + mesh_term2feature). No tabular features.",
    ),
]


def load_split(task: dict, split: str) -> tuple[pd.DataFrame, pd.Series]:
    xs, ys = [], []
    for phase in task["phases"]:
        x_path = DATA_ROOT / task["name"] / phase / f"{split}_x.csv"
        y_path = DATA_ROOT / task["name"] / phase / f"{split}_y{task['y_suffix']}.csv"
        x = pd.read_csv(x_path, index_col=0)
        y = pd.read_csv(y_path, index_col=0)
        y = y.loc[x.index]
        x = x.assign(phase_split=phase)
        xs.append(x)
        ys.append(y[task["target"]])
    X = pd.concat(xs, axis=0)
    y = pd.concat(ys, axis=0)
    return X, y


def preprocess(
    X_train: pd.DataFrame, X_test: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame]:
    drop_text = [c for c in TEXT_DROP if c in X_train.columns]
    X_train = X_train.drop(columns=drop_text)
    X_test = X_test.drop(columns=drop_text)
    nan_drop = [
        c for c in X_train.columns
        if X_train[c].isna().sum() > len(X_train) * 0.5
    ]
    X_train = X_train.drop(columns=nan_drop)
    X_test = X_test.drop(columns=nan_drop)
    for c in X_train.columns:
        if X_train[c].dtype == object:
            X_train[c] = X_train[c].astype("category")
            X_test[c] = X_test[c].astype("category")
    return X_train, X_test


def drop_y_nan(X: pd.DataFrame, y: pd.Series) -> tuple[pd.DataFrame, pd.Series]:
    mask = ~y.isna()
    return X.loc[mask], y.loc[mask]


def cls_metrics(y_true, proba, classes) -> dict:
    pred = classes[proba.argmax(axis=1)]
    out = {
        "accuracy": float(accuracy_score(y_true, pred)),
        "log_loss": float(log_loss(y_true, proba, labels=list(classes))),
    }
    if len(classes) == 2:
        # use the second class column as positive probability
        pos_idx = 1
        p_pos = proba[:, pos_idx]
        out["roc_auc"] = float(roc_auc_score(y_true == classes[pos_idx], p_pos))
        out["pr_auc"] = float(
            average_precision_score(y_true == classes[pos_idx], p_pos)
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


def run_classifier(task, X_train, y_train, X_test, y_test, args) -> dict:
    common = dict(
        device="cuda",
        n_estimators=args.n_estimators,
        ignore_pretraining_limits=True,
        inference_config={"SUBSAMPLE_SAMPLES": 50_000},
        random_state=args.seed,
        model_path=str(CLASSIFIER_CKPT),
    )

    print("  baseline...")
    t0 = time.perf_counter()
    base = TabPFNClassifier(**common)
    base.fit(X_train, y_train.values)
    base_proba = base.predict_proba(X_test)
    base_time = time.perf_counter() - t0
    base_m = cls_metrics(y_test.values, base_proba, base.classes_)
    base_m["time_s"] = base_time
    del base
    gc.collect()
    torch.cuda.empty_cache()

    print("  fine-tune...")
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
            "model_path": str(CLASSIFIER_CKPT),
        },
    )
    ft.fit(X_train, y_train.values)
    ft_proba = ft.predict_proba(X_test)
    ft_time = time.perf_counter() - t0
    ft_classes = ft.finetuned_inference_classifier_.classes_
    ft_m = cls_metrics(y_test.values, ft_proba, ft_classes)
    ft_m["time_s"] = ft_time
    ft_m["peak_vram_gb"] = torch.cuda.max_memory_allocated() / 1e9
    del ft
    gc.collect()
    torch.cuda.empty_cache()

    return {"baseline": base_m, "finetuned": ft_m}


def run_regressor(task, X_train, y_train, X_test, y_test, args) -> dict:
    common = dict(
        device="cuda",
        n_estimators=args.n_estimators,
        ignore_pretraining_limits=True,
        inference_config={"SUBSAMPLE_SAMPLES": 50_000},
        random_state=args.seed,
        model_path=str(REGRESSOR_CKPT),
    )

    print("  baseline...")
    t0 = time.perf_counter()
    base = TabPFNRegressor(**common)
    base.fit(X_train, y_train.values)
    base_pred = base.predict(X_test)
    base_time = time.perf_counter() - t0
    base_m = reg_metrics(y_test.values, base_pred)
    base_m["time_s"] = base_time
    del base
    gc.collect()
    torch.cuda.empty_cache()

    print("  fine-tune...")
    t0 = time.perf_counter()
    torch.cuda.reset_peak_memory_stats()
    ft = FinetunedTabPFNRegressor(
        device="cuda",
        epochs=args.epochs,
        learning_rate=args.lr,
        n_estimators_finetune=args.n_estimators,
        n_estimators_validation=args.n_estimators,
        n_estimators_final_inference=args.n_estimators,
        random_state=args.seed,
        extra_regressor_kwargs={
            "ignore_pretraining_limits": True,
            "inference_config": {"SUBSAMPLE_SAMPLES": 50_000},
            "model_path": str(REGRESSOR_CKPT),
        },
    )
    ft.fit(X_train, y_train.values)
    ft_pred = ft.predict(X_test)
    ft_time = time.perf_counter() - t0
    ft_m = reg_metrics(y_test.values, ft_pred)
    ft_m["time_s"] = ft_time
    ft_m["peak_vram_gb"] = torch.cuda.max_memory_allocated() / 1e9
    del ft
    gc.collect()
    torch.cuda.empty_cache()

    return {"baseline": base_m, "finetuned": ft_m}


def fmt(x):
    return f"{x:.4f}" if isinstance(x, float) else str(x)


def write_markdown(all_results: dict, args) -> None:
    binary_rows, multi_rows, reg_rows = [], [], []
    for r in all_results["tasks"]:
        if r.get("error"):
            continue
        if r["type"] == "binary":
            b, f = r["baseline"], r["finetuned"]
            binary_rows.append(
                (
                    r["name"], r["n_train"], r["n_test"],
                    b["roc_auc"], f["roc_auc"],
                    b["pr_auc"], f["pr_auc"],
                    b["log_loss"], f["log_loss"],
                    b["accuracy"], f["accuracy"],
                )
            )
        elif r["type"] == "multiclass":
            b, f = r["baseline"], r["finetuned"]
            multi_rows.append(
                (
                    r["name"], r.get("n_classes", "?"), r["n_train"], r["n_test"],
                    b["accuracy"], f["accuracy"],
                    b["f1_macro"], f["f1_macro"],
                    b["log_loss"], f["log_loss"],
                )
            )
        elif r["type"] == "regression":
            b, f = r["baseline"], r["finetuned"]
            reg_rows.append(
                (
                    r["name"], r["n_train"], r["n_test"],
                    b["mae"], f["mae"],
                    b["rmse"], f["rmse"],
                    b["r2"], f["r2"],
                )
            )

    md = []
    md.append("# TrialBench × TabPFN-2.5 — Baseline vs. 10-epoch Fine-tune\n")
    md.append(
        f"Generated: {all_results['generated']}  \n"
        f"Device: {all_results['device']}  \n"
        f"Pretrained classifier ckpt: `{all_results['classifier_ckpt']}`  \n"
        f"Run config: epochs={args.epochs}, lr={args.lr}, n_estimators={args.n_estimators}, seed={args.seed}\n"
    )
    md.append(
        "Baseline = TabPFN in-context learning (no gradient updates). "
        "Fine-tuned = `FinetunedTabPFNClassifier`/`...Regressor` for 10 epochs. "
        "Same train/test split (TrialBench default, all phases concatenated).\n"
    )

    if binary_rows:
        md.append("## Binary classification\n")
        md.append(
            "| Task | n_train | n_test | ROC-AUC base | ROC-AUC ft | PR-AUC base | PR-AUC ft | LogLoss base | LogLoss ft | Acc base | Acc ft |"
        )
        md.append(
            "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|"
        )
        for r in binary_rows:
            md.append("| " + " | ".join(fmt(x) for x in r) + " |")
        md.append("")

    if multi_rows:
        md.append("## Multiclass classification\n")
        md.append(
            "| Task | n_classes | n_train | n_test | Acc base | Acc ft | F1-macro base | F1-macro ft | LogLoss base | LogLoss ft |"
        )
        md.append(
            "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|"
        )
        for r in multi_rows:
            md.append("| " + " | ".join(fmt(x) for x in r) + " |")
        md.append("")

    if reg_rows:
        md.append("## Regression\n")
        md.append(
            "| Task | n_train | n_test | MAE base | MAE ft | RMSE base | RMSE ft | R² base | R² ft |"
        )
        md.append(
            "|---|---:|---:|---:|---:|---:|---:|---:|---:|"
        )
        for r in reg_rows:
            md.append("| " + " | ".join(fmt(x) for x in r) + " |")
        md.append("")

    md.append("## Not applicable\n")
    md.append("| Task | Reason |")
    md.append("|---|---|")
    for name, reason in NOT_APPLICABLE:
        md.append(f"| {name} | {reason} |")
    md.append("")

    md.append("## Errored runs\n")
    err_lines = []
    for r in all_results["tasks"]:
        if r.get("error"):
            err_lines.append(f"- **{r['name']}**: {r['error']}")
    if err_lines:
        md.append("\n".join(err_lines) + "\n")
    else:
        md.append("(none)\n")

    md.append("## Notes\n")
    md.append(
        "- For `trial-duration-forecasting` we report the `time_day` target.\n"
        "- All phases (Phase1–Phase4) are concatenated for tasks that have phases.\n"
        "- Long free-text columns are dropped before feeding to TabPFN; "
        "see `TEXT_DROP` in `script/trialbench_zero_shot_table.py`.\n"
        "- Raw metrics dump: `all_metrics.json` in this directory.\n"
    )

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "zero_shot.md").write_text("\n".join(md))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", type=int, default=10)
    parser.add_argument("--lr", type=float, default=2e-5)
    parser.add_argument("--n-estimators", type=int, default=2)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--only", type=str, default=None,
                        help="Comma-separated subtask substrings to run (debug).")
    args = parser.parse_args()

    if not torch.cuda.is_available():
        raise RuntimeError("CUDA required.")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Device: {torch.cuda.get_device_name(0)}")
    print(f"Output: {OUT_DIR}")

    tasks = TASKS
    if args.only:
        keys = [k.strip() for k in args.only.split(",") if k.strip()]
        tasks = [t for t in TASKS if any(k in t["name"] for k in keys)]

    all_results = {
        "generated": datetime.now().isoformat(timespec="seconds"),
        "device": torch.cuda.get_device_name(0),
        "classifier_ckpt": str(CLASSIFIER_CKPT),
        "args": vars(args),
        "tasks": [],
    }

    for task in tasks:
        print(f"\n=== {task['name']} ({task['type']}, target={task['target']}) ===")
        try:
            X_train, y_train = load_split(task, "train")
            X_test, y_test = load_split(task, "test")
            X_train, y_train = drop_y_nan(X_train, y_train)
            X_test, y_test = drop_y_nan(X_test, y_test)
            X_train, X_test = preprocess(X_train, X_test)
            print(f"  train {X_train.shape}, test {X_test.shape}")

            entry = {
                "name": task["name"],
                "type": task["type"],
                "target": task["target"],
                "n_train": int(len(X_train)),
                "n_test": int(len(X_test)),
                "n_features": int(X_train.shape[1]),
            }

            if task["type"] in ("binary", "multiclass"):
                entry["n_classes"] = int(y_train.nunique())
                m = run_classifier(task, X_train, y_train, X_test, y_test, args)
            elif task["type"] == "regression":
                m = run_regressor(task, X_train, y_train, X_test, y_test, args)
            else:
                raise ValueError(f"Unknown type {task['type']}")

            entry.update(m)
            all_results["tasks"].append(entry)
            print(
                f"  OK  baseline={m['baseline']}\n"
                f"      finetuned={m['finetuned']}"
            )
        except Exception as e:  # noqa: BLE001
            print(f"  ERROR: {e}")
            traceback.print_exc()
            all_results["tasks"].append({
                "name": task["name"],
                "type": task["type"],
                "target": task["target"],
                "error": f"{type(e).__name__}: {e}",
            })
        # write incrementally so partial runs are still recorded
        (OUT_DIR / "all_metrics.json").write_text(json.dumps(all_results, indent=2))
        write_markdown(all_results, args)

    print(f"\nWrote {OUT_DIR / 'zero_shot.md'}")
    print(f"Wrote {OUT_DIR / 'all_metrics.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
