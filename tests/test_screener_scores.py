import sqlite3
import pandas as pd
from pathlib import Path

project_root = Path(__file__).resolve().parents[1]

db_path = project_root / "db" / "nifty100.db"

conn = sqlite3.connect(db_path)

tables = pd.read_sql(
    "SELECT name FROM sqlite_master WHERE type='table'",
    conn
)

print(tables)

conn.close()