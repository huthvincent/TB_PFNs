# Doc/

> **进入本目录前请先看 [`/data2/zhu11/TB/ReadMeFirst.md`](../ReadMeFirst.md)。**

本目录放置**人工撰写的长文档**：设计文档、方法论说明、跨多次实验的综述对比、技术决策记录等。所有内容是手写的、独立于某一次具体 run。

---

## 子目录划分

```
Doc/
├── README.md                ← 本文件
├── results/                 ← 跨实验综述、模型对比、结果导向的分析文档
│   ├── README.md
│   └── ...
└── DAG/                     ← DAG（因果图）相关：node 设计、edge 审计、报告
    ├── README.md
    └── ...
```

进每个子目录前先读那个目录的 `README.md`。新增一类主题文档时，在 `Doc/` 下开一个新子目录（如 `Doc/finetuning/`、`Doc/features/`），并在本文件 §"子目录划分" 加一行。

---

## 与 `results/` 的边界

| | `results/<run_id>/*.md` | `Doc/**/*.md` |
|---|---|---|
| 来源 | 脚本自动生成 | 人工撰写 |
| 绑定 | 强绑定到一次具体 run | 不绑定任何一次 run（可以引用多次） |
| 内容 | 该 run 的 metrics 表、自动摘要 | 设计意图、方法论、跨实验对比、决策记录 |
| 修改 | 一般不手改（重跑会覆盖） | 手改是默认操作 |

**典型情况**：跑了 XGBoost cascade 和 TabPFN cascade 两个独立 run，各自的自动结果在 `results/cascade_xgboost/` 和 `results/cascade_TabPFN/`；想做一份对比并讨论 calibration 等结论 → 写一份 `Doc/results/3-Layer_XGBoost_TabPFN.md`，引用两边的数字。

---

## 命名规范

- 文件名用**有语义的英文短语**（可用 `_` 或 `-`），首字母大写更醒目
- 示例：
  - `Doc/results/3-Layer_XGBoost_TabPFN.md` — 跨实验对比
  - `Doc/DAG/DAG_node.md` / `Doc/DAG/DAG_report.md` — 设计/方法论文档
  - `Doc/DAG/uncertainty_edge.md` — 技术专题
- 不要写 `notes.md`、`tmp.md`、`misc.md`、`draft.md` 这种无语义命名
- 草稿可以加 `wip_` 前缀（work-in-progress），定稿后去掉

---

## 写作规约

每篇文档建议有：

1. 一句话开头说明**这篇文档解决什么问题**
2. 涉及实验结果时，**引用具体的 `results/<run_id>/...`**（让数字可追溯）
3. 引用其他 `Doc/` 文档用 markdown 链接（如 `[DAG report](../DAG/DAG_report.md)`）
4. 决策类文档要写清**做了什么选择、为什么、放弃了什么备选**——以后回看自己也看得懂

---

## 不要

- **不要**把 `Doc/` 里的文档自动覆盖（这些是手写的，覆盖会丢失你写的论述）
- **不要**把脚本生成的 markdown 直接放这里——那些进 `results/<run_id>/`
- **不要**在文件名里写时间戳；文档是长期演进的，不绑定一次时刻
- **不要**留 `tmp.md`、`draft.md` 这种死文件；清理或重命名
- **不要**在 `Doc/` 根直接堆 markdown——挑或新建一个子目录
