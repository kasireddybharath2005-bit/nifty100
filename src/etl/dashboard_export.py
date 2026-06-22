import sqlite3
import pandas as pd
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]

db_path = project_root / "db" / "nifty100.db"

conn = sqlite3.connect(db_path)

query = """
SELECT
    c.company_name,
    c.roce_percentage,
    a.roe
FROM companies c
LEFT JOIN analysis a
ON c.id = a.company_id
"""

df = pd.read_sql(query, conn)

output_path = project_root / "output"

df.to_csv(
    output_path / "dashboard_data.csv",
    index=False
)

print(df.head())
print(df.shape)

conn.close()

print("Dashboard dataset exported successfully")