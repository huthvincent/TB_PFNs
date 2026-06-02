#!/usr/bin/env python3
"""
subset_sae.py — Shrink the source embedding parquets to only the SAE Phase2/3
trials and cast embeddings to float16, writing small LOCAL copies into
branch/aggregate/data/ (replacing the symlinks).

Why: the source parquets are huge (I/E 2.5GB over all 4 phases / 158K groups;
9 text parquets 2.6GB over 48K rows). full_step2_tabicl_multi.py reloads every
source per subprocess run — loading ~5GB per 'all'/'text' run dominated wall
time (training itself is ~8s). Subsetting to SAE Phase2/3 (~13K trials) + fp16
shrinks each source ~6-12x so every run loads in <1s.

Handles both parquet formats:
  - wide:  trial_id, phase, emb_0..emb_{d-1}   (All_text)
  - list:  trial_id, phase, [type,] mean_emb   (I/E, SMILES)

Run once before run_multiseed_aggregate.py.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, "/data2/zhu11/TB/branch/IE_embedding/script")
from ablate_ie_features import load_split as load_split_generic  # noqa: E402

DATA = Path("/data2/zhu11/TB/branch/aggregate/data")
SUBTASK = "serious-adverse-event-forecasting"
PHASES = ["Phase2", "Phase3"]


def sae_keys() -> set:
    keys = set()
    for ph in PHASES:
        for split in ("train", "test"):
            X, _ = load_split_generic(SUBTASK, split, "Y/N", [ph])
            for tid in X.index.astype(str):
                keys.add((tid, ph))
    return keys


def shrink(path: Path, keys: set):
    # Resolve symlink to the real source, read, filter, fp16, overwrite local.
    real = path.resolve()
    df = pd.read_parquet(real)
    n0 = len(df)
    mask = [ (str(t), str(p)) in keys for t, p in zip(df["trial_id"], df["phase"]) ]
    df = df[mask].reset_index(drop=True)
    emb_cols = [c for c in df.columns if c.startswith("emb_")]
    if emb_cols:                       # wide
        df[emb_cols] = df[emb_cols].astype(np.float16)
    elif "mean_emb" in df.columns:     # list
        df["mean_emb"] = df["mean_emb"].apply(lambda v: np.asarray(v, dtype=np.float16))
    if path.is_symlink():
        path.unlink()
    df.to_parquet(path, index=False)
    return n0, len(df), path.stat().st_size / 1e6


def main():
    keys = sae_keys()
    print(f"SAE Phase2/3 (trial_id, phase) keys: {len(keys):,}")
    total = 0.0
    for path in sorted(DATA.glob("*.parquet")):
        n0, n1, mb = shrink(path, keys)
        total += mb
        print(f"  {path.name:55} {n0:>7} → {n1:>6} rows  {mb:6.1f} MB")
    print(f"total local data: {total:.1f} MB")


if __name__ == "__main__":
    main()
