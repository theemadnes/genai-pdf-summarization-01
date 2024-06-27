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
  print(f"Setting Gradio server port to {os.getenv('PORT')}")

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

def process_pdf(text_input, pdf_file):
  reader = PdfReader(pdf_file)
  text = ""
  for page in reader.pages:
    text += page.extract_text()

  # Combine the prompt and text
  full_text = text_input + "\n" + text
  print(model.count_tokens(full_text))
  response = model.generate_content(full_text)
  print(response.candidates)
  print(response.prompt_feedback)
  return f"{response.text}"

# Define the interface with file upload and text output
interface = gr.Interface(
  fn=process_pdf,
  inputs=[
    gr.Textbox(label="Enter prompt", lines=1, value="please summarize the entire following text for me"),
    gr.File(label="Upload PDF")],
  outputs="text",
  title=f"PDF Summarization App using {MODEL_VERSION} from zone {zone}",
  description="Upload a PDF file for text summarization using Gemini.",
  flagging_dir="/tmp/flagged" # directory to store flagged files, modified to store in tmp for Cloud Run
)

# Launch the Gradio app
interface.launch(server_name="0.0.0.0") # don't use 127.0.0.1