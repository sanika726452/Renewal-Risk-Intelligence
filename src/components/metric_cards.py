import streamlit as st


def metric_card(title, value, emoji):

    st.markdown(
        f"""
        <div class="metric-box">
            <div style="font-size:32px;">{emoji}</div>
            <div class="metric-number">{value}</div>
            <div class="metric-label">{title}</div>
        </div>
        """,
        unsafe_allow_html=True
    )