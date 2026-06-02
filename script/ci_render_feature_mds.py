"""ci_render_feature_mds.py — Stage 2 renderer.

Reads /data2/zhu11/TB/CI/DAG.json (produced by ci_build_dag.py) and writes
one markdown file per node under
/data2/zhu11/TB/CI/individual_col_description/{feature}.md.

For each node F, the markdown lists every other column that is associated
with F (per the screen in association.md), classified into three sections:

  ## Causes (direct parents of F)
  ## Effects (direct children of F)
  ## Associated but no direct causal edge

Each entry shows the partner, the association effect size from Stage 1, and
the mechanism + rationale (for causes / effects) or the reason (for no_direct)
from Stage 2.

Filename convention (matches DAG.json `filename_convention`):
    '/' -> '__'
    ' ' -> '_'
    '(' / ')' removed
"""

from __future__ import annotations

import json
from pathlib import Path

DAG_PATH = Path("/data2/zhu11/TB/CI/DAG.json")
OUT_DIR = Path("/data2/zhu11/TB/CI/individual_col_description")


def to_filename(col: str) -> str:
    return (
        col.replace("/", "__")
           .replace(" ", "_")
           .replace("(", "")
           .replace(")", "")
    ) + ".md"


def fmt_eff(x: float) -> str:
    return f"{x:.3f}"


def render_feature(
    feat: str,
    node: dict,
    causes: list[dict],
    effects: list[dict],
    no_direct: list[dict],
    n_associated_total: int,
) -> str:
    out: list[str] = []
    out.append(f"# {feat}")
    out.append("")
    out.append(f"- **Group:** `{node['group']}`")
    out.append(f"- **Dtype:** {node['dtype']}")
    out.append(f"- **Description:** {node['description']}")
    out.append(f"- **Associated partners (from `association.md`):** {n_associated_total}")
    out.append(f"  - Direct **causes** (parents of this feature): **{len(causes)}**")
    out.append(f"  - Direct **effects** (children of this feature): **{len(effects)}**")
    out.append(f"  - Associated but **no direct** causal edge: **{len(no_direct)}**")
    out.append("")
    out.append(
        "This per-feature file enumerates only **associated** partners. "
        "All other columns in `DAG.json` were ruled independent in the Stage-1 "
        "association screen and do not appear here. See `association.md` for the screen."
    )
    out.append("")
    out.append("---")
    out.append("")

    def section(title: str, items: list[dict], kind: str) -> None:
        out.append(f"## {title} ({len(items)})")
        out.append("")
        if not items:
            out.append("_(none)_")
            out.append("")
            return
        for it in items:
            partner = it["partner"]
            out.append(f"### `{partner}`")
            out.append("")
            out.append(f"- **Association:** effect = {fmt_eff(it['effect_size'])} ({it['metric']}), n_valid = {it['n_valid']:,}")
            if kind in ("cause", "effect"):
                out.append(f"- **Mechanism:** `{it['mechanism']}`")
                out.append(f"- **Provenance:** {it['provenance']}")
                out.append("")
                out.append(it["rationale"])
            else:
                out.append(f"- **Provenance:** {it['provenance']}")
                out.append("")
                out.append(it["reason"])
            out.append("")

    section("Direct causes", causes, "cause")
    out.append("---")
    out.append("")
    section("Direct effects", effects, "effect")
    out.append("---")
    out.append("")
    section("Associated but no direct causal edge", no_direct, "no_direct")
    return "\n".join(out)


def main() -> None:
    dag = json.loads(DAG_PATH.read_text())
    nodes = {n["id"]: n for n in dag["nodes"]}

    # Build per-feature index
    causes: dict[str, list[dict]] = {n: [] for n in nodes}
    effects: dict[str, list[dict]] = {n: [] for n in nodes}
    no_direct: dict[str, list[dict]] = {n: [] for n in nodes}

    for e in dag["edges"]:
        src, tgt = e["src"], e["tgt"]
        # parent -> child
        # for the child: src is a cause
        causes[tgt].append({
            "partner": src,
            "mechanism": e["mechanism"],
            "rationale": e["rationale"],
            "effect_size": e["effect_size"],
            "metric": e["metric"],
            "n_valid": e["n_valid"],
            "provenance": e["provenance"],
        })
        # for the parent: tgt is an effect
        effects[src].append({
            "partner": tgt,
            "mechanism": e["mechanism"],
            "rationale": e["rationale"],
            "effect_size": e["effect_size"],
            "metric": e["metric"],
            "n_valid": e["n_valid"],
            "provenance": e["provenance"],
        })

    for nd in dag["associated_no_direct"]:
        a, b = nd["a"], nd["b"]
        for x, y in ((a, b), (b, a)):
            no_direct[x].append({
                "partner": y,
                "reason": nd["reason"],
                "effect_size": nd["effect_size"],
                "metric": nd["metric"],
                "n_valid": nd["n_valid"],
                "provenance": nd["provenance"],
            })

    # Sort by effect_size desc within each section
    for d in (causes, effects, no_direct):
        for k in d:
            d[k].sort(key=lambda x: -x["effect_size"])

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    written = 0
    for feat, node in nodes.items():
        c = causes[feat]
        ef = effects[feat]
        nd = no_direct[feat]
        n_total = len(c) + len(ef) + len(nd)
        content = render_feature(feat, node, c, ef, nd, n_total)
        out_path = OUT_DIR / to_filename(feat)
        out_path.write_text(content)
        written += 1

    print(f"[ok] wrote {written} per-feature .md files under {OUT_DIR}")
    # Brief summary
    print("\n=== per-feature edge counts ===")
    print(f"{'feature':<50} {'causes':>7} {'effects':>8} {'no_dir':>7} {'total':>6}")
    for feat in nodes:
        c, ef, nd = len(causes[feat]), len(effects[feat]), len(no_direct[feat])
        print(f"{feat:<50} {c:>7} {ef:>8} {nd:>7} {c+ef+nd:>6}")


if __name__ == "__main__":
    main()
