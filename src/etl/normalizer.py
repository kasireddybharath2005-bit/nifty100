import pandas as pd
from pathlib import Path

raw_path = Path(r"C:\Users\kasir\PycharmProjects\PythonProject4\data\raw")
processed_path = Path(r"C:\Users\kasir\PycharmProjects\PythonProject4\data\processed")

processed_path.mkdir(exist_ok=True)

for file in raw_path.glob("*.xlsx"):

    df = pd.read_excel(file, engine="openpyxl")

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Remove completely empty rows
    df = df.dropna(how="all")

    # Standardize column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    output_file = processed_path / f"{file.stem}_cleaned.csv"

    df.to_csv(output_file, index=False)

    print(f"Saved: {output_file.name}")