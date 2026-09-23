import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

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
            "STATUS",
            "JUDGES"
        ],
        [
            "1",
            "WP 6554/2026",
            "K S SATHISH AND OTHERS\nvs\nSTATE OF KARNATAKA AND OTHERS",
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
        colWidths=[40, 80, 250, 35, 35, 35, 180, 220]
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
