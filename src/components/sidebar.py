import streamlit as st


def show_sidebar():

    st.sidebar.title("📊 Navigation")

    page = st.sidebar.radio(
        "",
        [
            "Dashboard",
            "Upload Data",
            "Risk Analysis",
            "AI Insights",
            "Export Report"
        ]
    )

    return page