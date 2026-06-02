#!/usr/bin/env python3
"""Smoke test: TabICLv2 fit+predict on tiny toy data, GPU."""
import time
import numpy as np
from sklearn.datasets import make_classification, make_regression
from sklearn.metrics import roc_auc_score, r2_score
from tabicl import TabICLClassifier, TabICLRegressor

from importlib.metadata import version as _pv
print(f"tabicl {_pv('tabicl')}")

# Binary
Xc, yc = make_classification(n_samples=400, n_features=10, random_state=0)
Xc_tr, Xc_te, yc_tr, yc_te = Xc[:300], Xc[300:], yc[:300], yc[300:]
t0 = time.perf_counter()
clf = TabICLClassifier(device="cuda", random_state=0)
clf.fit(Xc_tr, yc_tr)
proba = clf.predict_proba(Xc_te)
print(f"[clf] roc_auc={roc_auc_score(yc_te, proba[:, 1]):.4f}  time={time.perf_counter()-t0:.2f}s")

# Regression
Xr, yr = make_regression(n_samples=400, n_features=10, random_state=0)
Xr_tr, Xr_te, yr_tr, yr_te = Xr[:300], Xr[300:], yr[:300], yr[300:]
t0 = time.perf_counter()
reg = TabICLRegressor(device="cuda", random_state=0)
reg.fit(Xr_tr, yr_tr)
pred = reg.predict(Xr_te)
print(f"[reg] r2={r2_score(yr_te, pred):.4f}  time={time.perf_counter()-t0:.2f}s")
print("OK")
