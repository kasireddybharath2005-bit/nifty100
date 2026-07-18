from pathlib import Path
import pandas as pd

# --------------------------------------------------
# Project Paths
# --------------------------------------------------

project_root = Path(__file__).resolve().parents[2]

input_path = project_root / "data" / "raw"
output_path = project_root / "output"

output_path.mkdir(exist_ok=True)

# --------------------------------------------------
# Load Files
# --------------------------------------------------

market_df = pd.read_excel(
    input_path / "market_cap.xlsx"
)

cashflow_df = pd.read_excel(
    input_path / "cashflow.xlsx",
    header=1
)


# --------------------------------------------------
# Clean Year Columns
# --------------------------------------------------

market_df["year"] = pd.to_numeric(
    market_df["year"],
    errors="coerce"
).astype("Int64")

cashflow_df["year"] = (
    cashflow_df["year"]
    .astype(str)
    .str[-2:]
)

cashflow_df["year"] = (
    "20" + cashflow_df["year"]
)

cashflow_df["year"] = pd.to_numeric(
    cashflow_df["year"],
    errors="coerce"
).astype("Int64")


cashflow_df["free_cash_flow"] = (
    cashflow_df["operating_activity"]
    + cashflow_df["investing_activity"]
)




valuation_df = pd.merge(

    market_df,

    cashflow_df[
        [
            "company_id",
            "year",
            "free_cash_flow"
        ]
    ],

    on=["company_id","year"],

    how="left"

)

# --------------------------------------------------
# Check Merge Result
# --------------------------------------------------

print("=" * 60)
print("MERGE SUMMARY")
print("=" * 60)

print("Total rows :", len(valuation_df))
print("Matched FCF :", valuation_df["free_cash_flow"].notna().sum())
print("Missing FCF :", valuation_df["free_cash_flow"].isna().sum())

print("\nSample Merged Data")
print(
    valuation_df[
        [
            "company_id",
            "year",
            "market_cap_crore",
            "free_cash_flow"
        ]
    ].head(10)
)
# --------------------------------------------------
# Calculate FCF Yield
# --------------------------------------------------

valuation_df["fcf_yield_pct"] = (
    valuation_df["free_cash_flow"]
    / valuation_df["market_cap_crore"]
) * 100

print("=" * 60)
print("FCF YIELD")
print("=" * 60)

print(
    valuation_df[
        [
            "company_id",
            "year",
            "market_cap_crore",
            "free_cash_flow",
            "fcf_yield_pct"
        ]
    ].head(10)
)

# --------------------------------------------------
# Load Sector Data
# --------------------------------------------------

sector_df = pd.read_excel(
    input_path / "sectors.xlsx"
)

print("=" * 60)
print("SECTOR DATA")
print("=" * 60)

print(sector_df.head())

print("=" * 60)
print("SECTOR COLUMNS")
print("=" * 60)

for col in sector_df.columns:
    print(col)

# --------------------------------------------------
# Merge Sector Information
# --------------------------------------------------

valuation_df = pd.merge(
    valuation_df,
    sector_df[
        [
            "company_id",
            "broad_sector"
        ]
    ],
    on="company_id",
    how="left"
)

print("=" * 60)
print("VALUATION WITH SECTOR")
print("=" * 60)

print(
    valuation_df[
        [
            "company_id",
            "broad_sector",
            "market_cap_crore",
            "pe_ratio",
            "fcf_yield_pct"
        ]
    ].head()
)

# --------------------------------------------------
# Sector Median PE
# --------------------------------------------------

sector_pe = (
    valuation_df
    .groupby("broad_sector")["pe_ratio"]
    .median()
    .reset_index()
)

sector_pe.rename(
    columns={
        "pe_ratio": "sector_median_pe"
    },
    inplace=True
)

print("=" * 60)
print("SECTOR MEDIAN PE")
print("=" * 60)

print(sector_pe.head())

# --------------------------------------------------
# Merge Sector Median PE
# --------------------------------------------------

valuation_df = pd.merge(
    valuation_df,
    sector_pe,
    on="broad_sector",
    how="left"
)

print("=" * 60)
print("VALUATION WITH SECTOR PE")
print("=" * 60)

print(
    valuation_df[
        [
            "company_id",
            "broad_sector",
            "pe_ratio",
            "sector_median_pe"
        ]
    ].head()
)
# --------------------------------------------------
# PE Premium / Discount %
# --------------------------------------------------

valuation_df["pe_difference_pct"] = (
    (
        valuation_df["pe_ratio"]
        - valuation_df["sector_median_pe"]
    )
    /
    valuation_df["sector_median_pe"]
) * 100

print("=" * 60)
print("PE DIFFERENCE")
print("=" * 60)

print(
    valuation_df[
        [
            "company_id",
            "broad_sector",
            "pe_ratio",
            "sector_median_pe",
            "pe_difference_pct"
        ]
    ].head()
)
# --------------------------------------------------
# Valuation Flag
# --------------------------------------------------

def valuation_flag(row):

    if pd.isna(row["pe_difference_pct"]):
        return "Unknown"

    elif row["pe_difference_pct"] <= -20:
        return "Discount"

    elif row["pe_difference_pct"] >= 20:
        return "Caution"

    else:
        return "Fair"


valuation_df["valuation_flag"] = valuation_df.apply(
    valuation_flag,
    axis=1
)

print("=" * 60)
print("VALUATION FLAGS")
print("=" * 60)

print(
    valuation_df[
        [
            "company_id",
            "pe_ratio",
            "sector_median_pe",
            "pe_difference_pct",
            "valuation_flag"
        ]
    ].head(10)
)
# --------------------------------------------------
# Export Valuation Summary
# --------------------------------------------------

valuation_df.to_excel(
    output_path / "valuation_summary.xlsx",
    index=False
)

print("valuation_summary.xlsx created successfully.")

# --------------------------------------------------
# Export Valuation Flags
# --------------------------------------------------

flagged_df = valuation_df[
    valuation_df["valuation_flag"] != "Unknown"
]

flagged_df.to_csv(
    output_path / "valuation_flags.csv",
    index=False
)

print("valuation_flags.csv created successfully.")

# --------------------------------------------------
# Summary
# --------------------------------------------------

print("=" * 60)
print("VALUATION ANALYSIS COMPLETED")
print("=" * 60)

print(f"Total Companies : {len(valuation_df)}")
print(f"Discount Stocks : {(valuation_df['valuation_flag'] == 'Discount').sum()}")
print(f"Fair Stocks     : {(valuation_df['valuation_flag'] == 'Fair').sum()}")
print(f"Caution Stocks  : {(valuation_df['valuation_flag'] == 'Caution').sum()}")

print("\nOutput Files:")
print(output_path / "valuation_summary.xlsx")
print(output_path / "valuation_flags.csv")



print("="*60)

print(
    cashflow_df[
        [
            "company_id",
            "year",
            "operating_activity",
            "investing_activity",
            "free_cash_flow"
        ]
    ].head()
)
print("="*60)
print("MERGED DATA")
print("="*60)

print(valuation_df.head())
valuation_df["fcf_yield_pct"]=(

    valuation_df["free_cash_flow"]

    /

    valuation_df["market_cap_crore"]

)*100

print("="*60)
print("FCF YIELD")
print("="*60)

print(

valuation_df[

[
"company_id",

"market_cap_crore",

"free_cash_flow",

"fcf_yield_pct"

]

].head()

)
for col in cashflow_df.columns:
    print(col)

