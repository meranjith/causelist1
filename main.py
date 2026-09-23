import pdfplumber

with pdfplumber.open("Mahesh_Chowdhary.pdf") as pdf:
    for page in pdf.pages:
        tables = page.extract_tables()

        for table in tables:
            for row in table:
                if row and any("CRL.P 12024/2026" in str(x) for x in row if x):
                    print(row)

                if row and any("WP 16402/2026" in str(x) for x in row if x):
                    print(row)
