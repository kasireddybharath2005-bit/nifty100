import pandas as pd
from pathlib import Path

raw_path = Path(r"C:\Users\kasir\PycharmProjects\PythonProject4\data\raw")

for file in raw_path.glob("*.xlsx"):
    df = pd.read_excel(file, engine="openpyxl")

    print("=" * 50)
    print("File:", file.name)
    print("Shape:", df.shape)
    print(df.head())