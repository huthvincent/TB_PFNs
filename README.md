# TB_PFNs — TabPFN / TabICL × TrialBench

Tabular foundation models (TabPFN-v2.5, **TabICLv2**) for clinical-trial event
prediction on [TrialBench](https://github.com/ML2Health/ML2ClinicalTrials), with
**virtual-token injection** of unstructured trial information (eligibility
criteria, drug SMILES, MeSH terms) into a frozen TFM.

> **Start here:** [`ReadMeFirst.md`](ReadMeFirst.md) is the project contract —
> directory layout, naming conventions, where outputs go. Read it before
> touching anything. Each subdirectory has its own `README.md`; each `branch/`
> has an `initial_readme.md` (cold-read start) → `README.md` (progress log) →
> `final_readme.md` (terminal doc).

## What's here

| Path | What |
|---|---|
| [`script/`](script/) | Shared scripts (preprocess, baseline fine-tune, GPU self-check) |
| [`branch/`](branch/) | Exploratory sub-projects, each self-contained — see [`branch/README.md`](branch/README.md) |
| [`Doc/`](Doc/) | Hand-written design / methodology / cross-experiment docs |
| [`CI/`](CI/) | TrialBench column dictionary + DAG metadata |
| `results/`, `model_checkpoint/` | Run outputs (small files tracked; weights/embeddings git-ignored) |
| `dataset/`, `TabPFN/` | **Not in git** — obtain separately (see below) |

## Branches (research lines)

| Branch | Result |
|---|---|
| [`new_FM/`](branch/new_FM/final_readme.md) | TabPFN→**TabICLv2 (BSD-3)** drop-in; +I/E virtual tokens (Full Step 2) |
| [`IE_embedding/`](branch/IE_embedding/) | inclusion/exclusion criteria → embedding → virtual tokens |
| [`smiles/`](branch/smiles/final_readme.md) | +SMILES drug-structure token → **no robust gain on SAE** (4 chem encoders, multi-seed) |
| [`mesh/`](branch/mesh/final_readme.md) | +condition/intervention MeSH tokens → **MedCPT Phase2 small but significant gain (p<0.05)** |
| [`All_text_embedding/`](branch/All_text_embedding/) | all text columns → virtual tokens (in progress) |

**Headline methodology finding:** TabICL Full-Step-2 training is
CUDA-nondeterministic — single-run best-epoch noise ≈ ±0.009 ROC-AUC, the same
order as the effects under test. All conclusions in `smiles/` and `mesh/` use
**multi-seed (mean ± std) + paired t-tests** (last-5-epoch metric), not single runs.

## Not in git (regenerate / obtain separately)

To keep the repo lean, these are `.gitignore`d:

- **`dataset/`** — TrialBench (8 subtasks × 4 phases). Download from
  [ML2ClinicalTrials/Trialbench](https://github.com/ML2Health/ML2ClinicalTrials).
- **`TabPFN/`** — upstream [PriorLabs/TabPFN](https://github.com/PriorLabs/TabPFN)
  (editable install; the v2.5 checkpoint is non-commercial — see `new_FM/`).
- **Embeddings** (`*.parquet`, `*.npy`, `*.pkl`) — regenerate with each branch's
  `encode_*.py` (e.g. `branch/mesh/script/encode_mesh_hf.py`).
- **Model weights** (`*.pth`, `*.ckpt`, `*.safetensors`).

Every result is reproducible: each `branch/*/final_readme.md` has a copy-paste
reproduction command block, and `results/*/metrics.json` records the exact `args`.

## Environment

```bash
conda activate tabpfn   # python 3.11, torch 2.9.1+cu128, transformers 4.57.6, tabicl 2.1.1
```

GPU: single NVIDIA H200 NVL (143 GB). See [`ReadMeFirst.md`](ReadMeFirst.md) §6–§7.
