# branch/aggregate — 终态文档（final_readme）

> 终态文档，cold-read 5 分钟拿结论。过程/完整数字见 [`README.md`](README.md)。
> 进入本目录前先看 [`/data2/zhu11/TB/ReadMeFirst.md`](../../ReadMeFirst.md)；branch 规约见 [`../README.md`](../README.md)。

---

## 1. TL;DR

**把所有非 tabular 信号源（I + E + 9 个文本列 Qwen3 + SMILES = 12 个 virtual token）一次性塞进冻结的 TabICLv2，在 SAE 上不如只用 I+E（2 token）。** 堆 token 没有稳健增益：Phase2 加文本反而略负（p=0.065），Phase3 全在噪声内。**I+E 是甜点位**——eligibility criteria 已把 SAE 的可提取文本信号吃满，其余 9 文本列 + SMILES 边际信息为零甚至负（11 个随机初始化投影稀释冻结 base，5.87M 可训练参数是 B' 的 5.6× 却没换来增益）。

又一次验证多-seed 教训：n=5 时 Phase3 看着边际正（+0.007~+0.010, p≈0.09），**n=10 塌回 ~0**。

---

## 2. 结果（last5 ROC-AUC, mean±std, n=10 seed, 配对 t vs B'）

| | Phase2 Δ vs B' (p) | Phase3 Δ vs B' (p) |
|---|---|---|
| B' (I+E, 2 tok) | 0.8585 ± 0.0054 | 0.8851 ± 0.0094 |
| +all text (11 tok) | −0.0053 (0.065) | +0.0002 (0.945) |
| ALL +SMILES (12 tok) | −0.0014 (0.471) | +0.0026 (0.485) |

数据：[`results/multiseed_20260602_033240/`](results/multiseed_20260602_033240/)（`summary.md` + `raw_runs.jsonl` 60 行）。

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

## 7. 下一步建议

- **默认方案就用 I+E**（2 token），简洁且性价比最高。不建议为 SAE 堆 all-text/SMILES。
- 若要再榨 SAE：把 **MedCPT-MeSH（mesh branch 的 winner）** 并进这个多-token 框架单独验证（本 branch 没含），或转向**结构化药物属性**（ATC/给药途径）而非高维文本 embedding。
- all-text 对**其他 subtask**可能有用：[`../All_text_embedding/`](../All_text_embedding/) Step1 单次发现 brief_summary 明显帮 patient-dropout / failure-reason。本 branch 的"无用"结论是 **SAE-specific**。值得把这个多-token + 多-seed 框架扩到那些 subtask 复跑（它们的单次结论也该补误差棒）。

---

## 8. 关键产物索引

| 产物 | 路径 | 说明 |
|---|---|---|
| 多-token TabICL 训练 | `script/full_step2_tabicl_multi.py` | 任意 N 源, `path@TYPE`, 统一 loader |
| SAE 子集构建 | `script/subset_sae.py` | 源 parquet → SAE-only fp16 本地副本 |
| 多-seed + 配对 t | `script/run_multiseed_aggregate.py` | `--cells/--seed-start/--append-to` |
| 源 embedding（子集, git-ignored） | `data/{ie_embeddings_qwen3,smiles_embeddings_molformer,emb_*_qwen}.parquet` | 由 subset_sae.py 重建 |
| 结果 | `results/multiseed_20260602_033240/` | summary.md + raw_runs.jsonl (60 行) |
| 进度日志 | `README.md` §5 | 结果 + caveat |
