import os
import re
import pdfplumber

from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph
)

INPUT_FOLDER = "input"
OUTPUT_FILE = "Consolidated_Cause_List.pdf"

ADVOCATE_NAMES = [
    "MAHESH CHOWDHARY",
    "A MAHESH CHOWDHARY",
    "NAGARAJA NAIDU",
    "ABHIMANYU",
    "KRISHIKA VAISHNAV",
    "SHAHBAAZ HUSSAIN",
]

styles = getSampleStyleSheet()

styles["BodyText"].leading = 11
styles["BodyText"].spaceBefore = 0
styles["BodyText"].spaceAfter = 0

records = []


def clean(text):
    if text is None:
        return ""

    text = str(text)
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def get_advocate_name(filename):
    return (
        filename.replace(".pdf", "")
        .replace(".PDF", "")
        .replace("_", " ")
        .upper()
        .strip()
    )


def extract_case_number(text):

    text = clean(text)

    patterns = [
        r"WP\s+\d+/\d+",
        r"CRL\.?P\s+\d+/\d+",
        r"WA\s+\d+/\d+",
        r"RSA\s+\d+/\d+",
        r"MFA\s+\d+/\d+",
        r"CCC\s+\d+/\d+",
    ]

    for pattern in patterns:
        m = re.search(pattern, text, re.I)

        if m:
            return m.group(0)

    return text


def strip_advocates(value):

    value = clean(value)

    for adv in ADVOCATE_NAMES:
        value = re.sub(
            re.escape(adv),
            "",
            value,
            flags=re.I
        )

    return clean(value)


def extract_petitioner(text):

    if not text:
        return ""

    text = str(text)

    text = text.replace("PET:", "")

    lines = []

    for line in text.split("\n"):

        line = clean(line)

        if not line:
            continue

        upper_line = line.upper()

        if "FOR P" in upper_line:
            break

        if "FOR R" in upper_line:
            break

        if "ADVOCATE" in upper_line:
            break

        if "AGA" in upper_line:
            break

        if "HCGP" in upper_line:
            break

        if any(
            adv in upper_line
            for adv in ADVOCATE_NAMES
        ):
            break

        lines.append(line)

    result = clean(" ".join(lines))

    return strip_advocates(result)


def extract_respondent(text):

    if not text:
        return ""

    text = str(text)

    text = text.replace("RES:", "")

    lines = []

    stop_words = [
        "AGA",
        "HCGP",
        "FOR R",
        "FOR P",
        "ADVOCATE",
        "NOTICE",
        "V/O",
        "SD",
        "GOVT ADVOCATE",
    ]

    for line in text.split("\n"):

        line = clean(line)

        if not line:
            continue

        upper_line = line.upper()

        if any(
            adv in upper_line
            for adv in ADVOCATE_NAMES
        ):
            break

        stop = False

        for word in stop_words:
            if word in upper_line:
                stop = True
                break

        if stop:
            break

        lines.append(line)

    result = clean(" ".join(lines))

    return strip_advocates(result)


def build_case_name(row):

    pet = row["petitioner"]
    res = row["respondent"]

    if row["bold_side"] == "PET":
        pet = f"<b>{pet}</b>"

    if row["bold_side"] == "RES":
        res = f"<b>{res}</b>"

    return Paragraph(
        f"{pet}<br/>vs<br/>{res}",
        styles["BodyText"]
    )


def process_pdf(pdf_path, advocate):

    print("Processing:", pdf_path)

    current_judge = ""
    current_status = ""
    current_ch = ""
    current_list = ""

    with pdfplumber.open(pdf_path) as pdf:

        for page in pdf.pages:

            tables = page.extract_tables()

            if not tables:
                continue

            for table in tables:

                for row in table:

                    if not row:
                        continue

                    row_text = " ".join(
                        str(x)
                        for x in row
                        if x
                    )

                    upper_text = row_text.upper()

                    if "THE HON" in upper_text:
                        current_judge = clean(row_text)

                    if "COURT HALL NO" in upper_text:

                        ch_match = re.search(
                            r"COURT HALL NO\s*:\s*(\d+)",
                            row_text,
                            re.I
                        )

                        list_match = re.search(
                            r"CAUSE LIST NO\.?\s*(\d+)",
                            row_text,
                            re.I
                        )

                        if ch_match:
                            current_ch = ch_match.group(1)

                        if list_match:
                            current_list = list_match.group(1)

                    status_keywords = [
                        "PRELIMINARY HEARING",
                        "ADMISSION",
                        "ORDERS",
                        "FURTHER HEARING",
                        "HEARING -",
                    ]

                    for keyword in status_keywords:
                        if keyword in upper_text:
                            current_status = clean(row_text)

                    if len(row) < 6:
                        continue

                    sl_no = clean(row[0])

                    if not sl_no.isdigit():
                        continue

                    case_number = extract_case_number(
                        row[1]
                    )

                    pet_col = row[3] if len(row) > 3 else ""
                    res_col = row[5] if len(row) > 5 else ""

                    petitioner = extract_petitioner(
                        pet_col
                    )

                    respondent = extract_respondent(
                        res_col
                    )

                    bold_side = ""

                    pet_text = str(pet_col).upper()
                    res_text = str(res_col).upper()
                    
                    if advocate.upper() in pet_text:
                        bold_side = "PET"
                    
                    elif advocate.upper() in res_text:
                        bold_side = "RES"
                    
                    else:
                        row_text_upper = row_text.upper()
                    
                        if advocate.upper() in row_text_upper:
                    
                            adv_pos = row_text_upper.find(
                                advocate.upper()
                            )
                    
                            res_pos = row_text_upper.find(
                                "RES:"
                            )
                    
                            pet_pos = row_text_upper.find(
                                "PET:"
                            )
                    
                            if res_pos != -1 and adv_pos > res_pos:
                                bold_side = "RES"
                    
                            elif pet_pos != -1 and adv_pos > pet_pos:
                                bold_side = "PET"

                    records.append({
                        "sl_no": sl_no,
                        "case_number": case_number,
                        "petitioner": petitioner,
                        "respondent": respondent,
                        "bold_side": bold_side,
                        "ch": current_ch,
                        "list": current_list,
                        "status": current_status,
                        "judge": current_judge,
                    })


def generate_pdf():

    data = [[
        "SL NO",
        "CASE NUMBER",
        "CASE NAME",
        "CH",
        "LIST",
        "SL NO",
        "STATUS",
        "JUDGES"
    ]]

    for idx, row in enumerate(records, start=1):

        data.append([
            str(idx),

            Paragraph(
                f"<b>{row['case_number']}</b>",
                styles["BodyText"]
            ),

            build_case_name(row),

            row["ch"],
            row["list"],
            row["sl_no"],

            Paragraph(
                row["status"],
                styles["BodyText"]
            ),

            Paragraph(
                row["judge"],
                styles["BodyText"]
            )
        ])

    doc = SimpleDocTemplate(
        OUTPUT_FILE,
        pagesize=landscape(A4),
        leftMargin=10,
        rightMargin=10,
        topMargin=10,
        bottomMargin=10
    )

    table = Table(
        data,
        repeatRows=1,
        colWidths=[
            35,
            90,
            220,
            35,
            35,
            35,
            150,
            170
        ]
    )

    table.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
        ])
    )

    doc.build([table])


def main():

    print("STARTING")

    if not os.path.exists(INPUT_FOLDER):
        print("input folder not found")
        return

    files = [
        f for f in os.listdir(INPUT_FOLDER)
        if f.lower().endswith(".pdf")
    ]

    print("PDF COUNT:", len(files))

    for file in files:

        advocate = get_advocate_name(file)

        path = os.path.join(
            INPUT_FOLDER,
            file
        )

        process_pdf(
            path,
            advocate
        )

    print("RECORDS:", len(records))

    if len(records) == 0:
        print("NO RECORDS FOUND")
        return

    generate_pdf()

    print("PDF CREATED:", OUTPUT_FILE)


if __name__ == "__main__":
    main()
