#!/usr/bin/env python3
"""
ablation_search.py — Which virtual tokens, on top of TabICLv2, help SAE most?

In-process feature selection over the virtual-token pool. Loads every candidate
token source + bootstraps TabICL ONCE, then evaluates many token subsets cheaply
(each subset = new small projections + 30-epoch train, ~8s). This is the
efficient way to run hundreds of subset evals (the subprocess-per-run driver
reloaded ~1-5GB every run).

Token pool (each → 1 virtual feature column):
  base (always on): I, E            (Qwen3 4096, eligibility criteria)
  candidates:
    mesh_cond, mesh_interv          (MeSH terms, MedCPT 768 — mesh branch winner encoder)
    summary, title, condition, detail, interv_desc, interv_name, keyword,
        sd_interv_model, sd_masking (9 TrialBench text cols, Qwen3 4096)
    smiles                          (MolFormer 768)

Modes:
  --mode marginal : eval base and base+{c} for each candidate c; report Δ + paired t
  --mode greedy   : forward-greedy from base; each round add the candidate with the
                    largest mean last5 gain; stop when best gain ≤ --stop-eps or
                    --max-rounds reached

Metric: last5 = mean of last 5 eval-epoch test ROC-AUC (noise-robust; TabICL
Full-Step-2 is CUDA-nondeterministic). Multi-seed; paired by seed vs base.

Output: results/ablation_<mode>_<phase>_<ts>/{summary.md, raw.jsonl}
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F
from scipy import stats

sys.path.insert(0, "/data2/zhu11/TB/branch/aggregate/script")
from full_step2_tabicl_multi import (  # noqa: E402
    TabICLVirtualMulti, load_token_lookup, align, predict_full,
    build_sklearn_preprocessor, preprocess, load_split_generic, metrics_binary,
)

DEVICE = "cuda"
AGG = "/data2/zhu11/TB/branch/aggregate/data"
MESH = "/data2/zhu11/TB/branch/mesh/data"
RESULTS_ROOT = Path("/data2/zhu11/TB/branch/aggregate/results")

POOL_SPECS = {
    "I":               f"{AGG}/ie_embeddings_qwen3.parquet@I",
    "E":               f"{AGG}/ie_embeddings_qwen3.parquet@E",
    "mesh_cond":       f"{MESH}/mesh_embeddings_medcpt.parquet@condition",
    "mesh_interv":     f"{MESH}/mesh_embeddings_medcpt.parquet@intervention",
    "mesh_cond_q3":    f"{MESH}/mesh_embeddings_qwen3.parquet@condition",
    "mesh_interv_q3":  f"{MESH}/mesh_embeddings_qwen3.parquet@intervention",
    "summary":         f"{AGG}/emb_brief_summary_textblock_qwen.parquet",
    "title":           f"{AGG}/emb_brief_title_qwen.parquet",
    "condition":       f"{AGG}/emb_condition_qwen.parquet",
    "detail":          f"{AGG}/emb_detailed_description_textblock_qwen.parquet",
    "interv_desc":     f"{AGG}/emb_intervention_description_qwen.parquet",
    "interv_name":     f"{AGG}/emb_intervention_intervention_name_qwen.parquet",
    "keyword":         f"{AGG}/emb_keyword_qwen.parquet",
    "sd_interv_model": f"{AGG}/emb_study_design_info_intervention_model_description_qwen.parquet",
    "sd_masking":      f"{AGG}/emb_study_design_info_masking_description_qwen.parquet",
    "smiles":          f"{AGG}/smiles_embeddings_molformer.parquet",
}
BASE = ["I", "E"]
CANDIDATES = [k for k in POOL_SPECS if k not in BASE]


class PhaseData:
    """Everything needed to eval token subsets for one phase, prepared once."""
    def __init__(self, subtask, target, phase, echo):
        X_tr_df, y_tr = load_split_generic(subtask, "train", target, [phase])
        X_te_df, y_te = load_split_generic(subtask, "test", target, [phase])
        self.y_tr_int = y_tr.astype(int).values
        self.y_te_int = y_te.astype(int).values
        X_tr_p, X_te_p = preprocess(X_tr_df, X_te_df)
        sk = build_sklearn_preprocessor(X_tr_p)
        self.X_tr = torch.from_numpy(sk.fit_transform(X_tr_p).astype(np.float32))
        self.X_te = torch.from_numpy(sk.transform(X_te_p).astype(np.float32))
        self.y_tr_t = torch.from_numpy(self.y_tr_int.astype(np.int64))
        # align every pool token once
        self.tok = {}  # name -> (tr (n,d), te (m,d), d)
        for name, spec in POOL_SPECS.items():
            _, lk, d = load_token_lookup(spec)
            tr = align(X_tr_p, lk, d); te = align(X_te_p, lk, d)
            self.tok[name] = (tr, te, d)
        # bootstrap base once
        from tabicl import TabICLClassifier
        clf = TabICLClassifier(device=DEVICE, n_estimators=1, random_state=0, allow_auto_download=True)
        Xa = sk.transform(X_tr_p).astype(np.float32)
        n_init = min(50, len(Xa))
        idx = np.concatenate([np.where(self.y_tr_int == c)[0][:max(1, n_init // 2)] for c in (0, 1)])[:n_init]
        if len(idx) < 2:
            idx = np.arange(n_init)
        clf.fit(Xa[idx], self.y_tr_int[idx])
        self.base = clf.model_
        echo(f"  [{phase}] train={tuple(self.X_tr.shape)} test={tuple(self.X_te.shape)} "
             f"pos_rate={self.y_te_int.mean():.3f}")


def train_eval(pd_: PhaseData, names, seed, epochs=30, ctx=2000, qry=500,
               lr=1e-3, wd=1e-4, eval_every=2):
    """Train projections for token subset `names`, return last5 test ROC-AUC."""
    emb_dims = [pd_.tok[n][2] for n in names]
    virt_tr = [pd_.tok[n][0] for n in names]
    virt_te = [pd_.tok[n][1] for n in names]
    wrap = TabICLVirtualMulti(pd_.base, emb_dims).to(DEVICE)
    opt = torch.optim.AdamW([p for p in wrap.parameters() if p.requires_grad], lr=lr, weight_decay=wd)
    rng = np.random.RandomState(seed)
    n_train = pd_.X_tr.shape[0]
    hist = []
    for ep in range(epochs):
        wrap.train()
        perm = rng.permutation(n_train)
        ci = perm[:ctx]; qi = perm[ctx:ctx + qry]
        X_b = torch.cat([pd_.X_tr[ci], pd_.X_tr[qi]], 0).unsqueeze(0).to(DEVICE)
        y_b = pd_.y_tr_t[ci].float().unsqueeze(0).to(DEVICE)
        vb = [torch.from_numpy(np.concatenate([vt[ci], vt[qi]], 0)).to(DEVICE) for vt in virt_tr]
        tgt = pd_.y_tr_t[qi].long().to(DEVICE)
        out = wrap(X_b, y_b, vb)
        loss = F.cross_entropy(out[0, :, :2], tgt)
        opt.zero_grad(); loss.backward(); opt.step()
        if (ep + 1) % eval_every == 0 or ep == epochs - 1:
            wrap.eval()
            with torch.no_grad():
                proba = predict_full(wrap, pd_.X_tr, pd_.y_tr_t, pd_.X_te, virt_tr, virt_te, 2)
            hist.append(metrics_binary(pd_.y_te_int, proba)["roc_auc"])
    del wrap
    torch.cuda.empty_cache()
    return float(np.mean(hist[-5:]))


def agg(v):
    v = np.array(v, float)
    return {"mean": float(v.mean()), "std": float(v.std(ddof=1)) if len(v) > 1 else 0.0, "n": len(v)}


def main(args):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = RESULTS_ROOT / f"ablation_{args.mode}_{args.phase}_{ts}"
    out_dir.mkdir(parents=True, exist_ok=True)
    log_f = open(out_dir / "log.txt", "w"); raw_f = open(out_dir / "raw.jsonl", "w")

    def echo(*p):
        line = " ".join(str(x) for x in p); print(line, flush=True); print(line, file=log_f, flush=True)

    echo(f"[ablation] mode={args.mode} phase={args.phase} seeds={args.seeds} epochs={args.epochs}")
    echo("Preparing phase data (load tokens + bootstrap once) ...")
    t0 = time.time()
    pd_ = PhaseData(args.subtask, args.target, args.phase, echo)
    seeds = list(range(args.seeds))
    cache = {}  # frozenset(names) -> {seed: last5}

    def evalset(names):
        key = tuple(names)
        if key not in cache:
            cache[key] = {}
        for s in seeds:
            if s not in cache[key]:
                cache[key][s] = train_eval(pd_, list(names), s, epochs=args.epochs)
                raw_f.write(json.dumps({"names": list(names), "seed": s, "last5": cache[key][s]}) + "\n")
                raw_f.flush()
        return [cache[key][s] for s in seeds]

    echo(f"Setup done in {time.time()-t0:.0f}s. base={BASE}")
    base_vals = evalset(BASE)
    ba = agg(base_vals)
    echo(f"\nBASE (I+E) last5 = {ba['mean']:.4f} ± {ba['std']:.4f} (n={ba['n']})")

    lines = [f"# Ablation ({args.mode}, {args.phase}) — last5 ROC-AUC, n={args.seeds} seeds", "",
             f"BASE (I+E): {ba['mean']:.4f} ± {ba['std']:.4f}", ""]

    if args.mode == "marginal":
        echo("\n=== Marginal gain of each candidate over I+E ===")
        rows = []
        for c in CANDIDATES:
            vals = evalset(BASE + [c])
            a = agg(vals)
            d = np.array(vals) - np.array(base_vals)
            t, p = stats.ttest_rel(vals, base_vals)
            rows.append((c, a["mean"], a["std"], float(d.mean()), float(t), float(p)))
            echo(f"  +{c:16} {a['mean']:.4f} ± {a['std']:.4f}  Δ={d.mean():+.4f}  p={p:.3f}")
        rows.sort(key=lambda r: -r[3])
        lines += ["| + token | last5 | Δ vs I+E | paired t | p |", "|---|---|---|---|---|"]
        for c, m, s, dd, t, p in rows:
            sig = "***" if p < 0.01 else "**" if p < 0.05 else "*" if p < 0.1 else ""
            lines.append(f"| {c} | {m:.4f} ± {s:.4f} | {dd:+.4f} | {t:+.2f} | {p:.3f} {sig} |")
        lines.append("")

    elif args.mode == "fixed":
        echo("\n=== Fixed subsets vs I+E ===")
        subsets = [[s.strip() for s in grp.split(",") if s.strip()]
                   for grp in args.subsets.split(";") if grp.strip()]
        lines += ["| subset (on top of I+E) | size | last5 | Δ vs I+E | paired t | p |",
                  "|---|---|---|---|---|---|"]
        for extra in subsets:
            names = BASE + extra
            vals = evalset(names)
            a = agg(vals)
            d = np.array(vals) - np.array(base_vals)
            t, p = stats.ttest_rel(vals, base_vals)
            sig = "***" if p < 0.01 else "**" if p < 0.05 else "*" if p < 0.1 else ""
            label = "+".join(extra) if extra else "(none = I+E)"
            echo(f"  {label:40} {a['mean']:.4f} ± {a['std']:.4f}  Δ={d.mean():+.4f}  p={p:.3f} {sig}")
            lines.append(f"| {label} | {len(names)} | {a['mean']:.4f} ± {a['std']:.4f} | "
                         f"{d.mean():+.4f} | {t:+.2f} | {p:.3f} {sig} |")
        lines.append("")

    elif args.mode == "greedy":
        echo("\n=== Forward greedy from I+E ===")
        current = list(BASE)
        cur_vals = base_vals
        remaining = list(CANDIDATES)
        path = [("I+E", agg(base_vals)["mean"], 0.0, 1.0)]
        lines += ["| step | added | subset size | last5 | Δ | p |", "|---|---|---|---|---|---|"]
        lines.append(f"| 0 | (I+E) | 2 | {agg(base_vals)['mean']:.4f} | — | — |")
        for rnd in range(args.max_rounds):
            best = None
            for c in remaining:
                vals = evalset(current + [c])
                d = float(np.mean(np.array(vals) - np.array(cur_vals)))
                t, p = stats.ttest_rel(vals, cur_vals)
                if best is None or d > best[1]:
                    best = (c, d, float(p), vals, agg(vals)["mean"])
            c, d, p, vals, mean = best
            echo(f"  round {rnd+1}: best=+{c}  Δ={d:+.4f}  p={p:.3f}  → mean={mean:.4f}")
            sig = "***" if p < 0.01 else "**" if p < 0.05 else "*" if p < 0.1 else ""
            lines.append(f"| {rnd+1} | +{c} | {len(current)+1} | {mean:.4f} | {d:+.4f} | {p:.3f} {sig} |")
            if d <= args.stop_eps:
                echo(f"  STOP: best gain {d:+.4f} ≤ stop-eps {args.stop_eps}")
                lines.append(f"\n**Stopped**: best round gain {d:+.4f} ≤ stop-eps {args.stop_eps}. "
                             f"Selected subset: {current} (size {len(current)}).")
                break
            current.append(c); cur_vals = vals; remaining.remove(c)
            path.append((c, mean, d, p))
        else:
            lines.append(f"\nReached max-rounds. Final subset: {current}")
        echo(f"\nGreedy selected: {current}")

    (out_dir / "summary.md").write_text("\n".join(lines))
    echo("\n" + "\n".join(lines))
    echo(f"\nSaved: {out_dir/'summary.md'}")
    log_f.close(); raw_f.close()


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--mode", choices=["marginal", "greedy", "fixed"], default="marginal")
    p.add_argument("--subsets", default="",
                   help="fixed mode: ';'-separated groups, each a comma-list of token names "
                        "to add on top of I+E. e.g. 'title;title,mesh_interv;mesh_cond,mesh_interv'")
    p.add_argument("--phase", required=True, choices=["Phase2", "Phase3"])
    p.add_argument("--subtask", default="serious-adverse-event-forecasting")
    p.add_argument("--target", default="Y/N")
    p.add_argument("--seeds", type=int, default=5)
    p.add_argument("--epochs", type=int, default=30)
    p.add_argument("--max-rounds", type=int, default=5)
    p.add_argument("--stop-eps", type=float, default=0.0,
                   help="greedy stops when best round gain ≤ this (default 0: stop when no positive gain)")
    args = p.parse_args()
    main(args)
