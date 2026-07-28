import pandas as pd
import sqlite3
from pathlib import Path

# ==========================================
# PATHS
# ==========================================

project_root = Path(__file__).resolve().parents[2]

db_path = project_root / "db" / "nifty100.db"

output_path = project_root / "output"
output_path.mkdir(exist_ok=True)

# ==========================================
# LOAD DATABASE
# ==========================================

conn = sqlite3.connect(db_path)

df = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

conn.close()

print("Rows Loaded :", len(df))

# ==========================================
# CHECK REQUIRED COLUMNS
# ==========================================

required = ["company_id", "roe_calculated"]

for col in required:
    if col not in df.columns:
        raise Exception(f"{col} not found")

# ==========================================
# LOAD SOURCE ROE
# ==========================================

companies = pd.read_csv(
    project_root / "data" / "processed" / "companies_cleaned.csv"
)

print("Companies Loaded :", len(companies))

companies = companies[
    [
        "id",
        "company_name",
        "roce_percentage"
    ]
]

companies.rename(
    columns={
        "id": "company_id",
        "roce_percentage": "source_roce"
    },
    inplace=True
)
merged = pd.merge(
    df,
    companies,
    on="company_id",
    how="left"
)

print("Merged :", merged.shape)
merged["difference"] = (
    merged["roe_calculated"] -
    merged["source_roce"]
).abs()

def category(diff):

    if pd.isna(diff):
        return "Missing"

    if diff <= 5:
        return "OK"

    elif diff <= 10:
        return "Version Difference"

    elif diff <= 20:
        return "Formula Difference"

    else:
        return "Data Source Issue"


merged["category"] = merged[
    "difference"
].apply(category)
issues = merged[
    merged["difference"] > 5
]

print()

print("Issues Found :", len(issues))
issues[
    [
        "company_id",
        "company_name",
        "roe_calculated",
        "source_roce",
        "difference",
        "category"
    ]
].to_csv(

    output_path /
    "ratio_edge_cases.csv",

    index=False

)
log_file = output_path / "ratio_edge_cases.log"

with open(log_file, "w") as f:

    f.write("DAY 13 EDGE CASE REPORT\n")

    f.write("=" * 50 + "\n\n")

    f.write(f"Total Companies : {len(df)}\n")

    f.write(f"Issues Found : {len(issues)}\n\n")

    for _, row in issues.iterrows():

        f.write(
            f"{row['company_name']} | "
            f"ROE={row['roe_calculated']:.2f} | "
            f"Source={row['source_roce']:.2f} | "
            f"Diff={row['difference']:.2f} | "
            f"{row['category']}\n"
        )

print("Edge Case Log Generated")

print()

print("================================")

print("DAY 13 SUMMARY")

print("================================")

print("Rows Checked :", len(df))

print("Issues :", len(issues))

print()

print(
    issues["category"]
    .value_counts()
)

print()

print("CSV Saved")

print("LOG Saved")