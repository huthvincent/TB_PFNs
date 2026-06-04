# branch/smiles — 终态文档（final_readme）

> 终态文档，给 cold-read 的人 5 分钟拿到结论。过程/试错/完整进度见 [`README.md`](README.md) §11。
> 进入本目录前先看 [`/data2/zhu11/TB/ReadMeFirst.md`](../../ReadMeFirst.md)；branch 规约见 [`../README.md`](../README.md)。

---

## 1. TL;DR

固定 TabICLv2，baseline = **tabular + I/E**（Qwen3 编 I/E）。把药物 **SMILES 作 1 个额外 virtual token**（共 3 token），4 个化学 encoder × **5 task × Phase 1–3** 全面评估（**§2 主结果**）。

- **SMILES 整体很弱、多数在噪声内甚至净负**：跨 15 个 task×phase，最好的 **ChemBERTa-MTR** 平均才 +0.0035（win 60%），**MolFormer 净负**（−0.0041, win 27%）。**远弱于 MeSH**（最强 BioLORD +0.0105 / win 80%，见 [`../mesh/final_readme.md`](../mesh/final_readme.md)）。
- **唯一一致正的格子：trial-failure-reason Phase2/3**（ChemBERTa-MTR +0.039 P3、Mol2Vec +0.039 P3）。trial-duration Phase3 反而多为负（跟 MeSH 相反）。
- **覆盖率只 ~50%**（很多 trial 无药物 SMILES）严重稀释信号；SAE/mortality/Phase1 多在噪声内。
- **要药物信息，MeSH（药物受控术语）比 SMILES（分子结构）有效得多**。SMILES 不建议作为默认增强（除 failure-reason 外）。

> 方法论（来自 SAE 专项 §3）：TabICL Full-Step-2 是 **CUDA 非确定性**的（单次噪声底 ±0.005–0.01）。本 grid 是单 seed 点估计（用户要求不做多-seed），|Δ|<~0.01 在噪声内 —— 看跨 task/phase 的**模式**，确有信号的格子（failure-reason P2/3）建议补多-seed 坐实。SAE 专项的多-seed + 配对 t 详见 §3。
>
> **附带**：用 **Qwen3-Embedding-8B** 编 I/E（`data/ie_embeddings_qwen3.parquet`，全 trial）是项目统一 baseline；SAE 最终方案仍是 [`../new_FM/final_readme.md`](../new_FM/final_readme.md) 的 **TabICLv2 + I/E**。

---

## 2. 全面 SMILES 评估（5 任务 × Phase 1–3）★ 主结果

固定 TabICLv2，**baseline = tabular + I/E**（Qwen3-Embedding-8B, 2 virtual token）。每个 SMILES 列把药物 **SMILES 作 1 个额外 virtual token**（共 3 token；mean-pool 一个 trial 的多条 SMILES），用对应化学 encoder 编码。5 个 task × Phase 1–3，**单 seed**（seed=0），指标 = 末 5 eval-epoch primary metric 均值。Δ = SMILES − baseline（同 cell）。粗体 = 该行最佳 encoder。
数据：`results/smiles_grid_20260604_111257/grid.json`；脚本 `script/smiles_eval_grid.py` + `script/render_grid_smiles.py`。

> ⚠️ **单 seed 点估计**，噪声底 ~±0.005–0.010，|Δ|<~0.01 在噪声内 —— 看跨 phase/task 的**模式**。SMILES 覆盖率只 ~50%（很多 trial 无药物 SMILES）→ 信号被稀释，见 cov 列。

### serious-adverse-event (binary, ROC-AUC)

| Phase | baseline (tab+I/E) | SMILES cov | +ChemBERTa-MLM Δ | +ChemBERTa-MTR Δ | +MolFormer Δ | +Mol2Vec Δ |
|---|---|---|---|---|---|---|
| Phase1 | 0.8807 | 48% | -0.0010 | -0.0044 | **+0.0027** | -0.0041 |
| Phase2 | 0.8601 | 53% | -0.0021 | **+0.0046** | -0.0000 | +0.0015 |
| Phase3 | 0.8874 | 50% | **+0.0051** | +0.0039 | -0.0039 | +0.0015 |

### mortality-event (binary, ROC-AUC)

| Phase | baseline (tab+I/E) | SMILES cov | +ChemBERTa-MLM Δ | +ChemBERTa-MTR Δ | +MolFormer Δ | +Mol2Vec Δ |
|---|---|---|---|---|---|---|
| Phase1 | 0.9288 | 48% | -0.0134 | -0.0049 | -0.0041 | **+0.0042** |
| Phase2 | 0.8936 | 53% | **+0.0114** | +0.0021 | -0.0021 | -0.0033 |
| Phase3 | 0.8747 | 50% | -0.0033 | **+0.0065** | -0.0009 | -0.0056 |

### patient-dropout (binary, ROC-AUC)

| Phase | baseline (tab+I/E) | SMILES cov | +ChemBERTa-MLM Δ | +ChemBERTa-MTR Δ | +MolFormer Δ | +Mol2Vec Δ |
|---|---|---|---|---|---|---|
| Phase1 | 0.7049 | 48% | **+0.0224** | +0.0056 | -0.0050 | +0.0105 |
| Phase2 | 0.7690 | 58% | **+0.0008** | -0.0121 | -0.0165 | -0.0064 |
| Phase3 | 0.8428 | 54% | -0.0092 | -0.0075 | -0.0096 | -0.0075 |

### trial-duration (regression, R²)

| Phase | baseline (tab+I/E) | SMILES cov | +ChemBERTa-MLM Δ | +ChemBERTa-MTR Δ | +MolFormer Δ | +Mol2Vec Δ |
|---|---|---|---|---|---|---|
| Phase1 | 0.4907 | 34% | -0.0068 | -0.0100 | -0.0213 | -0.0145 |
| Phase2 | 0.2458 | 44% | +0.0082 | **+0.0149** | +0.0070 | +0.0024 |
| Phase3 | 0.2419 | 44% | -0.0238 | **+0.0080** | -0.0227 | -0.0452 |

### trial-failure-reason (multiclass, macro-F1)

| Phase | baseline (tab+I/E) | SMILES cov | +ChemBERTa-MLM Δ | +ChemBERTa-MTR Δ | +MolFormer Δ | +Mol2Vec Δ |
|---|---|---|---|---|---|---|
| Phase1 | 0.3293 | 43% | -0.0010 | -0.0115 | -0.0079 | -0.0120 |
| Phase2 | 0.3445 | 58% | +0.0166 | **+0.0186** | +0.0035 | +0.0097 |
| Phase3 | 0.3378 | 55% | +0.0114 | **+0.0391** | +0.0192 | +0.0386 |

### 全局汇总（15 个 task×phase cell）

| Encoder | mean Δ | median Δ | win-rate (Δ>0) | #cells Δ>+0.01 | #cells Δ<−0.01 |
|---|---|---|---|---|---|
| ChemBERTa-MLM | +0.0010 | -0.0010 | 47% (7/15) | 4 | 2 |
| **ChemBERTa-MTR** | **+0.0035** | **+0.0039** | **60% (9/15)** | 3 | 3 |
| MolFormer | −0.0041 | −0.0039 | 27% (4/15) | 1 | 3 |
| Mol2Vec | −0.0020 | −0.0033 | 47% (7/15) | 2 | 3 |

### 结论（全面 grid）

1. **SMILES 整体很弱、不稳**：最好的 **ChemBERTa-MTR** 平均才 +0.0035（win-rate 60%），**MolFormer 净负**（−0.0041, 27% win，多数 cell 拖累）。远弱于 MeSH（最强 BioLORD +0.0105 / 80%，见 [`../mesh/final_readme.md`](../mesh/final_readme.md) §2）。
2. **唯一一致正的格子：trial-failure-reason Phase2/3**（ChemBERTa-MTR +0.019 P2 / **+0.039 P3**、Mol2Vec +0.039 P3、MolFormer +0.019 P3）。分子结构可能跟"安全性失败"类别相关。
3. **trial-duration Phase3 多为负**（MolFormer −0.023、Mol2Vec −0.045）——跟 MeSH 相反（MeSH 在 duration P3 是大赢家）。SMILES 抓不到试验时长信号。
4. **Phase1 普遍负**（小数据 + SMILES 覆盖更低，duration P1 只 34%）。
5. **覆盖率只 ~50%**（vs MeSH condition 95% / intervention 67%）严重稀释信号——~一半 trial 没有药物 SMILES 喂的是零向量。
6. **结论：SMILES 不是有用的额外信号源**（除 failure-reason 外）。要药物信息，MeSH（药物受控术语）比 SMILES（分子结构）有效得多——印证 SAE 专项的发现：缺的是**药物身份/适应症语义**而非**分子结构**。

> 单 seed caveat：点估计，|Δ|<~0.01 在噪声内。failure-reason P2/3 是值得补多-seed 坐实的格子。

---

## 3. 候选对比（pk 掉了什么）

### 3.1 SMILES encoder（4 个全测，无显著差异）

| Encoder | HF / 来源 | d | Phase2 Δ vs B'(last5) | Phase3 Δ vs B'(last5) | 砍掉原因 |
|---|---|---|---|---|---|
| ChemBERTa-77M-MLM | `DeepChem/ChemBERTa-77M-MLM` | 384 | +0.0020 | −0.0067 | Phase3 显著退化 |
| ChemBERTa-77M-MTR | `DeepChem/ChemBERTa-77M-MTR` | 384 | +0.0027 | −0.0038 | 噪声内 / 略负 |
| MolFormer-XL | `ibm/MoLFormer-XL-both-10pct` | 768 | −0.0007 | −0.0009 | 中性（最不伤），但无增益 |
| Mol2Vec | gensim w2v `model_300dim.pkl` | 300 | +0.0029 | −0.0027 | 噪声内 / 略负 |

> 噪声底 std≈0.0033–0.0039（last5, n=5）。所有 |Δ| 要么小于各 cell 自身 std，要么（Phase3 ChemBERTa-MLM）为显著负。**没有任何 encoder 给出稳健正增益**。换 encoder 救不了——问题在信号本身。

### 3.2 为什么 SMILES 在 SAE 上没用

- **Cell D（仅 SMILES 非空子集，剔除 ~46% 缺失）也没翻盘**：C 在子集上仍 ≈ B' 或更差。→ 不是"缺失稀释"问题，是 SMILES 对 SAE 真没有 tabular+I/E 之外的增量信号。
- 严重不良事件率主要由 **试验设计 / 人群 / 给药方式**驱动，这些已被 tabular 列 + I/E 文本吃掉；分子结构的边际贡献被淹没。
- 印证 [`../new_FM/README.md`](../new_FM/README.md) patient-dropout 的发现：base 冻结、信号已满时，多加一个随机初始化的 trainable projection 只会扰动表征、轻微跑偏。

### 3.3 I/E encoder：Qwen3 vs 旧 MedCPT

| Phase | 旧 MedCPT +IE (768-d, §3) | Qwen3 B' best (4096-d, multiseed) | 判定 |
|---|---|---|---|
| 2 | 0.8658 | 0.8656 ± 0.0059 | 持平 |
| 3 | 0.9078 | 0.9150 ± 0.0051 | Qwen3 略好 +0.007 |

→ 换 Qwen3 不亏，且跟项目其他 branch 统一栈。

---

## 4. 接入方式（代码层面怎么用）

**基础架构**：fork 自 [`../new_FM/script/full_step2_tabicl.py`](../new_FM/script/full_step2_tabicl.py)，扩成 2 or 3 virtual feature column 注入 TabICL（在 `col_embedder` 与 `row_interactor` 之间 cat 虚拟列）。冻结 27.6M base，只训 projection + col_emb（2 token ~1.05M，3 token ~1.1M）。

```python
# 训练脚本：full_step2_tabicl_smiles.py
# Cell B' (+I+E only, 2 virtual tokens):
python script/full_step2_tabicl_smiles.py --phase Phase2 --epochs 30 --seed 0
# Cell C (+I+E+SMILES, 3 virtual tokens):
python script/full_step2_tabicl_smiles.py --phase Phase2 --epochs 30 --seed 0 \
    --smiles-emb data/smiles_embeddings_molformer.parquet
# Cell B' 但报 SMILES 子集指标（不注入 SMILES，仅用 mask）:
python script/full_step2_tabicl_smiles.py --phase Phase2 --epochs 30 --seed 0 \
    --report-subset-emb data/smiles_embeddings_chemberta_mlm.parquet
```

- `--ie-emb` 默认 `data/ie_embeddings_qwen3.parquet`；d_ie / d_smiles 从 parquet 自动探测，无需改代码换 encoder。
- embedding 复用：I/E 与 SMILES 都按 `(trial_id, phase)` 对齐，缺失填零向量。

**关键：多-seed 才可信**。单次 run 不要信。用 `run_multiseed.py` 跑 N seed，`aggregate_robust.py` 出 mean±std + last5 收敛指标。

---

## 5. 已知坑

1. **CUDA 非确定性**（最重要）：TabICL Full-Step-2 同配置同 seed 跑 3 次 → 0.8655/0.8724/0.8748。噪声底 best≈±0.009、last5≈±0.004。**结论必须建立在多-seed mean±std 上**，单次 Δ<0.01 是噪声。
2. **best-epoch 指标有 max-噪声偏置**：best (取 ~15 个含噪 eval 的 max) 比 last5 收敛值系统性高 ~0.011。报数优先用 **last5**（末 5 epoch 均值）；引用 §3 旧表时才用 best 对齐。
3. **`smiless` 在 `sae_finetune.preprocess` 的 `TEXT_DROP` 里**：SMILES encoding 必须从原始 `train_x.csv` 读，不能用 preprocess 后的 X。（已在 `encode_smiles_*.py` 正确处理）
4. **MolFormer init 在 CPU 做 QR 分解，bf16 报错** (`geqrf_cpu not implemented for BFloat16`)：必须 **fp32 加载 → 移 GPU → 再 cast bf16**。
5. **mol2vec 0.2.2 依赖 gensim 3.x API** (`model.wv.vocab`)，与装的 gensim 4.4 不兼容：在 `encode_smiles_mol2vec.py` inline 重写了 `sentences2vec`（modern `key_to_index`，行为等价 = 每分子 SUM token 向量）。需要预训练 `data/model_300dim.pkl`（74 MB，从 mol2vec GitHub 下）。
6. **torchvision 0.26 与 torch 2.9.1 不兼容**（`torchvision::nms` 注册失败，波及 transformers lazy import）：直接卸掉 torchvision（项目不用）。
7. **Qwen3 全量 encoding ~68 min / 1.58M criteria**：`encode_ie_qwen3.py` 已内置 checkpoint/resume（memmap 实时写 + 每 50 batch 落 state），中断用 `--resume <run_dir>` 续跑。
8. **Mol2Vec norm 跟分子大小强相关**（SUM 非 MEAN，norm 124±92），其余 encoder norm 小而稳；projection 是 Linear 无 bias，能自适应 scale，但留意。

---

## 6. 关键实验数据

完整 mean±std 表（last5 / best / final 三套指标）：
- [`results/multiseed_20260602_002504/robust_summary.md`](results/multiseed_20260602_002504/robust_summary.md)
- [`results/multiseed_20260602_002504/summary.md`](results/multiseed_20260602_002504/summary.md)（best-epoch 版）
- 每个 run 原始数：`results/multiseed_20260602_002504/raw_runs.jsonl`（50 行）+ 各 `results/full_step2_tabicl_smiles_*/metrics.json`

最终结论表（last5, mean±std over 5 seeds）见 [`README.md`](README.md) §11 2026-06-02 段。一句话：Phase2 SMILES Δ∈[−0.001,+0.003] 全在噪声内；Phase3 Δ∈[−0.007,−0.001] 略负。

---

## 7. 复现命令

```bash
source /data2/zhu11/miniconda3/etc/profile.d/conda.sh && conda activate tabpfn
cd /data2/zhu11/TB/branch/smiles

# 1. I/E embedding（Qwen3, ~68 min；可 --resume <run_dir> 续跑）
python script/encode_ie_qwen3.py --batch-size 128 --checkpoint-every 50

# === 全面 grid（§2 主结果）: 5 task × Phase1-3 × 5 cell ===
TASKS="serious-adverse-event-forecasting,mortality-event-prediction,patient-dropout-event-forecasting,trial-duration-forecasting,trial-failure-reason-identification"
# 2a. SMILES embedding 覆盖 5 个 task（--subtasks union；3 HF encoder + mol2vec）
for M in chemberta_mlm chemberta_mtr molformer; do python script/encode_smiles_hf.py --model $M --subtasks "$TASKS"; done
python script/encode_smiles_mol2vec.py --subtasks "$TASKS"   # 需先下 data/model_300dim.pkl
# 2b. 跑 grid（单 seed, ~17 min）+ 渲染
python script/smiles_eval_grid.py
python script/render_grid_smiles.py        # 输出 §2 的 markdown 表

# === SAE 专项（§3）: 多-seed + 配对 t（只 SAE）===
for M in chemberta_mlm chemberta_mtr molformer; do python script/encode_smiles_hf.py --model $M; done   # SAE-only
python script/encode_smiles_mol2vec.py
python script/run_multiseed.py --phases Phase2,Phase3 --seeds 5 --epochs 30
python script/aggregate_robust.py   # 默认取最新 multiseed_* dir
```

env：`torch 2.9.1 / transformers 4.57.6 / tabicl 2.1.1 / rdkit 2026.3.2 / gensim 4.4 / mol2vec 0.2.2`（torchvision 已卸）。

---

## 8. 下一步建议

- **不建议**在 SMILES 上继续调参（lr / epoch / pooling / 多 SMILES 拆 token）——信号本身不足，调参空间是噪声。
- 若仍想榨药物信息，方向是 **结构化药物属性**而非 raw SMILES：ATC 类、给药途径、是否生物制剂、剂量——这些更可能跟 SAE 因果相关，且能做成稳定 tabular 列而非高维 embedding。
- 平行的 [`mesh/`](../mesh/) branch（condition/intervention MeSH 作第 3 token）值得对照：若 MeSH 也无增益，则印证"tabular+I/E 已在 SAE 吃满信号"；若 MeSH 有增益而 SMILES 没有，则说明缺的是**适应症/人群**信息而非**分子**信息。
- **多-seed + last5 协议应推广到本项目所有 Full-Step-2 实验**（包括 new_FM / IE_embedding 的历史单次数，严格说都该补误差棒）。

---

## 9. 关键产物索引

| 产物 | 路径 | 说明 |
|---|---|---|
| I/E Qwen3 embedding | `data/ie_embeddings_qwen3.parquet` | d=4096, 158K groups, 覆盖全 4 phase |
| SMILES embedding ×4 | `data/smiles_embeddings_{chemberta_mlm,chemberta_mtr,molformer,mol2vec}.parquet` | d=384/384/768/300; 覆盖 5 task, 39,642 non-empty |
| mol2vec 预训练权重 | `data/model_300dim.pkl` | 74 MB, gensim w2v |
| SMILES encoding 脚本 | `script/encode_smiles_hf.py`（3 HF, `--subtasks`）/ `script/encode_smiles_mol2vec.py`（`--subtasks`） | |
| **全面 grid（§2 主结果）** | `script/smiles_eval_grid.py` + `render_grid_smiles.py` | in-process, 5 task×3 phase×5 cell, 单 seed |
| 全面 grid 结果 | `results/smiles_grid_20260604_111257/grid.json` | 75 cell raw |
| 训练脚本 | `script/full_step2_tabicl_smiles.py` | 2 or 3 virt token; `--smiles-emb` / `--report-subset-emb` |
| SAE 多-seed driver / 聚合（§3） | `script/run_multiseed.py` / `aggregate_robust.py` | last5/best/final mean±std + Δ vs B' |
| SAE 多-seed 结果（§3） | `results/multiseed_20260602_002504/` | summary / robust_summary / raw_runs.jsonl |
| 进度日志 | `README.md` §11 | 完整心路 + 踩坑 |
