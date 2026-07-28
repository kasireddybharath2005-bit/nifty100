from pathlib import Path
import pandas as pd
project_root = Path(__file__).resolve().parents[2]

input_path = project_root / "output"
output_path = project_root / "output"

output_path.mkdir(exist_ok=True)
ranking_df = pd.read_excel(
    input_path / "company_rankings.xlsx"
)

print("=" * 60)
print("COMPANY RANKINGS")
print("=" * 60)

print(ranking_df.head())
portfolio_df = ranking_df.head(10).copy()
portfolio_df["Weight (%)"] = round(
    100 / len(portfolio_df),
    2
)
investment = 1000000

portfolio_df["Investment (₹)"] = (
    portfolio_df["Weight (%)"] / 100
) * investment

print("=" * 60)
print("RECOMMENDED PORTFOLIO")
print("=" * 60)

print(
    portfolio_df[
        [
            "Final Rank",
            "company_id",
            "Weight (%)",
            "Investment (₹)"
        ]
    ]
)

portfolio_df.to_excel(
    output_path / "recommended_portfolio.xlsx",
    index=False
)

print("recommended_portfolio.xlsx created successfully.")