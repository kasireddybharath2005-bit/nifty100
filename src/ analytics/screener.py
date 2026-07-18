from pathlib import Path
import pandas as pd
project_root = Path(__file__).resolve().parents[2]

input_path = project_root / "data" / "raw"
output_path = project_root / "output"

output_path.mkdir(exist_ok=True)
ratios_df = pd.read_excel(
    input_path / "financial_ratios.xlsx"
)

print("=" * 60)
print("FINANCIAL RATIOS")
print("=" * 60)

print(ratios_df.head())

print("\nColumns:")
print(ratios_df.columns.tolist())
ratios_df = (
    ratios_df
    .sort_values("year")
    .groupby("company_id")
    .tail(1)
    .reset_index(drop=True)
)
screened_df = ratios_df[
    (ratios_df["return_on_equity_pct"] >= 15) &
    (ratios_df["debt_to_equity"] <= 1) &
    (ratios_df["net_profit_margin_pct"] >= 10)
]
print("=" * 60)
print("SCREENED COMPANIES")
print("=" * 60)

print(screened_df.head())

print("\nTotal Companies:", len(screened_df))

screened_df.to_excel(
    output_path / "screened_companies.xlsx",
    index=False
)

print("screened_companies.xlsx created successfully.")