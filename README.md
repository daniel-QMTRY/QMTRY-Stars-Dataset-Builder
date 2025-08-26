# QMTRY — **Stars Dataset Builder** (HEDIS® + Part D) 🚀

**Goal:** generate an **audit‑ready Stars dataset** from claims, eligibility, and pharmacy inputs—producing:
- `output_demo/measure_member_results.csv` *(member‑level flags and scores)*
- `output_demo/measure_contract_rollup.csv` *(contract‑level rollups)*

> Built for demos with synthetic data; production‑ready patterns (dbt + Great Expectations + Streamlit).

---

## What’s inside the dataset
- **HEDIS basics** (e.g., CBP blood pressure control †) and **Part D** metrics (e.g., **PDC adherence** and **SUPD**).
- **Value set mapping** (ICD/CPT/LOINC/NDC) via `/value_sets/`.
- **ECDS/FHIR‑ready** exchange stubs (DEQM bundle scaffolds) to support NCQA’s digital transition.
- **Evidence Bundle** with run metadata to support CMS audit traceability.

† See *CITATIONS.md* for public references to NCQA/CMS/PQA sources you must consult for official specs.

---

## Quickstart (demo data)
```bash
# 1) Create and activate a virtual env
python -m venv .venv && source .venv/bin/activate

# 2) Install
pip install -r requirements.txt

# 3) Build demo outputs from sample CSVs (synthetic)
python scripts/build_stars_dataset.py --start 2024-01-01 --end 2024-12-31

# 4) View the demo dashboard
streamlit run streamlit/app.py
```
Outputs land in `output_demo/` and include a tiny sample of **PDC** and **SUPD** results.

---

## Repository layout
```
.
├── README.md
├── CITATIONS.md
├── Makefile
├── requirements.txt
├── configs/
│   └── stars.yml
├── data_demo/                  # tiny synthetic inputs
│   ├── eligibility.csv
│   └── pharmacy_claims.csv
├── dbt/                        # placeholder dbt project (DuckDB)
│   ├── dbt_project.yml
│   └── models/stars/schema.yml
├── evidence/
│   └── RUN_2025-08-26.json        # run metadata (auto‑generated)
├── output_demo/
│   ├── measure_member_results.csv
│   └── measure_contract_rollup.csv
├── scripts/
│   └── build_stars_dataset.py  # demo PDC + SUPD logic
├── streamlit/
│   └── app.py                  # lightweight demo dashboard
├── tests/
│   └── test_demo_data.md
└── value_sets/
    ├── pqa_supd_ndc_example.csv
    └── drug_classes_example.csv
```

---

## Architecture (high level)

```mermaid
flowchart LR
    A[Claims + Eligibility + Rx] --> B[Standardize & Map 
 (/value_sets)]
    B --> C[Measure Calc 
 (PDC, SUPD, CBP*)]
    C --> D[Member Results CSV]
    D --> E[Contract Rollup CSV]
    C --> F[Great Expectations 
 Data Quality Checks]
    D --> G[Evidence Bundle]
    D --> H[Streamlit Dashboard]
```
*CBP and other HEDIS examples shown as placeholders; see NCQA for official specs.

---

## Data contracts (demo)
Minimal columns expected for the **pharmacy_claims.csv** demo:
- `member_id`, `fill_date` (YYYY‑MM‑DD), `days_supply` (int), `drug_class` (e.g., `statin`, `diabetes`)

Minimal columns for **eligibility.csv**:
- `member_id`, `contract_id`, `dob` (YYYY‑MM‑DD), `gender`, `effective_date`, `term_date` (YYYY‑MM‑DD or blank)

See `scripts/build_stars_dataset.py` for the small PDC/SUPD implementation used in the demo.

---

## Digital quality & interoperability
- **ECDS** is the NCQA path for digital HEDIS reporting; this repo includes **DEQM/FHIR** placeholder bundles you can extend to exchange measure results with providers and registries.
- Start with `/configs/stars.yml` to map your source systems; expand `/dbt` models for production pipelines.

---

## Evidence & governance
Each run writes an **evidence JSON** to `/evidence/` (inputs, row counts, time window, code hash). Add your Great Expectations validation results and attach to release artifacts for audit reviews.

---

## Roadmap
- Add: CBP (Controlling High Blood Pressure) demo with synthetic vitals
- Add: Home‑grown **value set loader** for ICD/CPT/LOINC/NDC
- Add: FHIR **DEQM** export for selected measures
- Add: dbt models + snapshots + lineage doc site

---

## Disclaimers
- **No PHI**. This repo uses synthetic demo data only.
- **Measure logic here is illustrative only**. Always implement **official specifications** from NCQA (HEDIS), CMS (Star Ratings), and PQA (Part D).

---

## License
MIT (see `LICENSE` in your fork).
