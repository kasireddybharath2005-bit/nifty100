import sqlite3
import pandas as pd
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]

db_path = project_root / "db" / "nifty100.db"

conn = sqlite3.connect(db_path)

tables = pd.read_sql(
    "SELECT name FROM sqlite_master WHERE type='table'",
    conn
)

audit = []

for table in tables["name"]:
    count = pd.read_sql(
        f"SELECT COUNT(*) as rows FROM {table}",
        conn
    ).iloc[0, 0]

    audit.append([table, count])

audit_df = pd.DataFrame(
    audit,
    columns=["table_name", "row_count"]
)

output_path = project_root / "output"

audit_df.to_csv(
    output_path / "load_audit.csv",
    index=False
)

print(audit_df)

conn.close()