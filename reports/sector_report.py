import os

pdfs = [
    f for f in os.listdir("reports/tearsheets")
    if f.endswith(".pdf")
]

print("Generated:", len(pdfs))
