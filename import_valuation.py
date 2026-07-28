from pathlib import Path
import pandas as pd
import sqlite3

project_root = Path(__file__).resolve().parent

excel_file = project_root / "output" / "valuation_summary.xlsx"

db_file = project_root / "db" / "nifty100.db"

df = pd.read_excel(excel_file)

print(df.head())

conn = sqlite3.connect(db_file)

df.to_sql(
    "valuation_summary",
    conn,
    if_exists="replace",
    index=False
)

conn.close()

print("valuation_summary table created successfully.")