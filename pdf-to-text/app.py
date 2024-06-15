from pypdf import PdfReader

reader = PdfReader("../pdf-samples/drylab.pdf")
#number_of_pages = len(reader.pages)
text = ""
for page in reader.pages:
    text += page.extract_text()
print(text)