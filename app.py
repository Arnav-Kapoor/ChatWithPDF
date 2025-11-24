import streamlit as st
from main import main
import os

st.title("📄 Document question answering")

st.write(
    "Upload a pdf document below and ask a question about it"
    )

uploaded_file = st.file_uploader(
        "Upload a pdf document", type=("pdf")
    )

question = st.text_area(
        "Now ask a question about the document!",
        placeholder="Can you give me a short summary?",
        disabled=not uploaded_file,
    )

if uploaded_file and question:

        # Process the uploaded file and question.
        os.makedirs("data",exist_ok=True)
        save_path=f"data/{uploaded_file.name}.pdf"
        with open(save_path,"w",encoding="cp1252") as file:
                file.write(uploaded_file.read())

        response=main(save_path,question)

        st.write_stream(response)
