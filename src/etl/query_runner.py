import sqlite3
import pandas as pd
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]

db_path = project_root / "db" / "nifty100.db"

conn = sqlite3.connect(db_path)

query = """
SELECT company_name, roce_percentage
FROM companies
ORDER BY roce_percentage DESC
LIMIT 10
"""

df = pd.read_sql(query, conn)

print(df)

conn.close()
