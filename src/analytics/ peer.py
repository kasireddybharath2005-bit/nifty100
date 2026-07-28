import sqlite3
import pandas as pd
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]

db_path = project_root / "db" / "nifty100.db"

conn = sqlite3.connect(db_path)
financial = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

peer = pd.read_sql(
    "SELECT * FROM peer_groups",
    conn
)
peer.columns = [
    "id",
    "peer_group_name",
    "company_id",
    "is_active"
]

print(financial.head())
print(peer.head())



print(peer.columns.tolist())
print(peer.head())

print(financial.columns.tolist())

print(financial.head(1).T)
print(peer.head(1).T)

df = pd.merge(
    financial,
    peer,
    on="company_id",
    how="left"
)

print(df.shape)
print(df.head())
missing = df["peer_group_name"].isna().sum()

print("Missing Peer Groups :", missing)

df = df.dropna(subset=["peer_group_name"])
metrics = [

    "roe_calculated",

    "roce_calculated",

    "net_profit_margin",

    "debt_to_equity",

    "free_cash_flow",

    "profit_cagr_5yr",

    "revenue_cagr_5yr",

    "eps_cagr_5yr",

    "interest_coverage",

    "asset_turnover"

]
records = []

groups = df.groupby("peer_group_name")

for group_name, group in groups:

    for metric in metrics:

        if metric not in group.columns:
            continue

        temp = group.copy()

        temp["percentile"] = (
            temp[metric]
            .rank(pct=True)
            * 100
        )

        if metric == "debt_to_equity":

            temp["percentile"] = (
                100 -
                temp["percentile"]
            )

        for _, row in temp.iterrows():

            records.append({

                "company_id": row["company_id"],

                "peer_group_name": group_name,

                "metric": metric,

                "value": row[metric],

                "percentile_rank": round(
                    row["percentile"], 2
                ),

                "year": row["year"]

            })

peer_percentiles = pd.DataFrame(records)

print(peer_percentiles.head())

print(peer_percentiles.shape)
peer_percentiles.to_sql(

    "peer_percentiles",

    conn,

    if_exists="replace",

    index=False

)

cursor = conn.cursor()

cursor.execute(

    "SELECT COUNT(*) FROM peer_percentiles"

)

print(

    "Rows Inserted :",

    cursor.fetchone()[0]

)

conn.close()

missing = df[df["peer_group_name"].isna()]

print(missing["company_id"].unique())