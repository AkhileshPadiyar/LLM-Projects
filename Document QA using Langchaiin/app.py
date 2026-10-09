import streamlit as st
from rag import (load_file, split_documents, create_embeddings, create_vector_store, load_vector_store, create_llm)
from dotenv import load_dotenv
from llm import generate_answer
import os

load_dotenv()

st.title("Document QA")

question = st.text_input("Enter the question you want to ask")

pdf_path = "C:\\Users\\ACER\\Downloads\\alice-s-adventures-in-wonderland-lewis-carroll-6330.pdf"

if not os.path.exists('./chroma_db'):
    doc = load_file(pdf_path)
    chunks = split_documents(doc)
    embeddings = create_embeddings()

    vector_store = create_vector_store(chunks, embeddings)
    st.success("Vector database created")

embeddings = create_embeddings()
vector_store = load_vector_store(embeddings)
st.write(vector_store)

if st.button("Generate answer"):
    with st.spinner("Generating answer ...."):
        embeddings = create_embeddings()
        vector_store = load_vector_store(embeddings)

        answer = generate_answer(vector_store, question)

        st.write(answer)






