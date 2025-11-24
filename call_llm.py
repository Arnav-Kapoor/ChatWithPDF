from langchain_ollama import OllamaLLM

def set_llm():
    llm=OllamaLLM(model='llama3')

    return llm

def invoke_llm(llm,prompt):
    response=llm.invoke(prompt)

    return response