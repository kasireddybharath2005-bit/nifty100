import sqlite3
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]
db_path = project_root / "db" / "nifty100.db"

conn = sqlite3.connect(db_path)

cursor = conn.cursor()

cursor.execute(
    "SELECT name FROM sqlite_master WHERE type='table';"
)

print(cursor.fetchall())

conn.close()