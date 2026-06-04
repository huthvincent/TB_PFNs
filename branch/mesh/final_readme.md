# branch/mesh — 终态文档（final_readme）

> 终态文档，cold-read 5 分钟拿结论。过程/踩坑/完整数字见 [`README.md`](README.md) §12。
> 进入本目录前先看 [`/data2/zhu11/TB/ReadMeFirst.md`](../../ReadMeFirst.md)；branch 规约见 [`../README.md`](../README.md)。

---

## 1. TL;DR

固定 TabICLv2，baseline = **tabular + I/E**（Qwen3 编 I/E）。把 **condition + intervention MeSH 作 2 个额外 virtual token**（共 4 token），5 个 encoder × **5 task × Phase 1–3** 全面评估（**§2 主结果**）。

- **MeSH 是小幅"锦上添花"，不是主力**：跨 15 个 task×phase，最强的 **BioLORD-2023** 平均才 +0.0105（win-rate 80%）；主力始终是 I/E（tabular→+I/E ≈ +0.076，见 aggregate branch）。
- **增益高度 task/phase 依赖**，集中在 **trial-duration Phase3**（所有 encoder 强正，BioLORD **+0.052**）和 **trial-failure-reason Phase2/3**（+0.02~+0.04）；SAE/mortality/Phase1 多在噪声内。
- **没有单一 encoder 全面最优**：综合最稳是 **BioLORD**；但 **SAE 专项**（多-seed + 配对 t，§3）里反而 **Qwen3-8B / MedCPT** 略好（Phase2 p<0.05）。encoder 该按 task 选。
- 量级整体小（多数 cell |Δ|<0.01，在单-seed 噪声内）；本表是单 seed 点估计，确有信号的格子建议补多-seed 坐实。

---

## 2. 全面 MeSH 评估（5 任务 × Phase 1–3）★ 主结果

固定 TabICLv2，**baseline = tabular + I/E**（Qwen3-Embedding-8B, 2 virtual token）。每个 MeSH 列把 **condition + intervention MeSH 作 2 个额外 virtual token**（共 4 token），用对应 embedding 编码。5 个 task × Phase 1–3，**单 seed**（seed=0），指标 = 末 5 eval-epoch primary metric 均值。Δ = MeSH − baseline（同 cell）。粗体 = 该行最佳 encoder。
数据：`results/mesh_grid_20260604_104310/grid.json`；脚本 `script/mesh_eval_grid.py`（in-process, I/E+MeSH 各加载一次）+ `script/render_grid.py`。

> ⚠️ **单 seed 点估计**。由前面多-seed 研究，本 setup 的 run-to-run 噪声底约 **±0.005–0.010**（binary/regression），所以 |Δ| < ~0.01 在噪声内 —— 看**跨 phase/task 的模式**，别抠单个 cell。

### serious-adverse-event (binary, ROC-AUC)

| Phase | baseline (tab+I/E) | +SapBERT Δ | +BioLORD Δ | +MedCPT Δ | +PubMedBERT Δ | +Qwen3-8B Δ |
|---|---|---|---|---|---|---|
| Phase1 | 0.8889 | -0.0113 | **+0.0056** | -0.0122 | -0.0120 | -0.0002 |
| Phase2 | 0.8652 | -0.0080 | -0.0114 | +0.0009 | +0.0013 | **+0.0026** |
| Phase3 | 0.8793 | +0.0068 | **+0.0192** | +0.0041 | -0.0004 | +0.0061 |

### mortality-event (binary, ROC-AUC)

| Phase | baseline (tab+I/E) | +SapBERT Δ | +BioLORD Δ | +MedCPT Δ | +PubMedBERT Δ | +Qwen3-8B Δ |
|---|---|---|---|---|---|---|
| Phase1 | 0.9187 | **+0.0119** | +0.0016 | +0.0094 | +0.0001 | -0.0171 |
| Phase2 | 0.8966 | -0.0083 | **+0.0028** | -0.0012 | +0.0003 | -0.0074 |
| Phase3 | 0.8723 | +0.0063 | -0.0050 | **+0.0114** | +0.0050 | +0.0024 |

### patient-dropout (binary, ROC-AUC)

| Phase | baseline (tab+I/E) | +SapBERT Δ | +BioLORD Δ | +MedCPT Δ | +PubMedBERT Δ | +Qwen3-8B Δ |
|---|---|---|---|---|---|---|
| Phase1 | 0.7102 | +0.0086 | +0.0044 | +0.0008 | -0.0092 | **+0.0166** |
| Phase2 | 0.7631 | **+0.0105** | +0.0054 | -0.0048 | -0.0010 | -0.0009 |
| Phase3 | 0.8313 | -0.0038 | +0.0095 | **+0.0119** | -0.0036 | -0.0134 |

### trial-duration (regression, R²)

| Phase | baseline (tab+I/E) | +SapBERT Δ | +BioLORD Δ | +MedCPT Δ | +PubMedBERT Δ | +Qwen3-8B Δ |
|---|---|---|---|---|---|---|
| Phase1 | 0.4786 | -0.0047 | **+0.0136** | -0.0079 | +0.0086 | -0.0119 |
| Phase2 | 0.2557 | +0.0034 | **+0.0081** | -0.0113 | -0.0005 | -0.0091 |
| Phase3 | 0.2264 | +0.0240 | **+0.0523** | +0.0283 | +0.0275 | +0.0406 |

### trial-failure-reason (multiclass, macro-F1)

| Phase | baseline (tab+I/E) | +SapBERT Δ | +BioLORD Δ | +MedCPT Δ | +PubMedBERT Δ | +Qwen3-8B Δ |
|---|---|---|---|---|---|---|
| Phase1 | 0.3347 | -0.0039 | -0.0043 | -0.0143 | -0.0088 | -0.0208 |
| Phase2 | 0.3438 | -0.0044 | +0.0219 | **+0.0295** | +0.0203 | +0.0195 |
| Phase3 | 0.3493 | **+0.0416** | +0.0341 | +0.0238 | +0.0016 | +0.0203 |

### 全局汇总（15 个 task×phase cell）

| Encoder | mean Δ | median Δ | win-rate (Δ>0) | #cells Δ>+0.01 | #cells Δ<−0.01 |
|---|---|---|---|---|---|
| SapBERT | +0.0046 | +0.0034 | 53% (8/15) | 4 | 1 |
| **BioLORD** | **+0.0105** | **+0.0056** | **80% (12/15)** | 5 | 1 |
| MedCPT | +0.0046 | +0.0009 | 60% (9/15) | 5 | 3 |
| PubMedBERT | +0.0019 | +0.0001 | 53% (8/15) | 2 | 1 |
| Qwen3-8B | +0.0018 | -0.0002 | 47% (7/15) | 4 | 4 |

### 结论（全面 grid）

1. **BioLORD-2023 综合最稳**：mean Δ **+0.0105**、win-rate **80% (12/15)**、5 个 cell 增益 >+0.01 而只有 1 个 < −0.01。是 5 个 encoder 里跨 task/phase 最一致正向的。
2. **MeSH 增益高度 task/phase 依赖**，集中在两处：
   - **trial-duration Phase3**：**所有** encoder 强正（BioLORD **+0.052**、Qwen3 +0.041、MedCPT +0.028、PubMedBERT +0.028、SapBERT +0.024）。低基线（R²≈0.23）+ 病种/药物显然跟试验时长相关 → MeSH 帮助最大。
   - **trial-failure-reason Phase2/3**：多数 encoder 正（MedCPT +0.030 P2、SapBERT +0.042 P3、BioLORD +0.034 P3）。
3. **Phase1 普遍弱或负**（小数据、噪声大、baseline 已高如 mortality 0.92 / SAE 0.89）。
4. **SAE / mortality 混合且小**（多在噪声内），印证 §3 的 SAE 专项结论。
5. **encoder 选择是 task-dependent**：综合选 **BioLORD**；但 SAE 上反而 Qwen3/MedCPT 略好（§3 多-seed 专项）。没有单一 encoder 全面碾压。
6. **整体量级仍小**（最强的 BioLORD 平均也才 +0.01，多数 cell 在噪声内）：MeSH 是"锦上添花"而非主力，主力是 I/E（见 §3 / aggregate branch：tabular→+I/E +0.0756）。

> 单 seed caveat：上表是点估计，|Δ|<~0.01 在噪声内。值得后续对**确有信号的格子**（trial-duration P3、failure-reason P2/3、BioLORD 整体）补多-seed + 配对 t 坐实。

---

## 3. SAE 专项：候选对比与多-seed 显著性

### 3.1 架构：4 个 virtual token

condition（疾病）和 intervention（药物）语义正交，分 2 个独立 token（跟 I/E 分开同理）：
`proj_incl + proj_excl + proj_cond + proj_interv`，col_emb(4, E=128)，可训练 ~1.25M（base TabICL 27.6M 全冻结）。

### 3.2 MeSH encoder（4 个全测，last5, n=10 Phase2, 配对 t vs B'）

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

### 3.3 vs SMILES branch

| 信号源 | Phase2 最佳 Δ (配对 p) | Phase3 | 结论 |
|---|---|---|---|
| SMILES（分子结构） | mol2vec +0.003 (n.s.) | 平/负 | 无稳健增益 |
| **MeSH（疾病+药物术语）** | **MedCPT +0.0046 full / +0.0073 子集 (p<0.05)** | 平 | Phase2 小幅稳健正 |

SAE 在 tabular+I/E 之外，缺的更多是**适应症/药物身份**（MeSH 摸到了）而非**分子结构**（SMILES 没摸到）。

---

## 4. 接入方式

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

## 5. 已知坑

1. **必须多-seed + 配对 t**：TabICL Full-Step-2 是 CUDA 非确定性的（best 单次噪声 ±0.009，last5 ±0.004~0.007）。MedCPT 的 +0.0046 只有靠 n=10 + 配对检验（同 seed 下 B'/C 共享数据采样，消掉采样方差）才能从噪声里分辨。**n=5 时 MedCPT p=0.052（边际），n=10 才坐实 p=0.039** —— 别用单次或小样本下结论。
2. **MeSH 两列在 `sae_finetune.preprocess` 的 `TEXT_DROP` 里**：encoding 必须从原始 `train_x.csv` 读。（`encode_mesh_hf.py` 已正确处理）
3. **MeSH 字段是 stringified list**（`"['Molgramostim', 'Sargramostim']"`）也可能是裸字符串：`ast.literal_eval` + 兜底。
4. **pooling 因 encoder 而异**：SapBERT/MedCPT 官方用 CLS，BioLORD/PubMedBERT 用 masked-mean。`encode_mesh_hf.py` 的 MODEL_REGISTRY 已按各自惯例配置；混用错 pooling 会显著降质。
5. **I/E 用 symlink 复用 smiles**：clone 后若 smiles branch 的 parquet 不在，需重新生成（见 §6）或改 `--ie-emb` 指向别处。

---

## 6. 关键实验数据

- 多-seed 完整表（last5/best/final, mean±std, Δ vs B'）：[`results/multiseed_20260602_023755/robust_summary.md`](results/multiseed_20260602_023755/robust_summary.md)
- 原始每-run 数据：`results/multiseed_20260602_023755/raw_runs.jsonl`（75 行 = B'+4enc × {P2 n=10, P3 n=5}）
- 各 run 训练 history：`results/full_step2_tabicl_mesh_*/metrics.json`
- 配对 t 检验复算：见 README §12（脚本可从 raw_runs.jsonl + 各 metrics.json 重算）

---

## 7. 复现命令

```bash
source /data2/zhu11/miniconda3/etc/profile.d/conda.sh && conda activate tabpfn
cd /data2/zhu11/TB/branch/mesh

# 1. I/E：复用 smiles 的 Qwen3 parquet（已 symlink）。若缺，先在 smiles branch 跑 encode_ie_qwen3.py

# === 全面 grid（§2 主结果）: 5 task × Phase1-3 × 6 cell ===
TASKS="serious-adverse-event-forecasting,mortality-event-prediction,patient-dropout-event-forecasting,trial-duration-forecasting,trial-failure-reason-identification"
# 2a. MeSH embedding 覆盖 5 个 task（--subtasks union；5 HF encoder + Qwen3）
for M in sapbert biolord medcpt pubmedbert; do python script/encode_mesh_hf.py --model $M --subtasks "$TASKS"; done
python script/encode_mesh_qwen3.py --subtasks "$TASKS"
# 2b. 跑 grid（单 seed, ~20 min）+ 渲染成表
python script/mesh_eval_grid.py
python script/render_grid.py            # 输出 §2 的 markdown 表

# === SAE 专项（§3）: 多-seed + 配对 t（只 SAE）===
for M in sapbert biolord medcpt pubmedbert; do python script/encode_mesh_hf.py --model $M; done   # SAE-only
python script/run_multiseed_mesh.py --phases Phase2,Phase3 --seeds 5 --epochs 30
python script/run_multiseed_mesh.py --phases Phase2 --seed-start 5 --seeds 5 --epochs 30 \
    --append-to results/multiseed_<那次的时间戳>
python script/aggregate_robust_mesh.py
```

env：`torch 2.9.1 / transformers 4.57.6 / tabicl 2.1.1 / scipy`（torchvision 已卸，见 smiles final_readme §4）。4 个 MeSH encoder 都是标准 HF BERT，首次自动下载（~440MB 各）。

---

## 8. 下一步建议 / 取舍

- **要不要纳入最终方案**：MedCPT MeSH 给 +0.005（full）~+0.007（intervention 子集），p<0.05，但只 Phase2、绝对量小、+1.25M 参数和一条 encoding pipeline 的复杂度。若追求极致指标可纳入（特别是 intervention 子集场景）；若要简洁，I+E 已是性价比最优，MeSH 边际收益不值复杂度。**建议：作为"可选增强"记录，默认方案不带。**
- **若继续**：(a) 只用 condition 或只用 intervention 单 token 消融，看增益来自哪列（数据提示 intervention 子集 Δ 更大 → 可能主要是药物 MeSH）；(b) MedCPT + 结构化药物属性（ATC/给药途径）联合；(c) 扩到其他 subtask（trial-approval / failure-reason 的 condition 信号可能比 SAE 更强）。
- **多-seed + 配对 t 协议**应推广到项目所有 Full-Step-2 实验（new_FM / IE_embedding 历史单次数严格说都该补误差棒）。

---

## 9. 关键产物索引

| 产物 | 路径 | 说明 |
|---|---|---|
| I/E（复用） | `data/ie_embeddings_qwen3.parquet` | symlink → smiles branch, d=4096, 全 trial |
| MeSH embedding ×5 | `data/mesh_embeddings_{sapbert,biolord,medcpt,pubmedbert,qwen3}.parquet` | d=768(×4)/4096(qwen3); 覆盖 5 task, 116,581 groups |
| MeSH encoding | `script/encode_mesh_hf.py` / `encode_mesh_qwen3.py` | `--model` / `--subtasks` (多任务 union) |
| 训练脚本 | `script/full_step2_tabicl_mesh.py` | 2 or 4 virt token; `--mesh-emb`/`--report-subset-mesh` |
| **全面 grid（§2 主结果）** | `script/mesh_eval_grid.py` + `render_grid.py` | in-process, 5 task×3 phase×6 cell, 单 seed |
| 全面 grid 结果 | `results/mesh_grid_20260604_104310/grid.json` | 90 cell raw |
| SAE 多-seed driver | `script/run_multiseed_mesh.py` | `--seed-start`/`--append-to`/`--cells` |
| SAE 稳健聚合 | `script/aggregate_robust_mesh.py` | last5/best/final mean±std + Δ vs B' |
| SAE 多-seed 结果（§3） | `results/multiseed_20260602_023755/` | summary / robust_summary / raw_runs.jsonl |
| 进度日志 | `README.md` §12 | 完整心路 + 配对 t + vs SMILES |
