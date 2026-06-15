# Healthcare_Cost_Lens

**Distributed big-data pipeline that processes 9.8M CMS Medicare records to detect billing fraud, geographic inequity, and access gaps — served via an interactive Streamlit dashboard.**

---

## Tech Stack

`Apache Spark` `Hadoop (HDFS + YARN)` `PySpark` `SparkSQL` `Spark MLlib` `Streamlit` `Plotly` `Docker Compose` `Python`

---

## What It Does

Ingests 6.8 GB of public CMS Medicare data across a 3-node Hadoop cluster and runs 5 analytical queries + 2 ML models, all surfaced through a multi-page dashboard.

| Query | What it answers |
|---|---|
| Q1 — Geographic payout | Which states overpay or underpay for the same procedure? |
| Q2 — Outlier detection | Which providers have statistically anomalous billing (z-score > 2)? |
| Q3 — Access gap | Where is the beneficiary-to-provider ratio dangerously high? |
| Q4 — Cost disparity | Which procedures have the worst reimbursement rates? |
| Q5 — Specialty volume | Which specialties dominate total Medicare spend? |

---

## Results

- **>40% payout variation** for identical procedures across U.S. states
- **Z-score of 198** flagged on a Texas provider billing $22,329 vs $45 national avg
- **2,694 beneficiaries per provider** in NC Internal Medicine — 5× a healthy ratio
- **12.9% reimbursement rate** on cardiac catheterisation (C9600)
- **$8.19B** attributed to Orthopedic Surgery — highest of any specialty

---

## ML Models

**K-Means Clustering (k=4)** — groups 9.8M provider records into billing archetypes (routine billers, high-charge specialists, high-volume primary care, anomalous outliers) using elbow-method optimisation.

**Random Forest Regression** — predicts Medicare payment amount; RMSE $208.65, R² 0.28 on held-out test set. Submitted charge accounts for 96% of feature importance, confirming Medicare's prospective payment structure.

---

## Pipeline

```
CMS CSV → HDFS (3-node) → PySpark ETL → SparkSQL (Q1–Q5) → Spark MLlib → Streamlit
```

54 HDFS blocks, replication factor 2, zero corrupt blocks across 6.8 GB ingested.

---

## Dashboard

5-page Streamlit app with Plotly Express charts:
- Choropleth map (state-level payout by procedure)
- Outlier + access gap views side-by-side
- Bubble scatter: payment rate vs submitted charge
- ML metrics + feature importance visualisation
- Cross-dataset NPI / HCPCS global search

---

## Data Source

[CMS Medicare Provider Utilization & Payment Data — Public Use File](https://data.cms.gov) · 2021 · 9,886,177 rows · No patient-level data

---

*DSE-3222: Big Data Analytics and Tools · Manipal Academy of Higher Education · 2026*
*Team: Prajwal K Amin · Rohit Vinod · Aditya Jain*
