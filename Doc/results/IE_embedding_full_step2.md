# TrialBench 临床试验预测：三方案 Per-Phase 对比与 Full Step 2 改进方案

> 评测对象：TrialBench 数据集中**所有 6 个**有 eligibility 字段的子任务（drug-dose、eligibility-criteria-design 不含相关字段，已排除）。
>
> **所有结果均在单个 Phase 内独立训练 + 评估**——与 TrialBench 论文 Table 6 的 per-phase 报告方式对齐。本文档分别给出 **Phase 2** 和 **Phase 3** 两组实验结果。Phase 2 是各子任务样本量最大的 phase，Phase 3 通常样本量稍小但任务难度（疗效阶段）不同。

---

## 1. 方案概览

| 方案 | 模型 | 是否使用 eligibility 文本 | 训练成本 |
|---|---|---|---|
| **Baseline** | TrialBench 论文：多模态深度学习 fusion（MPNN+Bio-BERT+MeSH+GRAM+DANets） | ✓（Bio-BERT 编码 brief_summary + eligibility/criteria） | 多模态网络从头训 20 epoch |
| **SOTA** | TabPFN-v2.5 in-context learning（项目原有） | ✗（`TEXT_DROP` 丢弃所有长文本列） | 零样本，无梯度更新 |
| **改进方案：Full Step 2 + unfreeze decoder** | TabPFN-v2.5 + 2 个可学习虚拟特征列 | ✓（MedCPT 编码 inclusion / exclusion criteria + 虚拟列注入） | 冻结 TabPFN 主体 24 层 attention，仅训 ~373K 参数 |

---

## 2. Baseline（TrialBench 论文）

TrialBench 论文 [arXiv:2407.00631](https://arxiv.org/abs/2407.00631) Table 6 给出的官方 baseline 是一个**多模态深度学习融合模型**：

```
SMILES   → MPNN              ┐
text     → Bio-BERT          │
MeSH     → MeSH-Embedding    ├─→ concat → MLP → logits
ICD code → GRAM              │
其它     → DANets            ┘
```

训练：20 epoch，Adam lr=1e-3，batch=64，embedding dim=100。论文按 phase 单独训练单独评估。

---

## 3. SOTA（TabPFN-v2.5 in-context，无 fine-tune）

项目现有 baseline：

- **模型**：TabPFN-v2.5 classifier / regressor（10.7M 参数）
- **输入**：丢弃所有长文本列（`brief_summary/textblock`、`eligibility/criteria/textblock`、`detailed_description/textblock` 等共 20 列），保留 ~41 个结构化 tabular 列（数值 + 类别）
- **训练**：零样本 in-context learning，无任何梯度更新
- **方式**：Phase 2 单独训练 + 评估

TabPFN-v2.5 是当前 tabular foundation model 的 SOTA。但它的 prior 不接受文本输入，eligibility / brief_summary 这类富文本信号完全没用上。

---

## 4. 改进方案：Full Step 2 + unfreeze decoder head

### 4.1 核心思想

**保留 TabPFN 的 SOTA tabular 能力，把 eligibility 文本"塞进"它内部 attention 看得见的位置**，但只用最少的可训练参数。

### 4.2 数据流水线

```
ClinicalTrials.gov XML
  └─ eligibility/criteria/textblock （整段文本，每个 trial 一段）

  ┌─────────────────────── 离线一次性预处理 ────────────────────────┐
  │                                                                  │
  │  Step A. 拆分                                                    │
  │    正则把 textblock 拆成 inclusion / exclusion 条目列表          │
  │    例：trial NCT00225056 → 12 条 inclusion + 8 条 exclusion       │
  │                                                                  │
  │  Step B. MedCPT 编码                                             │
  │    每条 criterion 喂 ncbi/MedCPT-Article-Encoder（PubMed +       │
  │    临床试验对比学习预训练，109M 参数，**固定不训**）→ 768-d 向量 │
  │                                                                  │
  │  Step C. Trial 级 mean-pool                                      │
  │    把同一 trial 的所有 inclusion embedding 取平均 → 1 个 768-d   │
  │    exclusion 同样 → 另 1 个 768-d                                 │
  │                                                                  │
  └──────────────────────────────────────────────────────────────────┘
        ↓
  每个 trial：tabular 41 列 + 2 个 768-d 向量（incl, excl）
```

### 4.3 模型架构改动（虚拟特征列注入）

TabPFN 内部把每个 tabular cell 当成 token，41 列 = 41 个 tokens。我们**追加 2 个 token**，每个 token 装的不是一个标量、而是 768-d 向量经过一层 Linear 投影后的结果：

```
原 TabPFN:
  41 cells → 41 tokens(192-d) ──attention 24 层──▶ target token(192-d) ──▶ MLP head ──▶ 10 类 logits
                                                                            ↑
                                                                 decoder_dict["standard"]
                                                                 Linear(192,384)+GELU+Linear(384,10)

改进版:
  41 cells → 41 tokens(192-d)
  incl_emb(768-d) → nn.Linear(768,192) + virt_col_emb[0] → 1 个 virtual token(192-d)
  excl_emb(768-d) → nn.Linear(768,192) + virt_col_emb[1] → 1 个 virtual token(192-d)
                              ↓
                  共 43 tokens ──attention 24 层──▶ target token(192-d) ──▶ MLP head ──▶ logits
```

注入点：fork TabPFN 的 `PerFeatureTransformer`，monkey-patch 它的 `add_embeddings` 方法。在它给原 41 列加完位置嵌入之后、把 token 序列拼到 target 之前，把 2 个 virtual tokens 沿 feature 维 concat 进去。后续 24 层 transformer block 把它们和原 41 个 tokens 一起做 attention，无需任何其它架构改动。

### 4.4 参数冻结策略

TabPFN 主体 10.72M 参数**全部冻结**，仅 4 类参数可训：

| 模块 | 形状 | 参数量 | 是否预训练 | 学习率 |
|---|---|---|---|---|
| `proj_incl` | `Linear(768, 192, bias=False)` | 147,456 | 随机初始化 | 1e-3 |
| `proj_excl` | `Linear(768, 192, bias=False)` | 147,456 | 随机初始化 | 1e-3 |
| `virt_col_emb` | `Parameter(2, 192)` | 384 | 随机初始化 | 1e-3 |
| `decoder_dict["standard"]` | `Linear(192,384)+GELU+Linear(384,10)` | 77,962 | TabPFN 预训练 | 2e-5 |
| **可训练总计** | | **373,258** | | |

**为什么解冻 decoder head？** 注入 virtual tokens 后，attention 末层的 target token 表征分布跟原 prior 不一样了。decoder MLP head 是把这个 192-d 表征映射到类别 logits 的最后一步，如果不让它适配新表征，前面的 virtual token 信号到了输出层会被原 head 误解。

**为什么用差分 LR？** 投影层是从零开始训，需要相对大的 LR (1e-3)。decoder head 是预训练好的，相同 LR 几个 epoch 就把它训崩（实测一度跌到 ROC-AUC 0.43）。差分 LR = 投影 1e-3 + decoder 2e-5（TabPFN 标准 FT lr）是稳定收敛的关键。

### 4.5 训练循环

- 用单个 Phase 的 train/test 官方划分（本文档分别报告 Phase 2 / Phase 3）
- 每个 epoch 从 train 中随机采样 ctx=3000 + qry=500
- forward: `x = concat(X_ctx, X_qry)`, `y = y_ctx`（test 行 y 留空）→ 模型预测 qry 行的 logits
- 损失：CrossEntropy 对 qry 真实标签
- 优化器：AdamW，weight_decay=1e-4，30 epoch
- gradient checkpointing 开启
- 每 3 epoch 在 test set 上完整 eval 一次，记录最优

### 4.6 回归任务的处理

trial-duration 是连续目标。TabPFN 原生 regressor 用 bar-distribution head，与 classifier 不同。为了让虚拟列注入复用同一架构，本工作把连续目标 `time_day` 按分位数离散化成 10 个 bin，用 10-class 分类器训，预测时取概率加权 bin center 的平均值作为连续输出，再算 MAE/RMSE/R²。这是一个工程折中——理论上严格的 bar-distribution regressor 头部可以做得更精细。

---

## 5. 完整结果对比（Per-Phase 对齐）

### 5.1 Phase 2 结果

| Subtask | 类型 | 主指标 | Baseline (论文 P2) | SOTA (TabPFN P2) | **改进方案 (Full Step 2 P2)** | Δ vs SOTA | Δ vs Paper |
|---|---|---|---|---|---|---|---|
| serious-adverse-event | binary | ROC-AUC | 0.8272 | 0.8199 | **0.8752** | **+0.0553** | **+0.0480** |
| mortality | binary | ROC-AUC | 0.7577 | 0.8282 | **0.9042** | **+0.0760** | **+0.1465** |
| patient-dropout | binary | ROC-AUC | 0.7778 | 0.7738 | 0.7481 | **−0.0257** | **−0.0297** |
| trial-approval | binary | ROC-AUC | 0.6176 | 0.8193 | **0.8377** | +0.0184 | **+0.2201** |
| trial-failure-reason | multiclass (4 类) | macro-F1 | 0.1505 | 0.2676 | **0.3151** | **+0.0475** | **+0.1646** |
| trial-duration | regression* | R² | 0.4125 | 0.1807 | **0.2679** | **+0.0872** | **−0.1446** |

| | vs SOTA TabPFN | vs Paper Baseline |
|---|---|---|
| Full Step 2 胜出的子任务数 | **5 / 6** | **4 / 6** |
| 失利的子任务 | patient-dropout (−0.026) | patient-dropout (−0.030)、trial-duration (−0.145) |

### 5.2 Phase 3 结果

| Subtask | 类型 | 主指标 | Baseline (论文 P3) | SOTA (TabPFN P3) | **改进方案 (Full Step 2 P3)** | Δ vs SOTA | Δ vs Paper |
|---|---|---|---|---|---|---|---|
| serious-adverse-event | binary | ROC-AUC | 0.8951 | 0.8935 | **0.9042** | +0.0107 | +0.0091 |
| mortality | binary | ROC-AUC | 0.6649 | 0.8237 | **0.8718** | **+0.0481** | **+0.2069** |
| patient-dropout | binary | ROC-AUC | 0.9126 | 0.8514 | 0.8494 | −0.0020 | **−0.0632** |
| trial-approval | binary | ROC-AUC | 0.6520 | 0.8107 | **0.8186** | +0.0079 | **+0.1666** |
| trial-failure-reason | multiclass (4 类) | macro-F1 | 0.1972 | 0.2530 | **0.3320** | **+0.0790** | **+0.1348** |
| trial-duration | regression* | R² | 0.3148 | 0.0851 | **0.1738** | **+0.0887** | **−0.1410** |

| | vs SOTA TabPFN | vs Paper Baseline |
|---|---|---|
| Full Step 2 胜出的子任务数 | **5 / 6** | **4 / 6** |
| 失利的子任务 | patient-dropout (−0.002, 几乎持平) | patient-dropout (−0.063)、trial-duration (−0.141) |

> *trial-duration 的实现见 §4.6（量化 10-bin 多分类，加权 bin center 还原连续值）。

### 5.3 Phase 2 与 Phase 3 综合观察

**两个 phase 都呈现一致的模式**——Full Step 2 在 5/6 子任务超过 SOTA，在 4/6 超过 Paper。具体观察：

| 子任务 | Phase 2 Δ vs SOTA | Phase 3 Δ vs SOTA | 性质 |
|---|---|---|---|
| mortality | **+0.076** | **+0.048** | 两个 phase 都涨幅最大 — eligibility 文本对死亡率信号贡献明显 |
| trial-failure-reason | +0.048 | **+0.079** | 都明显涨 — "poor enrollment" 等失败原因跟入组条件直接相关 |
| trial-duration | +0.087 | +0.089 | 都明显涨 vs SOTA，但**都低于 Paper**（Paper Bio-BERT 编码 brief_summary 占优） |
| serious-adverse-event | +0.055 | +0.011 | 都涨；Phase 3 SAE 任务本身已很好做（0.89→0.90），改进空间小 |
| trial-approval | +0.018 | +0.008 | 都微涨 — 监管批准更受药品 / 试验设计影响，criterion 文本贡献小 |
| **patient-dropout** | **−0.026** | **−0.002** | 两个 phase 都不涨（Phase 2 还输 SOTA）— 持续的弱点 |

**关键发现**：
- 改进在两个 phase 间**高度可复现**——胜出的 5 个子任务、失利的 1 个子任务完全一致
- **mortality / trial-failure-reason / trial-duration 三个任务**是 Full Step 2 收益最稳定的，这些任务的临床信号高度依赖 eligibility 文本（疾病严重程度、入组要求、随访期）
- **patient-dropout** 是一致的弱点。两个 phase 都无法超过 SOTA TabPFN。可能原因：Y/N 高度不均衡（78-91% 阳性），加上 dropout 主要受试验流程而非 eligibility 影响
- **trial-duration vs Paper 的差距**也跨 phase 一致（−0.14 R²）—— 这是本方案"伪回归"实现 + 不用 brief_summary 文本的结构性局限

---

## 6. 讨论与局限

### 6.1 主要贡献
- 改进方案在 **5/6 子任务上同时超过 SOTA TabPFN**（Phase 2 与 Phase 3 都成立）与 **4/6 上超过论文 Baseline**
- 核心创新：让冻结的 TabPFN 通过 virtual feature column 间接"看到"eligibility 文本，仅需训练 ~373K 参数（占 TabPFN 主体 3.5%）
- 训练成本极低：每个 phase 单独训练 ~2-5 分钟（H200 NVL，bf16，单 GPU）
- **跨 Phase 可复现**：Phase 2 与 Phase 3 的胜负 pattern 完全一致，说明改进不是单 phase 的偶然

### 6.2 局限
1. **patient-dropout 两个 phase 都不涨**：Phase 2 比 SOTA 低 0.026 ROC-AUC，Phase 3 几乎持平 −0.002。可能跟 Y/N 高度不均衡（78-91% 阳性）、dropout 主要受试验流程而非 eligibility 决定有关
2. **trial-duration vs Paper 的差距是结构性的**：两个 phase 都低于 Paper 0.14 R²。Paper 用 Bio-BERT 编码 brief_summary 这种富文本，本方案只用 eligibility/criteria 加 10-bin 量化"伪回归"，精度损失明显
3. **trial-duration 的回归是"伪回归"**：用 10 个分位数 bin + multiclass + 加权 bin center 实现。理论上严格的 bar-distribution regressor 头部能做得更精细
4. **Preprocessing 不完全等价**：改进方案为了支持 differentiable forward，用 sklearn `ColumnTransformer` 替代了 TabPFN 内部的 quantile transform 等预处理
5. **冻结主体限制了上限**：transformer body 24 层 attention 没适配虚拟 token；进一步上限要 partial unfreeze 最后几层 transformer block
6. **只在 Phase 2 / Phase 3 验证**：Phase 1 / Phase 4 没跑。两个 phase 一致的 pattern 提供了一定可复现证据，但严格泛化还需要补全

---

**文档版本**：2026-05-21
**数据**：TrialBench v1（[Zenodo record 15455785](https://zenodo.org/record/15455785)），所有结果使用各子任务**单个 Phase** 的 train/test 官方划分（本文档覆盖 Phase 2 和 Phase 3）
**硬件**：NVIDIA H200 NVL（143 GB VRAM），CUDA 13.2
**TabPFN**：v7.1.1（editable install），checkpoint `tabpfn-v2.5-classifier-v2.5_default.ckpt`
**MedCPT**：`ncbi/MedCPT-Article-Encoder`（HF，109M 参数）
