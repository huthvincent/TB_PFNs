# /data2/zhu11/TB/branch — 探索性子项目入口

> 进入任何 branch 之前请先看 [`../ReadMeFirst.md`](../ReadMeFirst.md)。

`branch/` 用来放**探索性子项目**：每个 branch 对应一条研究/实验线，每条线自成一个目录，自带 README、自带数据/脚本/结果。**主项目根目录 `/data2/zhu11/TB/` 只放共享的、稳定的东西**（dataset、上游 TabPFN、跨实验脚本）；任何"想试一下"的方向都开一个新 branch，不要把临时文件散落到根目录。

---

## 1. 现有 branches

| Branch | 主题 | 状态 | 入口文档 |
|---|---|---|---|
| [`IE_embedding/`](IE_embedding/) | `eligibility/criteria/textblock` 拆 inclusion/exclusion → MedCPT embedding → 注入 TabPFN（Step 1 stacking 8 列 / Step 2-Lite PCA 72 列 / Full Step 2 2 virtual tokens 三种方案） | 已落地，最优组合 Step 2-Lite (72 cols) 在 SAE 4-phase 上 0.9164 | `README.md`；（待补 `final_readme.md`） |
| [`All_text_embedding/`](All_text_embedding/) | 把 TrialBench 所有文本列各做一个 virtual token 注入 TabPFN | 进行中（3 步实验计划，详见其 README §2） | `README.md` |
| [`new_FM/`](new_FM/) | TabPFN 的 commercial-friendly 替代调研（5 个候选 FM × 6 子任务 × Phase2/3 × baseline+IE） | 已落地 → **TabICLv2 (BSD-3)** | [`new_FM/final_readme.md`](new_FM/final_readme.md) |
| [`mesh/`](mesh/) | 在 new_FM 的 TabICLv2+I+E 基础上加 condition/intervention MeSH 作 2 个 virtual token，SAE Phase2/3 | 已收尾 → **MedCPT MeSH Phase2 小幅显著正 (p<0.05)**，唯一稳健正信号 | [`mesh/final_readme.md`](mesh/final_readme.md) |
| [`smiles/`](smiles/) | 在 new_FM 的 TabICLv2+I+E 基础上加 SMILES 分子结构 virtual token，SAE Phase2/3 | 已收尾 → **SMILES 无稳健增益**（多-seed 验证） | [`smiles/final_readme.md`](smiles/final_readme.md) |
| [`aggregate/`](aggregate/) | 把 I+E+SMILES+9 个文本列(Qwen3) 全作 virtual token（共 12 个）塞进 TabICLv2，SAE Phase2/3 | 已收尾 → **全堆 12 token 不如只用 I+E**（n=10 多-seed；I+E 是甜点位） | [`aggregate/final_readme.md`](aggregate/final_readme.md) |

---

## 2. 每个 branch 的目录约定

```
<branch_name>/
├── initial_readme.md  ← (可选) 开工前的起点文档：开 branch 但还没开始做的时候放，
│                        给接手的 AI agent / 协作者 cold-read 用（详见 §3.1）。
│                        开工后第一件事就是改成 README.md。
├── README.md          ← 进度日志：每轮实验都加段，含实验细节、数字、踩过的坑（详见 §3.2）
├── final_readme.md    ← 终态文档：方案定下来后必须写（详见 §3.3）
├── script/            ← 该 branch 的脚本（不要塞进 ../script/）
├── data/              ← 中间产物：cache、解析结果、git clone 进来的小仓库
└── results/<run_id>/  ← 每次脚本运行的输出（metrics.json / log.txt / *.png）
```

- `run_id` 用 `<script_name>_<YYYYMMDD_HHMMSS>` 格式（跟主项目 [`../ReadMeFirst.md` §2.2](../ReadMeFirst.md) 一致）
- 数据来源依然是 `../dataset/TrialBench/`（只读，不动）
- fine-tune 出来的模型权重落 `../model_checkpoint/<run_id>/`（共用主项目 ckpt 池）
- 不要在 branch 里塞自写 TabPFN 改动；上游 `../TabPFN/` 是 editable install，保持只读
- 跨 branch 的综述 / 方法论 / 决策记录写到 `../Doc/`，**单 branch 内**的进度走自己的 `README.md`

---

## 3. 三类文档的分工

一个 branch 的整个生命周期可能产生三类 README，对应三个阶段：

```
开 branch + 待开工          开工中（迭代）             方案定下来收尾
─────────────────  →  ────────────────────  →  ─────────────────
initial_readme.md       README.md (进度日志)       final_readme.md
(给接手 agent 看起点)   (实验过程、踩坑、试错)     (终态文档，给后人 cold-read)
```

- **不**是每个 branch 都要有 initial_readme.md（只有"我想开这条线，但还没开始做"的情况才用）
- **不**是每个 branch 都要立刻有 final_readme.md（进行中的 branch 不需要）
- **必须**有 README.md（开工那一刻就要写第一段；如果之前有 initial_readme.md，改名为 README.md 然后开始往里面加进度）

### 3.1 initial_readme.md — 开工前的起点文档（可选）

用在这种情况：**你（或上一个 agent）准备开一条新 branch，给定了方向和约束，但实际工作要交给下一个 agent 做**。这种时候写一份 initial_readme.md，让接手的人 cold-read 之后就能开工，不用回去逐个读旧 branch 的代码。

必须包含：

1. **TL;DR**：这个 branch 一句话讲清要做什么
2. **项目上下文（30 秒速通）**：相关 branch 的简表 + 各自结论
3. **基础模型 / 当前 state**：本 branch 要建在什么基础上（指向具体的旧脚本或终态文档）
4. **本 branch 要做的新增**：架构 / 数据 / 训练协议的具体改动
5. **实验设计**：要跑哪些 cell，已有数字 vs 还要补哪些
6. **实现路径建议**：建议先写哪些脚本、fork 哪些现成脚本
7. **重要踩坑预警**：能省后人时间的（dtype 不匹配、env 兼容、HF 网络等）
8. **跟用户/团队对齐前的开放问题**：encoder 选哪个、token 几个、缺失值怎么处理
9. **重要参考文档**：按优先级列旧文档 / 旧脚本，注明"何时看、看什么"
10. **day-1 节奏**：一份 5-7 步的推荐起步路径

写 initial_readme.md 的最高目标：**让接手的 AI agent 不需要回去看旧代码就能开始工作，除非有"现在就必须看"的地方（用 §9 列出）**。

参考样板：[`mesh/initial_readme.md`](mesh/initial_readme.md) / [`smiles/initial_readme.md`](smiles/initial_readme.md)。

### 3.2 README.md — 进度日志（必须）

开工那一刻就要存在（要么从 initial_readme.md 改名，要么从零写）。

每轮实验跑完都加一段，记录：
- 这轮做了什么、为什么
- 用的命令、跑出来的数字（链到 results/<run_id>/metrics.json）
- 踩了什么坑、放弃了什么方案
- 下一轮打算做什么

可以很长（几百行）；不要求每段都精致，只要时间顺序清楚、读完能复盘整个心路历程。参考样板：[`new_FM/README.md`](new_FM/README.md)、[`IE_embedding/README.md`](IE_embedding/README.md)。

### 3.3 final_readme.md — 终态文档（方案定下来后必须）

**每个 branch 方案定下来之后必须新增一个 `final_readme.md`**（跟 `README.md` 并列在 branch 根目录）。

#### 为什么要终态文档

- `README.md` 是**过程**：每轮实验、试错、踩坑、未走通的方案都在里面，可能几百行；适合参与过的人回查
- `final_readme.md` 是**终态**：只写最后定下来的方案，目标是让后续 AI agent / 协作者 cold-read 5 分钟内拿到所有关键信息；适合接手的人

#### final_readme.md 必须包含

1. **TL;DR**：一两句话说清"这个 branch 最终选了什么，为什么"
2. **候选对比**：列出 pk 掉了哪些备选 + 砍掉的原因（license / 性能 / 兼容性）
3. **接入方式**：代码层面怎么用（pip install / API 兼容性 / drop-in 替换路径），有现成 example 代码片段
4. **已知坑**：容易踩、能省后人时间的（dtype 不匹配、env 兼容性、HF login 等）
5. **关键实验数据**：最有说服力的几张表，**链接到 `results/<run_id>/metrics.json`**；不要 paste 完整 50 行进度日志（那是 README.md 的活）
6. **复现命令**：一段可直接复制粘贴的 bash
7. **下一步建议**（可选）：后续可以接哪条线、能再榨的边际收益、license / 上游升级注意事项
8. **关键产物索引**：表格列出主要脚本 + 主要 results 子目录，方便定位

参考样板：[`new_FM/final_readme.md`](new_FM/final_readme.md)。

#### 写 final_readme.md 的时候

- **只引用已有数据**：所有数字必须能从 `results/<run_id>/metrics.json` 里查到，不为了写 final_readme.md 重新跑实验
- **可以反过来引用 README.md**：终态文档里说"详见 README §x 第 y 轮"是可以的，反过来不行
- **同步更新 `/data2/zhu11/TB/ReadMeFirst.md` §7 现状速览**：加一行指向新 branch 的 `final_readme.md`

---

## 4. 什么算"方案定下来了"

下面任一条满足就要写 final_readme.md：

- 拍板了用哪个 model / encoder / 流水线，下面准备进入下一阶段（例如 new_FM 已经拍 TabICLv2）
- 实验跑完，最终数字定型，写论文/汇报要从这个 branch 引数字
- 用户/team 显式说"这条线就到这了，做收尾"

如果一条 branch 还在反复试方向（如 All_text_embedding 还在 Step 1/2/3 之间走），暂时不需要写 final_readme.md；等到 3 步走完再写。

---

## 5. 关于这个目录本身

- `branch/README.md`（本文件）= branch 目录的总索引和规则
- 新开 branch 时记得来 §1 表格加一行
- 改动这个文件的规则就等于改项目契约，同步更新 `/data2/zhu11/TB/ReadMeFirst.md` 提到 branch 的相关章节
