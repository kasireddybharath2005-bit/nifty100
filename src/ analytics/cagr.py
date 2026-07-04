import pandas as pd
import numpy as np
from pathlib import Path

# ==========================================================
# PROJECT PATHS
# ==========================================================

project_root = Path(__file__).resolve().parents[2]

processed_path = project_root / "data" / "processed"
output_path = project_root / "output"

output_path.mkdir(exist_ok=True)

# ==========================================================
# LOAD DATA
# ==========================================================

pl = pd.read_csv(processed_path / "profitandloss_cleaned.csv")

print("Profit & Loss Dataset Loaded Successfully")
print("Rows :", len(pl))

# ==========================================================
# CLEAN YEAR COLUMN
# ==========================================================

# Converts "Mar 2016" -> 2016
# Extract 4-digit year
pl["year"] = pl["year"].astype(str).str.extract(r'(\d{4})')[0]

# Remove rows where year is missing
pl = pl.dropna(subset=["year"])

# Convert to integer
pl["year"] = pl["year"].astype(int)

pl = pl.sort_values(
    ["company_id", "year"]

)

print("Years Converted Successfully")

# ==========================================================
# CAGR FUNCTION
# ==========================================================

def calculate_cagr(start_value, end_value, years):
    """
    Returns CAGR %
    """

    if pd.isna(start_value):
        return None

    if pd.isna(end_value):
        return None

    if years <= 0:
        return None

    if start_value <= 0:
        return None

    if end_value <= 0:
        return None

    return round(
        (
            ((end_value / start_value) ** (1 / years))
            - 1
        ) * 100,
        2
    )

# ==========================================================
# EDGE CASE FUNCTION
# ==========================================================

def detect_case(start_value, end_value):

    if pd.isna(start_value) or pd.isna(end_value):
        return "INSUFFICIENT_DATA"

    if start_value == 0:
        return "ZERO_BASE"

    if start_value < 0 and end_value > 0:
        return "TURNAROUND"

    if start_value > 0 and end_value < 0:
        return "DECLINE_TO_LOSS"

    if start_value < 0 and end_value < 0:
        return "BOTH_NEGATIVE"

    return "NORMAL"

# ==========================================================
# RESULT STORAGE
# ==========================================================

results = []

companies = sorted(pl["company_id"].unique())

print("Companies Found :", len(companies))

print("Missing Years:", pl["year"].isna().sum())

# ==============================================
# Calculate 3, 5 and 10 Year CAGR
# ==============================================

periods = [3, 5, 10]

for company in companies:

    company_df = pl[
        pl["company_id"] == company
    ].sort_values("year")

    company_df = company_df.reset_index(drop=True)

    result = {
        "company_id": company
    }

    for period in periods:

        if len(company_df) >= period + 1:

            start = company_df.iloc[-(period + 1)]
            end = company_df.iloc[-1]

            # ---------------- Revenue CAGR ----------------

            result[f"revenue_cagr_{period}yr"] = calculate_cagr(
                start["sales"],
                end["sales"],
                period
            )

            result[f"revenue_flag_{period}yr"] = detect_case(
                start["sales"],
                end["sales"]
            )

            # ---------------- Profit CAGR ----------------

            result[f"profit_cagr_{period}yr"] = calculate_cagr(
                start["net_profit"],
                end["net_profit"],
                period
            )

            result[f"profit_flag_{period}yr"] = detect_case(
                start["net_profit"],
                end["net_profit"]
            )

            # ---------------- EPS CAGR ----------------

            result[f"eps_cagr_{period}yr"] = calculate_cagr(
                start["eps"],
                end["eps"],
                period
            )

            result[f"eps_flag_{period}yr"] = detect_case(
                start["eps"],
                end["eps"]
            )

        else:

            result[f"revenue_cagr_{period}yr"] = None
            result[f"revenue_flag_{period}yr"] = "INSUFFICIENT_DATA"

            result[f"profit_cagr_{period}yr"] = None
            result[f"profit_flag_{period}yr"] = "INSUFFICIENT_DATA"

            result[f"eps_cagr_{period}yr"] = None
            result[f"eps_flag_{period}yr"] = "INSUFFICIENT_DATA"

    results.append(result)

    result_df = pd.DataFrame(results)

    print(result_df.head())

    print()

    print("Total Companies:", len(result_df))

    result_df.to_csv(
        output_path / "day10_cagr.csv",
        index=False
    )



    print("CSV Saved Successfully")

    print(result_df.head())


    def detect_case(start_value, end_value):

        if pd.isna(start_value) or pd.isna(end_value):
            return "INSUFFICIENT_DATA"

        if start_value == 0:
            return "ZERO_BASE"

        if start_value > 0 and end_value > 0:
            return "NORMAL"

        if start_value < 0 and end_value > 0:
            return "TURNAROUND"

        if start_value > 0 and end_value < 0:
            return "DECLINE_TO_LOSS"

        if start_value < 0 and end_value < 0:
            return "BOTH_NEGATIVE"

        return "UNKNOWN"


    print("\n==============================")
    print("DAY 10 SUMMARY")
    print("==============================")

    print("Companies Processed :", len(result_df))

    print("Turnaround Cases :",
          (result_df.astype(str).apply(lambda c: c.str.contains("TURNAROUND")).sum()).sum())

    print("Decline To Loss :",
          (result_df.astype(str).apply(lambda c: c.str.contains("DECLINE_TO_LOSS")).sum()).sum())

    print("Both Negative :",
          (result_df.astype(str).apply(lambda c: c.str.contains("BOTH_NEGATIVE")).sum()).sum())

    print("Zero Base :",
          (result_df.astype(str).apply(lambda c: c.str.contains("ZERO_BASE")).sum()).sum())

    print("Insufficient Data :",
          (result_df.astype(str).apply(lambda c: c.str.contains("INSUFFICIENT_DATA")).sum()).sum())