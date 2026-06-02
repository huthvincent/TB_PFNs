#!/usr/bin/env python3
"""
encode_ie_qwen3.py — Encode every parsed criterion with Qwen/Qwen3-Embedding-8B
into a 4096-d vector, then mean-pool per (trial_id, phase, type).

Reads:
  /data2/zhu11/TB/branch/IE_embedding/data/inclusion.json   (81,786 entries → 685K criteria)
  /data2/zhu11/TB/branch/IE_embedding/data/exclusion.json   (81,786 entries → 893K criteria)

Writes (canonical, consumed by full_step2_tabicl_smiles.py):
  /data2/zhu11/TB/branch/smiles/data/ie_embeddings_qwen3.parquet
    columns: trial_id, phase, type ('I'|'E'), mean_emb (list[float32], len=4096)

Writes (audit / re-pool):
  /data2/zhu11/TB/branch/smiles/results/encode_ie_qwen3_<YYYYMMDD_HHMMSS>/
    per_criterion_embeddings.npy   # float16, (N, 4096)
    per_criterion_metadata.parquet # trial_id, phase, type, idx, text
    run_info.json                  # model, args, timing, stats
    log.txt

Pooling: last-token (Qwen-style; works with left padding). No L2 normalize
(downstream Linear projection re-scales freely; matches MedCPT pipeline).
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

SRC_DATA_DIR = Path("/data2/zhu11/TB/branch/IE_embedding/data")
OUT_DATA_DIR = Path("/data2/zhu11/TB/branch/smiles/data")
RESULTS_ROOT = Path("/data2/zhu11/TB/branch/smiles/results")
MODEL_NAME   = "Qwen/Qwen3-Embedding-8B"
EMBED_DIM    = 4096
MAX_LEN      = 512  # criteria are short; 512 covers ~99% without truncation


def load_all_criteria(limit: int | None = None) -> list[dict]:
    """Flatten inclusion.json + exclusion.json into one list of rows."""
    rows: list[dict] = []
    for fname, type_code in [("inclusion.json", "I"), ("exclusion.json", "E")]:
        with (SRC_DATA_DIR / fname).open() as f:
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


def last_token_pool(last_hidden_states: torch.Tensor,
                    attention_mask: torch.Tensor) -> torch.Tensor:
    """Qwen-style last-token pooling. Handles both left and right padding."""
    left_padding = (attention_mask[:, -1].sum() == attention_mask.shape[0])
    if left_padding:
        return last_hidden_states[:, -1]
    seq_lens = attention_mask.sum(dim=1) - 1
    return last_hidden_states[torch.arange(last_hidden_states.shape[0],
                                           device=last_hidden_states.device),
                              seq_lens]


@torch.inference_mode()
def encode_batch(texts, tokenizer, model, device):
    enc = tokenizer(
        texts, padding=True, truncation=True,
        max_length=MAX_LEN, return_tensors="pt",
    ).to(device)
    out = model(**enc)
    emb = last_token_pool(out.last_hidden_state, enc["attention_mask"])
    return emb.float().cpu().numpy()


def main(args):
    # ---- run_dir: new timestamped, or reuse via --resume ----
    if args.resume:
        run_dir = Path(args.resume)
        if not run_dir.exists():
            raise FileNotFoundError(f"--resume path does not exist: {run_dir}")
        run_id = run_dir.name
    else:
        run_id  = f"encode_ie_qwen3_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        run_dir = RESULTS_ROOT / run_id
        run_dir.mkdir(parents=True, exist_ok=True)
    OUT_DATA_DIR.mkdir(parents=True, exist_ok=True)
    log_f = open(run_dir / "log.txt", "a" if args.resume else "w")

    def echo(*parts):
        line = " ".join(str(p) for p in parts)
        print(line)
        print(line, file=log_f, flush=True)

    echo(f"\n[run_id] {run_id}  ({'RESUME' if args.resume else 'FRESH'})")
    echo(f"[run_dir] {run_dir}")

    t_start = time.time()
    echo("Loading criteria JSON ...")
    rows = load_all_criteria(limit=args.limit)
    n = len(rows)
    echo(f"  total criteria: {n:,}")

    echo("Sorting by text length (descending) for tight batching ...")
    order = sorted(range(n), key=lambda i: len(rows[i]["text"]), reverse=True)

    # ---- Persist metadata up front (deterministic; OK to overwrite on resume) ----
    meta_df = pd.DataFrame(rows)
    meta_df.to_parquet(run_dir / "per_criterion_metadata.parquet", index=False)

    # ---- Set up memmap + checkpoint state ----
    emb_path   = run_dir / "per_criterion_embeddings.npy"
    state_path = run_dir / "encode_state.json"

    start_batch = 0
    if args.resume:
        if not state_path.exists():
            raise FileNotFoundError(
                f"--resume but no state.json at {state_path}; that dir was not run with checkpointing.")
        st = json.loads(state_path.read_text())
        if st.get("completed"):
            echo(f"[resume] State says encoding already completed — skipping encode, going straight to mean-pool.")
            embs = np.load(emb_path, mmap_mode="r")
            start_batch = n  # signal: skip the loop
        else:
            if st["n_total"] != n or st["batch_size"] != args.batch_size:
                raise ValueError(
                    f"Checkpoint mismatch: state has n={st['n_total']} bs={st['batch_size']}, "
                    f"current n={n} bs={args.batch_size}. Re-run without --resume or fix args.")
            start_batch = st["next_batch_start"]
            embs = np.lib.format.open_memmap(emb_path, mode="r+")
            if embs.shape != (n, EMBED_DIM):
                raise ValueError(f"Memmap shape {embs.shape} != expected {(n, EMBED_DIM)}")
            echo(f"[resume] Picking up at batch_start={start_batch:,}/{n:,} "
                 f"({100*start_batch/n:.1f}% done).")
    else:
        embs = np.lib.format.open_memmap(emb_path, mode="w+", dtype=np.float16,
                                         shape=(n, EMBED_DIM))

    # ---- Load model (skip if resume + already-completed flag) ----
    if start_batch < n:
        echo(f"Loading {MODEL_NAME} (bf16; first time downloads ~16 GB from HF) ...")
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, padding_side="left")
        model = AutoModel.from_pretrained(MODEL_NAME, torch_dtype=torch.bfloat16).to(args.device).eval()
        n_params = sum(p.numel() for p in model.parameters())
        echo(f"  params={n_params:,}  device={args.device}  dtype=bf16  "
             f"batch_size={args.batch_size}  max_len={MAX_LEN}  ckpt_every={args.checkpoint_every}")

        # ---- Encode (resumable loop) ----
        total_batches = (n + args.batch_size - 1) // args.batch_size
        done_batches  = start_batch // args.batch_size
        t_enc_start = time.time()
        pbar = tqdm(range(start_batch, n, args.batch_size), desc="encoding",
                    initial=done_batches, total=total_batches)
        for loop_i, batch_start in enumerate(pbar):
            batch_idx = order[batch_start:batch_start + args.batch_size]
            texts = [rows[i]["text"] for i in batch_idx]
            emb = encode_batch(texts, tokenizer, model, args.device)
            for j, orig_i in enumerate(batch_idx):
                embs[orig_i] = emb[j].astype(np.float16)
            if (loop_i + 1) % args.checkpoint_every == 0:
                embs.flush()
                state_path.write_text(json.dumps({
                    "next_batch_start": batch_start + args.batch_size,
                    "n_total": n,
                    "batch_size": args.batch_size,
                    "model": MODEL_NAME,
                    "ckpt_unix_ts": int(time.time()),
                }))
        t_enc = time.time() - t_enc_start
        echo(f"  encode done in {t_enc:.1f}s ({n/t_enc:.1f}/s overall)")
        embs.flush()
        state_path.write_text(json.dumps({
            "next_batch_start": n, "n_total": n, "batch_size": args.batch_size,
            "model": MODEL_NAME, "completed": True, "ckpt_unix_ts": int(time.time()),
        }))
    else:
        t_enc = 0.0  # resume + completed: skip encoding

    # ---- Mean-pool per (trial_id, phase, type) on GPU ----
    echo("Mean-pooling per (trial_id, phase, type) ...")
    composite = (meta_df["trial_id"].astype(str) + "|" +
                 meta_df["phase"].astype(str)    + "|" +
                 meta_df["type"].astype(str))
    codes, uniques = pd.factorize(composite, sort=True)
    n_groups = len(uniques)

    e_t = torch.from_numpy(embs.astype(np.float32)).to(args.device)
    c_t = torch.from_numpy(codes.astype(np.int64)).to(args.device)
    sums = torch.zeros(n_groups, EMBED_DIM, device=args.device)
    cnts = torch.zeros(n_groups, device=args.device)
    sums.index_add_(0, c_t, e_t)
    cnts.index_add_(0, c_t, torch.ones_like(c_t, dtype=torch.float32))
    pooled = (sums / cnts.unsqueeze(1)).cpu().numpy().astype(np.float32)

    rows_out = []
    for i, key in enumerate(uniques):
        tid, ph, typ = key.split("|")
        rows_out.append({
            "trial_id": tid, "phase": ph, "type": typ,
            "mean_emb": pooled[i],  # 1-D np.float32 array length 4096
        })
    pool_df = pd.DataFrame(rows_out)
    out_path = OUT_DATA_DIR / "ie_embeddings_qwen3.parquet"
    pool_df.to_parquet(out_path, index=False)
    echo(f"  mean-pooled groups: {len(pool_df):,} → {out_path}")

    # ---- Stats ----
    norms = np.linalg.norm(embs.astype(np.float32), axis=1)
    n_nan = int(np.isnan(embs).any(axis=1).sum())
    info = {
        "run_id":            run_id,
        "model":             MODEL_NAME,
        "n_criteria":        n,
        "n_pooled_groups":   int(len(pool_df)),
        "embed_dim":         EMBED_DIM,
        "max_len":           MAX_LEN,
        "batch_size":        args.batch_size,
        "dtype_compute":     "bfloat16",
        "dtype_storage":     "float16",
        "device":            args.device,
        "elapsed_total_s":   round(time.time() - t_start, 2),
        "elapsed_encode_s":  round(t_enc, 2),
        "throughput_per_s":  round(n / t_enc, 1) if t_enc > 0 else None,
        "norm_mean":         float(norms.mean()),
        "norm_std":          float(norms.std()),
        "n_nan_rows":        n_nan,
        "args":              vars(args),
        "outputs": {
            "pooled_parquet":     str(out_path),
            "per_criterion_npy":  str(run_dir / "per_criterion_embeddings.npy"),
            "per_criterion_meta": str(run_dir / "per_criterion_metadata.parquet"),
        },
    }
    (run_dir / "run_info.json").write_text(json.dumps(info, indent=2))

    echo(f"\nDone in {info['elapsed_total_s']:.1f}s "
         f"(encode {info['elapsed_encode_s']:.1f}s @ {info['throughput_per_s']}/s)")
    echo(f"  norms: mean={info['norm_mean']:.2f}  std={info['norm_std']:.2f}  nan_rows={n_nan}")
    echo(f"  pooled parquet: {out_path}  ({out_path.stat().st_size/1e6:.1f} MB)")
    log_f.close()


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--batch-size", type=int, default=128)
    p.add_argument("--device", default="cuda")
    p.add_argument("--limit", type=int, default=None,
                   help="Encode only first N criteria (smoke test)")
    p.add_argument("--resume", default=None,
                   help="Path to a previous run_dir; resumes from its encode_state.json. "
                        "Requires same batch_size / n_criteria as the original run.")
    p.add_argument("--checkpoint-every", type=int, default=50,
                   help="Flush memmap + write state.json every N batches.")
    args = p.parse_args()
    main(args)
