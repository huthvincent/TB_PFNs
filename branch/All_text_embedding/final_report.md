# All_text_embedding 实验最终报告

> 本文档归纳 `branch/All_text_embedding/` 下完成的全部工作：方法、实施细节、踩过的坑、以及最终干净的结论。延续 `branch/IE_embedding/` 的 Full Step 2 + unfreeze decoder 架构，把 TrialBench 里**所有可用的文本列**作为虚拟特征列注入 frozen TabPFN，分阶段对比不同 encoder（MedCPT / Qwen3-Embedding-8B）的实际增益。

---

## 0. 速览（TL;DR）

| 阶段 | 做了什么 | 结论 |
|---|---|---|
| **Step 1** | 加 `brief_summary` 作第 3 个 virtual token（MedCPT），6 子任务 × P2/P3 = 12 run | 8/12 正向，**patient-dropout / failure-reason 大涨**（+0.030/+0.038），其余持平 |
| **Step 2** | Qwen3-Embedding-8B 编 8 个文本列，cumulative sweep 4-tok→11-tok × 6 子任务（Phase 2），48 run | **结果被泄漏 artifact 污染**——`detailed_description` 在其他子任务的部分覆盖让模型用"benchmark 数据集成员"做特征，假性 +0.10。**该轮结论作废** |
| **诊断** | 三个对照（zeroed / random / real） + LogReg 单列 → outcome AUC | 证实**内容无信号**，跳幅来自 coverage 模式；得出"列只在 CSV 存在它的子任务里用"的硬规则 |
| **SAE 边际 sweep（干净版）** | 对 SAE 的 8 个 CSV 内文本列各做 base+1，MedCPT 与 Qwen3 head-to-head，P2/P3，共 32 run | **Qwen 8 胜 / MedCPT 5 胜 / 3 平**；**brief_title 唯一稳定正向 (+0.015)**，其余 ±0.005 |

---

## 1. 背景与目标

### 1.1 起点

`branch/IE_embedding/` 已经实现并验证：

- **架构**：fork TabPFN-v2.5 `PerFeatureTransformer`，monkey-patch `add_embeddings`，在原 41 个 tabular cell-token 后面 concat N 个 virtual tokens。每个 virtual token = `Linear(d_text, 192)(text_embedding) + virt_col_emb`
- **训练**：TabPFN 主体 10.6M 参数**全部冻结**，只训 N 个投影层 + N 个 column embedding + decoder head MLP（≈ 几百 K 参数）。差分 LR：投影 1e-3，pretrained decoder 2e-5。
- **基线**：6 子任务 P2/P3 的 2-token Full Step 2（incl/excl 两个 MedCPT-encoded virtual token）已经存在并验证过，详见 `Doc/results/IE_embedding_full_step2.md`

### 1.2 本 branch 要回答的问题

1. **brief_summary 这一列加进去有用吗**？（即把 2-token base 扩到 3-token：incl/excl/summary）
2. **其它文本列**（detailed_description / condition / intervention 描述等）逐列加入，**各自单独**贡献多少？
3. **不同 encoder（MedCPT vs Qwen3-Embedding-8B）哪个适合临床试验文本**？

### 1.3 TrialBench 的 6 个子任务

只评测有 eligibility 字段的 6 个（drug-dose、eligibility-criteria-design 不含相关字段，排除）：

| 子任务 | 类型 | 目标 | metric |
|---|---|---|---|
| serious-adverse-event-forecasting (SAE) | binary | Y/N（严重不良事件） | ROC-AUC |
| mortality-event-prediction | binary | Y/N | ROC-AUC |
| patient-dropout-event-forecasting | binary | Y/N | ROC-AUC |
| trial-approval-forecasting | binary | outcome（批准/否） | ROC-AUC |
| trial-failure-reason-identification | multiclass (4 类) | failure_reason | macro-F1 |
| trial-duration-forecasting | regression | time_day | R²（10-bin 量化伪回归） |

---

## 2. 基础设施搭建

### 2.1 目录与文件

```
branch/All_text_embedding/
├── README.md               ← branch 概览 + 阶段汇总
├── SAE_marginal_results.md ← SAE 边际 sweep 的独立详细文档
├── final_report.md         ← 本文件
├── data/                   ← 编码产物（per-trial embedding parquet）
│   ├── emb_inclusion_medcpt.parquet            (81716, 770)
│   ├── emb_exclusion_medcpt.parquet            (76760, 770)
│   ├── emb_brief_summary_textblock_medcpt.parquet  (48145, 770)
│   ├── emb_brief_summary_textblock_qwen.parquet    (48145, 4098)
│   ├── emb_brief_title_<medcpt|qwen>.parquet
│   ├── emb_condition_<medcpt|qwen>.parquet
│   ├── emb_intervention_description_<medcpt|qwen>.parquet
│   ├── emb_intervention_intervention_name_<medcpt|qwen>.parquet
│   ├── emb_keyword_<medcpt|qwen>.parquet
│   ├── emb_study_design_info_intervention_model_description_<medcpt|qwen>.parquet
│   ├── emb_study_design_info_masking_description_<medcpt|qwen>.parquet
│   ├── emb_detailed_description_textblock_qwen.parquet     (only failure-reason scope)
│   ├── emb_detailed_description_ZEROED.parquet             (leak-diagnosis control)
│   └── emb_detailed_description_RANDOM.parquet             (leak-diagnosis control)
├── script/
│   ├── encode_text_column.py        ← 通用文本列编码（支持 medcpt + qwen）
│   ├── make_incl_excl_parquet.py    ← 把 IE_embedding 的 criterion embedding 重导成统一 parquet
│   ├── full_step2_multi.py          ← 通用 N-列 virtual-token 训练（VirtualInjectionMulti）
│   ├── run_step1.sh                 ← Step 1: 3-token MedCPT 完整 sweep
│   ├── run_step2.sh                 ← Step 2: Qwen 8 列编码 + cumulative sweep（污染版）
│   └── run_sae_marginal.sh          ← SAE 边际 sweep（干净版）
└── results/                         ← 训练 / 编码 run 输出
    ├── fs2multi_*/metrics.json
    └── *_log.txt
```

### 2.2 三个核心脚本

**`encode_text_column.py`**
- 输入：`--column "<csv-col-name>" --encoder {medcpt,qwen} --phases Phase2,Phase3`
- 流程：扫所有 6 子任务的 Phase2/Phase3 train_x.csv + test_x.csv（48 个 CSV），对 header 里有该列的 CSV 提取 (trial_id, cell)，按 (trial_id, phase) 去重；列表型 cell（如 `['A','B']`）解析后用 `, ` 拼成一个字符串；空 cell 填 `[empty]`
- 编码：
  - **MedCPT**：`ncbi/MedCPT-Article-Encoder`（109M，frozen），`[CLS]` 池化，max_length=512，输出 768-d
  - **Qwen**：`Qwen/Qwen3-Embedding-8B`（7.57B，frozen），last-token 池化 + L2 normalize，max_length=2048，输出 4096-d
- 输出：`data/emb_<safe_col>_<encoder>.parquet`，列 = `trial_id, phase, emb_0..emb_{d-1}`，存 float16

**`full_step2_multi.py`**（IE_embedding `full_step2_train.py` 的通用化版）
- 接受任意数量的 virt-embs parquet（`--virt-embs path1,path2,...`），每个对应一个 virtual token
- `VirtualInjectionMulti` 类：`nn.ModuleList([Linear(d_i, 192) for d_i in emb_dims])` + `nn.Parameter(N, 192)` column embeddings；monkey-patch `base.add_embeddings` 在 transformer 入口处 concat N 个 virtual tokens
- 冻结策略：TabPFN 全冻结，可选 `--unfreeze-decoder`（解冻 `decoder_dict["standard"]` 78K params）
- 训练：30 epoch，每 epoch 随机采样 ctx=3000 + qry=500，AdamW 差分 LR（投影 1e-3，base 2e-5），bf16 + gradient checkpointing
- 任务类型：binary / multiclass / regression（regression 走 10-bin 分位数量化 + 概率加权 bin center 还原）

**`make_incl_excl_parquet.py`**
- 把 IE_embedding 里 1.58M 条 criterion 的 MedCPT embedding 按 (trial_id, phase, type) GPU 上 mean-pool，导出 `emb_inclusion_medcpt.parquet` 和 `emb_exclusion_medcpt.parquet`，统一成跟其它文本列同格式，方便混合喂多列训练器

### 2.3 实施约定

- **编码范围**：只覆盖 6 子任务 Phase 2 / Phase 3 的 train + test 实际用到的 trial（去重后约 48K），不编全部 81K trial
- **分阶段评估**：每个子任务的 Phase 2 / Phase 3 各自独立训练 + 评估，与 TrialBench paper Table 6 per-phase 报告对齐
- **后台运行**：长 sweep 全部用 `nohup ... &` 启动，日志写文件，退出登录不停

---

## 3. Step 1：brief_summary (MedCPT) 作第 3 个 virtual token

### 3.1 做法

- 用 `encode_text_column.py --column brief_summary/textblock --encoder medcpt` 离线编码：48,145 (trial_id, phase)，190 秒
- 对每个子任务 × 每个 phase 跑 3-token Full Step 2：`virt-embs = inclusion_medcpt, exclusion_medcpt, brief_summary_medcpt`
- 共 6 × 2 = 12 run，每个 30 epoch，约 5 min
- 总 runner：`script/run_step1.sh`，nohup 启动

### 3.2 结果（vs IE_embedding 的 2-token Full Step 2 基线）

| Subtask | Phase | metric | 2-token | 3-token (+summary) | Δ |
|---|---|---|---|---|---|
| SAE | P2 | ROC-AUC | 0.8752 | 0.8781 | +0.003 |
| SAE | P3 | ROC-AUC | 0.9042 | 0.9035 | −0.001 |
| mortality | P2 | ROC-AUC | 0.9042 | 0.9012 | −0.003 |
| mortality | P3 | ROC-AUC | 0.8718 | 0.8761 | +0.004 |
| **patient-dropout** | **P2** | ROC-AUC | 0.7481 | **0.7783** | **+0.030** |
| patient-dropout | P3 | ROC-AUC | 0.8494 | 0.8532 | +0.004 |
| trial-approval | P2 | ROC-AUC | 0.8377 | 0.8324 | −0.005 |
| trial-approval | P3 | ROC-AUC | 0.8186 | 0.8277 | +0.009 |
| trial-failure-reason | P2 | macro-F1 | 0.3151 | 0.3318 | +0.017 |
| **trial-failure-reason** | **P3** | macro-F1 | 0.3320 | **0.3700** | **+0.038** |
| trial-duration | P2 | R² | 0.2679 | 0.2312 | −0.037 |
| trial-duration | P3 | R² | 0.1738 | 0.2490 | +0.075 |

**8/12 正向**。

**结论**：brief_summary 的最大贡献给到了 IE features 单独搞不定的任务——**patient-dropout**（之前的弱点）和 **trial-failure-reason**。这两个任务都受试验设计驱动，brief_summary 描述试验本身正好补上 eligibility criteria 给不出的信息。SAE / mortality / trial-approval 这些 criteria 已经够用的任务，summary 边际接近 0。trial-duration 高方差（量化回归本身不稳）单看不能定论。

---

## 4. Step 2：Qwen3-Embedding-8B 八列 cumulative sweep（**结果污染**）

### 4.1 做法

- 用 Qwen3-Embedding-8B 离线编码 8 个文本列：
  `detailed_description/textblock` → `intervention/description` → `condition` → `intervention/intervention_name` → `brief_title` → `keyword` → `study_design_info/intervention_model_description` → `study_design_info/masking_description`
- 每列 ~48K texts，batch 16，最长 2048 token，bf16，约 15-20 min/列
- 然后 cumulative sweep：base = 3-token (incl/excl/summary, MedCPT)，按上述顺序逐列加 Qwen-encoded 列，4-token → 11-token，**Phase 2 only**，6 子任务，共 8 × 6 = 48 run
- runner：`script/run_step2.sh`，nohup 启动

### 4.2 表面结果（**结论后来被推翻**）

| 子任务 P2 | 3-tok | …8 列累加…  | 11-tok | Δ |
|---|---|---|---|---|
| trial-approval | 0.8324 | …骤跳 0.8324→0.9376 @ 4-tok…  | 0.9401 | +0.108 |
| trial-failure-reason | 0.3318 | …骤跳 0.3297→0.4232 @ 5-tok… | 0.4139 | +0.082 |
| trial-duration | 0.2312 | …涨到 0.3454 @ 9-tok… | 0.3259 | +0.095 |
| mortality | 0.9012 | …+0.017… | 0.9184 | +0.017 |
| SAE | 0.8781 | …+0.006… | 0.8840 | +0.006 |
| patient-dropout | 0.7783 | …小波动… | 0.7724 | −0.006 |

trial-approval +0.108 这种量级**异常显眼**——这是触发后续诊断的关键信号。

### 4.3 三步诊断：泄漏定位

**Diagnosis 1：列在哪些 CSV 里**

```
detailed_description/textblock  ← 只在 trial-failure-reason 的 CSV
eligibility/gender_description  ← 只在 trial-failure-reason 的 CSV
intervention/intervention_type  ← 只在 trial-failure-reason 的 CSV
intervention/description        ← 在 5/6（缺 failure-reason）
study_design_info/masking_description  ← 在 4/6（缺 approval、failure）
```

trial-approval 的 CSV **没有** `detailed_description/textblock` 这一列。本应该不能用，但我的 `full_step2_multi.py` 在 align embedding 时是按 trial_id overlap 查的——trial-approval Phase 2 train 里有 49% 的 trial 跟 failure-reason 数据集**重叠**（同一个 NCT 出现在两个子任务），这些 trial 就拿到了 detailed_description 的 embedding，其余 51% 拿到零向量。

**Diagnosis 2：内容是否预测 outcome**

把 detailed_description embedding 单独喂 LogReg → outcome，5-fold AUC：

| column | d | covered | LogReg train→test AUC |
|---|---|---|---|
| detailed_description | 4096 | 49% | **0.4945** |
| intervention/description | 4096 | 100% | 0.4733 |
| condition | 4096 | 100% | 0.4998 |
| brief_summary | 768 | 100% | 0.4965 |

**所有文本 embedding 单独预测 trial-approval outcome 的 AUC 都 ≈ 0.5（纯随机）**——内容本身根本没有 outcome 信号。

**Diagnosis 3：三个对照实验**

把 detailed_description 列替换成（a）置零向量（b）随机单位向量（与真实相同的 49% coverage 模式），跑 trial-approval Phase 2 4-token：

| 4-token detailed_description 的内容 | best ROC-AUC |
|---|---|
| 3-token（不加这列）—— 参考 | 0.8324 |
| **置零**（所有 trial 同一常量 token） | 0.8361 |
| **随机向量**（每 trial 独立 4096-d 随机，同 coverage） | **0.9292** ← 跳了！ |
| **真实内容** | 0.9376 |

**随机内容跟真实内容几乎一样跳**，置零完全没跳 → 跳幅 100% 来自 **coverage 模式**，跟列的内容无关。

### 4.4 泄漏机制

> partial coverage = "有/无该 token" = "这个 trial 是否也出现在另一个 benchmark 子任务的数据集里" = **benchmark 构造元信息**

模型用 covered/uncovered 把训练集切成两个子群，**对两个子群学不同决策规则**（feature interaction）。Marginally outcome|covered ≈ outcome|uncovered（0.383 vs 0.386），所以"知道是否 covered"不是直接预测 outcome，而是**改变了 41 个 tabular 特征到 outcome 的映射**——这种 interaction 在 TabPFN 的 in-context attention 下可以给 +0.10 的 AUC。

这不是临床上的真实特征，是 dataset 构造产物，**属于泄漏**。

### 4.5 完整 coverage 审计

| 子任务 Phase 2 | detail_desc | interv_desc | condition | interv_name | brief_title | keyword | design_model | masking_desc |
|---|---|---|---|---|---|---|---|---|
| SAE | **22%** | 100% | 100% | 100% | 100% | 100% | 100% | 100% |
| mortality | **22%** | 100% | 100% | 100% | 100% | 100% | 100% | 100% |
| patient-dropout | **22%** | 100% | 100% | 100% | 100% | 100% | 100% | 100% |
| trial-approval | **49%** | 100% | 100% | 100% | 100% | 100% | **81%** | **60%** |
| trial-failure-reason | 100% | **84%** | 100% | 100% | 100% | 100% | 100% | **54%** |
| trial-duration | **22%** | 100% | 100% | 100% | 100% | 100% | 100% | 100% |

凡是 < ~99% 的 cell 都可能引入此类 artifact。`detailed_description` 在 cumulative sweep 里**第 1 个加入**，所以从 4-token 往后所有 5 个非-failure 子任务的 cumulative 结果都被它污染——**Step 2 的整张 sweep 表作废**。

### 4.6 教训 → 硬规则

```
一个文本列只能给该列实际出现在其 CSV header 里的子任务用；
否则这个子任务就不上这一列（不是"填零"，是不喂进模型）。
```

### 4.7 11 个文本列 × 6 子任务 CSV-存在性矩阵（修正后的正确依据）

| 列 | SAE | mortality | dropout | approval | failure | duration | 子任务数 |
|---|:-:|:-:|:-:|:-:|:-:|:-:|---|
| brief_summary/textblock | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 6/6 |
| brief_title | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 6/6 |
| condition | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 6/6 |
| eligibility/criteria/textblock | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 6/6（已作 incl/excl） |
| intervention/intervention_name | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 6/6 |
| keyword | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 6/6 |
| intervention/description | ✓ | ✓ | ✓ | ✓ | — | ✓ | 5/6 |
| study_design_info/intervention_model_description | ✓ | ✓ | ✓ | — | ✓ | ✓ | 5/6 |
| study_design_info/masking_description | ✓ | ✓ | ✓ | — | — | ✓ | 4/6 |
| detailed_description/textblock | — | — | — | — | ✓ | — | **1/6（only failure）** |
| eligibility/gender_description | — | — | — | — | ✓ | — | 1/6 |

---

## 5. SAE 边际 sweep（干净对比）

应用 §4.6 的规则后，先做 SAE 一个子任务，搞清楚两件事：

1. **每个文本列单独**加入（不是 cumulative）作为第 3 个 virtual token 对 SAE 的边际贡献
2. **MedCPT vs Qwen3-Embedding-8B** 哪个 encoder 更适合临床试验文本

### 5.1 实验设计

- **Base**：tabular 41 列 + incl + excl（IE_embedding 已知：P2 = 0.8752、P3 = 0.9042）
- **每个 col 一次实验**：base + 该 col 单一列 = 3-token Full Step 2，与 base 直接对比
- **两个 encoder 平行对比**：同一列分别用 MedCPT (768-d) 和 Qwen3-Embedding-8B (4096-d) 编码
- **两个 phase**：Phase 2 和 Phase 3 各跑
- **SAE 的 8 个 CSV 内文本列**（按 §4.7，detailed_description 不在 SAE CSV 里 → 直接不测，避免 §4 那种泄漏）
- 共 **8 × 2 × 2 = 32 run**，每个 30 epoch 约 3 min，加 7 个 MedCPT 编码（brief_summary MedCPT 已有），约 90 min 总

runner：`script/run_sae_marginal.sh`，nohup 启动。

### 5.2 完整结果表

| 列 | P2 MedCPT | P2 Qwen | P3 MedCPT | P3 Qwen | encoder 胜方 |
|---|---|---|---|---|---|
| brief_summary | 0.8733 | **0.8787** | 0.9063 | **0.9089** | Qwen 双胜 |
| **brief_title** | 0.8829 | **0.8906** | 0.9070 | **0.9183** | **Qwen 双胜（最强列）** |
| condition | 0.8713 | **0.8777** | **0.9090** | 0.9042 | 平 (P2 Q ↑, P3 M ↑) |
| intervention/description | 0.8697 | 0.8683 | **0.9068** | 0.9025 | 平 / M 微胜 |
| intervention/intervention_name | 0.8755 | **0.8812** | **0.9096** | 0.8993 | 平 (P2 Q ↑, P3 M ↑) |
| keyword | **0.8812** | 0.8720 | 0.8996 | 0.9008 | 平 / M 微胜 |
| study_design intervention_model_description | 0.8741 | **0.8799** | 0.9031 | **0.9101** | Qwen 双胜 |
| study_design masking_description | 0.8778 | **0.8334** ⚠️ | 0.9072 | **0.9111** | 分（P2 Q 没收敛；P3 Q ↑） |

> ⚠️ SAE P2 +masking_desc Qwen 的 best ROC-AUC = initial（epoch −1），30 epoch 训练一直没涨过随机投影 initial 值。单点失败，**MedCPT 16 cell 全部正常收敛**。
>
> Base (2-token): **P2 = 0.8752, P3 = 0.9042**

### 5.3 MedCPT vs Qwen head-to-head（16 cell）

| 结果 | 次数 | 列 / phase |
|---|---|---|
| **Qwen 胜**（Δ ≥ +0.003） | **8** | brief_summary P2, brief_title P2/P3, condition P2, interv_name P2, design_model P2/P3, masking_desc P3 |
| **MedCPT 胜**（Δ ≥ +0.003） | 5 | condition P3, interv_desc P3, interv_name P3, keyword P2, masking_desc P2 |
| 平（\|Δ\| < 0.003） | 3 | brief_summary P3, interv_desc P2, keyword P3 |

**Qwen3-Embedding-8B 略胜 MedCPT (8-5-3)**，差距大多 ±0.01 ROC-AUC 内（噪声量级）。

### 5.4 每列边际贡献（取两 encoder 中较好的 vs base）

| 列 | P2 best Δ | P3 best Δ | 平均 Δ | 评级 |
|---|---|---|---|---|
| **brief_title** | +0.015 (Q) | +0.014 (Q) | **+0.015** | 一致正向，唯一稳定收益列 |
| design_model | +0.005 (Q) | +0.006 (Q) | +0.006 | 两 phase 一致小正向 |
| masking_desc | +0.003 (M) | +0.007 (Q) | +0.005 | P2 小正、P3 涨 |
| interv_name | +0.006 (Q) | +0.005 (M) | +0.005 | 两 phase 各小正（不同 encoder） |
| brief_summary | +0.003 (Q) | +0.005 (Q) | +0.004 | 两 phase 小正 |
| condition | +0.003 (Q) | +0.005 (M) | +0.004 | 微小正 |
| keyword | +0.006 (M) | −0.005 (M) | 0 | 抵消 |
| interv_desc | −0.006 (M) | +0.003 (M) | −0.001 | 基本无效 |

### 5.5 SAE 上的结论

1. **encoder**：Qwen3-Embedding-8B 略胜 MedCPT 但优势很小（8-5-3），绝对差距 ±0.01 内。**Qwen 70 倍参数带来有限提升**——对临床文本，MedCPT（领域预训练）的小尺寸被 domain alignment 弥补。**MedCPT 性价比更高**（编码快 70 倍 + 全部收敛 + 实际差距小），要榨极限选 Qwen
2. **杀手列**：**`brief_title`**（+0.015 一致正向，跨 phase 跨 encoder 都最稳）
3. **小正向群**：design_model / masking_desc / interv_name / brief_summary / condition（+0.003~+0.006）——值得保留但贡献小
4. **基本无效**：keyword / interv_desc——单加进去对 SAE 没用
5. **SAE 整体头部空间小**：base 已是 0.875/0.904，**没有任何单列能再给 +0.02 以上**。SAE 主要靠 tabular + eligibility criteria 已经吃饱了文本信号

---

## 6. 跨实验综合教训

### 6.1 方法论层面（重要）

**虚拟列必须做 coverage 严格过滤**：

```
喂某个 virtual column 给某个子任务 ⟺ 该 column 出现在该子任务 CSV 的 header 里
```

不要用 trial_id overlap 跨子任务"借"embedding——这会把"是否被另一个 benchmark 包含"做成隐式特征，违反临床实践（推理时无法可得），且能虚抬 ROC-AUC 0.10 量级。

### 6.2 SAE 的实证发现

- IE_embedding 的 base（incl + excl）已经把 SAE 的"easy 文本信号"吃完，剩余文本列单独最多 +0.015
- 想再涨需要：
  - **联合多列**（多列互补，可能比单列加总大），但要严格控制 coverage
  - **换更大的 IE 池化方式**（不是 mean-pool 单列，比如 attention pool）
  - **对 patient-dropout / failure-reason 重点投资**——它们对 brief_summary 的反应最大（Step 1 数据），意味着这些任务的"任务设计/流程"信号在 brief_summary 里更密

### 6.3 encoder 选型实务

| 维度 | MedCPT | Qwen3-Embedding-8B |
|---|---|---|
| 参数量 | 109M | 7.57B（70×） |
| 编码速度（1.58M criteria） | ~190s | ~3h |
| 编码 1 列 ~48K texts | ~60s | ~15-20min |
| 输出维度 | 768 | 4096 |
| 投影层参数 (Linear(d, 192)) | 147K | **786K**（5.3×） |
| 训练 stability | 16/16 收敛 | 15/16（1 个未收敛） |
| SAE head-to-head | 5 胜 / 3 平 / 8 输 | **8 胜** / 3 平 / 5 输 |
| 实用推荐 | **大多数情况首选**（性价比高） | 高维度可榨极限场景 |

---

## 7. 当前推荐的最佳 SAE 配置

| 配置 | virtual tokens | ROC-AUC (best across P2/P3 phase) |
|---|---|---|
| TabPFN baseline | 0 | 0.8851 (4-phase combined) |
| Full Step 2 IE base | 2 (incl+excl MedCPT) | P2 0.8752 / P3 0.9042 |
| **+ brief_title (Qwen)** | **3** | **P2 0.8906 / P3 0.9183** |

加 brief_title (Qwen) 是当前 SAE 最干净的提升点（+0.015 平均）。其它列建议在做多列联合 ablation 后再决定是否纳入。

---

## 8. 局限与下一步

1. **本报告只系统跑了 SAE 一个子任务的干净版**。其它 5 个子任务的 per-column 边际 sweep 还没做（pipeline 已通用化，按 SAE 模板换 `--subtask` 即可）
2. **没做多列联合**。SAE 显示单列最多 +0.015，但 `brief_title + design_model + masking_desc` 这种几个小正向组合起来，是否仍正向且互补，未测
3. **trial-duration 的回归是 10-bin 量化伪回归**。严格 bar-distribution regressor 实现没做
4. **Qwen 偶尔不收敛**（SAE P2 +masking_desc）——值得调 lr / 试不同 seed 才能定论 Qwen 是否在小信号列上更脆弱
5. **Step 1 在其它 5 个子任务上的结果是 4-phase combined / partial coverage 设定下的，没按 §4.6 的硬规则核对**。严格说 Step 1 的 patient-dropout +0.030 等结论需要按 per-phase + per-subtask CSV 列存在性重新过一遍才能完全放心（不过 brief_summary 6/6 全覆盖，应当不受 §4 那种 artifact 影响）

---

## 9. 复现指令

```bash
# 激活环境
source /data2/zhu11/miniconda3/etc/profile.d/conda.sh && conda activate tabpfn
cd /data2/zhu11/TB/branch/All_text_embedding

# Step 1：brief_summary MedCPT 3-token sweep
nohup bash script/run_step1.sh > results/step1_log.txt 2>&1 &

# SAE 边际 sweep（干净版：每列单独加，MedCPT vs Qwen）
nohup bash script/run_sae_marginal.sh > results/sae_marginal_log.txt 2>&1 &

# 单个实验：base + 单列
PY=/data2/zhu11/miniconda3/envs/tabpfn/bin/python
D=data
$PY script/full_step2_multi.py \
    --virt-embs "$D/emb_inclusion_medcpt.parquet,$D/emb_exclusion_medcpt.parquet,$D/emb_brief_title_qwen.parquet" \
    --subtask serious-adverse-event-forecasting --target "Y/N" --task-type binary \
    --phases Phase2 --epochs 30 --lr 1e-3 --lr-base 2e-5 --eval-every 3 \
    --ctx-size 3000 --qry-size 500 --unfreeze-decoder
```

每个 run 产物：`results/fs2multi_<subtask>_<target>_<phase>_<timestamp>/metrics.json`，含 best_metrics、history、virt_embs、args 等完整信息。

---

**报告版本**：2026-05-22
**数据**：TrialBench v1（[Zenodo record 15455785](https://zenodo.org/record/15455785)），各子任务 Phase 2 / Phase 3 官方 train/test 划分
**硬件**：NVIDIA H200 NVL (143 GB)，CUDA 13.2
**TabPFN**：v7.1.1（editable install），ckpt `tabpfn-v2.5-classifier-v2.5_default.ckpt`
**MedCPT**：`ncbi/MedCPT-Article-Encoder`（109M）
**Qwen**：`Qwen/Qwen3-Embedding-8B`（7.57B，4096-d）
