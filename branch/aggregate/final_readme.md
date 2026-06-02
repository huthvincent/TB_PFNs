# branch/aggregate — 终态文档（final_readme）

> 终态文档，cold-read 5 分钟拿结论。过程/完整数字见 [`README.md`](README.md)。
> 进入本目录前先看 [`/data2/zhu11/TB/ReadMeFirst.md`](../../ReadMeFirst.md)；branch 规约见 [`../README.md`](../README.md)。

---

## 1. TL;DR

**SAE Phase 2 的完整 picture（同进程配对, n=10, 见 §2）：**

| 配置 | ROC-AUC | vs tabular | vs tabular+I/E |
|---|---|---|---|
| tabular only | 0.7810 | — | |
| tabular + I/E | 0.8566 | **+0.0756** | — |
| **+ title + intervention_MeSH（最优）** | **0.8658** | **+0.0848** | **+0.0092 (p=0.001)** |
| 全堆 12 token | 0.8530 | +0.0720 | **−0.0036 (p=0.045, 更差)** |

**三个结论：**
1. **I/E 是绝对主力**：tabular→+I/E **+0.0756**，占全部可榨增益的 ~90%。
2. **最优 = `tabular + I/E + brief_title + intervention_MeSH`（4 token）**：在 I+E 上再 +0.0092 (p=0.001)，对 tabular 共 +0.0848。`brief_title` 是最有价值的额外 token；`keyword` 显著有害。
3. **token 不是越多越好**：精选 4 token（最优）> 堆 11 文本 token（稀释回 0）> 全堆 12 token（比 baseline **显著更差**）。冻结 base 上每多一个随机初始化投影都是过拟合风险。

方法论：又一次验证多-seed 必要性（n=5 时 Phase3 全堆看着边际正 p≈0.09，n=10 塌回 0）。zero-shot 确定性（std=0）。

---

## 2. 结果：SAE Phase 2 — 最优 vs suboptimal vs baselines

**所有配置在同一进程、同样 10 个 seed、共享同一个 base 上评估**（TabICL CUDA 非确定性 → 跨 run 绝对值不可比；只有同进程配对才干净）。last5 test ROC-AUC，mean ± std (n=10)。`Δ vs tabular+I/E` 的 p 是配对 t 检验。
数据：[`results/comparison_Phase2_*/summary.md`](results/) + `raw.jsonl`。脚本 `script/comparison_table.py`。

| 配置 | tokens | Phase 2 ROC-AUC | Δ vs tabular | Δ vs tabular+I/E (p) |
|---|---|---|---|---|
| tabular only (zero-shot) | 0 | 0.7810 ± 0.0000 | — | — |
| **tabular + I/E** (baseline) | 2 | 0.8566 ± 0.0052 | **+0.0756** | — |
| + brief_title | 3 | 0.8652 ± 0.0050 | +0.0842 | +0.0086 (p=0.005) *** |
| **+ title + intervention_MeSH（最优）** | 4 | **0.8658 ± 0.0045** | **+0.0848** | **+0.0092 (p=0.001)** *** |
| + condition + intervention MeSH | 4 | 0.8611 ± 0.0027 | +0.0800 | +0.0045 (p=0.050) ** |
| + 全部 9 文本列 | 11 | 0.8551 ± 0.0044 | +0.0740 | −0.0015 (p=0.441) |
| + 9 文本 + SMILES（全堆 12） | 12 | 0.8530 ± 0.0060 | +0.0720 | **−0.0036 (p=0.045) ** 显著更差** |

**读这张表**：
1. **I/E 是绝对主力**：tabular 0.781 → +I/E 0.857，**+0.0756**。其余所有 token 加起来的空间不到这个的 1/8。
2. **最优 = `tabular + I/E + brief_title + intervention_MeSH`（4 token）**：比 tabular+I/E 再 **+0.0092 (p=0.001)**，比纯 tabular **+0.0848**。
3. **brief_title 一个就拿到大部分增量**（+0.0086），再加 intervention_MeSH 只多榨 +0.0006。
4. **suboptimal 们**：condition+intervention MeSH (mesh branch 组合) 只 +0.0045；**全堆 11/12 token 反而把增益稀释掉**——12-token 比 baseline **显著更差 −0.0036 (p=0.045)**。
5. zero-shot std=0.0000：不训练 → 无 CUDA 累加噪声 → 确定性。

> **MeSH encoder 注**：上表 intervention_MeSH 用 MedCPT。换 Qwen3-MeSH（`title+mesh_interv_q3`）增益相当且**跨 phase 更稳**（Phase2 +0.0076 p=0.001、Phase3 +0.0070 p=0.018 都显著；MedCPT 版 Phase3 p=0.14 不显著）。详见 [`../mesh/final_readme.md`](../mesh/final_readme.md)。

> Phase3 全堆主实验（B' vs +text vs ALL，n=10）：+text Δ=+0.0002 (p=0.945)、ALL Δ=+0.0026 (p=0.485)，均不显著；见 `results/multiseed_20260602_033240/`。

---

## 3. SAE 上三条 branch 的统一对比（都在 I+E baseline 之上加东西）

| 加的东西 | 编码 | token 数 | Phase2 最佳 Δ (配对 p) | Phase3 | 判定 |
|---|---|---|---|---|---|
| **(基线) I+E** | Qwen3 4096 | 2 | — | — | 甜点位 |
| SMILES（[`../smiles/`](../smiles/final_readme.md)） | 4 化学 encoder | 3 | mol2vec +0.003 (n.s.) | 平/负 | ❌ 无增益 |
| **MeSH**（[`../mesh/`](../mesh/final_readme.md)） | MedCPT 实体 | 4 | **MedCPT +0.0046 (0.039)** | 平 | ✅ 仅 Phase2 小幅显著 |
| all-text + SMILES（本 branch） | Qwen3 9 列 + MolFormer | 11~12 | −0.0053 (0.065, 略负) | 平 | ❌ 无增益，反稀释 |

**全局结论（SAE）**：
- **I+E 提供绝大部分可提取的非 tabular 信号**（A→B' 见 smiles final_readme：Phase2 +0.042 / Phase3 +0.018）。
- 在 I+E 之上，**唯一能稳健超过噪声的是 MeSH-term-via-MedCPT（Phase2 +0.0046, p<0.05）**，且量很小、只 Phase2。
- **SMILES、原始文本列（Qwen3）、以及把它们全堆上，都没有稳健增益**；堆多了还会因随机初始化投影稀释冻结 base 而略降。
- **token 数不是越多越好**：2 (I+E) > 12 (ALL)。

---

## 4. 为什么"全加"没用（而 mesh 的 MedCPT 有一点用）

- 本 branch 的 `condition` / `intervention_name` 用 **All_text 原始文本 + Qwen3** 编码；mesh 的小幅 winner 是 **MeSH 受控词表术语 + MedCPT**。**不同的编码** → 本 branch 不否定 mesh。aggregate 没纳入 mesh 的 winner（用户只要 I/E/SMILES/all-text-Qwen3）。
- 通用句向量（Qwen3）把一堆描述性文本压成 4096-d，对"严重不良事件率"这种由试验设计/人群/给药驱动的目标，边际信息已被 I+E + tabular 覆盖；再加只是噪声。
- 冻结 base + 多个随机初始化 `Linear(d,128)` 投影：token 越多，越容易在小训练集（SAE ~6.5K）上把这些投影学偏，轻微拖累。

---

## 5. 接入方式

通用多-token TabICL 注入脚本（任意 N 源，每源一 parquet）：

```bash
python script/full_step2_tabicl_multi.py --phase Phase2 --epochs 30 --seed 0 --tag all \
  --virt-embs "data/ie_embeddings_qwen3.parquet@I,data/ie_embeddings_qwen3.parquet@E,\
data/emb_condition_qwen.parquet,...(9 text)...,data/smiles_embeddings_molformer.parquet"
```

- spec 语法：`path` 或 `path@TYPE`（I/E 用 `@I` / `@E` 切 type）。
- 统一 loader 自动判格式：宽表 `emb_0..emb_{d-1}`（All_text）/ list `mean_emb`（SMILES）/ list+type（I/E）。
- 多-seed + 配对 t：`script/run_multiseed_aggregate.py`（`--cells`/`--seed-start`/`--append-to`）。

---

## 6. 已知坑

1. **源 parquet 巨大，按 SAE 子集 + fp16 预切**：原始 I/E 2.5GB + 9 text 2.6GB，每个子进程 run 全量重载 ~5GB，训练本身才 8s → I/O 完全主导。`script/subset_sae.py` 把每源过滤到 SAE Phase2/3 trial + 转 float16（5GB→1.1GB），`data/` 下是这些小子集（**git-ignored，clone 后跑 `subset_sae.py` 重建**）。
2. **多-seed + last5 + 配对 t 是硬要求**：n=5 的 Phase3 边际正 (p≈0.09) 在 n=10 塌成 0。CUDA 非确定性噪声 ±0.005~0.012，比效应大。
3. dtype：投影 fp32、TabICL fp16，cat 前 cast（见脚本 `forward`）。

---

## 7. Token 特征选择（哪些 token 最好）+ 下一步

`script/ablation_search.py`（in-process: 加载所有候选 token + bootstrap 一次，每子集训 8s）。marginal（单 token 边际增益）+ greedy + fixed（指定子集 n=10 确认）三模式。详见 [`README.md`](README.md) §7。

**最优子集 = `I + E + brief_title + intervention_MeSH`（4 token）**：Phase2 +0.0067 (p=0.007 ✦✦✦)，Phase3 +0.0056 (n.s.)。
- `brief_title` 最有价值（两 phase 一致正）；`keyword` 显著有害（两 phase 都负，p<0.05）；其余噪声。
- **token 越多越差**：title+mesh_interv (4) ≫ 6-token（稀释回 0）≫ 12-token（§5 略负）。

下一步：
- **SAE 默认就用 I+E**（性价比）；要榨极致用 `I+E+title+intervention_MeSH`，且把 mesh token 从 MedCPT 换 **Qwen3-MeSH**（mesh branch 后续发现 Qwen3-MeSH > MedCPT，title+mesh_interv 可能再高，待测）。
- all-text 对**其他 subtask**可能有用：[`../All_text_embedding/`](../All_text_embedding/) Step1 发现 brief_summary 明显帮 patient-dropout / failure-reason。本 branch 的"无用"结论是 **SAE-specific**；值得把此 ablation 框架扩到其它 subtask。

---

## 8. 关键产物索引

| 产物 | 路径 | 说明 |
|---|---|---|
| 多-token TabICL 训练 | `script/full_step2_tabicl_multi.py` | 任意 N 源, `path@TYPE`, 统一 loader |
| SAE 子集构建 | `script/subset_sae.py` | 源 parquet → SAE-only fp16 本地副本 |
| 多-seed + 配对 t | `script/run_multiseed_aggregate.py` | `--cells/--seed-start/--append-to` |
| **Token 特征选择** | `script/ablation_search.py` | marginal / greedy / fixed, in-process |
| 源 embedding（子集, git-ignored） | `data/{ie_embeddings_qwen3,smiles_embeddings_molformer,emb_*_qwen}.parquet` | 由 subset_sae.py 重建 |
| 结果（全堆） | `results/multiseed_20260602_033240/` | summary.md + raw_runs.jsonl (60 行) |
| 结果（特征选择） | `results/ablation_{marginal,fixed}_Phase{2,3}_*/` | summary.md |
| 进度日志 | `README.md` §5 (全堆) + §7 (特征选择) | 结果 + caveat |
