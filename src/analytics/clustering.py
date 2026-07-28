from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

project_root = Path(__file__).resolve().parents[2]

input_path = project_root / "output"

cluster_df = pd.read_excel(input_path / "valuation_summary.xlsx")


# Features for clustering
features = ["pe_ratio", "pb_ratio", "ev_ebitda", "fcf_yield_pct", "pe_difference_pct"]

# Keep sector for median filling
cluster_data = cluster_df[["company_id", "broad_sector"] + features].copy()

print(cluster_data.head())

print("=" * 60)
print("MISSING VALUES")
print("=" * 60)
print(cluster_data.isna().sum())

# Fill missing values using sector median
cluster_data[features] = cluster_data.groupby("broad_sector")[features].transform(
    lambda x: x.fillna(x.median())
)

print("=" * 60)
print("AFTER FILLING")
print("=" * 60)
print(cluster_data.isna().sum())

print("=" * 60)
print("AVAILABLE COLUMNS")
print("=" * 60)

for col in cluster_df.columns:
    print(col)


# Scale the data
scaler = StandardScaler()

scaled_data = scaler.fit_transform(cluster_data[features])

print("=" * 60)
print("SCALED DATA SHAPE")
print("=" * 60)
print(scaled_data.shape)


kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)

cluster_data["cluster_id"] = kmeans.fit_predict(scaled_data)

output_df = cluster_data[["company_id", "cluster_id"]]

output_df.to_csv(input_path / "cluster_labels.csv", index=False)

print("=" * 60)
print("CLUSTERING COMPLETED")
print("=" * 60)
print(output_df.head())


inertia = []

for k in range(2, 11):
    model = KMeans(n_clusters=k, random_state=42, n_init=10)

    model.fit(scaled_data)
    inertia.append(model.inertia_)

plt.figure(figsize=(8, 5))
plt.plot(range(2, 11), inertia, marker="o")
plt.xlabel("Number of Clusters (k)")
plt.ylabel("Inertia")
plt.title("Elbow Method")

plt.savefig(project_root / "reports" / "elbow_plot.png")

plt.show()
