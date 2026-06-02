#!/usr/bin/env python3
"""
encode_text_column.py — Encode one TrialBench text column into a per-trial
embedding parquet, for use as a virtual feature column in Full Step 2.

Scope: only trials that actually appear in Phase 2 / Phase 3 (train + test) of
the 6 subtasks with an eligibility field — deduplicated by (trial_id, phase).
This keeps the (potentially expensive) encoding limited to what the downstream
experiments evaluate.

For list-valued cells (e.g. keyword, condition, intervention_name stored as a
Python-list string like "['A', 'B']") the list is parsed and joined into one
string. Each trial → exactly one embedding (one virtual token).

Encoders:
  medcpt  — ncbi/MedCPT-Article-Encoder, 768-d, [CLS] pooling, frozen
  qwen    — Qwen/Qwen3-Embedding-8B, 4096-d, dedicated text-embedding model,
            last-token pooling + L2 normalize (added for Step 2/3)

Output:
  branch/All_text_embedding/data/emb_<safe_column>_<encoder>.parquet
  columns: trial_id, phase, emb_0 .. emb_{d-1}
"""

from __future__ import annotations

import argparse
import ast
import re
import time
from pathlib import Path

import numpy as np
import pandas as pd
import torch

DATA_ROOT = Path("/data2/zhu11/TB/dataset/TrialBench")
OUT_DIR   = Path("/data2/zhu11/TB/branch/All_text_embedding/data")
SUBTASKS = [
    "serious-adverse-event-forecasting",
    "mortality-event-prediction",
    "patient-dropout-event-forecasting",
    "trial-approval-forecasting",
    "trial-failure-reason-identification",
    "trial-duration-forecasting",
]
DEVICE = "cuda"
WS = re.compile(r"\s+")


# -------------------------------------------------------------------------
# Collect target trials & raw text
# -------------------------------------------------------------------------

def clean_cell(val) -> str:
    """Normalize one raw cell into a single text string. List-valued cells are
    parsed and joined; NaN → empty string."""
    if val is None or (isinstance(val, float) and np.isnan(val)):
        return ""
    s = str(val).strip()
    if not s:
        return ""
    # List-valued cell stored as a Python-list string
    if s.startswith("[") and s.endswith("]"):
        try:
            parsed = ast.literal_eval(s)
            if isinstance(parsed, (list, tuple)):
                s = ", ".join(str(x) for x in parsed if x is not None and str(x).strip())
        except (ValueError, SyntaxError):
            pass
    return WS.sub(" ", s).strip()


def collect_column(column: str, phases: list[str]) -> pd.DataFrame:
    """Return DataFrame [trial_id, phase, text] for every (trial_id, phase)
    appearing in the given phases of the 6 subtasks (train + test), dedup'd."""
    seen: dict[tuple[str, str], str] = {}
    n_files = 0
    for subtask in SUBTASKS:
        for phase in phases:
            for split in ["train_x.csv", "test_x.csv"]:
                csv = DATA_ROOT / subtask / phase / split
                if not csv.exists():
                    continue
                header = pd.read_csv(csv, nrows=0).columns.tolist()
                if column not in header:
                    continue
                id_col = header[0]
                df = pd.read_csv(csv, usecols=[id_col, column])
                df.columns = ["trial_id", "raw"]
                n_files += 1
                for tid, raw in zip(df["trial_id"], df["raw"]):
                    key = (str(tid), phase)
                    if key not in seen:
                        seen[key] = clean_cell(raw)
    rows = [{"trial_id": t, "phase": p, "text": txt} for (t, p), txt in seen.items()]
    out = pd.DataFrame(rows).sort_values(["phase", "trial_id"]).reset_index(drop=True)
    print(f"  scanned {n_files} CSVs → {len(out)} unique (trial_id, phase)")
    n_empty = int((out['text'].str.len() == 0).sum())
    print(f"  empty cells: {n_empty} ({n_empty/len(out)*100:.1f}%)")
    return out


# -------------------------------------------------------------------------
# Encoders
# -------------------------------------------------------------------------

@torch.inference_mode()
def encode_medcpt(texts: list[str], batch_size: int = 256) -> np.ndarray:
    from transformers import AutoModel, AutoTokenizer
    name = "ncbi/MedCPT-Article-Encoder"
    print(f"  loading {name} ...")
    tok = AutoTokenizer.from_pretrained(name)
    model = AutoModel.from_pretrained(name).to(DEVICE).eval()
    # length-sorted batching
    order = sorted(range(len(texts)), key=lambda i: len(texts[i]), reverse=True)
    out = np.zeros((len(texts), 768), dtype=np.float16)
    for s in range(0, len(texts), batch_size):
        idx = order[s:s + batch_size]
        batch = [texts[i] if texts[i] else "[empty]" for i in idx]
        enc = tok(batch, padding=True, truncation=True, max_length=512,
                  return_tensors="pt").to(DEVICE)
        with torch.autocast(device_type="cuda", dtype=torch.bfloat16):
            emb = model(**enc).last_hidden_state[:, 0, :]   # [CLS]
        emb = emb.float().cpu().numpy().astype(np.float16)
        for j, i in enumerate(idx):
            out[i] = emb[j]
    return out


@torch.inference_mode()
def encode_qwen(texts: list[str], batch_size: int = 16) -> np.ndarray:
    """Qwen3-Embedding-8B — a dedicated text-embedding model (Qwen3 family).
    Decoder backbone with last-token pooling; output is L2-normalized, 4096-d."""
    from transformers import AutoModel, AutoTokenizer
    name = "Qwen/Qwen3-Embedding-8B"
    print(f"  loading {name} ... (dedicated embedding model, last-token pooling)")
    tok = AutoTokenizer.from_pretrained(name, padding_side="left")
    model = AutoModel.from_pretrained(name, torch_dtype=torch.bfloat16).to(DEVICE).eval()
    hid = model.config.hidden_size
    order = sorted(range(len(texts)), key=lambda i: len(texts[i]), reverse=True)
    out = np.zeros((len(texts), hid), dtype=np.float16)
    for s in range(0, len(texts), batch_size):
        idx = order[s:s + batch_size]
        batch = [texts[i] if texts[i] else "[empty]" for i in idx]
        enc = tok(batch, padding=True, truncation=True, max_length=2048,
                  return_tensors="pt").to(DEVICE)
        with torch.autocast(device_type="cuda", dtype=torch.bfloat16):
            res = model(**enc)
        # left-padded → last real token is at position -1
        emb = res.last_hidden_state[:, -1, :]
        emb = torch.nn.functional.normalize(emb.float(), p=2, dim=-1)  # L2 normalize
        emb = emb.cpu().numpy().astype(np.float16)
        for j, i in enumerate(idx):
            out[i] = emb[j]
    return out


# -------------------------------------------------------------------------
# Main
# -------------------------------------------------------------------------

def main(args):
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    phases = [p.strip() for p in args.phases.split(",")]
    safe_col = args.column.replace("/", "_")
    out_path = OUT_DIR / f"emb_{safe_col}_{args.encoder}.parquet"
    print(f"[column] {args.column}")
    print(f"[encoder] {args.encoder}  [phases] {phases}")

    t0 = time.time()
    df = collect_column(args.column, phases)
    texts = df["text"].tolist()

    print(f"Encoding {len(texts)} texts with {args.encoder} ...")
    if args.encoder == "medcpt":
        embs = encode_medcpt(texts, batch_size=args.batch_size)
    elif args.encoder == "qwen":
        embs = encode_qwen(texts, batch_size=args.batch_size)
    else:
        raise ValueError(args.encoder)
    d = embs.shape[1]
    print(f"  embeddings: {embs.shape}  ({embs.nbytes/1e6:.1f} MB)  in {time.time()-t0:.1f}s")

    emb_df = pd.DataFrame(embs, columns=[f"emb_{i}" for i in range(d)])
    out = pd.concat([df[["trial_id", "phase"]].reset_index(drop=True), emb_df], axis=1)
    out.to_parquet(out_path, index=False)
    print(f"Wrote: {out_path}  shape={out.shape}")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--column", required=True, help="CSV column name, e.g. brief_summary/textblock")
    p.add_argument("--encoder", choices=["medcpt", "qwen"], default="medcpt")
    p.add_argument("--phases", default="Phase2,Phase3")
    p.add_argument("--batch-size", type=int, default=256)
    args = p.parse_args()
    main(args)
