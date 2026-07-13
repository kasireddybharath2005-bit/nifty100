import streamlit as st

from utils.db import (
    get_companies,
    get_peer_data
)

st.set_page_config(page_title="Peer Comparison")

st.title("🤝 Peer Comparison")

companies = get_companies()

company = st.selectbox(
    "Select Company",
    companies["company_id"]
)

peer_df = get_peer_data(company)

st.subheader("Peer Group Comparison")
st.dataframe(peer_df, use_container_width=True)

st.metric("Companies in Peer Group", len(peer_df))