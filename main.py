from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
)

OUTPUT_FILE = "Consolidated_Cause_List.pdf"

styles = getSampleStyleSheet()

styles["BodyText"].leading = 11
styles["BodyText"].spaceBefore = 0
styles["BodyText"].spaceAfter = 0


def main():

    data = [
        [
            "SL NO",
            "CASE NUMBER",
            "CASE NAME",
            "CH",
            "LIST",
            "SL NO",
            "STATUS",
            "JUDGES",
        ],
        [
            "1",
            Paragraph("<b>WP 6554/2026</b>", styles["BodyText"]),
            Paragraph(
                "<b>K S SATHISH AND OTHERS</b><br/>"
                "vs<br/>"
                "STATE OF KARNATAKA AND OTHERS",
                styles["BodyText"],
            ),
            "8",
            "1",
            "17",
            Paragraph(
                "PRELIMINARY HEARING - B GROUP",
                styles["BodyText"],
            ),
            Paragraph(
                "THE HON'BLE JUSTICE S SUNIL DUTT YADAV",
                styles["BodyText"],
            ),
        ],
    ]

    doc = SimpleDocTemplate(
        OUTPUT_FILE,
        pagesize=landscape(A4),
        leftMargin=10,
        rightMargin=10,
        topMargin=10,
        bottomMargin=10,
    )

    table = Table(
        data,
        colWidths=[35, 90, 220, 35, 35, 35, 150, 170],
        repeatRows=1,
    )

    table.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )

    doc.build([table])

    print("PDF CREATED:", OUTPUT_FILE)


if __name__ == "__main__":
    main()
``
