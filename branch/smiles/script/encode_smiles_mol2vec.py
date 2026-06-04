#!/usr/bin/env python3
"""
encode_smiles_mol2vec.py — Encode SMILES with Mol2Vec (word2vec-style 300-d
embedding over Morgan-radius-1 substructure identifiers), mean-pooled per
(trial_id, phase).

Mol2Vec (Jaeger et al. 2018) treats each SMILES → RDKit Mol → list of Morgan
fingerprint identifiers (radius=1) as a "sentence" of substructure tokens.
A pretrained word2vec model maps each token to a 300-d vector; per-molecule
embedding = mean of token vectors (handled by `sentences2vec`).

Pretrained weights:
  /data2/zhu11/TB/branch/smiles/data/model_300dim.pkl
  Downloaded from https://github.com/samoturk/mol2vec/raw/master/examples/models/model_300dim.pkl
  (21K-token vocabulary, 300-d, trained on ~20M ZINC + ChEMBL molecules)

Reads:
  /data2/zhu11/TB/dataset/TrialBench/<subtask>/Phase{1..4}/{train,test}_x.csv
  Same `smiless` column / dedup logic as encode_smiles_hf.py.

Writes (canonical):
  /data2/zhu11/TB/branch/smiles/data/smiles_embeddings_mol2vec.parquet
    columns: trial_id, phase, mean_emb (np.float32 array len=300), n_smiles (int)

Writes (audit):
  /data2/zhu11/TB/branch/smiles/results/encode_smiles_mol2vec_<YYYYMMDD_HHMMSS>/
    per_smiles_embeddings.npy
    per_smiles_metadata.parquet  # trial_id, phase, smiles, n_chars, valid
    run_info.json
    log.txt

CPU-only (gensim w2v + RDKit). No GPU needed.
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
from gensim.models import word2vec
from mol2vec.features import MolSentence, mol2alt_sentence
from rdkit import Chem, RDLogger


def sentences2vec(sentences, model, unseen="UNK"):
    """Re-implementation of mol2vec.features.sentences2vec for gensim >= 4.0.

    The upstream `sentences2vec` calls `model.wv.vocab` which was removed in
    gensim 4.0. Modern API uses `key_to_index` / `__contains__`. Behavior
    matches the upstream reference (sum of token vectors per sentence; unseen
    tokens replaced by the `unseen` token's vector when provided).
    """
    wv = model.wv
    unseen_vec = wv[unseen] if unseen is not None and unseen in wv else None
    out = []
    for sent in sentences:
        if unseen_vec is not None:
            vecs = [wv[t] if t in wv else unseen_vec for t in sent]
        else:
            vecs = [wv[t] for t in sent if t in wv]
        out.append(np.sum(vecs, axis=0) if vecs else np.zeros(wv.vector_size, dtype=np.float32))
    return np.asarray(out)
from tqdm import tqdm

# Silence RDKit's noisy "Explicit valence … is greater than permitted" warnings
# for the SMILES that come out malformed; we handle invalid mols explicitly.
RDLogger.DisableLog("rdApp.*")

DATASET_ROOT = Path("/data2/zhu11/TB/dataset/TrialBench")
OUT_DATA_DIR = Path("/data2/zhu11/TB/branch/smiles/data")
RESULTS_ROOT = Path("/data2/zhu11/TB/branch/smiles/results")
W2V_MODEL    = OUT_DATA_DIR / "model_300dim.pkl"
EMBED_DIM    = 300
RADIUS       = 1


def parse_smiles(s) -> list[str]:
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


def collect_smiles_corpus(subtask: str) -> dict:
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


def main(args):
    short = "mol2vec"
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
    echo(f"[subtask] {args.subtask}  [radius] {RADIUS}  [embed_dim] {EMBED_DIM}")

    t_start = time.time()

    # ---- 1. Collect SMILES (union over one or more subtasks) ----
    subtasks = [s.strip() for s in args.subtasks.split(",")] if args.subtasks else [args.subtask]
    echo(f"Scanning `smiless` over subtasks: {subtasks}")
    corpus = {}
    for st in subtasks:
        for k, smis in collect_smiles_corpus(st).items():
            corpus.setdefault(k, set()).update(smis)
    n_keys = len(corpus)
    n_keys_with_smiles = sum(1 for s in corpus.values() if s)
    echo(f"  {n_keys:,} (trial_id, phase) pairs  "
         f"({n_keys_with_smiles:,} non-empty, {100*n_keys_with_smiles/max(1,n_keys):.1f}%)")

    rows = []
    for (tid, ph), smis in corpus.items():
        for smi in smis:
            if smi and isinstance(smi, str):
                rows.append({"trial_id": tid, "phase": ph,
                             "smiles": smi, "n_chars": len(smi)})
    if args.limit:
        rows = rows[:args.limit]
    n = len(rows)
    if n == 0:
        raise RuntimeError("No SMILES to encode.")
    echo(f"  encoding {n:,} SMILES strings")

    # ---- 2. Load pretrained mol2vec ----
    echo(f"Loading mol2vec model: {W2V_MODEL} ...")
    if not W2V_MODEL.exists():
        raise FileNotFoundError(
            f"Pretrained mol2vec model not found at {W2V_MODEL}. "
            "Download it once: "
            "curl -fL -o " + str(W2V_MODEL) +
            " https://github.com/samoturk/mol2vec/raw/master/examples/models/model_300dim.pkl"
        )
    m2v = word2vec.Word2Vec.load(str(W2V_MODEL))
    echo(f"  vector_size={m2v.vector_size}  vocab={len(m2v.wv):,}")
    assert m2v.vector_size == EMBED_DIM, f"expected {EMBED_DIM}, got {m2v.vector_size}"

    # ---- 3. Build RDKit mols + Morgan substructure sentences ----
    echo("Converting SMILES → RDKit Mol → Morgan substructure sentences ...")
    valid_flags = np.zeros(n, dtype=bool)
    sentences: list = []
    sent_idx: list = []  # original row index for each valid sentence
    for i, r in enumerate(tqdm(rows, desc="rdkit")):
        mol = Chem.MolFromSmiles(r["smiles"])
        if mol is None:
            continue
        try:
            sent = MolSentence(mol2alt_sentence(mol, RADIUS))
        except Exception:
            continue
        if len(sent) == 0:
            continue
        valid_flags[i] = True
        sentences.append(sent)
        sent_idx.append(i)

    n_valid = len(sentences)
    echo(f"  RDKit-valid SMILES: {n_valid:,}/{n:,} ({100*n_valid/n:.1f}%)")

    # ---- 4. Vectorize sentences → 300-d via mol2vec ----
    echo("Vectorizing sentences (mean of substructure word vectors) ...")
    # sentences2vec returns numpy array (n_valid, 300)
    valid_vecs = np.asarray(sentences2vec(sentences, m2v, unseen="UNK"), dtype=np.float32)
    embs = np.zeros((n, EMBED_DIM), dtype=np.float32)
    for j, i in enumerate(sent_idx):
        embs[i] = valid_vecs[j]
    # Store as fp16 for parity with HF script outputs (300 floats per record is tiny)
    embs_f16 = embs.astype(np.float16)
    echo(f"  done")

    # ---- 5. Save per-SMILES audit ----
    np.save(run_dir / "per_smiles_embeddings.npy", embs_f16)
    meta = pd.DataFrame(rows)
    meta["valid"] = valid_flags
    meta.to_parquet(run_dir / "per_smiles_metadata.parquet", index=False)

    # ---- 6. Mean-pool per (trial_id, phase) over VALID SMILES only ----
    echo("Mean-pooling per (trial_id, phase) over valid SMILES ...")
    meta["composite"] = meta["trial_id"].astype(str) + "|" + meta["phase"].astype(str)
    pool_rows = []
    for key, grp in meta.groupby("composite"):
        valid_grp = grp[grp["valid"]]
        n_v = len(valid_grp)
        if n_v == 0:
            continue  # skip trials with no valid RDKit mols → training falls back to zeros
        mean_v = embs[valid_grp.index.to_numpy()].mean(axis=0).astype(np.float32)
        tid, ph = key.split("|")
        pool_rows.append({"trial_id": tid, "phase": ph,
                          "mean_emb": mean_v, "n_smiles": int(n_v)})
    pool_df = pd.DataFrame(pool_rows)
    out_path = OUT_DATA_DIR / f"smiles_embeddings_{short}.parquet"
    pool_df.to_parquet(out_path, index=False)
    echo(f"  mean-pooled groups: {len(pool_df):,} → {out_path}")

    # ---- 7. Stats ----
    valid_embs = embs[valid_flags]
    norms = np.linalg.norm(valid_embs, axis=1) if len(valid_embs) else np.array([0.0])
    info = {
        "run_id":             run_id,
        "model":              "mol2vec (gensim word2vec, Morgan radius=1)",
        "model_short":        short,
        "pretrained_pkl":     str(W2V_MODEL),
        "subtask":            args.subtask,
        "n_keys":             int(n_keys),
        "n_keys_with_smiles": int(n_keys_with_smiles),
        "n_unique_smiles":    int(n),
        "n_rdkit_valid":      int(n_valid),
        "n_pooled_groups":    int(len(pool_df)),
        "embed_dim":          EMBED_DIM,
        "radius":             RADIUS,
        "elapsed_total_s":    round(time.time() - t_start, 2),
        "norm_mean":          float(norms.mean()),
        "norm_std":           float(norms.std()),
        "args":               vars(args),
        "outputs": {
            "pooled_parquet": str(out_path),
            "per_smiles_npy": str(run_dir / "per_smiles_embeddings.npy"),
            "per_smiles_meta": str(run_dir / "per_smiles_metadata.parquet"),
        },
    }
    (run_dir / "run_info.json").write_text(json.dumps(info, indent=2))

    echo(f"\nDone in {info['elapsed_total_s']:.1f}s")
    echo(f"  pooled parquet: {out_path}  ({out_path.stat().st_size/1e6:.2f} MB)")
    echo(f"  norms (valid): mean={info['norm_mean']:.3f}  std={info['norm_std']:.3f}")
    log_f.close()


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--subtask", default="serious-adverse-event-forecasting")
    p.add_argument("--subtasks", default=None, help="comma-list of subtasks (union); overrides --subtask")
    p.add_argument("--limit", type=int, default=None)
    args = p.parse_args()
    main(args)
