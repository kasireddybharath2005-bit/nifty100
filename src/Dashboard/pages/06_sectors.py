import streamlit as st
import plotly.express as px
from utils.db import (
    get_sectors,
    get_sector_data,
    get_sector_distribution
)

st.set_page_config(page_title="Sector Analysis")

st.title("🏭 Sector Analysis")

sectors = get_sectors()

sector = st.selectbox(
    "Select Sector",
    sectors["sector_name"]
)
sector_df = get_sector_data(sector)

st.markdown("---")



st.subheader("Sector Companies")

st.dataframe(
    sector_df,
    use_container_width=True
)

st.markdown("---")

st.subheader("📊 Sector Distribution")

distribution_df = get_sector_distribution()

fig = px.bar(
    distribution_df,
    x="sector_name",
    y="total_companies",
    text="total_companies",
    title="Companies by Sector"
)

fig.update_layout(
    xaxis_title="Sector",
    yaxis_title="Number of Companies"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
st.markdown("---")

st.subheader("📌 Sector Summary")

total_sectors = distribution_df["sector_name"].nunique()

selected_companies = len(sector_df)

total_companies = distribution_df["total_companies"].sum()

sector_percentage = (
    selected_companies / total_companies * 100
    if total_companies > 0 else 0
)

industry_count = sector_df["industry"].nunique()
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Sectors",
    total_sectors
)

col2.metric(
    "Companies",
    selected_companies
)

col3.metric(
    "Industries",
    industry_count
)

col4.metric(
    "Share of Total",
    f"{sector_percentage:.1f}%"
)
st.markdown("---")

st.subheader("🏢 Industry Breakdown")
industry_df = (
    sector_df.groupby("industry")
    .size()
    .reset_index(name="company_count")
)
fig = px.bar(
    industry_df,
    x="industry",
    y="company_count",
    text="company_count",
    title=f"Industry Breakdown - {sector}"
)

fig.update_layout(
    xaxis_title="Industry",
    yaxis_title="Number of Companies"
)

st.plotly_chart(
    fig,
    use_container_width=True
)