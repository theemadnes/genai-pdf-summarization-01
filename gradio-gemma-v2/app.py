from langchain_community.llms import VLLM

llm = VLLM(
    model="google/gemma-2b",
    trust_remote_code=True,
    
)