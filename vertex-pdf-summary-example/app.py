from dotenv import load_dotenv
from pypdf import PdfReader
import vertexai
from vertexai.language_models import TextGenerationModel
import os

load_dotenv()

vertexai.init(project=os.getenv("PROJECT_ID"), location=os.getenv("REGION"))

parameters = {
    "temperature": 0,
    "max_output_tokens": 256,
    "top_p": 0.95,
    "top_k": 40,
}

reader = PdfReader("../pdf-samples/romeo_and_juliet.pdf")
text = ""
for page in reader.pages:
    text += page.extract_text()
#print(text)

prompt = "Provide a summary with about two sentences for the following article: " + text + " Summary:" 

model = TextGenerationModel.from_pretrained("text-bison@002")
response = model.predict(
    prompt,
    **parameters,
)
print(f"Response from Model: {response.text}")