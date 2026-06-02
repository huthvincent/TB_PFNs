#!/usr/bin/env python3
"""
make_step2_lite_pca.py — Step 2-Lite (unsupervised PCA variant):

  1. Per (trial_id, phase, type), mean-pool all 768-d criterion embeddings →
     one 768-d vector per group (typically ~163K groups for ~81K trials × 2 types).
  2. Fit PCA(K) on all pooled vectors (unsupervised; no labels touched, so no
     train/test leak even if applied to downstream evaluation).
  3. Pivot to wide table: (trial_id, phase) → 2K columns
     (incl_pca_0..K-1, excl_pca_0..K-1)

This is the cheap sanity check before doing supervised bottleneck or
full virtual-feature-column TabPFN modification (see README §4).
"""

from __future__ import annotations

import argparse
import json
import time
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA

EMB_RUN_DEFAULT = "/data2/zhu11/TB/branch/IE_embedding/results/encode_medcpt_20260520_154921"
RESULTS_ROOT    = Path("/data2/zhu11/TB/branch/IE_embedding/results")


def mean_pool_per_group(emb: np.ndarray, meta: pd.DataFrame) -> tuple[pd.DataFrame, np.ndarray]:
    """Group meta by (trial_id, phase, type) and mean-pool the corresponding
    rows of `emb`. Returns (group_df, pooled_matrix) where group_df has cols
    [trial_id, phase, type, n_criteria] and pooled_matrix is (n_groups, 768)."""
    print("Building group keys ...")
    # Concatenate fields into a single string key, factorize → integer ids
    composite = (meta["trial_id"].astype(str) + "|" +
                 meta["phase"].astype(str) + "|" +
                 meta["type"].astype(str))
    codes, uniques = pd.factorize(composite, sort=True)
    n_groups = len(uniques)
    print(f"  {n_groups:,} unique (trial_id, phase, type) groups from {len(meta):,} criteria")

    # Scatter-add via torch on GPU (faster than np.add.at on 1.58M rows)
    import torch
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Mean-pooling embeddings on {device} ...")
    emb_t  = torch.from_numpy(emb.astype(np.float32)).to(device)
    code_t = torch.from_numpy(codes.astype(np.int64)).to(device)
    sums   = torch.zeros((n_groups, emb.shape[1]), dtype=torch.float32, device=device)
    counts = torch.zeros(n_groups, dtype=torch.float32, device=device)
    sums.index_add_(0, code_t, emb_t)
    counts.index_add_(0, code_t, torch.ones_like(code_t, dtype=torch.float32))
    pooled = (sums / counts.unsqueeze(1)).cpu().numpy()

    # Reconstruct (trial_id, phase, type) from the composite key
    split_keys = [s.split("|") for s in uniques]
    group_df = pd.DataFrame(split_keys, columns=["trial_id", "phase", "type"])
    group_df["n_criteria"] = counts.cpu().numpy().astype(np.int64)
    return group_df, pooled


def pivot_to_wide(group_df: pd.DataFrame, projected: np.ndarray, k: int, prefix: str = "pca") -> pd.DataFrame:
    """group_df rows correspond to projected rows. Pivot type ∈ {I,E} into
    incl_<prefix>_0..k-1 / excl_<prefix>_0..k-1 columns."""
    df = group_df[["trial_id", "phase", "type"]].copy()
    for i in range(k):
        df[f"d{i}"] = projected[:, i].astype(np.float32)
    long_cols = [f"d{i}" for i in range(k)]

    wide = df.pivot_table(index=["trial_id", "phase"], columns="type",
                          values=long_cols, aggfunc="first").reset_index()
    # Flatten multiindex (dN, type) → "incl_<prefix>_N" / "excl_<prefix>_N"
    new_cols = []
    for c in wide.columns:
        if isinstance(c, tuple) and c[1] in ("I", "E"):
            stat, typ = c
            i = int(stat[1:])
            new_cols.append(f"{'incl' if typ == 'I' else 'excl'}_{prefix}_{i}")
        else:
            new_cols.append(c[0] if isinstance(c, tuple) else c)
    wide.columns = new_cols
    return wide


def main(args):
    run_id = f"step2_lite_pca_k{args.k}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    run_dir = RESULTS_ROOT / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    print(f"[run_id] {run_id}")

    emb_run = Path(args.emb_run)
    print(f"Loading from {emb_run} ...")
    emb = np.load(emb_run / "embeddings.npy")
    meta = pd.read_parquet(emb_run / "metadata.parquet")
    print(f"  emb {emb.shape}  meta {len(meta):,}")

    t0 = time.time()
    group_df, pooled = mean_pool_per_group(emb, meta)
    print(f"  pooled shape: {pooled.shape}  time={time.time()-t0:.1f}s")

    print(f"Fitting PCA(n_components={args.k}) on {pooled.shape[0]:,} pooled vectors ...")
    t1 = time.time()
    pca = PCA(n_components=args.k, random_state=args.seed)
    Z = pca.fit_transform(pooled.astype(np.float32))
    ev = float(pca.explained_variance_ratio_.sum())
    print(f"  PCA fit done in {time.time()-t1:.1f}s, explained var sum: {ev:.4f}")

    print("Pivoting to wide (incl/excl per trial) ...")
    wide = pivot_to_wide(group_df, Z, args.k, prefix="pca")
    print(f"  wide shape: {wide.shape}")
    print(wide.head(2).to_string())

    out_path = run_dir / "ie_features.parquet"  # same filename convention as Step 1
    wide.to_parquet(out_path, index=False)
    info = {
        "run_id": run_id,
        "emb_run": str(emb_run),
        "k": args.k,
        "n_groups_pooled": int(len(group_df)),
        "n_trials_in_wide": int(len(wide)),
        "explained_variance_ratio_sum": ev,
        "explained_variance_ratio_top10": pca.explained_variance_ratio_[:10].tolist(),
        "elapsed_s": round(time.time()-t0, 1),
        "args": vars(args),
    }
    with (run_dir / "run_info.json").open("w") as f:
        json.dump(info, f, indent=2)
    print(f"\nDone. Wrote: {out_path}  ({out_path.stat().st_size/1e6:.1f} MB)")
    print(f"  {run_dir}/run_info.json")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--emb-run", default=EMB_RUN_DEFAULT)
    p.add_argument("--k", type=int, default=32)
    p.add_argument("--seed", type=int, default=0)
    args = p.parse_args()
    main(args)
