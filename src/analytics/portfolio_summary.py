from pathlib import Path
import pandas as pd
project_root = Path(__file__).resolve().parents[2]

input_path = project_root / "output"
output_path = project_root / "output"

portfolio_df = pd.read_excel(
    input_path / "recommended_portfolio.xlsx"
)
total_investment = portfolio_df["Investment (₹)"].sum()

average_weight = portfolio_df["Weight (%)"].mean()

number_of_companies = len(portfolio_df)
print("="*60)
print("PORTFOLIO SUMMARY")
print("="*60)

print(f"Companies          : {number_of_companies}")
print(f"Investment         : ₹{total_investment:,.2f}")
print(f"Average Weight     : {average_weight:.2f}%")

summary_df = pd.DataFrame({

    "Metric":[
        "Companies",
        "Investment",
        "Average Weight (%)"
    ],

    "Value":[
        number_of_companies,
        total_investment,
        average_weight
    ]

})

summary_df.to_excel(

    output_path /

    "portfolio_summary.xlsx",

    index=False

)

print("portfolio_summary.xlsx created.")