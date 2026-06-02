# model_checkpoint/

> **进入本目录前请先看 [`/data2/zhu11/TB/ReadMeFirst.md`](../ReadMeFirst.md)。**

本目录只放 **fine-tune 产出的模型权重**。

**预训练 ckpt（HF 下载的 `tabpfn-v2.5-...ckpt`）不放这里**——那些是上游资源，放在 `/data2/zhu11/TB/TabPFN/models/`。

---

## 目录结构

```
model_checkpoint/
└── <run_id>/                       例：sae_finetune_20260510_103801
    ├── checkpoint_<steps>_best.pth     fine-tune 训练中按 val 最优自动写入
    └── checkpoint_<steps>_last.pth     最后一步的状态（可能存在）
```

`<run_id>` 与 `results/<run_id>/` 一一对应。

## 文件说明

`*.pth` 是 TabPFN finetuning 框架自动写入的 checkpoint，包含：
- `state_dict`：fine-tune 后的模型权重
- `optimizer_state` / `scaler_state`
- 其它训练元信息（epoch、步数）

格式与官方下载的 `*.ckpt` 兼容，可直接通过 `model_path=...pth` 传给 `TabPFNClassifier` 加载推理。

## 怎么生成

写脚本时给 `FinetunedTabPFNClassifier.fit(...)` 传 `output_dir=CKPT_ROOT / run_id`，框架会自动写入 best checkpoint。参考 `script/sae_finetune.py`。

## 加载推理

```python
from tabpfn import TabPFNClassifier
clf = TabPFNClassifier(
    device="cuda",
    model_path="/data2/zhu11/TB/model_checkpoint/<run_id>/checkpoint_<steps>_best.pth",
)
clf.fit(X_train, y_train)        # 仍需 fit（in-context 阶段）
proba = clf.predict_proba(X_test)
```

## 不要

- 直接把权重写到本目录根（必须放在 `<run_id>/` 子目录里）
- 把预训练 ckpt 拷到这里（应去 `TabPFN/models/`）
- 删掉别的 run_id 子目录（如要清理，先确认 `results/<run_id>/` 也一并清掉）
