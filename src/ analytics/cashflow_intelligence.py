from pathlib import Path
import pandas as pd
import numpy as np
project_root = Path(__file__).resolve().parents[2]

input_path = project_root / "data" / "raw"
output_path = project_root / "output"

output_path.mkdir(exist_ok=True)
cashflow_df = pd.read_excel(
    input_path / "cashflow.xlsx",
    header=1
)

balancesheet_df = pd.read_excel(
    input_path / "balancesheet.xlsx",
    header=1
)


ratios_df = pd.read_excel(
    input_path / "financial_ratios.xlsx",
    header=1
)



print("=" * 60)
print("CASHFLOW")
print("=" * 60)
print(cashflow_df.head())

print("=" * 60)
print("BALANCE SHEET")
print("=" * 60)
print(balancesheet_df.head())

print("=" * 60)
print("FINANCIAL RATIOS")
print("=" * 60)
print(ratios_df.head())
print("=" * 60)
print("CASHFLOW COLUMNS")
print("=" * 60)

for col in cashflow_df.columns:
    print(col)

print("=" * 60)
print("BALANCE SHEET COLUMNS")
print("=" * 60)

for col in balancesheet_df.columns:
    print(col)

print("=" * 60)
print("RATIO COLUMNS")
print("=" * 60)

for col in ratios_df.columns:
    print(col)
preview = pd.read_excel(
    input_path / "financial_ratios.xlsx",
    header=None
)

print(preview.iloc[:8])

cashflow_df["cfo_quality_score"] = np.where(
    cashflow_df["operating_activity"] > 0,
    100,
    40
)

cashflow_df["cfo_quality_label"] = np.where(
    cashflow_df["cfo_quality_score"] >= 80,
    "Strong",
    "Weak"
)

cashflow_df["capex_intensity_pct"] = (
    abs(cashflow_df["investing_activity"])
    /
    abs(cashflow_df["operating_activity"])
) * 100

cashflow_df["capex_label"] = np.where(
    cashflow_df["capex_intensity_pct"] >= 50,
    "High Investment",
    "Normal Investment"
)

cashflow_df["distress_flag"] = np.where(
    (cashflow_df["operating_activity"] < 0) &
    (cashflow_df["financing_activity"] < 0),
    "YES",
    "NO"
)
cashflow_df = pd.merge(
    cashflow_df,
    balancesheet_df[
        ["company_id", "year", "borrowings"]
    ],
    on=["company_id", "year"],
    how="left"
)

cashflow_df["deleveraging_flag"] = np.where(
    cashflow_df["borrowings"] < 0,
    "YES",
    "NO"
)
conditions = [
    (cashflow_df["operating_activity"] > 0) &
    (cashflow_df["investing_activity"] < 0),

    (cashflow_df["operating_activity"] < 0)
]

choices = [
    "Growth Investment",
    "Financial Stress"
]

cashflow_df["capital_allocation_label"] = np.select(
    conditions,
    choices,
    default="Stable"
)

cashflow_df.to_excel(
    output_path / "cashflow_intelligence.xlsx",
    index=False
)

cashflow_df[
    cashflow_df["distress_flag"] == "YES"
].to_csv(
    output_path / "distress_alerts.csv",
    index=False
)

cashflow_df[
    ["company_id", "year", "capital_allocation_label"]
].to_csv(
    output_path / "capital_labels.csv",
    index=False
)


print("=" * 60)
print("SUMMARY")
print("=" * 60)

print("Total Records :", len(cashflow_df))
print("Distress Companies :", (cashflow_df["distress_flag"] == "YES").sum())
print("Growth Investment :", (cashflow_df["capital_allocation_label"] == "Growth Investment").sum())

cashflow_intelligence = pd.merge(
    cashflow_df,
    balancesheet_df[
        [
            "company_id",
            "year",
            "borrowings",
            "total_assets"
        ]
    ],
    on=["company_id", "year"],
    how="left"
)

cashflow_intelligence["free_cash_flow"] = (
    cashflow_intelligence["operating_activity"]
    +
    cashflow_intelligence["investing_activity"]
)

cashflow_intelligence["cfo_quality_score"] = np.where(
    cashflow_intelligence["operating_activity"] > 0,
    100,
    40
)

cashflow_intelligence["cfo_quality_label"] = np.where(
    cashflow_intelligence["cfo_quality_score"] >= 80,
    "Strong",
    "Weak"
)
cashflow_intelligence["capex_intensity_pct"] = (
    abs(cashflow_intelligence["investing_activity"])
    /
    abs(cashflow_intelligence["operating_activity"])
) * 100

cashflow_intelligence["capex_label"] = np.where(
    cashflow_intelligence["capex_intensity_pct"] >= 50,
    "High",
    "Normal"
)

cashflow_intelligence["distress_flag"] = np.where(
    (
        cashflow_intelligence["operating_activity"] < 0
    )
    &
    (
        cashflow_intelligence["net_cash_flow"] < 0
    ),
    "YES",
    "NO"
)

conditions = [

    (
        (cashflow_intelligence["operating_activity"] > 0)
        &
        (cashflow_intelligence["investing_activity"] < 0)
    ),

    (
        (cashflow_intelligence["operating_activity"] < 0)
        &
        (cashflow_intelligence["financing_activity"] > 0)
    )

]

choices = [

    "Growth Investment",

    "Financial Stress"

]

cashflow_intelligence["capital_allocation_label"] = np.select(

    conditions,

    choices,

    default="Stable"

)

cashflow_intelligence.to_excel(
    output_path / "cashflow_intelligence.xlsx",
    index=False
)

cashflow_intelligence[
    cashflow_intelligence["distress_flag"] == "YES"
].to_csv(
    output_path / "distress_alerts.csv",
    index=False
)

cashflow_intelligence[
    [
        "company_id",
        "year",
        "capital_allocation_label"
    ]
].to_csv(
    output_path / "capital_labels.csv",
    index=False
)

print("=" * 60)
print("DAY 31 SUMMARY")
print("=" * 60)

print("Total Records :", len(cashflow_intelligence))

print(
    "Distress Companies :",
    (cashflow_intelligence["distress_flag"] == "YES").sum()
)

print(
    "Growth Investment :",
    (
        cashflow_intelligence[
            "capital_allocation_label"
        ] == "Growth Investment"
    ).sum()
)