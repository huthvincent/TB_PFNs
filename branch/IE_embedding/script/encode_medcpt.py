#!/usr/bin/env python3
"""
encode_medcpt.py — Encode every parsed criterion with ncbi/MedCPT-Article-Encoder
into a fixed 768-d vector. Frozen inference, no training.

Reads:
  /data2/zhu11/TB/branch/IE_embedding/data/inclusion.json
  /data2/zhu11/TB/branch/IE_embedding/data/exclusion.json

Writes:
  /data2/zhu11/TB/branch/IE_embedding/results/encode_medcpt_<YYYYMMDD_HHMMSS>/
    embeddings.npy    # float16 array, shape (N, 768), aligned with metadata
    metadata.parquet  # columns: trial_id, phase, type ('I'|'E'), idx, text
    run_info.json     # model, args, timing, stats

Length-sorted batching to minimize padding overhead.
"""

from __future__ import annotations

import argparse
import json
import time
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from tqdm import tqdm
from transformers import AutoModel, AutoTokenizer

DATA_DIR     = Path("/data2/zhu11/TB/branch/IE_embedding/data")
RESULTS_ROOT = Path("/data2/zhu11/TB/branch/IE_embedding/results")
MODEL_NAME   = "ncbi/MedCPT-Article-Encoder"
EMBED_DIM    = 768
MAX_LEN      = 512  # MedCPT context length


def load_all_criteria(limit: int | None = None) -> list[dict]:
    """Flatten inclusion.json + exclusion.json into one list of rows."""
    rows: list[dict] = []
    for fname, type_code in [("inclusion.json", "I"), ("exclusion.json", "E")]:
        with (DATA_DIR / fname).open() as f:
            entries = json.load(f)
        for e in entries:
            for i, c in enumerate(e["criteria"]):
                if not c or not c.strip():
                    continue
                rows.append({
                    "trial_id": e["trial_id"],
                    "phase":    e["phase"],
                    "type":     type_code,
                    "idx":      i,
                    "text":     c,
                })
    if limit:
        rows = rows[:limit]
    return rows


@torch.inference_mode()
def encode_batch(texts, tokenizer, model, device, dtype):
    enc = tokenizer(
        texts,
        padding=True,
        truncation=True,
        max_length=MAX_LEN,
        return_tensors="pt",
    ).to(device)
    with torch.autocast(device_type="cuda", dtype=dtype, enabled=(device == "cuda")):
        out = model(**enc)
    # MedCPT uses the [CLS] token from last hidden state
    emb = out.last_hidden_state[:, 0, :]
    return emb.float().cpu().numpy()


def main(args):
    run_id = f"encode_medcpt_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    run_dir = RESULTS_ROOT / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    print(f"[run_id] {run_id}")
    print(f"[run_dir] {run_dir}")

    t_start = time.time()

    # ---- Load criteria ----
    print("Loading criteria JSON...")
    rows = load_all_criteria(limit=args.limit)
    n = len(rows)
    print(f"  total criteria: {n:,}")

    # Length-sorted batching: process longest first to OOM-check early
    print("Sorting by text length (descending) for tight batching...")
    order = sorted(range(n), key=lambda i: len(rows[i]["text"]), reverse=True)

    # ---- Load model ----
    print(f"Loading model {MODEL_NAME}...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModel.from_pretrained(MODEL_NAME).to(args.device).eval()
    dtype = torch.bfloat16 if args.dtype == "bf16" else torch.float16
    print(f"  device={args.device}  dtype={args.dtype}  batch_size={args.batch_size}  max_len={MAX_LEN}")

    # ---- Encode ----
    embs = np.empty((n, EMBED_DIM), dtype=np.float16)
    t_enc_start = time.time()
    for batch_start in tqdm(range(0, n, args.batch_size), desc="encoding"):
        batch_idx = order[batch_start:batch_start + args.batch_size]
        texts = [rows[i]["text"] for i in batch_idx]
        emb = encode_batch(texts, tokenizer, model, args.device, dtype)
        for j, orig_i in enumerate(batch_idx):
            embs[orig_i] = emb[j].astype(np.float16)
    t_enc = time.time() - t_enc_start

    # ---- Save ----
    print("Saving outputs...")
    np.save(run_dir / "embeddings.npy", embs)
    meta_df = pd.DataFrame(rows)
    meta_df.to_parquet(run_dir / "metadata.parquet", index=False)

    # Quick sanity stats
    norms = np.linalg.norm(embs.astype(np.float32), axis=1)
    n_nan = int(np.isnan(embs).any(axis=1).sum())
    info = {
        "run_id":          run_id,
        "model":           MODEL_NAME,
        "n_criteria":      n,
        "embed_dim":       EMBED_DIM,
        "max_len":         MAX_LEN,
        "batch_size":      args.batch_size,
        "dtype_compute":   args.dtype,
        "dtype_storage":   "float16",
        "device":          args.device,
        "elapsed_total_s": round(time.time() - t_start, 2),
        "elapsed_encode_s": round(t_enc, 2),
        "throughput_per_s": round(n / t_enc, 1) if t_enc > 0 else None,
        "norm_mean":       float(norms.mean()),
        "norm_std":        float(norms.std()),
        "n_nan_rows":      n_nan,
        "args":            vars(args),
    }
    with (run_dir / "run_info.json").open("w") as f:
        json.dump(info, f, indent=2)

    print(f"\nDone in {info['elapsed_total_s']:.1f}s "
          f"(encode {info['elapsed_encode_s']:.1f}s, throughput {info['throughput_per_s']}/s)")
    print(f"  norms: mean={info['norm_mean']:.2f}  std={info['norm_std']:.2f}  nan_rows={n_nan}")
    print(f"  embeddings: {run_dir / 'embeddings.npy'}  shape={embs.shape}  ({embs.nbytes/1e6:.1f} MB)")
    print(f"  metadata:   {run_dir / 'metadata.parquet'}  ({(run_dir/'metadata.parquet').stat().st_size/1e6:.1f} MB)")
    print(f"  info:       {run_dir / 'run_info.json'}")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--batch-size", type=int, default=256)
    p.add_argument("--device", default="cuda")
    p.add_argument("--dtype", choices=["bf16", "fp16"], default="bf16")
    p.add_argument("--limit", type=int, default=None, help="Encode only first N (debug / smoke)")
    args = p.parse_args()
    main(args)
