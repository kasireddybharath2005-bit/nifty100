import streamlit as st

st.set_page_config(page_title="Home")

st.title("🏠 Home")

st.write("Welcome to Nifty100 Analytics Dashboard")

st.markdown("---")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Companies", "100")
col2.metric("Sectors", "10")
col3.metric("Peer Groups", "11")
col4.metric("Dashboard", "Running ✅")

st.markdown("---")

st.subheader("Project Overview")

st.write("""
This dashboard provides:

- 📊 Company Financial Profile
- 📈 Financial Ratio Analysis
- 🔍 Stock Screener
- 🤝 Peer Comparison
- 📉 Trend Analysis
- 🏭 Sector Analysis
- 💰 Capital Allocation
- 📄 Reports & Charts
""")

st.markdown("---")

st.success("Use the sidebar to navigate between dashboard pages.")

st.caption("Nifty100 Analytics Dashboard | Sprint 4")