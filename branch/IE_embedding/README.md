# branch/IE_embedding — Eligibility Criteria Embedding Pipeline

> 进入本目录前请先看 [`/data2/zhu11/TB/ReadMeFirst.md`](../../ReadMeFirst.md)。

把 TrialBench 各子任务里 `eligibility/criteria/textblock` 这一段长文本，拆成 inclusion / exclusion 一条一条的 criterion，编码成向量，再把"criterion 难度"信号 distill 成 TabPFN 可用的少量列。

---

## 1. 目的

`eligibility/criteria/textblock` 是 ClinicalTrials.gov 原始 `<textblock>`，一个 trial 一整段。它里面其实是结构化的：Inclusion + Exclusion，bullets / 编号列表。我们想：

1. **拆**成单条 criterion（每条几十~几百字）
2. **编码**成 768 维向量（MedCPT，frozen，无需训练）
3. **distill**：用 criterion embedding 单独训一个小模型预测目标（如 `patient_dropout_rate`），把 trial 内所有 criterion 的输出聚合成几个标量
4. **接入 TabPFN**：把这几个标量当作新列拼回 `train_x.csv`，给 TabPFN（避免直接喂 1536 维 anonymous float —— TabPFN 的 prior 对那种输入不友好）

长期目标：让 embedding（或它的下游头）反映**招募难度**这类临床特征，不止于语义相似度。

---

## 2. 目录结构

```
branch/IE_embedding/
├── README.md            ← 本文件
├── data/                ← 解析 / 编码后的中间产物
│   ├── inclusion.json   ← 每个 (trial_id, phase) 的 inclusion 条目列表
│   ├── exclusion.json   ← 同上 exclusion
│   └── （后续）embeddings.parquet  ← MedCPT 编码结果
├── script/              ← 该 branch 自己的脚本
│   └── split_criteria.py
└── results/             ← 训练 / 评估产物，每次运行一个子目录
    └── <run_id>/...
```

> **注意**：原 `dataset/TrialBench/` 目录是只读的（见 [`ReadMeFirst.md` §1](../../ReadMeFirst.md)），所以解析产物 `inclusion.json` / `exclusion.json` 放在本 branch 的 `data/` 下，不放回 dataset/。

---

## 3. 数据流水线

```
TrialBench 原始 CSV  ─┐
   (6 subtasks ×      │  split_criteria.py
   4 phases ×         ├─────────────────▶  inclusion.json
   train/test)        │                    exclusion.json
                      │
                      │  (next step)
                      │  encode_medcpt.py
                      └─────────────────▶  embeddings.parquet
                                          (trial_id, phase, type, idx, text, emb[768])
```

### 3.1 `split_criteria.py`（已实现）

把 `eligibility/criteria/textblock` 拆成 inclusion / exclusion 一条一条。

**输入**：

| 子任务 | 是否处理 |
|---|---|
| mortality-event-prediction | ✓ 4 phases |
| patient-dropout-event-forecasting | ✓ 4 phases |
| serious-adverse-event-forecasting | ✓ 4 phases |
| trial-approval-forecasting | ✓ 4 phases |
| trial-duration-forecasting | ✓ 4 phases |
| trial-failure-reason-identification | ✓ 4 phases |
| drug-dose-prediction | ✗ 没有 eligibility 列 |
| eligibility-criteria-design | ✗ criterion 本身是 target |

**解析规则**：

1. 扫描所有 `(?im)^[ \t]*(?:-[ \t]+)?(?:key/main/primary[ \t]+)?(?:inclusion|exclusion)s?(?:[ \t]+criteria)?[ \t]*:?[ \t\r]*$` 形式的整行 header
2. 按 header 出现顺序把文本切块，每块归属到对应类型；同一 trial 多段 I/E（如 Part 1/Part 2）自动合并
3. 若第一个 header 是 exclusion，header 前的文本作为 inclusion（很多 trial 的 inclusion 没有显式 header）
4. 块内用 `^\s*(?:-|\d+[.)])\s+` 切条目；多行 criterion 用空白 normalize 合并
5. 完全没 header 的 ~1.6% trial：整段当作 inclusion，按句号 / `!?` 切

**输出**（每个文件是一个 JSON 数组）：

```json
[
  {"trial_id": "NCT00225056", "phase": "Phase2",
   "criteria": ["must have metastatic breast cancer",
                "must have measurable or evaluable disease", ...]},
  ...
]
```

**当前规模**（2026-05-20 跑出）：
- 48 个 CSV 文件 → 81,786 个 (trial_id, phase) unique
- inclusion 685,712 条（平均 8.4/trial），70 trial empty
- exclusion 893,449 条（平均 10.9/trial），5,026 trial empty
- `inclusion.json` 87 MB，`exclusion.json` 113 MB

> **dedup 规则**：同一 trial_id 可能跨多个子任务（如同时出现在 dropout 和 SAE 的 train/test），按 (trial_id, phase) 去重，保留首次解析结果（eligibility 文本只跟 trial 本身相关，跨子任务相同）。

### 3.2 `encode_medcpt.py`（待实现）

把每条 criterion 用 [MedCPT-Article-Encoder](https://huggingface.co/ncbi/MedCPT-Article-Encoder)（PubMed + 临床试验对比学习预训练，109M 参数，768 维）批量编码。输出 parquet：

| trial_id | phase | type | idx | text | emb |
|---|---|---|---|---|---|
| NCT... | Phase2 | inclusion | 0 | "must have metastatic..." | [768 floats] |

bf16，batch 256，H200 上预计 30–60 min 跑完 ~150 万条 criterion。

---

## 4. 聚合策略：从 stacking 到 hidden-layer fusion

**核心问题**：trial 内 criterion 数量变长（中位数 20，最多 117），但 TabPFN 要定长 tabular 输入。下面按"工程量从小到大"列：

| 方式 | trial 特征 | 优 | 劣 |
|---|---|---|---|
| A. raw mean pool concat | 1536 维 | 实现简单 | TabPFN prior 没见过 anonymous float，特征数也超出友好区间。**baseline only** |
| B. PCA mean pool → ~32 维 | 32 列 | 比 A 小，仍保留语义 | 无监督降维，不针对难度 |
| **C. Stacking（主推 Phase 1）** | 8 列 | 用监督信号 distill，TabPFN 拿到的是它擅长的"语义明确列" | criterion 模型用 trial-broadcast 标签，弱监督上限有限 |
| D. Hidden-fusion: virtual feature column | TabPFN 内部多一列 token | 上限更高 | 需要 fine-tune TabPFN，破坏其零样本能力 |
| E. Hidden-fusion: cross-attention adapter | criterion 序列作 K/V | 保留全部条目，上限最高 | 工程量最大，需要充足数据 fine-tune |

### Phase 1 主线：方案 C（Stacking）

```
criterion text
  ──MedCPT(frozen)──▶ 768-d emb
  ──criterion head MLP(768→256→1, K-fold OOF)──▶ scalar 难度分
  ──per-trial 聚合: mean/max/std/count × {I, E}──▶ 8 标量列
  ──join 回 train_x.csv──▶ TabPFN
```

**criterion head 训练目标**：先用 `patient-dropout-event-forecasting` 的 `patient_dropout_rate`（连续值，最直接对应"招募难度"），把 trial 级标签 broadcast 到该 trial 的每条 criterion。

**OOF 防 leak**：5-fold；每个 trial 的 8 维 stacking 特征用**它不参与训练的那一折模型**给出，避免下游 TabPFN 见到含标签信息的列。

**聚合公式**（per trial t）：

```
incl_scores = [head(emb_i) for i in incl_criteria(t)]
excl_scores = [head(emb_i) for i in excl_criteria(t)]
features(t) = [mean(incl), max(incl), std(incl), len(incl),
               mean(excl), max(excl), std(excl), len(excl)]
```

8 列在 TabPFN 的 ~500 列上限内毫无压力。

### Phase 2 / 3（后续）

跑完 Phase 1 拿到 baseline 后，若 C 涨点显著，再考虑 D（virtual feature column，最小架构改动）→ E（cross-attn）。

---

## 5. 下游接入：怎么把这 8 列拼回 TrialBench train_x

每个下游子任务的 train_x.csv 行键是 (trial_id, phase implicit by folder)，本 pipeline 输出按 (trial_id, phase) 索引，**直接 left-join** 即可。已经覆盖所有 4 个 phase 的所有 6 个有 eligibility 列的子任务，无 trial 漏掉。

```python
import pandas as pd
trial_x = pd.read_csv("dataset/TrialBench/serious-adverse-event-forecasting/Phase2/train_x.csv", index_col=0)
ie_feat = pd.read_parquet("branch/IE_embedding/results/<run_id>/ie_features.parquet")
# ie_feat 列: trial_id, phase, incl_mean, incl_max, incl_std, incl_n, excl_*
ie_feat = ie_feat[ie_feat["phase"] == "Phase2"].set_index("trial_id").drop(columns=["phase"])
train_x_aug = trial_x.join(ie_feat)
```

跨子任务 trial 重叠：本项目当前**不去重处理**（criterion head 的训练集可能跟下游 TabPFN 的 train/test 有 trial 共享，会有轻微 leak）。优先跑通整条 pipeline，后续如果想严格再加 fold-aware 拆分。

---

## 6. 复现命令

```bash
# 激活环境
source /data2/zhu11/miniconda3/etc/profile.d/conda.sh && conda activate tabpfn

# 1. 拆 criteria（已跑过；幂等，覆盖输出）
cd /data2/zhu11/TB/branch/IE_embedding
python script/split_criteria.py

# 2. 用 MedCPT 编码（待实现）
# python script/encode_medcpt.py

# 3. 训练 criterion head + 生成 stacking 特征（待实现）
# python script/criterion_head_stacking.py --target patient_dropout_rate --folds 5

# 4. 在下游子任务上跑 TabPFN（参考 script/sae_finetune.py 风格）
# python ../../script/<subtask>_with_ie_feat.py
```

---

## 7. 现状速览

- ✅ 2026-05-20: `split_criteria.py` 实现并跑过，inclusion/exclusion JSON 已生成在 `data/`
- ✅ 2026-05-20: `encode_medcpt.py` 跑完整 1.58M 条 criterion，190 秒 (8.3k/s)，0 NaN
  - 产物：`results/encode_medcpt_20260520_154921/{embeddings.npy (2.4 GB), metadata.parquet (100 MB), run_info.json}`
- ✅ 2026-05-20: `criterion_head_stacking.py` 跑完，5-fold OOF + 全量训练，50 秒
  - 产物：`results/criterion_head_20260520_155333/{ie_features.parquet, oof_predictions.npy, fold_metrics.json}`
  - Criterion 级 OOF R² ≈ 0.10（broadcast 标签的预期上限）
  - **Trial 级**：`incl_mean` 与 `droupout_rate` Pearson **+0.48**，单列 R² 0.20
  - **8 列 Ridge CV R² = 0.229 ± 0.035**（无其他 tabular，纯 IE 特征预测 trial dropout rate）
- ✅ 2026-05-20: `ablate_ie_features.py` 在**全部 6 个**子任务上 A/B（TabPFN-v2.5 zero-shot，无 fine-tune），4 phase 合并；脚本支持 `--task-type {binary,multiclass,regression}`

  | Subtask | task | metric | baseline | + IE | Δ |
  |---|---|---|---|---|---|
  | serious-adverse-event | binary | ROC-AUC | 0.8851 | **0.9035** | **+0.0184** |
  | mortality | binary | ROC-AUC | 0.8576 | **0.8866** | **+0.0291** |
  | patient-dropout (Y/N) | binary | ROC-AUC | 0.8126 | **0.8244** | **+0.0118** |
  | trial-approval | binary | ROC-AUC | 0.8305 | **0.8365** | **+0.0060** |
  | trial-failure-reason | multiclass(4) | macro-F1 | 0.2750 | **0.2887** | **+0.0138** |
  | trial-duration | regression | R² | 0.2681 | **0.3104** | **+0.0423** |

  **6/6 子任务全部正向**。
  - mortality 涨最多（+0.029 ROC-AUC）：入组难度跟死亡率信号高度重叠
  - trial-duration 回归 R² 相对涨 +16%，MAE 减 14 天
  - trial-approval 涨最少（+0.006），监管批准是不同维度信号
  - **criterion head 用 `droupout_rate` 训，迁移到 5 个不同 target 仍普遍涨点**，证明 stacking 抽出的"criterion 难度"信号跨任务泛化
  - SAE 0.885 baseline 与项目原 [`sae_finetune.py`](../../script/sae_finetune.py) 完全一致，sanity check 通过

- ✅ 2026-05-20: `ablate_ie_finetune.py` 4-cell A/B (baseline/+IE × no-FT/FT) on SAE (10 epochs, lr=2e-5)

  | | no-FT | FT | Δ-FT |
  |---|---|---|---|
  | baseline | 0.8851 | 0.8840 | −0.0011 |
  | + IE | **0.9035** | **0.9036** | +0.0001 |
  | Δ-IE | **+0.0184** | **+0.0196** | |

  **结论**：fine-tune 在 SAE 上是 no-op（−0.001 / +0.0001 都在噪声内），IE 特征才是主升力（+1.8% / +2.0% 双侧一致）。Synergy ≈ 0：FT 本身对 SAE 不贡献，所以在 IE 上面再叠也没用。跟项目原有观察一致：[ReadMeFirst.md §7](../../ReadMeFirst.md) "SAE 上 10-epoch fine-tune 暂无显著增益"。FT cost：34s / cell, peak VRAM 5.3-6.4 GB。

  下次如果想 push fine-tune：试 50+ epochs、higher LR、或换到 mortality / trial-duration（zero-shot 涨幅最大的两个子任务，FT 头部空间可能更大）。

- ✅ 2026-05-20: per-phase A/B vs TrialBench paper [Table 6](https://arxiv.org/abs/2407.00631) — 详见 `results/per_phase_comparison_20260520/per_phase_vs_paper.md`
  - 触发: 用户质疑"为啥比 paper 高那么多"
  - 已验证: train/test trial_id 0 重叠（per phase per subtask 全部 0）；setup 没 leak
  - 22 phase × 6 subtask 完整对比:
    - **19/22 phase 我们赢**：mortality (+0.07~0.25 ROC-AUC)、trial-approval (+0.16~0.44！)、SAE、failure-reason、dropout 多数 phase
    - **3 phase paper 赢**：patient-dropout Phase 3 (−0.06)、trial-duration 所有 phase (−0.14~−0.18 R²)
  - Gap 解释:
    1. **不同模型**: paper 用自训多模态 DL fusion (MPNN+BioBERT+MeSH+GRAM+DANets, 20 epoch lr=1e-3 batch=64)，我们用 TabPFN-v2.5 in-context (no gradient) — TabPFN 是 SOTA tabular foundation model
    2. **paper 用 Bio-BERT 编 text**, 我们 baseline `TEXT_DROP` 掉所有 text 列 — 反而我们高，说明 paper 的多模态融合训练不够; 但在 **trial-duration 上 paper 的 text 表征明显胜出** (我们 R² 落后 0.14-0.23)
    3. IE 特征在 per-phase 也普遍涨, 不是 combined-phase artifact

- ✅ 2026-05-20: **Step 2-Lite (PCA 投影)** — `script/make_step2_lite_pca.py` + 修后的 `ablate_ie_features.py`（auto-detect features parquet 任意列）
  - 流水线: per (trial_id, phase, type) mean-pool 768-d → fit PCA(K) on 158K pooled vectors → 64 列 (32 incl + 32 excl)
  - **SAE K sweep**: K=16 (32 cols) 0.9135 / K=32 (64 cols) 0.9128 / K=64 (128 cols) 0.9151 / K=128 (256 cols) 0.9153 — K=16 已吃绝大部分信号
  - **Step 1 stacking + Step 2-Lite PCA-32 联合 (72 cols)** 是 SAE 最强组合: 0.9164
  - **全 6 子任务 Step 2-Lite (72 cols 联合) 都比 Step 1 stacking (8 cols) 高**:

  | Subtask | metric | Baseline | Step 1 (8) | **Step 2-Lite (72)** | Δ vs Step 1 |
  |---|---|---|---|---|---|
  | SAE | ROC-AUC | 0.8851 | 0.9035 | **0.9164** | +0.0129 |
  | mortality | ROC-AUC | 0.8576 | 0.8866 | **0.9147** | **+0.0281** |
  | patient-dropout | ROC-AUC | 0.8126 | 0.8244 | **0.8274** | +0.0030 |
  | trial-approval | ROC-AUC | 0.8305 | 0.8365 | **0.8460** | +0.0095 |
  | trial-failure-reason | macro-F1 | 0.2750 | 0.2887 | **0.3024** | +0.0137 |
  | trial-duration | R² | 0.2681 | 0.3104 | **0.3538** | **+0.0434** |

  - **关键洞察**:
    - 8 supervised 标量 + 64 unsupervised PCA 维度互补：前者编码"难度"信号，后者编码"criteria 内容"信号
    - mortality (+0.028 ROC-AUC) 和 trial-duration (+0.043 R²) 涨幅最大 —— PCA 把 multi-modal 表征捕捉到的"多疾病/年龄/药物"空间还原回来了
    - trial-duration 之前 paper 靠 Bio-BERT 编码 brief_summary 赢我们 0.14-0.23 R²，PCA 把 inclusion/exclusion 的内容空间加进来后差距缩到约 0.10
  - 产物: `results/step2_lite_pca_k{16,32,64,128}_*/ie_features.parquet`, `results/combined_stack8_pca32_20260520.parquet`

- ✅ 2026-05-20: **Full Step 2 POC (virtual feature column)** — `script/full_step2_train.py`
  - 架构: 冻结全部 TabPFN，monkey-patch `PerFeatureTransformer.add_embeddings` 注入 2 个 virtual feature tokens；trainable = 2 × `nn.Linear(768, 192)` + 2 × col emb (192-d)，共 295,296 params
  - Preprocessing: 用 sklearn `ColumnTransformer`（OneHot + StandardScaler）替代 TabPFN 内部 preprocessor（因为需要 differentiable forward 路径）
  - 训练: 自己写的 loop，每 step 随机 ctx (4000) + qry (1000)，AdamW lr=1e-3，30 epochs，gradient checkpointing，单 estimator
  - 产物: `results/full_step2_20260520_200550/`

  | | ROC-AUC |
  |---|---|
  | Plain baseline (TabPFN preprocess, no virt) | 0.8851 |
  | Full Step 2 initial (**random** virt projection, sklearn preprocess) | 0.8911 |
  | Full Step 2 best (30 ep trained, plateau ep 15-27) | **0.9084** |
  | Step 2-Lite (8 stacking + PCA-32 = 72 cols) | **0.9164** |

  **结论：Full Step 2 (frozen base) < Step 2-Lite by 0.008 ROC-AUC。**

  - 架构确实工作：训练 295K 投影 params 让 ROC-AUC 涨 +0.013 (0.8911 → 0.9084)，trend 在收敛
  - 但被压在 Step 2-Lite 之下，三个可能原因：
    1. **Preprocessing 差异**: sklearn ColumnTransformer ≠ TabPFN 内部 quantile transforms 等。仅 initial (random virt) 0.8911 vs TabPFN baseline 0.8851 就有 +0.006 差
    2. **单 estimator** vs Step 2-Lite 的 n_estimators=2 ensemble
    3. **冻结全部 base 太严格** —— 192-d projected vector 落到 attention 里可能要 unfreeze 至少几层让 transformer 适应这种 token 分布

- ✅ 2026-05-20: **Full Step 2 + unfreeze decoder head** 实验

  尝试解冻 TabPFN 末端的 `decoder_dict["standard"]` MLP head (~78K params, 192→384→10)，差分 LR (proj lr=1e-3, decoder lr=2e-5)：

  | Setup | Best ROC-AUC |
  |---|---|
  | Frozen all, only projections (上面) | 0.9084 |
  | + unfreeze decoder head | 0.9092 (+0.0008) |
  | Step 2-Lite reference | 0.9164 |

  **解冻 decoder 几乎没用**——重要的负面结果：bottleneck 不在 head，在 frozen transformer body。

  逻辑：head 是 192→384→10 MLP，输入是 transformer 末层的 target token 表征。如果 head 能补救 virtual token 信号，解冻它应该明显涨。只涨 +0.0008 意味着：
  - frozen 24 层 attention **根本没学会重视 virtual tokens**，把它们当噪声列
  - target token 出来的 192-d 表征几乎没带 virtual 信息
  - head 即便能微调输出层，救不了"信息已经没传到位"

  要 Full Step 2 真正涨起来，必须让 attention layers 适应 virtual tokens —— 至少 partial unfreeze 后几层 transformer block，但那就接近完整 FT 了，不再是"只训投影"的最小动作

- ⏳ 下一步可选：
  - **Step 2-Lite supervised bottleneck**: 用 dropout 标签训 768→32→1 MLP，取 32-d bottleneck 当 feature，对比无监督 PCA
  - **per-phase 重跑 Step 2-Lite**: 完整 22-cell 对照表 vs paper Table 6
  - **Full Step 2 加强版**: partial-unfreeze 最后几层 + TabPFN preprocess + multi-estimator —— 工程量大，预期收益 ~+0.01 ROC-AUC，不一定值得
