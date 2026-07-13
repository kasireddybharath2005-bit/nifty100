import streamlit as st
import pandas as pd

from utils.db import (
    get_companies,
    get_trend_data
)

st.set_page_config(page_title="Trends")

st.title("📈 Trends Analysis")

companies = get_companies()

company = st.selectbox(
    "Select Company",
    companies["company_id"]
)

trend_df = get_trend_data(company)

st.subheader("Financial Trend Data")

st.dataframe(trend_df, use_container_width=True)

if not trend_df.empty:

    trend_df["year"] = trend_df["year"].astype(str)

    st.subheader("ROE Trend")

    st.line_chart(
        trend_df.set_index("year")["roe_calculated"]
    )

    st.subheader("Net Profit Margin")

    st.line_chart(
        trend_df.set_index("year")["net_profit_margin"]
    )

    st.subheader("Operating Profit Margin")

    st.line_chart(
        trend_df.set_index("year")["operating_profit_margin"]
    )

    st.subheader("Asset Turnover")

    st.line_chart(
        trend_df.set_index("year")["asset_turnover"]
    )

    st.subheader("Debt to Equity")

    st.line_chart(
        trend_df.set_index("year")["debt_to_equity"]
    )

else:

    st.warning("No data found.")