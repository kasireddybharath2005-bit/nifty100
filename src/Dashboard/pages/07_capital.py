import streamlit as st
import plotly.express as px
import pandas as pd
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

st.markdown("---")

st.subheader("Capital Allocation Data")

st.dataframe(
    capital_df,
    use_container_width=True
)

st.markdown("---")

st.subheader("📈 Capital Allocation Trend")
metrics = [
    "equity_capital",
    "reserves",
    "borrowings"
]

# Include these only if they exist
for col in ["total_assets", "total_liabilities"]:
    if col in capital_df.columns:
        metrics.append(col)

# Create the chart AFTER the loop
fig = px.line(
    capital_df,
    x="year",
    y=metrics,
    markers=True,
    title=f"Capital Allocation - {company}"
)

fig.update_layout(
    xaxis_title="Year",
    yaxis_title="Amount",
    legend_title="Metrics"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
st.markdown("---")

st.subheader("📌 Latest Capital Position")
latest = capital_df.iloc[-1]
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Equity Capital",
    f"{latest['equity_capital']:.2f}"
)

col2.metric(
    "Reserves",
    f"{latest['reserves']:.2f}"
)

col3.metric(
    "Borrowings",
    f"{latest['borrowings']:.2f}"
)

if "debt_to_equity" in capital_df.columns:
    col4.metric(
        "Debt to Equity",
        f"{latest['debt_to_equity']:.2f}"
    )
else:
    col4.metric(
        "Debt to Equity",
        "N/A"
    )

    st.markdown("---")

    st.subheader("📊 Capital Structure Breakdown")

    breakdown_df = pd.DataFrame({
        "Component": [
            "Equity Capital",
            "Reserves",
            "Borrowings"
        ],
        "Amount": [
            latest["equity_capital"],
            latest["reserves"],
            latest["borrowings"]
        ]
    })

    fig = px.bar(
        breakdown_df,
        x="Component",
        y="Amount",
        text="Amount",
        title=f"Latest Capital Structure - {company}"
    )

    fig.update_layout(
        xaxis_title="Capital Components",
        yaxis_title="Amount"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )