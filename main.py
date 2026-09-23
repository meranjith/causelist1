import pdfplumber

with pdfplumber.open("input/Mahesh_Chowdhary.pdf") as pdf:

    page = pdf.pages[4]   # PAGE 5

    italic_lines = {}

    for ch in page.chars:

        if "Italic" not in ch["fontname"]:
            continue

        y = round(ch["top"])

        italic_lines.setdefault(y, "")
        italic_lines[y] += ch["text"]

    for y in sorted(italic_lines):
        print(y, "=>", italic_lines[y])
