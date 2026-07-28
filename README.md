# Nifty100 Analytics Dashboard

## Project Overview

The Nifty100 Analytics Dashboard is a Python-based financial analytics project that analyzes the financial performance of Nifty100 companies.

The project includes:

- ETL Pipeline
- SQLite Database
- FastAPI REST APIs
- Streamlit Dashboard
- Company Screener
- Peer Comparison
- Valuation Analysis
- KMeans Clustering
- PDF Tear Sheets
- Pytest Test Suite

---

# Technology Stack

- Python 3.13
- Pandas
- SQLite
- FastAPI
- Streamlit
- Matplotlib
- Scikit-Learn
- Pytest

---

# Project Structure

```
src/
    analytics/
    api/
    Dashboard/
    etl/
    screener/

db/
output/
reports/
tests/
docs/
```

---

# Installation

```
pip install -r requirements.txt
```

---

# Run ETL

```
python src/etl/loader.py
```

---

# Run FastAPI

```
uvicorn src.api.main:app --reload
```

---

# Run Dashboard

```
streamlit run src/Dashboard/app.py
```

---

# Run Tests

```
py -m pytest tests
```

---

# Generate HTML Report

```
py -m pytest tests --html=reports/pytest_report.html
```

---

# Author

Kasireddy Bharath Hari Kumar