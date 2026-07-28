from pathlib import Path
import pandas as pd
project_root = Path(__file__).resolve().parents[2]

output_path = project_root / "output"
ranking_df = pd.read_excel(
    output_path / "company_rankings.xlsx"
)

portfolio_df = pd.read_excel(
    output_path / "recommended_portfolio.xlsx"
)

summary_df = pd.read_excel(
    output_path / "portfolio_summary.xlsx"
)
with pd.ExcelWriter(

    output_path /

    "Final_Analytics_Report.xlsx"

) as writer:

    ranking_df.to_excel(
        writer,
        sheet_name="Rankings",
        index=False
    )

    portfolio_df.to_excel(
        writer,
        sheet_name="Portfolio",
        index=False
    )

    summary_df.to_excel(
        writer,
        sheet_name="Summary",
        index=False
    )

print("Final_Analytics_Report.xlsx created successfully.")