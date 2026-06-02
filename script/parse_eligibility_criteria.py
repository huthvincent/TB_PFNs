"""
Parse `eligibility/criteria/textblock` from TrialBench CSVs into per-trial
inclusion / exclusion criteria lists.

Outputs two JSON files (each is a list of objects):
  /data2/zhu11/TB/dataset/TrialBench/inclusion.json
  /data2/zhu11/TB/dataset/TrialBench/exclusion.json

Object shape:
  {"trial_id": "NCT...", "phase": "Phase1|Phase2|Phase3|Phase4",
   "inclusion": ["...", ...]}   # or "exclusion"

Source: 6 subtasks (mortality, dropout, SAE, approval, duration, failure-reason)
        x 4 phases x {train, test}, deduplicated by (trial_id, phase).

Parser:
  1. Split text on first occurrence of "Exclusion Criteria" / "Exclusion:".
  2. In each half, split on bullet markers `-` or `1.`/`1)`.
  3. If no bullets found, sentence-split as fallback.
"""

import glob
import json
import re
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path("/data2/zhu11/TB/dataset/TrialBench")
COL  = "eligibility/criteria/textblock"
OUT_INC = ROOT / "inclusion.json"
OUT_EXC = ROOT / "exclusion.json"

RE_EXCL  = re.compile(r"(?im)^[ \t]*(?:\w+[ \t]+)*exclusion(?:ary)?(?:[ \t]+criteri\w*|[ \t]*:)")
RE_BULL  = re.compile(r"(?m)^\s*(?:-|\d+[.)])\s+")
RE_WS    = re.compile(r"\s+")
RE_SENT  = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9])")
RE_PHASE = re.compile(r"/Phase([1-4])/")


def normalize(s: str) -> str:
    return RE_WS.sub(" ", s).strip()


def split_items(text: str) -> list:
    if not text or not text.strip():
        return []
    parts = RE_BULL.split(text)
    items = [normalize(p) for p in parts[1:] if normalize(p)]
    if items:
        return items
    sents = [normalize(s) for s in RE_SENT.split(text.strip())]
    return [s for s in sents if len(s) > 5]


def parse_textblock(text):
    if not isinstance(text, str) or not text.strip():
        return [], []
    m = RE_EXCL.search(text)
    if m:
        return split_items(text[:m.start()]), split_items(text[m.end():])
    return split_items(text), []


def phase_from_path(p: str):
    m = RE_PHASE.search(p)
    return f"Phase{m.group(1)}" if m else None


def main():
    csvs = sorted(glob.glob(str(ROOT / "**/*_x.csv"), recursive=True))
    seen = {}  # (trial_id, phase) -> textblock
    t0 = time.time()
    for f in csvs:
        phase = phase_from_path(f)
        if phase is None:
            continue
        try:
            df = pd.read_csv(f, usecols=lambda c: c in ("Unnamed: 0", COL), dtype=str)
        except ValueError:
            continue
        if COL not in df.columns:
            continue
        df = df.rename(columns={"Unnamed: 0": "trial_id"}).dropna(subset=[COL])
        added = 0
        for tid, tb in zip(df["trial_id"], df[COL]):
            key = (tid, phase)
            if key not in seen:
                seen[key] = tb
                added += 1
        rel = Path(f).relative_to(ROOT)
        print(f"  {str(rel):75s} rows={len(df):>6d}  new={added:>6d}  cum={len(seen)}")

    print(f"\n[load] {len(seen)} unique (trial_id, phase) in {time.time()-t0:.1f}s")

    inc_out, exc_out = [], []
    for (tid, phase), tb in seen.items():
        inc, exc = parse_textblock(tb)
        inc_out.append({"trial_id": tid, "phase": phase, "inclusion": inc})
        exc_out.append({"trial_id": tid, "phase": phase, "exclusion": exc})
    inc_out.sort(key=lambda x: (x["trial_id"], x["phase"]))
    exc_out.sort(key=lambda x: (x["trial_id"], x["phase"]))

    OUT_INC.write_text(json.dumps(inc_out, ensure_ascii=False))
    OUT_EXC.write_text(json.dumps(exc_out, ensure_ascii=False))

    inc_lens = np.array([len(d["inclusion"]) for d in inc_out])
    exc_lens = np.array([len(d["exclusion"]) for d in exc_out])
    print(f"\n[write] {OUT_INC} ({OUT_INC.stat().st_size/1e6:.1f} MB)")
    print(f"[write] {OUT_EXC} ({OUT_EXC.stat().st_size/1e6:.1f} MB)")
    print(f"\nTrials: {len(inc_out)}")
    print(f"Inclusion items / trial:  mean={inc_lens.mean():.2f}  median={np.median(inc_lens):.0f}  "
          f"max={inc_lens.max()}  zero={(inc_lens==0).sum()}")
    print(f"Exclusion items / trial:  mean={exc_lens.mean():.2f}  median={np.median(exc_lens):.0f}  "
          f"max={exc_lens.max()}  zero={(exc_lens==0).sum()}")
    print("\nPhase distribution:")
    phases = pd.Series([d["phase"] for d in inc_out]).value_counts().sort_index()
    print(phases.to_string())


if __name__ == "__main__":
    main()
