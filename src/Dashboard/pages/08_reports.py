import streamlit as st
import pandas as pd

from utils.db import (
    get_companies,
    get_company_report
)

st.set_page_config(page_title="Reports")

st.title("📄 Company Reports")

companies = get_companies()

company = st.selectbox(
    "Select Company",
    companies["company_id"]
)

ratios, pl, bs, cf = get_company_report(company)

st.subheader("Financial Ratios")

st.dataframe(
    ratios,
    use_container_width=True
)

st.subheader("Profit & Loss")

st.dataframe(
    pl,
    use_container_width=True
)

st.subheader("Balance Sheet")

st.dataframe(
    bs,
    use_container_width=True
)

st.subheader("Cash Flow")

st.dataframe(
    cf,
    use_container_width=True
)

report = pd.concat(
    [ratios, pl, bs, cf],
    ignore_index=True,
    sort=False
)

csv = report.to_csv(index=False)

st.download_button(
    "⬇ Download Report",
    csv,
    file_name=f"{company}_report.csv",
    mime="text/csv"
)