"""
Renewal Risk Intelligence Dashboard
A comprehensive Streamlit application for analyzing and managing customer renewal risk.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
from pathlib import Path


# PAGE CONFIGURATION


st.set_page_config(
    page_title="Renewal Risk Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": "Renewal Risk Intelligence Dashboard v1.0"
    }
)


# CUSTOM STYLING & THEME


st.markdown("""
<style>
    /* Main Background */
    .main {
        background-color: #f8f9fa;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #1e293b;
        color: #f1f5f9;
    }
    
    /* Header Styling */
    h1, h2, h3 {
        color: #0f172a;
        font-weight: 700;
    }
    
    /* Metric Card Styling */
    .metric-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        padding: 20px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .metric-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 12px rgba(0, 0, 0, 0.15);
    }
    
    .metric-number {
        font-size: 28px;
        font-weight: 700;
        margin: 10px 0;
    }
    
    .metric-label {
        font-size: 14px;
        opacity: 0.9;
    }
    
    /* Risk Tier Colors */
    .risk-high {
        color: #dc2626;
    }
    
    .risk-medium {
        color: #ea580c;
    }
    
    .risk-low {
        color: #16a34a;
    }
    
    /* Button Styling */
    .stButton > button {
        border-radius: 8px;
        border: none;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    /* Divider */
    hr {
        margin: 20px 0;
        border: none;
        border-top: 2px solid #e2e8f0;
    }
    
    /* Dataframe Styling */
    .dataframe {
        border-radius: 8px;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)


# LOAD & CACHE DATA


@st.cache_data
def load_data():
    """Load data from CSV with caching."""
    try:
        df = pd.read_csv("outputs/final_report.csv")
        return df
    except FileNotFoundError:
        st.error("❌ Data file not found. Please run `python main.py` first.")
        st.stop()

df = load_data()


# SIDEBAR FILTERS


st.sidebar.markdown("### 🔍 FILTERS")
st.sidebar.markdown("---")

# Risk Tier Filter
risk_filter = st.sidebar.multiselect(
    "Risk Tier",
    options=sorted(df["risk_tier"].dropna().unique()),
    default=sorted(df["risk_tier"].dropna().unique()),
    key="risk_filter"
)

# Region Filter
region_filter = st.sidebar.multiselect(
    "Region",
    options=sorted(df["region"].dropna().unique()),
    default=sorted(df["region"].dropna().unique()),
    key="region_filter"
)

# Industry Filter
industry_filter = st.sidebar.multiselect(
    "Industry",
    options=sorted(df["industry"].dropna().unique()),
    default=sorted(df["industry"].dropna().unique()),
    key="industry_filter"
)

# ARR Range Slider
arr_min, arr_max = float(df["arr"].min()), float(df["arr"].max())
arr_range = st.sidebar.slider(
    "ARR Range ($)",
    min_value=arr_min,
    max_value=arr_max,
    value=(arr_min, arr_max),
    step=10000.0
)

# Apply Filters
filtered_df = df[
    (df["risk_tier"].isin(risk_filter))
    & (df["region"].isin(region_filter))
    & (df["industry"].isin(industry_filter))
    & (df["arr"] >= arr_range[0])
    & (df["arr"] <= arr_range[1])
]

st.sidebar.markdown("---")
st.sidebar.info(f"📊 Showing {len(filtered_df)} of {len(df)} accounts")



# Title


st.title("📊 Renewal Risk Intelligence Dashboard")

st.markdown("---")


# KPI Cards


total_accounts = len(filtered_df)

high = len(filtered_df[filtered_df["risk_tier"] == "High"])

medium = len(filtered_df[filtered_df["risk_tier"] == "Medium"])

low = len(filtered_df[filtered_df["risk_tier"] == "Low"])

arr_at_risk = filtered_df[
    filtered_df["risk_tier"] == "High"
]["arr"].sum()

avg_risk_score = round(filtered_df["risk_score"].mean(), 1)

col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)

with col1:
    st.metric("Total Accounts", total_accounts)

with col2:
    st.metric("🔴 High Risk", high)

with col3:
    st.metric("🟡 Medium Risk", medium)

with col4:
    st.metric("🟢 Low Risk", low)

with col5:
    st.metric("💰 ARR at Risk", f"${arr_at_risk:,.0f}")

with col6:
    st.metric("📈 Avg Risk Score", avg_risk_score)

st.markdown("---")


# Charts


left, right = st.columns(2)

with left:

    fig = px.pie(
        filtered_df,
        names="risk_tier",
        title="Risk Tier Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

with right:

    fig = px.histogram(
        filtered_df,
        x="risk_score",
        nbins=20,
        title="Risk Score Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")


# ARR by Risk Tier


arr_df = (
    filtered_df
    .groupby("risk_tier")["arr"]
    .sum()
    .reset_index()
)

fig = px.bar(
    arr_df,
    x="risk_tier",
    y="arr",
    title="ARR by Risk Tier"
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")


# Top Risk Accounts


st.subheader("Top 10 High Risk Accounts")

top10 = (
    filtered_df
    .sort_values("risk_score", ascending=False)
    .head(10)
)

st.dataframe(
    top10[
        [
            "account_name",
            "risk_score",
            "risk_tier",
            "arr",
            "risk_reasons",
            "recommended_action"
        ]
    ],
    use_container_width=True
)

st.markdown("---")


# Account Explorer


st.subheader("Customer Explorer")

account = st.selectbox(
    "Select Account",
    filtered_df["account_name"].sort_values()
)

row = filtered_df[
    filtered_df["account_name"] == account
].iloc[0]

c1, c2 = st.columns(2)

with c1:

    st.write("### Customer Details")

    st.write(f"**Account:** {row['account_name']}")
    st.write(f"**Region:** {row['region']}")
    st.write(f"**Industry:** {row['industry']}")
    st.write(f"**Plan:** {row['plan_tier']}")
    st.write(f"**ARR:** ${row['arr']:,}")

with c2:

    st.write("### Risk Details")

    st.write(f"**Risk Score:** {row['risk_score']}")
    st.write(f"**Risk Tier:** {row['risk_tier']}")
    st.write(f"**Reasons:** {row['risk_reasons']}")
    st.write(f"**Recommendation:** {row['recommended_action']}")

st.markdown("---")

# Usage Metrics

st.subheader("Usage Metrics")

m1, m2, m3 = st.columns(3)

m1.metric(
    "API Decline %",
    f"{row['api_decline_pct']}%"
)

m2.metric(
    "Active User Decline %",
    f"{row['active_user_decline_pct']}%"
)

m3.metric(
    "Workflow Decline %",
    f"{row['workflow_decline_pct']}%"
)

st.markdown("---")


# Ticket & NPS Summary


a, b, c, d = st.columns(4)

a.metric("P1 Tickets", int(row["p1_tickets"]))

b.metric("Open Tickets", int(row["open_tickets"]))

score = row["score"] if pd.notna(row["score"]) else "N/A"
c.metric("NPS Score", score)

sdk = row["latest_sdk"] if pd.notna(row["latest_sdk"]) else "N/A"
d.metric("SDK Version", sdk)

st.markdown("---")


# Download Report


csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Final Report",
    data=csv,
    file_name="renewal_risk_report.csv",
    mime="text/csv"
)