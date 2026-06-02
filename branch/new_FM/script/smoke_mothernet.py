#!/usr/bin/env python3
"""Smoke test: MotherNet + TabFlex (microsoft/ticl) fit+predict on toy data."""
import time
import numpy as np
from sklearn.datasets import make_classification
from sklearn.metrics import roc_auc_score

Xc, yc = make_classification(n_samples=400, n_features=10, random_state=0)
Xc_tr, Xc_te, yc_tr, yc_te = Xc[:300], Xc[300:], yc[:300], yc[300:]

# MotherNet
print("--- MotherNet ---")
from ticl.prediction import MotherNetClassifier
t0 = time.perf_counter()
clf = MotherNetClassifier(device="cuda")
clf.fit(Xc_tr, yc_tr)
y_eval, p_eval = clf.predict(Xc_te, return_winning_probability=True)
proba = clf.predict_proba(Xc_te)
print(f"shape proba {proba.shape}, classes {clf.classes_}")
print(f"roc_auc={roc_auc_score(yc_te, proba[:, 1]):.4f}  time={time.perf_counter()-t0:.2f}s")

# TabFlex
print("--- TabFlex ---")
try:
    from ticl.prediction import TabFlexClassifier
    t0 = time.perf_counter()
    clf = TabFlexClassifier(device="cuda")
    clf.fit(Xc_tr, yc_tr)
    proba = clf.predict_proba(Xc_te)
    print(f"roc_auc={roc_auc_score(yc_te, proba[:, 1]):.4f}  time={time.perf_counter()-t0:.2f}s")
except (ImportError, AttributeError) as e:
    print(f"TabFlex not directly importable: {e}")
    # Try alternative entry points
    import ticl.prediction as tp
    print("Available in ticl.prediction:", [x for x in dir(tp) if not x.startswith('_')])
print("OK")
