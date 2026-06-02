#!/usr/bin/env python3
"""
make_incl_excl_parquet.py — Re-export the inclusion / exclusion mean-pooled
MedCPT embeddings (from branch/IE_embedding) as per-trial parquets in the same
format as encode_text_column.py output, so full_step2_multi.py can consume all
virtual columns uniformly.

Reads the criterion-level MedCPT embeddings produced by IE_embedding's
encode_medcpt.py, mean-pools per (trial_id, phase, type), and writes:
  data/emb_inclusion_medcpt.parquet
  data/emb_exclusion_medcpt.parquet
each with columns: trial_id, phase, emb_0 .. emb_767
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import torch

EMB_RUN = Path("/data2/zhu11/TB/branch/IE_embedding/results/encode_medcpt_20260520_154921")
OUT_DIR = Path("/data2/zhu11/TB/branch/All_text_embedding/data")
DEVICE  = "cuda" if torch.cuda.is_available() else "cpu"


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Loading criterion embeddings from {EMB_RUN} ...")
    emb = np.load(EMB_RUN / "embeddings.npy")
    meta = pd.read_parquet(EMB_RUN / "metadata.parquet")
    print(f"  emb {emb.shape}  meta {len(meta):,}")

    composite = (meta["trial_id"].astype(str) + "|" +
                 meta["phase"].astype(str) + "|" + meta["type"].astype(str))
    codes, uniques = pd.factorize(composite, sort=True)
    n_groups = len(uniques)

    print(f"Mean-pooling {n_groups:,} (trial,phase,type) groups on {DEVICE} ...")
    e_t = torch.from_numpy(emb.astype(np.float32)).to(DEVICE)
    c_t = torch.from_numpy(codes.astype(np.int64)).to(DEVICE)
    sums = torch.zeros(n_groups, emb.shape[1], device=DEVICE)
    cnts = torch.zeros(n_groups, device=DEVICE)
    sums.index_add_(0, c_t, e_t)
    cnts.index_add_(0, c_t, torch.ones_like(c_t, dtype=torch.float32))
    pooled = (sums / cnts.unsqueeze(1)).cpu().numpy().astype(np.float16)

    rows_I, rows_E = [], []
    for i, key in enumerate(uniques):
        tid, ph, typ = key.split("|")
        (rows_I if typ == "I" else rows_E).append((tid, ph, i))

    for type_code, rows, fname in [("I", rows_I, "emb_inclusion_medcpt.parquet"),
                                   ("E", rows_E, "emb_exclusion_medcpt.parquet")]:
        idx = [r[2] for r in rows]
        mat = pooled[idx]
        df = pd.DataFrame({"trial_id": [r[0] for r in rows],
                           "phase":    [r[1] for r in rows]})
        emb_df = pd.DataFrame(mat, columns=[f"emb_{i}" for i in range(mat.shape[1])])
        out = pd.concat([df, emb_df], axis=1)
        path = OUT_DIR / fname
        out.to_parquet(path, index=False)
        print(f"Wrote {path}  shape={out.shape}")


if __name__ == "__main__":
    main()
