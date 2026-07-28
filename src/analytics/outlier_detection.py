from pathlib import Path

import pandas as pd

project_root = Path(__file__).resolve().parents[2]

input_path = project_root / "output"

df = pd.read_excel(
    input_path / "valuation_summary.xlsx"
)

numeric = df.select_dtypes(include="number")

z = ((numeric - numeric.mean()) / numeric.std()).abs()

outliers = df[(z > 3).any(axis=1)]

outliers.to_csv(
    input_path / "outlier_report.csv",
    index=False
)

print(outliers.head())