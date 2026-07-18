import streamlit as st
import pandas as pd
import plotly.express as px

from utils.db import (
    get_companies,
    get_capital_data,
    get_capital_patterns
)

st.set_page_config(page_title="Capital Allocation")

st.title("💰 Capital Allocation")

# ----------------------------------------------------
# Select Company
# ----------------------------------------------------

companies = get_companies()

company = st.selectbox(
    "Select Company",
    companies["company_id"]
)

# ----------------------------------------------------
# Load Data
# ----------------------------------------------------

capital_df = get_capital_data(company)

pattern_df = get_capital_patterns()

# Keep only latest year for each company
pattern_df = pattern_df.sort_values("year")
pattern_df = pattern_df.groupby("company_id").tail(1).reset_index(drop=True)

# ----------------------------------------------------
# Capital Pattern Classification
# ----------------------------------------------------

def classify_pattern(row):

    equity = row["equity_capital"]
    reserves = row["reserves"]
    debt = row["borrowings"]

    if debt == 0 and reserves > equity:
        return "Cash Rich"

    elif debt == 0:
        return "Debt Free"

    elif debt > reserves * 2:
        return "Highly Leveraged"

    elif debt > reserves:
        return "Debt Heavy"

    elif reserves > debt * 2:
        return "Reserve Heavy"

    elif equity > reserves:
        return "Equity Heavy"

    elif debt == reserves:
        return "Balanced"

    else:
        return "Mixed Capital"

pattern_df["capital_pattern"] = pattern_df.apply(
    classify_pattern,
    axis=1
)
st.markdown("---")

st.subheader("🌳 Capital Allocation Patterns")

fig = px.treemap(
    pattern_df,
    path=["capital_pattern", "company_id"],
    values="total_assets",
    title="Capital Allocation Patterns"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.markdown("---")

pattern = st.selectbox(
    "Select Capital Pattern",
    sorted(pattern_df["capital_pattern"].unique())
)
filtered_df = pattern_df[
    pattern_df["capital_pattern"] == pattern
]

st.subheader(f"Companies in '{pattern}'")

st.dataframe(
    filtered_df,
    use_container_width=True
)
# ----------------------------------------------------
# Capital Allocation Data
# ----------------------------------------------------

st.markdown("---")

st.subheader("Capital Allocation Data")

st.dataframe(
    capital_df,
    use_container_width=True
)

# ----------------------------------------------------
# Trend Chart
# ----------------------------------------------------

metrics = [
    "equity_capital",
    "reserves",
    "borrowings"
]

for col in ["total_assets", "total_liabilities"]:
    if col in capital_df.columns:
        metrics.append(col)

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