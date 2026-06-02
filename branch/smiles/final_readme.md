# branch/smiles — 终态文档（final_readme）

> 终态文档，给 cold-read 的人 5 分钟拿到结论。过程/试错/完整进度见 [`README.md`](README.md) §11。
> 进入本目录前先看 [`/data2/zhu11/TB/ReadMeFirst.md`](../../ReadMeFirst.md)；branch 规约见 [`../README.md`](../README.md)。

---

## 1. TL;DR

**结论：在 SAE（serious-adverse-event-forecasting）上，把 SMILES 药物结构作为第 3 个 virtual feature token 加到 TabICLv2 + I/E 之上，没有稳健增益 —— Phase 2 ≈ 0，Phase 3 轻微为负。这条线不纳入 SAE 最终方案。**

- 测了 4 个化学 encoder（ChemBERTa-MLM / ChemBERTa-MTR / MolFormer-XL / Mol2Vec），全部在噪声内或略负。
- **关键方法论结论**：TabICL 的 Full-Step-2 训练是 **CUDA 非确定性**的，best-epoch ROC-AUC 单次 run 噪声底 ≈ **±0.009**。任何单次 run 的 Δ<0.01 都不可信，必须多-seed。本 branch 的负结论建立在 **5 config × 2 phase × 5 seed = 50 run** 的 mean±std 上。
- **附带正向结论**：用 **Qwen3-Embedding-8B (4096-d)** 重编 I/E embedding，在 I+E（不加 SMILES）上跟旧 MedCPT (768-d) 持平或略好（Phase3 +0.007），可作为项目统一的 I/E encoder。

SAE 最终方案仍是 [`../new_FM/final_readme.md`](../new_FM/final_readme.md) 的 **TabICLv2 + I+E (Full Step 2)**；I/E 建议用 Qwen3 版（`data/ie_embeddings_qwen3.parquet`）。

---

## 2. 候选对比（pk 掉了什么）

### 2.1 SMILES encoder（4 个全测，无显著差异）

| Encoder | HF / 来源 | d | Phase2 Δ vs B'(last5) | Phase3 Δ vs B'(last5) | 砍掉原因 |
|---|---|---|---|---|---|
| ChemBERTa-77M-MLM | `DeepChem/ChemBERTa-77M-MLM` | 384 | +0.0020 | −0.0067 | Phase3 显著退化 |
| ChemBERTa-77M-MTR | `DeepChem/ChemBERTa-77M-MTR` | 384 | +0.0027 | −0.0038 | 噪声内 / 略负 |
| MolFormer-XL | `ibm/MoLFormer-XL-both-10pct` | 768 | −0.0007 | −0.0009 | 中性（最不伤），但无增益 |
| Mol2Vec | gensim w2v `model_300dim.pkl` | 300 | +0.0029 | −0.0027 | 噪声内 / 略负 |

> 噪声底 std≈0.0033–0.0039（last5, n=5）。所有 |Δ| 要么小于各 cell 自身 std，要么（Phase3 ChemBERTa-MLM）为显著负。**没有任何 encoder 给出稳健正增益**。换 encoder 救不了——问题在信号本身。

### 2.2 为什么 SMILES 在 SAE 上没用

- **Cell D（仅 SMILES 非空子集，剔除 ~46% 缺失）也没翻盘**：C 在子集上仍 ≈ B' 或更差。→ 不是"缺失稀释"问题，是 SMILES 对 SAE 真没有 tabular+I/E 之外的增量信号。
- 严重不良事件率主要由 **试验设计 / 人群 / 给药方式**驱动，这些已被 tabular 列 + I/E 文本吃掉；分子结构的边际贡献被淹没。
- 印证 [`../new_FM/README.md`](../new_FM/README.md) patient-dropout 的发现：base 冻结、信号已满时，多加一个随机初始化的 trainable projection 只会扰动表征、轻微跑偏。

### 2.3 I/E encoder：Qwen3 vs 旧 MedCPT

| Phase | 旧 MedCPT +IE (768-d, §3) | Qwen3 B' best (4096-d, multiseed) | 判定 |
|---|---|---|---|
| 2 | 0.8658 | 0.8656 ± 0.0059 | 持平 |
| 3 | 0.9078 | 0.9150 ± 0.0051 | Qwen3 略好 +0.007 |

→ 换 Qwen3 不亏，且跟项目其他 branch 统一栈。

---

## 3. 接入方式（代码层面怎么用）

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

## 4. 已知坑

1. **CUDA 非确定性**（最重要）：TabICL Full-Step-2 同配置同 seed 跑 3 次 → 0.8655/0.8724/0.8748。噪声底 best≈±0.009、last5≈±0.004。**结论必须建立在多-seed mean±std 上**，单次 Δ<0.01 是噪声。
2. **best-epoch 指标有 max-噪声偏置**：best (取 ~15 个含噪 eval 的 max) 比 last5 收敛值系统性高 ~0.011。报数优先用 **last5**（末 5 epoch 均值）；引用 §3 旧表时才用 best 对齐。
3. **`smiless` 在 `sae_finetune.preprocess` 的 `TEXT_DROP` 里**：SMILES encoding 必须从原始 `train_x.csv` 读，不能用 preprocess 后的 X。（已在 `encode_smiles_*.py` 正确处理）
4. **MolFormer init 在 CPU 做 QR 分解，bf16 报错** (`geqrf_cpu not implemented for BFloat16`)：必须 **fp32 加载 → 移 GPU → 再 cast bf16**。
5. **mol2vec 0.2.2 依赖 gensim 3.x API** (`model.wv.vocab`)，与装的 gensim 4.4 不兼容：在 `encode_smiles_mol2vec.py` inline 重写了 `sentences2vec`（modern `key_to_index`，行为等价 = 每分子 SUM token 向量）。需要预训练 `data/model_300dim.pkl`（74 MB，从 mol2vec GitHub 下）。
6. **torchvision 0.26 与 torch 2.9.1 不兼容**（`torchvision::nms` 注册失败，波及 transformers lazy import）：直接卸掉 torchvision（项目不用）。
7. **Qwen3 全量 encoding ~68 min / 1.58M criteria**：`encode_ie_qwen3.py` 已内置 checkpoint/resume（memmap 实时写 + 每 50 batch 落 state），中断用 `--resume <run_dir>` 续跑。
8. **Mol2Vec norm 跟分子大小强相关**（SUM 非 MEAN，norm 124±92），其余 encoder norm 小而稳；projection 是 Linear 无 bias，能自适应 scale，但留意。

---

## 5. 关键实验数据

完整 mean±std 表（last5 / best / final 三套指标）：
- [`results/multiseed_20260602_002504/robust_summary.md`](results/multiseed_20260602_002504/robust_summary.md)
- [`results/multiseed_20260602_002504/summary.md`](results/multiseed_20260602_002504/summary.md)（best-epoch 版）
- 每个 run 原始数：`results/multiseed_20260602_002504/raw_runs.jsonl`（50 行）+ 各 `results/full_step2_tabicl_smiles_*/metrics.json`

最终结论表（last5, mean±std over 5 seeds）见 [`README.md`](README.md) §11 2026-06-02 段。一句话：Phase2 SMILES Δ∈[−0.001,+0.003] 全在噪声内；Phase3 Δ∈[−0.007,−0.001] 略负。

---

## 6. 复现命令

```bash
source /data2/zhu11/miniconda3/etc/profile.d/conda.sh && conda activate tabpfn
cd /data2/zhu11/TB/branch/smiles

# 1. I/E embedding（Qwen3, ~68 min；可 --resume <run_dir> 续跑）
python script/encode_ie_qwen3.py --batch-size 128 --checkpoint-every 50

# 2. SMILES embedding（4 个 encoder；HF 3 个 + mol2vec CPU）
python script/encode_smiles_hf.py --model chemberta_mlm
python script/encode_smiles_hf.py --model chemberta_mtr
python script/encode_smiles_hf.py --model molformer
python script/encode_smiles_mol2vec.py   # 需先下 data/model_300dim.pkl

# 3. 多-seed 实验（50 run，~1 h）+ 稳健聚合
python script/run_multiseed.py --phases Phase2,Phase3 --seeds 5 --epochs 30
python script/aggregate_robust.py   # 默认取最新 multiseed_* dir
```

env：`torch 2.9.1 / transformers 4.57.6 / tabicl 2.1.1 / rdkit 2026.3.2 / gensim 4.4 / mol2vec 0.2.2`（torchvision 已卸）。

---

## 7. 下一步建议

- **不建议**在 SMILES 上继续调参（lr / epoch / pooling / 多 SMILES 拆 token）——信号本身不足，调参空间是噪声。
- 若仍想榨药物信息，方向是 **结构化药物属性**而非 raw SMILES：ATC 类、给药途径、是否生物制剂、剂量——这些更可能跟 SAE 因果相关，且能做成稳定 tabular 列而非高维 embedding。
- 平行的 [`mesh/`](../mesh/) branch（condition/intervention MeSH 作第 3 token）值得对照：若 MeSH 也无增益，则印证"tabular+I/E 已在 SAE 吃满信号"；若 MeSH 有增益而 SMILES 没有，则说明缺的是**适应症/人群**信息而非**分子**信息。
- **多-seed + last5 协议应推广到本项目所有 Full-Step-2 实验**（包括 new_FM / IE_embedding 的历史单次数，严格说都该补误差棒）。

---

## 8. 关键产物索引

| 产物 | 路径 | 说明 |
|---|---|---|
| I/E Qwen3 embedding | `data/ie_embeddings_qwen3.parquet` | d=4096, 158K groups, 覆盖全 4 phase |
| SMILES embedding ×4 | `data/smiles_embeddings_{chemberta_mlm,chemberta_mtr,molformer,mol2vec}.parquet` | d=384/384/768/300 |
| mol2vec 预训练权重 | `data/model_300dim.pkl` | 74 MB, gensim w2v |
| I/E encoding 脚本 | `script/encode_ie_qwen3.py` | resumable, Qwen3-Embedding-8B |
| SMILES encoding 脚本 | `script/encode_smiles_hf.py`（3 HF）/ `script/encode_smiles_mol2vec.py` | |
| 训练脚本 | `script/full_step2_tabicl_smiles.py` | 2 or 3 virt token; `--smiles-emb` / `--report-subset-emb` |
| 多-seed driver | `script/run_multiseed.py` | 5 cfg × N phase × N seed |
| 稳健聚合 | `script/aggregate_robust.py` | last5/best/final mean±std + Δ vs B' |
| 最终结果 | `results/multiseed_20260602_002504/` | summary.md / robust_summary.md / raw_runs.jsonl |
| 进度日志 | `README.md` §11 | 完整心路 + 踩坑 |
