import streamlit as st

st.set_page_config(
    page_title="Nifty100 Analytics Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📈 Nifty100 Analytics Dashboard")

st.markdown("""
Welcome to the Nifty100 Analytics Dashboard.

Use the sidebar to navigate through all dashboard pages.
""")

st.sidebar.success("Select a page above.")

st.info("""
Available Pages

🏠 Home

🏢 Company Profile

🔎 Screener

👥 Peer Comparison

📈 Trends

🏭 Sectors

💰 Capital Allocation

📄 Reports
""")

col1, col2, col3 = st.columns(3)

col1.metric("Companies", "100")
col2.metric("Peer Groups", "11")
col3.metric("Status", "Running ✅")