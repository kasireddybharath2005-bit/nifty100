import pandas as pd

from pathlib import Path

project_root = Path(__file__).resolve().parents[2]
processed_path = project_root / "data" / "processed"


companies = pd.read_csv(processed_path/"companies_cleaned.csv")

print(companies.columns.tolist())
print(companies.shape)
print(processed_path)
print((processed_path / "companies_cleaned.csv").exists())

import pandas as pd
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]
processed_path = project_root / "data" / "processed"

companies = pd.read_csv(processed_path / "companies_cleaned.csv")
analysis = pd.read_csv(processed_path / "analysis_cleaned.csv")
balancesheet = pd.read_csv(processed_path / "balancesheet_cleaned.csv")
cashflow = pd.read_csv(processed_path / "cashflow_cleaned.csv")
duplicate_ids = companies["id"].duplicated().sum()


print("DQ-01 Duplicate IDs:", duplicate_ids)
missing_names = companies["company_name"].isnull().sum()

print("DQ-02 Missing Company Names:", missing_names)
invalid_face = (companies["face_value"] <= 0).sum()

print("DQ-03 Invalid Face Value:", invalid_face)
invalid_book = (companies["book_value"] <= 0).sum()

print("DQ-04 Invalid Book Value:", invalid_book)
results = {
    "Rule": [
        "DQ-01 Duplicate IDs",
        "DQ-02 Missing Company Names",
        "DQ-03 Invalid Face Value",
        "DQ-04 Invalid Book Value"
    ],
    "Failures": [
        duplicate_ids,
        missing_names,
        invalid_face,
        invalid_book
    ]
}

report = pd.DataFrame(results)

output_path = project_root / "output"
output_path.mkdir(exist_ok=True)

report.to_csv(
    output_path / "validation_failures.csv",
    index=False
)
missing_company_ids = (
    ~analysis["company_id"].isin(companies["id"])
).sum()

print("DQ-05 Missing Company References:", missing_company_ids)


missing_bs_ids = (
    ~balancesheet["company_id"].isin(companies["id"])
).sum()

print("DQ-06 Missing BalanceSheet References:", missing_bs_ids)
missing_cf_ids = (
    ~cashflow["company_id"].isin(companies["id"])
).sum()

print("DQ-07 Missing Cashflow References:", missing_cf_ids)
missing_years = balancesheet["year"].isnull().sum()

print("DQ-08 Missing Years:", missing_years)
invalid_equity = (
    balancesheet["equity_capital"] < 0
).sum()

print("DQ-09 Negative Equity Capital:", invalid_equity)
invalid_borrowings = (
    balancesheet["borrowings"] < 0
).sum()

print("DQ-10 Negative Borrowings:", invalid_borrowings)
missing_operating = (
    cashflow["operating_activity"]
    .isnull()
    .sum()
)

print("DQ-11 Missing Operating Activity:", missing_operating)
missing_net_cf = (
    cashflow["net_cash_flow"]
    .isnull()
    .sum()
)

print("DQ-12 Missing Net Cash Flow:", missing_net_cf)
missing_roe = analysis["roe"].isnull().sum()

print("DQ-13 Missing ROE:", missing_roe)
missing_sales_growth = (
    analysis["compounded_sales_growth"]
    .isnull()
    .sum()
)

print(
    "DQ-14 Missing Sales Growth:",
    missing_sales_growth
)
duplicate_names = (
    companies["company_name"]
    .duplicated()
    .sum()
)

print(
    "DQ-15 Duplicate Company Names:",
    duplicate_names
)
duplicate_company_year = (
    balancesheet
    .duplicated(
        subset=["company_id", "year"]
    )
    .sum()
)

print(
    "DQ-16 Duplicate Company-Year:",
    duplicate_company_year
)
from pathlib import Path
import pandas as pd

project_root = Path(__file__).resolve().parents[2]

output_path = project_root / "output"
output_path.mkdir(exist_ok=True)

report.to_csv(
    output_path / "validation_failures.csv",
    index=False
)

print("Validation report saved successfully")
results = {
    "Rule": [
        "DQ-01 Duplicate IDs",
        "DQ-02 Missing Company Names",
        "DQ-03 Invalid Face Value",
        "DQ-04 Invalid Book Value",
        "DQ-05 Missing Company References",
        "DQ-06 Missing BalanceSheet References",
        "DQ-07 Missing Cashflow References",
        "DQ-08 Missing Years",
        "DQ-09 Negative Equity Capital",
        "DQ-10 Negative Borrowings",
        "DQ-11 Missing Operating Activity",
        "DQ-12 Missing Net Cash Flow",
        "DQ-13 Missing ROE",
        "DQ-14 Missing Sales Growth",
        "DQ-15 Duplicate Company Names",
        "DQ-16 Duplicate Company-Year"
    ],

    "Failures": [
        duplicate_ids,
        missing_names,
        invalid_face,
        invalid_book,
        missing_company_ids,
        missing_bs_ids,
        missing_cf_ids,
        missing_years,
        invalid_equity,
        invalid_borrowings,
        missing_operating,
        missing_net_cf,
        missing_roe,
        missing_sales_growth,
        duplicate_names,
        duplicate_company_year
    ]
}

report = pd.DataFrame(results)
output_path = project_root / "output"

report.to_csv(
    output_path / "validation_failures.csv",
    index=False
)

print(report)