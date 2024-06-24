import gradio as gr
from pypdf import PdfReader
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Configure the API key (replace with your actual key)
genai.configure(api_key=os.getenv("API_KEY"))

model = genai.GenerativeModel('gemini-1.5-flash')

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
  title="PDF Summarization App using Gemini Flash",
  description="Upload a PDF file for text summarization using Gemini Flash."
)

# Launch the Gradio app
interface.launch()