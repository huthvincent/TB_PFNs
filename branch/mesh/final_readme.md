# branch/mesh — 终态文档（final_readme）

> 终态文档，cold-read 5 分钟拿结论。过程/踩坑/完整数字见 [`README.md`](README.md) §12。
> 进入本目录前先看 [`/data2/zhu11/TB/ReadMeFirst.md`](../../ReadMeFirst.md)；branch 规约见 [`../README.md`](../README.md)。

---

## 1. TL;DR

**在 TabICLv2 + I/E 之上，把 condition + intervention MeSH 术语作 2 个额外 virtual token（共 4 token），在 SAE 上：Qwen3-8B 和 MedCPT 编码的 MeSH 都在 Phase2 给出小幅但统计显著的正增益（Qwen3 full +0.0058 p=0.049 / 子集 +0.0086 p=0.019；MedCPT full +0.0046 p=0.039 / 子集 +0.0073 p=0.015；n=10 配对 t）；Phase3 全部无效；SapBERT/PubMedBERT 不显著。**

- **这是 SMILES + MeSH 两条 branch 里唯一稳健显著的正信号。**
- **5 个 encoder 里 Qwen3-Embedding-8B (4096-d) 最强**，略胜生物医学专用的 MedCPT (768-d)。即通用强 embedding 在 MeSH 受控术语上不输甚至优于领域专用 encoder——之前"专用打败通用"的猜测被推翻（注：Qwen3 是 2026-06-02 补测的，初版只测了 4 个生物医学 encoder）。
- 增益绝对量小（~+0.006）且不跨 phase 稳定 → 纳不纳入最终方案见 §7 取舍。

---

## 2. 候选对比

### 2.1 架构：4 个 virtual token

condition（疾病）和 intervention（药物）语义正交，分 2 个独立 token（跟 I/E 分开同理）：
`proj_incl + proj_excl + proj_cond + proj_interv`，col_emb(4, E=128)，可训练 ~1.25M（base TabICL 27.6M 全冻结）。

### 2.2 MeSH encoder（4 个全测，last5, n=10 Phase2, 配对 t vs B'）

| Encoder | HF | dim/pool | Phase2 full Δ (p) | Phase2 interv-subset Δ (p) | 判定 |
|---|---|---|---|---|---|
| **Qwen3-8B** | `Qwen/Qwen3-Embedding-8B` | 4096/last-tok | **+0.0058 (0.049**)** | **+0.0086 (0.019**)** | **最强** |
| **MedCPT** | `ncbi/MedCPT-Article-Encoder` | 768/CLS | **+0.0046 (0.039**)** | **+0.0073 (0.015**)** | **显著正** |
| BioLORD-2023 | `FremyCompany/BioLORD-2023` | 768/mean | +0.0031 (0.096) | +0.0016 (0.47) | 边际 |
| PubMedBERT | `microsoft/BiomedNLP-BiomedBERT-...` | 768/mean | +0.0016 (0.52) | +0.0037 (0.27) | 不显著 |
| SapBERT | `cambridgeltl/SapBERT-from-PubMedBERT` | 768/CLS | −0.0001 (0.97) | +0.0022 (0.63) | 不显著 |

Phase3（n=5）：全部不显著（最小 p=0.34），平。Qwen3 也是 full −0.0006 (p=0.91)。

**为什么 Qwen3 / MedCPT 赢、SapBERT / BioLORD 不行**：对 SAE 有用的是"这个病/这个药在文献里跟什么不良事件共现"。Qwen3（大规模通用语义）和 MedCPT（PubMed query-article 对比）都抓得住这种文献/语义共现；SapBERT（UMLS 同义词对比）和 BioLORD（概念定义对比）优化的是实体规范化/同义判定，跟本任务不对口。通用强 embedding (Qwen3) 在 MeSH 受控术语上**不输领域专用**，且跟项目统一 Qwen3 栈。

#### SAE Phase 2 — MeSH 2-token performance vs baseline (English summary)

Architecture: frozen TabICLv2. **Baseline = tabular + I/E (2 virtual tokens).** Each MeSH
row adds condition + intervention MeSH as **2 extra virtual tokens** (4 total), encoded by
the listed embedding model. Metric: last5 test ROC-AUC (mean of last-5 eval epochs),
mean ± std over **n=10 seeds**; Δ = paired t-test vs baseline.

| MeSH embedding (condition + intervention, 2 virtual tokens) | Dim | Phase 2 ROC-AUC | Δ vs baseline (p) |
|---|---|---|---|
| **Baseline (tabular + I/E, no MeSH)** | — | 0.8594 ± 0.0060 | — |
| Qwen3-Embedding-8B | 4096 | **0.8652 ± 0.0058** | **+0.0058 (p=0.049)** |
| MedCPT-Article-Encoder | 768 | 0.8640 ± 0.0052 | +0.0046 (p=0.039) |
| BioLORD-2023 | 768 | 0.8625 ± 0.0060 | +0.0031 (p=0.096) |
| PubMedBERT | 768 | 0.8610 ± 0.0055 | +0.0016 (p=0.524) |
| SapBERT | 768 | 0.8593 ± 0.0068 | −0.0001 (p=0.970) |

### 2.3 vs SMILES branch

| 信号源 | Phase2 最佳 Δ (配对 p) | Phase3 | 结论 |
|---|---|---|---|
| SMILES（分子结构） | mol2vec +0.003 (n.s.) | 平/负 | 无稳健增益 |
| **MeSH（疾病+药物术语）** | **MedCPT +0.0046 full / +0.0073 子集 (p<0.05)** | 平 | Phase2 小幅稳健正 |

SAE 在 tabular+I/E 之外，缺的更多是**适应症/药物身份**（MeSH 摸到了）而非**分子结构**（SMILES 没摸到）。

---

## 3. 接入方式

```bash
# Cell B' (+I+E only, 2 token)
python script/full_step2_tabicl_mesh.py --phase Phase2 --epochs 30 --seed 0
# Cell C (+I+E+condition+intervention, 4 token)
python script/full_step2_tabicl_mesh.py --phase Phase2 --epochs 30 --seed 0 \
    --mesh-emb data/mesh_embeddings_medcpt.parquet
# Cell B' 但报 intervention 子集指标（不注入 MeSH，仅 mask）
python script/full_step2_tabicl_mesh.py --phase Phase2 --epochs 30 --seed 0 \
    --report-subset-mesh data/mesh_embeddings_medcpt.parquet
```

- `--ie-emb` 默认指向 `data/ie_embeddings_qwen3.parquet`（symlink 到 smiles branch 的 Qwen3 I/E）。
- d_ie / d_mesh 从 parquet 自动探测；换 encoder 只改 `--mesh-emb` 路径。
- MeSH parquet 格式：`trial_id, phase, type∈{condition,intervention}, mean_emb, n_terms`。

---

## 4. 已知坑

1. **必须多-seed + 配对 t**：TabICL Full-Step-2 是 CUDA 非确定性的（best 单次噪声 ±0.009，last5 ±0.004~0.007）。MedCPT 的 +0.0046 只有靠 n=10 + 配对检验（同 seed 下 B'/C 共享数据采样，消掉采样方差）才能从噪声里分辨。**n=5 时 MedCPT p=0.052（边际），n=10 才坐实 p=0.039** —— 别用单次或小样本下结论。
2. **MeSH 两列在 `sae_finetune.preprocess` 的 `TEXT_DROP` 里**：encoding 必须从原始 `train_x.csv` 读。（`encode_mesh_hf.py` 已正确处理）
3. **MeSH 字段是 stringified list**（`"['Molgramostim', 'Sargramostim']"`）也可能是裸字符串：`ast.literal_eval` + 兜底。
4. **pooling 因 encoder 而异**：SapBERT/MedCPT 官方用 CLS，BioLORD/PubMedBERT 用 masked-mean。`encode_mesh_hf.py` 的 MODEL_REGISTRY 已按各自惯例配置；混用错 pooling 会显著降质。
5. **I/E 用 symlink 复用 smiles**：clone 后若 smiles branch 的 parquet 不在，需重新生成（见 §6）或改 `--ie-emb` 指向别处。

---

## 5. 关键实验数据

- 多-seed 完整表（last5/best/final, mean±std, Δ vs B'）：[`results/multiseed_20260602_023755/robust_summary.md`](results/multiseed_20260602_023755/robust_summary.md)
- 原始每-run 数据：`results/multiseed_20260602_023755/raw_runs.jsonl`（75 行 = B'+4enc × {P2 n=10, P3 n=5}）
- 各 run 训练 history：`results/full_step2_tabicl_mesh_*/metrics.json`
- 配对 t 检验复算：见 README §12（脚本可从 raw_runs.jsonl + 各 metrics.json 重算）

---

## 6. 复现命令

```bash
source /data2/zhu11/miniconda3/etc/profile.d/conda.sh && conda activate tabpfn
cd /data2/zhu11/TB/branch/mesh

# 1. I/E：复用 smiles 的 Qwen3 parquet（已 symlink）。若缺，先在 smiles branch 跑 encode_ie_qwen3.py
# 2. MeSH embedding（4 encoder，每个 ~3s）
for M in sapbert biolord medcpt pubmedbert; do python script/encode_mesh_hf.py --model $M; done
# 3. 多-seed（Phase2/3 × 5 seed = 50 run），再给 Phase2 补 5 seed 到 n=10
python script/run_multiseed_mesh.py --phases Phase2,Phase3 --seeds 5 --epochs 30
python script/run_multiseed_mesh.py --phases Phase2 --seed-start 5 --seeds 5 --epochs 30 \
    --append-to results/multiseed_<那次的时间戳>
python script/aggregate_robust_mesh.py
```

env：`torch 2.9.1 / transformers 4.57.6 / tabicl 2.1.1 / scipy`（torchvision 已卸，见 smiles final_readme §4）。4 个 MeSH encoder 都是标准 HF BERT，首次自动下载（~440MB 各）。

---

## 7. 下一步建议 / 取舍

- **要不要纳入最终方案**：MedCPT MeSH 给 +0.005（full）~+0.007（intervention 子集），p<0.05，但只 Phase2、绝对量小、+1.25M 参数和一条 encoding pipeline 的复杂度。若追求极致指标可纳入（特别是 intervention 子集场景）；若要简洁，I+E 已是性价比最优，MeSH 边际收益不值复杂度。**建议：作为"可选增强"记录，默认方案不带。**
- **若继续**：(a) 只用 condition 或只用 intervention 单 token 消融，看增益来自哪列（数据提示 intervention 子集 Δ 更大 → 可能主要是药物 MeSH）；(b) MedCPT + 结构化药物属性（ATC/给药途径）联合；(c) 扩到其他 subtask（trial-approval / failure-reason 的 condition 信号可能比 SAE 更强）。
- **多-seed + 配对 t 协议**应推广到项目所有 Full-Step-2 实验（new_FM / IE_embedding 历史单次数严格说都该补误差棒）。

---

## 8. 关键产物索引

| 产物 | 路径 | 说明 |
|---|---|---|
| I/E（复用） | `data/ie_embeddings_qwen3.parquet` | symlink → smiles branch, d=4096 |
| MeSH embedding ×4 | `data/mesh_embeddings_{sapbert,biolord,medcpt,pubmedbert}.parquet` | d=768, 28,750 groups |
| MeSH encoding | `script/encode_mesh_hf.py` | `--model` switch, 4 encoder |
| 训练脚本 | `script/full_step2_tabicl_mesh.py` | 2 or 4 virt token; `--mesh-emb`/`--report-subset-mesh` |
| 多-seed driver | `script/run_multiseed_mesh.py` | `--seed-start`/`--append-to` 支持增量加 seed |
| 稳健聚合 | `script/aggregate_robust_mesh.py` | last5/best/final mean±std + Δ vs B' |
| 最终结果 | `results/multiseed_20260602_023755/` | summary / robust_summary / raw_runs.jsonl |
| 进度日志 | `README.md` §12 | 完整心路 + 配对 t + vs SMILES |
