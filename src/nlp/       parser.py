from pathlib import Path
import pandas as pd
import re


def extract_metric(text):

    if pd.isna(text):
        return None, None

    text = str(text)

    pattern = r'(\d+)\s*Year[s]?:\s*(-?\d+(?:\.\d+)?)%'

    match = re.search(pattern, text)

    if match:

        years = int(match.group(1))
        value = float(match.group(2))

        return years, value

    return None, None

project_root = Path(__file__).resolve().parents[2]

input_path = project_root / "data" / "raw"

output_path = project_root / "output"




preview_df = pd.read_excel(
    input_path / "analysis.xlsx",
    header=None
)


analysis_df = pd.read_excel(
    input_path / "analysis.xlsx",
    header=1
)

print("=" * 60)
print("ANALYSIS DATA")
print("=" * 60)

print(analysis_df.head())

print("=" * 60)
print("COLUMNS")
print("=" * 60)

print(analysis_df.columns.tolist())

parsed_rows = []

target_columns = [
    "compounded_sales_growth",
    "compounded_profit_growth",
    "stock_price_cagr",
    "roe"
]

for _, row in analysis_df.iterrows():

    for metric in target_columns:

        years, value = extract_metric(row[metric])

        parsed_rows.append({

            "company_id": row["company_id"],
            "metric_type": metric,
            "period_years": years,
            "value_pct": value

        })
        parsed_df = pd.DataFrame(parsed_rows)

        print("=" * 60)
        print("PARSED DATA")
        print("=" * 60)

        print(parsed_df.head(20))

        parsed_df.to_csv(
            output_path / "analysis_parsed.csv",
            index=False
        )

        print("analysis_parsed.csv created successfully.")

        failures_df = parsed_df[
            parsed_df["period_years"].isna()
        ]

        failures_df.to_csv(
            output_path / "parse_failures.csv",
            index=False
        )

        print("parse_failures.csv created successfully.")

        print("=" * 60)
        print("SUMMARY")
        print("=" * 60)

        print(f"Total Parsed Records : {len(parsed_df)}")
        print(f"Successful Parses    : {parsed_df['period_years'].notna().sum()}")
        print(f"Failed Parses        : {parsed_df['period_years'].isna().sum()}")