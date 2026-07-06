import sqlite3
import pandas as pd
import yaml
from pathlib import Path

# ==========================================
# PROJECT PATH
# ==========================================

project_root = Path(__file__).resolve().parents[2]

db_path = project_root / "db" / "nifty100.db"

config_path = project_root / "src" / "screener" / "config.yaml"

output_path = project_root / "output"

output_path.mkdir(exist_ok=True)

# ==========================================
# LOAD CONFIG
# ==========================================

with open(config_path, "r") as f:
    config = yaml.safe_load(f)

print("Configuration Loaded")

# ==========================================
# LOAD DATABASE
# ==========================================

conn = sqlite3.connect(db_path)

df = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

conn.close()

print("Rows Loaded:", len(df))

# ==========================================
# APPLY FILTERS
# ==========================================

filtered = df[
    (df["roe_calculated"] >= config["roe_min"]) &
    (df["debt_to_equity"] <= config["debt_to_equity_max"]) &
    (df["net_profit_margin"] >= config["net_profit_margin_min"]) &
    (df["asset_turnover"] >= config["asset_turnover_min"]) &
    (df["revenue_cagr_5yr"] >= config["revenue_cagr_5yr_min"]) &
    (df["free_cash_flow"] >= config["fcf_min"])
]

print("Companies Selected:", len(filtered))

# ==========================================
# SORT
# ==========================================

filtered = filtered.sort_values(
    by=config["sort_by"],
    ascending=False
)

# ==========================================
# QUALITY SCORE
# ==========================================

filtered["quality_score"] = (
      filtered["roe_calculated"]
    + filtered["net_profit_margin"])
filtered["quality_score"] = (
    filtered["roe_calculated"].fillna(0)
    + filtered["net_profit_margin"].fillna(0)
    + filtered["asset_turnover"].fillna(0) * 10
    + filtered["revenue_cagr_5yr"].fillna(0)
)

filtered = filtered.sort_values(
    by="quality_score",
    ascending=False
)

result = filtered[
    [
        "company_id",
        "year",
        "roe_calculated",
        "debt_to_equity",
        "net_profit_margin",
        "asset_turnover",
        "revenue_cagr_5yr",
        "free_cash_flow",
        "quality_score"
    ]
]
result.to_csv(
    output_path / "screener_output.csv",
    index=False
)

print("\nTop 10 Companies")

print(result.head(10))

print("\nTotal Companies Selected :", len(result))

print("\nOutput Saved Successfully")