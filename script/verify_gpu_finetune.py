"""GPU fine-tune verification for tabpfn-v2.5-classifier-v2.5_default.ckpt.

Runs a short fine-tune on a small dataset and asserts:
  - CUDA is actually used (allocated VRAM > 0 mid-train),
  - Validation log-loss after fine-tune is sane,
  - predict_proba returns well-formed probabilities.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import torch
from sklearn.datasets import load_breast_cancer
from sklearn.metrics import log_loss, roc_auc_score
from sklearn.model_selection import train_test_split

from tabpfn.finetuning.finetuned_classifier import FinetunedTabPFNClassifier

CKPT = Path("/data2/zhu11/TB/TabPFN/models/tabpfn-v2.5-classifier-v2.5_default.ckpt")
RANDOM_STATE = 0


def main() -> int:
    if not torch.cuda.is_available():
        print("CUDA not available", file=sys.stderr)
        return 1
    if not CKPT.is_file():
        print(f"Checkpoint missing: {CKPT}", file=sys.stderr)
        return 1

    print(f"Device: {torch.cuda.get_device_name(0)}")
    print(f"Checkpoint: {CKPT} ({CKPT.stat().st_size / 1e6:.1f} MB)")

    X, y = load_breast_cancer(return_X_y=True, as_frame=True)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
    )
    print(f"Train: {X_train.shape}, Test: {X_test.shape}")

    torch.cuda.reset_peak_memory_stats()
    mem_before = torch.cuda.memory_allocated()

    clf = FinetunedTabPFNClassifier(
        device="cuda",
        epochs=3,
        learning_rate=2e-5,
        n_estimators_finetune=2,
        n_estimators_validation=2,
        n_estimators_final_inference=2,
        random_state=RANDOM_STATE,
        extra_classifier_kwargs={"model_path": str(CKPT)},
    )
    clf.fit(X_train, y_train)

    mem_peak = torch.cuda.max_memory_allocated()
    print(
        f"VRAM allocated before fit: {mem_before / 1e6:.1f} MB; "
        f"peak during fit: {mem_peak / 1e6:.1f} MB"
    )
    if mem_peak <= mem_before:
        print("FAIL: peak VRAM did not exceed baseline; model may not be on GPU",
              file=sys.stderr)
        return 1

    y_pred_proba = clf.predict_proba(X_test)
    assert y_pred_proba.shape == (len(X_test), 2), y_pred_proba.shape
    assert np.allclose(y_pred_proba.sum(axis=1), 1.0, atol=1e-4)

    auc = roc_auc_score(y_test, y_pred_proba[:, 1])
    ll = log_loss(y_test, y_pred_proba)
    print(f"Test ROC-AUC: {auc:.4f}")
    print(f"Test log-loss: {ll:.4f}")

    if auc < 0.9:
        print("FAIL: AUC unexpectedly low for breast_cancer", file=sys.stderr)
        return 1

    print("OK: GPU fine-tune verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
