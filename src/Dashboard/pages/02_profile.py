import streamlit as st

from utils.db import (
    get_ratios,
    get_pl,
    get_bs,
    get_cf,
    search_companies,
    get_company_info,
    get_revenue_profit,
    get_roe_asset_turnover
)

import plotly.express as px
st.set_page_config(page_title="Company Profile")

st.title("🏢 Company Profile")

# Search box
search_text = st.text_input(
    "🔍 Search Company",
    ""
)

companies = search_companies(search_text)

if companies.empty:
    st.warning("No matching company found.")
    st.stop()

company = st.selectbox(
    "Select Company",
    companies["company_id"]
)
info = get_company_info(company)
if not info.empty:

    st.subheader("🏢 Company Information")

    col1, col2 = st.columns(2)

    with col1:

        st.write("**Company** :", info.iloc[0]["company_id"])
        st.write("**Sector** :", info.iloc[0]["sector_name"])

    with col2:

        st.write("**Industry** :", info.iloc[0]["industry"])
        st.write("**Market Cap** :", info.iloc[0]["market_cap"])

    st.markdown("---")
# Load company data
ratios = get_ratios(company)
pl = get_pl(company)
bs = get_bs(company)
cf = get_cf(company)
revenue_df = get_revenue_profit(company)
roe_df = get_roe_asset_turnover(company)
st.subheader("📈 Revenue vs Net Profit (10 Years)")

fig = px.bar(
    revenue_df,
    x="year",
    y=["sales", "net_profit"],
    barmode="group",
    title="Revenue & Net Profit"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.markdown("---")
st.subheader("📈 ROE vs Asset Turnover")

fig = px.line(
    roe_df,
    x="year",
    y=[
        "roe_calculated",
        "asset_turnover"
    ],
    markers=True,
    title="ROE vs Asset Turnover"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
st.markdown("---")
st.header("📊 Financial Ratios")
st.dataframe(ratios, use_container_width=True)

st.header("📈 Profit & Loss")
st.dataframe(pl, use_container_width=True)

st.header("💰 Balance Sheet")
st.dataframe(bs, use_container_width=True)

st.header("💵 Cash Flow")
st.dataframe(cf, use_container_width=True)
