# Doc/results/

> **进入本目录前请先看 [`/data2/zhu11/TB/Doc/README.md`](../README.md) 和 [`/data2/zhu11/TB/ReadMeFirst.md`](../../ReadMeFirst.md)。**

本子目录放置**关于实验结果的人工长文档**：跨多次 run 的对比、模型 A vs 模型 B、消融总结、结论分析。

跟 `/data2/zhu11/TB/results/` 的区别：

- `results/<run_id>/*.md` 是**单次 run 的脚本自动产出**
- `Doc/results/*.md` 是**手写的、引用一次或多次 run 的结果**做对比/综述/解读

---

## 现有文档

| 文件 | 内容 |
|---|---|
| `3-Layer_XGBoost_TabPFN.md` | 3-layer cascade 任务上 XGBoost vs fine-tuned TabPFN 的对比（per-layer + joint metric），含 calibration 假设与修法建议 |

---

## 写作要点

- 文档顶部一句话写清楚"这篇文档对比/总结的是哪几次 run"，给出 `results/<run_id>/` 的相对链接
- 表格里的数字要可追溯——指向具体 run，不要凭印象写
- 不要复制粘贴自动 markdown 的整张大表过来；只保留为论述服务的那几列
