"""Render the pairwise-association results into /data2/zhu11/TB/CI/association.md.

Reads from a results dir produced by ci_pairwise_association.py:
  pairwise_all.csv          (all 2628 pairs)
  pairwise_associated.csv   (1241 pairs passing threshold)
  metrics.json              (summary)

Writes a single self-contained markdown to /data2/zhu11/TB/CI/association.md.

Usage:
    /data2/zhu11/miniconda3/envs/tabpfn/bin/python \
        /data2/zhu11/TB/script/ci_render_association_md.py \
        [run_id_directory]

If run_id_directory is omitted, the latest ci_pairwise_association_* dir under
/data2/zhu11/TB/results/ is used.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

RESULTS_ROOT = Path("/data2/zhu11/TB/results")
OUT_PATH = Path("/data2/zhu11/TB/CI/association.md")


def find_latest_run() -> Path:
    candidates = sorted(
        RESULTS_ROOT.glob("ci_pairwise_association_*"),
        key=lambda p: p.name,
    )
    if not candidates:
        raise FileNotFoundError(f"No ci_pairwise_association_* run dirs under {RESULTS_ROOT}")
    return candidates[-1]


def fmt_p(p: float) -> str:
    if p == 0 or p < 1e-300:
        return "<1e-300"
    if p < 1e-4:
        return f"{p:.2e}"
    return f"{p:.4f}"


def fmt_eff(x: float) -> str:
    return f"{x:.3f}"


def render(run_dir: Path) -> str:
    metrics = json.loads((run_dir / "metrics.json").read_text())
    all_pairs = pd.read_csv(run_dir / "pairwise_all.csv")
    assoc = pd.read_csv(run_dir / "pairwise_associated.csv")

    n_total = len(all_pairs)
    n_assoc = len(assoc)
    n_indep = n_total - n_assoc

    # Per-feature partner index from the associated set
    # partners[feature] -> list of dicts {partner, effect, metric, p_adj, n_valid, via}
    partners: dict[str, list[dict]] = {}
    for _, r in assoc.iterrows():
        for a, b in ((r["col_a"], r["col_b"]), (r["col_b"], r["col_a"])):
            partners.setdefault(a, []).append(
                {
                    "partner": b,
                    "effect": float(r["effect_size"]),
                    "metric": r["metric"],
                    "p_adj": float(r["p_adj"]),
                    "n_valid": int(r["n_valid"]),
                }
            )
    for k in partners:
        partners[k].sort(key=lambda d: -d["effect"])

    # All 73 feature names (recover from all_pairs)
    all_feats = sorted(set(all_pairs["col_a"]) | set(all_pairs["col_b"]))

    out: list[str] = []
    out.append("# Pairwise Association Screen — TrialBench_joined")
    out.append("")
    out.append(
        f"This file records the result of a marginal-association screen across the "
        f"{metrics['n_retained']} retained columns of "
        f"`/data2/zhu11/TB/dataset/TrialBench_joined/Phase{{1,2,3,4}}.parquet` "
        f"(n = {metrics['data_rows']:,} rows, concatenated)."
    )
    out.append("")
    out.append(
        "**Why this exists.** If two columns are not statistically associated in the data "
        "(under faithfulness), they cannot be linked by a direct causal arrow. So this screen "
        "prunes the edge candidate set for the DAG: only column pairs that appear in the "
        "*Per-feature association partners* tables below are eligible for causal edges. "
        "Pairs not listed have already been ruled out at this stage."
    )
    out.append("")
    out.append("---")
    out.append("")
    out.append("## Summary")
    out.append("")
    out.append("| Quantity                                  | Value           |")
    out.append("|-------------------------------------------|-----------------|")
    out.append(f"| Rows in TrialBench_joined                 | {metrics['data_rows']:,}          |")
    out.append(f"| Columns in source parquet                 | {metrics['n_columns_in_data']}              |")
    out.append(f"| Columns excluded                          | {metrics['n_excluded']}              |")
    out.append(f"| **Columns retained (nodes)**              | **{metrics['n_retained']}**              |")
    out.append(f"| Pairs tested                              | {n_total:,}           |")
    out.append(f"| Pairs passing threshold (associated)      | {n_assoc:,} ({100*n_assoc/n_total:.1f}%)   |")
    out.append(f"| Pairs filtered as independent             | {n_indep:,} ({100*n_indep/n_total:.1f}%)   |")
    out.append(f"| Effect-size threshold                     | > {metrics['effect_size_threshold']}          |")
    out.append(f"| FDR-adjusted p-value threshold            | < {metrics['p_adj_threshold']}          |")
    out.append(f"| Run directory                             | `{run_dir}` |")
    out.append("")
    out.append("### Excluded columns")
    out.append("")
    out.append("| Column | Reason |")
    out.append("|--------|--------|")
    for col, reason in metrics.get("excluded", {}).items():
        out.append(f"| `{col}` | {reason} |")
    out.append("")
    out.append(
        "After exclusion, the remaining **{n} columns** are the canonical DAG nodes for the rest of the "
        "CI/ pipeline.".format(n=metrics['n_retained'])
    )
    out.append("")
    out.append("---")
    out.append("")
    out.append("## Method")
    out.append("")
    out.append(
        f"Each of the {metrics['n_retained']} retained columns is mapped to **exactly one** internal "
        "representation so it can enter a standard effect-size test. The analysis dimensionality equals "
        "the number of retained columns; there is no fan-out into multiple sub-features per column."
    )
    out.append("")
    out.append("| Column type | Representation | Tested as |")
    out.append("|-------------|----------------|-----------|")
    out.append("| Numeric / boolean | raw value | numeric |")
    out.append("| Low-cardinality string (≤50 unique non-null values) | raw string | categorical |")
    out.append("| Structured-text / multi-valued (`condition`, `intervention/intervention_name`, `icdcode`, `smiless`, `condition_browse/mesh_term`, `intervention_browse/mesh_term`, `location/facility/address/city`, `brief_title`, `intervention/intervention_type`) | `n_items` = token count (0 ⟺ NaN) | numeric |")
    out.append("| Date string (`start_date`, `completion_date`) | days since 2000-01-01 | numeric |")
    out.append("| Age string (`eligibility/{maximum,minimum}_age`, e.g. '65 Years', '6 Months', 'N/A') | parsed to years (numeric) | numeric |")
    out.append("")
    out.append(
        "These conversions are **mandatory** for the high-cardinality / non-tabular columns — "
        "applying `χ²` to a (thousands × 4) contingency table or running `Spearman` on raw date "
        "strings does not give valid statistics. The conversions intentionally discard token content "
        "(which specific disease, which specific drug); only `whether reported / how many` is tested. "
        "The richer semantic associations enter the DAG later via domain knowledge."
    )
    out.append("")
    out.append("Pairwise effect-size tests (all rescaled to [0, 1]):")
    out.append("")
    out.append("| Pair type | Effect size                                         | p-value      |")
    out.append("|-----------|-----------------------------------------------------|--------------|")
    out.append("| num × num | \\|Spearman ρ\\|                                       | Spearman      |")
    out.append("| cat × cat | Cramér's V = √(χ² / (n · (min(r,c) − 1)))            | χ² of contingency |")
    out.append("| num × cat | η = √η² from one-way ANOVA                          | F-test of ANOVA |")
    out.append("")
    out.append(
        f"p-values are BH-FDR-adjusted across all {n_total:,} tests. A pair is marked **associated** iff "
        f"`effect_size > {metrics['effect_size_threshold']}` AND `p_adj < {metrics['p_adj_threshold']}`. "
        "All pairs (including those filtered out) live in `pairwise_all.csv` under the run directory."
    )
    out.append("")
    out.append("---")
    out.append("")
    out.append("## Strongest associations (top 30)")
    out.append("")
    out.append("These are deterministic / definitional pairs (e.g., `biology_pass ↔ biology_fail`, "
               "`MaskingType-* ↔ study_design_info/masking`, duration unit conversions) plus the "
               "first tier of clear mechanistic links. They will all anchor edges in the DAG.")
    out.append("")
    out.append("| col_a | col_b | effect | metric | n_valid | p_adj |")
    out.append("|-------|-------|--------|--------|---------|-------|")
    for _, r in assoc.head(30).iterrows():
        out.append(
            f"| `{r['col_a']}` | `{r['col_b']}` | {fmt_eff(r['effect_size'])} | "
            f"{r['metric']} | {int(r['n_valid']):,} | {fmt_p(float(r['p_adj']))} |"
        )
    out.append("")
    out.append("---")
    out.append("")
    out.append("## Per-feature association partners")
    out.append("")
    out.append(
        f"For each of the {metrics['n_retained']} retained columns, this section lists every other column "
        f"it is associated with, sorted by effect size. Use this view when deciding causal direction for "
        f"that feature in its `{{feature}}.md`."
    )
    out.append("")

    no_partners = []
    for feat in all_feats:
        plist = partners.get(feat, [])
        if not plist:
            no_partners.append(feat)
            continue
        out.append(f"### `{feat}`   *(partners: {len(plist)})*")
        out.append("")
        out.append("| partner | effect | metric | n_valid | p_adj |")
        out.append("|---------|--------|--------|---------|-------|")
        for p in plist:
            out.append(
                f"| `{p['partner']}` | {fmt_eff(p['effect'])} | {p['metric']} | "
                f"{p['n_valid']:,} | {fmt_p(p['p_adj'])} |"
            )
        out.append("")

    if no_partners:
        out.append("### Features with zero associated partners")
        out.append("")
        for f in no_partners:
            n_uniq_note = ""
            if f == "study_type":
                n_uniq_note = " — constant `'Interventional'` across all 81,786 rows; no variance ⇒ no signal."
            out.append(f"- `{f}`{n_uniq_note}")
        out.append("")
        out.append(
            "These features cannot be DAG-linked to any other feature in this dataset (they would need "
            "either more data variance or external knowledge to support an edge)."
        )
        out.append("")

    out.append("---")
    out.append("")
    out.append("## Caveats")
    out.append("")
    out.append(
        "1. **Faithfulness assumption.** \"No association ⇒ no direct edge\" relies on faithfulness — "
        "i.e., no exact cancellation of multiple causal paths. Standard assumption in causal discovery."
    )
    out.append(
        "2. **Marginal, not conditional.** This is a *marginal* association screen. Two features can be "
        "marginally associated through a chain `X → Z → Y` even if `X` and `Y` are conditionally independent "
        "given `Z`. The pair set here is therefore an over-approximation of the direct-edge set; the second "
        "stage (domain knowledge for direction) further prunes via mediation."
    )
    out.append(
        "3. **Missing-data heterogeneity.** `n_valid` varies dramatically across pairs (e.g., `biology_pass` "
        "is missing in ~60% of rows). Low-`n_valid` pairs near the threshold should be read with caution."
    )
    out.append(
        "4. **High-cardinality columns are coarsened.** Specific tokens of `condition`, `intervention/intervention_name`, "
        "etc., are not used in this screen — only `n_items` (token count, with 0 ⟺ NaN). Their richer "
        "semantic associations enter the DAG via domain knowledge in stage 2."
    )
    out.append(
        "5. **Two columns dropped before this screen.** `study_type` is constant ('Interventional') across "
        "all 81,786 rows so contributes no association signal; `regulatory_pass` is definitionally identical "
        "(|ρ|=1.0) to `approval_outcome` on overlapping rows and was merged into `approval_outcome` as a "
        "single node. See the *Excluded columns* table above for the full exclusion list."
    )
    out.append("")
    return "\n".join(out)


def main() -> None:
    run_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else find_latest_run()
    print(f"Reading from {run_dir}")
    content = render(run_dir)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(content)
    print(f"Wrote {OUT_PATH} ({len(content):,} chars, {content.count(chr(10))+1} lines)")


if __name__ == "__main__":
    main()
