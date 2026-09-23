import pdfplumber

pdf_file="input/Mahesh_Chowdhary.pdf"

with pdfplumber.open(pdf_file) as pdf:
    for page_no,page in enumerate(pdf.pages,1):

        print(f"\nPAGE {page_no}\n")

        tables=page.extract_tables()

        print("TABLE COUNT:",len(tables))

        for i,t in enumerate(tables,1):
            print("\nTABLE",i)

            for row in t[:10]:
                print(row)
