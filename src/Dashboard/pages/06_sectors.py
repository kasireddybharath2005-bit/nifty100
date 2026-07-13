import streamlit as st

from utils.db import get_sector_data

st.set_page_config(page_title="Sector Analysis")

st.title("🏭 Sector Analysis")

sector_df = get_sector_data()

st.subheader("Sector-wise Companies")

st.dataframe(sector_df, use_container_width=True)

st.subheader("Sector Distribution")

chart_df = sector_df.set_index("sector_name")

st.bar_chart(chart_df["total_companies"])

st.metric("Total Sectors", len(sector_df))