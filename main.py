import pdfplumber

with pdfplumber.open("input/Mahesh_Chowdhary.pdf") as pdf:

    for page_no, page in enumerate(pdf.pages, start=1):

        tables = page.extract_tables()

        print(f"\nPAGE {page_no}")

        for table in tables:

            for row in table:

                if row and len(row) >= 6:

                    sl = row[0]

                    case = row[1]

                    if sl and case:

                        print("SL:", sl)

                        print("CASE:", case)

                        print("---")
