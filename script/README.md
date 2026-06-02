# script/

> **进入本目录前请先看 [`/data2/zhu11/TB/ReadMeFirst.md`](../ReadMeFirst.md)。**

本目录放置**所有自写脚本**：数据处理、训练、fine-tune、评估、绘图等。

---

## 命名规范

- `<task>_<action>.py`，全小写下划线
- 一次性的探索脚本加 `scratch_` 前缀，跑完应及时删除
- 不允许 `tmp.py / test.py / new.py / a.py` 这类无语义命名

## 编写规范

每个脚本顶部应有：

1. 单行 docstring 说明用途
2. 路径常量（`DATA_ROOT`, `CKPT`, `RESULTS_ROOT`, `CKPT_ROOT`）放在 import 之后、main 之前
3. 用 `datetime.now().strftime('%Y%m%d_%H%M%S')` 生成 `run_id`
4. 在 `RESULTS_ROOT / run_id` 写 metrics（JSON），在 `CKPT_ROOT / run_id` 写模型权重

可直接参考 `sae_finetune.py` 的样板。

## 现有脚本

| 文件 | 用途 |
|---|---|
| `verify_gpu_finetune.py` | GPU + TabPFN fine-tune 自检（breast_cancer 数据，几秒钟） |
| `sae_finetune.py` | TrialBench SAE Forecasting baseline + fine-tune，自动落盘 metrics 与 ckpt |

## 运行环境

```bash
conda activate tabpfn
# 或：
/data2/zhu11/miniconda3/envs/tabpfn/bin/python <script>.py
```

`TABPFN_NO_BROWSER=1` 用于无头环境跳过浏览器登录。
