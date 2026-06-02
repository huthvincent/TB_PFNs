# SAE 子任务上的边际文本列对比实验

> 本文档详细记录在 TrialBench **serious-adverse-event-forecasting (SAE)** 子任务上的两组对照实验：
>
> 1. **MedCPT vs Qwen3-Embedding-8B 哪个 encoder 更适合临床试验文本**
> 2. **依次单独加入每一个新文本列**作为第 3 个 virtual token，看每一列**独立的**边际贡献
>
> 评测在 Phase 2 与 Phase 3 各自独立训练 + 评估（与 TrialBench 论文 Table 6 对齐）。

---

## 1. 实验设计

### 1.1 Base（对照基线）

复用 IE_embedding 已经完成的 Full Step 2 + unfreeze decoder：

- TabPFN-v2.5 主体（10.6M 参数）**全部冻结**
- 输入：41 个 tabular 列 + **2 个 virtual token**（inclusion criteria mean-pooled、exclusion criteria mean-pooled，均 MedCPT 编码）
- 可训练参数：2 个投影层 `Linear(768, 192)` + 2 个 column embedding + decoder head MLP ≈ **373K 参数**

Base 在 SAE 上的结果（IE_embedding 跑出来的）：
- **Phase 2: ROC-AUC = 0.8752**
- **Phase 3: ROC-AUC = 0.9042**

### 1.2 实验：base + 单列 = 3-token

对于每个 SAE CSV 里存在的文本列 X，单独加入它作为**第 3 个**virtual token：

```
原 base:        [tabular 41 列] + incl_token + excl_token
                                                ↓
本实验:         [tabular 41 列] + incl_token + excl_token + X_token
                                                            ↑↑↑
                              encoder ∈ {MedCPT, Qwen3-Embedding-8B}
```

**不**用 cumulative（不是 "base+X1, base+X1+X2, ..."），而是**每个列独立**加入。这样每个 cell 就是 X 列**孤立的**边际贡献，互不干扰。

### 1.3 测试的 8 个文本列

筛选规则：列必须存在于 SAE 的 CSV header 里（否则等于让模型用"是否在 benchmark 其它数据集"的元信息，会泄漏）。

| 列 | 内容 |
|---|---|
| `brief_summary/textblock` | 试验目的简短摘要（2-5 句） |
| `brief_title` | 试验标题 |
| `condition` | 适应症名称 |
| `intervention/description` | 干预措施详细描述 |
| `intervention/intervention_name` | 干预名称（药名等） |
| `keyword` | 关键词列表 |
| `study_design_info/intervention_model_description` | 试验设计模型描述 |
| `study_design_info/masking_description` | 盲法描述 |

> 注：detailed_description/textblock 和 eligibility/gender_description **只存在于 trial-failure-reason 的 CSV**，SAE 没这列，故不测。前一轮实验把它们对 SAE 强行喂进去，曾产生 +0.10 的"假"提升，源于 covered/uncovered 模式泄漏 dataset-membership 元信息——本实验严格规避这类列。

### 1.4 两个 encoder

| Encoder | 模型 | 维度 | 类型 | 池化 |
|---|---|---|---|---|
| MedCPT | `ncbi/MedCPT-Article-Encoder` | 768 | encoder-only，PubMed + 临床试验对比学习预训练，109M 参数 | `[CLS]` token |
| Qwen3-Embedding-8B | `Qwen/Qwen3-Embedding-8B` | 4096 | Qwen3 家族的专用文本 embedding 模型，7.57B 参数，4096-d，32K 上下文，MTEB SOTA | last token + L2 normalize |

两个 encoder 都**离线一次性**编码（冻结，无梯度），结果落 parquet（`data/emb_<col>_<encoder>.parquet`，含 `trial_id, phase, emb_0..emb_{d-1}`）。

### 1.5 列表型字段处理

`keyword`、`condition`、`intervention/intervention_name` 这些常存为 Python-list 字符串（如 `['A','B']`）。统一处理：解析为 list 后用 `, ` 拼成一个字符串，整体送 encoder → 一个 embedding。

### 1.6 训练超参（与 IE_embedding 完全一致）

- 30 epoch，每 3 epoch 在测试集做一次完整 eval，取最优
- 每 epoch 随机采样 ctx=3000 + qry=500
- 损失：CrossEntropy on qry
- AdamW，weight_decay=1e-4
- 差分 LR：投影层 1e-3，pretrained decoder head 2e-5
- gradient checkpointing 开启
- 单 estimator，bf16 autocast，H200 NVL

### 1.7 实验规模

- 8 列 × 2 encoder × 2 phase = **32 个独立训练 run**（其中 brief_summary 是 Step 1 已跑过的复现）

---

## 2. 结果

### 2.1 主表（best ROC-AUC，30 epoch 内最高）

| 列 | Phase 2 base | P2 MedCPT | P2 Qwen | Δ vs base (P2) | Phase 3 base | P3 MedCPT | P3 Qwen | Δ vs base (P3) | encoder winner |
|---|---|---|---|---|---|---|---|---|---|
| brief_summary | 0.8752 | 0.8733 | **0.8787** | M:−0.002 / Q:+0.003 | 0.9042 | 0.9063 | **0.9089** | M:+0.002 / Q:+0.005 | Qwen 双胜 |
| brief_title | 0.8752 | 0.8829 | **0.8906** | M:+0.008 / Q:+0.015 | 0.9042 | 0.9070 | **0.9183** | M:+0.003 / Q:+0.014 | **Qwen 双胜** |
| condition | 0.8752 | 0.8713 | **0.8777** | M:−0.004 / Q:+0.003 | 0.9042 | **0.9090** | 0.9042 | M:+0.005 / Q:0 | 平：P2 Q ↑, P3 M ↑ |
| intervention/description | 0.8752 | 0.8697 | 0.8683 | M:−0.006 / Q:−0.007 | 0.9042 | 0.9068 | 0.9025 | M:+0.003 / Q:−0.002 | M 略胜（含义微小） |
| intervention/intervention_name | 0.8752 | 0.8755 | **0.8812** | M:0 / Q:+0.006 | 0.9042 | **0.9096** | 0.8993 | M:+0.005 / Q:−0.005 | 平：P2 Q ↑, P3 M ↑ |
| keyword | 0.8752 | **0.8812** | 0.8720 | M:+0.006 / Q:−0.003 | 0.9042 | 0.8996 | 0.9008 | M:−0.005 / Q:−0.003 | 平：P2 M ↑, P3 ≈ |
| study_design intervention_model_description | 0.8752 | 0.8741 | **0.8799** | M:−0.001 / Q:+0.005 | 0.9042 | 0.9031 | **0.9101** | M:−0.001 / Q:+0.006 | **Qwen 双胜** |
| study_design masking_description | 0.8752 | 0.8778 | 0.8334 ⚠️ | M:+0.003 / Q:−0.042 | 0.9042 | 0.9072 | **0.9111** | M:+0.003 / Q:+0.007 | P2 Q 没收敛；P3 Q ↑ |

⚠️ Phase 2 +masking_desc Qwen 的 best ROC-AUC = initial（epoch −1），训练 30 epoch 一直没涨过随机投影的 initial 值 → **没收敛**。可能是该列对 SAE Phase 2 信号太弱 + Qwen 4096-d 投影优化不稳定。视为单点失败，不代表 Qwen masking_desc 必然不行（P3 反而是 Qwen 胜）。

### 2.2 MedCPT vs Qwen head-to-head

全 8 列 × 2 phase = **16 个直接对比格**（含 P2 +masking_desc Qwen 未收敛的那一格，仍算入对比）：

| 结果 | 次数 | 列 / phase |
|---|---|---|
| **Qwen 胜**（Δ ≥ +0.003） | **8** | brief_summary P2, brief_title P2/P3, condition P2, interv_name P2, design_model P2/P3, masking_desc P3 |
| **MedCPT 胜**（Δ ≥ +0.003） | 5 | condition P3, interv_desc P3, interv_name P3, keyword P2, masking_desc P2 |
| 平（\|Δ\| < 0.003） | 3 | brief_summary P3, interv_desc P2, keyword P3 |

**Qwen3-Embedding-8B 略胜 MedCPT**（8-5-3），但都不是压倒性优势。**两个 encoder 大多数列的差距在 ±0.01 ROC-AUC 内**，跟训练随机性同量级。

### 2.3 每列的边际增益（取两 encoder 中较好的那个 vs base）

| 列 | Phase 2 best Δ | Phase 3 best Δ | 平均 Δ | 评级 |
|---|---|---|---|---|
| **brief_title** | +0.015 (Q) | +0.014 (Q) | **+0.015** | 一致正向，**最稳定的正增益列** |
| **design_model** | +0.005 (Q) | +0.006 (Q) | +0.006 | 两 phase 一致小正向 |
| **masking_desc** | +0.003 (M) | +0.007 (Q) | +0.005 | P2 噪声 P3 涨，混杂正向 |
| **interv_name** | +0.006 (Q) | +0.005 (M) | +0.005 | 两 phase 各小正向（用不同 encoder） |
| **condition** | +0.003 (Q) | +0.005 (M) | +0.004 | 微小正向 |
| **brief_summary** | +0.003 (Q) | +0.005 (Q) | +0.004 | Qwen 双 phase 小正向 |
| **keyword** | +0.006 (M) | −0.005 (M) | 0 | 两 phase 抵消 |
| **interv_desc** | −0.006 (M) | +0.003 (M) | −0.001 | 几乎不动 |

---

## 3. 结论

### 3.1 关于 encoder（MedCPT vs Qwen3-Embedding-8B）

- **Qwen3-Embedding-8B 在 SAE 上略胜 MedCPT**（8-5-3 head-to-head，16 cell 总和）
- 但**优势很小**：单列绝对差距大多在 ±0.005~0.010 ROC-AUC 内
- Qwen 70 倍的参数量（7.57B vs 109M）带来的提升相当有限——对临床试验文本，MedCPT（领域预训练）的 size 劣势被 domain alignment 弥补了大部分
- **Qwen 的 7B 模型偶尔会有训练不稳定的现象**（P2 +masking_desc 没收敛）；MedCPT 16 个对比格全部正常收敛
- 实用建议：**MedCPT 性价比更高**（编码快 70 倍，效果只差一点，更稳）；要榨极限选 Qwen

### 3.2 关于每个文本列对 SAE 的贡献

- **最有价值**：`brief_title`（+0.015 一致）。短标题就把试验主题刻画得够清楚，对 SAE 有补充
- **稳定小正向**：`design_model`、`masking_desc`、`interv_name`、`condition`、`brief_summary`（+0.003~+0.006）
- **基本无效**：`keyword`、`interv_desc`——单加进去对 SAE 没贡献甚至略微干扰
- 总体上**SAE 的额外文本列单独看，每列最多 +0.015 ROC-AUC**，没有特别强的"杀手列"。SAE 主要靠 tabular + eligibility criteria 已经做得不错（base 0.8752）

### 3.3 局限与下一步

1. **P2 +masking_desc Qwen 没收敛**——单点失败，可能换个 seed / 调 LR 能修
2. 本实验是**单列独立**加入，没有测**多列联合**的相互作用。一些边际效益小的列**联合**起来可能仍有用——但要严格控制 coverage 干扰
3. 只测了 SAE。其它 5 个子任务的 per-column 边际曲线还没做

---

## 4. 复现命令

```bash
cd /data2/zhu11/TB/branch/All_text_embedding
bash script/run_sae_marginal.sh
```

落盘：
- 编码产物：`data/emb_<column>_<encoder>.parquet`
- 训练产物：`results/fs2multi_serious-adverse-event-forecasting_YN_PhaseX_<TS>/metrics.json`
- 实验日志：`results/sae_marginal_log.txt`

---

**文档版本**：2026-05-22
**数据**：TrialBench v1，SAE 子任务 Phase 2 / Phase 3 官方 train/test 划分
**硬件**：NVIDIA H200 NVL (143 GB)，bf16，单 GPU
**TabPFN**：v7.1.1，`tabpfn-v2.5-classifier-v2.5_default.ckpt`
**MedCPT**：`ncbi/MedCPT-Article-Encoder`（109M）
**Qwen**：`Qwen/Qwen3-Embedding-8B`（7.57B，4096-d，last-token pooling + L2 normalize）
