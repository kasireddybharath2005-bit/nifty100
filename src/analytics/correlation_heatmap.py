from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

project_root = Path(__file__).resolve().parents[2]

input_path = project_root / "output"

report_path = project_root / "reports"

df = pd.read_excel(
    input_path / "valuation_summary.xlsx"
)

features = [
    "pe_ratio",
    "pb_ratio",
    "ev_ebitda",
    "fcf_yield_pct",
    "market_cap_crore",
]

corr = df[features].corr()

plt.figure(figsize=(8, 6))

plt.imshow(corr)

plt.xticks(range(len(features)), features, rotation=45)

plt.yticks(range(len(features)), features)

plt.colorbar()

plt.tight_layout()

plt.savefig(
    report_path / "correlation_heatmap.png"
)

plt.show()