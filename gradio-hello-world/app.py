import gradio as gr
from pypdf import PdfReader
import google.generativeai as genai
from dotenv import load_dotenv
import os
import requests
from requests.adapters import HTTPAdapter
import urllib3
from urllib3 import Retry

load_dotenv()

# set model version
MODEL_VERSION = 'gemini-1.5-flash'

# check to see if $PORT is set, and if so, set Gradio env var to use it
if "PORT" in os.environ:
  os.environ["GRADIO_SERVER_PORT"] = os.getenv(
    "PORT"
  )

# gather region information
METADATA_URL = 'http://metadata.google.internal/computeMetadata/v1/'
METADATA_HEADERS = {'Metadata-Flavor': 'Google'}

session = requests.Session()
adapter = HTTPAdapter(max_retries=Retry(total=3, backoff_factor=1, allowed_methods=['GET'])) #, status_forcelist=[429, 500, 502, 503, 504]))
session.mount("http://", adapter)
session.mount("https://", adapter)

zone = "unknown" # default value

try:
  # grab info from GCE metadata
  r = session.get(METADATA_URL + '?recursive=true', headers=METADATA_HEADERS)
  if r.ok:
    print("Successfully accessed GCE metadata endpoint.")
    zone = r.json()['instance']['zone'].split('/')[-1]
except:
  print("Unable to access GCE metadata endpoint.")

# Configure the API key (replace with your actual key)
genai.configure(api_key=os.getenv("API_KEY"))

model = genai.GenerativeModel(MODEL_VERSION)

def process_pdf(pdf_file):
  reader = PdfReader(pdf_file)
  text = ""
  for page in reader.pages:
    text += page.extract_text()

  # Set the prompt for summarization
  prompt = "Please summarize the following text for me:"

  # Combine the prompt and text
  full_text = prompt + "\n" + text
  response = model.generate_content(full_text)
  #filename = pdf_file.name
  return f"{response.text}"

# Define the interface with file upload and text output
interface = gr.Interface(
  fn=process_pdf,
  inputs=gr.File(label="Upload PDF"),
  outputs="text",
  title=f"PDF Summarization App using {MODEL_VERSION} from zone {zone}",
  description="Upload a PDF file for text summarization using Gemini."
)

# Launch the Gradio app
interface.launch()