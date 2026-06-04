# ReadMeFirst —— TB 项目总入口

> **每位 vibe coding agent / 每个新任务开始前请先读完这份文档；进任何子目录前再读那个目录的 `README.md`。**

本目录 `/data2/zhu11/TB/` 是 TabPFN + TrialBench 相关工作的根目录。所有自写代码、实验结果、fine-tune 产物都按下面的约定放置。**不要在根目录乱放散文件。**

---

## 1. 目录结构（约定）

```
/data2/zhu11/TB/
├── ReadMeFirst.md           ← 本文件，先读
│
├── script/                  ← 所有自写脚本（数据处理、训练、评估、绘图…）
│   └── README.md
├── results/                 ← 实验输出（metrics、log、figure），每次运行一个子目录
│   └── README.md
├── model_checkpoint/        ← fine-tune 产出的模型权重，每次运行一个子目录
│   └── README.md
│
├── dataset/                 ← 数据集（只读，不改）
│   ├── README.md
│   └── TrialBench/          ← 已下载的 8 个 TrialBench 子任务
│
├── Doc/                     ← 人工撰写的长文档（设计 / 方法论 / 跨实验对比 / 决策记录）
│   ├── README.md
│   ├── results/             ← 跨实验综述、模型对比、结果导向的分析
│   └── DAG/                 ← DAG（因果图）相关：node 定义、edge 审计、报告
│
├── branch/                  ← 探索性子项目（每个一个目录，自带 README + data/script/results）
│   ├── README.md            ← branch 目录总索引 + 目录约定 + 三类 readme 规则 (initial/进度/final)
│   ├── IE_embedding/        ← eligibility/criteria/textblock → MedCPT embedding → stacking
│   ├── All_text_embedding/  ← 所有文本列 → embedding → virtual token 注入 TabPFN
│   ├── new_FM/              ← TabPFN 的 commercial-friendly 替代调研：TabICLv2 / TabDPT
│   │   └── final_readme.md  ← 方案定下来后的终态文档；其他 branch 收尾时也要写
│   ├── mesh/                ← 在 TabICLv2+I+E 基础上加 mesh virtual token (SAE Phase1-3)
│   │   └── initial_readme.md  ← 待开工，cold-read 入口
│   └── smiles/              ← 在 TabICLv2+I+E 基础上加 SMILES virtual token (SAE Phase1-3)
│       └── initial_readme.md  ← 待开工，cold-read 入口
│
├── TabPFN/                  ← PriorLabs/TabPFN 上游仓库（git clone）
│   ├── README.md (上游)
│   └── models/              ← 预训练 ckpt 缓存（HF 下载产物，只读）
│
└── （miniconda3/, BioNeMo/, evo-2/ 等是其他无关项目，不在本规约范围内）
```

**核心原则**：一个目录 = 一个职责。`script` 只放代码，`results` 只放脚本自动输出的结果，`Doc` 放人工撰写的文档，`model_checkpoint` 只放 fine-tune 模型，`dataset` 是只读数据，`TabPFN/` 是上游仓库（**不要**把自写代码混进去）。`branch/` 放探索性子项目（每个自带 README + data/script/results，避免污染主目录），**方案定下来后再加一个 `final_readme.md`** 作为终态文档（详见 [`branch/README.md`](branch/README.md) §3）。

**`results/` vs `Doc/` 的边界**：
- `results/<run_id>/...md` —— **脚本自动生成**的实验报告（metrics 表、自动摘要），跟该次运行强绑定
- `Doc/*.md` —— **手写**的长文档：设计文档、方法论、跨多次实验的总结对比、技术决策记录。可以引用 `results/` 里的数字，但本身是人写的、独立于具体某一次 run

---

## 2. 命名规范

### 2.1 脚本命名（`script/`）

- 格式：`<task>_<action>.py`，全小写下划线
  - `sae_finetune.py`：SAE 子任务上的 fine-tune
  - `verify_gpu_finetune.py`：GPU fine-tune 验证
- 一次性的探索脚本可以加 `scratch_` 前缀（如 `scratch_inspect_data.py`），跑完可删
- 不要写 `tmp.py`、`test.py`、`new.py` 这种没语义的名字

### 2.2 运行 ID（`results/` 和 `model_checkpoint/` 子目录名）

- 格式：`<script_name>_<YYYYMMDD_HHMMSS>`
  - 例：`sae_finetune_20260510_103801`
- **每次运行**（python 脚本执行一次）= **一个唯一 run_id 子目录**
- 同一个 run_id 同时出现在 `results/` 和 `model_checkpoint/`，方便对应

### 2.3 数据文件

- 不要修改 `dataset/` 下的原始文件。如需中间产物（特征工程后的 X/y），写到 `results/<run_id>/` 或 `script/cache/`（自行新建）

---

## 3. 生成文件去向（写脚本时严格遵守）

| 产物类型 | 落点 |
|---|---|
| 训练/评估的 metrics（JSON、CSV） | `/data2/zhu11/TB/results/<run_id>/metrics.json` |
| 训练日志 / stdout 重定向 | `/data2/zhu11/TB/results/<run_id>/log.txt` |
| 图（loss curve、ROC、混淆矩阵） | `/data2/zhu11/TB/results/<run_id>/*.png` |
| 脚本自动生成的实验报告 markdown | `/data2/zhu11/TB/results/<run_id>/*.md` |
| **人工撰写的长文档**（设计 / 方法论 / 跨实验综述） | `/data2/zhu11/TB/Doc/*.md` |
| fine-tune 后的模型权重 | `/data2/zhu11/TB/model_checkpoint/<run_id>/*.pth` |
| 预训练 ckpt（HF 下载，只读） | `/data2/zhu11/TB/TabPFN/models/`（同时 symlink 到 `~/.cache/tabpfn/`） |
| 临时中间产物 | `results/<run_id>/cache/` 内，跑完不留可删 |
| 探索性子项目的数据 / 脚本 / 结果 | `branch/<topic>/{data,script,results}/`，自带 README |

**写脚本时，把这些路径作为模块级常量放在文件顶部**，不要散落 `os.path.join(...)`。参考 `script/sae_finetune.py` 中：

```python
DATA_ROOT = Path("/data2/zhu11/TB/dataset/TrialBench/serious-adverse-event-forecasting")
CKPT      = Path("/data2/zhu11/TB/TabPFN/models/tabpfn-v2.5-classifier-v2.5_default.ckpt")
RESULTS_ROOT = Path("/data2/zhu11/TB/results")
CKPT_ROOT    = Path("/data2/zhu11/TB/model_checkpoint")
```

---

## 4. 出问题先去哪儿找

| 现象 | 先看哪儿 |
|---|---|
| 想知道某次实验结果 | `results/<run_id>/metrics.json` |
| 想看跨实验综述 / 设计文档 / 方法论 | `Doc/*.md`（人工写的；先看 `Doc/README.md`） |
| 想 reproduce 某次实验 | `results/<run_id>/metrics.json` 里有 `args` 字段，对照 `script/<script>.py` 跑同样命令 |
| GPU/CUDA 相关错误 | 先跑 `script/verify_gpu_finetune.py` 自检；H200 NVL，CUDA 13.2 driver |
| TabPFN API / 用法 | `TabPFN/README.md`、`TabPFN/examples/finetune_classifier.py`、`TabPFN/src/tabpfn/finetuning/` |
| 数据格式 / 列含义 | `dataset/README.md`，TrialBench 字段定义在 [TrialBench Comprehensive Guide](https://github.com/ML2Health/ML2ClinicalTrials/blob/main/Trialbench/A%20Comprehensive%20Guide%20to%20TrialBench.md) |
| Python 环境 | `conda activate tabpfn`（路径 `/data2/zhu11/miniconda3/envs/tabpfn`，python 3.11，torch 2.11+cu128） |
| 模型 ckpt 找不到 | `TabPFN/models/` 或 `~/.cache/tabpfn/`（已 symlink 到前者） |
| fine-tune 结果重复出现但不知是哪次 | 看 `model_checkpoint/<run_id>/` 时间戳，对应 `results/<run_id>/metrics.json` |

---

## 5. vibe coding agent 准则

每次新任务/对话开始时，agent 应：

1. **先读 `/data2/zhu11/TB/ReadMeFirst.md`（本文件）**
2. 进入任何子目录前，**读那个目录的 `README.md`**
3. 写代码前先明确：脚本写到 `script/`、自动生成结果写到 `results/<run_id>/`、ckpt 写到 `model_checkpoint/<run_id>/`、人工撰写的长文档写到 `Doc/`
4. **不要**在 `TabPFN/` 里塞自写代码，那是上游仓库（editable install）
5. **不要**修改 `dataset/` 下任何文件
6. **不要**复用其他 run 的 run_id；每次运行用 `datetime.now().strftime('%Y%m%d_%H%M%S')` 生成新的
7. 跑完后 `ls results/<run_id>/` 和 `ls model_checkpoint/<run_id>/` 自检一下产物是否落地
8. 如果新增一类产物（比如 `notebooks/`、`figures/`），先在本文件 §1 §3 加一行约定，再开新目录

---

## 6. 现成入口脚本

| 脚本 | 用途 | 命令 |
|---|---|---|
| `script/verify_gpu_finetune.py` | 5 秒自检：GPU 能跑 TabPFN fine-tune | `python script/verify_gpu_finetune.py` |
| `script/sae_finetune.py` | TrialBench SAE 子任务 baseline + fine-tune + 落盘 | `python script/sae_finetune.py --epochs 30 --lr 1e-5` |

环境激活：
```bash
source /data2/zhu11/miniconda3/etc/profile.d/conda.sh && conda activate tabpfn
# 或直接用绝对路径：
/data2/zhu11/miniconda3/envs/tabpfn/bin/python ...
```

---

## 7. 现状速览（保持更新）

- 上游 TabPFN 版本：`7.1.1`（editable 安装于 `TabPFN/`）
- 预训练 ckpt：`tabpfn-v2.5-classifier-v2.5_default.ckpt`（41 MB，已下载）
- TrialBench 数据：8 个子任务全下完并解压，位于 `dataset/TrialBench/`
- GPU：NVIDIA H200 NVL（143 GB VRAM）
- 已验证：SAE Forecasting 上 baseline ROC-AUC ≈ 0.885，10-epoch fine-tune 暂无显著增益（详见 `results/`）
- 进行中：`branch/IE_embedding/` —— 用 MedCPT 对 inclusion/exclusion criterion 编码 → criterion head OOF stacking → 8 列特征接入 TabPFN（详见 `branch/IE_embedding/README.md`）
- 2026-05-23: `branch/new_FM/` —— TabPFN 替代调研。第一/三轮 (6 子任务 × 4 FM × IE 8-col baseline-vs-+IE) 完成；TabICLv2 (BSD-3) 在多数 cell 拿 +IE 头名；Mitra zero-shot 在 multiclass 塌缩到 majority class。
- 2026-05-24: `branch/new_FM/` 第四轮 —— **Full Step 2 (2 virtual feature tokens, IE_embedding "最终方案")** 跨 3 FM (TabPFN / TabICL / Mitra；TabDPT 因架构无 column-axis attention 不支持) × 6 子任务 × Phase2/3 = 36 cells。**27/36 显著正向**，最大涨幅 **+0.164 R²** (TabPFN trial-duration Phase3) / **+0.130 macro-F1** (Mitra failure-reason Phase3 —— 把 zero-shot 塌缩问题救回来)。patient-dropout 子任务 3 个 FM 一致没涨。脚本：`branch/IE_embedding/script/full_step2_train.py` (TabPFN) + `branch/new_FM/script/full_step2_{tabicl,mitra}.py`。
- 2026-05-24: **`branch/new_FM/` 收尾** —— 最终方案 **TabICLv2 (BSD-3)**，cold-read 入口 [`branch/new_FM/final_readme.md`](branch/new_FM/final_readme.md)。同时在 `branch/README.md` 加了 final_readme.md 规约：所有 branch 方案定下来后必须写一个 final_readme.md 作为终态文档。
- 2026-06-01: 新开 [`branch/mesh/`](branch/mesh/) 和 [`branch/smiles/`](branch/smiles/) 两条线 —— 在 new_FM 的 TabICLv2+I+E (Full Step 2) 基础上分别加 condition/intervention MeSH 和 SMILES 分子结构作 3rd virtual token，SAE Phase 1/2/3 训练对比。两条 branch 各自的 `initial_readme.md` 是 cold-read 入口（给接手 agent 起步用）。同时在 `branch/README.md` §3 加了 `initial_readme.md` 规约（介于"开 branch 但还没开工"和 README.md 之间的一类文档）。
- 2026-06-02: **`branch/smiles/` 收尾 → SMILES 无稳健增益**，cold-read 入口 [`branch/smiles/final_readme.md`](branch/smiles/final_readme.md)。在 TabICLv2+I+E 上加 SMILES 第 3 virtual token（4 个化学 encoder: ChemBERTa-MLM/MTR、MolFormer-XL、Mol2Vec），SAE Phase2/3。**关键发现：TabICL Full-Step-2 训练是 CUDA 非确定性的，best-epoch 单次噪声 ≈ ±0.009**，跟 SMILES 效应同量级 → 改 **5 cfg × 2 phase × 5 seed = 50 run** 多-seed (mean±std)。结论：Phase2 Δ∈[−0.001,+0.003] 全在噪声内，Phase3 Δ∈[−0.007,−0.001] 略负；Cell D (SMILES 非空子集) 也没翻盘 → SMILES 对 SAE 在 tabular+I/E 之外无增量信号。**附带**：用 **Qwen3-Embedding-8B (4096-d)** 重编 I/E（落 `branch/smiles/data/ie_embeddings_qwen3.parquet`），在 I+E 上跟旧 MedCPT (768-d) 持平/略好。多-seed + last5 协议建议推广到所有 Full-Step-2 实验。
- 2026-06-02: **`branch/mesh/` 收尾 → MedCPT MeSH 在 Phase2 拿到唯一稳健显著正信号**，cold-read 入口 [`branch/mesh/final_readme.md`](branch/mesh/final_readme.md)。在 TabICLv2+I+E 上把 condition+intervention MeSH 作 **2 个额外 virtual token（共 4 token）**，4 个生物医学 encoder（SapBERT/BioLORD-2023/MedCPT/PubMedBERT），SAE Phase2/3。复用 smiles 的多-seed+配对 t 协议（I/E 直接 symlink 复用 smiles 的 Qwen3 parquet）。5 个 encoder（后补 Qwen3-Embedding-8B 4096-d）。**Qwen3 最强**：Phase2 full Δ=+0.0058 (p=0.049)、子集 +0.0086 (p=0.019)；MedCPT 次之 full +0.0046 (p=0.039)、子集 +0.0073 (p=0.015)，n=10 配对 t —— SMILES+MeSH 两 branch 唯一稳健显著正；SapBERT/PubMedBERT 与全部 Phase3 不显著。**通用强 embedding Qwen3 在 MeSH 受控术语上不输甚至优于领域专用 encoder**（原以为专用赢，被推翻；SAE 要的是疾病-药物文献共现语义，Qwen3/MedCPT 都抓得住）。**回答 smiles 开放问题：SAE 缺的更多是适应症/药物身份(MeSH)，而非分子结构(SMILES)**，但增益小(~+0.005)、只 Phase2，默认方案仍 I+E。
- 2026-06-02: **`branch/aggregate/` 收尾 → 全信号堆叠不如只用 I+E**，cold-read 入口 [`branch/aggregate/final_readme.md`](branch/aggregate/final_readme.md)。把 I+E (Qwen3) + 9 个文本列 (All_text Qwen3) + SMILES (MolFormer) 全作 virtual token（**共 12 个，5.87M 可训练参数**）塞进 TabICLv2，SAE Phase2/3，n=10 多-seed+配对 t。结论：**12 token 不如 2 token 的 I+E** —— Phase2 加文本反而略负 (Δ=−0.0053, p=0.065)，Phase3 全在噪声内 (p>0.48)。**I+E 是甜点位**，多余文本列+SMILES 边际信息为零甚至因随机投影稀释冻结 base 而略降。n=5 的 Phase3 边际正 (p≈0.09) 在 n=10 塌回 0（再次印证多-seed 必要性）。通用多-token 脚本 `full_step2_tabicl_multi.py`（任意 N 源, `path@TYPE` 语法）+ `subset_sae.py`（源 parquet 按 SAE 子集+fp16 预切，5GB→1.1GB 提速）。caveat：本 branch 的 condition/intervention 是原始文本 Qwen3 编码，**不含** mesh 的 MedCPT-MeSH winner，故不矛盾。**SAE 全局结论：I+E 提供绝大部分非 tabular 信号，其上唯一稳健正是 MedCPT-MeSH(Phase2 小幅)，SMILES/all-text-Qwen3 无增益。**

- 2026-06-04: **全面 MeSH / SMILES 评估（5 task × Phase1-3）**，单 seed。固定 TabICLv2，baseline=tabular+I/E(Qwen3)，跨 SAE/mortality/patient-dropout/trial-duration/trial-failure-reason。MeSH=condition+intervention 2 token（5 encoder），SMILES=1 token（4 encoder）。**MeSH > SMILES**：MeSH 最强 **BioLORD mean Δ +0.0105 / win 80%**；SMILES 最强 ChemBERTa-MTR 才 +0.0035 / 60%（MolFormer 净负）。增益集中在 **trial-duration Phase3**（MeSH 全 encoder 强正, BioLORD +0.052；SMILES 反而负）和 **trial-failure-reason Phase2/3**（两者都正）。SAE/mortality/Phase1 多在噪声内。encoder 选择 task-dependent（综合 MeSH 用 BioLORD，SAE 专项 Qwen3/MedCPT）。MeSH 是小幅锦上添花，I/E 始终是主力。完整表见 [`branch/mesh/final_readme.md`](branch/mesh/final_readme.md) §2 / [`branch/smiles/final_readme.md`](branch/smiles/final_readme.md) §2。新增 in-process grid 脚本 `{mesh,smiles}_eval_grid.py` + encoder 的 `--subtasks` 多任务 union。

—— 改动本文件等同改动项目契约，请同步更新各子目录的 `README.md`。
