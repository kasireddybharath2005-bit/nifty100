import sqlite3
import pandas as pd
from pathlib import Path

project_root = Path(__file__).resolve().parent

db_path = project_root / "db" / "nifty100.db"
csv_path = project_root / "data" / "processed" / "sectors_cleaned.csv"

# Read CSV without using the first row as headers
df = pd.read_csv(
    csv_path,
    header=None,
    names=[
        "id",
        "company_id",
        "sector_name",
        "industry",
        "weight",
        "market_cap"
    ]
)

print(df.head())

conn = sqlite3.connect(db_path)

conn.execute("DROP TABLE IF EXISTS sectors")

df.to_sql(
    "sectors",
    conn,
    if_exists="replace",
    index=False
)

conn.commit()

print("\nSectors table uploaded successfully!\n")

print(pd.read_sql("SELECT * FROM sectors LIMIT 10", conn))

conn.close()