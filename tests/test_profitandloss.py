import sqlite3
import pandas as pd
from pathlib import Path

project_root = Path(__file__).resolve().parents[1]

db = project_root / "db" / "nifty100.db"

conn = sqlite3.connect(db)

print(pd.read_sql("PRAGMA table_info(profitandloss)", conn))

conn.close()