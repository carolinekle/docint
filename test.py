import pymupdf
doc = pymupdf.open("test_data/mueller_report.pdf")
for i in range(len(doc)):
    if len(doc[i].get_images()) >= 2:
        print(i + 1, len(doc[i].get_images()))