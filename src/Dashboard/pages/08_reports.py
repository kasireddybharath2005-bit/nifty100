import streamlit as st
import pandas as pd
from utils.db import (
    get_companies,
    get_company_report,
    get_annual_reports

)

st.set_page_config(page_title="Company Reports")

st.title("📄 Company Financial Report")

companies = get_companies()

company = st.selectbox(
    "Select Company",
    companies["company_id"]
)

ratios, pl, bs, cf = get_company_report(company)
reports_df = get_annual_reports(company)

st.markdown("---")

st.subheader("📊 Financial Ratios")
st.dataframe(ratios, use_container_width=True)

st.subheader("💰 Profit & Loss")
st.dataframe(pl, use_container_width=True)

st.subheader("🏦 Balance Sheet")
st.dataframe(bs, use_container_width=True)

st.subheader("💵 Cash Flow")
st.dataframe(cf, use_container_width=True)

st.markdown("---")



st.subheader("📌 Report Summary")

latest_year = ratios["year"].max()

years_available = ratios["year"].nunique()

total_records = (
    len(ratios)
    + len(pl)
    + len(bs)
    + len(cf)
)

sections = 4
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Latest Year",
    latest_year
)

col2.metric(
    "Years Available",
    years_available
)

col3.metric(
    "Report Sections",
    sections
)

col4.metric(
    "Total Records",
    total_records
)

st.markdown("---")

st.subheader("📄 Annual Reports")
if reports_df.empty:

    st.warning("No annual reports available.")

else:

    for _, row in reports_df.iterrows():

        col1, col2 = st.columns([1, 3])

        with col1:
            st.write(f"**{row['Year']}**")

        with col2:

            if pd.isna(row["Annual_Report"]) or row["Annual_Report"] == "":

                st.error("🔴 Report unavailable")

            else:

                st.link_button(
                    "📄 Open Annual Report",
                    row["Annual_Report"]
                )
st.markdown("---")

st.subheader("⬇️ Download Report")
report_df = pd.concat(
    [
        ratios.assign(Section="Financial Ratios"),
        pl.assign(Section="Profit & Loss"),
        bs.assign(Section="Balance Sheet"),
        cf.assign(Section="Cash Flow")
    ],
    ignore_index=True,
    sort=False
)
csv = report_df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="📥 Download Company Report (CSV)",
    data=csv,
    file_name=f"{company}_financial_report.csv",
    mime="text/csv"
)
