from langchain_community.document_loaders import PDFPlumberLoader
from collections import defaultdict

from langchain_classic.schema import Document

def create_docs(final_tables,extracted_texts):
    documents=[]
    for page_num,text in extracted_texts.items():
        documents.append(Document(metadata={'page':page_num},page_content=text))

    
    final_table_markdown=defaultdict(list)
    for page_num,tables in final_tables.items():
        for table in tables:
            final_table_markdown[page_num].append(table.to_markdown())


    for document in documents:
        document.metadata['table_markdown']=final_table_markdown[document.metadata['page']]


    final_table_row_cols=defaultdict(list)
    for page_num,tables in final_tables.items():
        for table in tables:
            table_to_text=table.to_string().replace("   ",'')
            final_table_row_cols[page_num].append(table_to_text)


    for document in documents:
        document.metadata['page_text']=document.page_content
        document.page_content=document.page_content+" "+' '.join(final_table_row_cols[document.metadata['page']])

    clean_documents=[]
    for document in documents:
        if len(document.page_content.strip().split(' '))>=2:
            clean_documents.append(document)


    return clean_documents