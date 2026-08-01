# 📊 Renewal Risk Intelligence

## Overview

This project is a Renewal Risk Intelligence system built for the Contentstack Applied AI Engineer take-home assignment.

The goal is to help the BizOps team identify which customer accounts are most likely to churn or face renewal issues before their contract expires.

Instead of relying only on manual investigation, this project combines multiple customer signals such as product usage, support history, NPS responses, customer success notes, and product changelog information to generate a renewal risk score along with a clear explanation and recommended next action.

---

# Problem Statement

Customer Success teams receive information from many different places:

- Customer account details
- Product usage data
- Support tickets
- NPS survey responses
- CSM meeting notes
- Product changelog updates

Looking at these sources separately makes it difficult to understand the real health of a customer.

This project combines all these data sources into one Customer 360 view and predicts renewal risk in an explainable way.

---

# Features

✔ Loads and processes multiple data sources

✔ Cleans and merges customer information

✔ Builds Customer 360 dataset

✔ Engineers customer health features

✔ Calculates renewal risk score

✔ Classifies customers into High, Medium and Low risk

✔ Generates plain-English explanations

✔ Suggests recommended actions for Customer Success teams

✔ Uses an LLM to analyze unstructured CSM notes

✔ Detects migration risks from product changelog information

✔ Interactive Streamlit dashboard for exploring customer health

---

# Project Workflow

```
Raw Data
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
Risk Scoring Engine
    │
    ▼
LLM Analysis
    │
    ▼
Final Report
    │
    ▼
Streamlit Dashboard
```

---

# Project Structure

```
Renewal-Risk-Intelligence
│
├── raw/
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

# Technologies Used

- Python
- Pandas
- Streamlit
- Plotly
- OpenAI / OpenRouter API
- Regular Expressions (Regex)
- dotenv

---

# How the Risk Score is Calculated

The final renewal risk score is calculated using multiple customer signals, including:

- Product usage decline
- Active user decline
- Workflow activity
- SDK version
- Support ticket history
- P1 incidents
- Ticket escalation
- Resolution time
- NPS score
- Renewal timeline
- ARR value
- Plan tier
- AI analysis of customer notes

These signals are combined to classify each customer as:

- 🔴 High Risk
- 🟡 Medium Risk
- 🟢 Low Risk

---

# AI (LLM) Integration

The project uses an LLM through the OpenRouter API to analyze Customer Success Manager (CSM) notes.

The AI extracts useful business signals such as:

- Customer sentiment
- Budget concerns
- Migration issues
- Executive involvement
- Competitor mentions
- Renewal risk reason

These insights are then combined with structured customer data to improve the overall risk assessment.

---

# Dashboard

The Streamlit dashboard provides:

- Overall business KPIs
- Risk distribution
- ARR at risk
- Risk score distribution
- Top high-risk accounts
- Customer explorer
- Customer health summary
- Usage metrics
- Support metrics
- Downloadable final report

---

# Outputs

Running the project generates:

- Customer 360 Dataset
- Risk Scored Accounts
- Final Renewal Report
- LLM Analysis Results

All outputs are saved inside the `outputs/` folder.

---

# Run the Project

Install dependencies

```bash
pip install -r requirements.txt
```

(Optional) Add your API key

```
OPENROUTER_API_KEY=your_api_key
```

Run the pipeline

```bash
python main.py
```

Launch the dashboard

```bash
streamlit run app.py
```

---

# Future Improvements

If this project were developed further, I would add:

- Machine Learning based risk prediction
- Real-time dashboard updates
- Salesforce integration
- Automatic email alerts
- Better account matching
- Historical trend analysis
- Model monitoring and logging
- Cloud deployment

---

# Assignment Requirements Covered

✔ Python-based solution

✔ Multiple data sources integrated

✔ Customer 360 dataset

✔ Renewal risk scoring

✔ Plain-English explanations

✔ Recommended customer actions

✔ LLM integration

✔ Streamlit dashboard

✔ README documentation

✔ End-to-end working pipeline

---

# Author

**Sanika Thorat**
