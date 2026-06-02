# Doc/DAG/

> **进入本目录前请先看 [`/data2/zhu11/TB/Doc/README.md`](../README.md) 和 [`/data2/zhu11/TB/ReadMeFirst.md`](../../ReadMeFirst.md)。**

本子目录放置**DAG（因果图）相关的人工长文档**：节点定义、边审计、迭代报告、技术专题。

---

## 现有文档

| 文件 | 内容 |
|---|---|
| `DAG_node.md` | DAG 节点定义 |
| `DAG_report.md` | DAG 综合报告 |
| `uncertainty_edge.md` | 245-edge DAG（post-R9）上 20 个最不确定 edge 的审计 |

---

## 写作要点

- DAG 迭代轮次（R1, R2, …, R9, …）用一致的命名，文档里写清当前讨论的是哪一轮
- edge 用 ``source → target`` 引用，效应值用 `(eff=0.XXX)` 标注
- 删 / 改 / 保留 edge 的决策要写清楚理由——后面回看才追得清楚
