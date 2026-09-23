import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet

styles = getSampleStyleSheet()

OUTPUT_FILE = "Consolidated_Cause_List.pdf"

def main():

    print("STARTING...")

    data = [
        [
            "SL NO",
            "CASE NUMBER",
            "CASE NAME",
            "CH",
            "LIST",
            "SL NO",
            Paragraph(status, styles["BodyText"]),
            Paragraph(judge, styles["BodyText"])
        ],
        [
            "1",
            "WP 6554/2026",
            Paragraph(
    "K S SATHISH AND OTHERS<br/>vs<br/>STATE OF KARNATAKA AND OTHERS",
    styles["BodyText"]
),
            "8",
            "1",
            "17",
            "PRELIMINARY HEARING - B GROUP",
            "THE HONBLE JUSTICE S SUNIL DUTT YADAV"
        ]
    ]

    doc = SimpleDocTemplate(
        OUTPUT_FILE,
        pagesize=landscape(A4)
    )

    table = Table(
    data,
    colWidths=[
        30,   # SL NO
        80,   # CASE NUMBER
        220,  # CASE NAME
        30,   # CH
        30,   # LIST
        30,   # SL NO
        150,  # STATUS
        160   # JUDGES
    ]
)

    table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ]))

    doc.build([table])

    print("PDF CREATED:", OUTPUT_FILE)

if __name__ == "__main__":
    main()
