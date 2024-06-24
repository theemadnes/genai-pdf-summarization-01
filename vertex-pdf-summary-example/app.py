from dotenv import load_dotenv
from pypdf import PdfReader
import google.generativeai as genai
import os

load_dotenv()

# Configure the API key (replace with your actual key)
genai.configure(api_key=os.getenv("API_KEY"))

reader = PdfReader("../pdf-samples/romeo_and_juliet.pdf")
text = ""
for page in reader.pages:
    text += page.extract_text()

# Set the prompt for summarization
prompt = "Please summarize the following text for me:"

# Combine the prompt and text
full_text = prompt + "\n" + text

# Define the model to use (change for different models)
project_id = os.getenv("PROJECT_ID")  # Replace with your project ID
location = os.getenv("REGION")  # Specify the location
publisher = "google"
model = "gemini-1.5-flash-001"  # Flash summarization model

model = genai.GenerativeModel('gemini-1.5-flash')

'''
# Create the request object
request = genai.TextGenerationRequest(
    model=f"projects/{project_id}/locations/{location}/publishers/{publisher}/models/{model}",
    content=full_text,
)

# Send the request and get the response
try:
  response = genai.TextGenerationServiceClient().generate_content(request=request)
  # Access the generated summary
  summary = response.generated_texts[0].text
  print(f"Summary: {summary}")
except Exception as e:
  print(f"An error occurred: {e}")
'''

response = model.generate_content(full_text)
print(response.text)