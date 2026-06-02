# branch/All_text_embedding — All Text Columns as Virtual Tokens

> 进入本目录前请先看 [`/data2/zhu11/TB/ReadMeFirst.md`](../../ReadMeFirst.md)。

本 branch 是 [`branch/IE_embedding`](../IE_embedding) 的延续。IE_embedding 只把 `eligibility/criteria/textblock`（inclusion + exclusion）注入 TabPFN。本 branch 把 **TrialBench 里所有文本列**都编码成 embedding，每列形成一个 virtual token 拼进 TabPFN，逐列加入观察增量增益。

---

## 1. 实验背景

TrialBench 论文 baseline 用 5 个 modality（tabular / text / SMILES / MeSH / ICD）。IE_embedding 的 Full Step 2 只用了 tabular（TabPFN 原生）+ 1 个文本列（eligibility/criteria）。本 branch 把剩下的文本列补齐。

复用 IE_embedding 的"虚拟特征列注入"架构：每个文本列 → embedding → `Linear(d, 192)` 投影 → 1 个 virtual token → concat 进 TabPFN 的 token 序列。冻结 TabPFN 主体，只训投影层 + decoder head。详见 [`Doc/results/IE_embedding_full_step2.md`](../../Doc/results/IE_embedding_full_step2.md)。

---

## 2. 三步实验计划

| Step | 内容 | encoder |
|---|---|---|
| **Step 1** | 加 `brief_summary/textblock` 作第 3 个 virtual token（incl / excl / summary） | MedCPT-Article-Encoder（768-d） |
| **Step 2** | 其它文本列按重要度逐个加入，每列 1 个 virtual token，看每列的增量增益 | Qwen3-Embedding-8B（专用 embedding 模型，4096-d） |
| **Step 3** | 把 incl / excl / summary 的 encoder 从 MedCPT 换成 Qwen3-Embedding-8B，看是否有增益 | Qwen3-Embedding-8B |

**Step 2 文本列重要度顺序**（逐个加）：
`detailed_description/textblock` → `intervention/description` → `condition` → `intervention/intervention_name` → `brief_title` → `keyword` → `study_design_info/intervention_model_description` → `study_design_info/masking_description`

---

## 3. 约定

- **编码范围**：只编码 6 个子任务 Phase 2 / Phase 3 的 train + test 实际用到的 trial（去重），不编全部 81K trial
- **列表型字段**（keyword / condition / intervention_name 等多值）：拼成一个字符串编码一次 → 1 个 virtual token
- **缺失值**：trial 该列为空 → 用零向量
- **评测**：Phase 2 和 Phase 3 各子任务独立训练 + 评估，跟 IE_embedding / 论文 Table 6 对齐
- **对照基线**：IE_embedding 的 Full Step 2（2 个 virtual token：incl/excl）

---

## 4. 目录结构

```
branch/All_text_embedding/
├── README.md            ← 本文件（同时是实验记录，逐步更新）
├── data/                ← 每个文本列的 per-trial embedding parquet
│   └── emb_<column>_<encoder>.parquet  (trial_id, phase, emb_0..emb_{d-1})
├── script/              ← 本 branch 脚本
└── results/<run_id>/     ← 训练 / 评估产物
```

---

## 5. 现状速览（保持更新）

- ✅ Step 1 完成：brief_summary（MedCPT）作第 3 个 virtual token。8/12 正，patient-dropout / failure-reason 明显受益，详见 §6.1
- ⏳ Step 2 待开始：Qwen3-Embedding-8B 逐列加入其它文本列

---

## 6. 实验结果

（结果跑出来后逐步填入此节）

### Step 1: + brief_summary (MedCPT)

**做法**：在 IE_embedding 的 2-token Full Step 2（incl / excl）基础上，加 `brief_summary/textblock` 作第 3 个 virtual token，全部 MedCPT 编码。6 子任务 × {Phase2, Phase3} = 12 run，30 epoch，与 2-token baseline 完全同 setup（仅多 1 个虚拟列）。

**结果**（3-token vs IE_embedding 的 2-token Full Step 2）：

| Subtask | Phase | metric | 2-token | 3-token (+summary) | Δ |
|---|---|---|---|---|---|
| serious-adverse-event | P2 | ROC-AUC | 0.8752 | 0.8781 | +0.0029 |
| serious-adverse-event | P3 | ROC-AUC | 0.9042 | 0.9035 | −0.0007 |
| mortality | P2 | ROC-AUC | 0.9042 | 0.9012 | −0.0030 |
| mortality | P3 | ROC-AUC | 0.8718 | 0.8761 | +0.0043 |
| patient-dropout | P2 | ROC-AUC | 0.7481 | **0.7783** | **+0.0302** |
| patient-dropout | P3 | ROC-AUC | 0.8494 | 0.8532 | +0.0038 |
| trial-approval | P2 | ROC-AUC | 0.8377 | 0.8324 | −0.0053 |
| trial-approval | P3 | ROC-AUC | 0.8186 | 0.8277 | +0.0091 |
| trial-failure-reason | P2 | macro-F1 | 0.3151 | **0.3318** | **+0.0167** |
| trial-failure-reason | P3 | macro-F1 | 0.3320 | **0.3700** | **+0.0380** |
| trial-duration | P2 | R² | 0.2679 | 0.2312 | −0.0367 |
| trial-duration | P3 | R² | 0.1738 | **0.2490** | **+0.0752** |

**正/负**：8/12 正，4/12 负。

**关键观察**：
- **patient-dropout 明显受益**（P2 +0.030，P3 +0.004）。这是之前 2-token 的一致弱点（P2 才 0.7481，连 SOTA 0.7738 都没过）；加 brief_summary 后 P2 跳到 0.7783 **反超 SOTA**。合理——dropout 由试验流程/设计驱动，brief_summary 正是描述试验设计的，比 eligibility criteria 更对口
- **trial-failure-reason 明显受益**（P2 +0.017，P3 +0.038）。brief_summary 描述试验本身，跟"失败原因"强相关
- **SAE / mortality / trial-approval 基本持平**（±0.005 噪声内）。这些任务 eligibility criteria 已经够用，summary 边际信息有限
- **trial-duration 高方差**（P2 −0.037，P3 +0.075）—— 10-bin 量化回归本身不稳定，加一列噪声放大了波动，单看不能下结论

**小结**：brief_summary 是值得加的——它专门"救"了 criteria 单独搞不定的任务（dropout、failure-reason），对 criteria 已经够用的任务（SAE、mortality）是中性。trial-duration 太吵，需要更稳的回归实现才能判断。下一步 Step 2 起把 incl/excl/summary 之外的文本列逐列加入。

### Step 2: 其它文本列 (Qwen3.5-9B)

待跑。

### Step 3: incl/excl/summary 换 Qwen3.5-9B

待跑。
