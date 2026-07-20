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

report_path = project_root / "reports" / "portfolio"

report_path.mkdir(
    parents=True,
    exist_ok=True
)
cashflow_df = pd.read_excel(
    input_path / "cashflow_intelligence.xlsx"
)

pros_df = pd.read_csv(
    input_path / "pros_cons_generated.csv"
)
print(cashflow_df.head())

print(pros_df.head())

portfolio_df = (

    cashflow_df

    .sort_values("year")

    .groupby("company_id")

    .tail(1)

    .reset_index(drop=True)

)
print("=" * 60)

print("LATEST RECORDS")

print("=" * 60)

print(len(portfolio_df))

print(portfolio_df.head())
styles = getSampleStyleSheet()

pdf = SimpleDocTemplate(

    str(

        report_path /

        "portfolio_summary.pdf"

    )

)

story = []
story.append(

    Paragraph(

        "<b>Portfolio Summary Report</b>",

        styles["Title"]

    )

)

story.append(

    Spacer(1, 20)

)
table_data = [

    [

        "Company",

        "FCF",

        "CFO Quality",

        "Capital Allocation",

        "Distress"

    ]

]

for _, row in portfolio_df.iterrows():

    table_data.append([

        row["company_id"],

        row["free_cash_flow"],

        row["cfo_quality_label"],

        row["capital_allocation_label"],

        row["distress_flag"]

    ])
    table = Table(table_data)
    table.setStyle(

        TableStyle([

            ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),

            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

            ("GRID", (0, 0), (-1, -1), 1, colors.black),

            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),

            ("BOTTOMPADDING", (0, 0), (-1, 0), 10),

            ("FONTSIZE", (0, 0), (-1, -1), 8)

        ])

    )
    story.append(table)

    story.append(

        Spacer(1, 20)

    )
    story.append(

        Paragraph(

            "<b>Sprint 5 Summary</b>",

            styles["Heading2"]

        )

    )

    story.append(

        Paragraph(

            f"Total Companies : {len(portfolio_df)}",

            styles["BodyText"]

        )

    )

    story.append(

        Paragraph(

            "Cash Flow Intelligence Completed",

            styles["BodyText"]

        )

    )

    story.append(

        Paragraph(

            "Pros & Cons Generation Completed",

            styles["BodyText"]

        )

    )

    story.append(

        Paragraph(

            "Batch Tearsheet Generation Completed",

            styles["BodyText"]

        )

    )
    pdf.build(story)
    print("=" * 60)

    print("PORTFOLIO SUMMARY PDF GENERATED")

    print("=" * 60)

    print(report_path / "portfolio_summary.pdf")