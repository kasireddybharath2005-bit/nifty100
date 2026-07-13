import sqlite3
import pandas as pd
from pathlib import Path

project_root = Path(__file__).resolve().parent

db_path = project_root / "db" / "nifty100.db"
csv_path = project_root / "data" / "processed" / "peer_groups_cleaned.csv"

# Read CSV WITHOUT using first row as headers
df = pd.read_csv(
    csv_path,
    header=None,
    names=[
        "id",
        "peer_group_name",
        "company_id",
        "benchmark"
    ]
)

print(df.head())

conn = sqlite3.connect(db_path)

conn.execute("DROP TABLE IF EXISTS peer_groups")

df.to_sql(
    "peer_groups",
    conn,
    if_exists="replace",
    index=False
)

conn.commit()

print("\nUploaded Successfully!\n")

print(pd.read_sql("SELECT * FROM peer_groups LIMIT 10", conn))

conn.close()