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
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)  # Adjust chunk size as needed
chunks = text_splitter.split_text(text)

# Map chain to summarize each chunk
map_template = """Please summarize the following text:
{text}
Helpful Answer:"""
map_prompt = PromptTemplate.from_template(map_template)
map_chain = LLMChain(llm=llm, prompt=map_prompt)

# Reduce chain to combine summaries
reduce_template = """The following are summaries of different sections:
{text}
Please combine these summaries into a single, coherent summary of the entire text.
Helpful Answer:"""
reduce_prompt = PromptTemplate.from_template(reduce_template)
reduce_chain = LLMChain(llm=llm, prompt=reduce_prompt)

# MapReduce chain to process the chunks
map_reduce_chain = MapReduceDocumentsChain(
    llm_chain=map_chain,
    reduce_documents_chain=ReduceDocumentsChain(llm_chain=reduce_chain),
    document_variable_name="text",
    return_intermediate_steps=False,
)

# Summarize the text
summary = map_reduce_chain.run(chunks)

print(summary)