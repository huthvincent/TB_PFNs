"""ci_build_dag.py — Stage 2 of the CI pipeline.

Reads the latest ci_pairwise_association_*/pairwise_associated.csv (1,169 pairs
that passed effect_size > 0.05 AND BH-FDR p < 0.01) and classifies each pair
into one of three categories based on clinical-trial domain knowledge alone
(no data peeking):

    1. directed edge A -> B (causal)
    2. directed edge B -> A
    3. associated but no direct causal edge — either sibling under a common
       cause in the DAG, mediated through other nodes already present, or
       jointly-determined sponsor design choices.

Source-of-truth in this file (hand-authored):
    NODE_METADATA          : per-node (id, group, dtype, description) — 71 entries
    EXPLICIT_DIRECT_EDGES  : explicit causal edges with mechanism + rationale
    EXPLICIT_NO_DIRECT     : explicit associated-but-no-direct pairs with reason
    GROUP_TIER             : 4-tier ordering (design_top, downstream_design,
                             timing, safety, label) for the default rule
    DEFAULT_MECHANISM      : (src_tier, tgt_tier) -> default mechanism label

Default rule (applies only when neither EXPLICIT_DIRECT_EDGES nor
EXPLICIT_NO_DIRECT mentions the pair):
    - both nodes same tier  -> no_direct (sibling / joint design choice)
    - cross-tier            -> edge from lower-tier node to higher-tier node,
                               mechanism from DEFAULT_MECHANISM, rationale
                               from a short template.

Output:
    /data2/zhu11/TB/CI/DAG.json
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import pandas as pd

RESULTS_ROOT = Path("/data2/zhu11/TB/results")
OUT_PATH = Path("/data2/zhu11/TB/CI/DAG.json")


# ============================================================================
# 1. NODE METADATA (71 entries)
# ============================================================================

NODE_METADATA: dict[str, dict] = {
    # ---- design_top ----
    "phase": {
        "group": "design_top", "dtype": "categorical",
        "description": "Clinical trial phase: Phase 1 / 2 / 3 / 4. Set at registration; reflects the drug-development maturity (first-in-human safety -> mid-stage efficacy -> pivotal -> post-market).",
    },
    "study_design_info/primary_purpose": {
        "group": "design_top", "dtype": "categorical",
        "description": "Primary purpose: Treatment / Prevention / Diagnostic / Supportive Care / Screening / Health Services Research / Basic Science / Device Feasibility / Other.",
    },
    "study_design_info/intervention_model": {
        "group": "design_top", "dtype": "categorical",
        "description": "How participants are assigned to arms: Single Group / Parallel / Crossover / Factorial / Sequential.",
    },
    "study_design_info/allocation": {
        "group": "design_top", "dtype": "categorical",
        "description": "Randomized / Non-Randomized / N/A (N/A is consistent with single-group designs).",
    },
    "study_design_info/masking": {
        "group": "design_top", "dtype": "categorical",
        "description": "Blinding level: None (Open Label) / Single / Double / Triple / Quadruple, with the masked role(s) listed in parentheses.",
    },
    "intervention/intervention_type": {
        "group": "design_top", "dtype": "categorical_multivalued",
        "description": "Modality(ies) of intervention: Drug / Biological / Device / Behavioral / Procedure / Radiation / Dietary Supplement / Genetic / Diagnostic Test / Combination Product / Other.",
    },
    "condition": {
        "group": "design_top", "dtype": "high_cardinality_text",
        "description": "Sponsor-reported disease / condition label (free-text). Tested in the association screen via token count.",
    },
    "intervention/intervention_name": {
        "group": "design_top", "dtype": "high_cardinality_text",
        "description": "Specific intervention name(s) — drug brand / generic, device model, behavioral programme, etc. Tested via token count.",
    },
    "sponsors/lead_sponsor/agency_class": {
        "group": "design_top", "dtype": "categorical",
        "description": "Sponsor class: INDUSTRY / NIH / U.S. Fed / OTHER (academic, foundation, hospital).",
    },

    # ---- design_eligibility ----
    "eligibility/gender": {
        "group": "design_eligibility", "dtype": "categorical",
        "description": "Eligible sex / gender: All / Male / Female.",
    },
    "eligibility/healthy_volunteers": {
        "group": "design_eligibility", "dtype": "categorical",
        "description": "Whether healthy volunteers are accepted: 'Accepts Healthy Volunteers' / 'No' / NaN.",
    },
    "eligibility/maximum_age": {
        "group": "design_eligibility", "dtype": "numeric (years, parsed)",
        "description": "Upper age bound parsed to years from strings like '65 Years' / '6 Months' / 'N/A'.",
    },
    "eligibility/minimum_age": {
        "group": "design_eligibility", "dtype": "numeric (years, parsed)",
        "description": "Lower age bound parsed to years.",
    },

    # ---- design_oversight ----
    "responsible_party/responsible_party_type": {
        "group": "design_oversight", "dtype": "categorical",
        "description": "Who is responsible for the trial: Sponsor / Sponsor-Investigator / Principal Investigator.",
    },
    "oversight_info/has_dmc": {
        "group": "design_oversight", "dtype": "categorical (Yes/No)",
        "description": "Whether the trial has an independent Data Monitoring Committee.",
    },
    "oversight_info/is_fda_regulated_device": {
        "group": "design_oversight", "dtype": "categorical (Yes/No)",
        "description": "Whether the trial falls under FDA device regulation.",
    },
    "oversight_info/is_fda_regulated_drug": {
        "group": "design_oversight", "dtype": "categorical (Yes/No)",
        "description": "Whether the trial falls under FDA drug regulation.",
    },
    "has_expanded_access": {
        "group": "design_oversight", "dtype": "categorical (Yes/No)",
        "description": "Whether an expanded-access (compassionate use) program is associated with this drug.",
    },
    "patient_data/sharing_ipd": {
        "group": "design_oversight", "dtype": "categorical",
        "description": "Plan for sharing Individual Participant Data: Yes / No / Undecided.",
    },
    "ipd_info_type-Analytic Code": {
        "group": "design_oversight", "dtype": "indicator (0/1)",
        "description": "Analytic code is among the shared IPD document types.",
    },
    "ipd_info_type-Clinical Study Report (CSR)": {
        "group": "design_oversight", "dtype": "indicator (0/1)",
        "description": "Clinical Study Report is among the shared IPD document types.",
    },
    "ipd_info_type-Informed Consent Form (ICF)": {
        "group": "design_oversight", "dtype": "indicator (0/1)",
        "description": "Informed Consent Form is among the shared IPD document types.",
    },
    "ipd_info_type-Statistical Analysis Plan (SAP)": {
        "group": "design_oversight", "dtype": "indicator (0/1)",
        "description": "Statistical Analysis Plan is among the shared IPD document types.",
    },
    "ipd_info_type-Study Protocol": {
        "group": "design_oversight", "dtype": "indicator (0/1)",
        "description": "Study Protocol is among the shared IPD document types.",
    },

    # ---- design_derived ----
    "condition_browse/mesh_term": {
        "group": "design_derived", "dtype": "high_cardinality_text",
        "description": "MeSH-normalized term(s) for the condition, looked up from `condition`.",
    },
    "icdcode": {
        "group": "design_derived", "dtype": "high_cardinality_text",
        "description": "ICD code(s) tagged from `condition` by an external annotation pipeline.",
    },
    "intervention_browse/mesh_term": {
        "group": "design_derived", "dtype": "high_cardinality_text",
        "description": "MeSH-normalized term(s) for the intervention name.",
    },
    "smiless": {
        "group": "design_derived", "dtype": "high_cardinality_text",
        "description": "SMILES string(s) for drug intervention(s); NaN for non-drug interventions.",
    },
    "study_design_info/masking_num": {
        "group": "design_derived", "dtype": "float (0-4)",
        "description": "Count of masked roles; equals the sum of the four MaskingType-* indicators.",
    },
    "MaskingType-Care Provider": {
        "group": "design_derived", "dtype": "indicator (0/1)",
        "description": "Care provider is masked.",
    },
    "MaskingType-Investigator": {
        "group": "design_derived", "dtype": "indicator (0/1)",
        "description": "Investigator is masked.",
    },
    "MaskingType-Outcomes Assessor": {
        "group": "design_derived", "dtype": "indicator (0/1)",
        "description": "Outcomes assessor is masked.",
    },
    "MaskingType-Participant": {
        "group": "design_derived", "dtype": "indicator (0/1)",
        "description": "Participant is masked.",
    },
    "number_of_arms": {
        "group": "design_derived", "dtype": "float",
        "description": "Total number of arms in the trial. Sum of the six Arm Number columns.",
    },
    "Active Comparator Arm Number": {
        "group": "design_derived", "dtype": "float",
        "description": "Count of arms tagged 'Active Comparator'.",
    },
    "Experimental Arm Number": {
        "group": "design_derived", "dtype": "float",
        "description": "Count of arms tagged 'Experimental'.",
    },
    "No Intervention Arm Number": {
        "group": "design_derived", "dtype": "float",
        "description": "Count of arms tagged 'No Intervention'.",
    },
    "Other Arm Number": {
        "group": "design_derived", "dtype": "float",
        "description": "Count of arms tagged 'Other'.",
    },
    "Placebo Comparator Arm Number": {
        "group": "design_derived", "dtype": "float",
        "description": "Count of arms tagged 'Placebo Comparator'.",
    },
    "Sham Comparator Arm Number": {
        "group": "design_derived", "dtype": "float",
        "description": "Count of arms tagged 'Sham Comparator'.",
    },
    "Behavioral intervention Number": {
        "group": "design_derived", "dtype": "float",
        "description": "Count of interventions tagged 'Behavioral'.",
    },
    "Biological intervention Number": {
        "group": "design_derived", "dtype": "float",
        "description": "Count of interventions tagged 'Biological'.",
    },
    "Combination Product intervention Number": {
        "group": "design_derived", "dtype": "float",
        "description": "Count of interventions tagged 'Combination Product'.",
    },
    "Device intervention Number": {
        "group": "design_derived", "dtype": "float",
        "description": "Count of interventions tagged 'Device'.",
    },
    "Diagnostic Test intervention Number": {
        "group": "design_derived", "dtype": "float",
        "description": "Count of interventions tagged 'Diagnostic Test'.",
    },
    "Dietary Supplement intervention Number": {
        "group": "design_derived", "dtype": "float",
        "description": "Count of interventions tagged 'Dietary Supplement'.",
    },
    "Drug intervention Number": {
        "group": "design_derived", "dtype": "float",
        "description": "Count of interventions tagged 'Drug'.",
    },
    "Genetic intervention Number": {
        "group": "design_derived", "dtype": "float",
        "description": "Count of interventions tagged 'Genetic'.",
    },
    "Other intervention Number": {
        "group": "design_derived", "dtype": "float",
        "description": "Count of interventions tagged 'Other'.",
    },
    "Procedure intervention Number": {
        "group": "design_derived", "dtype": "float",
        "description": "Count of interventions tagged 'Procedure'.",
    },
    "Radiation intervention Number": {
        "group": "design_derived", "dtype": "float",
        "description": "Count of interventions tagged 'Radiation'.",
    },

    # ---- design_planning ----
    "enrollment": {
        "group": "design_planning", "dtype": "float",
        "description": "Planned (or actual-reported) participant enrollment count.",
    },
    "start_date": {
        "group": "design_planning", "dtype": "date (parsed to days)",
        "description": "Reported start date of the trial; parsed to days since 2000-01-01.",
    },
    "location/facility/address/city": {
        "group": "design_planning", "dtype": "high_cardinality_text",
        "description": "City/cities where the trial is conducted (tested via token count).",
    },
    "brief_title": {
        "group": "design_planning", "dtype": "high_cardinality_text",
        "description": "Short sponsor-authored title (free text).",
    },

    # ---- outcome_timing ----
    "completion_date": {
        "group": "outcome_timing", "dtype": "date (parsed to days)",
        "description": "Reported completion date of the trial.",
    },
    "duration_day": {
        "group": "outcome_timing", "dtype": "float",
        "description": "Total trial duration in days = completion_date - start_date.",
    },
    "duration_month": {
        "group": "outcome_timing", "dtype": "float",
        "description": "Total trial duration in months (duration_day / 30.44).",
    },
    "duration_year": {
        "group": "outcome_timing", "dtype": "float",
        "description": "Total trial duration in years (duration_day / 365.25).",
    },

    # ---- outcome_safety ----
    "dropout_YN": {
        "group": "outcome_safety", "dtype": "float (0/1)",
        "description": "Binary indicator: above-threshold dropout rate occurred.",
    },
    "dropout_rate": {
        "group": "outcome_safety", "dtype": "float [0,1]",
        "description": "Observed patient-dropout rate.",
    },
    "sae_YN": {
        "group": "outcome_safety", "dtype": "float (0/1)",
        "description": "Binary indicator: above-threshold serious-adverse-event rate occurred.",
    },
    "sae_rate": {
        "group": "outcome_safety", "dtype": "float [0,1]",
        "description": "Observed serious-adverse-event rate.",
    },
    "mortality_YN": {
        "group": "outcome_safety", "dtype": "float (0/1)",
        "description": "Binary indicator: above-threshold mortality rate occurred.",
    },
    "mortality_rate": {
        "group": "outcome_safety", "dtype": "float [0,1]",
        "description": "Observed mortality rate.",
    },

    # ---- outcome_label ----
    "failure_reason": {
        "group": "outcome_label", "dtype": "categorical",
        "description": "Reason a trial failed: 'poor enrollment' / 'efficacy' / 'safety' / 'Others' / NaN (no failure or unknown).",
    },
    "approval_outcome": {
        "group": "outcome_label", "dtype": "float (0/1)",
        "description": "Whether the trial result led to a successful drug/device approval. Merged with `regulatory_pass` (effect=1.0, definitionally identical).",
    },
    "execution_pass": {
        "group": "outcome_label", "dtype": "boolean",
        "description": "True if the trial executed without operational failure (e.g., enrolled, completed).",
    },
    "execution_fail": {
        "group": "outcome_label", "dtype": "boolean",
        "description": "NOT(execution_pass). Definitional negation.",
    },
    "biology_pass": {
        "group": "outcome_label", "dtype": "boolean",
        "description": "True if the intervention met its primary biological efficacy endpoint.",
    },
    "biology_fail": {
        "group": "outcome_label", "dtype": "boolean",
        "description": "NOT(biology_pass). Definitional negation.",
    },
}


# ============================================================================
# 2. TIER ORDERING (default rule)
# ============================================================================

GROUP_TIER = {
    "design_top":         0,   # sponsor design choices set jointly at registration
    "design_eligibility": 1,   # downstream-design tier — siblings of design_top
    "design_oversight":   1,
    "design_derived":     1,
    "design_planning":    1,
    "outcome_timing":     2,   # observed trial timing
    "outcome_safety":     3,   # observed safety outcomes
    "outcome_label":      4,   # post-hoc trial-success labels
}

DEFAULT_MECHANISM = {
    # (src_tier, tgt_tier) -> mechanism string for default cross-tier edges
    (0, 1): "design_choice",       # sponsor design top -> downstream design
    (0, 2): "design_choice",       # design top -> timing
    (0, 3): "biological",          # design top -> safety
    (0, 4): "biological",          # design top -> label
    (1, 2): "operational",         # downstream design -> timing
    (1, 3): "biological",          # downstream design -> safety
    (1, 4): "biological",          # downstream design -> label
    (2, 3): "operational",         # timing -> safety (longer trial -> more events)
    (2, 4): "operational",         # timing -> label
    (3, 4): "biological",          # safety -> label (sae -> biology_fail / failure_reason)
}

GROUP_DEFAULT_RATIONALE = {
    # (src_tier, tgt_tier) -> short template rationale
    (0, 1): "Sponsor design decision made at registration ({src}) that constrains a downstream design field ({tgt}).",
    (0, 2): "Sponsor design decision ({src}) that drives the realised trial-duration timeline ({tgt}).",
    (0, 3): "Sponsor design decision ({src}) that influences the realised safety outcome ({tgt}) through biology, population, or operations.",
    (0, 4): "Sponsor design decision ({src}) that influences the trial-success label ({tgt}) through the trial's biological and regulatory pathway.",
    (1, 2): "Downstream-design field ({src}) shifts the operational timeline of the trial ({tgt}).",
    (1, 3): "Downstream-design field ({src}) shifts the realised safety outcome ({tgt}) through population biology or trial operations.",
    (1, 4): "Downstream-design field ({src}) feeds the trial-success label ({tgt}) through biology, execution, or regulatory pathways.",
    (2, 3): "Longer / later trial timing ({src}) accrues more events, raising the realised safety outcome ({tgt}).",
    (2, 4): "Trial timing ({src}) propagates into the post-hoc trial-success label ({tgt}).",
    (3, 4): "Realised safety outcome ({src}) feeds the trial-success label ({tgt}) directly (e.g., 'safety' failure category, regulatory rejection).",
}


# ============================================================================
# 3. EXPLICIT DIRECT EDGES (within-group + cross-group exceptions)
# ============================================================================

# Each entry: (src, tgt, mechanism, rationale).
# Rationale must be domain-knowledge-based (no reference to data values).

EXPLICIT_DIRECT_EDGES: list[tuple[str, str, str, str]] = [
    # ---- Within design_top (sponsor design constraints) ----
    ("study_design_info/intervention_model", "study_design_info/allocation", "design_constraint",
     "Single Group Assignment forces allocation='N/A'; Parallel / Crossover / Factorial designs require Randomized or Non-Randomized allocation. The intervention model strictly constrains the feasible allocation."),
    ("phase", "study_design_info/intervention_model", "design_choice",
     "Phase 1 first-in-human trials are predominantly Single Group Assignment (no comparator yet); Phase 3 pivotal trials are Parallel Assignment for randomised comparison. Phase shapes the model choice."),
    ("phase", "study_design_info/allocation", "design_choice",
     "Phase 1 trials are usually non-randomised single-group; Phase 3 trials are typically randomised. Phase drives the allocation decision."),
    ("phase", "study_design_info/masking", "design_choice",
     "Phase 1 trials are commonly Open Label; Phase 3 confirmatory trials are commonly Double / Quadruple blinded. Phase drives the masking choice."),
    ("phase", "study_design_info/primary_purpose", "design_choice",
     "Phase 1 skews Treatment / Basic Science; Phase 4 picks up Supportive Care / Health Services Research. Phase shifts the typical purpose distribution."),
    ("condition", "study_design_info/primary_purpose", "design_choice",
     "The disease being studied directly determines whether a sponsor designs a Treatment, Prevention, Diagnostic, or Screening trial."),
    ("study_design_info/primary_purpose", "intervention/intervention_type", "design_constraint",
     "Diagnostic primary purpose forces intervention_type='Diagnostic Test'; Treatment is realised through Drug / Biological / Device / Behavioral / Procedure. Purpose constrains the feasible type set."),
    ("intervention/intervention_type", "intervention/intervention_name", "design_constraint",
     "The intervention type (Drug / Device / Behavioral / ...) coarsens the intervention name; a row with type='Device' has a name in the device-model space."),

    # ---- Within design_oversight (definitional/derived from the same sponsor policy) ----
    # patient_data/sharing_ipd -> ipd_info_type-* edges did NOT pass the screen, so we do not
    # add them here. They are mediated through sample-conditional rendering of "Yes" sub-rows.

    # ---- Within design_derived (sum constraints) ----
    ("MaskingType-Care Provider",     "study_design_info/masking_num", "deterministic",
     "masking_num is the sum of the four MaskingType-* indicators; this term is one summand."),
    ("MaskingType-Investigator",      "study_design_info/masking_num", "deterministic",
     "masking_num is the sum of the four MaskingType-* indicators; this term is one summand."),
    ("MaskingType-Outcomes Assessor", "study_design_info/masking_num", "deterministic",
     "masking_num is the sum of the four MaskingType-* indicators; this term is one summand."),
    ("MaskingType-Participant",       "study_design_info/masking_num", "deterministic",
     "masking_num is the sum of the four MaskingType-* indicators; this term is one summand."),
    ("Active Comparator Arm Number",  "number_of_arms", "deterministic",
     "number_of_arms is the sum of the six Arm-Number columns; this term is one summand."),
    ("Experimental Arm Number",       "number_of_arms", "deterministic",
     "number_of_arms is the sum of the six Arm-Number columns; this term is one summand."),
    ("No Intervention Arm Number",    "number_of_arms", "deterministic",
     "number_of_arms is the sum of the six Arm-Number columns; this term is one summand."),
    ("Other Arm Number",              "number_of_arms", "deterministic",
     "number_of_arms is the sum of the six Arm-Number columns; this term is one summand."),
    ("Placebo Comparator Arm Number", "number_of_arms", "deterministic",
     "number_of_arms is the sum of the six Arm-Number columns; this term is one summand."),
    ("Sham Comparator Arm Number",    "number_of_arms", "deterministic",
     "number_of_arms is the sum of the six Arm-Number columns; this term is one summand."),

    # ---- Within outcome_timing (unit conversion) ----
    ("duration_day", "duration_month", "deterministic",
     "Unit conversion: duration_month = duration_day / 30.44."),
    ("duration_day", "duration_year", "deterministic",
     "Unit conversion: duration_year = duration_day / 365.25."),

    # ---- Within outcome_safety (definitional / inclusion / biology) ----
    ("mortality_rate", "mortality_YN", "deterministic",
     "mortality_YN is the thresholded version of mortality_rate."),
    ("sae_rate",       "sae_YN",       "deterministic",
     "sae_YN is the thresholded version of sae_rate."),
    ("dropout_rate",   "dropout_YN",   "deterministic",
     "dropout_YN is the thresholded version of dropout_rate."),
    ("mortality_rate", "sae_rate",     "definitional",
     "ICH-GCP defines death as a serious adverse event, so mortality is a strict subset of SAE: any death contributes to sae_rate."),
    ("mortality_rate", "dropout_rate", "definitional",
     "Deaths are by definition dropouts (the participant can no longer continue), so mortality contributes to dropout_rate."),
    ("sae_rate",       "dropout_rate", "biological",
     "Participants with serious adverse events frequently withdraw from the trial (either by choice or by protocol mandate); SAEs are a causal driver of dropout."),

    # ---- Within outcome_label (definitional negations + preconditions) ----
    ("biology_pass",   "biology_fail",       "deterministic",
     "biology_fail = NOT biology_pass (definitional negation)."),
    ("execution_pass", "execution_fail",     "deterministic",
     "execution_fail = NOT execution_pass (definitional negation)."),
    ("failure_reason", "biology_pass",       "definitional",
     "TrialBench encodes biology_pass = False iff failure_reason in {'efficacy', 'safety'}; the categorical failure_reason directly populates the boolean."),
    ("failure_reason", "execution_pass",     "definitional",
     "TrialBench encodes execution_pass = False iff failure_reason = 'poor enrollment' (and related execution categories); failure_reason directly populates the boolean."),
    ("biology_pass",   "approval_outcome",   "regulatory",
     "Meeting the primary biological efficacy endpoint is a precondition for regulatory approval; biology_pass is the gating biology factor in approval_outcome."),
    ("execution_pass", "approval_outcome",   "operational",
     "A trial that fails to execute (recruit, complete) cannot deliver the evidence for regulatory submission; execution_pass is a precondition for approval_outcome."),

    # ---- Cross-tier deterministic / definitional edges (need explicit mechanism + rationale) ----
    # condition -> design_derived codes
    ("condition", "condition_browse/mesh_term", "definitional",
     "condition_browse/mesh_term is the MeSH-vocabulary normalisation of the free-text condition; the codes are looked up from the condition string."),
    ("condition", "icdcode", "definitional",
     "ICD codes are tagged from the condition text by an external annotation pipeline."),

    # intervention/intervention_name -> design_derived codes
    ("intervention/intervention_name", "intervention_browse/mesh_term", "definitional",
     "intervention_browse/mesh_term is the MeSH-vocabulary normalisation of the free-text intervention name."),
    ("intervention/intervention_name", "smiless", "definitional",
     "SMILES strings are looked up from the drug name; NaN for non-small-molecule interventions."),

    # intervention/intervention_type -> per-type tally columns (11 deterministic edges)
    ("intervention/intervention_type", "Behavioral intervention Number", "deterministic",
     "Per-type intervention count is a tally over intervention_type's multi-valued list."),
    ("intervention/intervention_type", "Biological intervention Number", "deterministic",
     "Per-type intervention count is a tally over intervention_type's multi-valued list."),
    ("intervention/intervention_type", "Combination Product intervention Number", "deterministic",
     "Per-type intervention count is a tally over intervention_type's multi-valued list."),
    ("intervention/intervention_type", "Device intervention Number", "deterministic",
     "Per-type intervention count is a tally over intervention_type's multi-valued list."),
    ("intervention/intervention_type", "Diagnostic Test intervention Number", "deterministic",
     "Per-type intervention count is a tally over intervention_type's multi-valued list."),
    ("intervention/intervention_type", "Dietary Supplement intervention Number", "deterministic",
     "Per-type intervention count is a tally over intervention_type's multi-valued list."),
    ("intervention/intervention_type", "Drug intervention Number", "deterministic",
     "Per-type intervention count is a tally over intervention_type's multi-valued list."),
    ("intervention/intervention_type", "Genetic intervention Number", "deterministic",
     "Per-type intervention count is a tally over intervention_type's multi-valued list."),
    ("intervention/intervention_type", "Other intervention Number", "deterministic",
     "Per-type intervention count is a tally over intervention_type's multi-valued list."),
    ("intervention/intervention_type", "Procedure intervention Number", "deterministic",
     "Per-type intervention count is a tally over intervention_type's multi-valued list."),
    ("intervention/intervention_type", "Radiation intervention Number", "deterministic",
     "Per-type intervention count is a tally over intervention_type's multi-valued list."),

    # study_design_info/masking -> 4 MaskingType-* indicators (deterministic role extraction)
    ("study_design_info/masking", "MaskingType-Care Provider", "deterministic",
     "Indicator is 1 iff 'Care Provider' appears in the parenthesised role list of the masking string."),
    ("study_design_info/masking", "MaskingType-Investigator", "deterministic",
     "Indicator is 1 iff 'Investigator' appears in the parenthesised role list of the masking string."),
    ("study_design_info/masking", "MaskingType-Outcomes Assessor", "deterministic",
     "Indicator is 1 iff 'Outcomes Assessor' appears in the parenthesised role list of the masking string."),
    ("study_design_info/masking", "MaskingType-Participant", "deterministic",
     "Indicator is 1 iff 'Participant' appears in the parenthesised role list of the masking string."),

    # study_design_info/masking -> masking_num (cross-group deterministic, even though one path goes via 4 indicators)
    ("study_design_info/masking", "study_design_info/masking_num", "deterministic",
     "masking_num is the count of masked roles encoded in the masking string."),

    # study_design_info/intervention_model -> number_of_arms (constraint)
    ("study_design_info/intervention_model", "number_of_arms", "design_constraint",
     "'Single Group Assignment' forces number_of_arms=1; 'Parallel' / 'Crossover' force >=2; 'Factorial' typically >=4. The intervention model strictly constrains the number of arms."),

    # intervention/intervention_type -> FDA regulation
    ("intervention/intervention_type", "oversight_info/is_fda_regulated_drug", "regulatory",
     "Type in {Drug, Biological} triggers FDA drug regulation (NDA / BLA pathway) by definition."),
    ("intervention/intervention_type", "oversight_info/is_fda_regulated_device", "regulatory",
     "Type in {Device, Combination Product} triggers FDA device regulation (PMA / 510(k) pathway)."),
    ("intervention/intervention_type", "has_expanded_access", "regulatory",
     "Expanded-access (compassionate use) programmes apply almost exclusively to Drug / Biological interventions; intervention type gates the feasibility of expanded access."),

    # start_date + completion_date -> duration_day (deterministic)
    ("start_date",      "duration_day", "deterministic",
     "duration_day = completion_date - start_date (in days)."),
    ("completion_date", "duration_day", "deterministic",
     "duration_day = completion_date - start_date (in days)."),

    # start_date -> completion_date (operational ordering)
    ("start_date", "completion_date", "operational",
     "The trial cannot complete before it has started; start_date temporally precedes completion_date."),

    # enrollment -> completion_date / duration (operational)
    ("enrollment", "completion_date", "operational",
     "Larger planned enrollment requires a longer recruitment window plus follow-up, pushing completion_date later."),
    ("enrollment", "duration_day", "operational",
     "Larger N requires more recruitment time and (typically) longer follow-up; enrollment is a direct driver of trial duration."),

    # phase -> enrollment (sample-size design choice)
    ("phase", "enrollment", "design_choice",
     "Phase 1 sizes trials at tens; Phase 2 ~100; Phase 3 hundreds-to-thousands; Phase 4 large pragmatic cohorts. Phase is the dominant design driver of N."),

    # condition / intervention -> outcomes (biological cascade)
    ("condition", "mortality_rate", "biological",
     "Background disease mortality differs by orders of magnitude across conditions (oncology vs migraine); condition drives the realised mortality rate."),
    ("condition", "sae_rate", "biological",
     "Disease-related adverse events differ across conditions, shifting the realised SAE rate."),

    # intervention/intervention_type -> safety outcomes (biological)
    ("intervention/intervention_type", "sae_rate", "biological",
     "Drug / Biological / Device / Behavioral interventions have systematically different safety profiles by mechanism of action."),
    ("intervention/intervention_type", "mortality_rate", "biological",
     "Cytotoxic Drugs (e.g., oncology) carry mortality footprint that Behavioral interventions do not; type drives realised mortality."),

    # eligibility/healthy_volunteers -> safety
    ("eligibility/healthy_volunteers", "sae_rate", "biological",
     "Healthy-volunteer trials show systematically lower SAE rates than diseased-population trials (no disease-driven AE component)."),
    ("eligibility/healthy_volunteers", "mortality_rate", "biological",
     "Healthy-volunteer trials have near-zero background mortality."),

    # eligibility age -> safety
    ("eligibility/maximum_age", "sae_rate", "biological",
     "Older eligibility envelopes admit more comorbid participants and elevate background SAE rate."),
    ("eligibility/maximum_age", "mortality_rate", "biological",
     "Older eligibility envelopes raise background mortality."),
    ("eligibility/minimum_age", "sae_rate", "biological",
     "Pediatric vs adult eligibility shifts the SAE landscape (different physiology, different reporting culture)."),

    # oversight_info/has_dmc -> safety / execution (early stopping)
    ("oversight_info/has_dmc", "sae_rate", "operational",
     "An active Data Monitoring Committee enforces early-stopping rules for safety, truncating realised SAE rates."),
    ("oversight_info/has_dmc", "mortality_rate", "operational",
     "DMC-driven futility / safety stops cap accrued mortality before the protocol-defined endpoint."),
    ("oversight_info/has_dmc", "execution_pass", "operational",
     "A functioning DMC catches operational issues mid-trial and improves the chance of successful execution."),

    # FDA regulation -> approval_outcome
    ("oversight_info/is_fda_regulated_drug", "approval_outcome", "regulatory",
     "FDA drug regulation is the gating mechanism for drug approval; trials outside this pathway cannot yield an FDA drug approval."),
    ("oversight_info/is_fda_regulated_device", "approval_outcome", "regulatory",
     "FDA device regulation gates device approval (PMA / 510(k) pathway)."),

    # sae -> failure_reason / biology_pass (clinical mechanism)
    ("sae_YN",   "failure_reason", "biological",
     "A substantial SAE incidence drives the trial to be terminated for safety, populating failure_reason='safety'."),
    ("sae_rate", "biology_pass",   "biological",
     "An unacceptable SAE rate forces biology_pass=False via the 'safety' failure category."),

    # duration_day -> safety outcomes (longer follow-up accrues more events)
    ("duration_day", "sae_rate", "operational",
     "Longer follow-up accumulates more adverse events; realised SAE rate increases with duration."),
    ("duration_day", "mortality_rate", "operational",
     "Longer follow-up in advanced-disease populations accrues more deaths."),
    ("duration_day", "dropout_rate", "operational",
     "Longer trials lose more participants to follow-up."),

    # sponsor -> downstream operational fields
    ("sponsors/lead_sponsor/agency_class", "enrollment", "design_choice",
     "Industry sponsors typically run larger trials than academic / NIH sponsors; sponsor class shifts the median planned N."),
    ("sponsors/lead_sponsor/agency_class", "approval_outcome", "regulatory",
     "Industry trials are designed-for-approval; academic / NIH trials less often pursue or attain regulatory approval."),

    # study_design_info/allocation -> biology_pass (cleaner efficacy estimate)
    ("study_design_info/allocation", "biology_pass", "biological",
     "Randomised allocation is the gold standard for unbiased efficacy estimation; non-randomised designs rarely satisfy regulators on biology_pass."),

    # study_design_info/masking -> biology_pass (blinding reduces bias)
    ("study_design_info/masking", "biology_pass", "biological",
     "Blinding reduces placebo / expectation bias, giving cleaner efficacy estimates and more reliable biology_pass calls."),
]


# ============================================================================
# 4. EXPLICIT NO-DIRECT PAIRS (cross-tier exceptions to the default)
# ============================================================================

# Each entry: (a, b, reason). Order doesn't matter.
# Use this for cross-tier pairs where the association is real but the
# causal arrow does NOT go directly between A and B (mediated through
# other DAG nodes, or A and B both derived from a common ancestor).

EXPLICIT_NO_DIRECT: list[tuple[str, str, str]] = [
    # --- approval_outcome ↔ biology_fail / execution_fail (mediated via _pass) ---
    ("approval_outcome", "biology_fail",
     "Mediated through `biology_pass`: biology_fail = NOT biology_pass, and biology_pass -> approval_outcome is the direct edge."),
    ("approval_outcome", "execution_fail",
     "Mediated through `execution_pass`: execution_fail = NOT execution_pass, and execution_pass -> approval_outcome is the direct edge."),

    # --- biology vs execution (independent preconditions, no direct arrow) ---
    ("biology_pass", "execution_pass",
     "biology_pass and execution_pass are independent preconditions for approval — biology is about whether the drug works, execution is about whether the trial was run properly. They are both downstream of failure_reason but do not directly cause each other."),
    ("biology_pass", "execution_fail",
     "Mediated through `execution_pass` (and the common parent `failure_reason`)."),
    ("biology_fail", "execution_pass",
     "Mediated through `biology_pass` (and the common parent `failure_reason`)."),
    ("biology_fail", "execution_fail",
     "Mediated through both negations of pass; no direct biology-execution arrow."),

    # --- duration_month ↔ duration_year (sibling under duration_day) ---
    ("duration_month", "duration_year",
     "Both are deterministic unit conversions of duration_day; siblings under common parent duration_day, no direct causal arrow."),

    # --- start_date ↔ duration_month / duration_year (mediated through duration_day) ---
    ("start_date", "duration_month",
     "Mediated through duration_day: start_date -> duration_day -> duration_month."),
    ("start_date", "duration_year",
     "Mediated through duration_day: start_date -> duration_day -> duration_year."),
    ("completion_date", "duration_month",
     "Mediated through duration_day: completion_date -> duration_day -> duration_month."),
    ("completion_date", "duration_year",
     "Mediated through duration_day: completion_date -> duration_day -> duration_year."),

    # --- mortality binary indicators with sae/dropout (mediated through rates) ---
    ("mortality_YN", "sae_rate",
     "Mediated through mortality_rate: mortality_YN <- mortality_rate -> sae_rate."),
    ("mortality_YN", "sae_YN",
     "Common cause: both downstream of mortality_rate -> sae_rate -> sae_YN; no direct YN-to-YN arrow."),
    ("mortality_YN", "dropout_rate",
     "Mediated through mortality_rate: mortality_YN <- mortality_rate -> dropout_rate."),
    ("mortality_YN", "dropout_YN",
     "Mediated chain through rates."),
    ("mortality_rate", "sae_YN",
     "Mediated through sae_rate: mortality_rate -> sae_rate -> sae_YN."),
    ("mortality_rate", "dropout_YN",
     "Mediated through dropout_rate."),
    ("sae_YN", "dropout_rate",
     "Mediated through sae_rate: sae_YN <- sae_rate -> dropout_rate."),
    ("sae_YN", "dropout_YN",
     "Common cause via sae_rate -> dropout_rate -> dropout_YN."),
    ("dropout_YN", "sae_rate",
     "Mediated through dropout_rate."),

    # --- Cross-tier no-direct: design_top pairs that are not directly causal even though they associate ---
    ("intervention/intervention_name", "phase",
     "Both reflect drug-development status (latent): intervention_name encodes which compound, and phase encodes how far it has progressed. No direct causal arrow at the column level — they are siblings under the unobserved 'drug pipeline status'."),
    ("intervention/intervention_name", "study_design_info/intervention_model",
     "Both jointly chosen sponsor design decisions; no direct arrow."),
    ("intervention/intervention_name", "study_design_info/masking",
     "Both jointly chosen sponsor design decisions; no direct arrow."),
    ("intervention/intervention_name", "study_design_info/allocation",
     "Both jointly chosen sponsor design decisions; no direct arrow."),
    ("intervention/intervention_name", "sponsors/lead_sponsor/agency_class",
     "Sponsor and specific drug correlate through portfolio (industry runs branded drugs, etc.) but neither directly causes the other."),
    ("phase", "sponsors/lead_sponsor/agency_class",
     "Both jointly chosen at trial registration; correlated via drug-development economics but no direct arrow."),
    ("condition", "sponsors/lead_sponsor/agency_class",
     "Both jointly chosen; sponsors specialise in indication portfolios but neither column directly causes the other."),
    ("condition", "phase",
     "Both jointly chosen at registration; a specific disease can be at any phase depending on the drug being tested."),
    ("condition", "study_design_info/intervention_model",
     "Both jointly chosen design decisions; no direct arrow."),
    ("condition", "study_design_info/masking",
     "Both jointly chosen design decisions; no direct arrow."),
    ("condition", "study_design_info/allocation",
     "Both jointly chosen design decisions; no direct arrow."),
    ("intervention/intervention_type", "study_design_info/masking",
     "Both jointly chosen design decisions; no direct arrow."),
    ("intervention/intervention_type", "study_design_info/primary_purpose",
     "Mediated through primary_purpose -> intervention_type (purpose constrains the feasible type set)."),
    ("study_design_info/intervention_model", "study_design_info/masking",
     "Both methodological choices made jointly; no direct arrow at this DAG resolution."),
    ("study_design_info/intervention_model", "study_design_info/primary_purpose",
     "Both jointly chosen; primary purpose doesn't strictly constrain intervention model."),
    ("study_design_info/allocation", "study_design_info/masking",
     "Both methodological choices made jointly; no direct arrow."),
    ("study_design_info/allocation", "study_design_info/primary_purpose",
     "Both jointly chosen design decisions."),
    ("study_design_info/masking", "study_design_info/primary_purpose",
     "Both jointly chosen design decisions."),
    ("sponsors/lead_sponsor/agency_class", "study_design_info/masking",
     "Both jointly chosen; sponsor class doesn't directly constrain masking choice."),
    ("sponsors/lead_sponsor/agency_class", "study_design_info/intervention_model",
     "Both jointly chosen."),
    ("sponsors/lead_sponsor/agency_class", "study_design_info/allocation",
     "Both jointly chosen."),
    ("sponsors/lead_sponsor/agency_class", "study_design_info/primary_purpose",
     "Both jointly chosen."),
]


# ============================================================================
# 5. CLASSIFIER
# ============================================================================


def find_latest_run() -> Path:
    candidates = sorted(
        RESULTS_ROOT.glob("ci_pairwise_association_*"),
        key=lambda p: p.name,
    )
    if not candidates:
        raise FileNotFoundError(f"No ci_pairwise_association_* under {RESULTS_ROOT}")
    return candidates[-1]


# ============================================================================
# 4b. CONFOUNDING-DEMOTION REVIEW (per-pair domain audit of default edges)
# ============================================================================
#
# The tier default rule (P4) only assigns a *direction*; it assumes a direct
# causal arrow exists for every cross-tier associated pair. That assumption is
# wrong for confounded / mediated pairs. This second pass demotes a default
# cross-tier edge to `associated_no_direct` when `src` has no plausible DIRECT
# causal mechanism to `tgt` (the association is fully mediated through a
# definitional parent, or confounded by sponsor class / trial era / indication
# mix). Rules are intentionally conservative and documented.

# SET A — re-encodings / tallies: their genuine cause is the definitional parent.
REENCODING_PARENT = {
    "condition_browse/mesh_term": "condition",
    "icdcode": "condition",
    "intervention_browse/mesh_term": "intervention/intervention_name",
    "smiless": "intervention/intervention_name",
    "study_design_info/masking_num": "study_design_info/masking",
    "MaskingType-Care Provider": "study_design_info/masking",
    "MaskingType-Investigator": "study_design_info/masking",
    "MaskingType-Outcomes Assessor": "study_design_info/masking",
    "MaskingType-Participant": "study_design_info/masking",
    "Behavioral intervention Number": "intervention/intervention_type",
    "Biological intervention Number": "intervention/intervention_type",
    "Combination Product intervention Number": "intervention/intervention_type",
    "Device intervention Number": "intervention/intervention_type",
    "Diagnostic Test intervention Number": "intervention/intervention_type",
    "Dietary Supplement intervention Number": "intervention/intervention_type",
    "Drug intervention Number": "intervention/intervention_type",
    "Genetic intervention Number": "intervention/intervention_type",
    "Other intervention Number": "intervention/intervention_type",
    "Procedure intervention Number": "intervention/intervention_type",
    "Radiation intervention Number": "intervention/intervention_type",
    "Active Comparator Arm Number": "study_design_info/intervention_model",
    "Experimental Arm Number": "study_design_info/intervention_model",
    "No Intervention Arm Number": "study_design_info/intervention_model",
    "Other Arm Number": "study_design_info/intervention_model",
    "Placebo Comparator Arm Number": "study_design_info/intervention_model",
    "Sham Comparator Arm Number": "study_design_info/intervention_model",
}

# SET B — administrative / policy / calendar / site-geography attributes with
# no direct biological or operational pathway to clinical outcomes.
NO_MECHANISM_SOURCES = {
    "responsible_party/responsible_party_type",
    "patient_data/sharing_ipd",
    "ipd_info_type-Analytic Code",
    "ipd_info_type-Clinical Study Report (CSR)",
    "ipd_info_type-Informed Consent Form (ICF)",
    "ipd_info_type-Statistical Analysis Plan (SAP)",
    "ipd_info_type-Study Protocol",
    "has_expanded_access",
    "brief_title",
    "location/facility/address/city",
    "start_date",
}

SAFETY_NODES = {
    "dropout_YN", "dropout_rate", "sae_YN", "sae_rate",
    "mortality_YN", "mortality_rate",
}
METHODOLOGY_DESIGN = {
    "sponsors/lead_sponsor/agency_class",
    "study_design_info/primary_purpose",
    "study_design_info/intervention_model",
    "study_design_info/allocation",
    "study_design_info/masking",
    "number_of_arms",
}
ELIGIBILITY_NODES = {
    "eligibility/gender", "eligibility/healthy_volunteers",
    "eligibility/maximum_age", "eligibility/minimum_age",
}

# R9 whitelist — the ONLY design_top -> {design_planning, design_eligibility}
# edges with a concrete direct mechanism. Everything else into these target
# groups is demoted. Targets absent from this dict (start_date,
# location/facility/address/city, brief_title) have NO whitelisted source, so
# every incoming edge is demoted.
R9_WHITELIST = {
    # Trial size is genuinely sized by phase / disease prevalence / sponsor
    # scale / intervention pool / multi-arm power requirements.
    "enrollment": {
        "phase", "condition", "sponsors/lead_sponsor/agency_class",
        "intervention/intervention_type", "intervention/intervention_name",
        "study_design_info/intervention_model",
    },
    # Whether healthy volunteers are admitted is set by phase (first-in-human),
    # the disease, the purpose (prevention/vaccine), and modality.
    "eligibility/healthy_volunteers": {
        "phase", "condition", "study_design_info/primary_purpose",
        "intervention/intervention_type",
    },
    # Sex / age bounds are set by the disease (sex-specific, pediatric vs
    # geriatric) and by phase (Phase-1 healthy-volunteer age caps).
    # Sex / age bounds are set by the DISEASE (sex-specific, pediatric vs
    # geriatric). `phase` was dropped here (R9-tightening): phase's direct
    # contribution to sex/upper-age eligibility is negligible vs `condition`.
    "eligibility/gender": {"condition"},
    "eligibility/maximum_age": {"condition"},
    # minimum_age keeps phase: Phase-1 commonly sets an 18y floor.
    "eligibility/minimum_age": {"condition", "phase"},
}


def confounding_demotion(src: str, tgt: str) -> str | None:
    """Return a demotion reason if the default edge src->tgt is confounded /
    mediated and should be `associated_no_direct`; else None (keep edge)."""
    sg = NODE_METADATA[src]["group"]
    tg = NODE_METADATA[tgt]["group"]

    # R1: re-encoding / tally source -> anything
    if src in REENCODING_PARENT:
        par = REENCODING_PARENT[src]
        return (f"`{src}` is a deterministic re-encoding / tally of `{par}`; its "
                f"association with `{tgt}` is fully mediated through that definitional "
                f"parent, which carries the genuine causal edge. (R1: proxy source.)")

    # R2: administrative / no-mechanism source -> outcome
    if src in NO_MECHANISM_SOURCES and tg.startswith("outcome"):
        return (f"`{src}` is an administrative / policy / calendar / site-geography "
                f"attribute with no direct biological or operational pathway to `{tgt}`; "
                f"the association is confounded by sponsor class, trial era, or "
                f"indication mix. (R2: no-mechanism source.)")

    # R3: rate invariance — enrollment does not change a per-trial rate
    if src == "enrollment" and tgt in SAFETY_NODES:
        return ("A rate is invariant to sample size in expectation; "
                f"`enrollment -> {tgt}` is a threshold-crossing artifact, not a causal "
                "effect of N on the safety rate. (R3: rate invariance. Genuine "
                "enrollment effects are kept for trial timing and the 'poor enrollment' "
                "execution-failure pathway.)")

    # R4: methodology / sponsor design -> safety is confounded via what is studied
    if src in METHODOLOGY_DESIGN and tg == "outcome_safety":
        return (f"`{src}` is a sponsor / methodology design choice with no direct "
                f"biological pathway to the realised safety rate `{tgt}`; the "
                "association is confounded through `intervention/intervention_type` and "
                "`condition` (what is being studied), which carry the genuine safety "
                "edges. (R4: confounded design->safety.)")

    # R5: methodology / eligibility -> timing is mediated through enrollment / model
    if (src in (METHODOLOGY_DESIGN | ELIGIBILITY_NODES)
            and src not in ("study_design_info/intervention_model",
                            "sponsors/lead_sponsor/agency_class",
                            "number_of_arms")
            and tg == "outcome_timing"):
        return (f"`{src}` affects the trial timeline only through `enrollment` / "
                "`study_design_info/intervention_model`, the direct parents of trial "
                f"duration; the marginal association with `{tgt}` is mediated, not "
                "direct. (R5: mediated design->timing.)")

    # R6: methodology / eligibility -> trial-success label is mediated
    if (src in (METHODOLOGY_DESIGN | ELIGIBILITY_NODES)
            and src not in ("study_design_info/allocation",
                            "study_design_info/masking")
            and tg == "outcome_label"):
        return (f"`{src}` reaches the trial-success label `{tgt}` only through "
                "biology / efficacy and enrollment mediators already in the DAG "
                "(`biology_pass`, `failure_reason`, `enrollment`); no direct arrow. "
                "(R6: mediated design->label.)")

    # R7: design_top -> design_derived non-definitional (mediated through the
    #     single definitional parent)
    if tg == "design_derived":
        return (f"`{tgt}` is a deterministic descendant of its single definitional "
                f"design parent; `{src}` reaches it only through that parent "
                "(mediated, not direct). (R7: mediated ->design_derived.)")

    # R8: design -> design_oversight confounded (keep only phase / sponsor /
    #     intervention_type which have genuine policy-setting mechanisms)
    if tg == "design_oversight" and src not in (
        "phase", "sponsors/lead_sponsor/agency_class",
        "intervention/intervention_type",
    ):
        return (f"`{src}` has no direct mechanism that sets the oversight / policy "
                f"field `{tgt}`; the association is confounded through sponsor class "
                "and trial type. (R8: confounded ->design_oversight.)")

    # R9: design_top -> design_planning / design_eligibility — keep ONLY edges
    #     with a concrete causal mechanism (whitelist below); demote the rest.
    #     `start_date`, `location/.../city`, `brief_title` have NO sensible
    #     design cause (calendar date / site footprint / free-text title) so
    #     every edge into them is demoted.
    if tg in ("design_planning", "design_eligibility"):
        allowed = R9_WHITELIST.get(tgt, set())
        if src not in allowed:
            return (f"`{src}` has no concrete causal mechanism that sets `{tgt}`. "
                    "Trial size, eligible population, calendar start date, site "
                    "geography and the free-text title are not directly caused by "
                    f"`{src}`; the association is a jointly-chosen-design / "
                    "sponsor-footprint / secular-trend confound. (R9: spurious "
                    "design->planning/eligibility.)")

    # R10: design_oversight -> outcome is confounded. An oversight / regulatory
    #      flag (is_fda_regulated_*, has_dmc) is a proxy for trial *type* and
    #      *scale*, not a direct cause of safety / efficacy / timing / label.
    #      The two genuine mechanisms are hand-authored EXPLICIT edges and never
    #      reach this pass (P1 classifies them first):
    #        - oversight_info/is_fda_regulated_{drug,device} -> approval_outcome
    #        - oversight_info/has_dmc -> {sae_rate, mortality_rate, execution_pass}
    if sg == "design_oversight" and tg.startswith("outcome"):
        return (f"`{src}` is an oversight / regulatory flag that proxies for "
                f"trial type and scale; its association with `{tgt}` is confounded "
                "through `intervention/intervention_type`, `phase`, and trial "
                "scale. The genuine oversight mechanisms (FDA-regulation -> "
                "approval_outcome; DMC early-stopping -> sae_rate / mortality_rate) "
                "are retained as explicit edges. (R10: confounded "
                "design_oversight->outcome.)")

    return None


def classify_pair(
    a: str,
    b: str,
    explicit_edges: dict[tuple[str, str], tuple[str, str, str, str]],
    explicit_no_direct: dict[tuple[str, str], str],
) -> tuple[str, dict]:
    """Return (verdict, payload). verdict in {'edge', 'no_direct'}.

    payload for edge:      {src, tgt, mechanism, rationale}
    payload for no_direct: {a, b, reason}
    """
    ga = NODE_METADATA[a]["group"]
    gb = NODE_METADATA[b]["group"]
    ta = GROUP_TIER[ga]
    tb = GROUP_TIER[gb]

    # P1: explicit edge in either direction
    if (a, b) in explicit_edges:
        _, _, mech, rat = explicit_edges[(a, b)]
        return "edge", {"src": a, "tgt": b, "mechanism": mech, "rationale": rat}
    if (b, a) in explicit_edges:
        _, _, mech, rat = explicit_edges[(b, a)]
        return "edge", {"src": b, "tgt": a, "mechanism": mech, "rationale": rat}

    # P2: explicit no-direct (unordered)
    key = tuple(sorted([a, b]))
    if key in explicit_no_direct:
        return "no_direct", {"a": a, "b": b, "reason": explicit_no_direct[key]}

    # P3: same tier -> no direct
    if ta == tb:
        if ga == gb:
            reason = (
                f"Both in group '{ga}' (tier {ta}); within-group pairs are siblings "
                "under common design parents or jointly-set sponsor decisions and "
                "have no direct causal arrow at this DAG resolution."
            )
        else:
            reason = (
                f"Both in tier {ta} (downstream-design sub-groups '{ga}' and '{gb}'); "
                "jointly determined by upstream design_top choices, no direct arrow."
            )
        return "no_direct", {"a": a, "b": b, "reason": reason}

    # P4: cross-tier default direction (lower tier -> higher tier)
    if ta < tb:
        src, tgt, sg, tg = a, b, ga, gb
        st, tt = ta, tb
    else:
        src, tgt, sg, tg = b, a, gb, ga
        st, tt = tb, ta
    # P4b: confounding-demotion review — does src have a direct mechanism to tgt?
    demote = confounding_demotion(src, tgt)
    if demote is not None:
        return "no_direct", {"a": src, "b": tgt, "reason": demote, "_prov": "demoted_confounded"}

    mech = DEFAULT_MECHANISM.get((st, tt), "domain_knowledge")
    rat_tpl = GROUP_DEFAULT_RATIONALE.get(
        (st, tt),
        "{src} ({sg}) causally precedes {tgt} ({tg}) in the trial timeline.",
    )
    rat = rat_tpl.format(src=src, tgt=tgt, sg=sg, tg=tg)
    return "edge", {"src": src, "tgt": tgt, "mechanism": mech, "rationale": rat, "_prov": "default_cross_tier"}


def topological_check(edges: list[dict], nodes: list[str]) -> list[str]:
    """Return list of nodes in cycle, or [] if acyclic."""
    from collections import defaultdict, deque

    adj = defaultdict(set)
    indeg = defaultdict(int)
    for e in edges:
        adj[e["src"]].add(e["tgt"])
        indeg[e["tgt"]] += 1
    for n in nodes:
        indeg.setdefault(n, 0)
    queue = deque(n for n in nodes if indeg[n] == 0)
    visited = 0
    while queue:
        n = queue.popleft()
        visited += 1
        for c in adj[n]:
            indeg[c] -= 1
            if indeg[c] == 0:
                queue.append(c)
    if visited == len(nodes):
        return []
    return [n for n, d in indeg.items() if d > 0]


def main() -> None:
    run_dir = find_latest_run()
    print(f"[info] reading associated pairs from {run_dir}")
    assoc = pd.read_csv(run_dir / "pairwise_associated.csv")
    print(f"[info] {len(assoc)} associated pairs")

    # Sanity: all column ids appear in NODE_METADATA
    cols_in_assoc = set(assoc["col_a"]) | set(assoc["col_b"])
    missing = cols_in_assoc - set(NODE_METADATA.keys())
    if missing:
        raise RuntimeError(f"Missing NODE_METADATA entries: {missing}")
    extra = set(NODE_METADATA.keys()) - cols_in_assoc
    if extra:
        # Allow: e.g., a retained column with zero partners (none expected after our drops)
        print(f"[warn] NODE_METADATA has columns with no associated partner: {extra}")

    # Build lookups
    edge_lookup: dict[tuple[str, str], tuple[str, str, str, str]] = {}
    for tup in EXPLICIT_DIRECT_EDGES:
        edge_lookup[(tup[0], tup[1])] = tup
    no_direct_lookup = {tuple(sorted([t[0], t[1]])): t[2] for t in EXPLICIT_NO_DIRECT}

    # Sanity: explicit lists reference known nodes only
    for s, t, _, _ in EXPLICIT_DIRECT_EDGES:
        for x in (s, t):
            if x not in NODE_METADATA:
                raise RuntimeError(f"EXPLICIT_DIRECT_EDGES references unknown node: {x}")
    for a, b, _ in EXPLICIT_NO_DIRECT:
        for x in (a, b):
            if x not in NODE_METADATA:
                raise RuntimeError(f"EXPLICIT_NO_DIRECT references unknown node: {x}")

    edges_out: list[dict] = []
    no_directs_out: list[dict] = []
    counts = {"edge": 0, "no_direct": 0}
    edge_sources = {"explicit": 0, "default_within_tier": 0, "default_cross_tier": 0}

    for _, r in assoc.iterrows():
        a, b = r["col_a"], r["col_b"]
        effect = float(r["effect_size"])
        metric = r["metric"]
        n_valid = int(r["n_valid"])
        p_adj = float(r["p_adj"])

        verdict, payload = classify_pair(a, b, edge_lookup, no_direct_lookup)
        # Provenance: honor an explicit hint from classify_pair (P4/P4b);
        # otherwise infer it.
        if "_prov" in payload:
            src_kind = payload.pop("_prov")
        elif (a, b) in edge_lookup or (b, a) in edge_lookup:
            src_kind = "explicit"
        elif tuple(sorted([a, b])) in no_direct_lookup:
            src_kind = "explicit"
        elif NODE_METADATA[a]["group"] == NODE_METADATA[b]["group"] or GROUP_TIER[NODE_METADATA[a]["group"]] == GROUP_TIER[NODE_METADATA[b]["group"]]:
            src_kind = "default_within_tier"
        else:
            src_kind = "default_cross_tier"

        common = {
            "effect_size": effect,
            "metric": metric,
            "n_valid": n_valid,
            "p_adj": p_adj,
            "provenance": src_kind,
        }
        if verdict == "edge":
            edges_out.append({**payload, **common})
            counts["edge"] += 1
            edge_sources[src_kind] = edge_sources.get(src_kind, 0) + 1
        else:
            no_directs_out.append({**payload, **common})
            counts["no_direct"] += 1
            counts.setdefault("no_direct_by_prov", {})
            counts["no_direct_by_prov"][src_kind] = counts["no_direct_by_prov"].get(src_kind, 0) + 1

    # Acyclicity check
    nodes_list = list(NODE_METADATA.keys())
    cycle_nodes = topological_check(edges_out, nodes_list)
    if cycle_nodes:
        print(f"[error] DAG has a cycle involving: {cycle_nodes}")
    else:
        print("[ok] DAG is acyclic.")

    # Group nodes for output
    groups: dict[str, list[str]] = {}
    for n, m in NODE_METADATA.items():
        groups.setdefault(m["group"], []).append(n)

    out = {
        "schema_version": "1.0",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "dataset": "TrialBench_joined (Phase1-4 concatenated, n=81786)",
        "association_run": str(run_dir),
        "n_nodes": len(NODE_METADATA),
        "n_directed_edges": counts["edge"],
        "n_associated_no_direct": counts["no_direct"],
        "n_associated_total": counts["edge"] + counts["no_direct"],
        "acyclic": len(cycle_nodes) == 0,
        "construction_methodology": (
            "Stage 1 (data): pairwise association screen on 71 retained columns; "
            "threshold effect_size > 0.05 AND BH-FDR p < 0.01 keeps 1,169 pairs. "
            "Stage 2 (domain knowledge, this file): each associated pair is classified "
            "as a directed edge A->B / B->A or an associated-but-no-direct pair. A "
            "per-pair confounding-demotion review (8 documented rules, R1-R8) demotes "
            "default cross-tier edges to associated_no_direct when src has no direct "
            "causal mechanism to tgt (re-encoding/proxy source, no-mechanism admin "
            "source, rate invariance, or mediation through a definitional parent). The "
            "classification is sourced from clinical-trial domain knowledge (no data "
            "peeking at column values)."
        ),
        "tier_ordering": GROUP_TIER,
        "default_mechanism_by_tier_pair": {f"{k[0]}->{k[1]}": v for k, v in DEFAULT_MECHANISM.items()},
        "edge_provenance_counts": edge_sources,
        "no_direct_provenance_counts": counts.get("no_direct_by_prov", {}),
        "node_groups": groups,
        "nodes": [
            {"id": n, **m}
            for n, m in NODE_METADATA.items()
        ],
        "edges": edges_out,
        "associated_no_direct": no_directs_out,
    }

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(out, indent=2, ensure_ascii=False))
    print(f"[ok] wrote {OUT_PATH}")
    print(
        f"[summary] nodes={out['n_nodes']}  edges={out['n_directed_edges']}  "
        f"no_direct={out['n_associated_no_direct']}  acyclic={out['acyclic']}"
    )
    print(f"[edge provenance] {edge_sources}")
    print(f"[no_direct provenance] {counts.get('no_direct_by_prov', {})}")


if __name__ == "__main__":
    main()
