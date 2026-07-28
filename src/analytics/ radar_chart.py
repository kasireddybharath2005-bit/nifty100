import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# -----------------------------
# Project Paths
# -----------------------------
project_root = Path(__file__).resolve().parents[2]

db_path = project_root / "db" / "nifty100.db"
peer_csv = project_root / "data" / "processed" / "peer_groups_cleaned.csv"

report_path = project_root / "reports" / "radar_charts"
report_path.mkdir(parents=True, exist_ok=True)

# -----------------------------
# Database Connection
# -----------------------------
conn = sqlite3.connect(db_path)

# -----------------------------
# Load Financial Ratios
# -----------------------------
financial = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

# -----------------------------
# Load Peer Groups
# -----------------------------
peer = pd.read_csv(
    peer_csv,
    header=None
)

peer.columns = [
    "id",
    "peer_group_name",
    "company_id",
    "is_active"
]

# -----------------------------
# Merge Tables
# -----------------------------
df = pd.merge(
    financial,
    peer,
    on="company_id",
    how="left"
)

# Remove companies without peer group
df = df.dropna(subset=["peer_group_name"])

print("Merged Shape :", df.shape)

# -----------------------------
# Metrics for Radar Chart
# -----------------------------
metrics = [
    "roe_calculated",
    "net_profit_margin",
    "debt_to_equity",
    "free_cash_flow",
    "profit_cagr_5yr",
    "revenue_cagr_5yr"
]

# Check missing columns
missing = [c for c in metrics if c not in df.columns]

if missing:
    print("Missing Columns :", missing)
    conn.close()
    raise Exception("Required columns not found.")

companies = sorted(df["company_id"].unique())

print("Companies Found :", len(companies))
# ------------------------------------------
# Generate Radar Chart for Each Company
# ------------------------------------------

for company in companies:

    # Get company data
    company_df = df[df["company_id"] == company]

    if company_df.empty:
        continue

    # Get Peer Group
    peer_group = company_df.iloc[0]["peer_group_name"]

    # Get all peer companies
    peer_df = df[df["peer_group_name"] == peer_group]

    # -----------------------
    # Company Values
    # -----------------------
    company_values = []

    for metric in metrics:

        value = company_df.iloc[0][metric]

        if pd.isna(value):
            value = 0

        company_values.append(float(value))

    # -----------------------
    # Peer Average
    # -----------------------
    peer_average = []

    for metric in metrics:

        avg = peer_df[metric].fillna(0).mean()

        peer_average.append(float(avg))

    # -----------------------
    # Radar Labels
    # -----------------------
    labels = [
        "ROE",
        "NPM",
        "D/E",
        "FCF",
        "Profit CAGR 5Y",
        "Revenue CAGR 5Y"
    ]

    # -----------------------
    # Radar Angles
    # -----------------------
    angles = np.linspace(
        0,
        2 * np.pi,
        len(labels),
        endpoint=False
    ).tolist()

    # Close the polygon
    angles.append(angles[0])

    company_values.append(company_values[0])
    peer_average.append(peer_average[0])

    # -----------------------
    # Create Figure
    # -----------------------
    fig, ax = plt.subplots(
        figsize=(8, 8),
        subplot_kw=dict(polar=True)
    )

    # -----------------------
    # Company Plot
    # -----------------------
    ax.plot(
        angles,
        company_values,
        linewidth=2,
        color="blue",
        label=company
    )

    ax.fill(
        angles,
        company_values,
        alpha=0.30,
        color="blue"
    )

    # -----------------------
    # Peer Average Plot
    # -----------------------
    ax.plot(
        angles,
        peer_average,
        linestyle="--",
        linewidth=2,
        color="red",
        label="Peer Average"
    )

    # -----------------------
    # Axis Labels
    # -----------------------
    ax.set_xticks(angles[:-1])

    ax.set_xticklabels(
        labels,
        fontsize=10
    )

    # -----------------------
    # Chart Title
    # -----------------------
    ax.set_title(
        f"{company}\n({peer_group})",
        fontsize=14
    )

    ax.legend(
        loc="upper right"
    )

    plt.tight_layout()

    # -----------------------
    # Save PNG
    # -----------------------
    plt.savefig(
        report_path / f"{company}_radar.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(f"Generated : {company}")
    # ------------------------------------------
    # Close Database
    # ------------------------------------------

    conn.close()

    # ------------------------------------------
    # Count Generated Charts
    # ------------------------------------------

    png_files = list(report_path.glob("*.png"))

    print("\n" + "=" * 50)
    print("DAY 19 COMPLETED SUCCESSFULLY")
    print("=" * 50)

    print(f"Total Companies Processed : {len(companies)}")
    print(f"Radar Charts Generated    : {len(png_files)}")
    print(f"Reports Folder            : {report_path}")

    print("=" * 50)

    if len(png_files) > 0:
        print("\nSample Charts:")

        for file in png_files[:10]:
            print(file.name)

    print("\nRadar Chart Generation Finished Successfully.")