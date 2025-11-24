from all_prompts import create_query_enhancer_prompt

def get_context(db,llm,query:str,k=10,filter_thresh=0.64):
    query_enhance_prompt=create_query_enhancer_prompt()
    
    formatted_enhanced_prompt=query_enhance_prompt.format(query=query)
    query=llm.invoke(formatted_enhanced_prompt)
    print(query)
    docs=db.similarity_search_with_relevance_scores(query,k=k)
    docs=sorted(filter(lambda x:x[1]>filter_thresh,docs),key=lambda k:k[1],reverse=True)
    # print(len(docs))
    # print(docs)
    context=""
    tables=""
    for doc in docs:
        print(doc[0].metadata['page'])
        context+=doc[0].metadata['page_text']
        tables+="\n".join(doc[0].metadata["table_markdown"])

    return context,tables
