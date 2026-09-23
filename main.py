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

records = []


def clean(text):
    if not text:
        return ""

    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def normalize_advocate(filename):

    return (
        os.path.splitext(filename)[0]
        .replace("_", " ")
        .upper()
        .strip()
    )


def extract_case_no(text):

    if not text:
        return ""

    m = re.search(
        r'(WP|CRL\.?P|WA|WP\(C\)|RSA|MFA|CCC)\s+\d+/\d+',
        text,
        re.I
    )

    return m.group(0) if m else clean(text.split("\n")[0])


def extract_party(text, prefix):

    if not text:
        return ""

    m = re.search(
        rf'{prefix}\s*:\s*(.*)',
        text,
        re.I | re.S
    )
