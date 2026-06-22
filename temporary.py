import pandas as pd

df = pd.read_excel(
    "data/raw/companies.xlsx",
    header=1
)

print(df.head())
print(df.columns.tolist())