#!/usr/bin/env python3
"""
encode_smiles_hf.py — Encode SMILES strings with one of three HF chemistry
transformer encoders, then mean-pool per (trial_id, phase).

Supported encoders (--model):
  chemberta_mlm : DeepChem/ChemBERTa-77M-MLM       (d=384, MLM-pretrained)
  chemberta_mtr : DeepChem/ChemBERTa-77M-MTR       (d=384, multi-task-regression variant)
  molformer     : ibm/MoLFormer-XL-both-10pct      (d=768, requires trust_remote_code)

Reads:
  /data2/zhu11/TB/dataset/TrialBench/<subtask>/Phase{1..4}/{train,test}_x.csv
  Extracts `smiless` column (stringified Python list of SMILES strings per trial).

Writes (canonical, consumed by full_step2_tabicl_smiles.py):
  /data2/zhu11/TB/branch/smiles/data/smiles_embeddings_<short>.parquet
    columns: trial_id, phase, mean_emb (np.float32 array len=d), n_smiles (int)

Writes (audit):
  /data2/zhu11/TB/branch/smiles/results/encode_smiles_<short>_<YYYYMMDD_HHMMSS>/
    per_smiles_embeddings.npy
    per_smiles_metadata.parquet  # trial_id, phase, smiles, n_chars
    run_info.json
    log.txt

Pooling within a SMILES string: mean of last_hidden_state masked by attention,
unless the model has a native pooler (MoLFormer's pooler_output).
Per trial: mean of its unique SMILES embeddings.
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
OUT_DATA_DIR = Path("/data2/zhu11/TB/branch/smiles/data")
RESULTS_ROOT = Path("/data2/zhu11/TB/branch/smiles/results")

# (hf_repo, short_name, pool_strategy)
#   "cls_mean"   – mean of last_hidden_state with attention mask (works for BERT-likes)
#   "pooler"     – use model's pooler_output (MoLFormer)
MODEL_REGISTRY = {
    "chemberta_mlm": ("DeepChem/ChemBERTa-77M-MLM", "chemberta_mlm", "cls_mean"),
    "chemberta_mtr": ("DeepChem/ChemBERTa-77M-MTR", "chemberta_mtr", "cls_mean"),
    "molformer":     ("ibm/MoLFormer-XL-both-10pct", "molformer",     "pooler"),
}


def parse_smiles(s) -> list[str]:
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
            return [s]  # fall back to treating the whole field as a single SMILES


def collect_smiles_corpus(subtask: str) -> dict:
    """Scan all phases × {train,test} of one subtask. Returns
    {(trial_id, phase) → set(SMILES)} — deduped within a (trial, phase)."""
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
            if "smiless" not in cols:
                continue
            df = pd.read_csv(csv, index_col=0, usecols=[cols[0], "smiless"])
            for trial_id, smi_str in df["smiless"].items():
                key = (str(trial_id), phase)
                out.setdefault(key, set()).update(parse_smiles(smi_str))
    return out


def build_flat_queue(corpus: dict) -> list[dict]:
    """Flatten (trial_id, phase) → set(SMILES) into encoding queue rows."""
    rows: list[dict] = []
    for (tid, ph), smis in corpus.items():
        for smi in smis:
            if smi and isinstance(smi, str):
                rows.append({"trial_id": tid, "phase": ph,
                             "smiles": smi, "n_chars": len(smi)})
    return rows


@torch.inference_mode()
def encode_batch(texts, tokenizer, model, device, pool_strategy):
    enc = tokenizer(texts, padding=True, truncation=True,
                    max_length=512, return_tensors="pt").to(device)
    out = model(**enc)
    if pool_strategy == "pooler":
        emb = out.pooler_output
    elif pool_strategy == "cls_mean":
        # Masked mean over last_hidden_state (avoids dominance of CLS or pad tokens).
        h = out.last_hidden_state                   # (B, T, D)
        mask = enc["attention_mask"].unsqueeze(-1).float()  # (B, T, 1)
        emb = (h * mask).sum(dim=1) / mask.sum(dim=1).clamp(min=1)
    else:
        raise ValueError(f"unknown pool_strategy: {pool_strategy}")
    return emb.float().cpu().numpy()


def main(args):
    if args.model not in MODEL_REGISTRY:
        raise ValueError(f"--model must be one of {list(MODEL_REGISTRY)}")
    hf_repo, short, pool_strategy = MODEL_REGISTRY[args.model]

    run_id  = f"encode_smiles_{short}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    run_dir = RESULTS_ROOT / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    OUT_DATA_DIR.mkdir(parents=True, exist_ok=True)
    log_f = open(run_dir / "log.txt", "w")

    def echo(*parts):
        line = " ".join(str(p) for p in parts)
        print(line)
        print(line, file=log_f, flush=True)

    echo(f"[run_id] {run_id}")
    echo(f"[model] {hf_repo}  short={short}  pool={pool_strategy}")
    echo(f"[subtask] {args.subtask}")

    t_start = time.time()

    # ---- 1. Collect SMILES corpus ----
    echo("Scanning train_x.csv / test_x.csv for `smiless` column ...")
    corpus = collect_smiles_corpus(args.subtask)
    n_keys = len(corpus)
    n_keys_with_smiles = sum(1 for s in corpus.values() if s)
    n_unique_smiles_total = sum(len(s) for s in corpus.values())
    echo(f"  {n_keys:,} (trial_id, phase) pairs  "
         f"({n_keys_with_smiles:,} non-empty, "
         f"{100*n_keys_with_smiles/n_keys:.1f}%)")
    echo(f"  total unique (trial_id, phase, smiles) triples to encode: {n_unique_smiles_total:,}")

    rows = build_flat_queue(corpus)
    if args.limit:
        rows = rows[:args.limit]
    n = len(rows)
    if n == 0:
        raise RuntimeError("No SMILES to encode — corpus is empty.")
    echo(f"  encoding {n:,} SMILES strings")

    # ---- 2. Length-sorted batching ----
    order = sorted(range(n), key=lambda i: rows[i]["n_chars"], reverse=True)

    # ---- 3. Load model ----
    # NOTE: load in fp32, move to device, then cast. Some models (MolFormer)
    # initialize random-orthogonal buffers on CPU and QR-decompose them at
    # __init__ time, which torch doesn't implement for bf16/fp16 on CPU.
    echo(f"Loading {hf_repo} ...")
    tok_kwargs = {"trust_remote_code": pool_strategy == "pooler"}
    mdl_kwargs = {"trust_remote_code": pool_strategy == "pooler"}
    if pool_strategy == "pooler":
        mdl_kwargs["deterministic_eval"] = True
    target_dtype = torch.bfloat16 if args.dtype == "bf16" else torch.float16
    tokenizer = AutoTokenizer.from_pretrained(hf_repo, **tok_kwargs)
    model = AutoModel.from_pretrained(hf_repo, **mdl_kwargs).to(args.device).to(target_dtype).eval()
    n_params = sum(p.numel() for p in model.parameters())
    echo(f"  params={n_params:,}  dtype={args.dtype}  batch_size={args.batch_size}")

    # Detect output dim with one forward.
    with torch.inference_mode():
        sample = encode_batch([rows[order[0]]["smiles"]], tokenizer, model,
                              args.device, pool_strategy)
    embed_dim = sample.shape[-1]
    echo(f"  embed_dim (detected): {embed_dim}")

    # ---- 4. Encode ----
    embs = np.empty((n, embed_dim), dtype=np.float16)
    t_enc_start = time.time()
    for batch_start in tqdm(range(0, n, args.batch_size), desc="encoding"):
        batch_idx = order[batch_start:batch_start + args.batch_size]
        texts = [rows[i]["smiles"] for i in batch_idx]
        emb = encode_batch(texts, tokenizer, model, args.device, pool_strategy)
        for j, orig_i in enumerate(batch_idx):
            embs[orig_i] = emb[j].astype(np.float16)
    t_enc = time.time() - t_enc_start
    echo(f"  encode done in {t_enc:.1f}s ({n/t_enc:.1f}/s)")

    # ---- 5. Save per-SMILES audit ----
    np.save(run_dir / "per_smiles_embeddings.npy", embs)
    meta_df = pd.DataFrame(rows)
    meta_df.to_parquet(run_dir / "per_smiles_metadata.parquet", index=False)

    # ---- 6. Mean-pool per (trial_id, phase) ----
    echo("Mean-pooling per (trial_id, phase) ...")
    composite = (meta_df["trial_id"].astype(str) + "|" + meta_df["phase"].astype(str))
    codes, uniques = pd.factorize(composite, sort=True)
    n_groups = len(uniques)

    e_t = torch.from_numpy(embs.astype(np.float32)).to(args.device)
    c_t = torch.from_numpy(codes.astype(np.int64)).to(args.device)
    sums = torch.zeros(n_groups, embed_dim, device=args.device)
    cnts = torch.zeros(n_groups, device=args.device)
    sums.index_add_(0, c_t, e_t)
    cnts.index_add_(0, c_t, torch.ones_like(c_t, dtype=torch.float32))
    pooled = (sums / cnts.unsqueeze(1)).cpu().numpy().astype(np.float32)
    counts_cpu = cnts.cpu().numpy().astype(np.int64)

    rows_out = []
    for i, key in enumerate(uniques):
        tid, ph = key.split("|")
        rows_out.append({
            "trial_id": tid, "phase": ph,
            "mean_emb": pooled[i],          # 1-D np.float32 array, len=embed_dim
            "n_smiles": int(counts_cpu[i]),  # how many SMILES went into the mean
        })
    pool_df = pd.DataFrame(rows_out)
    out_path = OUT_DATA_DIR / f"smiles_embeddings_{short}.parquet"
    pool_df.to_parquet(out_path, index=False)
    echo(f"  mean-pooled groups: {len(pool_df):,} → {out_path}")

    # ---- 7. Stats ----
    norms = np.linalg.norm(embs.astype(np.float32), axis=1)
    info = {
        "run_id":              run_id,
        "model":               hf_repo,
        "model_short":         short,
        "pool_strategy":       pool_strategy,
        "subtask":             args.subtask,
        "n_keys":              int(n_keys),
        "n_keys_with_smiles":  int(n_keys_with_smiles),
        "n_unique_smiles":     int(n),
        "n_pooled_groups":     int(len(pool_df)),
        "embed_dim":           int(embed_dim),
        "batch_size":          int(args.batch_size),
        "dtype_compute":       args.dtype,
        "dtype_storage":       "float16",
        "device":              args.device,
        "elapsed_total_s":     round(time.time() - t_start, 2),
        "elapsed_encode_s":    round(t_enc, 2),
        "throughput_per_s":    round(n / t_enc, 1) if t_enc > 0 else None,
        "norm_mean":           float(norms.mean()),
        "norm_std":            float(norms.std()),
        "args":                vars(args),
        "outputs": {
            "pooled_parquet": str(out_path),
            "per_smiles_npy": str(run_dir / "per_smiles_embeddings.npy"),
            "per_smiles_meta": str(run_dir / "per_smiles_metadata.parquet"),
        },
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
    p.add_argument("--batch-size", type=int, default=128)
    p.add_argument("--device", default="cuda")
    p.add_argument("--dtype", choices=["bf16", "fp16"], default="bf16")
    p.add_argument("--limit", type=int, default=None,
                   help="Encode only first N SMILES (smoke test)")
    args = p.parse_args()
    main(args)
