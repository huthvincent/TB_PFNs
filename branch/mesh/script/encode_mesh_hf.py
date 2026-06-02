#!/usr/bin/env python3
"""
encode_mesh_hf.py — Encode MeSH terms (condition + intervention) with one of four
biomedical text encoders, then mean-pool per (trial_id, phase, type).

MeSH terms are short controlled-vocabulary entities (e.g. "Prostatic Neoplasms",
"Ocrelizumab"), NOT sentences. We test encoders designed for biomedical
entities/concepts:

  --model:
    sapbert    : cambridgeltl/SapBERT-from-PubMedBERT-fulltext  (768, CLS pool) — UMLS synonym contrastive, entity SOTA
    biolord    : FremyCompany/BioLORD-2023                       (768, mean pool) — clinical concept SOTA (sentence-transformers)
    medcpt     : ncbi/MedCPT-Article-Encoder                     (768, CLS pool) — project I/E history; already cached
    pubmedbert : microsoft/BiomedNLP-BiomedBERT-base-uncased-abstract-fulltext (768, mean) — generic biomedical baseline

Pooling is per each encoder's recommended convention (CLS for SapBERT/MedCPT,
masked-mean for BioLORD/PubMedBERT) so each encoder is shown at its best.

Reads:
  /data2/zhu11/TB/dataset/TrialBench/<subtask>/Phase{1..4}/{train,test}_x.csv
  Columns: condition_browse/mesh_term  +  intervention_browse/mesh_term
  Each is a stringified python list of MeSH term strings (or a bare string).

Writes (canonical, consumed by full_step2_tabicl_mesh.py):
  /data2/zhu11/TB/branch/mesh/data/mesh_embeddings_<short>.parquet
    columns: trial_id, phase, type ∈ {condition, intervention}, mean_emb (np.float32 len=d), n_terms

Writes (audit):
  /data2/zhu11/TB/branch/mesh/results/encode_mesh_<short>_<YYYYMMDD_HHMMSS>/
    per_term_embeddings.npy, per_term_metadata.parquet, run_info.json, log.txt

Mirrors branch/smiles/script/encode_smiles_hf.py — only the source columns,
the {condition,intervention} type axis, and the encoder registry differ.
"""

from __future__ import annotations

import argparse
import ast
import json
import time
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from tqdm import tqdm
from transformers import AutoModel, AutoTokenizer

DATASET_ROOT = Path("/data2/zhu11/TB/dataset/TrialBench")
OUT_DATA_DIR = Path("/data2/zhu11/TB/branch/mesh/data")
RESULTS_ROOT = Path("/data2/zhu11/TB/branch/mesh/results")
MAX_LEN      = 64  # MeSH terms are short (max ~105 chars)

MESH_COLS = {
    "condition":    "condition_browse/mesh_term",
    "intervention": "intervention_browse/mesh_term",
}

# (hf_repo, short_name, pool_strategy ∈ {"cls","mean"})
MODEL_REGISTRY = {
    "sapbert":    ("cambridgeltl/SapBERT-from-PubMedBERT-fulltext", "sapbert",    "cls"),
    "biolord":    ("FremyCompany/BioLORD-2023",                     "biolord",    "mean"),
    "medcpt":     ("ncbi/MedCPT-Article-Encoder",                   "medcpt",     "cls"),
    "pubmedbert": ("microsoft/BiomedNLP-BiomedBERT-base-uncased-abstract-fulltext", "pubmedbert", "mean"),
}


def parse_terms(s) -> list[str]:
    """Tolerant parse: stringified list → list[str]. Empty/NaN → []."""
    if not isinstance(s, str) or not s.strip():
        return []
    try:
        v = ast.literal_eval(s)
        return [str(x) for x in (v if isinstance(v, list) else [v])]
    except Exception:
        try:
            v = json.loads(s)
            return [str(x) for x in (v if isinstance(v, list) else [v])]
        except Exception:
            return [s]


def collect_mesh_corpus(subtask: str) -> dict:
    """Scan all phases × {train,test}. Returns {(trial_id, phase, type) → set(terms)}
    deduped within each (trial, phase, type)."""
    out: dict[tuple, set] = {}
    base = DATASET_ROOT / subtask
    if not base.exists():
        raise FileNotFoundError(f"Subtask root not found: {base}")
    phases = sorted([p.name for p in base.iterdir() if p.is_dir() and p.name.startswith("Phase")])
    for phase in phases:
        for split in ("train", "test"):
            csv = base / phase / f"{split}_x.csv"
            if not csv.exists():
                continue
            cols = pd.read_csv(csv, nrows=0).columns.tolist()
            want = [c for c in MESH_COLS.values() if c in cols]
            if not want:
                continue
            df = pd.read_csv(csv, index_col=0, usecols=[cols[0], *want])
            for type_key, col in MESH_COLS.items():
                if col not in df.columns:
                    continue
                for trial_id, cell in df[col].items():
                    key = (str(trial_id), phase, type_key)
                    out.setdefault(key, set()).update(parse_terms(cell))
    return out


@torch.inference_mode()
def encode_batch(texts, tokenizer, model, device, pool):
    enc = tokenizer(texts, padding=True, truncation=True,
                    max_length=MAX_LEN, return_tensors="pt").to(device)
    out = model(**enc)
    if pool == "cls":
        emb = out.last_hidden_state[:, 0, :]
    elif pool == "mean":
        h = out.last_hidden_state
        mask = enc["attention_mask"].unsqueeze(-1).float()
        emb = (h * mask).sum(dim=1) / mask.sum(dim=1).clamp(min=1)
    else:
        raise ValueError(pool)
    return emb.float().cpu().numpy()


def main(args):
    if args.model not in MODEL_REGISTRY:
        raise ValueError(f"--model must be one of {list(MODEL_REGISTRY)}")
    hf_repo, short, pool = MODEL_REGISTRY[args.model]

    run_id  = f"encode_mesh_{short}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    run_dir = RESULTS_ROOT / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    OUT_DATA_DIR.mkdir(parents=True, exist_ok=True)
    log_f = open(run_dir / "log.txt", "w")

    def echo(*parts):
        line = " ".join(str(p) for p in parts)
        print(line); print(line, file=log_f, flush=True)

    echo(f"[run_id] {run_id}")
    echo(f"[model] {hf_repo}  short={short}  pool={pool}")
    echo(f"[subtask] {args.subtask}")

    t_start = time.time()

    # ---- 1. Collect MeSH corpus ----
    echo("Scanning train_x.csv / test_x.csv for condition + intervention MeSH ...")
    corpus = collect_mesh_corpus(args.subtask)
    by_type = {"condition": 0, "intervention": 0}
    for (tid, ph, ty), terms in corpus.items():
        if terms:
            by_type[ty] += 1
    n_keys = len(corpus)
    echo(f"  (trial,phase,type) keys: {n_keys:,}  "
         f"(condition non-empty {by_type['condition']:,}, intervention non-empty {by_type['intervention']:,})")

    rows = []
    for (tid, ph, ty), terms in corpus.items():
        for t in terms:
            if t and isinstance(t, str):
                rows.append({"trial_id": tid, "phase": ph, "type": ty,
                             "term": t, "n_chars": len(t)})
    if args.limit:
        rows = rows[:args.limit]
    n = len(rows)
    if n == 0:
        raise RuntimeError("No MeSH terms to encode.")
    echo(f"  total (trial,phase,type,term) rows to encode: {n:,}  "
         f"(unique terms: {len({r['term'] for r in rows}):,})")

    order = sorted(range(n), key=lambda i: rows[i]["n_chars"], reverse=True)

    # ---- 2. Load encoder ----
    echo(f"Loading {hf_repo} (bf16) ...")
    tokenizer = AutoTokenizer.from_pretrained(hf_repo)
    model = AutoModel.from_pretrained(hf_repo, torch_dtype=torch.bfloat16).to(args.device).eval()
    n_params = sum(p.numel() for p in model.parameters())
    with torch.inference_mode():
        sample = encode_batch([rows[order[0]]["term"]], tokenizer, model, args.device, pool)
    embed_dim = sample.shape[-1]
    echo(f"  params={n_params:,}  embed_dim={embed_dim}  pool={pool}  batch_size={args.batch_size}")

    # ---- 3. Encode ----
    embs = np.empty((n, embed_dim), dtype=np.float16)
    t_enc_start = time.time()
    for bs in tqdm(range(0, n, args.batch_size), desc="encoding"):
        bidx = order[bs:bs + args.batch_size]
        emb = encode_batch([rows[i]["term"] for i in bidx], tokenizer, model, args.device, pool)
        for j, oi in enumerate(bidx):
            embs[oi] = emb[j].astype(np.float16)
    t_enc = time.time() - t_enc_start
    echo(f"  encode done in {t_enc:.1f}s ({n/t_enc:.1f}/s)")

    # ---- 4. Save per-term audit ----
    np.save(run_dir / "per_term_embeddings.npy", embs)
    meta_df = pd.DataFrame(rows)
    meta_df.to_parquet(run_dir / "per_term_metadata.parquet", index=False)

    # ---- 5. Mean-pool per (trial_id, phase, type) ----
    echo("Mean-pooling per (trial_id, phase, type) ...")
    composite = (meta_df["trial_id"].astype(str) + "|" + meta_df["phase"].astype(str)
                 + "|" + meta_df["type"].astype(str))
    codes, uniques = pd.factorize(composite, sort=True)
    n_groups = len(uniques)
    e_t = torch.from_numpy(embs.astype(np.float32)).to(args.device)
    c_t = torch.from_numpy(codes.astype(np.int64)).to(args.device)
    sums = torch.zeros(n_groups, embed_dim, device=args.device)
    cnts = torch.zeros(n_groups, device=args.device)
    sums.index_add_(0, c_t, e_t)
    cnts.index_add_(0, c_t, torch.ones_like(c_t, dtype=torch.float32))
    pooled = (sums / cnts.unsqueeze(1)).cpu().numpy().astype(np.float32)
    counts = cnts.cpu().numpy().astype(np.int64)

    rows_out = []
    for i, key in enumerate(uniques):
        tid, ph, ty = key.split("|")
        rows_out.append({"trial_id": tid, "phase": ph, "type": ty,
                         "mean_emb": pooled[i], "n_terms": int(counts[i])})
    pool_df = pd.DataFrame(rows_out)
    out_path = OUT_DATA_DIR / f"mesh_embeddings_{short}.parquet"
    pool_df.to_parquet(out_path, index=False)
    echo(f"  mean-pooled groups: {len(pool_df):,} → {out_path}")

    # ---- 6. Stats ----
    norms = np.linalg.norm(embs.astype(np.float32), axis=1)
    info = {
        "run_id": run_id, "model": hf_repo, "model_short": short, "pool_strategy": pool,
        "subtask": args.subtask, "n_keys": int(n_keys), "n_terms_rows": int(n),
        "n_pooled_groups": int(len(pool_df)), "embed_dim": int(embed_dim),
        "max_len": MAX_LEN, "batch_size": int(args.batch_size),
        "dtype_compute": "bfloat16", "dtype_storage": "float16", "device": args.device,
        "elapsed_total_s": round(time.time() - t_start, 2), "elapsed_encode_s": round(t_enc, 2),
        "throughput_per_s": round(n / t_enc, 1) if t_enc > 0 else None,
        "norm_mean": float(norms.mean()), "norm_std": float(norms.std()),
        "args": vars(args),
        "outputs": {"pooled_parquet": str(out_path)},
    }
    (run_dir / "run_info.json").write_text(json.dumps(info, indent=2))
    echo(f"\nDone in {info['elapsed_total_s']:.1f}s")
    echo(f"  pooled parquet: {out_path}  ({out_path.stat().st_size/1e6:.2f} MB)")
    echo(f"  norms: mean={info['norm_mean']:.3f}  std={info['norm_std']:.3f}")
    log_f.close()


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--model", required=True, choices=list(MODEL_REGISTRY))
    p.add_argument("--subtask", default="serious-adverse-event-forecasting")
    p.add_argument("--batch-size", type=int, default=256)
    p.add_argument("--device", default="cuda")
    p.add_argument("--limit", type=int, default=None, help="Encode only first N terms (smoke)")
    args = p.parse_args()
    main(args)
