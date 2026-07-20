
from pathlib import Path
import pandas as pd
project_root = Path(__file__).resolve().parents[2]

input_path = project_root / "data" / "raw"

output_path = project_root / "output"

output_path.mkdir(exist_ok=True)
ratios_df = pd.read_excel(
    input_path / "financial_ratios.xlsx"
)

analysis_df = pd.read_csv(
    output_path / "analysis_parsed.csv"
)

print("=" * 60)
print("FINANCIAL RATIOS")
print("=" * 60)

print(ratios_df.head())

print("=" * 60)
print("ANALYSIS PARSED")
print("=" * 60)

print(analysis_df.head())
# --------------------------------------------------
# Store Generated Pros & Cons
# --------------------------------------------------

pros_cons = []

# --------------------------------------------------
# Pro Rule 1
# --------------------------------------------------

roe_df = analysis_df[
    analysis_df["metric_type"] == "roe"
]

for _, row in roe_df.iterrows():

    if row["value_pct"] >= 20:

        pros_cons.append({

            "company_id": row["company_id"],

            "type": "Pro",

            "rule_id": "PRO_1",

            "text": "Consistently high return on equity above 20% demonstrates exceptional capital efficiency.",

            "confidence_pct": 95

        })
        # --------------------------------------------------
        # Pro Rule 4
        # --------------------------------------------------

        sales_df = analysis_df[
            analysis_df["metric_type"] ==
            "compounded_sales_growth"
            ]

        for _, row in sales_df.iterrows():

            if row["value_pct"] >= 15:
                pros_cons.append({

                    "company_id": row["company_id"],

                    "type": "Pro",

                    "rule_id": "PRO_4",

                    "text": "Revenue growing above 15% CAGR reflects strong business momentum.",

                    "confidence_pct": 90

                })

                # --------------------------------------------------
                # Pro Rule 6
                # --------------------------------------------------

                profit_df = analysis_df[
                    analysis_df["metric_type"] ==
                    "compounded_profit_growth"
                    ]

                for _, row in profit_df.iterrows():

                    if row["value_pct"] >= 20:
                        pros_cons.append({

                            "company_id": row["company_id"],

                            "type": "Pro",

                            "rule_id": "PRO_6",

                            "text": "Net profit compounding above 20% over the selected period creates significant shareholder value.",

                            "confidence_pct": 92

                        })

                        # --------------------------------------------------
                        # Pro Rule 9
                        # --------------------------------------------------

                        stock_df = analysis_df[
                            analysis_df["metric_type"] ==
                            "stock_price_cagr"
                            ]

                        for _, row in stock_df.iterrows():

                            if row["value_pct"] >= 15:
                                pros_cons.append({

                                    "company_id": row["company_id"],

                                    "type": "Pro",

                                    "rule_id": "PRO_9",

                                    "text": "Stock price has delivered strong CAGR over the selected investment period.",

                                    "confidence_pct": 88

                                })

                                print("=" * 60)
                                print("GENERATED PROS")
                                print("=" * 60)

                                pros_df = pd.DataFrame(pros_cons)

                                print(pros_df.head(20))

                                pros_df.to_csv(
                                    output_path / "pros_cons_generated.csv",
                                    index=False
                                )

                                print("pros_cons_generated.csv created successfully.")

    # --------------------------------------------------
    # Con Rule 1
    # --------------------------------------------------

for _, row in ratios_df.iterrows():

    if row["debt_to_equity"] >= 2:
        pros_cons.append({

            "company_id": row["company_id"],

            "type": "Con",

            "rule_id": "CON_1",

            "text": "Debt-to-equity ratio is high and warrants monitoring.",

            "confidence_pct": 92

        })

        # --------------------------------------------------
        # Con Rule 6
        # --------------------------------------------------

        for _, row in ratios_df.iterrows():

            if row["interest_coverage"] < 1.5:
                pros_cons.append({

                    "company_id": row["company_id"],

                    "type": "Con",

                    "rule_id": "CON_6",

                    "text": "Interest coverage below 1.5 indicates financial stress.",

                    "confidence_pct": 95

                })

                # --------------------------------------------------
                # Pro Rule 7
                # --------------------------------------------------

                for _, row in ratios_df.iterrows():

                    if row["interest_coverage"] > 10:
                        pros_cons.append({

                            "company_id": row["company_id"],

                            "type": "Pro",

                            "rule_id": "PRO_7",

                            "text": "Very high interest coverage reflects negligible financial stress.",

                            "confidence_pct": 90

                        })

                        # --------------------------------------------------
                        # Pro Rule 3
                        # --------------------------------------------------

                        for _, row in ratios_df.iterrows():

                            if row["debt_to_equity"] == 0:
                                pros_cons.append({

                                    "company_id": row["company_id"],

                                    "type": "Pro",

                                    "rule_id": "PRO_3",

                                    "text": "Debt-free balance sheet provides financial flexibility.",

                                    "confidence_pct": 93

                                })

                                pros_df = pd.DataFrame(pros_cons)

                                print("=" * 60)
                                print("GENERATED PROS & CONS")
                                print("=" * 60)

                                print(pros_df.head(30))

                                pros_df = pros_df.drop_duplicates(
                                    subset=[
                                        "company_id",
                                        "rule_id"
                                    ]
                                )

                                pros_df.to_csv(

                                    output_path /

                                    "pros_cons_generated.csv",

                                    index=False

                                )

                                print("pros_cons_generated.csv created successfully.")

                                print("=" * 60)
                                print("SUMMARY")
                                print("=" * 60)

                                print("Total Rules Generated :", len(pros_df))

                                print("Pros :", len(pros_df[pros_df["type"] == "Pro"]))

                                print("Cons :", len(pros_df[pros_df["type"] == "Con"]))

                                # --------------------------------------------------
                                # Pro Rule 2
                                # --------------------------------------------------

                                for _, row in ratios_df.iterrows():

                                    if row["cash_from_operations_cr"] > 0:
                                        pros_cons.append({

                                            "company_id": row["company_id"],

                                            "type": "Pro",

                                            "rule_id": "PRO_2",

                                            "text": "Positive cash flow from operations indicates healthy business fundamentals.",

                                            "confidence_pct": 90

                                        })

                                        # --------------------------------------------------
                                        # Pro Rule 5
                                        # --------------------------------------------------

                                        for _, row in ratios_df.iterrows():

                                            if row["operating_profit_margin_pct"] >= 25:
                                                pros_cons.append({

                                                    "company_id": row["company_id"],

                                                    "type": "Pro",

                                                    "rule_id": "PRO_5",

                                                    "text": "Operating profit margin above 25% indicates strong pricing power.",

                                                    "confidence_pct": 91

                                                })
                                                # --------------------------------------------------
                                                # Pro Rule 8
                                                # --------------------------------------------------

                                                if "dividend_yield_pct" in ratios_df.columns:

                                                    for _, row in ratios_df.iterrows():

                                                        if row["dividend_yield_pct"] >= 2:
                                                            pros_cons.append({

                                                                "company_id": row["company_id"],

                                                                "type": "Pro",

                                                                "rule_id": "PRO_8",

                                                                "text": "Consistent dividend yield above 2% supports shareholder returns.",

                                                                "confidence_pct": 87

                                                            })

                                                            # --------------------------------------------------
                                                            # Pro Rule 10
                                                            # --------------------------------------------------

                                                            if "asset_turnover" in ratios_df.columns:

                                                                for _, row in ratios_df.iterrows():

                                                                    if row["asset_turnover"] >= 1.5:
                                                                        pros_cons.append({

                                                                            "company_id": row["company_id"],

                                                                            "type": "Pro",

                                                                            "rule_id": "PRO_10",

                                                                            "text": "High asset turnover reflects efficient asset utilization.",

                                                                            "confidence_pct": 85

                                                                        })

                                                                        # --------------------------------------------------
                                                                        # Con Rule 2
                                                                        # --------------------------------------------------

                                                                        for _, row in ratios_df.iterrows():

                                                                            if row["cash_from_operations_cr"] < 0:
                                                                                pros_cons.append({

                                                                                    "company_id": row["company_id"],

                                                                                    "type": "Con",

                                                                                    "rule_id": "CON_2",

                                                                                    "text": "Negative operating cash flow may indicate weak cash generation.",

                                                                                    "confidence_pct": 94

                                                                                })

                                                                                # --------------------------------------------------
                                                                                # Con Rule 3
                                                                                # --------------------------------------------------

                                                                                for _, row in ratios_df.iterrows():

                                                                                    if row[
                                                                                        "operating_profit_margin_pct"] < 10:
                                                                                        pros_cons.append({

                                                                                            "company_id": row[
                                                                                                "company_id"],

                                                                                            "type": "Con",

                                                                                            "rule_id": "CON_3",

                                                                                            "text": "Low operating margin suggests pressure on profitability.",

                                                                                            "confidence_pct": 88

                                                                                        })

                                                                                        # --------------------------------------------------
                                                                                        # Con Rule 4
                                                                                        # --------------------------------------------------

                                                                                        for _, row in ratios_df.iterrows():

                                                                                            if row[
                                                                                                "net_profit_margin_pct"] < 0:
                                                                                                pros_cons.append({

                                                                                                    "company_id": row[
                                                                                                        "company_id"],

                                                                                                    "type": "Con",

                                                                                                    "rule_id": "CON_4",

                                                                                                    "text": "Negative net profit margin indicates recent losses.",

                                                                                                    "confidence_pct": 96

                                                                                                })
                                                                                                # --------------------------------------------------
                                                                                                # Con Rule 10
                                                                                                # --------------------------------------------------

                                                                                                for _, row in ratios_df.iterrows():

                                                                                                    if row[
                                                                                                        "return_on_equity_pct"] < 10:
                                                                                                        pros_cons.append(
                                                                                                            {

                                                                                                                "company_id":
                                                                                                                    row[
                                                                                                                        "company_id"],

                                                                                                                "type": "Con",

                                                                                                                "rule_id": "CON_10",

                                                                                                                "text": "Low return on equity indicates weak capital efficiency.",

                                                                                                                "confidence_pct": 90

                                                                                                            })

                                            # --------------------------------------------------
                                            # Pro Rule 11
                                            # --------------------------------------------------

                                        sales_df = analysis_df[
                                            analysis_df["metric_type"] == "compounded_sales_growth"
                                            ]

                                        profit_df = analysis_df[
                                            analysis_df["metric_type"] == "compounded_profit_growth"
                                            ]

                                        merged_growth = pd.merge(
                                            sales_df,
                                            profit_df,
                                            on="company_id",
                                            suffixes=("_sales", "_profit")
                                        )

                                        for _, row in merged_growth.iterrows():

                                            if row["value_pct_sales"] > row["value_pct_profit"]:
                                                pros_cons.append({

                                                    "company_id": row["company_id"],

                                                    "type": "Pro",

                                                    "rule_id": "PRO_11",

                                                    "text": "Revenue growth exceeds profit growth, indicating sustained business expansion.",

                                                    "confidence_pct": 85

                                                })
                                                # --------------------------------------------------
                                                # Con Rule 5
                                                # --------------------------------------------------

                                                sales_df = analysis_df[
                                                    analysis_df["metric_type"] == "compounded_sales_growth"
                                                    ]

                                                for _, row in sales_df.iterrows():

                                                    if row["value_pct"] < 5:
                                                        pros_cons.append({

                                                            "company_id": row["company_id"],

                                                            "type": "Con",

                                                            "rule_id": "CON_5",

                                                            "text": "Revenue growth below 5% indicates weak business momentum.",

                                                            "confidence_pct": 90

                                                        })
                                                        summary_df = (
                                                            pd.DataFrame(pros_cons)
                                                            .groupby(["company_id", "type"])
                                                            .size()
                                                            .unstack(fill_value=0)
                                                            .reset_index()
                                                        )

                                                        summary_df.columns.name = None

                                                        if "Pro" not in summary_df.columns:
                                                            summary_df["Pro"] = 0

                                                        if "Con" not in summary_df.columns:
                                                            summary_df["Con"] = 0

                                                        print("=" * 60)
                                                        print("COMPANY SUMMARY")
                                                        print("=" * 60)

                                                        print(summary_df.head())

                                                        summary_df.to_csv(
                                                            output_path / "pros_cons_summary.csv",
                                                            index=False
                                                        )

                                                        print("pros_cons_summary.csv created successfully.")

                                                        print("=" * 60)
                                                        print("FINAL SUMMARY")
                                                        print("=" * 60)

                                                        pros_df = pd.DataFrame(pros_cons)

                                                        print(f"Total Rules Generated : {len(pros_df)}")
                                                        print(
                                                            f"Unique Companies      : {pros_df['company_id'].nunique()}")
                                                        print(
                                                            f"Pros Generated        : {(pros_df['type'] == 'Pro').sum()}")
                                                        print(
                                                            f"Cons Generated        : {(pros_df['type'] == 'Con').sum()}")
