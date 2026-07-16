import streamlit as st
import plotly.express as px
from utils.db import (
    get_home_kpis,
    get_sector_distribution,
    get_top_companies,
    get_years
)
st.set_page_config(
    page_title="Home",
    page_icon="🏠",
    layout="wide"
)
st.sidebar.header("Dashboard Filters")

years = get_years()

selected_year = st.sidebar.selectbox(
    "Select Year",
    years
)
st.title("🏠 Home")
st.write(f"📅 Selected Year: **{selected_year}**")
st.write("Welcome to Nifty100 Analytics Dashboard")

st.markdown("---")

kpi = get_home_kpis(selected_year)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Average ROE",
        f"{kpi['avg_roe']} %"
    )

with col2:
    st.metric(
        "Average Debt/Equity",
        kpi["avg_de"]
    )

with col3:
    st.metric(
        "Average Asset Turnover",
        kpi["avg_asset_turnover"]
    )

col4, col5, col6 = st.columns(3)

with col4:
    st.metric(
        "Revenue CAGR (5Y)",
        f"{kpi['avg_revenue_cagr']} %"
    )

with col5:
    st.metric(
        "EPS CAGR (3Y)",
        f"{kpi['avg_eps_growth']} %"
    )

with col6:
    st.metric(
        "Debt-Free Companies",
        int(kpi["debt_free_companies"])
    )
st.markdown("---")

st.subheader("Sector Distribution")

sector_df = get_sector_distribution()

fig = px.pie(
    sector_df,
    names="sector_name",
    values="total_companies",
    hole=0.5,
    title="Companies by Sector"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
st.metric(
    "Total Sectors",
    sector_df.shape[0]
)
st.markdown("---")


st.subheader("🏆 Top 5 Companies by Composite Score")
top_df = get_top_companies(selected_year)

top_df.index = top_df.index + 1

st.dataframe(
    top_df,
    use_container_width=True
)
st.subheader("Project Overview")

st.write("""
📊 Company Financial Profile

📈 Financial Ratio Analysis

🔍 Stock Screener

🤝 Peer Comparison

📉 Trend Analysis

🏭 Sector Analysis

💰 Capital Allocation

📄 Reports & Charts
""")

