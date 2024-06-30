from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader
from langchain.prompts import PromptTemplate
from langchain.chains import MapReduceDocumentsChain, ReduceDocumentsChain, LLMChain
from langchain_community.llms import VLLMOpenAI

llm_url="127.0.0.1:8000/generate"

llm = VLLMOpenAI(
openai_api_key="EMPTY",
openai_api_base=f"{llm_url}",
#model_name=f"{llm_name}",
model_kwargs={"stop": ["."]},
)

reader = PdfReader("../pdf-samples/aesops_fables.pdf")
text = ""
for page in reader.pages:
    text += page.extract_text()

# Split the text into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_text(text)

# Map
map_template = """The following is a set of documents
{docs}
Based on this list of docs, please identify the main themes 
Helpful Answer:"""
map_prompt = PromptTemplate.from_template(map_template)
map_chain = LLMChain(llm=llm, prompt=map_prompt)

# Reduce
reduce_template = """The following is set of summaries:
{docs}
Take these and distill it into a final, consolidated summary of the main themes. 
Helpful Answer:"""
reduce_prompt = PromptTemplate.from_template(reduce_template)
reduce_chain = LLMChain(llm=llm, prompt=reduce_prompt)
# Combine documents by mapping a chain over them, then combining results
map_reduce_chain = MapReduceDocumentsChain(
    llm_chain=map_chain,
    reduce_documents_chain=reduce_documents_chain,
    document_variable_name="docs",
    return_intermediate_steps=False,
)

# Set the prompt for summarization
prompt = "Please summarize the following text for me:"

# Combine the prompt and text
#full_text = prompt + "\n" + text

#print(full_text)