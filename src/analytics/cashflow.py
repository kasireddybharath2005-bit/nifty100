import pandas as pd
from pathlib import Path

# ==========================================
# PROJECT PATH
# ==========================================

project_root = Path(__file__).resolve().parents[2]

processed_path = project_root / "data" / "processed"

output_path = project_root / "output"
output_path.mkdir(exist_ok=True)

# ==========================================
# LOAD DATA
# ==========================================

cashflow = pd.read_csv(
    processed_path / "cashflow_cleaned.csv"
)

profitloss = pd.read_csv(
    processed_path / "profitandloss_cleaned.csv"
)

print("Datasets Loaded Successfully")

# ==========================================
# MERGE
# ==========================================

df = pd.merge(
    cashflow,
    profitloss,
    on=["company_id", "year"],
    how="inner"
)

print("Merged Shape :", df.shape)

# ==========================================
# FREE CASH FLOW
# ==========================================

df["free_cash_flow"] = (
    df["operating_activity"] +
    df["investing_activity"]
)

# ==========================================
# CFO QUALITY SCORE
# ==========================================

def cfo_quality(cfo, profit):

    if profit == 0:
        return None

    score = cfo / profit

    if score > 1:

        return "High Quality"

    elif score >= 0.5:

        return "Moderate"

    else:

        return "Low Quality"

df["cfo_quality"] = df.apply(
    lambda row:
    cfo_quality(
        row["operating_activity"],
        row["net_profit"]
    ),
    axis=1
)

# ==========================================
# CAPEX INTENSITY
# ==========================================

def capex_label(value):

    if value < 3:
        return "Asset Light"

    elif value <= 8:
        return "Moderate"

    else:
        return "Capital Intensive"

df["capex_intensity"] = (
    abs(df["investing_activity"])
    / df["sales"]
) * 100

df["capex_label"] = df[
    "capex_intensity"
].apply(capex_label)

# ==========================================
# FCF CONVERSION
# ==========================================

def fcf_conversion(fcf, op):

    if op == 0:
        return None

    return round((fcf / op) * 100, 2)

df["fcf_conversion"] = df.apply(

    lambda row:
    fcf_conversion(
        row["free_cash_flow"],
        row["operating_profit"]
    ),

    axis=1
)

# ==========================================
# CAPITAL ALLOCATION
# ==========================================

def sign(x):

    if x > 0:
        return "+"

    elif x < 0:
        return "-"

    return "0"

def pattern(cfo, cfi, cff):

    code = (
        sign(cfo),
        sign(cfi),
        sign(cff)
    )

    mapping = {

        ("+","-","-"):"Shareholder Returns",

        ("+","+","+"):"Cash Accumulator",

        ("+","-","+"):"Growth Funded by Debt",

        ("-","+","+"):"Distress Signal",

        ("-","-","-"):"Pre-Revenue",

        ("+","+","-"):"Liquidating Assets"

    }

    return mapping.get(code,"Mixed")

df["capital_pattern"] = df.apply(

    lambda row:

    pattern(

        row["operating_activity"],

        row["investing_activity"],

        row["financing_activity"]

    ),

    axis=1

)

# ==========================================
# SAVE
# ==========================================

columns = [

    "company_id",

    "year",

    "free_cash_flow",

    "cfo_quality",

    "capex_intensity",

    "capex_label",

    "fcf_conversion",

    "capital_pattern"

]

result = df[columns]

result.to_csv(

    output_path / "capital_allocation.csv",

    index=False

)

print()

print(result.head())

print()

print("Rows :", len(result))

print("Saved Successfully")