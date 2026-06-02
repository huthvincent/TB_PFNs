#!/bin/bash
# run_sae_marginal.sh — SAE marginal-injection sweep.
#
# For each text column X that exists in SAE's CSV, and for each encoder
# E ∈ {MedCPT, Qwen3-Embedding-8B}, run Full Step 2 with 3 virtual tokens:
#   incl (MedCPT) + excl (MedCPT) + X (E)
# vs the 2-token baseline (incl + excl) to measure each column's marginal gain
# in isolation and compare MedCPT vs Qwen3 per column.
#
# 8 columns × 2 encoders × 2 phases = 32 training runs.
set -u
cd /data2/zhu11/TB/branch/All_text_embedding
PY=/data2/zhu11/miniconda3/envs/tabpfn/bin/python
D=data

# Columns present in SAE's CSV (skip 1/6 columns: detailed_description, gender_description)
COLS=(
  "brief_summary/textblock"
  "brief_title"
  "condition"
  "intervention/description"
  "intervention/intervention_name"
  "keyword"
  "study_design_info/intervention_model_description"
  "study_design_info/masking_description"
)

# ---- Part A: MedCPT-encode any columns not yet encoded ----
for col in "${COLS[@]}"; do
  safe=${col//\//_}
  out="$D/emb_${safe}_medcpt.parquet"
  if [ -f "$out" ]; then
    echo "skip MedCPT encode $col (exists)"
    continue
  fi
  echo "##### ENCODE $col (medcpt) #####"
  $PY script/encode_text_column.py --column "$col" --encoder medcpt --phases Phase2,Phase3 --batch-size 256
done
echo "ENCODE_DONE"

# ---- Part B: 3-token Full Step 2 for each (column, encoder, phase) ----
BASE="$D/emb_inclusion_medcpt.parquet,$D/emb_exclusion_medcpt.parquet"
for col in "${COLS[@]}"; do
  safe=${col//\//_}
  for enc in medcpt qwen; do
    emb="$D/emb_${safe}_${enc}.parquet"
    if [ ! -f "$emb" ]; then
      echo "MISSING $emb — skip ($col, $enc)"; continue
    fi
    for PH in Phase2 Phase3; do
      echo "===== SAE $PH +${safe} ($enc) ====="
      $PY script/full_step2_multi.py \
        --virt-embs "$BASE,$emb" \
        --subtask serious-adverse-event-forecasting --target "Y/N" --task-type binary \
        --phases $PH --epochs 30 --lr 1e-3 --lr-base 2e-5 --eval-every 3 \
        --ctx-size 3000 --qry-size 500 --unfreeze-decoder
    done
  done
done
echo "SAE_MARGINAL_DONE"
