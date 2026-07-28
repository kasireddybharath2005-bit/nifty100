from pathlib import Path
import pandas as pd

project_root = Path(__file__).resolve().parents[2]

input_path = project_root / "output"
output_path = project_root / "output"

screened_df = pd.read_excel(
    input_path / "screened_companies.xlsx"
)

print("="*60)
print("SCREENED DATA")
print("="*60)

print(screened_df.head())
screened_df["ROE Rank"] = screened_df[
    "return_on_equity_pct"
].rank(ascending=False)

screened_df["Margin Rank"] = screened_df[
    "net_profit_margin_pct"
].rank(ascending=False)

screened_df["Debt Rank"] = screened_df[
    "debt_to_equity"
].rank(ascending=True)

screened_df["Total Score"] = (

    screened_df["ROE Rank"]

    +

    screened_df["Margin Rank"]

    +

    screened_df["Debt Rank"]

)
ranking_df = screened_df.sort_values(
    "Total Score"
)
ranking_df["Final Rank"] = range(
    1,
    len(ranking_df)+1
)
print("="*60)
print("TOP COMPANIES")
print("="*60)

print(

ranking_df[
[
"Final Rank",
"company_id",
"return_on_equity_pct",
"net_profit_margin_pct",
"debt_to_equity",
"Total Score"
]
].head(20)

)
ranking_df.to_excel(

    output_path /

    "company_rankings.xlsx",

    index=False

)

print("company_rankings.xlsx created.")