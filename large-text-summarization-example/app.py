#from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader
#from langchain.prompts import PromptTemplate
from langchain.chains import (
    StuffDocumentsChain,
    LLMChain,
    ReduceDocumentsChain,
    MapReduceDocumentsChain,
)
from langchain_community.llms import VLLMOpenAI
from langchain_core.prompts import PromptTemplate
#from langchain_community.llms import VLLM
#from langchain.llms import VLLM

llm_url="127.0.0.1:8000/generate"

'''
llm = VLLMOpenAI(
openai_api_key="EMPTY",
openai_api_base=f"{llm_url}",
#model_name=f"{llm_name}",
model_kwargs={"stop": ["."]},
)'''

llm = VLLMOpenAI(
    openai_api_key="EMPTY",
    openai_api_base="http://localhost:8000/v1/completions",
    model_name="google/gemma-2b",
    model_kwargs={"stop": ["."]},
)

# Define your large text (replace with actual text or loading function)
large_text = """
This is a very long piece of text that goes on for multiple paragraphs 
and contains a lot of information. It's too big for the LLM to handle at once.

Here are some more details within this large text to showcase its volume. 
We can include various topics or specific points to ensure the LLM 
captures the essence of the content during summarization.

For better understanding, let's add some contrasting viewpoints or arguments 
to enrich the information density. This will allow the summary to 
highlight the key points and opposing ideas.

Finally, we can conclude with a brief reiteration of the main themes 
discussed throughout this extensive text. 
"""

# Define the chunk size for splitting the text
chunk_size = 500

document_prompt = PromptTemplate(
    input_variables=["page_content"],
     template="{page_content}"
)
document_variable_name = "context"

prompt = PromptTemplate.from_template(
    "Summarize this content: {context}"
)

print(llm)

llm_chain = LLMChain(llm=llm, prompt=prompt)

# We now define how to combine these summaries
reduce_prompt = PromptTemplate.from_template(
    "Combine these summaries: {context}"
)

reduce_llm_chain = LLMChain(llm=llm, prompt=reduce_prompt)
combine_documents_chain = StuffDocumentsChain(
    llm_chain=reduce_llm_chain,
    document_prompt=document_prompt,
    document_variable_name=document_variable_name
)
reduce_documents_chain = ReduceDocumentsChain(
    combine_documents_chain=combine_documents_chain,
)
chain = MapReduceDocumentsChain(
    llm_chain=llm_chain,
    reduce_documents_chain=reduce_documents_chain,
)

chain.run(documents=[large_text])

'''
# Create a MapReduceDocumentsChain instance
summarizer = MapReduceDocumentsChain(
    llm_chain=LLMChain(llm)
)

# Summarize the large text
summary = summarizer.run(documents=[large_text])

# Print the resulting summary
print(f"Summary of the large text: \n {summary}")

'''