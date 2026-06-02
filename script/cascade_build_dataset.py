"""Build joined wide tables per phase for the 3-layer cascade.

For each phase, joins features and labels from the 6 cascade subtasks by
NCT id (train + test pooled — we re-split downstream), derives cascade
labels, writes one parquet to /data2/zhu11/TB/dataset/TrialBench_joined/.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

DATA_ROOT = Path("/data2/zhu11/TB/dataset/TrialBench")
OUT_ROOT = Path("/data2/zhu11/TB/dataset/TrialBench_joined")
PHASES = ["Phase1", "Phase2", "Phase3", "Phase4"]

SUBTASKS = [
    "patient-dropout-event-forecasting",
    "trial-duration-forecasting",
    "serious-adverse-event-forecasting",
    "mortality-event-prediction",
    "trial-failure-reason-identification",
    "trial-approval-forecasting",
]

# Map each subtask's y columns to globally unique label names.
LABEL_MAP = {
    "patient-dropout-event-forecasting": {"Y/N": "dropout_YN", "droupout_rate": "dropout_rate"},
    "trial-duration-forecasting": {
        "start_date": "start_date", "completion_date": "completion_date",
        "time_day": "duration_day", "month": "duration_month", "year": "duration_year",
    },
    "serious-adverse-event-forecasting": {"Y/N": "sae_YN", "serious_adverse_rate": "sae_rate"},
    "mortality-event-prediction": {"Y/N": "mortality_YN", "mortality_rate": "mortality_rate"},
    "trial-failure-reason-identification": {"failure_reason": "failure_reason"},
    "trial-approval-forecasting": {"outcome": "approval_outcome"},
}


def load_subtask(subtask: str, phase: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    xs, ys = [], []
    for split in ["train", "test"]:
        x_path = DATA_ROOT / subtask / phase / f"{split}_x.csv"
        y_path = DATA_ROOT / subtask / phase / f"{split}_y.csv"
        x = pd.read_csv(x_path, index_col=0)
        y = pd.read_csv(y_path, index_col=0)
        y = y.loc[x.index]
        xs.append(x)
        ys.append(y)
    return pd.concat(xs, axis=0), pd.concat(ys, axis=0)


def build_phase(phase: str) -> pd.DataFrame:
    print(f"=== {phase} ===")
    Xs, Ys = [], []
    for subtask in SUBTASKS:
        X, y = load_subtask(subtask, phase)
        Xs.append(X)
        renamed = y.rename(columns=LABEL_MAP[subtask])
        renamed = renamed[list(LABEL_MAP[subtask].values())]
        Ys.append(renamed)
        print(f"  {subtask:50s} X={X.shape}  y_cols={list(renamed.columns)}")

    # Concatenate all X (keep first occurrence per NCT — features are trial metadata)
    X_all = pd.concat(Xs, axis=0)
    X_all = X_all[~X_all.index.duplicated(keep="first")]

    # Combine y across subtasks: each subtask contributes its own columns;
    # take first non-null per NCT per column.
    y_all = pd.concat(Ys, axis=0)
    y_all = y_all.groupby(level=0).first()

    df = X_all.join(y_all, how="left")
    df.index.name = "nctid"

    # ---- Derive cascade labels ----
    # L1 primary: execution_fail = (dropout_YN==1) OR (failure_reason=='poor enrollment')
    has_dropout = df["dropout_YN"].notna()
    has_fr = df["failure_reason"].notna()
    has_signal_L1 = has_dropout | has_fr

    dropout_fail = (df["dropout_YN"] == 1).astype("boolean")
    dropout_fail[~has_dropout] = pd.NA
    poor_enroll = (df["failure_reason"] == "poor enrollment").astype("boolean")
    poor_enroll[~has_fr] = pd.NA

    exec_fail = (dropout_fail.fillna(False) | poor_enroll.fillna(False)).astype("boolean")
    exec_fail[~has_signal_L1] = pd.NA
    df["execution_fail"] = exec_fail
    df["execution_pass"] = (~exec_fail).astype("boolean")

    # ---- L2 primary (nested with L3) ----
    # biology_pass:
    #   TRUE  if approval_outcome == 1                          (approved ⇒ biology must have passed)
    #   FALSE if failure_reason == 'efficacy'                   (failed for efficacy)
    #   TRUE  if failure_reason known and != 'efficacy'         (failed for non-bio reason)
    #   NaN   otherwise (no signal — unknown)
    has_approval = df["approval_outcome"].notna()
    approved_pos = (df["approval_outcome"] == 1) & has_approval

    # Start with NaN
    bio_pass = pd.Series(pd.NA, index=df.index, dtype="boolean")
    # failure_reason known → label by failure_reason
    fr_known_efficacy = has_fr & (df["failure_reason"] == "efficacy")
    fr_known_other = has_fr & (df["failure_reason"] != "efficacy")
    bio_pass[fr_known_efficacy] = False
    bio_pass[fr_known_other] = True
    # approval == 1 overrides as TRUE (approved trials biologically passed by construction)
    bio_pass[approved_pos] = True

    df["biology_pass"] = bio_pass
    df["biology_fail"] = (~bio_pass).astype("boolean")

    # L3 primary: approval_outcome (raw); cascade filter applied at training time
    has_approval = df["approval_outcome"].notna()
    reg_pass = (df["approval_outcome"] == 1).astype("boolean")
    reg_pass[~has_approval] = pd.NA
    df["regulatory_pass"] = reg_pass

    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    out_path = OUT_ROOT / f"{phase}.parquet"
    df.to_parquet(out_path)
    print(f"  wrote {out_path}  shape={df.shape}")
    return df


def main() -> None:
    for phase in PHASES:
        build_phase(phase)


if __name__ == "__main__":
    main()
