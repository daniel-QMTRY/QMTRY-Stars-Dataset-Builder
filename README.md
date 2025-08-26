<p align="center">
  <img alt="QMTRY Stars" src="https://img.shields.io/badge/QMTRY-Stars_Dataset_Builder-00B3A4?style=for-the-badge">
  <img alt="License" src="https://img.shields.io/badge/License-MIT-black?style=for-the-badge">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.10+-black?style=for-the-badge">
</p>

# ⭐ QMTRY — Stars Dataset Builder (HEDIS® + Part D)

**Outcome:** a clean, **audit-ready dataset** that payers and provider partners can trust:
- `output_demo/measure_member_results.csv` — member-level flags & scores (PDC, SUPD, etc.)
- `output_demo/measure_contract_rollup.csv` — contract-level rollups for executive reporting

This repo ships with synthetic demo data and a Streamlit app so leaders can **see value in minutes**—while keeping the architecture ready for **dbt**, **Great Expectations**, and **FHIR/DEQM** exports in production.

---

## Why CEOs care (executive summary)

- **Direct line to Star Ratings:** focuses on Part D adherence (PDC) and SUPD, with clear expansion points for HEDIS clinical measures.
- **Provider-actionable outputs:** member lists and concise contract rollups to drive prospective, year-round gap closure.
- **Audit discipline baked in:** evidence JSON + data quality hooks for reliable compliance reviews.
- **Digital-quality ready:** ECDS posture today; DEQM/FHIR export stubs to exchange results with provider systems tomorrow.

**KPI quick looks**

| Domain | Example KPI | Target |
|---|---|---|
| Part D | PDC ≥ 80% (Diabetes) | ≥ 0.80 |
| Part D | SUPD rate | ↑ quarter-over-quarter |
| Ops | Evidence bundle completeness | 100% of runs |
| Data Quality | Critical validations passing | 100% |

---

## What’s inside (scope)

- **HEDIS / Part D foundations**: demo logic for **PDC** and **SUPD** with value-set stubs you replace with licensed sources.
- **Interoperability**: placeholders for **DEQM/FHIR** bundles; ECDS-friendly structure.
- **Governance**: per-run **Evidence Bundle** with time window, row counts, and code hash.
- **Production runway**: dbt project + Great Expectations hooks; keep demo simple, scale when you’re ready.

---

## Architecture

```mermaid
flowchart LR
    A[Inputs: Claims • Eligibility • Pharmacy] --> B[Standardize & Map\n(value_sets/*)]
    B --> C[Measure Engine\n(PDC • SUPD • HEDIS demos)]
    C --> D[Member Results CSV]
    D --> E[Contract Rollup CSV]
    C --> F[Data Quality\n(Great Expectations)]
    D --> G[Evidence Bundle\n(JSON per run)]
    D --> H[Streamlit Dashboard]
Quickstart (5 minutes)
bash
Copy
Edit
# 1) Environment
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2) Build demo outputs (synthetic data)
python scripts/build_stars_dataset.py --start 2024-01-01 --end 2024-12-31

# 3) Explore visuals
streamlit run streamlit/app.py
Outputs land in output_demo/:

measure_member_results.csv → member_id, contract_id, pdc_diabetes, pdc_statin, supd_flag

measure_contract_rollup.csv → contract_id, members, pdc_diabetes_avg, pdc_statin_avg, supd_rate

Data contracts (demo)
pharmacy_claims.csv
member_id, fill_date (YYYY-MM-DD), days_supply (int), drug_class (statin|diabetes|...)

eligibility.csv
member_id, contract_id, dob, gender, effective_date, term_date

Replace with your production schemas and map value sets under /value_sets.

Measure notes (demo logic)
PDC (Proportion of Days Covered) — days covered by fills / days in period, computed per drug class.

SUPD (Statin Use in Persons with Diabetes) — demo rule: ≥2 diabetes fills and ≥1 statin fill within the window.

Thresholds like PDC ≥80% are shown in the app; calibrate to the official specs licensed by your organization.

Governance workflow
mermaid
Copy
Edit
flowchart TD
    R[Run job] --> V[Validations (GX)]
    V -->|pass| EB[Write Evidence JSON]
    V -->|fail| A[Alert + Block publish]
    EB --> REL[Attach to Release/Artifact]
    REL --> AUD[Audit / Review]
Evidence includes: dates, input paths, row counts, and a code hash for traceability.

Delivery plan (pilot to scale)
mermaid
Copy
Edit
gantt
dateFormat  YYYY-MM-DD
title Stars Pilot (Illustrative)
section Build
Demo dataset & app       :done,   d1, 2025-08-01, 2025-08-07
dbt models + GX          :active, d2, 2025-08-08, 2025-08-21
DEQM/FHIR export PoC     :        d3, 2025-08-22, 2025-09-05
section Operate
Provider enablement kit  :        o1, 2025-09-06, 2025-09-20
Monthly Stars cadence    :        o2, 2025-09-21, 2025-12-15
Repository layout
bash
Copy
Edit
.
├── README.md
├── CITATIONS.md
├── requirements.txt
├── configs/stars.yml
├── data_demo/
│   ├── eligibility.csv
│   └── pharmacy_claims.csv
├── scripts/
│   └── build_stars_dataset.py
├── output_demo/
│   ├── measure_member_results.csv
│   └── measure_contract_rollup.csv
├── streamlit/app.py
├── dbt/ (placeholder)
├── value_sets/ (stubs; replace with licensed sources)
└── evidence/ RUN_YYYY-MM-DD.json
Security & compliance
No PHI in this repo; demo data only.

Specs: HEDIS®, CMS Star Ratings, and PQA details are licensed—use official sources for production logic.

Chain-of-custody: every build writes an Evidence JSON; attach validations and commit hashes to releases.

Roadmap
Add CBP demo (Controlling High Blood Pressure) with synthetic vitals

Expand value-set loader (ICD/CPT/LOINC/NDC)

Add DEQM export for select measures

dbt lineage docs + CI checks

License
MIT 
