import pymupdf

pdf_path = "Documents/Git_Handbook_Cleaned.pdf"

pdf = pymupdf.open(pdf_path)

print("Number of pages:", pdf.page_count)

text = ""

for page in pdf:
    page_text = page.get_text()

    if page_text:
        text += page_text + "\n"

total = len(text)
whitespace = sum(char.isspace() for char in text)
non_whitespace = total - whitespace

print("Total characters      :", total)
print("Whitespace characters :", whitespace)
print("Non-whitespace        :", non_whitespace)
print("Whitespace percentage :", round((whitespace / total) * 100, 2), "%")