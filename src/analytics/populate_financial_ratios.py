import sqlite3
import pandas as pd
from pathlib import Path

# ==========================================
# PATHS
# ==========================================

project_root = Path(__file__).resolve().parents[2]

output_path = project_root / "output"

db_path = project_root / "db" / "nifty100.db"

# ==========================================
# LOAD FILES
# ==========================================

day8 = pd.read_csv(output_path / "day8_profitability_ratios.csv")

day9 = pd.read_csv(output_path / "day9_leverage_ratios.csv")

day10 = pd.read_csv(output_path / "day10_cagr.csv")

day11 = pd.read_csv(output_path / "capital_allocation.csv")

print("All files loaded successfully")

# ==========================================
# KEEP KPI COLUMNS ONLY
# ==========================================

day8 = day8[
    [
        "company_id",
        "year",
        "net_profit_margin",
        "operating_profit_margin",
        "roe_calculated",
        "roa"
    ]
]

day9 = day9[
    [
        "company_id",
        "year",
        "debt_to_equity",
        "interest_coverage",
        "asset_turnover",
        "net_debt",
        "high_leverage_flag",
        "icr_label"
    ]
]

day11 = day11[
    [
        "company_id",
        "year",
        "free_cash_flow",
        "cfo_quality",
        "capex_intensity",
        "capex_label",
        "fcf_conversion",
        "capital_pattern"
    ]
]

# ==========================================
# MERGE
# ==========================================

financial = pd.merge(
    day8,
    day9,
    on=["company_id", "year"],
    how="outer"
)

financial = pd.merge(
    financial,
    day11,
    on=["company_id", "year"],
    how="outer"
)

financial = pd.merge(
    financial,
    day10,
    on="company_id",
    how="left"
)

print("Merged Shape :", financial.shape)

# ==========================================
# SAVE SQLITE
# ==========================================

conn = sqlite3.connect(db_path)

financial.to_sql(
    "financial_ratios",
    conn,
    if_exists="replace",
    index=False
)

# ==========================================
# VERIFY
# ==========================================

cursor = conn.cursor()

cursor.execute(
    "SELECT COUNT(*) FROM financial_ratios"
)

rows = cursor.fetchone()[0]

print()

print("Rows Inserted :", rows)

cursor.execute(
    """
    SELECT company_id,
           year,
           net_profit_margin,
           debt_to_equity,
           revenue_cagr_5yr
    FROM financial_ratios
    LIMIT 5
    """
)

print()

for row in cursor.fetchall():

    print(row)

conn.close()

print()

print("Day 12 Completed Successfully")