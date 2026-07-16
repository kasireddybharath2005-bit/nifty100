import streamlit as st
from utils.db import get_screener_filtered

st.set_page_config(page_title="Stock Screener")

st.title("📈 Stock Screener")

st.sidebar.header("Filters")
st.sidebar.markdown("## Presets")

quality = st.sidebar.button("⭐ Quality")
growth = st.sidebar.button("📈 Growth")
value = st.sidebar.button("💎 Value")
dividend = st.sidebar.button("💰 Dividend")
debt_free = st.sidebar.button("🏦 Debt Free")
turnaround = st.sidebar.button("🔄 Turnaround")

roe = st.sidebar.slider(
    "Minimum ROE",
    0.0, 50.0, 10.0
)

debt = st.sidebar.slider(
    "Maximum Debt/Equity",
    0.0, 10.0, 2.0
)

revenue = st.sidebar.slider(
    "Minimum Revenue CAGR",
    0.0, 50.0, 5.0
)

profit = st.sidebar.slider(
    "Minimum Profit CAGR",
    0.0, 50.0, 5.0
)

opm = st.sidebar.slider(
    "Minimum Operating Profit Margin",
    0.0, 60.0, 10.0
)

icr = st.sidebar.slider(
    "Minimum Interest Coverage",
    0.0, 100.0, 2.0
)
if quality:
    roe = 20
    debt = 0.5
    revenue = 10
    profit = 10
    opm = 15
    icr = 5

elif growth:
    roe = 15
    debt = 2
    revenue = 20
    profit = 20
    opm = 10
    icr = 2

elif value:
    roe = 12
    debt = 1
    revenue = 5
    profit = 5
    opm = 10
    icr = 2

elif dividend:
    roe = 10
    debt = 1
    revenue = 5
    profit = 5
    opm = 8
    icr = 2

elif debt_free:
    roe = 10
    debt = 0
    revenue = 5
    profit = 5
    opm = 8
    icr = 2

elif turnaround:
    roe = 5
    debt = 3
    revenue = 10
    profit = 10
    opm = 5
    icr = 1
df = get_screener_filtered(
    roe,
    debt,
    revenue,
    profit,
    opm,
    icr
)

st.subheader("📊 Filter Results")

st.metric(
    "Matching Companies",
    len(df)
)

if df.empty:

    st.warning("No companies match the selected filters.")

else:

    st.dataframe(
        df,
        use_container_width=True
    )

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name="filtered_companies.csv",
        mime="text/csv"
    )