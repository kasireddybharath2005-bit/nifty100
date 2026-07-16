import streamlit as st
from utils.db import get_screener_filtered

st.set_page_config(page_title="Stock Screener")

st.title("📈 Stock Screener")

st.sidebar.header("Filters")

roe = st.sidebar.slider(
    "Minimum ROE",
    0.0,
    50.0,
    10.0
)

debt = st.sidebar.slider(
    "Maximum Debt/Equity",
    0.0,
    10.0,
    2.0
)

npm = st.sidebar.slider(
    "Minimum Net Profit Margin",
    0.0,
    50.0,
    5.0
)

opm = st.sidebar.slider(
    "Minimum Operating Profit Margin",
    0.0,
    60.0,
    10.0
)

asset = st.sidebar.slider(
    "Minimum Asset Turnover",
    0.0,
    5.0,
    1.0
)

df = get_screener_filtered(
    roe,
    debt,
    npm,
    opm,
    asset
)

st.metric(
    "Matching Companies",
    len(df)
)

st.dataframe(
    df,
    use_container_width=True
)