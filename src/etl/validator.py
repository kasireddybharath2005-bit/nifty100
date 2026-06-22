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

print(report)