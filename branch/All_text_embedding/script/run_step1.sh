#!/bin/bash
# run_step1.sh — Step 1: Full Step 2 with 3 virtual tokens (incl / excl / brief_summary,
# all MedCPT-encoded). 6 subtasks × {Phase2, Phase3} = 12 runs, 30 epochs each.
set -u
cd /data2/zhu11/TB/branch/All_text_embedding
PY=/data2/zhu11/miniconda3/envs/tabpfn/bin/python
D=data
EMBS="$D/emb_inclusion_medcpt.parquet,$D/emb_exclusion_medcpt.parquet,$D/emb_brief_summary_textblock_medcpt.parquet"

for cfg in "serious-adverse-event-forecasting|Y/N|binary" \
           "mortality-event-prediction|Y/N|binary" \
           "patient-dropout-event-forecasting|Y/N|binary" \
           "trial-approval-forecasting|outcome|binary" \
           "trial-failure-reason-identification|failure_reason|multiclass" \
           "trial-duration-forecasting|time_day|regression"; do
  IFS='|' read -r ST T TT <<< "$cfg"
  for PH in Phase2 Phase3; do
    echo "===== $ST $PH ($TT) ====="
    $PY script/full_step2_multi.py \
      --virt-embs "$EMBS" \
      --subtask "$ST" --target "$T" --task-type "$TT" \
      --phases "$PH" --epochs 30 --lr 1e-3 --lr-base 2e-5 --eval-every 3 \
      --ctx-size 3000 --qry-size 500 --unfreeze-decoder
  done
done
echo "STEP1_ALL_DONE"
