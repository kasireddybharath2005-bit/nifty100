from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

from scipy.stats import zscore

# ----------------------------------------------------
# PATHS
# ----------------------------------------------------

project_root = Path(__file__).resolve().parents[2]

input_path = project_root / "output"
report_path = project_root / "reports"

report_path.mkdir(parents=True, exist_ok=True)

# ----------------------------------------------------
# LOAD FILES
# ----------------------------------------------------

cluster_df = pd.read_csv(
    input_path / "cluster_labels.csv"
)

valuation_df = pd.read_excel(
    input_path / "valuation_summary.xlsx"
)

print("=" * 60)
print("FILES LOADED")
print("=" * 60)

print(cluster_df.head())
print(valuation_df.head())

# ----------------------------------------------------
# MERGE
# ----------------------------------------------------

df = valuation_df.merge(
    cluster_df,
    on="company_id",
    how="left"
)

print("=" * 60)
print("MERGED DATA")
print("=" * 60)

print(df.head())

# ----------------------------------------------------
# FEATURES
# ----------------------------------------------------

features = [
    "pe_ratio",
    "pb_ratio",
    "ev_ebitda",
    "fcf_yield_pct",
    "pe_difference_pct"
]

# ----------------------------------------------------
# CLUSTER STATISTICS
# ----------------------------------------------------

cluster_stats = (
    df.groupby("cluster_id")[features]
      .agg(["mean", "median"])
)

cluster_stats.to_csv(
    input_path / "cluster_statistics.csv"
)

print("=" * 60)
print("CLUSTER STATISTICS")
print("=" * 60)

print(cluster_stats)

# ----------------------------------------------------
# COMPANY COUNT
# ----------------------------------------------------

company_count = (
    df.groupby("cluster_id")
      .size()
      .reset_index(name="company_count")
)

print("=" * 60)
print("COMPANIES PER CLUSTER")
print("=" * 60)

print(company_count)

# ----------------------------------------------------
# CLUSTER NAMES
# ----------------------------------------------------

cluster_names = {
    0: "High Quality",
    1: "Value Stocks",
    2: "Dividend Leaders",
    3: "Growth Companies",
    4: "Turnaround"
}

df["cluster_name"] = (
    df["cluster_id"].map(cluster_names)
)

# ----------------------------------------------------
# CORRELATION HEATMAP
# ----------------------------------------------------

corr = df[features].corr()

plt.figure(figsize=(8,6))

plt.imshow(corr, cmap="coolwarm")

plt.colorbar()

plt.xticks(
    range(len(features)),
    features,
    rotation=45,
    ha="right"
)

plt.yticks(
    range(len(features)),
    features
)

plt.title("Correlation Heatmap")

plt.tight_layout()

plt.savefig(
    report_path / "correlation_heatmap.png"
)

plt.close()

# ----------------------------------------------------
# OUTLIER DETECTION
# ----------------------------------------------------

outlier_df = df.copy()

for col in features:

    outlier_df[col + "_zscore"] = zscore(
        outlier_df[col].fillna(
            outlier_df[col].median()
        )
    )

mask = False

for col in features:

    mask = mask | (
        outlier_df[col + "_zscore"].abs() > 3
    )

outliers = outlier_df[mask]

outliers.to_csv(
    input_path / "outlier_report.csv",
    index=False
)

print("=" * 60)
print("OUTLIERS")
print("=" * 60)

print(len(outliers))

# ----------------------------------------------------
# PORTFOLIO STATISTICS
# ----------------------------------------------------

portfolio_stats = []

for col in features:

    values = df[col].dropna()

    portfolio_stats.append({

        "metric": col,

        "P10": values.quantile(0.10),

        "P25": values.quantile(0.25),

        "P50": values.quantile(0.50),

        "P75": values.quantile(0.75),

        "P90": values.quantile(0.90),

        "Mean": values.mean(),

        "Std": values.std()

    })

portfolio_stats = pd.DataFrame(
    portfolio_stats
)

portfolio_stats.to_csv(

    input_path / "portfolio_stats.csv",

    index=False

)

print("=" * 60)
print("PORTFOLIO STATS")
print("=" * 60)

print(portfolio_stats)

# ----------------------------------------------------
# SAVE FINAL LABELS
# ----------------------------------------------------

df.to_csv(
    input_path / "cluster_profile.csv",
    index=False
)

# ----------------------------------------------------
# SUMMARY
# ----------------------------------------------------

print("=" * 60)
print("DAY 37 SUMMARY")
print("=" * 60)

print("Total Companies :", len(df))
print("Clusters :", df["cluster_id"].nunique())
print("Statistics File : cluster_statistics.csv")
print("Portfolio Stats : portfolio_stats.csv")
print("Outlier Report : outlier_report.csv")
print("Heatmap : correlation_heatmap.png")
print("Completed Successfully")
print("=" * 60)