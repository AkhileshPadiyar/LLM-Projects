import streamlit as st
import os
from config import connect
from llm import generate_answer, generate_rag_answer
from dotenv import load_dotenv
from document import extract_text
from chunker import create_chunks
from embeddings.embedder import generate_embedding, generate_query_embeddings
import hashlib
from vector_db.chroma_db import store_embeddings, search, document_exists, get_documents, delete_document

load_dotenv()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "document_ids" not in st.session_state:
    st.session_state.document_ids= []
if "saved_documents" not in st.session_state:
    st.session_state.saved_documents = 1


st.title("AI Knowledge Assistant")

client = connect()

model_name = st.selectbox("Enter the model name", [os.getenv("MODEL_NAME"), "mistral:7b", "mistral:7b-instruct"])

system_prompt = st.text_input("Enter the system prompt", placeholder= "Your are a 4th class child....")

st.subheader("Uploaded Documents")
documents = get_documents()

for document_id, filename in documents.items():
    st.write(filename)
    if st.button("Delete File", key = document_id):
        delete_document(document_id)
        st.success("Document Deleted Successfully")


txt_file = st.file_uploader("Upload a file", type = ['.txt'])


if txt_file:
    try:
        text,filename = extract_text(txt_file)
        document_id = hashlib.sha256(text.encode('utf-8')).hexdigest()
        if not document_exists(document_id):
            chunks = create_chunks(text, 500, 50)
            st.write(f"Total Chunks: {len(chunks)}")
            embeddings = generate_embedding(chunks)
            st.write(f"Embeddings shape : {embeddings.shape}")
            store_embeddings(document_id, chunks, embeddings, filename)
            st.success("Document Stored successfully")
        else:
            st.warning("File already uploaded")


    except Exception as e:
        st.error(f"Error loading the file: {e}")

if st.session_state.saved_documents > 0:
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    question = st.text_area("Enter the question to ask: ", placeholder="What is machine learning")

    if st.button("Generate Answer"):
        if question.strip():
            try:
                with st.spinner("Generating answer..."):
                    query_embeddings = generate_query_embeddings(question)
                    result = search(query_embeddings, 3)
                    documents = '\n'.join(result['documents'][0])
                    metadatas = result['metadatas'][0]
                    chat_history = st.session_state.chat_history
                    llm_response = generate_rag_answer(documents, question, model_name, system_prompt, chat_history)
                    st.write(llm_response)
                    st.write("Sources: ")
                    for i, data in enumerate(metadatas):
                        st.write(f'{i + 1}. {data["filename"]} -- Chunk : {data["chunk"]} ')

                    st.session_state.chat_history.append({"role": "user", "content": question})
                    st.session_state.chat_history.append({"role": "assistant", "content": llm_response})

            except Exception as e:
                st.error(f"Failed to get results {e}")

        else:
            st.warning("Enter the question to ask first")


