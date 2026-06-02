"""Per-phase Tier 1 tuning of TabPFN on TrialBench subtasks.

Runs the full Tier 1 pipeline (val-based hp selection, full-train refit,
seed ensemble, threshold tuning) independently on EACH (subtask × phase)
pair — i.e. for each phase we use only that phase's train data for
fine-tune and only that phase's test data for evaluation.

Outputs:
  /data2/zhu11/TB/results/TrialBench_TabPFN_tier1_per_phase/
      zero_shot_per_phase.md
      all_metrics.json
      per_task/<subtask>__<phase>.json
"""

from __future__ import annotations

import argparse
import json
import sys
import traceback
from datetime import datetime
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).parent))
from trialbench_zero_shot_table import TASKS, NOT_APPLICABLE  # noqa: E402
from tier1_tune import (  # noqa: E402
    PRIMARY,
    run_classification_task,
    run_regression_task,
)

OUT_DIR = Path("/data2/zhu11/TB/results/TrialBench_TabPFN_tier1_per_phase")
PER_TASK_DIR = OUT_DIR / "per_task"


def fmt(x):
    return f"{x:.4f}" if isinstance(x, float) else str(x)


def write_markdown(records: list[dict], args) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    by_subtask: dict[str, list[dict]] = {}
    for r in records:
        if r.get("error"):
            by_subtask.setdefault(r["task"], []).append(r)
            continue
        by_subtask.setdefault(r["task"], []).append(r)

    lines = []
    lines.append("# TrialBench × TabPFN-2.5 — **Per-phase** Tier-1 results\n")
    lines.append(
        f"Generated: {datetime.now().isoformat(timespec='seconds')}  \n"
        f"Device: {torch.cuda.get_device_name(0)}  \n"
        f"Run config: n_est_grid={args.n_est_grid}, lr_grid={args.lr_grid}, "
        f"ft_epochs={args.ft_epochs}, n_est_ft={args.n_est_ft}, "
        f"ens_seeds={args.ens_seeds}\n"
    )
    lines.append(
        "**Per-phase isolation**: each row uses ONLY that phase's train CSV "
        "(80/20 → train'/val for hp selection, then refit best config on full "
        "phase-train) and ONLY that phase's test CSV. No cross-phase mixing.\n"
    )
    lines.append(
        "`vanilla` = best Phase-A baseline (no fine-tune, val-selected ckpt + "
        "n_estimators). `Tier-1` = full pipeline test result. `Δ` = Tier-1 − "
        "vanilla, both measured on the same per-phase test set.\n"
    )

    # Group subtasks by type so we can pick the right metric.
    type_order = ["binary", "multiclass", "regression"]
    subtask_type = {r["task"]: r["type"] for r in records if "type" in r}

    for t_type in type_order:
        subtasks = sorted(
            {n for n, t in subtask_type.items() if t == t_type}
        )
        if not subtasks:
            continue
        primary = PRIMARY[t_type]
        type_label = {
            "binary": "Binary classification",
            "multiclass": "Multiclass classification",
            "regression": "Regression",
        }[t_type]
        lines.append(f"## {type_label} (per phase, primary metric = `{primary}`)\n")

        for subtask in subtasks:
            lines.append(f"### {subtask}\n")
            if t_type == "binary":
                header = (
                    f"| Phase | n_train | n_test | ROC-AUC vanilla | "
                    f"ROC-AUC Tier-1 | Δ | PR-AUC | LogLoss | Acc (tuned) | "
                    f"best_threshold | Selected config |"
                )
                sep = "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|"
            elif t_type == "multiclass":
                header = (
                    f"| Phase | n_classes | n_train | n_test | Acc vanilla | "
                    f"Acc Tier-1 | Δ | F1-macro | LogLoss | Selected config |"
                )
                sep = "|---|---:|---:|---:|---:|---:|---:|---:|---:|---|"
            else:
                header = (
                    f"| Phase | n_train | n_test | R² vanilla | R² Tier-1 | "
                    f"Δ | MAE | RMSE | Selected config |"
                )
                sep = "|---|---:|---:|---:|---:|---:|---:|---:|---|"
            lines.append(header)
            lines.append(sep)

            phase_recs = sorted(
                [r for r in by_subtask.get(subtask, []) if not r.get("error")],
                key=lambda r: r.get("phase", ""),
            )
            for r in phase_recs:
                vanilla = max(r["phase_a"], key=lambda x: x[primary])[primary]
                tier1 = r["test"][primary]
                delta = tier1 - vanilla
                best = r["best_on_val"]
                cfg = (
                    f"phase={best['phase']} ckpt={best['ckpt']} "
                    f"n_est={best['n_estimators']}"
                    + (f" lr={best['lr']:.0e}" if 'lr' in best else "")
                    + (f" log={int(best['y_log'])}" if 'y_log' in best else "")
                    + (" no-imp" if best.get("no_improvement") else "")
                )
                t = r["test"]
                if t_type == "binary":
                    row = (
                        f"| {r['phase']} | {r['n_train_full']} | {r['n_test']} | "
                        f"{fmt(vanilla)} | **{fmt(tier1)}** | "
                        f"{('+' if delta >= 0 else '')}{delta:.4f} | "
                        f"{fmt(t['pr_auc'])} | {fmt(t['log_loss'])} | "
                        f"{fmt(t.get('accuracy_tuned', t['accuracy']))} | "
                        f"{fmt(t.get('best_threshold', 0.5))} | `{cfg}` |"
                    )
                elif t_type == "multiclass":
                    row = (
                        f"| {r['phase']} | {r['n_classes']} | {r['n_train_full']} | "
                        f"{r['n_test']} | "
                        f"{fmt(vanilla)} | **{fmt(tier1)}** | "
                        f"{('+' if delta >= 0 else '')}{delta:.4f} | "
                        f"{fmt(t['f1_macro'])} | {fmt(t['log_loss'])} | `{cfg}` |"
                    )
                else:
                    row = (
                        f"| {r['phase']} | {r['n_train_full']} | {r['n_test']} | "
                        f"{fmt(vanilla)} | **{fmt(tier1)}** | "
                        f"{('+' if delta >= 0 else '')}{delta:.4f} | "
                        f"{fmt(t['mae'])} | {fmt(t['rmse'])} | `{cfg}` |"
                    )
                lines.append(row)
            # Errored phases for this subtask, if any
            for r in by_subtask.get(subtask, []):
                if r.get("error"):
                    lines.append(
                        f"| {r.get('phase', '?')} | — | — | — | — | — | "
                        f"ERROR: {r['error']} |"
                    )
            lines.append("")

    lines.append("## Not applicable\n")
    lines.append("| Task | Reason |")
    lines.append("|---|---|")
    for name, reason in NOT_APPLICABLE:
        lines.append(f"| {name} | {reason} |")
    lines.append("")

    lines.append("## Methodology notes\n")
    lines.append(
        "- For each (subtask, phase): load only that phase's train/test CSVs. "
        "Split phase-train 80/20 → train'/val (stratified for classification). "
        "Run the same pipeline as `tier1_tune.py`: Phase A (baseline sweep), "
        "Phase B (fine-tune sweep with val early-stop), pick winner on val, "
        "Phase C (refit best config on full phase-train, k-seed ensemble), "
        "Phase D (binary: tune threshold on val_proba).\n"
        "- `vanilla` column = the best Phase-A baseline (val-selected ckpt × "
        "n_estimators, no fine-tune). It already includes the 'just bump "
        "n_estimators + try both ckpts' improvements.\n"
        "- `Tier-1` column = full pipeline (vanilla + fine-tune + 3-seed "
        "ensemble + threshold tuning where applicable).\n"
        "- All hp/ckpt/threshold choices made on val. Test evaluated once.\n"
        "- Per-(subtask, phase) full sweep details: `per_task/<subtask>__<phase>.json`.\n"
    )

    (OUT_DIR / "zero_shot_per_phase.md").write_text("\n".join(lines))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n-est-grid", type=int, nargs="+", default=[4, 8, 16, 32])
    parser.add_argument("--lr-grid", type=float, nargs="+", default=[1e-5, 2e-5, 5e-5])
    parser.add_argument("--ft-epochs", type=int, default=30)
    parser.add_argument("--n-est-ft", type=int, default=2)
    parser.add_argument("--ens-seeds", type=int, nargs="+", default=[0, 1, 2])
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--phases", type=str, nargs="+",
                        default=["Phase1", "Phase2", "Phase3", "Phase4"])
    parser.add_argument("--only", type=str, default=None,
                        help="Comma-separated subtask substrings to run.")
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
    print(f"Subtasks: {[t['name'] for t in tasks]}")
    print(f"Phases:   {args.phases}")
    print(f"args: {vars(args)}")

    records: list[dict] = []
    aggregate = {
        "generated": datetime.now().isoformat(timespec="seconds"),
        "device": torch.cuda.get_device_name(0),
        "args": vars(args),
        "records": [],
    }

    for task in tasks:
        task_phases = [p for p in args.phases if p in task.get("phases", [])]
        for phase in task_phases:
            print(f"\n>>>>>>>>>> {task['name']} :: {phase} <<<<<<<<<<")
            phase_task = {**task, "phases": [phase]}
            try:
                if task["type"] in ("binary", "multiclass"):
                    rec = run_classification_task(phase_task, args)
                else:
                    rec = run_regression_task(phase_task, args)
            except Exception as e:  # noqa: BLE001
                print(f"  ERROR: {e}")
                traceback.print_exc()
                rec = {"task": task["name"], "type": task["type"],
                       "phase": phase,
                       "error": f"{type(e).__name__}: {e}"}
            rec["phase"] = phase  # tag the record
            records.append(rec)
            aggregate["records"].append(rec)
            (PER_TASK_DIR / f"{task['name']}__{phase}.json").write_text(
                json.dumps(rec, indent=2)
            )
            (OUT_DIR / "all_metrics.json").write_text(json.dumps(aggregate, indent=2))
            write_markdown(records, args)

    print(f"\nWrote {OUT_DIR / 'zero_shot_per_phase.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
