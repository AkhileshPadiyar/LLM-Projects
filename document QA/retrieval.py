import streamlit as st
from vector_store import search
from rag import generate_answer


def retrieve_chunks(question, model):
    status_container = st.status("Generating answer...")
    status_container.write("Searching the question in the context.....")
    query_embeddings = model.encode(question)

    relevant_chunks = search(query_embeddings)
    status_container.write("Generating the relevant answer...")

    result = generate_answer(relevant_chunks, question)
    status_container.update(label="✅ Answer generated successfully!", state="complete", expanded=False)

    st.write("###Answer")
    st.write(result)