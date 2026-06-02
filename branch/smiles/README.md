# branch/smiles — 在 TabICLv2+I+E 基础上加 SMILES virtual token

> 进入本目录前请先看 [`/data2/zhu11/TB/ReadMeFirst.md`](../../ReadMeFirst.md)；branch 规约见 [`../README.md`](../README.md)。
>
> 本文件原为 `initial_readme.md`（cold-read 起点文档），现已升格为 `README.md`（进度日志）。下方 §1-§10 仍保留原始起点文档内容（架构/数据/设计决策的 cold-read 入口），**新增的实验进度记录在文末 §11 "实施进度日志"** 里，按时间顺序追加。

---

## 1. TL;DR — 这个 branch 要做什么

在 **TabICLv2 + tabular + I/E 两个 virtual token** 的基础架构上，**多加一个 SMILES virtual token**（药物分子结构 embedding），在 **SAE (serious-adverse-event-forecasting) Phase 1 / Phase 2 / Phase 3 三个 phase 分别**训练并测试。

期望产出：每个 phase 一行 `baseline (TabICL zero-shot) | +I+E | +I+E+smiles | Δ` 的对照表。

---

## 2. 项目上下文（30 秒速通）

`/data2/zhu11/TB/` 是 TabPFN + TrialBench 的工作目录。我们在临床试验数据（TrialBench, 8 个子任务 × 4 个 phase）上预测各种事件。

| Branch | 状态 | 重要结论 |
|---|---|---|
| `IE_embedding/` | 已落地 | 把 eligibility 的 inclusion/exclusion criterion 文本编码 → mean-pool → 注入 TabPFN 做 +IE 增益（历史用 MedCPT 编的，新分支统一改用 Qwen3-Embedding-8B；详见 §3 / §4.2 Q1） |
| `new_FM/` | 已收尾 → **TabICLv2** | TabPFN 权重 non-commercial，找了 BSD-3 的 TabICLv2 替代；同样支持 "2 virtual feature token" 注入 |
| `mesh/` | 另一条 branch（并行做） | 加 condition/intervention MeSH 作 3rd virtual token |
| `smiles/` | **本 branch（待开工）** | 加 SMILES 作 3rd virtual token |

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
      I/E embedding** 落 branch/smiles/data/ie_embeddings_qwen3.parquet，再做 smiles。

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
proj_incl(incl_mean)    + col_emb[0]   # 已有
proj_excl(excl_mean)    + col_emb[1]   # 已有
proj_smiles(smiles_mean) + col_emb[2]  # 新增
cat → (B, T, H+3, 128)
```

**encoder 选用**：
- I 和 E 用 **Qwen3-Embedding-8B**（d_IE ≈ 4096，跟项目其他 branch 统一）
- SMILES 用**单独的化学 encoder**——具体哪个 **TBD**，开工前要跟用户对齐（详见 §4.2 Q1）

可训练参数 ≈ `2 × Linear(4096, 128) + 1 × Linear(d_smiles, 128) + col_emb(3, 128)`。Qwen3 那两路占 ~1.05M；SMILES proj 那一路看 encoder 输出维度（384-d 类的加 ~50K，768-d 类的加 ~100K，4096-d 类的加 ~525K）。总数大致 1.1–1.6M，仍只占 base TabICL 27.6M 的 4–6%。

### 4.1 SMILES 数据源（在 TrialBench train_x.csv 里）

| 列名 | 非空率 (SAE Phase2) | 典型值 |
|---|---|---|
| `smiless` | 54.3% | 字符串化的 SMILES 列表 `"['CN1CCN(CCOC2=CC3=...)CC1']"`；多数情况是 1 条 SMILES，少数 trial 有多条 |

**重要 caveats**：
- 这一列是 **stringified Python list literal**，要 `ast.literal_eval` 解析；解析失败时尝试 `json.loads`；都失败就当一条 SMILES
- **非空率只有 54%** —— 比 mesh (95%/67%) 低很多。意思是 ~46% 的 SAE Phase 2 trial 没有 SMILES，强烈影响信号上限。考虑在 final_readme 里 report "有 SMILES 子集" vs "全集" 两套数字
- 一个 trial 可能有 ≥1 个 SMILES（多药联合用药）。mean-pool 是稳妥默认；也可以试 max-pool / 看不同药分开（但 4 个 token 就更多了）

### 4.2 设计选择（要先跟用户/团队确认）

| 问题 | 选项 | 推荐 |
|---|---|---|
| Q1: SMILES 用什么 encoder | **TBD —— 开工前要跟用户讨论**。候选清单（agent 起步可以先列出来跟用户对齐）：(a) ChemBERTa-77M-MLM (DeepChem, BPE on SMILES, d=384) / (b) MolFormer-XL (IBM, SMILES+物性联合, d=768) / (c) Mol2Vec (老 word2vec 风格, d=300) / (d) ChemBERTa-2 / MoLFormer-XL-both-10pct 等更新版 / (e) 其他 | **TBD**——这一栏空着，等用户给方向。**I 和 E 走 Qwen3-Embedding-8B 不变**（项目其他 branch 一致），但 SMILES 一定用独立的化学 encoder（用户明确要求 mesh / SMILES 各自专用 encoder） |
| Q2: 多 SMILES per trial 怎么聚合 | (a) mean-pool / (b) max-pool 拼接 / (c) 每个 SMILES 都做 1 个 token（动态列数） | **(a) mean-pool** 最稳，跟 IE 的 mean-pool criterion 风格一致 |
| Q3: 缺失 SMILES 的 trial（~46%）怎么处理 | (a) 零向量 / (b) 在 dataset 里 drop 掉这些 trial / (c) 用全集 SMILES mean 当 fallback | **(a) 零向量** 跟 [`full_step2_tabicl.py`](../new_FM/script/full_step2_tabicl.py) 的现有 mesh-style fallback 一致；同时**额外 report**「只跑 SMILES 非空子集」一套数字看真实信号 |

---

## 5. 实验设计

### 5.1 训练 / 评估范围

只测 **SAE (serious-adverse-event-forecasting)**，binary 分类，target = `Y/N`。

3 个 phase 分开跑（不合并）：Phase 1、Phase 2、Phase 3。

每个 phase 跑：
- **Cell A**: baseline = TabICL zero-shot（无虚拟列）
- **Cell B**: +I+E = TabICL Full Step 2 with 2 virt tokens
- **Cell C**: +I+E+smiles = TabICL Full Step 2 with 3 virt tokens — **本 branch 的核心**
- **(可选) Cell D**: Cell C 在 SMILES 非空子集上的数字（剔除 ~46% 没 SMILES 的 trial）

共 9–12 个 cells。Cell A、B 在 Phase 2/3 已有现成结果（见 §3 表），只需要补 Phase 1 + Phase 1/2/3 的 Cell C。

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
# X_train / X_test 是 pandas DataFrame，含 'smiless' 列
```

注意：`preprocess()` 会 drop 一组 TEXT_DROP 文本列。**确认 `smiless` 不在 TEXT_DROP 里**（TEXT_DROP 见 `script/sae_finetune.py` 顶部，需要的时候 grep 一下确认）。如果在，需要在 SMILES encoding pipeline 里**先**从原始 `X_train`/`X_test` 提取再做 preprocess。

---

## 6. 实现路径（建议）

### 6.1 Encoding 脚本（两个，分别用不同 encoder）

#### 6.1.a I/E embedding (Qwen3)

新建 `branch/smiles/script/encode_ie_qwen3.py`：
- 用 `Qwen/Qwen3-Embedding-8B` 把 inclusion / exclusion criterion 重编一份
- 输出：`branch/smiles/data/ie_embeddings_qwen3.parquet` 含列 `trial_id, phase, type ∈ {I, E}, mean_emb` （d≈4096）

> 项目历史在 `branch/IE_embedding/results/encode_medcpt_*` 有 MedCPT 版的 I/E embedding 缓存，但 d=768；本 branch 要重编 Qwen3 版好跟其他 Qwen3-using branch 对齐。

#### 6.1.b SMILES embedding (encoder TBD)

新建 `branch/smiles/script/encode_smiles_<encoder>.py`（文件名等 §4.2 Q1 跟用户对齐后再定）：
- 输入：扫描所有 (subtask, phase, split) 的 train_x.csv，提取 `smiless` 列
- 对每个 (trial_id, phase)：
  1. 解析 SMILES list（`ast.literal_eval` + 兜底单字符串）
  2. 每条 SMILES 用**待定的化学 encoder** 编码 → d_smiles 维（具体维度看 encoder）
  3. mean-pool over 该 trial 的所有 SMILES → 1 个 d_smiles 向量
- 输出：`branch/smiles/data/smiles_embeddings.parquet` 含列 `trial_id, phase, mean_emb` （维度看选的 encoder）

#### Pipeline 形状参考

无论用什么 encoder，两个脚本的整体形状都跟 [`branch/IE_embedding/script/encode_medcpt.py`](../IE_embedding/script/encode_medcpt.py)（~200 行）一样：批量编码 + parquet 落盘 + 进度条 + bf16 forward。**只是 encoder load 和 tokenizer 那两行换掉**。看那个脚本能 cold read 学到所有 boilerplate，~10 分钟内就能 fork。

**注意（SMILES 特定）**：
- SMILES 是 ASCII 字符串，化学 encoder 一般直接吃 raw SMILES（不需要 RDKit 预处理）；但选定 encoder 后要看它的 tokenizer 是否需要特定预处理（如 canonicalize）
- 多数化学 encoder 的 batch size 可以比 IE 大（SMILES 平均长度 30~80 chars，比 criterion text 短）
- bf16 forward；最后存 fp32 parquet
- 跟 IE 一样用 `(trial_id, phase)` 作 key

### 6.2 Full Step 2 训练脚本

新建 `branch/smiles/script/full_step2_tabicl_smiles.py`：fork `branch/new_FM/script/full_step2_tabicl.py`，改：

1. 加载 I/E (Qwen3, 4096-d) + SMILES (TBD encoder, d_smiles) embedding 并对齐到 X_train.index：
   ```python
   D_IE = 4096          # Qwen3-Embedding-8B output dim
   D_SM = ...           # SMILES encoder output dim, 看 §4.2 Q1 选的 encoder
   ie_emb     = pd.read_parquet("data/ie_embeddings_qwen3.parquet").set_index(["trial_id", "phase", "type"])
   smiles_emb = pd.read_parquet("data/smiles_embeddings.parquet").set_index(["trial_id", "phase"])
   def align(X_df, kind):
       d = D_SM if kind == "smiles" else D_IE
       out = np.zeros((len(X_df), d), dtype=np.float32)
       for i, (tid, ph) in enumerate(zip(X_df.index.astype(str), X_df["phase_split"].astype(str))):
           key = (tid, ph) if kind == "smiles" else (tid, ph, kind)  # 'I'/'E'/'smiles'
           src = smiles_emb if kind == "smiles" else ie_emb
           if key in src.index:
               out[i] = src.loc[key, "mean_emb"]
       return out
   incl_train = align(X_train_p, "I");  excl_train = align(X_train_p, "E"); smiles_train = align(X_train_p, "smiles")
   incl_test  = align(X_test_p,  "I");  excl_test  = align(X_test_p,  "E"); smiles_test  = align(X_test_p,  "smiles")
   ```
2. `TabICLVirtualInjection` 类：把 `proj_incl/proj_excl + virt_col_emb (2, E)` 扩成 3 套——`proj_incl: Linear(4096, E)`、`proj_excl: Linear(4096, E)`（I/E 都是 Qwen3 4096-d），`proj_smiles: Linear(D_SM, E)`（化学 encoder 维度），`virt_col_emb (3, E)`。`forward` cat 3 列虚拟而不是 2 列
3. 注意 dtype: 投影输出 fp32，cat 前 cast 回 col_out.dtype（fp16）

### 6.3 跑实验

```bash
# 先确保 Phase 1 的 baseline 和 +I+E 已经跑过（§3 末尾的 2 个 cmd）

# 然后跑本 branch 的 Cell C × 3 phase
for ph in Phase1 Phase2 Phase3; do
  python /data2/zhu11/TB/branch/smiles/script/full_step2_tabicl_smiles.py \
    --subtask serious-adverse-event-forecasting --target Y/N --task-type binary \
    --phase $ph --epochs 30
done
```

---

## 7. 期望产出

| 文件 | 用途 |
|---|---|
| `branch/smiles/data/ie_embeddings_qwen3.parquet` | Qwen3-Embedding-8B 重编的 I/E embedding（替换历史 MedCPT 768-d 版本，d≈4096） |
| `branch/smiles/data/smiles_embeddings.parquet` | SMILES 专用化学 encoder 编的 embedding（encoder TBD）|
| `branch/smiles/script/encode_ie_qwen3.py` | I/E encoding 脚本（Qwen3）|
| `branch/smiles/script/encode_smiles_<encoder>.py` | SMILES encoding 脚本（encoder 名待定）|
| `branch/smiles/script/full_step2_tabicl_smiles.py` | TabICL Full Step 2 + 3 virt tokens 训练脚本 |
| `branch/smiles/results/<run_id>/metrics.json` | 每个 phase 的 train history + best metrics |
| `branch/smiles/README.md` | 进度日志（替换本 `initial_readme.md`，详见 [`branch/README.md`](../README.md) §3） |
| `branch/smiles/final_readme.md` | 终态文档（方案定下来后写）|

最终在 `README.md` 或 `final_readme.md` 里要给出 3 phase × 3 cell = 9 cell 表（外加可选的 Cell D "SMILES 非空子集"）：

```
| Phase | TabICL zero-shot | +I+E | +I+E+smiles | Δ(smiles) | +I+E+smiles (SMILES-only subset) |
| 1     | ?                | ?    | ?           | ?         | ?                                 |
| 2     | 0.8241           | 0.8658 | ?         | ?         | ?                                 |
| 3     | 0.8968           | 0.9078 | ?         | ?         | ?                                 |
```

**预期方向**：SMILES 加进来主要应该帮区分**药物结构 / 药效团相关的副作用倾向**。但 SAE 的副作用率跟 trial 设计、人群、给药方式都相关，SMILES 边际信号可能不大。**~46% 的 trial 没 SMILES**，这本身就拖低信号上限——所以 Cell D（SMILES-only subset）是判断"真实增益 vs 平均化"的关键。

可能的负向情景：参考 [`branch/new_FM/README.md` §5 第四轮结论 §3 关于 patient-dropout subtask 的发现](../new_FM/README.md) —— 当 tabular + IE 已经把信号吃完时，多加 token 反而会引入扰动让 trained projection 跑偏。

---

## 8. 重要踩坑预警

### 8.1 TabICL 内部 fp16，projection 输出 fp32

cat 之前要 cast。参考 [`full_step2_tabicl.py:112-119`](../new_FM/script/full_step2_tabicl.py)：

```python
v_in = smiles_T_d.to(col_out.device).to(self.proj_smiles.weight.dtype)  # fp32 做投影；d = SMILES encoder 输出维度
smiles_te = self.proj_smiles(v_in) + self.virt_col_emb[2]                # (T, E) fp32
smiles_t1e = smiles_te.unsqueeze(1).to(col_out.dtype)                    # (T, 1, E) cast 回 fp16
smiles_b_t_1_e = smiles_t1e.unsqueeze(0).expand(B, -1, -1, -1).contiguous()
col_aug = torch.cat([col_out, virt_incl_excl, smiles_b_t_1_e], dim=2)
```

### 8.2 SMILES 解析容错

```python
import ast, json
def parse_smiles(s):
    if not isinstance(s, str) or not s.strip():
        return []
    try:
        v = ast.literal_eval(s)
        return v if isinstance(v, list) else [v]
    except Exception:
        try:
            v = json.loads(s)
            return v if isinstance(v, list) else [v]
        except Exception:
            return [s]  # 兜底当成单条 SMILES
```

### 8.3 SMILES 非空率只有 54%

显著影响信号。强烈建议：训练完后**额外** report 一组「SMILES 非空 trial 子集」上的指标 (Cell D)，跟全集 (Cell C) 对照看 SMILES 信号真实强度。

### 8.4 同一个 (trial_id, phase) 跨 subtask 共享

跟 IE 一样，SMILES 属于 trial 自己的属性，不同 subtask 共享。本 branch 只跑 SAE，无所谓；将来扩到其他 subtask 时直接 join 即可。

### 8.5 env 注意

```bash
source /data2/zhu11/miniconda3/etc/profile.d/conda.sh && conda activate tabpfn
```

`tabpfn` env 里 `torch 2.9.1` / `transformers 4.57.6` / `pandas 2.3.3` / `tabicl 2.1.1` 都装好了。

**Qwen3-Embedding-8B** (I/E 用)：`transformers.AutoTokenizer + AutoModel.from_pretrained('Qwen/Qwen3-Embedding-8B', torch_dtype='bfloat16')` 加载，~16 GB bf16 权重，首次自动从 HF 下；H200 单卡放得下。

**SMILES encoder** (待定)：等 §4.2 Q1 跟用户对齐选定后再装。多数化学 encoder（ChemBERTa / MolFormer 等）都在 HF 上，直接 `pip install transformers` 应该够（env 里有 transformers 4.57.6）；如果选 RDKit-based 工具或专项框架，可能需要额外装包甚至单建 env。

---

## 9. 跟用户/团队对齐（开工前请确认）

1. §4.2 Q1: **SMILES encoder 选哪个 —— 必须先跟用户对齐**（用户明确说 SMILES 要用专用化学 embedder，不复用 Qwen3）。开工前先列一个候选清单（ChemBERTa / MolFormer / Mol2Vec / 其他）跟用户讨论拍板。**I/E 走 Qwen3 不需要对齐**（已定）
2. §4.2 Q3: 缺失 SMILES 怎么处理（推荐零向量 + 额外 report SMILES-only subset）
3. §5.1 实验范围：只 SAE 还是顺手把其他 5 个 subtask 也加上（user 说 "在 SAE 的 phase 1-3 上"，所以默认只 SAE，但跑完可以聊扩展）
4. **不**对齐就开始 §6 的 6.1 + 6.2，把 encoding pipeline 跑通是确定能用的工作

---

## 10. 重要参考文档（按优先级，需要时按需读）

| 文件 | 何时看 | 看什么 |
|---|---|---|
| [`/data2/zhu11/TB/branch/README.md`](../README.md) | **开工前必看** | branch 目录规约、README.md vs final_readme.md 区别 |
| [`/data2/zhu11/TB/branch/new_FM/final_readme.md`](../new_FM/final_readme.md) | **开工前必看** | TabICLv2 的 license / API / drop-in 方式 / 已知坑 |
| [`/data2/zhu11/TB/branch/new_FM/script/full_step2_tabicl.py`](../new_FM/script/full_step2_tabicl.py) | **要 fork 它** | 337 行；这是基础模型的完整实现，看 `TabICLVirtualInjection` 类（~50 行）+ `main()` 训练 loop 即可 |
| [`/data2/zhu11/TB/branch/IE_embedding/script/encode_medcpt.py`](../IE_embedding/script/encode_medcpt.py) | 写 encode_ie_qwen3 和 encode_smiles_<...> 时参考 | **批量 HF transformer 编码 pipeline 模板**（GPU、bf16、进度条、parquet 落盘）—— 只看 pipeline 形状，**I/E 那条 encoder 换成 Qwen3-Embedding-8B；SMILES 那条 encoder 等 §4.2 Q1 跟用户对齐再定** |
| [`/data2/zhu11/TB/branch/IE_embedding/script/full_step2_train.py`](../IE_embedding/script/full_step2_train.py) | mean_pool_per_trial 工具函数 | full_step2_tabicl.py 顶部 import 的 `mean_pool_per_trial / align_virt_emb / build_sklearn_preprocessor` 都在这；改写时直接 import 复用 |
| [`/data2/zhu11/TB/ReadMeFirst.md`](../../ReadMeFirst.md) | env / 路径不熟时翻 | 项目顶层规约、命名 / 落盘约定 |
| [`/data2/zhu11/TB/branch/IE_embedding/README.md`](../IE_embedding/README.md) §4 | 想理解架构选型时 | 为什么是 virtual token + 几个备选 (raw concat / PCA / stacking / Full Step 2) 的对比 |

旧 readme 不要全部塞进 context，按上表按需 cherrypick；先把这份 initial_readme 内化好，对架构和数据流就够了。

---

## 11. 一个推荐的 day-1 节奏

1. (10 min) 读 §1-§5 + 上面 §10 前 3 行
2. (15 min) 准备 §9 三个问题（特别是 Q1 SMILES encoder 候选清单）跟用户对齐
3. (30 min) 把 SAE Phase 1 的 baseline (Cell A) 和 +I+E (Cell B) 用现成脚本补完（§3 末尾两个 cmd）；同时跑一次 EDA 看 SMILES 列的真实结构 + 多 SMILES per trial 比例
3. (1 h) 写 `encode_ie_qwen3.py`：参考 [`encode_medcpt.py`](../IE_embedding/script/encode_medcpt.py) 的 pipeline 形状 fork 一份，encoder 换成 **Qwen3-Embedding-8B**，输入字段是 inclusion/exclusion criterion 文本（用 Qwen3 重编一份 I/E embedding 落 `data/ie_embeddings_qwen3.parquet`）
4. (0.5 h) 跟用户对齐 §4.2 Q1 SMILES encoder 选哪个，定下来后写 `encode_smiles_<encoder>.py`（pipeline 形状一样，encoder load 换一下）
5. (1-2 h) 跑两条 encoding，产出 `data/ie_embeddings_qwen3.parquet` + `data/smiles_embeddings.parquet`，sanity check shape 和缺失率
6. (1 h) fork [`full_step2_tabicl.py`](../new_FM/script/full_step2_tabicl.py)，扩成 3 virtual token（I/E 走 4096-d，SMILES 走 d_smiles）；先跑 SAE Phase 2 smoke 看是否能收敛、跟 +I+E only 比有没有有意义的 Δ
7. 跑完 3 phase × Cell C；如果想 push，加 Cell D (SMILES-only subset)。Δ 显著正向 → 写 `final_readme.md`；不显著 → epoch / lr / 多 SMILES 处理调参，或跟用户讨论换一个化学 encoder 重跑

祝顺利。有疑问翻 §10 的文档；架构疑问直接读 `full_step2_tabicl.py`，比看任何二手描述都直接。

---

## 11. 实施进度日志

按时间倒序，每轮实验完后追加一段。

### 2026-06-01 — Day 1：encoding pipeline + 训练脚本搭好

**对齐**：跟用户确认 (1) 只测 Phase 2/3，(2) SMILES 用 4 个 encoder 都跑一遍取最强，(3) 缺失 SMILES 用零向量 fill + 额外 report SMILES-only subset (Cell D)，(4) 只 SAE 子任务，(5) Qwen3 重编 I/E embedding 落 `data/ie_embeddings_qwen3.parquet`。新发现 ——§3 表里旧的 +I+E 数 (Phase2 0.8658 / Phase3 0.9078) 是 MedCPT 768-d 编码，要换 Qwen3 4096-d 后**重跑 Cell B'**，确保跟 Cell C 公平对照。

**实验矩阵确定**（Phase 2/3 × 5 cell config = 10 个训练 run）：

| Cell | 内容 | n run |
|---|---|---|
| A | TabICL 零样本（已有数 §3） | 0 |
| B' | TabICL +I+E (Qwen3) | 2 |
| C₁..C₄ | TabICL +I+E+SMILES，4 个 encoder | 2 × 4 = 8 |
| D | C 在 SMILES 非空子集 re-eval | 同 C run 内输出 |

**写完 + smoke 过的脚本**：

| 脚本 | 用途 | smoke 结论 |
|---|---|---|
| `script/encode_ie_qwen3.py` | 用 Qwen3-Embedding-8B 编 1.58M criterion → mean-pool per (trial_id, phase, type) → 4096-d | smoke `--limit 4096` @ batch 128 跑出 495/s；预计全量 ~3 h |
| `script/encode_smiles_hf.py` | 一个脚本带 `--model` switch 支持 3 个 HF chem encoder | 3 个 encoder 都 smoke 过 |
| `script/encode_smiles_mol2vec.py` | gensim Word2Vec + RDKit Morgan radius=1 SMILES → 300-d (CPU-only) | 200 SMILES @ 5600/s |
| `script/full_step2_tabicl_smiles.py` | fork 自 `../new_FM/script/full_step2_tabicl.py`：扩成 2 or 3 virt token（`--smiles-emb` 决定），auto-detect d_ie/d_sm，Cell D 子集 metrics 内置 | 2-epoch smoke @ Phase2 跑通；初值 ROC-AUC 0.80，3 virt cols 1.1M 可训练参数 |

**踩坑**：
- `torchvision 0.26.0+cu128` 跟 `torch 2.9.1` 不兼容（`torchvision::nms` operator 注册失败），波及 transformers 的 lazy import 链 → 直接卸 torchvision（项目不用）
- MolFormer 的 init 在 CPU 做 QR 分解，bf16 不支持 → fp32 加载 + 移 GPU 后再 cast bf16
- mol2vec 0.2.2 用 gensim 3.x API (`model.wv.vocab`)，跟 gensim 4.x 不兼容 → inline 重写 `sentences2vec`（modern `key_to_index` API，行为等价：SUM of token vectors per molecule）
- `sae_finetune.preprocess` 的 `TEXT_DROP` 包含 `smiless` —— SMILES encoding 要从原始 `train_x.csv` 读，不能依赖 preprocess 后的 X（已正确实现）

**4 个 SMILES encoder 全量产物**（跑完，每个 SAE 全 17,916 (trial_id, phase) × 53.7% non-empty = 9,612 行 mean-pool 输出）：

| Encoder | HF model | d | norm mean ± std |
|---|---|---|---|
| ChemBERTa-MLM | `DeepChem/ChemBERTa-77M-MLM` | 384 | 3.23 ± 0.43 |
| ChemBERTa-MTR | `DeepChem/ChemBERTa-77M-MTR` | 384 | 7.80 ± 2.13 |
| MolFormer-XL | `ibm/MoLFormer-XL-both-10pct` | 768 | 15.76 ± 1.75 |
| Mol2Vec | gensim `model_300dim.pkl` | 300 | 124.70 ± 91.80 (SUM not MEAN, 跟分子大小相关) |

**目前进行中**：I/E Qwen3 全量 encoding @ batch 128（启动 21:41，~3 h ETA → 预计 00:30 完成）。完成后立刻跑 10 个训练 run（每个 ~1-2 min）。

**下一步**：等 I/E 完成 → 10 训练 run → 汇总到 9-cell + Cell D 表 → 决定是否写 `final_readme.md`（Δ 显著正向）或调参重跑（Δ 不显著）。

### 2026-06-02 — I/E 完成 + 训练 + **发现 CUDA 非确定性 → 改多-seed** + 最终结论

**I/E Qwen3 全量完成**：1,579,161 criteria，68 min（387/s, batch 128），158,476 mean-pool groups（I 81,716 / E 76,760），覆盖 81,742 个 (trial_id, phase)；无 NaN，norm 131.7±2.4。落 `data/ie_embeddings_qwen3.parquet`（2.6 GB, d=4096）。SAE Phase2/3 覆盖率 ~100%（Phase2 train 6513/6516，test 1600/1600；Phase3 train 3892/3895，test 945/945）。

> **踩坑**：第一次跑到 28% 被打断且未落盘（脚本只在跑完才 mean-pool）。给 `encode_ie_qwen3.py` 加了 **checkpoint/resume**：`np.lib.format.open_memmap` 实时写 + 每 50 batch 落 `encode_state.json`，支持 `--resume <run_dir>`。验证过 resume 与一次跑完结果一致。

**第一轮 10 个单次 run（已弃用，仅作教训）**：跑出来的数看着像"Phase3 ChemBERTa-MLM 0.9246 (+0.0096 over B')、Phase2 Mol2Vec 0.8773"等正向 Δ。**但这些是单次结果，不可信**（见下）。

**🔴 关键发现 —— TabICL forward/backward 是 CUDA 非确定性的**。同一配置、同一 `--seed` 连跑 3 次 B' Phase2：**0.8655 / 0.8724 / 0.8748**，spread ≈ 0.009 ROC-AUC。噪声来自 30 epoch 训练 projection 时 GPU atomic 累加的非确定性归约顺序。**这个噪声底跟想测的 SMILES 效应同量级**，单次 run 的 ±0.01 Δ 完全没有意义。

→ 改用 **多-seed 实验**：`script/run_multiseed.py`，5 config (B' + 4 encoder) × 2 phase × 5 seed = **50 run**，报 mean ± std。同时 `script/aggregate_robust.py` 从每个 child 的 history 额外算 **last5**（末 5 eval epoch 均值，绕开 best-epoch 的 max-噪声偏置）和 final 两个收敛指标。
- run_dir: [`results/multiseed_20260602_002504/`](results/multiseed_20260602_002504/)（`summary.md` / `robust_summary.md` / `raw_runs.jsonl`）
- 给训练脚本加了 `--report-subset-emb`：B' 不注入 SMILES，但用同一 mask 报 SMILES 子集指标，作为 Cell D 的干净 baseline（之前缺 B'-subset 无法干净归因）

**最终结果（mean ± std over 5 seeds，metric = last5 末5epoch均值）**：

Phase 2（full test 1600；SMILES 子集 n=844）：

| Cell | Full ROC-AUC | Δ vs B' | SMILES 子集 | Δ vs B' |
|---|---|---|---|---|
| B' (+I+E, Qwen3) | 0.8541 ± 0.0039 | — | 0.8543 ± 0.0032 | — |
| C: ChemBERTa-MLM | 0.8561 ± 0.0069 | +0.0020 | 0.8551 ± 0.0041 | +0.0009 |
| C: ChemBERTa-MTR | 0.8568 ± 0.0043 | +0.0027 | 0.8563 ± 0.0047 | +0.0020 |
| C: MolFormer | 0.8534 ± 0.0038 | −0.0007 | 0.8498 ± 0.0045 | −0.0044 |
| C: Mol2Vec | 0.8570 ± 0.0048 | +0.0029 | 0.8565 ± 0.0065 | +0.0022 |

Phase 3（full test 945；SMILES 子集 n=470）：

| Cell | Full ROC-AUC | Δ vs B' | SMILES 子集 | Δ vs B' |
|---|---|---|---|---|
| B' (+I+E, Qwen3) | 0.8925 ± 0.0033 | — | 0.9087 ± 0.0075 | — |
| C: ChemBERTa-MLM | 0.8858 ± 0.0066 | −0.0067 | 0.9044 ± 0.0052 | −0.0043 |
| C: ChemBERTa-MTR | 0.8887 ± 0.0103 | −0.0038 | 0.9009 ± 0.0079 | −0.0078 |
| C: MolFormer | 0.8915 ± 0.0060 | −0.0009 | 0.9110 ± 0.0060 | +0.0023 |
| C: Mol2Vec | 0.8898 ± 0.0054 | −0.0027 | 0.9076 ± 0.0049 | −0.0011 |

（best-epoch 与 final 指标的完整表见 [`results/multiseed_20260602_002504/robust_summary.md`](results/multiseed_20260602_002504/robust_summary.md)；趋势一致。）

**结论：在 SAE 上，把 SMILES 作为第 3 个 virtual token 没有稳健增益。**
1. **Phase 2**：4 个 encoder 的 Δ 都在 +0.002~+0.003，**小于各自 std**，统计上 ≈ 0。
2. **Phase 3**：Δ 全部为负（−0.007~−0.001），ChemBERTa-MLM 的 −0.0067 超过噪声底 → 轻微但真实的退化。
3. **Cell D 没翻盘**：即使只看有 SMILES 的 trial，C 仍 ≈ B' 或更差。说明不是"46% 缺失稀释"问题，而是 **SMILES 对 SAE 在 tabular + I/E 之外没有增量信号**。
4. **encoder 之间无显著差异**（都在噪声内）；MolFormer 在 Phase3 最不伤（full −0.0009 / 子集 +0.0023，均在噪声内 = 中性）。
5. 印证了 initial_readme §7 / new_FM patient-dropout 的预警：tabular+IE 已吃满信号时，多加一个 trainable projection 反而扰动 frozen base、轻微跑偏。

**附带正向结论 —— Qwen3 I+E（B'）本身是有效的**（A→B' 用 best 指标对照 §3）：

| Phase | A 零样本(§3) | 旧 MedCPT +IE(§3) | Qwen3 B' best (multiseed) | A→B' |
|---|---|---|---|---|
| 2 | 0.8241 | 0.8658 | 0.8656 ± 0.0059 | **+0.0415** |
| 3 | 0.8968 | 0.9078 | 0.9150 ± 0.0051 | **+0.0182** |

Qwen3 (4096-d) 跟旧 MedCPT (768-d) 在 I+E 上基本持平（P2 0.8656≈0.8658，P3 0.9150>0.9078 略好），换 encoder 不亏，且统一了项目栈。

**方案定型**：SMILES 这条线到此为止——**不纳入 SAE 最终方案**。最优配置仍是 new_FM 的 **TabICLv2 + I+E (Full Step 2)**，I/E 用 Qwen3-Embedding-8B 重编。下一步写 `final_readme.md` 收尾（终态文档），并在 `../README.md` §1 表 + `ReadMeFirst.md` §7 更新状态。

**关键产物索引**：

| 产物 | 路径 |
|---|---|
| I/E Qwen3 embedding | `data/ie_embeddings_qwen3.parquet` (d=4096) |
| 4 个 SMILES embedding | `data/smiles_embeddings_{chemberta_mlm,chemberta_mtr,molformer,mol2vec}.parquet` |
| 多-seed 最终结果 | `results/multiseed_20260602_002504/{summary,robust_summary}.md` + `raw_runs.jsonl` |
| encoding 脚本 | `script/encode_ie_qwen3.py`（resumable）/ `encode_smiles_hf.py` / `encode_smiles_mol2vec.py` |
| 训练脚本 | `script/full_step2_tabicl_smiles.py`（2 or 3 virt token, `--smiles-emb` / `--report-subset-emb`）|
| 多-seed driver + 聚合 | `script/run_multiseed.py` / `script/aggregate_robust.py` |
