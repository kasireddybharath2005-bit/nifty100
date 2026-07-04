import pandas as pd
from pathlib import Path

# -------------------------------
# Project Paths
# -------------------------------

project_root = Path(__file__).resolve().parents[2]

processed_path = project_root / "data" / "processed"
output_path = project_root / "output"

output_path.mkdir(exist_ok=True)

# -------------------------------
# Load datasets
# -------------------------------

companies = pd.read_csv(processed_path / "companies_cleaned.csv")
profitloss = pd.read_csv(processed_path / "profitandloss_cleaned.csv")
balancesheet = pd.read_csv(processed_path / "balancesheet_cleaned.csv")

print("Datasets Loaded Successfully")

# -------------------------------
# Merge
# -------------------------------

merged = pd.merge(
    profitloss,
    balancesheet,
    on=["company_id", "year"],
    how="inner"
)

print("Merged Rows :", merged.shape[0])

# -------------------------------
# Debt to Equity
# -------------------------------

merged["debt_to_equity"] = (
    merged["borrowings"] /
    (merged["equity_capital"] + merged["reserves"])
)

# -------------------------------
# Interest Coverage Ratio
# -------------------------------

merged["interest_coverage"] = (
    merged["operating_profit"] /
    merged["interest"]
)

# Replace divide-by-zero results

merged.loc[
    merged["interest"] == 0,
    "interest_coverage"
] = None

# -------------------------------
# Asset Turnover
# -------------------------------

merged["asset_turnover"] = (
    merged["sales"] /
    merged["total_assets"]
)

# -------------------------------
# Net Debt
# -------------------------------

merged["net_debt"] = merged["borrowings"]

# -------------------------------
# High Leverage Flag
# -------------------------------

merged["high_leverage_flag"] = merged["debt_to_equity"].apply(
    lambda x: True if x > 5 else False
)

# -------------------------------
# Debt Free Label
# -------------------------------

merged["icr_label"] = merged["borrowings"].apply(
    lambda x: "Debt Free" if x == 0 else "Has Debt"
)

# -------------------------------
# Save CSV
# -------------------------------

merged.to_csv(
    output_path / "day9_leverage_ratios.csv",
    index=False
)

print("\nDay 9 Completed Successfully")

print(
    merged[
        [
            "company_id",
            "year",
            "debt_to_equity",
            "interest_coverage",
            "asset_turnover",
            "net_debt",
            "high_leverage_flag",
            "icr_label"
        ]
    ].head()
)