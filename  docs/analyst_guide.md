# Nifty100 Analytics Dashboard

# User Guide

---

# 1. Introduction

This dashboard provides financial analysis for Nifty100 companies.

---

# 2. Dashboard

The dashboard contains

- Company Profile
- Screener
- Valuation
- Sector Analysis
- Peer Comparison
- Reports

---

# 3. Company Profile

Search company by ticker.

Example:

TCS

INFY

ABB

---

# 4. Screener

Apply filters

- ROE
- PE Ratio
- PB Ratio
- CAGR
- Debt

---

# 5. Sector Analysis

Compare companies by sector.

---

# 6. Peer Comparison

Compare companies within the same peer group.

---

# 7. Valuation

Shows

- PE Ratio
- PB Ratio
- EV/EBITDA
- Dividend Yield

---

# 8. Portfolio

Displays portfolio summary.

---

# 9. REST API

Base URL

http://127.0.0.1:8000

Example

GET /api/v1/companies

GET /api/v1/valuation

GET /api/v1/sectors

GET /api/v1/screener

---

# 10. Troubleshooting

If API is unavailable

Restart

uvicorn src.api.main:app --reload

If Dashboard fails

Restart

streamlit run src/Dashboard/app.py

---

# End