# Renewal Risk Intelligence

## Overview

Renewal Risk Intelligence is an end-to-end Python application that helps Customer Success and BizOps teams identify customer accounts that are at risk of churn or downgrade before renewal.

The system combines multiple business signals such as product usage, support history, NPS feedback, CSM notes, and product changelog information to generate a unified Customer 360 view, calculate renewal risk, and recommend proactive actions.

An interactive Streamlit dashboard is included to help users explore renewal insights visually.

---

# Problem Statement

Customer renewal decisions are rarely influenced by a single metric.

Important signals are spread across different systems:

* CRM account information
* Product usage trends
* Support ticket history
* Customer satisfaction (NPS)
* Customer Success Manager notes
* Product release and migration updates

The goal of this project is to combine these disconnected signals into one intelligent system that highlights customers requiring attention before renewal.

---

# Features

* Multi-source data ingestion
* Data cleaning and preprocessing
* Customer 360 dataset creation
* Product usage trend analysis
* Support health analysis
* NPS analysis
* LLM-powered CSM note analysis
* Product changelog analysis
* Explainable renewal risk scoring
* Plain-English risk explanations
* Recommended next actions
* Interactive Streamlit dashboard
* Exportable renewal reports

---

# Project Architecture

```
Raw Data
│
├── accounts.csv
├── usage_metrics.csv
├── support_tickets.csv
├── nps_responses.csv
├── csm_notes.txt
└── changelog.md
        │
        ▼
Data Loading
        │
        ▼
Data Cleaning
        │
        ▼
Feature Engineering
        │
        ▼
Customer 360 Dataset
        │
        ▼
Risk Engine
        │
        ▼
LLM Analysis
        │
        ▼
Report Generator
        │
        ▼
Streamlit Dashboard
```

---

# Project Structure

```
Renewal-Risk-Intelligence/

├── data/
│   ├── accounts.csv
│   ├── usage_metrics.csv
│   ├── support_tickets.csv
│   ├── nps_responses.csv
│   ├── csm_notes.txt
│   └── changelog.md
│
├── outputs/
│   ├── customer_360.csv
│   ├── risk_scored_accounts.csv
│   ├── final_report.csv
│   └── llm_analysis.csv
│
├── src/
│   ├── services/
│   ├── scoring/
│   ├── reporting/
│   ├── analysis/
│   └── utils/
│
├── app.py
├── main.py
├── requirements.txt
└── README.md
```

---

# Workflow

### Step 1 — Data Loading

The application loads all provided datasets including account information, product usage, support tickets, NPS responses, CSM notes, and the product changelog.

---

### Step 2 — Data Cleaning

The datasets are cleaned by:

* Handling missing values
* Standardizing formats
* Parsing dates
* Removing inconsistent records
* Preparing the data for feature engineering

---

### Step 3 — Feature Engineering

Business features are created such as:

* API usage decline
* Active user decline
* Workflow decline
* Ticket counts
* Escalations
* Resolution time
* Days until renewal
* NPS category

These features provide a complete view of customer health.

---

### Step 4 — Customer 360

All engineered features are merged into a single Customer 360 dataset.

Each row represents one customer and contains all important renewal signals.

---

### Step 5 — Risk Engine

A transparent rule-based scoring engine assigns a renewal risk score based on:

* Product adoption decline
* Customer activity decline
* Support ticket severity
* NPS feedback
* SDK version
* Contract renewal timeline
* ARR impact

Each account is classified as:

* High Risk
* Medium Risk
* Low Risk

The engine also records the reasons behind every score.

---

### Step 6 — LLM Analysis

Customer Success Manager notes are analyzed using an LLM through OpenRouter.

The model extracts business signals such as:

* Overall customer sentiment
* Budget concerns
* Competitor mentions
* Migration issues
* Executive involvement
* Renewal risk reasons

If an API key is unavailable, the application gracefully falls back to a deterministic heuristic approach so the project remains fully runnable.

---

### Step 7 — Report Generation

The report generator creates:

* Plain-English explanations
* Recommended actions
* Risk priorities

This makes the output useful for Customer Success Managers without requiring them to interpret raw metrics.

---

### Step 8 — Streamlit Dashboard

The dashboard allows users to:

* Filter customers by region, industry, and risk tier
* View renewal KPIs
* Explore risk distribution
* Analyze ARR at risk
* Review the highest-risk accounts
* Drill into individual customer details
* Download the final report

---

# Risk Scoring Logic

The final renewal risk score considers multiple business signals including:

* Product usage decline
* Active user decline
* Workflow decline
* Deprecated SDK usage
* Critical support tickets
* Ticket escalations
* Resolution time
* Customer satisfaction (NPS)
* Renewal timeline
* ARR value
* Plan tier
* AI-generated customer signals

This creates a more balanced view than relying on any single metric.

---

# Non-Obvious Insight

One insight identified in this project is that customers still using deprecated SDK versions often exhibit increased renewal risk, even when traditional customer health metrics appear acceptable.

By combining changelog information with product usage and support data, these hidden migration risks become visible much earlier.

---

# Technology Stack

* Python
* Pandas
* NumPy
* OpenAI SDK
* OpenRouter API
* Streamlit
* Plotly
* Regex
* dotenv

---

# Running the Project

## 1. Install dependencies

```bash
pip install -r requirements.txt
```

## 2. Configure API Key (Optional)

Create a `.env` file:

```text
OPENROUTER_API_KEY=your_api_key
```

The project can still run without an API key by using the fallback analysis.

---

## 3. Execute the pipeline

```bash
python main.py
```

Generated files will be saved in the `outputs` folder.

---

## 4. Launch the dashboard

```bash
streamlit run app.py
```

---

# Production Improvements

If this were developed further for production use, I would add:

* Machine learning-based risk prediction
* Automated entity matching across inconsistent customer names
* Prompt versioning and LLM monitoring
* Data validation and quality monitoring
* Pipeline scheduling using Airflow or Prefect
* Model performance tracking
* Better dashboard filtering and search
* Integration with CRM platforms such as Salesforce

---

# Tradeoffs

For this prototype, I chose a transparent and explainable rule-based scoring engine instead of a complex predictive model.

This makes every risk score easy to understand, debug, and explain to Customer Success teams while still demonstrating how AI can enhance decision-making through LLM-powered analysis of unstructured customer notes.

---

# Author

**Sanika Thorat**

Applied AI Engineer Take-Home Assignment
