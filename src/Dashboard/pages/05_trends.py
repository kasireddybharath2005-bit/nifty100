import streamlit as st
import plotly.express as px
import numpy as np
import pandas as pd

from utils.db import (
    get_trend_companies,
    get_company_trend
)

st.set_page_config(
    page_title="Trend Analysis"
)

st.title("📈 Trend Analysis")

companies = get_trend_companies()

company = st.selectbox(
    "Select Company",
    companies["company_id"]
)

trend_df = get_company_trend(company)
st.markdown("---")

st.subheader("📊 Select Metrics")

metric_options = [
    "roe_calculated",
    "roa",
    "net_profit_margin",
    "operating_profit_margin",
    "asset_turnover",
    "debt_to_equity",
    "revenue_cagr_3yr",
    "revenue_cagr_5yr",
    "revenue_cagr_10yr",
    "profit_cagr_3yr",
    "profit_cagr_5yr",
    "profit_cagr_10yr",
    "eps_cagr_3yr",
    "eps_cagr_5yr",
    "eps_cagr_10yr"
]

selected_metrics = st.multiselect(
    "Choose up to 3 metrics",
    metric_options,
    default=["roe_calculated"],
    max_selections=3
)
st.write("Selected Metrics:")

st.write(selected_metrics)
st.markdown("---")

st.subheader("📈 Trend Chart")

if len(selected_metrics) > 0:

    fig = px.line(
        trend_df,
        x="year",
        y=selected_metrics,
        markers=True,
        title="Financial Trends Over Time"
    )

    for metric in selected_metrics:

        yoy = trend_df[metric].pct_change() * 100

        for i in range(1, len(trend_df)):

            if pd.notna(yoy.iloc[i]):
                fig.add_annotation(
                    x=trend_df["year"].iloc[i],
                    y=trend_df[metric].iloc[i],
                    text=f"{yoy.iloc[i]:.1f}%",
                    showarrow=False,
                    font=dict(size=9)
                )

    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Metric Value",
        legend_title="Metrics"
    )


    fig.update_xaxes(
        tickangle=-45
    )



    st.plotly_chart(
        fig,
        use_container_width=True
    )
st.markdown("---")


st.subheader("Financial Data")

st.dataframe(
    trend_df,
    use_container_width=True
)

st.markdown("---")

st.subheader("📌 Latest Values")

latest = trend_df.iloc[-1]

cols = st.columns(len(selected_metrics))

for i, metric in enumerate(selected_metrics):

    cols[i].metric(
        metric.replace("_", " ").title(),
        round(latest[metric], 2)
    )