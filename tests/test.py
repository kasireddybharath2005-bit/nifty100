import sqlite3
import pandas as pd
from pathlib import Path

# Project root
project_root = Path(__file__).resolve().parents[1]

# Database path
db_path = project_root / "db" / "nifty100.db"

print("Database Path:", db_path)
print("Exists:", db_path.exists())

# Connect to database
conn = sqlite3.connect(db_path)

# Read first 5 rows
df = pd.read_sql(
    "SELECT * FROM financial_ratios LIMIT 5",
    conn
)

# Print all column names
print("\nColumns:")
print(df.columns.tolist())
for col in df.columns:
    print(col)