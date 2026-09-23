import pdfplumber

pdf_file = "input/Mahesh_Chowdhary.pdf"

with pdfplumber.open(pdf_file) as pdf:
    for i, page in enumerate(pdf.pages):
        print("=" * 100)
        print(f"PAGE {i+1}")
        print("=" * 100)

        text = page.extract_text()

        if text:
            print(text)
