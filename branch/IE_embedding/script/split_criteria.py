#!/usr/bin/env python3
"""
split_criteria.py — Parse `eligibility/criteria/textblock` from all TrialBench
subtasks into per-criterion inclusion / exclusion JSON files.

Scope:
  - 6 subtasks × 4 phases × {train_x, test_x} = 48 CSVs
  - Skipped: drug-dose-prediction, eligibility-criteria-design (no eligibility col)
  - Dedup key = (trial_id, phase); a trial that appears in multiple subtasks with
    the same phase keeps the first parsed copy (eligibility text is identical
    across subtasks for a given trial).

Parser rules:
  1. Split textblock on the first `Exclusion(s) [Criteria]?:` header (case-insensitive,
     word-boundary). Everything before = inclusion section; after = exclusion section.
  2. Strip leading `Inclusion [Criteria]?:` header from the inclusion section.
  3. In each section, find bullets via `^\\s*(- | \\d+[.)])\\s+` (multiline);
     text between consecutive bullet positions is one criterion (whitespace-normalized).
  4. If a section has no bullets, fall back to sentence split (`. ! ?`), keeping
     fragments with len > 5 chars.

Output (two files, valid JSON arrays):
  /data2/zhu11/TB/branch/IE_embedding/data/inclusion.json
  /data2/zhu11/TB/branch/IE_embedding/data/exclusion.json

Each entry: {"trial_id": "NCT...", "phase": "Phase2", "criteria": ["...", "...", ...]}
"""

import json
import re
from pathlib import Path

import pandas as pd

DATA_ROOT = Path("/data2/zhu11/TB/dataset/TrialBench")
OUT_DIR   = Path("/data2/zhu11/TB/branch/IE_embedding/data")

SUBTASKS = [
    "mortality-event-prediction",
    "patient-dropout-event-forecasting",
    "serious-adverse-event-forecasting",
    "trial-approval-forecasting",
    "trial-duration-forecasting",
    "trial-failure-reason-identification",
]
PHASES = ["Phase1", "Phase2", "Phase3", "Phase4"]
SPLITS = ["train_x.csv", "test_x.csv"]

CRIT_COL = "eligibility/criteria/textblock"

_HDR_PREFIX = r"^[ \t]*(?:-[ \t]+)?(?:key[ \t]+|main[ \t]+|primary[ \t]+)?"
_HDR_SUFFIX = r"(?:[ \t]+criteria)?[ \t]*:?[ \t\r]*$"
EXCL_HEADER = re.compile(rf"(?im){_HDR_PREFIX}exclusions?{_HDR_SUFFIX}")
INCL_HEADER = re.compile(rf"(?im){_HDR_PREFIX}inclusions?{_HDR_SUFFIX}")
ITEM_PAT    = re.compile(r"(?m)^\s*(?:-|\d+[.)])\s+")
SENT_PAT    = re.compile(r"(?<=[.!?])\s+")
WS_PAT      = re.compile(r"\s+")


def split_block_into_items(text: str) -> list[str]:
    if not text or not text.strip():
        return []
    matches = list(ITEM_PAT.finditer(text))
    if matches:
        items = []
        for i, m in enumerate(matches):
            start = m.end()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            piece = WS_PAT.sub(" ", text[start:end]).strip()
            if piece:
                items.append(piece)
        return items
    sents = [WS_PAT.sub(" ", s).strip() for s in SENT_PAT.split(text.strip())]
    return [s for s in sents if len(s) > 5]


def parse_eligibility(text) -> tuple[list[str], list[str]]:
    """Split textblock into (inclusion_items, exclusion_items).

    Scans for ALL inclusion / exclusion section headers and assigns the text
    chunk after each header to the matching bucket. Handles multi-part trials
    (e.g., Part 1 / Part 2 with separate I/E for each).
    """
    if not isinstance(text, str) or not text.strip():
        return [], []
    headers = []
    for m in INCL_HEADER.finditer(text):
        headers.append((m.start(), m.end(), "incl"))
    for m in EXCL_HEADER.finditer(text):
        headers.append((m.start(), m.end(), "excl"))
    headers.sort()

    if not headers:
        # No structure — treat whole text as inclusion via fallback splitter
        return split_block_into_items(text), []

    # If the first header is exclusion, the preceding text is the (header-less)
    # inclusion section — insert a virtual inclusion header at position 0.
    if headers[0][2] == "excl":
        headers.insert(0, (0, 0, "incl"))

    incl_items, excl_items = [], []
    for i, (_, hdr_end, kind) in enumerate(headers):
        chunk_end = headers[i + 1][0] if i + 1 < len(headers) else len(text)
        items = split_block_into_items(text[hdr_end:chunk_end])
        (incl_items if kind == "incl" else excl_items).extend(items)
    return incl_items, excl_items


def read_eligibility(csv_path: Path) -> pd.Series | None:
    """Return Series indexed by trial_id with eligibility text. None if col absent."""
    header = pd.read_csv(csv_path, nrows=0).columns.tolist()
    if CRIT_COL not in header:
        return None
    id_col = header[0]
    df = pd.read_csv(csv_path, usecols=[id_col, CRIT_COL])
    df.columns = ["trial_id", "criteria_text"]
    return df.set_index("trial_id")["criteria_text"]


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    seen: dict[tuple[str, str], tuple[list[str], list[str]]] = {}
    n_files = 0
    n_rows = 0

    for subtask in SUBTASKS:
        for phase in PHASES:
            phase_dir = DATA_ROOT / subtask / phase
            if not phase_dir.is_dir():
                continue
            for split in SPLITS:
                csv = phase_dir / split
                if not csv.exists():
                    continue
                col = read_eligibility(csv)
                if col is None:
                    continue
                n_files += 1
                added = 0
                for trial_id, text in col.items():
                    n_rows += 1
                    key = (str(trial_id), phase)
                    if key in seen:
                        continue
                    seen[key] = parse_eligibility(text)
                    added += 1
                print(f"  {subtask}/{phase}/{split}: rows={len(col)} new={added}")

    incl_list, excl_list = [], []
    for (trial_id, phase), (incl, excl) in sorted(seen.items()):
        incl_list.append({"trial_id": trial_id, "phase": phase, "criteria": incl})
        excl_list.append({"trial_id": trial_id, "phase": phase, "criteria": excl})

    out_incl = OUT_DIR / "inclusion.json"
    out_excl = OUT_DIR / "exclusion.json"
    with out_incl.open("w") as f:
        json.dump(incl_list, f, ensure_ascii=False)
    with out_excl.open("w") as f:
        json.dump(excl_list, f, ensure_ascii=False)

    n_trials = len(seen)
    n_i = sum(len(v[0]) for v in seen.values())
    n_e = sum(len(v[1]) for v in seen.values())
    n_empty_incl = sum(1 for v in seen.values() if not v[0])
    n_empty_excl = sum(1 for v in seen.values() if not v[1])

    print(f"\nFiles processed:           {n_files}")
    print(f"Rows scanned (w/ dups):    {n_rows}")
    print(f"Unique (trial_id, phase):  {n_trials}")
    print(f"Inclusion items total:     {n_i}   (avg {n_i/n_trials:.2f}/trial)")
    print(f"Exclusion items total:     {n_e}   (avg {n_e/n_trials:.2f}/trial)")
    print(f"Trials with empty incl:    {n_empty_incl}")
    print(f"Trials with empty excl:    {n_empty_excl}")
    print(f"Wrote: {out_incl}  ({out_incl.stat().st_size/1e6:.1f} MB)")
    print(f"Wrote: {out_excl}  ({out_excl.stat().st_size/1e6:.1f} MB)")


if __name__ == "__main__":
    main()
