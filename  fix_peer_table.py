import sqlite3
from pathlib import Path

db = Path("db") / "nifty100.db"

conn = sqlite3.connect(db)

cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS peer_groups")

cursor.execute("""
CREATE TABLE peer_groups (
    id INTEGER PRIMARY KEY,
    peer_group_name TEXT,
    company_id TEXT,
    benchmark INTEGER
)
""")

conn.commit()

print("peer_groups table recreated successfully!")

conn.close()