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