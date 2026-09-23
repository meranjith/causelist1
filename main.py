import pdfplumber

with pdfplumber.open("input/Mahesh_Chowdhary.pdf") as pdf:

    for page_no, page in enumerate(pdf.pages, start=1):

        italic_text = ""

        for ch in page.chars:

            if "Italic" in ch["fontname"]:
                italic_text += ch["text"]

        print("\n")
        print("=" * 80)
        print("PAGE", page_no)
        print("=" * 80)
        print(italic_text)
