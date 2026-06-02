# branch/new_FM/final_readme.md — TabPFN → TabICLv2 替代方案（最终结论）

> 这是 `branch/new_FM/` 的**终态文档**，给后续 AI agent / 协作者 cold-read 用。
> 进度日志 / 试错过程见 [`README.md`](README.md)；进 branch 之前请先看 [`../../ReadMeFirst.md`](../../ReadMeFirst.md)。

---

## TL;DR

TabPFN-v2.5 模型权重以 **non-commercial** 条款单独授权（research 免费、商用付费）；为给 TabBench 的下游产品/商用管线准备替代，本 branch 测了 5 个候选 tabular FM。

**最终选定 [TabICLv2](https://github.com/soda-inria/tabicl) (BSD-3-Clause, INRIA Soda, Qu et al., 2025)** 作为 TabPFN 的 drop-in 替代：

- License 干净：BSD-3-Clause，不要 PriorLabs-style 强制归属；商用只要在源码层保留 LICENSE 文件即可
- 性能持平甚至略优 TabPFN-v2.5：6 个 TrialBench 子任务 4-phase 合并 zero-shot 上，TabICL 全 6 个持平或微优，trial-duration regression 上明显胜出 (+0.0185 R²)
- 接入零成本：sklearn-style `fit / predict_proba`，唯一差异是非数值列要先 ordinal encoding（TabPFN 直接吃 pandas string，TabICL 要 numeric ndarray）
- 推理时间相当或更快：同等 setup 下与 TabPFN 在 3~5s/任务 量级一致

下面给具体数据、接入方式、和已知坑。

---

## 1. 候选清单 + 为什么不是其他几个

按 license 和可用性筛后，本轮实际测试了 **4 个**：

| Model | License | 测试结果 | 选 / 没选 |
|---|---|---|---|
| **TabPFN-v2.5** | Apache 2.0 + Llama-style 归属；**权重 non-commercial** | 项目当前 anchor | 商用不能用 → 砍 |
| **TabICLv2** | **BSD-3-Clause** | 6/6 zero-shot 持平或微优 TabPFN | **选** |
| **TabDPT-v1.1** | Apache-2.0 | 5/6 binary/multiclass 略弱 TabPFN (−0.005 ~ −0.012)；regression 微优；推理时间 4–50× 慢 | 备选；性能 + 速度都不如 TabICL |
| **Mitra (autogluon)** | Apache-2.0 | zero-shot 在 multiclass 塌缩到 majority class（failure-reason macro-F1=0.150 完全没动）；binary/regression OK | 备选；需要 `fine_tune=True` 才能发挥，没有 zero-shot 的简洁性 |

**调研但本轮跑不了的**（详见 [`README.md` §2](README.md)）：

| Model | License | 阻塞 |
|---|---|---|
| MotherNet / TabFlex / GAMformer (microsoft/ticl) | Apache-2.0 | 权重托管在 `amuellermothernet.blob.core.windows.net`（已下线），HF 上无镜像；torch 2.11 兼容补丁已打在 `data/mothernet/ticl/models/layer.py`，等权重可访问就能跑 |
| sap-rpt-1-oss (前 ContextTab) | Apache-2.0 | HF gated (auto-approve)，本机无 HF_TOKEN |
| LimiX-16M / 2M | Apache-2.0 | 要 Python 3.12.7 + flash-attn，本 env 是 3.11，需要单建 env |
| HyperFast | **CC BY-NC 4.0** | non-commercial，不符合 license 要求 |
| nanoTabPFN | (educational) | 没有 pretrained 权重，只是训练代码 |

---

## 2. TabICLv2 详情

- **GitHub**: <https://github.com/soda-inria/tabicl>
- **HuggingFace 权重**: `jingang/TabICL-clf`（分类）/ `jingang/TabICL-reg`（回归），自动下载到 `~/.cache/huggingface/`
- **论文**: [arXiv:2502.05564](https://arxiv.org/abs/2502.05564) — "TabICL: A Tabular Foundation Model for In-Context Learning on Large Data"
- **架构**: 3 阶段 transformer
  1. **Column-wise embedding** (`col_embedder`): 每个 cell → distribution-aware embedding (B, T, H, E=128)，含 G 个 feature group + C 个 CLS tokens
  2. **Row-wise interaction** (`row_interactor`): 跨 feature attention per row
  3. **ICL predictor** (`icl_predictor`): in-context learning over labeled rows，输出 (B, test_size, max_classes=10) 或 (B, test_size, num_quantiles)
- **参数量**: 27.6M（embed_dim=128, col 3 blocks, row 3 blocks, icl 12 blocks）
- **Pre-train 范围**: 训练数据 300–100,000 samples × 2–100 features，号称可外推到 ~500k samples（论文 §6.2 实验）
- **TabArena 上 SOTA**: 当前 (2026) 公开 tabular FM 里 zero-shot 性能第一，超 RealTabPFN-2.5

### Install

```bash
pip install tabicl                  # 我们装的是 tabicl 2.1.1
# 首次调用自动下 jingang/TabICL/<ckpt-name>.ckpt 到 ~/.cache/huggingface/
# 离线场景把 ckpt 拷到 ~/.cache/huggingface/hub/models--jingang--TabICL/snapshots/.../
```

### API（sklearn-style）

```python
from tabicl import TabICLClassifier, TabICLRegressor

clf = TabICLClassifier(
    device="cuda",
    n_estimators=8,          # 默认 8；可降到 2 跟 TabPFN 项目历史保持一致
    random_state=0,
    allow_auto_download=True,
)
clf.fit(X_train_arr, y_train_arr)       # X 必须是 numeric ndarray
proba = clf.predict_proba(X_test_arr)   # (n_test, n_classes)
classes = clf.classes_                  # sorted unique y_train

reg = TabICLRegressor(device="cuda", n_estimators=8, random_state=0)
reg.fit(X_train_arr, y_train_arr.astype(np.float32))
pred = reg.predict(X_test_arr)          # (n_test,)
```

---

## 3. 接入项目（drop-in vs TabPFN）

代码层面 99% 兼容。唯一差异：**非数值列处理**。

TabPFN 接受 pandas DataFrame 含 string/object/category dtype（内部自己做 LabelEncoder）。TabICL 需要 **numeric ndarray**，所以非数值列要先 ordinal encoding。

具体到 TrialBench 数据：[`branch/IE_embedding/script/ablate_ie_features.py`](../IE_embedding/script/ablate_ie_features.py) 用 `preprocess(X)`（drop TEXT_DROP + drop NaN > 50% 列 + `object → category`）后直接喂 TabPFN。换 TabICL 时加一步：

```python
# 复用现成的 to_numeric_array (script/fm_bench_ie.py 第 48 行)
def to_numeric_array(X_train: pd.DataFrame, X_test: pd.DataFrame):
    """Categorical / string / object 列 → train+test union ordinal codes
    (NaN 保留为 NaN)；numeric 列 → float32"""
    ...

X_train_arr, X_test_arr = to_numeric_array(X_train_p, X_test_p)
clf = TabICLClassifier(device="cuda")
clf.fit(X_train_arr, y_train.astype(int).values)
proba = clf.predict_proba(X_test_arr)
```

完整替换 example: [`script/fm_bench_ie.py:run_tabicl`](script/fm_bench_ie.py)。

---

## 4. 已知坑

### 4.1 TrialBench 是 PyArrow string，不是 legacy object

`/data2/zhu11/TB/script/sae_finetune.py:preprocess` 的 `if X[c].dtype == object` 判断**捕获不到** PyArrow-backed string dtype，所以原 `preprocess()` 出来的 DataFrame 还带着 string 列（TabPFN 不在乎；TabICL 在乎）。

修：用 `pd.api.types.is_numeric_dtype(X[c])` 反向判断（[`script/fm_bench_ie.py:to_numeric_array`](script/fm_bench_ie.py)）。

### 4.2 train+test union encoding（避免 test-only category 撞 -1=missing）

```python
combined = pd.concat([X_train[c].astype("object"), X_test[c].astype("object")])
codes = combined.astype("category").cat.codes   # train+test 一起 fit
codes[codes == -1] = np.nan                     # 原本 -1 是 missing 标记，换 NaN
```

### 4.3 Full Step 2 注入时 dtype

TabICL 内部走 fp16（AMP），projection 输出是 fp32。Concat 之前要 cast 回 `col_out.dtype`：

```python
v_in = virt_T2_768.to(col_out.device).to(self.proj_incl.weight.dtype)  # 提到 fp32 做投影
incl_te = self.proj_incl(v_in[:, 0, :]) + self.virt_col_emb[0]
virt_t2e = torch.stack([incl_te, excl_te], dim=1).to(col_out.dtype)    # cast 回 fp16
```

完整代码见 [`script/full_step2_tabicl.py`](script/full_step2_tabicl.py)。

---

## 5. 实验结果（TabICLv2 切片）

### 5.1 Zero-shot 横向（6 子任务 × 4-phase 合并）

对照 TabPFN-v2.5 同 setup（n_estimators=2 for TabPFN，n_estimators=8 for TabICL 默认）。来源: [`results/fm_bench_*_20260523_*/metrics.json`](results/)。

| Subtask | task | metric | TabPFN-v2.5 | **TabICLv2** | Δ |
|---|---|---|---|---|---|
| serious-adverse-event-forecasting | binary | ROC-AUC | 0.8851 | **0.8854** | +0.0003 |
| mortality-event-prediction | binary | ROC-AUC | 0.8576 | **0.8603** | +0.0027 |
| patient-dropout-event-forecasting | binary | ROC-AUC | 0.8126 | **0.8128** | +0.0002 |
| trial-approval-forecasting | binary | ROC-AUC | 0.8305 | **0.8327** | +0.0022 |
| trial-failure-reason-identification | multiclass(4) | macro-F1 | 0.2750 | **0.2802** | +0.0052 |
| trial-duration-forecasting | regression | R² | 0.2681 | **0.2866** | **+0.0185** |

**6/6 持平或微优**；trial-duration regression 上明显胜出。

推理时间（4-phase 合并，H200）：

| Subtask | TabPFN (n_est=2) | **TabICL (n_est=8)** |
|---|---|---|
| SAE | 2.9s | **2.7s** |
| mortality | 2.9s | **2.7s** |
| patient-dropout | 4.9s | **3.9s** |
| trial-approval | 4.0s | **3.4s** |
| failure-reason | 2.7s | **2.6s** |
| trial-duration | 5.7s | **4.1s** |

TabICL **n_est=8 比 TabPFN n_est=2 还快**（column-then-row attention 比 TabPFN 的 per-feature 在这个量级更高效）。

### 5.2 IE 8-col stacking A/B（per-phase × 4 FM × 12 cells，TabICL 切片）

baseline = TabICL zero-shot；+IE = baseline 再拼 8 列 stacking 特征（incl/excl × mean/max/std/n，来源 IE_embedding criterion_head OOF）。来源: [`results/fm_bench_ie_*/metrics.json`](results/)。

| Subtask | Phase | TabICL baseline | TabICL +IE | Δ |
|---|---|---|---|---|
| SAE | Phase 2 | 0.8241 | **0.8628** | **+0.0387** |
| SAE | Phase 3 | 0.8968 | **0.9100** | **+0.0133** |
| mortality | Phase 2 | 0.8338 | **0.8768** | **+0.0430** |
| mortality | Phase 3 | 0.8256 | **0.8478** | **+0.0222** |
| patient-dropout | Phase 2 | 0.7699 | **0.7824** | +0.0125 |
| patient-dropout | Phase 3 | 0.8592 | **0.8627** | +0.0035 |
| trial-approval | Phase 2 | 0.8165 | **0.8335** | **+0.0169** |
| trial-approval | Phase 3 | 0.8121 | **0.8261** | **+0.0140** |
| failure-reason (mF1) | Phase 2 | 0.2297 | **0.2936** | **+0.0639** |
| failure-reason (mF1) | Phase 3 | 0.2707 | **0.3021** | **+0.0314** |
| trial-duration (R²) | Phase 2 | 0.1761 | **0.2412** | **+0.0651** |
| trial-duration (R²) | Phase 3 | 0.1014 | **0.1847** | **+0.0833** |

**12/12 全部正向**。TabICL 在 12 个 (subtask, phase) 单元里有 8 个拿了 +IE 后头名（4 FM 横向对比），1 个被 TabDPT 反超 (failure-reason Phase2)。

### 5.3 Full Step 2（2 virtual feature tokens, IE_embedding 最终方案）

baseline = TabICL zero-shot；+IE = sklearn preprocess + 2 个 virtual feature token 注入 `col_embedder` 输出 (B, T, H, 128)，仅训 `Linear(768→128) × 2 + col_emb × 2`（197K 参 / 27.6M），30 epoch，lr=1e-3, ctx=2000, qry=500。脚本: [`script/full_step2_tabicl.py`](script/full_step2_tabicl.py)。来源: [`results/full_step2_tabicl_*/metrics.json`](results/)。

| Subtask | Phase | TabICL baseline | TabICL +IE Full Step 2 | Δ |
|---|---|---|---|---|
| SAE | Phase 2 | 0.8241 | **0.8658** | **+0.0418** |
| SAE | Phase 3 | 0.8968 | **0.9078** | +0.0110 |
| mortality | Phase 2 | 0.8338 | **0.8878** | **+0.0541** |
| mortality | Phase 3 | 0.8256 | **0.8744** | **+0.0488** |
| patient-dropout | Phase 2 | 0.7699 | 0.7495 | **−0.0204** |
| patient-dropout | Phase 3 | 0.8592 | 0.8490 | **−0.0102** |
| trial-approval | Phase 2 | 0.8165 | 0.7898 | **−0.0267** |
| trial-approval | Phase 3 | 0.8121 | **0.8349** | **+0.0228** |
| failure-reason (mF1) | Phase 2 | 0.2297 | **0.3323** | **+0.1026** |
| failure-reason (mF1) | Phase 3 | 0.2707 | **0.3779** | **+0.1072** |
| trial-duration (R²) | Phase 2 | 0.1761 | **0.2576** | **+0.0816** |
| trial-duration (R²) | Phase 3 | 0.1014 | **0.2563** | **+0.1549** |

**9/12 显著正向**，3/12 显著负向（patient-dropout 两 phase + trial-approval Phase 2）。Full Step 2 的最大涨幅（+0.155 R²）远大于 +IE 8-col 的最大涨幅（+0.083 R²），但代价是 patient-dropout 和 approval 上的负效应（30 epoch + 仅 197K 参在 27M 模型上可能欠拟合）。

**Caveat**: baseline 用 TabICL native preprocess，+IE Full Step 2 用 sklearn ColumnTransformer。Δ 里混了 (a) preprocessor 切换 + (b) 2 个虚拟列。要严格分离需要再跑一个 "sklearn preprocess + 0 个虚拟列" 控制组（详见 [`README.md` §5 第四轮 caveat 6](README.md)）。

---

## 6. 复现命令

```bash
source /data2/zhu11/miniconda3/etc/profile.d/conda.sh && conda activate tabpfn

# 0. 安装（torch 2.9.1 / pandas 2.3.3 是 autogluon[mitra] 兼容后的版本，TabICL 无碍）
pip install tabicl                    # 2.1.1

# 1. Smoke test
python /data2/zhu11/TB/branch/new_FM/script/smoke_tabicl.py

# 2. Zero-shot 6 子任务对比（TabPFN vs TabICL vs TabDPT）—— 复现 §5.1
python /data2/zhu11/TB/branch/new_FM/script/fm_bench.py \
  --subtask serious-adverse-event-forecasting --target Y/N --task-type binary
# 其余 5 个子任务参数见 README §6

# 3. IE 8-col A/B per phase × 4 FM —— 复现 §5.2
python /data2/zhu11/TB/branch/new_FM/script/fm_bench_ie.py \
  --subtask serious-adverse-event-forecasting --target Y/N --task-type binary --phase Phase2

# 4. Full Step 2 (2 virtual tokens) —— 复现 §5.3
python /data2/zhu11/TB/branch/new_FM/script/full_step2_tabicl.py \
  --subtask serious-adverse-event-forecasting --target Y/N --task-type binary --phase Phase2 --epochs 30
```

---

## 7. 下一步建议

1. **把 TabICL 接进 `branch/IE_embedding` 流水线** 替代 TabPFN：复用 [`ablate_ie_features.py`](../IE_embedding/script/ablate_ie_features.py)，把 `from tabpfn import TabPFNClassifier` 换成 `from tabicl import TabICLClassifier` + 在 fit 前补 `to_numeric_array()`，看 +IE 涨点（8 列 SAE +0.018 / 72 列 +0.0313）是否完整保留。
2. **TabICL fine-tune extras**: `pip install tabicl[finetune]`，对照 IE_embedding 里 TabPFN FT 的 no-op 结论。
3. **Full Step 2 调更多 epoch / 大 ctx_size** 看 patient-dropout 和 trial-approval Phase 2 的负 Δ 是否能拉回来（30 epoch 可能不够）。
4. 如果上游 TabICL release 加大模型，记得同步换 ckpt（`checkpoint_version` 参数）。
5. License：上游进商业管线时记得保留 `tabicl` 包附带的 LICENSE 文件；BSD-3 不要求强制归属（区别于 TabPFN 的 Llama-style 归属条款）。

---

## 8. 关键产物索引

| 文件 | 用途 |
|---|---|
| [`script/fm_bench.py`](script/fm_bench.py) | 3 FM zero-shot 横向对比（TabPFN / TabICL / TabDPT），6 子任务 4-phase 合并 |
| [`script/fm_bench_ie.py`](script/fm_bench_ie.py) | 4 FM × IE 8-col A/B，单 phase；含 `to_numeric_array()` 工具函数 |
| [`script/full_step2_tabicl.py`](script/full_step2_tabicl.py) | TabICL 上的 Full Step 2 (2 virtual feature tokens) wrapper + 训练 loop |
| [`script/aggregate_full_step2.py`](script/aggregate_full_step2.py) | 把 3 FM × 12 cell 拉成一张 markdown 表 |
| `results/fm_bench_*_20260523_172*/`            | §5.1 zero-shot 结果（6 子任务） |
| `results/fm_bench_ie_*_Phase{2,3}_20260524_00*/` | §5.2 IE 8-col A/B（12 cells × 4 FM） |
| `results/full_step2_tabicl_*_Phase{2,3}_20260524_*/` | §5.3 Full Step 2（12 cells） |
