import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Renewal Risk Intelligence",
    page_icon="📊",
    layout="wide"
)

# =====================================================
# Load Data
# =====================================================

df = pd.read_csv("outputs/final_report.csv")

# =====================================================
# Sidebar Filters
# =====================================================

st.sidebar.title("Filters")

risk_filter = st.sidebar.multiselect(
    "Risk Tier",
    options=df["risk_tier"].dropna().unique(),
    default=df["risk_tier"].dropna().unique()
)

region_filter = st.sidebar.multiselect(
    "Region",
    options=df["region"].dropna().unique(),
    default=df["region"].dropna().unique()
)

industry_filter = st.sidebar.multiselect(
    "Industry",
    options=df["industry"].dropna().unique(),
    default=df["industry"].dropna().unique()
)

filtered_df = df[
    (df["risk_tier"].isin(risk_filter))
    &
    (df["region"].isin(region_filter))
    &
    (df["industry"].isin(industry_filter))
]

# =====================================================
# Title
# =====================================================

st.title("📊 Renewal Risk Intelligence Dashboard")

st.markdown("---")

# =====================================================
# KPI Cards
# =====================================================

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

# =====================================================
# Charts
# =====================================================

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

# =====================================================
# ARR by Risk Tier
# =====================================================

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

# =====================================================
# Top Risk Accounts
# =====================================================

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

# =====================================================
# Account Explorer
# =====================================================

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

# =====================================================
# Usage Metrics
# =====================================================

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

# =====================================================
# Ticket & NPS Summary
# =====================================================

a, b, c, d = st.columns(4)

a.metric("P1 Tickets", int(row["p1_tickets"]))

b.metric("Open Tickets", int(row["open_tickets"]))

score = row["score"] if pd.notna(row["score"]) else "N/A"
c.metric("NPS Score", score)

sdk = row["latest_sdk"] if pd.notna(row["latest_sdk"]) else "N/A"
d.metric("SDK Version", sdk)

st.markdown("---")

# =====================================================
# Download Report
# =====================================================

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Final Report",
    data=csv,
    file_name="renewal_risk_report.csv",
    mime="text/csv"
)