from langchain_community.embeddings import OllamaEmbeddings

def set_embeddings():
    embeddings=OllamaEmbeddings(model="nomic-embed-text")

    return embeddings