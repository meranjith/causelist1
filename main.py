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
    Paragraph,
)

INPUT_FOLDER = "input"
OUTPUT_FILE = "Consolidated_Cause_List.pdf"

styles = getSampleStyleSheet()

styles["BodyText"].leading = 11
styles["BodyText"].spaceBefore = 0
styles["BodyText"].spaceAfter = 0

records = []


def clean(text):
    if not text:
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
        r'WP\s+\d+/\d+',
        r'CRL\.?P\s+\d+/\d+',
        r'WA\s+\d+/\d+',
        r'RSA\s+\d+/\d+',
        r'MFA\s+\d+/\d+',
        r'CCC\s+\d+/\d+',
    ]

    for pattern in patterns:
        m = re.search(pattern, text, re.I)

        if m:
            return m.group(0)

    return text


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

        stop_words = [
            " FOR P",
            " FOR R",
            "ADVOCATE",
            "AGA",
            "HCGP",
            "SD",
            "V/O",
        ]

        if any(word in upper_
