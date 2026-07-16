import sqlite3
import pandas as pd
from pathlib import Path

project_root = Path(__file__).resolve().parents[1]
db = project_root / "db" / "nifty100.db"

conn = sqlite3.connect(db)

company = "INFY"

query = """
SELECT *
FROM peer_percentiles
WHERE company_id = ?
"""

df = pd.read_sql(query, conn, params=[company])

print(df)

conn.close()