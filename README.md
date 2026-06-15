<div align="center">

<img src="https://img.shields.io/badge/Apache%20Spark-3.x-E25A1C?style=for-the-badge&logo=apachespark&logoColor=white"/>
<img src="https://img.shields.io/badge/Hadoop-HDFS%20%2B%20YARN-66CCFF?style=for-the-badge&logo=apachehadoop&logoColor=black"/>
<img src="https://img.shields.io/badge/PySpark-SparkSQL%20%7C%20MLlib-E25A1C?style=for-the-badge&logo=apachespark&logoColor=white"/>
<img src="https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>
<img src="https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white"/>
<img src="https://img.shields.io/badge/Records-9.8M%20CMS-blueviolet?style=for-the-badge"/>
<img src="https://img.shields.io/badge/License-MIT-brightgreen?style=for-the-badge"/>

# 🏥 HealthcareCost Lens

### Distributed Big-Data Pipeline for Medicare Fraud Detection, Geographic Inequity & Access Gap Analysis

**6.8 GB · 9.8M records · 3-node Hadoop cluster · 5 SparkSQL queries · 2 ML models · 1 interactive dashboard**

[**Results**](#-results-at-a-glance) · [**Architecture**](#-pipeline-architecture) · [**ML Models**](#-ml-models) · [**Dashboard**](#-dashboard) · [**Quickstart**](#-quickstart)

---

</div>

## 📌 The Problem

Medicare processes over **$900 billion** in annual payments — yet geographic payout inequity, provider billing anomalies, and beneficiary access gaps remain largely invisible without large-scale infrastructure to surface them. Fraud, waste, and abuse cost the U.S. healthcare system an estimated **$60–90 billion per year**, much of it buried in datasets too large for conventional analysis.

**HealthcareCost Lens** applies distributed computing and machine learning to 9.8 million CMS provider records to answer five questions that regulators, insurers, and policymakers need answered — at a scale most tools cannot reach.

---

## ⚡ Results at a Glance

| Finding | Detail |
|---|---|
| 📍 **Geographic payout variation** | >40% difference for identical procedures across U.S. states |
| 🚨 **Highest billing outlier** | Texas provider: z-score **198** — billing $22,329 vs. $45 national average |
| 🏥 **Worst access gap** | 2,694 beneficiaries per provider in NC Internal Medicine — **5× a healthy ratio** |
| 💸 **Lowest reimbursement rate** | 12.9% on cardiac catheterisation (HCPCS C9600) |
| 🦴 **Highest specialty spend** | $8.19B attributed to Orthopedic Surgery — highest of any specialty |

---

## 🏗️ Pipeline Architecture

```
CMS Medicare CSV (6.8 GB · 9,886,177 rows)
        │
        ▼
┌───────────────────────────────┐
│   HDFS Ingestion              │  ← 3-node Hadoop cluster (1 NameNode + 2 DataNodes)
│   54 blocks · replication 2  │    YARN resource management · zero corrupt blocks
└──────────────┬────────────────┘
               │
               ▼
┌───────────────────────────────┐
│   PySpark ETL                 │  ← Schema enforcement · null handling
│                               │    Type casting · column normalisation
└──────────────┬────────────────┘
               │
        ┌──────┴──────┐
        ▼             ▼
┌──────────────┐  ┌──────────────────┐
│  SparkSQL    │  │  Spark MLlib     │
│  Q1 – Q5    │  │  K-Means · RF    │
└──────┬───────┘  └───────┬──────────┘
        └──────┬───────────┘
               ▼
┌───────────────────────────────┐
│   Streamlit Dashboard         │  ← 5-page interactive app · Plotly Express
└───────────────────────────────┘
```

---

## 🔍 Analytical Queries (SparkSQL)

| Query | Business Question | Key Output |
|---|---|---|
| **Q1 — Geographic Payout** | Which states overpay or underpay for the same procedure? | >40% payout variation detected across states |
| **Q2 — Outlier Detection** | Which providers have statistically anomalous billing? (z-score > 2) | Z-score = 198 flagged in Texas |
| **Q3 — Access Gap** | Where is the beneficiary-to-provider ratio dangerously high? | 2,694 beneficiaries/provider in NC Internal Medicine |
| **Q4 — Cost Disparity** | Which procedures have the worst reimbursement rates? | 12.9% reimbursement on cardiac catheterisation C9600 |
| **Q5 — Specialty Volume** | Which specialties dominate total Medicare spend? | Orthopedic Surgery: $8.19B — highest of any specialty |

---

## 📊 Dashboard Preview

<img width="883" height="540" alt="HealthcareCost Lens Dashboard — Geographic Payout View" src="https://github.com/user-attachments/assets/c1801046-4dcb-4628-9a9b-925ee181a42d"/>

<img width="887" height="602" alt="HealthcareCost Lens Dashboard — Outlier Detection View" src="https://github.com/user-attachments/assets/3c909426-1ca4-4647-8c3a-169eeab37373"/>

The 5-page Streamlit app surfaces every query and model result through interactive Plotly Express charts:

| Page | Visualization |
|---|---|
| **Geographic Payout** | Choropleth map — state-level payout variation by procedure |
| **Outlier Detection** | Provider-level z-score ranking with drill-down detail |
| **Access Gap** | Beneficiary-to-provider ratios by state and specialty |
| **Cost Disparity** | Bubble scatter — payment rate vs. submitted charge by procedure |
| **ML Insights** | K-Means cluster profiles · RF feature importance · model metrics |

A global **NPI / HCPCS search bar** spans all pages for cross-dataset provider and procedure lookup.

---

## 🤖 ML Models

### K-Means Clustering (k = 4)
Groups 9.8M provider records into four billing archetypes using elbow-method optimisation:

| Cluster | Archetype | Profile |
|---|---|---|
| 0 | **Routine Billers** | Low charge, low volume, standard reimbursement |
| 1 | **High-Charge Specialists** | Elevated submitted charges, lower volume |
| 2 | **High-Volume Primary Care** | High beneficiary counts, moderate billing |
| 3 | **Anomalous Outliers** | Statistical extremes in charge or volume — fraud candidates |

### Random Forest Regression

Predicts Medicare payment amount from provider billing features on held-out test data:

| Metric | Value |
|---|---|
| RMSE | **$208.65** |
| R² | **0.28** |
| Dominant Feature | Submitted charge — **96% of feature importance** |

> The 96% concentration on submitted charge confirms Medicare's prospective payment structure: the system largely reimburses within fee schedule bounds relative to what is billed — making anomalous submitted charges both the clearest fraud signal and the model's most predictive input.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Distributed Storage | `Apache Hadoop` · HDFS + YARN · 3-node cluster |
| Distributed Processing | `Apache Spark` · `PySpark` · `SparkSQL` |
| Machine Learning | `Spark MLlib` · K-Means clustering · Random Forest regression |
| Visualization | `Plotly Express` · choropleth · scatter · bar |
| Dashboard | `Streamlit` · 5-page multi-view application |
| Containerization | `Docker Compose` |
| Language | `Python 3.8+` |

---

## 🚀 Quickstart

```bash
# 1. Clone the repository
git clone https://github.com/your-username/healthcarecost-lens.git
cd healthcarecost-lens

# 2. Start the Hadoop + Spark cluster
docker-compose up -d

# 3. Ingest CMS data into HDFS
bash scripts/ingest_hdfs.sh data/cms_medicare_2021.csv

# 4. Run the full pipeline (ETL → SparkSQL → MLlib)
spark-submit src/pipeline.py

# 5. Launch the dashboard
streamlit run app/dashboard.py
```

> **Data:** Download the CMS Medicare Provider Utilization & Payment Data (2021) from [data.cms.gov](https://data.cms.gov) and place in `/data` before running ingestion. No patient-level data is used — all records are provider-level aggregates.

---

## 📁 Repository Structure

```
healthcarecost-lens/
│
├── data/                           # Raw CMS CSV (download separately)
│
├── src/
│   ├── ingest.py                   # HDFS ingestion and block verification
│   ├── etl.py                      # PySpark ETL — schema, types, nulls
│   ├── queries.py                  # SparkSQL Q1–Q5 implementations
│   ├── models.py                   # K-Means clustering + RF regression
│   └── pipeline.py                 # End-to-end orchestration
│
├── app/
│   ├── dashboard.py                # Streamlit entry point
│   └── pages/
│       ├── 01_geographic.py
│       ├── 02_outliers.py
│       ├── 03_access_gap.py
│       ├── 04_cost_disparity.py
│       └── 05_ml_insights.py
│
├── scripts/
│   └── ingest_hdfs.sh              # Shell helper for HDFS data load
│
├── docker-compose.yml              # 3-node Hadoop + Spark cluster config
├── requirements.txt
└── README.md
```

---

## 📂 Data Source

**CMS Medicare Provider Utilization & Payment Data — Public Use File · 2021**
- 9,886,177 provider-level records · 6.8 GB uncompressed
- No patient-level data — all records are provider-level aggregates
- Source: [data.cms.gov](https://data.cms.gov)

---

## 🔭 Roadmap

- [ ] Real-time fraud scoring via Spark Structured Streaming
- [ ] SHAP values for explainable ML output on Random Forest predictions
- [ ] Multi-year trend analysis across 2018–2023 CMS cohorts
- [ ] County-level geospatial access gap mapping (GeoPandas + Folium)
- [ ] REST API layer for integration with external healthcare analytics platforms

---

## 📄 License

MIT — see [LICENSE](LICENSE) for details.

---

<div align="center">

**Built to prove that public data, processed at scale, can expose what $900 billion in annual payments obscures.**

⭐ Star this repo if it changed how you think about healthcare analytics at scale.

</div>
---

*DSE-3222: Big Data Analytics and Tools · Manipal Academy of Higher Education · 2026*
*Team: Prajwal K Amin · Rohit Vinod · Aditya Jain*
