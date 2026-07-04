import pandas as pd
from pathlib import Path

# Project root
project_root = Path(__file__).resolve().parents[2]

# Processed data folder
processed_path = project_root / "data" / "processed"

# Load datasets
companies = pd.read_csv(processed_path / "companies_cleaned.csv")
profitloss = pd.read_csv(processed_path / "profitandloss_cleaned.csv")
balancesheet = pd.read_csv(processed_path / "balancesheet_cleaned.csv")
cashflow = pd.read_csv(processed_path / "cashflow_cleaned.csv")

# Print basic information
print("=" * 50)
print("Companies")
print(companies.head())
print("Shape:", companies.shape)

# Merge Profit & Loss with Balance Sheet
merged_df = pd.merge(
    profitloss,
    balancesheet,
    on=["company_id", "year"],
    how="inner"
)

print("\nMerged Dataset")
print(merged_df.head())
print("Shape:", merged_df.shape)

# Net Profit Margin
merged_df["net_profit_margin"] = (
    merged_df["net_profit"] /
    merged_df["sales"]
) * 100

print("\nNet Profit Margin")
print(
    merged_df[
        ["company_id", "year", "net_profit_margin"]
    ].head()
)

print("=" * 50)
print("Profit & Loss")
print(profitloss.head())
print("Shape:", profitloss.shape)

print("=" * 50)
print("Balance Sheet")
print(balancesheet.head())
print("Shape:", balancesheet.shape)

print("=" * 50)
print("Cash Flow")
print(cashflow.head())
print("Shape:", cashflow.shape)

print("\n✅ All datasets loaded successfully!")

merged_df["operating_profit_margin"] = (
    merged_df["operating_profit"] /
    merged_df["sales"]
) * 100

print(
    merged_df[
        ["company_id", "operating_profit_margin"]
    ].head()
)

merged_df["roe_calculated"] = (
    merged_df["net_profit"] /
    (
        merged_df["equity_capital"] +
        merged_df["reserves"]
    )
) * 100

merged_df["roa"] = (
    merged_df["net_profit"] /
    merged_df["total_assets"]
) * 100
output_path = project_root / "output"

merged_df.to_csv(
    output_path / "day8_profitability_ratios.csv",
    index=False
)

print("\nDay 8 completed successfully!")