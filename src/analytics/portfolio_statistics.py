from pathlib import Path

import pandas as pd

project_root = Path(__file__).resolve().parents[2]

input_path = project_root / "output"

df = pd.read_excel(
    input_path / "valuation_summary.xlsx"
)

numeric = df.select_dtypes(include="number")

stats = numeric.describe(
    percentiles=[0.10, 0.25, 0.50, 0.75, 0.90]
)

stats.to_csv(
    input_path / "portfolio_stats.csv"
)

print(stats)