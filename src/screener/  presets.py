import sqlite3
import pandas as pd
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]

db_path = project_root / "db" / "nifty100.db"

output_path = project_root / "output"

conn = sqlite3.connect(db_path)

df = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

conn.close()

print("Rows Loaded :", len(df))

quality = df[
    (df["roe_calculated"] > 15) &
    (df["debt_to_equity"] < 1) &
    (df["free_cash_flow"] > 0) &
    (df["revenue_cagr_5yr"] > 10)
]

print("Quality :", len(quality))

value = df[
    (df["debt_to_equity"] < 2)
]

growth = df[
    (df["profit_cagr_5yr"] > 20) &
    (df["revenue_cagr_5yr"] > 15) &
    (df["debt_to_equity"] < 2)
]

dividend = df[
    df["free_cash_flow"] > 0
]

debtfree = df[
    (df["debt_to_equity"] == 0) &
    (df["roe_calculated"] > 12)
]

turnaround = df[
    (df["revenue_cagr_3yr"] > 10) &
    (df["free_cash_flow"] > 0)
]

with pd.ExcelWriter(
    output_path / "screener_output.xlsx"
) as writer:

    quality.to_excel(
        writer,
        sheet_name="Quality",
        index=False
    )

    value.to_excel(
        writer,
        sheet_name="Value",
        index=False
    )

    growth.to_excel(
        writer,
        sheet_name="Growth",
        index=False
    )

    dividend.to_excel(
        writer,
        sheet_name="Dividend",
        index=False
    )

    debtfree.to_excel(
        writer,
        sheet_name="DebtFree",
        index=False
    )

    turnaround.to_excel(
        writer,
        sheet_name="Turnaround",
        index=False
    )

print("Excel Export Completed")

print()

print("========== DAY 16 ==========")

print("Quality :", len(quality))

print("Value :", len(value))

print("Growth :", len(growth))

print("Dividend :", len(dividend))

print("Debt Free :", len(debtfree))

print("Turnaround :", len(turnaround))