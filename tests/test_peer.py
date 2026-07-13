
import sqlite3
from pathlib import Path

db = Path("db") / "nifty100.db"

conn = sqlite3.connect(db)

cursor = conn.cursor()

cursor.execute("PRAGMA table_info(peer_groups)")

print("Columns:\n")

for row in cursor.fetchall():
    print(row)

conn.close()