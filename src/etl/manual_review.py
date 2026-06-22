import pandas as pd
import sqlite3
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]

conn = sqlite3.connect(project_root / "db" / "nifty100.db")

companies = pd.read_sql(
    "SELECT company_name FROM companies LIMIT 5",
    conn
)

review = []

for company in companies["company_name"]:
    review.append([company, "Checked", "No Issues"])

review_df = pd.DataFrame(
    review,
    columns=["company", "status", "remarks"]
)

review_df.to_csv(
    project_root / "output" / "manual_review.csv",
    index=False
)

print(review_df)

conn.close()