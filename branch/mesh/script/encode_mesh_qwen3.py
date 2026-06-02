#!/usr/bin/env python3
"""
encode_mesh_qwen3.py — Encode MeSH terms (condition + intervention) with
Qwen/Qwen3-Embedding-8B (4096-d, last-token pool), mean-pooled per
(trial_id, phase, type). The Qwen3 counterpart of encode_mesh_hf.py — added so
we can compare a general strong embedding (Qwen3) against the biomedical-
specialist encoders (SapBERT/BioLORD/MedCPT/PubMedBERT, all 768-d) on the SAME
MeSH controlled-vocabulary terms.

NOTE: this encodes the MeSH *terms* (e.g. "Prostatic Neoplasms"), NOT the raw
condition/intervention free-text columns (those are the All_text/aggregate
`emb_condition_qwen` etc.). Different input → different result.

Reuses encode_mesh_hf.collect_mesh_corpus (two-column scan + tolerant parse) and
encode_ie_qwen3.last_token_pool (Qwen-style pooling). Output schema matches the
other mesh parquets so full_step2_tabicl_mesh.py consumes it unchanged:
  branch/mesh/data/mesh_embeddings_qwen3.parquet
    columns: trial_id, phase, type ∈ {condition, intervention}, mean_emb (4096), n_terms
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from tqdm import tqdm
from transformers import AutoModel, AutoTokenizer

sys.path.insert(0, "/data2/zhu11/TB/branch/mesh/script")
from encode_mesh_hf import collect_mesh_corpus  # noqa: E402
sys.path.insert(0, "/data2/zhu11/TB/branch/smiles/script")
from encode_ie_qwen3 import last_token_pool  # noqa: E402

OUT_DATA_DIR = Path("/data2/zhu11/TB/branch/mesh/data")
RESULTS_ROOT = Path("/data2/zhu11/TB/branch/mesh/results")
MODEL_NAME   = "Qwen/Qwen3-Embedding-8B"
EMBED_DIM    = 4096
MAX_LEN      = 64  # MeSH terms are short


@torch.inference_mode()
def encode_batch(texts, tokenizer, model, device):
    enc = tokenizer(texts, padding=True, truncation=True,
                    max_length=MAX_LEN, return_tensors="pt").to(device)
    out = model(**enc)
    emb = last_token_pool(out.last_hidden_state, enc["attention_mask"])
    return emb.float().cpu().numpy()


def main(args):
    run_id  = f"encode_mesh_qwen3_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    run_dir = RESULTS_ROOT / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    OUT_DATA_DIR.mkdir(parents=True, exist_ok=True)
    log_f = open(run_dir / "log.txt", "w")

    def echo(*p):
        line = " ".join(str(x) for x in p); print(line); print(line, file=log_f, flush=True)

    echo(f"[run_id] {run_id}  [model] {MODEL_NAME}  [subtask] {args.subtask}")
    t0 = time.time()

    echo("Scanning condition + intervention MeSH ...")
    corpus = collect_mesh_corpus(args.subtask)
    rows = []
    for (tid, ph, ty), terms in corpus.items():
        for t in terms:
            if t and isinstance(t, str):
                rows.append({"trial_id": tid, "phase": ph, "type": ty, "term": t, "n_chars": len(t)})
    if args.limit:
        rows = rows[:args.limit]
    n = len(rows)
    echo(f"  rows to encode: {n:,}  (unique terms: {len({r['term'] for r in rows}):,})")
    order = sorted(range(n), key=lambda i: rows[i]["n_chars"], reverse=True)

    echo(f"Loading {MODEL_NAME} (bf16) ...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, padding_side="left")
    model = AutoModel.from_pretrained(MODEL_NAME, torch_dtype=torch.bfloat16).to(args.device).eval()
    echo(f"  params={sum(p.numel() for p in model.parameters()):,}  batch={args.batch_size}")

    embs = np.empty((n, EMBED_DIM), dtype=np.float16)
    t_enc = time.time()
    for bs in tqdm(range(0, n, args.batch_size), desc="encoding"):
        bidx = order[bs:bs + args.batch_size]
        emb = encode_batch([rows[i]["term"] for i in bidx], tokenizer, model, args.device)
        for j, oi in enumerate(bidx):
            embs[oi] = emb[j].astype(np.float16)
    echo(f"  encode done in {time.time()-t_enc:.1f}s")

    meta = pd.DataFrame(rows)
    composite = meta["trial_id"].astype(str) + "|" + meta["phase"].astype(str) + "|" + meta["type"].astype(str)
    codes, uniques = pd.factorize(composite, sort=True)
    e_t = torch.from_numpy(embs.astype(np.float32)).to(args.device)
    c_t = torch.from_numpy(codes.astype(np.int64)).to(args.device)
    sums = torch.zeros(len(uniques), EMBED_DIM, device=args.device)
    cnts = torch.zeros(len(uniques), device=args.device)
    sums.index_add_(0, c_t, e_t); cnts.index_add_(0, c_t, torch.ones_like(c_t, dtype=torch.float32))
    pooled = (sums / cnts.unsqueeze(1)).cpu().numpy().astype(np.float32)
    counts = cnts.cpu().numpy().astype(np.int64)

    out_rows = []
    for i, key in enumerate(uniques):
        tid, ph, ty = key.split("|")
        out_rows.append({"trial_id": tid, "phase": ph, "type": ty,
                         "mean_emb": pooled[i], "n_terms": int(counts[i])})
    pool_df = pd.DataFrame(out_rows)
    out_path = OUT_DATA_DIR / "mesh_embeddings_qwen3.parquet"
    pool_df.to_parquet(out_path, index=False)
    echo(f"  mean-pooled groups: {len(pool_df):,} → {out_path}  ({out_path.stat().st_size/1e6:.1f} MB)")

    (run_dir / "run_info.json").write_text(json.dumps({
        "run_id": run_id, "model": MODEL_NAME, "embed_dim": EMBED_DIM, "max_len": MAX_LEN,
        "n_terms_rows": n, "n_pooled_groups": int(len(pool_df)),
        "elapsed_total_s": round(time.time() - t0, 1), "outputs": {"pooled_parquet": str(out_path)},
    }, indent=2))
    echo(f"Done in {time.time()-t0:.1f}s")
    log_f.close()


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--subtask", default="serious-adverse-event-forecasting")
    p.add_argument("--batch-size", type=int, default=128)
    p.add_argument("--device", default="cuda")
    p.add_argument("--limit", type=int, default=None)
    args = p.parse_args()
    main(args)
