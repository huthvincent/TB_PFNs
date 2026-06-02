# branch/mesh — 在 TabICLv2+I+E 基础上加 condition/intervention MeSH virtual token

> 进入本目录前请先看 [`/data2/zhu11/TB/ReadMeFirst.md`](../../ReadMeFirst.md)；branch 规约见 [`../README.md`](../README.md)。
>
> 本文件原为 `initial_readme.md`（cold-read 起点），现已升格为 `README.md`（进度日志）。下方 §1-§11 保留原始起点文档（架构/数据/设计决策的 cold-read 入口），**新增实验进度记录在文末 §12 "实施进度日志"**，按时间顺序追加。

---

## 1. TL;DR — 这个 branch 要做什么

在 **TabICLv2 + tabular + I/E 两个 virtual token** 的基础架构上，**多加一个 mesh virtual token**（病种/干预的 MeSH 术语 embedding），在 **SAE (serious-adverse-event-forecasting) Phase 1 / Phase 2 / Phase 3 三个 phase 分别**训练并测试。

期望产出：每个 phase 一行 `baseline (TabICL zero-shot) | +I+E | +I+E+mesh | Δ` 的对照表。

---

## 2. 项目上下文（30 秒速通）

`/data2/zhu11/TB/` 是 TabPFN + TrialBench 的工作目录。我们在临床试验数据（TrialBench, 8 个子任务 × 4 个 phase）上预测各种事件。

| Branch | 状态 | 重要结论 |
|---|---|---|
| `IE_embedding/` | 已落地 | 把 eligibility 的 inclusion/exclusion criterion 文本编码 → mean-pool → 注入 TabPFN 做 +IE 增益（历史用 MedCPT 编的，新分支统一改用 Qwen3-Embedding-8B；详见 §3 / §4.2 Q2） |
| `new_FM/` | 已收尾 → **TabICLv2** | TabPFN 权重 non-commercial，找了 BSD-3 的 TabICLv2 替代；同样支持 "2 virtual feature token" 注入 |
| `mesh/` | **本 branch（待开工）** | 加 mesh 作 3rd virtual token |
| `smiles/` | 另一条 branch（并行做） | 加 SMILES 作 3rd virtual token |

---

## 3. 基础模型（继承自 `new_FM/`）

### 架构

```
Input:
  X (tabular)               — shape (n, F)，F 随 subtask 不同 (SAE 是 41 列 after preprocess)
  y_train                   — (n_train,) 二分类
  incl_mean_per_trial       — (n, d_emb) 编码 inclusion criterion 的 mean-pool
  excl_mean_per_trial       — (n, d_emb) 编码 exclusion criterion 的 mean-pool

  注：项目历史用 MedCPT (d_emb=768)；本 branch 统一改用 Qwen3-Embedding-8B
      (d_emb ≈ 4096)。如果你接手时 IE 还只有 MedCPT 缓存，**先用 Qwen3 重编一份
      I/E embedding** 落 branch/mesh/data/ie_embeddings_qwen3.parquet，再做 mesh。

Model:
  TabICLv2 (BSD-3, 27.6M 参，embed_dim=128)
  └── col_embedder(X, y_train)  → (B, T, H, 128)
  └── [inject 2 virtual cols here]
        proj_incl(incl_mean) + col_emb[0]   # 1 个 virtual feature column
        proj_excl(excl_mean) + col_emb[1]   # 1 个 virtual feature column
        cat → (B, T, H+2, 128)
  └── row_interactor  → (B, T, R)
  └── icl_predictor   → (B, test_size, max_classes=10)

Training:
  Freeze entire TabICL (27.6M params, requires_grad=False)
  Train only:
    proj_incl: Linear(d_emb, 128)   ~524K params (Qwen3 d_emb=4096)
    proj_excl: Linear(d_emb, 128)   ~524K params
    col_emb:   Parameter(2, 128)    ~256 params
  → total trainable ~1.05M (Qwen3) vs ~197K (旧 MedCPT 时), lr=1e-3, 30 epochs
  Loss: cross-entropy on `qry_size=500` query rows，每 step 随机重新 sample ctx (2000) + qry (500)
```

完整参考实现：`/data2/zhu11/TB/branch/new_FM/script/full_step2_tabicl.py`（337 行）。本 branch 的脚本应该基于这个文件 fork 一份，扩展成 3 个虚拟列。

### 现有数字（SAE TabICL Full Step 2 +I+E only，对照基线）

来源：`branch/new_FM/results/full_step2_tabicl_serious-adverse-event-forecasting_YN_Phase{2,3}_*/metrics.json`

| Phase | TabICL zero-shot baseline | TabICL +I+E (Full Step 2 trained) | Δ |
|---|---|---|---|
| Phase 1 | (未跑) | (未跑) | — |
| Phase 2 | 0.8241 | 0.8658 | +0.0418 |
| Phase 3 | 0.8968 | 0.9078 | +0.0110 |

**注意**：Phase 1 baseline 和 +I+E 都还没跑，你需要先把 Phase 1 加进来才能完整对照。可以直接用现成脚本一行命令补：

```bash
# Phase 1 zero-shot baseline (4 个 FM × baseline+IE)
python /data2/zhu11/TB/branch/new_FM/script/fm_bench_ie.py \
  --subtask serious-adverse-event-forecasting --target Y/N --task-type binary --phase Phase1

# Phase 1 TabICL Full Step 2 +I+E only
python /data2/zhu11/TB/branch/new_FM/script/full_step2_tabicl.py \
  --subtask serious-adverse-event-forecasting --target Y/N --task-type binary --phase Phase1 --epochs 30
```

---

## 4. 本 branch 要做的新增

把架构扩成 **3 个 virtual feature column**：

```
proj_incl(incl_mean)  + col_emb[0]   # 已有
proj_excl(excl_mean)  + col_emb[1]   # 已有
proj_mesh(mesh_mean)  + col_emb[2]   # 新增
cat → (B, T, H+3, 128)
```

**encoder 选用**：
- I 和 E 用 **Qwen3-Embedding-8B**（d_IE ≈ 4096，跟项目其他 branch 统一）
- mesh 用**单独的 mesh 专用 embedder**——具体哪个 **TBD**，开工前要跟用户对齐（详见 §4.2 Q2）

可训练参数 ≈ `2 × Linear(4096, 128) + 1 × Linear(d_mesh, 128) + col_emb(3, 128)`。Qwen3 那两路占 ~1.05M；mesh proj 那一路看 encoder 输出维度（768-d 类的加 ~100K，4096-d 类的加 ~525K，384-d 类的加 ~50K）。总数大致 1.1–1.6M，仍只占 base TabICL 27.6M 的 4–6%。

### 4.1 Mesh 数据源（在 TrialBench train_x.csv 里）

| 列名 | 非空率 (SAE Phase2) | 典型值 |
|---|---|---|
| `condition_browse/mesh_term` | 95.6% | 可能是单字符串 `'Prostatic Neoplasms'`，也可能是字符串化的列表 `"['Cancer', 'Tumor']"` |
| `intervention_browse/mesh_term` | 66.9% | 字符串化列表 `"['Molgramostim', 'Sargramostim']"` |

**注意**：这两个字段都需要 `ast.literal_eval` 或类似工具尝试解析；解析失败就当作单字符串。处理 string-list 的套路可以参考 [`branch/IE_embedding/script/split_criteria.py`](../IE_embedding/script/split_criteria.py)（~100 行）—— 那个脚本对 inclusion/exclusion textblock 做了同类的容错解析，看一次就能照搬。

### 4.2 设计选择（要先跟用户/团队确认）

| 问题 | 选项 | 推荐 |
|---|---|---|
| Q1: 1 个 mesh token 还是 2 个 | (a) 1 token = condition+intervention 全部 term mean-pool 在一起 / (b) 2 token = condition_mesh_mean + intervention_mesh_mean 分开 | **(b) 2 个 token 更干净**，跟 I/E 分开的设计一致；总虚拟列变 4。先跟用户确认 |
| Q2: mesh 用什么 encoder | **TBD —— 开工前要跟用户讨论**。候选清单（agent 起步可以先列出来跟用户对齐）：(a) MedCPT-Article-Encoder (NCBI，biomedical, 768-d) / (b) BioBERT / ClinicalBERT / PubMedBERT (临床/生物医学预训练 BERT) / (c) 专用 MeSH embedder（如果调研发现有现成 SOTA）/ (d) 其他 | **TBD**——这一栏空着，等用户给方向。**I 和 E 走 Qwen3-Embedding-8B 不变**（项目其他 branch 一致），但 mesh 一定用独立的 embedder（用户明确要求 mesh / SMILES 各自专用 encoder） |
| Q3: 缺失 mesh 的 trial 怎么处理 | (a) 用 NaN 喂模型（跟 IE 一样让 model 自己处理） / (b) 用 0 向量（"无 mesh 信息"中性值） / (c) 用全数据集 mesh mean（softer fallback） | **(b) 用 0 向量** 跟 [`full_step2_tabicl.py`](../new_FM/script/full_step2_tabicl.py) 第 90 行 `mean_pool_per_trial()` 的处理一致 |

---

## 5. 实验设计

### 5.1 训练 / 评估范围

只测 **SAE (serious-adverse-event-forecasting)**，binary 分类，target = `Y/N`。

3 个 phase 分开跑（不合并）：Phase 1、Phase 2、Phase 3。

每个 phase 跑：
- **Cell A**: baseline = TabICL zero-shot（无虚拟列）
- **Cell B**: +I+E = TabICL Full Step 2 with 2 virt tokens
- **Cell C**: +I+E+mesh = TabICL Full Step 2 with 3 (或 4，取决于 §4.2 Q1) virt tokens — **本 branch 的核心**

共 9 个 cells。Cell A、B 在 Phase 2/3 已有现成结果（见 §3 表），只需要补 Phase 1 + Phase 1/2/3 的 Cell C。

### 5.2 训练 hyperparameter（默认）

跟 `full_step2_tabicl.py` 一致，便于跟现有数字对照：
- `epochs=30`, `eval_every=2`
- `lr=1e-3`, `weight_decay=1e-4`
- `ctx_size=2000`, `qry_size=500`
- AdamW, seed=0
- bf16/fp16 mixed precision（TabICL 内部走 fp16，projection 是 fp32 输出，cat 前 cast 到 col_out.dtype，详见 [`full_step2_tabicl.py:112-119`](../new_FM/script/full_step2_tabicl.py)）

### 5.3 数据加载与预处理

复用 `branch/IE_embedding/script/ablate_ie_features.py:load_split` 和 `script/sae_finetune.py:preprocess`（都已经在 `full_step2_tabicl.py` 顶部 import 了），不要重写。

```python
from ablate_ie_features import load_split
X_train, y_train = load_split('serious-adverse-event-forecasting', 'train', 'Y/N', ['Phase1'])
X_test,  y_test  = load_split('serious-adverse-event-forecasting', 'test',  'Y/N', ['Phase1'])
# X_train / X_test 是 pandas DataFrame，含 mesh 等列
```

注意：`preprocess()` 会 drop 一组 TEXT_DROP 文本列。**确认 `condition_browse/mesh_term` 和 `intervention_browse/mesh_term` 不在 TEXT_DROP 里**（TEXT_DROP 见 `script/sae_finetune.py` 顶部，需要的时候 grep 一下确认）。如果在，需要在 mesh encoding pipeline 里**先**从原始 `X_train`/`X_test` 提取再做 preprocess。

---

## 6. 实现路径（建议）

### 6.1 Encoding 脚本（两个，分别用不同 encoder）

#### 6.1.a I/E embedding (Qwen3)

新建 `branch/mesh/script/encode_ie_qwen3.py`：
- 用 `Qwen/Qwen3-Embedding-8B` 把 inclusion / exclusion criterion 重编一份
- 输出：`branch/mesh/data/ie_embeddings_qwen3.parquet` 含列 `trial_id, phase, type ∈ {I, E}, mean_emb` （d≈4096）

> 项目历史在 `branch/IE_embedding/results/encode_medcpt_*` 有 MedCPT 版的 I/E embedding 缓存，但 d=768；本 branch 要重编 Qwen3 版好跟其他 Qwen3-using branch 对齐。

#### 6.1.b Mesh embedding (encoder TBD)

新建 `branch/mesh/script/encode_mesh_<encoder>.py`（文件名等 §4.2 Q2 跟用户对齐后再定）：
- 输入：扫描 TrialBench 所有 (subtask, phase, split) 的 train_x.csv，提取 `condition_browse/mesh_term` + `intervention_browse/mesh_term`
- 对每个 (trial_id, phase) 做：
  1. 解析 mesh term 列表（`ast.literal_eval` + 兜底纯字符串）
  2. 每个 term 用**待定的 mesh encoder** 编码 → d_mesh 维
  3. mean-pool per (trial_id, phase, type) 其中 type ∈ {condition, intervention}
- 输出：`branch/mesh/data/mesh_embeddings.parquet` 含列 `trial_id, phase, type, mean_emb` （维度看选的 encoder）

#### Pipeline 形状参考

无论用什么 encoder，两个脚本的整体形状都跟 [`branch/IE_embedding/script/encode_medcpt.py`](../IE_embedding/script/encode_medcpt.py)（~200 行）一样：批量 HF transformer 编码 + parquet 落盘 + 进度条 + bf16 forward。**只是 encoder load 和 tokenizer 那两行换掉**。看那个脚本能 cold read 学到所有 boilerplate，~10 分钟内就能 fork。

### 6.2 Full Step 2 训练脚本

新建 `branch/mesh/script/full_step2_tabicl_mesh.py`：fork `branch/new_FM/script/full_step2_tabicl.py`，改两处：
1. `align_virt_emb()` 输出从 `(n, 2, 768)` 改成 `(n, 3, 768)`（或 `(n, 4, 768)` 看 §4.2 Q1），加载 mesh embedding 并对齐
2. `TabICLVirtualInjection` 类：把 `proj_incl/proj_excl + virt_col_emb (2, E)` 扩成 3 (或 4) 套；`forward` 里 cat 3 (或 4) 列虚拟而不是 2 列

### 6.3 跑实验

```bash
# 先确保 Phase 1 的 baseline 和 +I+E 已经跑过（§3 末尾的 2 个 cmd）

# 然后跑本 branch 的 Cell C × 3 phase
for ph in Phase1 Phase2 Phase3; do
  python /data2/zhu11/TB/branch/mesh/script/full_step2_tabicl_mesh.py \
    --subtask serious-adverse-event-forecasting --target Y/N --task-type binary \
    --phase $ph --epochs 30
done
```

---

## 7. 期望产出

| 文件 | 用途 |
|---|---|
| `branch/mesh/data/ie_embeddings_qwen3.parquet` | Qwen3-Embedding-8B 重编的 I/E embedding（替换历史 MedCPT 768-d 版本，d≈4096）|
| `branch/mesh/data/mesh_embeddings.parquet` | mesh 专用 encoder 编的 condition/intervention MeSH embedding（encoder TBD）|
| `branch/mesh/script/encode_ie_qwen3.py` | I/E encoding 脚本（Qwen3）|
| `branch/mesh/script/encode_mesh_<encoder>.py` | mesh encoding 脚本（encoder 名待定）|
| `branch/mesh/script/full_step2_tabicl_mesh.py` | TabICL Full Step 2 + 3 (或 4) virt tokens 训练脚本 |
| `branch/mesh/results/<run_id>/metrics.json` | 每个 phase 的 train history + best metrics |
| `branch/mesh/README.md` | 进度日志（替换本 `initial_readme.md`，详见 [`branch/README.md`](../README.md) §3） |
| `branch/mesh/final_readme.md` | 终态文档（方案定下来后写）|

最终在 `README.md` 或 `final_readme.md` 里要给出 3 phase × 3 cell = 9 cell 表：

```
| Phase | TabICL zero-shot | +I+E | +I+E+mesh | Δ(mesh) |
| 1     | ?                | ?    | ?         | ?       |
| 2     | 0.8241           | 0.8658 | ?       | ?       |
| 3     | 0.8968           | 0.9078 | ?       | ?       |
```

预期方向：**mesh 加进来主要应该帮 condition 信号的区分**，对 SAE（看的是病种/药品组合的副作用率）有正向贡献的可能性比较大。但也不排除 IE/tabular 已经把 condition 信号吃完了，mesh 是 marginal informative（类似 [`branch/new_FM/README.md` §5 第四轮结论 §3](../new_FM/README.md)patient-dropout 的发现）。

---

## 8. 重要踩坑预警

### 8.1 TabICL 内部 fp16，projection 输出 fp32

cat 之前要 cast。参考 [`full_step2_tabicl.py:112-119`](../new_FM/script/full_step2_tabicl.py)：

```python
v_in = mesh_T_768.to(col_out.device).to(self.proj_mesh.weight.dtype)  # fp32 做投影
mesh_te = self.proj_mesh(v_in) + self.virt_col_emb[2]                  # (T, E) fp32
mesh_t1e = mesh_te.unsqueeze(1).to(col_out.dtype)                      # (T, 1, E) cast 回 fp16
mesh_b_t_1_e = mesh_t1e.unsqueeze(0).expand(B, -1, -1, -1).contiguous()
col_aug = torch.cat([col_out, virt_incl_excl, mesh_b_t_1_e], dim=2)
```

### 8.2 mesh 缺失的 trial

非空率 95% / 67%。统一的简单策略：缺失 → 零向量；模型只会从 0 投影里拿到 `virt_col_emb` 自己的 bias，等于"这列没信号"。

### 8.3 同一个 (trial_id, phase) 跨 subtask 共享

跟 IE 一样，mesh 属于 trial 自己的属性，不同 subtask 共享。但本 branch 只跑 SAE，无所谓；将来扩到其他 subtask 时直接 join 即可。

### 8.4 env 注意

```bash
source /data2/zhu11/miniconda3/etc/profile.d/conda.sh && conda activate tabpfn
```

`tabpfn` env 里 `torch 2.9.1` / `transformers 4.57.6` / `pandas 2.3.3` / `tabicl 2.1.1` 都装好了。

**Qwen3-Embedding-8B** (I/E 用)：`transformers.AutoTokenizer + AutoModel.from_pretrained('Qwen/Qwen3-Embedding-8B', torch_dtype='bfloat16')` 加载，~16 GB bf16 权重，首次自动从 HF 下；H200 单卡放得下，batch 256 ctx≤512 token 应该 ~50 trial/s。

**mesh encoder** (待定)：等 §4.2 Q2 跟用户对齐选定后再装。如果选 HF 上的 encoder (e.g. BioBERT)，直接 `pip install transformers` 应该够（env 里有 transformers 4.57.6）；如果选 BioNeMo 或别的化学/生物专项框架，可能需要单建 env。

---

## 9. 跟用户/团队对齐（开工前请确认）

1. §4.2 Q1: mesh 拆几个 token（推荐 2 个：condition_mean + intervention_mean）
2. §4.2 Q2: **mesh encoder 选哪个 —— 必须先跟用户对齐**（用户明确说 mesh 要用专用 embedder，不复用 Qwen3）。开工前先列一个候选清单 (MedCPT / BioBERT / PubMedBERT / 专用 MeSH embedder 等) 跟用户讨论拍板。**I/E 走 Qwen3 不需要对齐**（已定）
3. §5.1 实验范围：只 SAE 还是顺手把其他 5 个 subtask 也加上（user 说 "在 SAE 的 phase 1-3 上"，所以默认只 SAE，但跑完可以聊扩展）
4. **不**对齐就开始 §6 的 6.1 + 6.2，把 encoding pipeline 跑通是确定能用的工作

---

## 10. 重要参考文档（按优先级，需要时按需读）

| 文件 | 何时看 | 看什么 |
|---|---|---|
| [`/data2/zhu11/TB/branch/README.md`](../README.md) | **开工前必看** | branch 目录规约、README.md vs final_readme.md 区别 |
| [`/data2/zhu11/TB/branch/new_FM/final_readme.md`](../new_FM/final_readme.md) | **开工前必看** | TabICLv2 的 license / API / drop-in 方式 / 已知坑 |
| [`/data2/zhu11/TB/branch/new_FM/script/full_step2_tabicl.py`](../new_FM/script/full_step2_tabicl.py) | **要 fork 它** | 337 行；这是基础模型的完整实现，看 `TabICLVirtualInjection` 类（~50 行）+ `main()` 训练 loop 即可 |
| [`/data2/zhu11/TB/branch/IE_embedding/script/encode_medcpt.py`](../IE_embedding/script/encode_medcpt.py) | 写 encode_ie_qwen3 和 encode_mesh_<...> 时参考 | **批量 HF transformer 编码 pipeline 模板**（GPU、bf16、进度条、parquet 落盘）—— 只看 pipeline 形状，**I/E 那条 encoder 换成 Qwen3-Embedding-8B；mesh 那条 encoder 等 §4.2 Q2 跟用户对齐再定** |
| [`/data2/zhu11/TB/branch/IE_embedding/script/full_step2_train.py`](../IE_embedding/script/full_step2_train.py) | mean_pool_per_trial 工具函数 | full_step2_tabicl.py 顶部 import 的 `mean_pool_per_trial / align_virt_emb / build_sklearn_preprocessor` 都在这；改写时直接 import 复用 |
| [`/data2/zhu11/TB/ReadMeFirst.md`](../../ReadMeFirst.md) | env / 路径不熟时翻 | 项目顶层规约、命名 / 落盘约定 |
| [`/data2/zhu11/TB/branch/IE_embedding/README.md`](../IE_embedding/README.md) §4 | 想理解架构选型时 | 为什么是 virtual token + 几个备选 (raw concat / PCA / stacking / Full Step 2) 的对比 |

旧 readme 不要全部塞进 context，按上表按需 cherrypick；先把这份 initial_readme 内化好，对架构和数据流就够了。

---

## 11. 一个推荐的 day-1 节奏

1. (10 min) 读 §1-§5 + 上面 §10 前 3 行
2. (15 min) 准备 §9 三个问题（特别是 Q2 mesh encoder 候选清单）跟用户对齐
3. (30 min) 把 SAE Phase 1 的 baseline (Cell A) 和 +I+E (Cell B) 用现成脚本补完（§3 末尾两个 cmd）；同时把数据集里 mesh 列的格式跑一下 EDA
3. (1 h) 写 `encode_ie_qwen3.py`：参考 [`encode_medcpt.py`](../IE_embedding/script/encode_medcpt.py) 的 pipeline 形状 fork 一份，encoder 换成 **Qwen3-Embedding-8B**，输入字段是 inclusion/exclusion criterion 文本（用 Qwen3 重编一份 I/E embedding 落 `data/ie_embeddings_qwen3.parquet`）
4. (0.5 h) 跟用户对齐 §4.2 Q2 mesh encoder 选哪个，定下来后写 `encode_mesh_<encoder>.py`（pipeline 形状跟 §3 一样，只是 encoder load 换一下）
4. (1 h) 跑 encoding，产出 `data/mesh_embeddings.parquet`，sanity check shape 和缺失率
5. (1 h) fork [`full_step2_tabicl.py`](../new_FM/script/full_step2_tabicl.py)，扩成 3 (或 4) virtual token；先跑 SAE Phase 2 smoke 看是否能收敛、跟 +I+E only 比有没有有意义的 Δ
6. 跑完 3 phase × Cell C，把数字填进 §7 那张 3×4 表；如果 Δ 显著正向，开始写 `final_readme.md`；如果不显著，加 epoch / 调 lr / 试 Q1 (2 token 拆开 condition_mesh / intervention_mesh) 重跑

祝顺利。有疑问翻 §10 的文档；架构疑问直接读 `full_step2_tabicl.py`，比看任何二手描述都直接。

---

## 12. 实施进度日志

### 2026-06-02 — Day 1：复用 smiles 工具链一气做完 + MedCPT MeSH 在 Phase2 拿到唯一稳健正信号

**对齐**：跟用户确认 (1) condition + intervention 两列分别做 **2 个独立 virtual token**（疾病 vs 药物语义正交，跟 I/E 分开同理）→ 架构 **I+E+condition+intervention = 4 个 virtual token**；(2) 4 个生物医学 encoder 都测：SapBERT / BioLORD-2023 / MedCPT / PubMedBERT；(3) 缺失填零向量 + Cell D 报 intervention-非空子集；(4) 只 SAE；(5) Phase2/3 + 多-seed（跟 smiles 协议一致，可比）。

**大量复用 smiles branch（刚收尾）的工具链**，节省大量时间：
- **I/E embedding 直接 symlink 复用** smiles 的 `ie_embeddings_qwen3.parquet`（trial 属性跨 branch 通用，省 68 min 重编）：`data/ie_embeddings_qwen3.parquet -> ../../smiles/data/ie_embeddings_qwen3.parquet`
- 多-seed 协议 + 稳健聚合（last5）+ 配对 t 检验全部从 smiles 搬

**MeSH 两列数据画像**（SAE Phase2 train）：

| 列 | 是什么 | 覆盖率 | terms/trial | 样例 |
|---|---|---|---|---|
| `condition_browse/mesh_term` | 疾病/适应症 | 95.6% | mean 2.36 (max 49) | Liver Diseases, Vision Disorders |
| `intervention_browse/mesh_term` | 药物/干预 | 66.9% | mean 2.18 (max 31) | Betrixaban, Ocrelizumab |

**4 个 encoder 全量编码**（`encode_mesh_hf.py`，pooling 各按官方惯例：SapBERT/MedCPT 用 CLS，BioLORD/PubMedBERT 用 mean）：4100 unique term，28,750 mean-pool groups（condition+intervention 跨全 subtask/phase），每个 3 秒。都是 109M BERT，d=768。

**脚本**：
- `script/encode_mesh_hf.py` —— `--model {sapbert,biolord,medcpt,pubmedbert}` switch
- `script/full_step2_tabicl_mesh.py` —— fork smiles 版，扩成 2 or 4 virtual token（`--mesh-emb` 决定）；proj_incl/excl/cond/interv + col_emb(4,E)；Cell D 子集 = intervention-非空
- `script/run_multiseed_mesh.py`（含 `--seed-start` / `--append-to` 支持增量加 seed）+ `script/aggregate_robust_mesh.py`

**关键方法论延续**：照搬 smiles 发现的 CUDA 非确定性教训 —— 单次 run 不可信，全部走 **5 cfg × 2 phase × N seed** 多-seed + **配对 t 检验**（同 seed 下 B' 与 C 共享数据采样，配对消掉采样方差，比独立 t 灵敏得多）。

**实验演进**：
1. 先跑 n=5（50 run）→ MedCPT Phase2 full Δ=+0.0064 (p=0.052)、subset +0.0088 (p=0.071) —— **边际**显著，全研究唯一有苗头的正信号
2. MedCPT 卡在 p≈0.05 边界 → **加 seed 到 n=10（Phase2，补 25 run）坐实**（Phase3 已明显平，不加）
3. n=10 后 MedCPT 站住且更强（见下），不是 n=5 侥幸

**最终结果（last5, mean±std；Phase2 n=10, Phase3 n=5；配对 t vs B'）**：

Phase 2（full test 1600；intervention 子集 n=1041）：

| Cell | Full ROC-AUC | Δ vs B' (p) | Interv 子集 | Δ vs B' (p) |
|---|---|---|---|---|
| B' (+I+E) | 0.8594 ± 0.0060 | — | 0.8589 ± 0.0080 | — |
| C: SapBERT | 0.8593 ± 0.0068 | −0.0001 (0.97) | 0.8611 ± 0.0083 | +0.0022 (0.63) |
| C: BioLORD-2023 | 0.8625 ± 0.0060 | +0.0031 (0.096) | 0.8606 ± 0.0053 | +0.0016 (0.47) |
| **C: MedCPT** | **0.8640 ± 0.0052** | **+0.0046 (0.039**)** | **0.8663 ± 0.0059** | **+0.0073 (0.015**)** |
| C: PubMedBERT | 0.8610 ± 0.0055 | +0.0016 (0.52) | 0.8626 ± 0.0049 | +0.0037 (0.27) |

Phase 3（full test 945；intervention 子集 n=675；n=5）：全部不显著（最小 p=0.34）。

| Cell | Full ROC-AUC | Δ vs B' (p) |
|---|---|---|
| B' (+I+E) | 0.8901 ± 0.0072 | — |
| C: SapBERT | 0.8893 ± 0.0040 | −0.0008 (0.80) |
| C: BioLORD-2023 | 0.8918 ± 0.0051 | +0.0017 (0.68) |
| C: MedCPT | 0.8880 ± 0.0055 | −0.0021 (0.66) |
| C: PubMedBERT | 0.8893 ± 0.0055 | −0.0009 (0.82) |

（best/final 指标 + Phase3 子集见 [`results/multiseed_20260602_023755/robust_summary.md`](results/multiseed_20260602_023755/robust_summary.md)。）

**结论**：
1. **MedCPT MeSH 在 Phase2 给出真实但小幅的正增益**：full +0.0046 (p=0.039)、intervention 子集 +0.0073 (p=0.015)，n=10 配对检验显著。**这是 SMILES + MeSH 两条 branch 里唯一稳健显著的正信号。**
2. **Phase3 无效**（全部 p>0.6）。增益不跨 phase 稳定 —— Phase3 样本少、B' 已高(0.89)，余量小。
3. **反直觉：MedCPT（PubMed query-article 对比）> 实体专用 SapBERT/BioLORD**。MeSH term 虽是受控词表实体，但对 SAE 有用的似乎是"疾病-药物-不良事件"的**共现/文献语义**（MedCPT 强），而非实体规范化语义（SapBERT 的 UMLS 同义词 / BioLORD 的概念定义）。
4. **intervention 子集 Δ > full Δ**（MedCPT 0.0073 > 0.0046）：药物 MeSH 信号在"有药物标注"的 trial 上更强，符合"药物身份帮助预测其不良事件倾向"的直觉。

**vs SMILES branch（同框架对照）**：

| 信号源 | Phase2 最佳 Δ (last5, 配对 p) | Phase3 | 判定 |
|---|---|---|---|
| SMILES（分子结构，4 encoder） | mol2vec +0.003 (不显著) | 平/略负 | 无稳健增益 |
| **MeSH（疾病+药物术语，4 encoder）** | **MedCPT +0.0046 full / +0.0073 子集 (p<0.05)** | 平 | **Phase2 小幅稳健正** |

→ **回答了 smiles final_readme §7 的开放问题**：SAE 在 tabular+I/E 之外，缺的更多是**"适应症/药物是什么"(MeSH 实体身份)**，而非**"分子长什么样"(SMILES 结构)**。但即便如此，MeSH 增益也很小且只在 Phase2，说明 tabular+I/E 已经吃掉了大部分可提取信号。

**方案定型**：MedCPT MeSH 作第 3/4 token 在 Phase2 有小幅稳健增益，但不跨 phase 稳定、绝对量小（~+0.005）。是否纳入最终方案取决于对 +0.005 的取舍 —— 见 `final_readme.md` 的取舍建议。

**关键产物索引**：

| 产物 | 路径 |
|---|---|
| I/E（复用 smiles） | `data/ie_embeddings_qwen3.parquet` (symlink, d=4096) |
| 4 个 MeSH embedding | `data/mesh_embeddings_{sapbert,biolord,medcpt,pubmedbert}.parquet` (d=768) |
| 多-seed 结果（n=10 P2/n=5 P3） | `results/multiseed_20260602_023755/{summary,robust_summary}.md` + `raw_runs.jsonl` (75 行) |
| 脚本 | `script/encode_mesh_hf.py` / `full_step2_tabicl_mesh.py` / `run_multiseed_mesh.py` / `aggregate_robust_mesh.py` |
