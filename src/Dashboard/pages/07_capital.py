import streamlit as st

from utils.db import (
    get_companies,
    get_capital_data
)

st.set_page_config(page_title="Capital Allocation")

st.title("💰 Capital Allocation")

companies = get_companies()

company = st.selectbox(
    "Select Company",
    companies["company_id"]
)

capital_df = get_capital_data(company)

st.subheader("Capital Allocation Table")

st.dataframe(
    capital_df,
    use_container_width=True
)

if not capital_df.empty:

    latest = capital_df.iloc[-1]

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Equity Capital",
        latest["equity_capital"]
    )

    c2.metric(
        "Reserves",
        latest["reserves"]
    )

    c3.metric(
        "Borrowings",
        latest["borrowings"]
    )

    st.markdown("---")

    st.subheader("Equity Capital Trend")

    st.line_chart(
        capital_df.set_index("year")["equity_capital"]
    )

    st.subheader("Reserves Trend")

    st.line_chart(
        capital_df.set_index("year")["reserves"]
    )

    st.subheader("Borrowings Trend")

    st.line_chart(
        capital_df.set_index("year")["borrowings"]
    )