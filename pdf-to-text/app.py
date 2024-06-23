from pypdf import PdfReader

reader = PdfReader("../pdf-samples/romeo_and_juliet.pdf")
#number_of_pages = len(reader.pages)
text = ""
for page in reader.pages:
    text += page.extract_text()
print(text)