from pathlib import Path
import sqlite3

project_root = Path(__file__).resolve().parents[2]

db_folder = project_root / "db"
db_folder.mkdir(exist_ok=True)

db_path = db_folder / "nifty100.db"
print(db_path)
conn = sqlite3.connect(db_path)
import pandas as pd

processed_path = project_root / "data" / "processed"

for file in processed_path.glob("*_cleaned.csv"):
    table_name = file.stem.replace("_cleaned", "")

    df = pd.read_csv(file)

    df.to_sql(
        table_name,
        conn,
        if_exists="replace",
        index=False
    )

    print(f"Loaded {table_name} : {len(df)} rows")

conn.close()

print("Database Created Successfully")
