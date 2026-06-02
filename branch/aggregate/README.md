# branch/aggregate — 所有信号源一起塞进 TabICLv2

> 进入本目录前请先看 [`/data2/zhu11/TB/ReadMeFirst.md`](../../ReadMeFirst.md)；branch 规约见 [`../README.md`](../README.md)。

## 1. TL;DR

把前面几条 branch 探索过的**全部非 tabular 信号源**，一次性作为 virtual feature token 注入冻结的 **TabICLv2**，在 SAE 上看"全都加进来"的效果：

- **I, E**（eligibility inclusion/exclusion criterion，Qwen3-Embedding-8B 4096-d）
- **SMILES**（药物分子结构，MolFormer-XL 768-d —— SMILES 单独在 SAE 已证明无用，这里作"全加"的一员，选 MolFormer 作代表）
- **all text**（All_text_embedding branch 的 **9 个 TrialBench 文本列**，Qwen3 4096-d）：brief_summary / brief_title / condition / detailed_description / intervention_description / intervention_name / keyword / study_design_info(intervention_model_description, masking_description)

合计 **2 + 1 + 9 = 12 个 virtual token**。base TabICL（27.6M）全冻结，只训 12 个 `Linear(d_i, 128)` 投影 + `col_emb(12,128)` ≈ **5.87M 可训练参数**。

## 2. 对照 cell（SAE, binary Y/N, Phase2/3）

| Cell | token | 含义 |
|---|---|---|
| **B'** | 2 (I+E) | baseline，跟 smiles/mesh branch 的 B' 同配置 |
| **+text** | 11 (I+E+9text) | 加全部文本列，看文本整体贡献 |
| **ALL** | 12 (I+E+9text+SMILES) | 全都加，本 branch 核心 |

SMILES-only（I+E+SMILES）已在 [`../smiles/`](../smiles/) 多-seed 测过（无稳健增益），不重跑。

## 3. 方法

- 架构 = Full Step 2 虚拟列注入（col_embedder 后、row_interactor 前 cat N 列），fork 自 [`../mesh/script/full_step2_tabicl_mesh.py`](../mesh/script/full_step2_tabicl_mesh.py) 注入机制 + [`../All_text_embedding/script/full_step2_multi.py`](../All_text_embedding/script/full_step2_multi.py) 的 N 列设计。
- 统一 loader 兼容三种 parquet 格式：宽表 `emb_0..emb_{d-1}`（All_text）/ list 列 `mean_emb`（SMILES）/ list+type（I/E 用 `path@I`、`path@E` 切片）。
- **多-seed + 配对 t 检验 + last5 指标**（沿用 smiles 发现的 CUDA 非确定性教训：单次 run 不可信）。
- 复现命令见 §6。

## 4. 关键超参 / 环境

跟 smiles/mesh 一致：`epochs=30, lr=1e-3, ctx=2000, qry=500, AdamW, eval_every=2`。env `conda activate tabpfn`。I/E、SMILES、9 个 text parquet 全部 symlink 复用各源 branch（见 `data/`），不重编。

## 5. 结果

**多-seed last5 ROC-AUC（mean ± std），配对 t 检验 vs B'。Phase2/3 各 n=10 seed。**
来源：[`results/multiseed_20260602_033240/summary.md`](results/multiseed_20260602_033240/summary.md) + `raw_runs.jsonl`（60 行）。

### Phase 2

| Cell | tokens | 可训练参数 | last5 ROC-AUC | Δ vs B' | p (配对) |
|---|---|---|---|---|---|
| B' (I+E) | 2 | 1.05M | 0.8585 ± 0.0054 | — | — |
| +all text | 11 | 5.77M | 0.8532 ± 0.0066 | −0.0053 | 0.065 |
| ALL (+SMILES) | 12 | 5.87M | 0.8571 ± 0.0065 | −0.0014 | 0.471 |

### Phase 3

| Cell | tokens | 可训练参数 | last5 ROC-AUC | Δ vs B' | p (配对) |
|---|---|---|---|---|---|
| B' (I+E) | 2 | 1.05M | 0.8851 ± 0.0094 | — | — |
| +all text | 11 | 5.77M | 0.8854 ± 0.0075 | +0.0002 | 0.945 |
| ALL (+SMILES) | 12 | 5.87M | 0.8878 ± 0.0101 | +0.0026 | 0.485 |

### 结论

1. **把 12 个 token 全堆上不如只用 I+E（2 token）**。Phase2 加文本反而略降（+text p=0.065），Phase3 全在噪声内（p>0.48）。5.87M 可训练参数（B' 的 5.6×）没换来任何稳健增益。
2. **n=5 的假象**：n=5 时 Phase3 +text/ALL 看着边际正（+0.007~+0.010, p≈0.085~0.10），**加到 n=10 后塌回 ~0**（+0.0002 / +0.0026）。又一次印证 smiles 发现的教训——小样本 + best/单次会骗人，必须多-seed + last5 + 配对 t。
3. **I+E 是甜点位**：eligibility criteria 已经把 SAE 可提取的文本信号吃满；再加 brief_summary / condition / intervention / keyword / … 9 列 + SMILES，边际信息为零甚至负（11 个随机初始化投影稀释冻结 base）。
4. **ALL(12) 略好于 +text(11)**（两 phase 都是，Phase2 −0.0014 vs −0.0053；Phase3 +0.0026 vs +0.0002）——把 SMILES 加回去反而把"过多文本"的轻微拖累拉回一点，但都在噪声内，不可解读。

### ⚠️ 重要 caveat：这跟 mesh branch 不矛盾

本 branch 的 `condition` / `intervention_name` 是 **All_text 的原始文本经 Qwen3** 编码；而 [`../mesh/`](../mesh/) 的小幅 Phase2 增益（MedCPT MeSH +0.0046, p=0.039）来自 **MeSH 受控词表术语经 MedCPT** 编码——**两种是不同的东西**。本 branch 说明"把那些字段当普通 Qwen3 文本堆进去没用"，不否定"MeSH-term-via-MedCPT 有小幅作用"。aggregate **没有**包含 mesh 的那个 winner（用户只要 I/E/SMILES/all-text-Qwen3）。要进一步榨，可把 MedCPT-MeSH 也并进来单独测。

## 6. 复现

```bash
source /data2/zhu11/miniconda3/etc/profile.d/conda.sh && conda activate tabpfn
cd /data2/zhu11/TB/branch/aggregate
# data/ 下的 parquet 都是 symlink 到 smiles / All_text branch；若缺，先在那两个 branch 生成
python script/run_multiseed_aggregate.py --phases Phase2,Phase3 --seeds 5 --epochs 30
# 关键 cell 补 seed 到 n=10（Phase2）：
python script/run_multiseed_aggregate.py --phases Phase2 --seed-start 5 --seeds 5 \
    --append-to results/multiseed_<时间戳>
```

## 7. 关键产物

| 产物 | 路径 |
|---|---|
| 多-token TabICL 训练脚本 | `script/full_step2_tabicl_multi.py`（`--virt-embs` 任意 N 源, `path@TYPE` 语法）|
| 多-seed driver + 配对 t | `script/run_multiseed_aggregate.py` |
| 源 embedding（symlink） | `data/{ie_embeddings_qwen3,smiles_embeddings_molformer,emb_*_qwen}.parquet` |
| 结果 | `results/multiseed_*/summary.md` + `raw_runs.jsonl` |
