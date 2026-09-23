import pdfplumber

with pdfplumber.open("input/Mahesh_Chowdhary.pdf") as pdf:
    page = pdf.pages[0]

    italic_text = ""

    for ch in page.chars:
        if "Italic" in ch["fontname"]:
            italic_text += ch["text"]

    print(italic_text)
