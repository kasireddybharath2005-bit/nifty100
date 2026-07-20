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


# ----------------------------------------------------
# PROJECT PATHS
# ----------------------------------------------------

project_root = Path(__file__).resolve().parent.parent

input_path = project_root / "output"

report_path = project_root / "reports" / "pdf"

report_path.mkdir(parents=True, exist_ok=True)


# ----------------------------------------------------
# LOAD FILES
# ----------------------------------------------------

cashflow_df = pd.read_excel(
    input_path / "cashflow_intelligence.xlsx"
)

pros_df = pd.read_csv(
    input_path / "pros_cons_generated.csv"
)


# ----------------------------------------------------
# SELECT COMPANY
# ----------------------------------------------------

company = "TCS"

company_cashflow = cashflow_df[
    cashflow_df["company_id"] == company
]

company_pros = pros_df[
    pros_df["company_id"] == company
]


if company_cashflow.empty:
    raise ValueError(f"No cashflow data found for {company}")

latest = company_cashflow.iloc[-1]


# ----------------------------------------------------
# PDF
# ----------------------------------------------------

styles = getSampleStyleSheet()

pdf_file = report_path / f"{company}_tearsheet.pdf"

doc = SimpleDocTemplate(str(pdf_file))

story = []


# ----------------------------------------------------
# TITLE
# ----------------------------------------------------

story.append(
    Paragraph(
        f"<b>{company} Financial Tearsheet</b>",
        styles["Title"]
    )
)

story.append(Spacer(1, 20))


# ----------------------------------------------------
# KPI TABLE
# ----------------------------------------------------

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

        ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),

        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

        ("GRID", (0, 0), (-1, -1), 1, colors.black),

        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),

        ("BOTTOMPADDING", (0, 0), (-1, 0), 10)

    ])

)

story.append(table)

story.append(Spacer(1, 20))


# ----------------------------------------------------
# PROS
# ----------------------------------------------------

story.append(
    Paragraph(
        "<b>Pros</b>",
        styles["Heading2"]
    )
)

pros = company_pros[
    company_pros["type"] == "Pro"
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


story.append(Spacer(1, 20))


# ----------------------------------------------------
# CONS
# ----------------------------------------------------

story.append(

    Paragraph(

        "<b>Cons</b>",

        styles["Heading2"]

    )

)

cons = company_pros[
    company_pros["type"] == "Con"
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


# ----------------------------------------------------
# BUILD PDF
# ----------------------------------------------------

doc.build(story)

print("=" * 60)
print("PDF GENERATED SUCCESSFULLY")
print("=" * 60)
print(pdf_file)