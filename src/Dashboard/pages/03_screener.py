import streamlit as st

from utils.db import get_screener_data

st.set_page_config(
    page_title="Stock Screener",
    page_icon="🔎",
    layout="wide"
)

st.title("🔎 Stock Screener")

df = get_screener_data()

st.sidebar.header("Filters")

min_roe = st.sidebar.slider(
    "Minimum ROE",
    0.0,
    50.0,
    15.0
)

max_de = st.sidebar.slider(
    "Maximum Debt to Equity",
    0.0,
    5.0,
    1.0
)

min_margin = st.sidebar.slider(
    "Minimum Net Profit Margin",
    0.0,
    50.0,
    10.0
)

filtered = df[
    (df["roe_calculated"] >= min_roe) &
    (df["debt_to_equity"] <= max_de) &
    (df["net_profit_margin"] >= min_margin)
]

st.subheader("Filtered Companies")

st.dataframe(
    filtered,
    use_container_width=True
)

st.success(f"{len(filtered)} Companies Found")