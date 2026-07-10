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

print(df.shape)

columns = [

    "company_id",

    "year",

    "roe_calculated",

    "net_profit_margin",

    "revenue_cagr_5yr",

    "free_cash_flow",

    "debt_to_equity",

    "asset_turnover"

]

df = df[columns]

df.fillna(0, inplace=True)

def normalize(column):

    minimum = column.min()

    maximum = column.max()

    if maximum == minimum:

        return 0

    return ((column - minimum) / (maximum - minimum)) * 100

df["roe_score"] = normalize(df["roe_calculated"])

df["npm_score"] = normalize(df["net_profit_margin"])

df["cagr_score"] = normalize(df["revenue_cagr_5yr"])

df["fcf_score"] = normalize(df["free_cash_flow"])

df["asset_score"] = normalize(df["asset_turnover"])

df["debt_score"] = 100 - normalize(df["debt_to_equity"])

df["composite_score"] = (

      df["roe_score"]*0.20

    + df["npm_score"]*0.15

    + df["fcf_score"]*0.15

    + df["asset_score"]*0.15

    + df["cagr_score"]*0.20

    + df["debt_score"]*0.15

)
df["composite_score"] = df[
    "composite_score"
].round(2)

df = df.sort_values(

    by="composite_score",

    ascending=False

)

df["rank"] = range(

    1,

    len(df)+1

)

with pd.ExcelWriter(

    output_path/

    "screener_output.xlsx"

) as writer:

    df.to_excel(

        writer,

        index=False,

        sheet_name="Composite Score"

    )
    print()

    print(df.head(20))

    print()

    print("Rows :", len(df))

    print()

    print("Top Company")

    print(df.iloc[0]["company_id"])

    print()

    print("Composite Score")

    print(df.iloc[0]["composite_score"])