import sqlite3
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]

db_path = project_root / "db" / "nifty100.db"

conn = sqlite3.connect(db_path)

cursor = conn.cursor()

print("=" * 60)
print("DAY 14 FINAL VERIFICATION")
print("=" * 60)

queries = {

    "Total Records":
    "SELECT COUNT(*) FROM financial_ratios",

    "Unique Companies":
    "SELECT COUNT(DISTINCT company_id) FROM financial_ratios",

    "Average ROE":
    "SELECT ROUND(AVG(roe_calculated),2) FROM financial_ratios",

    "Average Net Profit Margin":
    "SELECT ROUND(AVG(net_profit_margin),2) FROM financial_ratios",

    "Average Debt To Equity":
    "SELECT ROUND(AVG(debt_to_equity),2) FROM financial_ratios",

    "Average Asset Turnover":
    "SELECT ROUND(AVG(asset_turnover),2) FROM financial_ratios"

}

for title, sql in queries.items():

    cursor.execute(sql)

    print(f"{title:<30} {cursor.fetchone()[0]}")

conn.close()

print("\nVerification Completed Successfully")