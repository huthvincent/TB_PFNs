# results/

> **进入本目录前请先看 [`/data2/zhu11/TB/ReadMeFirst.md`](../ReadMeFirst.md)。**

本目录放置**实验结果**（metrics、log、figure），每次运行一个子目录。

---

## 目录结构

```
results/
└── <run_id>/                       例：sae_finetune_20260510_103801
    ├── metrics.json                必有：metrics + 运行参数
    ├── log.txt                     可选：stdout 重定向
    └── *.png                       可选：loss 曲线、ROC、混淆矩阵等
```

`<run_id>` 与 `model_checkpoint/<run_id>/` 一一对应（同一个时间戳）。

## metrics.json 约定字段

```json
{
  "run_id": "...",
  "device": "NVIDIA H200 NVL",
  "pretrained_ckpt": "/data2/zhu11/TB/TabPFN/models/...",
  "args": { "epochs": 10, "lr": 2e-5, ... },
  "n_train": 14368,
  "n_test": 3548,
  "n_features": 41,
  "baseline":  { "time_s": ..., "roc_auc": ..., "pr_auc": ..., "log_loss": ..., "accuracy": ... },
  "finetuned": { "time_s": ..., "peak_vram_gb": ..., "roc_auc": ..., ... }
}
```

新脚本可在此基础上加字段，但**不要重命名上述字段**，方便横向对比。

## 怎么找历史结果

- 列表：`ls results/`
- 读最近一次：`cat results/$(ls -t results/ | head -1)/metrics.json | jq`
- 多次对比：写个一次性 `scratch_compare.py` 在 `script/` 里聚合，结果落到新的 `results/<run_id>/comparison.csv`

## 不要

- 直接把结果写到本目录根（必须放在 `<run_id>/` 子目录里）
- 修改/删除别人的 run_id 子目录（除非确认是自己跑的且不再需要）
- 把模型权重塞到这里——权重去 `model_checkpoint/`
