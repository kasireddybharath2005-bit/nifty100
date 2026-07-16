import sqlite3
import pandas as pd
from pathlib import Path

project_root = Path(__file__).resolve().parents[1]

db_path = project_root / "db" / "nifty100.db"

conn = sqlite3.connect(db_path)

print(pd.read_sql("PRAGMA table_info(peer_percentiles)", conn))

conn.close()