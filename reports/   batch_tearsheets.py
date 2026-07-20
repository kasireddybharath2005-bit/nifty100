from pathlib import Path
import pandas as pd

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
project_root = Path(__file__).resolve().parent.parent

input_path = project_root / "output"

report_path = project_root / "reports" / "tearsheets"

report_path.mkdir(
    parents=True,
    exist_ok=True
)
cashflow_df = pd.read_excel(

    input_path /
    "cashflow_intelligence.xlsx"

)

pros_df = pd.read_csv(

    input_path /
    "pros_cons_generated.csv"

)
print(cashflow_df.head())

print(pros_df.head())
companies = sorted(

    cashflow_df[
        "company_id"
    ].unique()

)
print("=" * 60)

print("TOTAL COMPANIES")

print("=" * 60)

print(len(companies))

print(companies[:10])
skipped = []

for company in companies:

    print(company)

    company_cashflow = cashflow_df[
        cashflow_df["company_id"] == company
    ]


    company_cashflow = cashflow_df[

            cashflow_df["company_id"]

            ==

            company

            ]

    print(

            company,

            len(company_cashflow)

        )

    if len(company_cashflow) < 3:
            skipped.append(company)

            continue
    latest = company_cashflow.iloc[-1]

    styles = getSampleStyleSheet()

    pdf = SimpleDocTemplate(

                str(report_path /f"{company}_tearsheet.pdf")
        )

    story = []
    story.append(

                Paragraph(

                    f"<b>{company} Financial Tearsheet</b>",

                    styles["Title"]

                )

            )

    story.append(

        Spacer(1, 20)

            )

    table_data = [

                ["Metric", "Value"],

                ["Operating Cash Flow",

                 latest["operating_activity"]],

                ["Free Cash Flow",

                 latest["free_cash_flow"]],

                ["CFO Quality",

                 latest["cfo_quality_label"]],

                ["Capital Allocation",

                 latest["capital_allocation_label"]],

                ["Distress",

                 latest["distress_flag"]]

            ]
    table = Table(table_data)

    table.setStyle(

                TableStyle([

                    ("BACKGROUND",

                     (0, 0),

                     (-1, 0),

                     colors.darkblue),

                    ("TEXTCOLOR",

                     (0, 0),

                     (-1, 0),

                     colors.white),

                    ("GRID",

                     (0, 0),

                     (-1, -1),

                     1,

                     colors.black),

                    ("BACKGROUND",

                     (0, 1),

                     (-1, -1),

                     colors.beige),

                    ("BOTTOMPADDING",

                     (0, 0),

                     (-1, 0),

                     10)

                ])

            )
    story.append(table)

    story.append(

                Spacer(1, 20)

            )
    story.append(

                Paragraph(

                    "<b>Pros</b>",

                    styles["Heading2"]

                )

            )
    pros = pros_df[

                (pros_df["company_id"] == company)

                &

                (pros_df["type"] == "Pro")

                ]
    if len(pros) == 0:

                story.append(

                    Paragraph(

                        "No Pros Available",

                        styles["BodyText"]

                    )

    )

    else:

                for _, row in pros.iterrows():
                    story.append(

                        Paragraph(

                            "• " + str(row["text"]),

                            styles["BodyText"]

                        )

                    )
                    pdf.build(story)

                    print(

                        f"{company} PDF Generated"

        )
    print(

                company,

                latest["free_cash_flow"]

            )

    story.append(

        Spacer(1, 20)

    )

    story.append(

        Paragraph(

            "<b>Cons</b>",

            styles["Heading2"]

        )

    )
    cons = pros_df[

        (pros_df["company_id"] == company)

        &

        (pros_df["type"] == "Con")

        ]

    if len(cons) == 0:

        story.append(

            Paragraph(

                "No Cons Available",

                styles["BodyText"]

            )

        )

    else:

        for _, row in cons.iterrows():
            story.append(

                Paragraph(

                    "• " + str(row["text"]),

                    styles["BodyText"]

                )

            )

            pdf.build(story)

            print(f"{company} PDF Generated")

            skipped_df = pd.DataFrame({

                "company_id": skipped,

                "reason": "Less than 3 years of data"

            })

            skipped_df.to_csv(

                input_path /

                "skipped_tearsheets.csv",

                index=False

            )

            generated = len(companies) - len(skipped)

            print("=" * 60)

            print("DAY 34 SUMMARY")

            print("=" * 60)

            print("Total Companies :", len(companies))

            print("Generated PDFs :", generated)

            print("Skipped :", len(skipped))