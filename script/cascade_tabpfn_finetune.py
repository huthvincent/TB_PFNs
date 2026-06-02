"""3-layer cascade with fine-tuned TabPFN — primary models only.

Same cascade structure and label definitions as `cascade_xgboost_primary.py`
(see `results/cascade_xgboost/cascade_results.md` for the canonical layer
definitions). The only change is the classifier: each layer's primary model
is a `FinetunedTabPFNClassifier` instead of XGBoost.

Scope: Phase 1, 2, 3 (no Phase 4).
Outputs to /data2/zhu11/TB/results/cascade_TabPFN/.
"""

from __future__ import annotations

import gc
import json
import tempfile
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
from sklearn.model_selection import train_test_split

from tabpfn.finetuning.finetuned_classifier import FinetunedTabPFNClassifier

JOINED_ROOT = Path("/data2/zhu11/TB/dataset/TrialBench_joined")
OUT_DIR = Path("/data2/zhu11/TB/results/cascade_TabPFN")
CLASSIFIER_CKPT = (
    "/data2/zhu11/TB/TabPFN/models/tabpfn-v2.5-classifier-v2.5_default.ckpt"
)
PHASES = ["Phase1", "Phase2", "Phase3"]
SEED = 42
TEST_FRAC = 0.20

# Fine-tune hyperparameters (fixed; no sweep — mirrors the XGBoost script's
# "single config" style for direct comparability). N_EST is shared across
# fine-tune / validation / inference to satisfy use_fixed_preprocessing_seed.
FT_EPOCHS = 30
LR = 2e-5
N_EST = 4

TEXT_DROP = [
    "brief_summary/textblock", "brief_title", "condition",
    "condition_browse/mesh_term", "eligibility/criteria/textblock",
    "eligibility/study_pop/textblock", "intervention/description",
    "intervention/intervention_name", "intervention/other_name",
    "intervention_browse/mesh_term", "keyword",
    "location/facility/address/city", "smiless", "icdcode",
    "study_design_info/intervention_model_description",
    "study_design_info/masking_description",
    "eligibility/gender_description", "biospec_descr/textblock",
    "detailed_description/textblock",
]

LABEL_DROP = [
    "dropout_YN", "dropout_rate",
    "sae_YN", "sae_rate",
    "mortality_YN", "mortality_rate",
    "failure_reason",
    "approval_outcome",
    "start_date", "completion_date",
    "duration_day", "duration_month", "duration_year",
    "execution_fail", "execution_pass",
    "biology_fail", "biology_pass",
    "regulatory_pass",
]


def preprocess_features(df: pd.DataFrame) -> pd.DataFrame:
    """Drop text + label columns; drop >50% NaN cols; cast strings to category."""
    drop = [c for c in TEXT_DROP + LABEL_DROP if c in df.columns]
    X = df.drop(columns=drop)
    nan_drop = [c for c in X.columns if X[c].isna().sum() > len(X) * 0.5]
    X = X.drop(columns=nan_drop)
    for c in X.columns:
        dtype = X[c].dtype
        if dtype == object or pd.api.types.is_string_dtype(dtype):
            X[c] = X[c].astype("string").astype("category")
    return X


def fit_tabpfn_finetune(X_tr, y_tr):
    """Fine-tune TabPFN on (X_tr, y_tr); return fitted classifier ready to predict."""
    ft = FinetunedTabPFNClassifier(
        device="cuda",
        epochs=FT_EPOCHS,
        learning_rate=LR,
        n_estimators_finetune=N_EST,
        n_estimators_validation=N_EST,
        n_estimators_final_inference=N_EST,
        random_state=SEED,
        early_stopping=False,
        extra_classifier_kwargs={
            "ignore_pretraining_limits": True,
            "inference_config": {"SUBSAMPLE_SAMPLES": 50_000},
            "model_path": CLASSIFIER_CKPT,
        },
    )
    # Output dir cleaned up after fit; in-memory model is what we use to predict.
    with tempfile.TemporaryDirectory() as tmp:
        ft.fit(X_tr, y_tr, output_dir=Path(tmp))
    return ft


def predict_pos(ft, X) -> np.ndarray:
    proba = ft.predict_proba(X)
    classes = ft.finetuned_inference_classifier_.classes_
    pos_idx = int(np.where(classes == 1)[0][0]) if 1 in classes else 1
    return proba[:, pos_idx]


def metrics(y_true, p_pos) -> dict:
    proba2 = np.column_stack([1 - p_pos, p_pos])
    return {
        "roc_auc": float(roc_auc_score(y_true, p_pos)),
        "pr_auc": float(average_precision_score(y_true, p_pos)),
        "log_loss": float(log_loss(y_true, proba2, labels=[0, 1])),
        "accuracy": float(accuracy_score(y_true, p_pos >= 0.5)),
    }


def run_phase(phase: str) -> dict:
    print(f"\n=== {phase} ===")
    df = pd.read_parquet(JOINED_ROOT / f"{phase}.parquet")
    print(f"  loaded {df.shape}")

    X_all = preprocess_features(df)
    print(f"  feature frame: {X_all.shape}  "
          f"({(X_all.dtypes == 'category').sum()} cat, "
          f"{(X_all.dtypes != 'category').sum()} numeric)")

    train_nct, test_nct = train_test_split(
        np.asarray(df.index, dtype=object), test_size=TEST_FRAC, random_state=SEED
    )
    train_idx = pd.Index(train_nct)
    test_idx = pd.Index(test_nct)

    results = {
        "phase": phase, "n_total": int(len(df)),
        "n_train_nct": len(train_nct), "n_test_nct": len(test_nct),
        "layers": {},
    }
    full_test_proba: dict[str, pd.Series] = {}

    # ------------------------------------------------------------ L1
    print("\n  -- L1 Execution --")
    mask_tr = df["execution_pass"].notna() & df.index.isin(train_idx)
    mask_te = df["execution_pass"].notna() & df.index.isin(test_idx)
    y_tr = df.loc[mask_tr, "execution_pass"].astype(int).values
    y_te = df.loc[mask_te, "execution_pass"].astype(int).values
    X_tr = X_all.loc[mask_tr]
    X_te = X_all.loc[mask_te]
    print(f"     train: {X_tr.shape}, test: {X_te.shape}, "
          f"train pos rate: {y_tr.mean():.3f}")
    t0 = time.perf_counter()
    ft_l1 = fit_tabpfn_finetune(X_tr, y_tr)
    p_te = predict_pos(ft_l1, X_te)
    m_l1 = metrics(y_te, p_te)
    full_test_proba["L1"] = pd.Series(
        predict_pos(ft_l1, X_all.loc[test_idx]), index=test_idx
    )
    del ft_l1
    gc.collect()
    torch.cuda.empty_cache()
    results["layers"]["L1_execution"] = {
        "label": "execution_pass = NOT (dropout_YN==1 OR failure_reason=='poor enrollment')",
        "n_train": int(len(X_tr)), "n_test": int(len(X_te)),
        "train_class_balance": {"pos": int((y_tr == 1).sum()), "neg": int((y_tr == 0).sum())},
        "fit_time_s": time.perf_counter() - t0,
        **m_l1,
    }
    print(f"     ROC-AUC={m_l1['roc_auc']:.4f}  PR-AUC={m_l1['pr_auc']:.4f}  "
          f"LogLoss={m_l1['log_loss']:.4f}  Acc={m_l1['accuracy']:.4f}  "
          f"({results['layers']['L1_execution']['fit_time_s']:.1f}s)")

    # ------------------------------------------------------------ L2
    print("\n  -- L2 Biology --")
    base_l2 = df["execution_pass"].eq(True) & df["biology_pass"].notna()
    mask_tr = base_l2 & df.index.isin(train_idx)
    mask_te = base_l2 & df.index.isin(test_idx)
    y_tr = df.loc[mask_tr, "biology_pass"].astype(int).values
    y_te = df.loc[mask_te, "biology_pass"].astype(int).values
    X_tr = X_all.loc[mask_tr]
    X_te = X_all.loc[mask_te]
    print(f"     train: {X_tr.shape}, test: {X_te.shape}, "
          f"train pos rate: {y_tr.mean():.3f}")
    t0 = time.perf_counter()
    ft_l2 = fit_tabpfn_finetune(X_tr, y_tr)
    p_te = predict_pos(ft_l2, X_te)
    m_l2 = metrics(y_te, p_te)
    full_test_proba["L2"] = pd.Series(
        predict_pos(ft_l2, X_all.loc[test_idx]), index=test_idx
    )
    del ft_l2
    gc.collect()
    torch.cuda.empty_cache()
    results["layers"]["L2_biology"] = {
        "label": "biology_pass per CASE expression (approval=1 ⇒ TRUE, "
                 "failure_reason=='efficacy' ⇒ FALSE, "
                 "failure_reason known and != 'efficacy' ⇒ TRUE)",
        "n_train": int(len(X_tr)), "n_test": int(len(X_te)),
        "train_class_balance": {"pos": int((y_tr == 1).sum()), "neg": int((y_tr == 0).sum())},
        "fit_time_s": time.perf_counter() - t0,
        **m_l2,
    }
    print(f"     ROC-AUC={m_l2['roc_auc']:.4f}  PR-AUC={m_l2['pr_auc']:.4f}  "
          f"LogLoss={m_l2['log_loss']:.4f}  Acc={m_l2['accuracy']:.4f}  "
          f"({results['layers']['L2_biology']['fit_time_s']:.1f}s)")

    # ------------------------------------------------------------ L3
    print("\n  -- L3 Regulatory --")
    base_l3 = (
        df["execution_pass"].eq(True)
        & df["biology_pass"].eq(True)
        & df["regulatory_pass"].notna()
    )
    mask_tr = base_l3 & df.index.isin(train_idx)
    mask_te = base_l3 & df.index.isin(test_idx)
    y_tr = df.loc[mask_tr, "regulatory_pass"].astype(int).values
    y_te = df.loc[mask_te, "regulatory_pass"].astype(int).values
    X_tr = X_all.loc[mask_tr]
    X_te = X_all.loc[mask_te]
    print(f"     train: {X_tr.shape}, test: {X_te.shape}, "
          f"train pos rate: {y_tr.mean():.3f}")
    t0 = time.perf_counter()
    ft_l3 = fit_tabpfn_finetune(X_tr, y_tr)
    p_te = predict_pos(ft_l3, X_te)
    m_l3 = metrics(y_te, p_te)
    full_test_proba["L3"] = pd.Series(
        predict_pos(ft_l3, X_all.loc[test_idx]), index=test_idx
    )
    del ft_l3
    gc.collect()
    torch.cuda.empty_cache()
    results["layers"]["L3_regulatory"] = {
        "label": "regulatory_pass = (approval_outcome == 1)",
        "n_train": int(len(X_tr)), "n_test": int(len(X_te)),
        "train_class_balance": {"pos": int((y_tr == 1).sum()), "neg": int((y_tr == 0).sum())},
        "fit_time_s": time.perf_counter() - t0,
        **m_l3,
    }
    print(f"     ROC-AUC={m_l3['roc_auc']:.4f}  PR-AUC={m_l3['pr_auc']:.4f}  "
          f"LogLoss={m_l3['log_loss']:.4f}  Acc={m_l3['accuracy']:.4f}  "
          f"({results['layers']['L3_regulatory']['fit_time_s']:.1f}s)")

    # ------------------------------------------------------------ Joint
    print("\n  -- Joint approval prediction --")
    has_approval = df["approval_outcome"].notna() & df.index.isin(test_idx)
    joint_idx = df.index[has_approval]
    p_joint = (
        full_test_proba["L1"].loc[joint_idx]
        * full_test_proba["L2"].loc[joint_idx]
        * full_test_proba["L3"].loc[joint_idx]
    )
    y_joint = df.loc[joint_idx, "approval_outcome"].astype(int).values
    m_j = metrics(y_joint, p_joint.values)
    results["joint"] = {
        "definition": "P(L1_pass) × P(L2_pass) × P(L3_pass) vs approval_outcome",
        "n_test": int(len(joint_idx)),
        "test_pos_rate": float(y_joint.mean()),
        **m_j,
    }
    print(f"     n={len(joint_idx)}  test pos rate={y_joint.mean():.3f}")
    print(f"     ROC-AUC={m_j['roc_auc']:.4f}  PR-AUC={m_j['pr_auc']:.4f}  "
          f"LogLoss={m_j['log_loss']:.4f}  Acc={m_j['accuracy']:.4f}")

    return results


def fmt(x):
    return f"{x:.4f}" if isinstance(x, float) else str(x)


def write_markdown(all_results: list[dict]) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    lines = []
    lines.append("# 3-Layer Cascade × fine-tuned TabPFN — baseline\n")
    lines.append("\n")
    lines.append(
        "Model: fine-tuned TabPFN (FinetunedTabPFNClassifier on "
        "`tabpfn-v2.5-classifier-v2.5_default.ckpt`, "
        f"epochs={FT_EPOCHS}, lr={LR}, n_estimators={N_EST} "
        f"(shared across fine-tune/val/inference), no early stopping).  \n"
    )
    lines.append(
        f"Split: NCT-level 80/20 per phase (seed={SEED}). All layers within a "
        "phase share the same split — a test NCT in L3 is never in L1/L2 train.  \n"
        "Cascade filter uses **real upstream labels** (not predictions) — "
        "avoids contaminating downstream layers with upstream-model errors.\n"
    )

    lines.append("## Per-layer test metrics (per phase)\n")
    lines.append(
        "| Phase | Layer | n_train | n_test | train pos rate | ROC-AUC | PR-AUC | LogLoss | Acc |"
    )
    lines.append("|---|---|---:|---:|---:|---:|---:|---:|---:|")
    for r in all_results:
        for layer_name, m in r["layers"].items():
            pos_rate = m['train_class_balance']['pos'] / max(
                m['train_class_balance']['pos'] + m['train_class_balance']['neg'], 1
            )
            lines.append(
                f"| {r['phase']} | {layer_name} | {m['n_train']} | {m['n_test']} | "
                f"{pos_rate:.3f} | {fmt(m['roc_auc'])} | {fmt(m['pr_auc'])} | "
                f"{fmt(m['log_loss'])} | {fmt(m['accuracy'])} |"
            )
    lines.append("")

    lines.append(
        "Note: when L3 reports very high ROC-AUC, recall (per "
        "`cascade_xgboost/cascade_results.md`) that L3's training pool consists "
        "of two systematically different groups — \"approved trials (label=1)\" "
        "and \"failed-for-non-efficacy-reasons trials (label=0)\". These differ "
        "in metadata features (trial phase, enrollment size, sponsor type) and "
        "are therefore easy to separate. This is NOT leakage (both "
        "`approval_outcome` and `failure_reason` are excluded via `LABEL_DROP`); "
        "rather, it is a discrimination problem within a pre-filtered subset, "
        "not a pure \"predict whether a future trial will be approved\" task.\n"
    )

    lines.append("## Joint approval metric (per phase)\n")
    lines.append(
        "P(approved) = P(L1_pass) × P(L2_pass) × P(L3_pass), evaluated on the "
        "test NCTs that have `approval_outcome` known.\n"
    )
    lines.append("| Phase | n_test | test pos rate | ROC-AUC | PR-AUC | LogLoss | Acc |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|")
    for r in all_results:
        j = r["joint"]
        lines.append(
            f"| {r['phase']} | {j['n_test']} | {j['test_pos_rate']:.3f} | "
            f"{fmt(j['roc_auc'])} | {fmt(j['pr_auc'])} | "
            f"{fmt(j['log_loss'])} | {fmt(j['accuracy'])} |"
        )
    lines.append("")

    lines.append("## Layer definitions\n")
    lines.append(
        "Cascade is **strictly nested**: every L3-trainable trial is in L2's pool, "
        "every L2-trainable trial is in L1's pool. Cascade filters use **real upstream "
        "labels**, not predictions.\n"
    )
    lines.append(
        "### Layer 1 — Execution\n\n"
        "**Task**: Using trial registration-time metadata features, predict whether the "
        "trial will fail at the execution layer (high dropout or unable to enroll).  \n"
        "**Training filter**: No upstream filter; samples only need to have an L1 label "
        "signal observable.  \n"
        "**Label SQL**:\n"
        "```sql\n"
        "execution_fail = (dropout_YN = 1) OR (failure_reason = 'poor enrollment')\n"
        "execution_pass = NOT execution_fail\n"
        "-- observable when: dropout_YN IS NOT NULL OR failure_reason IS NOT NULL\n"
        "-- (NaN does not trigger either condition; at least one signal must be known\n"
        "--  to enter the training pool)\n"
        "```\n\n"
        "### Layer 2 — Biology\n\n"
        "**Task**: Among trials that have passed L1, predict whether the drug's "
        "biological efficacy will pass (will not fail due to efficacy).  \n"
        "**Training filter**: `execution_pass = TRUE` (filtered by the real L1 label), "
        "AND `biology_pass` is observable.  \n"
        "**Label SQL**:\n"
        "```sql\n"
        "biology_pass =\n"
        "  CASE\n"
        "    WHEN approval_outcome = 1            THEN TRUE   -- approved => biology must have passed\n"
        "    WHEN failure_reason = 'efficacy'     THEN FALSE  -- failed for efficacy => did not pass\n"
        "    WHEN failure_reason IS NOT NULL      THEN TRUE   -- failed for other reasons => biology passed\n"
        "    ELSE NULL\n"
        "  END\n"
        "-- observable when: approval_outcome = 1 OR failure_reason IS NOT NULL\n"
        "```\n\n"
        "### Layer 3 — Regulatory\n\n"
        "**Task**: Among trials that have passed both L1 and L2, predict whether the "
        "trial will be approved by regulators.  \n"
        "**Training filter**: `execution_pass = TRUE` AND `biology_pass = TRUE` "
        "(double real-label filter), AND `approval_outcome` is known.  \n"
        "**Label SQL**:\n"
        "```sql\n"
        "regulatory_pass = (approval_outcome = 1)\n"
        "-- observable when: approval_outcome IS NOT NULL\n"
        "-- Note: the L3 training pool consists of two groups — approval=1 (label TRUE)\n"
        "--   and failed-non-efficacy with known approval (label FALSE)\n"
        "```\n\n"
        "### Cascade nesting property\n\n"
        "L3 ⊆ L2 ⊆ L1 (trainable subsets strictly nested):\n"
        "- L1 trainable: at least one of dropout_YN or failure_reason is observable\n"
        "- L2 trainable: subset of L1 with execution_pass=TRUE AND (approval=1 OR failure_reason known)\n"
        "- L3 trainable: subset of L2 with biology_pass=TRUE AND approval_outcome known\n"
    )

    (OUT_DIR / "cascade_results.md").write_text("\n".join(lines))


def main() -> None:
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA required.")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    all_results: list[dict] = []
    aggregate = {
        "generated": datetime.now().isoformat(timespec="seconds"),
        "device": torch.cuda.get_device_name(0),
        "seed": SEED,
        "fine_tune": {"epochs": FT_EPOCHS, "lr": LR, "n_est": N_EST},
        "phases": [],
    }
    for phase in PHASES:
        r = run_phase(phase)
        all_results.append(r)
        aggregate["phases"].append(r)
        (OUT_DIR / f"{phase}.json").write_text(json.dumps(r, indent=2))
        (OUT_DIR / "all_metrics.json").write_text(json.dumps(aggregate, indent=2))
        write_markdown(all_results)
    print(f"\nWrote {OUT_DIR / 'cascade_results.md'}")


if __name__ == "__main__":
    main()
