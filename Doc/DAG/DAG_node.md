# TrialBench_joined DAG — Node Catalogue

Total nodes: **71**.


---

## Tier 0 — `design_top` (sponsor's primary design choices, set jointly at registration)  (9 nodes)

| Node | Dtype | Description |
|------|-------|-------------|
| `condition` | high_cardinality_text | Sponsor-reported disease / condition label (free-text). Tested in the association screen via token count. |
| `intervention/intervention_name` | high_cardinality_text | Specific intervention name(s) — drug brand / generic, device model, behavioral programme, etc. Tested via token count. |
| `intervention/intervention_type` | categorical_multivalued | Modality(ies) of intervention: Drug / Biological / Device / Behavioral / Procedure / Radiation / Dietary Supplement / Genetic / Diagnostic Test / Combination Product / Other. |
| `phase` | categorical | Clinical trial phase: Phase 1 / 2 / 3 / 4. Set at registration; reflects the drug-development maturity (first-in-human safety -> mid-stage efficacy -> pivotal -> post-market). |
| `sponsors/lead_sponsor/agency_class` | categorical | Sponsor class: INDUSTRY / NIH / U.S. Fed / OTHER (academic, foundation, hospital). |
| `study_design_info/allocation` | categorical | Randomized / Non-Randomized / N/A (N/A is consistent with single-group designs). |
| `study_design_info/intervention_model` | categorical | How participants are assigned to arms: Single Group / Parallel / Crossover / Factorial / Sequential. |
| `study_design_info/masking` | categorical | Blinding level: None (Open Label) / Single / Double / Triple / Quadruple, with the masked role(s) listed in parentheses. |
| `study_design_info/primary_purpose` | categorical | Primary purpose: Treatment / Prevention / Diagnostic / Supportive Care / Screening / Health Services Research / Basic Science / Device Feasibility / Other. |

---

## Tier 1 — `design_derived` (deterministic / coded artefacts of upstream design choices)  (27 nodes)

| Node | Dtype | Description |
|------|-------|-------------|
| `Active Comparator Arm Number` | float | Count of arms tagged 'Active Comparator'. |
| `Behavioral intervention Number` | float | Count of interventions tagged 'Behavioral'. |
| `Biological intervention Number` | float | Count of interventions tagged 'Biological'. |
| `Combination Product intervention Number` | float | Count of interventions tagged 'Combination Product'. |
| `Device intervention Number` | float | Count of interventions tagged 'Device'. |
| `Diagnostic Test intervention Number` | float | Count of interventions tagged 'Diagnostic Test'. |
| `Dietary Supplement intervention Number` | float | Count of interventions tagged 'Dietary Supplement'. |
| `Drug intervention Number` | float | Count of interventions tagged 'Drug'. |
| `Experimental Arm Number` | float | Count of arms tagged 'Experimental'. |
| `Genetic intervention Number` | float | Count of interventions tagged 'Genetic'. |
| `MaskingType-Care Provider` | indicator (0/1) | Care provider is masked. |
| `MaskingType-Investigator` | indicator (0/1) | Investigator is masked. |
| `MaskingType-Outcomes Assessor` | indicator (0/1) | Outcomes assessor is masked. |
| `MaskingType-Participant` | indicator (0/1) | Participant is masked. |
| `No Intervention Arm Number` | float | Count of arms tagged 'No Intervention'. |
| `Other Arm Number` | float | Count of arms tagged 'Other'. |
| `Other intervention Number` | float | Count of interventions tagged 'Other'. |
| `Placebo Comparator Arm Number` | float | Count of arms tagged 'Placebo Comparator'. |
| `Procedure intervention Number` | float | Count of interventions tagged 'Procedure'. |
| `Radiation intervention Number` | float | Count of interventions tagged 'Radiation'. |
| `Sham Comparator Arm Number` | float | Count of arms tagged 'Sham Comparator'. |
| `condition_browse/mesh_term` | high_cardinality_text | MeSH-normalized term(s) for the condition, looked up from `condition`. |
| `icdcode` | high_cardinality_text | ICD code(s) tagged from `condition` by an external annotation pipeline. |
| `intervention_browse/mesh_term` | high_cardinality_text | MeSH-normalized term(s) for the intervention name. |
| `number_of_arms` | float | Total number of arms in the trial. Sum of the six Arm Number columns. |
| `smiless` | high_cardinality_text | SMILES string(s) for drug intervention(s); NaN for non-drug interventions. |
| `study_design_info/masking_num` | float (0-4) | Count of masked roles; equals the sum of the four MaskingType-* indicators. |

---

## Tier 1 — `design_eligibility` (downstream-design: who is eligible to enrol)  (4 nodes)

| Node | Dtype | Description |
|------|-------|-------------|
| `eligibility/gender` | categorical | Eligible sex / gender: All / Male / Female. |
| `eligibility/healthy_volunteers` | categorical | Whether healthy volunteers are accepted: 'Accepts Healthy Volunteers' / 'No' / NaN. |
| `eligibility/maximum_age` | numeric (years, parsed) | Upper age bound parsed to years from strings like '65 Years' / '6 Months' / 'N/A'. |
| `eligibility/minimum_age` | numeric (years, parsed) | Lower age bound parsed to years. |

---

## Tier 1 — `design_oversight` (downstream-design: regulatory / monitoring / IPD-sharing policies)  (11 nodes)

| Node | Dtype | Description |
|------|-------|-------------|
| `has_expanded_access` | categorical (Yes/No) | Whether an expanded-access (compassionate use) program is associated with this drug. |
| `ipd_info_type-Analytic Code` | indicator (0/1) | Analytic code is among the shared IPD document types. |
| `ipd_info_type-Clinical Study Report (CSR)` | indicator (0/1) | Clinical Study Report is among the shared IPD document types. |
| `ipd_info_type-Informed Consent Form (ICF)` | indicator (0/1) | Informed Consent Form is among the shared IPD document types. |
| `ipd_info_type-Statistical Analysis Plan (SAP)` | indicator (0/1) | Statistical Analysis Plan is among the shared IPD document types. |
| `ipd_info_type-Study Protocol` | indicator (0/1) | Study Protocol is among the shared IPD document types. |
| `oversight_info/has_dmc` | categorical (Yes/No) | Whether the trial has an independent Data Monitoring Committee. |
| `oversight_info/is_fda_regulated_device` | categorical (Yes/No) | Whether the trial falls under FDA device regulation. |
| `oversight_info/is_fda_regulated_drug` | categorical (Yes/No) | Whether the trial falls under FDA drug regulation. |
| `patient_data/sharing_ipd` | categorical | Plan for sharing Individual Participant Data: Yes / No / Undecided. |
| `responsible_party/responsible_party_type` | categorical | Who is responsible for the trial: Sponsor / Sponsor-Investigator / Principal Investigator. |

---

## Tier 1 — `design_planning` (planning fields: enrolment target, start date, sites, title)  (4 nodes)

| Node | Dtype | Description |
|------|-------|-------------|
| `brief_title` | high_cardinality_text | Short sponsor-authored title (free text). |
| `enrollment` | float | Planned (or actual-reported) participant enrollment count. |
| `location/facility/address/city` | high_cardinality_text | City/cities where the trial is conducted (tested via token count). |
| `start_date` | date (parsed to days) | Reported start date of the trial; parsed to days since 2000-01-01. |

---

## Tier 2 — `outcome_timing` (observed trial timing)  (4 nodes)

| Node | Dtype | Description |
|------|-------|-------------|
| `completion_date` | date (parsed to days) | Reported completion date of the trial. |
| `duration_day` | float | Total trial duration in days = completion_date - start_date. |
| `duration_month` | float | Total trial duration in months (duration_day / 30.44). |
| `duration_year` | float | Total trial duration in years (duration_day / 365.25). |

---

## Tier 3 — `outcome_safety` (observed safety / dropout outcomes)  (6 nodes)

| Node | Dtype | Description |
|------|-------|-------------|
| `dropout_YN` | float (0/1) | Binary indicator: above-threshold dropout rate occurred. |
| `dropout_rate` | float [0,1] | Observed patient-dropout rate. |
| `mortality_YN` | float (0/1) | Binary indicator: above-threshold mortality rate occurred. |
| `mortality_rate` | float [0,1] | Observed mortality rate. |
| `sae_YN` | float (0/1) | Binary indicator: above-threshold serious-adverse-event rate occurred. |
| `sae_rate` | float [0,1] | Observed serious-adverse-event rate. |

---

## Tier 4 — `outcome_label` (post-hoc trial-success labels)  (6 nodes)

| Node | Dtype | Description |
|------|-------|-------------|
| `approval_outcome` | float (0/1) | Whether the trial result led to a successful drug/device approval. Merged with `regulatory_pass` (effect=1.0, definitionally identical). |
| `biology_fail` | boolean | NOT(biology_pass). Definitional negation. |
| `biology_pass` | boolean | True if the intervention met its primary biological efficacy endpoint. |
| `execution_fail` | boolean | NOT(execution_pass). Definitional negation. |
| `execution_pass` | boolean | True if the trial executed without operational failure (e.g., enrolled, completed). |
| `failure_reason` | categorical | Reason a trial failed: 'poor enrollment' / 'efficacy' / 'safety' / 'Others' / NaN (no failure or unknown). |

---

## Reference: 10 columns excluded from the DAG

These columns are present in the source parquet but were not retained as DAG nodes (see `association.md` § *Excluded columns* for the full rationale):

| Excluded column | Reason |
|-----------------|--------|
| `brief_summary/textblock` | free-text trial summary |
| `eligibility/criteria/textblock` | free-text eligibility criteria |
| `intervention/description` | free-text intervention description |
| `detailed_description/textblock` | free-text long description |
| `study_design_info/intervention_model_description` | free-text annotation on intervention_model |
| `study_design_info/masking_description` | free-text annotation on masking |
| `eligibility/gender_description` | free-text annotation on eligibility/gender |
| `keyword` | free-text keyword list with no fixed vocabulary |
| `study_type` | constant 'Interventional' in all 81,786 rows; zero variance, zero associated partners |
| `regulatory_pass` | identical (|rho|=1.0) to `approval_outcome` on overlapping rows; merged into `approval_outcome` as a single node |
