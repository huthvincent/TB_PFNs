# Pairwise Association Screen — TrialBench_joined

This file records the result of a marginal-association screen across the 71 retained columns of `/data2/zhu11/TB/dataset/TrialBench_joined/Phase{1,2,3,4}.parquet` (n = 81,786 rows, concatenated).

**Why this exists.** If two columns are not statistically associated in the data (under faithfulness), they cannot be linked by a direct causal arrow. So this screen prunes the edge candidate set for the DAG: only column pairs that appear in the *Per-feature association partners* tables below are eligible for causal edges. Pairs not listed have already been ruled out at this stage.

---

## Summary

| Quantity                                  | Value           |
|-------------------------------------------|-----------------|
| Rows in TrialBench_joined                 | 81,786          |
| Columns in source parquet                 | 81              |
| Columns excluded                          | 10              |
| **Columns retained (nodes)**              | **71**              |
| Pairs tested                              | 2,485           |
| Pairs passing threshold (associated)      | 1,169 (47.0%)   |
| Pairs filtered as independent             | 1,316 (53.0%)   |
| Effect-size threshold                     | > 0.05          |
| FDR-adjusted p-value threshold            | < 0.01          |
| Run directory                             | `/data2/zhu11/TB/results/ci_pairwise_association_20260512_093044` |

### Excluded columns

| Column | Reason |
|--------|--------|
| `brief_summary/textblock` | free-text trial summary |
| `eligibility/criteria/textblock` | free-text eligibility criteria |
| `intervention/description` | free-text intervention description |
| `detailed_description/textblock` | free-text long description |
| `study_design_info/intervention_model_description` | free-text annotation on intervention_model |
| `study_design_info/masking_description` | free-text annotation on masking |
| `eligibility/gender_description` | free-text annotation on eligibility/gender |
| `keyword` | free-text keyword list with no fixed vocabulary |
| `study_type` | constant 'Interventional' in all 81786 rows; zero variance, zero associated partners |
| `regulatory_pass` | identical (|rho|=1.0) to approval_outcome on 30683 overlapping rows; merged into approval_outcome as a single node |

After exclusion, the remaining **71 columns** are the canonical DAG nodes for the rest of the CI/ pipeline.

---

## Method

Each of the 71 retained columns is mapped to **exactly one** internal representation so it can enter a standard effect-size test. The analysis dimensionality equals the number of retained columns; there is no fan-out into multiple sub-features per column.

| Column type | Representation | Tested as |
|-------------|----------------|-----------|
| Numeric / boolean | raw value | numeric |
| Low-cardinality string (≤50 unique non-null values) | raw string | categorical |
| Structured-text / multi-valued (`condition`, `intervention/intervention_name`, `icdcode`, `smiless`, `condition_browse/mesh_term`, `intervention_browse/mesh_term`, `location/facility/address/city`, `brief_title`, `intervention/intervention_type`) | `n_items` = token count (0 ⟺ NaN) | numeric |
| Date string (`start_date`, `completion_date`) | days since 2000-01-01 | numeric |
| Age string (`eligibility/{maximum,minimum}_age`, e.g. '65 Years', '6 Months', 'N/A') | parsed to years (numeric) | numeric |

These conversions are **mandatory** for the high-cardinality / non-tabular columns — applying `χ²` to a (thousands × 4) contingency table or running `Spearman` on raw date strings does not give valid statistics. The conversions intentionally discard token content (which specific disease, which specific drug); only `whether reported / how many` is tested. The richer semantic associations enter the DAG later via domain knowledge.

Pairwise effect-size tests (all rescaled to [0, 1]):

| Pair type | Effect size                                         | p-value      |
|-----------|-----------------------------------------------------|--------------|
| num × num | \|Spearman ρ\|                                       | Spearman      |
| cat × cat | Cramér's V = √(χ² / (n · (min(r,c) − 1)))            | χ² of contingency |
| num × cat | η = √η² from one-way ANOVA                          | F-test of ANOVA |

p-values are BH-FDR-adjusted across all 2,485 tests. A pair is marked **associated** iff `effect_size > 0.05` AND `p_adj < 0.01`. All pairs (including those filtered out) live in `pairwise_all.csv` under the run directory.

---

## Strongest associations (top 30)

These are deterministic / definitional pairs (e.g., `biology_pass ↔ biology_fail`, `MaskingType-* ↔ study_design_info/masking`, duration unit conversions) plus the first tier of clear mechanistic links. They will all anchor edges in the DAG.

| col_a | col_b | effect | metric | n_valid | p_adj |
|-------|-------|--------|--------|---------|-------|
| `execution_fail` | `execution_pass` | 1.000 | abs_spearman | 52,772 | <1e-300 |
| `biology_fail` | `biology_pass` | 1.000 | abs_spearman | 34,427 | <1e-300 |
| `biology_pass` | `failure_reason` | 1.000 | eta | 20,769 | <1e-300 |
| `biology_fail` | `failure_reason` | 1.000 | eta | 20,769 | <1e-300 |
| `MaskingType-Participant` | `study_design_info/masking` | 1.000 | eta | 75,043 | <1e-300 |
| `MaskingType-Care Provider` | `study_design_info/masking` | 1.000 | eta | 75,043 | <1e-300 |
| `MaskingType-Investigator` | `study_design_info/masking` | 1.000 | eta | 75,043 | <1e-300 |
| `MaskingType-Outcomes Assessor` | `study_design_info/masking` | 1.000 | eta | 75,043 | <1e-300 |
| `study_design_info/masking` | `study_design_info/masking_num` | 1.000 | eta | 75,043 | <1e-300 |
| `duration_day` | `duration_year` | 1.000 | abs_spearman | 42,855 | <1e-300 |
| `duration_day` | `duration_month` | 1.000 | abs_spearman | 42,855 | <1e-300 |
| `duration_month` | `duration_year` | 1.000 | abs_spearman | 42,855 | <1e-300 |
| `mortality_YN` | `mortality_rate` | 0.960 | abs_spearman | 17,916 | <1e-300 |
| `dropout_YN` | `execution_fail` | 0.940 | abs_spearman | 38,302 | <1e-300 |
| `dropout_YN` | `execution_pass` | 0.940 | abs_spearman | 38,302 | <1e-300 |
| `MaskingType-Participant` | `study_design_info/masking_num` | 0.915 | abs_spearman | 81,170 | <1e-300 |
| `MaskingType-Investigator` | `study_design_info/masking_num` | 0.892 | abs_spearman | 81,170 | <1e-300 |
| `MaskingType-Investigator` | `MaskingType-Participant` | 0.878 | abs_spearman | 81,170 | <1e-300 |
| `completion_date` | `start_date` | 0.868 | abs_spearman | 42,855 | <1e-300 |
| `sae_YN` | `sae_rate` | 0.831 | abs_spearman | 17,916 | <1e-300 |
| `MaskingType-Care Provider` | `study_design_info/masking_num` | 0.779 | abs_spearman | 81,170 | <1e-300 |
| `execution_fail` | `failure_reason` | 0.755 | eta | 20,769 | <1e-300 |
| `execution_pass` | `failure_reason` | 0.755 | eta | 20,769 | <1e-300 |
| `MaskingType-Outcomes Assessor` | `study_design_info/masking_num` | 0.748 | abs_spearman | 81,170 | <1e-300 |
| `dropout_YN` | `dropout_rate` | 0.715 | abs_spearman | 38,302 | <1e-300 |
| `MaskingType-Participant` | `Placebo Comparator Arm Number` | 0.687 | abs_spearman | 77,947 | <1e-300 |
| `Placebo Comparator Arm Number` | `study_design_info/masking_num` | 0.685 | abs_spearman | 77,947 | <1e-300 |
| `MaskingType-Investigator` | `Placebo Comparator Arm Number` | 0.675 | abs_spearman | 77,947 | <1e-300 |
| `dropout_rate` | `execution_pass` | 0.671 | abs_spearman | 38,302 | <1e-300 |
| `dropout_rate` | `execution_fail` | 0.671 | abs_spearman | 38,302 | <1e-300 |

---

## Per-feature association partners

For each of the 71 retained columns, this section lists every other column it is associated with, sorted by effect size. Use this view when deciding causal direction for that feature in its `{feature}.md`.

### `Active Comparator Arm Number`   *(partners: 28)*

| partner | effect | metric | n_valid | p_adj |
|---------|--------|--------|---------|-------|
| `Experimental Arm Number` | 0.404 | abs_spearman | 69,293 | <1e-300 |
| `study_design_info/intervention_model` | 0.338 | eta | 69,093 | <1e-300 |
| `number_of_arms` | 0.278 | abs_spearman | 69,293 | <1e-300 |
| `phase` | 0.227 | eta | 69,293 | <1e-300 |
| `enrollment` | 0.222 | abs_spearman | 43,117 | <1e-300 |
| `intervention/intervention_name` | 0.220 | abs_spearman | 69,293 | <1e-300 |
| `intervention_browse/mesh_term` | 0.217 | abs_spearman | 69,293 | <1e-300 |
| `study_design_info/masking` | 0.201 | eta | 64,055 | <1e-300 |
| `study_design_info/allocation` | 0.167 | eta | 52,870 | <1e-300 |
| `Drug intervention Number` | 0.151 | abs_spearman | 69,293 | <1e-300 |
| `study_design_info/masking_num` | 0.141 | abs_spearman | 69,142 | <1e-300 |
| `smiless` | 0.140 | abs_spearman | 69,293 | 2.92e-300 |
| `responsible_party/responsible_party_type` | 0.120 | eta | 66,924 | 1.02e-210 |
| `MaskingType-Participant` | 0.120 | abs_spearman | 69,142 | 1.19e-218 |
| `sponsors/lead_sponsor/agency_class` | 0.116 | eta | 69,293 | 6.20e-201 |
| `MaskingType-Outcomes Assessor` | 0.115 | abs_spearman | 69,142 | 1.60e-200 |
| `sae_rate` | 0.111 | abs_spearman | 17,886 | 4.53e-50 |
| `MaskingType-Investigator` | 0.096 | abs_spearman | 69,142 | 1.97e-139 |
| `Other Arm Number` | 0.088 | abs_spearman | 69,293 | 1.18e-118 |
| `study_design_info/primary_purpose` | 0.085 | eta | 68,722 | 5.04e-102 |
| `MaskingType-Care Provider` | 0.081 | abs_spearman | 69,142 | 1.09e-100 |
| `failure_reason` | 0.071 | eta | 10,089 | 1.33e-10 |
| `sae_YN` | 0.069 | abs_spearman | 17,886 | 4.31e-20 |
| `brief_title` | 0.064 | abs_spearman | 69,293 | 1.10e-62 |
| `ipd_info_type-Analytic Code` | 0.062 | abs_spearman | 2,139 | 0.0060 |
| `dropout_rate` | 0.058 | abs_spearman | 38,016 | 1.79e-29 |
| `Placebo Comparator Arm Number` | 0.054 | abs_spearman | 69,293 | 7.22e-45 |
| `Behavioral intervention Number` | 0.053 | abs_spearman | 69,293 | 4.76e-43 |

### `Behavioral intervention Number`   *(partners: 13)*

| partner | effect | metric | n_valid | p_adj |
|---------|--------|--------|---------|-------|
| `ipd_info_type-Clinical Study Report (CSR)` | 0.137 | abs_spearman | 2,145 | 3.77e-10 |
| `study_design_info/masking` | 0.132 | eta | 75,043 | 2.42e-270 |
| `sponsors/lead_sponsor/agency_class` | 0.128 | eta | 71,221 | 4.37e-253 |
| `study_design_info/intervention_model` | 0.108 | eta | 80,897 | 5.14e-205 |
| `Drug intervention Number` | 0.083 | abs_spearman | 81,786 | 5.36e-124 |
| `responsible_party/responsible_party_type` | 0.078 | eta | 67,878 | 4.22e-90 |
| `ipd_info_type-Statistical Analysis Plan (SAP)` | 0.076 | abs_spearman | 2,297 | 0.0004 |
| `No Intervention Arm Number` | 0.070 | abs_spearman | 69,293 | 2.05e-75 |
| `study_design_info/primary_purpose` | 0.066 | eta | 80,983 | 3.34e-70 |
| `sae_rate` | 0.066 | abs_spearman | 17,916 | 2.75e-18 |
| `sae_YN` | 0.055 | abs_spearman | 17,916 | 3.41e-13 |
| `Active Comparator Arm Number` | 0.053 | abs_spearman | 69,293 | 4.76e-43 |
| `intervention/intervention_name` | 0.050 | abs_spearman | 81,786 | 1.69e-46 |

### `Biological intervention Number`   *(partners: 26)*

| partner | effect | metric | n_valid | p_adj |
|---------|--------|--------|---------|-------|
| `Drug intervention Number` | 0.386 | abs_spearman | 81,786 | <1e-300 |
| `study_design_info/primary_purpose` | 0.330 | eta | 80,983 | <1e-300 |
| `ipd_info_type-Informed Consent Form (ICF)` | 0.244 | abs_spearman | 2,145 | 4.01e-30 |
| `smiless` | 0.197 | abs_spearman | 81,786 | <1e-300 |
| `patient_data/sharing_ipd` | 0.187 | eta | 13,510 | 3.32e-104 |
| `eligibility/healthy_volunteers` | 0.172 | eta | 81,613 | <1e-300 |
| `eligibility/maximum_age` | 0.136 | abs_spearman | 42,760 | 1.72e-174 |
| `sae_YN` | 0.132 | abs_spearman | 17,916 | 3.30e-70 |
| `sae_rate` | 0.105 | abs_spearman | 17,916 | 2.25e-44 |
| `sponsors/lead_sponsor/agency_class` | 0.102 | eta | 71,221 | 2.07e-159 |
| `eligibility/minimum_age` | 0.099 | abs_spearman | 79,650 | 1.75e-172 |
| `Experimental Arm Number` | 0.094 | abs_spearman | 78,123 | 7.32e-153 |
| `study_design_info/intervention_model` | 0.088 | eta | 80,897 | 1.38e-134 |
| `responsible_party/responsible_party_type` | 0.083 | eta | 67,878 | 4.21e-103 |
| `mortality_rate` | 0.083 | abs_spearman | 17,916 | 1.67e-28 |
| `approval_outcome` | 0.081 | abs_spearman | 30,683 | 8.13e-46 |
| `mortality_YN` | 0.080 | abs_spearman | 17,916 | 1.09e-26 |
| `ipd_info_type-Analytic Code` | 0.079 | abs_spearman | 2,297 | 0.0002 |
| `phase` | 0.076 | eta | 81,786 | 7.06e-102 |
| `intervention/intervention_name` | 0.074 | abs_spearman | 81,786 | 3.04e-98 |
| `Other intervention Number` | 0.073 | abs_spearman | 71,221 | 3.32e-83 |
| `enrollment` | 0.072 | abs_spearman | 44,446 | 2.05e-51 |
| `brief_title` | 0.065 | abs_spearman | 81,786 | 7.45e-77 |
| `intervention_browse/mesh_term` | 0.062 | abs_spearman | 81,786 | 3.34e-70 |
| `oversight_info/has_dmc` | 0.054 | eta | 45,926 | 1.70e-30 |
| `Placebo Comparator Arm Number` | 0.053 | abs_spearman | 78,123 | 1.76e-48 |

### `Combination Product intervention Number`   *(partners: 4)*

| partner | effect | metric | n_valid | p_adj |
|---------|--------|--------|---------|-------|
| `oversight_info/is_fda_regulated_device` | 0.182 | eta | 13,676 | 2.13e-101 |
| `Drug intervention Number` | 0.097 | abs_spearman | 81,786 | 1.11e-168 |
| `start_date` | 0.065 | abs_spearman | 42,855 | 2.82e-41 |
| `completion_date` | 0.054 | abs_spearman | 42,855 | 3.19e-28 |

### `Device intervention Number`   *(partners: 18)*

| partner | effect | metric | n_valid | p_adj |
|---------|--------|--------|---------|-------|
| `oversight_info/is_fda_regulated_device` | 0.637 | eta | 11,258 | <1e-300 |
| `Drug intervention Number` | 0.180 | abs_spearman | 71,221 | <1e-300 |
| `study_design_info/masking` | 0.132 | eta | 64,727 | 1.53e-231 |
| `Sham Comparator Arm Number` | 0.118 | abs_spearman | 69,293 | 4.92e-213 |
| `oversight_info/is_fda_regulated_drug` | 0.116 | eta | 11,339 | 1.33e-34 |
| `smiless` | 0.098 | abs_spearman | 71,221 | 2.84e-150 |
| `intervention_browse/mesh_term` | 0.094 | abs_spearman | 71,221 | 7.87e-139 |
| `study_design_info/primary_purpose` | 0.087 | eta | 70,604 | 1.74e-108 |
| `phase` | 0.078 | eta | 71,221 | 7.13e-93 |
| `MaskingType-Investigator` | 0.076 | abs_spearman | 70,854 | 1.03e-89 |
| `Placebo Comparator Arm Number` | 0.072 | abs_spearman | 69,293 | 1.02e-79 |
| `sae_YN` | 0.064 | abs_spearman | 17,916 | 3.18e-17 |
| `failure_reason` | 0.060 | eta | 10,204 | 9.11e-08 |
| `Experimental Arm Number` | 0.060 | abs_spearman | 69,293 | 1.96e-55 |
| `patient_data/sharing_ipd` | 0.056 | eta | 13,510 | 1.15e-09 |
| `sponsors/lead_sponsor/agency_class` | 0.055 | eta | 71,221 | 1.64e-46 |
| `sae_rate` | 0.053 | abs_spearman | 17,916 | 3.01e-12 |
| `MaskingType-Care Provider` | 0.050 | abs_spearman | 70,854 | 5.26e-40 |

### `Diagnostic Test intervention Number`   *(partners: 1)*

| partner | effect | metric | n_valid | p_adj |
|---------|--------|--------|---------|-------|
| `study_design_info/primary_purpose` | 0.083 | eta | 70,604 | 1.62e-97 |

### `Dietary Supplement intervention Number`   *(partners: 7)*

| partner | effect | metric | n_valid | p_adj |
|---------|--------|--------|---------|-------|
| `Drug intervention Number` | 0.107 | abs_spearman | 81,786 | 1.03e-205 |
| `study_design_info/primary_purpose` | 0.089 | eta | 80,983 | 1.45e-131 |
| `sponsors/lead_sponsor/agency_class` | 0.061 | eta | 71,221 | 1.14e-56 |
| `Placebo Comparator Arm Number` | 0.060 | abs_spearman | 78,123 | 2.05e-62 |
| `study_design_info/masking` | 0.059 | eta | 75,043 | 3.38e-46 |
| `responsible_party/responsible_party_type` | 0.054 | eta | 67,878 | 1.16e-43 |
| `study_design_info/intervention_model` | 0.051 | eta | 80,897 | 3.41e-44 |

### `Drug intervention Number`   *(partners: 48)*

| partner | effect | metric | n_valid | p_adj |
|---------|--------|--------|---------|-------|
| `intervention/intervention_name` | 0.668 | abs_spearman | 81,786 | <1e-300 |
| `smiless` | 0.510 | abs_spearman | 81,786 | <1e-300 |
| `intervention_browse/mesh_term` | 0.442 | abs_spearman | 81,786 | <1e-300 |
| `Biological intervention Number` | 0.386 | abs_spearman | 81,786 | <1e-300 |
| `number_of_arms` | 0.323 | abs_spearman | 78,123 | <1e-300 |
| `MaskingType-Investigator` | 0.250 | abs_spearman | 81,170 | <1e-300 |
| `MaskingType-Participant` | 0.235 | abs_spearman | 81,170 | <1e-300 |
| `study_design_info/masking_num` | 0.224 | abs_spearman | 81,170 | <1e-300 |
| `Placebo Comparator Arm Number` | 0.208 | abs_spearman | 78,123 | <1e-300 |
| `study_design_info/intervention_model` | 0.200 | eta | 80,897 | <1e-300 |
| `Device intervention Number` | 0.180 | abs_spearman | 71,221 | <1e-300 |
| `study_design_info/primary_purpose` | 0.179 | eta | 80,983 | <1e-300 |
| `study_design_info/masking` | 0.178 | eta | 75,043 | <1e-300 |
| `ipd_info_type-Informed Consent Form (ICF)` | 0.171 | abs_spearman | 2,145 | 3.24e-15 |
| `Other intervention Number` | 0.156 | abs_spearman | 71,221 | <1e-300 |
| `MaskingType-Care Provider` | 0.155 | abs_spearman | 81,170 | <1e-300 |
| `Active Comparator Arm Number` | 0.151 | abs_spearman | 69,293 | <1e-300 |
| `Experimental Arm Number` | 0.151 | abs_spearman | 78,123 | <1e-300 |
| `enrollment` | 0.145 | abs_spearman | 44,446 | 1.66e-205 |
| `No Intervention Arm Number` | 0.122 | abs_spearman | 69,293 | 8.70e-227 |
| `MaskingType-Outcomes Assessor` | 0.113 | abs_spearman | 81,170 | 1.01e-228 |
| `location/facility/address/city` | 0.112 | abs_spearman | 81,786 | 1.03e-224 |
| `Dietary Supplement intervention Number` | 0.107 | abs_spearman | 81,786 | 1.03e-205 |
| `oversight_info/is_fda_regulated_drug` | 0.103 | eta | 13,761 | 2.24e-33 |
| `oversight_info/is_fda_regulated_device` | 0.097 | eta | 13,676 | 1.16e-29 |
| `Combination Product intervention Number` | 0.097 | abs_spearman | 81,786 | 1.11e-168 |
| `icdcode` | 0.091 | abs_spearman | 81,786 | 1.81e-150 |
| `sponsors/lead_sponsor/agency_class` | 0.089 | eta | 71,221 | 1.04e-120 |
| `study_design_info/allocation` | 0.088 | eta | 62,081 | 4.78e-107 |
| `Behavioral intervention Number` | 0.083 | abs_spearman | 81,786 | 5.36e-124 |
| `execution_pass` | 0.075 | abs_spearman | 52,772 | 6.97e-66 |
| `execution_fail` | 0.075 | abs_spearman | 52,772 | 6.97e-66 |
| `eligibility/maximum_age` | 0.070 | abs_spearman | 42,760 | 6.54e-47 |
| `responsible_party/responsible_party_type` | 0.067 | eta | 67,878 | 4.89e-67 |
| `patient_data/sharing_ipd` | 0.066 | eta | 13,510 | 3.01e-13 |
| `Other Arm Number` | 0.065 | abs_spearman | 78,123 | 2.93e-73 |
| `failure_reason` | 0.065 | eta | 20,769 | 1.81e-18 |
| `brief_title` | 0.064 | abs_spearman | 81,786 | 3.89e-74 |
| `ipd_info_type-Statistical Analysis Plan (SAP)` | 0.062 | abs_spearman | 2,297 | 0.0044 |
| `intervention/intervention_type` | 0.061 | abs_spearman | 81,786 | 2.49e-67 |
| `mortality_YN` | 0.060 | abs_spearman | 17,916 | 1.45e-15 |
| `eligibility/minimum_age` | 0.059 | abs_spearman | 79,650 | 2.21e-62 |
| `eligibility/healthy_volunteers` | 0.059 | eta | 81,613 | 1.01e-62 |
| `phase` | 0.058 | eta | 81,786 | 3.54e-59 |
| `mortality_rate` | 0.058 | abs_spearman | 17,916 | 1.83e-14 |
| `approval_outcome` | 0.056 | abs_spearman | 30,683 | 1.38e-22 |
| `Sham Comparator Arm Number` | 0.052 | abs_spearman | 69,293 | 1.28e-42 |
| `dropout_YN` | 0.052 | abs_spearman | 38,302 | 4.48e-24 |

### `Experimental Arm Number`   *(partners: 38)*

| partner | effect | metric | n_valid | p_adj |
|---------|--------|--------|---------|-------|
| `number_of_arms` | 0.488 | abs_spearman | 78,123 | <1e-300 |
| `Active Comparator Arm Number` | 0.404 | abs_spearman | 69,293 | <1e-300 |
| `phase` | 0.279 | eta | 78,123 | <1e-300 |
| `study_design_info/intervention_model` | 0.250 | eta | 77,887 | <1e-300 |
| `sponsors/lead_sponsor/agency_class` | 0.247 | eta | 69,293 | <1e-300 |
| `Other Arm Number` | 0.222 | abs_spearman | 78,123 | <1e-300 |
| `intervention/intervention_name` | 0.200 | abs_spearman | 78,123 | <1e-300 |
| `responsible_party/responsible_party_type` | 0.179 | eta | 66,924 | <1e-300 |
| `eligibility/healthy_volunteers` | 0.177 | eta | 78,060 | <1e-300 |
| `patient_data/sharing_ipd` | 0.172 | eta | 13,438 | 3.57e-88 |
| `Drug intervention Number` | 0.151 | abs_spearman | 78,123 | <1e-300 |
| `study_design_info/allocation` | 0.146 | eta | 59,269 | 4.00e-278 |
| `ipd_info_type-Clinical Study Report (CSR)` | 0.136 | abs_spearman | 2,139 | 5.05e-10 |
| `failure_reason` | 0.134 | eta | 18,919 | 4.20e-73 |
| `ipd_info_type-Statistical Analysis Plan (SAP)` | 0.128 | abs_spearman | 2,290 | 1.36e-09 |
| `location/facility/address/city` | 0.122 | abs_spearman | 78,123 | 3.71e-254 |
| `approval_outcome` | 0.121 | abs_spearman | 28,187 | 2.03e-91 |
| `duration_month` | 0.120 | abs_spearman | 42,293 | 2.25e-135 |
| `duration_year` | 0.120 | abs_spearman | 42,293 | 1.11e-133 |
| `duration_day` | 0.120 | abs_spearman | 42,293 | 1.11e-133 |
| `enrollment` | 0.111 | abs_spearman | 43,117 | 1.59e-118 |
| `sae_YN` | 0.110 | abs_spearman | 17,886 | 3.61e-49 |
| `brief_title` | 0.110 | abs_spearman | 78,123 | 6.92e-208 |
| `ipd_info_type-Analytic Code` | 0.097 | abs_spearman | 2,290 | 5.06e-06 |
| `Biological intervention Number` | 0.094 | abs_spearman | 78,123 | 7.32e-153 |
| `study_design_info/primary_purpose` | 0.092 | eta | 77,416 | 9.05e-137 |
| `study_design_info/masking` | 0.083 | eta | 72,860 | 1.34e-94 |
| `intervention/intervention_type` | 0.076 | abs_spearman | 78,123 | 1.41e-98 |
| `No Intervention Arm Number` | 0.073 | abs_spearman | 69,293 | 2.53e-81 |
| `eligibility/gender` | 0.067 | eta | 69,293 | 6.49e-68 |
| `Device intervention Number` | 0.060 | abs_spearman | 69,293 | 1.96e-55 |
| `sae_rate` | 0.060 | abs_spearman | 17,886 | 2.74e-15 |
| `Placebo Comparator Arm Number` | 0.059 | abs_spearman | 78,123 | 1.91e-61 |
| `ipd_info_type-Study Protocol` | 0.059 | abs_spearman | 2,290 | 0.0066 |
| `condition_browse/mesh_term` | 0.055 | abs_spearman | 78,123 | 5.45e-52 |
| `eligibility/maximum_age` | 0.054 | abs_spearman | 41,114 | 8.58e-28 |
| `intervention_browse/mesh_term` | 0.051 | abs_spearman | 78,123 | 1.14e-45 |
| `Procedure intervention Number` | 0.051 | abs_spearman | 69,293 | 3.03e-40 |

### `Genetic intervention Number`   *(partners: 2)*

| partner | effect | metric | n_valid | p_adj |
|---------|--------|--------|---------|-------|
| `Other intervention Number` | 0.078 | abs_spearman | 71,221 | 1.15e-96 |
| `Procedure intervention Number` | 0.069 | abs_spearman | 71,221 | 4.27e-76 |

### `MaskingType-Care Provider`   *(partners: 36)*

| partner | effect | metric | n_valid | p_adj |
|---------|--------|--------|---------|-------|
| `study_design_info/masking` | 1.000 | eta | 75,043 | <1e-300 |
| `study_design_info/masking_num` | 0.779 | abs_spearman | 81,170 | <1e-300 |
| `MaskingType-Outcomes Assessor` | 0.656 | abs_spearman | 81,170 | <1e-300 |
| `MaskingType-Participant` | 0.638 | abs_spearman | 81,170 | <1e-300 |
| `MaskingType-Investigator` | 0.634 | abs_spearman | 81,170 | <1e-300 |
| `Placebo Comparator Arm Number` | 0.494 | abs_spearman | 77,947 | <1e-300 |
| `study_design_info/intervention_model` | 0.345 | eta | 80,702 | <1e-300 |
| `number_of_arms` | 0.278 | abs_spearman | 77,947 | <1e-300 |
| `study_design_info/allocation` | 0.269 | eta | 61,818 | <1e-300 |
| `enrollment` | 0.187 | abs_spearman | 44,289 | <1e-300 |
| `intervention/intervention_name` | 0.171 | abs_spearman | 81,170 | <1e-300 |
| `Drug intervention Number` | 0.155 | abs_spearman | 81,170 | <1e-300 |
| `phase` | 0.151 | eta | 81,170 | <1e-300 |
| `mortality_rate` | 0.131 | abs_spearman | 17,890 | 5.56e-69 |
| `sae_rate` | 0.112 | abs_spearman | 17,890 | 1.13e-50 |
| `study_design_info/primary_purpose` | 0.100 | eta | 80,406 | 2.72e-168 |
| `location/facility/address/city` | 0.094 | abs_spearman | 81,170 | 3.00e-156 |
| `ipd_info_type-Analytic Code` | 0.087 | abs_spearman | 2,297 | 4.51e-05 |
| `mortality_YN` | 0.086 | abs_spearman | 17,890 | 2.19e-30 |
| `dropout_YN` | 0.085 | abs_spearman | 38,218 | 2.04e-61 |
| `oversight_info/has_dmc` | 0.084 | eta | 45,821 | 9.67e-72 |
| `Active Comparator Arm Number` | 0.081 | abs_spearman | 69,142 | 1.09e-100 |
| `start_date` | 0.076 | abs_spearman | 42,635 | 1.17e-55 |
| `Radiation intervention Number` | 0.075 | abs_spearman | 81,170 | 1.27e-100 |
| `ipd_info_type-Clinical Study Report (CSR)` | 0.074 | abs_spearman | 2,145 | 0.0008 |
| `Procedure intervention Number` | 0.072 | abs_spearman | 70,854 | 1.11e-81 |
| `execution_pass` | 0.069 | abs_spearman | 52,422 | 3.32e-56 |
| `execution_fail` | 0.069 | abs_spearman | 52,422 | 3.32e-56 |
| `intervention_browse/mesh_term` | 0.062 | abs_spearman | 81,170 | 7.35e-69 |
| `Other Arm Number` | 0.060 | abs_spearman | 77,947 | 2.32e-63 |
| `Other intervention Number` | 0.060 | abs_spearman | 70,854 | 8.56e-57 |
| `oversight_info/is_fda_regulated_device` | 0.055 | eta | 13,666 | 1.72e-10 |
| `sponsors/lead_sponsor/agency_class` | 0.055 | eta | 70,854 | 2.92e-46 |
| `completion_date` | 0.052 | abs_spearman | 42,635 | 1.04e-26 |
| `No Intervention Arm Number` | 0.052 | abs_spearman | 69,142 | 2.64e-42 |
| `Device intervention Number` | 0.050 | abs_spearman | 70,854 | 5.26e-40 |

### `MaskingType-Investigator`   *(partners: 43)*

| partner | effect | metric | n_valid | p_adj |
|---------|--------|--------|---------|-------|
| `study_design_info/masking` | 1.000 | eta | 75,043 | <1e-300 |
| `study_design_info/masking_num` | 0.892 | abs_spearman | 81,170 | <1e-300 |
| `MaskingType-Participant` | 0.878 | abs_spearman | 81,170 | <1e-300 |
| `Placebo Comparator Arm Number` | 0.675 | abs_spearman | 77,947 | <1e-300 |
| `MaskingType-Care Provider` | 0.634 | abs_spearman | 81,170 | <1e-300 |
| `MaskingType-Outcomes Assessor` | 0.547 | abs_spearman | 81,170 | <1e-300 |
| `study_design_info/intervention_model` | 0.479 | eta | 80,702 | <1e-300 |
| `number_of_arms` | 0.419 | abs_spearman | 77,947 | <1e-300 |
| `study_design_info/allocation` | 0.405 | eta | 61,818 | <1e-300 |
| `enrollment` | 0.287 | abs_spearman | 44,289 | <1e-300 |
| `intervention/intervention_name` | 0.271 | abs_spearman | 81,170 | <1e-300 |
| `Drug intervention Number` | 0.250 | abs_spearman | 81,170 | <1e-300 |
| `mortality_rate` | 0.205 | abs_spearman | 17,890 | 3.43e-168 |
| `phase` | 0.185 | eta | 81,170 | <1e-300 |
| `sae_rate` | 0.182 | abs_spearman | 17,890 | 7.78e-133 |
| `ipd_info_type-Clinical Study Report (CSR)` | 0.158 | abs_spearman | 2,145 | 3.33e-13 |
| `sponsors/lead_sponsor/agency_class` | 0.153 | eta | 70,854 | <1e-300 |
| `mortality_YN` | 0.140 | abs_spearman | 17,890 | 8.90e-79 |
| `dropout_YN` | 0.137 | abs_spearman | 38,218 | 1.93e-158 |
| `execution_pass` | 0.115 | abs_spearman | 52,422 | 5.41e-154 |
| `execution_fail` | 0.115 | abs_spearman | 52,422 | 5.41e-154 |
| `location/facility/address/city` | 0.111 | abs_spearman | 81,170 | 2.13e-221 |
| `Radiation intervention Number` | 0.106 | abs_spearman | 81,170 | 9.78e-200 |
| `Procedure intervention Number` | 0.104 | abs_spearman | 70,854 | 5.59e-169 |
| `study_design_info/primary_purpose` | 0.103 | eta | 80,406 | 8.35e-179 |
| `Active Comparator Arm Number` | 0.096 | abs_spearman | 69,142 | 1.97e-139 |
| `duration_month` | 0.085 | abs_spearman | 42,635 | 6.87e-68 |
| `patient_data/sharing_ipd` | 0.085 | eta | 13,493 | 2.35e-21 |
| `duration_day` | 0.084 | abs_spearman | 42,635 | 3.17e-67 |
| `duration_year` | 0.084 | abs_spearman | 42,635 | 3.17e-67 |
| `Other intervention Number` | 0.084 | abs_spearman | 70,854 | 7.13e-110 |
| `intervention_browse/mesh_term` | 0.083 | abs_spearman | 81,170 | 7.04e-124 |
| `approval_outcome` | 0.083 | abs_spearman | 30,351 | 8.78e-47 |
| `No Intervention Arm Number` | 0.079 | abs_spearman | 69,142 | 1.44e-96 |
| `Other Arm Number` | 0.077 | abs_spearman | 77,947 | 2.20e-103 |
| `Device intervention Number` | 0.076 | abs_spearman | 70,854 | 1.03e-89 |
| `oversight_info/is_fda_regulated_device` | 0.074 | eta | 13,666 | 1.18e-17 |
| `failure_reason` | 0.071 | eta | 20,495 | 8.60e-22 |
| `ipd_info_type-Informed Consent Form (ICF)` | 0.069 | abs_spearman | 2,145 | 0.0021 |
| `intervention/intervention_type` | 0.064 | abs_spearman | 81,170 | 4.35e-73 |
| `condition` | 0.059 | abs_spearman | 81,170 | 8.73e-63 |
| `start_date` | 0.055 | abs_spearman | 42,635 | 1.03e-29 |
| `eligibility/minimum_age` | 0.052 | abs_spearman | 79,096 | 1.72e-47 |

### `MaskingType-Outcomes Assessor`   *(partners: 33)*

| partner | effect | metric | n_valid | p_adj |
|---------|--------|--------|---------|-------|
| `study_design_info/masking` | 1.000 | eta | 75,043 | <1e-300 |
| `study_design_info/masking_num` | 0.748 | abs_spearman | 81,170 | <1e-300 |
| `MaskingType-Care Provider` | 0.656 | abs_spearman | 81,170 | <1e-300 |
| `MaskingType-Participant` | 0.554 | abs_spearman | 81,170 | <1e-300 |
| `MaskingType-Investigator` | 0.547 | abs_spearman | 81,170 | <1e-300 |
| `Placebo Comparator Arm Number` | 0.412 | abs_spearman | 77,947 | <1e-300 |
| `study_design_info/intervention_model` | 0.352 | eta | 80,702 | <1e-300 |
| `number_of_arms` | 0.277 | abs_spearman | 77,947 | <1e-300 |
| `study_design_info/allocation` | 0.268 | eta | 61,818 | <1e-300 |
| `enrollment` | 0.196 | abs_spearman | 44,289 | <1e-300 |
| `intervention/intervention_name` | 0.165 | abs_spearman | 81,170 | <1e-300 |
| `phase` | 0.159 | eta | 81,170 | <1e-300 |
| `sae_rate` | 0.144 | abs_spearman | 17,890 | 1.81e-82 |
| `mortality_rate` | 0.142 | abs_spearman | 17,890 | 2.72e-80 |
| `Active Comparator Arm Number` | 0.115 | abs_spearman | 69,142 | 1.60e-200 |
| `Drug intervention Number` | 0.113 | abs_spearman | 81,170 | 1.01e-228 |
| `study_design_info/primary_purpose` | 0.097 | eta | 80,406 | 3.15e-157 |
| `mortality_YN` | 0.096 | abs_spearman | 17,890 | 2.00e-37 |
| `dropout_YN` | 0.084 | abs_spearman | 38,218 | 8.26e-61 |
| `location/facility/address/city` | 0.077 | abs_spearman | 81,170 | 1.67e-107 |
| `Radiation intervention Number` | 0.077 | abs_spearman | 81,170 | 2.41e-106 |
| `start_date` | 0.075 | abs_spearman | 42,635 | 4.58e-53 |
| `execution_fail` | 0.073 | abs_spearman | 52,422 | 1.36e-62 |
| `execution_pass` | 0.073 | abs_spearman | 52,422 | 1.36e-62 |
| `Sham Comparator Arm Number` | 0.071 | abs_spearman | 69,142 | 3.64e-78 |
| `sponsors/lead_sponsor/agency_class` | 0.062 | eta | 70,854 | 4.74e-59 |
| `oversight_info/has_dmc` | 0.060 | eta | 45,821 | 7.72e-37 |
| `ipd_info_type-Analytic Code` | 0.059 | abs_spearman | 2,297 | 0.0063 |
| `Other intervention Number` | 0.058 | abs_spearman | 70,854 | 7.25e-53 |
| `intervention_browse/mesh_term` | 0.056 | abs_spearman | 81,170 | 9.11e-58 |
| `responsible_party/responsible_party_type` | 0.054 | eta | 67,639 | 9.24e-44 |
| `eligibility/gender` | 0.052 | eta | 70,854 | 3.02e-42 |
| `completion_date` | 0.051 | abs_spearman | 42,635 | 4.11e-25 |

### `MaskingType-Participant`   *(partners: 44)*

| partner | effect | metric | n_valid | p_adj |
|---------|--------|--------|---------|-------|
| `study_design_info/masking` | 1.000 | eta | 75,043 | <1e-300 |
| `study_design_info/masking_num` | 0.915 | abs_spearman | 81,170 | <1e-300 |
| `MaskingType-Investigator` | 0.878 | abs_spearman | 81,170 | <1e-300 |
| `Placebo Comparator Arm Number` | 0.687 | abs_spearman | 77,947 | <1e-300 |
| `MaskingType-Care Provider` | 0.638 | abs_spearman | 81,170 | <1e-300 |
| `MaskingType-Outcomes Assessor` | 0.554 | abs_spearman | 81,170 | <1e-300 |
| `study_design_info/intervention_model` | 0.512 | eta | 80,702 | <1e-300 |
| `number_of_arms` | 0.443 | abs_spearman | 77,947 | <1e-300 |
| `study_design_info/allocation` | 0.436 | eta | 61,818 | <1e-300 |
| `intervention/intervention_name` | 0.279 | abs_spearman | 81,170 | <1e-300 |
| `enrollment` | 0.279 | abs_spearman | 44,289 | <1e-300 |
| `Drug intervention Number` | 0.235 | abs_spearman | 81,170 | <1e-300 |
| `mortality_rate` | 0.230 | abs_spearman | 17,890 | 7.62e-213 |
| `sae_rate` | 0.220 | abs_spearman | 17,890 | 3.43e-194 |
| `phase` | 0.173 | eta | 81,170 | <1e-300 |
| `mortality_YN` | 0.164 | abs_spearman | 17,890 | 7.41e-108 |
| `ipd_info_type-Clinical Study Report (CSR)` | 0.135 | abs_spearman | 2,145 | 7.13e-10 |
| `dropout_YN` | 0.121 | abs_spearman | 38,218 | 1.50e-124 |
| `Active Comparator Arm Number` | 0.120 | abs_spearman | 69,142 | 1.19e-218 |
| `sponsors/lead_sponsor/agency_class` | 0.118 | eta | 70,854 | 1.37e-213 |
| `study_design_info/primary_purpose` | 0.115 | eta | 80,406 | 4.45e-223 |
| `Radiation intervention Number` | 0.113 | abs_spearman | 81,170 | 1.72e-227 |
| `execution_pass` | 0.102 | abs_spearman | 52,422 | 3.62e-121 |
| `execution_fail` | 0.102 | abs_spearman | 52,422 | 3.62e-121 |
| `duration_month` | 0.102 | abs_spearman | 42,635 | 3.67e-98 |
| `duration_year` | 0.102 | abs_spearman | 42,635 | 9.19e-98 |
| `duration_day` | 0.102 | abs_spearman | 42,635 | 9.19e-98 |
| `intervention_browse/mesh_term` | 0.094 | abs_spearman | 81,170 | 8.76e-157 |
| `Other intervention Number` | 0.093 | abs_spearman | 70,854 | 1.03e-133 |
| `location/facility/address/city` | 0.088 | abs_spearman | 81,170 | 1.26e-139 |
| `Procedure intervention Number` | 0.085 | abs_spearman | 70,854 | 4.62e-113 |
| `Other Arm Number` | 0.080 | abs_spearman | 77,947 | 3.18e-109 |
| `start_date` | 0.076 | abs_spearman | 42,635 | 2.69e-55 |
| `No Intervention Arm Number` | 0.073 | abs_spearman | 69,142 | 6.46e-81 |
| `approval_outcome` | 0.071 | abs_spearman | 30,351 | 3.86e-35 |
| `Sham Comparator Arm Number` | 0.067 | abs_spearman | 69,142 | 5.16e-69 |
| `patient_data/sharing_ipd` | 0.066 | eta | 13,493 | 4.75e-13 |
| `failure_reason` | 0.065 | eta | 20,495 | 3.18e-18 |
| `ipd_info_type-Informed Consent Form (ICF)` | 0.064 | abs_spearman | 2,145 | 0.0042 |
| `intervention/intervention_type` | 0.064 | abs_spearman | 81,170 | 1.08e-73 |
| `eligibility/minimum_age` | 0.064 | abs_spearman | 79,096 | 1.15e-71 |
| `eligibility/healthy_volunteers` | 0.058 | eta | 81,014 | 1.34e-60 |
| `oversight_info/is_fda_regulated_device` | 0.055 | eta | 13,666 | 2.05e-10 |
| `condition` | 0.055 | abs_spearman | 81,170 | 2.69e-54 |

### `No Intervention Arm Number`   *(partners: 22)*

| partner | effect | metric | n_valid | p_adj |
|---------|--------|--------|---------|-------|
| `intervention/intervention_name` | 0.148 | abs_spearman | 69,293 | <1e-300 |
| `sponsors/lead_sponsor/agency_class` | 0.137 | eta | 69,293 | 1.54e-281 |
| `study_design_info/masking` | 0.134 | eta | 64,055 | 3.81e-234 |
| `Drug intervention Number` | 0.122 | abs_spearman | 69,293 | 8.70e-227 |
| `responsible_party/responsible_party_type` | 0.113 | eta | 66,924 | 1.99e-186 |
| `study_design_info/intervention_model` | 0.099 | eta | 69,093 | 5.10e-146 |
| `Placebo Comparator Arm Number` | 0.093 | abs_spearman | 69,293 | 6.95e-132 |
| `phase` | 0.090 | eta | 69,293 | 8.35e-121 |
| `MaskingType-Investigator` | 0.079 | abs_spearman | 69,142 | 1.44e-96 |
| `study_design_info/primary_purpose` | 0.078 | eta | 68,722 | 4.38e-85 |
| `Experimental Arm Number` | 0.073 | abs_spearman | 69,293 | 2.53e-81 |
| `MaskingType-Participant` | 0.073 | abs_spearman | 69,142 | 6.46e-81 |
| `Behavioral intervention Number` | 0.070 | abs_spearman | 69,293 | 2.05e-75 |
| `sae_rate` | 0.069 | abs_spearman | 17,886 | 8.01e-20 |
| `sae_YN` | 0.068 | abs_spearman | 17,886 | 3.16e-19 |
| `approval_outcome` | 0.066 | abs_spearman | 22,770 | 5.39e-23 |
| `location/facility/address/city` | 0.063 | abs_spearman | 69,293 | 7.89e-61 |
| `ipd_info_type-Statistical Analysis Plan (SAP)` | 0.060 | abs_spearman | 2,139 | 0.0077 |
| `patient_data/sharing_ipd` | 0.058 | eta | 13,438 | 2.36e-10 |
| `number_of_arms` | 0.057 | abs_spearman | 69,293 | 9.39e-51 |
| `study_design_info/masking_num` | 0.057 | abs_spearman | 69,142 | 9.27e-50 |
| `MaskingType-Care Provider` | 0.052 | abs_spearman | 69,142 | 2.64e-42 |

### `Other Arm Number`   *(partners: 16)*

| partner | effect | metric | n_valid | p_adj |
|---------|--------|--------|---------|-------|
| `Experimental Arm Number` | 0.222 | abs_spearman | 78,123 | <1e-300 |
| `Placebo Comparator Arm Number` | 0.101 | abs_spearman | 78,123 | 4.10e-174 |
| `Active Comparator Arm Number` | 0.088 | abs_spearman | 69,293 | 1.18e-118 |
| `study_design_info/primary_purpose` | 0.082 | eta | 77,416 | 4.49e-106 |
| `MaskingType-Participant` | 0.080 | abs_spearman | 77,947 | 3.18e-109 |
| `MaskingType-Investigator` | 0.077 | abs_spearman | 77,947 | 2.20e-103 |
| `study_design_info/masking_num` | 0.076 | abs_spearman | 77,947 | 3.47e-100 |
| `Other intervention Number` | 0.072 | abs_spearman | 69,293 | 1.16e-79 |
| `Drug intervention Number` | 0.065 | abs_spearman | 78,123 | 2.93e-73 |
| `phase` | 0.061 | eta | 78,123 | 9.70e-63 |
| `study_design_info/intervention_model` | 0.061 | eta | 77,887 | 3.48e-60 |
| `MaskingType-Care Provider` | 0.060 | abs_spearman | 77,947 | 2.32e-63 |
| `ipd_info_type-Study Protocol` | 0.060 | abs_spearman | 2,290 | 0.0054 |
| `sae_YN` | 0.057 | abs_spearman | 17,886 | 5.30e-14 |
| `study_design_info/masking` | 0.056 | eta | 72,860 | 2.05e-38 |
| `sae_rate` | 0.055 | abs_spearman | 17,886 | 5.45e-13 |

### `Other intervention Number`   *(partners: 24)*

| partner | effect | metric | n_valid | p_adj |
|---------|--------|--------|---------|-------|
| `sponsors/lead_sponsor/agency_class` | 0.185 | eta | 71,221 | <1e-300 |
| `intervention/intervention_name` | 0.181 | abs_spearman | 71,221 | <1e-300 |
| `Drug intervention Number` | 0.156 | abs_spearman | 71,221 | <1e-300 |
| `Placebo Comparator Arm Number` | 0.114 | abs_spearman | 69,293 | 1.43e-199 |
| `condition` | 0.093 | abs_spearman | 71,221 | 4.79e-135 |
| `MaskingType-Participant` | 0.093 | abs_spearman | 70,854 | 1.03e-133 |
| `study_design_info/masking_num` | 0.088 | abs_spearman | 70,854 | 7.29e-122 |
| `MaskingType-Investigator` | 0.084 | abs_spearman | 70,854 | 7.13e-110 |
| `icdcode` | 0.081 | abs_spearman | 71,221 | 1.29e-103 |
| `Genetic intervention Number` | 0.078 | abs_spearman | 71,221 | 1.15e-96 |
| `study_design_info/primary_purpose` | 0.075 | eta | 70,604 | 1.83e-80 |
| `study_design_info/masking` | 0.075 | eta | 64,727 | 4.89e-67 |
| `oversight_info/has_dmc` | 0.074 | eta | 37,612 | 2.12e-46 |
| `Biological intervention Number` | 0.073 | abs_spearman | 71,221 | 3.32e-83 |
| `approval_outcome` | 0.072 | abs_spearman | 24,108 | 9.10e-29 |
| `Other Arm Number` | 0.072 | abs_spearman | 69,293 | 1.16e-79 |
| `MaskingType-Care Provider` | 0.060 | abs_spearman | 70,854 | 8.56e-57 |
| `MaskingType-Outcomes Assessor` | 0.058 | abs_spearman | 70,854 | 7.25e-53 |
| `study_design_info/allocation` | 0.058 | eta | 54,376 | 1.27e-40 |
| `duration_month` | 0.057 | abs_spearman | 42,855 | 4.05e-32 |
| `duration_day` | 0.057 | abs_spearman | 42,855 | 4.15e-32 |
| `duration_year` | 0.057 | abs_spearman | 42,855 | 4.15e-32 |
| `Procedure intervention Number` | 0.055 | abs_spearman | 71,221 | 2.15e-48 |
| `study_design_info/intervention_model` | 0.054 | eta | 70,749 | 6.09e-43 |

### `Placebo Comparator Arm Number`   *(partners: 41)*

| partner | effect | metric | n_valid | p_adj |
|---------|--------|--------|---------|-------|
| `MaskingType-Participant` | 0.687 | abs_spearman | 77,947 | <1e-300 |
| `study_design_info/masking_num` | 0.685 | abs_spearman | 77,947 | <1e-300 |
| `MaskingType-Investigator` | 0.675 | abs_spearman | 77,947 | <1e-300 |
| `study_design_info/masking` | 0.616 | eta | 72,860 | <1e-300 |
| `MaskingType-Care Provider` | 0.494 | abs_spearman | 77,947 | <1e-300 |
| `MaskingType-Outcomes Assessor` | 0.412 | abs_spearman | 77,947 | <1e-300 |
| `number_of_arms` | 0.352 | abs_spearman | 78,123 | <1e-300 |
| `study_design_info/intervention_model` | 0.341 | eta | 77,887 | <1e-300 |
| `study_design_info/allocation` | 0.261 | eta | 59,269 | <1e-300 |
| `intervention/intervention_name` | 0.213 | abs_spearman | 78,123 | <1e-300 |
| `Drug intervention Number` | 0.208 | abs_spearman | 78,123 | <1e-300 |
| `enrollment` | 0.202 | abs_spearman | 43,117 | <1e-300 |
| `mortality_rate` | 0.182 | abs_spearman | 17,886 | 1.98e-132 |
| `sae_rate` | 0.154 | abs_spearman | 17,886 | 1.01e-94 |
| `intervention_browse/mesh_term` | 0.142 | abs_spearman | 78,123 | <1e-300 |
| `mortality_YN` | 0.137 | abs_spearman | 17,886 | 3.29e-75 |
| `Other intervention Number` | 0.114 | abs_spearman | 69,293 | 1.43e-199 |
| `ipd_info_type-Clinical Study Report (CSR)` | 0.114 | abs_spearman | 2,139 | 2.28e-07 |
| `dropout_YN` | 0.114 | abs_spearman | 38,016 | 7.11e-109 |
| `sponsors/lead_sponsor/agency_class` | 0.104 | eta | 69,293 | 3.80e-161 |
| `Other Arm Number` | 0.101 | abs_spearman | 78,123 | 4.10e-174 |
| `phase` | 0.094 | eta | 78,123 | 9.42e-151 |
| `No Intervention Arm Number` | 0.093 | abs_spearman | 69,293 | 6.95e-132 |
| `Procedure intervention Number` | 0.091 | abs_spearman | 69,293 | 2.21e-125 |
| `ipd_info_type-Informed Consent Form (ICF)` | 0.090 | abs_spearman | 2,139 | 4.58e-05 |
| `Radiation intervention Number` | 0.087 | abs_spearman | 78,123 | 4.09e-129 |
| `execution_pass` | 0.079 | abs_spearman | 50,684 | 1.36e-70 |
| `execution_fail` | 0.079 | abs_spearman | 50,684 | 1.36e-70 |
| `study_design_info/primary_purpose` | 0.077 | eta | 77,416 | 1.07e-93 |
| `location/facility/address/city` | 0.076 | abs_spearman | 78,123 | 3.59e-99 |
| `Device intervention Number` | 0.072 | abs_spearman | 69,293 | 1.02e-79 |
| `failure_reason` | 0.069 | eta | 18,919 | 7.68e-19 |
| `oversight_info/is_fda_regulated_device` | 0.065 | eta | 13,650 | 7.62e-14 |
| `Dietary Supplement intervention Number` | 0.060 | abs_spearman | 78,123 | 2.05e-62 |
| `Experimental Arm Number` | 0.059 | abs_spearman | 78,123 | 1.91e-61 |
| `smiless` | 0.057 | abs_spearman | 78,123 | 8.46e-56 |
| `eligibility/minimum_age` | 0.054 | abs_spearman | 76,141 | 1.24e-50 |
| `Active Comparator Arm Number` | 0.054 | abs_spearman | 69,293 | 7.22e-45 |
| `Biological intervention Number` | 0.053 | abs_spearman | 78,123 | 1.76e-48 |
| `condition` | 0.051 | abs_spearman | 78,123 | 6.67e-46 |
| `oversight_info/is_fda_regulated_drug` | 0.050 | eta | 13,735 | 6.13e-09 |

### `Procedure intervention Number`   *(partners: 37)*

| partner | effect | metric | n_valid | p_adj |
|---------|--------|--------|---------|-------|
| `Radiation intervention Number` | 0.211 | abs_spearman | 71,221 | <1e-300 |
| `intervention/intervention_name` | 0.163 | abs_spearman | 71,221 | <1e-300 |
| `sponsors/lead_sponsor/agency_class` | 0.149 | eta | 71,221 | <1e-300 |
| `duration_month` | 0.104 | abs_spearman | 42,855 | 5.71e-103 |
| `MaskingType-Investigator` | 0.104 | abs_spearman | 70,854 | 5.59e-169 |
| `duration_year` | 0.104 | abs_spearman | 42,855 | 2.14e-102 |
| `duration_day` | 0.104 | abs_spearman | 42,855 | 2.14e-102 |
| `study_design_info/masking` | 0.101 | eta | 64,727 | 5.44e-128 |
| `mortality_rate` | 0.092 | abs_spearman | 17,916 | 2.08e-34 |
| `Placebo Comparator Arm Number` | 0.091 | abs_spearman | 69,293 | 2.21e-125 |
| `study_design_info/masking_num` | 0.090 | abs_spearman | 70,854 | 1.23e-125 |
| `ipd_info_type-Statistical Analysis Plan (SAP)` | 0.085 | abs_spearman | 2,145 | 0.0001 |
| `MaskingType-Participant` | 0.085 | abs_spearman | 70,854 | 4.62e-113 |
| `approval_outcome` | 0.080 | abs_spearman | 24,108 | 5.33e-35 |
| `start_date` | 0.078 | abs_spearman | 42,855 | 1.70e-58 |
| `failure_reason` | 0.077 | eta | 10,204 | 6.13e-13 |
| `ipd_info_type-Clinical Study Report (CSR)` | 0.076 | abs_spearman | 2,145 | 0.0006 |
| `ipd_info_type-Informed Consent Form (ICF)` | 0.075 | abs_spearman | 2,145 | 0.0007 |
| `mortality_YN` | 0.073 | abs_spearman | 17,916 | 3.83e-22 |
| `condition` | 0.073 | abs_spearman | 71,221 | 1.50e-83 |
| `MaskingType-Care Provider` | 0.072 | abs_spearman | 70,854 | 1.11e-81 |
| `number_of_arms` | 0.070 | abs_spearman | 69,293 | 4.59e-76 |
| `Genetic intervention Number` | 0.069 | abs_spearman | 71,221 | 4.27e-76 |
| `enrollment` | 0.067 | abs_spearman | 44,446 | 6.83e-45 |
| `study_design_info/primary_purpose` | 0.067 | eta | 70,604 | 1.62e-61 |
| `patient_data/sharing_ipd` | 0.062 | eta | 13,510 | 7.44e-12 |
| `study_design_info/intervention_model` | 0.060 | eta | 70,749 | 5.11e-54 |
| `responsible_party/responsible_party_type` | 0.056 | eta | 67,878 | 1.92e-46 |
| `oversight_info/has_dmc` | 0.056 | eta | 37,612 | 5.37e-27 |
| `Sham Comparator Arm Number` | 0.055 | abs_spearman | 69,293 | 2.20e-47 |
| `Other intervention Number` | 0.055 | abs_spearman | 71,221 | 2.15e-48 |
| `phase` | 0.054 | eta | 71,221 | 6.74e-45 |
| `dropout_YN` | 0.053 | abs_spearman | 38,302 | 3.02e-25 |
| `eligibility/maximum_age` | 0.052 | abs_spearman | 37,908 | 2.64e-23 |
| `icdcode` | 0.051 | abs_spearman | 71,221 | 8.87e-42 |
| `Experimental Arm Number` | 0.051 | abs_spearman | 69,293 | 3.03e-40 |
| `eligibility/healthy_volunteers` | 0.051 | eta | 71,109 | 5.48e-41 |

### `Radiation intervention Number`   *(partners: 33)*

| partner | effect | metric | n_valid | p_adj |
|---------|--------|--------|---------|-------|
| `Procedure intervention Number` | 0.211 | abs_spearman | 71,221 | <1e-300 |
| `mortality_rate` | 0.146 | abs_spearman | 17,916 | 5.43e-85 |
| `intervention/intervention_name` | 0.136 | abs_spearman | 81,786 | <1e-300 |
| `sponsors/lead_sponsor/agency_class` | 0.134 | eta | 71,221 | 1.42e-279 |
| `duration_month` | 0.131 | abs_spearman | 42,855 | 1.81e-162 |
| `duration_day` | 0.131 | abs_spearman | 42,855 | 2.21e-162 |
| `duration_year` | 0.131 | abs_spearman | 42,855 | 2.21e-162 |
| `mortality_YN` | 0.119 | abs_spearman | 17,916 | 8.24e-57 |
| `study_design_info/masking_num` | 0.118 | abs_spearman | 81,170 | 6.43e-249 |
| `study_design_info/masking` | 0.115 | eta | 75,043 | 3.52e-201 |
| `MaskingType-Participant` | 0.113 | abs_spearman | 81,170 | 1.72e-227 |
| `MaskingType-Investigator` | 0.106 | abs_spearman | 81,170 | 9.78e-200 |
| `sae_rate` | 0.098 | abs_spearman | 17,916 | 6.36e-39 |
| `number_of_arms` | 0.093 | abs_spearman | 78,123 | 3.16e-149 |
| `start_date` | 0.089 | abs_spearman | 42,855 | 9.48e-75 |
| `study_design_info/intervention_model` | 0.089 | eta | 80,897 | 1.17e-135 |
| `Placebo Comparator Arm Number` | 0.087 | abs_spearman | 78,123 | 4.09e-129 |
| `phase` | 0.080 | eta | 81,786 | 8.54e-112 |
| `MaskingType-Outcomes Assessor` | 0.077 | abs_spearman | 81,170 | 2.41e-106 |
| `oversight_info/has_dmc` | 0.076 | eta | 45,926 | 2.06e-59 |
| `MaskingType-Care Provider` | 0.075 | abs_spearman | 81,170 | 1.27e-100 |
| `approval_outcome` | 0.069 | abs_spearman | 30,683 | 2.51e-33 |
| `intervention_browse/mesh_term` | 0.068 | abs_spearman | 81,786 | 1.27e-83 |
| `ipd_info_type-Clinical Study Report (CSR)` | 0.066 | abs_spearman | 2,145 | 0.0034 |
| `eligibility/healthy_volunteers` | 0.065 | eta | 81,613 | 1.42e-76 |
| `smiless` | 0.065 | abs_spearman | 81,786 | 2.71e-76 |
| `oversight_info/is_fda_regulated_device` | 0.065 | eta | 13,676 | 8.02e-14 |
| `failure_reason` | 0.061 | eta | 20,769 | 2.44e-16 |
| `eligibility/maximum_age` | 0.060 | abs_spearman | 42,760 | 6.21e-35 |
| `study_design_info/primary_purpose` | 0.058 | eta | 80,983 | 8.81e-53 |
| `sae_YN` | 0.057 | abs_spearman | 17,916 | 4.58e-14 |
| `enrollment` | 0.057 | abs_spearman | 44,446 | 1.35e-32 |
| `icdcode` | 0.052 | abs_spearman | 81,786 | 1.03e-49 |

### `Sham Comparator Arm Number`   *(partners: 9)*

| partner | effect | metric | n_valid | p_adj |
|---------|--------|--------|---------|-------|
| `study_design_info/masking` | 0.135 | eta | 64,055 | 3.90e-238 |
| `Device intervention Number` | 0.118 | abs_spearman | 69,293 | 4.92e-213 |
| `oversight_info/is_fda_regulated_device` | 0.110 | eta | 11,246 | 4.61e-31 |
| `MaskingType-Outcomes Assessor` | 0.071 | abs_spearman | 69,142 | 3.64e-78 |
| `MaskingType-Participant` | 0.067 | abs_spearman | 69,142 | 5.16e-69 |
| `study_design_info/masking_num` | 0.064 | abs_spearman | 69,142 | 5.76e-64 |
| `study_design_info/intervention_model` | 0.056 | eta | 69,093 | 1.05e-44 |
| `Procedure intervention Number` | 0.055 | abs_spearman | 69,293 | 2.20e-47 |
| `Drug intervention Number` | 0.052 | abs_spearman | 69,293 | 1.28e-42 |

### `approval_outcome`   *(partners: 37)*

| partner | effect | metric | n_valid | p_adj |
|---------|--------|--------|---------|-------|
| `intervention/intervention_type` | 0.464 | abs_spearman | 30,683 | <1e-300 |
| `location/facility/address/city` | 0.360 | abs_spearman | 30,683 | <1e-300 |
| `completion_date` | 0.333 | abs_spearman | 9,263 | 1.97e-237 |
| `start_date` | 0.296 | abs_spearman | 9,263 | 2.90e-185 |
| `biology_pass` | 0.295 | abs_spearman | 27,420 | <1e-300 |
| `biology_fail` | 0.295 | abs_spearman | 27,420 | <1e-300 |
| `enrollment` | 0.288 | abs_spearman | 20,273 | <1e-300 |
| `sponsors/lead_sponsor/agency_class` | 0.275 | eta | 24,108 | <1e-300 |
| `patient_data/sharing_ipd` | 0.248 | eta | 4,575 | 2.12e-63 |
| `execution_pass` | 0.226 | abs_spearman | 23,059 | 4.06e-264 |
| `execution_fail` | 0.226 | abs_spearman | 23,059 | 4.06e-264 |
| `sae_YN` | 0.175 | abs_spearman | 5,434 | 4.42e-38 |
| `phase` | 0.156 | eta | 30,683 | 1.19e-162 |
| `dropout_YN` | 0.154 | abs_spearman | 14,131 | 3.86e-75 |
| `study_design_info/masking` | 0.147 | eta | 24,224 | 2.27e-101 |
| `responsible_party/responsible_party_type` | 0.147 | eta | 21,870 | 1.01e-103 |
| `dropout_rate` | 0.143 | abs_spearman | 14,131 | 7.36e-65 |
| `ipd_info_type-Statistical Analysis Plan (SAP)` | 0.131 | abs_spearman | 746 | 0.0005 |
| `Experimental Arm Number` | 0.121 | abs_spearman | 28,187 | 2.03e-91 |
| `oversight_info/has_dmc` | 0.116 | eta | 21,810 | 5.91e-66 |
| `number_of_arms` | 0.108 | abs_spearman | 28,187 | 1.14e-73 |
| `study_design_info/primary_purpose` | 0.107 | eta | 30,383 | 2.41e-69 |
| `MaskingType-Investigator` | 0.083 | abs_spearman | 30,351 | 8.78e-47 |
| `Biological intervention Number` | 0.081 | abs_spearman | 30,683 | 8.13e-46 |
| `Procedure intervention Number` | 0.080 | abs_spearman | 24,108 | 5.33e-35 |
| `study_design_info/masking_num` | 0.074 | abs_spearman | 30,351 | 1.42e-37 |
| `Other intervention Number` | 0.072 | abs_spearman | 24,108 | 9.10e-29 |
| `study_design_info/intervention_model` | 0.072 | eta | 30,122 | 3.30e-32 |
| `MaskingType-Participant` | 0.071 | abs_spearman | 30,351 | 3.86e-35 |
| `Radiation intervention Number` | 0.069 | abs_spearman | 30,683 | 2.51e-33 |
| `eligibility/healthy_volunteers` | 0.068 | eta | 30,572 | 3.83e-32 |
| `eligibility/maximum_age` | 0.067 | abs_spearman | 13,782 | 8.37e-15 |
| `No Intervention Arm Number` | 0.066 | abs_spearman | 22,770 | 5.39e-23 |
| `condition` | 0.061 | abs_spearman | 30,683 | 1.84e-26 |
| `intervention/intervention_name` | 0.059 | abs_spearman | 30,683 | 1.78e-24 |
| `Drug intervention Number` | 0.056 | abs_spearman | 30,683 | 1.38e-22 |
| `mortality_rate` | 0.056 | abs_spearman | 5,434 | 6.23e-05 |

### `biology_fail`   *(partners: 16)*

| partner | effect | metric | n_valid | p_adj |
|---------|--------|--------|---------|-------|
| `biology_pass` | 1.000 | abs_spearman | 34,427 | <1e-300 |
| `failure_reason` | 1.000 | eta | 20,769 | <1e-300 |
| `approval_outcome` | 0.295 | abs_spearman | 27,420 | <1e-300 |
| `execution_pass` | 0.125 | abs_spearman | 28,367 | 1.59e-98 |
| `execution_fail` | 0.125 | abs_spearman | 28,367 | 1.59e-98 |
| `dropout_rate` | 0.105 | abs_spearman | 13,897 | 5.36e-35 |
| `phase` | 0.098 | eta | 34,427 | 1.21e-71 |
| `sae_rate` | 0.084 | abs_spearman | 5,792 | 3.48e-10 |
| `sae_YN` | 0.083 | abs_spearman | 5,792 | 3.86e-10 |
| `sponsors/lead_sponsor/agency_class` | 0.082 | eta | 23,862 | 1.37e-34 |
| `mortality_rate` | 0.081 | abs_spearman | 5,792 | 1.47e-09 |
| `completion_date` | 0.076 | abs_spearman | 10,917 | 3.34e-15 |
| `mortality_YN` | 0.074 | abs_spearman | 5,792 | 2.79e-08 |
| `oversight_info/is_fda_regulated_drug` | 0.065 | eta | 5,975 | 6.93e-07 |
| `oversight_info/has_dmc` | 0.063 | eta | 23,795 | 3.43e-22 |
| `start_date` | 0.059 | abs_spearman | 10,917 | 1.06e-09 |

### `biology_pass`   *(partners: 16)*

| partner | effect | metric | n_valid | p_adj |
|---------|--------|--------|---------|-------|
| `biology_fail` | 1.000 | abs_spearman | 34,427 | <1e-300 |
| `failure_reason` | 1.000 | eta | 20,769 | <1e-300 |
| `approval_outcome` | 0.295 | abs_spearman | 27,420 | <1e-300 |
| `execution_pass` | 0.125 | abs_spearman | 28,367 | 1.59e-98 |
| `execution_fail` | 0.125 | abs_spearman | 28,367 | 1.59e-98 |
| `dropout_rate` | 0.105 | abs_spearman | 13,897 | 5.36e-35 |
| `phase` | 0.098 | eta | 34,427 | 1.21e-71 |
| `sae_rate` | 0.084 | abs_spearman | 5,792 | 3.48e-10 |
| `sae_YN` | 0.083 | abs_spearman | 5,792 | 3.86e-10 |
| `sponsors/lead_sponsor/agency_class` | 0.082 | eta | 23,862 | 1.37e-34 |
| `mortality_rate` | 0.081 | abs_spearman | 5,792 | 1.47e-09 |
| `completion_date` | 0.076 | abs_spearman | 10,917 | 3.34e-15 |
| `mortality_YN` | 0.074 | abs_spearman | 5,792 | 2.79e-08 |
| `oversight_info/is_fda_regulated_drug` | 0.065 | eta | 5,975 | 6.93e-07 |
| `oversight_info/has_dmc` | 0.063 | eta | 23,795 | 3.43e-22 |
| `start_date` | 0.059 | abs_spearman | 10,917 | 1.06e-09 |

### `brief_title`   *(partners: 19)*

| partner | effect | metric | n_valid | p_adj |
|---------|--------|--------|---------|-------|
| `phase` | 0.139 | eta | 81,786 | <1e-300 |
| `sponsors/lead_sponsor/agency_class` | 0.113 | eta | 71,221 | 1.35e-198 |
| `Experimental Arm Number` | 0.110 | abs_spearman | 78,123 | 6.92e-208 |
| `responsible_party/responsible_party_type` | 0.106 | eta | 67,878 | 4.72e-165 |
| `intervention/intervention_name` | 0.094 | abs_spearman | 81,786 | 3.66e-160 |
| `ipd_info_type-Informed Consent Form (ICF)` | 0.094 | abs_spearman | 2,145 | 2.00e-05 |
| `study_design_info/intervention_model` | 0.085 | eta | 80,897 | 9.18e-126 |
| `patient_data/sharing_ipd` | 0.076 | eta | 13,510 | 2.81e-17 |
| `eligibility/healthy_volunteers` | 0.072 | eta | 81,613 | 4.24e-94 |
| `sae_YN` | 0.070 | abs_spearman | 17,916 | 1.79e-20 |
| `ipd_info_type-Analytic Code` | 0.068 | abs_spearman | 2,297 | 0.0016 |
| `Biological intervention Number` | 0.065 | abs_spearman | 81,786 | 7.45e-77 |
| `ipd_info_type-Statistical Analysis Plan (SAP)` | 0.064 | abs_spearman | 2,297 | 0.0030 |
| `Drug intervention Number` | 0.064 | abs_spearman | 81,786 | 3.89e-74 |
| `Active Comparator Arm Number` | 0.064 | abs_spearman | 69,293 | 1.10e-62 |
| `sae_rate` | 0.060 | abs_spearman | 17,916 | 3.35e-15 |
| `failure_reason` | 0.055 | eta | 20,769 | 4.28e-13 |
| `number_of_arms` | 0.053 | abs_spearman | 78,123 | 6.67e-50 |
| `study_design_info/masking` | 0.053 | eta | 75,043 | 2.62e-34 |

### `completion_date`   *(partners: 28)*

| partner | effect | metric | n_valid | p_adj |
|---------|--------|--------|---------|-------|
| `start_date` | 0.868 | abs_spearman | 42,855 | <1e-300 |
| `approval_outcome` | 0.333 | abs_spearman | 9,263 | 1.97e-237 |
| `patient_data/sharing_ipd` | 0.200 | eta | 9,341 | 6.02e-83 |
| `study_design_info/masking` | 0.182 | eta | 42,635 | 5.40e-295 |
| `ipd_info_type-Clinical Study Report (CSR)` | 0.140 | abs_spearman | 1,728 | 9.17e-09 |
| `execution_fail` | 0.139 | abs_spearman | 20,062 | 1.18e-86 |
| `execution_pass` | 0.139 | abs_spearman | 20,062 | 1.18e-86 |
| `study_design_info/intervention_model` | 0.123 | eta | 42,592 | 2.12e-137 |
| `failure_reason` | 0.115 | eta | 6,904 | 2.71e-19 |
| `enrollment` | 0.113 | abs_spearman | 16,162 | 9.88e-47 |
| `intervention_browse/mesh_term` | 0.112 | abs_spearman | 42,855 | 8.54e-119 |
| `responsible_party/responsible_party_type` | 0.109 | eta | 42,745 | 2.51e-110 |
| `sponsors/lead_sponsor/agency_class` | 0.103 | eta | 42,855 | 8.56e-99 |
| `oversight_info/has_dmc` | 0.099 | eta | 14,181 | 4.37e-32 |
| `ipd_info_type-Analytic Code` | 0.092 | abs_spearman | 1,728 | 0.0002 |
| `smiless` | 0.090 | abs_spearman | 42,855 | 4.38e-77 |
| `oversight_info/is_fda_regulated_drug` | 0.087 | eta | 9,820 | 1.51e-17 |
| `ipd_info_type-Informed Consent Form (ICF)` | 0.086 | abs_spearman | 1,728 | 0.0005 |
| `phase` | 0.081 | eta | 42,855 | 3.53e-60 |
| `ipd_info_type-Study Protocol` | 0.077 | abs_spearman | 1,728 | 0.0019 |
| `biology_pass` | 0.076 | abs_spearman | 10,917 | 3.34e-15 |
| `biology_fail` | 0.076 | abs_spearman | 10,917 | 3.34e-15 |
| `eligibility/healthy_volunteers` | 0.060 | eta | 42,833 | 7.26e-35 |
| `intervention/intervention_name` | 0.054 | abs_spearman | 42,855 | 4.51e-29 |
| `Combination Product intervention Number` | 0.054 | abs_spearman | 42,855 | 3.19e-28 |
| `dropout_YN` | 0.053 | abs_spearman | 16,162 | 2.51e-11 |
| `MaskingType-Care Provider` | 0.052 | abs_spearman | 42,635 | 1.04e-26 |
| `MaskingType-Outcomes Assessor` | 0.051 | abs_spearman | 42,635 | 4.11e-25 |

### `condition`   *(partners: 28)*

| partner | effect | metric | n_valid | p_adj |
|---------|--------|--------|---------|-------|
| `icdcode` | 0.531 | abs_spearman | 81,786 | <1e-300 |
| `condition_browse/mesh_term` | 0.408 | abs_spearman | 81,786 | <1e-300 |
| `sponsors/lead_sponsor/agency_class` | 0.177 | eta | 71,221 | <1e-300 |
| `duration_month` | 0.131 | abs_spearman | 42,855 | 6.31e-162 |
| `duration_year` | 0.131 | abs_spearman | 42,855 | 9.35e-162 |
| `duration_day` | 0.131 | abs_spearman | 42,855 | 9.35e-162 |
| `ipd_info_type-Informed Consent Form (ICF)` | 0.128 | abs_spearman | 2,145 | 4.30e-09 |
| `mortality_rate` | 0.110 | abs_spearman | 17,916 | 1.33e-48 |
| `Other intervention Number` | 0.093 | abs_spearman | 71,221 | 4.79e-135 |
| `ipd_info_type-Statistical Analysis Plan (SAP)` | 0.090 | abs_spearman | 2,297 | 2.42e-05 |
| `mortality_YN` | 0.085 | abs_spearman | 17,916 | 1.05e-29 |
| `study_design_info/primary_purpose` | 0.082 | eta | 80,983 | 8.09e-110 |
| `sae_rate` | 0.081 | abs_spearman | 17,916 | 2.25e-27 |
| `study_design_info/intervention_model` | 0.077 | eta | 80,897 | 2.09e-103 |
| `study_design_info/masking` | 0.076 | eta | 75,043 | 1.01e-80 |
| `Procedure intervention Number` | 0.073 | abs_spearman | 71,221 | 1.50e-83 |
| `intervention_browse/mesh_term` | 0.065 | abs_spearman | 81,786 | 6.27e-77 |
| `ipd_info_type-Clinical Study Report (CSR)` | 0.065 | abs_spearman | 2,145 | 0.0038 |
| `number_of_arms` | 0.062 | abs_spearman | 78,123 | 6.06e-66 |
| `approval_outcome` | 0.061 | abs_spearman | 30,683 | 1.84e-26 |
| `MaskingType-Investigator` | 0.059 | abs_spearman | 81,170 | 8.73e-63 |
| `eligibility/healthy_volunteers` | 0.058 | eta | 81,613 | 6.17e-61 |
| `start_date` | 0.056 | abs_spearman | 42,855 | 2.06e-30 |
| `MaskingType-Participant` | 0.055 | abs_spearman | 81,170 | 2.69e-54 |
| `oversight_info/has_dmc` | 0.054 | eta | 45,926 | 2.44e-30 |
| `phase` | 0.051 | eta | 81,786 | 7.89e-46 |
| `Placebo Comparator Arm Number` | 0.051 | abs_spearman | 78,123 | 6.67e-46 |
| `study_design_info/allocation` | 0.051 | eta | 62,081 | 4.76e-36 |

### `condition_browse/mesh_term`   *(partners: 29)*

| partner | effect | metric | n_valid | p_adj |
|---------|--------|--------|---------|-------|
| `condition` | 0.408 | abs_spearman | 81,786 | <1e-300 |
| `icdcode` | 0.289 | abs_spearman | 81,786 | <1e-300 |
| `duration_year` | 0.276 | abs_spearman | 42,855 | <1e-300 |
| `duration_day` | 0.276 | abs_spearman | 42,855 | <1e-300 |
| `duration_month` | 0.276 | abs_spearman | 42,855 | <1e-300 |
| `eligibility/healthy_volunteers` | 0.233 | eta | 81,613 | <1e-300 |
| `sae_rate` | 0.184 | abs_spearman | 17,916 | 4.88e-135 |
| `sae_YN` | 0.163 | abs_spearman | 17,916 | 1.14e-106 |
| `study_design_info/primary_purpose` | 0.162 | eta | 80,983 | <1e-300 |
| `phase` | 0.149 | eta | 81,786 | <1e-300 |
| `eligibility/maximum_age` | 0.148 | abs_spearman | 42,760 | 3.78e-207 |
| `start_date` | 0.145 | abs_spearman | 42,855 | 3.45e-200 |
| `mortality_rate` | 0.134 | abs_spearman | 17,916 | 1.05e-71 |
| `study_design_info/intervention_model` | 0.134 | eta | 80,897 | <1e-300 |
| `sponsors/lead_sponsor/agency_class` | 0.129 | eta | 71,221 | 1.08e-258 |
| `mortality_YN` | 0.128 | abs_spearman | 17,916 | 2.99e-65 |
| `eligibility/gender` | 0.123 | eta | 71,221 | 5.95e-235 |
| `ipd_info_type-Informed Consent Form (ICF)` | 0.107 | abs_spearman | 2,145 | 1.21e-06 |
| `location/facility/address/city` | 0.098 | abs_spearman | 81,786 | 2.04e-174 |
| `dropout_YN` | 0.084 | abs_spearman | 38,302 | 1.02e-59 |
| `dropout_rate` | 0.083 | abs_spearman | 38,302 | 6.78e-59 |
| `number_of_arms` | 0.079 | abs_spearman | 78,123 | 1.06e-107 |
| `oversight_info/has_dmc` | 0.071 | eta | 45,926 | 1.33e-52 |
| `study_design_info/masking` | 0.063 | eta | 75,043 | 2.24e-52 |
| `execution_pass` | 0.062 | abs_spearman | 52,772 | 4.05e-45 |
| `execution_fail` | 0.062 | abs_spearman | 52,772 | 4.05e-45 |
| `oversight_info/is_fda_regulated_drug` | 0.059 | eta | 13,761 | 7.46e-12 |
| `Experimental Arm Number` | 0.055 | abs_spearman | 78,123 | 5.45e-52 |
| `intervention_browse/mesh_term` | 0.054 | abs_spearman | 81,786 | 7.73e-54 |

### `dropout_YN`   *(partners: 41)*

| partner | effect | metric | n_valid | p_adj |
|---------|--------|--------|---------|-------|
| `execution_fail` | 0.940 | abs_spearman | 38,302 | <1e-300 |
| `execution_pass` | 0.940 | abs_spearman | 38,302 | <1e-300 |
| `dropout_rate` | 0.715 | abs_spearman | 38,302 | <1e-300 |
| `enrollment` | 0.364 | abs_spearman | 38,301 | <1e-300 |
| `sae_YN` | 0.290 | abs_spearman | 17,873 | <1e-300 |
| `location/facility/address/city` | 0.289 | abs_spearman | 38,302 | <1e-300 |
| `phase` | 0.252 | eta | 38,302 | <1e-300 |
| `study_design_info/intervention_model` | 0.240 | eta | 38,137 | <1e-300 |
| `sponsors/lead_sponsor/agency_class` | 0.213 | eta | 38,302 | <1e-300 |
| `sae_rate` | 0.191 | abs_spearman | 17,873 | 1.05e-145 |
| `patient_data/sharing_ipd` | 0.177 | eta | 12,952 | 5.55e-90 |
| `study_design_info/primary_purpose` | 0.167 | eta | 37,812 | 2.88e-223 |
| `eligibility/healthy_volunteers` | 0.166 | eta | 38,268 | 2.33e-232 |
| `ipd_info_type-Informed Consent Form (ICF)` | 0.156 | abs_spearman | 2,105 | 1.44e-12 |
| `approval_outcome` | 0.154 | abs_spearman | 14,131 | 3.86e-75 |
| `study_design_info/masking` | 0.151 | eta | 38,218 | 3.64e-175 |
| `mortality_YN` | 0.150 | abs_spearman | 17,873 | 2.56e-90 |
| `responsible_party/responsible_party_type` | 0.145 | eta | 36,674 | 2.75e-168 |
| `MaskingType-Investigator` | 0.137 | abs_spearman | 38,218 | 1.93e-158 |
| `duration_year` | 0.131 | abs_spearman | 16,162 | 1.97e-62 |
| `duration_day` | 0.131 | abs_spearman | 16,162 | 1.97e-62 |
| `duration_month` | 0.131 | abs_spearman | 16,162 | 4.45e-62 |
| `study_design_info/masking_num` | 0.129 | abs_spearman | 38,218 | 8.64e-141 |
| `failure_reason` | 0.127 | eta | 6,299 | 8.18e-22 |
| `MaskingType-Participant` | 0.121 | abs_spearman | 38,218 | 1.50e-124 |
| `Placebo Comparator Arm Number` | 0.114 | abs_spearman | 38,016 | 7.11e-109 |
| `mortality_rate` | 0.111 | abs_spearman | 17,873 | 5.60e-50 |
| `start_date` | 0.099 | abs_spearman | 16,162 | 8.87e-36 |
| `MaskingType-Care Provider` | 0.085 | abs_spearman | 38,218 | 2.04e-61 |
| `MaskingType-Outcomes Assessor` | 0.084 | abs_spearman | 38,218 | 8.26e-61 |
| `condition_browse/mesh_term` | 0.084 | abs_spearman | 38,302 | 1.02e-59 |
| `number_of_arms` | 0.083 | abs_spearman | 38,016 | 4.01e-58 |
| `ipd_info_type-Statistical Analysis Plan (SAP)` | 0.082 | abs_spearman | 2,105 | 0.0003 |
| `study_design_info/allocation` | 0.076 | eta | 29,014 | 2.55e-38 |
| `ipd_info_type-Study Protocol` | 0.066 | abs_spearman | 2,105 | 0.0035 |
| `eligibility/gender` | 0.062 | eta | 38,302 | 1.14e-32 |
| `intervention/intervention_name` | 0.062 | abs_spearman | 38,302 | 9.88e-34 |
| `Procedure intervention Number` | 0.053 | abs_spearman | 38,302 | 3.02e-25 |
| `completion_date` | 0.053 | abs_spearman | 16,162 | 2.51e-11 |
| `eligibility/maximum_age` | 0.053 | abs_spearman | 18,312 | 2.12e-12 |
| `Drug intervention Number` | 0.052 | abs_spearman | 38,302 | 4.48e-24 |

### `dropout_rate`   *(partners: 35)*

| partner | effect | metric | n_valid | p_adj |
|---------|--------|--------|---------|-------|
| `dropout_YN` | 0.715 | abs_spearman | 38,302 | <1e-300 |
| `execution_pass` | 0.671 | abs_spearman | 38,302 | <1e-300 |
| `execution_fail` | 0.671 | abs_spearman | 38,302 | <1e-300 |
| `sae_rate` | 0.342 | abs_spearman | 17,873 | <1e-300 |
| `sae_YN` | 0.291 | abs_spearman | 17,873 | <1e-300 |
| `mortality_rate` | 0.275 | abs_spearman | 17,873 | <1e-300 |
| `location/facility/address/city` | 0.268 | abs_spearman | 38,302 | <1e-300 |
| `mortality_YN` | 0.266 | abs_spearman | 17,873 | 8.14e-287 |
| `duration_day` | 0.252 | abs_spearman | 16,162 | 4.24e-232 |
| `duration_year` | 0.252 | abs_spearman | 16,162 | 4.24e-232 |
| `duration_month` | 0.252 | abs_spearman | 16,162 | 1.53e-231 |
| `eligibility/healthy_volunteers` | 0.203 | eta | 38,268 | <1e-300 |
| `ipd_info_type-Informed Consent Form (ICF)` | 0.178 | abs_spearman | 2,105 | 4.46e-16 |
| `study_design_info/intervention_model` | 0.170 | eta | 38,137 | 1.32e-240 |
| `study_design_info/primary_purpose` | 0.164 | eta | 37,812 | 3.02e-216 |
| `study_design_info/masking` | 0.156 | eta | 38,218 | 5.23e-189 |
| `approval_outcome` | 0.143 | abs_spearman | 14,131 | 7.36e-65 |
| `enrollment` | 0.143 | abs_spearman | 38,301 | 2.90e-172 |
| `start_date` | 0.131 | abs_spearman | 16,162 | 1.44e-62 |
| `phase` | 0.131 | eta | 38,302 | 1.62e-141 |
| `study_design_info/allocation` | 0.120 | eta | 29,014 | 1.67e-93 |
| `sponsors/lead_sponsor/agency_class` | 0.115 | eta | 38,302 | 2.34e-109 |
| `failure_reason` | 0.111 | eta | 6,299 | 1.42e-16 |
| `eligibility/maximum_age` | 0.110 | abs_spearman | 18,312 | 1.51e-49 |
| `biology_fail` | 0.105 | abs_spearman | 13,897 | 5.36e-35 |
| `biology_pass` | 0.105 | abs_spearman | 13,897 | 5.36e-35 |
| `patient_data/sharing_ipd` | 0.102 | eta | 12,952 | 1.36e-29 |
| `responsible_party/responsible_party_type` | 0.094 | eta | 36,674 | 3.18e-70 |
| `oversight_info/is_fda_regulated_drug` | 0.090 | eta | 11,191 | 4.12e-21 |
| `condition_browse/mesh_term` | 0.083 | abs_spearman | 38,302 | 6.78e-59 |
| `oversight_info/has_dmc` | 0.078 | eta | 32,996 | 1.14e-45 |
| `ipd_info_type-Statistical Analysis Plan (SAP)` | 0.075 | abs_spearman | 2,105 | 0.0009 |
| `Active Comparator Arm Number` | 0.058 | abs_spearman | 38,016 | 1.79e-29 |
| `has_expanded_access` | 0.057 | eta | 37,901 | 2.51e-28 |
| `smiless` | 0.051 | abs_spearman | 38,302 | 4.58e-23 |

### `duration_day`   *(partners: 40)*

| partner | effect | metric | n_valid | p_adj |
|---------|--------|--------|---------|-------|
| `duration_year` | 1.000 | abs_spearman | 42,855 | <1e-300 |
| `duration_month` | 1.000 | abs_spearman | 42,855 | <1e-300 |
| `sae_rate` | 0.430 | abs_spearman | 13,278 | <1e-300 |
| `start_date` | 0.425 | abs_spearman | 42,855 | <1e-300 |
| `mortality_rate` | 0.377 | abs_spearman | 13,278 | <1e-300 |
| `mortality_YN` | 0.359 | abs_spearman | 13,278 | <1e-300 |
| `eligibility/healthy_volunteers` | 0.351 | eta | 42,833 | <1e-300 |
| `sae_YN` | 0.313 | abs_spearman | 13,278 | 9.64e-298 |
| `sponsors/lead_sponsor/agency_class` | 0.282 | eta | 42,855 | <1e-300 |
| `condition_browse/mesh_term` | 0.276 | abs_spearman | 42,855 | <1e-300 |
| `location/facility/address/city` | 0.256 | abs_spearman | 42,855 | <1e-300 |
| `dropout_rate` | 0.252 | abs_spearman | 16,162 | 4.24e-232 |
| `study_design_info/intervention_model` | 0.249 | eta | 42,592 | <1e-300 |
| `oversight_info/has_dmc` | 0.228 | eta | 14,181 | 2.91e-166 |
| `phase` | 0.223 | eta | 42,855 | <1e-300 |
| `eligibility/maximum_age` | 0.202 | abs_spearman | 24,161 | 2.53e-220 |
| `study_design_info/primary_purpose` | 0.195 | eta | 42,836 | <1e-300 |
| `number_of_arms` | 0.161 | abs_spearman | 42,293 | 3.03e-242 |
| `study_design_info/masking` | 0.156 | eta | 42,635 | 2.39e-210 |
| `execution_pass` | 0.141 | abs_spearman | 20,062 | 4.22e-89 |
| `execution_fail` | 0.141 | abs_spearman | 20,062 | 4.22e-89 |
| `intervention_browse/mesh_term` | 0.133 | abs_spearman | 42,855 | 3.99e-168 |
| `dropout_YN` | 0.131 | abs_spearman | 16,162 | 1.97e-62 |
| `Radiation intervention Number` | 0.131 | abs_spearman | 42,855 | 2.21e-162 |
| `condition` | 0.131 | abs_spearman | 42,855 | 9.35e-162 |
| `Experimental Arm Number` | 0.120 | abs_spearman | 42,293 | 1.11e-133 |
| `enrollment` | 0.111 | abs_spearman | 16,162 | 1.01e-44 |
| `Procedure intervention Number` | 0.104 | abs_spearman | 42,855 | 2.14e-102 |
| `eligibility/gender` | 0.104 | eta | 42,855 | 7.78e-101 |
| `icdcode` | 0.103 | abs_spearman | 42,855 | 3.30e-101 |
| `MaskingType-Participant` | 0.102 | abs_spearman | 42,635 | 9.19e-98 |
| `failure_reason` | 0.096 | eta | 6,904 | 1.67e-13 |
| `study_design_info/allocation` | 0.092 | eta | 32,550 | 5.05e-62 |
| `smiless` | 0.090 | abs_spearman | 42,855 | 6.62e-78 |
| `oversight_info/is_fda_regulated_drug` | 0.090 | eta | 9,820 | 7.07e-19 |
| `study_design_info/masking_num` | 0.086 | abs_spearman | 42,635 | 3.22e-70 |
| `MaskingType-Investigator` | 0.084 | abs_spearman | 42,635 | 3.17e-67 |
| `eligibility/minimum_age` | 0.077 | abs_spearman | 41,982 | 7.81e-56 |
| `responsible_party/responsible_party_type` | 0.075 | eta | 42,745 | 2.51e-52 |
| `Other intervention Number` | 0.057 | abs_spearman | 42,855 | 4.15e-32 |

### `duration_month`   *(partners: 40)*

| partner | effect | metric | n_valid | p_adj |
|---------|--------|--------|---------|-------|
| `duration_day` | 1.000 | abs_spearman | 42,855 | <1e-300 |
| `duration_year` | 1.000 | abs_spearman | 42,855 | <1e-300 |
| `sae_rate` | 0.429 | abs_spearman | 13,278 | <1e-300 |
| `start_date` | 0.426 | abs_spearman | 42,855 | <1e-300 |
| `mortality_rate` | 0.377 | abs_spearman | 13,278 | <1e-300 |
| `mortality_YN` | 0.359 | abs_spearman | 13,278 | <1e-300 |
| `eligibility/healthy_volunteers` | 0.351 | eta | 42,833 | <1e-300 |
| `sae_YN` | 0.312 | abs_spearman | 13,278 | 3.86e-297 |
| `sponsors/lead_sponsor/agency_class` | 0.282 | eta | 42,855 | <1e-300 |
| `condition_browse/mesh_term` | 0.276 | abs_spearman | 42,855 | <1e-300 |
| `location/facility/address/city` | 0.255 | abs_spearman | 42,855 | <1e-300 |
| `dropout_rate` | 0.252 | abs_spearman | 16,162 | 1.53e-231 |
| `study_design_info/intervention_model` | 0.249 | eta | 42,592 | <1e-300 |
| `oversight_info/has_dmc` | 0.228 | eta | 14,181 | 3.84e-166 |
| `phase` | 0.224 | eta | 42,855 | <1e-300 |
| `eligibility/maximum_age` | 0.202 | abs_spearman | 24,161 | 1.16e-219 |
| `study_design_info/primary_purpose` | 0.195 | eta | 42,836 | <1e-300 |
| `number_of_arms` | 0.161 | abs_spearman | 42,293 | 1.91e-243 |
| `study_design_info/masking` | 0.155 | eta | 42,635 | 1.03e-209 |
| `execution_fail` | 0.141 | abs_spearman | 20,062 | 8.10e-89 |
| `execution_pass` | 0.141 | abs_spearman | 20,062 | 8.10e-89 |
| `intervention_browse/mesh_term` | 0.134 | abs_spearman | 42,855 | 2.97e-169 |
| `Radiation intervention Number` | 0.131 | abs_spearman | 42,855 | 1.81e-162 |
| `dropout_YN` | 0.131 | abs_spearman | 16,162 | 4.45e-62 |
| `condition` | 0.131 | abs_spearman | 42,855 | 6.31e-162 |
| `Experimental Arm Number` | 0.120 | abs_spearman | 42,293 | 2.25e-135 |
| `enrollment` | 0.110 | abs_spearman | 16,162 | 1.36e-44 |
| `Procedure intervention Number` | 0.104 | abs_spearman | 42,855 | 5.71e-103 |
| `eligibility/gender` | 0.104 | eta | 42,855 | 4.05e-101 |
| `icdcode` | 0.103 | abs_spearman | 42,855 | 1.41e-100 |
| `MaskingType-Participant` | 0.102 | abs_spearman | 42,635 | 3.67e-98 |
| `failure_reason` | 0.096 | eta | 6,904 | 1.81e-13 |
| `study_design_info/allocation` | 0.092 | eta | 32,550 | 7.18e-62 |
| `smiless` | 0.091 | abs_spearman | 42,855 | 2.30e-78 |
| `oversight_info/is_fda_regulated_drug` | 0.090 | eta | 9,820 | 7.68e-19 |
| `study_design_info/masking_num` | 0.086 | abs_spearman | 42,635 | 1.50e-70 |
| `MaskingType-Investigator` | 0.085 | abs_spearman | 42,635 | 6.87e-68 |
| `eligibility/minimum_age` | 0.077 | abs_spearman | 41,982 | 8.82e-56 |
| `responsible_party/responsible_party_type` | 0.075 | eta | 42,745 | 4.72e-53 |
| `Other intervention Number` | 0.057 | abs_spearman | 42,855 | 4.05e-32 |

### `duration_year`   *(partners: 40)*

| partner | effect | metric | n_valid | p_adj |
|---------|--------|--------|---------|-------|
| `duration_day` | 1.000 | abs_spearman | 42,855 | <1e-300 |
| `duration_month` | 1.000 | abs_spearman | 42,855 | <1e-300 |
| `sae_rate` | 0.430 | abs_spearman | 13,278 | <1e-300 |
| `start_date` | 0.425 | abs_spearman | 42,855 | <1e-300 |
| `mortality_rate` | 0.377 | abs_spearman | 13,278 | <1e-300 |
| `mortality_YN` | 0.359 | abs_spearman | 13,278 | <1e-300 |
| `eligibility/healthy_volunteers` | 0.351 | eta | 42,833 | <1e-300 |
| `sae_YN` | 0.313 | abs_spearman | 13,278 | 9.64e-298 |
| `sponsors/lead_sponsor/agency_class` | 0.282 | eta | 42,855 | <1e-300 |
| `condition_browse/mesh_term` | 0.276 | abs_spearman | 42,855 | <1e-300 |
| `location/facility/address/city` | 0.256 | abs_spearman | 42,855 | <1e-300 |
| `dropout_rate` | 0.252 | abs_spearman | 16,162 | 4.24e-232 |
| `study_design_info/intervention_model` | 0.249 | eta | 42,592 | <1e-300 |
| `oversight_info/has_dmc` | 0.228 | eta | 14,181 | 2.91e-166 |
| `phase` | 0.223 | eta | 42,855 | <1e-300 |
| `eligibility/maximum_age` | 0.202 | abs_spearman | 24,161 | 2.53e-220 |
| `study_design_info/primary_purpose` | 0.195 | eta | 42,836 | <1e-300 |
| `number_of_arms` | 0.161 | abs_spearman | 42,293 | 3.03e-242 |
| `study_design_info/masking` | 0.156 | eta | 42,635 | 2.39e-210 |
| `execution_fail` | 0.141 | abs_spearman | 20,062 | 4.22e-89 |
| `execution_pass` | 0.141 | abs_spearman | 20,062 | 4.22e-89 |
| `intervention_browse/mesh_term` | 0.133 | abs_spearman | 42,855 | 3.99e-168 |
| `dropout_YN` | 0.131 | abs_spearman | 16,162 | 1.97e-62 |
| `Radiation intervention Number` | 0.131 | abs_spearman | 42,855 | 2.21e-162 |
| `condition` | 0.131 | abs_spearman | 42,855 | 9.35e-162 |
| `Experimental Arm Number` | 0.120 | abs_spearman | 42,293 | 1.11e-133 |
| `enrollment` | 0.111 | abs_spearman | 16,162 | 1.01e-44 |
| `Procedure intervention Number` | 0.104 | abs_spearman | 42,855 | 2.14e-102 |
| `eligibility/gender` | 0.104 | eta | 42,855 | 7.78e-101 |
| `icdcode` | 0.103 | abs_spearman | 42,855 | 3.30e-101 |
| `MaskingType-Participant` | 0.102 | abs_spearman | 42,635 | 9.19e-98 |
| `failure_reason` | 0.096 | eta | 6,904 | 1.67e-13 |
| `study_design_info/allocation` | 0.092 | eta | 32,550 | 5.05e-62 |
| `smiless` | 0.090 | abs_spearman | 42,855 | 6.62e-78 |
| `oversight_info/is_fda_regulated_drug` | 0.090 | eta | 9,820 | 7.07e-19 |
| `study_design_info/masking_num` | 0.086 | abs_spearman | 42,635 | 3.22e-70 |
| `MaskingType-Investigator` | 0.084 | abs_spearman | 42,635 | 3.17e-67 |
| `eligibility/minimum_age` | 0.077 | abs_spearman | 41,982 | 7.81e-56 |
| `responsible_party/responsible_party_type` | 0.075 | eta | 42,745 | 2.51e-52 |
| `Other intervention Number` | 0.057 | abs_spearman | 42,855 | 4.15e-32 |

### `eligibility/gender`   *(partners: 24)*

| partner | effect | metric | n_valid | p_adj |
|---------|--------|--------|---------|-------|
| `eligibility/healthy_volunteers` | 0.170 | cramers_v | 71,109 | <1e-300 |
| `phase` | 0.128 | cramers_v | 71,221 | <1e-300 |
| `condition_browse/mesh_term` | 0.123 | eta | 71,221 | 5.95e-235 |
| `duration_month` | 0.104 | eta | 42,855 | 4.05e-101 |
| `duration_day` | 0.104 | eta | 42,855 | 7.78e-101 |
| `duration_year` | 0.104 | eta | 42,855 | 7.78e-101 |
| `study_design_info/primary_purpose` | 0.097 | cramers_v | 70,604 | 1.97e-268 |
| `sae_YN` | 0.088 | eta | 17,916 | 9.67e-31 |
| `study_design_info/intervention_model` | 0.087 | cramers_v | 70,749 | 9.49e-224 |
| `sponsors/lead_sponsor/agency_class` | 0.084 | cramers_v | 71,221 | 4.03e-214 |
| `sae_rate` | 0.078 | eta | 17,916 | 8.20e-24 |
| `mortality_YN` | 0.072 | eta | 17,916 | 2.09e-20 |
| `eligibility/maximum_age` | 0.068 | eta | 37,908 | 1.30e-38 |
| `Experimental Arm Number` | 0.067 | eta | 69,293 | 6.49e-68 |
| `oversight_info/is_fda_regulated_drug` | 0.065 | cramers_v | 11,339 | 1.07e-10 |
| `dropout_YN` | 0.062 | eta | 38,302 | 1.14e-32 |
| `intervention_browse/mesh_term` | 0.061 | eta | 71,221 | 5.48e-57 |
| `eligibility/minimum_age` | 0.060 | eta | 69,489 | 9.73e-54 |
| `responsible_party/responsible_party_type` | 0.059 | cramers_v | 67,878 | 3.70e-99 |
| `execution_fail` | 0.058 | eta | 42,207 | 6.10e-31 |
| `execution_pass` | 0.058 | eta | 42,207 | 6.10e-31 |
| `study_design_info/masking` | 0.057 | cramers_v | 64,727 | 1.81e-67 |
| `study_design_info/masking_num` | 0.055 | eta | 70,854 | 5.16e-47 |
| `MaskingType-Outcomes Assessor` | 0.052 | eta | 70,854 | 3.02e-42 |

### `eligibility/healthy_volunteers`   *(partners: 41)*

| partner | effect | metric | n_valid | p_adj |
|---------|--------|--------|---------|-------|
| `study_design_info/primary_purpose` | 0.455 | cramers_v | 80,843 | <1e-300 |
| `phase` | 0.411 | cramers_v | 81,613 | <1e-300 |
| `duration_month` | 0.351 | eta | 42,833 | <1e-300 |
| `duration_day` | 0.351 | eta | 42,833 | <1e-300 |
| `duration_year` | 0.351 | eta | 42,833 | <1e-300 |
| `ipd_info_type-Informed Consent Form (ICF)` | 0.332 | eta | 2,145 | 5.89e-56 |
| `sae_YN` | 0.309 | eta | 17,914 | <1e-300 |
| `study_design_info/intervention_model` | 0.293 | cramers_v | 80,743 | <1e-300 |
| `sae_rate` | 0.261 | eta | 17,914 | 4.72e-275 |
| `mortality_YN` | 0.256 | eta | 17,914 | 4.73e-265 |
| `condition_browse/mesh_term` | 0.233 | eta | 81,613 | <1e-300 |
| `eligibility/maximum_age` | 0.224 | eta | 42,674 | <1e-300 |
| `number_of_arms` | 0.210 | eta | 78,060 | <1e-300 |
| `dropout_rate` | 0.203 | eta | 38,268 | <1e-300 |
| `start_date` | 0.198 | eta | 42,833 | <1e-300 |
| `mortality_rate` | 0.184 | eta | 17,914 | 1.06e-134 |
| `Experimental Arm Number` | 0.177 | eta | 78,060 | <1e-300 |
| `Biological intervention Number` | 0.172 | eta | 81,613 | <1e-300 |
| `eligibility/gender` | 0.170 | cramers_v | 71,109 | <1e-300 |
| `dropout_YN` | 0.166 | eta | 38,268 | 2.33e-232 |
| `location/facility/address/city` | 0.122 | eta | 81,613 | 3.93e-268 |
| `failure_reason` | 0.118 | cramers_v | 20,706 | 2.44e-61 |
| `execution_pass` | 0.116 | eta | 52,677 | 2.35e-156 |
| `execution_fail` | 0.116 | eta | 52,677 | 2.35e-156 |
| `intervention_browse/mesh_term` | 0.115 | eta | 81,613 | 3.28e-238 |
| `oversight_info/has_dmc` | 0.114 | cramers_v | 45,906 | 1.65e-130 |
| `sponsors/lead_sponsor/agency_class` | 0.112 | cramers_v | 71,109 | 9.56e-191 |
| `study_design_info/masking` | 0.108 | cramers_v | 74,940 | 1.00e-175 |
| `oversight_info/is_fda_regulated_drug` | 0.105 | cramers_v | 13,761 | 1.27e-34 |
| `ipd_info_type-Clinical Study Report (CSR)` | 0.097 | eta | 2,145 | 1.12e-05 |
| `smiless` | 0.092 | eta | 81,613 | 2.53e-151 |
| `icdcode` | 0.074 | eta | 81,613 | 1.49e-97 |
| `brief_title` | 0.072 | eta | 81,613 | 4.24e-94 |
| `intervention/intervention_type` | 0.070 | eta | 81,613 | 9.88e-88 |
| `approval_outcome` | 0.068 | eta | 30,572 | 3.83e-32 |
| `Radiation intervention Number` | 0.065 | eta | 81,613 | 1.42e-76 |
| `completion_date` | 0.060 | eta | 42,833 | 7.26e-35 |
| `Drug intervention Number` | 0.059 | eta | 81,613 | 1.01e-62 |
| `MaskingType-Participant` | 0.058 | eta | 81,014 | 1.34e-60 |
| `condition` | 0.058 | eta | 81,613 | 6.17e-61 |
| `Procedure intervention Number` | 0.051 | eta | 71,109 | 5.48e-41 |

### `eligibility/maximum_age`   *(partners: 31)*

| partner | effect | metric | n_valid | p_adj |
|---------|--------|--------|---------|-------|
| `eligibility/minimum_age` | 0.465 | abs_spearman | 41,854 | <1e-300 |
| `ipd_info_type-Informed Consent Form (ICF)` | 0.297 | abs_spearman | 1,034 | 4.63e-22 |
| `ipd_info_type-Clinical Study Report (CSR)` | 0.280 | abs_spearman | 1,034 | 1.09e-19 |
| `mortality_rate` | 0.253 | abs_spearman | 8,723 | 1.73e-126 |
| `mortality_YN` | 0.242 | abs_spearman | 8,723 | 6.80e-116 |
| `study_design_info/primary_purpose` | 0.233 | eta | 42,342 | <1e-300 |
| `eligibility/healthy_volunteers` | 0.224 | eta | 42,674 | <1e-300 |
| `duration_day` | 0.202 | abs_spearman | 24,161 | 2.53e-220 |
| `duration_year` | 0.202 | abs_spearman | 24,161 | 2.53e-220 |
| `duration_month` | 0.202 | abs_spearman | 24,161 | 1.16e-219 |
| `sae_rate` | 0.178 | abs_spearman | 8,723 | 2.08e-62 |
| `condition_browse/mesh_term` | 0.148 | abs_spearman | 42,760 | 3.78e-207 |
| `Biological intervention Number` | 0.136 | abs_spearman | 42,760 | 1.72e-174 |
| `patient_data/sharing_ipd` | 0.129 | eta | 6,857 | 2.23e-25 |
| `phase` | 0.124 | eta | 42,760 | 2.19e-141 |
| `sae_YN` | 0.123 | abs_spearman | 8,723 | 1.45e-30 |
| `icdcode` | 0.113 | abs_spearman | 42,760 | 1.43e-120 |
| `dropout_rate` | 0.110 | abs_spearman | 18,312 | 1.51e-49 |
| `study_design_info/masking` | 0.072 | eta | 39,233 | 9.51e-34 |
| `Drug intervention Number` | 0.070 | abs_spearman | 42,760 | 6.54e-47 |
| `eligibility/gender` | 0.068 | eta | 37,908 | 1.30e-38 |
| `approval_outcome` | 0.067 | abs_spearman | 13,782 | 8.37e-15 |
| `location/facility/address/city` | 0.062 | abs_spearman | 42,760 | 8.54e-38 |
| `number_of_arms` | 0.061 | abs_spearman | 41,114 | 7.46e-35 |
| `Radiation intervention Number` | 0.060 | abs_spearman | 42,760 | 6.21e-35 |
| `Experimental Arm Number` | 0.054 | abs_spearman | 41,114 | 8.58e-28 |
| `intervention/intervention_type` | 0.054 | abs_spearman | 42,760 | 8.40e-29 |
| `start_date` | 0.053 | abs_spearman | 24,161 | 1.97e-16 |
| `dropout_YN` | 0.053 | abs_spearman | 18,312 | 2.12e-12 |
| `Procedure intervention Number` | 0.052 | abs_spearman | 37,908 | 2.64e-23 |
| `study_design_info/intervention_model` | 0.051 | eta | 42,360 | 2.33e-22 |

### `eligibility/minimum_age`   *(partners: 16)*

| partner | effect | metric | n_valid | p_adj |
|---------|--------|--------|---------|-------|
| `eligibility/maximum_age` | 0.465 | abs_spearman | 41,854 | <1e-300 |
| `Biological intervention Number` | 0.099 | abs_spearman | 79,650 | 1.75e-172 |
| `study_design_info/masking` | 0.095 | eta | 73,073 | 9.06e-130 |
| `ipd_info_type-Informed Consent Form (ICF)` | 0.082 | abs_spearman | 2,103 | 0.0003 |
| `duration_year` | 0.077 | abs_spearman | 41,982 | 7.81e-56 |
| `duration_day` | 0.077 | abs_spearman | 41,982 | 7.81e-56 |
| `duration_month` | 0.077 | abs_spearman | 41,982 | 8.82e-56 |
| `MaskingType-Participant` | 0.064 | abs_spearman | 79,096 | 1.15e-71 |
| `study_design_info/intervention_model` | 0.061 | eta | 78,839 | 6.71e-62 |
| `eligibility/gender` | 0.060 | eta | 69,489 | 9.73e-54 |
| `Drug intervention Number` | 0.059 | abs_spearman | 79,650 | 2.21e-62 |
| `mortality_YN` | 0.058 | abs_spearman | 17,440 | 3.84e-14 |
| `study_design_info/masking_num` | 0.055 | abs_spearman | 79,096 | 2.61e-54 |
| `Placebo Comparator Arm Number` | 0.054 | abs_spearman | 76,141 | 1.24e-50 |
| `study_design_info/allocation` | 0.054 | eta | 60,725 | 1.19e-40 |
| `MaskingType-Investigator` | 0.052 | abs_spearman | 79,096 | 1.72e-47 |

### `enrollment`   *(partners: 38)*

| partner | effect | metric | n_valid | p_adj |
|---------|--------|--------|---------|-------|
| `location/facility/address/city` | 0.456 | abs_spearman | 44,446 | <1e-300 |
| `dropout_YN` | 0.364 | abs_spearman | 38,301 | <1e-300 |
| `sae_YN` | 0.355 | abs_spearman | 17,881 | <1e-300 |
| `number_of_arms` | 0.350 | abs_spearman | 43,117 | <1e-300 |
| `execution_pass` | 0.308 | abs_spearman | 38,306 | <1e-300 |
| `execution_fail` | 0.308 | abs_spearman | 38,306 | <1e-300 |
| `study_design_info/masking_num` | 0.303 | abs_spearman | 44,289 | <1e-300 |
| `approval_outcome` | 0.288 | abs_spearman | 20,273 | <1e-300 |
| `MaskingType-Investigator` | 0.287 | abs_spearman | 44,289 | <1e-300 |
| `MaskingType-Participant` | 0.279 | abs_spearman | 44,289 | <1e-300 |
| `mortality_YN` | 0.249 | abs_spearman | 17,881 | 3.47e-250 |
| `Active Comparator Arm Number` | 0.222 | abs_spearman | 43,117 | <1e-300 |
| `intervention/intervention_name` | 0.212 | abs_spearman | 44,446 | <1e-300 |
| `Placebo Comparator Arm Number` | 0.202 | abs_spearman | 43,117 | <1e-300 |
| `MaskingType-Outcomes Assessor` | 0.196 | abs_spearman | 44,289 | <1e-300 |
| `MaskingType-Care Provider` | 0.187 | abs_spearman | 44,289 | <1e-300 |
| `ipd_info_type-Clinical Study Report (CSR)` | 0.159 | abs_spearman | 2,145 | 2.83e-13 |
| `ipd_info_type-Statistical Analysis Plan (SAP)` | 0.154 | abs_spearman | 2,145 | 1.61e-12 |
| `mortality_rate` | 0.152 | abs_spearman | 17,881 | 2.42e-92 |
| `start_date` | 0.151 | abs_spearman | 16,162 | 1.84e-82 |
| `Drug intervention Number` | 0.145 | abs_spearman | 44,446 | 1.66e-205 |
| `dropout_rate` | 0.143 | abs_spearman | 38,301 | 2.90e-172 |
| `failure_reason` | 0.134 | eta | 6,304 | 4.71e-24 |
| `ipd_info_type-Informed Consent Form (ICF)` | 0.127 | abs_spearman | 2,145 | 6.26e-09 |
| `sae_rate` | 0.123 | abs_spearman | 17,881 | 1.44e-60 |
| `completion_date` | 0.113 | abs_spearman | 16,162 | 9.88e-47 |
| `Experimental Arm Number` | 0.111 | abs_spearman | 43,117 | 1.59e-118 |
| `phase` | 0.111 | eta | 44,446 | 1.01e-117 |
| `duration_day` | 0.111 | abs_spearman | 16,162 | 1.01e-44 |
| `duration_year` | 0.111 | abs_spearman | 16,162 | 1.01e-44 |
| `duration_month` | 0.110 | abs_spearman | 16,162 | 1.36e-44 |
| `study_design_info/primary_purpose` | 0.107 | eta | 43,857 | 1.37e-102 |
| `study_design_info/intervention_model` | 0.080 | eta | 44,158 | 2.27e-59 |
| `Biological intervention Number` | 0.072 | abs_spearman | 44,446 | 2.05e-51 |
| `Procedure intervention Number` | 0.067 | abs_spearman | 44,446 | 6.83e-45 |
| `study_design_info/masking` | 0.059 | eta | 38,225 | 1.88e-19 |
| `Radiation intervention Number` | 0.057 | abs_spearman | 44,446 | 1.35e-32 |
| `intervention_browse/mesh_term` | 0.052 | abs_spearman | 44,446 | 3.43e-27 |

### `execution_fail`   *(partners: 44)*

| partner | effect | metric | n_valid | p_adj |
|---------|--------|--------|---------|-------|
| `execution_pass` | 1.000 | abs_spearman | 52,772 | <1e-300 |
| `dropout_YN` | 0.940 | abs_spearman | 38,302 | <1e-300 |
| `failure_reason` | 0.755 | eta | 20,769 | <1e-300 |
| `dropout_rate` | 0.671 | abs_spearman | 38,302 | <1e-300 |
| `location/facility/address/city` | 0.393 | abs_spearman | 52,772 | <1e-300 |
| `intervention/intervention_type` | 0.377 | abs_spearman | 52,772 | <1e-300 |
| `enrollment` | 0.308 | abs_spearman | 38,306 | <1e-300 |
| `sae_YN` | 0.269 | abs_spearman | 17,903 | 3.81e-293 |
| `phase` | 0.261 | eta | 52,772 | <1e-300 |
| `approval_outcome` | 0.226 | abs_spearman | 23,059 | 4.06e-264 |
| `sae_rate` | 0.185 | abs_spearman | 17,903 | 3.31e-136 |
| `start_date` | 0.177 | abs_spearman | 20,062 | 1.67e-140 |
| `study_design_info/intervention_model` | 0.176 | eta | 52,169 | <1e-300 |
| `oversight_info/is_fda_regulated_drug` | 0.151 | eta | 13,615 | 5.69e-70 |
| `patient_data/sharing_ipd` | 0.148 | eta | 12,954 | 3.10e-62 |
| `ipd_info_type-Informed Consent Form (ICF)` | 0.147 | abs_spearman | 2,105 | 2.05e-11 |
| `mortality_YN` | 0.145 | abs_spearman | 17,903 | 4.23e-84 |
| `sponsors/lead_sponsor/agency_class` | 0.145 | eta | 42,207 | 9.92e-193 |
| `duration_year` | 0.141 | abs_spearman | 20,062 | 4.22e-89 |
| `duration_day` | 0.141 | abs_spearman | 20,062 | 4.22e-89 |
| `duration_month` | 0.141 | abs_spearman | 20,062 | 8.10e-89 |
| `completion_date` | 0.139 | abs_spearman | 20,062 | 1.18e-86 |
| `biology_pass` | 0.125 | abs_spearman | 28,367 | 1.59e-98 |
| `biology_fail` | 0.125 | abs_spearman | 28,367 | 1.59e-98 |
| `study_design_info/masking` | 0.124 | eta | 52,422 | 2.61e-161 |
| `study_design_info/primary_purpose` | 0.119 | eta | 52,095 | 4.42e-152 |
| `eligibility/healthy_volunteers` | 0.116 | eta | 52,677 | 2.35e-156 |
| `MaskingType-Investigator` | 0.115 | abs_spearman | 52,422 | 5.41e-154 |
| `mortality_rate` | 0.111 | abs_spearman | 17,903 | 1.24e-49 |
| `ipd_info_type-Statistical Analysis Plan (SAP)` | 0.103 | abs_spearman | 2,257 | 1.72e-06 |
| `MaskingType-Participant` | 0.102 | abs_spearman | 52,422 | 3.62e-121 |
| `study_design_info/masking_num` | 0.099 | abs_spearman | 52,422 | 6.97e-113 |
| `responsible_party/responsible_party_type` | 0.098 | eta | 40,560 | 8.45e-86 |
| `study_design_info/allocation` | 0.093 | eta | 39,412 | 3.95e-76 |
| `intervention/intervention_name` | 0.091 | abs_spearman | 52,772 | 4.05e-97 |
| `Placebo Comparator Arm Number` | 0.079 | abs_spearman | 50,684 | 1.36e-70 |
| `intervention_browse/mesh_term` | 0.077 | abs_spearman | 52,772 | 4.24e-70 |
| `Drug intervention Number` | 0.075 | abs_spearman | 52,772 | 6.97e-66 |
| `MaskingType-Outcomes Assessor` | 0.073 | abs_spearman | 52,422 | 1.36e-62 |
| `MaskingType-Care Provider` | 0.069 | abs_spearman | 52,422 | 3.32e-56 |
| `number_of_arms` | 0.063 | abs_spearman | 50,684 | 2.00e-45 |
| `condition_browse/mesh_term` | 0.062 | abs_spearman | 52,772 | 4.05e-45 |
| `eligibility/gender` | 0.058 | eta | 42,207 | 6.10e-31 |
| `smiless` | 0.052 | abs_spearman | 52,772 | 2.90e-32 |

### `execution_pass`   *(partners: 44)*

| partner | effect | metric | n_valid | p_adj |
|---------|--------|--------|---------|-------|
| `execution_fail` | 1.000 | abs_spearman | 52,772 | <1e-300 |
| `dropout_YN` | 0.940 | abs_spearman | 38,302 | <1e-300 |
| `failure_reason` | 0.755 | eta | 20,769 | <1e-300 |
| `dropout_rate` | 0.671 | abs_spearman | 38,302 | <1e-300 |
| `location/facility/address/city` | 0.393 | abs_spearman | 52,772 | <1e-300 |
| `intervention/intervention_type` | 0.377 | abs_spearman | 52,772 | <1e-300 |
| `enrollment` | 0.308 | abs_spearman | 38,306 | <1e-300 |
| `sae_YN` | 0.269 | abs_spearman | 17,903 | 3.81e-293 |
| `phase` | 0.261 | eta | 52,772 | <1e-300 |
| `approval_outcome` | 0.226 | abs_spearman | 23,059 | 4.06e-264 |
| `sae_rate` | 0.185 | abs_spearman | 17,903 | 3.31e-136 |
| `start_date` | 0.177 | abs_spearman | 20,062 | 1.67e-140 |
| `study_design_info/intervention_model` | 0.176 | eta | 52,169 | <1e-300 |
| `oversight_info/is_fda_regulated_drug` | 0.151 | eta | 13,615 | 5.69e-70 |
| `patient_data/sharing_ipd` | 0.148 | eta | 12,954 | 3.10e-62 |
| `ipd_info_type-Informed Consent Form (ICF)` | 0.147 | abs_spearman | 2,105 | 2.05e-11 |
| `mortality_YN` | 0.145 | abs_spearman | 17,903 | 4.23e-84 |
| `sponsors/lead_sponsor/agency_class` | 0.145 | eta | 42,207 | 9.92e-193 |
| `duration_year` | 0.141 | abs_spearman | 20,062 | 4.22e-89 |
| `duration_day` | 0.141 | abs_spearman | 20,062 | 4.22e-89 |
| `duration_month` | 0.141 | abs_spearman | 20,062 | 8.10e-89 |
| `completion_date` | 0.139 | abs_spearman | 20,062 | 1.18e-86 |
| `biology_pass` | 0.125 | abs_spearman | 28,367 | 1.59e-98 |
| `biology_fail` | 0.125 | abs_spearman | 28,367 | 1.59e-98 |
| `study_design_info/masking` | 0.124 | eta | 52,422 | 2.61e-161 |
| `study_design_info/primary_purpose` | 0.119 | eta | 52,095 | 4.42e-152 |
| `eligibility/healthy_volunteers` | 0.116 | eta | 52,677 | 2.35e-156 |
| `MaskingType-Investigator` | 0.115 | abs_spearman | 52,422 | 5.41e-154 |
| `mortality_rate` | 0.111 | abs_spearman | 17,903 | 1.24e-49 |
| `ipd_info_type-Statistical Analysis Plan (SAP)` | 0.103 | abs_spearman | 2,257 | 1.72e-06 |
| `MaskingType-Participant` | 0.102 | abs_spearman | 52,422 | 3.62e-121 |
| `study_design_info/masking_num` | 0.099 | abs_spearman | 52,422 | 6.97e-113 |
| `responsible_party/responsible_party_type` | 0.098 | eta | 40,560 | 8.45e-86 |
| `study_design_info/allocation` | 0.093 | eta | 39,412 | 3.95e-76 |
| `intervention/intervention_name` | 0.091 | abs_spearman | 52,772 | 4.05e-97 |
| `Placebo Comparator Arm Number` | 0.079 | abs_spearman | 50,684 | 1.36e-70 |
| `intervention_browse/mesh_term` | 0.077 | abs_spearman | 52,772 | 4.24e-70 |
| `Drug intervention Number` | 0.075 | abs_spearman | 52,772 | 6.97e-66 |
| `MaskingType-Outcomes Assessor` | 0.073 | abs_spearman | 52,422 | 1.36e-62 |
| `MaskingType-Care Provider` | 0.069 | abs_spearman | 52,422 | 3.32e-56 |
| `number_of_arms` | 0.063 | abs_spearman | 50,684 | 2.00e-45 |
| `condition_browse/mesh_term` | 0.062 | abs_spearman | 52,772 | 4.05e-45 |
| `eligibility/gender` | 0.058 | eta | 42,207 | 6.10e-31 |
| `smiless` | 0.052 | abs_spearman | 52,772 | 2.90e-32 |

### `failure_reason`   *(partners: 41)*

| partner | effect | metric | n_valid | p_adj |
|---------|--------|--------|---------|-------|
| `biology_pass` | 1.000 | eta | 20,769 | <1e-300 |
| `biology_fail` | 1.000 | eta | 20,769 | <1e-300 |
| `execution_fail` | 0.755 | eta | 20,769 | <1e-300 |
| `execution_pass` | 0.755 | eta | 20,769 | <1e-300 |
| `sae_YN` | 0.240 | eta | 3,199 | 1.79e-40 |
| `sponsors/lead_sponsor/agency_class` | 0.169 | cramers_v | 10,204 | 1.59e-180 |
| `location/facility/address/city` | 0.160 | eta | 20,769 | 7.36e-116 |
| `mortality_YN` | 0.153 | eta | 3,199 | 7.04e-16 |
| `patient_data/sharing_ipd` | 0.143 | cramers_v | 2,274 | 1.47e-17 |
| `Experimental Arm Number` | 0.134 | eta | 18,919 | 4.20e-73 |
| `enrollment` | 0.134 | eta | 6,304 | 4.71e-24 |
| `dropout_YN` | 0.127 | eta | 6,299 | 8.18e-22 |
| `phase` | 0.127 | cramers_v | 20,769 | 5.35e-208 |
| `start_date` | 0.123 | eta | 6,904 | 3.56e-22 |
| `eligibility/healthy_volunteers` | 0.118 | cramers_v | 20,706 | 2.44e-61 |
| `oversight_info/is_fda_regulated_drug` | 0.118 | cramers_v | 4,623 | 1.81e-13 |
| `completion_date` | 0.115 | eta | 6,904 | 2.71e-19 |
| `dropout_rate` | 0.111 | eta | 6,299 | 1.42e-16 |
| `intervention/intervention_type` | 0.110 | eta | 20,769 | 4.19e-54 |
| `number_of_arms` | 0.108 | eta | 18,919 | 1.54e-47 |
| `responsible_party/responsible_party_type` | 0.107 | cramers_v | 10,039 | 5.84e-46 |
| `duration_day` | 0.096 | eta | 6,904 | 1.67e-13 |
| `duration_year` | 0.096 | eta | 6,904 | 1.67e-13 |
| `duration_month` | 0.096 | eta | 6,904 | 1.81e-13 |
| `intervention_browse/mesh_term` | 0.079 | eta | 20,769 | 8.41e-28 |
| `Procedure intervention Number` | 0.077 | eta | 10,204 | 6.13e-13 |
| `mortality_rate` | 0.072 | eta | 3,199 | 0.0014 |
| `MaskingType-Investigator` | 0.071 | eta | 20,495 | 8.60e-22 |
| `Active Comparator Arm Number` | 0.071 | eta | 10,089 | 1.33e-10 |
| `study_design_info/masking_num` | 0.069 | eta | 20,495 | 9.49e-21 |
| `Placebo Comparator Arm Number` | 0.069 | eta | 18,919 | 7.68e-19 |
| `MaskingType-Participant` | 0.065 | eta | 20,495 | 3.18e-18 |
| `Drug intervention Number` | 0.065 | eta | 20,769 | 1.81e-18 |
| `oversight_info/has_dmc` | 0.064 | cramers_v | 13,941 | 6.76e-12 |
| `Radiation intervention Number` | 0.061 | eta | 20,769 | 2.44e-16 |
| `smiless` | 0.061 | eta | 20,769 | 2.96e-16 |
| `Device intervention Number` | 0.060 | eta | 10,204 | 9.11e-08 |
| `study_design_info/masking` | 0.058 | cramers_v | 20,495 | 3.93e-20 |
| `brief_title` | 0.055 | eta | 20,769 | 4.28e-13 |
| `study_design_info/primary_purpose` | 0.055 | cramers_v | 20,561 | 8.34e-25 |
| `study_design_info/intervention_model` | 0.053 | cramers_v | 20,298 | 6.08e-30 |

### `has_expanded_access`   *(partners: 9)*

| partner | effect | metric | n_valid | p_adj |
|---------|--------|--------|---------|-------|
| `patient_data/sharing_ipd` | 0.073 | cramers_v | 13,298 | 1.15e-15 |
| `sae_YN` | 0.072 | eta | 17,570 | 3.93e-21 |
| `sponsors/lead_sponsor/agency_class` | 0.069 | cramers_v | 70,125 | 3.96e-72 |
| `ipd_info_type-Informed Consent Form (ICF)` | 0.066 | eta | 2,123 | 0.0033 |
| `sae_rate` | 0.064 | eta | 17,570 | 4.53e-17 |
| `mortality_YN` | 0.063 | eta | 17,570 | 2.07e-16 |
| `dropout_rate` | 0.057 | eta | 37,901 | 2.51e-28 |
| `location/facility/address/city` | 0.056 | eta | 70,125 | 7.03e-49 |
| `mortality_rate` | 0.054 | eta | 17,570 | 1.83e-12 |

### `icdcode`   *(partners: 27)*

| partner | effect | metric | n_valid | p_adj |
|---------|--------|--------|---------|-------|
| `condition` | 0.531 | abs_spearman | 81,786 | <1e-300 |
| `condition_browse/mesh_term` | 0.289 | abs_spearman | 81,786 | <1e-300 |
| `sponsors/lead_sponsor/agency_class` | 0.144 | eta | 71,221 | <1e-300 |
| `mortality_rate` | 0.123 | abs_spearman | 17,916 | 9.54e-61 |
| `eligibility/maximum_age` | 0.113 | abs_spearman | 42,760 | 1.43e-120 |
| `mortality_YN` | 0.105 | abs_spearman | 17,916 | 1.11e-44 |
| `duration_day` | 0.103 | abs_spearman | 42,855 | 3.30e-101 |
| `duration_year` | 0.103 | abs_spearman | 42,855 | 3.30e-101 |
| `duration_month` | 0.103 | abs_spearman | 42,855 | 1.41e-100 |
| `intervention_browse/mesh_term` | 0.101 | abs_spearman | 81,786 | 1.52e-183 |
| `smiless` | 0.100 | abs_spearman | 81,786 | 3.04e-181 |
| `Drug intervention Number` | 0.091 | abs_spearman | 81,786 | 1.81e-150 |
| `study_design_info/primary_purpose` | 0.087 | eta | 80,983 | 1.85e-126 |
| `sae_rate` | 0.086 | abs_spearman | 17,916 | 1.72e-30 |
| `ipd_info_type-Statistical Analysis Plan (SAP)` | 0.083 | abs_spearman | 2,297 | 0.0001 |
| `Other intervention Number` | 0.081 | abs_spearman | 71,221 | 1.29e-103 |
| `intervention/intervention_name` | 0.078 | abs_spearman | 81,786 | 1.14e-109 |
| `eligibility/healthy_volunteers` | 0.074 | eta | 81,613 | 1.49e-97 |
| `ipd_info_type-Clinical Study Report (CSR)` | 0.072 | abs_spearman | 2,145 | 0.0013 |
| `start_date` | 0.070 | abs_spearman | 42,855 | 7.45e-47 |
| `study_design_info/masking` | 0.063 | eta | 75,043 | 6.32e-53 |
| `study_design_info/intervention_model` | 0.061 | eta | 80,897 | 2.66e-64 |
| `patient_data/sharing_ipd` | 0.059 | eta | 13,510 | 1.22e-10 |
| `phase` | 0.054 | eta | 81,786 | 6.37e-51 |
| `Radiation intervention Number` | 0.052 | abs_spearman | 81,786 | 1.03e-49 |
| `Procedure intervention Number` | 0.051 | abs_spearman | 71,221 | 8.87e-42 |
| `oversight_info/has_dmc` | 0.051 | eta | 45,926 | 3.56e-27 |

### `intervention/intervention_name`   *(partners: 41)*

| partner | effect | metric | n_valid | p_adj |
|---------|--------|--------|---------|-------|
| `Drug intervention Number` | 0.668 | abs_spearman | 81,786 | <1e-300 |
| `number_of_arms` | 0.440 | abs_spearman | 78,123 | <1e-300 |
| `intervention_browse/mesh_term` | 0.394 | abs_spearman | 81,786 | <1e-300 |
| `smiless` | 0.371 | abs_spearman | 81,786 | <1e-300 |
| `MaskingType-Participant` | 0.279 | abs_spearman | 81,170 | <1e-300 |
| `MaskingType-Investigator` | 0.271 | abs_spearman | 81,170 | <1e-300 |
| `study_design_info/masking_num` | 0.265 | abs_spearman | 81,170 | <1e-300 |
| `Active Comparator Arm Number` | 0.220 | abs_spearman | 69,293 | <1e-300 |
| `Placebo Comparator Arm Number` | 0.213 | abs_spearman | 78,123 | <1e-300 |
| `enrollment` | 0.212 | abs_spearman | 44,446 | <1e-300 |
| `Experimental Arm Number` | 0.200 | abs_spearman | 78,123 | <1e-300 |
| `study_design_info/intervention_model` | 0.199 | eta | 80,897 | <1e-300 |
| `Other intervention Number` | 0.181 | abs_spearman | 71,221 | <1e-300 |
| `MaskingType-Care Provider` | 0.171 | abs_spearman | 81,170 | <1e-300 |
| `MaskingType-Outcomes Assessor` | 0.165 | abs_spearman | 81,170 | <1e-300 |
| `Procedure intervention Number` | 0.163 | abs_spearman | 71,221 | <1e-300 |
| `No Intervention Arm Number` | 0.148 | abs_spearman | 69,293 | <1e-300 |
| `Radiation intervention Number` | 0.136 | abs_spearman | 81,786 | <1e-300 |
| `study_design_info/masking` | 0.136 | eta | 75,043 | 6.79e-285 |
| `patient_data/sharing_ipd` | 0.115 | eta | 13,510 | 1.72e-39 |
| `location/facility/address/city` | 0.109 | abs_spearman | 81,786 | 2.10e-212 |
| `mortality_YN` | 0.102 | abs_spearman | 17,916 | 2.43e-42 |
| `mortality_rate` | 0.097 | abs_spearman | 17,916 | 2.38e-38 |
| `study_design_info/allocation` | 0.096 | eta | 62,081 | 3.90e-126 |
| `brief_title` | 0.094 | abs_spearman | 81,786 | 3.66e-160 |
| `execution_pass` | 0.091 | abs_spearman | 52,772 | 4.05e-97 |
| `execution_fail` | 0.091 | abs_spearman | 52,772 | 4.05e-97 |
| `sae_YN` | 0.086 | abs_spearman | 17,916 | 2.00e-30 |
| `phase` | 0.081 | eta | 81,786 | 5.61e-116 |
| `icdcode` | 0.078 | abs_spearman | 81,786 | 1.14e-109 |
| `Biological intervention Number` | 0.074 | abs_spearman | 81,786 | 3.04e-98 |
| `oversight_info/is_fda_regulated_drug` | 0.073 | eta | 13,761 | 1.85e-17 |
| `oversight_info/has_dmc` | 0.067 | eta | 45,926 | 6.38e-46 |
| `dropout_YN` | 0.062 | abs_spearman | 38,302 | 9.88e-34 |
| `responsible_party/responsible_party_type` | 0.062 | eta | 67,878 | 5.48e-57 |
| `start_date` | 0.062 | abs_spearman | 42,855 | 3.19e-37 |
| `sponsors/lead_sponsor/agency_class` | 0.062 | eta | 71,221 | 9.67e-58 |
| `approval_outcome` | 0.059 | abs_spearman | 30,683 | 1.78e-24 |
| `sae_rate` | 0.056 | abs_spearman | 17,916 | 9.33e-14 |
| `completion_date` | 0.054 | abs_spearman | 42,855 | 4.51e-29 |
| `Behavioral intervention Number` | 0.050 | abs_spearman | 81,786 | 1.69e-46 |

### `intervention/intervention_type`   *(partners: 17)*

| partner | effect | metric | n_valid | p_adj |
|---------|--------|--------|---------|-------|
| `location/facility/address/city` | 0.566 | abs_spearman | 81,786 | <1e-300 |
| `approval_outcome` | 0.464 | abs_spearman | 30,683 | <1e-300 |
| `execution_pass` | 0.377 | abs_spearman | 52,772 | <1e-300 |
| `execution_fail` | 0.377 | abs_spearman | 52,772 | <1e-300 |
| `oversight_info/is_fda_regulated_drug` | 0.133 | eta | 13,761 | 7.14e-55 |
| `failure_reason` | 0.110 | eta | 20,769 | 4.19e-54 |
| `ipd_info_type-Statistical Analysis Plan (SAP)` | 0.095 | abs_spearman | 2,297 | 8.24e-06 |
| `study_design_info/masking` | 0.080 | eta | 75,043 | 4.37e-92 |
| `ipd_info_type-Analytic Code` | 0.077 | abs_spearman | 2,297 | 0.0003 |
| `Experimental Arm Number` | 0.076 | abs_spearman | 78,123 | 1.41e-98 |
| `number_of_arms` | 0.071 | abs_spearman | 78,123 | 2.33e-86 |
| `eligibility/healthy_volunteers` | 0.070 | eta | 81,613 | 9.88e-88 |
| `MaskingType-Participant` | 0.064 | abs_spearman | 81,170 | 1.08e-73 |
| `MaskingType-Investigator` | 0.064 | abs_spearman | 81,170 | 4.35e-73 |
| `Drug intervention Number` | 0.061 | abs_spearman | 81,786 | 2.49e-67 |
| `eligibility/maximum_age` | 0.054 | abs_spearman | 42,760 | 8.40e-29 |
| `study_design_info/primary_purpose` | 0.053 | eta | 80,983 | 1.05e-43 |

### `intervention_browse/mesh_term`   *(partners: 41)*

| partner | effect | metric | n_valid | p_adj |
|---------|--------|--------|---------|-------|
| `smiless` | 0.550 | abs_spearman | 81,786 | <1e-300 |
| `Drug intervention Number` | 0.442 | abs_spearman | 81,786 | <1e-300 |
| `intervention/intervention_name` | 0.394 | abs_spearman | 81,786 | <1e-300 |
| `Active Comparator Arm Number` | 0.217 | abs_spearman | 69,293 | <1e-300 |
| `sponsors/lead_sponsor/agency_class` | 0.174 | eta | 71,221 | <1e-300 |
| `mortality_rate` | 0.166 | abs_spearman | 17,916 | 3.08e-110 |
| `ipd_info_type-Clinical Study Report (CSR)` | 0.165 | abs_spearman | 2,145 | 2.95e-14 |
| `start_date` | 0.164 | abs_spearman | 42,855 | 5.39e-254 |
| `Placebo Comparator Arm Number` | 0.142 | abs_spearman | 78,123 | <1e-300 |
| `mortality_YN` | 0.138 | abs_spearman | 17,916 | 2.10e-76 |
| `duration_month` | 0.134 | abs_spearman | 42,855 | 2.97e-169 |
| `duration_day` | 0.133 | abs_spearman | 42,855 | 3.99e-168 |
| `duration_year` | 0.133 | abs_spearman | 42,855 | 3.99e-168 |
| `phase` | 0.123 | eta | 81,786 | 7.34e-270 |
| `ipd_info_type-Informed Consent Form (ICF)` | 0.117 | abs_spearman | 2,145 | 8.80e-08 |
| `eligibility/healthy_volunteers` | 0.115 | eta | 81,613 | 3.28e-238 |
| `completion_date` | 0.112 | abs_spearman | 42,855 | 8.54e-119 |
| `study_design_info/masking` | 0.110 | eta | 75,043 | 1.86e-181 |
| `icdcode` | 0.101 | abs_spearman | 81,786 | 1.52e-183 |
| `sae_rate` | 0.098 | abs_spearman | 17,916 | 1.02e-38 |
| `Device intervention Number` | 0.094 | abs_spearman | 71,221 | 7.87e-139 |
| `MaskingType-Participant` | 0.094 | abs_spearman | 81,170 | 8.76e-157 |
| `study_design_info/primary_purpose` | 0.094 | eta | 80,983 | 1.05e-146 |
| `study_design_info/masking_num` | 0.089 | abs_spearman | 81,170 | 4.80e-143 |
| `MaskingType-Investigator` | 0.083 | abs_spearman | 81,170 | 7.04e-124 |
| `failure_reason` | 0.079 | eta | 20,769 | 8.41e-28 |
| `execution_pass` | 0.077 | abs_spearman | 52,772 | 4.24e-70 |
| `execution_fail` | 0.077 | abs_spearman | 52,772 | 4.24e-70 |
| `oversight_info/is_fda_regulated_drug` | 0.074 | eta | 13,761 | 5.09e-18 |
| `study_design_info/intervention_model` | 0.073 | eta | 80,897 | 4.15e-92 |
| `ipd_info_type-Statistical Analysis Plan (SAP)` | 0.069 | abs_spearman | 2,297 | 0.0013 |
| `Radiation intervention Number` | 0.068 | abs_spearman | 81,786 | 1.27e-83 |
| `condition` | 0.065 | abs_spearman | 81,786 | 6.27e-77 |
| `Biological intervention Number` | 0.062 | abs_spearman | 81,786 | 3.34e-70 |
| `MaskingType-Care Provider` | 0.062 | abs_spearman | 81,170 | 7.35e-69 |
| `eligibility/gender` | 0.061 | eta | 71,221 | 5.48e-57 |
| `MaskingType-Outcomes Assessor` | 0.056 | abs_spearman | 81,170 | 9.11e-58 |
| `condition_browse/mesh_term` | 0.054 | abs_spearman | 81,786 | 7.73e-54 |
| `enrollment` | 0.052 | abs_spearman | 44,446 | 3.43e-27 |
| `responsible_party/responsible_party_type` | 0.051 | eta | 67,878 | 1.08e-38 |
| `Experimental Arm Number` | 0.051 | abs_spearman | 78,123 | 1.14e-45 |

### `ipd_info_type-Analytic Code`   *(partners: 21)*

| partner | effect | metric | n_valid | p_adj |
|---------|--------|--------|---------|-------|
| `sponsors/lead_sponsor/agency_class` | 0.205 | eta | 2,145 | 2.20e-19 |
| `responsible_party/responsible_party_type` | 0.127 | eta | 2,136 | 5.37e-08 |
| `phase` | 0.114 | eta | 2,297 | 2.33e-06 |
| `start_date` | 0.107 | abs_spearman | 1,728 | 1.38e-05 |
| `location/facility/address/city` | 0.101 | abs_spearman | 2,297 | 1.93e-06 |
| `Experimental Arm Number` | 0.097 | abs_spearman | 2,290 | 5.06e-06 |
| `completion_date` | 0.092 | abs_spearman | 1,728 | 0.0002 |
| `MaskingType-Care Provider` | 0.087 | abs_spearman | 2,297 | 4.51e-05 |
| `ipd_info_type-Clinical Study Report (CSR)` | 0.084 | abs_spearman | 2,145 | 0.0002 |
| `Biological intervention Number` | 0.079 | abs_spearman | 2,297 | 0.0002 |
| `sae_rate` | 0.078 | abs_spearman | 1,818 | 0.0012 |
| `intervention/intervention_type` | 0.077 | abs_spearman | 2,297 | 0.0003 |
| `sae_YN` | 0.076 | abs_spearman | 1,818 | 0.0018 |
| `ipd_info_type-Study Protocol` | 0.069 | abs_spearman | 2,297 | 0.0014 |
| `brief_title` | 0.068 | abs_spearman | 2,297 | 0.0016 |
| `mortality_YN` | 0.067 | abs_spearman | 1,818 | 0.0061 |
| `mortality_rate` | 0.064 | abs_spearman | 1,818 | 0.0090 |
| `Active Comparator Arm Number` | 0.062 | abs_spearman | 2,139 | 0.0060 |
| `smiless` | 0.061 | abs_spearman | 2,297 | 0.0052 |
| `MaskingType-Outcomes Assessor` | 0.059 | abs_spearman | 2,297 | 0.0063 |
| `study_design_info/masking_num` | 0.059 | abs_spearman | 2,297 | 0.0068 |

### `ipd_info_type-Clinical Study Report (CSR)`   *(partners: 33)*

| partner | effect | metric | n_valid | p_adj |
|---------|--------|--------|---------|-------|
| `sponsors/lead_sponsor/agency_class` | 0.462 | eta | 2,145 | 2.51e-110 |
| `responsible_party/responsible_party_type` | 0.315 | eta | 2,136 | 9.36e-49 |
| `eligibility/maximum_age` | 0.280 | abs_spearman | 1,034 | 1.09e-19 |
| `ipd_info_type-Statistical Analysis Plan (SAP)` | 0.236 | abs_spearman | 2,145 | 3.17e-28 |
| `ipd_info_type-Informed Consent Form (ICF)` | 0.209 | abs_spearman | 2,145 | 3.77e-22 |
| `location/facility/address/city` | 0.166 | abs_spearman | 2,145 | 1.81e-14 |
| `intervention_browse/mesh_term` | 0.165 | abs_spearman | 2,145 | 2.95e-14 |
| `mortality_rate` | 0.159 | abs_spearman | 1,818 | 1.69e-11 |
| `enrollment` | 0.159 | abs_spearman | 2,145 | 2.83e-13 |
| `MaskingType-Investigator` | 0.158 | abs_spearman | 2,145 | 3.33e-13 |
| `oversight_info/has_dmc` | 0.143 | eta | 1,919 | 6.54e-10 |
| `completion_date` | 0.140 | abs_spearman | 1,728 | 9.17e-09 |
| `Behavioral intervention Number` | 0.137 | abs_spearman | 2,145 | 3.77e-10 |
| `Experimental Arm Number` | 0.136 | abs_spearman | 2,139 | 5.05e-10 |
| `MaskingType-Participant` | 0.135 | abs_spearman | 2,145 | 7.13e-10 |
| `study_design_info/masking_num` | 0.128 | abs_spearman | 2,145 | 5.06e-09 |
| `phase` | 0.123 | eta | 2,145 | 6.08e-07 |
| `number_of_arms` | 0.123 | abs_spearman | 2,139 | 2.17e-08 |
| `Placebo Comparator Arm Number` | 0.114 | abs_spearman | 2,139 | 2.28e-07 |
| `mortality_YN` | 0.112 | abs_spearman | 1,818 | 2.60e-06 |
| `start_date` | 0.100 | abs_spearman | 1,728 | 4.55e-05 |
| `study_design_info/intervention_model` | 0.100 | eta | 2,140 | 0.0004 |
| `eligibility/healthy_volunteers` | 0.097 | eta | 2,145 | 1.12e-05 |
| `study_design_info/allocation` | 0.097 | eta | 1,724 | 8.75e-05 |
| `ipd_info_type-Analytic Code` | 0.084 | abs_spearman | 2,145 | 0.0002 |
| `oversight_info/is_fda_regulated_drug` | 0.083 | eta | 1,457 | 0.0021 |
| `sae_rate` | 0.078 | abs_spearman | 1,818 | 0.0014 |
| `Procedure intervention Number` | 0.076 | abs_spearman | 2,145 | 0.0006 |
| `MaskingType-Care Provider` | 0.074 | abs_spearman | 2,145 | 0.0008 |
| `icdcode` | 0.072 | abs_spearman | 2,145 | 0.0013 |
| `smiless` | 0.069 | abs_spearman | 2,145 | 0.0020 |
| `Radiation intervention Number` | 0.066 | abs_spearman | 2,145 | 0.0034 |
| `condition` | 0.065 | abs_spearman | 2,145 | 0.0038 |

### `ipd_info_type-Informed Consent Form (ICF)`   *(partners: 35)*

| partner | effect | metric | n_valid | p_adj |
|---------|--------|--------|---------|-------|
| `eligibility/healthy_volunteers` | 0.332 | eta | 2,145 | 5.89e-56 |
| `eligibility/maximum_age` | 0.297 | abs_spearman | 1,034 | 4.63e-22 |
| `location/facility/address/city` | 0.244 | abs_spearman | 2,145 | 3.95e-30 |
| `Biological intervention Number` | 0.244 | abs_spearman | 2,145 | 4.01e-30 |
| `ipd_info_type-Clinical Study Report (CSR)` | 0.209 | abs_spearman | 2,145 | 3.77e-22 |
| `phase` | 0.209 | eta | 2,145 | 3.91e-20 |
| `dropout_rate` | 0.178 | abs_spearman | 2,105 | 4.46e-16 |
| `Drug intervention Number` | 0.171 | abs_spearman | 2,145 | 3.24e-15 |
| `oversight_info/is_fda_regulated_drug` | 0.171 | eta | 1,457 | 1.08e-10 |
| `sponsors/lead_sponsor/agency_class` | 0.162 | eta | 2,145 | 4.57e-12 |
| `dropout_YN` | 0.156 | abs_spearman | 2,105 | 1.44e-12 |
| `sae_YN` | 0.153 | abs_spearman | 1,818 | 1.16e-10 |
| `study_design_info/intervention_model` | 0.152 | eta | 2,140 | 6.64e-10 |
| `execution_pass` | 0.147 | abs_spearman | 2,105 | 2.05e-11 |
| `execution_fail` | 0.147 | abs_spearman | 2,105 | 2.05e-11 |
| `responsible_party/responsible_party_type` | 0.130 | eta | 2,136 | 2.58e-08 |
| `condition` | 0.128 | abs_spearman | 2,145 | 4.30e-09 |
| `enrollment` | 0.127 | abs_spearman | 2,145 | 6.26e-09 |
| `mortality_YN` | 0.123 | abs_spearman | 1,818 | 2.67e-07 |
| `oversight_info/has_dmc` | 0.123 | eta | 1,919 | 1.22e-07 |
| `mortality_rate` | 0.120 | abs_spearman | 1,818 | 5.40e-07 |
| `intervention_browse/mesh_term` | 0.117 | abs_spearman | 2,145 | 8.80e-08 |
| `sae_rate` | 0.107 | abs_spearman | 1,818 | 7.51e-06 |
| `condition_browse/mesh_term` | 0.107 | abs_spearman | 2,145 | 1.21e-06 |
| `brief_title` | 0.094 | abs_spearman | 2,145 | 2.00e-05 |
| `Placebo Comparator Arm Number` | 0.090 | abs_spearman | 2,139 | 4.58e-05 |
| `completion_date` | 0.086 | abs_spearman | 1,728 | 0.0005 |
| `eligibility/minimum_age` | 0.082 | abs_spearman | 2,103 | 0.0003 |
| `start_date` | 0.080 | abs_spearman | 1,728 | 0.0013 |
| `smiless` | 0.079 | abs_spearman | 2,145 | 0.0004 |
| `Procedure intervention Number` | 0.075 | abs_spearman | 2,145 | 0.0007 |
| `ipd_info_type-Study Protocol` | 0.070 | abs_spearman | 2,145 | 0.0016 |
| `MaskingType-Investigator` | 0.069 | abs_spearman | 2,145 | 0.0021 |
| `has_expanded_access` | 0.066 | eta | 2,123 | 0.0033 |
| `MaskingType-Participant` | 0.064 | abs_spearman | 2,145 | 0.0042 |

### `ipd_info_type-Statistical Analysis Plan (SAP)`   *(partners: 27)*

| partner | effect | metric | n_valid | p_adj |
|---------|--------|--------|---------|-------|
| `sponsors/lead_sponsor/agency_class` | 0.433 | eta | 2,145 | 1.47e-95 |
| `ipd_info_type-Study Protocol` | 0.242 | abs_spearman | 2,297 | 1.25e-31 |
| `ipd_info_type-Clinical Study Report (CSR)` | 0.236 | abs_spearman | 2,145 | 3.17e-28 |
| `responsible_party/responsible_party_type` | 0.222 | eta | 2,136 | 1.20e-23 |
| `location/facility/address/city` | 0.221 | abs_spearman | 2,297 | 1.67e-26 |
| `sae_YN` | 0.204 | abs_spearman | 1,818 | 3.56e-18 |
| `enrollment` | 0.154 | abs_spearman | 2,145 | 1.61e-12 |
| `phase` | 0.149 | eta | 2,297 | 7.42e-11 |
| `approval_outcome` | 0.131 | abs_spearman | 746 | 0.0005 |
| `Experimental Arm Number` | 0.128 | abs_spearman | 2,290 | 1.36e-09 |
| `sae_rate` | 0.127 | abs_spearman | 1,818 | 9.30e-08 |
| `execution_fail` | 0.103 | abs_spearman | 2,257 | 1.72e-06 |
| `execution_pass` | 0.103 | abs_spearman | 2,257 | 1.72e-06 |
| `intervention/intervention_type` | 0.095 | abs_spearman | 2,297 | 8.24e-06 |
| `oversight_info/has_dmc` | 0.090 | eta | 2,059 | 6.15e-05 |
| `condition` | 0.090 | abs_spearman | 2,297 | 2.42e-05 |
| `Procedure intervention Number` | 0.085 | abs_spearman | 2,145 | 0.0001 |
| `icdcode` | 0.083 | abs_spearman | 2,297 | 0.0001 |
| `dropout_YN` | 0.082 | abs_spearman | 2,105 | 0.0003 |
| `Behavioral intervention Number` | 0.076 | abs_spearman | 2,297 | 0.0004 |
| `dropout_rate` | 0.075 | abs_spearman | 2,105 | 0.0009 |
| `intervention_browse/mesh_term` | 0.069 | abs_spearman | 2,297 | 0.0013 |
| `brief_title` | 0.064 | abs_spearman | 2,297 | 0.0030 |
| `mortality_YN` | 0.064 | abs_spearman | 1,818 | 0.0090 |
| `Drug intervention Number` | 0.062 | abs_spearman | 2,297 | 0.0044 |
| `No Intervention Arm Number` | 0.060 | abs_spearman | 2,139 | 0.0077 |
| `number_of_arms` | 0.056 | abs_spearman | 2,290 | 0.0097 |

### `ipd_info_type-Study Protocol`   *(partners: 16)*

| partner | effect | metric | n_valid | p_adj |
|---------|--------|--------|---------|-------|
| `ipd_info_type-Statistical Analysis Plan (SAP)` | 0.242 | abs_spearman | 2,297 | 1.25e-31 |
| `sponsors/lead_sponsor/agency_class` | 0.227 | eta | 2,145 | 5.89e-24 |
| `responsible_party/responsible_party_type` | 0.161 | eta | 2,136 | 1.40e-12 |
| `sae_rate` | 0.098 | abs_spearman | 1,818 | 4.78e-05 |
| `sae_YN` | 0.094 | abs_spearman | 1,818 | 9.75e-05 |
| `start_date` | 0.085 | abs_spearman | 1,728 | 0.0006 |
| `completion_date` | 0.077 | abs_spearman | 1,728 | 0.0019 |
| `location/facility/address/city` | 0.077 | abs_spearman | 2,297 | 0.0004 |
| `ipd_info_type-Informed Consent Form (ICF)` | 0.070 | abs_spearman | 2,145 | 0.0016 |
| `ipd_info_type-Analytic Code` | 0.069 | abs_spearman | 2,297 | 0.0014 |
| `mortality_rate` | 0.068 | abs_spearman | 1,818 | 0.0049 |
| `dropout_YN` | 0.066 | abs_spearman | 2,105 | 0.0035 |
| `mortality_YN` | 0.065 | abs_spearman | 1,818 | 0.0076 |
| `number_of_arms` | 0.064 | abs_spearman | 2,290 | 0.0029 |
| `Other Arm Number` | 0.060 | abs_spearman | 2,290 | 0.0054 |
| `Experimental Arm Number` | 0.059 | abs_spearman | 2,290 | 0.0066 |

### `location/facility/address/city`   *(partners: 46)*

| partner | effect | metric | n_valid | p_adj |
|---------|--------|--------|---------|-------|
| `intervention/intervention_type` | 0.566 | abs_spearman | 81,786 | <1e-300 |
| `sae_YN` | 0.477 | abs_spearman | 17,916 | <1e-300 |
| `enrollment` | 0.456 | abs_spearman | 44,446 | <1e-300 |
| `execution_pass` | 0.393 | abs_spearman | 52,772 | <1e-300 |
| `execution_fail` | 0.393 | abs_spearman | 52,772 | <1e-300 |
| `sae_rate` | 0.371 | abs_spearman | 17,916 | <1e-300 |
| `approval_outcome` | 0.360 | abs_spearman | 30,683 | <1e-300 |
| `mortality_YN` | 0.318 | abs_spearman | 17,916 | <1e-300 |
| `dropout_YN` | 0.289 | abs_spearman | 38,302 | <1e-300 |
| `phase` | 0.274 | eta | 81,786 | <1e-300 |
| `dropout_rate` | 0.268 | abs_spearman | 38,302 | <1e-300 |
| `mortality_rate` | 0.265 | abs_spearman | 17,916 | 4.15e-284 |
| `duration_year` | 0.256 | abs_spearman | 42,855 | <1e-300 |
| `duration_day` | 0.256 | abs_spearman | 42,855 | <1e-300 |
| `duration_month` | 0.255 | abs_spearman | 42,855 | <1e-300 |
| `ipd_info_type-Informed Consent Form (ICF)` | 0.244 | abs_spearman | 2,145 | 3.95e-30 |
| `patient_data/sharing_ipd` | 0.228 | eta | 13,510 | 8.13e-157 |
| `ipd_info_type-Statistical Analysis Plan (SAP)` | 0.221 | abs_spearman | 2,297 | 1.67e-26 |
| `sponsors/lead_sponsor/agency_class` | 0.174 | eta | 71,221 | <1e-300 |
| `ipd_info_type-Clinical Study Report (CSR)` | 0.166 | abs_spearman | 2,145 | 1.81e-14 |
| `failure_reason` | 0.160 | eta | 20,769 | 7.36e-116 |
| `responsible_party/responsible_party_type` | 0.146 | eta | 67,878 | <1e-300 |
| `study_design_info/intervention_model` | 0.140 | eta | 80,897 | <1e-300 |
| `eligibility/healthy_volunteers` | 0.122 | eta | 81,613 | 3.93e-268 |
| `Experimental Arm Number` | 0.122 | abs_spearman | 78,123 | 3.71e-254 |
| `study_design_info/masking` | 0.116 | eta | 75,043 | 4.39e-203 |
| `Drug intervention Number` | 0.112 | abs_spearman | 81,786 | 1.03e-224 |
| `MaskingType-Investigator` | 0.111 | abs_spearman | 81,170 | 2.13e-221 |
| `intervention/intervention_name` | 0.109 | abs_spearman | 81,786 | 2.10e-212 |
| `oversight_info/is_fda_regulated_drug` | 0.108 | eta | 13,761 | 8.26e-37 |
| `oversight_info/has_dmc` | 0.103 | eta | 45,926 | 2.39e-108 |
| `ipd_info_type-Analytic Code` | 0.101 | abs_spearman | 2,297 | 1.93e-06 |
| `condition_browse/mesh_term` | 0.098 | abs_spearman | 81,786 | 2.04e-174 |
| `study_design_info/masking_num` | 0.094 | abs_spearman | 81,170 | 4.38e-159 |
| `MaskingType-Care Provider` | 0.094 | abs_spearman | 81,170 | 3.00e-156 |
| `number_of_arms` | 0.091 | abs_spearman | 78,123 | 1.23e-143 |
| `MaskingType-Participant` | 0.088 | abs_spearman | 81,170 | 1.26e-139 |
| `study_design_info/primary_purpose` | 0.084 | eta | 80,983 | 3.60e-117 |
| `MaskingType-Outcomes Assessor` | 0.077 | abs_spearman | 81,170 | 1.67e-107 |
| `ipd_info_type-Study Protocol` | 0.077 | abs_spearman | 2,297 | 0.0004 |
| `Placebo Comparator Arm Number` | 0.076 | abs_spearman | 78,123 | 3.59e-99 |
| `study_design_info/allocation` | 0.074 | eta | 62,081 | 3.90e-76 |
| `start_date` | 0.070 | abs_spearman | 42,855 | 9.34e-48 |
| `No Intervention Arm Number` | 0.063 | abs_spearman | 69,293 | 7.89e-61 |
| `eligibility/maximum_age` | 0.062 | abs_spearman | 42,760 | 8.54e-38 |
| `has_expanded_access` | 0.056 | eta | 70,125 | 7.03e-49 |

### `mortality_YN`   *(partners: 53)*

| partner | effect | metric | n_valid | p_adj |
|---------|--------|--------|---------|-------|
| `mortality_rate` | 0.960 | abs_spearman | 17,916 | <1e-300 |
| `sae_rate` | 0.632 | abs_spearman | 17,916 | <1e-300 |
| `sae_YN` | 0.480 | abs_spearman | 17,916 | <1e-300 |
| `duration_day` | 0.359 | abs_spearman | 13,278 | <1e-300 |
| `duration_year` | 0.359 | abs_spearman | 13,278 | <1e-300 |
| `duration_month` | 0.359 | abs_spearman | 13,278 | <1e-300 |
| `location/facility/address/city` | 0.318 | abs_spearman | 17,916 | <1e-300 |
| `dropout_rate` | 0.266 | abs_spearman | 17,873 | 8.14e-287 |
| `eligibility/healthy_volunteers` | 0.256 | eta | 17,914 | 4.73e-265 |
| `enrollment` | 0.249 | abs_spearman | 17,881 | 3.47e-250 |
| `eligibility/maximum_age` | 0.242 | abs_spearman | 8,723 | 6.80e-116 |
| `phase` | 0.238 | eta | 17,916 | 3.00e-224 |
| `oversight_info/has_dmc` | 0.216 | eta | 16,069 | 2.56e-168 |
| `study_design_info/primary_purpose` | 0.198 | eta | 17,911 | 2.85e-148 |
| `start_date` | 0.196 | abs_spearman | 13,278 | 8.10e-114 |
| `study_design_info/masking` | 0.189 | eta | 17,890 | 7.26e-127 |
| `study_design_info/intervention_model` | 0.186 | eta | 17,857 | 1.17e-133 |
| `MaskingType-Participant` | 0.164 | abs_spearman | 17,890 | 7.41e-108 |
| `study_design_info/masking_num` | 0.155 | abs_spearman | 17,890 | 1.45e-95 |
| `failure_reason` | 0.153 | eta | 3,199 | 7.04e-16 |
| `patient_data/sharing_ipd` | 0.151 | eta | 9,941 | 4.07e-50 |
| `dropout_YN` | 0.150 | abs_spearman | 17,873 | 2.56e-90 |
| `execution_pass` | 0.145 | abs_spearman | 17,903 | 4.23e-84 |
| `execution_fail` | 0.145 | abs_spearman | 17,903 | 4.23e-84 |
| `MaskingType-Investigator` | 0.140 | abs_spearman | 17,890 | 8.90e-79 |
| `intervention_browse/mesh_term` | 0.138 | abs_spearman | 17,916 | 2.10e-76 |
| `Placebo Comparator Arm Number` | 0.137 | abs_spearman | 17,886 | 3.29e-75 |
| `condition_browse/mesh_term` | 0.128 | abs_spearman | 17,916 | 2.99e-65 |
| `ipd_info_type-Informed Consent Form (ICF)` | 0.123 | abs_spearman | 1,818 | 2.67e-07 |
| `Radiation intervention Number` | 0.119 | abs_spearman | 17,916 | 8.24e-57 |
| `smiless` | 0.113 | abs_spearman | 17,916 | 6.53e-52 |
| `ipd_info_type-Clinical Study Report (CSR)` | 0.112 | abs_spearman | 1,818 | 2.60e-06 |
| `responsible_party/responsible_party_type` | 0.111 | eta | 17,899 | 1.11e-48 |
| `icdcode` | 0.105 | abs_spearman | 17,916 | 1.11e-44 |
| `intervention/intervention_name` | 0.102 | abs_spearman | 17,916 | 2.43e-42 |
| `MaskingType-Outcomes Assessor` | 0.096 | abs_spearman | 17,890 | 2.00e-37 |
| `number_of_arms` | 0.096 | abs_spearman | 17,886 | 2.77e-37 |
| `oversight_info/is_fda_regulated_drug` | 0.095 | eta | 10,445 | 5.42e-22 |
| `MaskingType-Care Provider` | 0.086 | abs_spearman | 17,890 | 2.19e-30 |
| `condition` | 0.085 | abs_spearman | 17,916 | 1.05e-29 |
| `Biological intervention Number` | 0.080 | abs_spearman | 17,916 | 1.09e-26 |
| `sponsors/lead_sponsor/agency_class` | 0.078 | eta | 17,916 | 2.86e-23 |
| `biology_pass` | 0.074 | abs_spearman | 5,792 | 2.79e-08 |
| `biology_fail` | 0.074 | abs_spearman | 5,792 | 2.79e-08 |
| `Procedure intervention Number` | 0.073 | abs_spearman | 17,916 | 3.83e-22 |
| `eligibility/gender` | 0.072 | eta | 17,916 | 2.09e-20 |
| `ipd_info_type-Analytic Code` | 0.067 | abs_spearman | 1,818 | 0.0061 |
| `ipd_info_type-Study Protocol` | 0.065 | abs_spearman | 1,818 | 0.0076 |
| `study_design_info/allocation` | 0.064 | eta | 13,259 | 2.27e-13 |
| `ipd_info_type-Statistical Analysis Plan (SAP)` | 0.064 | abs_spearman | 1,818 | 0.0090 |
| `has_expanded_access` | 0.063 | eta | 17,570 | 2.07e-16 |
| `Drug intervention Number` | 0.060 | abs_spearman | 17,916 | 1.45e-15 |
| `eligibility/minimum_age` | 0.058 | abs_spearman | 17,440 | 3.84e-14 |

### `mortality_rate`   *(partners: 49)*

| partner | effect | metric | n_valid | p_adj |
|---------|--------|--------|---------|-------|
| `mortality_YN` | 0.960 | abs_spearman | 17,916 | <1e-300 |
| `sae_rate` | 0.666 | abs_spearman | 17,916 | <1e-300 |
| `sae_YN` | 0.456 | abs_spearman | 17,916 | <1e-300 |
| `duration_day` | 0.377 | abs_spearman | 13,278 | <1e-300 |
| `duration_year` | 0.377 | abs_spearman | 13,278 | <1e-300 |
| `duration_month` | 0.377 | abs_spearman | 13,278 | <1e-300 |
| `study_design_info/masking` | 0.279 | eta | 17,890 | 1.24e-296 |
| `dropout_rate` | 0.275 | abs_spearman | 17,873 | <1e-300 |
| `location/facility/address/city` | 0.265 | abs_spearman | 17,916 | 4.15e-284 |
| `eligibility/maximum_age` | 0.253 | abs_spearman | 8,723 | 1.73e-126 |
| `MaskingType-Participant` | 0.230 | abs_spearman | 17,890 | 7.62e-213 |
| `study_design_info/masking_num` | 0.221 | abs_spearman | 17,890 | 1.83e-196 |
| `MaskingType-Investigator` | 0.205 | abs_spearman | 17,890 | 3.43e-168 |
| `start_date` | 0.205 | abs_spearman | 13,278 | 4.20e-125 |
| `phase` | 0.204 | eta | 17,916 | 2.18e-163 |
| `study_design_info/intervention_model` | 0.202 | eta | 17,857 | 2.95e-158 |
| `eligibility/healthy_volunteers` | 0.184 | eta | 17,914 | 1.06e-134 |
| `Placebo Comparator Arm Number` | 0.182 | abs_spearman | 17,886 | 1.98e-132 |
| `study_design_info/primary_purpose` | 0.169 | eta | 17,911 | 1.23e-105 |
| `intervention_browse/mesh_term` | 0.166 | abs_spearman | 17,916 | 3.08e-110 |
| `ipd_info_type-Clinical Study Report (CSR)` | 0.159 | abs_spearman | 1,818 | 1.69e-11 |
| `enrollment` | 0.152 | abs_spearman | 17,881 | 2.42e-92 |
| `oversight_info/has_dmc` | 0.150 | eta | 16,069 | 4.23e-81 |
| `study_design_info/allocation` | 0.148 | eta | 13,259 | 6.36e-65 |
| `Radiation intervention Number` | 0.146 | abs_spearman | 17,916 | 5.43e-85 |
| `number_of_arms` | 0.145 | abs_spearman | 17,886 | 4.89e-84 |
| `MaskingType-Outcomes Assessor` | 0.142 | abs_spearman | 17,890 | 2.72e-80 |
| `smiless` | 0.139 | abs_spearman | 17,916 | 2.32e-77 |
| `condition_browse/mesh_term` | 0.134 | abs_spearman | 17,916 | 1.05e-71 |
| `MaskingType-Care Provider` | 0.131 | abs_spearman | 17,890 | 5.56e-69 |
| `icdcode` | 0.123 | abs_spearman | 17,916 | 9.54e-61 |
| `ipd_info_type-Informed Consent Form (ICF)` | 0.120 | abs_spearman | 1,818 | 5.40e-07 |
| `dropout_YN` | 0.111 | abs_spearman | 17,873 | 5.60e-50 |
| `execution_fail` | 0.111 | abs_spearman | 17,903 | 1.24e-49 |
| `execution_pass` | 0.111 | abs_spearman | 17,903 | 1.24e-49 |
| `sponsors/lead_sponsor/agency_class` | 0.111 | eta | 17,916 | 3.04e-47 |
| `condition` | 0.110 | abs_spearman | 17,916 | 1.33e-48 |
| `intervention/intervention_name` | 0.097 | abs_spearman | 17,916 | 2.38e-38 |
| `Procedure intervention Number` | 0.092 | abs_spearman | 17,916 | 2.08e-34 |
| `Biological intervention Number` | 0.083 | abs_spearman | 17,916 | 1.67e-28 |
| `biology_fail` | 0.081 | abs_spearman | 5,792 | 1.47e-09 |
| `biology_pass` | 0.081 | abs_spearman | 5,792 | 1.47e-09 |
| `oversight_info/is_fda_regulated_drug` | 0.080 | eta | 10,445 | 7.81e-16 |
| `failure_reason` | 0.072 | eta | 3,199 | 0.0014 |
| `ipd_info_type-Study Protocol` | 0.068 | abs_spearman | 1,818 | 0.0049 |
| `ipd_info_type-Analytic Code` | 0.064 | abs_spearman | 1,818 | 0.0090 |
| `Drug intervention Number` | 0.058 | abs_spearman | 17,916 | 1.83e-14 |
| `approval_outcome` | 0.056 | abs_spearman | 5,434 | 6.23e-05 |
| `has_expanded_access` | 0.054 | eta | 17,570 | 1.83e-12 |

### `number_of_arms`   *(partners: 43)*

| partner | effect | metric | n_valid | p_adj |
|---------|--------|--------|---------|-------|
| `Experimental Arm Number` | 0.488 | abs_spearman | 78,123 | <1e-300 |
| `study_design_info/intervention_model` | 0.451 | eta | 77,887 | <1e-300 |
| `study_design_info/masking_num` | 0.446 | abs_spearman | 77,947 | <1e-300 |
| `MaskingType-Participant` | 0.443 | abs_spearman | 77,947 | <1e-300 |
| `intervention/intervention_name` | 0.440 | abs_spearman | 78,123 | <1e-300 |
| `MaskingType-Investigator` | 0.419 | abs_spearman | 77,947 | <1e-300 |
| `Placebo Comparator Arm Number` | 0.352 | abs_spearman | 78,123 | <1e-300 |
| `enrollment` | 0.350 | abs_spearman | 43,117 | <1e-300 |
| `Drug intervention Number` | 0.323 | abs_spearman | 78,123 | <1e-300 |
| `study_design_info/masking` | 0.293 | eta | 72,860 | <1e-300 |
| `Active Comparator Arm Number` | 0.278 | abs_spearman | 69,293 | <1e-300 |
| `MaskingType-Care Provider` | 0.278 | abs_spearman | 77,947 | <1e-300 |
| `MaskingType-Outcomes Assessor` | 0.277 | abs_spearman | 77,947 | <1e-300 |
| `eligibility/healthy_volunteers` | 0.210 | eta | 78,060 | <1e-300 |
| `sponsors/lead_sponsor/agency_class` | 0.198 | eta | 69,293 | <1e-300 |
| `duration_month` | 0.161 | abs_spearman | 42,293 | 1.91e-243 |
| `duration_day` | 0.161 | abs_spearman | 42,293 | 3.03e-242 |
| `duration_year` | 0.161 | abs_spearman | 42,293 | 3.03e-242 |
| `sae_rate` | 0.160 | abs_spearman | 17,886 | 6.05e-102 |
| `patient_data/sharing_ipd` | 0.152 | eta | 13,438 | 1.64e-68 |
| `phase` | 0.148 | eta | 78,123 | <1e-300 |
| `mortality_rate` | 0.145 | abs_spearman | 17,886 | 4.89e-84 |
| `ipd_info_type-Clinical Study Report (CSR)` | 0.123 | abs_spearman | 2,139 | 2.17e-08 |
| `study_design_info/primary_purpose` | 0.114 | eta | 77,416 | 3.82e-211 |
| `responsible_party/responsible_party_type` | 0.110 | eta | 66,924 | 9.27e-178 |
| `approval_outcome` | 0.108 | abs_spearman | 28,187 | 1.14e-73 |
| `failure_reason` | 0.108 | eta | 18,919 | 1.54e-47 |
| `mortality_YN` | 0.096 | abs_spearman | 17,886 | 2.77e-37 |
| `Radiation intervention Number` | 0.093 | abs_spearman | 78,123 | 3.16e-149 |
| `location/facility/address/city` | 0.091 | abs_spearman | 78,123 | 1.23e-143 |
| `dropout_YN` | 0.083 | abs_spearman | 38,016 | 4.01e-58 |
| `condition_browse/mesh_term` | 0.079 | abs_spearman | 78,123 | 1.06e-107 |
| `start_date` | 0.075 | abs_spearman | 42,293 | 8.41e-53 |
| `intervention/intervention_type` | 0.071 | abs_spearman | 78,123 | 2.33e-86 |
| `Procedure intervention Number` | 0.070 | abs_spearman | 69,293 | 4.59e-76 |
| `ipd_info_type-Study Protocol` | 0.064 | abs_spearman | 2,290 | 0.0029 |
| `execution_pass` | 0.063 | abs_spearman | 50,684 | 2.00e-45 |
| `execution_fail` | 0.063 | abs_spearman | 50,684 | 2.00e-45 |
| `condition` | 0.062 | abs_spearman | 78,123 | 6.06e-66 |
| `eligibility/maximum_age` | 0.061 | abs_spearman | 41,114 | 7.46e-35 |
| `No Intervention Arm Number` | 0.057 | abs_spearman | 69,293 | 9.39e-51 |
| `ipd_info_type-Statistical Analysis Plan (SAP)` | 0.056 | abs_spearman | 2,290 | 0.0097 |
| `brief_title` | 0.053 | abs_spearman | 78,123 | 6.67e-50 |

### `oversight_info/has_dmc`   *(partners: 38)*

| partner | effect | metric | n_valid | p_adj |
|---------|--------|--------|---------|-------|
| `sponsors/lead_sponsor/agency_class` | 0.261 | cramers_v | 37,612 | <1e-300 |
| `duration_year` | 0.228 | eta | 14,181 | 2.91e-166 |
| `duration_day` | 0.228 | eta | 14,181 | 2.91e-166 |
| `duration_month` | 0.228 | eta | 14,181 | 3.84e-166 |
| `mortality_YN` | 0.216 | eta | 16,069 | 2.56e-168 |
| `sae_YN` | 0.176 | eta | 16,069 | 1.02e-111 |
| `sae_rate` | 0.174 | eta | 16,069 | 2.08e-108 |
| `phase` | 0.164 | cramers_v | 45,926 | 2.57e-266 |
| `mortality_rate` | 0.150 | eta | 16,069 | 4.23e-81 |
| `ipd_info_type-Clinical Study Report (CSR)` | 0.143 | eta | 1,919 | 6.54e-10 |
| `responsible_party/responsible_party_type` | 0.140 | cramers_v | 35,645 | 6.89e-151 |
| `study_design_info/primary_purpose` | 0.125 | cramers_v | 45,283 | 2.75e-147 |
| `study_design_info/intervention_model` | 0.124 | cramers_v | 45,679 | 2.36e-150 |
| `ipd_info_type-Informed Consent Form (ICF)` | 0.123 | eta | 1,919 | 1.22e-07 |
| `approval_outcome` | 0.116 | eta | 21,810 | 5.91e-66 |
| `eligibility/healthy_volunteers` | 0.114 | cramers_v | 45,906 | 1.65e-130 |
| `oversight_info/is_fda_regulated_drug` | 0.107 | cramers_v | 12,404 | 3.88e-32 |
| `location/facility/address/city` | 0.103 | eta | 45,926 | 2.39e-108 |
| `study_design_info/masking` | 0.102 | cramers_v | 41,228 | 1.32e-79 |
| `completion_date` | 0.099 | eta | 14,181 | 4.37e-32 |
| `ipd_info_type-Statistical Analysis Plan (SAP)` | 0.090 | eta | 2,059 | 6.15e-05 |
| `MaskingType-Care Provider` | 0.084 | eta | 45,821 | 9.67e-72 |
| `dropout_rate` | 0.078 | eta | 32,996 | 1.14e-45 |
| `Radiation intervention Number` | 0.076 | eta | 45,926 | 2.06e-59 |
| `Other intervention Number` | 0.074 | eta | 37,612 | 2.12e-46 |
| `condition_browse/mesh_term` | 0.071 | eta | 45,926 | 1.33e-52 |
| `study_design_info/allocation` | 0.071 | cramers_v | 34,580 | 1.18e-39 |
| `intervention/intervention_name` | 0.067 | eta | 45,926 | 6.38e-46 |
| `patient_data/sharing_ipd` | 0.065 | cramers_v | 12,367 | 8.01e-12 |
| `failure_reason` | 0.064 | cramers_v | 13,941 | 6.76e-12 |
| `biology_pass` | 0.063 | eta | 23,795 | 3.43e-22 |
| `biology_fail` | 0.063 | eta | 23,795 | 3.43e-22 |
| `study_design_info/masking_num` | 0.060 | eta | 45,821 | 3.78e-37 |
| `MaskingType-Outcomes Assessor` | 0.060 | eta | 45,821 | 7.72e-37 |
| `Procedure intervention Number` | 0.056 | eta | 37,612 | 5.37e-27 |
| `Biological intervention Number` | 0.054 | eta | 45,926 | 1.70e-30 |
| `condition` | 0.054 | eta | 45,926 | 2.44e-30 |
| `icdcode` | 0.051 | eta | 45,926 | 3.56e-27 |

### `oversight_info/is_fda_regulated_device`   *(partners: 16)*

| partner | effect | metric | n_valid | p_adj |
|---------|--------|--------|---------|-------|
| `Device intervention Number` | 0.637 | eta | 11,258 | <1e-300 |
| `Combination Product intervention Number` | 0.182 | eta | 13,676 | 2.13e-101 |
| `study_design_info/masking` | 0.117 | cramers_v | 13,530 | 4.92e-30 |
| `study_design_info/primary_purpose` | 0.116 | cramers_v | 13,675 | 7.56e-35 |
| `Sham Comparator Arm Number` | 0.110 | eta | 11,246 | 4.61e-31 |
| `Drug intervention Number` | 0.097 | eta | 13,676 | 1.16e-29 |
| `oversight_info/is_fda_regulated_drug` | 0.096 | cramers_v | 13,554 | 1.39e-28 |
| `MaskingType-Investigator` | 0.074 | eta | 13,666 | 1.18e-17 |
| `patient_data/sharing_ipd` | 0.068 | cramers_v | 7,697 | 2.99e-08 |
| `Placebo Comparator Arm Number` | 0.065 | eta | 13,650 | 7.62e-14 |
| `Radiation intervention Number` | 0.065 | eta | 13,676 | 8.02e-14 |
| `sae_YN` | 0.060 | eta | 10,378 | 1.37e-09 |
| `study_design_info/masking_num` | 0.060 | eta | 13,666 | 5.00e-12 |
| `MaskingType-Care Provider` | 0.055 | eta | 13,666 | 1.72e-10 |
| `MaskingType-Participant` | 0.055 | eta | 13,666 | 2.05e-10 |
| `phase` | 0.054 | cramers_v | 13,676 | 2.20e-08 |

### `oversight_info/is_fda_regulated_drug`   *(partners: 35)*

| partner | effect | metric | n_valid | p_adj |
|---------|--------|--------|---------|-------|
| `ipd_info_type-Informed Consent Form (ICF)` | 0.171 | eta | 1,457 | 1.08e-10 |
| `execution_fail` | 0.151 | eta | 13,615 | 5.69e-70 |
| `execution_pass` | 0.151 | eta | 13,615 | 5.69e-70 |
| `phase` | 0.144 | cramers_v | 13,761 | 1.05e-60 |
| `intervention/intervention_type` | 0.133 | eta | 13,761 | 7.14e-55 |
| `failure_reason` | 0.118 | cramers_v | 4,623 | 1.81e-13 |
| `Device intervention Number` | 0.116 | eta | 11,339 | 1.33e-34 |
| `location/facility/address/city` | 0.108 | eta | 13,761 | 8.26e-37 |
| `oversight_info/has_dmc` | 0.107 | cramers_v | 12,404 | 3.88e-32 |
| `eligibility/healthy_volunteers` | 0.105 | cramers_v | 13,761 | 1.27e-34 |
| `Drug intervention Number` | 0.103 | eta | 13,761 | 2.24e-33 |
| `sae_YN` | 0.099 | eta | 10,445 | 5.44e-24 |
| `study_design_info/primary_purpose` | 0.099 | cramers_v | 13,761 | 9.45e-25 |
| `sae_rate` | 0.097 | eta | 10,445 | 7.85e-23 |
| `oversight_info/is_fda_regulated_device` | 0.096 | cramers_v | 13,554 | 1.39e-28 |
| `mortality_YN` | 0.095 | eta | 10,445 | 5.42e-22 |
| `study_design_info/masking` | 0.094 | cramers_v | 13,609 | 4.45e-17 |
| `duration_day` | 0.090 | eta | 9,820 | 7.07e-19 |
| `duration_year` | 0.090 | eta | 9,820 | 7.07e-19 |
| `duration_month` | 0.090 | eta | 9,820 | 7.68e-19 |
| `dropout_rate` | 0.090 | eta | 11,191 | 4.12e-21 |
| `completion_date` | 0.087 | eta | 9,820 | 1.51e-17 |
| `ipd_info_type-Clinical Study Report (CSR)` | 0.083 | eta | 1,457 | 0.0021 |
| `sponsors/lead_sponsor/agency_class` | 0.080 | cramers_v | 11,339 | 1.79e-15 |
| `mortality_rate` | 0.080 | eta | 10,445 | 7.81e-16 |
| `intervention_browse/mesh_term` | 0.074 | eta | 13,761 | 5.09e-18 |
| `intervention/intervention_name` | 0.073 | eta | 13,761 | 1.85e-17 |
| `smiless` | 0.069 | eta | 13,761 | 7.31e-16 |
| `patient_data/sharing_ipd` | 0.066 | cramers_v | 7,749 | 7.96e-08 |
| `biology_pass` | 0.065 | eta | 5,975 | 6.93e-07 |
| `biology_fail` | 0.065 | eta | 5,975 | 6.93e-07 |
| `eligibility/gender` | 0.065 | cramers_v | 11,339 | 1.07e-10 |
| `study_design_info/intervention_model` | 0.060 | cramers_v | 13,721 | 7.76e-10 |
| `condition_browse/mesh_term` | 0.059 | eta | 13,761 | 7.46e-12 |
| `Placebo Comparator Arm Number` | 0.050 | eta | 13,735 | 6.13e-09 |

### `patient_data/sharing_ipd`   *(partners: 35)*

| partner | effect | metric | n_valid | p_adj |
|---------|--------|--------|---------|-------|
| `sponsors/lead_sponsor/agency_class` | 0.319 | cramers_v | 13,510 | <1e-300 |
| `sae_YN` | 0.251 | eta | 9,941 | 2.96e-140 |
| `approval_outcome` | 0.248 | eta | 4,575 | 2.12e-63 |
| `location/facility/address/city` | 0.228 | eta | 13,510 | 8.13e-157 |
| `responsible_party/responsible_party_type` | 0.223 | cramers_v | 13,499 | 2.12e-287 |
| `completion_date` | 0.200 | eta | 9,341 | 6.02e-83 |
| `Biological intervention Number` | 0.187 | eta | 13,510 | 3.32e-104 |
| `phase` | 0.182 | cramers_v | 13,510 | 3.06e-189 |
| `start_date` | 0.180 | eta | 9,341 | 1.18e-66 |
| `dropout_YN` | 0.177 | eta | 12,952 | 5.55e-90 |
| `Experimental Arm Number` | 0.172 | eta | 13,438 | 3.57e-88 |
| `number_of_arms` | 0.152 | eta | 13,438 | 1.64e-68 |
| `mortality_YN` | 0.151 | eta | 9,941 | 4.07e-50 |
| `execution_pass` | 0.148 | eta | 12,954 | 3.10e-62 |
| `execution_fail` | 0.148 | eta | 12,954 | 3.10e-62 |
| `failure_reason` | 0.143 | cramers_v | 2,274 | 1.47e-17 |
| `eligibility/maximum_age` | 0.129 | eta | 6,857 | 2.23e-25 |
| `study_design_info/primary_purpose` | 0.125 | cramers_v | 13,490 | 1.34e-78 |
| `study_design_info/masking` | 0.124 | cramers_v | 12,943 | 1.71e-62 |
| `intervention/intervention_name` | 0.115 | eta | 13,510 | 1.72e-39 |
| `dropout_rate` | 0.102 | eta | 12,952 | 1.36e-29 |
| `study_design_info/intervention_model` | 0.095 | cramers_v | 13,425 | 2.21e-47 |
| `MaskingType-Investigator` | 0.085 | eta | 13,493 | 2.35e-21 |
| `sae_rate` | 0.078 | eta | 9,941 | 1.86e-13 |
| `brief_title` | 0.076 | eta | 13,510 | 2.81e-17 |
| `has_expanded_access` | 0.073 | cramers_v | 13,298 | 1.15e-15 |
| `oversight_info/is_fda_regulated_device` | 0.068 | cramers_v | 7,697 | 2.99e-08 |
| `Drug intervention Number` | 0.066 | eta | 13,510 | 3.01e-13 |
| `oversight_info/is_fda_regulated_drug` | 0.066 | cramers_v | 7,749 | 7.96e-08 |
| `MaskingType-Participant` | 0.066 | eta | 13,493 | 4.75e-13 |
| `oversight_info/has_dmc` | 0.065 | cramers_v | 12,367 | 8.01e-12 |
| `Procedure intervention Number` | 0.062 | eta | 13,510 | 7.44e-12 |
| `icdcode` | 0.059 | eta | 13,510 | 1.22e-10 |
| `No Intervention Arm Number` | 0.058 | eta | 13,438 | 2.36e-10 |
| `Device intervention Number` | 0.056 | eta | 13,510 | 1.15e-09 |

### `phase`   *(partners: 59)*

| partner | effect | metric | n_valid | p_adj |
|---------|--------|--------|---------|-------|
| `eligibility/healthy_volunteers` | 0.411 | cramers_v | 81,613 | <1e-300 |
| `sae_YN` | 0.365 | eta | 17,916 | <1e-300 |
| `Experimental Arm Number` | 0.279 | eta | 78,123 | <1e-300 |
| `location/facility/address/city` | 0.274 | eta | 81,786 | <1e-300 |
| `execution_fail` | 0.261 | eta | 52,772 | <1e-300 |
| `execution_pass` | 0.261 | eta | 52,772 | <1e-300 |
| `dropout_YN` | 0.252 | eta | 38,302 | <1e-300 |
| `study_design_info/allocation` | 0.250 | cramers_v | 62,081 | <1e-300 |
| `study_design_info/intervention_model` | 0.245 | cramers_v | 80,897 | <1e-300 |
| `mortality_YN` | 0.238 | eta | 17,916 | 3.00e-224 |
| `Active Comparator Arm Number` | 0.227 | eta | 69,293 | <1e-300 |
| `duration_month` | 0.224 | eta | 42,855 | <1e-300 |
| `duration_day` | 0.223 | eta | 42,855 | <1e-300 |
| `duration_year` | 0.223 | eta | 42,855 | <1e-300 |
| `sae_rate` | 0.223 | eta | 17,916 | 1.72e-196 |
| `responsible_party/responsible_party_type` | 0.209 | cramers_v | 67,878 | <1e-300 |
| `ipd_info_type-Informed Consent Form (ICF)` | 0.209 | eta | 2,145 | 3.91e-20 |
| `sponsors/lead_sponsor/agency_class` | 0.207 | cramers_v | 71,221 | <1e-300 |
| `study_design_info/masking_num` | 0.205 | eta | 81,170 | <1e-300 |
| `mortality_rate` | 0.204 | eta | 17,916 | 2.18e-163 |
| `study_design_info/primary_purpose` | 0.194 | cramers_v | 80,983 | <1e-300 |
| `MaskingType-Investigator` | 0.185 | eta | 81,170 | <1e-300 |
| `patient_data/sharing_ipd` | 0.182 | cramers_v | 13,510 | 3.06e-189 |
| `MaskingType-Participant` | 0.173 | eta | 81,170 | <1e-300 |
| `oversight_info/has_dmc` | 0.164 | cramers_v | 45,926 | 2.57e-266 |
| `study_design_info/masking` | 0.161 | cramers_v | 75,043 | <1e-300 |
| `MaskingType-Outcomes Assessor` | 0.159 | eta | 81,170 | <1e-300 |
| `start_date` | 0.156 | eta | 42,855 | 9.49e-229 |
| `approval_outcome` | 0.156 | eta | 30,683 | 1.19e-162 |
| `MaskingType-Care Provider` | 0.151 | eta | 81,170 | <1e-300 |
| `ipd_info_type-Statistical Analysis Plan (SAP)` | 0.149 | eta | 2,297 | 7.42e-11 |
| `condition_browse/mesh_term` | 0.149 | eta | 81,786 | <1e-300 |
| `number_of_arms` | 0.148 | eta | 78,123 | <1e-300 |
| `oversight_info/is_fda_regulated_drug` | 0.144 | cramers_v | 13,761 | 1.05e-60 |
| `brief_title` | 0.139 | eta | 81,786 | <1e-300 |
| `dropout_rate` | 0.131 | eta | 38,302 | 1.62e-141 |
| `eligibility/gender` | 0.128 | cramers_v | 71,221 | <1e-300 |
| `failure_reason` | 0.127 | cramers_v | 20,769 | 5.35e-208 |
| `eligibility/maximum_age` | 0.124 | eta | 42,760 | 2.19e-141 |
| `ipd_info_type-Clinical Study Report (CSR)` | 0.123 | eta | 2,145 | 6.08e-07 |
| `intervention_browse/mesh_term` | 0.123 | eta | 81,786 | 7.34e-270 |
| `ipd_info_type-Analytic Code` | 0.114 | eta | 2,297 | 2.33e-06 |
| `enrollment` | 0.111 | eta | 44,446 | 1.01e-117 |
| `biology_fail` | 0.098 | eta | 34,427 | 1.21e-71 |
| `biology_pass` | 0.098 | eta | 34,427 | 1.21e-71 |
| `Placebo Comparator Arm Number` | 0.094 | eta | 78,123 | 9.42e-151 |
| `No Intervention Arm Number` | 0.090 | eta | 69,293 | 8.35e-121 |
| `intervention/intervention_name` | 0.081 | eta | 81,786 | 5.61e-116 |
| `completion_date` | 0.081 | eta | 42,855 | 3.53e-60 |
| `Radiation intervention Number` | 0.080 | eta | 81,786 | 8.54e-112 |
| `Device intervention Number` | 0.078 | eta | 71,221 | 7.13e-93 |
| `Biological intervention Number` | 0.076 | eta | 81,786 | 7.06e-102 |
| `smiless` | 0.069 | eta | 81,786 | 8.12e-83 |
| `Other Arm Number` | 0.061 | eta | 78,123 | 9.70e-63 |
| `Drug intervention Number` | 0.058 | eta | 81,786 | 3.54e-59 |
| `Procedure intervention Number` | 0.054 | eta | 71,221 | 6.74e-45 |
| `icdcode` | 0.054 | eta | 81,786 | 6.37e-51 |
| `oversight_info/is_fda_regulated_device` | 0.054 | cramers_v | 13,676 | 2.20e-08 |
| `condition` | 0.051 | eta | 81,786 | 7.89e-46 |

### `responsible_party/responsible_party_type`   *(partners: 42)*

| partner | effect | metric | n_valid | p_adj |
|---------|--------|--------|---------|-------|
| `sponsors/lead_sponsor/agency_class` | 0.420 | cramers_v | 67,878 | <1e-300 |
| `ipd_info_type-Clinical Study Report (CSR)` | 0.315 | eta | 2,136 | 9.36e-49 |
| `sae_YN` | 0.260 | eta | 17,899 | 4.94e-272 |
| `patient_data/sharing_ipd` | 0.223 | cramers_v | 13,499 | 2.12e-287 |
| `ipd_info_type-Statistical Analysis Plan (SAP)` | 0.222 | eta | 2,136 | 1.20e-23 |
| `phase` | 0.209 | cramers_v | 67,878 | <1e-300 |
| `Experimental Arm Number` | 0.179 | eta | 66,924 | <1e-300 |
| `ipd_info_type-Study Protocol` | 0.161 | eta | 2,136 | 1.40e-12 |
| `approval_outcome` | 0.147 | eta | 21,870 | 1.01e-103 |
| `location/facility/address/city` | 0.146 | eta | 67,878 | <1e-300 |
| `dropout_YN` | 0.145 | eta | 36,674 | 2.75e-168 |
| `oversight_info/has_dmc` | 0.140 | cramers_v | 35,645 | 6.89e-151 |
| `study_design_info/masking` | 0.131 | cramers_v | 63,064 | <1e-300 |
| `ipd_info_type-Informed Consent Form (ICF)` | 0.130 | eta | 2,136 | 2.58e-08 |
| `ipd_info_type-Analytic Code` | 0.127 | eta | 2,136 | 5.37e-08 |
| `Active Comparator Arm Number` | 0.120 | eta | 66,924 | 1.02e-210 |
| `No Intervention Arm Number` | 0.113 | eta | 66,924 | 1.99e-186 |
| `mortality_YN` | 0.111 | eta | 17,899 | 1.11e-48 |
| `number_of_arms` | 0.110 | eta | 66,924 | 9.27e-178 |
| `completion_date` | 0.109 | eta | 42,745 | 2.51e-110 |
| `failure_reason` | 0.107 | cramers_v | 10,039 | 5.84e-46 |
| `brief_title` | 0.106 | eta | 67,878 | 4.72e-165 |
| `execution_fail` | 0.098 | eta | 40,560 | 8.45e-86 |
| `execution_pass` | 0.098 | eta | 40,560 | 8.45e-86 |
| `dropout_rate` | 0.094 | eta | 36,674 | 3.18e-70 |
| `Biological intervention Number` | 0.083 | eta | 67,878 | 4.21e-103 |
| `Behavioral intervention Number` | 0.078 | eta | 67,878 | 4.22e-90 |
| `duration_month` | 0.075 | eta | 42,745 | 4.72e-53 |
| `duration_day` | 0.075 | eta | 42,745 | 2.51e-52 |
| `duration_year` | 0.075 | eta | 42,745 | 2.51e-52 |
| `sae_rate` | 0.071 | eta | 17,899 | 7.14e-20 |
| `study_design_info/allocation` | 0.071 | cramers_v | 51,309 | 7.43e-56 |
| `start_date` | 0.069 | eta | 42,745 | 2.33e-44 |
| `study_design_info/primary_purpose` | 0.069 | cramers_v | 67,490 | 9.70e-124 |
| `Drug intervention Number` | 0.067 | eta | 67,878 | 4.89e-67 |
| `intervention/intervention_name` | 0.062 | eta | 67,878 | 5.48e-57 |
| `study_design_info/intervention_model` | 0.062 | cramers_v | 67,576 | 1.05e-104 |
| `eligibility/gender` | 0.059 | cramers_v | 67,878 | 3.70e-99 |
| `Procedure intervention Number` | 0.056 | eta | 67,878 | 1.92e-46 |
| `MaskingType-Outcomes Assessor` | 0.054 | eta | 67,639 | 9.24e-44 |
| `Dietary Supplement intervention Number` | 0.054 | eta | 67,878 | 1.16e-43 |
| `intervention_browse/mesh_term` | 0.051 | eta | 67,878 | 1.08e-38 |

### `sae_YN`   *(partners: 46)*

| partner | effect | metric | n_valid | p_adj |
|---------|--------|--------|---------|-------|
| `sae_rate` | 0.831 | abs_spearman | 17,916 | <1e-300 |
| `mortality_YN` | 0.480 | abs_spearman | 17,916 | <1e-300 |
| `location/facility/address/city` | 0.477 | abs_spearman | 17,916 | <1e-300 |
| `mortality_rate` | 0.456 | abs_spearman | 17,916 | <1e-300 |
| `phase` | 0.365 | eta | 17,916 | <1e-300 |
| `enrollment` | 0.355 | abs_spearman | 17,881 | <1e-300 |
| `duration_year` | 0.313 | abs_spearman | 13,278 | 9.64e-298 |
| `duration_day` | 0.313 | abs_spearman | 13,278 | 9.64e-298 |
| `duration_month` | 0.312 | abs_spearman | 13,278 | 3.86e-297 |
| `eligibility/healthy_volunteers` | 0.309 | eta | 17,914 | <1e-300 |
| `dropout_rate` | 0.291 | abs_spearman | 17,873 | <1e-300 |
| `dropout_YN` | 0.290 | abs_spearman | 17,873 | <1e-300 |
| `sponsors/lead_sponsor/agency_class` | 0.287 | eta | 17,916 | <1e-300 |
| `study_design_info/primary_purpose` | 0.280 | eta | 17,911 | <1e-300 |
| `execution_fail` | 0.269 | abs_spearman | 17,903 | 3.81e-293 |
| `execution_pass` | 0.269 | abs_spearman | 17,903 | 3.81e-293 |
| `responsible_party/responsible_party_type` | 0.260 | eta | 17,899 | 4.94e-272 |
| `patient_data/sharing_ipd` | 0.251 | eta | 9,941 | 2.96e-140 |
| `failure_reason` | 0.240 | eta | 3,199 | 1.79e-40 |
| `study_design_info/intervention_model` | 0.234 | eta | 17,857 | 4.88e-215 |
| `ipd_info_type-Statistical Analysis Plan (SAP)` | 0.204 | abs_spearman | 1,818 | 3.56e-18 |
| `start_date` | 0.198 | abs_spearman | 13,278 | 2.20e-116 |
| `oversight_info/has_dmc` | 0.176 | eta | 16,069 | 1.02e-111 |
| `approval_outcome` | 0.175 | abs_spearman | 5,434 | 4.42e-38 |
| `condition_browse/mesh_term` | 0.163 | abs_spearman | 17,916 | 1.14e-106 |
| `study_design_info/masking` | 0.154 | eta | 17,890 | 7.28e-80 |
| `ipd_info_type-Informed Consent Form (ICF)` | 0.153 | abs_spearman | 1,818 | 1.16e-10 |
| `Biological intervention Number` | 0.132 | abs_spearman | 17,916 | 3.30e-70 |
| `eligibility/maximum_age` | 0.123 | abs_spearman | 8,723 | 1.45e-30 |
| `Experimental Arm Number` | 0.110 | abs_spearman | 17,886 | 3.61e-49 |
| `oversight_info/is_fda_regulated_drug` | 0.099 | eta | 10,445 | 5.44e-24 |
| `ipd_info_type-Study Protocol` | 0.094 | abs_spearman | 1,818 | 9.75e-05 |
| `eligibility/gender` | 0.088 | eta | 17,916 | 9.67e-31 |
| `intervention/intervention_name` | 0.086 | abs_spearman | 17,916 | 2.00e-30 |
| `biology_pass` | 0.083 | abs_spearman | 5,792 | 3.86e-10 |
| `biology_fail` | 0.083 | abs_spearman | 5,792 | 3.86e-10 |
| `ipd_info_type-Analytic Code` | 0.076 | abs_spearman | 1,818 | 0.0018 |
| `has_expanded_access` | 0.072 | eta | 17,570 | 3.93e-21 |
| `brief_title` | 0.070 | abs_spearman | 17,916 | 1.79e-20 |
| `Active Comparator Arm Number` | 0.069 | abs_spearman | 17,886 | 4.31e-20 |
| `No Intervention Arm Number` | 0.068 | abs_spearman | 17,886 | 3.16e-19 |
| `Device intervention Number` | 0.064 | abs_spearman | 17,916 | 3.18e-17 |
| `oversight_info/is_fda_regulated_device` | 0.060 | eta | 10,378 | 1.37e-09 |
| `Radiation intervention Number` | 0.057 | abs_spearman | 17,916 | 4.58e-14 |
| `Other Arm Number` | 0.057 | abs_spearman | 17,886 | 5.30e-14 |
| `Behavioral intervention Number` | 0.055 | abs_spearman | 17,916 | 3.41e-13 |

### `sae_rate`   *(partners: 56)*

| partner | effect | metric | n_valid | p_adj |
|---------|--------|--------|---------|-------|
| `sae_YN` | 0.831 | abs_spearman | 17,916 | <1e-300 |
| `mortality_rate` | 0.666 | abs_spearman | 17,916 | <1e-300 |
| `mortality_YN` | 0.632 | abs_spearman | 17,916 | <1e-300 |
| `duration_year` | 0.430 | abs_spearman | 13,278 | <1e-300 |
| `duration_day` | 0.430 | abs_spearman | 13,278 | <1e-300 |
| `duration_month` | 0.429 | abs_spearman | 13,278 | <1e-300 |
| `location/facility/address/city` | 0.371 | abs_spearman | 17,916 | <1e-300 |
| `dropout_rate` | 0.342 | abs_spearman | 17,873 | <1e-300 |
| `study_design_info/masking` | 0.313 | eta | 17,890 | <1e-300 |
| `study_design_info/intervention_model` | 0.271 | eta | 17,857 | 8.90e-292 |
| `eligibility/healthy_volunteers` | 0.261 | eta | 17,914 | 4.72e-275 |
| `start_date` | 0.257 | abs_spearman | 13,278 | 1.05e-198 |
| `phase` | 0.223 | eta | 17,916 | 1.72e-196 |
| `MaskingType-Participant` | 0.220 | abs_spearman | 17,890 | 3.43e-194 |
| `study_design_info/masking_num` | 0.209 | abs_spearman | 17,890 | 6.75e-175 |
| `study_design_info/primary_purpose` | 0.208 | eta | 17,911 | 3.07e-165 |
| `study_design_info/allocation` | 0.200 | eta | 13,259 | 3.07e-119 |
| `dropout_YN` | 0.191 | abs_spearman | 17,873 | 1.05e-145 |
| `execution_fail` | 0.185 | abs_spearman | 17,903 | 3.31e-136 |
| `execution_pass` | 0.185 | abs_spearman | 17,903 | 3.31e-136 |
| `condition_browse/mesh_term` | 0.184 | abs_spearman | 17,916 | 4.88e-135 |
| `MaskingType-Investigator` | 0.182 | abs_spearman | 17,890 | 7.78e-133 |
| `eligibility/maximum_age` | 0.178 | abs_spearman | 8,723 | 2.08e-62 |
| `oversight_info/has_dmc` | 0.174 | eta | 16,069 | 2.08e-108 |
| `number_of_arms` | 0.160 | abs_spearman | 17,886 | 6.05e-102 |
| `Placebo Comparator Arm Number` | 0.154 | abs_spearman | 17,886 | 1.01e-94 |
| `MaskingType-Outcomes Assessor` | 0.144 | abs_spearman | 17,890 | 1.81e-82 |
| `ipd_info_type-Statistical Analysis Plan (SAP)` | 0.127 | abs_spearman | 1,818 | 9.30e-08 |
| `enrollment` | 0.123 | abs_spearman | 17,881 | 1.44e-60 |
| `MaskingType-Care Provider` | 0.112 | abs_spearman | 17,890 | 1.13e-50 |
| `Active Comparator Arm Number` | 0.111 | abs_spearman | 17,886 | 4.53e-50 |
| `sponsors/lead_sponsor/agency_class` | 0.110 | eta | 17,916 | 1.57e-46 |
| `ipd_info_type-Informed Consent Form (ICF)` | 0.107 | abs_spearman | 1,818 | 7.51e-06 |
| `Biological intervention Number` | 0.105 | abs_spearman | 17,916 | 2.25e-44 |
| `Radiation intervention Number` | 0.098 | abs_spearman | 17,916 | 6.36e-39 |
| `ipd_info_type-Study Protocol` | 0.098 | abs_spearman | 1,818 | 4.78e-05 |
| `intervention_browse/mesh_term` | 0.098 | abs_spearman | 17,916 | 1.02e-38 |
| `oversight_info/is_fda_regulated_drug` | 0.097 | eta | 10,445 | 7.85e-23 |
| `icdcode` | 0.086 | abs_spearman | 17,916 | 1.72e-30 |
| `biology_fail` | 0.084 | abs_spearman | 5,792 | 3.48e-10 |
| `biology_pass` | 0.084 | abs_spearman | 5,792 | 3.48e-10 |
| `condition` | 0.081 | abs_spearman | 17,916 | 2.25e-27 |
| `ipd_info_type-Analytic Code` | 0.078 | abs_spearman | 1,818 | 0.0012 |
| `patient_data/sharing_ipd` | 0.078 | eta | 9,941 | 1.86e-13 |
| `ipd_info_type-Clinical Study Report (CSR)` | 0.078 | abs_spearman | 1,818 | 0.0014 |
| `eligibility/gender` | 0.078 | eta | 17,916 | 8.20e-24 |
| `smiless` | 0.075 | abs_spearman | 17,916 | 1.32e-23 |
| `responsible_party/responsible_party_type` | 0.071 | eta | 17,899 | 7.14e-20 |
| `No Intervention Arm Number` | 0.069 | abs_spearman | 17,886 | 8.01e-20 |
| `Behavioral intervention Number` | 0.066 | abs_spearman | 17,916 | 2.75e-18 |
| `has_expanded_access` | 0.064 | eta | 17,570 | 4.53e-17 |
| `Experimental Arm Number` | 0.060 | abs_spearman | 17,886 | 2.74e-15 |
| `brief_title` | 0.060 | abs_spearman | 17,916 | 3.35e-15 |
| `intervention/intervention_name` | 0.056 | abs_spearman | 17,916 | 9.33e-14 |
| `Other Arm Number` | 0.055 | abs_spearman | 17,886 | 5.45e-13 |
| `Device intervention Number` | 0.053 | abs_spearman | 17,916 | 3.01e-12 |

### `smiless`   *(partners: 31)*

| partner | effect | metric | n_valid | p_adj |
|---------|--------|--------|---------|-------|
| `intervention_browse/mesh_term` | 0.550 | abs_spearman | 81,786 | <1e-300 |
| `Drug intervention Number` | 0.510 | abs_spearman | 81,786 | <1e-300 |
| `intervention/intervention_name` | 0.371 | abs_spearman | 81,786 | <1e-300 |
| `Biological intervention Number` | 0.197 | abs_spearman | 81,786 | <1e-300 |
| `Active Comparator Arm Number` | 0.140 | abs_spearman | 69,293 | 2.92e-300 |
| `mortality_rate` | 0.139 | abs_spearman | 17,916 | 2.32e-77 |
| `start_date` | 0.127 | abs_spearman | 42,855 | 5.89e-153 |
| `mortality_YN` | 0.113 | abs_spearman | 17,916 | 6.53e-52 |
| `study_design_info/primary_purpose` | 0.104 | eta | 80,983 | 2.04e-183 |
| `sponsors/lead_sponsor/agency_class` | 0.101 | eta | 71,221 | 1.05e-157 |
| `icdcode` | 0.100 | abs_spearman | 81,786 | 3.04e-181 |
| `Device intervention Number` | 0.098 | abs_spearman | 71,221 | 2.84e-150 |
| `eligibility/healthy_volunteers` | 0.092 | eta | 81,613 | 2.53e-151 |
| `duration_month` | 0.091 | abs_spearman | 42,855 | 2.30e-78 |
| `duration_day` | 0.090 | abs_spearman | 42,855 | 6.62e-78 |
| `duration_year` | 0.090 | abs_spearman | 42,855 | 6.62e-78 |
| `completion_date` | 0.090 | abs_spearman | 42,855 | 4.38e-77 |
| `ipd_info_type-Informed Consent Form (ICF)` | 0.079 | abs_spearman | 2,145 | 0.0004 |
| `sae_rate` | 0.075 | abs_spearman | 17,916 | 1.32e-23 |
| `oversight_info/is_fda_regulated_drug` | 0.069 | eta | 13,761 | 7.31e-16 |
| `study_design_info/intervention_model` | 0.069 | eta | 80,897 | 2.88e-82 |
| `ipd_info_type-Clinical Study Report (CSR)` | 0.069 | abs_spearman | 2,145 | 0.0020 |
| `phase` | 0.069 | eta | 81,786 | 8.12e-83 |
| `Radiation intervention Number` | 0.065 | abs_spearman | 81,786 | 2.71e-76 |
| `failure_reason` | 0.061 | eta | 20,769 | 2.96e-16 |
| `ipd_info_type-Analytic Code` | 0.061 | abs_spearman | 2,297 | 0.0052 |
| `study_design_info/masking` | 0.059 | eta | 75,043 | 7.15e-45 |
| `Placebo Comparator Arm Number` | 0.057 | abs_spearman | 78,123 | 8.46e-56 |
| `execution_pass` | 0.052 | abs_spearman | 52,772 | 2.90e-32 |
| `execution_fail` | 0.052 | abs_spearman | 52,772 | 2.90e-32 |
| `dropout_rate` | 0.051 | abs_spearman | 38,302 | 4.58e-23 |

### `sponsors/lead_sponsor/agency_class`   *(partners: 60)*

| partner | effect | metric | n_valid | p_adj |
|---------|--------|--------|---------|-------|
| `ipd_info_type-Clinical Study Report (CSR)` | 0.462 | eta | 2,145 | 2.51e-110 |
| `ipd_info_type-Statistical Analysis Plan (SAP)` | 0.433 | eta | 2,145 | 1.47e-95 |
| `responsible_party/responsible_party_type` | 0.420 | cramers_v | 67,878 | <1e-300 |
| `patient_data/sharing_ipd` | 0.319 | cramers_v | 13,510 | <1e-300 |
| `sae_YN` | 0.287 | eta | 17,916 | <1e-300 |
| `duration_month` | 0.282 | eta | 42,855 | <1e-300 |
| `duration_year` | 0.282 | eta | 42,855 | <1e-300 |
| `duration_day` | 0.282 | eta | 42,855 | <1e-300 |
| `approval_outcome` | 0.275 | eta | 24,108 | <1e-300 |
| `oversight_info/has_dmc` | 0.261 | cramers_v | 37,612 | <1e-300 |
| `Experimental Arm Number` | 0.247 | eta | 69,293 | <1e-300 |
| `ipd_info_type-Study Protocol` | 0.227 | eta | 2,145 | 5.89e-24 |
| `dropout_YN` | 0.213 | eta | 38,302 | <1e-300 |
| `phase` | 0.207 | cramers_v | 71,221 | <1e-300 |
| `ipd_info_type-Analytic Code` | 0.205 | eta | 2,145 | 2.20e-19 |
| `number_of_arms` | 0.198 | eta | 69,293 | <1e-300 |
| `Other intervention Number` | 0.185 | eta | 71,221 | <1e-300 |
| `condition` | 0.177 | eta | 71,221 | <1e-300 |
| `location/facility/address/city` | 0.174 | eta | 71,221 | <1e-300 |
| `intervention_browse/mesh_term` | 0.174 | eta | 71,221 | <1e-300 |
| `failure_reason` | 0.169 | cramers_v | 10,204 | 1.59e-180 |
| `ipd_info_type-Informed Consent Form (ICF)` | 0.162 | eta | 2,145 | 4.57e-12 |
| `MaskingType-Investigator` | 0.153 | eta | 70,854 | <1e-300 |
| `Procedure intervention Number` | 0.149 | eta | 71,221 | <1e-300 |
| `execution_fail` | 0.145 | eta | 42,207 | 9.92e-193 |
| `execution_pass` | 0.145 | eta | 42,207 | 9.92e-193 |
| `icdcode` | 0.144 | eta | 71,221 | <1e-300 |
| `study_design_info/masking` | 0.138 | cramers_v | 64,727 | <1e-300 |
| `No Intervention Arm Number` | 0.137 | eta | 69,293 | 1.54e-281 |
| `Radiation intervention Number` | 0.134 | eta | 71,221 | 1.42e-279 |
| `condition_browse/mesh_term` | 0.129 | eta | 71,221 | 1.08e-258 |
| `Behavioral intervention Number` | 0.128 | eta | 71,221 | 4.37e-253 |
| `study_design_info/masking_num` | 0.118 | eta | 70,854 | 1.50e-215 |
| `MaskingType-Participant` | 0.118 | eta | 70,854 | 1.37e-213 |
| `Active Comparator Arm Number` | 0.116 | eta | 69,293 | 6.20e-201 |
| `dropout_rate` | 0.115 | eta | 38,302 | 2.34e-109 |
| `brief_title` | 0.113 | eta | 71,221 | 1.35e-198 |
| `eligibility/healthy_volunteers` | 0.112 | cramers_v | 71,109 | 9.56e-191 |
| `mortality_rate` | 0.111 | eta | 17,916 | 3.04e-47 |
| `sae_rate` | 0.110 | eta | 17,916 | 1.57e-46 |
| `Placebo Comparator Arm Number` | 0.104 | eta | 69,293 | 3.80e-161 |
| `completion_date` | 0.103 | eta | 42,855 | 8.56e-99 |
| `Biological intervention Number` | 0.102 | eta | 71,221 | 2.07e-159 |
| `smiless` | 0.101 | eta | 71,221 | 1.05e-157 |
| `study_design_info/intervention_model` | 0.100 | cramers_v | 70,749 | <1e-300 |
| `study_design_info/primary_purpose` | 0.090 | cramers_v | 70,604 | <1e-300 |
| `Drug intervention Number` | 0.089 | eta | 71,221 | 1.04e-120 |
| `eligibility/gender` | 0.084 | cramers_v | 71,221 | 4.03e-214 |
| `start_date` | 0.084 | eta | 42,855 | 1.80e-64 |
| `biology_fail` | 0.082 | eta | 23,862 | 1.37e-34 |
| `biology_pass` | 0.082 | eta | 23,862 | 1.37e-34 |
| `oversight_info/is_fda_regulated_drug` | 0.080 | cramers_v | 11,339 | 1.79e-15 |
| `mortality_YN` | 0.078 | eta | 17,916 | 2.86e-23 |
| `has_expanded_access` | 0.069 | cramers_v | 70,125 | 3.96e-72 |
| `MaskingType-Outcomes Assessor` | 0.062 | eta | 70,854 | 4.74e-59 |
| `intervention/intervention_name` | 0.062 | eta | 71,221 | 9.67e-58 |
| `Dietary Supplement intervention Number` | 0.061 | eta | 71,221 | 1.14e-56 |
| `study_design_info/allocation` | 0.059 | cramers_v | 54,376 | 3.62e-40 |
| `Device intervention Number` | 0.055 | eta | 71,221 | 1.64e-46 |
| `MaskingType-Care Provider` | 0.055 | eta | 70,854 | 2.92e-46 |

### `start_date`   *(partners: 46)*

| partner | effect | metric | n_valid | p_adj |
|---------|--------|--------|---------|-------|
| `completion_date` | 0.868 | abs_spearman | 42,855 | <1e-300 |
| `duration_month` | 0.426 | abs_spearman | 42,855 | <1e-300 |
| `duration_year` | 0.425 | abs_spearman | 42,855 | <1e-300 |
| `duration_day` | 0.425 | abs_spearman | 42,855 | <1e-300 |
| `approval_outcome` | 0.296 | abs_spearman | 9,263 | 2.90e-185 |
| `sae_rate` | 0.257 | abs_spearman | 13,278 | 1.05e-198 |
| `mortality_rate` | 0.205 | abs_spearman | 13,278 | 4.20e-125 |
| `eligibility/healthy_volunteers` | 0.198 | eta | 42,833 | <1e-300 |
| `sae_YN` | 0.198 | abs_spearman | 13,278 | 2.20e-116 |
| `mortality_YN` | 0.196 | abs_spearman | 13,278 | 8.10e-114 |
| `patient_data/sharing_ipd` | 0.180 | eta | 9,341 | 1.18e-66 |
| `execution_pass` | 0.177 | abs_spearman | 20,062 | 1.67e-140 |
| `execution_fail` | 0.177 | abs_spearman | 20,062 | 1.67e-140 |
| `study_design_info/intervention_model` | 0.174 | eta | 42,592 | 1.67e-280 |
| `study_design_info/masking` | 0.173 | eta | 42,635 | 1.27e-262 |
| `intervention_browse/mesh_term` | 0.164 | abs_spearman | 42,855 | 5.39e-254 |
| `phase` | 0.156 | eta | 42,855 | 9.49e-229 |
| `enrollment` | 0.151 | abs_spearman | 16,162 | 1.84e-82 |
| `condition_browse/mesh_term` | 0.145 | abs_spearman | 42,855 | 3.45e-200 |
| `dropout_rate` | 0.131 | abs_spearman | 16,162 | 1.44e-62 |
| `smiless` | 0.127 | abs_spearman | 42,855 | 5.89e-153 |
| `failure_reason` | 0.123 | eta | 6,904 | 3.56e-22 |
| `study_design_info/primary_purpose` | 0.119 | eta | 42,836 | 4.27e-125 |
| `ipd_info_type-Analytic Code` | 0.107 | abs_spearman | 1,728 | 1.38e-05 |
| `ipd_info_type-Clinical Study Report (CSR)` | 0.100 | abs_spearman | 1,728 | 4.55e-05 |
| `dropout_YN` | 0.099 | abs_spearman | 16,162 | 8.87e-36 |
| `Radiation intervention Number` | 0.089 | abs_spearman | 42,855 | 9.48e-75 |
| `ipd_info_type-Study Protocol` | 0.085 | abs_spearman | 1,728 | 0.0006 |
| `sponsors/lead_sponsor/agency_class` | 0.084 | eta | 42,855 | 1.80e-64 |
| `ipd_info_type-Informed Consent Form (ICF)` | 0.080 | abs_spearman | 1,728 | 0.0013 |
| `Procedure intervention Number` | 0.078 | abs_spearman | 42,855 | 1.70e-58 |
| `study_design_info/masking_num` | 0.076 | abs_spearman | 42,635 | 8.72e-56 |
| `MaskingType-Care Provider` | 0.076 | abs_spearman | 42,635 | 1.17e-55 |
| `MaskingType-Participant` | 0.076 | abs_spearman | 42,635 | 2.69e-55 |
| `number_of_arms` | 0.075 | abs_spearman | 42,293 | 8.41e-53 |
| `MaskingType-Outcomes Assessor` | 0.075 | abs_spearman | 42,635 | 4.58e-53 |
| `location/facility/address/city` | 0.070 | abs_spearman | 42,855 | 9.34e-48 |
| `icdcode` | 0.070 | abs_spearman | 42,855 | 7.45e-47 |
| `responsible_party/responsible_party_type` | 0.069 | eta | 42,745 | 2.33e-44 |
| `Combination Product intervention Number` | 0.065 | abs_spearman | 42,855 | 2.82e-41 |
| `intervention/intervention_name` | 0.062 | abs_spearman | 42,855 | 3.19e-37 |
| `biology_pass` | 0.059 | abs_spearman | 10,917 | 1.06e-09 |
| `biology_fail` | 0.059 | abs_spearman | 10,917 | 1.06e-09 |
| `condition` | 0.056 | abs_spearman | 42,855 | 2.06e-30 |
| `MaskingType-Investigator` | 0.055 | abs_spearman | 42,635 | 1.03e-29 |
| `eligibility/maximum_age` | 0.053 | abs_spearman | 24,161 | 1.97e-16 |

### `study_design_info/allocation`   *(partners: 32)*

| partner | effect | metric | n_valid | p_adj |
|---------|--------|--------|---------|-------|
| `study_design_info/intervention_model` | 0.554 | cramers_v | 61,697 | <1e-300 |
| `study_design_info/masking` | 0.488 | cramers_v | 56,864 | <1e-300 |
| `MaskingType-Participant` | 0.436 | eta | 61,818 | <1e-300 |
| `study_design_info/masking_num` | 0.430 | eta | 61,818 | <1e-300 |
| `MaskingType-Investigator` | 0.405 | eta | 61,818 | <1e-300 |
| `MaskingType-Care Provider` | 0.269 | eta | 61,818 | <1e-300 |
| `MaskingType-Outcomes Assessor` | 0.268 | eta | 61,818 | <1e-300 |
| `Placebo Comparator Arm Number` | 0.261 | eta | 59,269 | <1e-300 |
| `phase` | 0.250 | cramers_v | 62,081 | <1e-300 |
| `sae_rate` | 0.200 | eta | 13,259 | 3.07e-119 |
| `Active Comparator Arm Number` | 0.167 | eta | 52,870 | <1e-300 |
| `mortality_rate` | 0.148 | eta | 13,259 | 6.36e-65 |
| `Experimental Arm Number` | 0.146 | eta | 59,269 | 4.00e-278 |
| `dropout_rate` | 0.120 | eta | 29,014 | 1.67e-93 |
| `study_design_info/primary_purpose` | 0.105 | cramers_v | 61,425 | 2.25e-138 |
| `ipd_info_type-Clinical Study Report (CSR)` | 0.097 | eta | 1,724 | 8.75e-05 |
| `intervention/intervention_name` | 0.096 | eta | 62,081 | 3.90e-126 |
| `execution_fail` | 0.093 | eta | 39,412 | 3.95e-76 |
| `execution_pass` | 0.093 | eta | 39,412 | 3.95e-76 |
| `duration_day` | 0.092 | eta | 32,550 | 5.05e-62 |
| `duration_year` | 0.092 | eta | 32,550 | 5.05e-62 |
| `duration_month` | 0.092 | eta | 32,550 | 7.18e-62 |
| `Drug intervention Number` | 0.088 | eta | 62,081 | 4.78e-107 |
| `dropout_YN` | 0.076 | eta | 29,014 | 2.55e-38 |
| `location/facility/address/city` | 0.074 | eta | 62,081 | 3.90e-76 |
| `oversight_info/has_dmc` | 0.071 | cramers_v | 34,580 | 1.18e-39 |
| `responsible_party/responsible_party_type` | 0.071 | cramers_v | 51,309 | 7.43e-56 |
| `mortality_YN` | 0.064 | eta | 13,259 | 2.27e-13 |
| `sponsors/lead_sponsor/agency_class` | 0.059 | cramers_v | 54,376 | 3.62e-40 |
| `Other intervention Number` | 0.058 | eta | 54,376 | 1.27e-40 |
| `eligibility/minimum_age` | 0.054 | eta | 60,725 | 1.19e-40 |
| `condition` | 0.051 | eta | 62,081 | 4.76e-36 |

### `study_design_info/intervention_model`   *(partners: 58)*

| partner | effect | metric | n_valid | p_adj |
|---------|--------|--------|---------|-------|
| `study_design_info/allocation` | 0.554 | cramers_v | 61,697 | <1e-300 |
| `MaskingType-Participant` | 0.512 | eta | 80,702 | <1e-300 |
| `study_design_info/masking_num` | 0.508 | eta | 80,702 | <1e-300 |
| `MaskingType-Investigator` | 0.479 | eta | 80,702 | <1e-300 |
| `number_of_arms` | 0.451 | eta | 77,887 | <1e-300 |
| `MaskingType-Outcomes Assessor` | 0.352 | eta | 80,702 | <1e-300 |
| `MaskingType-Care Provider` | 0.345 | eta | 80,702 | <1e-300 |
| `Placebo Comparator Arm Number` | 0.341 | eta | 77,887 | <1e-300 |
| `Active Comparator Arm Number` | 0.338 | eta | 69,093 | <1e-300 |
| `eligibility/healthy_volunteers` | 0.293 | cramers_v | 80,743 | <1e-300 |
| `study_design_info/masking` | 0.282 | cramers_v | 74,651 | <1e-300 |
| `sae_rate` | 0.271 | eta | 17,857 | 8.90e-292 |
| `Experimental Arm Number` | 0.250 | eta | 77,887 | <1e-300 |
| `duration_month` | 0.249 | eta | 42,592 | <1e-300 |
| `duration_year` | 0.249 | eta | 42,592 | <1e-300 |
| `duration_day` | 0.249 | eta | 42,592 | <1e-300 |
| `phase` | 0.245 | cramers_v | 80,897 | <1e-300 |
| `dropout_YN` | 0.240 | eta | 38,137 | <1e-300 |
| `sae_YN` | 0.234 | eta | 17,857 | 4.88e-215 |
| `mortality_rate` | 0.202 | eta | 17,857 | 2.95e-158 |
| `Drug intervention Number` | 0.200 | eta | 80,897 | <1e-300 |
| `intervention/intervention_name` | 0.199 | eta | 80,897 | <1e-300 |
| `mortality_YN` | 0.186 | eta | 17,857 | 1.17e-133 |
| `execution_pass` | 0.176 | eta | 52,169 | <1e-300 |
| `execution_fail` | 0.176 | eta | 52,169 | <1e-300 |
| `start_date` | 0.174 | eta | 42,592 | 1.67e-280 |
| `dropout_rate` | 0.170 | eta | 38,137 | 1.32e-240 |
| `ipd_info_type-Informed Consent Form (ICF)` | 0.152 | eta | 2,140 | 6.64e-10 |
| `study_design_info/primary_purpose` | 0.142 | cramers_v | 80,137 | <1e-300 |
| `location/facility/address/city` | 0.140 | eta | 80,897 | <1e-300 |
| `condition_browse/mesh_term` | 0.134 | eta | 80,897 | <1e-300 |
| `oversight_info/has_dmc` | 0.124 | cramers_v | 45,679 | 2.36e-150 |
| `completion_date` | 0.123 | eta | 42,592 | 2.12e-137 |
| `Behavioral intervention Number` | 0.108 | eta | 80,897 | 5.14e-205 |
| `ipd_info_type-Clinical Study Report (CSR)` | 0.100 | eta | 2,140 | 0.0004 |
| `sponsors/lead_sponsor/agency_class` | 0.100 | cramers_v | 70,749 | <1e-300 |
| `No Intervention Arm Number` | 0.099 | eta | 69,093 | 5.10e-146 |
| `patient_data/sharing_ipd` | 0.095 | cramers_v | 13,425 | 2.21e-47 |
| `Radiation intervention Number` | 0.089 | eta | 80,897 | 1.17e-135 |
| `Biological intervention Number` | 0.088 | eta | 80,897 | 1.38e-134 |
| `eligibility/gender` | 0.087 | cramers_v | 70,749 | 9.49e-224 |
| `brief_title` | 0.085 | eta | 80,897 | 9.18e-126 |
| `enrollment` | 0.080 | eta | 44,158 | 2.27e-59 |
| `condition` | 0.077 | eta | 80,897 | 2.09e-103 |
| `intervention_browse/mesh_term` | 0.073 | eta | 80,897 | 4.15e-92 |
| `approval_outcome` | 0.072 | eta | 30,122 | 3.30e-32 |
| `smiless` | 0.069 | eta | 80,897 | 2.88e-82 |
| `responsible_party/responsible_party_type` | 0.062 | cramers_v | 67,576 | 1.05e-104 |
| `icdcode` | 0.061 | eta | 80,897 | 2.66e-64 |
| `eligibility/minimum_age` | 0.061 | eta | 78,839 | 6.71e-62 |
| `Other Arm Number` | 0.061 | eta | 77,887 | 3.48e-60 |
| `Procedure intervention Number` | 0.060 | eta | 70,749 | 5.11e-54 |
| `oversight_info/is_fda_regulated_drug` | 0.060 | cramers_v | 13,721 | 7.76e-10 |
| `Sham Comparator Arm Number` | 0.056 | eta | 69,093 | 1.05e-44 |
| `Other intervention Number` | 0.054 | eta | 70,749 | 6.09e-43 |
| `failure_reason` | 0.053 | cramers_v | 20,298 | 6.08e-30 |
| `Dietary Supplement intervention Number` | 0.051 | eta | 80,897 | 3.41e-44 |
| `eligibility/maximum_age` | 0.051 | eta | 42,360 | 2.33e-22 |

### `study_design_info/masking`   *(partners: 58)*

| partner | effect | metric | n_valid | p_adj |
|---------|--------|--------|---------|-------|
| `MaskingType-Participant` | 1.000 | eta | 75,043 | <1e-300 |
| `MaskingType-Care Provider` | 1.000 | eta | 75,043 | <1e-300 |
| `MaskingType-Investigator` | 1.000 | eta | 75,043 | <1e-300 |
| `MaskingType-Outcomes Assessor` | 1.000 | eta | 75,043 | <1e-300 |
| `study_design_info/masking_num` | 1.000 | eta | 75,043 | <1e-300 |
| `Placebo Comparator Arm Number` | 0.616 | eta | 72,860 | <1e-300 |
| `study_design_info/allocation` | 0.488 | cramers_v | 56,864 | <1e-300 |
| `sae_rate` | 0.313 | eta | 17,890 | <1e-300 |
| `number_of_arms` | 0.293 | eta | 72,860 | <1e-300 |
| `study_design_info/intervention_model` | 0.282 | cramers_v | 74,651 | <1e-300 |
| `mortality_rate` | 0.279 | eta | 17,890 | 1.24e-296 |
| `Active Comparator Arm Number` | 0.201 | eta | 64,055 | <1e-300 |
| `mortality_YN` | 0.189 | eta | 17,890 | 7.26e-127 |
| `completion_date` | 0.182 | eta | 42,635 | 5.40e-295 |
| `Drug intervention Number` | 0.178 | eta | 75,043 | <1e-300 |
| `start_date` | 0.173 | eta | 42,635 | 1.27e-262 |
| `phase` | 0.161 | cramers_v | 75,043 | <1e-300 |
| `dropout_rate` | 0.156 | eta | 38,218 | 5.23e-189 |
| `duration_year` | 0.156 | eta | 42,635 | 2.39e-210 |
| `duration_day` | 0.156 | eta | 42,635 | 2.39e-210 |
| `duration_month` | 0.155 | eta | 42,635 | 1.03e-209 |
| `sae_YN` | 0.154 | eta | 17,890 | 7.28e-80 |
| `dropout_YN` | 0.151 | eta | 38,218 | 3.64e-175 |
| `approval_outcome` | 0.147 | eta | 24,224 | 2.27e-101 |
| `sponsors/lead_sponsor/agency_class` | 0.138 | cramers_v | 64,727 | <1e-300 |
| `intervention/intervention_name` | 0.136 | eta | 75,043 | 6.79e-285 |
| `Sham Comparator Arm Number` | 0.135 | eta | 64,055 | 3.90e-238 |
| `No Intervention Arm Number` | 0.134 | eta | 64,055 | 3.81e-234 |
| `Device intervention Number` | 0.132 | eta | 64,727 | 1.53e-231 |
| `Behavioral intervention Number` | 0.132 | eta | 75,043 | 2.42e-270 |
| `responsible_party/responsible_party_type` | 0.131 | cramers_v | 63,064 | <1e-300 |
| `execution_fail` | 0.124 | eta | 52,422 | 2.61e-161 |
| `execution_pass` | 0.124 | eta | 52,422 | 2.61e-161 |
| `patient_data/sharing_ipd` | 0.124 | cramers_v | 12,943 | 1.71e-62 |
| `oversight_info/is_fda_regulated_device` | 0.117 | cramers_v | 13,530 | 4.92e-30 |
| `location/facility/address/city` | 0.116 | eta | 75,043 | 4.39e-203 |
| `Radiation intervention Number` | 0.115 | eta | 75,043 | 3.52e-201 |
| `intervention_browse/mesh_term` | 0.110 | eta | 75,043 | 1.86e-181 |
| `eligibility/healthy_volunteers` | 0.108 | cramers_v | 74,940 | 1.00e-175 |
| `oversight_info/has_dmc` | 0.102 | cramers_v | 41,228 | 1.32e-79 |
| `Procedure intervention Number` | 0.101 | eta | 64,727 | 5.44e-128 |
| `eligibility/minimum_age` | 0.095 | eta | 73,073 | 9.06e-130 |
| `oversight_info/is_fda_regulated_drug` | 0.094 | cramers_v | 13,609 | 4.45e-17 |
| `Experimental Arm Number` | 0.083 | eta | 72,860 | 1.34e-94 |
| `intervention/intervention_type` | 0.080 | eta | 75,043 | 4.37e-92 |
| `condition` | 0.076 | eta | 75,043 | 1.01e-80 |
| `Other intervention Number` | 0.075 | eta | 64,727 | 4.89e-67 |
| `eligibility/maximum_age` | 0.072 | eta | 39,233 | 9.51e-34 |
| `icdcode` | 0.063 | eta | 75,043 | 6.32e-53 |
| `condition_browse/mesh_term` | 0.063 | eta | 75,043 | 2.24e-52 |
| `study_design_info/primary_purpose` | 0.060 | cramers_v | 74,379 | <1e-300 |
| `Dietary Supplement intervention Number` | 0.059 | eta | 75,043 | 3.38e-46 |
| `smiless` | 0.059 | eta | 75,043 | 7.15e-45 |
| `enrollment` | 0.059 | eta | 38,225 | 1.88e-19 |
| `failure_reason` | 0.058 | cramers_v | 20,495 | 3.93e-20 |
| `eligibility/gender` | 0.057 | cramers_v | 64,727 | 1.81e-67 |
| `Other Arm Number` | 0.056 | eta | 72,860 | 2.05e-38 |
| `brief_title` | 0.053 | eta | 75,043 | 2.62e-34 |

### `study_design_info/masking_num`   *(partners: 42)*

| partner | effect | metric | n_valid | p_adj |
|---------|--------|--------|---------|-------|
| `study_design_info/masking` | 1.000 | eta | 75,043 | <1e-300 |
| `MaskingType-Participant` | 0.915 | abs_spearman | 81,170 | <1e-300 |
| `MaskingType-Investigator` | 0.892 | abs_spearman | 81,170 | <1e-300 |
| `MaskingType-Care Provider` | 0.779 | abs_spearman | 81,170 | <1e-300 |
| `MaskingType-Outcomes Assessor` | 0.748 | abs_spearman | 81,170 | <1e-300 |
| `Placebo Comparator Arm Number` | 0.685 | abs_spearman | 77,947 | <1e-300 |
| `study_design_info/intervention_model` | 0.508 | eta | 80,702 | <1e-300 |
| `number_of_arms` | 0.446 | abs_spearman | 77,947 | <1e-300 |
| `study_design_info/allocation` | 0.430 | eta | 61,818 | <1e-300 |
| `enrollment` | 0.303 | abs_spearman | 44,289 | <1e-300 |
| `intervention/intervention_name` | 0.265 | abs_spearman | 81,170 | <1e-300 |
| `Drug intervention Number` | 0.224 | abs_spearman | 81,170 | <1e-300 |
| `mortality_rate` | 0.221 | abs_spearman | 17,890 | 1.83e-196 |
| `sae_rate` | 0.209 | abs_spearman | 17,890 | 6.75e-175 |
| `phase` | 0.205 | eta | 81,170 | <1e-300 |
| `mortality_YN` | 0.155 | abs_spearman | 17,890 | 1.45e-95 |
| `Active Comparator Arm Number` | 0.141 | abs_spearman | 69,142 | <1e-300 |
| `dropout_YN` | 0.129 | abs_spearman | 38,218 | 8.64e-141 |
| `ipd_info_type-Clinical Study Report (CSR)` | 0.128 | abs_spearman | 2,145 | 5.06e-09 |
| `study_design_info/primary_purpose` | 0.121 | eta | 80,406 | 3.36e-247 |
| `sponsors/lead_sponsor/agency_class` | 0.118 | eta | 70,854 | 1.50e-215 |
| `Radiation intervention Number` | 0.118 | abs_spearman | 81,170 | 6.43e-249 |
| `execution_pass` | 0.099 | abs_spearman | 52,422 | 6.97e-113 |
| `execution_fail` | 0.099 | abs_spearman | 52,422 | 6.97e-113 |
| `location/facility/address/city` | 0.094 | abs_spearman | 81,170 | 4.38e-159 |
| `Procedure intervention Number` | 0.090 | abs_spearman | 70,854 | 1.23e-125 |
| `intervention_browse/mesh_term` | 0.089 | abs_spearman | 81,170 | 4.80e-143 |
| `Other intervention Number` | 0.088 | abs_spearman | 70,854 | 7.29e-122 |
| `duration_month` | 0.086 | abs_spearman | 42,635 | 1.50e-70 |
| `duration_day` | 0.086 | abs_spearman | 42,635 | 3.22e-70 |
| `duration_year` | 0.086 | abs_spearman | 42,635 | 3.22e-70 |
| `start_date` | 0.076 | abs_spearman | 42,635 | 8.72e-56 |
| `Other Arm Number` | 0.076 | abs_spearman | 77,947 | 3.47e-100 |
| `approval_outcome` | 0.074 | abs_spearman | 30,351 | 1.42e-37 |
| `failure_reason` | 0.069 | eta | 20,495 | 9.49e-21 |
| `Sham Comparator Arm Number` | 0.064 | abs_spearman | 69,142 | 5.76e-64 |
| `oversight_info/is_fda_regulated_device` | 0.060 | eta | 13,666 | 5.00e-12 |
| `oversight_info/has_dmc` | 0.060 | eta | 45,821 | 3.78e-37 |
| `ipd_info_type-Analytic Code` | 0.059 | abs_spearman | 2,297 | 0.0068 |
| `No Intervention Arm Number` | 0.057 | abs_spearman | 69,142 | 9.27e-50 |
| `eligibility/minimum_age` | 0.055 | abs_spearman | 79,096 | 2.61e-54 |
| `eligibility/gender` | 0.055 | eta | 70,854 | 5.16e-47 |

### `study_design_info/primary_purpose`   *(partners: 55)*

| partner | effect | metric | n_valid | p_adj |
|---------|--------|--------|---------|-------|
| `eligibility/healthy_volunteers` | 0.455 | cramers_v | 80,843 | <1e-300 |
| `Biological intervention Number` | 0.330 | eta | 80,983 | <1e-300 |
| `sae_YN` | 0.280 | eta | 17,911 | <1e-300 |
| `eligibility/maximum_age` | 0.233 | eta | 42,342 | <1e-300 |
| `sae_rate` | 0.208 | eta | 17,911 | 3.07e-165 |
| `mortality_YN` | 0.198 | eta | 17,911 | 2.85e-148 |
| `duration_month` | 0.195 | eta | 42,836 | <1e-300 |
| `duration_day` | 0.195 | eta | 42,836 | <1e-300 |
| `duration_year` | 0.195 | eta | 42,836 | <1e-300 |
| `phase` | 0.194 | cramers_v | 80,983 | <1e-300 |
| `Drug intervention Number` | 0.179 | eta | 80,983 | <1e-300 |
| `mortality_rate` | 0.169 | eta | 17,911 | 1.23e-105 |
| `dropout_YN` | 0.167 | eta | 37,812 | 2.88e-223 |
| `dropout_rate` | 0.164 | eta | 37,812 | 3.02e-216 |
| `condition_browse/mesh_term` | 0.162 | eta | 80,983 | <1e-300 |
| `study_design_info/intervention_model` | 0.142 | cramers_v | 80,137 | <1e-300 |
| `oversight_info/has_dmc` | 0.125 | cramers_v | 45,283 | 2.75e-147 |
| `patient_data/sharing_ipd` | 0.125 | cramers_v | 13,490 | 1.34e-78 |
| `study_design_info/masking_num` | 0.121 | eta | 80,406 | 3.36e-247 |
| `start_date` | 0.119 | eta | 42,836 | 4.27e-125 |
| `execution_pass` | 0.119 | eta | 52,095 | 4.42e-152 |
| `execution_fail` | 0.119 | eta | 52,095 | 4.42e-152 |
| `oversight_info/is_fda_regulated_device` | 0.116 | cramers_v | 13,675 | 7.56e-35 |
| `MaskingType-Participant` | 0.115 | eta | 80,406 | 4.45e-223 |
| `number_of_arms` | 0.114 | eta | 77,416 | 3.82e-211 |
| `enrollment` | 0.107 | eta | 43,857 | 1.37e-102 |
| `approval_outcome` | 0.107 | eta | 30,383 | 2.41e-69 |
| `study_design_info/allocation` | 0.105 | cramers_v | 61,425 | 2.25e-138 |
| `smiless` | 0.104 | eta | 80,983 | 2.04e-183 |
| `MaskingType-Investigator` | 0.103 | eta | 80,406 | 8.35e-179 |
| `MaskingType-Care Provider` | 0.100 | eta | 80,406 | 2.72e-168 |
| `oversight_info/is_fda_regulated_drug` | 0.099 | cramers_v | 13,761 | 9.45e-25 |
| `MaskingType-Outcomes Assessor` | 0.097 | eta | 80,406 | 3.15e-157 |
| `eligibility/gender` | 0.097 | cramers_v | 70,604 | 1.97e-268 |
| `intervention_browse/mesh_term` | 0.094 | eta | 80,983 | 1.05e-146 |
| `Experimental Arm Number` | 0.092 | eta | 77,416 | 9.05e-137 |
| `sponsors/lead_sponsor/agency_class` | 0.090 | cramers_v | 70,604 | <1e-300 |
| `Dietary Supplement intervention Number` | 0.089 | eta | 80,983 | 1.45e-131 |
| `icdcode` | 0.087 | eta | 80,983 | 1.85e-126 |
| `Device intervention Number` | 0.087 | eta | 70,604 | 1.74e-108 |
| `Active Comparator Arm Number` | 0.085 | eta | 68,722 | 5.04e-102 |
| `location/facility/address/city` | 0.084 | eta | 80,983 | 3.60e-117 |
| `Diagnostic Test intervention Number` | 0.083 | eta | 70,604 | 1.62e-97 |
| `Other Arm Number` | 0.082 | eta | 77,416 | 4.49e-106 |
| `condition` | 0.082 | eta | 80,983 | 8.09e-110 |
| `No Intervention Arm Number` | 0.078 | eta | 68,722 | 4.38e-85 |
| `Placebo Comparator Arm Number` | 0.077 | eta | 77,416 | 1.07e-93 |
| `Other intervention Number` | 0.075 | eta | 70,604 | 1.83e-80 |
| `responsible_party/responsible_party_type` | 0.069 | cramers_v | 67,490 | 9.70e-124 |
| `Procedure intervention Number` | 0.067 | eta | 70,604 | 1.62e-61 |
| `Behavioral intervention Number` | 0.066 | eta | 80,983 | 3.34e-70 |
| `study_design_info/masking` | 0.060 | cramers_v | 74,379 | <1e-300 |
| `Radiation intervention Number` | 0.058 | eta | 80,983 | 8.81e-53 |
| `failure_reason` | 0.055 | cramers_v | 20,561 | 8.34e-25 |
| `intervention/intervention_type` | 0.053 | eta | 80,983 | 1.05e-43 |

---

## Caveats

1. **Faithfulness assumption.** "No association ⇒ no direct edge" relies on faithfulness — i.e., no exact cancellation of multiple causal paths. Standard assumption in causal discovery.
2. **Marginal, not conditional.** This is a *marginal* association screen. Two features can be marginally associated through a chain `X → Z → Y` even if `X` and `Y` are conditionally independent given `Z`. The pair set here is therefore an over-approximation of the direct-edge set; the second stage (domain knowledge for direction) further prunes via mediation.
3. **Missing-data heterogeneity.** `n_valid` varies dramatically across pairs (e.g., `biology_pass` is missing in ~60% of rows). Low-`n_valid` pairs near the threshold should be read with caution.
4. **High-cardinality columns are coarsened.** Specific tokens of `condition`, `intervention/intervention_name`, etc., are not used in this screen — only `n_items` (token count, with 0 ⟺ NaN). Their richer semantic associations enter the DAG via domain knowledge in stage 2.
5. **Two columns dropped before this screen.** `study_type` is constant ('Interventional') across all 81,786 rows so contributes no association signal; `regulatory_pass` is definitionally identical (|ρ|=1.0) to `approval_outcome` on overlapping rows and was merged into `approval_outcome` as a single node. See the *Excluded columns* table above for the full exclusion list.
