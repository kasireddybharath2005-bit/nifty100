import pandas as pd
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]

output = project_root / "output"

df = pd.read_csv(output / "screener_output.csv")

print(df.head())

print()

print("Rows :", len(df))

assert len(df) > 0

print("Test Passed")