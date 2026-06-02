#!/bin/bash
# run_step2.sh — Step 2: encode the remaining text columns with Qwen3-Embedding-8B,
# then a cumulative sweep adding one Qwen column at a time on top of the
# 3-token base (incl/excl/summary, MedCPT). Phase 2 only for the incremental
# curve; Phase 3 confirmation done separately afterwards.
set -u
cd /data2/zhu11/TB/branch/All_text_embedding
PY=/data2/zhu11/miniconda3/envs/tabpfn/bin/python
D=data

# ---- Part A: encode 8 text columns with Qwen3-Embedding-8B ----
COLS=(
  "detailed_description/textblock"
  "intervention/description"
  "condition"
  "intervention/intervention_name"
  "brief_title"
  "keyword"
  "study_design_info/intervention_model_description"
  "study_design_info/masking_description"
)
for col in "${COLS[@]}"; do
  echo "##### ENCODE $col (qwen) #####"
  $PY script/encode_text_column.py --column "$col" --encoder qwen \
      --phases Phase2,Phase3 --batch-size 16
done
echo "STEP2_ENCODE_DONE"

# ---- Part B: cumulative sweep (Phase 2) ----
BASE="$D/emb_inclusion_medcpt.parquet,$D/emb_exclusion_medcpt.parquet,$D/emb_brief_summary_textblock_medcpt.parquet"
QCOLS=(
  "$D/emb_detailed_description_textblock_qwen.parquet"
  "$D/emb_intervention_description_qwen.parquet"
  "$D/emb_condition_qwen.parquet"
  "$D/emb_intervention_intervention_name_qwen.parquet"
  "$D/emb_brief_title_qwen.parquet"
  "$D/emb_keyword_qwen.parquet"
  "$D/emb_study_design_info_intervention_model_description_qwen.parquet"
  "$D/emb_study_design_info_masking_description_qwen.parquet"
)
SUBTASKS=(
  "serious-adverse-event-forecasting|Y/N|binary"
  "mortality-event-prediction|Y/N|binary"
  "patient-dropout-event-forecasting|Y/N|binary"
  "trial-approval-forecasting|outcome|binary"
  "trial-failure-reason-identification|failure_reason|multiclass"
  "trial-duration-forecasting|time_day|regression"
)

EMBS="$BASE"
for k in 0 1 2 3 4 5 6 7; do
  EMBS="$EMBS,${QCOLS[$k]}"
  NTOK=$((4 + k))
  for cfg in "${SUBTASKS[@]}"; do
    IFS='|' read -r ST T TT <<< "$cfg"
    echo "===== ${NTOK}tok $ST Phase2 ($TT) ====="
    $PY script/full_step2_multi.py \
      --virt-embs "$EMBS" \
      --subtask "$ST" --target "$T" --task-type "$TT" \
      --phases Phase2 --epochs 30 --lr 1e-3 --lr-base 2e-5 --eval-every 3 \
      --ctx-size 3000 --qry-size 500 --unfreeze-decoder
  done
done
echo "STEP2_SWEEP_DONE"
