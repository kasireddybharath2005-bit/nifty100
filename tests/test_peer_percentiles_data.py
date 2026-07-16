
import sqlite3
import pandas as pd
from pathlib import Path

project_root = Path(__file__).resolve().parents[1]
db_path = project_root / "db" / "nifty100.db"

conn = sqlite3.connect(db_path)

df = pd.read_sql("""
SELECT DISTINCT company_id, peer_group_name
FROM peer_percentiles
LIMIT 30
""", conn)

print(df)

conn.close
