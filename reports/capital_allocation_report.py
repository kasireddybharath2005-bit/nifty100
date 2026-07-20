from pathlib import Path
import pandas as pd

project_root = Path(__file__).resolve().parent.parent

input_path = project_root / "output"
output_path = project_root / "output"
output_path.mkdir(exist_ok=True)
cashflow_df = pd.read_excel(
    input_path / "cashflow_intelligence.xlsx"
)

print(cashflow_df.head())
distribution = (
    cashflow_df
    .groupby("capital_allocation_label")
    .size()
    .reset_index(name="company_count")
)

print(distribution)
distribution.to_csv(
    output_path / "capital_distribution_summary.csv",
    index=False
)
capital_report = cashflow_df[
    [
        "company_id",
        "year",
        "capital_allocation_label",
        "cfo_quality_score",
        "capex_intensity_pct",
        "distress_flag"
    ]
]

capital_report.to_csv(
    output_path / "capital_allocation.csv",
    index=False
)
cashflow_df = cashflow_df.sort_values(
    ["company_id", "year"]
)

cashflow_df["previous_label"] = (
    cashflow_df
    .groupby("company_id")["capital_allocation_label"]
    .shift(1)
)

pattern_changes = cashflow_df[
    cashflow_df["previous_label"].notna() &
    (
        cashflow_df["previous_label"] !=
        cashflow_df["capital_allocation_label"]
    )
]
pattern_changes.to_csv(
    output_path / "pattern_changes.csv",
    index=False
)
print("=" * 60)
print("DAY 32 SUMMARY")
print("=" * 60)

print("Capital Allocation Records :", len(capital_report))
print("Pattern Changes :", len(pattern_changes))
print("Distribution Categories :", len(distribution))


print(project_root)
print(input_path)