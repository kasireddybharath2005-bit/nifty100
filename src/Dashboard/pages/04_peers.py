import streamlit as st

from utils.db import (
    get_peer_companies,
    get_peer_comparison,
    get_peer_radar,
    get_peer_summary
)

import plotly.graph_objects as go
st.set_page_config(
    page_title="Peer Comparison"
)

st.title("🤝 Peer Comparison")

companies = get_peer_companies()




company = st.selectbox(
    "Select Company",
    companies["company_id"]
)

peer_df = get_peer_comparison(company)
st.subheader("📊 Peer Comparison Table")

st.dataframe(
    peer_df,
    use_container_width=True
)

st.markdown("---")

st.subheader("📈 Radar Chart")

company_metrics, peer_metrics = get_peer_radar(company)

fig = go.Figure()

fig.add_trace(
    go.Scatterpolar(
        r=company_metrics["value"],
        theta=company_metrics["metric"],
        fill="toself",
        name=company
    )
)

fig.add_trace(
    go.Scatterpolar(
        r=peer_metrics["avg_value"],
        theta=peer_metrics["metric"],
        fill="toself",
        name="Peer Average"
    )
)

fig.update_layout(
    title="Peer Radar Comparison",
    polar=dict(
        radialaxis=dict(
            visible=True
        )
    ),
    showlegend=True
)

st.plotly_chart(
    fig,
    use_container_width=True
)
st.markdown("---")

st.subheader("📋 KPI Summary")

summary_df = get_peer_summary(company)

st.dataframe(
    summary_df,
    use_container_width=True
)