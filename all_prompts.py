from langchain_classic.prompts import PromptTemplate

def create_query_enhancer_prompt():
    query_enhance_template="""You are a highly reliable assistant specialized in optimizing user queries for Retrieval-Augmented Generation (RAG) systems.
    Your goal is to analyze the user's query and rewrite it so that the RAG system retrieves the most contextually relevant and high-quality documents.

    Rewrite the query to be clear, specific, unambiguous, and retrieval-friendly while preserving the original intent.
    Return only the optimized query.

    User query: {query}
    """
    query_enhance_prompt=PromptTemplate(template=query_enhance_template,input_variables=['query'])

    return query_enhance_prompt



def create_chat_prompt():
    template = """
    You are a highly reliable question-answering assistant specialized in analyzing PDF documents.
    You may receive both text and tabular data or chat history as context.

    Your job is to carefully analyze the provided content and respond **only** using the given context, tables and chat history.

    Follow these rules:
    1. **Answer length** - Adjust naturally based on the question:
    - If the query asks for a list, summary, or table of contents, give a clear, concise structured answer.
    - If the query asks for explanation, comparison, or interpretation, respond in detail.
    2. **Table handling** - If a table is provided, consider it part of the context. Never state that no table exists.
    3. **Truthfulness** - Do not guess or fabricate. If the answer cannot be found in the provided data, convey that you dont know.
    4. **Clarity** - Avoid redundant introductions (e.g., "Based on the context..."). Go straight to the answer and explain it nicely instead of just printing the context or table directly.
    5. **Politeness** - If the user's query is unclear or incomplete, ask for clarification politely.

    DO NOT MENTION ABOUT CONTEXT OR TABLE OR ANYTHING JUST UNDERSTAND WHAT IT SAYS AND EXPLAIN IT TO SATISFY THE USER QUERY.

    Context:
    {context}

    Tables:
    {tables_text}

    Chat History:
    {chat_history}

    User Query:
    {query}
    """


    prompt=PromptTemplate(input_variables=['context','tables_text','query','chat_history'],template=template)

    return prompt


def create_summarizer_prompt():
    summarizer_template="""You are an assistant highly skilled at summarizing conversations.
    You will be given a user query and an AI response.
    Your task is to produce a concise, accurate, and information-preserving summary of the interaction.

    The summary must:

    Follow the format: "user asked: ..., ai replied: ..."

    Be as short as possible while keeping all essential information.

    Contain no extra commentary, no explanations, no prefixes, and no added details.

    Not omit or distort any information.

    Never include anything beyond the summary.

    User query: {query}
    AI response: {response}
    """

    summarizer_prompt=PromptTemplate(input_variables=['query','response'],template=summarizer_template)

    return summarizer_prompt

