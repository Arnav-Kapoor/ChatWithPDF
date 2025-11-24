from langchain_weaviate import WeaviateVectorStore

def vectors_in_db(client,embeddings,documents):
    db = WeaviateVectorStore.from_documents(documents, embeddings, client=client,index_name="ChatWithPDF")

    return db

def fetch_existing_vectors(client,embeddings):
    db=WeaviateVectorStore(client=client,index_name="ChatWithPDF",text_key="text",embedding=embeddings)

    return db