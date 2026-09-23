import pdfplumber

with pdfplumber.open("input/Mahesh_Chowdhary.pdf") as pdf:

    page = pdf.pages[0]

    count = 0

    for ch in page.chars:

        if "Italic" in ch["fontname"]:

            print(ch["text"], ch["fontname"])

            count += 1

            if count > 200:
                break
