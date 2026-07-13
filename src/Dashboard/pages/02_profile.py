import streamlit as st

from utils.db import (
    get_companies,
    get_ratios,
    get_pl,
    get_bs,
    get_cf
)

st.set_page_config(page_title="Company Profile")

st.title("🏢 Company Profile")

companies = get_companies()

company = st.selectbox(
    "Select Company",
    companies["company_id"]
)

ratios = get_ratios(company)
pl = get_pl(company)
bs = get_bs(company)
cf = get_cf(company)

st.header("📊 Financial Ratios")
st.dataframe(ratios, use_container_width=True)

st.header("📈 Profit & Loss")
st.dataframe(pl, use_container_width=True)

st.header("💰 Balance Sheet")
st.dataframe(bs, use_container_width=True)

st.header("💵 Cash Flow")
st.dataframe(cf, use_container_width=True)