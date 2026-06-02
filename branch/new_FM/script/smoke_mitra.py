#!/usr/bin/env python3
"""Smoke test: Mitra (AWS/AutoGluon) classifier on toy data."""
import time
import numpy as np
from sklearn.datasets import make_classification
from sklearn.metrics import roc_auc_score

from autogluon.tabular.models.mitra.sklearn_interface import MitraClassifier

Xc, yc = make_classification(n_samples=400, n_features=10, random_state=0)
Xc_tr, Xc_te, yc_tr, yc_te = Xc[:300], Xc[300:], yc[:300], yc[300:]

print("--- Mitra (zero-shot, fine_tune=False, n_estimators=1) ---")
t0 = time.perf_counter()
clf = MitraClassifier(device="cuda", fine_tune=False, n_estimators=1, verbose=False)
clf.fit(Xc_tr, yc_tr)
proba = clf.predict_proba(Xc_te)
print(f"proba shape: {proba.shape}  roc_auc={roc_auc_score(yc_te, proba[:, 1]):.4f}  time={time.perf_counter()-t0:.1f}s")
print("OK")
