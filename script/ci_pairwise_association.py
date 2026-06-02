"""Pairwise association screen for TrialBench_joined columns.

Stage 1 of the CI / DAG pipeline. The user's claim: if two features have no
association in the data, they cannot be causally linked, so we can prune the
edge space before applying domain knowledge for causal direction.

For each pair of retained columns we report an effect size in [0, 1] and a
BH-FDR-adjusted p-value, then mark the pair as 'associated' iff
    effect_size > 0.05  AND  p_adj < 0.01.

Tests by dtype pair:
  - num x num : |Spearman rho|
  - cat x cat : Cramer's V (chi-square)
  - num x cat : eta (= sqrt(eta^2) from one-way ANOVA)

High-cardinality structured-text columns (condition, intervention_name,
icdcode, smiless, mesh_terms, city, brief_title, intervention_type) are
represented by two numeric sub-features (is_non_null, n_items). Date columns
are parsed to (is_non_null, days_since_epoch). Age strings ('65 Years',
'6 Months') are parsed to years. For each original-column pair, the reported
effect size is the max across the cross-product of sub-features.

Each retained original column is mapped to ONE sub-feature internally (the
representation it can be tested in: n_items for structured text, days for
dates, years for ages, raw value for boolean/numeric/low-card categorical).
The analysis dimensionality therefore equals the number of retained columns.

Outputs (per-run, /data2/zhu11/TB/results/<run_id>/):
  pairwise_all.csv           one row per retained-column pair (n_retained * (n_retained - 1) / 2)
  pairwise_associated.csv    subset passing effect_size > 0.05 AND FDR-p < 0.01
  metrics.json               run summary (counts, thresholds, exclusion reasons)
  log.txt                    captured stdout

Usage:
    /data2/zhu11/miniconda3/envs/tabpfn/bin/python \
        /data2/zhu11/TB/script/ci_pairwise_association.py
"""

from __future__ import annotations

import ast
import json
import warnings
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests

warnings.filterwarnings("ignore")

# ----------------------------------------------------------------------------
# Paths
# ----------------------------------------------------------------------------
DATA_ROOT = Path("/data2/zhu11/TB/dataset/TrialBench_joined")
RESULTS_ROOT = Path("/data2/zhu11/TB/results")
SCRIPT_NAME = Path(__file__).stem
RUN_ID = f"{SCRIPT_NAME}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
RESULTS_DIR = RESULTS_ROOT / RUN_ID
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# ----------------------------------------------------------------------------
# Thresholds (confirmed with user)
# ----------------------------------------------------------------------------
EFFECT_SIZE_THRESHOLD = 0.05
P_ADJ_THRESHOLD = 0.01

# ----------------------------------------------------------------------------
# Column policy (matches CI/DAG.json)
# ----------------------------------------------------------------------------
# Each entry maps column name -> short reason. Membership tests use the dict keys.
EXCLUDED_COLS_REASONS = {
    # 8 long free-text columns (decided 2026-05-11)
    "brief_summary/textblock":                            "free-text trial summary",
    "eligibility/criteria/textblock":                     "free-text eligibility criteria",
    "intervention/description":                           "free-text intervention description",
    "detailed_description/textblock":                     "free-text long description",
    "study_design_info/intervention_model_description":   "free-text annotation on intervention_model",
    "study_design_info/masking_description":              "free-text annotation on masking",
    "eligibility/gender_description":                     "free-text annotation on eligibility/gender",
    "keyword":                                            "free-text keyword list with no fixed vocabulary",
    # 2 user-decided exclusions after association screen (2026-05-12)
    "study_type":                                         "constant 'Interventional' in all 81786 rows; zero variance, zero associated partners",
    "regulatory_pass":                                    "identical (|rho|=1.0) to approval_outcome on 30683 overlapping rows; merged into approval_outcome as a single node",
}
EXCLUDED_COLS = set(EXCLUDED_COLS_REASONS.keys())

# High-cardinality structured-text columns -> (is_non_null, n_items)
STRUCT_TEXT_COLS = {
    "condition",
    "condition_browse/mesh_term",
    "icdcode",
    "intervention/intervention_name",
    "intervention_browse/mesh_term",
    "smiless",
    "location/facility/address/city",
    "brief_title",
    "intervention/intervention_type",
}

DATE_COLS = {"start_date", "completion_date"}
AGE_COLS = {"eligibility/maximum_age", "eligibility/minimum_age"}

LOW_CARD_CATEGORICAL_MAX = 50  # if non-listed string column has <= this many unique non-null values, treat as categorical

# ----------------------------------------------------------------------------
# Logging
# ----------------------------------------------------------------------------
LOG_LINES: list[str] = []


def log(msg: str) -> None:
    print(msg, flush=True)
    LOG_LINES.append(msg)


# ----------------------------------------------------------------------------
# Feature extraction
# ----------------------------------------------------------------------------
def count_tokens(x) -> int:
    """Count comma-separated tokens, handling python-list-repr strings."""
    if pd.isna(x):
        return 0
    s = str(x).strip()
    if s.startswith("[") and s.endswith("]"):
        try:
            v = ast.literal_eval(s)
            if isinstance(v, (list, tuple)):
                return len(v)
        except (ValueError, SyntaxError):
            pass
    return len([t for t in s.split(",") if t.strip()])


def parse_age_years(x):
    """'65 Years' -> 65.0,  '6 Months' -> 0.5,  'N/A' -> NaN."""
    if pd.isna(x):
        return np.nan
    s = str(x).strip()
    if s.upper() in ("N/A", "NA", "", "NONE"):
        return np.nan
    parts = s.split()
    try:
        val = float(parts[0])
    except (ValueError, IndexError):
        return np.nan
    if len(parts) < 2:
        return np.nan
    unit = parts[1].lower()
    if unit.startswith("year"):
        return val
    if unit.startswith("month"):
        return val / 12.0
    if unit.startswith("week"):
        return val / 52.18
    if unit.startswith("day"):
        return val / 365.25
    if unit.startswith("hour"):
        return val / (24 * 365.25)
    if unit.startswith("minute"):
        return val / (60 * 24 * 365.25)
    return np.nan


def parse_dates_to_days(series: pd.Series) -> np.ndarray:
    """Parse 'YYYY-MM-DD' or 'Month YYYY' or 'Month DD, YYYY' to days since 2000-01-01."""
    parsed = pd.to_datetime(series, errors="coerce", format="mixed")
    days = (parsed - pd.Timestamp("2000-01-01")).dt.days
    return days.astype(float).to_numpy()


def get_features(df: pd.DataFrame) -> dict[str, tuple[str, str, np.ndarray]]:
    """Return dict[orig_col -> (sub_name, role, np.ndarray)].

    Each retained original column is mapped to EXACTLY ONE sub-feature:
      - structured-text columns (multi-valued strings, high-cardinality codes, free text)
            -> token count `<col>__n_items` (numeric).
            Note: n_items == 0 iff the original cell is NaN, so n_items strictly
            dominates an is_non_null indicator.
      - date columns ('start_date', 'completion_date')
            -> `<col>__days`, days since 2000-01-01 (numeric, NaN if unparseable).
      - age columns (eligibility/{minimum,maximum}_age, formatted '65 Years' etc.)
            -> `<col>__years`, parsed to numeric years (NaN if unparseable).
      - boolean / numeric -> as-is.
      - low-cardinality string (<=50 unique non-null values) -> as-is, categorical.
      - any other high-cardinality string (not pre-listed) -> n_items fallback.

    role in {'num', 'cat'}. Numeric arrays are float with NaN for missing.
    Categorical arrays are object dtype with pd.NA / np.nan for missing.
    """
    out: dict[str, tuple[str, str, np.ndarray]] = {}
    for col in df.columns:
        if col in EXCLUDED_COLS:
            continue
        s = df[col]

        if col in STRUCT_TEXT_COLS:
            n_items = s.apply(count_tokens).astype(float).to_numpy()
            out[col] = (f"{col}__n_items", "num", n_items)
            continue
        if col in DATE_COLS:
            days = parse_dates_to_days(s)
            out[col] = (f"{col}__days", "num", days)
            continue
        if col in AGE_COLS:
            years = s.apply(parse_age_years).astype(float).to_numpy()
            out[col] = (f"{col}__years", "num", years)
            continue
        if pd.api.types.is_bool_dtype(s):
            v = s.astype("Float64").to_numpy(dtype=float, na_value=np.nan)
            out[col] = (col, "num", v)
            continue
        if pd.api.types.is_numeric_dtype(s):
            v = s.astype(float).to_numpy()
            out[col] = (col, "num", v)
            continue

        # remaining: string columns
        n_uniq = s.dropna().nunique()
        if n_uniq <= LOW_CARD_CATEGORICAL_MAX:
            cat_arr = s.astype("string").to_numpy()  # NaN preserved as pd.NA
            out[col] = (col, "cat", cat_arr)
        else:
            # high cardinality not listed in STRUCT_TEXT_COLS -> fallback to n_items
            n_items = s.apply(count_tokens).astype(float).to_numpy()
            out[col] = (f"{col}__n_items", "num", n_items)
    return out


# ----------------------------------------------------------------------------
# Effect-size tests
# ----------------------------------------------------------------------------
def spearman_pair(x: np.ndarray, y: np.ndarray) -> tuple[float, float, int]:
    """|rho|, p, n_valid for two numeric arrays."""
    mask = ~(np.isnan(x) | np.isnan(y))
    n = int(mask.sum())
    if n < 3:
        return np.nan, np.nan, n
    a, b = x[mask], y[mask]
    if np.std(a) == 0 or np.std(b) == 0:
        return 0.0, 1.0, n
    rho, p = stats.spearmanr(a, b)
    if np.isnan(rho):
        return 0.0, 1.0, n
    return float(abs(rho)), float(p), n


def _cat_mask(x: np.ndarray) -> np.ndarray:
    """Return boolean mask for non-missing categorical entries."""
    s = pd.Series(x)
    return s.notna().to_numpy()


def cramers_v_pair(x: np.ndarray, y: np.ndarray) -> tuple[float, float, int]:
    """Cramer's V, p, n_valid for two categorical arrays."""
    mask = _cat_mask(x) & _cat_mask(y)
    n = int(mask.sum())
    if n < 3:
        return np.nan, np.nan, n
    a = pd.Series(x)[mask].astype("string")
    b = pd.Series(y)[mask].astype("string")
    if a.nunique() < 2 or b.nunique() < 2:
        return 0.0, 1.0, n
    ct = pd.crosstab(a, b)
    if ct.size == 0 or ct.shape[0] < 2 or ct.shape[1] < 2:
        return 0.0, 1.0, n
    try:
        chi2, p, _dof, _exp = stats.chi2_contingency(ct, correction=False)
    except ValueError:
        return 0.0, 1.0, n
    denom = n * (min(ct.shape) - 1)
    if denom <= 0:
        return 0.0, 1.0, n
    v = float(np.sqrt(chi2 / denom))
    return min(v, 1.0), float(p), n


def eta_pair(num: np.ndarray, cat: np.ndarray) -> tuple[float, float, int]:
    """eta = sqrt(eta^2), p, n_valid for numeric vs categorical."""
    mask_n = ~np.isnan(num)
    mask_c = _cat_mask(cat)
    mask = mask_n & mask_c
    n = int(mask.sum())
    if n < 3:
        return np.nan, np.nan, n
    y = num[mask]
    g = pd.Series(cat)[mask].astype("string").to_numpy()
    levels = np.unique(g)
    if len(levels) < 2 or np.std(y) == 0:
        return 0.0, 1.0, n
    grand = float(np.mean(y))
    ss_total = float(np.sum((y - grand) ** 2))
    if ss_total <= 0:
        return 0.0, 1.0, n
    ss_between = 0.0
    groups = []
    for lv in levels:
        gy = y[g == lv]
        if len(gy) < 1:
            continue
        ss_between += len(gy) * (float(np.mean(gy)) - grand) ** 2
        groups.append(gy)
    eta2 = max(0.0, min(1.0, ss_between / ss_total))
    eta = float(np.sqrt(eta2))
    if len(groups) >= 2 and all(len(grp) >= 2 for grp in groups):
        try:
            _f, p = stats.f_oneway(*groups)
            if p is None or np.isnan(p):
                p = 1.0
        except (ValueError, FloatingPointError):
            p = 1.0
    else:
        p = 1.0
    return eta, float(p), n


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------
def main() -> None:
    log(f"=== ci_pairwise_association {datetime.now().isoformat()} ===")
    log(f"RUN_ID = {RUN_ID}")
    log(f"results -> {RESULTS_DIR}")

    log(f"Loading parquet files from {DATA_ROOT}")
    dfs = []
    for phase in ["Phase1", "Phase2", "Phase3", "Phase4"]:
        p = DATA_ROOT / f"{phase}.parquet"
        d = pd.read_parquet(p)
        log(f"  {phase}: shape={d.shape}")
        dfs.append(d)
    df = pd.concat(dfs, ignore_index=True)
    log(f"concat shape: {df.shape}")

    log("Extracting features (one sub-feature per retained original column) ...")
    feats = get_features(df)
    log(f"  retained columns: {len(feats)}")

    # Summarize role breakdown
    role_counts: dict[str, int] = {}
    for _, role, _ in feats.values():
        role_counts[role] = role_counts.get(role, 0) + 1
    log(f"  role mix: {role_counts}")
    log(f"  excluded columns: {len(EXCLUDED_COLS)} ({sorted(EXCLUDED_COLS)})")

    # Flatten to a stable-ordered list of (orig, sub_name, role, arr)
    flat: list[tuple[str, str, str, np.ndarray]] = []
    for orig, (name, role, arr) in feats.items():
        flat.append((orig, name, role, arr))

    n = len(flat)
    n_pairs = n * (n - 1) // 2
    log(f"Computing {n_pairs} column pairs ...")

    results: list[dict] = []
    for i in range(n):
        if i % 10 == 0:
            log(f"  progress: outer index {i}/{n}, results so far {len(results)}")
        orig_a, name_a, role_a, arr_a = flat[i]
        for j in range(i + 1, n):
            orig_b, name_b, role_b, arr_b = flat[j]
            if role_a == "num" and role_b == "num":
                eff, p, nv = spearman_pair(arr_a, arr_b)
                metric = "abs_spearman"
            elif role_a == "cat" and role_b == "cat":
                eff, p, nv = cramers_v_pair(arr_a, arr_b)
                metric = "cramers_v"
            elif role_a == "num" and role_b == "cat":
                eff, p, nv = eta_pair(arr_a, arr_b)
                metric = "eta"
            else:  # cat vs num
                eff, p, nv = eta_pair(arr_b, arr_a)
                metric = "eta"
            if np.isnan(eff):
                continue
            results.append(
                {
                    "col_a": orig_a,
                    "col_b": orig_b,
                    "sub_a": name_a,
                    "sub_b": name_b,
                    "role_a": role_a,
                    "role_b": role_b,
                    "metric": metric,
                    "effect_size": float(eff),
                    "p": float(p),
                    "n_valid": int(nv),
                }
            )

    log(f"Done. {len(results)} pair entries.")
    pair_df = pd.DataFrame(results)

    # Normalize ordering so (col_a, col_b) is alphabetically sorted, for stable output
    swap = pair_df["col_a"] > pair_df["col_b"]
    if swap.any():
        for a, b in [("col_a", "col_b"), ("sub_a", "sub_b"), ("role_a", "role_b")]:
            tmp = pair_df.loc[swap, a].copy()
            pair_df.loc[swap, a] = pair_df.loc[swap, b].to_numpy()
            pair_df.loc[swap, b] = tmp.to_numpy()

    # BH-FDR adjustment on p
    p_vals = pair_df["p"].fillna(1.0).to_numpy()
    _, p_adj, _, _ = multipletests(p_vals, method="fdr_bh")
    pair_df["p_adj"] = p_adj

    pair_df = pair_df.sort_values("effect_size", ascending=False).reset_index(drop=True)

    all_path = RESULTS_DIR / "pairwise_all.csv"
    pair_df.to_csv(all_path, index=False)
    log(f"Wrote {all_path} ({len(pair_df)} rows).")

    assoc_df = pair_df[
        (pair_df["effect_size"] > EFFECT_SIZE_THRESHOLD)
        & (pair_df["p_adj"] < P_ADJ_THRESHOLD)
    ].reset_index(drop=True)
    assoc_path = RESULTS_DIR / "pairwise_associated.csv"
    assoc_df.to_csv(assoc_path, index=False)
    log(f"Associated pairs (effect>{EFFECT_SIZE_THRESHOLD} AND FDR-p<{P_ADJ_THRESHOLD}): {len(assoc_df)} / {len(pair_df)}")

    metrics = {
        "run_id": RUN_ID,
        "data_rows": int(len(df)),
        "n_columns_in_data": int(df.shape[1]),
        "n_excluded": len(EXCLUDED_COLS),
        "excluded": EXCLUDED_COLS_REASONS,
        "n_retained": len(feats),
        "role_mix": role_counts,
        "n_pairs_tested": int(len(pair_df)),
        "n_associated_pairs": int(len(assoc_df)),
        "effect_size_threshold": EFFECT_SIZE_THRESHOLD,
        "p_adj_threshold": P_ADJ_THRESHOLD,
        "files": {
            "all_pairs": str(all_path),
            "associated_pairs": str(assoc_path),
        },
    }
    with open(RESULTS_DIR / "metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)
    log("metrics.json:")
    log(json.dumps(metrics, indent=2))

    with open(RESULTS_DIR / "log.txt", "w") as f:
        f.write("\n".join(LOG_LINES))


if __name__ == "__main__":
    main()
