from langchain_community.llms import VLLMOpenAI

model = "google/gemma-2-2b-it"

llm = VLLMOpenAI(
    openai_api_key="EMPTY",
    openai_api_base="http://localhost:8000/v1",
    model_name=model,
    #model_kwargs={"stop": ["."]},
)
print(llm.invoke("Rome is"))