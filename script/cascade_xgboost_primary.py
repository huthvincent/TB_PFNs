"""3-layer cascade with XGBoost — primary models only (no aux, no stacker).

Per phase, runs:
  L1 (Execution):  primary = NOT (dropout_YN==1 OR failure_reason=='poor enrollment')
                   train on trials with L1 label observable.
  L2 (Biology, strict): primary = NOT (failure_reason == 'efficacy')
                   train on trials with execution_pass==True AND failure_reason known.
  L3 (Regulatory, relaxed): primary = (approval_outcome == 1)
                   train on trials with approval_outcome known AND
                   NOT (dropout_YN==1 OR failure_reason in {'poor enrollment','efficacy'}).

Also computes a JOINT metric on the test set:
  P(approved) = P(L1_pass) × P(L2_pass) × P(L3_pass)
  measured against the actual approval_outcome.

Outputs to /data2/zhu11/TB/results/cascade_xgboost/.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    log_loss,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split

JOINED_ROOT = Path("/data2/zhu11/TB/dataset/TrialBench_joined")
OUT_DIR = Path("/data2/zhu11/TB/results/cascade_xgboost")
PHASES = ["Phase1", "Phase2", "Phase3", "Phase4"]
SEED = 42
TEST_FRAC = 0.20

# Long-text / list-valued / very-high-cardinality columns (drop from features).
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

# All label / cascade-derived / future-info columns (drop from features).
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


def fit_xgb(X_tr, y_tr, X_te, y_te):
    n_pos = int((y_tr == 1).sum())
    n_neg = int((y_tr == 0).sum())
    spw = n_neg / max(n_pos, 1)
    clf = xgb.XGBClassifier(
        n_estimators=500,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.9,
        colsample_bytree=0.9,
        scale_pos_weight=spw,
        tree_method="hist",
        enable_categorical=True,
        random_state=SEED,
        n_jobs=-1,
        eval_metric="logloss",
    )
    clf.fit(X_tr, y_tr)
    proba = clf.predict_proba(X_te)[:, 1]
    return clf, proba, {"scale_pos_weight": spw, "n_train_pos": n_pos, "n_train_neg": n_neg}


def metrics(y_true, proba) -> dict:
    return {
        "roc_auc": float(roc_auc_score(y_true, proba)),
        "pr_auc": float(average_precision_score(y_true, proba)),
        "log_loss": float(log_loss(y_true, proba, labels=[0, 1])),
        "accuracy": float(accuracy_score(y_true, proba >= 0.5)),
    }


def run_phase(phase: str) -> dict:
    print(f"\n=== {phase} ===")
    df = pd.read_parquet(JOINED_ROOT / f"{phase}.parquet")
    print(f"  loaded {df.shape}")

    # One feature frame per phase (consistent columns across layers).
    X_all = preprocess_features(df)
    print(f"  feature frame: {X_all.shape}  "
          f"({(X_all.dtypes == 'category').sum()} cat, "
          f"{(X_all.dtypes != 'category').sum()} numeric)")

    # NCT-level 80/20 random split (shared across all layers).
    train_nct, test_nct = train_test_split(
        np.asarray(df.index, dtype=object), test_size=TEST_FRAC, random_state=SEED
    )
    train_idx = pd.Index(train_nct)
    test_idx = pd.Index(test_nct)

    results = {"phase": phase, "n_total": int(len(df)),
               "n_train_nct": len(train_nct), "n_test_nct": len(test_nct),
               "layers": {}}

    # For joint metric: keep each layer's proba on the FULL test split.
    full_test_proba = {}

    # ------------------------------------------------------------ L1
    print("\n  -- L1 Execution --")
    mask_tr = df["execution_pass"].notna() & df.index.isin(train_idx)
    mask_te = df["execution_pass"].notna() & df.index.isin(test_idx)
    y_tr = df.loc[mask_tr, "execution_pass"].astype(int).values
    y_te = df.loc[mask_te, "execution_pass"].astype(int).values
    X_tr = X_all.loc[mask_tr]
    X_te = X_all.loc[mask_te]
    print(f"     train: {X_tr.shape}, test: {X_te.shape}, "
          f"train pos rate: {y_tr.mean():.3f}, test pos rate: {y_te.mean():.3f}")
    clf_l1, proba_te_l1, train_info = fit_xgb(X_tr, y_tr, X_te, y_te)
    m_l1 = metrics(y_te, proba_te_l1)
    full_test_proba["L1"] = pd.Series(
        clf_l1.predict_proba(X_all.loc[test_idx])[:, 1], index=test_idx
    )
    results["layers"]["L1_execution"] = {
        "label": "execution_pass = NOT (dropout_YN==1 OR failure_reason=='poor enrollment')",
        "n_train": int(len(X_tr)), "n_test": int(len(X_te)),
        "train_class_balance": {"pos": train_info["n_train_pos"], "neg": train_info["n_train_neg"]},
        "scale_pos_weight": train_info["scale_pos_weight"],
        **m_l1,
    }
    print(f"     ROC-AUC={m_l1['roc_auc']:.4f}  PR-AUC={m_l1['pr_auc']:.4f}  "
          f"LogLoss={m_l1['log_loss']:.4f}  Acc={m_l1['accuracy']:.4f}")

    # ------------------------------------------------------------ L2 (strict)
    print("\n  -- L2 Biology (strict) --")
    base = df["execution_pass"].eq(True) & df["biology_pass"].notna()
    mask_tr = base & df.index.isin(train_idx)
    mask_te = base & df.index.isin(test_idx)
    if mask_tr.sum() < 50 or mask_te.sum() < 20:
        print(f"     SKIP — too few trainable trials "
              f"(train={int(mask_tr.sum())}, test={int(mask_te.sum())})")
        results["layers"]["L2_biology"] = {
            "label": "biology_pass = NOT (failure_reason == 'efficacy')",
            "skipped": True,
            "n_train": int(mask_tr.sum()), "n_test": int(mask_te.sum()),
        }
        full_test_proba["L2"] = pd.Series(0.5, index=test_idx)
    else:
        y_tr = df.loc[mask_tr, "biology_pass"].astype(int).values
        y_te = df.loc[mask_te, "biology_pass"].astype(int).values
        X_tr = X_all.loc[mask_tr]
        X_te = X_all.loc[mask_te]
        print(f"     train: {X_tr.shape}, test: {X_te.shape}, "
              f"train pos rate: {y_tr.mean():.3f}, test pos rate: {y_te.mean():.3f}")
        clf_l2, proba_te_l2, train_info = fit_xgb(X_tr, y_tr, X_te, y_te)
        m_l2 = metrics(y_te, proba_te_l2)
        full_test_proba["L2"] = pd.Series(
            clf_l2.predict_proba(X_all.loc[test_idx])[:, 1], index=test_idx
        )
        results["layers"]["L2_biology"] = {
            "label": "biology_pass = NOT (failure_reason == 'efficacy')",
            "n_train": int(len(X_tr)), "n_test": int(len(X_te)),
            "train_class_balance": {"pos": train_info["n_train_pos"], "neg": train_info["n_train_neg"]},
            "scale_pos_weight": train_info["scale_pos_weight"],
            **m_l2,
        }
        print(f"     ROC-AUC={m_l2['roc_auc']:.4f}  PR-AUC={m_l2['pr_auc']:.4f}  "
              f"LogLoss={m_l2['log_loss']:.4f}  Acc={m_l2['accuracy']:.4f}")

    # ------------------------------------------------------------ L3 (strict-nested)
    print("\n  -- L3 Regulatory (strict-nested) --")
    base = (
        df["execution_pass"].eq(True)
        & df["biology_pass"].eq(True)
        & df["regulatory_pass"].notna()
    )
    mask_tr = base & df.index.isin(train_idx)
    mask_te = base & df.index.isin(test_idx)
    y_tr = df.loc[mask_tr, "regulatory_pass"].astype(int).values
    y_te = df.loc[mask_te, "regulatory_pass"].astype(int).values
    X_tr = X_all.loc[mask_tr]
    X_te = X_all.loc[mask_te]
    print(f"     train: {X_tr.shape}, test: {X_te.shape}, "
          f"train pos rate: {y_tr.mean():.3f}, test pos rate: {y_te.mean():.3f}")
    clf_l3, proba_te_l3, train_info = fit_xgb(X_tr, y_tr, X_te, y_te)
    m_l3 = metrics(y_te, proba_te_l3)
    full_test_proba["L3"] = pd.Series(
        clf_l3.predict_proba(X_all.loc[test_idx])[:, 1], index=test_idx
    )
    results["layers"]["L3_regulatory"] = {
        "label": "regulatory_pass = (approval_outcome == 1)",
        "n_train": int(len(X_tr)), "n_test": int(len(X_te)),
        "train_class_balance": {"pos": train_info["n_train_pos"], "neg": train_info["n_train_neg"]},
        "scale_pos_weight": train_info["scale_pos_weight"],
        **m_l3,
    }
    print(f"     ROC-AUC={m_l3['roc_auc']:.4f}  PR-AUC={m_l3['pr_auc']:.4f}  "
          f"LogLoss={m_l3['log_loss']:.4f}  Acc={m_l3['accuracy']:.4f}")

    # ------------------------------------------------------------ Joint
    print("\n  -- Joint approval prediction --")
    has_approval = df["approval_outcome"].notna() & df.index.isin(test_idx)
    joint_idx = df.index[has_approval]
    if len(joint_idx) >= 20:
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
        print(f"     n={len(joint_idx)} approval pos rate={y_joint.mean():.3f}")
        print(f"     ROC-AUC={m_j['roc_auc']:.4f}  PR-AUC={m_j['pr_auc']:.4f}  "
              f"LogLoss={m_j['log_loss']:.4f}  Acc={m_j['accuracy']:.4f}")
    else:
        results["joint"] = {"skipped": True, "n_test": int(len(joint_idx))}

    return results


def fmt(x):
    return f"{x:.4f}" if isinstance(x, float) else str(x)


def write_markdown(all_results: list[dict]) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    lines = []
    lines.append("# 3-Layer Cascade × XGBoost — Primary-only baseline\n")
    lines.append(
        f"Generated: {datetime.now().isoformat(timespec='seconds')}  \n"
        f"Model: XGBoost (n_estimators=500, max_depth=6, lr=0.05, "
        f"`scale_pos_weight` per class balance, `enable_categorical=True`).  \n"
        f"Split: NCT-level random 80/20 per phase, `seed={SEED}`. "
        f"All layers within a phase share the same split — a test NCT in L3 is "
        f"never in L1/L2 train.  \n"
        f"Cascade filter uses **real upstream labels** (not predictions) — "
        f"avoids contaminating downstream layers with upstream-model errors.\n"
    )

    lines.append("## Per-layer test metrics (per phase)\n")
    lines.append(
        "| Phase | Layer | n_train | n_test | train pos rate | ROC-AUC | PR-AUC | LogLoss | Acc |"
    )
    lines.append("|---|---|---:|---:|---:|---:|---:|---:|---:|")
    for r in all_results:
        for layer_name, m in r["layers"].items():
            if m.get("skipped"):
                lines.append(
                    f"| {r['phase']} | {layer_name} | {m['n_train']} | {m['n_test']} | "
                    f"SKIPPED | — | — | — | — |"
                )
                continue
            pos_rate = m['train_class_balance']['pos'] / max(
                m['train_class_balance']['pos'] + m['train_class_balance']['neg'], 1
            )
            lines.append(
                f"| {r['phase']} | {layer_name} | {m['n_train']} | {m['n_test']} | "
                f"{pos_rate:.3f} | {fmt(m['roc_auc'])} | {fmt(m['pr_auc'])} | "
                f"{fmt(m['log_loss'])} | {fmt(m['accuracy'])} |"
            )
    lines.append("")

    lines.append("## Joint approval metric (per phase)\n")
    lines.append(
        "P(approved) = P(L1_pass) × P(L2_pass) × P(L3_pass), evaluated on the "
        "test NCTs that have `approval_outcome` known.\n"
    )
    lines.append("| Phase | n_test | test pos rate | ROC-AUC | PR-AUC | LogLoss | Acc |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|")
    for r in all_results:
        j = r.get("joint", {})
        if j.get("skipped"):
            lines.append(f"| {r['phase']} | {j.get('n_test', 0)} | — | — | — | — | — |")
            continue
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

    lines.append("## Notes\n")
    lines.append(
        "- No auxiliary labels, no stacking. Pure primary-label XGBoost classifiers.\n"
        "- `scale_pos_weight = n_neg / n_pos` from training set (automatic class imbalance handling).\n"
        "- `duration_day` / `completion_date` are **not** features (they're trial-completion-time info; would leak).\n"
        "- Categorical columns handled natively by XGBoost via `enable_categorical=True`.\n"
        "- L2 strict can have very few negatives per phase — read `train_class_balance` "
        "in `all_metrics.json` to spot small-sample issues.\n"
        "- Per-phase raw metrics: `<phase>.json`.\n"
    )

    (OUT_DIR / "cascade_results.md").write_text("\n".join(lines))


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    all_results = []
    aggregate = {
        "generated": datetime.now().isoformat(timespec="seconds"),
        "seed": SEED,
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
