import sqlite3

conn = sqlite3.connect("db/nifty100.db")

cursor = conn.execute("""
SELECT DISTINCT broad_sector
FROM valuation_summary
ORDER BY broad_sector
""")

for row in cursor.fetchall():
    print(row[0])

conn.close()