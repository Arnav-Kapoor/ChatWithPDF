from get_table_transformer import table_transformer
from table_text_extraction import read_tables_text
from process_tables import preprocessing
from create_documents_for_vectordb import create_docs
from setup_embeddings import set_embeddings
from vectordb_connection import set_connection
from create_vectors import vectors_in_db
from call_llm import set_llm,invoke_llm
from get_context import get_context
from all_prompts import create_chat_prompt,create_summarizer_prompt
import pdfplumber


def main(pdf_path,query):
    model,image_processor=table_transformer()
    embeddings=set_embeddings()

    # pdf_path="nestle_report.pdf"
    pdf=pdfplumber.open(pdf_path)
    chat_history=[]

    pdfplumber_tables, camelot_tables, tabula_tables, extracted_texts=read_tables_text(pdf_path,model,image_processor,pdf)
    print("tables fetched")

    final_tables=preprocessing(pdfplumber_tables,camelot_tables,tabula_tables)

    clean_documents=create_docs(final_tables,extracted_texts)
    print("documents ready")

    client=set_connection()

    db=vectors_in_db(client,embeddings,clean_documents)
    print("db is set")

    vector_created=True

    llm=set_llm()

    # query="What is the document about"
    context,tables=get_context(db,llm,query)

    prompt=create_chat_prompt()
    prompt=prompt.format(context=context,tables_text=tables,query=query,chat_history=chat_history)

    response=invoke_llm(llm,prompt)
    print(response)

    summary_prompt=create_summarizer_prompt()
    summary_prompt=summary_prompt.format(query=query,response=response)

    summary=invoke_llm(llm,summary_prompt)
    print(summary)

    chat_history.append(summary)

    return response

if __name__=="__main__":
    # main()
    pass








