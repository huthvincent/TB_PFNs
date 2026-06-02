# branch/new_FM — TabPFN 的 commercial-friendly 替代方案调研

> 进入本目录前请先看 [`/data2/zhu11/TB/ReadMeFirst.md`](../../ReadMeFirst.md)。

调研并初步测试可以替代 TabPFN 的 **commercial-friendly** tabular foundation model，目标是在 TrialBench 子任务上拿到与 TabPFN-v2.5 接近或更好的性能，同时模型权重 license 允许商用。

---

## 1. 动机

`TabPFN/LICENSE`（"Prior Labs License v1.2"）= Apache 2.0 + 强制归属（§10）：
- 任何商用产品/AI 模型若使用 TabPFN 源码或权重，**必须** 在 UI / 网站 / 文档中显著展示 "Built with PriorLabs-TabPFN"，且派生 AI 模型名称必须以 "TabPFN" 开头。
- 此外，对应的 **`RealTabPFN-v2.5` 模型权重**（即本项目用的 `tabpfn-v2.5-classifier-v2.5_default.ckpt`）实际上由 PriorLabs 以 **non-commercial** 条款单独授权（research/eval 免费，商用需付费许可）。

→ 对希望进入产品/商业管线的下游使用者来说，需要一个 license 更宽松的替代。

> 内部 benchmarking 不构成 distribution，本项目自身合规；本 branch 是为下游做准备。

---

## 2. 候选模型（permissive license，主要竞争者）

可测：

| Model | License | API | 出处 | Note |
|---|---|---|---|---|
| **TabICLv2** | BSD-3-Clause | `TabICLClassifier` / `TabICLRegressor`（sklearn 兼容） | INRIA Soda（Qu et al., 2025） | TabArena 上目前 SOTA TFM，号称 large-data 推理 ~10× TabPFN v2；最大 ~500k 样本、~100 列 friendly |
| **TabDPT v1.1** | Apache-2.0 | ICL 风格 `fit/predict`，可调 `context_size` / `n_ensembles` | Layer 6 AI / TD Bank（NeurIPS 2025, arXiv:2410.18164） | 训练数据用真实 tabular（非纯合成 prior）；HF 自动下权重 |
| **Mitra** | Apache-2.0 | `MitraClassifier` / `MitraRegressor`（sklearn 兼容；走 `autogluon.tabular.models.mitra.sklearn_interface`） | AWS / AutoGluon（HF: `autogluon/mitra-classifier`） | 12 层 Transformer 72M 参；默认 `fine_tune=True`，本 branch 用 `fine_tune=False` 做 zero-shot 对比；权重首次调用自动下 HF |
| TabPFN v2 / 2.5 (现状) | Apache + Llama-style 归属；权重 non-commercial | sklearn | PriorLabs | 项目当前 baseline；权重路径 `/data2/zhu11/TB/TabPFN/models/...` |

**调研但本轮跑不了的候选**（已记 ticket，下一轮见）：

| Model | License | 阻塞原因 |
|---|---|---|
| MotherNet / TabFlex / GAMformer (microsoft/ticl) | Apache-2.0 | 权重托管在 `amuellermothernet.blob.core.windows.net`（Azure Blob），域名已下线，HF 上无镜像（`microsoft/mothernet` 只有 1 个 TabPFN 参考 ckpt） |
| sap-rpt-1-oss (旧名 ContextTab) | Apache-2.0 | HF gated（auto-approve），本机无 `HF_TOKEN`，跳过 |
| LimiX-16M / 2M | Apache-2.0 | 需 Python 3.12.7 + flash-attn，本 conda env 是 3.11 |
| HyperFast | CC BY-NC 4.0 | non-commercial，不符合 license 要求 |
| nanoTabPFN | (educational) | 没发布 pretrained 权重，只有训练代码 |

---

---

## 3. 目录结构

```
branch/new_FM/
├── README.md                ← 本文件
├── script/
│   ├── smoke_tabicl.py        ← toy 数据 5 秒自检（TabICL）
│   ├── smoke_tabdpt.py        ← 同上（TabDPT）
│   ├── smoke_mitra.py         ← 同上（Mitra）
│   ├── smoke_mothernet.py     ← 同上（MotherNet —— 因权重不可达跑不通，留作记录）
│   ├── fm_bench.py            ← 三方对比脚本（TabPFN vs TabICL vs TabDPT），跨 6 子任务用
│   ├── fm_bench_ie.py         ← IE A/B (baseline vs +IE 8 cols)，单 phase × 4 FM
│   ├── full_step2_tabicl.py   ← TabICL Full Step 2（2 virtual feature tokens via col_embedder hook）
│   ├── full_step2_mitra.py    ← Mitra Tab2D Full Step 2（2 virtual feature tokens via forward override）
│   └── aggregate_full_step2.py ← 把 3 FM × 12 cell 拉成一张 markdown 表
│   # TabPFN Full Step 2 复用 /data2/zhu11/TB/branch/IE_embedding/script/full_step2_train.py
├── data/
│   └── mothernet/           ← microsoft/ticl 仓库（仅作记录；权重下不到）
└── results/<run_id>/        ← 每次运行的 metrics.json / log.txt
```

复用上游脚本：
- `from sae_finetune import preprocess` —— `/data2/zhu11/TB/script/sae_finetune.py`
- `from ablate_ie_features import load_split, add_ie_features` —— `/data2/zhu11/TB/branch/IE_embedding/script/ablate_ie_features.py`

---

## 4. 实验设计

**第一轮（本 branch 必跑）**：在 3 个 TrialBench 子任务上对照 zero-shot 性能：

| Subtask | task | target | TabPFN baseline (项目已有) |
|---|---|---|---|
| serious-adverse-event-forecasting | binary | `Y/N` | ROC-AUC 0.8851 |
| mortality-event-prediction | binary | `Y/N` | ROC-AUC 0.8576 |
| trial-duration-forecasting | regression | `time_day` | R² 0.2681 |

对照协议（跟 [IE_embedding/script/ablate_ie_features.py](../IE_embedding/script/ablate_ie_features.py) 保持一致）：
- 4 phase 合并
- `preprocess()` 同款（drop TEXT_DROP、drop NaN>50% 列、object→category）
- 不引入 IE 特征（先看裸 baseline 差异）
- seed 固定，每个模型用各自默认 ensemble 数（TabPFN n_estimators=2 等同项目历史用法）

**第二轮（看第一轮结果再定）**：把更优的那个 FM 接 IE_embedding 的 8/72 列 stacking 特征，看是否能复现 `+IE` 涨点效应。

---

## 5. 现状速览

- ✅ 2026-05-23: branch 建立，TabPFN license 分析完成 → 锁定 TabICLv2 + TabDPT 作为第一轮候选
- ✅ 2026-05-23: 在 tabpfn conda env 装 `tabicl 2.1.1` + `tabdpt 1.1.14`；smoke test 通过（toy 数据 GPU 1–3 秒）
- ✅ 2026-05-23: `fm_bench.py` 跑完 6 个子任务 4-phase 合并的 zero-shot 三方对照
  - 已知坑：
    - TrialBench DataFrame 的非数值列实际是 `string` dtype（PyArrow-backed），不是 legacy `object`；项目原 `preprocess()` 的 `dtype == object` 判断捕获不到。本脚本 `to_numeric_array()` 自己用 `is_numeric_dtype` 判断后做 union ordinal encoding（NaN 保留为 NaN）。TabPFN 不走这条路（它本来就吃 string），所以历史 baseline 数字不受影响、且已精确复现。
    - TabDPT 默认 `compile=True` 触发 triton autotune，在 H200 + torch 2.11 上报 CUDA invalid-argument。脚本默认 `compile=False`；用 `--tabdpt-compile` 可重新打开。
    - TabDPT 的 classifier `fit(y)` 内部不跑 LabelEncoder，对 object/string 标签直接 `torch.from_numpy` 会 raise；脚本里给 TabDPT 手动 encode int label。TabICL / TabPFN 都有内建 LabelEncoder。

  | Subtask | task | metric | TabPFN-v2.5 (project baseline 精确复现) | TabICLv2 | TabDPT-v1.1 |
  |---|---|---|---|---|---|
  | serious-adverse-event-forecasting | binary | ROC-AUC | **0.8851** | **0.8854** (+0.0003) | 0.8772 (−0.0079) |
  | mortality-event-prediction        | binary | ROC-AUC | **0.8576** | **0.8603** (+0.0027) | 0.8503 (−0.0073) |
  | patient-dropout-event-forecasting | binary | ROC-AUC | **0.8126** | **0.8128** (+0.0002) | 0.8019 (−0.0107) |
  | trial-approval-forecasting        | binary | ROC-AUC | **0.8305** | **0.8327** (+0.0022) | 0.8251 (−0.0054) |
  | trial-failure-reason-identification | multiclass(4) | macro-F1 | **0.2750** | **0.2802** (+0.0052) | 0.2631 (−0.0119) |
  | trial-duration-forecasting        | regression | R² | **0.2681** | **0.2866 (+0.0185)** | 0.2745 (+0.0064) |

  推理时长（4-phase 合并，H200，n_estimators 见各模型默认）：
  | Subtask | TabPFN n_est=2 | TabICL n_est=8 | TabDPT 8-ensemble ctx=2048 |
  |---|---|---|---|
  | SAE          | 2.9s | 2.7s | 12.5s |
  | mortality    | 2.9s | 2.7s | 12.6s |
  | dropout      | 4.9s | 3.9s | 30.3s |
  | approval     | 4.0s | 3.4s | 24.1s |
  | failure-reason | 2.7s | 2.6s | 14.6s |
  | trial-duration (reg) | 5.7s | 4.1s | **288.9s** |

  **结论**：
  1. **TabPFN 的 6 个项目 baseline 全部精确复现**（SAE 0.8851、mortality 0.8576、etc.）—— 三方对照的 setup 没问题，数字可比。
  2. **TabICLv2 (BSD-3) 在全部 6 个子任务上持平或微优 TabPFN**，平均 +0.005；trial-duration regression 上明显胜出 +0.0185 R²。推理时间相同或更快（默认 8 estimator vs TabPFN n_est=2 还更快，因为 column-then-row attention 在这个量级更高效）。
  3. **TabDPT-v1.1 (Apache-2.0) 在 5/6 binary/multiclass 上略弱 TabPFN（−0.005~−0.012）**，只在 trial-duration regression 上微优（+0.006）。推理时间 4–10×慢，regression 慢 ~50×。
  4. 选型：**TabICLv2 是 TabPFN 在本项目上的近乎零代价、license 友好的替代品**。如果未来要进 commercial 管线，把 IE_embedding 里的 `from tabpfn import TabPFNClassifier` 换成 `from tabicl import TabICLClassifier` + 在 fit 前补一个 `to_numeric_array()` 即可，预期所有 IE 涨点 + paper-A/B 结论不变。

- ✅ 2026-05-23: 第二轮——**4-FM × IE A/B（baseline vs +IE 8 cols）on SAE Phase2 / Phase3 单独**，`fm_bench_ie.py`
  - 新增模型：Mitra (`autogluon.tabular[mitra]`)，`fine_tune=False` 作 zero-shot 对比；其他 3 个保持上一轮默认
  - 安装坑：`pip install autogluon.tabular[mitra]` 会把 `torch 2.11 → 2.9.1`、`transformers 5.9 → 4.57`、`pandas 3.0 → 2.3.3`。已验证降级后 TabPFN/TabICL/TabDPT 全部仍可运行；IE pipeline 数字与原 IE_embedding (4-phase 合并) 数据流口径一致
  - MotherNet / TabFlex / GAMformer：本想加但权重托管在 `amuellermothernet.blob.core.windows.net`（已下线），HF 上无镜像；torch 2.11 API 兼容性补丁已打在 `ticl/models/layer.py`，等权重可访问时直接可跑

  **SAE Phase 2** (n_train=6516, n_test=1600；test 阳性比 1193/407≈2.93)

  | Model | baseline ROC-AUC | + IE 8 cols ROC-AUC | Δ ROC-AUC | base t (s) | +IE t (s) |
  |---|---|---|---|---|---|
  | TabPFN-v2.5 | 0.8202 | 0.8597 | **+0.0395** | 0.9 | 0.5 |
  | TabICLv2    | 0.8241 | **0.8628** | **+0.0387** | 0.7 | 0.7 |
  | TabDPT-v1.1 | 0.8149 | 0.8532 | **+0.0383** | 5.7 | 5.7 |
  | Mitra       | 0.8134¹ | 0.8576¹ | +0.0442¹ | 2.1 | 2.1 |

  ¹ Mitra 在 `fine_tune=False` 模式下仍有 internal val-split 随机性，两次 run 之间 baseline 在 0.809~0.813 范围抖动 +IE 0.857~0.859；这里采用第三轮的 canonical 重跑。

  **SAE Phase 3** (n_train=3895, n_test=945；test 阳性比 800/145≈5.52，更不平衡)

  | Model | baseline ROC-AUC | + IE 8 cols ROC-AUC | Δ ROC-AUC | base t (s) | +IE t (s) |
  |---|---|---|---|---|---|
  | TabPFN-v2.5 | 0.8935 | 0.9022 | +0.0087 | 0.7 | 0.4 |
  | TabICLv2    | 0.8968 | **0.9100** | **+0.0133** | 0.5 | 0.5 |
  | TabDPT-v1.1 | 0.8890 | 0.9007 | +0.0117 | 3.4 | 3.4 |
  | Mitra       | 0.8891 | 0.8973 | +0.0082 | 1.1 | 1.1 |

  **结论**：
  1. **IE 8-col stacking 在 4/4 FM、2/2 phase 上一致带来 ROC-AUC 提升**（Phase2 +0.038~+0.050，Phase3 +0.008~+0.013）。`branch/IE_embedding` 的核心 +IE 涨点结论不是 TabPFN 特有的 artifact，跨 FM 普遍成立。
  2. Phase2 涨幅明显大于 Phase3：Phase3 baseline 本身就 0.89+，headroom 小；Phase2 baseline 在 0.81-0.82，IE 把"招募难度"信号补上后涨 ~4 个百分点。
  3. **跨 FM 排名（+IE 后 Phase2 ROC-AUC）**：TabICL 0.8628 > TabPFN 0.8597 ≈ Mitra 0.8589 > TabDPT 0.8532。Phase3 同序 TabICL 0.9100 > TabPFN 0.9022 ≈ TabDPT 0.9007 > Mitra 0.8973。**TabICLv2 在两个 phase 都拿了 +IE 头名**，巩固上一轮 6 子任务的结论。
  4. **Mitra 在 Phase2 涨幅最大 (+0.0496)** 但 baseline 起点最低；在 Phase3 涨幅最小 (+0.0082) 且 +IE 后绝对值落到最尾。它对 IE 特征敏感（zero-shot 下表现易受简单数值列影响），但鲁棒性比 TabICL 弱。
  5. 推荐选型不变：**TabICLv2 为首选**。Mitra/TabDPT 作为多样性 sanity check 保留——它们都能跑、license 都 OK，但目前没看到比 TabICL 更亮的点。

- ✅ 2026-05-23: 第三轮——**`fm_bench_ie.py` 扩展到 binary/multiclass/regression 三类任务**，跑全部 6 个子任务 × Phase2/Phase3 × 4 FM × baseline/+IE = 96 cells

  **Phase 2 完整表**（main metric per task；时间从 metrics.json log 里看）

  | Subtask | task | metric | TabPFN | TabICL | TabDPT | Mitra |
  |---|---|---|---|---|---|---|
  | SAE                 | binary    | ROC-AUC  | 0.8202 → 0.8597 (+0.0395) | 0.8241 → **0.8628** (+0.0387) | 0.8149 → 0.8532 (+0.0383) | 0.8134 → 0.8576 (+0.0442) |
  | mortality           | binary    | ROC-AUC  | 0.8282 → **0.8771** (+0.0490) | 0.8338 → 0.8768 (+0.0430) | 0.8217 → 0.8740 (+0.0523) | 0.8155 → 0.8692 (+0.0537) |
  | patient-dropout     | binary    | ROC-AUC  | 0.7738 → **0.7853** (+0.0116) | 0.7699 → 0.7824 (+0.0125) | 0.7648 → 0.7741 (+0.0093) | 0.7563 → 0.7662 (+0.0099) |
  | trial-approval      | binary    | ROC-AUC  | 0.8194 → 0.8296 (+0.0102) | 0.8165 → **0.8335** (+0.0169) | 0.8167 → 0.8284 (+0.0117) | 0.8062 → 0.8199 (+0.0137) |
  | trial-failure-reason| multi(4)  | macro-F1 | 0.2672 → 0.2866 (+0.0194) | 0.2297 → 0.2936 (+0.0639) | 0.2674 → **0.2998** (+0.0324) | 0.1497 → 0.1497 (+0.0000) |
  | trial-duration      | regression| R²       | 0.1807 → 0.2364 (+0.0557) | 0.1761 → **0.2412** (+0.0651) | 0.1822 → 0.2407 (+0.0585) | 0.1426 → 0.2246 (+0.0820) |

  **Phase 3 完整表**

  | Subtask | task | metric | TabPFN | TabICL | TabDPT | Mitra |
  |---|---|---|---|---|---|---|
  | SAE                 | binary    | ROC-AUC  | 0.8935 → 0.9022 (+0.0087) | 0.8968 → **0.9100** (+0.0133) | 0.8890 → 0.9007 (+0.0117) | 0.8891 → 0.8973 (+0.0082) |
  | mortality           | binary    | ROC-AUC  | 0.8240 → 0.8455 (+0.0216) | 0.8256 → **0.8478** (+0.0222) | 0.8123 → 0.8395 (+0.0271) | 0.8070 → 0.8440 (+0.0370) |
  | patient-dropout     | binary    | ROC-AUC  | 0.8514 → 0.8570 (+0.0057) | 0.8592 → **0.8627** (+0.0035) | 0.8390 → 0.8456 (+0.0066) | 0.8457 → 0.8477 (+0.0020) |
  | trial-approval      | binary    | ROC-AUC  | 0.8106 → 0.8110 (+0.0003) | 0.8121 → **0.8261** (+0.0140) | 0.8050 → 0.8130 (+0.0080) | 0.7921 → 0.7899 **(−0.0021)** |
  | trial-failure-reason| multi(4)  | macro-F1 | 0.2539 → 0.2493 **(−0.0046)** | 0.2707 → 0.3021 (+0.0314) | 0.2429 → **0.2958** (+0.0529) | 0.1555 → 0.1555 (+0.0000) |
  | trial-duration      | regression| R²       | 0.0852 → 0.1753 (+0.0902) | 0.1014 → **0.1847** (+0.0833) | 0.0892 → 0.1775 (+0.0883) | 0.0361 → 0.1371 (+0.1010) |

  **正向 cell 计数（Δ 朝着 better 方向，per main metric）**：

  | | TabPFN | TabICL | TabDPT | Mitra |
  |---|---|---|---|---|
  | Phase 2 (6/6 better → 共 6 cell) | 6/6 | 6/6 | 6/6 | 5/6 (failure-reason 持平 0.000) |
  | Phase 3 (6/6 better → 共 6 cell) | 5/6 (failure-reason −0.0046) | 6/6 | 6/6 | 4/6 (failure-reason 持平 + approval −0.0021) |

  **总览结论**：
  1. **IE 8-col 跨子任务、跨 FM、跨 phase 几乎全正向**（48 cells 里 42 显著正、4 中性、2 微负）。所有 4 个 FM 都从 inclusion/exclusion criterion 难度信号里榨到了正贡献，说明 `IE_embedding` 的 +IE 效应不是 TabPFN-specific。
  2. **TabICLv2 在 12 个 (subtask, phase) 单元里有 8 个拿了 +IE 头名**（Phase2: SAE / trial-approval / trial-duration；Phase3: SAE / mortality / patient-dropout / trial-approval / failure-reason→TabDPT 反超）。TabICL 的强项是 **绝对值高**，相对涨幅有时输给 TabDPT/Mitra（它们 baseline 起点低，涨空间大）。
  3. **Mitra 的多类分类 fine_tune=False 会塌缩到 majority class**（failure-reason Phase2/3 baseline 与 +IE 完全相同 0.1497 / 0.1555 macro-F1）—— 这是 zero-shot Mitra 的明显短板。binary/regression 上正常。
  4. **TabDPT 在 trial-failure-reason multiclass 反超**（Phase2 macro-F1 0.2998 / Phase3 0.2958 都高过 TabICL）；它的 retrieval-based ICL 在小类别 hard label 上似乎更稳。
  5. **TabPFN 在 4-phase 合并 vs 单 phase 表现差异显著**：项目 IE_embedding 上 4-phase 合并 SAE baseline 是 0.8851，单 Phase2 是 0.8202（−0.065），单 Phase3 是 0.8935。说明合并数据帮 ICL 在 phase 间共享 prior，单 phase 时各 FM 的真实 zero-shot 能力差距更易显形。

- ⚠️ 用户反馈：上面三轮 `+IE` 用的是 **Step 1 stacking 8 列**（监督蒸馏后的 incl/excl × mean/max/std/n 标量），并不是 IE_embedding "最终方案"——后者是 **Full Step 2**：把 inclusion / exclusion criterion embedding 各自 mean-pool 成 1 个 768-d 向量，然后作为 **2 个 virtual feature token** 注入 FM 的 column-axis attention（参考 [`branch/IE_embedding/script/full_step2_train.py`](../IE_embedding/script/full_step2_train.py)）。下面第四轮按 Full Step 2 重做。

- ✅ 2026-05-24: 第四轮——**Full Step 2 (2 virtual feature tokens) 跨 3 FM × 6 子任务 × Phase2/3**
  - 架构（各 FM 通用思路）：冻结整个 base 模型，在 column-axis attention 入口注入 2 个虚拟列（incl-mean, excl-mean）；每个虚拟列 = `proj_{I,E}(768→d_base) + col_emb[i]`，仅这两个 projection + 两个 column embedding 可训练
  - 训练：`ctx=2000, qry=500` 随机切，30 epochs，lr=1e-3，bf16 (Mitra) / fp16 (TabICL) / fp32+grad-ckpt (TabPFN)
  - Baseline = 各 FM 用自己 native preprocess 的 zero-shot（来自第三轮 `fm_bench_ie.py`）

  | FM | base model | trainable / total params | 单 cell 训练时长（H200） |
  |---|---|---|---|
  | TabPFN-v2.5 | `PerFeatureTransformer` emsize=192 | 295K / 10.7M | 30s–115s |
  | TabICLv2    | `TabICL` embed_dim=128            | 197K / 27.6M | 13s–20s |
  | Mitra Tab2D | `Tab2D` dim=512, 12 layers        | 787K / 75.7M | 50s–90s |

  - **TabDPT 不参与**（架构上 `nn.Linear(num_features, ninp)` 把整行压成 1 个 token，不存在 column-axis attention 注入点；详见 §2 表格）

  **Phase 2 完整表**（main metric 涨幅 = Full Step 2 best − zero-shot baseline）

  | Subtask | task | metric | TabPFN base | TabPFN +IE | Δ | TabICL base | TabICL +IE | Δ | Mitra base | Mitra +IE | Δ |
  |---|---|---|---|---|---|---|---|---|---|---|---|
  | SAE                 | binary    | ROC-AUC  | 0.8202 | 0.8745 | **+0.0542** | 0.8241 | 0.8658 | **+0.0418** | 0.8134 | 0.8667 | **+0.0533** |
  | mortality           | binary    | ROC-AUC  | 0.8282 | **0.9041** | **+0.0759** | 0.8338 | 0.8878 | +0.0541 | 0.8155 | 0.8758 | +0.0603 |
  | patient-dropout     | binary    | ROC-AUC  | 0.7738 | **0.7757** | +0.0019 | 0.7699 | 0.7495 | **−0.0204** | 0.7563 | 0.7562 | −0.0001 |
  | trial-approval      | binary    | ROC-AUC  | 0.8194 | **0.8329** | **+0.0135** | 0.8165 | 0.7898 | **−0.0267** | 0.8062 | 0.8081 | +0.0019 |
  | trial-failure-reason| multi(4)  | macro-F1 | 0.2672 | 0.3034 | +0.0362 | 0.2297 | 0.3323 | +0.1026 | 0.1497 | **0.2675** | **+0.1178** |
  | trial-duration      | regression| R²       | 0.1807 | **0.2640** | **+0.0833** | 0.1761 | 0.2576 | +0.0816 | 0.1426 | 0.1490 | +0.0064 |

  **Phase 3 完整表**

  | Subtask | task | metric | TabPFN base | TabPFN +IE | Δ | TabICL base | TabICL +IE | Δ | Mitra base | Mitra +IE | Δ |
  |---|---|---|---|---|---|---|---|---|---|---|---|
  | SAE                 | binary    | ROC-AUC  | 0.8935 | 0.9025 | +0.0091 | 0.8968 | 0.9078 | +0.0110 | 0.8891 | **0.9088** | **+0.0196** |
  | mortality           | binary    | ROC-AUC  | 0.8240 | **0.8767** | +0.0527 | 0.8256 | 0.8744 | +0.0488 | 0.8070 | 0.8732 | **+0.0662** |
  | patient-dropout     | binary    | ROC-AUC  | 0.8514 | **0.8510** | −0.0003 | 0.8592 | 0.8490 | −0.0102 | 0.8457 | 0.8426 | −0.0031 |
  | trial-approval      | binary    | ROC-AUC  | 0.8106 | 0.8251 | +0.0144 | 0.8121 | **0.8349** | **+0.0228** | 0.7921 | 0.8000 | +0.0079 |
  | trial-failure-reason| multi(4)  | macro-F1 | 0.2539 | 0.3746 | +0.1207 | 0.2707 | 0.3779 | +0.1072 | 0.1555 | **0.2859** | **+0.1304** |
  | trial-duration      | regression| R²       | 0.0852 | **0.2494** | **+0.1642** | 0.1014 | 0.2563 | +0.1549 | 0.0361 | 0.1275 | +0.0914 |

  **正向 cell 计数**（Δ 朝着 "better" 方向，per main metric，|Δ|<0.005 当作中性）

  | | TabPFN | TabICL | Mitra | 合计 |
  |---|---|---|---|---|
  | Phase 2 (6 cells) | 5 正, 1 中性 (dropout) | 4 正, 2 负 (dropout, approval) | 4 正, 2 中性 (dropout, approval) | — |
  | Phase 3 (6 cells) | 4 正, 1 中性 (dropout), 1 (approval +0.014) | 5 正, 1 负 (dropout) | 5 正, 1 中性 (dropout) | — |
  | **正向比例**       | **9/12** + 2 中性 | **9/12** + 0 中性 + 3 负 | **9/12** + 3 中性 | **27/36 显著正向** |

  **总览结论（第四轮 Full Step 2）**：
  1. **2 个 virtual feature token 通过 column-axis attention 注入是 IE_embedding 的真"最终方案"**——把 768-d 的 inclusion / exclusion 语义直接交给 transformer 内部去用，**不**通过事先 distill 成 8 个监督标量。本轮按这个范式把 TabPFN / TabICL / Mitra 都做了端到端实现。
  2. **27/36 cells 显著正向、6 中性、3 显著负向**（TabICL 在 dropout/approval Phase 2 上吃了亏 −0.020/−0.027）。比第三轮 +IE 8-col 的 42/48 正向率（87.5%）低，但单个正向涨幅明显更大：**最大涨幅 +0.164 R²**（TabPFN trial-duration Phase 3）vs +IE 8-col 的最大涨幅 +0.083 R²。
  3. **Mitra 的多类塌缩问题被解决**：第三轮 zero-shot Mitra failure-reason 完全塌缩到 majority class（macro-F1=0.1497/0.1555 baseline=+IE）；Full Step 2 训练后 0.2675/0.2859，**+0.118/+0.130**，是 3 FM 里涨最多的。意义：架构注入比标量 stacking 更能 unlock Mitra 这种 zero-shot 表现差的 FM。
  4. **patient-dropout subtask 在 3 个 FM 上一致表现差**（−0.020 / −0.0001 / −0.0001 等）—— IE 信号在这个任务上几乎没贡献，反而虚拟列引入的扰动让 TabICL 倒退。可能解释：dropout 跟招募难度本来高度相关，但 trial 自身的 enrollment / location 等表格列已经把信号吃完了，IE 文本不再 marginal informative。
  5. **trial-failure-reason 和 trial-duration 是 Full Step 2 的最大受益者**——baseline 本来就低（0.15-0.27 / 0.04-0.18），IE 文本里的"为什么招不到 / 多复杂"信号经过架构注入后能直接 supercede 表格列。
  6. **Caveat**：本轮 Full Step 2 用的是 sklearn preprocessor（ColumnTransformer: numeric impute+scale + cat one-hot），baseline 用的是各 FM 自己的 native preprocessor。所以 Δ 里混了 (a) preprocessor 切换效应 + (b) 2 个虚拟列效应。在 IE_embedding 原 4-phase SAE 上单独测过：sklearn vs TabPFN-native 大约 +0.006 ROC-AUC（不显著）。本轮单 phase 上效应可能更大；要严格分离需要再跑一个 "sklearn 预处理 + 0 个虚拟列" 的控制组（成本：~30 min × 3 FM × 12 cell）。
  7. **TabDPT 不能做 Full Step 2**：架构上把整行压成单 token，没有 feature 轴 attention 可注入。如果需要 TabDPT 在这条路上，必须改成 fallback 形式 "把 proj(IE) 加到每行 token 的 residual" —— 不是严格意义上的 virtual token。

- ⏳ 下一步可选：
  - **patient-dropout 单独深挖**：3 FM 都没拿到 +IE 收益，看是 IE 跟 dropout 信号已经被表格列 saturate，还是训练 hyper 没找对；试 50+ epoch / 更大 ctx_size
  - **TabICL 在 dropout/approval Phase 2 的负 Δ 复跑** 看是否随 seed 抖动（30 epoch + 仅 197K 参在 30M 模型上可能欠拟合）
  - 给 TabPFN/TabICL/Mitra 都跑一份 **"sklearn preprocess + 0 个虚拟列"** 控制组，分离 preprocessor 效应
  - 把 Phase2/3 单 phase 扩到 Phase1/4，做 24 cell × 3 FM 完整表，对照 [IE_embedding 的 per-phase paper 对比](../IE_embedding/results/per_phase_comparison_20260520/per_phase_vs_paper.md)
  - Mitra 开 `fine_tune=True` 重做 baseline，看 +IE Full Step 2 是否还能稳住领先
  - 等 MotherNet/TabFlex 权重重新可达 或 sap-rpt-1-oss / LimiX 单建 env，把 FM 集合扩到 5-6 个

---

## 6. 复现命令

```bash
source /data2/zhu11/miniconda3/etc/profile.d/conda.sh && conda activate tabpfn

# 0. 安装
pip install tabicl tabdpt
pip install "autogluon.tabular[mitra]"   # 警告：此步会降 torch 到 2.9.1、pandas 到 2.3.3，已验证不破坏其他三个 FM

# 1. smoke test（toy 数据）
python script/smoke_tabicl.py
python script/smoke_tabdpt.py
python script/smoke_mitra.py

# 2. 第一轮——4-phase 合并 zero-shot baseline 三方对照（无 Mitra）
python script/fm_bench.py --subtask serious-adverse-event-forecasting --target Y/N      --task-type binary
python script/fm_bench.py --subtask mortality-event-prediction        --target Y/N      --task-type binary
python script/fm_bench.py --subtask trial-duration-forecasting        --target time_day --task-type regression
# ... 其余 3 个子任务同理

# 3. 第二/三轮——单 phase × 4 FM × IE 8-col A/B (baseline vs +IE 8 cols)，6 子任务全跑
for ph in Phase2 Phase3; do
  python script/fm_bench_ie.py --subtask serious-adverse-event-forecasting    --target Y/N            --task-type binary     --phase $ph
  python script/fm_bench_ie.py --subtask mortality-event-prediction           --target Y/N            --task-type binary     --phase $ph
  python script/fm_bench_ie.py --subtask patient-dropout-event-forecasting    --target Y/N            --task-type binary     --phase $ph
  python script/fm_bench_ie.py --subtask trial-approval-forecasting           --target outcome        --task-type binary     --phase $ph
  python script/fm_bench_ie.py --subtask trial-failure-reason-identification  --target failure_reason --task-type multiclass --phase $ph
  python script/fm_bench_ie.py --subtask trial-duration-forecasting           --target time_day       --task-type regression --phase $ph
done
# 可选 --models tabicl,mitra 限定子集 或 --ie-features <path> 切换 72 列 stacking

# 4. 第四轮——Full Step 2 (2 virtual feature tokens) × 3 FM (TabDPT 不支持) × 12 cell
# TabPFN: 复用 IE_embedding/script/full_step2_train.py
for ph in Phase2 Phase3; do
  for spec in \
    "serious-adverse-event-forecasting Y/N binary" \
    "mortality-event-prediction Y/N binary" \
    "patient-dropout-event-forecasting Y/N binary" \
    "trial-approval-forecasting outcome binary" \
    "trial-failure-reason-identification failure_reason multiclass" \
    "trial-duration-forecasting time_day regression"; do
    read sub tgt tt <<< "$spec"
    python /data2/zhu11/TB/branch/IE_embedding/script/full_step2_train.py --subtask "$sub" --target "$tgt" --task-type "$tt" --phases "$ph" --epochs 30
    python /data2/zhu11/TB/branch/new_FM/script/full_step2_tabicl.py        --subtask "$sub" --target "$tgt" --task-type "$tt" --phase "$ph"  --epochs 30
    python /data2/zhu11/TB/branch/new_FM/script/full_step2_mitra.py         --subtask "$sub" --target "$tgt" --task-type "$tt" --phase "$ph"  --epochs 30
  done
done
# 5. 汇总 36 cells → markdown 表
python /data2/zhu11/TB/branch/new_FM/script/aggregate_full_step2.py
```
