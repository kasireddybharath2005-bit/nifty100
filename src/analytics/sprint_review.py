import sqlite3
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]

db_path = project_root / "db" / "nifty100.db"

output = project_root / "output"

conn = sqlite3.connect(db_path)

cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM financial_ratios")

rows = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(DISTINCT company_id) FROM financial_ratios")

companies = cursor.fetchone()[0]

report = f"""

SPRINT 2 REVIEW
==============================

Database : nifty100.db

financial_ratios Table : YES

Rows Loaded : {rows}

Companies : {companies}

Days Completed
Day 8 - Profitability Ratios
Day 9 - Leverage Ratios
Day 10 - CAGR Engine
Day 11 - Cash Flow KPIs
Day 12 - Financial Ratio Table
Day 13 - Edge Case Validation
Day 14 - Testing & Review

Status : SUCCESS

"""

with open(output / "sprint2_review.txt", "w", encoding="utf-8") as f:

    f.write(report)

print(report)

conn.close()