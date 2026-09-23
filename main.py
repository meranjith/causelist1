import pdfplumber

with pdfplumber.open("input/Mahesh_Chowdhary.pdf") as pdf:

    page = pdf.pages[0]

    fonts = set()

    for ch in page.chars:
        fonts.add(ch["fontname"])

    print(fonts)
